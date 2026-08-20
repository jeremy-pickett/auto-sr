# Autonomous Semantic Ruliology
## Frontend Visualization Uplift — Omnibus 2.2

**Status:** draft, revised. Sections 4, 5, and 6 are specified to contract depth;
Sections 7 and 8 are specified to intent depth and need a calibration pass before code.
**Targets:** Omnibus Requirements **v3**.
**Supersedes:** uplift 2.2 draft v0.1. See §0.7 for what changed and why.
**Companion:** uplift **2.3** holds the scope this document deliberately excludes. Read
§10 here before assuming anything is missing.
**Purpose:** raise the amount of information a single glance at a run conveys, and give
the cell inspector something to point at.

**What this uplift is for, in one sentence:** the grid renderer shows the one layer of
state that is allowed to lie, so this adds a layer that names what actually formed.

---

## 0. Reading This Document

**REQ-0.1 applies unchanged.** Plain language everywhere. `traveler`, not `spaceship`.
`repeater`, not `oscillator`. Standard terms appear once, in a comment, and never in a
column name or a UI label.

### 0.5 Numbering and fold-in

**REQ-0.5 — This document writes into the omnibus namespace, not a private one.** Every
identifier here is a `REQ-` identifier slotted into the omnibus section it belongs to.
There is no `VIS-` prefix, no parallel numbering, and no translation table to maintain.
When this uplift lands, its sections are cut and pasted into v4 of the omnibus and this
file is marked superseded.

**REQ-0.5.1 — Reserved blocks.** The following are claimed by this document and must not
be issued to anything else, including a v4 revision written independently of it. Uplift
2.3 claims a separate, non-overlapping set.

| Block | Belongs to |
|---|---|
| REQ-13.12 – REQ-13.20 | §13 Frontend |
| REQ-15.9 – REQ-15.13 | §15 Testing |
| REQ-16.12 – REQ-16.16 | §16 Explicitly Not in v1 |
| REQ-17.9 – REQ-17.13 | §17 Open Items |
| REQ-19.1 – REQ-19.20 | §19 Recurrent Structure Detection — **new section** |

**REQ-0.5.2 — Version numbers are not aligned and that is not a mistake.** This is
uplift *2.2* against omnibus *v3*. The uplift series numbers proposals; the omnibus
numbers contracts. A reader six months out should not conclude this file predates v3.

**REQ-0.2 applies unchanged.** Nothing in this document retires an existing identifier.
If implementation forces a retirement, it is recorded in this section, not silently
dropped.

### 0.6 What is being fixed

Three complaints drove this, recorded so they are not re-derived:

1. **The cell inspector (REQ-13.4) has no discovery path.** It answers "what is this
   cell doing" for a cell the user already found. On a 40,000-cell grid, finding one is
   the whole problem.
2. **A still picture is currently patched with a paragraph.** REQ-13.11 exists because
   the pattern layer can look dead while the computational layer is running. That is an
   honest disclosure and a poor rendering.
3. **One glance conveys roughly one bit.** A run reads as "moving" or "not moving."
   Everything else — what persists, what travels, what is merely churning — requires
   watching five hundred ticks.

### 0.7 Revision record — what changed from draft v0.1

Four changes, three of them fixes to defects found in review. Recorded rather than
silently applied, because the reasoning matters more than the edits.

