# Engine Internals

> **Release 2.2.1** · documented 2026-08-20 · **unchanged in 2.2.1.**
> `backend/asr/engine/` has no diff against the 2.2.0 text of this document; it was
> re-verified against the source at this release rather than assumed current. Neither
> feature family in 2.2.1 — the system page and the uplift-2.2 §8 render styles —
> touches the engine. Both are, by design, downstream of it: the render styles are
> display-only (REQ-13.16, REQ-13.2) and cannot reach a fingerprint, and the system
> page reads session bookkeeping that no engine code is aware of.

This is part 1 of a six-part deep-dive series on Autonomous Semantic Ruliology (ASR), covering `backend/asr/engine/` — the deterministic core that every rule, generated or hand-written, runs on top of. Everything here is upstream of generation (Stage A/B/C) and storage: the engine defines what a cellular-automaton "rule" is allowed to be, what a "tick" means, and what "the same state twice" means. Every code excerpt below is quoted verbatim from the repository with file and line numbers so it can be checked against the source.

The engine package has ten files:

```
backend/asr/engine/
  cells.py         the grid container
  declaration.py   what a rule declares about itself
  geometry.py       neighborhood shapes and headings
  helpers.py        neighbor-lookup functions bound to one declaration
  dice.py           the only source of randomness
  modifiers.py       the v1 modifier catalog
  tick.py           tick-0 construction and one-tick advance
  fingerprint.py     computational vs. pattern fingerprints
  run.py             the run loop and stopping conditions
  classify.py        the deterministic outcome classifier
```

The governing idea, stated in `CLAUDE.md` and enforced throughout this code, is that **a rule proposes and the harness disposes**. A generated rule's `step` method returns what it *wants* the next grid to look like; the engine — never the rule — applies modifiers, performs every random draw, computes derived properties, and decides whether the run has stopped. This split is not a style preference. It is what makes 50,000 LLM-written rules replayable, comparable, and safe to run unattended: the part of the system an LLM writes is small, pure, and cannot touch randomness or bookkeeping, and the part that can is fixed, tested engine code.

---

## 1. The state model

### 1.1 A cell is not an object

REQ-4.1 states it plainly: "A cell is a set of named, typed properties stored as **parallel numpy arrays** of shape `(height, width)` — one array per property, never an array of cell objects." There is no `Cell` class anywhere in this codebase. A 200×200 grid over 500 ticks is 20 million cell updates; the architecture doc's rationale table gives exactly this as the reason (`documents/asr-requirements-v3.md:104`). Every property — `kind`, `age`, `weight`, `heading`, whatever — is one whole `numpy` array the size of the grid. "This cell's kind" is `kind[row, col]`; "all cells with kind 1" is `kind == 1`, a vectorized boolean array, not a loop.

### 1.2 `Cells`: a named bag of arrays, not an array-like

`Cells` (`backend/asr/engine/cells.py:28-75`) is the container that groups those parallel arrays together. It is deliberately inert — no arithmetic, no broadcasting, no public constructor:

```python
class Cells:
    """A named bag of same-shaped arrays. Read a property as an
    attribute: cells.kind, cells.energy. Rule code can never assign
    one (REQ-4.5); the harness writes through the private _set.
    """

    __slots__ = ("_arrays", "_rule_owned")

    def __init__(self, *_args, **_kwargs):
        raise TypeError(
            "Cells has no public constructor; build a grid with make_cells (REQ-6.2)"
        )
```
(`backend/asr/engine/cells.py:28-39`)

Instantiating `Cells()` directly always raises. The only way anything — generated rule code or the harness itself — gets a `Cells` instance is through the `_assemble` classmethod, called by `make_cells` (below) or by the harness's own tick machinery. Reading a property is attribute access (`cells.kind`), routed through `__getattr__` into a private dict; *writing* one is blocked outright:

```python
def __setattr__(self, name, _value):
    raise AttributeError(
        f"cell property arrays are read-only to rule code; "
        f"cannot assign {name!r} (REQ-4.5)"
    )
```
(`backend/asr/engine/cells.py:56-60`)

This is a second, runtime net underneath the AST-level Stage C validator — `documents/architecture.md:41-43` calls it out explicitly: "`Cells` is write-protected at runtime too. Attribute assignment raises; the harness mutates through a private `_set`. The AST validator remains the primary enforcement (REQ-4.5), this is a second net." The harness's own code never uses the public interface either — it always goes through `_set`, `_has`, `_names`, `_shape`, all underscore-prefixed and therefore already unreachable to generated code even before the static validator runs (the restricted namespace has no dunder/underscore attribute access at all — REQ-7.8 item 2).

### 1.3 Building a grid: `make_cells`

The only way a rule constructs a `Cells` is `make_cells` (`backend/asr/engine/cells.py:78-107`):

```python
def make_cells(kind, **core_properties) -> Cells:
    """Build a grid from rule-owned arrays. The only way generated code
    creates a Cells (REQ-6.2).
    ...
    """
    if not isinstance(kind, np.ndarray) or kind.ndim != 2:
        raise ValueError("kind must be a 2-D numpy array")
    if kind.dtype != np.uint8:
        raise ValueError(f"kind must have dtype uint8, got {kind.dtype}")

    arrays = {"kind": kind}
    for name, array in core_properties.items():
        wanted_dtype = OPTIONAL_CORE_PROPERTIES.get(name)
        if wanted_dtype is None:
            raise ValueError(
                f"{name!r} is not a core property; the choices are "
                f"{tuple(OPTIONAL_CORE_PROPERTIES)}"
            )
        if not isinstance(array, np.ndarray) or array.shape != kind.shape:
            raise ValueError(f"{name} must be a numpy array shaped like kind {kind.shape}")
        if array.dtype != wanted_dtype:
            raise ValueError(f"{name} must have dtype {np.dtype(wanted_dtype)}, got {array.dtype}")
        arrays[name] = array

    return Cells._assemble(arrays, tuple(arrays))
```

`kind` is mandatory, must be 2-D `uint8`. Keyword arguments name **optional core properties**, defined in the same file:

```python
OPTIONAL_CORE_PROPERTIES = {
    "energy": np.uint8,
    "heading": np.uint8,
    "memory": np.uint8,
}

DERIVED_PROPERTIES = {
    "age": np.uint16,
    "changed_last_tick": np.bool_,
}
```
(`backend/asr/engine/cells.py:15-25`)

Note what `make_cells` does *not* accept: modifier arrays (`weight`, `stubbornness`, `rate`), semantic-slot arrays, or the two derived arrays. Those are allocated and attached by the harness after `make_start` returns, and after every `step` returns — a rule can never construct or overwrite them, because `make_cells` is structurally the only entry point and it does not offer a keyword for them. `documents/architecture.md:44-48` calls this out as a deliberate design choice: "`step()` returns a rule-owned-only grid... This keeps `make_cells` the single construction path (REQ-6.2) and makes it structurally impossible for a rule to alter a modifier array."

### 1.4 What a rule declares about itself: the `Declaration`

Every rule class carries a fixed set of class attributes — `KINDS`, `NEIGHBORS`, `REACH`, `USES`, `READS`, `MODIFIERS`, `SEMANTIC_SLOTS`, `ASSIGN` — and `Declaration` (`backend/asr/engine/declaration.py`) is the engine's validated, structured read of them:

```python
@dataclass(frozen=True)
class Declaration:
    kinds: int
    neighbors: str
    reach: int
    uses: tuple = ()
    reads: tuple = ()
    modifiers: tuple = ()
    semantic_slots: dict = field(default_factory=dict)
    assign: dict = field(default_factory=dict)
```
(`backend/asr/engine/declaration.py:19-28`)

Each field means:

