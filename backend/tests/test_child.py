"""The child-process runner (REQ-7.6.1, REQ-15.7). The child receives
rule source, exactly as production does.
"""

import inspect
import time

import pytest

from asr.contract.child import RuleCrashed, run_in_child
from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import walker


def test_a_run_through_the_child_matches_the_in_process_run():
    declaration = Declaration.from_rule(walker.Rule)
    common = dict(seed=1, width=10, height=6, max_ticks=50)
    direct = run_rule(walker.Rule, declaration, tick_timeout_seconds=2.0, **common)
    childed = run_in_child(
        inspect.getsource(walker.Rule), declaration, tick_timeout_seconds=2.0,
        memory_limit_mb=4096, **common,
    )
    assert childed.stopped_because == direct.stopped_because
    assert childed.loop_length == direct.loop_length
    assert [t.state_fingerprint for t in childed.ticks] == [
        t.state_fingerprint for t in direct.ticks
    ]


HANGS_FOREVER = """
class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        while True:
            pass
"""


def test_a_hung_tick_is_killed_by_the_parent_and_recorded_too_slow():
    # REQ-15.7: a deliberate endless tick is killed by the parent and
    # recorded as too_slow without taking the server down.
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    started = time.monotonic()
    result = run_in_child(
        HANGS_FOREVER, declaration, seed=1, width=6, height=6,
        max_ticks=10, tick_timeout_seconds=0.3, memory_limit_mb=4096,
    )
    assert result.stopped_because == "too_slow"
    assert result.ticks_run == 0  # only tick 0 completed
    assert time.monotonic() - started < 40  # killed, not waited out


BLOWS_UP = """
class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        # Raising needs no builtin: an unknown property blows up in the
        # Cells attribute lookup with a distinctive message.
        return cells.deliberately_broken
"""


def test_a_crashing_rule_surfaces_its_traceback():
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    with pytest.raises(RuleCrashed) as caught:
        run_in_child(
            BLOWS_UP, declaration, seed=1, width=6, height=6,
            max_ticks=10, tick_timeout_seconds=1.0, memory_limit_mb=4096,
        )
    assert "deliberately_broken" in str(caught.value)
