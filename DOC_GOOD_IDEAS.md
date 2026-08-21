# Documentation ideas worth keeping

**Status:** working notes · **Date:** 2026-08-20
**Context:** brainstorm toward SCR 3.x documentation, prompted by the "What a Cell would carry" section of `documents/v3_docs/labs/short-lab-definitions/04-dune-and-ripple-lab.md`
**Cites:** SCR-F v0.2 §13.1, §25.3, §30, §41–43, §45.12; F-7, F-17

---

## The move that section makes

"What a Cell would carry" is where the brief stops describing sand and asks what the *domain forces the abstraction to hold* — and then lets the domain push back. Directional asymmetry is "a real requirement rather than a preference." The hop "stretches the definition of a local mechanism in an interesting and honest way." That's a Lab testing the platform instead of the platform absorbing the Lab, and it's the same instinct behind §30's "Labs should be allowed to fail these reviews."

---

## The load-bearing reframe

Both briefs independently arrived at the same sentence, in slightly different words:

> **Computational irreducibility is not a property of a domain. It is a property of a regime.**

That is the platform's whole value proposition, and it's currently nowhere in SCR-F. Stated plainly: **if a shortcut exists, SCR is worthless there.** Rothermel gives steady spread in homogeneous fuel; Bagnold gives transport rate; ripple wavelength has a linear-stability answer. In all of those SCR is laboriously rediscovering closed forms. SCR earns its keep only where the shortcut has broken — near percolation thresholds, in dune collisions, in path-dependent burnout ordering.

The dune brief calls the failure mode by name: **rediscovery, not discovery.** If SCR produces barchans, the honest reading is "the platform works," not "we learned about sand."

---

## What irreducibility means at each tentpole

| Component | The irreducibility angle |
|---|---|
| **Cell** | The §13.1 ceiling is an *irreducibility guarantee*, not just tidiness. Unbounded state lets you smuggle the answer into the cell — emergence you didn't actually compute. |
| **World** | Reducibility is partly a Layout property. Near a percolation threshold you must run it; far from it, mean-field works. A World should record where it sits relative to known critical points. |
| **Generation** | Should be biased *toward* the irreducible. A generator that keeps producing rules with closed-form behavior is burning money. |
| **Plugin** | Readability is the anti-shortcut guarantee — you can see whether it iterates or looks up an answer. A Plugin calling a closed-form solver is a shortcut wearing a mechanism's clothes. |
| **Reactor** | The only component permitted to know the outcome, and it only knows by having run. Determinism is what makes irreducibility *measurable* rather than confusable with noise. |
| **Run** | The receipt for work that could not be skipped. Ticks-to-outcome is an unused measurement of what the answer cost. |
| **Study** | **A Study is an admission of irreducibility.** If you could compute the answer you wouldn't run twenty starts. |
| **Reader** | A Reader is a *discovered pocket of reducibility* — a compression of a whole history into a fact. |
| **Corpus** | Not a shortcut around irreducibility — **amortization** of it. "We can't predict it, but we already ran it." |
| **Search** | What irreducibility forces you into. You can't derive the rule that branches, so you retrieve one that did. |
| **Visualization** | The eye is a Reader with no version number — and the one instrument that finds structure no analytic method does. Also the one that can *manufacture* apparent reducibility. |
| **Lab** | Owns the reducibility audit for its domain. Currently doing it by instinct in two briefs, mandated nowhere. |

---

## The five ideas I'd actually pursue

**1. The five properties that make it "cellular" — and which four 3.x is already negotiating away.**

A CA is: discrete cells · bounded local state · one uniform rule everywhere · simultaneous update · local interaction. Line them up against the registry:

- discrete cells, bounded state → §13.1, decided
- **uniform rule everywhere → DEC-1** (multiple Plugins = a non-uniform rule)
- **simultaneous update → DEC-3**
- **local interaction → not registered anywhere**