- **`KINDS`** — how many distinct values `kind` can take, `2..8` (`KINDS_RANGE = (2, 8)`, `declaration.py:16`). This is the cell's fundamental type; a Life-like rule uses `KINDS = 2` (dead/alive).
- **`NEIGHBORS`** and **`REACH`** — together they pick the neighborhood shape (`all_8` or `plus_4`) and how far it extends (1–3). Section 2 below covers geometry in detail.
- **`USES`** — which *optional core properties* (`energy`, `heading`, `memory`) this rule owns and rewrites every tick, beyond the mandatory `kind`. `Declaration.rule_owned()` (`declaration.py:107-109`) returns `("kind",) + tuple(self.uses)` — exactly the set of arrays a rule's `make_start`/`step` are responsible for building.
- **`READS`** — which *derived* properties (`age`, `changed_last_tick`) the rule's `step` is allowed to read. This matters for more than access control: REQ-4.3.2 ties it directly into loop detection ("`READS` feeds the computational fingerprint (REQ-9.7.1), so an undeclared read silently corrupts loop detection" — `documents/asr-requirements-v3.md:172-175`). If a rule secretly read `age` without declaring it, two grids with identical `kind`/modifier arrays but different `age` would hash to the same computational fingerprint even though they have different futures.
- **`MODIFIERS`** — which of the harness-applied modifiers (`weight`, `stubbornness`, `rate` — see §3) are in scope for this rule.
- **`SEMANTIC_SLOTS`** — up to two named enum properties the rule itself defines (e.g. `mood: [none, restless, settled]`), capped at two by `__post_init__` (`declaration.py:90-91`, REQ-5.5).
- **`ASSIGN`** — the harness-performed random assignment for each in-scope modifier or slot: `{"value": v, "chance": p}`. The rule never draws; it only declares the odds. `__post_init__` validates the shape of every `ASSIGN` entry strictly — it must name a modifier actually in `MODIFIERS`, its value must be an integer inside the modifier's declared range, and its chance must be in `[0, 1]` (`declaration.py:44-66`).

`Declaration.from_rule(rule_class)` (`declaration.py:93-105`) is how the engine turns a loaded `Rule` class into one of these; Stage C's "declaration match" check (REQ-7.8 item 3) is exactly a comparison between what Stage A declared and what `Declaration.from_rule` reads off the implementation — any mismatch means "the implementation silently rewrote the experiment" and the rule is rejected.

One more method earns a close look, because it drives whether a run's RNG state has to be tracked for loop detection:

```python
def declares_birth_draws(self) -> bool:
    """Whether any draw happens after tick 0 — the condition for the
    RNG state joining the computational fingerprint (REQ-9.7.1).
    """
    for name in self.modifiers:
        if MODIFIER_CATALOG[name].assign_when == "birth" and name in self.assign:
            return True
    for slot in self.semantic_slots.values():
        if slot.get("assign_when") == "birth" and slot.get("assign"):
            return True
    return False
```
(`declaration.py:111-121`)

This is used by `fingerprint.py` (§6) to decide whether the RNG state is future-relevant for this particular rule.

### 1.5 The shape of a rule plugin

A generated (or hand-written) rule is a single class with declarations and exactly two methods:

```python
class Rule:
    KINDS: int
    NEIGHBORS: str
    REACH: int
    USES: list[str]
    READS: list[str]
    MODIFIERS: list[str]
    SEMANTIC_SLOTS: dict
    ASSIGN: dict
    SUGGESTED_DISPLAY: dict

    def __init__(self, dice) -> None:
        """`dice` may be used in make_start only. See REQ-7.4.1."""

    def make_start(self, width: int, height: int) -> Cells:
        """Build the tick-0 grid via make_cells. The only place randomness
        is permitted."""

    def step(self, cells: Cells) -> Cells:
        """Return the NEXT grid. Deterministic. Must not modify its input."""
```
(`documents/asr-requirements-v3.md:533-553`, REQ-7.1)

`make_start` and `step` split the two things a cellular automaton needs — an initial condition and a transition law — along exactly the line where randomness is or isn't allowed. `make_start` receives `self.dice` (the `Dice` facade, §4) and is the *only* place a rule may draw random numbers, because it only ever runs once, at construction of tick 0. `step` is called once per subsequent tick and must be a pure function of the `cells` it is handed: REQ-7.4.1 is unambiguous — "`self.dice` may appear only inside `make_start`. Any reference in `step` is a validation failure." The `life` fixture shows the pattern cleanly:

```python
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
        # A live cell survives with 2 or 3 live neighbors; an empty
        # cell comes alive with exactly 3.
        alive = cells.kind == 1
        crowd = count_neighbors(cells, "kind", 1)
        keeps_living = alive & ((crowd == 2) | (crowd == 3))
        comes_alive = ~alive & (crowd == 3)
        return make_cells((keeps_living | comes_alive).astype(np.uint8))
```
(`backend/asr/fixtures/life.py:22-47`)

`self.dice` appears in `make_start`, never in `step`. `__init__` stores `dice` as an instance attribute — permitted, because REQ-7.4 allows "constants set in `__init__`," but nothing in `step` ever assigns to `self`, and the engine's Stage C static checker rejects any `step` that does. `step` never touches `cells` in place; it computes new boolean arrays and returns a brand-new `Cells` built with `make_cells`. Why the "must not modify its input" rule (REQ-7.5) matters mechanically: `run.py` (§7) marks every array read-only (`setflags(write=False)`) right after it's produced, specifically so an in-place write inside `step` raises immediately instead of silently corrupting recorded tick history (`backend/asr/engine/run.py:105-114`).

`SUGGESTED_DISPLAY` is the odd one out — it is advisory only, telling the UI which property to map to color and which to brightness. REQ-7.1.1 is explicit that it "never affects any fingerprint."

---

## 2. Geometry

`geometry.py` defines the grid's two neighborhood shapes and the wraparound rule, all in plain-language terms per REQ-0.1, with the standard mathematical term named once in a comment.

### 2.1 Wraparound (toroidal) edges

The module docstring states the rule up front: "Grid edges always wrap: top to bottom, left to right. (Standard term: toroidal.)" (`backend/asr/engine/geometry.py:1-6`). There is no special-casing of edge cells anywhere in the engine; wrapping is implemented, once, via `numpy.roll` inside the bound helpers (§3) — `np.roll` cycles array elements around an axis, which is exactly toroidal wraparound. Every helper that looks at a neighbor or moves a cell uses `np.roll`, so wraparound is not a rule that generated code needs to know about or could get wrong — it is baked into the only mechanism a rule has for touching another cell.

### 2.2 Offsets, neighborhoods, and reach

An offset is a `(down, right)` pair — "rows toward the bottom of the screen and columns toward the right" (`geometry.py:5-6`). Two neighborhood shapes exist, `all_8` and `plus_4`, each parameterized by `REACH` (1–3):

```python
def neighbor_offsets(neighbors: str, reach: int) -> tuple[tuple[int, int], ...]:
    """Every (down, right) offset that counts as a neighbor (REQ-6.3).

    all_8 at reach r is the whole surrounding square, (2r+1)**2 - 1 cells
    (standard term: Chebyshev distance <= r), never the cell itself.
    plus_4 at reach r is the four straight rays up, down, left, right --
    4r cells, deliberately NOT the diamond (REQ-6.3.2), so "plus_4" keeps
    its plus-sign meaning at every reach.
    """
    check_geometry(neighbors, reach)
    offsets: list[tuple[int, int]] = []
    if neighbors == "all_8":
        for down in range(-reach, reach + 1):
            for right in range(-reach, reach + 1):
                if (down, right) != (0, 0):
                    offsets.append((down, right))
    else:
        for step in range(1, reach + 1):
            offsets.extend([(-step, 0), (step, 0), (0, -step), (0, step)])
    return tuple(offsets)
```
(`backend/asr/engine/geometry.py:55-74`)

