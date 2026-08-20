# Semantic Cellular Ruliology 3.x
## Critique of Lab Knowledge Briefs 21–30
### Excitable Media · Cortical Spreading Depression · Avascular Tumor Growth · Wound Healing · Biofilm Morphology · Immune Response · Cell Sorting/Tissue Boundary · Corrosion Pitting · Dendritic Solidification · Grain Growth

**Status:** family critique of first-pass Lab Knowledge Briefs  
**Scope:** Labs 21–30  
**Intent:** critique these Labs as a connected stress test of SCR, not as finished domain papers or completed fit reviews.

---

## Executive assessment

Labs 21–30 are the strongest batch so far for answering a question that has hovered over the entire catalog:

> **What is SCR actually good at when the field already has excellent models?**

This set contains several domains where cellular, agent-based, Potts, reaction–diffusion, or phase-field models are already canonical. That could have made the whole batch redundant.

Instead, the briefs repeatedly find a narrower and more defensible role:

- not “invent the idea of modeling this spatially”;
- not “replace the mature simulator”;
- not “predict a patient, tissue, casting, or component”;
- but **systematically explore mechanism families, compare them under one evidence protocol, retain failures, and identify cross-domain structural similarities.**

That is a much stronger position.

This batch also produces the cleanest examples yet of three different kinds of Lab value:

1. **Flagship mechanism Lab** — Excitable Media.
2. **Controlled experimental calibration Lab** — Biofilm Morphology, Wound Healing.
3. **Exact-answer platform calibration Lab** — Grain Growth.

Grain Growth is especially important. Wildfire can tell us whether SCR produces something plausible. Biofilms can tell us whether it produces something quantitatively comparable to a cheap experiment. Grain growth can tell us whether a generated mechanism obeys a known exact relation. Those are three different forms of platform validation, and the distinction is valuable.

The batch also sharpens several architectural problems:

- a Cell may represent a fixed site while the domain contains moving biological cells;
- one biological entity may occupy many lattice sites;
- a World may need to grow during a Run;
- geometry may be a folded manifold rather than a flat grid;
- physical anisotropy can be indistinguishable from lattice anisotropy;
- hidden state may have clinical consequence;
- global fields and long-range coupling can quietly become the real mechanism;
- highly persuasive medical and engineering visuals create unusually severe credibility risks.

The strongest entries in this batch are not necessarily the most commercially obvious ones. Excitable Media and Biofilm Morphology are excellent. Grain Growth may be even more important to SCR despite being weak as a research opportunity. Tumor Growth and Corrosion Pitting have interesting questions but dangerous abstraction and credibility gaps. Immune Response and Cell Sorting are useful largely because they reveal where the platform should say “not yet” or “not this way.”

---

# 1. This batch separates three kinds of correctness

The first twenty Labs mostly talked about fit and validation.

Labs 21–30 suggest SCR needs a more explicit hierarchy.

## Behavioral plausibility

Does the mechanism produce a pattern or trajectory resembling the domain?

Wildfire is an example.

## Experimental agreement

Does it reproduce measured quantities from a controlled or observational reference?

Biofilm colony morphology and wound-healing time-lapse data are examples.

## Law-level correctness

Does it satisfy a known analytic relation that must hold?

Grain Growth is the clearest example.

These should not be treated as equivalent evidence.

A beautiful tumor spheroid may have behavioral plausibility.

A biofilm Run matching branch spacing and sector statistics has experimental agreement.

A grain-growth mechanism satisfying von Neumann–Mullins across many grains has law-level correctness.

Recommendation:

> **Lab standing should eventually record what level of external check is available.**

This will matter enormously when Search ranks mechanisms.

---

# 2. Grain Growth may be the most important calibration Lab in the catalog

The brief is right to call it weak research and excellent calibration.

That distinction should be preserved.

A domain with an exact relation gives SCR something most Labs cannot:

> **a hard answer the platform is not allowed to negotiate with.**

That enables unusually strong platform Studies:

- Does Generation rediscover mechanism families consistent with the law?
- How often does semantic intent produce code that violates the law?
- Do repair passes improve law compliance?
- Does the Corpus learn that some mechanism families systematically fail?
- Does Search rank law-consistent mechanisms above superficially similar wrong ones?
- Can a Reader detect exactly how and where a candidate violates the expected relation?