Four of five are in play and nobody has written that down. §45.12 asks reviewers to hunt over-generalization; this is the checklist that hunt needs. It also gives an honest answer to "when does SCR stop being ruliology and become a generic simulator" — when you've spent all five.

**2. The reach question is a missing DEC.**

The dune brief found it: a saltation hop is *non-local by design*. And then it noticed the shape generalizes — wildfire spotting, ecological dispersal, scanning worms. There's a spectrum: nearest neighbor → bounded reach → fixed-length hop → arbitrary graph edge → global broadcast. Somewhere on it, "local mechanism" stops meaning anything. That line is undrawn and consequential — it constrains the Plugin contract, every Layout family, and at least four Labs. Strongest DEC candidate I've seen so far.

**3. Readers as a catalog of discovered shortcuts.**

If a Reader reliably says "traveler, speed 2, period 4," it has found a pocket where the system *is* predictable. Where a Reader stops working is the boundary of that pocket — and that boundary is a **research finding**, not a QA note. This inverts how Reader coverage gets treated: "this Reader works on 60% of runs" currently reads as a weakness; it should read as a map.

**4. Studies as an empirical irreducibility instrument.**

The Small-Change Test is already a direct probe: flip one cell, watch whether divergence is bounded or total. §25.3's ambient sensitivity is the other half — and it's currently framed defensively, as deception-avoidance. It's better than that. **Uniform sensitivity across a sample of comparable changes is a measurement of the system's irreducibility**, producible cheaply, from evidence you already have. §25.3 even says "uniform sensitivity is itself the finding" — it just doesn't say what the finding *is*.

**5. The claim SCR should refuse to make.**

Wolfram's Principle of Computational Equivalence says most non-trivial systems are equivalently sophisticated. If SCR leans on that, it loses the ability to say some Labs fit better than others — everything's equally irreducible, so nothing is distinctive. SCR should take the **weaker, more defensible claim**: what predicts fit isn't computational class, it's whether *adjacency in the model corresponds to adjacency in the world*. The wildfire brief already states this as the selection rule. Making the refusal explicit costs nothing and inoculates the platform against its most tempting overreach.

---

## Where this lands as documentation

Three shapes, roughly in order of leverage:

- **A tenth §30 question — the reducibility audit.** §30 asks about domain fit, world fit, mechanism fit, time, evidence, accuracy, failure boundaries, comparison to tools, transfer limits. None asks *"where does this domain already have a formula?"* §30.8 is adjacent but not the same — the established tool might be another simulation. Two briefs invented this question independently; that's the signal it belongs in the platform. Amending §30 is an SCR-F amendment, so it's a DEC-shaped move, not an edit.
- **A Level 1 document on irreducibility and what "cellular" means** — idea 1 and idea 5, in `00-start-here/`. It's the missing intellectual spine: the tree currently explains what the components are and never explains why local mechanisms are the right instrument at all.
- **Two new DEC records** — the reach question, and possibly Reader-coverage-as-finding.

---

# Addendum (2026-08-21): data — ingestion, and synthetic first

## Ingestion, turned the right way around

"How do we generate cells from unstructured data" points backwards. **The Lab declares what a Cell is (fit question §30.2), before any data arrives; ingestion fits data into the declared schema.** Where the data won't fit, that is the fit review being tested empirically — the misfit is the finding, not an ingestion failure.

"Ingestion" is four pipelines with four existing homes:

1. **World structure** — for relational worlds, the data *is* the layout: an auth log is the connection graph. Grid worlds choose resolution; data supplies values.
2. **Starting State, via a recipe** — an ingestion procedure is a start recipe (DEC-23) whose input is a dataset instead of a seed. Same binding: recipe + realized values + source, all on the Run.
3. **External inputs** — recorded wind, tide tables, scheduled expiries: literally the tape WORLD-7 was written for. No cells involved.
4. **Reference cases** — most real data never enters the simulation at all; it is the comparison target (REFCASE-1). The accuracy story needs far less ingestion than it appears.

