# Autonomous Semantic Ruliology
## Frontend Visualization Uplift — 2.2

**Status:** draft. Not cleared for implementation. Sections 4 and 5 are specified to
contract depth; Sections 6 and 7 are specified to intent depth and need a calibration
pass before code.
**Targets:** Omnibus Requirements **v3**. Read that document first; this one assumes it
and does not restate it.
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
be issued to anything else, including a v4 revision written independently of it:

| Block | Belongs to |
|---|---|
| REQ-13.12 – REQ-13.20 | §13 Frontend |
| REQ-15.9 – REQ-15.13 | §15 Testing |
| REQ-16.12 – REQ-16.16 | §16 Explicitly Not in v1 |
| REQ-17.9 – REQ-17.13 | §17 Open Items |
| REQ-19.1 – REQ-19.20 | §19 Structure Detection — **new section** |

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

---

## 1. Concept

A structure is a group of cells that comes back. Nothing more is assumed and nothing
about Life's named menagerie is hardcoded. The harness does not need to know what a
glider is; it needs to notice that a small clump of cells returned to its own shape
somewhere else, and then say so.

**REQ-19.1** Structure detection is **observation, not classification.** It reports what
recurred. It does not decide whether a run is interesting, does not set
`guessed_behavior`, and does not enter the coverage map. Those are separate questions
with their own requirements and their own blast radius.

**REQ-19.1.1** The reason: `guessed_behavior` feeds Stage A context (REQ-8.3), so any
change to how it is computed silently reweights what the generator explores. A detector
calibrated against nothing must not be given that lever on its first day. See REQ-17.9.

---

## 2. Decisions and Rationale

| Decision | Why |
|---|---|
| **Detection matches on `kind` only** (REQ-19.4) | This is REQ-9.7's pattern/computational split applied one level down. A shape that recurs in `kind` while its `energy` climbs is a real phenomenon Life has no word for; matching on every property would render it invisible by calling it "not a structure." |
| **Property drift is an annotation, not a disqualifier** (REQ-19.5) | Same reason, stated positively. The drifting case is the one this system can find and Wolfram's numbering cannot. |
| **Adjacency for grouping is the rule's own declared neighborhood** (REQ-19.3) | Two cells belong to the same structure if one can influence the other. Any other choice imports an assumption the rule never made. |
| **Detection is post-hoc over stored history** (REQ-19.2) | Mirrors REQ-9.1. Runs already complete before playback; there is no reason to make the hot loop carry this. |
| **Detection output is a cache, not history** (REQ-19.9) | It is derived from immutable ticks and is fully recomputable. Treating it as history would put it under REQ-11.3 and make detector improvements impossible. |
| **New render modes are view-only** (REQ-13.16) | REQ-13.2 already establishes that display never touches a fingerprint. Trails and relief are display. |
| **No WebGL** (REQ-3.2, REQ-16.10 unchanged) | Both new render modes are compositor and shading passes over the existing one-texel-per-cell canvas. Neither needs a GPU target, and reaching for one would drag in the whole REQ-16.10 argument for no gain. |
| **Structure names are mechanical, not generated** (REQ-19.7) | An LLM asked to name shapes will name shapes, including the ones that are not there. |

---

## 3. Configuration additions

**REQ-3.11** Added to the §3.9 table:

| Variable | Default | Affects |
|---|---|---|
| `STRUCTURE_MIN_CELLS` | 2 | Smallest group that can be called a structure. |
| `STRUCTURE_MAX_CELLS` | 64 | Largest. Above this the group is terrain, not a structure. |
| `STRUCTURE_MAX_PERIOD` | 32 | Longest recurrence period searched. |
| `STRUCTURE_MIN_REPEATS` | 2 | Times a signature must recur before it is reported. |
| `STRUCTURE_DETECT_BUDGET_SECONDS` | 10.0 | Wall clock for one run's detection pass. |
| `TRAIL_WINDOW_TICKS` | 40 | Ticks composited into one trails frame. |

**REQ-3.11.1** All six are first guesses calibrated against nothing. REQ-17.10 owns
re-deriving them.

---

## 4. Structure Detection — the algorithm

**REQ-19.2 — When it runs.** Detection runs over a completed, stored run, lazily on
first request, and the result is cached (REQ-19.9). It never runs during generation and
never during playback. Generation stays synchronous (REQ-3.6) and is not slowed by this.

**REQ-19.3 — Grouping.** For each tick, group all cells with `kind != 0` into connected
groups, where two cells are connected if one lies within the other's declared
neighborhood (`NEIGHBORS`, `REACH`). Grouping wraps at every edge, per REQ-3.5.

**REQ-19.3.1** Groups outside `[STRUCTURE_MIN_CELLS, STRUCTURE_MAX_CELLS]` are dropped
before matching. A group spanning most of the grid is the background, and matching it
against itself produces a true but useless answer.

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
`1 <= p <= STRUCTURE_MAX_PERIOD`, are the same structure when their signatures are equal
and the displacement between their corners is consistent across every repeat. Displacement
is measured on the wrapped grid and is the shortest of the wrapped candidates.

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