This is not metallurgy research.

It is **instrument calibration**.

That is extremely valuable.

I would formalize at least three Lab roles now:

- **Domain Lab**
- **Benchmark Lab**
- **Calibration Lab**

A Lab may be more than one.

Grain Growth is the strongest Calibration Lab so far.

---

# 3. Excitable Media is the strongest mechanism-family Lab so far

Excitable Media is not merely a good domain fit.

It is a candidate **reference mechanism family** for the whole Corpus.

The same abstract structure recurs in:

- cardiac tissue;
- cortical spreading depression;
- chemical waves;
- calcium signaling;
- possibly cellular convection;
- future electrical/chemical/network propagation Labs.

This is exactly where cross-Lab semantic retrieval should shine.

The Lab therefore has two jobs.

## Domain job

Study initiation, break, anchoring, drift, and destabilization in excitable media.

## Platform job

Provide a canonical cross-domain mechanism family against which Search and Corpus organization can be tested.

That second role may be more strategically important.

Recommendation:

> **Treat Excitable Media as a reference family in the mechanism ontology, not merely Lab #21.**

---

# 4. Cross-Lab “same instability” claims need a stricter standard

This batch repeatedly connects tumor margins, wound edges, biofilms, and dendrites through protrusion-driven fingering.

That is useful.

But the catalog risks using “same mechanism” too loosely.

All four involve a protrusion gaining some advantage, but the actual fields differ:

- oxygen/nutrient diffusion in tumor;
- mechanical and migratory feedback in wound healing;
- nutrient diffusion and motility in biofilms;
- heat/solute diffusion plus surface-energy anisotropy in solidification.

The correct claim may be:

> **They share an abstract instability structure.**

That is weaker and better than saying they are literally the same mechanism.

SCR needs vocabulary for this.

Possible levels:

- **Same mechanism** — equivalent local causal structure.
- **Same mechanism family** — shared abstract interaction pattern with different state meanings.
- **Same behavior family** — similar outcome without demonstrated causal equivalence.

This distinction will prevent cross-Lab retrieval from turning into metaphor matching.

---

# 5. Medical Labs require a stronger trust boundary than ordinary non-claims

Labs 21–27 repeatedly warn about clinical over-reading.

That is correct, but the current “Non-claims” section may eventually be insufficient.

A rendered arrhythmia, tumor, migraine wave, immune lesion, or wound is not neutral.

Users will infer clinical significance because the subject itself carries it.

The platform should eventually support a **Lab credibility class** or similar policy surface.

For medical Labs, that might control:

- mandatory labeling;
- export/report language;
- whether patient-specific inputs are accepted;
- whether real clinical units are displayed;
- whether marketing screenshots can appear without context;
- whether a generated Study can use words such as “treatment,” “response,” “risk,” or “prediction.”

This is not about hiding capabilities.

It is about preventing the View layer from silently upgrading a mechanism experiment into a medical claim.

The medical batch is where that requirement becomes unavoidable.

---

# 6. “Cell” now has three meanings and the architecture must survive them

Family D exposes a naming collision that the core docs already anticipated.

There are at least three concepts:

### SCR Cell
The platform's bounded state-bearing unit.

### Biological cell
An actual moving/deforming organismal unit.

### Lattice site
A fixed spatial location that may contain a biological cell or part of one.

These are not equivalent.

Examples:

- Immune Response: biological immune cells move between SCR lattice sites.
- Cell Sorting: one biological cell may occupy many lattice sites.
- Wound Healing: a site might represent occupancy, but the biology cares about a moving cell sheet.
- Tumor Growth: one site may represent one cell, tissue volume, or occupancy state depending on resolution.

The platform does not need to abandon “Cell.”

But every Lab should state explicitly:

> **What does an SCR Cell correspond to in this Lab?**

And when the domain itself uses the word cell, documentation must disambiguate relentlessly.

This is not cosmetic.

Semantic clarity is one of SCR's architectural principles.

---

# 7. Many-sites-per-entity is a real boundary

Cell Sorting raises a platform capability not encountered cleanly before:

> **one domain object occupies a variable connected region of World state.**

That is how Cellular Potts models represent deformable biological cells.

