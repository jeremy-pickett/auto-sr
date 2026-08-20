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

from asr.api.auth import get_current_user
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


def _rule_hidden_from(visibility: str, owner_uid: str | None, user: dict | None) -> bool:
    """A private rule is invisible to everyone except its owner. Every
    caller of this raises the exact same 404 message as a genuine
    not-found, so the response never distinguishes "doesn't exist"
    from "exists but isn't yours."
    """
    return visibility == "private" and (user is None or user["uid"] != owner_uid)


def _rule_summary(
    row, user: dict | None = None, favorited_ids: set | None = None,
    favorite_counts: dict | None = None, comment_counts: dict | None = None,
) -> dict:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "description": row["description"],
        "title": row["title"],
        "slug": row["slug"],
        "spark": row["spark"],
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
        "visibility": row["visibility"],
        # A server-computed membership flag, never the raw owner_uid --
        # no reason to hand one user's opaque identifier to another.
        "mine": bool(user) and row["owner_uid"] == user["uid"],
        # Lets the frontend tell "nobody owns this, anyone may title it"
        # apart from "someone else owns this" without ever learning who.
        "has_owner": row["owner_uid"] is not None,
        "favorited": bool(favorited_ids) and row["id"] in favorited_ids,
        # Doubles as the "likes/upvotes" signal from the feature list --
        # same underlying mechanism as favoriting (one row per user per
        # rule), just read as a public count instead of a private flag.
        # Building two near-identical tables for what's structurally the
        # same thing wasn't worth it; this is the count that makes the
        # one table cover both.
        "favorite_count": (favorite_counts or {}).get(row["id"], 0),
        "comment_count": (comment_counts or {}).get(row["id"], 0),
    }


_SLUG_KEEP = "abcdefghijklmnopqrstuvwxyz0123456789-"


def _slugify(text: str) -> str:
    lowered = "".join(c if c.isalnum() else "-" for c in text.lower())
    lowered = "".join(c for c in lowered if c in _SLUG_KEEP)
    while "--" in lowered:
        lowered = lowered.replace("--", "-")
    return lowered.strip("-")[:60] or "rule"


def _unique_slug(conn, base: str, rule_id: int) -> str:
    """Append -2, -3, ... until the slug is free (ignoring this rule's
    own current row, so re-saving the same title doesn't collide with
    itself)."""
    candidate = base
    n = 2
    while conn.execute(
        "SELECT 1 FROM rules WHERE slug = ? AND id != ?", (candidate, rule_id)
    ).fetchone():
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def _apply_title(conn, rule_id: int, title: str | None) -> None:
    """The shared title+slug write, used by both PATCH /rules/{id} and
    naming a rule at the moment it's invented. A blank/None title is a
    no-op here (the row already defaults to title=NULL) -- clearing an
    *existing* title is PATCH /rules/{id}'s job specifically.
    """
    if not title or not title.strip():
        return
    cleaned = title.strip()[:120]
    slug = _unique_slug(conn, _slugify(cleaned), rule_id)
    conn.execute("UPDATE rules SET title = ?, slug = ? WHERE id = ?", (cleaned, slug, rule_id))
    conn.commit()


def _favorited_ids(conn, user: dict | None) -> set:
    if not user:
        return set()
    return {
        row["rule_id"]
        for row in conn.execute("SELECT rule_id FROM favorites WHERE user_uid = ?", (user["uid"],))
    }


def _favorite_counts(conn, rule_ids) -> dict:
    ids = list(rule_ids)
    if not ids:
        return {}
    placeholders = ",".join("?" * len(ids))
    return {
        row["rule_id"]: row["n"]
        for row in conn.execute(
            f"SELECT rule_id, COUNT(*) AS n FROM favorites WHERE rule_id IN ({placeholders}) GROUP BY rule_id",
            ids,
        )
    }


