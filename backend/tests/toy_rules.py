"""Tiny hand-written rules shared by the run-loop and state-model
tests. Not fixtures — just minimal, predictable behaviors.
"""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.helpers import bind_helpers

_all8 = bind_helpers("all_8", 1)
count_neighbors = _all8["count_neighbors"]

_CONSTANTS = dict(
    KINDS=2, NEIGHBORS="all_8", REACH=1, USES=[], READS=[],
    MODIFIERS=[], SEMANTIC_SLOTS={}, ASSIGN={},
    SUGGESTED_DISPLAY={"color": "kind", "brightness": "age"},
)


class FlipEveryTick:
    """Every cell alternates kind 0 and 1 — maximal churn."""

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        return make_cells((1 - cells.kind).astype(np.uint8))


class NeverChanges:
    """A completely static rule."""

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        return make_cells(cells.kind.copy())


class SpreadsOut:
    """Kind 1 floods outward from the center until the grid fills,
    then nothing changes ever again — births happen for a few ticks
    and then cease.
    """

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        kind = np.zeros((height, width), dtype=np.uint8)
        kind[height // 2, width // 2] = 1
        return make_cells(kind)

    def step(self, cells):
        crowd = count_neighbors(cells, "kind", 1)
        return make_cells(((cells.kind == 1) | (crowd > 0)).astype(np.uint8))


for _rule in (FlipEveryTick, NeverChanges, SpreadsOut):
    for _name, _value in _CONSTANTS.items():
        setattr(_rule, _name, _value)
