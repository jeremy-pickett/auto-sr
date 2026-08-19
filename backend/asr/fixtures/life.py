"""Conway's Game of Life — the `life` fixture (REQ-14.1).

Exercises count_neighbors, two kinds, all_8 at reach 1. Expected
outcome: structured — gliders survive and travel, and one crossing the
wrap boundary intact is the single best end-to-end proof that the wrap
logic is correct (REQ-14.2).
"""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.helpers import bind_helpers

_helpers = bind_helpers("all_8", 1)
count_neighbors = _helpers["count_neighbors"]


def next_generation(cells):
    """One Life step: a live cell survives with 2 or 3 live neighbors,
    an empty cell comes alive with exactly 3. Shared with tests that
    plant specific shapes.
    """
    alive = cells.kind == 1
    crowd = count_neighbors(cells, "kind", 1)
    keeps_living = alive & ((crowd == 2) | (crowd == 3))
    comes_alive = ~alive & (crowd == 3)
    return make_cells((keeps_living | comes_alive).astype(np.uint8))


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
        # A random soup: roughly a third of cells start alive.
        return make_cells(self.dice.chance(0.35).astype(np.uint8))

    def step(self, cells):
        return next_generation(cells)
