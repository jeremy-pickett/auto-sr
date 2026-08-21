# Proposals from the sixty-Lab catalog

**Document class:** Level 2 — Architecture Decisions (proposal index) · **Status:** draft
**Path:** `04-decisions/proposed-from-the-lab-catalog.md`
**Source:** the nine family reports in `../labs/*/family-*-report-v1.md`, covering catalog entries 1–60
**Cites:** SCR-F v0.2 §36.2, §36.3, §36.5, §36.6, §40; F-22 · `../01-core/labs.md` LAB-5, LAB-16 · DEC-1 to DEC-24

> **This document mints nothing.** It does not assign DEC identifiers, does not decide anything, and does not amend SCR-F. Identifiers are permanent and adoption is a human act (§36.3). What follows is a triage, so that assigning them becomes mechanical rather than a fresh act of judgement.

---

## Why this exists

Writing the sixty Lab papers surfaced **44 platform questions** that no decision record owns. They were recorded family by family, in nine separately-written documents, and the predictable happened:

> **The same requirement was invented independently under different names in different families.**

That is precisely the drift §36 exists to prevent — a model-written tree drifting at the root, one plausibly-interpreted ambiguity at a time — and the sixty-Lab exercise produced a clean instance of it in its own output. The reports are individually consistent and collectively duplicated.

Deduplicated, the 44 rows are **19 distinct requirements**. They fall into three buckets, and most are not new decisions at all.

---

## §1. Naming normalization

These pairs and triples are the same requirement under different names. **The family reports should be normalized to the canonical name** so retrieval across them works.

| Canonical name | Recorded in the reports as | Families |
| :--- | :--- | :--- |
| **Globally-computed drivers** | "Globally-computed drivers"; "Global-driver dependency declared in fit review" | E, G |
| **World / Seen / Recorded state** | "Observation model — true / observable / recorded"; "Belief and seen-state as a core World capability"; "Seen State versus World State" | C, F, H |
| **Mechanism analysis as a mode** | "Mechanism discovery vs mechanism analysis as two modes"; "Mechanism analysis as a distinct mode" | F, G |
| **Mechanism identity layers** | "Mechanism-similarity vocabulary"; "Mechanism-family language, not identity"; "Observable-equivalence identity" | D, E |
| **Lattice-artifact control Study** | "Anisotropy control Study"; "Orientation-control Study" | D, E, F |
| **Connection model** | "Multiple Connection classes in one World"; "Connection state as first-class and bounded"; "Dynamic connection strength vs existence" | A, G |
| **Dynamic Connections** | "Dynamic Connections"; "Topology classes — fixed / state-weighted / constructed" | A, C, H, I |
| **Evidence standing metadata** | "Validation standing as a searchable property"; "Correctness levels recorded in standing"; "Evidence external-validity metadata" | A, D, H |
| **Output risk policy** | "Lab credibility class"; "Provenance inside high-risk Views"; "Socially portable output as a hazard class" | D, H, I |
| **Named geometry families** | "Geometry families"; "Surface topology independent of display coordinates" | A, B, D |

---

## §2. Bucket A — candidates for new decision records

Seven questions that are genuinely open, genuinely consequential, and not owned by DEC-1 through DEC-24. Plain questions are drafted in the registry's house style. **Numbers are deliberately omitted.**

### A1. What may a mechanism depend on that it cannot compute for itself?

*Formal name:* **Globally-computed drivers.** *Raised by:* entries 31 (decisive), 42, 43, 9, 18, 28, 34, 5 — **the most recurrent unregistered question in the catalog.**

Three cases must be separated, and the third is the boundary:

| Case | Verdict |
| :--- | :--- |
| **Local driver** — the mechanism computes what it needs from bounded nearby state | The platform's ideal |
| **Generic global property** — the Reactor computes a subject-neutral quantity: connected components, shortest path, a conserved total, graph degree | May fit, if the helper is generic and fully declared |
| **Subject-defining global solve** — a specialized solve *is* the driver: elasticity, electrochemical potential, hydraulic pressure, power flow | **The mechanism becomes ceremonial** |

The proposed rule, already applied in three family reports: *a Lab fails mechanism fit if the subject-defining causal step must be supplied by a specialized global solver and the local mechanism merely consumes its answer.* That does not forbid interoperating with such solvers; it forbids selling the result as discovery of a local mechanism.