| Change | Nature |
|---|---|
| **`kind == 0` is no longer assumed empty** (§4) | **Factual error in v0.1.** REQ-4.2 defines `kind` as "what the cell is" over `0..KINDS-1` and makes no kind empty. The Stage A prompt template *tells* the generator kind 0 is empty ground, but that is generation guidance — validated nowhere, absent from the contract, and unenforced. A rule declaring `0 = predator` or `0 = water` would have broken the detector silently while appearing to work. Replaced with an explicit background declaration (REQ-19.3) and honest marking wherever background is assumed rather than declared. |
| **Renamed to recurrent structures** (throughout) | **Naming defect in v0.1.** The detector finds recurrent connected components. Expanding wavefronts, replicators, irregular domain walls, distributed synchronized patterns, and 400-tick transients that never exactly recur are all structures it cannot see. `structures = []` would be read as "this run has no structure." The noun now says what the detector actually does. |
| **Grouping split from interaction** (REQ-19.3.2) | **Design defect in v0.1**, and the fix for what v0.1 itself flagged as its weakest requirement. "Can influence one another" and "belong to the same object" are different relations. Grouping is now morphological; the declared neighborhood describes interaction *between* grouped objects. Retires the reach-3 blowup that v0.1 could only log as an open item. |
| **Activity views added; relief demoted** (§8, §12) | **Priority correction.** An activity field is nearly free — `changed_last_tick` is already reconstructed — and the kind-stable/state-active view retires complaint 2 above without a paragraph of apology. Relief was the most work for the least research value in v0.1 and is now optional. |

**REQ-0.7** The kind-0 item is recorded as an error rather than a refinement
deliberately. A defect logged as a preference gets re-argued; a defect logged as a
defect gets fixed.

---

## 1. Concept

A recurrent local structure is a group of cells that comes back. Nothing more is assumed
and nothing about Life's named menagerie is hardcoded. The harness does not need to know
what a glider is; it needs to notice that a small clump of cells returned to its own
shape somewhere else, and then say so.

**REQ-19.1 — Detection is observation, not classification.** It reports what recurred.
It does not decide whether a run is interesting, does not set `guessed_behavior`, and
does not enter the coverage map. Those are separate questions with their own
requirements and their own blast radius.

**REQ-19.1.1** The reason: `guessed_behavior` feeds Stage A context (REQ-8.3), so any
change to how it is computed silently reweights what the generator explores. A detector
calibrated against nothing must not be given that lever on its first day. See REQ-17.9.

**REQ-19.1.2 — The noun is narrow on purpose.** This detector finds **recurrent**
structures: groups whose shape returns exactly, in place or displaced. It cannot see an
expanding wavefront, a replicator that doubles rather than returns, a domain wall in
irregular motion, a coherent spiral with a continuously changing boundary, a long-lived
transient that never exactly recurs, or a synchronized pattern whose active parts are
not adjacent. Every one of those is a structure. None satisfies REQ-19.5. An empty
result means *this detector found no exact recurrent components*, and every label,
column, and UI string must be written so that it cannot be read as *this run contains no
structure*.

---

## 2. Decisions and Rationale

| Decision | Why |
|---|---|
| **Background kind is declared, never inferred** (REQ-19.3) | No requirement makes any kind empty. The generator is *told* kind 0 is ground in the Stage A prompt, but prompt text is not a contract and nothing validates it. A semantically named world — `SEA`, `SOIL`, `SKY` — has no empty kind at all, and a detector that assumes one imports Life's ontology into a system built to escape it. |
| **Grouping is morphological; the declared neighborhood is interaction** (REQ-19.3.2) | "Can influence one another" and "belong to the same object" are different relations. Under `all_8` at `REACH = 3` a cell influences a 7×7 window, so grouping by the declared neighborhood merges most of the world into one blob. Grouping at touch-distance gives objects; the declared graph over those objects gives interaction clusters, which is a second thing worth seeing rather than a cost. |
| **Detection matches on `kind` only** (REQ-19.4) | This is REQ-9.7's pattern/computational split applied one level down. A shape that recurs in `kind` while its `energy` climbs is a real phenomenon Life has no word for; matching on every property would render it invisible by calling it "not a structure." |
| **Property drift is an annotation, not a disqualifier** (REQ-19.6.1) | Same reason, stated positively. The drifting case is the one this system can find and Wolfram's numbering cannot. |
| **Detection is post-hoc over stored history** (REQ-19.2) | Mirrors REQ-9.1. Runs already complete before playback; there is no reason to make the hot loop carry this. |
| **Detection output is a cache, not history** (REQ-19.9) | It is derived from immutable ticks and is fully recomputable. Treating it as history would put it under REQ-11.3 and make detector improvements impossible. |
| **New render modes are view-only** (REQ-13.16) | REQ-13.2 already establishes that display never touches a fingerprint. Activity, trails, and relief are display. |
| **Activity views outrank relief** (§12) | The activity field and the kind-stable/state-active view need no detector, no new storage, and answer §0.6 complaint 2 directly. Relief is a shading pass that makes gradients legible — useful, but the least research value per unit of work in this document. |
| **No WebGL** (REQ-3.2, REQ-16.10 unchanged) | Every render mode here is a compositor or shading pass over the existing one-texel-per-cell canvas. None needs a GPU target, and reaching for one would drag in the whole REQ-16.10 argument for no gain. |
| **Structure names are mechanical, not generated** (REQ-19.7) | An LLM asked to name shapes will name shapes, including the ones that are not there. |

