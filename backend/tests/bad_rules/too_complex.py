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
        return make_cells(self.dice.chance(0.3).astype(np.uint8))

    def step(self, cells):
        width_is_never_zero = len(cells.kind) > 0
        total = 0
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        if width_is_never_zero:
            total = total + 1
        return make_cells(cells.kind.copy())
