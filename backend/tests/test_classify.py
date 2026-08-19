"""The deterministic behavior classifier (REQ-9.16), row by row."""

from asr.engine.classify import classify
from asr.engine.run import RunResult, TickRecord

AREA = 100 * 100


def fake_run(stopped_because, loop_length=None, changes=(), varieties=()):
    ticks = [
        TickRecord(
            tick=i,
            arrays={},
            kind_counts=[],
            variety=varieties[i] if varieties else 0.5,
            cells_changed=changes[i] if changes else 0,
            kind_quiet_for=0,
            state_fingerprint=b"",
            pattern_fingerprint=b"",
        )
        for i in range(len(changes) or 100)
    ]
    return RunResult(
        stopped_because=stopped_because,
        loop_length=loop_length,
        ticks_run=len(ticks) - 1,
        pattern_settled_at=None,
        ticks=ticks,
    )


def test_row_1_short_loop_is_repeats():
    assert classify(fake_run("looping", 30), 100, 100) == ("repeats", "high")


def test_row_2_long_loop_is_unclassified_with_confidence():
    # A long loop is genuinely not the same phenomenon (REQ-9.13).
    assert classify(fake_run("looping", 80), 100, 100) == ("unclassified", "high")


def test_row_3_too_slow_is_unclassified():
    assert classify(fake_run("too_slow"), 100, 100) == ("unclassified", "high")


def test_row_4_frozen_is_settles():
    assert classify(fake_run("frozen"), 100, 100) == ("settles", "high")


def test_row_5_quiet_pattern_without_exact_freeze_is_settles_low():
    run = fake_run("ran_out", changes=[3] * 100, varieties=[0.5] * 100)
    assert classify(run, 100, 100) == ("settles", "low")  # 3/10000 < 0.0005


def test_row_6_high_churn_high_variety_is_noisy():
    run = fake_run("ran_out", changes=[1500] * 100, varieties=[0.8] * 100)
    assert classify(run, 100, 100) == ("noisy", "high")


def test_row_7_level_moderate_churn_low_variety_is_structured():
    run = fake_run("ran_out", changes=[100] * 100, varieties=[0.3] * 100)
    assert classify(run, 100, 100) == ("structured", "low")


def test_row_7_rejects_a_decaying_run():
    # cells_changed falling faster than 0.001 x area per tick reads as
    # slow death, not persistence (REQ-9.16.1).
    # Mean change rate 0.076 passes the moderate-churn gate; the slope
    # of -15/tick (threshold: -10/tick at this area) is what rejects it.
    fading = [1500 - 15 * i for i in range(100)]
    run = fake_run("ran_out", changes=fading, varieties=[0.3] * 100)
    assert classify(run, 100, 100) == ("unclassified", "low")


def test_row_8_odd_mixtures_fall_through_unclassified():
    # Moderate churn but high variety fits no row.
    run = fake_run("ran_out", changes=[500] * 100, varieties=[0.9] * 100)
    assert classify(run, 100, 100) == ("unclassified", "low")
