"""The Dice facade (spec section 6.7)."""

import numpy as np
import pytest

from asr.engine.dice import Dice


def test_every_draw_fills_the_whole_grid():
    dice = Dice(seed=1, height=4, width=6)
    assert dice.chance(0.5).shape == (4, 6)
    assert dice.integers(0, 10).shape == (4, 6)
    assert dice.choice(3).shape == (4, 6)


def test_same_seed_replays_the_same_draws():
    a = Dice(seed=42, height=5, width=5)
    b = Dice(seed=42, height=5, width=5)
    assert np.array_equal(a.chance(0.3), b.chance(0.3))
    assert np.array_equal(a.integers(1, 5), b.integers(1, 5))
    assert np.array_equal(a.choice(8), b.choice(8))


def test_chance_extremes():
    dice = Dice(seed=7, height=8, width=8)
    assert not dice.chance(0.0).any()
    assert dice.chance(1.0).all()


def test_draw_ranges():
    dice = Dice(seed=7, height=16, width=16)
    drawn = dice.integers(2, 5)
    assert drawn.min() >= 2 and drawn.max() < 5
    chosen = dice.choice(3)
    assert chosen.min() >= 0 and chosen.max() < 3


def test_bad_arguments_are_rejected():
    dice = Dice(seed=7, height=2, width=2)
    with pytest.raises(ValueError):
        dice.chance(1.5)
    with pytest.raises(ValueError):
        dice.integers(5, 5)
    with pytest.raises(ValueError):
        dice.choice(0)


def test_state_bytes_track_consumption():
    # The RNG state feeds the computational fingerprint (REQ-9.7.1):
    # equal before any draw, different after one side draws.
    a = Dice(seed=9, height=3, width=3)
    b = Dice(seed=9, height=3, width=3)
    assert a._state_bytes() == b._state_bytes()
    a.chance(0.5)
    assert a._state_bytes() != b._state_bytes()
