"""Storage round trips (REQ-12.5, REQ-12.6) and reconstruction
(REQ-15.4): every tick of a fixture run rebuilt from payloads must
match the grids captured live — across all three encodings, derived
arrays included.
"""

import numpy as np
import pytest

from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import FIXTURES
from asr.storage import db
from asr.storage.reconstruct import ReconstructionCache, reconstruct_range

import slow_burn_fixture


@pytest.fixture()
def library(tmp_path):
    conn = db.connect(tmp_path / "library.db")
    yield conn
    conn.close()


def saved_run(conn, rule_class, *, seed, width, height, max_ticks, snapshot_every):
    declaration = Declaration.from_rule(rule_class)
    result = run_rule(
        rule_class, declaration, seed, width, height,
        max_ticks=max_ticks, tick_timeout_seconds=2.0,
    )
    rule_id = db.insert_rule(
        conn,
        {
            "description": "test rule",
            "kinds": declaration.kinds,
            "neighbors": declaration.neighbors,
            "reach": declaration.reach,
            "source_code": "test",
            "source_hash": "test",
            "status": "ok",
            "engine_version": "test",
        },
    )
    run_id = db.save_run(
        conn, rule_id, result,
        start_seed=seed, width=width, height=height, max_ticks=max_ticks,
        guessed_behavior="settles", guess_confidence="high",
        engine_version="test", snapshot_every=snapshot_every, is_canonical=True,
    )
    return run_id, result


def encodings_used(conn, run_id):
    return {
        row["payload_encoding"]
        for row in conn.execute(
            "SELECT DISTINCT payload_encoding FROM ticks WHERE run_id = ?", (run_id,)
        )
    }


def assert_rebuild_matches_live(conn, run_id, result, properties):
    rebuilt = reconstruct_range(conn, run_id, properties, 0, result.ticks_run)
    for name in properties:
        for record in result.ticks:
            assert np.array_equal(
                rebuilt[name][record.tick], record.arrays[name]
            ), f"{name} differs at tick {record.tick}"


def test_every_tick_rebuilds_exactly_with_derived_arrays(library):
    # Walker changes 2 cells per tick (sparse); slow_burn increments
    # every cell's memory every tick (dense); snapshots come from the
    # interval. Together the three encodings are all exercised.
    walker_id, walker = saved_run(
        library, FIXTURES["walker"], seed=1, width=10, height=6,
        max_ticks=50, snapshot_every=10,
    )
    burn_id, burn = saved_run(
        library, slow_burn_fixture.Rule, seed=2, width=10, height=10,
        max_ticks=300, snapshot_every=50,
    )
    assert_rebuild_matches_live(
        library, walker_id, walker, ["kind", "heading", "age", "changed_last_tick"]
    )
    assert_rebuild_matches_live(
        library, burn_id, burn, ["kind", "memory", "age", "changed_last_tick"]
    )
    assert encodings_used(library, walker_id) | encodings_used(library, burn_id) == {
        "snapshot", "sparse", "dense",
    }


def test_a_middle_range_rebuilds_from_the_nearest_snapshot(library):
    run_id, result = saved_run(
        library, slow_burn_fixture.Rule, seed=2, width=10, height=10,
        max_ticks=100, snapshot_every=10,
    )
    piece = reconstruct_range(library, run_id, ["kind", "age", "changed_last_tick"], 25, 40)
    for offset, tick in enumerate(range(25, 41)):
        for name in ("kind", "age", "changed_last_tick"):
            assert np.array_equal(piece[name][offset], result.ticks[tick].arrays[name])


def test_life_history_round_trips(library):
    run_id, result = saved_run(
        library, FIXTURES["life"], seed=9, width=16, height=16,
        max_ticks=80, snapshot_every=20,
    )
    assert_rebuild_matches_live(library, run_id, result, ["kind", "age"])


def test_run_row_records_the_outcome(library):
    run_id, result = saved_run(
        library, FIXTURES["walker"], seed=1, width=10, height=6,
        max_ticks=50, snapshot_every=10,
    )
    row = library.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    assert row["stopped_because"] == "looping"
    assert row["loop_length"] == 10
    assert row["ticks_run"] == result.ticks_run
    assert row["is_canonical"] == 1
    assert row["user_behavior"] is None
    assert row["user_flagged"] == 0


def test_cache_evicts_by_bytes_and_reuses_hits(library):
    run_id, result = saved_run(
        library, FIXTURES["walker"], seed=1, width=10, height=6,
        max_ticks=50, snapshot_every=10,
    )
    kind_stack_bytes = (result.ticks_run + 1) * 10 * 6  # uint8
    cache = ReconstructionCache(budget_bytes=int(kind_stack_bytes * 1.5))
    first = cache.property_history(library, run_id, "kind")
    again = cache.property_history(library, run_id, "kind")
    assert again is first  # a hit, not a rebuild
    cache.property_history(library, run_id, "heading")  # pushes over budget
    assert len(cache._held) == 1  # the older stack was evicted
    assert np.array_equal(first[10], result.ticks[10].arrays["kind"])