**Relation to existing records:** adjacent to DEC-7 (what a rule is allowed to do), which governs the mechanism's *surface*. This governs what the surface is allowed to *read from outside itself*. Neither subsumes the other.

### A2. Does a participant act on what is true, or on what it has been told?

*Formal name:* **World, Seen, and Recorded state.** *Raised by:* entries 40 (where it is the phenomenon), 14, 16, 47, 52, 55, 2, 22, 46.

Four states, and the reports argue this is execution semantics rather than an interface concern:

- **World truth** — what is actually the case;
- **Participant belief** — what this participant currently holds;
- **Observation channel** — what it is able to receive, and when;
- **Recorded evidence** — what the Reactor knows and stores.

**The strongest argument for registering it is that ecology raised it before security did.** Invasion Ecology distinguishes *established* from *detected*; Pest Outbreak distinguishes a living population from visible mortality a year later. Limited and delayed observation is therefore **general, not adversarial**, and should not be built as a security feature.

**Relation to existing records:** DEC-3 owns *when* things happen; this owns *who knows what*. SCR-F §18.5 already places observation staleness with the World and Reactor, so placement is arguably settled and the mechanics are not.

**Sequencing note carried from the reports:** entry 40 is the cheap, low-stakes place to build this — a sympathetic domain where architectural mistakes are pedagogical. Family H is where they would be consequential. **Build it before Family H, not after.**

### A3. May a mechanism create or destroy relations?

*Formal name:* **Dynamic Connections.** *Raised by:* entries 48 (where it *is* the mechanism under study), 56, 18, 50, 58, 6, 41.

Three topology classes now need separating, and the reports treat conflating them as an error:

| Class | Meaning | Example |
| :--- | :--- | :--- |
| **Fixed** | Connections exist for the whole Run | A lattice; an inherited fracture network |
| **State-weighted** | Connections exist; strength or direction changes with state | Flow routing in a braided river |
| **Constructed** | Connections are created or destroyed by the mechanism | Mycelial cords; delegation grants; dependency edges |

The control rule proposed throughout is the platform's existing law with a new effect type: **the mechanism proposes a Connection change; the Reactor validates and applies it** under declared allowed relation classes, endpoint type restrictions, budgets, duplicate-relation rules, reversibility, and complete history — including whether topology counts as future-relevant state.

**Why now:** the reports describe this as having moved from speculative ornament to likely requirement, because the platform's strongest relational Labs need it. Entry 48 is the flagship decision case — **if SCR cannot express this safely, that Lab does not fit**; entry 58 is the cheapest test.

### A4. Is a relation a thing with state, or just a permission to interact?

*Formal name:* **The Connection model.** *Raised by:* entries 45, 46, 41, 6, 47.

Connections in several Labs are no longer bare adjacency. They may need declared direction, type, latency, capacity, visibility, current state, permission semantics, and possibly bounded in-flight payload. And one World may need **several Connection classes at once** — entry 41 wants spatial adjacency *and* road connectivity *and* jurisdiction membership, and entry 47 wants network reachability *and* identity trust.

The proposed answer is deliberately cheap: **not a HybridWorld abstraction, but a World declaring more than one Connection class, with a mechanism declaring which it reads.** Treat Grid, Network, Identity, and Agent as common *patterns* rather than mutually exclusive boxes.

The matching discipline: **Connection state should be first-class and bounded exactly as Cell state is.** A Connection must not become an object with unlimited hidden logic.

**Relation to existing records:** overlaps DEC-8 (one filing system for two shapes of world) substantially. **This may be DEC-8's answer rather than a separate record** — a judgement for whoever owns DEC-8.

### A5. Does some state belong to the traveller rather than the place?

*Formal name:* **Moving participants.** *Raised by:* entries 59 (the proposed acceptance case), 36, 37, 38, 39, 40, 17, 26, 24, 47.

Location state and participant state are consistently different — a floor cell versus a pedestrian, a road cell versus a vehicle, a floor cell versus a robot with a task and a battery, a substrate patch versus a grazer. Destination, speed, group, cargo, task, memory, and belief travel with the participant, and a fixed cell is not their natural owner.

The proposed construct is narrower than a full Agent ontology:

> **Mover** — a bounded state-bearing participant occupying a World location and changing location through Reactor-controlled transitions.

