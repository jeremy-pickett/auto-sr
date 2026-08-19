"""The `slow_burn` fixture — test-only, never shown in the library
(REQ-14.4). It counts in hidden memory for sixty ticks with the picture
completely still, then flips kind. It exists solely to prove that a
quiet pattern never terminates a run (REQ-9.8.1).
"""

import numpy as np

from asr.engine.cells import make_cells

FLIP_AT = 60


class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = ["memory"]
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "memory"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(
            np.zeros((height, width), dtype=np.uint8),
            memory=np.zeros((height, width), dtype=np.uint8),
        )

    def step(self, cells):
        counted = np.minimum(cells.memory.astype(np.int32) + 1, 255).astype(np.uint8)
        flipped = np.where(counted >= FLIP_AT, np.uint8(1), cells.kind).astype(np.uint8)
        return make_cells(flipped, memory=counted)
