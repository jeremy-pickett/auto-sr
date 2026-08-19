# Autonomous Semantic Ruliology
## Omnibus Requirements — v3

**Status:** contract-complete. Cleared for harness implementation.
**Purpose:** single source of truth for the build, and the reference target for bug
tracking. Every requirement carries a stable `REQ-` identifier. Cite identifiers in
issues rather than describing behavior in prose.

**What this system is, in one sentence:** it teaches a machine to ask "what simple rule
should I try next?" and then makes it prove the answer by running the experiment.

---

## 0. Reading This Document

**REQ-0.1 — Plain language.** No mathematical jargon in code, property names, UI labels,
or documentation. A second-year CS student who is bad at math must read any name in this
system and immediately know what it means. Where a standard technical term exists, use a
plain-English name and mention the standard term once, in a comment.

**REQ-0.1.1** The project *name* is exempt from REQ-0.1. A project may be pretentious; a
variable may not.

**REQ-0.2 — Identifier stability.** `REQ-` identifiers are permanent. A removed
requirement's identifier is retired, never reused.

**REQ-0.3 — Credits.** The application credits state that the project is inspired by
Stephen Wolfram's work on cellular automata. It is not a reproduction of it and makes no
claim to be.

### 0.4 Changes from v2

| Area | Change | Driver |
|---|---|---|
| Stage C matching | `READS` added to the declaration-match check. | Review 3 §1 |
| `Cells` | Constructor and merge specified; container arithmetic removed. | Review 3 §2 |
| Fingerprint | `age` included whenever `stubbornness` is in scope, clamped. | Review 3 §3, extended |
| Stopping | **`visually_frozen` removed entirely.** | Review 3 §4 |
| Naming | `visual_fingerprint` → `pattern_fingerprint`. | Review 3 §4 |
| Helpers | Raw `shift` removed; `look` and `move` added, both bound to the declaration. | Review 3 §5 |
| Randomness | `Dice` facade specified; tick-0 assignment order fixed. | Review 3 §6 |
| Randomness | Birth draws skipped entirely when nothing was born. | Review 3 §7 |
| Transport | Binary framing and streaming-fetch requirement specified. | Review 3 §8 |
| Storage | Derived arrays no longer stored per tick. | Review 3 §9, extended |
| Classification | Deterministic thresholds replace qualitative bands. | Review 3 §10 |
| Coverage map | Now carries attempts and rejections, not only canonical outcomes. | Review 3, v2.1 note |
| Provenance | Fully rendered prompts stored, not only template hashes. | Review 3, v2.1 note |

**Retired identifiers:** REQ-9.5 (float quantization), REQ-13.10 (visually-frozen UI
copy), REQ-17.5 (visual freeze threshold tuning). Config variable `VISUAL_FREEZE_TICKS`
is removed.

**New in v3:** REQ-4.6.1, REQ-4.6.2, REQ-6.2.1, REQ-6.6, REQ-6.7, REQ-7.9.4, REQ-8.8,
REQ-9.7.6, REQ-9.7.7, REQ-9.15, REQ-9.16, REQ-11.4.1, REQ-11.5.1, REQ-12.6, REQ-12.7,
REQ-13.11, REQ-15.8.

---

## 1. Concept

Rules are not written by a person. When the user clicks **Run New Rule**, the backend
makes two primary LLM calls: the first invents a rule and describes it in English, the
second turns that description into Python. The result is checked, run, measured, and
added permanently to a growing library.

**REQ-1.2** Two *primary* generation calls. Optional additional calls occur for shape
tagging when static inference is inconclusive (REQ-8.2.1) and for a single repair attempt
(REQ-7.8 step 7). Documentation and UI must not claim exactly two.

**REQ-1.3** "Meta-cognitive" here means *history-informed hypothesis generation*. No claim
is made about machine metacognition in any stronger sense.

### 1.1 The library is the product

**REQ-1.4** Individual rules matter very little. The durable artifact is the corpus
linking natural-language descriptions of computational ideas to observed emergent
behavior: descriptions, reasoning, implementations, structure tags, seeds, trajectories,
measurements, failures, ancestry, and human corrections.

**REQ-1.1** The system makes no claim to enumerate or cover a rule space. An LLM samples
according to its own priors; coverage is neither exhaustive nor measurable in the Wolfram
sense. UI text or documentation implying exhaustive search is a bug.

---

## 2. Decisions and Rationale

Recorded so reviewers do not re-decide them.

| Decision | Why |
|---|---|
| **Simplicity limit** (REQ-7.6) | Complexity must emerge from iteration, not rule richness. Unconstrained, the generator writes elaborate machines and the Rule 110 surprise never appears. |
| **Runtime limit is a separate mechanism** (REQ-7.6.1) | Different job. `while True: pass` is one AST node. |
| **Identity defaults for modifiers** (REQ-5.1) | Lets the catalog grow without bound while staying free. A modifier whose default changes behavior is state, not a modifier. |
| **Computational state ≠ pattern state** (REQ-9.7) | Exact recurrence, a quiet picture, float drift, scheduler phase, and RNG advance are five different things. |
| **Nothing stops a run because the picture went quiet** (REQ-9.8.1) | A rule counting to fifty in `memory` before flipping `kind` looks dead for forty-nine ticks. Delayed emergence from hidden state is the thing this system exists to find. |
| **`step` is deterministic** (REQ-7.4.1) | Random initial conditions with a deterministic law is the cleaner experiment, and it removes a class of loop-detection ambiguity. |
| **Every spatial helper is bound to the declaration** (REQ-6.2.1) | An unbound `shift` lets a REACH=1 rule reach seventeen cells and quietly falsify its own coverage entry. |
| **Runs execute to completion before playback** (REQ-9.1) | Makes pause/step/scrub a video player over immutable history. |
| **Enum instead of string** (REQ-5.2.1) | A numpy grid of strings is fixed-width bytes or object dtype, and both destroy vectorization. |
| **One non-default modifier per generation** (REQ-5.7) | Modifiers are the experimental variable. More than one and every result is a confound. |
| **Coverage map instead of a rule list** (REQ-8.1) | The prompt cannot hold 500 rules, and truncating a list biases the generator invisibly. |
| **Harness owns modifier application and all draws** (REQ-5.6, REQ-6.4) | Anything the generator implements, it eventually implements wrong. |
| **Parallel numpy arrays, not cell objects** (REQ-4.1) | 200×200 over 500 ticks is 20 million cell updates. |
| **Generated rules run in a child process** (REQ-7.6.1) | Not sandboxing. Python cannot safely kill a runaway thread, and an infinite loop must not take FastAPI down. |
| **Derived arrays are reconstructed, not stored** (REQ-12.6) | `age` changes on nearly every cell every tick, which would make every "settled" tick dense and destroy sparse delta encoding. |
| **Broken rules and rejections stay in the library** (REQ-7.8.1, REQ-7.11) | What the generator gets wrong is data about the generator. |

---

## 3. Stack and Deployment

**REQ-3.1** Backend: Python 3.11+, FastAPI, uvicorn.
**REQ-3.2** Frontend: React via Vite. Canvas rendering, no WebGL in v1.
**REQ-3.3** Storage: SQLite, single file, WAL mode.
**REQ-3.4** Single user, local. No authentication, accounts, or per-user config.
**REQ-3.5** Grid edges always wrap: top to bottom, left to right. (Standard term:
toroidal.)
**REQ-3.6** Generation is synchronous — one click, one rule. No job queue, no background
workers. Progress is streamed within the single request (REQ-11.4).
**REQ-3.7** Rules are atomic. One rule per run. Rules do not compose, nest, or invoke one
another.
**REQ-3.8** Sandboxing of generated code is out of scope. The host is assumed hardened.
**REQ-3.10** The restricted execution namespace (REQ-7.9) is **language-contract
enforcement, not a security boundary.** Do not describe it as a sandbox.