def _comment_counts(conn, rule_ids) -> dict:
    ids = list(rule_ids)
    if not ids:
        return {}
    placeholders = ",".join("?" * len(ids))
    return {
        row["rule_id"]: row["n"]
        for row in conn.execute(
            f"SELECT rule_id, COUNT(*) AS n FROM comments WHERE rule_id IN ({placeholders}) GROUP BY rule_id",
            ids,
        )
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
    mine: bool = Query(False),
    favorited: bool = Query(False),
    sort: str = Query("newest"),
    user: dict | None = Depends(get_current_user),
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
    if favorited:
        if user is None:
            raise HTTPException(401, "sign in to view your favorites")
        clauses.append("EXISTS (SELECT 1 FROM favorites fav WHERE fav.rule_id = rules.id AND fav.user_uid = ?)")
        params.append(user["uid"])
    # The default listing is always the public/global library, no
    # matter who's asking. mine=true is the personal library --
    # everything you own, public or private -- and requires sign-in.
    if mine:
        if user is None:
            raise HTTPException(401, "sign in to view your personal library")
        clauses.append("rules.owner_uid = ?")
        params.append(user["uid"])
    else:
        clauses.append("rules.visibility = 'public'")
    order = "rules.id DESC"
    if sort == "most_liked":
        order = "(SELECT COUNT(*) FROM favorites lk WHERE lk.rule_id = rules.id) DESC, rules.id DESC"
    elif sort == "most_discussed":
        order = "(SELECT COUNT(*) FROM comments cm WHERE cm.rule_id = rules.id) DESC, rules.id DESC"
    elif sort == "most_looped":
        # "Most looped" reinterpreted concretely for this app's actual
        # domain: the canonical run's loop_length, i.e. the longest
        # repeating cycle a rule settled into -- not a generic "play
        # count" (which isn't tracked anywhere and would need new
        # instrumentation to add just for a sort option). Rules that
        # never reached a detected loop sort last, not excluded.
        order = "COALESCE(canon.loop_length, -1) DESC, rules.id DESC"
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    base = f"""FROM rules
               LEFT JOIN runs canon
                 ON canon.rule_id = rules.id AND canon.is_canonical = 1
               {where}"""
    total = conn.execute(f"SELECT COUNT(*) AS n {base}", params).fetchone()["n"]
    rows = conn.execute(
        f"""SELECT rules.*, canon.id AS canonical_run_id,
                   canon.stopped_because AS run_stopped_because,
                   canon.ticks_run AS run_ticks_run,
                   canon.guessed_behavior, canon.guess_confidence,
                   canon.user_behavior, canon.user_flagged AS run_user_flagged
            {base}
            ORDER BY {order} LIMIT ? OFFSET ?""",
        params + [page_size, (page - 1) * page_size],
    ).fetchall()
    favorited_ids = _favorited_ids(conn, user)
    rule_ids = [row["id"] for row in rows]
    favorite_counts = _favorite_counts(conn, rule_ids)
    comment_counts = _comment_counts(conn, rule_ids)
    rules = []
    for row in rows:
        summary = _rule_summary(row, user, favorited_ids, favorite_counts, comment_counts)
        summary["canonical_run"] = (
            {
                "id": row["canonical_run_id"],
                "stopped_because": row["run_stopped_because"],
                "ticks_run": row["run_ticks_run"],
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


def _full_rule_detail(row, user, conn) -> dict:
    runs = conn.execute(
        "SELECT * FROM runs WHERE rule_id = ? ORDER BY id", (row["id"],)
    ).fetchall()
    full = _rule_summary(
        row, user, _favorited_ids(conn, user),
        _favorite_counts(conn, [row["id"]]), _comment_counts(conn, [row["id"]]),
    )
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


@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    return _full_rule_detail(row, user, conn)


@router.get("/rules/by-slug/{slug}")
def get_rule_by_slug(slug: str, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    """The clean-URL lookup a title's slug resolves through
    (#/r/:slug in the frontend). Doesn't replace the numeric #/rules/:id
    route anywhere -- purely additive, so nothing already working
    changes shape.
    """
    row = conn.execute("SELECT * FROM rules WHERE slug = ?", (slug,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    return _full_rule_detail(row, user, conn)


class RuleTitle(BaseModel):
    title: str | None = None


@router.patch("/rules/{rule_id}")
def set_rule_title(
    rule_id: int, body: RuleTitle,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    """The one mutation a rule permits: a user-editable display name,
    layered over the AI-generated description exactly the way
    user_behavior layers over guessed_behavior -- the description
    itself never changes. Ownerless (anonymous-generated) rules can be
    titled by anyone, matching how they're already open to anyone for
    running/correcting; an owned rule can only be retitled by its
    owner, so a stranger can't rename someone else's public rule.
    """
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    if row["owner_uid"] is not None and (user is None or user["uid"] != row["owner_uid"]):
        raise HTTPException(403, "only this rule's owner can rename it")

    if body.title is None or not body.title.strip():
        conn.execute("UPDATE rules SET title = NULL, slug = NULL WHERE id = ?", (rule_id,))
        conn.commit()
    else:
        _apply_title(conn, rule_id, body.title)
    fresh = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    return _rule_summary(
        fresh, user, _favorited_ids(conn, user),
        _favorite_counts(conn, [rule_id]), _comment_counts(conn, [rule_id]),
    )


@router.post("/rules/{rule_id}/favorite")
def add_favorite(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    if user is None:
        raise HTTPException(401, "sign in to favorite a rule")
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    conn.execute(
        "INSERT OR IGNORE INTO favorites(user_uid, rule_id, created_at) VALUES(?,?,?)",
        (user["uid"], rule_id, db.now()),
    )
    conn.commit()
    return {"favorited": True}


@router.delete("/rules/{rule_id}/favorite")
def remove_favorite(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    if user is None:
        raise HTTPException(401, "sign in to favorite a rule")
    conn.execute("DELETE FROM favorites WHERE user_uid = ? AND rule_id = ?", (user["uid"], rule_id))
    conn.commit()
    return {"favorited": False}


# Kept in sync by hand with frontend/src/lib/palette.js's KIND_COLORS --
# there's no shared config between the two languages, and duplicating
# eight hex triples isn't worth building one for. If the frontend
# palette changes, this should too.
_PREVIEW_PALETTE = [
    (0x18, 0x21, 0x30), (0x95, 0xc2, 0xfa), (0xf4, 0x9e, 0x7b), (0x38, 0xf0, 0xb0),
    (0xff, 0xbc, 0x3a), (0xf2, 0xa4, 0xc0), (0x00, 0xf3, 0x00), (0xe5, 0xe2, 0xfd),
]


@router.get("/rules/{rule_id}/preview.png")
def rule_preview_image(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    """A static PNG of the canonical run's final frame -- for Open
    Graph/Twitter card previews and anywhere else a rule needs a
    plain image rather than the live player. Same visibility check as
    every other rule-scoped endpoint: a private rule's preview 404s
    for non-owners, so a sharing platform's crawler (which never
    carries an auth token) can never fetch one.
    """
    import io

    import numpy as np
    from PIL import Image

    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    canon = conn.execute(
        "SELECT id, ticks_run FROM runs WHERE rule_id = ? AND is_canonical = 1", (rule_id,)
    ).fetchone()
    if canon is None:
        raise HTTPException(404, "this rule has no canonical run to preview")

    stacks = reconstruct_range(conn, canon["id"], ["kind"], canon["ticks_run"], canon["ticks_run"])
    grid = stacks["kind"][0]
    height, width = grid.shape
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    for kind, color in enumerate(_PREVIEW_PALETTE):
        rgb[grid == kind] = color

    image = Image.fromarray(rgb, "RGB")
    scale = max(1, 640 // max(width, height))
    if scale > 1:
        image = image.resize((width * scale, height * scale), Image.NEAREST)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")


class NewRun(BaseModel):
    seed: int | None = None


@router.post("/rules/{rule_id}/runs")
def rerun_rule(
    rule_id: int, body: NewRun,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    """Run again with a new seed. Never canonical (REQ-8.6)."""
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
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
def get_run(run_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    row = conn.execute(
        """SELECT runs.*, rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
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
    user: dict | None = Depends(get_current_user),
    conn=Depends(get_db),
):
    row = conn.execute(
        """SELECT runs.ticks_run, rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
        raise HTTPException(404, "no such run")
    last = row["ticks_run"] if to_tick is None else min(to_tick, row["ticks_run"])
    if from_tick > last:
        raise HTTPException(400, "empty tick range")
    if last - from_tick + 1 > MOST_TICKS_PER_GRID_REQUEST:
        raise HTTPException(
            400, f"ask for at most {MOST_TICKS_PER_GRID_REQUEST} ticks per request"
        )
    names = [p.strip() for p in props.split(",") if p.strip()]
    # A run's property history never changes once recorded, so it's
    # cached whole (REQ-11.2) rather than re-decoded from the nearest
    # snapshot on every request -- the first grids request for a run
    # pays to decode the full run per property; every later chunk,
    # including scrubs, loops, and reruns of the same range, is a
    # cheap in-memory slice instead.
    cache = request.app.state.cache
    try:
        stacks = {
            name: cache.property_history(conn, run_id, name)[from_tick : last + 1]
            for name in names
        }
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


@router.get("/runs/{run_id}/export")
def export_run(
    run_id: int,
    request: Request,
    from_tick: int = Query(0, alias="from", ge=0),
    to_tick: int | None = Query(None, alias="to", ge=0),
    props: str = "kind",
    user: dict | None = Depends(get_current_user),
    conn=Depends(get_db),
):
    """The full tick range as plain JSON, uncapped — deliberately not
    the packed binary framing GET /runs/{id}/grids uses. That format
    exists for a canvas decoder; this one exists so a script (or
    another Claude session) can fetch a run's raw history with a
    single request and json.loads it, no custom binary parser needed.
    Genuinely large for a full run — that's the tradeoff for "plain
    and simple to consume," not an oversight.
    """
    row = conn.execute(
        """SELECT runs.ticks_run, runs.width, runs.height,
                  rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
        raise HTTPException(404, "no such run")
    last = row["ticks_run"] if to_tick is None else min(to_tick, row["ticks_run"])
    if from_tick > last:
        raise HTTPException(400, "empty tick range")
    names = [p.strip() for p in props.split(",") if p.strip()]
    try:
        stacks = reconstruct_range(conn, run_id, names, from_tick, last)
    except KeyError as missing:
        raise HTTPException(400, f"this run has no property named {missing}")

    payload = json.dumps({
        "run_id": run_id,
        "shape": [row["height"], row["width"]],
        "ticks": [from_tick, last],
        "properties": {name: stack.tolist() for name, stack in stacks.items()},
    }).encode()

    headers = {}
    if "gzip" in (request.headers.get("accept-encoding") or ""):
        import gzip

        payload = gzip.compress(payload, compresslevel=1)
        headers["Content-Encoding"] = "gzip"
    return Response(content=payload, media_type="application/json", headers=headers)


@router.get("/runs/{run_id}/cell/{y}/{x}")
def get_cell_history(
    run_id: int, y: int, x: int, props: str = "kind", request: Request = None,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    row = conn.execute(
        """SELECT runs.ticks_run, runs.width, runs.height,
                  rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
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
def correct_run(
    run_id: int, body: RunCorrection,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    """The only mutation recorded history permits (REQ-11.3): the
    user's behavior override (never overwriting the guess, REQ-9.14)
    and the interesting-flag (REQ-12.7). Neither ever enters generation
    context (REQ-8.5).
    """
    row = conn.execute(
        """SELECT runs.id, rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
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


MOST_RSS_ITEMS = 30


@router.get("/library/feed.rss")
def library_feed(request: Request, conn=Depends(get_db)):
    """A plain RSS 2.0 feed of the most recently invented public
    rules -- 'for people who want to watch the library grow passively'
    per the feature request. Public rules only: an RSS reader carries
    no auth token, so a private rule couldn't be fetched by its own
    detail endpoint either -- consistent with everything else, not a
    special case. Deliberately not building the webhook half of that
    same feature-list item: a user-supplied delivery URL is a real
    SSRF surface (the server would be making outbound requests to
    wherever a caller points it) and there's no delivery/retry
    infrastructure in this app to do it safely. Logged.
    """
    import datetime
    import email.utils
    from xml.sax.saxutils import escape

    rows = conn.execute(
        """SELECT id, title, description, created_at FROM rules
           WHERE visibility = 'public' ORDER BY id DESC LIMIT ?""",
        (MOST_RSS_ITEMS,),
    ).fetchall()
    base = str(request.base_url).rstrip("/")
    items = []
    for row in rows:
        link = f"{base}/#/rules/{row['id']}"
        title = escape(row["title"] or f"rule #{row['id']}")
        description = escape((row["description"] or "")[:500])
        try:
            pub_date = email.utils.format_datetime(
                datetime.datetime.fromisoformat(row["created_at"])
            )
        except ValueError:
            pub_date = ""
        items.append(
            f"<item><title>{title}</title><link>{link}</link>"
            f"<guid>{link}</guid><pubDate>{pub_date}</pubDate>"
            f"<description>{description}</description></item>"
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        "<title>Autonomous Semantic Ruliology</title>"
        f"<link>{base}/</link>"
        "<description>Newly invented cellular-automaton rules, as the library grows.</description>"
        + "".join(items)
        + "</channel></rss>"
    )
    return Response(content=body, media_type="application/rss+xml")