---

## 3. Configuration additions

**REQ-3.11** Added to the §3.9 table:

| Variable | Default | Affects |
|---|---|---|
| `STRUCTURE_MIN_CELLS` | 2 | Smallest group that can be called a recurrent structure. |
| `STRUCTURE_MAX_CELLS` | 64 | Largest. Above this the group is terrain, not a structure. |
| `STRUCTURE_MAX_PERIOD` | 32 | Longest recurrence period searched. |
| `STRUCTURE_MIN_REPEATS` | 2 | Times a signature must recur before it is reported. |
| `STRUCTURE_DETECT_BUDGET_SECONDS` | 10.0 | Wall clock for one run's detection pass. |
| `TRAIL_WINDOW_TICKS` | 40 | Ticks composited into one trails frame. |

**REQ-3.11.1** All six are first guesses calibrated against nothing. REQ-17.10 owns
re-deriving them.

---

## 4. Detection — what counts as a group

**REQ-19.2 — When it runs.** Detection runs over a completed, stored run, lazily on
first request, and the result is cached (REQ-19.9). It never runs during generation and
never during playback. Generation stays synchronous (REQ-3.6) and is not slowed by this.

### 4.1 Background

**REQ-19.3 — Background kind is declared, not inferred.** Stage A may declare an
optional `BACKGROUND_KIND`: the single kind, if any, that means "nothing is here."
Cells of that kind are excluded from grouping. The declaration is **analytical metadata
only** — it never affects execution, the tick order, any fingerprint, or the coverage
map, and a rule that declares it wrongly still runs identically.

**REQ-19.3.1 — `none` is a first-class, handled case.** A rule may declare no background
kind, and many will: a world of `SEA` / `SOIL` / `SKY` has no empty state. Where no
background is declared, grouping is performed **per kind** — cells are grouped with
adjacent cells *of the same kind*, and every kind is grouped independently. This is
strictly more general than background exclusion and reduces to it when one kind happens
to dominate.

**REQ-19.3.1.1** The reason for per-kind grouping rather than refusing to detect: a
domain of `SOIL` bordered by `SEA` is a structure whether or not either is "empty," and
a detector that only worked on worlds containing a void would be blind to exactly the
semantically rich rules this project exists to generate.

**REQ-19.3.1.2 — Rules generated before the declaration existed.** Where a rule predates
`BACKGROUND_KIND` and declares nothing, the detector may assume kind 0 is background,
because the Stage A prompt in force at the time told the generator so. Any result
produced under that assumption is stored with an `assumed_background` flag and the UI
says so. An assumption inherited from a prompt template is not a declaration and must
never be presented as one.

### 4.2 Grouping

**REQ-19.3.2 — Grouping is morphological, not interactional.** Two cells belong to the
same group when they touch: adjacency is **`all_8` at reach 1**, independent of the
rule's declared `NEIGHBORS` and `REACH`. Grouping wraps at every edge, per REQ-3.5.