This is not the same as a Cell having more properties.

It is a different ontology.

If SCR supports it, the platform needs concepts such as:

- entity identity shared across sites;
- entity volume/area;
- entity boundary;
- connectedness;
- shape;
- interfacial energy;
- splitting/merging constraints.

That could massively expand scope.

The brief is right to treat this as an architectural probe rather than silently bending the existing Cell abstraction.

Recommendation:

> **Do not add many-sites-per-entity merely to rescue Cell Sorting. Record it as a platform boundary until another strong Lab independently demands it.**

That is exactly what the sixty-Lab exercise is for.

---

# 8. Growing Worlds are now a concrete requirement candidate

Biological Pattern Formation already raised growing domains.

This batch reinforces it indirectly through tissue growth and morphology.

A World whose number of Cells changes during a Run is not merely dynamic state.

It changes:

- topology;
- identity;
- storage;
- replay;
- Reader comparison;
- coordinate systems;
- future-relevant state;
- Study comparability.

Before SCR supports actual Cell creation/destruction, ask whether growth can be represented by:

- activating previously inactive sites;
- changing occupancy inside a fixed larger World;
- remapping coordinates;
- or true topology growth.

Those options have different architecture costs.

Do not leap to dynamically allocating Cells unless the fixed-capacity representation genuinely fails.

---

# 9. Physical anisotropy versus lattice anisotropy is now a major validation problem

Labs 23, 25, 29, and 30 make this especially sharp.

The platform needs to distinguish:

### Desired anisotropy
Real physical directional behavior.

Examples:

- cardiac fiber conduction;
- crystal growth directions;
- perhaps epithelial packing.

### Numerical anisotropy
Directional behavior caused by grid geometry.

Examples:

- square-grid tumor protrusions;
- axis-aligned biofilm branches;
- faceted Potts grain boundaries.

In Dendritic Solidification the two can look identical.

That is dangerous.

A visually convincing dendrite may be nothing more than a rendering of the lattice.

Recommendation:

> **Any Lab whose headline measurement includes orientation, roughness, branching, or front shape should require a lattice-artifact control Study.**

For example:

- rotate the initial condition relative to the lattice;
- repeat on alternate lattice geometry;
- compare neighborhood definitions;
- measure orientation bias explicitly.

This is exactly the kind of test SCR can automate well.

---

# 10. Excitable Media Lab

## What works

This is close to an ideal SCR Lab.

The state is tiny.

The local interaction is physically real.

The canonical CA precedent is strong.

The reducible boundary is well understood.

The interesting questions are strongly temporal.

The data type—optical mapping movies—matches SCR's stored Run history unusually well.

The cross-Lab mechanism family is excellent.

## Main critique

The clinical framing occasionally approaches “the irreducible half is the half people die of,” which is powerful but risks overselling SCR's relevance to clinical electrophysiology.

The strongest position is narrower:

> **The clinically consequential phenomena are often initiation-, heterogeneity-, and state-dependent, which makes ensemble mechanism exploration scientifically relevant even though SCR is not a clinical model.**

Also, defibrillation is likely too close to a patient/treatment problem for an early Lab scope.

It may be better as background/stress case rather than an initial Study target.

## Architecture pressure

- anisotropic local coupling;
- refractory state;
- precise timing;
- wave history;
- medical credibility.

## Recommendation

**Top-tier flagship and cross-Lab reference family.**

---

# 11. Cortical Spreading Depression Lab

## What works

As a paired Lab with Excitable Media, this is strategically excellent.

It tests whether the platform can transfer a mechanism family across very different physiology.

The folded-cortex issue also creates a genuinely useful Layout challenge.

The hidden metabolic reserve example is strong.

## Main critique

The brief's claim that the reducible core is much weaker than cardiac electrophysiology should be phrased cautiously.

Spreading-depolarization theory is richer than propagation speed alone, and a domain expert may object to the contrast.

The Lab does not need that claim.

Its value survives with:

> **many clinically interesting questions concern initiation, recurrence, geometry, and compromised tissue rather than homogeneous propagation.**

The second issue is geometry.

A folded cortical sheet is naturally a mesh/manifold problem.

Flattening it while preserving adjacency may be possible.

The requirement may therefore be less “3D World” and more:

