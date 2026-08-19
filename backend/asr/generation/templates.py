"""Prompt templates as files (REQ-10.1) and their rendering.

Templates are the highest-leverage artifact in the project: they live
in version control, are hashed together into prompt_set_hash
(REQ-10.5), and every fully rendered prompt is stored per rule
(REQ-12.4.1) — the coverage summary injected into Stage A *is* the
reasoning input, and without it the corpus cannot answer what the
generator was looking at.
"""

import hashlib
import re
from pathlib import Path

from asr.contract.namespace import (
    APPROVED_ARRAY_METHODS,
    APPROVED_NUMPY_DTYPES,
    APPROVED_NUMPY_FUNCTIONS,
)
from asr.generation.context import CONCEPT_VOCABULARY

PROMPT_DIRECTORY = Path(__file__).resolve().parent / "prompts"
TEMPLATE_FILES = ("stage_a.txt", "stage_b.txt", "repair.txt")


def load_template(name: str) -> str:
    return (PROMPT_DIRECTORY / name).read_text()


def prompt_set_hash() -> str:
    """One stamp over the whole template set (REQ-10.5). The concept
    vocabulary rides along: it is part of what the generator was told.
    """
    digest = hashlib.blake2b(digest_size=16)
    for name in TEMPLATE_FILES:
        digest.update(name.encode())
        digest.update((PROMPT_DIRECTORY / name).read_bytes())
    digest.update("|".join(CONCEPT_VOCABULARY).encode())
    return digest.hexdigest()


def render(template: str, values: dict) -> str:
    """Fill {name} placeholders for the given names only — the JSON
    braces in the templates themselves stay untouched.
    """
    pattern = re.compile("|".join(r"\{" + re.escape(name) + r"\}" for name in values))
    return pattern.sub(lambda match: str(values[match.group()[1:-1]]), template)


# ---- static blocks injected into the templates ------------------------

CELL_SCHEMA = """\
Every cell has a `kind` (which of your KINDS it currently is; kind 0 is
the empty ground). A rule may also own extra whole-number properties
(0..255 each), declared in USES: `energy`, `heading`, or `memory`.
The harness additionally maintains two read-only derived properties —
`age` (ticks since this cell last changed kind) and `changed_last_tick`
— which a rule may read only if declared in READS."""

GEOMETRY_SPEC = """\
The grid wraps around at every edge (top meets bottom, left meets
right). NEIGHBORS is "all_8" (the full ring of surrounding cells) or
"plus_4" (up, down, left, right only). REACH 1, 2, or 3 says how far
away still counts as a neighbor. A cell is never its own neighbor.
Helpers do all neighbor lookups; the rule never indexes the grid by
position."""

SLOTS_AVAILABILITY = """\
You may declare up to two named enum properties of your own invention
("mood", "role", ...) — a hook for meaning. Each needs at least two
values with the identity value listed first, an assign_when of "start"
or "birth", and optionally an assign draw:
  "semantic_slots": {"mood": {"values": ["none", "restless"],
                              "assign_when": "birth",
                              "assign": {"value": "restless", "chance": 0.05}}}
The harness owns these arrays and performs every draw; your rule can
read them (MOOD.restless) but never write them. Use {} for none."""

PLUGIN_CONTRACT = """\
class Rule:
    KINDS: int              # how many kinds a cell can be, 2..8
    NEIGHBORS: str          # "all_8" or "plus_4"
    REACH: int              # how far away still counts as a neighbor, 1..3
    USES: list[str]         # optional core properties, e.g. ["energy"]
    READS: list[str]        # derived properties read, e.g. ["age"]
    MODIFIERS: list[str]    # catalog modifiers in scope
    SEMANTIC_SLOTS: dict    # your enum slots, or {}
    ASSIGN: dict            # modifier draws, or {}
    SUGGESTED_DISPLAY: dict # e.g. {"color": "kind", "brightness": "energy"}

    def __init__(self, dice):
        self.dice = dice    # usable in make_start only

    def make_start(self, width, height):
        \"\"\"Build the tick-0 grid via make_cells. The only place
        randomness is permitted.\"\"\"

    def step(self, cells):
        \"\"\"Return the NEXT grid. Deterministic. Must not modify its
        input.\"\"\""""

HELPER_SIGNATURES = """\
Spatial helpers (already bound to your declared neighborhood; they wrap
around the grid edges automatically):
- look(cells, prop, down, right) -> array: a neighbor's values as seen
  from each cell. Both offsets must be literal integers inside your
  declared neighborhood.
- move(cells, prop, direction) -> array: the property displaced exactly
  one cell toward a HEADING constant (HEADING.n, HEADING.ne, HEADING.e,
  ... HEADING.none). plus_4 rules cannot move diagonally.
- count_neighbors(cells, prop, value) -> array: how many neighbors have
  prop equal to value.
- count_neighbors_where(cells, mask) -> array: how many neighbors
  satisfy a boolean array you computed.
- sum_neighbors(cells, prop) -> array: the total of neighbors' values.
- make_cells(kind, **extra) -> Cells: build a grid from your arrays.
  kind must be uint8; extras must match your USES declaration."""

DICE_FACADE = """\
self.dice (make_start only) — every method fills the whole grid at once:
- self.dice.chance(p) -> boolean array, True with probability p
- self.dice.integers(low, high) -> int32 array, uniform in [low, high)
- self.dice.choice(n) -> int32 array, uniform in [0, n)
Cast into your uint8 arrays with .astype(np.uint8)."""


def approved_numpy_surface() -> str:
    functions = ", ".join("np." + name for name in APPROVED_NUMPY_FUNCTIONS)
    dtypes = ", ".join("np." + name for name in APPROVED_NUMPY_DTYPES)
    methods = ", ".join("." + name for name in APPROVED_ARRAY_METHODS)
    return (
        "Approved numpy surface (nothing else exists):\n"
        f"- functions: {functions}\n"
        f"- dtypes: {dtypes}\n"
        f"- array methods: {methods}\n"
        "- array operators work as usual: + - * // % == != < <= > >= & | ~ ^"
    )


def concept_vocabulary_block() -> str:
    return ", ".join(CONCEPT_VOCABULARY)
