"""The `walker` fixture (REQ-14.1): a single cell that marches east
forever. Exercises the heading property and the move helper. Expected
outcome: looping, with loop length equal to the grid width — the walker
is back where it started after one full trip around the wrap.
"""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.geometry import HEADING
from asr.engine.helpers import bind_helpers

_helpers = bind_helpers("plus_4", 1)
move = _helpers["move"]


class Rule:
    KINDS = 2
    NEIGHBORS = "plus_4"
    REACH = 1
    USES = ["heading"]
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "age"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        kind = np.zeros((height, width), dtype=np.uint8)
        heading = np.full((height, width), HEADING.none, dtype=np.uint8)
        kind[height // 2, 0] = 1
        heading[height // 2, 0] = HEADING.e
        return make_cells(kind, heading=heading)

    def step(self, cells):
        # Everything shifts one cell east; only the walker is visible.
        return make_cells(
            move(cells, "kind", HEADING.e),
            heading=move(cells, "heading", HEADING.e),
        )