> **surface topology must be independent of display coordinates.**

That would be a useful general platform property.

## Recommendation

**Keep as a paired cross-Lab mechanism-transfer Lab, not a standalone flagship.**

---

# 12. Avascular Tumor Growth Lab

## What works

The brief is disciplined about scope.

“Avascular” prevents the Lab from becoming a fake whole-cancer simulator.

The size/shape distinction is useful.

Spatial refuges and clonal surfing are genuine ensemble questions.

The laboratory spheroid reference system is strong.

## Main critique

“Everything about tumor size is reducible; everything about shape and composition is not” is too clean.

Even avascular spheroid growth can involve nonlinear coupled nutrient, mechanics, death, and heterogeneity where size dynamics are not trivially Gompertzian.

Treat Gompertz/logistic as empirical reduced descriptions, not complete causal solutions.

The stronger distinction:

> **Bulk size trajectories often admit useful reduced descriptions; spatial morphology and composition require explicitly spatial models.**

That is more defensible.

The second concern is treatment-response language.

Even mechanistic treatment refuges pull the Lab toward clinical interpretation very quickly.

Early scope should probably emphasize morphology and clonal spatial competition, with treatment-response Studies explicitly deferred.

## Recommendation

**Plausible, scientifically legitimate, but not an early public-facing Lab.**

---

# 13. Wound Healing Lab

## What works

This is an excellent calibration/validation Lab.

The reference data type matches SCR perfectly: time-lapse spatial evolution.

The brief correctly focuses on transient geometry rather than closure time.

Leader-cell emergence is a clean mechanism-supply question.

## Main critique

Calling closure rate simply “a Fisher wave speed” risks flattening too much of the scratch-assay literature.

Scratch assays can involve proliferation, collective mechanics, edge effects, density dependence, substrate adhesion, and migration regimes.

The point should be:

> **simple closure-rate summaries are already well modeled and measured; SCR's opening is transient spatial organization.**

That survives without overclaiming the exact reduced law.

Second, leader/follower designation should not automatically be Cell state if leadership is supposed to emerge.

If Generation is testing mechanisms for leader selection, pre-labeling a `leader` state may smuggle the answer into the model.

The deep pass should distinguish:

- observed Reader label “leader-like”;
- internal state variable explicitly proposed by a mechanism;
- imposed Cell type.

## Recommendation

**Strong calibration Lab; good early build candidate.**

---

# 14. Biofilm Morphology Lab

## What works

This may be the strongest controlled-experiment Lab yet.

The experiment is cheap.

The output is directly imageable.

The parameter space is manipulable.

The reference metrics are quantitative.

The cross-Lab fingering connection is useful.

The limiting-regime-versus-middle framing is excellent.

## Main critique

“Biofilm” may be too broad a title for a Lab focused mainly on colony morphology on agar.

A mature Lab should distinguish:

- surface colony growth on nutrient agar;
- attached hydrated biofilms under flow;
- clinical biofilm physiology.

Those are not the same World.

If the current brief is about plate colonies, name that honestly or create subprofiles.

The drug-tolerance angle also moves toward three-dimensional hydrated biofilms where the simple 2D plate abstraction becomes less faithful.

Do not let the excellent plate validation silently authorize clinical biofilm claims.

## Recommendation

**Top-tier calibration candidate, possibly second only to Grain Growth for platform testing.**

---

# 15. Immune Response Lab

## What works

The brief is appropriately skeptical.

The granuloma is a genuine emergent spatial structure.

The sanctuary mechanism creates a useful cross-Lab family with tumors and biofilms.

The vocabulary collision is identified honestly.

## Main critique

This may be too broad even as a title.

“Immune Response” covers an enormous domain, while the only defensible local-spatial case in the brief is essentially:

> **granuloma formation and containment.**

Rename/narrowing would improve credibility immediately.

The second problem is worse: the incumbent is already an agent-based spatial model family built specifically for this question.

SCR's only distinctive contribution would be bulk mechanism generation/corpus comparison, but validation is poor.

That is not enough for early priority.

## Recommendation

**Weak-to-plausible; narrow to Granuloma Formation if retained, and build late.**

---

# 16. Cell Sorting and Tissue Boundary Lab

## What works

This is an excellent negative/calibration case.