**REQ-19.3.2.1** The reason, stated at length because v0.1 got this wrong: the declared
neighborhood is the relation "these cells can influence one another." Object membership
is the relation "these cells constitute one shape." They are not the same relation, and
conflating them means that under `all_8` at `REACH = 3` — a 7×7 influence window —
nearly every populated cell joins one component, which `STRUCTURE_MAX_CELLS` then
discards. High-reach rules would have reported zero structures for a reason that has
nothing to do with the rules.

**REQ-19.3.3 — Interaction clusters are reported separately.** Over the *groups*
produced by REQ-19.3.2, the rule's declared `NEIGHBORS × REACH` defines a second
relation: two groups are in the same interaction cluster when any cell of one lies
within the declared neighborhood of any cell of the other. Clusters are recorded per
tick range and are the basis for REQ-13.14.2.

**REQ-19.3.3.1** This is the payoff of the split rather than a consolation for it. Object
membership and object interaction become independently visible: *these pixels are one
shape*, and *these three shapes can currently reach each other*. Collisions, approaches,
and the moment two travelers enter each other's range become renderable events rather
than things a user must catch by eye.

**REQ-19.3.4 — Size filter.** Groups outside `[STRUCTURE_MIN_CELLS,
STRUCTURE_MAX_CELLS]` are dropped before matching. A group spanning most of the grid is
terrain, and matching it against itself produces a true but useless answer.

**REQ-19.3.4.1** Where the size filter discards more than half of all grouped cells at a
tick, detection records it. A run reported as structureless because its groups were all
too large is a very different statement from a run with no recurrence, and REQ-13.14.1
requires the UI to distinguish them.

---

## 5. Detection — matching and labels

**REQ-19.4 — Signature.** A group's signature is the set of `(down, right)` offsets from
its bounding-box top-left corner, each paired with that cell's `kind`. Offsets follow the
REQ-6.2.1 convention. The signature is translation-normalized and nothing else: no
rotation, no reflection, no scaling.

**REQ-19.4.1** Signatures are built from `kind` alone. Rule-owned properties (`energy`,
`heading`, `memory`), harness modifiers (`weight`, `stubbornness`, `rate`), and derived
properties (`age`, `changed_last_tick`) are excluded from the signature. See the §2
rationale.

**REQ-19.4.2 — Rejected approach.** Signing on every rule-owned property. It sounds
stricter and is in fact blinder: under it, a shape that travels cleanly while
accumulating `energy` reports as five hundred unrelated one-tick groups.

**REQ-19.5 — Matching.** A group at tick `t` and a group at tick `t + p`, for
`1 <= p <= STRUCTURE_MAX_PERIOD`, are the same recurrent structure when their signatures
are equal and the displacement between their corners is consistent across every repeat.
Displacement is measured on the wrapped grid and is the shortest of the wrapped
candidates.

**REQ-19.5.1** A match is reported only after `STRUCTURE_MIN_REPEATS` consistent repeats.
One coincidence is a coincidence.

**REQ-19.6 — Labels.** Exactly three, plus one annotation:

| Label | Condition | Recorded |
|---|---|---|
| `still` | `p == 1`, displacement `(0, 0)` | first tick, last tick, cell count |
| `repeater` | `p > 1`, displacement `(0, 0)` | period `p` |
| `traveler` | displacement `!= (0, 0)` | period `p`, displacement `(down, right)` |

**REQ-19.6.1 — The `drifting` annotation.** A matched structure whose signature recurs
but whose non-`kind` property values do **not** recur across the same period is marked
`drifting`, and the drifting property names are recorded. This is not a fourth label; a
structure is `still` *and* `drifting`, or `traveler` *and* `drifting`.

**REQ-19.6.2** The reason: this is the same distinction REQ-9.7 draws for a whole run,
drawn for one shape. A `drifting` structure is the local case of REQ-13.11 — the picture
repeats, the bookkeeping does not, and a change there could wake it up. It is also the
single most interesting thing this detector can find, because it is the category that
exists here and does not exist in a two-state automaton.

