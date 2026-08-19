"""The run loop, the fixtures, and the stopping rules (spec sections
9 and 14).
"""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import FIXTURES

import slow_burn_fixture
from toy_rules import NeverChanges


def run_fixture(rule_class, seed, width, height, max_ticks=300):
    declaration = Declaration.from_rule(rule_class)
    return run_rule(
        rule_class, declaration, seed, width, height,
        max_ticks=max_ticks, tick_timeout_seconds=2.0,
    )


def test_walker_loops_once_around_the_grid():
    # REQ-14.1: loop length equal to the grid width.
    result = run_fixture(FIXTURES["walker"], seed=1, width=10, height=6)
    assert result.stopped_because == "looping"
    assert result.loop_length == 10


def test_majority_settles_fast():
    # REQ-14.1: simple counting, fast convergence.
    result = run_fixture(FIXTURES["majority"], seed=7, width=24, height=24)
    assert result.stopped_because == "frozen"
    assert result.ticks_run <= 50


def test_every_fixture_replays_exactly_from_its_seed():
    # REQ-15.3: same seed, identical fingerprints at every tick.
    shapes = {"life": (16, 16), "majority": (16, 16), "walker": (10, 6)}
    for name, rule_class in FIXTURES.items():
        width, height = shapes[name]
        first = run_fixture(rule_class, seed=9, width=width, height=height, max_ticks=80)
        second = run_fixture(rule_class, seed=9, width=width, height=height, max_ticks=80)
        assert [t.state_fingerprint for t in first.ticks] == [
            t.state_fingerprint for t in second.ticks
        ], name
        assert [t.pattern_fingerprint for t in first.ticks] == [
            t.pattern_fingerprint for t in second.ticks
        ], name


class PlantedGlider(FIXTURES["life"]):
    """Life with one glider aimed at the wrap seam (REQ-14.2). Test
    code may subclass; generated code may not."""

    def make_start(self, width, height):
        kind = np.zeros((height, width), dtype=np.uint8)
        for y, x in [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            kind[y, x] = 1
        return make_cells(kind)


def test_glider_crosses_the_wrap_boundary_intact():
    # REQ-14.2: the single best end-to-end proof of the wrap logic.
    # A glider moves one cell diagonally every 4 ticks, so on an 8x8
    # torus it is home — having crossed both seams — after exactly 32.
    result = run_fixture(PlantedGlider, seed=0, width=8, height=8, max_ticks=100)
    assert result.stopped_because == "looping"
    assert result.loop_length == 32
    # Five live cells in every glider phase; any corruption at the seam
    # would change the count.
    assert all(int(t.arrays["kind"].sum()) == 5 for t in result.ticks)
    assert np.array_equal(result.ticks[32].arrays["kind"], result.ticks[0].arrays["kind"])


def test_slow_burn_outlives_its_quiet_start():
    # REQ-15.8: a run ending before tick 60 is a REQ-9.8.1 regression —
    # the pattern is dead still while hidden memory counts up.
    result = run_fixture(slow_burn_fixture.Rule, seed=2, width=10, height=10)
    assert result.ticks_run > slow_burn_fixture.FLIP_AT
    flip = result.ticks[slow_burn_fixture.FLIP_AT]
    assert flip.cells_changed == 100  # the whole grid flips at once
    # kind_quiet_for (REQ-9.15) watched the stillness without acting.
    assert result.ticks[slow_burn_fixture.FLIP_AT - 1].kind_quiet_for == 59
    assert result.stopped_because == "frozen"  # memory saturates later


def test_pattern_settled_at_zero_for_a_run_that_never_moved():
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    result = run_rule(
        NeverChanges, declaration, seed=1, width=6, height=6,
        max_ticks=20, tick_timeout_seconds=2.0,
    )
    assert result.stopped_because == "frozen"
    assert result.pattern_settled_at == 0