`all_8` at reach *r* is the full `(2r+1)² − 1` surrounding square (8, 24, 48 cells at r=1,2,3), excluding the cell itself — `(0, 0)` is never included, which is the engine's guarantee that "a cell is never its own neighbor." `plus_4` is *not* the Manhattan diamond you'd get by simply extending a plus-sign shape at longer range — REQ-6.3.2 is explicit that this is a deliberate choice, "so `plus_4` keeps its intuitive meaning at every reach": it is always exactly the four straight rays (up, down, left, right), `4r` cells total, never diagonal, never widening into a diamond.

`REACH` and `NEIGHBORS` together are also what bounds `move`'s direction set:

```python
def allowed_move_headings(neighbors: str) -> tuple[str, ...]:
    """Which headings `move` accepts (REQ-6.3.3): the four straight ones
    for plus_4, all eight for all_8. Reach never matters -- move always
    displaces by exactly one cell (REQ-6.2.3).
    """
    if neighbors == "plus_4":
        return ("n", "e", "s", "w")
    if neighbors == "all_8":
        return ("n", "ne", "e", "se", "s", "sw", "w", "nw")
```
(`geometry.py:77-86`)

Note the last line of that docstring: reach never affects `move` — a walker always displaces by exactly one cell regardless of how far the rule can *look*. This is the "looking vs. moving are separate operations" distinction covered in §3.

### 2.3 Headings as enum constants, not strings

Directions are stored as `uint8`, never strings, per REQ-5.2.1 ("Anything that wants to be a string is an enum. Rule code reads `HOLIDAY.halloween`, never `"halloween"`" — a numpy grid of strings would be fixed-width bytes or object dtype, both of which destroy vectorization):

```python
HEADING_NAMES = ("n", "ne", "e", "se", "s", "sw", "w", "nw", "none")

HEADING_OFFSETS = {
    "n": (-1, 0),
    "ne": (-1, 1),
    "e": (0, 1),
    "se": (1, 1),
    "s": (1, 0),
    "sw": (1, -1),
    "w": (0, -1),
    "nw": (-1, -1),
}


class HEADING:
    n = 0
    ne = 1
    e = 2
    se = 3
    s = 4
    sw = 5
    w = 6
    nw = 7
    none = 8
```
(`geometry.py:8-37`)

Row 0 is the top of the grid, so heading `n` (north) is `(-1, 0)` — negative `down` — which the module notes explicitly (`geometry.py:11`). `HEADING.none = 8` is the "not moving / not applicable" value, used for cells with no direction (like every cell in the `walker` fixture except the one walker cell — see the worked example, §9).

---

## 3. Bound helpers: the only way to touch a neighbor

### 3.1 Why bound, not free functions

`helpers.py`'s docstring states the reason for existing directly: "`bind_helpers(neighbors, reach)` bakes the declared neighborhood into every helper before rule code ever sees them, so a rule can never look or reach farther than its declaration — and its coverage entry — claims. There is no unbound shift anywhere (REQ-6.2.3)." (`backend/asr/engine/helpers.py:1-10`). The rationale table in the spec puts it even more sharply: "An unbound `shift` lets a REACH=1 rule reach seventeen cells and quietly falsify its own coverage entry" (`documents/asr-requirements-v3.md:98`). Since Stage A's generation context — the coverage map — is keyed partly on `REACH`, a rule that could silently reach further than declared would corrupt the very data the generator learns from.

`bind_helpers(neighbors, reach)` (`helpers.py:22-115`) is a closure factory: it computes the declared offset set *once*, and every helper function it returns checks against that closed-over set. Generated code never calls `bind_helpers` itself — the harness calls it once per rule, using the rule's own `NEIGHBORS`/`REACH` declaration, and drops the resulting functions into the restricted execution namespace before the rule's code ever runs. Fixtures reproduce this exactly, e.g. `life.py`:

```python
count_neighbors = bind_helpers("all_8", 1)["count_neighbors"]
```
(`backend/asr/fixtures/life.py:19`)

### 3.2 The five bound helpers

```python
def bind_helpers(neighbors: str, reach: int) -> dict:
    offsets = neighbor_offsets(neighbors, reach)
    offset_set = set(offsets)
    move_headings = allowed_move_headings(neighbors)

    def _weight(cells):
        # When `weight` is in scope each neighbor contributes its own
        # weight instead of 1 — the only thing weight does (REQ-5.4.1).
        # Rules do not opt in.
        return cells._arrays["weight"] if cells._has("weight") else 1

    def _tally(cells, counts_as):
        # Each neighbor's contribution lands on the cell it neighbors.
        # A cell is never its own neighbor: (0, 0) is not an offset.
        total = np.zeros(cells._shape(), dtype=np.int32)
        for down, right in offsets:
            total += np.roll(counts_as, (-down, -right), axis=(0, 1))
        return total

    def look(cells, prop, down, right):
        if (down, right) not in offset_set:
            raise ValueError(
                f"offset ({down}, {right}) is outside the declared "
                f"neighborhood {neighbors} at reach {reach} (REQ-6.2.1)"
            )
        return np.roll(_property_array(cells, prop), (down, right), axis=(0, 1))

    def move(cells, prop, direction):
        name = HEADING_NAMES[direction]
        if name not in move_headings:
            raise ValueError(
                f"move toward {name!r} is not allowed under {neighbors}; "
                f"the choices are {move_headings} (REQ-6.3.3)"
            )
        return np.roll(_property_array(cells, prop), HEADING_OFFSETS[name], axis=(0, 1))

    def count_neighbors(cells, prop, value):
        match = _property_array(cells, prop) == value
        return _tally(cells, match.astype(np.int32) * _weight(cells))

    def count_neighbors_where(cells, mask):
        ...
        return _tally(cells, mask.astype(np.int32) * _weight(cells))

    def sum_neighbors(cells, prop):
        values = _property_array(cells, prop).astype(np.int32)
        return _tally(cells, values * _weight(cells))

    return {
        "look": look,
        "move": move,
        "count_neighbors": count_neighbors,
        "count_neighbors_where": count_neighbors_where,
        "sum_neighbors": sum_neighbors,
    }
```
(condensed from `backend/asr/engine/helpers.py:22-115`)

Each helper's job:

- **`look(cells, prop, down, right)`** — the value of `prop` at one specific declared offset, wrapped. Rejects any `(down, right)` outside the bound neighborhood, at runtime, unconditionally — this is the runtime backstop behind the static AST check that spatial offsets must be literal (REQ-6.2.2). Positive `down` "brings the UPSTAIRS neighbor's value into this cell's position" (`helpers.py:56-57`) — `np.roll` with a positive shift along an axis moves each element's *index* forward, which is equivalent to pulling the value from the position *behind* it in that direction.
- **`move(cells, prop, direction)`** — displaces a whole property array by exactly one cell in a `HEADING` direction, independent of `REACH`. `documents/asr-requirements-v3.md:361-364` explains why this exists as a distinct primitive from `look`: "*Looking* and *moving* are separate operations and were accidentally conflated in v2... `move` displaces content by exactly one cell in a declared direction, independent of `REACH`, and exists so walker rules do not need wide reach merely to relocate." A `REACH=1` walker can still move — reach governs *observation* distance, not *displacement* distance.
- **`count_neighbors(cells, prop, value)`** — vectorized tally of how many of each cell's declared neighbors have `prop == value`. This is the single most common helper generated rules use (Life's survival/birth rule is built from it). It is also the *sole* place `weight` (§_5.4) enters a rule's computation, and crucially a rule does not opt in to that: `_weight` checks `cells._has("weight")` itself, so "a generator that forgets weight exists still respects it" (`helpers.py:37-41`, echoing `documents/asr-requirements-v3.md:392-397`).
- **`count_neighbors_where(cells, mask)`** — same tally, but over an arbitrary precomputed boolean condition (e.g. "neighbors with energy above 5") instead of a flat equality test.
- **`sum_neighbors(cells, prop)`** — sums (rather than counts) a numeric property across declared neighbors, same weighting and self-exclusion.