**REQ-19.7 — Naming.** The three labels above are the entire vocabulary. No LLM call
names structures in this uplift. Anything beyond `still`/`repeater`/`traveler` plus its
measured period and displacement is deferred to REQ-16.14.

**REQ-19.8 — Overlap.** A cell may belong to at most one reported structure per tick.
Where two matches claim the same cell, the longer-lived one wins; ties break toward the
smaller cell count. Discarded matches are dropped silently and not recorded.

**REQ-19.8.1** This is a reporting rule, not a claim about the world. Overlapping
recurrences are physically real; the UI just cannot usefully outline both. Revisit if
REQ-17.11 shows the discards are load-bearing.

---

## 6. Storage, transport, budget

**REQ-19.9 — Derived, cached, disposable.** Detection output is stored in a
`recurrent_structures` table that may be deleted and rebuilt at any time. It is **not**
covered by REQ-11.3, because it is not recorded history — it is a reading of recorded
history.

```sql
recurrent_structures(id, run_id, label,
                     first_tick, last_tick,
                     period, move_down, move_right,
                     cell_count, anchor_y, anchor_x,
                     kind_set_json,
                     signature_hash,
                     drifting, drifting_props_json,
                     cluster_id,
                     detector_version, assumed_background)
```

**REQ-19.9.1** `detector_version` is mandatory and follows the REQ-12.4.2 argument
exactly: two readings of the same immutable run under different detectors are different
readings. Rows whose `detector_version` does not match the running detector are
recomputed, not trusted.

**REQ-19.9.2** `anchor_y` / `anchor_x` are the structure's bounding-box corner at
`first_tick`, kept so the UI can jump to it without replaying the match.

**REQ-19.9.3** `assumed_background` records that no `BACKGROUND_KIND` was declared and
kind 0 was assumed empty under REQ-19.3.1.2. It exists so that a corpus query years from
now can separate declared facts from inherited prompt assumptions.

**REQ-19.9.4 — Table shape anticipates a general analysis layer.** This table is the
first of what will be several derived readings, and uplift 2.3 proposes splitting
uniform provenance (analyzer, version, parameters, status) from typed per-analyzer
results. Nothing here blocks that split; the columns above are the typed-result half of
it already.

**REQ-19.10 — API.**

| Method | Path | Purpose |
|---|---|---|
| GET | `/runs/{id}/structures` | Recurrent structures for a run. Computes and caches on first call. |

**REQ-19.10.1** The response includes `detector_version`, a `computed_at`, and the
`assumed_background` state. A client must not assume a run has no structures because the
list is empty; empty, not-yet-computed, partial, and filtered-out-by-size are
distinguishable in the response.

**REQ-19.11 — Budget and honesty on failure.** Detection is bounded by
`STRUCTURE_DETECT_BUDGET_SECONDS`. On overrun it stops, stores what it has, and marks the
result **partial**. The UI says so (REQ-13.14.1). A partial result is never presented as
a complete census.

**REQ-19.11.1** The reason: the failure mode of a silent budget cut is a user concluding
a rule produced two travelers when it produced forty. Wrong in a way that looks like a
finding.

---

## 7. Frontend — structure-aware inspection

**REQ-13.12 — Structure list.** The run view lists detected recurrent structures for the
current run: label, period, displacement, lifetime in ticks, cell count, the kinds
involved, and the `drifting` marker with its property names. The list is the discovery
path REQ-13.4 lacks.

**REQ-13.13 — Selecting a structure.** Selecting a list entry seeks playback to the
structure's `first_tick` and centers or highlights it. Selection is the intended way to
reach REQ-13.4 cell inspection; clicking a raw pixel remains supported and unchanged.

**REQ-13.14 — Overlay.** While paused, detected structures are outlined on the grid,
colored by label. The overlay is off by default during playback and toggleable.