The real work is **the collapse, recorded**: the semantic ceiling makes ingestion lossy by design (the wildfire brief's one-moisture-scalar-for-four-classes case). Contract is provenance-shaped, same as GEN-16: source identity (hashed), the mapping including resolution, what was dropped, gaps and their handling. *An interpolated value presented as observed is a fabrication.*

Open: who owns shared ingestion machinery (it is the fifth member of DEC-5's translation family); recipes with enough power to be mechanisms in disguise (DEC-23 question 3, sharpened). The hunt list is already half-written — every Lab brief's §30.6 accuracy section names its datasets.

## Synthetic before wild

Order of operations: fixtures (exist) → clean synthetic → degraded synthetic → real data. Rationale from the owner: test user stories, use cases, integration resiliency, code dependencies, and rapid feature development before hunting.

**The killer property: ground truth by construction.** Plant a known mechanism → generate its data → ingest → Study → does the platform recover what was planted? Tests the whole evidence chain on a subject where the answer is known in advance — REFCASE-8's calibration purpose without waiting for real data. A synthetic dataset is (generator version, parameters, seed): a recipe, provenance-native, regenerable rather than archived.

**Tier 2 (degraded) tests ingestion honesty**, which real data never can: synthesize the known pathologies — gaps, the high-degree hub (WORLD-15), malformed records, duplicates, unit drift — and assert the collapse machinery told the truth about what it dropped and where the gaps were, because for once we know.

**Two rules, set early, non-negotiable:**

1. Synthetic is marked synthetic in provenance, permanently. It never drifts into looking like an observed reference case.
2. **Never confirm a Lab against its own synthetic data.** Generator-is-a-cellular-mechanism → SCR-finds-a-cellular-mechanism is planting the answer; it will look exactly like successful confirmation and it proves nothing about any subject. Recovery tests are evidence about the platform (ACCURACY-10 at maximum strength). Subject claims begin at real data, not before.

## Correction from the owner: synthetic tests fidelity, never efficacy

Three claims, never sold as one another:

- **Fidelity** — components keep their promises to each other: ingestion preserved what it claims, the chain recovers what was planted, pathologies are reported honestly. **The only rung synthetic can reach.** (testing.md's territory.)
- **Confirmation** — output agrees with a named real reference case, per regime. Real data only. (accuracy.md's territory.)
- **Efficacy** — the output was worth having: a practitioner took a candidate mechanism, validated it with their own tools, and acted differently. Real use, real recipients (DEC-20), and time. A reference-case match is still not efficacy.

Consequence: the synthetic phase can produce a platform that is provably faithful and still worthless — and fidelity testing feels productive (green checks accumulate) while the deciding risk sits untouched at rung three. **The synthetic phase gets an exit criterion written in advance**: it ends when round-trip, recovery-of-planted, and pathology-honesty are demonstrated — not one generator later.

---

# Addendum (2026-08-21): archetypes, and the visualization arsenal

## Cell feature archetypes — the cross-Lab discovery question, and the synthetic kit, are one artifact

Seven archetypes recur across the catalog wearing different names: **the store** (depletable supply: fuel, susceptible pool, sand), **the fuse** (accumulator + threshold: heat-to-ignition, exposure-to-infection, saturation-to-failure), **the one-way door** (irreversible state machine: burnt, infected, compromised), **the cooldown** (recovery timer: immunity, regrowth, patched), **the tilt** (static bias: slope, wind, topology weights), **the moving pile** (conserved transferable quantity: sand, water, load — conservation is a checkable fidelity assertion inside the semantics), **the ember** (hidden live state under a quiet surface: smoldering peat, incubation, dormant persistence — §38.6 as an archetype, the platform's signature).

Payoffs: synthetic generators become archetype compositions (one kit, cross-Lab coverage, parametric drama); the §21 neutral-Reader list maps onto archetypes ~1:1 (front-speed ↔ one-way door, loading-detection ↔ fuse, conservation-check ↔ moving pile) — now we know why that list is what it is; a testable corpus-scale claim — do Labs sharing an archetype signature produce overlapping behavior families? (fronts need the door, waves need the cooldown, cascades need the fuse, long-quiet surprises need the ember); and a candidate DEC-24 floor statement: every Cell is a composition of a small set of bounded feature archetypes.

## The visualization arsenal (all pass VIS-8: rendered later from stored evidence; together they define what DEC-13 makes storage keep)

1. **Time-solid** — a whole Run as one rotatable object, time as an axis; travelers become diagonal crystal threads. A shelf of them is a library of universes.
2. **Recurrence crystal** — periodicity as geometry: the sculpture goes crystalline exactly where prediction becomes possible. The reducibility audit, visible.
3. **Butterfly cone with ghosts** — one flip's divergence cone among twenty translucent comparables; §25.3's ambient honesty makes the shot stronger, not weaker.
4. **Invention feed** — proposal → code → gauntlet → first bloom. The loop is the product; this is the five-second answer (three seconds of feed, then collapse to time-solid, rack onto the shelf).
5. **Ember x-ray** — split screen: quiet surface, charging fuses beneath. Partly built already (2.x kind_stable is the seed). The security pitch in one frame.
6. **Library galaxy** — every mechanism as a star by named similarity; failures kept, as dark matter.
7. **Behavior terrain** — Try Many Settings as landscape; cliffs are phase transitions; every point an actual experiment.
8. **Sensitivity cable** — a Study's runs as braided threads; the one that leaves the braid is the finding.

## Pitch legitimacy

A Run of a synthetic world is a real Run — the demo shows true executions of invented universes. Label the substrate ("rendered from live executions of synthetic worlds") and the deck is not merely compliant, it is **auditable**: technical DD can scrub the evidence behind every frame. The one uncrossable line: a synthetic shot never implies a domain forecast. Show universes, not fire predictions.

---

# Addendum (2026-08-21): riff on the visual idioms survey; the 3D selection

**Survey:** `documents/v3_docs/surveys/scr-visual-idioms-survey-v0.1.md`. Its §7 is right; four extensions:

1. **AOV channels answer DEC-13.** Per-step channels (kind, properties, changed-mask, plus derived channels) ARE the evidence format the advanced views need — 2.x already half-does this (stores kind/age, reconstructs changed). Our cryptomatte improves on film's: structure identity is a Reader-written **derived-evidence channel, versioned and recomputable** (the recurrent-structure detector, REQ-19.x, is its writer). Channel storage is the one decision Tier B/C both stand on — write it down first.
2. **One master object.** Time-solid (world × time) is the master; kymograph = a line-slice of it; Run barcode = total collapse (library page, nearly free); the existing 2D player = a **section plane** through it — scrubbing is sectioning, the slider is the plane. Building the solid generalizes the player rather than adding a feature beside it.
3. **The survey's missing idiom is drawable, by us alone: the said-vs-did chart.** DEC-12 keeps intent-similarity and observed-similarity separate, so plot each mechanism at (intent-sim, behaviour-sim) vs a reference: the diagonal did-what-it-said, the off-diagonal quadrants are §3's gap as *positions*. Nobody else records intent as an artifact, so nobody else can draw it.
4. **Select 3D by one rule: the third axis must be data, never decoration.** Three honest uses: time-as-axis (the solid family: cones, ghosts, crystal, section playback); genuinely 3D worlds (peat depth — the ember lives underground; karst; convection); derived landscapes (height = Reader measurement). Refusals, permanent: 3D node-link graphs (security iterated to 2D for a reason), spinning globes, cameras implying depth that isn't data.

**Build ladder:** A (days, 2D): barcode, onion-skin in player (trails half-is this), wedge grid, kymograph slice. B (the one 3D investment): time-solid + section scrubbing + ghost cones + recurrence crystal — one renderer, four shots, includes the five-second pitch. C (data-gated): terrain, said-vs-did, galaxy, ember volume.