The private `_tally` helper is worth reading closely: for each declared offset, it rolls the "counts as" array by `(-down, -right)` and accumulates. Rolling by the *negative* of the offset is what makes "this cell's tally" equal "the sum, over each neighbor position, of what that neighbor contributes" rather than the other way around — each neighbor's value lands on the cell that is looking at it, not on itself.

`count_neighbors`, `count_neighbors_where`, and `sum_neighbors` all take `cells` (the whole grid container) rather than a bare array specifically so `_weight` can reach `cells._arrays["weight"]` when it exists — this is the mechanical reason those three functions are shaped the way they are (`documents/asr-requirements-v3.md:396-397`).

---

## 4. The Dice facade

### 4.1 Why a facade, and why only in `make_start`

`dice.py`'s docstring is unambiguous about scope: "A thin cover over a seeded numpy random Generator. Only whole-grid draws are exposed, so there is no scalar draw to tempt a per-cell loop... Rule code may touch dice only inside make_start (REQ-7.4.1). After tick 0 the only consumer is the harness's birth assignments (REQ-6.6)." (`backend/asr/engine/dice.py:1-10`). The rationale, from the spec's decision table: "Random initial conditions with a deterministic law is the cleaner experiment, and it removes a class of loop-detection ambiguity" (`documents/asr-requirements-v3.md:97`). If `step` could draw randomly, the same grid at the same tick could have two different possible futures depending on unseen RNG state, which would make the whole notion of an exact "loop" (§6) ill-defined without also hashing RNG state into every single tick's fingerprint — instead the engine confines all post-tick-0 randomness to a single, harness-controlled channel: birth assignment draws.

### 4.2 The full surface

```python
class Dice:
    def __init__(self, seed: int, height: int, width: int):
        self._shape = (height, width)
        self._random = np.random.default_rng(seed)

    def chance(self, p) -> np.ndarray:
        """Boolean array, True with probability p."""
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be between 0 and 1, got {p!r}")
        return self._random.random(self._shape) < p

    def integers(self, low, high) -> np.ndarray:
        """Integer array, uniform in [low, high)."""
        if high <= low:
            raise ValueError(f"high must be above low, got [{low!r}, {high!r})")
        return self._random.integers(low, high, size=self._shape, dtype=np.int32)

    def choice(self, n) -> np.ndarray:
        """Integer array, uniform in [0, n)."""
        if n < 1:
            raise ValueError(f"n must be at least 1, got {n!r}")
        return self._random.integers(0, n, size=self._shape, dtype=np.int32)

    # ---- harness-private surface below.

    def _state_bytes(self) -> bytes:
        """The generator's exact internal state, as stable bytes.

        Feeds the computational fingerprint when birth draws are
        declared (REQ-9.7.1): two grids with different randomness ahead
        of them are different states, even if every array matches.
        """
        return repr(self._random.bit_generator.state).encode("utf-8")
```
(`backend/asr/engine/dice.py:15-47`)