**REQ-13.14.1 — The empty and partial cases must be legible.** Four distinct states —
*not yet computed*, *computed, nothing recurred*, *computed, partial (budget)*, and
*computed, groups discarded as too large* — are shown as four different messages. Where
the result relied on an assumed rather than declared background (REQ-19.3.1.2), the UI
says that too. Reuses the plainspoken register of the REQ-13.11 banner.

**REQ-13.14.2 — Interaction clusters.** Where two or more structures share an
interaction cluster (REQ-19.3.3), the overlay may connect them. This is what makes an
approach or a collision visible as an event rather than something the user must catch by
eye.

**REQ-13.15 — At-a-glance line.** The run view carries a one-line summary built from
structure counts — for example, "3 stills, 1 repeater (period 4), 1 traveler (period 4,
moving down-right), 1 drifting." This is the direct answer to complaint 3 in §0.6.

**REQ-13.15.1** The line is built from measured values only. It contains no adjective
about whether the run is interesting, and it names the detector's scope: it summarizes
recurrent structures, not structure.

---

## 8. Frontend — render modes

**REQ-13.16 — View-only, always.** Every mode below is display, governed by REQ-13.2.
None affects any fingerprint, the classifier, stopping, storage, or the coverage map.
All compose over the existing per-tick offscreen canvas; none introduces a second
renderer, and none requires WebGL (REQ-3.2 stands).

**REQ-13.17 — Activity field.** A cell lights where `kind` changed on this tick; an
alternate mapping sets brightness by ticks since that cell last changed. Derived from
reconstructed history (REQ-12.6), and available for any property, not only `kind`.

**REQ-13.17.1** Nearly free, since `changed_last_tick` is already reconstructed, and it
answers "where is computation happening" — a question the default view answers only by
implication.

**REQ-13.18 — Kind-stable, state-active.** A cell glows where `kind` held constant but
some other property changed. A grid that reads as completely frozen in the default view
lights up like a city in this one.

**REQ-13.18.1** This is the cell-level form of the `drifting` annotation (REQ-19.6.1) and
the continuous form of REQ-13.11's banner. It is the most direct visual expression the
system has of REQ-9.7's central distinction — pattern state versus computational state —
it needs no detector, and it costs a reconstruction pass. It is the highest
value-to-cost item in this document.

**REQ-13.19 — Trails.** Composites the last `TRAIL_WINDOW_TICKS` ticks into one frame
with decaying contribution, so one image carries recent history instead of one instant.

**REQ-13.19.1** The reason it is worth building: the run classifier's own vocabulary
(REQ-9.16) falls out of it visually. A settled run's trail collapses to a point, a
`repeats` run traces a closed figure, a `noisy` run smears everywhere. That is the
classification legible in one frame rather than five hundred.

**REQ-13.19.2** Trails must never be the default mode and must be labeled in the UI. A
trails frame is not a tick, and a user who does not know that is reading a smear as a
state.

**REQ-13.20 — Relief (optional).** Treats a chosen scalar property as a height field,
derives a surface normal from the local gradient, and shades it with a fixed light
direction. A shading pass over already-painted pixels; the underlying texel data is
untouched, in the same spirit as the existing circular-cell mask. It applies to one
scalar property at a time, chosen by the REQ-13.2 precedence.

**REQ-13.20.1** Marked optional deliberately. It makes gradients readable as ridges and
basins where a color ramp hides them, which is a real gain — but it is the most work for
the least research value in this document, and cutting it costs nothing else. The
legibility trick is borrowed from molecular surface rendering; **only** the trick is
borrowed, nothing here is three-dimensional, and the UI must not imply that it is.

**REQ-13.20.2 — Render mode is not persisted to the run.** Mode is UI state. It is never
written to `runs`, never given authority over what a run *is*, and never enters
generation context.

**REQ-13.20.3 — The existing player remains the default.** Grid, kind-to-color,
age-to-brightness, crossfade playback. Everything in §8 is an alternate view a user opts
into. A first-time visitor sees what they see today.

---

## 9. Testing

**REQ-15.1 applies unchanged:** every requirement below runs against fixtures only.

