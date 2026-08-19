"""The six state-model cases of REQ-15.6: what counts as the same
state, and therefore what is allowed to stop a run.
"""

from asr.engine.declaration import Declaration
from asr.engine.run import run_rule

from toy_rules import FlipEveryTick, NeverChanges, SpreadsOut

SIZE = 6


def run(rule_class, declaration, max_ticks=30, seed=4):
    return run_rule(
        rule_class, declaration, seed, SIZE, SIZE,
        max_ticks=max_ticks, tick_timeout_seconds=2.0,
    )


def declaration(**overrides):
    base = dict(kinds=2, neighbors="all_8", reach=1)
    base.update(overrides)
    return Declaration(**base)


def test_a_rule_reading_age_never_freezes_on_a_static_grid():
    # Its future depends on age, and age keeps rising.
    result = run(NeverChanges, declaration(reads=("age",)), max_ticks=20)
    assert result.stopped_because == "ran_out"


def test_the_same_rule_without_the_read_freezes_immediately():
    result = run(NeverChanges, declaration(), max_ticks=20)
    assert result.stopped_because == "frozen"
    assert result.ticks_run == 1


def test_stubbornness_in_scope_freezes_once_ages_pass_the_clamp():
    # REQ-9.7.6: the harness only asks age >= stubbornness (max 3), so
    # clamped ages 1, 2, 3 differ and then the state repeats at tick 4.
    result = run(NeverChanges, declaration(modifiers=("stubbornness",)), max_ticks=20)
    assert result.stopped_because == "frozen"
    assert result.ticks_run == 4


def test_rate_prevents_false_loops_across_scheduler_phases():
    # Flipping under rate 2: the kinds recur every 4 ticks, but two
    # grids at different points in the rate cycle have different
    # futures, so the true loop is the full 12-tick scheduler cycle.
    result = run(
        FlipEveryTick,
        declaration(modifiers=("rate",), assign={"rate": {"value": 2, "chance": 1.0}}),
        max_ticks=40,
    )
    assert result.stopped_because == "looping"
    assert result.loop_length == 12


def test_a_stochastic_rule_that_settles_reaches_frozen():
    # REQ-9.7.7: birth draws stop once births stop, so the RNG state
    # stops advancing and exact freezing becomes possible.
    result = run(
        SpreadsOut,
        declaration(modifiers=("weight",), assign={"weight": {"value": 2, "chance": 0.5}}),
        max_ticks=30,
    )
    assert result.stopped_because == "frozen"


def test_a_stochastic_rule_with_endless_births_runs_out_its_budget():
    result = run(
        FlipEveryTick,
        declaration(modifiers=("weight",), assign={"weight": {"value": 2, "chance": 0.5}}),
        max_ticks=30,
    )
    assert result.stopped_because == "ran_out"
