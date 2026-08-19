"""The HTTP API (spec section 11). POST /rules/generate arrives with
the generation pipeline phase; everything else is here.

Recorded history is immutable: the only write this API performs on a
stored run is the PATCH setting user_behavior and user_flagged
(REQ-11.3).
"""

import json
import random

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel

from asr.config import settings
from asr.contract.child import RuleCrashed, run_in_child
from asr.engine.classify import classify
from asr.engine.declaration import Declaration
from asr.storage import db
from asr.storage.reconstruct import reconstruct_range
from asr.version import engine_version

router = APIRouter()

BEHAVIOR_NAMES = ("settles", "repeats", "noisy", "structured", "unclassified")
MOST_TICKS_PER_GRID_REQUEST = 250


def get_db(request: Request):
    conn = db.connect(request.app.state.database_path)
    try:
        yield conn
    finally:
        conn.close()


def _rule_summary(row) -> dict:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "description": row["description"],
        "status": row["status"],
        "failed_check": row["failed_check"],
        "mode": row["mode"],
        "kinds": row["kinds"],
        "neighbors": row["neighbors"],
        "reach": row["reach"],
        "uses": json.loads(row["uses_json"]),
        "modifiers": json.loads(row["modifiers_json"]),
        "concepts": json.loads(row["concepts_json"]),
        "requested_shape": row["requested_shape"],
        "observed_shape": row["observed_shape"],
        "suggested_display": json.loads(row["suggested_display_json"]),
    }


def _run_summary(row) -> dict:
    return {
        "id": row["id"],
        "rule_id": row["rule_id"],
        "created_at": row["created_at"],
        "start_seed": row["start_seed"],
        "width": row["width"],
        "height": row["height"],
        "max_ticks": row["max_ticks"],
        "ticks_run": row["ticks_run"],
        "is_canonical": bool(row["is_canonical"]),
        "stopped_because": row["stopped_because"],
        "loop_length": row["loop_length"],
        "pattern_settled_at": row["pattern_settled_at"],
        "guessed_behavior": row["guessed_behavior"],
        "guess_confidence": row["guess_confidence"],
        "user_behavior": row["user_behavior"],
        "user_flagged": bool(row["user_flagged"]),
    }


@router.get("/rules")
def list_rules(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    status: str | None = None,
    behavior: str | None = None,
    concept: str | None = None,
    flagged: bool | None = None,
    conn=Depends(get_db),
):
    clauses, params = [], []
    if status:
        clauses.append("rules.status = ?")
        params.append(status)
    if concept:
        clauses.append("rules.concepts_json LIKE ?")
        params.append(f'%"{concept}"%')
    if behavior:
        clauses.append("COALESCE(canon.user_behavior, canon.guessed_behavior) = ?")
        params.append(behavior)
    if flagged:
        clauses.append(
            "EXISTS (SELECT 1 FROM runs f WHERE f.rule_id = rules.id AND f.user_flagged = 1)"
        )
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    base = f"""FROM rules
               LEFT JOIN runs canon
                 ON canon.rule_id = rules.id AND canon.is_canonical = 1
               {where}"""
    total = conn.execute(f"SELECT COUNT(*) AS n {base}", params).fetchone()["n"]
    rows = conn.execute(
        f"""SELECT rules.*, canon.id AS canonical_run_id,
                   canon.stopped_because AS run_stopped_because,
                   canon.guessed_behavior, canon.guess_confidence,
                   canon.user_behavior, canon.user_flagged AS run_user_flagged
            {base}
            ORDER BY rules.id DESC LIMIT ? OFFSET ?""",
        params + [page_size, (page - 1) * page_size],
    ).fetchall()
    rules = []
    for row in rows:
        summary = _rule_summary(row)
        summary["canonical_run"] = (
            {
                "id": row["canonical_run_id"],
                "stopped_because": row["run_stopped_because"],
                "guessed_behavior": row["guessed_behavior"],
                "guess_confidence": row["guess_confidence"],
                "user_behavior": row["user_behavior"],
                "user_flagged": bool(row["run_user_flagged"]),
            }
            if row["canonical_run_id"] is not None
            else None
        )
        rules.append(summary)
    return {"total": total, "page": page, "page_size": page_size, "rules": rules}


