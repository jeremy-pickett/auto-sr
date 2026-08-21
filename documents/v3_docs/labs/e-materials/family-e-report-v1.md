# Family E — Materials
## Lab Knowledge Report v1

### Corrosion Pitting · Dendritic Solidification · Grain Growth · Fracture Propagation · Sintering · Thin-Film Growth · Battery Dendrite · Catalytic Surface Reaction

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/e-materials/family-e-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family E (entries 28–35)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md`
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 28–35 in `../short-lab-definitions/`
**Responds to:** `../../critiques/SCR_Labs_21-30_Critique_v0.1.md` (28–30), `../../critiques/SCR_Labs_31-40_Critique_v0.1.md` (31–35)
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41–43; F-7, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

## What this family is for

This is where SCR's boundaries stop being theoretical. Family E contains, simultaneously, **the catalog's best calibration Lab and its clearest rejection** — and both are valuable for the same reason.

Four findings run through it, and all four are platform findings rather than materials findings.

### 1. The globally-computed-driver boundary

Fracture gives the cleanest statement in the catalog:

> **The state change is local, but the quantity driving it is not.**

A crack tip advances locally; the stress field deciding whether and where it advances is the solution of a whole-body elasticity problem. The same structure now appears in fracture stress, mycelial flow, pond water level, coastal shadowing, electrochemical potential in battery deposition, and power flow in Family G. Three cases must be separated:

| Case | Meaning | Verdict |
| :--- | :--- | :--- |
| **Local driver** | The Plugin computes what it needs from bounded nearby state | The SCR ideal |
| **Generic global property** | The Reactor computes a subject-neutral quantity — connected components, shortest path, a conserved total, graph degree | May fit, if the helper is generic and fully declared |
| **Domain-defining global solve** | A specialized mathematical solve *is* the mechanism's driver — elasticity, electrostatic potential, Navier–Stokes pressure, power flow | **The local Plugin becomes ceremonial** |

> **A Lab should fail mechanism fit if the domain-defining causal step must be supplied by a specialized global solver and the local Plugin merely consumes its answer.**

That does not forbid interoperating with such solvers. It means the result must not be sold as discovery of a local mechanism.

### 2. Rejection is a first-class outcome

**A catalog in which all sixty Labs eventually become "plausible" is not a scientific catalog. It is a sales deck.**

Standing should eventually admit: *strong fit · plausible fit · conditional fit · boundary case · rejected fit · benchmark only · architecture test only.* **Rejected does not mean delete the document** — it means the Lab established a useful boundary of the platform (§30, closing). Entry 31 may be one of the most important Labs here precisely because its best result is *SCR should not model this mechanism locally.*

### 3. Behaviour-equivalence collapse

Universality means many microscopically different mechanisms produce identical large-scale exponents. That attacks a naive Corpus premise — *different mechanisms produce different measurable behaviours* — because sometimes they do not. A hundred deposition rules may all land in the same class, and a Corpus ranking them separately because their Python differs is presenting distinctions the measured system cannot resolve.

Three layers of mechanism identity are needed:

- **Implementation identity** — these are different Plugins.
- **Mechanism-family identity** — different variants of the same causal structure.
- **Observable-equivalence identity** — under the current Reader set, they cannot be distinguished.

A Study should be able to ask *which mechanism families are distinguishable by these measurements?* and its inverse. **That a practitioner's planned measurement cannot separate their candidates is a genuinely valuable negative result**, not a failure.

### 4. Benchmark leakage

Several canonical mechanisms in this family are almost certainly in foundation-model training data — Potts grain growth, DLA and Eden, classical dendrites, and the ZGB surface-reaction model. If SCR "discovers" them, did the platform infer the mechanism from evidence, or did the model remember the literature?

> **Calibration Labs need blinded benchmark modes.** A benchmark Study must record what Generation received: subject name, known mechanism names, canonical citations, target behaviour only, abstracted measurements, or deliberately disguised vocabulary.

The strong test: **can Generation recover a known mechanism family from behaviour descriptors when the subject name and canonical vocabulary are withheld?** That tests mechanism supply rather than literature recall.

### The anisotropy control Study is mandatory here

Four entries in this family have a headline measurement that is orientation, roughness, branching, or front shape, and **physical anisotropy and numerical anisotropy can look identical** — nowhere more dangerously than in entry 29, where a convincing dendrite may be nothing more than a rendering of the lattice. Rotate the initial condition, repeat on an alternate lattice geometry, vary the neighbourhood, measure orientation bias explicitly.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 28 — Corrosion Pitting

| | |
| :--- | :--- |
| **Role** | Incumbent-assumption challenge |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Does pit interaction systematically bias the extreme-value extrapolation that asset-integrity practice rests on? |
| **World fit** | Good — a surface is a lattice |
| **Mechanism fit** | **Conditional** — see below |
| **Evidence fit** | Good — inspection datasets, laboratory coupons |
| **Question fit** | Narrow and real |
| **Visual credibility** | Class 1 — safety-critical assets |

**The phenomenon.** Stainless steel resists corrosion because a passive oxide film covers it. Pitting is that film failing at a point: the metal beneath dissolves, the local chemistry inside the pit becomes more aggressive, the film cannot re-form, and dissolution accelerates. A pit digs itself deeper. Most pits initiate and die; a few become stable and grow. **Failure is governed by the deepest single pit, not the average corrosion rate.**

**The established shortcut, and it is the method in actual use.** Because failure is governed by the deepest pit, industry fits **extreme-value distributions** to maximum pit depths measured on inspection coupons and extrapolates to the largest pit likely on a much larger structure [11]. Pit depth grows as a power of time. The stability criterion — a pit stays active only if current density times depth exceeds a threshold maintaining the aggressive interior — is well established.

**The pitch, which is unusually concrete and the right way to enter a mature engineering field:**

> **The industrial shortcut assumes pits are independent. Interacting pits may violate that assumption.**

Pits are not independent: an active pit consumes surrounding cathodic capacity and suppresses initiation nearby. That makes the spatial distribution non-random, and extreme-value statistics fitted under an independence assumption is estimating the wrong distribution.

**The fit question, stated as a precondition rather than a hope.** Pit interaction is mediated by electrochemical potential, current distribution, ionic transport, solution chemistry, geometry, and sometimes metallurgy. **If the mechanism of interest is precisely pit interaction, discarding the non-local electrochemistry may discard the thing being studied.** So:

> **Can a bounded local surrogate preserve the population-level interaction effect well enough to test the independence assumption?**

That must be demonstrated against a higher-fidelity or experimental reference **before any inference is drawn.** This is the generic-global-property versus domain-defining-solve question (§1 above), and it is not yet answered.

**On dimensionality.** Do not require 3-D automatically. If the outcome of interest is pit survival and population spacing rather than undercut geometry, a 2-D abstraction may be valid. **Tie dimensionality to the Study question.**

**Cell state.** *Persistent:* metal present or dissolved, passive film integrity, local aggressive-species concentration. *Static:* microstructural susceptibility. *Derived or globally computed:* local current — and which decides the Lab's viability.

**Assessment.** *(judgment, no standing)* **Plausible as a narrow assumption-testing Lab; too risky for predictive positioning.** Nobody replaces extreme-value statistics with a cellular model — but demonstrating, across many candidate interaction mechanisms, that pit interaction biases the extrapolated maximum depth in a particular direction would be useful and needs no claim about any specific structure.

---

## Lab 29 — Dendritic Solidification

| | |
| :--- | :--- |
| **Role** | **Theory anchor / cross-Lab instability reference** — weak research Lab |
| **Standing** | Ungraded; I would grade it **weak for research, strong for reference** |
| **Falsifiable question** | Does grain competition under a fixed thermal gradient produce the measured texture distribution across many nucleation realizations? |
| **World fit** | Good |
| **Mechanism fit** | Good, but **morphology claims are blocked** until lattice controls pass |
| **Evidence fit** | Good — electron backscatter diffraction gives full orientation maps |
| **Question fit** | Narrow; the residual is small |
| **Visual credibility** | Class 2 |

**The phenomenon.** When molten metal freezes the solid does not advance as a flat front. A protrusion into the melt finds cooler, less solute-rich liquid, grows faster, and protrudes more. The front breaks into dendrites with primary arms, side arms, and sidebranches on those. The resulting **microstructure** determines the metal's mechanical properties, and every cast component's properties are set by this process.

**The established shortcut, and it is unusually complete.** Mullins and Sekerka (1964) gave the linear stability analysis of a solidifying interface, balancing the destabilizing diffusion field against stabilizing surface tension [11]. Ivantsov's needle solution leaves a degeneracy that **microscopic solvability** resolves: crystalline anisotropy in surface energy selects a unique tip operating point — without anisotropy there is no dendrite, only unstable fingers [11]. Arm spacing scales with cooling rate through established power laws used in foundry practice. **Phase-field is a strong, validated, quantitative incumbent**, and CA–finite-element grain-structure prediction is already industrial practice [11].

That leaves a small residual, and the brief should say so plainly.

**Irreducible.** Sidebranch statistics — where side arms appear along a primary arm and how their amplitude grows, driven by selective amplification of thermal noise. Arm competition and coarsening. **Grain competition** — neighbouring grains with different orientations grow toward each other and the better-aligned one wins, so which grains dominate a casting is decided by initial nucleation positions and orientations. The columnar-to-equiaxed transition.

**The cross-Lab role, stated with the right strength.** This is the theoretically rigorous physics anchor for the **diffusion-limited fingering family** that appears in tumour margins (23), wound edges (24), and biofilms (25). But the claim must be **mechanism-family language, not identity**: biological fronts include mechanics, motility, growth, and signalling absent from solidification. The Lab serves as the physics anchor for one abstract instability family **without implying that tumour or wound behaviour is Mullins–Sekerka in a literal sense.**

**The lattice-anisotropy hazard is at its worst here.** Real dendrites grow along preferred crystal directions; a square lattice also has preferred directions; the two are easy to confuse and a lattice model can produce four-fold dendrites that merely display the grid. Grain orientation makes it worse — a grain at 30° to the lattice must not grow differently from an aligned one, and on a naive lattice it will.

> **This Lab is forbidden from making morphology claims until it passes explicit rotation and alternate-lattice controls.**

**Cell state.** *Persistent:* solid fraction, crystallographic orientation. *Derived or field:* temperature, solute concentration.

**Assessment.** *(judgment, no standing)* **Weak research Lab; strong cross-Lab theory and reference Lab.** The theory covers the main questions, phase-field is a strong incumbent, and CA solidification is already industrial practice — no methodological novelty. Its value is as the rigorous anchor that keeps the biological fingering Labs honest about what they are and are not claiming.

---

## Lab 30 — Grain Growth

| | |
| :--- | :--- |
| **Role** | **Exact-answer platform calibration Lab.** Its primary customer is SCR itself. |
| **Standing** | Ungraded; **weak as research, excellent as calibration** — and the distinction should be preserved |
| **Falsifiable question** | Does a generated mechanism satisfy the von Neumann–Mullins relation across many grains, and where exactly does a failing candidate violate it? |
| **World fit** | Excellent |
| **Mechanism fit** | Excellent |
| **Evidence fit** | **Law-level correctness** — the only entry in this catalog with one |
| **Question fit** | Platform, not metallurgy |
| **Visual credibility** | Class 3 |

**The phenomenon.** A metal is a mosaic of crystal grains meeting at boundaries that carry energy. Heat it and boundaries move: large grains eat small ones, small grains vanish, mean size grows. Grain size controls strength through Hall–Petch, so controlling it thermally is a routine industrial lever. Occasionally a few grains grow enormously while the rest stay small — **abnormal grain growth**, which ruins properties and is not fully predictable.

**This is the most rigorously reduced domain in the catalog, and that is the point.**

**The exact law.** Over fifty years ago von Neumann derived an exact formula for the growth rate of a cell in a two-dimensional cellular structure, from the relation between wall velocity and mean curvature, the fact that three walls meet at 120°, and basic topology — the basis of modern grain growth theory. **MacPherson and Srolovitz (2007)** extended it exactly into three and higher dimensions, relating an individual grain's rate of volume change to its mean width and total triple-line length in an isotropic polycrystal [1].

**The canonical lattice model** is Monte Carlo Potts, introduced for grain growth in the mid-1980s: sites carry an orientation label, boundary energy is counted between unlike neighbours, sites flip by Metropolis dynamics [11]. It reproduces the growth exponent, the self-similar size distribution, and the topological statistics. Textbook, cellular, and forty years old.

**Reducible.** Individual grain evolution — exactly, from topology alone. Mean size growth exponent. Steady-state size distribution. Topological statistics. Zener limiting size under particle pinning. **Close to a complete answer for normal grain growth.**

**Irreducible.** Abnormal grain growth — which grain escapes, and whether it happens at all, is a symmetry-breaking event triggered by local conditions and not predicted by mean-field theory. Anisotropic boundary properties, where energy and mobility depend on misorientation and the clean topological laws stop applying. Texture evolution. Pinning breakdown as particles coarsen.

**Why this is the catalog's most important calibration Lab.** A domain with an exact relation gives SCR something almost nothing else does: **a hard answer the platform is not allowed to negotiate with.** That enables platform Studies no other Lab supports — does Generation rediscover mechanism families consistent with the law? How often does semantic intent produce code that violates it? Do repair passes improve compliance? Does the Corpus learn that some mechanism families systematically fail? Does Search rank law-consistent mechanisms above superficially similar wrong ones? Can a Reader detect exactly *where* a candidate violates the expected relation?

**This is not metallurgy research. It is instrument calibration**, and its research weakness is irrelevant to that role.

**Two cautions the Lab must respect.**

*The law is not automatically a per-step prediction.* Von Neumann–Mullins is a **continuous-time area-change relation under specific ideal assumptions**, not a literal expected delta per arbitrary Reactor step. It can still be used as an exact relationship after mapping Reactor time and scale appropriately — **and that mapping must itself be tested** before any compliance claim.

*Blinded benchmarking is required.* A foundation model almost certainly knows Potts grain growth. If Generation is prompted with the law, rediscovery proves nothing. The benchmark protocol must define what the model is allowed to know.

**Lattice faceting is a documented artifact with documented fixes** — square-lattice Potts models produce faceted boundaries and can freeze at low simulation temperature. The field solved this in the 1980s with larger neighbourhoods, finite temperature, and triangular lattices. A Lab reproducing the artifact would be reproducing a corrected mistake.

**Cell state.** *Persistent:* orientation label. *Optional static:* pinning-particle flag, stored energy. The smallest state in the catalog — a single integer.

**Assessment.** *(judgment, no standing)* **Build early as a calibration Lab.** There is no serious argument that SCR contributes to normal grain growth, and none is needed. Wildfire tells us whether SCR produces something *plausible*; biofilms whether it produces something *quantitatively comparable to a cheap experiment*; grain growth whether a generated mechanism **obeys a known exact relation.** Those are three different forms of platform validation and this is the only source of the third.

---

## Lab 31 — Fracture Propagation

| | |
| :--- | :--- |
| **Role** | **Boundary-calibration Lab.** Its best result may be *SCR should not model this locally.* |
| **Standing** | Ungraded; I would grade it **weak / rejected for core local-mechanism fit** |
| **Falsifiable question** | Can a local load-transfer surrogate reproduce crack *paths* — not merely avalanche exponents — against a globally solved reference? |
| **World fit** | Good — a lattice looks natural |
| **Mechanism fit** | **Failing.** The domain-defining driver is a global solve. |
| **Evidence fit** | Good in principle |
| **Question fit** | Poor for SCR; excellent for the platform's boundary |
| **Visual credibility** | **Class 1** — safety-critical, and convincing pictures from wrong mechanics |

**The phenomenon.** Load a solid; a crack starts at a flaw; the crack concentrates stress at its own tip so the material there sees far more load than average, and extends — sharpening the concentration further. In a real heterogeneous material it wanders, branches, and sometimes arrests. Acoustic emissions before failure come in bursts with a heavy-tailed size distribution.

**The established shortcut.** Griffith (1921) gave the energy criterion: a crack grows when released elastic energy exceeds the cost of new surface [11]. Linear elastic fracture mechanics is the engineering framework — stress intensity factor against fracture toughness, with handbook solutions and design codes built on it. Crack path in homogeneous isotropic material follows from the principle of local symmetry. Weibull weakest-link statistics give brittle strength distributions.

**The lattice tradition is real.** The **random fuse model** — a lattice of fuses with random thresholds carrying current, burning out one at a time — is the canonical minimal model of disordered fracture, and fiber bundle models are its mean-field cousin. Both produce avalanche statistics and size effects [11].

**Why this Lab fails, stated precisely.** **Elasticity is not local.** When a crack extends, the stress field changes everywhere in the body — in the quasi-static approximation, instantaneously. (A dynamic fracture model has finite elastic wave propagation; that makes the wording more precise and does not rescue locality.) Load redistributes according to a long-range kernel, not to neighbours.

The random fuse model is instructive precisely here: it is a lattice model, and **each step requires solving a global linear system for the current distribution.** The lattice provides the geometry; the physics is solved globally.

The fit failure is therefore specific, and the distinction matters:

> **Random fuse models are not useless. They are legitimate reduced models. They are simply not an example of the local-Plugin mechanism SCR claims to study, unless the global solve is admitted as part of the mechanism.**

The alternative — a purely local rule where a broken element dumps load on neighbours — inherits the sandpile objection from entry 3: **plausible avalanche exponents can coexist with physically wrong crack paths.** In a domain where engineers make load-bearing decisions, that gap is dangerous, and getting the exponent right does not mean getting the physics right.

**Cell state.** *Persistent:* intact or broken, accumulated damage. *Static:* local strength threshold. *Globally computed:* local stress — which is the entire problem.

**Assessment.** *(judgment, no standing)* **Grade weak or rejected for core local-mechanism fit; keep prominently as a boundary-calibration Lab.** This is the strongest rejection case in the catalog and one of its most valuable documents. It acknowledges a famous lattice tradition, acknowledges that the lattice reproduces plausible statistics, and then shows the load redistribution requires a global solve that a neighbour-transfer surrogate does not physically replicate. **That is exactly what a fit review is for.**

There is one legitimate narrow use: a **demonstrator of the failure mode**, showing side by side that a local transfer rule and a globally-solved model produce similar avalanche statistics and different crack paths. That is a real methodological result and it argues for SCR's discipline rather than its reach.

---

## Lab 32 — Sintering

| | |
| :--- | :--- |
| **Role** | Shrinkage and deformation architecture probe |
| **Standing** | Ungraded; **weak-to-plausible** |
| **Falsifiable question** | Which local densification rules produce pore stranding at the observed rate in a disordered packing, at fixed geometry? |
| **World fit** | **Failing for the commercial question** — the World shrinks |
| **Mechanism fit** | Conditional; warping likely needs a continuum solve |
| **Evidence fit** | Good for density, poor for distortion without mechanics |
| **Question fit** | Real but architecturally blocked |
| **Visual credibility** | Class 1 if framed as manufacturing prediction |

**The phenomenon.** Press a powder and heat it below melting. Particles bond where they touch, necks thicken, pores shrink and round, and the compact densifies — shrinking, sometimes by a fifth of its linear dimension. This is how most ceramics and powder-metallurgy parts are made, and it is the consolidation step in metal 3-D printing. The failure modes are geometric: pores that detach from grain boundaries become nearly impossible to remove, and regions densifying at different rates warp the part.

**The established shortcut.** Classical theory gives scaling laws — neck growth follows a power law whose exponent identifies the dominant diffusion path, Herring scaling relates rates across particle sizes, and Coble's analysis gives intermediate and final stage densification kinetics [11]. Ashby-style sintering maps identify which mechanism dominates. **Pore–boundary separation has a classical criterion**: a pore is dragged along only if the boundary moves slowly enough, and past a critical grain growth rate it strands.

**Irreducible.** Real disordered packing, where which pores close depends on specific local coordination — a large pore surrounded by many particles is far more stable than average theory suggests. Pore stranding realization. Coupled grain growth and densification, which compete, and where the trajectory through that competition is why sintering *schedules* rather than temperatures are the industrial control.

**Two nested fit failures, and the second is the one the first pass underplayed.**

1. **Fixed geometry cannot represent shrinkage.** A lattice with fixed spacing cannot represent a body contracting by tens of percent, except indirectly through density — which discards the warping question.
2. **Warping itself may require a continuum mechanical solve.** Differential densification generates stresses that distort the part. If SCR cannot represent deformation and stress honestly, this Lab inherits entry 31's global-field problem.

**A more defensible early scope**, sacrificing commercial glamour for fit:

> **Pore survival, stranding, and local densification in fixed geometry** — rather than final-part distortion.

**On the geometry-change taxonomy.** The catalog now contains five distinct kinds, which must not be conflated: *occupancy change in fixed geometry* (easy); *topology change* (entry 18); *population growth* (entry 20); *physical contraction and expansion* (this Lab); and *deformation under force* (entries 31, 32, and possibly crowd compression). **Do not add deformable Worlds because Sintering wants them.** Record physical deformation as a separate unsupported capability until several high-value Labs justify it — a DEC-24 expenditure of the largest kind.

**Cell state.** *Persistent:* material or pore state, grain orientation, vacancy concentration. *Derived:* local curvature, coordination.

**Assessment.** *(judgment, no standing)* **Weak-to-plausible; keep as a shrinkage and deformation architecture probe. Do not build early.** The commercially live thread is real — additive manufacturing revived sintering as an expensive unsolved problem, currently handled by empirical shape compensation — but it sits behind two architecture questions the platform has not answered.

---

## Lab 33 — Thin-Film Growth

| | |
| :--- | :--- |
| **Role** | **Strong platform and intellectual Lab**; plausible domain Lab |
| **Standing** | Ungraded; I would grade it **strong for the platform question** |
| **Falsifiable question** | Which local growth mechanism families map to which universality classes, and which collapse into the same observable class? |
| **World fit** | **Excellent — the lattice is the physics.** Atoms occupy discrete sites. |
| **Mechanism fit** | Excellent |
| **Evidence fit** | Good — scanning probe and X-ray reflectivity roughness measurements |
| **Question fit** | Platform-shaped, and genuinely unclaimed |
| **Visual credibility** | Class 3 |

**The phenomenon.** Deposit atoms onto a surface. Each lands, hops if it has thermal energy, and sticks — usually beside an atom already there. Repeat a few billion times and you have a film. Whether it is smooth or rough, continuous or full of pinholes, and whether it grows layer-by-layer or as islands that merge, determines its usefulness.

**The established shortcut, and it is the largest in the catalog.** A growing surface's roughness increases as a power law and saturates at a size-dependent value, with exponents tied by Family–Vicsek scaling. **Kardar, Parisi and Zhang (1986)** wrote the continuum equation for an interface with lateral growth and, via renormalization-group techniques and mappings to Burgers' equation and directed polymers, obtained the exact scaling exponents in one dimension [2]. Ballistic deposition and Eden fall in the KPZ class; deposition with surface relaxation falls in a different linear class. Growth-mode selection follows from surface energies. **Lattice models are the field's standard tool and always have been.**

**The universality problem, which is this Lab's whole intellectual content.** If a mechanism belongs to a known class, its exponents were fixed before it ran. **A hundred distinct mechanisms give the same number.** That is a direct challenge to the premise that different mechanisms are worth cataloguing separately.

**The inversion, and it is genuinely Corpus-shaped.** The interesting question is not *what are the exponents* but:

> **Which mechanism families map to which universality classes, and where are the boundaries between classes?**

No individual investigator does this systematically — it is not a paper. A corpus does it as a byproduct of existing, and the resulting map has real content: knowing a proposed rule family is KPZ tells an experimentalist their measured exponent cannot discriminate among their candidates. **That is a valuable negative result.**

**Correction from the first pass.** "Which universality class a mechanism belongs to" is not inherently computationally irreducible in the strongest sense — renormalization-group reasoning, symmetries, conservation laws, and continuum mappings can sometimes classify a model without brute-force simulation. The safer formulation:

> **For many novel discrete rules, classification is established empirically or through nontrivial analysis, and automated simulation can supply that evidence cheaply.**

**A Reader-validation warning that must not be skipped.** Measuring exponents reliably requires severe finite-size and crossover discipline. **A naive Reader will confidently classify the wrong universality class.** This Lab needs unusually rigorous Reader validation before any classification claim, and the crossover length and time — which are non-universal and mechanism-specific — are themselves what an experimentalist actually measures.

**Cell state.** *Persistent:* column height, occupancy. *Optional:* species, mobility state. A solid-on-solid model needs one integer per column.

**Assessment.** *(judgment, no standing)* **Strong platform Lab, plausible domain Lab. Keep.** This is where **observable-equivalence identity** should be formalized, and the concept matters far outside materials — biological patterning, epidemic curves, network propagation, and security alert cascades all have domains where multiple mechanisms generate the same coarse statistic.

---

## Lab 34 — Battery Dendrite

| | |
| :--- | :--- |
| **Role** | High-value later research Lab — **conditional on mechanism-fit validation** |
| **Standing** | Ungraded; **the strongest Family E research opportunity**, conditionally |
| **Falsifiable question** | Do local interphase cracking-and-repair rules reproduce the observed transition from mossy to dendritic growth and the cycle-to-failure distribution? |
| **World fit** | Good |
| **Mechanism fit** | **Conditional — possibly the same fatal issue as entry 31** |
| **Evidence fit** | Good — operando tomography, cryo-electron microscopy, cycling statistics |
| **Question fit** | Excellent |
| **Visual credibility** | **Class 1** — safety-critical |

**The phenomenon.** Charging moves lithium to the negative electrode. Too fast, too cold, or too full, and lithium plates as metal instead of intercalating — and metal deposition from solution is unstable in the familiar way: a bump reaches fresher electrolyte, grows faster, becomes a spike. Grown far enough it bridges to the other electrode and short-circuits the cell. It is also the barrier to lithium-metal anodes, which would substantially raise energy density and are not commercial precisely because of this.

**The established shortcut — and it does not apply to the case anyone cares about.** In a dilute binary electrolyte at high current, ion concentration at the electrode falls to zero after **Sand's time**, after which the interface becomes unstable; Chazalviel's model connected concentration depletion, space charge, and dendrite initiation [11]. Below the limiting current, growth should be stable and mossy.

But commercial electrolytes are **concentrated**, not dilute, and the lithium surface carries a **solid electrolyte interphase** — a passivating film from electrolyte decomposition whose mechanical and transport properties largely control where deposition occurs. Real deposits are frequently mossy, whisker-like, or dead-lithium fragments. **Sand's time predicts onset in conditions no commercial cell operates in.** That mismatch is the opening.

**Irreducible.** Where nucleation happens, at defects and cracks in a heterogeneous film that itself formed stochastically. **The film's feedback loop** — deposition strains and cracks the interphase; cracks expose fresh lithium; fresh lithium reacts and reforms film, consuming electrolyte; the reformed film is heterogeneous. A self-modifying substrate with memory across hundreds of cycles. Cycle-to-cycle accumulation, where dendrites that dissolve on discharge leave disconnected dead lithium and roughened surfaces that seed the next cycle worse.

**The condition this Lab must meet before it means anything.** The global electric and potential field is not a side issue — it may be entry 31's fatal problem in another costume. The first pass identified this and then stayed optimistic. That optimism needs a formal requirement:

> **The Lab survives only if a local or generic-field surrogate can reproduce the cycling statistics of interest against a trusted reference.** Otherwise the local mechanism is decorating an electrochemical solve.

**Two scope boundaries.** *Solid-state penetration* couples to fracture mechanics and inherits entry 31's problem compounded — a separate later sub-Lab, not part of a first build. *Battery-fire language stays downstream of scope*: this Lab studies deposition morphology and cycling accumulation, **not thermal runaway prediction.**

**Phase schedule.** Charge and discharge are not one mechanism time-reversed — deposition leaves dead lithium and surface damage that dissolution does not undo. The Run contains **named process phases with different allowed transitions**, which is the same structure as wet/dry seasons, heat/cool cycles, and attacker/defender turns. A Plugin must not own a clock, but a World or Study may legitimately declare *100 charge steps, then 100 discharge steps, repeat*, each phase exposing different capabilities while remaining deterministic. **Phase schedule belongs in the temporal-semantics discussion rather than being treated as delay or asynchrony.**

**Cell state.** *Persistent:* deposited lithium, interphase film thickness and integrity, accumulated damage. *Derived or globally computed:* local overpotential, ion concentration.

**Assessment.** *(judgment, no standing)* **Promising, conditional on mechanism-fit validation. A high-value later Lab, not an early architecture anchor.** The distinguishing feature is a mature theory covering conditions nobody operates in alongside an urgent funded problem in the regime that matters — exactly where cheap mechanism supply has room. Failure here is a **distribution over hundreds of cycles** with the safety-relevant quantity in the tail, which is Study-shaped and suits F-14 directly.

---

## Lab 35 — Catalytic Surface Reaction

| | |
| :--- | :--- |
| **Role** | **Correctness and fit calibration Lab**; moderate research opportunity |
| **Standing** | Ungraded; **excellent for calibration** |
| **Falsifiable question** | Asked for "a surface reaction where one species needs two adjacent free sites", does Generation produce something with the ZGB phase structure — with the canonical vocabulary withheld? |
| **World fit** | **The cleanest correspondence in the catalog** — a lattice site is an adsorption site |
| **Mechanism fit** | Excellent |
| **Evidence fit** | Strong — an exact published phase diagram, plus PEEM movies |
| **Question fit** | Platform-shaped; research headroom in small particles |
| **Visual credibility** | Class 3 |

**The phenomenon.** A catalyst lets reactants adsorb, meet, react, and leave. On platinum oxidizing carbon monoxide — the catalytic converter reaction — CO adsorbs on one site, oxygen adsorbs by splitting across **two adjacent** empty sites, and adjacent CO and O combine and desorb, freeing both. That asymmetry makes the surface competitive: too much CO and it poisons, since oxygen cannot find adjacent pairs. Under the right conditions it does not settle at all, producing travelling waves, rotating spirals, and global rate oscillations — imaged in real time on real platinum, work recognized by the 2007 Nobel Prize in Chemistry for the study of chemical processes on solid surfaces.

**The established shortcut, and it is a strong correctness target.** **Ziff, Gulari and Barshad (1986)** wrote down exactly those rules with a single parameter — the CO fraction in the gas — and found the adsorbed species undergo **both first- and second-order kinetic phase transitions** corresponding to catalyst poisoning [3]. The ZGB model is a genuinely important object in statistical physics; its continuous transition belongs to the directed percolation universality class, and it became a standard test case for absorbing-state transitions. Mean-field Langmuir–Hinshelwood kinetics covers the rest.

**Correction from the first pass.** "The rules are the chemistry" is slightly too strong — they are a deliberately reduced representation, and real rates depend on activation barriers, site heterogeneity, temperature, surface reconstruction, and diffusion. The point survives as:

> **The discrete local-rule abstraction corresponds unusually directly to the physical events being modelled.**

**Irreducible.** Pattern selection among spirals, targets, standing waves, and turbulent regimes. Poisoning as an **absorbing state** — once poisoned the surface does not spontaneously recover, so the system has irreversible history, and near the transition a specific run's outcome is genuinely undetermined. Real catalysts are **nanoparticles** with facets, edges, and steps rather than infinite crystals, and at a few hundred surface sites mean-field kinetics fails and the reaction can switch state from fluctuation alone.

**Benchmark leakage applies with full force.** A foundation model almost certainly knows ZGB. **A calibration Study must blind the canonical names and rules if the goal is rediscovery**, or the test measures literature recall rather than mechanism supply.

**Geometry is chemistry here.** The honest lattice is the crystallography — square for one platinum face, hexagonal for another — and the choice matters, because the two-adjacent-site requirement for oxygen depends on the neighbour structure. **Changing the lattice here changes the chemistry, correctly.**

**Cell state.** *Persistent:* occupancy (empty / CO / O), surface reconstruction state for the oscillating case. *Optional static:* site-type label for the nanoparticle question. The smallest state in the catalog alongside entry 30.

**Assessment.** *(judgment, no standing)* **Excellent correctness and fit calibration Lab; moderate research opportunity in heterogeneous small-particle regimes.** If a fit review wants a worked example of what a *good* World fit looks like (§30.2), this is it — a Cell is an adsorption site, and an adsorption site is a real, discrete, countable thing. One caution beyond leakage: the beautiful ultra-high-vacuum experiments sit far from operating pressures, and the **pressure gap** is a known, serious issue in translating those results.

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Globally-computed drivers** — local / generic global property / domain-defining solve | *unregistered* — **strongest new DEC candidate from this batch** | 31 (decisive), 34 (conditional), 28 (open) |
| **Standing vocabulary admitting rejection** | **DEC-15** | 31. "Rejected" must not mean "deleted". |
| **Observable-equivalence identity** — behavioural equivalence under a specified measurement set | *unregistered* | 33 |
| **Blinded benchmark modes** — what Generation was allowed to know | *unregistered* | 30, 35. Without it, calibration measures literature recall. |
| **Geometry-change taxonomy** — occupancy / topology / population / contraction / deformation | **DEC-24** | 32. Do not spend on deformable Worlds for one Lab. |
| **Phase schedule** in temporal semantics | **DEC-3** | 34. Declared phases, Reactor-owned, deterministic. |
| **Anisotropy control Study** | *unregistered* | 29 (mandatory before morphology claims), 30 (documented faceting) |
| **Reader validation rigour** — finite-size and crossover discipline | *unregistered* | 33. A naive Reader will misclassify confidently. |
| **Mechanism-family language, not identity** | *unregistered* | 29 as the physics anchor for the fingering family |

### Three kinds of platform validation, now complete

| Level | Lab | What it proves |
| :--- | :--- | :--- |
| Behavioural plausibility | Wildfire (1) | The output resembles the subject |
| Experimental agreement | Biofilm (25), Wound healing (24) | It matches a cheap controlled measurement |
| **Law-level correctness** | **Grain growth (30)** | **A generated mechanism obeys a known exact relation** |

Family E supplies the third, and it is the only source of it in the catalog.

### Build priority within the family

**Build early — for the platform, not the domain.** **Grain Growth (30)** — the exact-answer calibration anchor. **Catalytic Surface Reaction (35)** — correctness calibration with the cleanest World fit.

**Strong platform value.** **Thin-Film Growth (33)** — where observable equivalence gets formalized.

**Conditional / later.** **Battery Dendrite (34)** — highest research value, blocked on a mechanism-fit demonstration. **Corrosion Pitting (28)** — narrow assumption test, same precondition.

**Reference and boundary.** **Dendritic Solidification (29)** — the theory anchor for the fingering family. **Fracture Propagation (31)** — the catalog's clearest rejection, and one of its most valuable documents. **Sintering (32)** — architecture probe, do not build early.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** MacPherson, R. D. & Srolovitz, D. J. (2007). The von Neumann relation generalized to coarsening of three-dimensional microstructures. *Nature* **446**, 1053–1055. *(Exact 3-D relation between a grain's rate of volume change, its mean width, and total triple-line length, for isotropic boundaries. Extends von Neumann's exact 2-D result of ~50 years earlier.)*
2. **[V]** Kardar, M., Parisi, G. & Zhang, Y.-C. (1986). Dynamic scaling of growing interfaces. *Physical Review Letters* **56**, 889. *(Renormalization-group treatment with mappings to Burgers' equation and directed polymers; exact scaling exponents in one dimension.)*
3. **[V]** Ziff, R. M., Gulari, E. & Barshad, Y. (1986). Kinetic phase transitions in an irreversible surface-reaction model. *Physical Review Letters* **56**, 2553–2556. *(CO/O₂ on a catalyst surface; both first- and second-order kinetic phase transitions corresponding to poisoning.)*
4. **[D]** von Neumann, J. (1952) and Mullins, W. W. (1956) — the exact two-dimensional grain area-change relation.
5. **[D]** Anderson, M. P., Srolovitz, D. J., Grest, G. S. & Sahni, P. S. (1984 onward) — Monte Carlo Potts model for grain growth.
6. **[D]** Mullins, W. W. & Sekerka, R. F. (1964). Stability of a planar interface during solidification of a dilute binary alloy. *Journal of Applied Physics* **35**, 444.
7. **[D]** Griffith, A. A. (1921) — the energy criterion for crack growth.
8. **[D]** Karma, A. & Rappel, W.-J. (late 1990s) — quantitative phase-field simulation of dendritic growth.
9. **[D]** Chazalviel, J.-N. (1990) — concentration depletion, space charge, and dendrite initiation; Sand's time for the dilute limit.
10. **[D]** Ertl, G. — Nobel Prize in Chemistry 2007 for studies of chemical processes on solid surfaces; PEEM imaging of spiral and target patterns on Pt.
11. **[D]** Extreme-value statistics for maximum pit depth in asset-integrity practice; pit stability criterion; Ivantsov needle solution and microscopic solvability; primary and secondary dendrite arm spacing correlations; CA–finite-element casting grain-structure prediction; random fuse and fiber bundle models; Weibull weakest-link strength statistics; Coble and Herring sintering analyses; Ashby sintering maps; pore–boundary separation criterion; Family–Vicsek scaling; Zener pinning; Hall–Petch.

---

## Non-claims

This report performs no fit reviews and establishes no fit. Nothing here predicts microstructure, corrosion, fracture, densification, film properties, battery behaviour, or catalyst performance in any real material, component, cell, or process. **Nothing here bears on structural integrity, asset inspection, battery safety, thermal runaway, or any engineering or safety decision** (§41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment, carry no standing, and do not promote any entry.