### 3.9 Configuration

| Variable | Default | Affects |
|---|---|---|
| `GRID_WIDTH` | 200 | Every run. Not user-selectable in v1. |
| `GRID_HEIGHT` | 200 | Every run. |
| `MAX_TICKS` | 500 | Budget before `ran_out`. |
| `SNAPSHOT_EVERY` | 50 | Full-grid storage interval. |
| `TICK_TIMEOUT_SECONDS` | 2.0 | Per-tick wall clock before `too_slow`. |
| `RUN_MEMORY_LIMIT_MB` | 2048 | Child process ceiling. |
| `SIMPLICITY_LIMIT` | 40 | Max branch/loop/comprehension nodes in `step`. |
| `LINEAGE_CHANCE` | 0.0 | Probability a generation is a variation. |
| `RUN_CACHE_BUDGET_MB` | 512 | Reconstruction cache ceiling. |
| `ANTHROPIC_MODEL` | (explicit) | Recorded per rule. |
| `DATABASE_PATH` | `./library.db` | |

---

## 4. The Cell

**REQ-4.1** A cell is a set of named, typed properties stored as **parallel numpy arrays**
of shape `(height, width)` — one array per property, never an array of cell objects.

### 4.2 Core properties — the rule owns these

| Name | Type | Range | Required | Purpose |
|---|---|---|---|---|
| `kind` | uint8 | `0 .. KINDS-1`, KINDS ≤ 8 | yes | What the cell is. Drives color. |
| `energy` | uint8 | 0–255 | no | Accumulation, decay, spreading. |
| `heading` | enum | `n ne e se s sw w nw none` | no | Direction. Enables walker rules. |
| `memory` | uint8 | 0–255 | no | Free scratch space. |

**REQ-4.2.1** Optional core properties are declared in `USES`. Undeclared properties are
not allocated; touching one is a validation failure.

### 4.3 Derived properties — the harness owns these

| Name | Type | Purpose |
|---|---|---|
| `age` | uint16 | Ticks since this cell's `kind` last changed. Saturates at 65535. |
| `changed_last_tick` | bool | Whether `kind` changed on the previous tick. |

**REQ-4.3** Recomputed after every tick. Read-only to the rule.
**REQ-4.3.1** `age` counts elapsed ticks, not update opportunities. A cell gated by `rate`
still ages on ticks it skipped.
**REQ-4.3.2** A rule reading a derived property must declare it in `READS`. The validator
derives the actual set from the AST and rejects any mismatch. `READS` feeds the
computational fingerprint (REQ-9.7.1), so an undeclared read silently corrupts loop
detection.

### 4.4 Modifiers

**REQ-4.4** Optional per-cell properties that change *how* a rule is applied. Section 5.
**REQ-4.5** Modifier and semantic-slot arrays are **read-only to generated code.** The rule
declares assignments in `ASSIGN`; the harness writes. Reading is permitted; any assignment
is a validation failure.

### 4.6 Initial conditions

**REQ-4.6 — Exact initialization sequence.** Tick 0 is the initial state, before any
transition. The harness performs, in order:

1. Call `rule.make_start(width, height)`, which returns rule-owned arrays (`kind` plus
   each entry in `USES`) via `make_cells` (REQ-6.2).
2. Allocate every in-scope modifier and semantic-slot array at its identity default.
3. Apply all `assign_when: start` draws.
4. Apply all `assign_when: birth` draws, treating **every tick-0 cell as newly born**.
5. Set `age` to 0 and `changed_last_tick` to False everywhere.
6. Compute and record the tick-0 fingerprints.

**REQ-4.6.1** Step 4 is a deliberate decision: at tick 0 every cell is new, so
`assign_when: birth` and `assign_when: start` produce statistically identical results at
tick 0 and diverge thereafter. The alternative — birth-assigned modifiers being wholly
absent until the pattern first churns — makes the initial condition inconsistent with the
rule's declared intent and makes early behavior depend on an invisible warm-up.

**REQ-4.6.2** Despite step 4, `age` is 0 and `changed_last_tick` is False at tick 0. Birth
*assignment* and the derived birth *flag* are separate concepts.

**REQ-4.6.3** The tick-0 fingerprint participates in loop detection, so a rule returning
exactly to its starting state is `looping` with period equal to the current tick.

---

## 5. Modifiers

### 5.1 The identity-default rule

**REQ-5.1** Every modifier's default must be an **identity** — a value at which the
modifier has no effect whatsoever. `weight = 1` is free because multiplying by one does
nothing.
**REQ-5.1.1** If a property's default still changes behavior, it is not a modifier. It is
state, and it belongs in REQ-4.2.

### 5.2 Property types

| Type | Storage | Notes |
|---|---|---|
| `int(min, max)` | smallest numpy int that fits | Preferred. |
| `float(min, max)` | float32 | Never quantized before fingerprinting (REQ-9.7.2). |
| `enum(values...)` | uint8 index | Labels exposed to rule code as named constants. |
| `bool` | numpy bool | |

**REQ-5.2.1 — No string type.** Anything that wants to be a string is an enum. Rule code
reads `HOLIDAY.halloween`, never `"halloween"`.

### 5.3 Catalog entry format

```yaml
weight:
  type: int(1, 4)
  default: 1                 # must be an identity value (REQ-5.1)
  applied_by: harness
  effect: counts_as
  assign_when: birth         # start | birth
  availability: sometimes(0.3)
  blurb: "How strongly this cell counts when its neighbors tally it up."
```

**REQ-5.3.1** `assign_when: start` — drawn once at grid creation, never changes. Behaves
like terrain.
**REQ-5.3.2** `assign_when: birth` — redrawn whenever `kind` changes, plus at tick 0
(REQ-4.6). Belongs to the current occupant.
**REQ-5.3.3** `availability` is `always`, `off`, or `sometimes(p)`, evaluated at generation
time. Stage A sees only in-scope modifiers.
**REQ-5.3.4** `blurb` is passed to Stage A verbatim and is the generator's only description
of the modifier.

### 5.4 Harness-applied modifiers — v1 set

| Name | Type | Default | Effect |
|---|---|---|---|
| `weight` | int(1,4) | 1 | Neighbor tallies count this cell as `weight` instead of 1. |
| `stubbornness` | int(0,3) | 0 | A `kind` change applies only if `age >= stubbornness`. |
| `rate` | int(1,4) | 1 | The cell updates only on ticks where `tick % rate == 0`. |

**REQ-5.4.1** `weight` affects **counting influence only.** It does not extend reach.
Permanent exclusion.
**REQ-5.4.2** `stubbornness` is evaluated by the harness against `age` regardless of
whether the rule declares `READS = ["age"]`. This makes `age` future-relevant whenever
stubbornness is in scope — see REQ-9.7.6.

### 5.5 Semantic slots

**REQ-5.5** Up to **two** enum slots per rule, named and defined by the generator, with a
mandatory identity value listed first.
**REQ-5.5.1** These exist because an LLM writes the rules, and a property with a meaningful
name is a hook the generator produces interesting behavior from. The two-slot cap keeps it
from becoming the whole system.
**REQ-5.5.2 — Declaration:**

```python
SEMANTIC_SLOTS = {
    "mood": {
        "values": ["none", "restless", "settled"],   # index 0 is the identity
        "assign_when": "birth",
        "assign": {"value": "restless", "chance": 0.05},
    }
}
```

