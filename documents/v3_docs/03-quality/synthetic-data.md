# Synthetic data

**Document class:** Level 3 — Requirements · **Status:** draft (first pass)
**Path:** `03-quality/synthetic-data.md`
**Identifier namespace:** `SYNTH-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §7, §10, §32, §38.6, §41–43; F-14, F-21 · `../01-core/labs.md` (LAB-5, LAB-6), `../01-core/worlds.md`, `../01-core/readers.md` · `testing.md` (TEST-), `accuracy.md` (ACCURACY-), `reference-cases.md` (REFCASE-) · DEC-3, DEC-21, DEC-22, DEC-23, DEC-24
**Source:** `DOC_GOOD_IDEAS.md` addenda (2026-08-21) and the nine family reports in `../labs/`

> **The suite generates universes, never observations.** Everything it produces is marked synthetic permanently and can never become a reference case. It tests whether the platform keeps its promises to itself — and it cannot, in principle, tell us whether the platform is any good at a real subject.

---

## 1. What varies across Labs, and what does not

The intuition that synthetic generation is mostly about Cell properties is **half right, and the wrong half is where the work is.**

Cell state is the *most compressible* axis. Seven feature archetypes recur across the whole sixty-Lab catalog under different vocabulary — **the store** (depletable supply), **the fuse** (accumulator plus threshold), **the one-way door** (irreversible state machine), **the cooldown** (recovery timer), **the tilt** (static bias), **the moving pile** (conserved transferable quantity), and **the ember** (hidden live state under a quiet surface). Sixty Labs' worth of Cell state collapses to compositions of those seven.

But counting what the family reports actually demanded, Cell state is not the bulk of it:

| Axis | Times demanded across the nine reports | Compressible? |
| :--- | :--- | :--- |
| External input drivers (wind, rainfall, warming, wave climate, load) | **22** | Into a handful of forcing shapes |
| Non-grid layout (network, identity, directed acyclic) | **13** | Into graph families with declared statistics |
| Moving participants carrying their own state | **12** | Partly |
| Connection state — direction, latency, capacity, in-flight | **6** | Yes |
| Observation channel — seen versus true, with delay | **5** | Yes |

**SYNTH-1.** The suite is **five orthogonal generators plus a degradation layer**, not one generator per Lab. A Lab's synthetic setup is a selection from the five, not a bespoke program.

That is the whole reason a single kit covers sixty Labs.

---

## 2. The five generators

**SYNTH-2 — Cell state.** Emits per-location bounded state as a **composition of feature archetypes**, parameterized (store capacity and depletion rate; fuse threshold and accumulation rate; door transition conditions; cooldown duration; tilt field; pile conservation law; ember visibility mask). The archetype composition is part of the recipe, not an implementation detail.

**SYNTH-3 — World structure.** Emits a Layout with declared properties: a grid at a stated resolution; a graph with a stated degree distribution, clustering, and community structure; an identity graph with stated delegation depth and nesting; a directed acyclic graph with stated fan-out and depth. **For relational Worlds the generated structure *is* the dataset** — there is no separate "data" to ingest into it, which is the point the ingestion note makes and which this generator has to honour.

**SYNTH-4 — Connection state.** Rides on SYNTH-3 and attaches declared direction, type, latency, capacity, and visibility. Bounded and readable under the same discipline as Cell state; a Connection must not become an object with hidden logic.

**SYNTH-5 — External input tapes.** Emits recorded forcing series with declared statistics — steady, seasonal, event-punctuated, heavy-tailed, or replayed from a stated shape. **No Cells involved.** This is the tape the World reads, and it is the single most-demanded generator in the catalog.

**SYNTH-6 — Observation channel.** Emits the mapping from World truth to what a participant or Reader can see: delay, dropout, aggregation, quantization, staleness. **This generator is what makes World/Seen/Recorded state testable at all**, and it is worth building early for the reason the reports give — ecology needs it before security does, and it is cheaper to get wrong on an evacuation Lab than on an intrusion Lab.

**SYNTH-7 — Degradation layer.** Operates on the *output* of any of the five and injects known pathologies: gaps, duplicates, malformed records, unit drift, the high-degree hub, timestamp disorder, silent truncation. Because the pathology was planted, **what should have been reported is known in advance.**

---

## 3. What the suite is for

Four jobs, in descending order of how much they are worth.

**SYNTH-8 — Recovery of a planted mechanism.** Plant a known mechanism, generate its data, ingest, run a Study, and ask whether the platform recovers what was planted. This is ground truth by construction, and it exercises the entire evidence chain on a subject where the answer is known before the run.

**SYNTH-9 — Ingestion honesty.** Run the degraded tier and assert that the collapse machinery told the truth about what it dropped, where the gaps were, and what it interpolated. **Real data can never test this**, because with real data nobody knows the ground truth of the loss. An interpolated value presented as observed is a fabrication, and this is the only place that can be caught deliberately rather than by luck.

**SYNTH-10 — Round-trip regeneration.** A synthetic dataset is a **recipe — generator version, parameters, seed — not an archive.** It is regenerated on demand and its identity is the recipe. Storing the bytes is permitted as a cache and is never the record.

**SYNTH-11 — Parametric drama.** Generators expose a control over how visible the phenomenon is, so a demonstration or a Reader test can be given a clean case, a marginal case, or an absent case on request. This is what makes the platform demonstrable before any real dataset exists — and every frame so produced is a real execution of an invented universe, not a depiction of anything.

---

## 4. Two circularity traps

The first is already stated in the source notes. The second is not, and I think it is the sharper one.

**SYNTH-12 — Never confirm a Lab against its own synthetic data.** A generator that is a cellular mechanism, feeding a platform that finds cellular mechanisms, is planting the answer. It will look exactly like successful confirmation and it proves nothing about any subject. Recovery tests are evidence about the **platform**; subject claims begin at real data.

**SYNTH-13 — At least one generator family must be out-of-vocabulary.** The archetype kit and the generator kit being the same artifact is the payoff *and* a hazard. If Cells are compositions of seven archetypes and generators are compositions of the same seven, then **every synthetic world is expressible in the platform's vocabulary by construction.** Recovery then demonstrates that the platform can recover things it can already express — a real fidelity result, and zero evidence that real subjects are expressible.

The suite therefore needs generators that are deliberately *not* archetype compositions: continuum fields sampled onto a lattice, globally-solved drivers, unbounded per-participant memory, semantic payloads that a scalar cannot carry. **Their job is to fail**, visibly and in a recorded way, and the failure boundary is the finding — the same discipline §30 applies to Labs, applied to the generator kit itself.

**SYNTH-14 — Include a null generator.** Data with the right marginal statistics and **no mechanism at all.** If a Study reports a recovered mechanism from null input, that is a false-positive rate, and the platform currently has no measurement of one. This is cheap, standard in other fields, and absent from the plan.

---

## 5. The claim ladder

**SYNTH-15.** Three claims, never sold as one another:

| Claim | Question | Reachable by synthetic? |
| :--- | :--- | :--- |
| **Fidelity** | Do components keep their promises to each other? | **Yes — the only rung it reaches** |
| **Confirmation** | Does output agree with a named real reference case, per regime? | No — real data only (`accuracy.md`) |
| **Efficacy** | Was the output worth having to a practitioner who acted differently? | No — real use, real recipients, time |

The consequence is uncomfortable and worth writing down: **the synthetic phase can produce a platform that is provably faithful and still worthless.** Fidelity testing feels productive because green checks accumulate, while the deciding risk sits untouched at rung three.

**SYNTH-16 — The synthetic phase has an exit criterion written in advance.** It ends when round-trip regeneration, recovery-of-planted, pathology-honesty, and the null false-positive rate are demonstrated. **Not one generator later.**

---

## 6. Provenance

**SYNTH-17.** Synthetic origin is recorded permanently and travels with every derived artifact — Runs, Reader outputs, Studies, reports, exported frames. It is never inferred from a filename or a directory.

**SYNTH-18.** A synthetic dataset never becomes a reference case (REFCASE-). The two are different kinds of thing and the boundary is one-way.

**SYNTH-19.** Any rendered output derived from synthetic input carries its substrate in the frame, not in adjacent prose — *rendered from live executions of synthetic worlds.* The line this protects is the one that cannot be crossed: **a synthetic frame must never imply a subject forecast.**

---

## 7. Build order

**SYNTH-20.** Fixtures (exist) → clean synthetic → degraded synthetic → real data. Within the clean tier, the order that maximizes what is learned per generator built:

1. **SYNTH-5 (tapes)** — most demanded, simplest, and unblocks the external-input driver class immediately.
2. **SYNTH-3 (world structure)** — unblocks every relational Lab, and for those Labs it *is* the dataset.
3. **SYNTH-2 (cell archetypes)** — the compressible part, and the one already half-specified.
4. **SYNTH-6 (observation channel)** — build before the security Labs need it, on a Lab where mistakes are pedagogical.
5. **SYNTH-14 (null)** — cheap, and the false-positive number is needed before any recovery claim means anything.
6. **SYNTH-7 (degradation)** — the second tier.
7. **SYNTH-4 (connection state)** — last; fewest Labs blocked on it.

**SYNTH-13's out-of-vocabulary generators are not a tier.** They are written alongside whichever generator they are meant to defeat.

---

## 8. A testable claim the suite makes possible

**SYNTH-21.** If archetype signature predicts behaviour family, then a generator built from *(store + fuse + one-way door)* should produce front-shaped behaviour **regardless of which Lab's vocabulary is painted on it** — and a Study should retrieve the same mechanism family across unrelated subjects. Fronts need the door; waves need the cooldown; cascades need the fuse; long-quiet surprises need the ember.

That is the cross-Lab retrieval hypothesis (DEC-12) made cheap to test, because the archetype composition is known in advance rather than inferred. If it fails, the archetype taxonomy is decoration.

---

## 9. Open questions

- **Who owns the generators?** They are neither Labs nor Platform Services cleanly, and shared ingestion machinery is already noted as the fifth member of DEC-5's translation family.
- **Are recipes mechanisms in disguise?** A sufficiently expressive generator is a Plugin with a different name. This sharpens DEC-23's third question and needs a bound.
- **Does SYNTH-13 have a stopping rule?** "Generators that should fail" is unbounded, and without a principle for which failures are worth building, it becomes busywork.
- **Does the null generator need a Lab?** A false-positive rate is per-Reader and per-Study-pattern, not global, and where that measurement lives is unsettled.
