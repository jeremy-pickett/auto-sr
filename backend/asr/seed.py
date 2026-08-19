"""Seed the library with the reference rules (spec section 14) and the
modifier catalog, then record one canonical run for each rule.

Run from backend/:  .venv/bin/python -m asr.seed
Idempotent: a rule whose source hash is already present is skipped.
"""

import hashlib
import inspect
import json

from asr.config import settings
from asr.engine.classify import classify
from asr.engine.declaration import Declaration
from asr.engine.modifiers import MODIFIER_CATALOG
from asr.engine.run import run_rule
from asr.fixtures import life, majority, walker
from asr.storage import db
from asr.version import HELPER_VERSION, engine_version

FIXTURE_CARDS = [
    {
        "module": life,
        "description": (
            "A cell looks at its eight neighbors. A living cell keeps living "
            "with two or three living neighbors; an empty cell comes alive "
            "with exactly three. (Conway's Game of Life.)"
        ),
        "requested_shape": "count_based",
        "concepts": ["counts", "competes"],
    },
    {
        "module": majority,
        "description": (
            "A cell joins whichever kind holds the majority among itself and "
            "its eight neighbors. Nine voters, so there are no ties."
        ),
        "requested_shape": "count_based",
        "concepts": ["counts", "spreads"],
    },
    {
        "module": walker,
        "description": (
            "A single cell marches east forever, carrying its heading with "
            "it, wrapping around the grid."
        ),
        "requested_shape": "walker",
        "concepts": ["moves"],
    },
]


def seed_catalog(conn) -> None:
    for spec in MODIFIER_CATALOG.values():
        conn.execute(
            """INSERT OR REPLACE INTO modifier_catalog
               (name, type_spec, default_value, applied_by, effect,
                assign_when, availability, blurb)
               VALUES(?,?,?,?,?,?,?,?)""",
            (
                spec.name,
                f"int({spec.lowest}, {spec.highest})",
                str(spec.identity),
                "harness",
                spec.effect,
                spec.assign_when,
                spec.availability,
                spec.blurb,
            ),
        )
    conn.commit()


def seed_fixture(conn, card) -> int | None:
    rule_class = card["module"].Rule
    source = inspect.getsource(rule_class)
    source_hash = hashlib.blake2b(source.encode(), digest_size=16).hexdigest()
    already = conn.execute(
        "SELECT id FROM rules WHERE source_hash = ?", (source_hash,)
    ).fetchone()
    if already:
        return None

    declaration = Declaration.from_rule(rule_class)
    rule_id = db.insert_rule(
        conn,
        {
            "description": card["description"],
            "reasoning": "Hand-written reference rule (spec section 14).",
            "kinds": declaration.kinds,
            "neighbors": declaration.neighbors,
            "reach": declaration.reach,
            "uses_json": json.dumps(list(declaration.uses)),
            "reads_json": json.dumps(list(declaration.reads)),
            "modifiers_json": json.dumps(list(declaration.modifiers)),
            "semantic_slots_json": json.dumps(declaration.semantic_slots),
            "assign_json": json.dumps(declaration.assign),
            "suggested_display_json": json.dumps(rule_class.SUGGESTED_DISPLAY),
            "requested_shape": card["requested_shape"],
            "observed_shape": card["requested_shape"],
            "concepts_json": json.dumps(card["concepts"]),
            "source_code": source,
            "source_hash": source_hash,
            "status": "ok",
            "engine_version": engine_version(),
            "helper_version": HELPER_VERSION,
            "model_id": "hand_written",
        },
    )

    result = run_rule(
        rule_class,
        declaration,
        seed=1,
        width=settings.grid_width,
        height=settings.grid_height,
        max_ticks=settings.max_ticks,
        tick_timeout_seconds=settings.tick_timeout_seconds,
    )
    behavior, confidence = classify(result, settings.grid_width, settings.grid_height)
    db.save_run(
        conn,
        rule_id,
        result,
        start_seed=1,
        width=settings.grid_width,
        height=settings.grid_height,
        max_ticks=settings.max_ticks,
        guessed_behavior=behavior,
        guess_confidence=confidence,
        engine_version=engine_version(),
        snapshot_every=settings.snapshot_every,
        is_canonical=True,
    )
    return rule_id


def main() -> None:
    conn = db.connect(settings.database_path)
    seed_catalog(conn)
    for card in FIXTURE_CARDS:
        rule_id = seed_fixture(conn, card)
        name = card["module"].__name__.rsplit(".", 1)[-1]
        if rule_id is None:
            print(f"{name}: already seeded")
        else:
            row = conn.execute(
                """SELECT stopped_because, ticks_run, guessed_behavior FROM runs
                   WHERE rule_id = ? AND is_canonical = 1""",
                (rule_id,),
            ).fetchone()
            print(
                f"{name}: rule {rule_id}, {row['ticks_run']} ticks, "
                f"{row['stopped_because']}, guessed {row['guessed_behavior']}"
            )
    conn.close()


if __name__ == "__main__":
    main()