## 5. Structure Detection — storage, transport, budget

**REQ-19.9 — Derived, cached, disposable.** Detection output is stored in a
`structures` table that may be deleted and rebuilt at any time. It is **not** covered by
REQ-11.3, because it is not recorded history — it is a reading of recorded history.

```sql
structures(id, run_id, label,
           first_tick, last_tick,
           period, move_down, move_right,
           cell_count, anchor_y, anchor_x,
           signature_hash,
           drifting, drifting_props_json,
           detector_version)
```

**REQ-19.9.1** `detector_version` is mandatory and follows the REQ-12.4.2 argument
exactly: two readings of the same immutable run under different detectors are different
readings. Rows whose `detector_version` does not match the running detector are
recomputed, not trusted.

**REQ-19.9.2** `anchor_y` / `anchor_x` are the structure's bounding-box corner at
`first_tick`, kept so the UI can jump to it without replaying the match.

**REQ-19.10 — API.**

| Method | Path | Purpose |
|---|---|---|
| GET | `/runs/{id}/structures` | All detected structures for a run. Computes and caches on first call. |

**REQ-19.10.1** The response includes `detector_version` and a `computed_at`. A client
must not assume a run has no structures because the list is empty; empty and
not-yet-computed are distinguishable in the response.

**REQ-19.11 — Budget and honesty on failure.** Detection is bounded by
`STRUCTURE_DETECT_BUDGET_SECONDS`. On overrun it stops, stores what it has, and marks the
result **partial**. The UI says so (REQ-13.14.1). A partial result is never presented as
a complete census.

**REQ-19.11.1** The reason: the failure mode of a silent budget cut is a user concluding
a rule produced two travelers when it produced forty. Wrong in a way that looks like a
finding.

---

## 6. Frontend — structure-aware inspection

**REQ-13.12 — Structure list.** The run view lists detected structures for the current
run: label, period, displacement, lifetime in ticks, cell count, and the `drifting`
marker with its property names. The list is the discovery path REQ-13.4 lacks.

**REQ-13.13 — Selecting a structure.** Selecting a list entry seeks playback to the
structure's `first_tick` and centers or highlights it. Selection is the intended way to
reach REQ-13.4 cell inspection; clicking a raw pixel remains supported and unchanged.

**REQ-13.14 — Overlay.** While paused, detected structures are outlined on the grid,
colored by label. The overlay is off by default during playback and toggleable.

**REQ-13.14.1** Where detection returned a partial result (REQ-19.11), the run view says
the census is incomplete and why. Reuses the plainspoken register of the REQ-13.11
banner.

**REQ-13.15 — At-a-glance line.** The run view carries a one-line summary built from
structure counts — for example, "3 stills, 1 repeater (period 4), 1 traveler (period 4,
moving down-right), 1 drifting." This is the direct answer to complaint 3 in §0.6.

**REQ-13.15.1** The line is built from measured values only. It contains no adjective
about whether the run is interesting.

---

## 7. Frontend — two new render modes

**REQ-13.16 — View-only, always.** Both modes below are display, governed by REQ-13.2.
Neither affects any fingerprint, the classifier, stopping, storage, or the coverage map.
Both compose over the existing per-tick offscreen canvas; neither introduces a second
renderer, and neither requires WebGL (REQ-3.2 stands).

**REQ-13.17 — Trails.** Composites the last `TRAIL_WINDOW_TICKS` ticks into one frame
with decaying contribution, so one image carries recent history instead of one instant.

**REQ-13.17.1** The reason it is worth building: the run classifier's own vocabulary
(REQ-9.16) falls out of it visually. A settled run's trail collapses to a point, a
`repeats` run traces a closed figure, a `noisy` run smears everywhere. That is the
classification legible in one frame rather than five hundred.

**REQ-13.17.2** Trails must never be the default mode and must be labeled in the UI. A
trails frame is not a tick, and a user who does not know that is reading a smear as a
state.

**REQ-13.18 — Relief.** Treats a chosen scalar property as a height field, derives a
surface normal from the local gradient, and shades it with a fixed light direction. A
shading pass over already-painted pixels; the underlying texel data is untouched, in the
same spirit as the existing circular-cell mask.

**REQ-13.18.1** The reason: gradients in a property are close to unreadable on a color
ramp and immediately readable as ridges and basins. This is the legibility trick borrowed
from molecular surface rendering, and it is worth being clear that only the trick is
borrowed — nothing here is three-dimensional and the UI must not imply that it is.

**REQ-13.18.2** Relief applies to one scalar property at a time, chosen by the same
precedence as REQ-13.2: user override, then `SUGGESTED_DISPLAY`, then default.