**REQ-15.9 — `life` finds a traveler.** Detection over a canonical `life` run reports at
least one `traveler` with period 4 and displacement of one cell on both axes.

**REQ-15.9.1 — Wrap, again.** A `life` traveler crossing the wrap boundary must be
reported as **one** structure with continuous `first_tick`/`last_tick`, not as one
ending at the edge and a second starting on the far side. This is REQ-14.2 restated for
the detector, and it is the single best proof REQ-19.5's wrapped-displacement handling is
correct.

**REQ-15.10 — `walker` finds exactly one traveler.** Period 1, displacement equal to its
heading step, lifetime equal to the run, and no other structure reported.

**REQ-15.11 — `majority` settles into stills.** After the run reaches `frozen`, every
reported structure is `still` and none is `repeater` or `traveler`.

**REQ-15.12 — `slow_burn` proves the annotation.** Before tick 60, `slow_burn`'s cells
report as `still` **and** `drifting`, with `memory` named as the drifting property. A run
where they report as `still` without the annotation is a REQ-19.6.1 regression, and is
the same class of blindness REQ-9.8.1 exists to prevent.

**REQ-15.12.1** The same fixture reads as entirely dark in the activity field
(REQ-13.17) and entirely lit in the kind-stable/state-active view (REQ-13.18) before tick
60, and swaps after. This is the cleanest executable test of REQ-9.7's distinction
anywhere in the system.

**REQ-15.13 — Determinism.** Detection run twice over the same stored run produces
byte-identical rows, ordering included. A detector whose output depends on iteration
order is a detector whose findings cannot be compared across runs.

**REQ-15.13.1 — Grouping does not depend on the declaration.** A fixture run under
identical conditions but declaring different `NEIGHBORS`/`REACH` values must produce
identical **groups** (REQ-19.3.2) and may produce different **interaction clusters**
(REQ-19.3.3). This is the executable form of the morphology/interaction split, and it is
the test that would have caught the v0.1 defect.

**REQ-15.13.2 — Background handling.** A fixture declaring no background kind must
produce per-kind groups (REQ-19.3.1) and must not silently exclude kind 0. A fixture
declaring a background must exclude exactly that kind and no other. A result produced
under the legacy assumption (REQ-19.3.1.2) must carry `assumed_background`.

---

## 10. Explicitly Not in This Uplift

Everything below is held in uplift **2.3**, which is a stash rather than a plan. Nothing
here is dismissed.

**REQ-16.12 — Perturbation and sensitivity maps.** Flipping a cell at tick 0, re-running,
and diffing to show what the outcome depended on. Genuinely valuable and genuinely
excluded here: **REQ-16.4 already excludes it** on the grounds that perturbation turns
history from a tick list into a version tree. 2.3 proposes narrowing REQ-16.4 around a
disposable `probe` concept; until that narrowing survives review, REQ-16.4 stands.

**REQ-16.13 — Non-grid layouts.** Scattering cells by two of their own properties, or
laying out the neighbor graph with a force-directed pass. **REQ-16.5 already excludes
non-grid layouts.** The property-space version is the more defensible of the two; the
graph-layout version costs wrap intuition — a traveler crossing the boundary becomes
illegible — which is a bad trade in a system where REQ-14.2 treats that exact behavior as
the correctness proof.

**REQ-16.14 — Generated structure names.** Asking an LLM to name detected shapes. Waits
on evidence that the mechanical labels are insufficient, and on REQ-19.7's constraint that
it may only name what the harness already confirmed.

**REQ-16.15 — Spacetime lenses and structure tracks.** `X × time` and `Y × time`
projections, and structure anchors plotted as trajectories. Cheap, high research value,
and squarely 2.3's opening section — held back only because it is a new lens family
rather than a fix to the one this document adds. Note that REQ-16.5's wording may need
narrowing before it lands; 2.3 owns that question.

