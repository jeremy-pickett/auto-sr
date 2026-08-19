class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = ["age"]
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "age"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(self.dice.chance(0.3).astype(np.uint8))

    def step(self, cells):
        keep = cells.age >= 0
        return make_cells(np.where(keep, cells.kind, 0).astype(np.uint8))