Stored in `rules.semantic_slots_json`. Values exposed as constants (`MOOD.restless`).
Arrays are read-only to the rule (REQ-4.5).

**REQ-5.5.3 — Kill criterion.** If, after 200 rules declaring slots, the slot value is
determined by `kind` in more than 80% of them, the generator is using slots as duplicate
state and the feature is cut.

### 5.6 Assignment draws

**REQ-5.6** The **harness** performs all draws; the rule only declares them. Draws are made
for the whole grid at once and masked down to affected cells — never per cell in a loop.

**REQ-5.6.2** During a run, if no cell was born on a tick, **no draw is made at all.**
`born.any()` is deterministic, so skipping preserves consumption order and reproducibility.
This is what allows a settled system to eventually stop touching the RNG and become
exactly `frozen` (REQ-9.7.7).

### 5.7 Gating

**REQ-5.7** At most **one non-`always` modifier in scope per generation.**
**REQ-5.7.1** Gating is the experimental control. Without it every modifier is a confound.
**REQ-5.8** Semantic slots are gated independently and do not count against REQ-5.7. They
are a separate boolean coverage axis.

---

## 6. The Cells Container and Helpers

**REQ-6.1** The harness provides `Cells`, `make_cells`, and the helpers below in the
namespace of every generated rule. Generated code never implements neighbor lookup or edge
wrapping itself.

**REQ-6.2 — Construction.** Generated code builds a grid with `make_cells`. `Cells` has no
public constructor and no arithmetic or broadcasting semantics; it is a named bag of
arrays, not an array-like.

```python
def make_cells(kind, **core_properties):
    """Build a Cells from rule-owned arrays. The only way generated code
    creates one.

    Affects: make_start(), which must return a Cells. `kind` is required;
    each keyword must be a declared entry in USES. Modifier, slot, and
    derived arrays are NOT passed here -- the harness allocates those
    (REQ-4.6 steps 2-5), and the rule cannot write them (REQ-4.5).
    """


def merge_cells(mask, chosen_where_true, chosen_where_false):
    """HARNESS-PRIVATE. Field-by-field select across rule-owned arrays.

    Affects: the rate gate (REQ-6.4 step 2). Cells is not an ndarray, so
    np.where cannot be applied to it directly; this walks `kind` plus every
    entry in USES and applies the mask to each. Modifier and slot arrays are
    untouched because the rule never writes them, so `proposed` already
    carries them forward unchanged.

    Not exposed to generated code.
    """
```

### 6.2.1 Spatial helpers are bound to the declaration

**REQ-6.2.1** Every spatial helper available to generated code validates its offsets
against the rule's declared `NEIGHBORS` and `REACH`. No unbound shift is exposed. A rule
declaring `plus_4, REACH=1` and calling a raw shift with offset `(0, 17)` would reach
seventeen cells while its coverage entry claimed one, which falsifies the library.

**REQ-6.2.2** Offsets must be integer literals, or values drawn from a literal tuple or
list in an enclosing `for` (REQ-7.6.1). This is what makes static validation possible. A
runtime check also raises on an out-of-contract offset, so the Stage C trial catches
anything the static pass misses.

**REQ-6.2.3** *Looking* and *moving* are separate operations and were accidentally
conflated in v2. `look` observes within the declared neighborhood. `move` displaces content
by exactly one cell in a declared direction, independent of `REACH`, and exists so walker
rules do not need wide reach merely to relocate.

```python
def look(cells, prop, down, right):
    """One property array as seen from an offset neighbor, wrapping.

    Affects: any rule that needs a specific direction rather than a tally.
    (down, right) must be inside the declared neighborhood (REQ-6.3) --
    rejected statically where possible and at runtime always.

    Positive `down` brings the UPSTAIRS neighbor's value into this cell's
    position.
    """


def move(cells, prop, direction):
    """One property array displaced exactly one cell in `direction`.

    Affects: walker rules. `direction` is a heading constant and must be
    one of the directions the declared NEIGHBORS permits -- plus_4 rules
    cannot move diagonally. Displacement is always one cell regardless of
    REACH, so movement never inflates the declared reach.
    """


def count_neighbors(cells, prop, value):
    """How many of each cell's neighbors have `prop` equal to `value`.

    Affects: nearly every generated rule, and the entire meaning of
    `weight`. When `weight` is in scope, each neighbor contributes its own
    weight instead of 1 -- that substitution is the ONLY thing weight does
    (REQ-5.4.1). Rules do not opt in, so a generator that forgets weight
    exists still respects it. This is why the helper takes `cells` rather
    than a bare array: it needs cells.weight.

    Neighborhood shape and reach come from the declaration, NOT from
    arguments, so a rule cannot widen its reach at the call site.

    A cell is never its own neighbor.
    """


def count_neighbors_where(cells, mask):
    """Same, over an arbitrary boolean array -- "neighbors with energy
    above 5". Same automatic weighting and self-exclusion. Exists so that
    needing a computed condition does not push the generator into writing
    its own neighbor loop.
    """


def sum_neighbors(cells, prop):
    """Total of each cell's neighbors' values for `prop`. Same weighting
    and self-exclusion as count_neighbors.
    """
```

### 6.3 Neighborhood geometry

**REQ-6.3** `NEIGHBORS` and `REACH` together define exactly which cells are neighbors.
**REQ-6.3.1 — `all_8`** at reach *r*: every cell within Chebyshev distance *r*, excluding
self. The `(2r+1)²−1` cells of the surrounding square — 8, 24, 48 for r = 1, 2, 3.
**REQ-6.3.2 — `plus_4`** at reach *r*: the four orthogonal **rays**, `4r` cells — 4, 8, 12
for r = 1, 2, 3. Deliberately **not** the Manhattan diamond, so "plus_4" keeps its
intuitive meaning at every reach.

```
all_8, reach 2            plus_4, reach 2
o o o o o                 . . o . .
o o o o o                 . . o . .
o o X o o                 o o X o o
o o o o o                 . . o . .
o o o o o                 . . o . .
(24 neighbors)            (8 neighbors)
```

**REQ-6.3.3** The permitted offset set for `look` is exactly the neighbor set above. The
permitted direction set for `move` is the four orthogonal headings for `plus_4`, all eight
for `all_8`.

### 6.4 Tick application order

**REQ-6.4** One tick is applied in exactly this order. The order is part of the
specification; changing it changes rule semantics.

```python
def apply_tick(rule, cells, tick, dice):
    """Advance one tick and apply all harness-owned semantics.

    Affects: the observable behavior of every rule using a modifier.

    Note what is absent: the rule cannot consume randomness (REQ-7.4.1).
    Every draw here is the harness's, and they are the only reason a run's
    RNG state advances after tick 0.
    """

    # 1. The rule proposes a whole next grid. It sees pre-tick `age`, so the
    #    stubbornness comparison below uses the age entering the tick.
    proposed = rule.step(cells)

    # 2. `rate` gate. Cells not scheduled this tick keep their previous values
    #    entirely -- the proposal for them is discarded, not blended. Uses
    #    merge_cells because Cells is not an ndarray (REQ-6.2).
    #    Affects: gated cells are NOT counted as changed, so they neither
    #    reset age nor trigger a birth draw.
    scheduled = (tick % cells.rate) == 0
    proposed = merge_cells(scheduled, proposed, cells)

    # 3. `stubbornness` gate. A kind change is refused if the cell has not
    #    held its current kind long enough. Uses pre-tick age.
    #    Affects: propagation speed. High stubbornness turns fast rules slow
    #    rather than changing what they converge to.
    proposed.kind = np.where(cells.age >= cells.stubbornness,
                             proposed.kind, cells.kind)

    # 4. Birth draws for `assign_when: birth` modifiers and slots, for cells
    #    whose kind actually changed after steps 2 and 3. Skipped entirely
    #    when nothing was born (REQ-5.6.2) -- that is what lets a settled
    #    system stop advancing the RNG and become exactly frozen.
    born = proposed.kind != cells.kind
    if born.any():
        apply_birth_assignments(proposed, born, dice)

    # 5. Derived properties last, so they describe the tick that just ended.
    proposed.changed_last_tick = born
    proposed.age = np.where(born, 0, np.minimum(cells.age + 1, 65535))

    return proposed
```