@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, conn=Depends(get_db)):
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "no such rule")
    runs = conn.execute(
        "SELECT * FROM runs WHERE rule_id = ? ORDER BY id", (rule_id,)
    ).fetchall()
    full = _rule_summary(row)
    full.update(
        {
            "reasoning": row["reasoning"],
            "reads": json.loads(row["reads_json"]),
            "semantic_slots": json.loads(row["semantic_slots_json"]),
            "assign": json.loads(row["assign_json"]),
            "source_code": row["source_code"],
            "source_hash": row["source_hash"],
            "error_text": row["error_text"],
            "parent_rule_id": row["parent_rule_id"],
            "change_note": row["change_note"],
            "provenance": {
                "engine_version": row["engine_version"],
                "prompt_set_hash": row["prompt_set_hash"],
                "modifier_catalog_hash": row["modifier_catalog_hash"],
                "helper_version": row["helper_version"],
                "model_id": row["model_id"],
                "model_params": row["model_params_json"],
                "stage_a_rendered": row["stage_a_rendered"],
                "stage_a_raw": row["stage_a_raw"],
                "stage_b_rendered": row["stage_b_rendered"],
                "stage_b_raw": row["stage_b_raw"],
                "repair_rendered": row["repair_rendered"],
                "repair_raw": row["repair_raw"],
            },
            "runs": [_run_summary(r) for r in runs],
        }
    )
    return full


class NewRun(BaseModel):
    seed: int | None = None


@router.post("/rules/{rule_id}/runs")
def rerun_rule(rule_id: int, body: NewRun, conn=Depends(get_db)):
    """Run again with a new seed. Never canonical (REQ-8.6)."""
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "no such rule")
    if row["status"] != "ok":
        raise HTTPException(409, "a broken rule cannot run")
    canon = conn.execute(
        "SELECT width, height, max_ticks FROM runs WHERE rule_id = ? AND is_canonical = 1",
        (rule_id,),
    ).fetchone()
    width = canon["width"] if canon else settings.grid_width
    height = canon["height"] if canon else settings.grid_height
    max_ticks = canon["max_ticks"] if canon else settings.max_ticks

    declaration = Declaration(
        kinds=row["kinds"],
        neighbors=row["neighbors"],
        reach=row["reach"],
        uses=tuple(json.loads(row["uses_json"])),
        reads=tuple(json.loads(row["reads_json"])),
        modifiers=tuple(json.loads(row["modifiers_json"])),
        semantic_slots=json.loads(row["semantic_slots_json"]),
        assign=json.loads(row["assign_json"]),
    )
    seed = body.seed if body.seed is not None else random.randrange(2**31)
    try:
        result = run_in_child(
            row["source_code"], declaration, seed, width, height, max_ticks,
            settings.tick_timeout_seconds, settings.run_memory_limit_mb,
        )
    except RuleCrashed as crashed:
        raise HTTPException(500, f"the rule crashed while running: {crashed}")
    behavior, confidence = classify(result, width, height)
    run_id = db.save_run(
        conn, rule_id, result,
        start_seed=seed, width=width, height=height, max_ticks=max_ticks,
        guessed_behavior=behavior, guess_confidence=confidence,
        engine_version=engine_version(),
        snapshot_every=settings.snapshot_every,
        is_canonical=False,
    )
    fresh = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    return _run_summary(fresh)


@router.get("/runs/{run_id}")
def get_run(run_id: int, conn=Depends(get_db)):
    row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "no such run")
    numbers = conn.execute(
        """SELECT tick, variety, cells_changed, kind_quiet_for, kind_counts_json
           FROM ticks WHERE run_id = ? ORDER BY tick""",
        (run_id,),
    ).fetchall()
    summary = _run_summary(row)
    summary["numbers"] = {
        "variety": [n["variety"] for n in numbers],
        "cells_changed": [n["cells_changed"] for n in numbers],
        "kind_quiet_for": [n["kind_quiet_for"] for n in numbers],
        "kind_counts": [json.loads(n["kind_counts_json"]) for n in numbers],
    }
    return summary


