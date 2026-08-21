# Family I — Weak fits and boundary markers
## Lab Knowledge Report v1

### Epidemic Spread · Opinion and Adoption · Ant Trail · Parking Lot

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/i-boundary-markers/family-i-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family I (entries 57–60)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md`
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 57–60 in `../short-lab-definitions/`
**Responds to:** `../../critiques/SCR_Labs_51-60_Critique_v0.1.md`
**Cites:** SCR-F v0.2 §11, §12, §15, §29, §30, §41–43; F-7, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

## What this family is for

**This is a deliberate boundary family, and it is not a weak ending.**

The sixty-Lab catalog's final four are not increasingly desperate attempts to find uses for SCR. Each tests a different temptation, and each answers it:

| Entry | The temptation | The answer |
| :--- | :--- | :--- |
| 57 Epidemic Spread | *Contagion is local, therefore grid.* | No. |
| 58 Opinion and Adoption | *Neighbour influence exists, therefore CA.* | No — and for two independent reasons. |
| 59 Ant Trail | *Agents plus a local field looks like CA.* | Maybe — but only if the architecture supports both honestly. |
| 60 Parking Lot | *A spatial occupancy pattern exists, therefore a local mechanism.* | Absolutely not. |

**A sixty-Lab catalog in which every entry somehow became "plausible" would be evidence that the fit-review method cannot say no.** This family exists so the fit scale has a real floor, and so the [strong] grades elsewhere mean something.

It is less about where SCR should make money than about **whether the platform knows when to stop.**

### The catalog's boundary is not one line

The single most important thing the sixty-Lab exercise produced is that **SCR's boundary is a set of distinct failure modes**, not a single threshold. Seven have now been named across the catalog:

| Reason | Meaning | Examples |
| :--- | :--- | :--- |
| **A — Wrong interaction structure** | The apparent spatial arrangement is not the causal interaction network | **60**, grid-based **58**, grid-based **57** |
| **B — Domain-defining global solve** | A local-looking event is driven by a whole-system solve | 42, 43, 31; parts of 34 and 18 |
| **C — Solved dynamics; the real problem is observation** | Dynamics are analytically understood; practice struggles because state is unmeasured | 51 |
| **D — Planned or coordinated process** | A scheduler or organizational plan determines the dominant dynamics | 53, 39, much of 44 |
| **E — Substrate ages faster than generalization** | Historical evidence stays valid; **external validity decays** | 49 |
| **F — Mature incumbent already answers the question** | Overlaps others but deserves naming | 43, static reachability in Family H, classical 30 |
| **G — Representation destroys the mechanism** | The Cell/World abstraction is too coarse even where the interaction idea is attractive | Text reduced to a contamination scalar (49); deformable cells as fixed sites (27); moving substrates (13) |

> **The final fit-review framework should record rejection reason(s), not merely a grade.** A Lab can fail for two independent reasons — entry 58 does.

### Not every "reducible" claim is equally strong

A correction that applies across all sixty briefs. "Reducible" has been used for six different things, and SCR's opening differs in each:

| Level | Meaning | Opening left |
| :--- | :--- | :--- |
| **Analytically reducible** | Closed form or theorem | Very little |
| **Algorithmically tractable** | Efficient exact or controlled computation | Little |
| **Numerically solved** | A standard solver answers reliably | Little |
| **Empirically parameterized** | An observed curve predicts adequately | **Mechanism uncertainty remains** |
| **Operationally sufficient** | Practitioners have a serviceable method | **Possibly real** |

A mature empirical fit may leave substantial mechanism uncertainty; an exact theorem usually leaves much less. The omnibus should adopt this distinction.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 57 — Epidemic Spread

| | |
| :--- | :--- |
| **Role** | High-risk rejected / weak-topology benchmark |
| **Standing** | **[weak]**, inherited; not re-derived |
| **Rejection reasons** | **A — wrong interaction structure**; **F — mature incumbent** |
| **Recommendation** | **Do not build a public-facing human epidemic Lab** |
| **Visual credibility** | **Class 1, and the catalog's most likely to cause real harm** |

**The phenomenon.** An infectious disease passes between people in contact. From local transmission repeated come epidemic curves, waves, spatial spread, herd immunity thresholds, and pathogen persistence or extinction.

**The established shortcut, and it is enormous.** The compartmental framework dates to Kermack and McKendrick (1927) and gives the epidemic curve, the final size relation, and the threshold condition in closed form. **R₀** is the field's central quantity: above one the epidemic grows, below one it dies, and the herd immunity threshold is 1 − 1/R₀. The network version is also largely solved — epidemic thresholds depend on the degree distribution, and the threshold **vanishes** on scale-free networks with a heavy enough tail, so any transmissibility can sustain an epidemic [11]. Percolation theory maps epidemics on networks to bond percolation, giving final sizes and thresholds analytically.

**Two independent failures.**

*Wrong topology.* Real human contact structure is **not a geographic lattice** at the scales public health cares about. It is heavy-tailed, clustered, assortative by age, and has long-range links from travel — and the last of these is decisive, because metapopulation models coupling local transmission to air travel reproduce global spread timing precisely because **long-range mixing dominates the geography.** A grid model produces a smooth advancing front, which is a picture of a process that does not occur.

*Mature field.* The reducible core is vast, and the serious residual questions already have sophisticated network and agent models with large research communities and national-scale calibration.

**The product concern is more important than either**, and it is a different kind of hazard from the rest of the catalog:

> **The output is socially portable.** A vivid animation will escape its caveats.

That is not a practitioner over-reading a technical visualization. It is model output circulating in policy argument, screenshotted without its caption, quoted by people with strong priors. §12 and §26 are not sufficient protection against it.

**The genuine residue, and it does not rescue the grid.** Superspreading — transmission is highly overdispersed, so early outbreak outcomes are bimodal and stochastic in a way mean R₀ does not capture, and whether an introduced chain takes off is genuinely uncertain. That is ensemble-shaped and suits the platform. But the abstract case is solved by branching-process theory, and the interesting version needs realistic contact structure, which returns to a Network World. **There is no version of this Lab where a grid earns its place.**

**Assessment.** **Keep weak; avoid a public-facing build.** The cross-Lab contagion mechanism family can exist without public-health theatre — **use lower-risk analogues: worms (54), invasion fronts (14), biofilm spread (25), excitable media (21).**

---

## Lab 58 — Opinion and Adoption

| | |
| :--- | :--- |
| **Role** | **Double-rejection reference case**; low-stakes rewiring benchmark |
| **Standing** | **[weak]**, inherited; not re-derived |
| **Rejection reasons** | **A — wrong interaction structure**; **F — solved canonical lattice models**; plus weak measurement semantics |
| **Recommendation** | Rejection and dynamic-topology toy benchmark only |
| **Visual credibility** | **Class 1 by political readability**, not by technical persuasiveness |

**The phenomenon.** People's views and choices are influenced by those around them, producing consensus, persistent disagreement, regional blocs, surviving minorities, and adoption curves that take off suddenly after long quiet periods.

**Why this entry is especially valuable: it fails twice, independently.**

*Wrong World.* A social network is not a square lattice, and it differs in every property these dynamics depend on — degree distribution, clustering, path length, community structure.

*Solved canonical lattice models.* Where the lattice abstraction is used, **many famous results are already known analytically.** The voter model's behaviour on lattices is understood rigorously: coarsening to consensus in one and two dimensions with known exponents, consensus time scaling with system size, and no consensus in the infinite system above two dimensions. These are theorems. The Ising model at zero temperature is the physics parent; Sznajd, majority-rule, bounded-confidence, and Axelrod models all have substantial analytic and numerical literatures [11]. Threshold models cover adoption, including the counterintuitive result that cascades are possible only within a window of connectivity [11].

**So the abstraction is wrong for the domain, and where the abstraction is right, the answer is already a theorem.** That is a stronger rejection than entry 57's, which at least retains a genuine irreducible residue.

*A third issue: weak measurement semantics.* "Opinion" as a scalar often lacks a direct empirical observable. Physics Labs can point to a thermometer; this one cannot, and the field's own literature acknowledges it. **That makes apparent precision especially dangerous.**

**The one architecturally useful residue.** **Co-evolving network structure** — people change who they talk to based on what those people think, producing fragmentation into disconnected like-minded groups. That is self-constructed topology (entries 18, 48, 56), it is not analytically solved, and **this is the cheapest domain in the catalog in which to test it**: one state variable, a two-line rule, and nobody harmed by getting it wrong.

But that does not rescue Opinion Dynamics as a domain Lab.

**Assessment.** **Keep as a rejection reference and a low-stakes rewiring benchmark only.** One caution the catalog should record: **do not let its political readability turn it into a marketing visualization.** A simulation captioned *how minorities become majorities* will be read as a claim about actual political processes by people with strong priors, regardless of what the document says.

---

## Lab 59 — Ant Trail

| | |
| :--- | :--- |
| **Role** | **Agent-plus-field composition acceptance Lab** |
| **Standing** | **[weak]**, inherited — but **weak for a reason entirely different from 57 and 58** |
| **Rejection reason** | None of A–G. **The mechanism is genuinely local and spatial; the problem is architectural.** |
| **Recommendation** | **If SCR introduces moving Participants plus persistent fields, this should be the first acceptance Lab** |
| **Visual credibility** | Class 3 |

**The phenomenon.** An ant that finds food walks home laying a chemical trail. Others encountering it tend to follow, and reinforce it if they also find food. The pheromone evaporates, so trails to exhausted sources fade. Within minutes a colony converges on a food source, and on the shortest of several routes, without any individual knowing the layout. This is the founding example of **stigmergy** — coordination through modification of a shared environment rather than direct communication.

**The established shortcut.** The canonical double-bridge experiment (Deneubourg and colleagues, around 1990) gave ants two paths of different length; the shorter accumulated pheromone faster because round trips completed sooner, and the colony converged on it [11]. The accompanying model — choice probability as a nonlinear function of relative pheromone concentration — has a **symmetry-breaking bifurcation** that is analytically tractable: below a threshold nonlinearity traffic splits, above it the colony commits. With two paths of *equal* length the colony still commits to one, chosen by amplified fluctuation.

**Why this is the best kind of weak Lab.** Entries 57, 58, and 60 fail because their substrates are wrong. **This one fails for an architectural reason**, and the domain mechanism is actually local and spatial. The problem is the composition:

- moving agents;
- a persistent scalar field;
- field decay;
- agents modifying the field;
- the field modifying agent decisions.

**That means the Lab becomes valid if SCR deliberately supports this composition.** It is a fixable failure, which entry 60's is not.

**Why it is the ideal acceptance test.** Unlike immune cells, wildfire, or complex robotics, the canonical ant experiment is **tiny, low-stakes, measurable, analytically characterized, and visually obvious**. There is a known right answer to check against.

> **Do not justify a moving-participant feature with a high-stakes Lab first. Use ants.**

**What it clarifies about composition.** "Two mechanisms" is too coarse for this case. The ants have an action policy; the pheromone has field dynamics; both evolve; **they are not symmetrical Plugins.** A useful composition model may need different declared roles:

| Role | Function |
| :--- | :--- |
| **Participant mechanism** | Proposes movement or action for bounded moving participants |
| **Field mechanism** | Updates persistent environmental quantities |
| **External input** | Changes independent of simulated state |
| **Coordinator mechanism** | Makes global decisions, if SCR ultimately supports one |

That taxonomy is more honest than *multiple Plugins, all peers.* **Do not implement these as special Lab types yet — but use Ant Trail as the test case when designing the composition contract** (DEC-1).

**Correction from the first pass.** The first pass leaned on ant colony optimization's status as an algorithm. The domain caution is that real ants use trail pheromones alongside visual landmarks, path integration, and individual memory, and many species do not use trails at all — the tidy stigmergic story is one mechanism among several, drawn from the species the models were built from.

**Assessment.** **Weak as a domain Lab, and the most useful of the four here.** The amplified-fluctuation commitment on equal branches is also a fine demonstration object: identical initial conditions, deterministic-looking convergence, an outcome decided by noise. Run it twenty times and get a distribution — F-14 and §20.3 in miniature, on a system where nobody could be harmed by the result.

---

## Lab 60 — Parking Lot

| | |
| :--- | :--- |
| **Role** | **Terminal boundary marker / fit-review floor** |
| **Standing** | **[insane]**, inherited — **and the grade should not be softened** |
| **Rejection reason** | **A — wrong interaction structure**, in its purest form |
| **Recommendation** | **Keep the document permanently. Never build the Lab.** |

**The phenomenon.** Cars enter a car park, drivers look for a space, and occupancy patterns form — spaces near the entrance and the shop door fill first, distant rows stay empty until nearly full, waves of arrival and departure through the day.

Superficially: an occupancy field evolving on a grid, with local rules about which space a driver takes.

**Why nothing rescues it.** A driver's choice is not influenced by the cars in adjacent spaces. It is influenced by the position of the building entrance, the visible extent of vacancy across the whole lot, and the driver's plan. **Adjacency in the model does not correspond to influence in the world** — the selection rule's failure at its most direct.

There is no local mechanism to be irreducible *about*. Occupancy is the aggregate of independent decisions each made against a global view, and aggregate independent choices are describable statistically. Where computation is genuinely required it is optimization: assigning drivers to spaces to minimize walking is a polynomial assignment problem, and cruising-for-parking is a search and queueing problem with tractable treatments. The relevant literature is economics and operations — pricing to maintain target vacancy, search traffic as a component of urban congestion — addressed with those tools, and where individual choice is modelled it is **discrete choice** against a utility function, which matches what drivers actually do.

**What this entry demonstrates, and why it earns permanent shelf space.**

- **Bounded Cell state is not sufficient.** A parking space trivially clears the semantic ceiling and the Lab is still hopeless — the ceiling is a necessary condition, not a sufficient one, and a fit review must not be reassured by passing it.
- **Spatial occupancy is not evidence of spatial causation.**
- **Visible pattern is not evidence of an emergent local mechanism.**
- **A grid can represent an *outcome* while having nothing to do with the *decision structure*.**

That last point is the most valuable. Many bad cellular models begin with *the output is a map, therefore the mechanism belongs on a grid.* **Parking Lot demolishes that**, and it does so more cleanly than any argued case could.

Every other weak entry in this catalog has some residue worth stating — 57 has superspreading, 58 has co-evolving networks, 59 has agent-plus-field architecture, 51 has deletion racing re-derivation. **This one has nothing, and that is precisely its usefulness.** A boundary needs a point that is unambiguously outside it.

**Assessment.** **Insane, as inherited, and not to be softened.** It is a unit test for intellectual restraint, and retaining it is the discipline §30 and §41–43 claim, made visible.

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Moving Participants as a first-class World capability** | **DEC-24** | 59 is the ideal acceptance case. State has now appeared on movers in ecology, immunology, crowds, robots, evacuation, ants, and attacker abstractions. |
| **Composition roles** — participant / field / external input / coordinator | **DEC-1** | 59. More honest than "multiple Plugins, all peers". |
| **Dynamic Connections** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | 58 is the cheapest, lowest-stakes test |
| **Rejection reasons recorded, not just grades** | **DEC-15** | The whole family; 58 fails twice |
| **Reducibility levels** — analytic / algorithmic / numerical / empirical / operational | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | Applies retroactively to all sixty briefs |
| **Output risk policy** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | 57, and 58 by political readability |

### A proposed model, from the catalog as a whole

Across sixty entries the same shape keeps appearing, and it can be stated cleanly:

- **Cells** are locations and state-bearing substrate.
- **Participants** are bounded mobile state records.
- **Connections and Layout** are permitted relations and movement.
- **Plugins** propose participant and Cell changes.
- **The Reactor decides.**

That preserves the original Cell concept rather than overloading it, and **Ant Trail is the ideal acceptance case** for the participant half.

### Build priority

**Build if and only if moving participants plus persistent fields are adopted.** **Ant Trail (59)** — the acceptance Lab, and the first one, not a high-stakes Lab.

**Keep permanently, never build.** **Parking Lot (60)** — the fit-review floor.

**Keep as rejection references.** **Epidemic Spread (57)** — and use lower-risk contagion analogues instead. **Opinion and Adoption (58)** — usable as a rewiring toy benchmark, not as a domain Lab or a demonstration.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[D]** Kermack, W. O. & McKendrick, A. G. (1927) — the compartmental epidemic framework, final size relation, and threshold condition.
2. **[D]** Pastor-Satorras, R. & Vespignani, A. (2001) — epidemic threshold vanishing on scale-free networks; metapopulation models coupling local transmission to air travel.
3. **[D]** Voter model exact results on lattices — coarsening exponents, consensus time scaling, and dimensional dependence; Castellano, C., Fortunato, S. & Loreto, V. (2009) *Statistical physics of social dynamics*, the standard review.
4. **[D]** Granovetter, M. (1978) threshold models of collective behaviour; Watts, D. J. (2002) global cascades on random networks — cascades possible only within a connectivity window.
5. **[D]** Deneubourg, J.-L. and colleagues (around 1990) — the double-bridge experiment and the nonlinear choice model with its symmetry-breaking bifurcation; ant colony optimization as its algorithmic descendant.
6. **[D]** Discrete choice modelling of parking search in transport economics; parking pricing for target vacancy; cruising-for-parking as a component of urban congestion.

*Family I is deliberately reference-light. Its entries are boundary markers, and their value is in the argument rather than in domain evidence.*

---

## Non-claims

This report performs no fit reviews and establishes no fit. **Nothing in this family models any real disease, population, political process, insect species, or facility. Nothing here predicts transmission, evaluates any intervention, describes opinion change or adoption in any real population, or informs public health, clinical, policy, social, commercial, or facility decisions** (§41, §43). Entry 57's output in particular must not be presented in any form that could circulate as a public-health claim. Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment and carry no standing.