**REQ-16.16 — Corpus-level views, studies, and the general analysis layer.** Multi-seed
studies, cross-run structure matching, intent-versus-outcome maps, and the generalized
analyzer schema. The corpus is not large enough for the corpus items to show anything but
noise; the schema items are 2.3's §20. A scale gate for some of it and a sequencing
decision for the rest, not a design objection to any of it.

---

## 11. Open Items

**REQ-17.9 — Whether structure counts should feed the classifier.** REQ-17.2 already
suspects `structured` detection needs something computed over the X×Y×T volume rather than
per-tick scalars, and observes that a traveler is a straight line in that volume while a
repeater is a corrugated pillar. This detector finds exactly those objects. The temptation
to wire it into REQ-9.16 row 7 is therefore strong and is deliberately resisted here: it
would change `guessed_behavior`, which changes Stage A context (REQ-8.3), which changes
what gets generated. Decide only with the accumulated user-override column (REQ-9.14) as
evidence, and record the classifier revision when it changes.

**REQ-17.10 — Every threshold in REQ-3.11 is a guess.** `STRUCTURE_MAX_CELLS = 64` in
particular is arbitrary. Re-derive from the first two hundred runs and record the
detector revision.

**REQ-17.11 — Whether `all_8` at reach 1 is the right universal grouping.** REQ-19.3.2
adopts the standard connected-component convention independent of the rule's declaration,
which fixes the reach-3 blowup but is still a choice. A `plus_4` rule may produce shapes a
human reads as two objects and all-8 grouping reads as one. Measure before deciding
whether grouping adjacency should follow `NEIGHBORS` at reach 1 while continuing to ignore
`REACH`.

**REQ-17.12 — Whether `drifting` is rare or universal.** If almost every structure drifts
in something, the annotation carries no information and needs a materiality threshold. If
almost none do, the detector may be matching too loosely. Both outcomes are informative
about REQ-19.4's kind-only choice and neither is predictable from here.

**REQ-17.13 — Detection cost at scale.** REQ-19.11's budget is a guess and the cost is
not linear in ticks: per-tick grouping is cheap, per-kind grouping (REQ-19.3.1) multiplies
it by `KINDS`, and cross-tick matching over `STRUCTURE_MAX_PERIOD` is worse than either.
Measure against the fixtures before assuming lazy computation on first request is fast
enough to sit in front of a page load.

**REQ-17.13.1** Related and unmeasured: how often the generator declares a background kind
once it can, how often it declares none, and whether the `none` rules are systematically
the ones detection goes quiet on.

---

## 12. Priority of Work

**REQ-19.20** Within this uplift, settle in this order. Each item constrains the ones
below it, and reordering means rewriting.

1. **Background declaration and grouping (§4).** What counts as a group, and what counts
   as nothing, decides everything downstream. This is where v0.1 was wrong and where a
   second mistake would be most expensive.
2. **The signature contract (REQ-19.4).** What counts as the same shape decides what the
   detector can see at all.
3. **Wrapped displacement (REQ-19.5, REQ-15.9.1).** Get it wrong and every traveler in
   the library is silently two structures.
4. **The `drifting` annotation (REQ-19.6.1).** It is the reason to prefer kind-only
   matching, so it ships with the matching, not after.
5. **Storage and `detector_version` (REQ-19.9).** Before any UI depends on cached rows.
6. **Kind-stable / state-active view (REQ-13.18).** Out of dependency order deliberately:
   it needs nothing above it, costs a reconstruction pass, and is the highest
   value-to-cost item here. Build it first if the detector stalls.
7. **Structure list and selection (REQ-13.12, REQ-13.13).** The actual fix for §0.6
   complaint 1.
8. **Activity field (REQ-13.17), then trails (REQ-13.19).** Independent of the detector
   and of each other.
9. **Interaction cluster overlay (REQ-13.14.2), then relief (REQ-13.20).** Both optional;
   either can be cut without touching anything else.

Items 1 through 5 are contract-shaped and should not be tightened once code exists. Items
6 through 9 can be revised freely.
