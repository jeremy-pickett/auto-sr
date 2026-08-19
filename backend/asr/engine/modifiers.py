"""The v1 modifier set (spec section 5.4) and what the engine needs to
apply it.

A modifier is an optional per-cell property that changes HOW a rule is
applied, never WHAT the rule is. Every default is an identity — a value
at which the modifier does nothing at all (REQ-5.1); that is checked by
test, not trusted (REQ-15.2). The harness owns these arrays: rules may
read them, never write them (REQ-4.5).
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ModifierSpec:
    name: str
    dtype: type  # smallest numpy int that fits the range (section 5.2)
    lowest: int
    highest: int
    identity: int  # the do-nothing default (REQ-5.1)
    assign_when: str  # "start" (terrain-like) or "birth" (current occupant's)
    effect: str
    availability: str  # evaluated at generation time (REQ-5.3.3)
    blurb: str  # the generator's only description of it (REQ-5.3.4)


MODIFIER_CATALOG = {
    "weight": ModifierSpec(
        name="weight",
        dtype=np.uint8,
        lowest=1,
        highest=4,
        identity=1,
        assign_when="birth",
        effect="counts_as",
        availability="sometimes(0.3)",
        blurb="How strongly this cell counts when its neighbors tally it up.",
    ),
    "stubbornness": ModifierSpec(
        name="stubbornness",
        dtype=np.uint8,
        lowest=0,
        highest=3,
        identity=0,
        assign_when="birth",
        effect="refuses_change",
        availability="sometimes(0.3)",
        blurb=(
            "A cell refuses to change kind until it has held its current "
            "kind at least this many ticks."
        ),
    ),
    "rate": ModifierSpec(
        name="rate",
        dtype=np.uint8,
        lowest=1,
        highest=4,
        identity=1,
        assign_when="start",
        effect="skips_ticks",
        availability="sometimes(0.3)",
        blurb=(
            "The cell only takes its turn on ticks that divide evenly by "
            "this; on the other ticks it keeps its old values."
        ),
    ),
}