**REQ-13.19 — Mode is not persisted to the run.** Render mode is UI state. It is never
written to `runs`, never included in a share link's authority over what a run *is*, and
never enters generation context.

**REQ-13.20 — The existing player remains the default.** Grid, kind-to-color,
age-to-brightness, crossfade playback. Everything in §7 is an alternate view a user opts
into. A first-time visitor sees what they see today.

---

## 8. Testing

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

**REQ-15.13 — Determinism.** Detection run twice over the same stored run produces
byte-identical rows, ordering included. A detector whose output depends on iteration
order is a detector whose findings cannot be compared across runs.

---

## 9. Explicitly Not in This Uplift

**REQ-16.12 — Perturbation and sensitivity maps.** Flipping a cell at tick 0, re-running,
and diffing to show what the outcome depended on. Genuinely valuable and genuinely
excluded: **REQ-16.4 already excludes it** on the grounds that perturbation turns history
from a tick list into a version tree. A harness-driven probe is not user grid editing and
the exclusion is arguably narrower than it reads — but the version-tree problem is
identical either way, and every probe would land in a library whose stated premise is that
everything in it is permanent (REQ-1.4). Revisit only with a `probe` concept that is
explicitly cheaper and more disposable than a run. Do not build it under the current
storage contract.

**REQ-16.13 — Non-grid layouts.** Scattering cells by two of their own properties
(`weight` against `stubbornness`, `heading` against `age`) instead of by position, or
laying out the neighbor graph with a force-directed pass. **REQ-16.5 already excludes
non-grid layouts.** The property-space version is the more defensible of the two and
should be the one reconsidered first; the graph-layout version costs wrap intuition —
a traveler crossing the boundary becomes illegible — which is a bad trade in a system
where REQ-14.2 treats that exact behavior as the correctness proof.

**REQ-16.14 — Generated structure names.** Asking an LLM to name detected shapes. Waits
on evidence that the mechanical labels are insufficient, and on REQ-19.7's constraint that
it may only name what the harness already confirmed.

**REQ-16.15 — Sonification of the computational layer.** Mapping per-tick change in
`weight`, `stubbornness`, scheduler phase, and RNG advance to an ambient signal, so a
frozen-looking grid audibly hums while its hidden state moves. This is the continuous
version of the REQ-13.11 banner and it is a good idea. It is out of scope here because it
is a whole new output medium with its own accessibility, autoplay, and calibration
surface, and none of that belongs in the same pass as a shading mode. Deferred, not
dismissed.

**REQ-16.16 — Corpus-level views.** Intent-versus-outcome matrices, per-concept structure
yields, generator calibration curves. The corpus is not large enough for any of it to show
anything but noise. This is a scale gate, not a design objection: it unblocks on volume,
and REQ-8.4's 300-rule threshold is the nearest existing marker of when to look again.

---

## 10. Open Items

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

**REQ-17.11 — Grouping blows up at high `REACH`.** Under `all_8` with `REACH = 3`, a cell
influences a 7×7 window, so REQ-19.3's adjacency merges nearly everything into one group
and `STRUCTURE_MAX_CELLS` throws it away. The likely outcome is that high-reach rules
report zero structures for a bad reason. Measure before deciding between a reach-dependent
size ceiling, a second adjacency at reach 1 for grouping only, or accepting the gap and
saying so in the UI.

**REQ-17.12 — Whether `drifting` is rare or universal.** If almost every structure drifts
in something, the annotation carries no information and needs a materiality threshold. If
almost none do, the detector may be matching too loosely. Both outcomes are informative
about REQ-19.4's kind-only choice and neither is predictable from here.

**REQ-17.13 — Detection cost at scale.** REQ-19.11's budget is a guess and the cost is
not linear in ticks: per-tick grouping is cheap, cross-tick matching over
`STRUCTURE_MAX_PERIOD` is not. Measure against the fixtures before assuming lazy
computation on first request is fast enough to sit in front of a page load.

---

## 11. Priority of Work

**REQ-19.20** Within this uplift, settle in this order. Each item constrains the ones
below it, and reordering means rewriting:

1. **The signature contract (§4, REQ-19.4).** What counts as the same shape decides what
   the detector can see at all. Everything else is downstream.
2. **Wrapped displacement (REQ-19.5, REQ-15.9.1).** Get it wrong and every traveler in
   the library is silently two structures.
3. **The `drifting` annotation (REQ-19.6.1).** It is the reason to prefer kind-only
   matching, so it ships with the matching, not after.
4. **Storage and `detector_version` (REQ-19.9).** Before any UI depends on cached rows.
5. **Structure list and selection (REQ-13.12, REQ-13.13).** The actual fix for §0.6
   complaint 1.
6. **Trails (REQ-13.17), then relief (REQ-13.18).** Independent of everything above and
   of each other; either can be cut without touching the detector.

Items 1 through 4 are contract-shaped and should not be tightened once code exists.
Items 5 and 6 can be revised freely.