**REQ-6.6** `apply_birth_assignments` is the only consumer of `dice` after tick 0.

### 6.7 The Dice facade

**REQ-6.7** `dice` is a small facade over a seeded `numpy.random.Generator`, not the
generator itself. Only whole-array operations are exposed, so there is no scalar draw to
tempt a per-cell loop.

```python
class Dice:
    """The only randomness available, and only inside make_start()
    (REQ-7.4.1).

    Affects: reproducibility. Every method draws for a whole (height, width)
    array in one call, in a fixed order, so a run is reproducible from its
    seed. There is deliberately no scalar draw and no shape argument -- the
    shape is always the grid.
    """

    def chance(self, p):
        """Boolean array, True with probability p."""

    def integers(self, low, high):
        """Integer array, uniform in [low, high)."""

    def choice(self, n):
        """Integer array, uniform in [0, n)."""
```

**REQ-6.7.1** Additions to this surface are a spec change requiring a new REQ identifier,
not an implementation decision.

---

## 7. The Rule Plugin Contract

**REQ-7.1** A generated rule is a Python module defining exactly one top-level class named
`Rule`, with no base classes, decorators, or metaclass.

```python
class Rule:
    KINDS: int              # how many kinds a cell can be, 2..8
    NEIGHBORS: str          # "all_8" or "plus_4"
    REACH: int              # how far away still counts as a neighbor, 1..3
    USES: list[str]         # optional core properties, e.g. ["energy"]
    READS: list[str]        # derived properties read, e.g. ["age"]
    MODIFIERS: list[str]    # catalog modifiers in scope
    SEMANTIC_SLOTS: dict    # see REQ-5.5.2, or {}
    ASSIGN: dict            # modifier draws, see REQ-5.6
    SUGGESTED_DISPLAY: dict # e.g. {"color": "kind", "brightness": "energy"}

    def __init__(self, dice) -> None:
        """`dice` may be used in make_start only. See REQ-7.4.1."""

    def make_start(self, width: int, height: int) -> Cells:
        """Build the tick-0 grid via make_cells. The only place randomness
        is permitted."""

    def step(self, cells: Cells) -> Cells:
        """Return the NEXT grid. Deterministic. Must not modify its input."""
```

**REQ-7.1.1** `SUGGESTED_DISPLAY` names which property drives color and which drives
brightness. It is advisory — the UI default and the user override both take precedence
(REQ-13.2) — and it never affects any fingerprint.

### 7.2–7.7 Constraints stated in the generation prompt

**REQ-7.2** No imports. `np`, the helpers from §6, `make_cells`, and enum constants are
pre-bound.
**REQ-7.3** No file, network, subprocess, or clock access.
**REQ-7.4** No mutable state on the `Rule` instance. `step` may not assign to `self`.
Constants set in `__init__` are permitted.
**REQ-7.4.1 — `step` is deterministic.** `self.dice` may appear only inside `make_start`.
Any reference in `step` is a validation failure. Random initial conditions with a
deterministic law is the cleaner experiment, and it removes the ambiguity where the same
grid at two ticks has different futures because the RNG advanced.
**REQ-7.5** `step` must not modify the grid it receives. Copy first.
**REQ-7.6 — Simplicity limit.** `step` may contain at most `SIMPLICITY_LIMIT` (default 40)
branch, loop, and comprehension AST nodes.
**REQ-7.6.1 — Runtime limit, separate mechanism.** The simplicity limit does not bound
runtime: `while True: pass` is one node and nested grid loops are fewer than ten.
Therefore:

- `ast.While` is **banned outright.** Vectorized rules have no legitimate use for it.
- `ast.For` is permitted **only** over `range(n)` with a literal `n <= 8`, or over a
  literal tuple or list. Any loop whose bound derives from a grid dimension is rejected.
- Every run executes in a **child process** with `RUN_MEMORY_LIMIT_MB` via `setrlimit`. The
  parent owns the per-tick wall clock and kills the child on `TICK_TIMEOUT_SECONDS`. Python
  cannot safely terminate a runaway thread, and `signal.alarm` is not usable under
  FastAPI's worker threads.
- The Stage C trial run executes at **full configured grid size**, not 16×16. Ten ticks at
  200×200 is nearly free vectorized and catches a timeout directly rather than inferring it
  from the AST.

**REQ-7.7** Derived properties are read-only and must be declared in `READS` (REQ-4.3.2).
Modifier and slot arrays are read-only (REQ-4.5).

### 7.8 Validation — Stage C

**REQ-7.8** Every generated rule passes all of the following before entering the library as
`ok`:

1. **Structure.** Exactly one top-level `ClassDef` named `Rule`, no bases, decorators, or
   metaclass. Class body contains only the approved constant assignments and the three
   method definitions.
2. **Static check.** Reject on: any import; any dunder attribute access; `ast.While`; a
   non-conforming `ast.For`; a non-literal spatial offset (REQ-6.2.2); an offset outside
   the declared neighborhood; `self.dice` outside `make_start`; assignment to `self` inside
   `step`; writes to derived, modifier, or slot arrays; a core property not in `USES`; a
   derived read not in `READS`; a modifier not in `MODIFIERS`; or simplicity limit
   exceeded.
3. **Declaration match.** `KINDS`, `NEIGHBORS`, `REACH`, `USES`, **`READS`**, `MODIFIERS`,
   `SEMANTIC_SLOTS`, and `ASSIGN` must exactly match what Stage A declared. A mismatch
   means the implementation silently rewrote the experiment.
4. **Load check.** Import into the restricted namespace (REQ-7.9). Reject on exception.
5. **Trial run.** Full grid size, 10 ticks, fixed seed, in the child process. Reject on
   exception, wrong shape or dtype, values outside declared ranges, modification of the
   input grid, an out-of-contract offset raised at runtime, or per-tick timeout.
6. **Reproducibility check.** Run the trial twice with the same seed and compare
   fingerprints. Reject if they differ. **This does not catch order-dependent random
   draws** — a fixed-order loop reproduces perfectly. REQ-7.4.1 handles that class
   statically. This check catches nondeterminism from other sources.
7. **One repair attempt.** On rejection, return the specific failing check and error text to
   the model once. If the repair fails, mark `broken`, store the error, stop.

**REQ-7.8.1** Broken rules remain in the library permanently and appear in Stage A context.

### 7.9 Restricted execution namespace

**REQ-7.9** Generated code executes with an explicit `__builtins__` dictionary and a NumPy
proxy exposing only approved operations. **Contract enforcement, not security**
(REQ-3.10) — full NumPy includes file I/O, and Python builtins include `open`, `eval`,
`exec`, and `getattr`.

**REQ-7.9.1 — Approved builtins:** `len`, `range`, `min`, `max`, `abs`, `int`, `float`,
`bool`.
**REQ-7.9.2 — Approved NumPy surface:** `zeros`, `ones`, `full`, `zeros_like`, `ones_like`,
`full_like`, `where`, `minimum`, `maximum`, `clip`, `abs`, `sign`, `mod`, `floor_divide`,
`logical_and`, `logical_or`, `logical_not`, `logical_xor`, `sum`, `count_nonzero`, and the
dtypes `uint8`, `uint16`, `int32`, `float32`, `bool_`. Array methods limited to `astype`,
`copy`, and `sum`.
**REQ-7.9.3** Additions to either list are a spec change requiring a new REQ identifier.
**REQ-7.9.4** `np.random` is absent from the proxy entirely. Randomness reaches generated
code only through the `Dice` facade (REQ-6.7), and only in `make_start`.