with the original Cell concept preserved: **Cells are locations and state-bearing substrate; Participants are bounded mobile state records; Connections and Layout are permitted relations and movement; mechanisms propose; the Reactor decides.**

**Relation to existing records:** overlaps DEC-22 (must every participant be the same kind of thing) and spends against DEC-24. It may be DEC-22's answer.

**Acceptance case, and the reports are emphatic:** *do not justify this capability with a high-stakes Lab first.* Entry 59 is tiny, low-stakes, measurable, analytically characterized, and has a known right answer.

### A6. What is the model allowed to know when we are testing the platform?

*Formal name:* **Blinded benchmark modes.** *Raised by:* entries 30, 35, 37, 4, 6, 10, 20.

Several canonical mechanisms in this catalog are almost certainly in foundation-model training data — Potts grain growth, DLA and Eden, classical dendrites, the ZGB surface-reaction model, Nagel–Schreckenberg, Werner dunes, Murray–Paola braiding. **If SCR "discovers" them, did the platform infer the mechanism from evidence, or did the model remember the literature?**

A benchmark Study should record what Generation received: subject name, known mechanism names, canonical citations, target behaviour only, abstracted measurements, or deliberately disguised vocabulary. The strong test:

> **Can Generation recover a known mechanism family from behaviour descriptors when the subject name and canonical vocabulary are withheld?**

Without this, calibration measures literature recall and reports it as mechanism supply.

**Relation to existing records:** adjacent to DEC-17 (what changes when we change the AI). This is narrower and sharper: not provider neutrality but **benchmark integrity.**

### A7. What may leave the building, and with what attached?

*Formal name:* **Output risk policy.** *Raised by:* Family D throughout, entries 52, 55, 57, 36, 42, 1, 8, 5.

A non-claims paragraph is insufficient where the subject itself carries weight. A rendered arrhythmia, tumour, migraine wave, fire front, shoreline retreat, epidemic wave, or luminous path to Domain Admin **is not neutral** — readers infer significance from the subject regardless of caption, and all of them crop beautifully.

Three hazard classes were used across the reports: *mistakable for an operational forecast*; *mistakable for scientific significance it does not have*; *low hazard*. Entry 57 adds a fourth that is different in kind — **socially portable output**, which escapes not by a practitioner over-reading but by circulating without its caption into policy argument.

The proposed policy surface governs mandatory labelling, export and report language, whether patient-specific or customer-specific inputs are accepted, whether real units are displayed, whether output may appear without Study context, and whether a Study may use words such as *treatment*, *response*, *risk*, or *prediction*. For high-risk Views, provenance should be **inside the rendered evidence**, not adjacent prose.

**Relation to existing records:** DEC-14 covers video provenance and DEC-20 covers handing results to domain experts. This is broader than either and would likely constrain both.

---

## §3. Bucket B — already owned; normalize the reports instead

Six recorded items are within an existing record's scope. **No new record is needed; the family reports should cite the owner.**

| Recorded as | Owner | Note |
| :--- | :--- | :--- |
| Catalog governance — merge, demote, benchmark-only, rejected | **DEC-15** | The reports ask standing to admit outcomes beyond pass/fail: *standalone · sub-Lab · benchmark-only · architecture test · boundary case · rejected fit.* **"Rejected" must not mean "deleted"** — it means the Lab established a boundary. |
| Evidence standing metadata | **DEC-15** with **DEC-12** | Three correctness levels — behavioural plausibility, experimental agreement, law-level correctness — must never look equivalent in Search. Plus external-validity lifetime for versioned substrates (**DEC-17**). |
| Mechanism identity layers | **DEC-11** and **DEC-12** | Implementation identity · mechanism-family identity · observable-equivalence identity. DEC-11 asks when two rules are the same rule; DEC-12 asks *similar how, exactly*. This is their answer, not a new question. |
| Cross-Lab mechanism retrieval | **DEC-12** | Stated as a falsifiable platform hypothesis: *if Search only finds cloud mechanisms when asked about clouds, the semantic Corpus is much less interesting than claimed.* |
| Named geometry families | **DEC-8** | Grid World must not mean Cartesian grid. Includes surface topology being independent of display coordinates — cheaper and more general than a 3-D World. |
| Shared domain World templates distinct from Labs | **DEC-8** with **DEC-15** | Family H is one World with several mechanisms, not ten Labs. *Lab is a problem-space boundary; a World template may be shared across Labs.* |

