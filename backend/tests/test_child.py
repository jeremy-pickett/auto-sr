"""The child-process runner (REQ-7.6.1, REQ-15.7)."""

import time

import numpy as np
import pytest

from asr.contract.child import RuleCrashed, run_in_child
from asr.engine.cells import make_cells
from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import FIXTURES


def test_a_run_through_the_child_matches_the_in_process_run():
    rule_class = FIXTURES["walker"]
    declaration = Declaration.from_rule(rule_class)
    common = dict(seed=1, width=10, height=6, max_ticks=50)
    direct = run_rule(rule_class, declaration, tick_timeout_seconds=2.0, **common)
    childed = run_in_child(
        rule_class, declaration, tick_timeout_seconds=2.0,
        memory_limit_mb=4096, **common,
    )
    assert childed.stopped_because == direct.stopped_because
    assert childed.loop_length == direct.loop_length
    assert [t.state_fingerprint for t in childed.ticks] == [
        t.state_fingerprint for t in direct.ticks
    ]


class HangsForever:
    """A deliberate long tick (REQ-15.7)."""

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        time.sleep(60)
        return make_cells(cells.kind.copy())


def test_a_hung_tick_is_killed_by_the_parent_and_recorded_too_slow():
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    started = time.monotonic()
    result = run_in_child(
        HangsForever, declaration, seed=1, width=6, height=6,
        max_ticks=10, tick_timeout_seconds=0.3, memory_limit_mb=4096,
    )
    assert result.stopped_because == "too_slow"
    assert result.ticks_run == 0  # only tick 0 completed
    assert time.monotonic() - started < 30  # killed, not waited out


class BlowsUp:
    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        raise ValueError("this rule is deliberately broken")


def test_a_crashing_rule_surfaces_its_traceback():
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    with pytest.raises(RuleCrashed) as caught:
        run_in_child(
            BlowsUp, declaration, seed=1, width=6, height=6,
            max_ticks=10, tick_timeout_seconds=1.0, memory_limit_mb=4096,
        )
    assert "deliberately broken" in str(caught.value)