### 7.10 Lineage

**REQ-7.10** Stage A may propose a **variation** on one earlier rule. Its output includes
`mode` (`"new"` or `"variation"`), `parent_rule_id`, and a one-sentence `change`.
**REQ-7.10.1** `parent_rule_id` must be one of the rule IDs actually supplied in the Stage A
examples. Any other value is a generation failure, not a rule failure.
**REQ-7.10.2** In variation mode, Stage B additionally receives the parent's description and
source.
**REQ-7.10.3** Controlled by `LINEAGE_CHANCE`, **default 0.0.** The path is built and
tested; the behavior is off.

### 7.11 Rejected descriptions

**REQ-7.11** When a rule reaches `broken`, the Stage A description, its reasoning, its
concept tags, and the failing check are retained in `rejections`.
**REQ-7.11.1** The reason: the simplicity limit rejects longer implementations, and richer
English descriptions produce longer implementations. Rejections are therefore
**systematically biased against semantically rich descriptions**, and the corpus
under-represents exactly the region the semantic framing exists to explore. The bias is
acceptable but must be measurable.

---

## 8. The Library and the Coverage Map

**REQ-8.1** Stage A is never sent a list of rules. It is sent a coverage map, which stays
the same size forever.

**REQ-8.2 — Coverage map axes:**

`KINDS` × `NEIGHBORS` × `REACH` × **requested shape** × **modifier in scope** ×
**slots used (bool)**

Shape is one of `count_based`, `threshold`, `even_odd`, `lookup_table`, `copying`, `walker`,
`other`.

**REQ-8.2.1 — Two shape tags.** `requested_shape` comes from Stage A's declaration.
`observed_shape` is inferred from the implementation — statically where possible, by a small
LLM call where not. Both stored. A generator claiming a walker and implementing a threshold
rule is producing useful generator-quality data. The coverage map uses `requested_shape`,
because that is what Stage A was reasoning about.

**REQ-8.8 — Each map cell carries three counts, not one:** attempts, successful canonical
runs, and rejections. Outcome distribution is computed over the successful runs only.

**REQ-8.8.1** The reason: with outcomes alone, a semantic region the generator repeatedly
*fails to implement* looks permanently unexplored, and Stage A keeps attacking it forever.
Attempts and rejections make the difference between "nobody has tried this" and "this has
been tried eleven times and never compiled" visible in the same table.

**REQ-8.3 — Stage A context budget: 2,000–3,000 tokens**, in this order:

1. **Totals.** "412 rules so far: 38% settle, 41% repeat, 18% noisy, 3% structured."
2. **The coverage map**, with all three counts per cell.
3. **Examples**, in three groups: most recent, most notable, and a handful from thinly
   attempted map cells.
4. **Recent failure modes**, from the rejection tally.

**REQ-8.3.1 — Rejected approach.** Showing only the interesting rules. The generator loses
all sense of how rare interesting is and begins assuming its ideas usually work.

**REQ-8.5 — Machine observations only.** Stage A context is built exclusively from
machine-derived outcomes. User behavior overrides (REQ-9.14) and user flags (REQ-12.7) are
stored and displayed but **never enter the generation context.** REQ-16.1 excludes user
influence over generation.
**REQ-8.5.1** "Most notable" is computed from machine signals — `structured` classification,
outlier metrics, unusual loop lengths — not from user flags.

**REQ-8.6 — One rule, one vote.** The coverage map counts each rule's **canonical run** only
(`runs.is_canonical`, set on the first run). Additional runs belong to analysis. Without
this, a user rerunning an interesting rule twenty times silently reweights the distribution
Stage A reasons over — user influence over generation through the back door.

**REQ-8.4** Description clustering is deferred until roughly 300 rules, when the example
groups stop being representative.

**REQ-8.7 — Concept tagging.** Each description is tagged at generation time against a fixed
controlled vocabulary (`spreads`, `resists`, `copies`, `decays`, `counts`, `remembers`,
`moves`, `competes`, ...), stored in `rules.concepts_json`.
**REQ-8.7.1** The reason: the corpus's stated value (REQ-1.4) is the link between
natural-language ideas and observed behavior, and questions like "which concepts produce
persistent moving structures" cannot be asked of free text across 50,000 rows without
reprocessing all of them — by which point the generating model has changed and the tagging
is inconsistent. The vocabulary is fixed in v1 and versioned via `prompt_set_hash`.

---

## 9. Running a Rule, and the State Model

**REQ-9.1** A **run** is one rule, one starting grid, up to `MAX_TICKS` ticks, executed to
completion server-side before playback begins.
**REQ-9.1.1** This makes playback pure scrubbing over stored immutable history.

### 9.7 Computational state versus pattern state

**REQ-9.7** These are different things. **Loop equality means equality of all
future-relevant state, not a quiet picture.**

**REQ-9.7.1 — Computational fingerprint.** Covers everything determining the future:

- every rule-owned array (`kind` plus each entry in `USES`)
- every modifier array in `MODIFIERS`, and every semantic slot array
- every derived array required by REQ-9.7.6
- **scheduler phase** — `tick % 12` when `rate` is in scope. Twelve is the least common
  multiple of the permitted rates 1–4; without it, two identical grids at different points
  in the rate cycle have different futures.
- **RNG state** — the serialized bit generator state, when any birth assignment is declared.

**REQ-9.7.2** Computed over **exact bytes. Floats are never quantized.** Quantizing can
collapse two computationally distinct states into a false loop, which is worse than missing
a real one.

**REQ-9.7.3 — Pattern fingerprint.** `kind` only. Renamed from `visual_fingerprint` in v2,
which was a misnomer: the default renderer maps `age` to brightness, so this is not a
fingerprint of what is displayed. It is a fingerprint of the pattern of kinds.

**REQ-9.7.4** Both use blake2b-128. Arrays are hashed in **name-sorted order**, each
preceded by its name and dtype, so the hash is stable across changes in allocation order.

**REQ-9.7.5** The pattern fingerprint is **an observation only.** It never terminates a run
(REQ-9.8.1) and never enters the computational fingerprint.

**REQ-9.7.6 — Which derived arrays enter the computational fingerprint.** Not only those the
rule reads. The rule is one consumer of derived state; **active harness semantics are
another.** The dependency set is:

- `age` at full precision when `"age" in READS` — the rule may compare it against any value.
- `age` clamped to `minimum(age, 3)` when `stubbornness` is in scope but `age` is not in
  `READS`. The harness only ever evaluates `age >= stubbornness`, and stubbornness is capped
  at 3, so ages above 3 are indistinguishable to the future. Clamping is what allows a
  stubbornness rule to report `frozen` at all — unclamped, `age` increments every tick until
  it saturates at 65535, far beyond `MAX_TICKS`, and exact freezing becomes impossible.
- `changed_last_tick` when it appears in `READS`.

**REQ-9.7.6.1** When a future modifier consumes derived state, its dependency — and the
tightest correct clamp — is added here. Adding a modifier without updating this requirement
is a loop-detection bug, not a feature gap.

**REQ-9.7.7** Because birth draws are skipped when nothing was born (REQ-5.6.2), a stochastic
rule that settles stops advancing the RNG and *can* reach `frozen`. A stochastic rule that
keeps producing births will not, and will run to its tick budget. Both are correct.