---

## §4. Bucket C — requirements for existing documents, not decisions

Six items are contract or procedure requirements with an obvious home. They belong in the owning document's identifier namespace, **not** in the registry.

| Requirement | Home | Substance |
| :--- | :--- | :--- |
| **Abstraction-level declaration** | `01-core/labs.md` (LAB-) | Every Lab states what one Cell represents and **what disappears at that level.** Raised independently by Families B, C, and D; the same subject gives different answers at different levels (entry 11 is defensible at the convective-cell level and dubious at the fluid-element level). |
| **"Static analysis owns this" concession** | `01-core/labs.md` | Every Family H Lab opens by conceding what existing tooling answers. Without it the family becomes a weaker attack-path product with prettier playback. |
| **Fit frames for high-overclaim Labs** | `01-core/labs.md` | For Labs whose commercial attraction would bias the review, write a document **whose explicit job is to make rejection possible**, before the Knowledge Brief. Vindicated by `47-lateral-movement-lab.fit-frame.md`. |
| **Reducibility levels** | `01-core/labs.md` (LAB-6, LAB-7) | "Reducible" has carried six meanings across the catalog: analytically reducible · algorithmically tractable · numerically solved · empirically parameterized · operationally sufficient. **SCR's opening differs in each** — a mature empirical fit leaves real mechanism uncertainty; an exact theorem leaves almost none. Applies retroactively to all sixty briefs. |
| **Lattice-artifact control Study** | `01-core/studies.md` | Any Lab whose headline measurement is orientation, roughness, branching, front shape, or lane direction must rotate the initial condition, repeat on an alternate lattice, vary the neighbourhood, and measure orientation bias. **Physical and numerical anisotropy can look identical.** Automatable. |
| **Reader discrimination and validation rigour** | `01-core/readers.md` | Readers must distinguish *same picture, different mechanism* — response to perturbation, growth-history response, defect motion, recovery after damage, scaling under growth. And they must not classify confidently past their finite-size and crossover discipline. |
| **Mechanism analysis as a mode** | `01-core/studies.md`, `01-core/generation.md` | The mechanism may be supplied rather than inferred — a retry policy, a routing protocol, a scheduler. **Study orchestration over known readable mechanisms is as native to SCR as Generation is**, and defining the product identity narrowly around Generation would exclude several of the strongest Labs. |
| **Semantic-state sufficiency test** | `01-core/labs.md` with the §13.1 ceiling | Where a Lab compresses meaning into a scalar — contamination, distortion, confidence, trust — the fit review must test whether the abstraction preserves the behaviour, because a malicious instruction survives by its meaning in context and a summary drifts in a *direction*. **If the scalar cannot carry it, the Lab fails rather than promoting opaque embeddings as fake precision.** |

---

## §5. What the catalog also produced that is not a requirement

Two artifacts that belong in the eventual omnibus rather than in any document listed above.

**The rejection taxonomy.** SCR's boundary is not one line; it is seven distinct failure modes — wrong interaction structure · subject-defining global solve · solved dynamics with an observation problem · planned rather than emergent process · substrate ageing faster than generalization · mature incumbent · representation destroying the mechanism. **A fit review should record rejection reason(s), not merely a grade**, and a Lab can fail for two independent reasons (entry 58 does).

**The DEC-3 execution vocabulary.** Five entries pressure temporal semantics and need different things. **Do not resolve DEC-3 with a boolean such as "supports async."** The proposed vocabulary — *step · delayed effect · message · scheduled event · phase* — is recorded in the Family G report with its acceptance cases: entry 46 for *message*, entry 44 for *scheduled event*, entry 34 for *phase*.

---

## §6. What this document does not do

It assigns no identifiers, decides nothing, and resolves no DEC-owned question (F-22, §36.6). It does not amend SCR-F §40 — adding records there is a pending amendment under §36.5, as the existing DEC-21 to DEC-24 block already notes.

It also does not claim the triage is correct. Two entries in Bucket A (**A4** and **A5**) may turn out to be answers to DEC-8 and DEC-22 rather than separate records, and that is a judgement for whoever owns those. Bucket B's assignments are proposals, not findings.

**The one thing it does assert:** the sixty-Lab exercise generated these questions from domains rather than from architecture speculation, which is what gives them standing. Several were invented independently in three or four unrelated families. That recurrence is the evidence.
