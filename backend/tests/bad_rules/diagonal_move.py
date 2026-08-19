class Rule:
    KINDS = 2
    NEIGHBORS = "plus_4"
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
        return make_cells(self.dice.chance(0.3).astype(np.uint8))

    def step(self, cells):
        slid = move(cells, "kind", HEADING.ne)
        return make_cells(slid.copy())