**REQ-9.2 — Recorded every tick:**

- Tick number.
- Rule-owned and modifier/slot arrays — snapshot every `SNAPSHOT_EVERY` ticks,
  difference-only between (REQ-12.5). Derived arrays are **not** stored (REQ-12.6).
- How many cells of each kind.
- `variety` (REQ-9.10).
- `cells_changed` — how many cells changed `kind` since the previous tick. (Standard term:
  Hamming distance.)
- `state_fingerprint` and `pattern_fingerprint`.

### 9.8 Stopping conditions

**REQ-9.8** Checked every tick, in this precedence:

| Condition | Trigger |
|---|---|
| `frozen` | Computational fingerprint equals the previous tick's. |
| `looping` | Computational fingerprint seen earlier this run. Loop length recorded. |
| `ran_out` | Tick budget exhausted. |
| `too_slow` | A single tick exceeded `TICK_TIMEOUT_SECONDS`. |

**REQ-9.8.1 — Nothing stops because the pattern went quiet.** A rule with `USES=["memory"]`
may increment `memory` for fifty ticks and then flip `kind`. Its pattern fingerprint is
unchanged throughout, and a quiet-pattern stop would kill the run before the behavior
occurs. The same holds for `energy` and for any future hidden property. Arbitrary hidden
state can produce arbitrarily long pattern latency, so the only trustworthy stops are exact
recurrence, the tick budget, and the timeout.

**REQ-9.15 — `kind_quiet_for`** is recorded every tick: how many consecutive ticks the
pattern fingerprint has been unchanged. An observation and a classifier input, never a
stopping condition.

**REQ-9.9** A map of computational fingerprint → tick number, held for the run, is the entire
exact-loop detector. Tick 0 participates (REQ-4.6.3).

**REQ-9.10 — `variety`** is Shannon entropy of the `kind` distribution divided by
`log(KINDS)`: 0.0 for a single kind present, 1.0 for a perfectly even spread. Over `kind`
only.

**REQ-9.11 — `pattern_settled_at`** is the earliest tick after which the pattern fingerprint
never changes again. Computable only at run end. Null if it never stops changing.

### 9.12 Describing a run afterward

**REQ-9.6** Wolfram's numbered classes, renamed. Stored as a guess **alongside the numbers
that produced it**, never as fact.

**REQ-9.16 — Deterministic classifier.** No qualitative bands. Let *W* be the final 100
ticks of the run (or the whole run if shorter), `change_rate` the mean of `cells_changed`
over *W* divided by `width × height`, and `mean_variety` the mean of `variety` over *W*.

| Order | Label | Condition |
|---|---|---|
| 1 | `repeats` | `stopped_because == looping` and `loop_length <= 50` |
| 2 | `unclassified` | `stopped_because == looping` and `loop_length > 50` |
| 3 | `unclassified` | `stopped_because == too_slow` |
| 4 | `settles` | `stopped_because == frozen` |
| 5 | `settles` | `change_rate < 0.0005` (pattern stopped moving without exact freeze) |
| 6 | `noisy` | `change_rate >= 0.10` and `mean_variety >= 0.60` |
| 7 | `structured` | `0.0005 <= change_rate < 0.10` and `mean_variety < 0.60` and the linear slope of `cells_changed` over *W* is greater than `-0.001 × width × height` per tick |
| 8 | `unclassified` | anything reaching this row |

**REQ-9.16.1** `guess_confidence` is `low` for rows 5, 7, and 8, and `high` otherwise. Row 7
is the unreliable one: it is a threshold heuristic standing in for "stable shapes that move
or persist," and the slope term exists only to separate persistence from slow decay.

**REQ-9.16.2** `broken` is **not** a run classification. A broken rule fails before any run
exists; its status lives on the rule, not on a run.

**REQ-9.13** `unclassified` is a real outcome, not an error. A long loop is genuinely not the
same phenomenon as a short one, and forcing it into `repeats` would corrupt the coverage
distribution.

**REQ-9.14** The user may overrule the guessed behavior. Stored in a separate column, never
overwrites the guess, never enters generation context (REQ-8.5).

---

## 10. Generation Prompts

**REQ-10.1** Prompt templates live in version control as files, not string literals. They
are the highest-leverage artifact in the project and must be diffable.
**REQ-10.5** The template set is hashed into `prompt_set_hash`, and the **fully rendered**
prompts are stored per rule (REQ-12.4).

### 10.2 Stage A — invent and describe

```
You are inventing a cellular automaton rule for a research library.

The library exists to find simple rules that produce surprising behavior.
Simple is the point. A rule that is complicated is a failure even if its
output is pretty.

WHAT A CELL IS
{cell_schema}

NEIGHBORHOOD GEOMETRY
{geometry_spec}

MODIFIERS AVAILABLE FOR THIS RULE
{modifier_blurbs}
You may use at most one. You may use none.

SEMANTIC SLOTS
{slots_availability}

CONCEPT VOCABULARY
{concept_vocabulary}

WHAT WE HAVE TRIED SO FAR
{library_summary}
Each coverage cell shows attempts, successful runs, and rejections. A cell
with many attempts and no successes is not unexplored -- it is difficult.

Propose ONE rule to try next. Return JSON:
{
  "mode": "new" | "variation",
  "parent_rule_id": <required if variation; must be an ID shown above>,
  "change": "<required if variation; one sentence, one thing changed>",
  "description": "Plain English. What a cell looks at, and what it becomes.
                  Written for someone who will implement it without asking
                  you questions.",
  "reasoning":   "Why this is useful given the above. Reference coverage
                  gaps or prior outcomes directly.",
  "kinds": <int 2-8>,
  "neighbors": "all_8" | "plus_4",
  "reach": <int 1-3>,
  "uses":    [<optional core properties>],
  "reads":   [<derived properties your rule will read>],
  "modifiers": [<at most one, from the list above>],
  "semantic_slots": {<see schema, or {}>},
  "assign": {<modifier draws, or {}>},
  "suggested_display": {"color": "<property>", "brightness": "<property>"},
  "shape": "count_based"|"threshold"|"even_odd"|"lookup_table"|"copying"|"walker"|"other",
  "concepts": [<2-4 tags from the vocabulary above>]
}
```

### 10.3 Stage B — implement

```
Implement this rule as a Python class.

THE RULE
{description}

DECLARED PROPERTIES
{declared_properties}

THE CONTRACT
{plugin_contract}

AVAILABLE IN YOUR NAMESPACE
{helper_signatures}
{dice_facade}
{approved_numpy_surface}

HARD RULES
- No imports. numpy is bound as np, restricted to the surface above.
- Build your starting grid with make_cells(). Cells has no constructor and
  no arithmetic -- it is a bag of named arrays, not an array.
- Do not modify the grid passed to step(). Copy it first.
- step() must be deterministic. self.dice may be used ONLY in make_start(),
  and only through the methods listed above.
- step() may not assign to self.
- age and changed_last_tick are read-only, and any you use must appear in
  READS.
- Modifier and semantic slot arrays are read-only. Declare draws in ASSIGN;
  the harness performs them.
- Spatial helpers take literal offsets only, and every offset must lie
  inside your declared neighborhood. look() observes; move() displaces by
  exactly one cell. There is no unrestricted shift.
- No while loops. for loops only over range(n) with a literal n <= 8, or
  over a literal tuple or list. Never loop over grid dimensions -- use the
  helpers and whole-array operations.
- step() may contain at most {simplicity_limit} branches, loops, and
  comprehensions combined. Simpler is better. If your implementation is
  near the limit, the rule is wrong, not the limit.
- Your declared KINDS, NEIGHBORS, REACH, USES, READS, MODIFIERS,
  SEMANTIC_SLOTS, and ASSIGN must match the values above exactly.

Return exactly one complete `class Rule:` definition, including the class
statement itself. No imports, no top-level statements outside the class, no
prose, no markdown fences.
```

