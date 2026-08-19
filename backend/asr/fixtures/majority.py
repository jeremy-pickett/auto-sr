"""The `majority` fixture (REQ-14.1): each cell joins whichever kind
holds the majority among itself and its eight neighbors — nine voters,
so there are no ties. Simple counting, fast convergence; expected to
settle within roughly fifty ticks.
"""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.helpers import bind_helpers

_helpers = bind_helpers("all_8", 1)
count_neighbors = _helpers["count_neighbors"]


class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "age"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(self.dice.chance(0.5).astype(np.uint8))

    def step(self, cells):
        votes_for_one = count_neighbors(cells, "kind", 1) + cells.kind
        return make_cells((votes_for_one >= 5).astype(np.uint8))