The endpoint is reducible.

The incumbent is canonical and mature.

The representation does not fit SCR cleanly.

The Lab therefore tests whether the platform can say:

> **the interesting question is only the kinetics, and the architecture may not support the honest representation.**

That is valuable.

## Main critique

The brief's “outcome is predictable from thermodynamics” should be constrained to systems where differential-interfacial-tension assumptions actually apply.

Modern developmental boundary formation can involve active forces and signaling, as the brief itself notes.

So avoid turning Steinberg into a universal answer.

The stronger statement:

> **For the classical passive differential-adhesion regime, endpoint ordering is reducible; active boundary systems are a different mechanism class.**

That actually sharpens the Lab.

## Architecture pressure

- many-sites-per-biological-cell;
- deformable entities;
- boundary geometry;
- active vs passive dynamics.

## Recommendation

**Weak as research; excellent architecture boundary test. Do not expand core ontology just to support it.**

---

# 17. Corrosion Pitting Lab

## What works

The pitch is unusually concrete:

> **The industrial shortcut assumes independence; interacting pits may violate that assumption.**

That is exactly the right way to enter a mature engineering field.

The data and commercial relevance are stronger than most materials Labs.

## Main critique

The abstraction gap may be larger than the brief allows.

Pit interaction is mediated by electrochemical potential, current distribution, ionic transport, solution chemistry, geometry, and sometimes metallurgy.

If the mechanism of interest is precisely pit interaction, discarding the non-local electrochemistry may discard the thing being studied.

This makes the key fit question:

> **Can a bounded local surrogate preserve the population-level interaction effect well enough to test the independence assumption?**

That must be demonstrated against a higher-fidelity or experimental reference before any useful inference is made.

The second issue is 3D.

If the outcome of interest is pit survival/population spacing rather than undercut geometry, a 2D abstraction may still be valid.

Do not require 3D automatically; tie dimensionality to the Study question.

## Recommendation

**Plausible as a narrow assumption-testing Lab; too risky for predictive positioning.**

---

# 18. Dendritic Solidification Lab

## What works

This brief is exceptionally honest about how little space SCR has.

The field has analytic theory, strong phase-field incumbents, and existing industrial CA.

That leaves a small residual.

The cross-Lab role, however, is excellent: this is the theoretically rigorous reference for diffusion-limited fingering seen in several biological Labs.

## Main critique

The “same instability” connection must use mechanism-family language, not claim identity.

Biological fronts include mechanics, motility, growth, signaling, and other effects absent from solidification.

The Lab can serve as the **physics anchor for one abstract instability family** without implying that tumor or wound behavior is Mullins–Sekerka in a literal sense.

The biggest practical concern is lattice anisotropy.

This Lab should be forbidden from making morphology claims until it passes explicit rotation/lattice controls.

## Recommendation

**Weak research Lab; strong cross-Lab theory/reference Lab.**

---

# 19. Grain Growth Lab

## What works

Almost all of it.

This is the best example so far of a Lab whose primary customer is SCR itself.

The exact law and canonical Potts model provide:

- correctness benchmarks;
- known artifact tests;
- known negative results;
- known topological statistics;
- cheap repeatability.

That is gold for platform validation.

## Main critique

The phrase “per-grain, per-step prediction” should be used carefully.

Von Neumann–Mullins is a continuous-time area-change relation under specific ideal assumptions, not automatically a literal expected delta per arbitrary SCR step.

The Lab can still use it as an exact relationship after mapping Reactor time/scale appropriately.

That mapping must itself be tested.

Second, the platform should avoid training/generation leakage if this becomes a benchmark.

If Generation is prompted with the exact law, rediscovery proves little.

A benchmark protocol should define what the model is allowed to know.

That is a deeper point:

> **Calibration Labs need blinded benchmark modes.**

Otherwise an LLM may merely reproduce memorized textbook mechanisms.

## Recommendation

**Build early as a calibration Lab. Its research weakness is irrelevant to that role.**

---

# 20. Benchmark leakage becomes a real problem in this batch

Several canonical domains are likely present in foundation-model training data:

- Greenberg–Hastings excitable media;
- Cellular Potts sorting;
- DLA/Eden biofilms/tumors;
- Potts grain growth;
- classical dendrites.