### 10.4 Repair

**REQ-10.4** The repair prompt contains the original Stage B prompt, the returned code, and
the **specific** failure — the failing check by name, plus the exception text or the
offending AST node. One attempt only.

---

## 11. HTTP API

**REQ-11.1**

| Method | Path | Purpose |
|---|---|---|
| POST | `/rules/generate` | Full pipeline, streamed. REQ-11.4. |
| GET | `/rules` | Library list, paged, filterable by status, behavior, concept. |
| GET | `/rules/{id}` | One rule with source, provenance, and its runs. |
| POST | `/rules/{id}/runs` | Run again with a new seed. Never canonical. |
| GET | `/runs/{id}` | Run metadata and summary numbers. |
| GET | `/runs/{id}/grids?from=&to=&props=` | Packed grids for a tick range. REQ-11.5. |
| GET | `/runs/{id}/cell/{y}/{x}?props=` | One cell's history. REQ-11.2. |
| PATCH | `/runs/{id}` | Set `user_behavior` and `user_flagged`. Nothing else. |
| GET | `/catalog/modifiers` | Read-only in v1. |
| GET | `/library/summary` | Coverage map, totals, rejection tally. |

**REQ-11.4 — Progress streaming.** `POST /rules/generate` responds `text/event-stream` and
emits `stage_a_started`, `stage_a_complete`, `stage_b_started`, `stage_b_complete`,
`validating`, `validation_failed`, `repairing`, `running`, `tick_progress`, and `complete`.
This satisfies REQ-13.7 without a job queue, leaving REQ-3.6 intact.

**REQ-11.4.1** The browser's native `EventSource` **cannot issue a POST.** The frontend must
consume this with streaming `fetch()` and a `ReadableStream` reader. Do not "fix" this by
converting the API into an asynchronous POST-then-GET job model — that reintroduces exactly
the queue REQ-3.6 excludes.

**REQ-11.5 — Wire format.** Grid payloads are packed binary, never nested JSON arrays.
Twenty million JSON integers per property per run is not a viable transport for 30fps
playback.

**REQ-11.5.1 — Framing**, specified so both ends cannot invent incompatible protocols:

```
bytes 0..3     uint32, little-endian: byte length of the JSON header
bytes 4..N     UTF-8 JSON header:
                 { "ticks": [from, to],
                   "shape": [height, width],
                   "properties": [
                     {"name": "kind", "dtype": "uint8",
                      "offset": <bytes from start of payload region>,
                      "length": <bytes>}
                   ] }
bytes N..       payload region: C-order array blocks at the stated offsets
```

**REQ-11.2 — Reconstruction cache.** Cell history requires one position across every tick,
which means reconstructing the run. Reconstruct **per requested property**, cache, evict LRU
against `RUN_CACHE_BUDGET_MB`.
**REQ-11.2.1** For 500 ticks at 200×200: a uint8 property is 20 MB, `age` at uint16 is 40 MB,
a float32 property is 80 MB. The cache budget is in **bytes, not runs.**
**REQ-11.3** No endpoint may modify a stored run other than `PATCH /runs/{id}` setting
`user_behavior` and `user_flagged`. Recorded history is immutable.

---

## 12. Storage

**REQ-12.1**

```sql
rules(id, created_at,
      mode, parent_rule_id, change_note,
      description, reasoning,
      kinds, neighbors, reach,
      uses_json, reads_json, modifiers_json, semantic_slots_json, assign_json,
      suggested_display_json,
      requested_shape, observed_shape, concepts_json,
      source_code, source_hash,
      status,                  -- ok | broken
      failed_check, error_text,
      engine_version, prompt_set_hash, modifier_catalog_hash, helper_version,
      model_id, model_params_json,
      stage_a_rendered, stage_a_raw,
      stage_b_rendered, stage_b_raw,
      repair_rendered, repair_raw)

runs(id, rule_id, created_at, start_seed, width, height, max_ticks, ticks_run,
     is_canonical,
     stopped_because,          -- frozen | looping | ran_out | too_slow
     loop_length, pattern_settled_at,
     guessed_behavior, guess_confidence, user_behavior, user_flagged,
     engine_version)

ticks(run_id, tick, payload_encoding, payload_blob,
      variety, cells_changed, kind_quiet_for, kind_counts_json,
      state_fingerprint, pattern_fingerprint,
      PRIMARY KEY (run_id, tick))

modifier_catalog(name, type_spec, default_value, applied_by, effect,
                 assign_when, availability, blurb)

rejections(id, created_at, rule_id, failed_check,
           stage_a_description, concepts_json, requested_shape,
           kinds, neighbors, reach, modifier_in_scope)
```

**REQ-12.4 — Provenance.** Every rule stores `engine_version` (git revision),
`prompt_set_hash`, `modifier_catalog_hash`, `helper_version`, `model_id`,
`model_params_json`, and both the **fully rendered** prompts and the raw responses for
Stage A, Stage B, and repair.

**REQ-12.4.1** Rendered prompts, not just template hashes. A template hash does not
reconstruct the coverage summary that was actually injected into Stage A at the time, and
that summary *is* the reasoning input. Without it, the most interesting question the corpus
can answer — what the generator was looking at when it proposed something — is unanswerable.

**REQ-12.4.2** `source_hash` cannot tell you that `count_neighbors` changed, a prompt was
reworded, or modifier semantics moved. Two runs of byte-identical source under different
harness revisions are **different experiments**, so every run is stamped with the engine
revision that produced it.

**REQ-12.2** `source_hash` catches byte-identical regenerations. It will not catch two rules
that behave identically but are written differently. Accepted.

**REQ-12.5 — Tick payload encoding.** `payload_encoding` is `snapshot`, `sparse`, or `dense`.
A snapshot is written every `SNAPSHOT_EVERY` ticks. Between snapshots, store a
**changed-index list** when few cells changed and a **dense XOR** when many did — whichever
is smaller for that tick. All payloads are Zstandard-compressed.

**REQ-12.6 — Derived arrays are not stored per tick.** `age` and `changed_last_tick` are
exactly reconstructable from the `kind` history and are omitted from delta payloads.

**REQ-12.6.1** The reason: `age` changes on nearly every cell every tick, so including it
would make almost every *settled* tick dense and destroy the value of sparse encoding — the
exact case REQ-12.5 exists to optimize. At configured dimensions this saves roughly 40 MB per
run for `age` alone.

**REQ-12.6.2** `age` **is** included in snapshots. Reconstruction otherwise requires walking
`kind` from tick 0, because a cell's age can exceed the snapshot interval; with age in the
snapshot, reconstruction walks forward at most `SNAPSHOT_EVERY` ticks. The cost is roughly
0.8 MB per run.

**REQ-12.7 — `user_flagged`** is a boolean on `runs`, writable only through `PATCH`. It marks
a run as interesting to the user, is shown in the library browser, and is **excluded from
Stage A context** (REQ-8.5).

**REQ-12.3** Index `ticks(run_id, tick)`, `rules(status, requested_shape)`, and
`runs(rule_id, is_canonical)`.

---

## 13. Frontend