@router.get("/runs/{run_id}/grids")
def get_grids(
    run_id: int,
    request: Request,
    from_tick: int = Query(0, alias="from", ge=0),
    to_tick: int | None = Query(None, alias="to", ge=0),
    props: str = "kind",
    conn=Depends(get_db),
):
    row = conn.execute(
        "SELECT ticks_run FROM runs WHERE id = ?", (run_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "no such run")
    last = row["ticks_run"] if to_tick is None else min(to_tick, row["ticks_run"])
    if from_tick > last:
        raise HTTPException(400, "empty tick range")
    if last - from_tick + 1 > MOST_TICKS_PER_GRID_REQUEST:
        raise HTTPException(
            400, f"ask for at most {MOST_TICKS_PER_GRID_REQUEST} ticks per request"
        )
    names = [p.strip() for p in props.split(",") if p.strip()]
    try:
        stacks = reconstruct_range(conn, run_id, names, from_tick, last)
    except KeyError as missing:
        raise HTTPException(400, f"this run has no property named {missing}")
    from asr.api.framing import frame_grids

    body = frame_grids(from_tick, last, stacks)
    headers = {}
    # Grid stacks are huge but repetitive; wire compression cuts them
    # ~20x and playback smoothness lives or dies on transfer time. The
    # framing itself (REQ-11.5.1) is unchanged — the browser undoes
    # transport encoding before the decoder ever sees the bytes.
    if "gzip" in (request.headers.get("accept-encoding") or ""):
        import gzip

        body = gzip.compress(body, compresslevel=1)
        headers["Content-Encoding"] = "gzip"
    return Response(
        content=body,
        media_type="application/octet-stream",
        headers=headers,
    )


@router.get("/runs/{run_id}/cell/{y}/{x}")
def get_cell_history(
    run_id: int, y: int, x: int, props: str = "kind", request: Request = None,
    conn=Depends(get_db),
):
    row = conn.execute(
        "SELECT ticks_run, width, height FROM runs WHERE id = ?", (run_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "no such run")
    if not (0 <= y < row["height"] and 0 <= x < row["width"]):
        raise HTTPException(400, "cell is outside the grid")
    cache = request.app.state.cache
    names = [p.strip() for p in props.split(",") if p.strip()]
    history = {}
    for name in names:
        try:
            stack = cache.property_history(conn, run_id, name)
        except KeyError as missing:
            raise HTTPException(400, f"this run has no property named {missing}")
        history[name] = stack[:, y, x].tolist()
    return {"run_id": run_id, "y": y, "x": x, "history": history}


class RunCorrection(BaseModel):
    user_behavior: str | None = None
    user_flagged: bool | None = None


@router.patch("/runs/{run_id}")
def correct_run(run_id: int, body: RunCorrection, conn=Depends(get_db)):
    """The only mutation recorded history permits (REQ-11.3): the
    user's behavior override (never overwriting the guess, REQ-9.14)
    and the interesting-flag (REQ-12.7). Neither ever enters generation
    context (REQ-8.5).
    """
    row = conn.execute("SELECT id FROM runs WHERE id = ?", (run_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "no such run")
    provided = body.model_fields_set
    if "user_behavior" in provided:
        if body.user_behavior is not None and body.user_behavior not in BEHAVIOR_NAMES:
            raise HTTPException(400, f"behavior must be one of {BEHAVIOR_NAMES}")
        conn.execute(
            "UPDATE runs SET user_behavior = ? WHERE id = ?",
            (body.user_behavior, run_id),
        )
    if "user_flagged" in provided and body.user_flagged is not None:
        conn.execute(
            "UPDATE runs SET user_flagged = ? WHERE id = ?",
            (int(body.user_flagged), run_id),
        )
    conn.commit()
    fresh = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    return _run_summary(fresh)


@router.get("/catalog/modifiers")
def get_modifier_catalog(conn=Depends(get_db)):
    rows = conn.execute("SELECT * FROM modifier_catalog ORDER BY name").fetchall()
    return {"modifiers": [dict(r) for r in rows]}


@router.get("/library/summary")
def library_summary(conn=Depends(get_db)):
    """Totals, the coverage map, and the rejection tally (REQ-8.2,
    REQ-8.8). One implementation, shared with Stage A context: the
    coverage counts canonical runs only (REQ-8.6).
    """
    from asr.generation import context

    return {
        "totals": context.totals(conn),
        "coverage": context.coverage_map(conn),
        "rejections": context.rejection_tally(conn),
    }