If SCR “discovers” them, did the platform infer the mechanism from evidence?

Or did the LLM remember the literature?

This was already a threat in the position paper.

These Labs make it operational.

For benchmark Studies, SCR should record whether Generation received:

- domain name;
- known mechanism names;
- canonical citations;
- target behavior only;
- abstracted measurements;
- deliberately disguised vocabulary.

A powerful test would be:

> **Can Generation recover a known mechanism family from behavior descriptors when the domain name and canonical vocabulary are withheld?**

That tests mechanism supply rather than literature recall.

Grain Growth, Excitable Media, and Biofilm Morphology are excellent places to do it.

---

# 21. Hidden-state / sanctuary mechanisms become a strong cross-Lab family

Tumors, biofilms, granulomas, and cortical spreading depression all contain a form of hidden state that changes outcome.

But there are at least two distinct families.

## Spatial sanctuary

Where something survives because position protects it.

- hypoxic tumor interior;
- dormant biofilm interior;
- pathogen reservoir inside granuloma.

## Recovery debt / hidden physiological state

Where visible activity stops but the system is not restored.

- cortical metabolic reserve;
- excitable refractory tissue;
- smoldering underground fire in earlier batches.

These should not be merged under one vague “hidden state” label.

Readers and Search should be able to distinguish them.

---

# 22. This batch strengthens the case for Reader-first validation

Many headline outcomes are too easy to fake visually.

A serious Study should compare mechanisms using Readers such as:

- spiral core count;
- wave-break frequency;
- refractory recovery distribution;
- tumor margin roughness;
- branch spacing;
- leader spacing;
- sector survival statistics;
- granuloma core/periphery ratios;
- pit spatial inhibition statistics;
- grain side-number/area-change relation;
- orientation bias;
- abnormal-grain fraction.

The View should show the phenomenon.

The Reader should decide whether the mechanism matched the reference statistic.

This batch is where the “Reader interprets evidence” architecture becomes obviously necessary.

---

# 23. Suggested Lab roles for 21–30

## Excitable Media
**Flagship mechanism-family / cross-Lab reference Lab**

## Cortical Spreading Depression
**Paired transfer Lab / geometry stress test**

## Avascular Tumor Growth
**Spatial morphology / ensemble research Lab**

## Wound Healing
**Controlled validation / transient-dynamics Lab**

## Biofilm Morphology
**Controlled calibration / fingering-family Lab**

## Immune Response
**Spatial-sanctuary cross-Lab case; likely narrow/late**

## Cell Sorting and Tissue Boundary
**Architecture boundary / reducible-endpoint calibration case**

## Corrosion Pitting
**Incumbent-assumption challenge / engineering stress Lab**

## Dendritic Solidification
**Theory anchor / cross-Lab instability reference**

## Grain Growth
**Exact-answer platform calibration Lab**

---

# 24. Suggested ranking for this batch

This is critique-oriented prioritization, not completed fit review.

## Tier A — strongest combined value

### Excitable Media
Excellent mechanism fit, history data, cross-domain leverage.

### Biofilm Morphology
Exceptional experimental testability and strong mechanism-family links.

### Grain Growth
Weak domain novelty, extraordinary platform-calibration value.

### Wound Healing
Excellent time-lapse validation and a real transient mechanism question.

## Tier B — valuable, narrower, or higher-risk

### Avascular Tumor Growth
Good spatial questions, crowded field, severe credibility hazard.

### Cortical Spreading Depression
Useful as a paired Excitable Media transfer Lab, weaker standalone.

### Corrosion Pitting
Compelling assumption-testing pitch, large abstraction gap.

### Dendritic Solidification
Low novelty, but valuable as rigorous theory anchor.

## Tier C — architecture value exceeds research value

### Cell Sorting and Tissue Boundary
Excellent boundary test; endpoint mostly reducible.

### Immune Response
Interesting emergent object, poor validation, incumbent is already the same class of model.

---

# 25. Candidate scope reductions

## Immune Response → Granuloma Formation

This would make the Lab much more honest and bounded.

## Biofilm Morphology → Colony Morphology + later Biofilm profile

Plate colonies and hydrated clinical biofilms should not share assumptions casually.

## Avascular Tumor Growth

