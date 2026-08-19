"""Guessing what kind of behavior a finished run showed (REQ-9.16).

Deterministic thresholds, no qualitative judgment. The guess is stored
alongside the numbers that produced it, never as fact (REQ-9.6), and
the user may overrule it without erasing it (REQ-9.14). `unclassified`
is a real outcome, not an error (REQ-9.13). `broken` is never a run
classification — it lives on the rule (REQ-9.16.2).
"""

import numpy as np

from .run import RunResult

WINDOW = 100  # final ticks examined
SHORT_LOOP = 50  # a loop this long or shorter counts as `repeats`
SETTLED_CHANGE_RATE = 0.0005  # below this the pattern stopped moving
NOISY_CHANGE_RATE = 0.10
NOISY_VARIETY = 0.60
DECAY_SLOPE = -0.001  # per tick, scaled by grid area


def classify(result: RunResult, width: int, height: int) -> tuple:
    """Returns (guessed_behavior, guess_confidence)."""
    window = result.ticks[-WINDOW:]
    area = width * height
    change_rate = float(np.mean([t.cells_changed for t in window])) / area
    mean_variety = float(np.mean([t.variety for t in window]))

    # Rows 1-4: the stop reason alone decides.
    if result.stopped_because == "looping":
        if result.loop_length <= SHORT_LOOP:
            return "repeats", "high"
        return "unclassified", "high"  # a long loop is a different phenomenon
    if result.stopped_because == "too_slow":
        return "unclassified", "high"
    if result.stopped_because == "frozen":
        return "settles", "high"

    # Rows 5-8: the run ran out its budget; read the final window.
    if change_rate < SETTLED_CHANGE_RATE:
        # The pattern stopped moving without an exact freeze.
        return "settles", "low"
    if change_rate >= NOISY_CHANGE_RATE and mean_variety >= NOISY_VARIETY:
        return "noisy", "high"
    if change_rate < NOISY_CHANGE_RATE and mean_variety < NOISY_VARIETY:
        # The slope term separates persistence from slow decay: stable
        # shapes that move or persist keep cells_changed level, while a
        # dying run's cells_changed falls tick over tick (REQ-9.16.1).
        ticks = [t.tick for t in window]
        changes = [t.cells_changed for t in window]
        slope = float(np.polyfit(ticks, changes, 1)[0]) if len(window) > 1 else 0.0
        if slope > DECAY_SLOPE * area:
            return "structured", "low"

    return "unclassified", "low"