That is the entire class: three public methods, all whole-grid, all filling exactly `(height, width)` in one call — `chance(p)`, `integers(low, high)`, `choice(n)`. There is no scalar draw and no shape parameter; the shape is always the grid, which is precisely what removes the temptation (and the possibility, since a scalar draw simply doesn't exist) to write a per-cell Python loop over random numbers. `documents/asr-requirements-v3.md:522-523` (REQ-6.7.1) states that "Additions to this surface are a spec change requiring a new REQ identifier, not an implementation decision" — `CLAUDE.md` repeats this as a hard rule.

Internally it wraps exactly one `numpy.random.Generator`, seeded once at run start (`np.random.default_rng(seed)`), so a run is fully reproducible from that single integer seed as long as draws happen in a fixed, deterministic order — which `tick.py` (§5) guarantees by always drawing modifiers and slots in name-sorted order.

`_state_bytes()` is underscore-prefixed harness-private surface, unreachable from generated code, and it exists purely to feed the computational fingerprint (§6): the raw `repr()` of the bit generator's internal state, encoded to bytes. This is what makes "the RNG has more draws queued up ahead of it" a distinguishable state from "the RNG has fewer," even when every visible array is byte-identical.

### 4.3 What's off-limits

- `np.random` itself is entirely absent from the restricted NumPy proxy handed to generated code (REQ-7.9.4) — there is no way to reach any random source except through `self.dice`.
- `self.dice` referenced anywhere inside `step` is a Stage C static-validation failure (REQ-7.8 item 2 explicitly lists "`self.dice` outside `make_start`" as a rejection cause).
- No scalar draw exists on `Dice` at all — `chance`, `integers`, and `choice` always return a full `(height, width)` array.

---

## 5. Tick order

`tick.py`'s docstring states the stakes up front: "The order of operations here is part of the specification — changing it changes rule semantics. The rule proposes; the harness disposes: every modifier gate and every random draw below belongs to the harness, which is the only thing that touches `dice` after tick 0 (REQ-6.6)." (`backend/asr/engine/tick.py:1-11`)

### 5.1 Building tick 0

```python
def start_grid(rule, declaration: Declaration, width: int, height: int, dice: Dice) -> Cells:
    """The exact tick-0 sequence of REQ-4.6."""
    # 1. The rule builds its own arrays through make_cells.
    cells = rule.make_start(width, height)
    ...
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
```
(`backend/asr/engine/tick.py:23-57`)

This is REQ-4.6's six-step sequence (`documents/asr-requirements-v3.md:186-195`) implemented directly: (1) the rule builds its own arrays via `make_start`/`make_cells`; (2) every in-scope modifier and slot array is allocated at its **identity** default (§_5.4 explains why identity matters — REQ-5.1); (3) `start`-timed draws happen; (4) `birth`-timed draws happen too, treating *every* tick-0 cell as newly born (`everyone = np.ones(shape, dtype=bool)`); (5) `age` and `changed_last_tick` are forced to zero/False regardless. Step 4 looks redundant with step 3 at first glance, but REQ-4.6.1 explains why it isn't a bug: treating every tick-0 cell as freshly born makes `start`- and `birth`-assigned modifiers statistically identical at tick 0 and only diverge afterward — "the alternative — birth-assigned modifiers being wholly absent until the pattern first churns — makes the initial condition inconsistent with the rule's declared intent." Step 5 then deliberately *overrides* what step 4 might imply about "changed" — REQ-4.6.2 separates "birth assignment" (a modifier value) from "the derived birth flag" (`changed_last_tick`): a cell can be birth-assigned at tick 0 while still correctly reporting `changed_last_tick = False`, because nothing "changed" relative to a prior tick that doesn't exist.

### 5.2 Advancing one tick

```python
def apply_tick(rule, declaration: Declaration, cells: Cells, tick: int, dice: Dice) -> Cells:
    # 1. The rule proposes a whole next grid. It sees pre-tick age, so
    #    the stubbornness gate below uses the age entering the tick.
    proposed = rule.step(cells)
    ...
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
```
(`backend/asr/engine/tick.py:60-122`, condensed for readability but every kept line is verbatim)

Walking it in order:

1. **The rule proposes.** `rule.step(cells)` sees `cells` — including its *pre-tick* `age` array — and returns a new `Cells` containing only rule-owned arrays (`kind` plus whatever `USES` declares). Everything the proposal doesn't carry (modifier arrays, slot arrays — the rule never builds those) is copied straight through from the previous `cells` (`for name in cells._names(): if not proposed._has(name): proposed._set(name, cells._arrays[name])`).
2. **The `rate` gate.** If `rate` is in scope, `scheduled = (tick % cells.rate) == 0` computes which cells are due to update *this* tick, and `merge_cells` (§1.3's sibling function — see below) discards the rule's proposal wholesale for every cell that isn't scheduled, replacing it with that cell's *old* values, unchanged. This is a hard discard, not an interpolation.
3. **The `stubbornness` gate.** If `stubbornness` is in scope, a `kind` change is only allowed through if the cell's age (entering this tick, i.e. pre-tick) is at least its stubbornness value; otherwise the old `kind` wins over the proposed one, cell by cell, via `np.where`.
4. **Birth draws.** `born` is computed as `proposed.kind != cells.kind` — after both gates have already had their say, so a cell that the `rate` gate froze in place, or that `stubbornness` refused to let change, is correctly *not* counted as born. If `born.any()` is `True`, `_apply_draws` runs; if it's `False`, the harness makes **no call into `dice` at all** for this tick. This conditional is the crux of §6's frozen/looping distinction and is discussed there.
5. **Derived properties, last.** `changed_last_tick` is set to exactly the `born` mask just computed. `age` becomes `0` wherever a cell was born, otherwise its old age plus one, saturating (via `np.minimum`) at `AGE_CEILING = 65535` rather than wrapping around to zero. Crucially, this increment happens unconditionally to every non-born cell — including ones the `rate` gate held motionless — which is REQ-4.3.1: "`age` counts elapsed ticks, not update opportunities. A cell gated by `rate` still ages on ticks it skipped."

`merge_cells`, used in step 2, is the `Cells`-aware analogue of `np.where` (`Cells` has no arithmetic, so `np.where` can't apply to it directly):

```python
def merge_cells(mask, chosen_where_true: Cells, chosen_where_false: Cells) -> Cells:
    """HARNESS-PRIVATE field-by-field select across rule-owned arrays. ...
    Everything else (modifier, slot, derived arrays) is carried from
    `chosen_where_true` untouched, because the rule never writes those
    (REQ-4.5).
    """
    if chosen_where_true._rule_owned != chosen_where_false._rule_owned:
        raise ValueError(...)
    arrays = dict(chosen_where_true._arrays)
    for name in chosen_where_true._rule_owned:
        arrays[name] = np.where(
            mask, chosen_where_true._arrays[name], chosen_where_false._arrays[name]
        )
    return Cells._assemble(arrays, chosen_where_true._rule_owned)
```
(`backend/asr/engine/cells.py:110-132`)

It walks `kind` plus every `USES` entry and selects field-by-field; everything not rule-owned is simply carried through from the "true" side (the proposal), since the rule never writes those arrays anyway and they're already correct.

### 5.3 Why the order is load-bearing

Two concrete failure modes if the order were changed:

- **Swap steps 2 and 3 (stubbornness before rate).** Consider a cell with `rate = 3` (updates only on ticks divisible by 3) and `stubbornness = 2`. On a tick where `tick % rate != 0`, the correct behavior (current order) is: the rule's proposal for that cell is discarded outright by the rate gate in step 2, so the stubbornness comparison in step 3 never even has a chance to matter for it — its `kind` simply doesn't change, full stop. If stubbornness ran *first*, it would compare `age >= stubbornness` and potentially let a `kind` change through on a tick the cell wasn't even scheduled to update on, before the rate gate discarded the proposal anyway — but discarding happens by replacing the *entire* rule-owned array set with the old grid, so whatever stubbornness decided would be silently overwritten either way in this particular implementation. The actual hazard the fixed order avoids is subtler and matters for the *birth* step: because gating happens (rate, then stubbornness) strictly *before* `born` is computed in step 4, a cell that never actually changed `kind` — because rate skipped it or stubbornness refused it — is guaranteed to be excluded from `born`. If birth detection ran before the gates, a cell whose *proposal* differed from its old kind, but whose gated *outcome* did not, would incorrectly trigger a birth draw (and, worse, incorrectly reset its `age` to 0 later) even though nothing observable about it changed.
- **Compute `age`/`changed_last_tick` before the birth draw (swap steps 4 and 5).** The birth draws in step 4 read and write modifier/slot arrays for cells in `born`, but `born` itself is derived purely from `kind`, which step 4 does not touch. So in *this* engine reordering steps 4 and 5 wouldn't corrupt `age`/`changed_last_tick` correctness directly — but it would corrupt reproducibility of anything that reads derived state during a birth-timed draw evaluation in a future modifier, and more importantly it would break the invariant that "age describes the tick that just ended": a modifier's birth draw for a stubbornness-scoped rule needs `stubbornness` reads to see the *pre-tick* age (step 3 uses `cells.age`, not `proposed.age`), and if age were finalized before the birth draws ran, the harness would need a second, inconsistent copy of "old age" — the fixed order avoids that entirely by finalizing derived state only once everything that needs pre-tick values has already consumed them.

The example that best demonstrates *why order is semantics* rather than an implementation detail is the rate/stubbornness interaction in the first bullet: change either gate's position relative to `born = proposed.kind != cells.kind`, and a cell whose only observable behavior across a tick was "held in place by a modifier" would incorrectly consume a birth draw and reset its age — which would make the RNG state and the age array diverge from a byte-identical run of the un-reordered engine, silently breaking exact-loop detection (§6) for every rule using both `rate` and `stubbornness` together.

---

## 6. Fingerprints: computational vs. pattern

This is, per `CLAUDE.md`, "the subtlest part of the spec," and `fingerprint.py`'s docstring states the distinction as sharply as the code does:

> Two different things, deliberately:
> - The COMPUTATIONAL fingerprint covers everything that determines the future — every array the rule or the harness will consult, the scheduler phase when `rate` is in scope, and the RNG state when birth draws are declared. Loop detection compares these and nothing else.
> - The PATTERN fingerprint covers `kind` only. It is an observation of the picture, never a stopping condition (REQ-9.7.5, REQ-9.8.1).
>
> Both hash exact bytes — floats are never quantized (REQ-9.7.2) — with blake2b-128, arrays taken in name-sorted order and each preceded by its name and dtype so the hash never depends on allocation order (REQ-9.7.4).

(`backend/asr/engine/fingerprint.py:1-15`)

### 6.1 The computational fingerprint

```python
SCHEDULER_CYCLE = 12  # LCM of the permitted rates 1-4
STUBBORNNESS_AGE_CLAMP = 3

def computational_fingerprint(
    cells: Cells, declaration: Declaration, tick: int, dice: Dice
) -> bytes:
    """Everything that determines the future, in 16 bytes."""
    arrays: dict[str, np.ndarray] = {}

    for name in declaration.rule_owned():
        arrays[name] = cells._arrays[name]
    for name in declaration.modifiers:
        arrays[name] = cells._arrays[name]
    for name in declaration.semantic_slots:
        arrays[name] = cells._arrays[name]

    # Derived state enters when any consumer — the rule or an active
    # harness semantic — can see it (REQ-9.7.6).
    if "age" in declaration.reads:
        arrays["age"] = cells._arrays["age"]
    elif "stubbornness" in declaration.modifiers:
        arrays["age"] = np.minimum(cells._arrays["age"], STUBBORNNESS_AGE_CLAMP)
    if "changed_last_tick" in declaration.reads:
        arrays["changed_last_tick"] = cells._arrays["changed_last_tick"]

    digest = hashlib.blake2b(digest_size=16)
    for name in sorted(arrays):
        _add_array(digest, name, arrays[name])

    if "rate" in declaration.modifiers:
        digest.update(b"scheduler_phase")
        digest.update(str(tick % SCHEDULER_CYCLE).encode("utf-8"))

    if declaration.declares_birth_draws():
        digest.update(b"rng_state")
        digest.update(dice._state_bytes())

    return digest.digest()
```
(`backend/asr/engine/fingerprint.py:37-77`)

Exactly what goes in, and why each piece is necessary for the future to be fully determined:

- **Every rule-owned array** (`kind` plus each `USES` entry) — this is the state the rule's own `step` directly consumes.
- **Every in-scope modifier array** (`weight`, `stubbornness`, `rate`) and **every semantic-slot array** — these change how the harness applies the rule, so two grids that differ only in, say, `stubbornness` values have different futures even with identical `kind`.
- **`age`, conditionally** — this is the most delicate piece. If the rule declared `READS = ["age"]`, the *full-precision* `age` array is hashed, because the rule can compare it against any arbitrary value and any difference is future-relevant. If the rule doesn't read `age` but `stubbornness` is in scope, `age` is still hashed — but **clamped** to `min(age, 3)` first. The reasoning (REQ-9.7.6, quoted above) is that the harness itself only ever evaluates `age >= stubbornness`, and `stubbornness`'s declared range tops out at 3 (`ModifierSpec(..., lowest=0, highest=3, ...)` in `modifiers.py:41-54`), so any age of 3 or higher is behaviorally indistinguishable from any other age of 3 or higher, forever. Without this clamp, `age` would climb without bound every tick a cell survives and the computational fingerprint would essentially never repeat, making `frozen`/`looping` practically unreachable for any rule using `stubbornness` — REQ-9.7.6 states this outright: "unclamped, `age` increments every tick until it saturates at 65535, far beyond `MAX_TICKS`, and exact freezing becomes impossible." If neither condition holds, `age` is excluded from the fingerprint entirely — it genuinely doesn't affect the future for that rule.
- **`changed_last_tick`, conditionally** — included only if the rule declared `READS = ["changed_last_tick"]`.
- **Scheduler phase**, `tick % 12`, when `rate` is in scope. `SCHEDULER_CYCLE = 12` is chosen as the LCM of the four permitted `rate` values (1, 2, 3, 4) specifically because "two identical grids at different points in the rate cycle have different futures" (comment at `fingerprint.py:26-28`) — a cell with `rate = 4` scheduled on tick 8 behaves differently going forward than the same cell-state reached at tick 9, even though every array might coincidentally match, because it's due to update on a different set of upcoming ticks.
- **RNG state**, only when `declaration.declares_birth_draws()` is true (§1.4) — i.e. only for rules that actually have at least one `assign_when: "birth"` modifier or slot with an `assign` entry. For everything else, the RNG is irrelevant to the future because it's never consulted again.

`_add_array` (`fingerprint.py:37-40`) is the primitive both fingerprints build on: it feeds the property's *name*, its *dtype string*, and its raw bytes (`np.ascontiguousarray(array).tobytes()`) into the digest, in that order — this is what makes the hash depend only on content, never on which order Python happened to allocate the arrays in (`arrays` is a plain dict; `sorted(arrays)` iterates alphabetically before hashing).

### 6.2 The pattern fingerprint

```python
def pattern_fingerprint(cells: Cells) -> bytes:
    """The pattern of kinds, in 16 bytes. An observation only — it never
    stops a run and never joins the computational fingerprint.
    """
    digest = hashlib.blake2b(digest_size=16)
    _add_array(digest, "kind", cells._arrays["kind"])
    return digest.digest()
```
(`fingerprint.py:80-86`)

This hashes `kind` — and only `kind` — nothing else. It has no idea what `age`, `energy`, `memory`, modifier state, or RNG state look like. Two ticks with wildly different hidden state (different `memory` counters mid-countdown, different `stubbornness` ages, different RNG position) but the same visible `kind` grid produce the *same* pattern fingerprint and *different* computational fingerprints — which is exactly the gap REQ-9.7.5 exists to name: "The pattern fingerprint is an observation only. It never terminates a run (REQ-9.8.1) and never enters the computational fingerprint."

### 6.3 Why birth draws being skipped is what makes `frozen` reachable

Tie this back to `apply_tick` (§5.2), step 4: `if born.any(): _apply_draws(...)`. When nothing was born on a tick, the harness makes literally zero calls into `dice`, so the RNG's internal state does not advance. That means on a tick where a stochastic rule's population has genuinely stopped producing new births — every cell that would have changed kind has already settled into a configuration where `step` returns exactly the same `kind` as before — the *entire* computational fingerprint (rule-owned arrays unchanged, modifier/slot arrays unchanged because nothing was born to redraw them, RNG state unchanged because it was never touched) becomes byte-identical to the previous tick's. That equality is precisely what the run loop checks for `frozen` (§7). REQ-9.7.7 states the consequence directly: "Because birth draws are skipped when nothing was born (REQ-5.6.2), a stochastic rule that settles stops advancing the RNG and *can* reach `frozen`. A stochastic rule that keeps producing births will not, and will run to its tick budget. Both are correct." Without the `if born.any()` guard, a rule with any birth-timed modifier would advance its RNG state on *every* tick regardless of whether the visible system was static, and the computational fingerprint could never repeat exactly — `frozen` would be structurally unreachable for any rule using birth-timed randomness, even ones that have genuinely stopped doing anything.

### 6.4 Nothing stops a run because the picture went quiet

This is REQ-9.8.1, and the engine enforces it by construction rather than by a special case: the *only* fingerprint the stopping logic in `run.py` ever compares is the computational one (§7). The pattern fingerprint is computed and recorded every tick (`_record` in `run.py:57-75` calls `pattern_fingerprint(cells)`), tracked for `kind_quiet_for` bookkeeping, and used later by the classifier (§9) and by `pattern_settled_at` — but it is never once passed into the `stopped_because` decision. `backend/tests/slow_burn_fixture.py` exists purely to prove this: its `Rule` holds `kind` at a constant value for 60 ticks while silently incrementing a hidden `memory` counter, then flips `kind` once the counter hits 60:

```python
FLIP_AT = 60

class Rule:
    KINDS = 2
    ...
    USES = ["memory"]
    ...
    def step(self, cells):
        counted = np.minimum(cells.memory.astype(np.int32) + 1, 255).astype(np.uint8)
        flipped = np.where(counted >= FLIP_AT, np.uint8(1), cells.kind).astype(np.uint8)
        return make_cells(flipped, memory=counted)
```
(`backend/tests/slow_burn_fixture.py:11-37`)

Its docstring states the purpose outright: "it counts in hidden memory for sixty ticks with the picture completely still, then flips kind. It exists solely to prove that a quiet pattern never terminates a run (REQ-9.8.1)." For 59 ticks, the pattern fingerprint (hash of `kind` alone) is identical tick over tick — a naive "stop when the picture stops changing" rule would kill this run around tick 1 or 2. But `memory` is rule-owned (declared in `USES`), so it is part of the computational fingerprint every tick, and it changes every tick — the computational fingerprint therefore keeps changing right up until the flip, and the run correctly keeps going. This fixture is deliberately test-only and excluded from the library and Stage A context (REQ-14.4) — its whole purpose is a targeted proof, not a representative behavior sample.

---

## 7. The run loop

`run.py`'s docstring: "A run is one rule, one starting grid, up to `MAX_TICKS` ticks, executed to completion before playback begins (REQ-9.1). Every tick is recorded; stopping is decided by exact recurrence of the computational fingerprint, the tick budget, or the per-tick timeout — never by the picture going quiet (REQ-9.8.1)." (`backend/asr/engine/run.py:1-8`)

### 7.1 `run_rule`

```python
def run_rule(
    rule_class, declaration, seed, width, height, max_ticks, tick_timeout_seconds, on_tick=None,
) -> RunResult:
    dice = Dice(seed, height, width)
    rule = rule_class(dice)
    cells = start_grid(rule, declaration, width, height, dice)
    _freeze(cells)

    record = _record(cells, declaration, 0, dice, previous=None)
    ticks = [record]
    if on_tick:
        on_tick(record)
    # Fingerprint -> tick map: the entire exact-loop detector (REQ-9.9).
    # Tick 0 participates (REQ-4.6.3).
    seen = {record.state_fingerprint: 0}

    stopped_because = None
    loop_length = None
    for tick in range(1, max_ticks + 1):
        started = time.perf_counter()
        cells = apply_tick(rule, declaration, cells, tick, dice)
        _freeze(cells)
        elapsed = time.perf_counter() - started

        record = _record(cells, declaration, tick, dice, previous=ticks[-1])
        ticks.append(record)
        if on_tick:
            on_tick(record)

        # Stopping conditions in spec precedence (REQ-9.8).
        fingerprint = record.state_fingerprint
        if fingerprint == ticks[-2].state_fingerprint:
            stopped_because = "frozen"
        elif fingerprint in seen:
            stopped_because = "looping"
            loop_length = tick - seen[fingerprint]
        elif tick == max_ticks:
            stopped_because = "ran_out"
        elif elapsed > tick_timeout_seconds:
            stopped_because = "too_slow"
        if stopped_because:
            break
        seen[fingerprint] = tick

    return assemble_result(ticks, stopped_because, loop_length)
```
(`backend/asr/engine/run.py:117-175`)

One rule instance, one seeded `Dice`, one starting grid built by `start_grid` (§5.1). Each tick calls `apply_tick` (§5.2), immediately calls `_freeze` on the result (making every array in it read-only, `run.py:105-114`, so the *next* call to `step` cannot corrupt history even accidentally), times how long the tick took, and builds a `TickRecord`.

Stopping is checked in exactly REQ-9.8's precedence, every tick:

1. **`frozen`** — the new tick's computational fingerprint equals the *immediately previous* tick's (`ticks[-2]`, i.e. the one before the one just appended).
2. **`looping`** — the new fingerprint was already `seen` at some earlier tick in this same run; `loop_length` is `tick - seen[fingerprint]`, the gap between the two occurrences.
3. **`ran_out`** — the tick counter hit `max_ticks`.
4. **`too_slow`** — this single tick's wall-clock time exceeded `tick_timeout_seconds`.

`seen`, the fingerprint→tick map, "is the entire exact-loop detector" (REQ-9.9) — a plain dict, checked and appended to every tick, with tick 0's fingerprint seeded into it before the loop even starts (`seen = {record.state_fingerprint: 0}`), which is what makes a rule that returns to its exact tick-0 state after some ticks correctly register as `looping` with a loop length equal to the current tick (REQ-4.6.3).

Production runs never call `run_rule` directly in-process — `run.py`'s docstring notes "Production runs go through `contract.child` so a runaway rule cannot take the server down (REQ-7.6.1); the loop itself is identical" (`run.py:129-131`). That child-process isolation is contract-enforcement machinery covered by a different document in this series; the loop logic itself, quoted above, is unchanged whether it executes in the parent process (as fixtures and tests do) or inside the sandboxed child.

### 7.2 What each tick records

```python
@dataclass
class TickRecord:
    tick: int
    arrays: dict  # every array at this tick, by property name
    kind_counts: list
    variety: float
    cells_changed: int
    kind_quiet_for: int
    state_fingerprint: bytes
    pattern_fingerprint: bytes
```
(`run.py:24-33`)

Built by `_record` (`run.py:57-75`): `kind_counts` is `np.bincount` over `kind`, giving a per-`KINDS`-value population count; `variety` is Shannon entropy of that distribution divided by `log(KINDS)` — 0.0 for a single kind present everywhere, 1.0 for a perfectly even spread (REQ-9.10):

```python
def _variety(kind: np.ndarray, kinds: int) -> float:
    counts = np.bincount(kind.ravel(), minlength=kinds)
    total = kind.size
    shares = counts[counts > 0] / total
    spread = -(shares * np.log(shares)).sum()
    return float(spread / math.log(kinds))
```
(`run.py:45-54`)

`cells_changed` is how many cells' `kind` differ from the previous tick (the "standard term: Hamming distance" the comment notes, REQ-9.2). `kind_quiet_for` tracks consecutive ticks the *pattern* fingerprint hasn't changed — purely an observation used by the classifier, explicitly never a stopping condition (REQ-9.15: "An observation and a classifier input, never a stopping condition").

`pattern_settled_at` (`run.py:91-102`) is computed once, at the very end of a completed run: the earliest tick after which the pattern fingerprint never changes again, or `None` if it was still changing on the final recorded tick (REQ-9.11).

---

## 8. The classifier

`classify.py`'s docstring: "Guessing what kind of behavior a finished run showed (REQ-9.16). Deterministic thresholds, no qualitative judgment. The guess is stored alongside the numbers that produced it, never as fact (REQ-9.6), and the user may overrule it without erasing it (REQ-9.14). `unclassified` is a real outcome, not an error (REQ-9.13). `broken` is never a run classification — it lives on the rule (REQ-9.16.2)." (`backend/asr/engine/classify.py:1-8`)

```python
WINDOW = 100
SHORT_LOOP = 50
SETTLED_CHANGE_RATE = 0.0005
NOISY_CHANGE_RATE = 0.10
NOISY_VARIETY = 0.60
DECAY_SLOPE = -0.001

def classify(result: RunResult, width: int, height: int) -> tuple:
    """Returns (guessed_behavior, guess_confidence)."""
    window = result.ticks[-WINDOW:]
    area = width * height
    change_rate = float(np.mean([t.cells_changed for t in window])) / area
    mean_variety = float(np.mean([t.variety for t in window]))

    # Rows 1-4: the stop reason alone decides.
    if result.stopped_because == "looping":
        if result.loop_length <= SHORT_LOOP:
            return "repeats", "high"
        return "unclassified", "high"  # a long loop is a different phenomenon
    if result.stopped_because == "too_slow":
        return "unclassified", "high"
    if result.stopped_because == "frozen":
        return "settles", "high"

    # Rows 5-8: the run ran out its budget; read the final window.
    if change_rate < SETTLED_CHANGE_RATE:
        return "settles", "low"
    if change_rate >= NOISY_CHANGE_RATE and mean_variety >= NOISY_VARIETY:
        return "noisy", "high"
    if change_rate < NOISY_CHANGE_RATE and mean_variety < NOISY_VARIETY:
        ticks = [t.tick for t in window]
        changes = [t.cells_changed for t in window]
        slope = float(np.polyfit(ticks, changes, 1)[0]) if len(window) > 1 else 0.0
        if slope > DECAY_SLOPE * area:
            return "structured", "low"

    return "unclassified", "low"
```
(`backend/asr/engine/classify.py:14-55`)

This mirrors REQ-9.16's table exactly. Let *W* be the final 100 recorded ticks (or the whole run, if it's shorter). `change_rate` is mean `cells_changed` over *W*, divided by grid area; `mean_variety` is mean `variety` over *W*.

| Order | Label | Condition |
|---|---|---|
| 1 | `repeats` | stopped because `looping` and `loop_length <= 50` |
| 2 | `unclassified` | stopped because `looping` and `loop_length > 50` |
| 3 | `unclassified` | stopped because `too_slow` |
| 4 | `settles` | stopped because `frozen` |
| 5 | `settles` | `change_rate < 0.0005` (stopped moving, but never hit exact freeze) |
| 6 | `noisy` | `change_rate >= 0.10` and `mean_variety >= 0.60` |
| 7 | `structured` | `0.0005 <= change_rate < 0.10`, `mean_variety < 0.60`, and the slope of `cells_changed` over *W* is above `-0.001 × area` per tick |
| 8 | `unclassified` | anything else |

The first four rows are decided purely by *how the run stopped* — the classifier doesn't even look at the tick window for them. A short exact loop (≤50 ticks) is `repeats`; a long one is a genuinely different, `unclassified` phenomenon (REQ-9.13: "A long loop is genuinely not the same phenomenon as a short one, and forcing it into `repeats` would corrupt the coverage distribution"). `frozen` (exact recurrence one tick apart) is always `settles`.

For runs that exhausted their tick budget (`ran_out`), rows 5–8 read the trailing window. Row 5 catches patterns that are *almost* frozen — moving so little that they never happen to hit exact byte-for-byte recurrence but are visually static (a common case for float-bearing or slowly-drifting rules). Rows 6 and 7 split the remaining space along two axes, change rate and variety: high change *and* high variety is `noisy`; low-to-moderate change and low variety is a `structured` candidate, gated further by a linear-regression slope over `cells_changed` in the window — this is what the comment calls "the slope term... to separate persistence from slow decay: stable shapes that move or persist keep `cells_changed` level, while a dying run's `cells_changed` falls tick over tick" (`classify.py:46-48`, REQ-9.16.1). Anything that falls through all of it lands in `unclassified` — an intentional, non-error outcome. Confidence is `high` for rows 1, 3, 4, 6 and `low` for rows 2, 5, 7, 8 — row 7 (`structured`) is explicitly flagged as the least reliable, "a threshold heuristic standing in for 'stable shapes that move or persist'" per REQ-9.16.1, and `documents/architecture.md:76-78`'s calibration notes record that its thresholds are "first guesses, calibrated against nothing" pending real data.

`broken` never appears anywhere in this module — REQ-9.16.2 is explicit that it "is not a run classification. A broken rule fails before any run exists; its status lives on the rule, not on a run" — a rule that fails Stage C validation never produces a `RunResult` in the first place.

---

## 9. Worked example: tracing `life` through one tick

The `life` fixture (`backend/asr/fixtures/life.py`) is Conway's Game of Life expressed in this engine's contract: `KINDS = 2`, `NEIGHBORS = "all_8"`, `REACH = 1`, no `USES`, `READS`, `MODIFIERS`, or `SEMANTIC_SLOTS` — the simplest possible rule, useful precisely because it exercises `count_neighbors` and the wraparound geometry without any modifier or gating complexity in the way. Its docstring notes exactly why it's a fixture: "one crossing the wrap boundary intact is the single best end-to-end proof that the wrap logic is correct" (`backend/asr/fixtures/life.py:1-6`).

Running it on a small 6×6 grid with `seed=42` produces this tick-0 `kind` array (0 = dead, 1 = alive; rows top to bottom, columns left to right):

```
tick 0:
[[0 0 0 0 1 0]
 [0 0 1 0 0 0]
 [0 0 0 1 0 1]
 [0 0 0 0 0 0]
 [0 1 0 1 1 0]
 [0 0 1 0 0 1]]
```

This came directly from `make_start`: `make_cells(self.dice.chance(0.35).astype(np.uint8))` — a single whole-grid `Dice.chance(0.35)` call, cast to `uint8`, wrapped in `make_cells`. No modifiers are in scope, so `start_grid`'s steps 2–4 (§5.1) allocate nothing and perform no draws; `age` and `changed_last_tick` are simply zeroed everywhere.

Take cell `(row=0, col=3)`, which is dead (`0`) at tick 0. Its eight `all_8`, reach-1 neighbors wrap across the top edge (row `-1` becomes row `5`, the bottom row) and are, reading row 5 / row 0 / row 1 across columns 2–4:

```
row 5, cols 2-4: 1 0 0
row 0, cols 2-4: 0 . 1   (col 3 is the cell itself, excluded)
row 1, cols 2-4: 1 0 0
```

Summing the six occupied positions: `1+0+0 + 0+1 + 1+0+0 = 3` live neighbors. `life.py`'s rule is `comes_alive = ~alive & (crowd == 3)` — dead with exactly 3 live neighbors — so this cell is born at tick 1. Applying `apply_tick`: `rule.step(cells)` computes this via `count_neighbors(cells, "kind", 1)`, which internally is `bind_helpers("all_8", 1)`'s `count_neighbors` — for each of the eight offsets in the declared neighborhood, `np.roll` the `kind == 1` boolean array by that offset (negated) and sum. No modifiers are declared, so steps 2 and 3 of `apply_tick` (the `rate` and `stubbornness` gates) are skipped outright (`"rate" in declaration.modifiers` and `"stubbornness" in declaration.modifiers` are both `False`). `born = proposed.kind != cells.kind` is `True` for `(0, 3)`; since `MODIFIERS = []`, `_apply_draws` has nothing to assign even though `born.any()` is `True` overall (no modifier or slot has `assign_when == "birth"` with an `ASSIGN` entry, so the loops inside `_apply_draws` simply do nothing for this rule — the harness still checks `born.any()`, finds cells born, calls `_apply_draws`, and that call is a no-op). Finally, `changed_last_tick[0,3]` becomes `True` and `age[0,3]` resets to `0`.

Symmetrically, cell `(0, 4)` is *alive* at tick 0. Its neighbors (row 5 / row 0 / row 1, columns 3–5, excluding itself at row 0 col 4):

```
row 5, cols 3-5: 0 0 1
row 0, cols 3-5: 0 . 0
row 1, cols 3-5: 0 0 0
```

Sum = `1` live neighbor. Life's survival rule is `keeps_living = alive & ((crowd == 2) | (crowd == 3))` — with only 1 neighbor, this cell does not survive; it dies at tick 1 (`comes_alive` doesn't apply since it's already alive, and `keeps_living` is `False`).

Actually running `apply_tick` for tick 1 on this grid produces:

```
tick 1 kind:
[[0 0 0 1 0 0]
 [0 0 0 1 1 0]
 [0 0 0 0 0 0]
 [0 0 1 1 0 0]
 [0 0 1 1 1 0]
 [0 0 1 0 0 1]]

tick 1 age:
[[1 1 1 0 0 1]
 [1 1 0 0 0 1]
 [1 1 1 0 1 0]
 [1 1 0 0 1 1]
 [1 0 0 1 1 1]
 [1 1 1 1 1 1]]

tick 1 changed_last_tick:
[[False False False  True  True False]
 [False False  True  True  True False]
 [False False False  True False  True]
 [False False  True  True False False]
 [False  True  True False False False]
 [False False False False False False]]
```

Confirming both hand calculations: `kind[0,3]` is now `1` (born, as predicted), `kind[0,4]` is now `0` (died, as predicted), and their `age`/`changed_last_tick` entries line up exactly — `age[0,3] = 0` and `changed_last_tick[0,3] = True` because it was born; `age[0,4] = 1` (incremented from 0) and `changed_last_tick[0,4] = True` because it also changed (died counts as a `kind` change, same as being born — `changed_last_tick` tracks any `kind` change, not just births); a cell like `(0,0)`, which stayed dead, shows `age = 1, changed_last_tick = False` — its age advanced by exactly one tick, unconditionally, exactly as REQ-4.3.1 requires.

Because `life` declares no modifiers, its computational fingerprint (`computational_fingerprint` in `fingerprint.py`) reduces to just `kind` hashed with blake2b-128 — no `age` (not in `READS`, and `stubbornness` isn't in scope so no clamped-age fallback either), no scheduler phase (no `rate`), no RNG state (no birth-timed draws declared at all, so `declares_birth_draws()` is `False`). That means for `life` specifically, the computational and pattern fingerprints are *almost* the same computation (both ultimately just hash `kind`) — but they remain conceptually distinct fields computed by two different functions, and the moment a rule adds so much as `USES = ["memory"]` (as `slow_burn` does), that near-equivalence disappears, which is exactly the point §6.4's worked example makes with a different fixture.

---

## Where this fits in the larger system

This document covers `backend/asr/engine/` only — the deterministic core. It does not cover:

- **`backend/asr/contract/`** — how generated Python source is statically validated against the AST rules referenced above (REQ-7.6–7.9), and how it's actually executed inside a memory-and-timeout-limited child process. `run_rule`'s docstring points at this directly: production runs go through `contract.child`, "so a runaway rule cannot take the server down."
- **`backend/asr/storage/`** — how `TickRecord`s are actually persisted (snapshot-plus-delta encoding, Zstandard compression) and reconstructed for playback.
- **`backend/asr/generation/`** — how Stage A/B/C actually produce a `Declaration` and a `Rule` class in the first place, including the coverage map that gates which `Declaration` shapes get attempted.

Each is the subject of its own document in this series.