Keep “avascular” aggressively. Angiogenesis should be a separate Lab or explicit exclusion.

## Excitable Media

Keep the abstract family broad, but individual domain Studies should remain clearly separated.

---

# 26. New platform requirements exposed by Labs 21–30

## P15. Calibration level

A Lab declares whether validation can reach plausibility, experimental agreement, or law-level correctness.

## P16. Biological/domain entity mapping

Every Lab states what an SCR Cell corresponds to.

## P17. Lattice-artifact controls

Shape-sensitive Labs require automated anisotropy checks.

## P18. Mechanism-family similarity levels

Same mechanism, same mechanism family, and same behavior family must be distinguishable.

## P19. Benchmark leakage protocol

Canonical benchmark Labs need blinded generation modes.

## P20. Many-sites-per-entity boundary

Explicitly unsupported unless/until promoted by a platform decision.

## P21. Surface/manifold Layout

World adjacency must not depend on flat display coordinates.

## P22. Lab credibility class

High-consequence medical/engineering Labs need stronger presentation/export guardrails.

---

# 27. What I would not change yet

I would not yet:

- add deformable entities to SCR;
- add a full mesh/manifold engine;
- introduce patient-specific data;
- build clinical treatment Studies;
- solve electrochemistry globally inside the Reactor;
- add phase-field solvers;
- make every biology Lab agent-based;
- promote hidden-state visualizations into scientific claims;
- merge all fingering Labs into one;
- use benchmark rediscovery as evidence of novelty.

The remaining thirty Labs may either reinforce or kill some of these requirements.

That is why this catalog pass matters.

---

# 28. Questions for Claude, Gemini, and domain reviewers

1. Which medical/engineering claim still sounds too close to prediction despite the non-claims?
2. Which "closed form" or "reducible" statement is oversimplified?
3. Which Lab's Cell represents the wrong causal scale?
4. Which biological “cell” is being confused with an SCR Cell?
5. Where does one real entity need to occupy many lattice sites?
6. Where is the lattice producing the morphology attributed to physics?
7. Which cross-Lab “same mechanism” claim is actually only analogous behavior?
8. Which Lab requires a global field solver that would swallow the local rule?
9. Which exact/reference benchmark could be contaminated by LLM memorization?
10. How should a benchmark be blinded so rediscovery means something?
11. Which hidden state is genuinely future-relevant and which is only a Reader-derived label?
12. Which Lab should be renamed to narrow its actual scope?
13. Which reference experiment can falsify a mechanism rather than merely look similar?
14. Which incumbent is already doing mechanism exploration better than SCR plausibly could?
15. Which Lab has a compelling negative-space result even if no novel positive mechanism appears?
16. Where should a View be prohibited from displaying physical/clinical units because users will over-read it?
17. Which lattice-artifact control would a domain reviewer expect before trusting morphology?
18. What sentence would make a competent practitioner immediately distrust the brief?

---

# 29. Final assessment

Labs 21–30 add an important new dimension to the SCR story.

The first batches asked whether the platform could model interesting mechanisms honestly.

This batch asks whether it can be **scientifically disciplined in fields where the models already exist.**

That is harder.

The best answer emerging is:

> **SCR's contribution is often not a better single model. It is a systematic mechanism experiment system that can generate, test, reject, compare, and retain many readable mechanism candidates under a common evidence protocol.**

Excitable Media is the strongest mechanism-family Lab.

Biofilm Morphology is one of the strongest experimental-validation Labs.

Wound Healing is an excellent transient-dynamics calibration case.

Grain Growth is probably the strongest correctness-calibration Lab in the catalog.

Dendritic Solidification is a useful theory anchor despite weak novelty.

Tumor Growth and Corrosion Pitting have real openings but demand narrow claims.

Immune Response and Cell Sorting are valuable largely because they expose platform limits.

The biggest new architectural issue is the **mapping between SCR Cells, domain entities, and geometry**.

The biggest validation issue is **lattice artifact versus physical anisotropy**.

The biggest methodological issue is **benchmark leakage from LLM prior knowledge**.

And the most important positive development is that the Lab catalog now contains enough canonical mechanism families to test whether SCR's cross-domain Corpus is actually more than a collection of simulations.

That is a serious milestone.