**REQ-13.1** Canvas grid renderer. 200×200 at 30fps playback.
**REQ-13.2 — Display mapping.** Any property may drive color; any may drive brightness.
Precedence: user override, then `SUGGESTED_DISPLAY` from the rule (REQ-7.1.1), then the
default of `kind` → color and `age` → brightness. Display mapping never affects any
fingerprint.
**REQ-13.3 — Transport.** Play, pause, one tick forward, one tick back, jump to tick, speed.
Playback reads stored ticks and never re-runs the rule.
**REQ-13.4 — Cell inspection.** While paused, clicking a cell shows all its property values,
its neighbors' values, and a strip of that cell's own history across the run. Strictly
read-only.
**REQ-13.5 — Numbers panel.** `variety`, `cells_changed`, and `kind_quiet_for` against ticks,
current tick marked, `pattern_settled_at` indicated if present.
**REQ-13.6 — Library browser.** Every rule with description, status, stop reason, behavior,
confidence, modifiers, and concepts. Filterable by concept and by `user_flagged`. Click
through to source, provenance, or a new run.
**REQ-13.7 — Run New Rule.** One button, showing live progress through the pipeline stages
from the stream (REQ-11.4), including validation failures and the repair attempt.
**REQ-13.8** Controls to overrule the guessed behavior and to flag a run.
**REQ-13.9** Modifier catalog view, read-only in v1.
**REQ-13.11** Where a run ended `ran_out` with a high `kind_quiet_for`, the UI says the
pattern stopped moving while the underlying state kept changing, and shows which properties
were still active. This is the case REQ-9.8.1 deliberately refuses to terminate, and the user
should be able to see it rather than wonder why a still image ran for five hundred ticks.

---

## 14. Reference Rules

**REQ-14.1** Three hand-written fixtures ship with the system, so the harness can be tested
independently of the generator. Without them, a harness bug and a bad generation are
indistinguishable.

| Fixture | Exercises | Expected outcome |
|---|---|---|
| `life` | `count_neighbors`, two kinds, all_8 reach 1 | `structured` — gliders survive and travel |
| `majority` | Simple counting, fast convergence | `settles` within ~50 ticks |
| `walker` | `heading`, `move`, single moving cell | `looping`, loop length equal to grid width |

**REQ-14.2** A glider in `life` must cross the wrap boundary intact. This is the single best
end-to-end proof that the wrap logic is correct — every generated rule inherits that bug if
it exists.
**REQ-14.3** Fixtures obey the full contract, so they also serve as worked examples in the
Stage B prompt if few-shot proves necessary.
**REQ-14.4** A fourth fixture, `slow_burn`, is test-only and not shown in the library: it
increments `memory` for sixty ticks with `kind` unchanged, then flips. It exists solely to
prove REQ-9.8.1 — that a quiet pattern never terminates a run.

---

## 15. Testing

**REQ-15.1** Harness tests run against fixtures only, never generated rules.
**REQ-15.2** Every modifier has a test asserting that at its default value, output is
bit-identical to the same rule run with the modifier absent. REQ-5.1 as an executable check.
**REQ-15.3** Every fixture, run twice with the same seed, produces identical fingerprints at
every tick.
**REQ-15.4** Reconstruction is tested by rebuilding every tick of a fixture run and comparing
to grids captured live — across all three payload encodings, and including derived arrays
rebuilt per REQ-12.6.
**REQ-15.5** Validation tests use hand-written *bad* rules, one per rejection path: an import;
an input mutation; a simplicity-limit overrun; a `while` loop; a `for` over a grid dimension;
`self.dice` in `step`; an assignment to `self` in `step`; a write to `age`; a write to a
modifier array; an undeclared `READS`; a `look` offset outside the declared neighborhood; a
computed (non-literal) offset; a diagonal `move` under `plus_4`; and a declaration mismatch
with Stage A **including a `READS` mismatch**.
**REQ-15.6 — State-model tests:**
- A rule declaring `READS = ["age"]` must not report `frozen` on a static grid.
- The same rule without that declaration must report `frozen` on the same grid.
- A rule with `stubbornness` in scope and no `READS` must report `frozen` on a static grid
  once all ages exceed 3 — proving the clamp in REQ-9.7.6 works.
- A `rate`-gated rule must not report `looping` at a tick offset where scheduler phase
  differs.
- A stochastic rule that settles must report `frozen` once births cease (REQ-9.7.7).
- A stochastic rule with continuous births must run to its tick budget.
**REQ-15.7** A timeout test: a fixture with a deliberate long tick is killed by the parent and
recorded as `too_slow` without taking the server down.
**REQ-15.8** `slow_burn` (REQ-14.4) must run past tick 60 and record the `kind` flip. A run
terminating before tick 60 is a REQ-9.8.1 regression.

---

## 16. Explicitly Not in v1

**REQ-16.1** Any user influence over generation. REQ-8.5 and REQ-8.6 close the two back doors.
**REQ-16.2** Editing the modifier catalog from the UI.
**REQ-16.3** Live streaming of a run in progress; open-ended runs with no tick budget.
**REQ-16.4** Grid editing, hand-seeded shapes, drawing initial states, branching a run from a
paused tick. Perturbation turns history from a tick list into a version tree, with branch,
diff, and provenance questions attached. Different product.
**REQ-16.5** Non-grid layouts.
**REQ-16.6** Rule composition.
**REQ-16.7** Multi-user, accounts, per-user configuration.
**REQ-16.8** Sandboxing of generated code.
**REQ-16.9** Any claim about how much of a rule space has been covered.
**REQ-16.10** GPU or shader targets. Transpiling to WGSL is a compiler, not a translation, and
harness modifiers depending on a global tick counter and a seeded RNG do not survive the
crossing. The correct route, if ever wanted, is a restricted rule DSL from which both NumPy
and WGSL are generated — which would enforce the simplicity premise harder than REQ-7.6 does.
**REQ-16.11** Parameterized rules with swept thresholds. Attractive — it would turn the library
from a set of points into a set of families and expose phase boundaries — but it changes the
meaning of "a rule" and therefore the entire coverage map. Deferred, not dismissed.

---

## 17. Open Items

**REQ-17.1** `SNAPSHOT_EVERY = 50` is a guess. Tune once storage-versus-reconstruction cost is
measurable.
**REQ-17.2** Whether `structured` detection can be made reliable without a human. REQ-9.16 row
7 is a threshold heuristic and is marked low-confidence. The user-override column accumulates
labeled examples that might support a better detector — most likely one computed over the
stored X×Y×T volume rather than per-tick scalars, since a glider is a straight line in that
volume and an oscillator is a corrugated pillar, and those separate cleanly where the scalars
do not.
**REQ-17.3** `rate` and `age` interact oddly: a cell updating every fourth tick still ages on
the three it skipped. Watch before deciding whether to add an `updates` counter.
**REQ-17.4** Whether semantic slots get used well or degenerate into a second `kind`. REQ-5.5.3
defines the kill criterion.
**REQ-17.6** Whether the concept vocabulary should stay fixed or be allowed to grow. Fixed is
queryable; growing is expressive. Fixed for v1.
**REQ-17.7** REQ-9.16's thresholds are first guesses calibrated against nothing. Re-derive them
from the first two hundred runs and record the revision.
**REQ-17.8** With `visually_frozen` removed, more runs reach `ran_out`, so mean run cost rises.
Measure before assuming `MAX_TICKS = 500` is still the right budget.

---

## 18. Priority of Work

**REQ-18** These affect foundational interfaces or correctness and must be settled before core
abstractions are written: the state model (§9.7), the randomness model (REQ-7.4.1, §6.7), the
`Cells` construction and merge contract (§6.2), bound spatial helpers (§6.2.1), neighborhood
geometry (§6.3), the initialization sequence (§4.6), the Stage B output contract (§10.3), the
restricted namespace (§7.9), runtime enforcement (REQ-7.6.1), and the transport framing
(§11.5.1).

Everything else can be tightened while scaffolding is underway.
