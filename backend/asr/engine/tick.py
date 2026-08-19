"""Building tick 0 and advancing one tick (spec sections 4.6 and 6.4).

The order of operations here is part of the specification — changing it
changes rule semantics. The rule proposes; the harness disposes: every
modifier gate and every random draw below belongs to the harness, which
is the only thing that touches `dice` after tick 0 (REQ-6.6).

Draw order is fixed so runs replay exactly from a seed: modifiers in
name-sorted order, then semantic slots in name-sorted order, start
assignments before birth assignments at tick 0 (REQ-4.6).
"""

import numpy as np

from .cells import Cells, merge_cells
from .declaration import Declaration
from .dice import Dice
from .modifiers import MODIFIER_CATALOG

AGE_CEILING = 65535  # age saturates instead of wrapping (section 4.3)


def start_grid(rule, declaration: Declaration, width: int, height: int, dice: Dice) -> Cells:
    """The exact tick-0 sequence of REQ-4.6."""
    # 1. The rule builds its own arrays through make_cells.
    cells = rule.make_start(width, height)
    if not isinstance(cells, Cells):
        raise ValueError("make_start must return a Cells built with make_cells")
    if set(cells._rule_owned) != set(declaration.rule_owned()):
        raise ValueError(
            f"make_start built {cells._rule_owned} but the declaration owns "
            f"{declaration.rule_owned()}"
        )
    shape = (height, width)
    if cells._shape() != shape:
        raise ValueError(f"make_start built {cells._shape()}, wanted {shape}")

    # 2. Every in-scope modifier and slot array at its identity default.
    for name in sorted(declaration.modifiers):
        spec = MODIFIER_CATALOG[name]
        cells._set(name, np.full(shape, spec.identity, dtype=spec.dtype))
    for name in sorted(declaration.semantic_slots):
        # Index 0 is the slot's mandatory identity value (REQ-5.5).
        cells._set(name, np.zeros(shape, dtype=np.uint8))

    # 3. Start draws, then 4. birth draws with every cell newly born —
    # at tick 0 the two produce statistically identical results and
    # diverge only afterward (REQ-4.6.1).
    everyone = np.ones(shape, dtype=bool)
    _apply_draws(cells, everyone, dice, declaration, when="start")
    _apply_draws(cells, everyone, dice, declaration, when="birth")

    # 5. Birth assignment and the derived birth flag are separate
    # concepts: tick 0 starts unaged and unchanged (REQ-4.6.2).
    cells._set("age", np.zeros(shape, dtype=np.uint16))
    cells._set("changed_last_tick", np.zeros(shape, dtype=bool))
    return cells


def apply_tick(rule, declaration: Declaration, cells: Cells, tick: int, dice: Dice) -> Cells:
    """Advance one tick, applying all harness-owned semantics in the
    exact order of REQ-6.4. `tick` is the number of the tick being
    produced. The rule cannot consume randomness here (REQ-7.4.1);
    every draw is the harness's.
    """
    # 1. The rule proposes a whole next grid. It sees pre-tick age, so
    #    the stubbornness gate below uses the age entering the tick.
    proposed = rule.step(cells)
    if not isinstance(proposed, Cells):
        raise ValueError("step must return a Cells built with make_cells")
    if set(proposed._rule_owned) != set(cells._rule_owned):
        raise ValueError(
            f"step built {proposed._rule_owned} but the grid owns {cells._rule_owned}"
        )
    if proposed._shape() != cells._shape():
        raise ValueError(
            f"step built a {proposed._shape()} grid but received {cells._shape()}"
        )
    # The proposal carries only rule-owned arrays; the harness carries
    # everything else forward, unchanged because the rule cannot write
    # any of it (REQ-4.5).
    for name in cells._names():
        if not proposed._has(name):
            proposed._set(name, cells._arrays[name])

    # 2. `rate` gate: cells not scheduled this tick keep their previous
    #    values entirely — the proposal for them is discarded, not
    #    blended — so they neither reset age nor trigger a birth draw.
    if "rate" in declaration.modifiers:
        scheduled = (tick % cells._arrays["rate"]) == 0
        proposed = merge_cells(scheduled, proposed, cells)

    # 3. `stubbornness` gate: a kind change is refused until the cell
    #    has held its current kind long enough. Pre-tick age.
    if "stubbornness" in declaration.modifiers:
        proposed._set(
            "kind",
            np.where(
                cells._arrays["age"] >= cells._arrays["stubbornness"],
                proposed._arrays["kind"],
                cells._arrays["kind"],
            ),
        )

    # 4. Birth draws, only for cells whose kind actually changed after
    #    the gates. Skipped entirely when nothing was born (REQ-5.6.2):
    #    that is what lets a settled system stop touching the RNG and
    #    become exactly frozen (REQ-9.7.7).
    born = proposed._arrays["kind"] != cells._arrays["kind"]
    if born.any():
        _apply_draws(proposed, born, dice, declaration, when="birth")

    # 5. Derived properties last, so they describe the tick that just
    #    ended. A cell gated by rate still ages on ticks it skipped
    #    (REQ-4.3.1); age saturates rather than wrapping.
    proposed._set("changed_last_tick", born)
    older = np.minimum(
        cells._arrays["age"].astype(np.uint32) + 1, AGE_CEILING
    ).astype(np.uint16)
    proposed._set("age", np.where(born, np.uint16(0), older))

    return proposed


def _apply_draws(cells: Cells, born, dice: Dice, declaration: Declaration, when: str) -> None:
    """Perform the declared assignment draws for one moment (`start` or
    `birth`) over the whole grid, masked down to the affected cells —
    never per cell in a loop (REQ-5.6).

    An assignment declares {"value": v, "chance": p}: each affected cell
    gets v with probability p, its identity value otherwise.
    """
    for name in sorted(declaration.modifiers):
        spec = MODIFIER_CATALOG[name]
        wanted = declaration.assign.get(name)
        if spec.assign_when != when or not wanted:
            continue
        drawn = dice.chance(wanted["chance"])
        value = spec.dtype(wanted["value"])
        fresh = np.where(drawn, value, spec.dtype(spec.identity))
        cells._set(name, np.where(born, fresh, cells._arrays[name]).astype(spec.dtype))

    for name in sorted(declaration.semantic_slots):
        slot = declaration.semantic_slots[name]
        wanted = slot.get("assign")
        if slot.get("assign_when") != when or not wanted:
            continue
        drawn = dice.chance(wanted["chance"])
        value = np.uint8(slot["values"].index(wanted["value"]))
        fresh = np.where(drawn, value, np.uint8(0))
        cells._set(name, np.where(born, fresh, cells._arrays[name]).astype(np.uint8))
