# Family D — Cells, tissue, and disease
## Lab Knowledge Report v1

### Biological Pattern Formation · Excitable Media · Cortical Spreading Depression · Avascular Tumour Growth · Wound Healing · Biofilm Morphology · Immune Response · Cell Sorting and Tissue Boundary

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/d-cells-tissue-and-disease/family-d-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family D (entries 20–27)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md` — four axes, Lab roles, visualization credibility class
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 20–27 in `../short-lab-definitions/`
**Responds to:** `../../critiques/SCR_Labs_11-20_Critique_v0.1.md` (entry 20), `../../critiques/SCR_Labs_21-30_Critique_v0.1.md` (entries 21–27)
**Cites:** SCR-F v0.2 §5, §11, §12, §15, §26, §29, §30, §38.6, §41–43; F-5, F-7, F-17 · LAB-3, LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

> ## Medical scope statement — read before anything else
>
> Every Lab in this family names a subject that carries clinical weight. A rendered arrhythmia, tumour, migraine wave, immune lesion, or healing wound **is not neutral**: readers infer clinical significance from the subject itself, regardless of caption.
>
> **Nothing in this family models a patient, bears on diagnosis, prognosis, device design, drug effect, or therapy, or is suitable for any medical decision.** No entry here accepts patient-specific input, displays clinical units, or supports Study language such as *treatment*, *response*, *risk*, or *prediction*.
>
> A standard non-claims paragraph is probably insufficient for this family. What is needed is a **policy surface** — a Lab credibility class that governs labelling, export and report language, and whether output may appear without Study context. That is recorded as an unregistered platform requirement below, not resolved here.
>
> The risk this guards against is specific: **the View layer silently upgrading a mechanism experiment into a medical claim** (§12, §26).

---

## What this family is for

This is the batch that answers a question hanging over the whole catalog: **what is SCR good at when the field already has excellent models?**

Cellular, agent-based, Potts, reaction–diffusion, and phase-field models are canonical across this family. That could have made the whole thing redundant. Instead the defensible role is narrower and stronger — not *invent the idea of modelling this spatially*, not *replace the mature simulator*, not *predict a patient*, but:

> **systematically explore mechanism families, compare them under one evidence protocol, retain the failures, and identify cross-domain structural similarity.**

### Three kinds of correctness, which are not equivalent evidence

This family makes a distinction the earlier batches only gestured at. **Lab standing must record which level of external check is available**, because it will matter enormously when Search ranks mechanisms:

| Level | Question | Example in this catalog |
| :--- | :--- | :--- |
| **Behavioural plausibility** | Does it produce a pattern resembling the subject? | Wildfire (entry 1) |
| **Experimental agreement** | Does it reproduce measured quantities from a controlled reference? | **Biofilm (25), Wound healing (24)** |
| **Law-level correctness** | Does it satisfy a known analytic relation that must hold? | Grain growth (entry 30, Family E) |

A beautiful tumour spheroid has behavioural plausibility. A biofilm Run matching branch spacing and sector statistics has experimental agreement. These must never look equivalent.

### Cross-Lab similarity needs stricter vocabulary

This family repeatedly connects tumour margins, wound edges, biofilm fronts, and dendrites through protrusion-driven fingering. That connection is useful and it is being stated too loosely. The driving fields genuinely differ — nutrient diffusion in a tumour, mechanical and migratory feedback at a wound edge, nutrient and motility in a biofilm, heat and solute plus surface-energy anisotropy in solidification.

Three levels, and the catalog should use them precisely:

- **Same mechanism** — equivalent local causal structure.
- **Same mechanism family** — shared abstract interaction pattern, different state meanings. *This is the honest claim for the fingering group.*
- **Same behaviour family** — similar outcome without demonstrated causal equivalence.

Without this, cross-Lab retrieval degrades into metaphor matching.

### "Cell" now means three things

The naming collision is unavoidable here and §5 makes it a system property rather than a style preference. Three distinct concepts:

- **SCR Cell** — the platform's bounded state-bearing unit.
- **Biological cell** — an actual moving, deformable organismal unit.
- **Lattice site** — a fixed location that may contain a biological cell, part of one, or none.

Immune cells *move between* SCR Cells. One sorting cell *occupies many* lattice sites. Every entry below therefore states explicitly what an SCR Cell corresponds to, and the family uses "site" where the biological reading would be ambiguous.

### The anisotropy control Study

Four entries in this family and the next have a headline measurement that is orientation, roughness, branching, or front shape. **Physical anisotropy and numerical anisotropy can look identical.**

> **Any Lab whose headline measurement includes orientation, roughness, branching, or front shape requires a lattice-artifact control Study:** rotate the initial condition relative to the lattice, repeat on an alternate lattice geometry, vary the neighbourhood definition, and measure orientation bias explicitly.

This is exactly the kind of test SCR can automate well, and it is a genuine platform capability rather than a caveat.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 20 — Biological Pattern Formation

| | |
| :--- | :--- |
| **Role** | **Flagship** corpus / mechanism-family / robustness Lab |
| **SCR Cell =** | A tissue element or pigment-cell site. Biological cells map roughly one-to-one at this resolution. |
| **Standing** | [strong], inherited; not re-derived |
| **Falsifiable question** | Which mechanism families produce the target pattern *robustly* under noise, rather than accidentally from lucky initial conditions? |
| **Correctness available** | Experimental agreement (measured stripe spacing, rearrangement under growth) |
| **Rediscovery risk** | Medium — Turing patterns fall out of many mechanisms |
| **Reach** | Neighbour-local |
| **Drivers** | Two signals at different ranges — a mild composition case (DEC-1) |
| **Visual credibility** | Class 2 |

**The phenomenon.** A leopard has spots, a zebra stripes, an angelfish stripes that reorganize as it grows, a seashell a permanent record of a one-dimensional process along its growing edge. The general recipe is **short-range activation and long-range inhibition**: something makes a cell adopt a state and encourages immediate neighbours to do the same while suppressing it further away. Two opposed ranges give a characteristic spacing and — depending on parameters — spots, stripes, labyrinths, or inverse spots.

**The established shortcut.** Turing (1952) showed two diffusing substances, the inhibitor faster, can destabilize a uniform state into a periodic pattern [12]. Linear stability gives the wavelength and the existence conditions; the gross spots/stripes classification is mapped.

**The experimental turn, and it is stronger than the first pass credited.** Before 1995 there was **no conclusive experimental evidence** for a Turing system in biology. Kondo and Asai showed that stripes on the marine angelfish *Pomacanthus* are not fixed — unlike mammal patterns that enlarge proportionally, the stripes maintain their spacing by continuous rearrangement as the fish grows — and that a Turing-based simulation **correctly predicted future stripe patterns** [1]. Prediction, not resemblance. That is the strongest single result behind this Lab.

**Real mechanisms are often not diffusing chemicals.** Zebrafish stripes involve direct interactions between pigment cell types with different ranges; appendage spacing involves mechanics as well as chemistry [11]. The *structure* holds while the substrate varies — which means a lattice with local rules is not merely approximating a PDE. For contact-mediated systems it may be closer to the truth than the PDE is.

**Reducible.** Whether a given activator–inhibitor system patterns at all, and at what wavelength. The parameter conditions. The gross morphology classification. Wavelength scaling with domain size.

**Irreducible.** Selection among coexisting stable patterns — linear analysis says the uniform state is unstable and gives the wavelength; it does not say whether you get spots or stripes when both are stable. Defect positions and their coarsening. Patterning on a **growing domain**, which produces the stripe insertion and splitting the angelfish result depends on. Robustness: many mechanisms that pattern do not pattern *reliably*.

**Correction from the first pass.** Calling pattern selection, defect statistics, and robustness "open" as one category overstates it — all three have substantial theoretical and computational literatures. The opportunity is different and probably stronger:

> **SCR could systematically compare many semantically described mechanism families under one evidence protocol**, which no individual investigator does because it is not a paper.

**The mechanism-identity problem, and this Lab is the natural benchmark for it.** Two mechanisms producing indistinguishable spots are not scientifically equivalent. Readers must measure more than morphology. Candidate discriminators: response to perturbation, growth-history response, defect motion, recovery after damage, scaling under domain growth, robustness to noise. **This Lab could become the platform's benchmark for distinguishing *same picture, different mechanism*.**

**On growing domains.** The World's participant count changes during a Run. Before adding dynamic Cell allocation, ask whether growth can be represented by activating previously inactive sites inside a fixed larger World, or by coordinate remapping. Those have very different architecture costs, and true topology growth is a DEC-24 expenditure.

**Cell state.** *Persistent:* signal concentrations or pigment-cell type, differentiation state. *Derived:* local activation and inhibition levels.

**Assessment.** *(judgment, no standing)* **Top-tier flagship and calibration candidate.** The mechanism is local and the locality is physical; the reducible boundary is crisp and documented by the field; the phenomenon is visible, measurable and photographable; and unusually, a lattice may be *more* faithful than the continuum model for contact-mediated systems. This is also the natural home for the corpus argument — pattern formation is the field where the same abstract mechanism recurs under different biological substrates, and where a practitioner's real question is *what local rule structure could produce this?*

---

## Lab 21 — Excitable Media

| | |
| :--- | :--- |
| **Role** | **Flagship** domain Lab **and cross-Lab reference mechanism family** |
| **SCR Cell =** | A tissue element. Not a biological cell — coarser. |
| **Standing** | [strong], inherited; not re-derived |
| **Falsifiable question** | Which local heterogeneity structures permit a premature stimulus to break a wavefront and initiate re-entry? |
| **Correctness available** | Experimental agreement — optical mapping movies match SCR's stored-history data type unusually well |
| **Rediscovery risk** | Low for initiation; the canonical CA is the *baseline*, not the target |
| **Reach** | Neighbour-local, **physically anisotropic** |
| **Drivers** | Stimulus as external input |
| **Visual credibility** | **Class 1 — highest in the family** |

**The phenomenon.** Three states and one rule: a resting element does nothing until a neighbour excites it; once excited it fires and excites its neighbours; then it is refractory before returning to rest. From that you get travelling waves that annihilate on collision, and — if a wave is broken so one end is free — **spiral waves** rotating indefinitely, re-exciting tissue as fast as it recovers.

In heart muscle this is not an abstraction. A normal beat is one wave sweeping once. A spiral is re-entry. When it breaks into many wavelets, the result is fibrillation.

**The established shortcut.** Wiener and Rosenblueth described cardiac excitation in essentially these terms in 1946 [11]. **Greenberg and Hastings (1978)** gave the minimal three-state discrete model, showing that spatial inhomogeneities in an excitable medium organize into spatial patterns oscillating periodically in time [2]. Continuum theory supplies plane wave speed, the **eikonal relation** (speed falls with front curvature, which sets a minimum spiral core), and spiral period from wavelength and refractory time [11]. **Restitution** — action potential duration depending on the preceding rest interval — gives a genuine analytic criterion for alternans onset [11].

**Reducible.** Plane wave speed. Curvature–speed relation. Minimum core radius. Spiral period. Whether a medium is excitable. One-dimensional conduction block. A substantial body of real results.

**Irreducible.** **Wave break initiation** — a spiral needs a broken front, and breaks arise where a wave meets partly-refractory tissue at a scar, a fibrotic patch, or a region of altered channel expression. Whether a given premature beat at a given phase breaks against a given heterogeneity is arrangement- and timing-dependent with no closed form. Spiral breakup into many wavelets. Anchoring, drift, and meander, which decide whether an arrhythmia is stable or self-terminates.

**Correction from the first pass.** "The irreducible half is the half people die of" is powerful and oversells SCR's relevance to clinical electrophysiology. The defensible version:

> **The clinically consequential phenomena are often initiation-, heterogeneity-, and state-dependent, which makes ensemble mechanism exploration scientifically relevant even though SCR is not a clinical model.**

**Defibrillation is out of early scope.** Whether a shock terminates fibrillation is close to a patient-and-treatment problem. Retain it as a background stress case, not an initial Study target.

**Anisotropy is physiology here.** Cardiac fibres conduct several times faster along their axis, and fibre orientation rotates through the ventricular wall. That is *desired* anisotropy — a Lab that ignores it models a different tissue — which makes the lattice-artifact control Study especially necessary, because desired and numerical anisotropy must be separated rather than conflated.

**Cell state.** *Persistent:* excitation state (resting / excited / refractory), recovery timer. *Static:* local excitability, coupling strength, fibre direction, scar flag. Extremely small — Greenberg–Hastings uses a single integer.

**Assessment.** *(judgment, no standing)* **Top-tier flagship, and the catalog's strongest candidate for a *reference mechanism family*.** The platform job may matter more than the domain job: the same abstract structure recurs in cardiac tissue, cortical depolarization (22), chemical waves (35), calcium signalling, and possibly cloud convection (11). **Treat Excitable Media as a reference family in the mechanism ontology, not merely Lab #21** — it is where cross-Lab semantic retrieval should first be tested, and if Search cannot connect these, the Corpus claim is much weaker than advertised.

---

## Lab 22 — Cortical Spreading Depression

| | |
| :--- | :--- |
| **Role** | **Paired cross-Lab mechanism-transfer Lab** — not a standalone flagship |
| **SCR Cell =** | A cortical tissue element on a folded surface. |
| **Standing** | Ungraded |
| **Falsifiable question** | Does a mechanism family retrieved for cardiac wave break also produce propagation block at folded cortical boundaries? |
| **Correctness available** | Behavioural plausibility; some direct human electrocorticographic recording |
| **Rediscovery risk** | Low |
| **Reach** | Neighbour-local **on a manifold** |
| **Drivers** | Metabolic supply as external input |
| **Visual credibility** | Class 1 |

**The phenomenon.** A wave of near-complete depolarization crosses the cortex slowly, leaving tens of minutes of electrical silence before recovery. Leão described it in rabbit cortex in 1944, observing a depression of EEG activity moving at **3–6 mm/min** after stimulation [3]. Lashley, charting his own migraine auras in 1941, had inferred a cortical process progressing at about 3 mm/min across visual cortex; the connection between the two is the basis of the spreading-depression account of migraine aura [11]. In injured brain, recurrent depolarizations are recorded directly and associated with worse outcomes, apparently because compromised tissue cannot afford the energy cost of restoring ion gradients.

**The established shortcut.** The mechanism is ionic and diffusive — potassium and glutamate released from depolarizing cells diffuse out, depolarize neighbours past threshold, and propagate. Propagation speed follows from diffusivity and kinetics as a standard reaction–diffusion wave speed. Refractory duration follows from pump capacity.

**Correction from the first pass.** Claiming the reducible core is "much weaker than cardiac electrophysiology" is a comparison a domain expert would object to — spreading-depolarization theory is richer than propagation speed alone. The Lab does not need the claim. Its value survives on:

> **Many clinically interesting questions concern initiation, recurrence, geometry, and compromised tissue rather than homogeneous propagation.**

**Irreducible.** Propagation block at anatomical boundaries — the wave does not cross everywhere, and which regions depolarize decides what symptoms occur. Initiation, genuinely unknown in migraine. Recurrence and clustering in injured brain, where whether tissue has recovered enough to support the next wave is history-dependent. Interaction with compromised tissue, where a wave crossing tissue that cannot repolarize converts a transient event into permanent injury.

**The geometry point, restated usefully.** Cortex is a folded sheet. The first pass called this a 3-D problem; the sharper requirement is narrower and more generally valuable:

> **Surface topology must be independent of display coordinates.**

A folded sheet can be flattened while preserving adjacency. What must not happen is adjacency being inferred from rendering position. That is a platform property worth having regardless of this Lab.

**Hidden state with consequence.** Tissue that has depolarized and not yet restored its gradients looks quiet and is in danger. A view keyed to depolarization shows recovery; a view keyed to metabolic reserve shows accumulating injury — §38.6 at the highest stakes it reaches in this catalog.

**Cell state.** *Persistent:* depolarization state, recovery progress, metabolic reserve, tissue viability. *Derived:* extracellular potassium or a generic excitatory signal, if not carried explicitly.

**Assessment.** *(judgment, no standing)* **Keep as a paired cross-Lab mechanism-transfer Lab, not a standalone flagship.** Standalone the field is small and the incumbents cover the reducible questions. Paired with entry 21 the marginal cost is low and the marginal insight is a genuine test of whether a mechanism retrieved in one physiology illuminates another — which is the platform's most distinctive potential capability.

---

## Lab 23 — Avascular Tumour Growth

| | |
| :--- | :--- |
| **Role** | Mechanism-supply (spatial clonal competition); **not an early public-facing Lab** |
| **SCR Cell =** | A tissue site holding an occupancy state. May be one biological cell or a small volume depending on resolution — **state which**. |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Which local growth and competition rules produce infiltrative rather than compact margins, and which clonal lineages survive an expansion? |
| **Correctness available** | Experimental agreement — spheroid assays give growth curves, layer thicknesses, margin morphology |
| **Rediscovery risk** | Medium — hybrid CA tumour models are thirty years old |
| **Reach** | Neighbour-local |
| **Drivers** | Nutrient field as **interactive mechanism** — consumed by the thing it drives |
| **Visual credibility** | **Class 1, and the family's most dangerous subject** |

**The phenomenon.** A tumour with no blood supply lives on diffusion, which penetrates a hundred to a few hundred micrometres. Past a certain size it develops proliferating rim, quiescent layer, and necrotic core, and growth stalls at roughly one to two millimetres. Escaping that ceiling needs vasculature — a different phenomenon and a different Lab.

Within the ceiling the interesting variable is **margin morphology**, and it matters clinically out of proportion to its subtlety: an infiltrative margin is what makes complete surgical removal impossible.

**The established shortcut.** Gompertz and logistic curves fit tumour growth and have for a century. The critical radius for necrosis follows from oxygen diffusivity and consumption. The margin instability has the Mullins–Sekerka structure [11]. Lattice models are a large established literature, and **lattice artifacts are a known, managed problem in that field** — unusual, and SCR inherits both the problem and the field's awareness of it.

**Correction from the first pass.** "Everything about tumour size is reducible; everything about shape and composition is not" is too clean. Even avascular spheroid growth can involve nonlinear coupled nutrient, mechanics, death, and heterogeneity where size dynamics are not trivially Gompertzian. Treat Gompertz and logistic as **empirical reduced descriptions, not complete causal solutions**. The defensible split:

> **Bulk size trajectories often admit useful reduced descriptions; spatial morphology and composition require explicitly spatial models.**

**A second correction, and this one reverses the first pass's emphasis.** Waclaw and colleagues (2015) is not a demonstration that spatial structure *produces* heterogeneity. Its finding is the opposite and more interesting: large tumours are strikingly **homogeneous** where slow mutation accumulation would predict diversity, and **short-range dispersal and cell turnover limit intratumour heterogeneity** by causing rapid mixing — which also lets even a small selective advantage dominate quickly [4]. The first pass had this backwards.

**Irreducible.** Which morphology develops — stability analysis says the margin becomes unstable, not what shape results. Clonal competition in space. Treatment response with spatial refuges, where hypoxic cells are less sensitive *because of where they are* and survivors are not a random sample. Heterogeneous surrounding tissue.

**Treatment-response language is deferred.** Even mechanistic refuges pull the Lab toward clinical interpretation immediately. Early scope emphasizes morphology and clonal spatial competition; treatment-response Studies are explicitly out of scope for a first build.

**Cell state.** *Persistent:* occupancy state (empty / proliferating / quiescent / necrotic), division timer, clonal identity tag. *Derived:* local nutrient concentration, if the field is computed rather than carried.

**Assessment.** *(judgment, no standing)* **Plausible and scientifically legitimate, but not an early public-facing Lab.** Mathematical oncology is substantial, funded, and has run hybrid CA tumour models for thirty years — SCR arrives as a bulk generator of variants of an approach the field already uses well. The honest opening is the *ensemble*: the field publishes individual mechanisms and does not systematically publish which families fail.

---

## Lab 24 — Wound Healing

| | |
| :--- | :--- |
| **Role** | **Calibration Lab; good early build candidate** |
| **SCR Cell =** | A site in an epithelial sheet. Biological cells *move between* sites — the sheet is the thing that migrates. |
| **Standing** | Ungraded |
| **Falsifiable question** | Which local rules cause a uniform advancing edge to select a discrete set of leaders at a characteristic spacing? |
| **Correctness available** | **Experimental agreement, exceptional** — time-lapse spatial evolution, the same data type a Run stores |
| **Rediscovery risk** | Low for the transient; high for closure rate |
| **Reach** | Neighbour-local, with mechanical coupling through the sheet |
| **Drivers** | None external — a rare clean case |
| **Visual credibility** | Class 2 — "wound healing" sounds clinical; this is monolayer cell biology |

**The phenomenon.** Make a hole in an epithelial monolayer and it closes. Cells at the margin lose contact inhibition on that side, crawl in, divide to replace themselves, and stop when they meet. In small wounds a contractile **purse string** pulls the hole shut; in larger ones cells crawl, and the edge is not smooth — some cells become **leaders**, protruding ahead and dragging files of followers, so the closing edge fingers.

**The established shortcut.** The **scratch assay** is among the most-performed experiments in cell biology: scrape a monolayer, photograph it over hours, measure the gap. Cheap, standard, quantified, and routinely used to screen drug effects on migration.

**Correction from the first pass.** Calling closure rate "a Fisher wave speed" flattens too much of the scratch-assay literature — closure involves proliferation, collective mechanics, edge effects, density dependence, substrate adhesion, and distinct migration regimes. The point survives without the overclaim:

> **Simple closure-rate summaries are already well modelled and measured; SCR's opening is transient spatial organization.**

**Irreducible.** **Leader cell emergence and spacing** — a smooth edge spontaneously fingers, and which cells lead is amplified fluctuation among nominally identical cells. Collective versus individual migration, where adhesion relative to traction decides whether the sheet moves coherently, tears, or advances in swirling patches. Closure completion, where interdigitating fingers leave different residual structure than flat edges colliding. Contact inhibition failure, which is the biologically interesting mode.

**A methodological trap the Lab must avoid.** If leadership is supposed to *emerge*, a pre-labelled `leader` Cell state smuggles the answer into the model. Three things must be kept distinct:

- an **observed Reader label** — "leader-like", measured from behaviour;
- an **internal state variable** a mechanism explicitly proposes;
- an **imposed Cell type**, which is a modelling assumption and must be declared as one.

This generalizes: it is the §13.1 test in a specific form — *does this value need to persist to determine the future, or does storing it place the answer by hand?*

**Cell state.** *Persistent:* occupancy, migration polarity, division timer, adhesion state. *Derived:* contact count, leader-like classification (a Reader output, not state).

**Assessment.** *(judgment, no standing)* **Strong calibration Lab and a good early build.** The data argument is the strong one: a Run's stored history and a scratch-assay movie are structurally the same object — a sequence of frames of a spatial state — which makes accuracy testing genuinely feasible rather than aspirational. Leader emergence is a real, open, symmetry-breaking question in a funded field, and it is the same abstract instability as entries 23, 25, and 29 — **same mechanism family, not same mechanism.**

---

## Lab 25 — Biofilm Morphology

| | |
| :--- | :--- |
| **Role** | **Top-tier calibration candidate** — possibly second only to Grain Growth for platform testing |
| **Catalog status** | **Rename recommended: plate colony morphology.** See below. |
| **SCR Cell =** | A lattice site on an agar surface holding local biomass. Not one bacterium. |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | In the dense-branching regime between the DLA and Eden limits, which local rules reproduce measured branch spacing and sector statistics? |
| **Correctness available** | **Experimental agreement, and cheap** — a plate overnight, at known agar and nutrient concentration |
| **Rediscovery risk** | Medium — the phase diagram is mapped, the middle is not |
| **Reach** | Neighbour-local |
| **Drivers** | Nutrient field as **interactive mechanism** |
| **Visual credibility** | Class 2, rising to Class 1 if clinical language enters |

**The phenomenon.** Bacteria on a nutrient plate produce compact discs, fractal branching, dense concentric rings, or chiral pinwheels depending on agar hardness and nutrient concentration. Scarce nutrient makes growth diffusion-limited, so protruding tips get more food than valleys and branches sharpen; hard agar sharpens branching further.

There is a second, quieter phenomenon at the front. **Hallatschek, Hersen, Ramanathan and Nelson (2007)** showed that initially well-mixed populations of two fluorescently labelled *E. coli* strains develop well-defined sector-like regions with fractal boundaries as the colony expands, driven by random fluctuations originating in a thin band of pioneers at the frontier — and that the same occurs in yeast, suggesting a generic footprint of range expansion [5]. Neutral variants occupy whole sectors purely by position, with no fitness difference.

**The established shortcut.** The morphology phase diagram against agar hardness and nutrient concentration was mapped through the late 1980s and 1990s [11]. The branching is the familiar diffusion-limited instability; DLA and Eden are the limiting models with known exponents.

**Reducible.** Morphology class from the two conditions — read the diagram. Fractal dimension in the DLA limit — universal. Colony radius growth in the nutrient-rich compact regime. Sector count scaling in neutral range expansion, which the Hallatschek theory gives.

**Irreducible.** Branch geometry in the **dense-branching middle** between the limits, where neither limiting theory applies and where real colonies mostly live. Which lineage wins a sector — the statistics are predicted, the realization is not, and when a mutation is involved rather than a neutral marker the realization is what matters. Multi-species interpenetration. Spatially structured stress tolerance, where interior cells are metabolically inactive and drug-tolerant because of where they are.

**Correction from the first pass — scope.** "Biofilm" is too broad for a Lab about colony morphology on agar. A mature Lab must distinguish three different Worlds:

- **surface colony growth on nutrient agar** — what this brief is actually about;
- **attached hydrated biofilms under flow**;
- **clinical biofilm physiology**.

The drug-tolerance angle moves toward three-dimensional hydrated biofilms where the flat plate abstraction is much less faithful. **Excellent plate validation must not silently authorize clinical biofilm claims.** Name the scope honestly or create subprofiles.

**Cell state.** *Persistent:* biomass or occupancy, metabolic state (active / dormant), lineage tag. *Derived:* local nutrient concentration, growth rate.

**Assessment.** *(judgment, no standing)* **Top-tier calibration candidate.** The reference experiment is cheap, fast, controlled, and repeatable at will rather than observed opportunistically — a colony grows overnight at known conditions and the result is a photograph with measurable fractal dimension, branch spacing, and sector statistics. Very few Labs in this catalog can be checked against a controlled experiment costing a few pounds. Requires the lattice-artifact control Study, since branch geometry is the headline measurement and the field knows it.

---

## Lab 26 — Immune Response

| | |
| :--- | :--- |
| **Role** | Narrow mechanism-supply; **build late** |
| **Catalog status** | **Rename recommended: Granuloma Formation.** "Immune Response" is far too broad for the one defensible local-spatial case. |
| **SCR Cell =** | A tissue site. **Immune cells move between sites** — the vocabulary collision is at its worst here (§5). |
| **Standing** | Ungraded; I would grade it **weak-to-plausible** |
| **Falsifiable question** | Which local recruitment and killing rules produce a containing granuloma structure rather than clearance or dissemination? |
| **Correctness available** | **Qualitative only** — endpoint histology cannot check a time course |
| **Rediscovery risk** | High — the incumbent is an agent-based spatial model family built for this exact question |
| **Reach** | Neighbour-local; **recruitment arrives from outside the World** |
| **Drivers** | Circulating cell supply as external input — and it dominates |
| **Visual credibility** | Class 1 |

**The phenomenon.** Infection begins locally; resident cells detect it and release signals; signals recruit circulating cells; recruited cells kill infected cells and release more signals. When it fails, the response organizes instead: a **granuloma** is a ball of immune cells walled around a pathogen the body cannot eliminate — the characteristic lesion of tuberculosis, a containment rather than a cure, persisting for decades and able to break down.

The granuloma is genuinely emergent. Nobody designs it; it arises from cells following local rules about where to move, what to secrete, and when to kill.

**The established shortcut.** Target-cell-limited ODE models give clearance criteria, peak load timing, and within-host reproductive number for well-mixed infections. **Granuloma modelling has been explicitly agent-based for two decades** — spatial models with macrophages, T cells, bacteria, and diffusing chemokines on a grid, used to ask which local rules produce containment versus dissemination [11].

**Irreducible.** Containment as a *geometric* outcome — a well-mixed model cannot represent containment at all, only clearance or failure. Sanctuary by geometry, the same spatial-refuge mechanism as entries 23 and 25, and why tuberculosis treatment takes months. Recruitment feedback with delay, which can produce oscillation and self-sustaining inflammation with no pathogen left. Tipping between control and dissemination.

**Why it should be built late.** Three reasons compound. The incumbent is the same class of model with two decades of domain expertise. The parameters — recruitment rates, killing efficiency, in vivo cytokine diffusion — are poorly measured and individually variable, so calibration is out of reach. And the observations are endpoint histology: a slice through a lesion at biopsy, not a time course. **Genuine irreducible content plus near-total inability to check any of it is the worst case for accuracy (§30.6).**

**Cell state.** *Persistent:* occupancy by cell type, pathogen load, activation or exhaustion state. *Derived:* local signal concentration. Note that *occupancy by a motile cell type* is a site property, not a biological-cell property — the distinction must be maintained relentlessly in this Lab's writing.

**Assessment.** *(judgment, no standing)* **Weak-to-plausible; narrow to granuloma formation if retained, and build late.** The one genuinely valuable thread is the **cross-Lab spatial sanctuary family** with entries 23 and 25 — in all three a population survives treatment because of where it is, not what it is. That is a real observation a mechanism-indexed corpus is uniquely able to make. The granuloma is also a good §38.6 demonstrator: a stable-looking structure with live bacteria inside is the definition of latent infection.

---

## Lab 27 — Cell Sorting and Tissue Boundary

| | |
| :--- | :--- |
| **Role** | **Architecture boundary test** — excellent negative case |
| **SCR Cell =** | **Unresolvable cleanly.** One biological cell occupies *many* lattice sites in the honest representation. This is the entry's whole point. |
| **Standing** | Ungraded; I would grade it **weak as research** |
| **Falsifiable question** | Under which local rules does sorting become kinetically trapped rather than reaching the predicted equilibrium? |
| **Correctness available** | Experimental agreement for endpoint; hanging-drop aggregates are cheap and quantitative |
| **Rediscovery risk** | **High** — the canonical model is itself a lattice model in wide use |
| **Reach** | Neighbour-local |
| **Drivers** | None external |
| **Visual credibility** | Class 3 |

**The phenomenon.** Dissociate two embryonic tissues, mix the cells, and they sort — one type gathers into a ball, the other surrounds it, with a sharp boundary, often reproducing the layering they had in the embryo. Nothing directs this. It comes from cells preferring some neighbours over others, plus enough random motion to rearrange.

**The established shortcut, and it is the Lab's central problem.** Steinberg's **differential adhesion hypothesis** (early 1960s) is a thermodynamic argument: treat the populations as immiscible liquids with surface tensions set by adhesion, and the final configuration minimizes interfacial energy, with a transitive, predictable engulfment ordering [11]. **The endpoint is a shortcut, and a good one.**

**The canonical model is a lattice model.** Graner and Glazier (1992) introduced the two-dimensional extended Potts model for biological cell sorting [6]; Glazier and Graner (1993) extended it, showing differential adhesion with fluctuations suffices to produce complete and partial sorting, checkerboard, position reversal, and dispersal [7]. It is now among the most widely used frameworks in computational developmental biology. *(The first pass cited "Glazier–Graner 1992"; the 1992 paper is Graner and Glazier in Physical Review Letters, the 1993 is Glazier and Graner in Physical Review E — author order and venue both differ.)*

**Correction from the first pass — and it sharpens the Lab.** "The outcome is predictable from thermodynamics" must be constrained. Modern developmental boundary formation can involve active forces and signalling rather than passive adhesion. The stronger statement:

> **For the classical passive differential-adhesion regime, endpoint ordering is reducible. Active boundary systems are a different mechanism class.**

That is better than treating Steinberg as a universal answer, and it gives the Lab a real distinction to test.

**Irreducible.** Whether sorting completes and how long it takes — real aggregates get **kinetically trapped** in configurations that are not the global minimum, and whether they do depends on initial arrangement and available motion. Coarsening dynamics and their exponent. Boundary maintenance under continuous cell division, which is a dynamic balance rather than a minimum.

**The architecture boundary this Lab exists to mark.** In the cellular Potts tradition **one biological cell occupies a variable connected region of lattice sites** — which is what allows shape, and shape is part of the mechanism, because interfacial tension is a property of a surface. That is not "a Cell with more properties." It is a different ontology, requiring entity identity shared across sites, entity volume, boundary, connectedness, shape, interfacial energy, and splitting and merging constraints.

> **Do not add many-sites-per-entity merely to rescue this Lab.** Record it as a platform boundary until another strong Lab independently demands it. That is exactly what the sixty-Lab exercise is for, and it is a DEC-24 expenditure of the largest kind.

**Cell state.** *Persistent:* cell type identity, adhesion parameters, motility. *Unrepresentable at one-cell-per-site:* shape, surface, interfacial energy.

**Assessment.** *(judgment, no standing)* **Weak as research; excellent as an architecture boundary test.** The outcome is predicted by a sixty-year-old thermodynamic argument, the canonical model is a widely-used lattice model, and the honest representation does not fit SCR's Cell. Its value is that it forces the platform to say *the interesting question is only the kinetics, and the architecture may not support the honest representation* — which is a verdict the fit review must be capable of reaching (§30, closing).

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Output risk policy** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | The whole family. **Non-claims paragraphs are insufficient where the subject itself carries clinical weight.** |
| **Many-sites-per-entity** — one domain object occupying a variable connected region | **DEC-24** | 27. Record as a boundary; do not spend to rescue one weak Lab. |
| **Growing Worlds** — participant count changing during a Run | **DEC-24** | 20. Prefer activating inactive sites or coordinate remapping over dynamic allocation. |
| **Named geometry families** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | 22. More general and cheaper than "3-D World". |
| **Mechanism identity layers** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | The fingering group (23, 24, 25, and 29 in Family E) |
| **Lattice-artifact control Study** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | 21 (desired), 23 and 25 (numerical). Automatable. |
| **Evidence standing metadata** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | The whole family; decides how Search ranks mechanisms. |
| **"Cell" disambiguation in Lab writing** | **§5, LAB-3** | 24, 26, 27. Semantic clarity is an architectural principle, not a style preference. |
| **Mechanism discrimination beyond morphology** | *unregistered — [triaged](../../04-decisions/proposed-from-the-lab-catalog.md)* | 20. Two mechanisms producing indistinguishable spots are not equivalent. |

### Cross-Lab mechanism families in this batch

- **Excitable / refractory** — 21, 22, plus 11 (convection) and 35 (catalytic surfaces). **Entry 21 is the proposed reference family.**
- **Diffusion-limited fingering** — 23, 24, 25, plus 29 and 34 in Family E. *Same mechanism family, not same mechanism.*
- **Short activation / long inhibition** — 20, plus 12 (vegetation banding).
- **Spatial sanctuary** — 23, 25, 26. A population survives treatment because of where it is.

### Build priority within the family

**Tier A.** **Excitable Media (21)** — flagship and reference mechanism family. **Biological Pattern Formation (20)** — flagship corpus Lab and the natural benchmark for *same picture, different mechanism*. **Biofilm Morphology (25)** — top calibration candidate, cheap controlled experiment. **Wound Healing (24)** — calibration, good early build.

**Tier B.** **Cortical Spreading Depression (22)** — build paired with 21, not alone. **Avascular Tumour Growth (23)** — legitimate, not early, not public-facing.

**Tier C — architecture value exceeds domain value.** **Cell Sorting (27)** — the many-sites-per-entity boundary. **Immune Response (26)** — narrow to granuloma formation, build late.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** Kondo, S. & Asai, R. (1995). A reaction–diffusion wave on the skin of the marine angelfish *Pomacanthus*. *Nature* **376**, 765–768. *(Before this there was no conclusive experimental evidence for a Turing system in biology; a Turing-based simulation correctly predicted future stripe patterns.)*
2. **[V]** Greenberg, J. M. & Hastings, S. P. (1978). Spatial patterns for discrete models of diffusion in excitable media. *SIAM Journal on Applied Mathematics* **34**, 515–523.
3. **[V]** Leão, A. A. P. (1944). Spreading depression of activity in the cerebral cortex. *Journal of Neurophysiology* **7**(6), 359. *(Depression of EEG activity moving through rabbit cortex at 3–6 mm/min.)*
4. **[V]** Waclaw, B., Bozic, I., Pittman, M. E. et al. (2015). A spatial model predicts that dispersal and cell turnover **limit** intratumour heterogeneity. *Nature* **525**, 261–264. *(Large tumours are strikingly homogeneous; short-range dispersal and turnover cause rapid mixing, letting a small selective advantage dominate. The first pass had this reversed.)*
5. **[V]** Hallatschek, O., Hersen, P., Ramanathan, S. & Nelson, D. R. (2007). Genetic drift at expanding frontiers promotes gene segregation. *PNAS* **104**, 19926–19930. *(Sector-like regions with fractal boundaries from fluctuations in a thin band of pioneers; observed in E. coli and yeast.)*
6. **[V]** Graner, F. & Glazier, J. A. (1992). Simulation of biological cell sorting using a two-dimensional extended Potts model. *Physical Review Letters* **69**, 2013–2016.
7. **[V]** Glazier, J. A. & Graner, F. (1993). Simulation of the differential adhesion driven rearrangement of biological cells. *Physical Review E* **47**(3), 2128–2154. *(Differential adhesion with fluctuations suffices for complete and partial sorting, checkerboard, position reversal, and dispersal.)*
8. **[D]** Lashley, K. S. (1941) — self-charted migraine aura progressing at about 3 mm/min across visual cortex; Milner (1958) connected it to Leão's spreading depression.
9. **[D]** Turing, A. M. (1952). The chemical basis of morphogenesis. *Philosophical Transactions of the Royal Society B* **237**, 37–72.
10. **[D]** Kondo, S. & Miura, T. (2010). Reaction–diffusion model as a framework for understanding biological pattern formation. *Science* **329**. Meinhardt on mollusc shell patterns.
11. **[D]** Wiener & Rosenblueth (1946) on cardiac excitation; FitzHugh–Nagumo; eikonal curvature–speed relation and restitution/alternans theory; Mullins–Sekerka interface stability; Matsushita & Fujikawa and Ben-Jacob on colony morphology diagrams; Segovia-Juárez and Kirschner on agent-based granuloma models; Steinberg's differential adhesion hypothesis and measured tissue surface tensions; zebrafish pigment-cell interaction studies.
12. **[D]** Luo–Rudy lineage of detailed cardiac ionic models; optical mapping of cardiac tissue; the COSBID collaboration on human electrocorticographic recording of spreading depolarization.

---

## Non-claims

This report performs no fit reviews and establishes no fit. **Nothing in this family models any patient, bears on diagnosis, prognosis, device design, drug effect, or therapy, or is suitable for any medical or clinical decision.** Nothing here bears on cancer, arrhythmia, migraine, brain injury, infection, or wound care. Mechanisms these Labs would generate are candidate explanations requiring domain validation in domain tooling (§41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment, carry no standing, and do not promote any entry.
