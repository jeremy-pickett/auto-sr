# Semantic Cellular Ruliology 3.x
## Critique of Lab Knowledge Briefs 1–10
### Wildfire · Smoldering/Peat · Landslide/Debris Flow · Dune/Ripple · Coastal Erosion · River Braiding · Karst Dissolution · Permafrost Thaw · Sea-Ice Melt Ponds · Snow/Crystal Growth

**Status:** family critique of first-pass Lab Knowledge Briefs  
**Scope:** Labs 1–10  
**Intent:** critique these Labs as a connected stress test of SCR, not as finished domain papers or completed fit reviews.

---

## Executive assessment

This first ten-Lab set is much stronger than a typical “applications catalog.”

The documents are not asking whether cellular automata can make visually plausible versions of the named phenomena. They repeatedly ask the more useful questions:

- Which parts of the domain are already reducible to formulas, regime maps, or established reduced models?
- Where does simulation become necessary because path, coupling, threshold crossing, or history matters?
- What would SCR actually contribute rather than merely reproduce?
- Which parts of the phenomenon fit a local-mechanism abstraction honestly?
- Where would the platform’s own architecture have to change?
- What evidence exists to falsify a candidate mechanism?
- What claims would be dangerous or misleading?

That framing is the strongest feature of the set.

Across Labs 1–10, a recurring pattern appears:

> **The best SCR fit is not “this domain is complex.” It is “the domain has a known shortcut for one regime, and a specific interaction-dominated regime where that shortcut fails.”**

Wildfire, coastal erosion, river braiding, permafrost, and melt ponds all express this cleanly. Landslides do too, through the contrast between per-cell susceptibility and interacting load-transfer cascades. Dunes and snow/crystals show the opposite problem: the platform fit is excellent, but the domain already has canonical local-rule models, so SCR risks rediscovery more than discovery.

That distinction is important enough that I would eventually make it a formal Lab-fit question.

The major architectural lesson from this batch is equally clear:

> **The Labs are already doing architecture work.**

These ten briefs collectively force decisions about:

- non-local but physically meaningful transport;
- external fields versus second mechanisms;
- state-dependent connections;
- multiple timescales;
- 3-D state spaces;
- hidden computational state;
- dynamic observability;
- domain-specific geometry;
- grid versus network layouts;
- validation quality;
- visual credibility hazards.

That is exactly what the Lab system should do.

---

# 1. The shared strength: every Lab asks “where is the shortcut?”

The “Where the shortcut holds, and where it breaks” section is the best structural choice in these briefs.

Keep it.

It prevents SCR from becoming a hammer looking for nails.

The strongest examples are:

- **Wildfire:** steady homogeneous spread is already well served by Rothermel/Huygens-style approaches; the interesting territory is heterogeneity, spotting, junction behavior, and coupled fire–atmosphere effects.
- **Landslide:** static susceptibility is largely reducible; interaction enters through load transfer, progressive failure, entrainment, and rainfall history.
- **Coastal erosion:** low-angle transport behaves diffusively and is reducible; high-angle instability becomes path-dependent and pattern-forming.
- **River braiding:** regime classification is reducible; the actual realization of channels and avulsions is not.
- **Permafrost:** vertical thaw depth is reducible; lateral connectivity and wetting/draining bifurcation are not.
- **Melt ponds:** static percolation explains much of the geometry; the co-evolving substrate and drainage history do not.

This is the right conceptual filter.

I would sharpen the language slightly across the whole catalog:

### Reducible does not mean “simple”

It means a cheaper, established method already answers the question to the required level.

### Irreducible does not mean “mysterious”

It means the requested outcome depends on iterative state evolution, arrangement, history, or coupling strongly enough that the shortcut no longer determines the answer.

That distinction will matter when outside reviewers attack the word “irreducible” as too broad.

---

# 2. The biggest recurring architecture problem: external fields versus mechanisms

DEC-1 appears everywhere because the Labs are revealing a real unresolved platform question.

Examples:

- wildfire and wind;
- dunes and wind;
- coastal erosion and wave climate;
- river braiding and water/sediment;
- landslides and rainfall/shaking;
- permafrost and climate forcing;
- snow/crystals and vapor diffusion.

The current briefs sometimes call these “second mechanisms,” but not all time-varying drivers should be modeled the same way.

The platform probably needs at least three categories.

## Static World condition

A property that does not evolve during a Run.

Examples:

- fixed slope;
- bedrock type;
- initial fracture network;
- fixed prevailing direction.

## External input

A field or schedule that changes during a Run but is supplied from outside the simulated state and does not react to it.

Examples:

- recorded wind series;
- rainfall sequence;
- prescribed wave climate;
- temperature history.

## Interactive mechanism

A process whose future state depends on simulated state.

Examples:

- fire changing local airflow;
- drainage changing future thaw;
- water routing changing sediment transport;
- vapor depletion changing future crystal growth.

This split is cleaner than “everything dynamic is another Plugin.”

It also matters for Studies. A Study may want to hold the mechanism fixed and vary an external input. That should not require pretending the input is part of the mechanism.

Recommendation:

> **Resolve DEC-1 partly by introducing explicit external inputs before deciding the full multi-Plugin composition model.**

That will eliminate several false composition problems while preserving the genuinely coupled ones.

---

# 3. “Local” is already under serious pressure

These Labs are excellent stress tests of SCR’s local-mechanism identity.

The recurring cases are not the same.

### Wildfire spotting

An ember may ignite far ahead of the front.

This is long-range transport with stochastic placement.

### Dune saltation

A sand slab makes a physically meaningful finite hop.

This is non-neighbor transport, but still highly local in physical mechanism.

### Coastal shadowing

A cape changes which waves can reach another part of the coast.

This requires geometry that may depend on a large portion of the shoreline.

### Melt ponds

Connected water shares a level across the whole connected region.

This is effectively a global constraint within a connected component.

### River braiding

Reach may remain local, but the direction of interaction changes with state.

These should not be collapsed into one “non-local” label.

A useful eventual taxonomy might be:

- **Neighbor-local:** immediate declared neighbors.
- **Bounded transport:** finite jump/hop governed by a local rule.
- **Path-local:** influence follows declared connections over bounded path length.
- **Connected-region constraint:** behavior depends on all members of one connected region.
- **Global read:** mechanism may inspect arbitrary world state.

The first four may still fit SCR honestly, depending on implementation.

The fifth is where the platform risks becoming a general simulator.

I would not decide the exact boundary from these ten Labs alone, but I would register the distinction now. “Local” is too important to remain a vibe.

---

# 4. Time semantics are not one problem

The briefs repeatedly say “one tick cannot mean all of this,” correctly.

But there are at least three different time problems.

## Scale span

Smoldering: hours to months or decades.  
Permafrost: season to century.  
Coastal erosion: hours to decades.

## Event duration mismatch

A catastrophic breach may occur in minutes inside a model otherwise progressing over months.

## Different process clocks

Wind, heat, hydrology, erosion, and biological or chemical response may have different natural update rates.

These are not necessarily solved by giving every Plugin an arbitrary asynchronous clock.

That would be dangerous.

A better future design may offer named Reactor execution models such as:

- fixed-step synchronous;
- fixed-step phased;
- scheduled external inputs;
- bounded delayed effects;
- event-triggered substeps;
- multi-rate phases with deterministic ordering.

The important point for this Lab set:

> **Do not let every Lab invent its own temporal workaround.**

DEC-3 needs a small closed set of platform-supported temporal semantics.

---

# 5. Validation strength varies so much that “Lab standing” needs dimensions

The briefs already distinguish “standing” from “fit review,” which is good.

But a single grade such as strong/plausible/moderate may eventually compress too much.

These ten Labs differ along at least four axes.

## Mechanism fit

Does the local-state abstraction make sense?

## Validation quality

Can outputs be checked against direct observation, controlled experiments, or only indirect statistics?

## Novelty headroom

Is there room for new mechanism supply, or is the canonical local-rule model already known?

## Practical usefulness

Would anyone actually use the resulting mechanism catalog?

Examples:

### Wildfire
High fit, high validation, meaningful headroom, meaningful audience.

### Dune/Ripple
High fit, excellent validation, low novelty headroom, modest audience.

### Karst
High conceptual fit, low direct validation, some scientific interest, small audience.

### Snow/Crystal
Excellent fit and visuals, excellent experimental precedent, but very low practical need and high rediscovery risk.

### Smoldering
Strong conceptual demonstrator, but poor validation.

I would not yet build a scoring formula.

I would, however, require every completed fit review to state these dimensions separately.

---

# 6. Visualization risk is not secondary—it is part of scientific integrity

Several Labs identify this independently:

- wildfire fronts look like forecasts;
- coastal erosion near houses looks like property prediction;
- permafrost visualizations can be mistaken for climate projections;
- snow crystals can look scientifically profound while saying nothing new.

This is important enough to become a Lab-review requirement.

A visual can be accurate as a rendering and still be misleading as a product claim.

Every Lab should eventually document:

- which views are scientifically useful;
- which views are especially easy to over-read;
- what evidence each visual element comes from;
- what captions/watermarks/context are mandatory;
- whether a visual may appear in marketing without its Study context.

The Snow and Crystal Growth Lab is the cleanest demonstration:

> **Beauty is the failure mode.**

Keep that language somewhere.

It is useful beyond snow.

---

# 7. Lab roles are emerging, and that is healthy

Not every Lab needs to justify itself by producing new domain science.

This batch naturally separates into roles.

## Calibration anchor

A Lab with good ground truth used partly to prove SCR’s evidence chain.

- Wildfire

## Rediscovery benchmark

A Lab where a canonical local-rule model exists and SCR should be able to recover something like it.

- Dunes
- River braiding
- Snow/crystal growth

## Architecture stress test

A Lab that forces the platform to confront a difficult capability.

- Smoldering: 3-D + hidden state
- Karst: network layout
- Coastal erosion: shadowing/non-local geometry
- Melt ponds: connected-region constraints

## Mechanism-supply candidate

A Lab with a specific underexplored interaction problem.

- Landslide load transfer
- Permafrost wetting/draining transition
- River avulsion timing
- Melt-pond co-evolving substrate
- Wildfire junction/spotting mechanisms

This taxonomy may be more useful than one global rank.

A Lab can be commercially weak but architecturally essential.

---

# 8. Wildfire Lab

## What works

This is the strongest all-around Lab in the batch.

The brief does three things especially well.

First, it refuses to compete with established operational spread models in regimes where they are appropriate.

Second, it identifies specific failure regimes rather than making generic “wildfire is complex” claims.

Third, it has unusually good validation prospects.

Calling wildfire the calibration anchor is justified.

## Main critique

The phrase “candidate local rules for the regimes where fast models are known to fail” is good, but the Lab must be extremely careful around coupled fire–atmosphere behavior.

Once fire alters wind strongly, a simple local CA may no longer be the right abstraction.

That does not make the Lab invalid.

It means the fit review must draw a line between:

- local front mechanisms under prescribed or weakly coupled wind;
- reduced two-way coupling SCR can represent honestly;
- full fire–atmosphere dynamics requiring CFD or coupled physical models.

The Lab should not let “candidate mechanism supply” become a license to imitate plume physics with arbitrary local heuristics.

## Architecture pressure

- external input vs coupled mechanism;
- long-range transport;
- anisotropy;
- dimensional time mapping;
- visual forecast risk.

## Recommendation

**Keep as top-tier and likely first-wave Lab.**

---

# 9. Smoldering and Peat Fire Lab

## What works

Conceptually, this may be the best demonstrator of hidden computational state.

The brief is correct that “quiet picture ≠ stopped computation” is not merely an abstract SCR principle here; it is physically the phenomenon.

That is unusually powerful.

## Main critique

“3D or nothing” is rhetorically strong and mostly fair, but the fit review should distinguish:

- true volumetric 3-D;
- layered 2.5-D;
- reduced depth columns with lateral coupling.

A reduced representation may still be scientifically honest for some questions.

The Lab should not accidentally make full volumetric simulation a requirement before testing whether simpler abstractions preserve the mechanism of interest.

## Validation concern

The brief already flags the biggest problem: direct subsurface ground truth is sparse.

This should reduce its scientific standing even if its platform-demonstrator value remains high.

## Recommendation

**Keep, but classify primarily as architecture/demo value unless validation improves.**

---

# 10. Landslide and Debris Flow Lab

## What works

The strongest sentence is the one that says SCR’s potential contribution is the coupling term.

That is crisp.

Static susceptibility is already strong enough that “CA landslide susceptibility” would be pointless.

The interaction question—whether local load transfer changes observed failure clustering—is much better.

## Main critique

The Cell proposal risks collapsing too much continuum physics into local scalar load.

The brief acknowledges this, but the eventual fit review must be harsher.

Stress redistribution in real slope materials depends on geometry, constitutive behavior, and continuum mechanics.

A local transfer rule may be:

- a useful toy mechanism;
- a reduced model;
- or physically misleading.

The Lab must define which claim it is making.

## Validation opportunity

Observed post-storm inventories provide strong spatial statistics.

This is a real advantage.

## Recommendation

**Plausible, but only if the Lab narrowly targets cascade structure rather than general slope stability.**

---

# 11. Dune and Ripple Lab

## What works

Excellent honesty about rediscovery.

This Lab is almost ideal as a platform benchmark.

It tests whether:

- Generation can find Werner-like mechanism families;
- the Corpus distinguishes rediscovery from novelty;
- non-neighbor hops can be expressed honestly;
- known morphology classes emerge.

## Main critique

The Lab title currently joins dunes and ripples even though the brief itself says they arise from separate instabilities at different scales.

That may be too broad.

A future deep pass should consider splitting:

- **Ripple Lab**
- **Dune Lab**

or making “Dune and Ripple” explicitly a paired Lab with separate mechanism classes.

Otherwise one Lab may quietly violate its own Cell/time assumptions by pretending the same mechanism spans both.

## Recommendation

**Keep as a high-value benchmark; strongly consider splitting the scales.**

---

# 12. Coastal Erosion Lab

## What works

Very strong reducible/irreducible framing.

The high-angle instability threshold gives this Lab a particularly clean boundary between where reduced models suffice and where pattern realization becomes important.

The historical cellular-model precedent also fits the platform thesis well.

## Main critique

Shadowing may be more than a “strain” on locality.

Depending on implementation, it can require a global geometric visibility calculation.

If so, that calculation belongs either:

- to the World/Reactor as a declared helper;
- or outside SCR’s allowed local mechanism class.

The Plugin should not be given arbitrary global geometry access.

## Product risk

The brief correctly identifies the danger of rendered shoreline retreat being mistaken for real property prediction.

This Lab needs unusually strict visualization labeling.

## Recommendation

**Keep; excellent stress test of global-helper boundaries and high-value validation data.**

---

# 13. River Braiding Lab

## What works

“Classification is reducible, realization is not” is one of the best reusable phrases in the set.

The Lab also has an unusually strong validation stack:

- canonical local-rule precedent;
- controlled flume experiments;
- real satellite observations.

That makes it a superb platform benchmark.

## Main critique

The document says connections are directed and direction depends on state.

That may be the wrong abstraction.

The World Layout can remain fixed adjacency while the **weight or allowed flow along connections** changes with elevation/state.

That distinction matters.

If every state-dependent interaction is modeled as a changing graph, the platform may make dynamic connections much more complicated than necessary.

Recommendation:

> Distinguish dynamic connection existence from dynamic connection strength/direction.

In a grid, all downhill-adjacent edges can exist while the Reactor/Plugin computes which carry flow.

## Recommendation

**Keep as a benchmark/calibration Lab; refine the connection model.**

---

# 14. Karst Dissolution Lab

## What works

This is the strongest argument in the batch for Network World.

The phenomenon naturally follows a pre-existing fracture graph.

Using a grid by default would be less honest.

The positive-feedback competition between nearly identical fractures is also a very pure mechanism-supply example.

## Main critique

The brief sometimes treats sensitivity to tiny differences as sufficient evidence of computational irreducibility.

Be careful.

Sensitivity and irreducibility are related but not equivalent.

A system can be highly sensitive and still have useful reduced statistical predictions.

The stronger claim is:

> exact conduit realization depends on the iterated competition among fractures and cannot be obtained from the single-fracture shortcut.

That is enough.

No need to overclaim philosophical irreducibility.

## Validation concern

Direct validation is extremely weak.

This should substantially lower its standing as domain science.

## Recommendation

**Keep as a Network World and sensitivity demonstrator; weak candidate for early external validation.**

---

# 15. Permafrost Thaw Lab

## What works

This is one of the strongest genuine mechanism-supply opportunities in the batch.

The contrast between vertical column thaw models and laterally coupled connectivity effects is clean.

The wetting-versus-draining bifurcation is an excellent Study.

The validation landscape is also unusually good for a complex climate-adjacent domain.

## Main critique

The brief should be careful not to imply that abrupt thaw is missing from all modern land-surface/permafrost models.

The safer claim is that many operational/climate-scale representations remain coarse and that abrupt lateral thermokarst processes are difficult to represent faithfully at scale.

The eventual deep paper will need strong citations here.

## Architecture pressure

- external climate forcing;
- inherited polygon geometry;
- connectivity transitions;
- seasonal/century scale separation.

## Recommendation

**Strong candidate for a serious early Lab, with unusually strict non-claim and visualization controls.**

---

# 16. Sea-Ice Melt Pond Lab

## What works

This is an unusually rigorous brief.

It attacks its own value proposition directly:

> if percolation universality already explains the statistics, SCR may have nothing to contribute.

That is excellent.

The opening left for SCR—co-evolving substrate plus drainage—is specific and defensible.

## Main critique

The “water finds level” issue may imply that this Lab cannot be expressed purely through local Plugin rules without a Reactor/World helper.

That is not necessarily a failure.

It may reveal a useful class of **declared physical constraints** that the Reactor can solve deterministically.

But if the platform starts adding arbitrary domain solvers as helpers, the Labs can smuggle whole models into the Reactor.

The rule should be:

> a helper may provide a generic execution primitive, not domain-specific answers.

Connected-component equalization may be generic enough.

“Melt pond hydrology solver” is not.

## Recommendation

**Keep; excellent test of helper boundaries and one of the strongest data-backed Labs.**

---

# 17. Snow and Crystal Growth Lab

## What works

Excellent honesty.

This Lab understands its own danger better than almost any other.

The platform-fit is superb.

The scientific need is weak.

The visuals will be spectacular.

That combination is exactly why the Lab is valuable as an integrity test.

## Main critique

The phrase “habit class from temperature and supersaturation—read the diagram” may simplify too much.

The morphology diagram is a strong empirical guide, but actual habit depends on more than two idealized variables and transitions can be complicated.

The eventual deep paper should nuance that.

The larger architectural issue is geometry.

A hexagonal/triangular layout is not an exotic exception; it is evidence that Grid World must not mean “square grid.”

The platform should support named lattice geometries or general local spatial graphs rather than hard-code Cartesian adjacency.

## Recommendation

**Keep as a benchmark and visualization-honesty Lab, not as a flagship science opportunity.**

---

# 18. Two Labs may need to split before they deepen

The first ten already contain examples where one Lab name hides multiple process scales.

## Dune and Ripple

The document explicitly says ripples and dunes are separate instabilities.

That is a warning.

## Wildfire

Surface flame spread, spotting, and coupled plume dynamics may become too broad if treated as one mechanism space.

They may remain under one Lab umbrella, but likely as explicit subdomains.

## Smoldering

Peat, duff, coal seam, and overwintering fire share mechanism families but differ enormously in geometry and timescale.

The Lab may need named study profiles.

The general rule:

> **A Lab may contain several related phenomena, but one Plugin contract should not be forced to explain all of them merely because the words share a domain.**

---

# 19. Some “Cell carries” sections are still mixing state with derived measurement

The Cell sections are generally good, but a few candidate properties may belong elsewhere.

Examples:

- local slope may be static World data rather than mutable Cell state;
- local flow/discharge may be derived by Reactor/Plugin rather than stored state;
- shadow state may be a derived observation;
- albedo state might be derived from ice/water/lid state;
- accumulated heat may be a convenience variable rather than fundamental state.

This is not a problem yet.

These are briefs.

But the deep fit reviews should ask:

> **Does this value need to persist to determine the future, or is it cheaply derived from other state?**

That matters because Cells are supposed to remain bounded and simple.

The more derived conveniences get stored, the easier it becomes to hide mechanism complexity in state.

---

# 20. The canonical-model Labs should become explicit regression targets

Dunes, rivers, and snow/crystals all have famous local-rule precedents.

Do not merely cite them.

Use them.

For each such Lab, define a future platform regression question:

> Can SCR, without being directly handed the known implementation, generate a mechanism family whose behavior falls within the known benchmark class?

That is a serious test of Generation.

A second test:

> When Search is asked for the observed behavior, does the Corpus retrieve those mechanisms?

A third:

> Does the negative space reveal failed mechanism families rather than simply noise?

These Labs may tell us more about SCR quality than about their domains.

---

# 21. The strongest mechanism-supply questions in Labs 1–10

Not every brief’s “upside” is equally sharp.

The strongest candidate Study questions are:

### Wildfire
Which simple interaction rules produce junction acceleration or spotting-driven pattern changes under otherwise fixed forcing?

### Landslide
Does local load transfer improve the spatial and size statistics of failures beyond uncoupled susceptibility?

### River braiding
Which local rule structures control avulsion timing and channel capture?

### Permafrost
What local coupling rules produce the wetting-versus-draining connectivity transition under fixed warming?

### Melt ponds
What local rules reproduce pond morphology when the substrate itself evolves and drainage can reset the system?

### Snow/crystal
Which local attachment/noise mechanisms reproduce measured sidebranch statistics or degree of symmetry?

### Karst
Which local competition rules produce observed network topology statistics from plausible fracture populations?

These are much better than generic “simulate X” goals.

They should eventually appear near the top of the Lab documents.

---

# 22. The weakest novelty positions in Labs 1–10

The highest rediscovery risk is:

1. **Dunes**
2. **Snow/crystal growth**
3. **River braiding**
4. **Coastal erosion**

This does not mean remove them.

It means their role should be explicit.

A good Lab description might say:

> **Primary role: platform benchmark. Secondary role: mechanism exploration in unresolved regimes.**

That is more credible than trying to sell every Lab as a frontier research opportunity.

---

# 23. The weakest validation positions

The most serious validation constraints are:

1. **Karst**
2. **Deep smoldering/peat**
3. parts of **wildfire coupled-atmosphere behavior**
4. long-horizon **permafrost process attribution**

These Labs may still generate valuable mechanisms.

But the Corpus should distinguish:

- behavior matched to direct observation;
- behavior matched to indirect statistics;
- behavior matched only to qualitative domain expectation.

Those evidence levels should never look equivalent in Search.

---

# 24. The ten Labs expose at least eight platform decisions

I would explicitly feed these back into the SCR Decision Registry.

## P1. External input versus mechanism

Repeated in at least six Labs.

## P2. Locality/reach classes

Neighbor, hop, connection path, connected-region, global.

## P3. Spatial geometry families

Square, hexagonal/triangular, layered 3-D, arbitrary network.

## P4. Dynamic connection semantics

Connection existence versus state-dependent direction/weight.

## P5. Multi-rate temporal semantics

Needed across the family.

## P6. Generic physical constraints/helpers

Example: connected-region leveling without domain-specific solvers.

## P7. Validation standing

Direct observation versus indirect/statistical evidence.

## P8. Visualization credibility class

How easy a Lab’s output is to mistake for real prediction.

The important point:

> These are not requirements invented by architecture speculation. The Labs independently demanded them.

That gives them stronger legitimacy.

---

# 25. Suggested additions to the Lab Knowledge Brief template

The current template is already very good.

I would add only a few short fields.

## Primary Lab role

One or more of:

- mechanism-supply;
- calibration;
- rediscovery benchmark;
- platform stress test;
- visualization/integrity demonstrator.

## Strongest falsifiable question

One sentence.

## Validation class

For example:

- direct experimental;
- direct observational;
- indirect/statistical;
- qualitative only.

## Platform pressure

List the architectural decisions this Lab stresses.

## Rediscovery risk

Low / medium / high, with one sentence.

These five additions would make later catalog synthesis much easier.

---

# 26. Suggested ranking for this batch

This is not a formal fit review.

It is a critique-oriented prioritization based on the briefs as written.

## Tier A — strongest combined value

### Wildfire
Best overall calibration anchor and credible mechanism-supply opportunity.

### Permafrost thaw
Strong real gap, strong data, strong Study structure, high credibility risk but manageable.

### River braiding
Excellent benchmark and validation environment, with a real narrow open question.

### Sea-ice melt ponds
Very rigorous, strong measurable statistics, narrow but real gap.

## Tier B — valuable for specific roles

### Landslide/debris flow
Good coupling question, but abstraction risk is substantial.

### Coastal erosion
Good benchmark and instability regime, but shadowing/non-locality must be handled honestly.

### Dune/ripple
Excellent benchmark and reach test; limited novelty.

### Smoldering/peat
Exceptional hidden-state demonstrator; weak validation.

## Tier C — keep for architecture/intellectual value

### Karst
Beautiful fit and useful Network World stress test; weak direct validation and tiny audience.

### Snow/crystal growth
Excellent benchmark and honesty test; limited need and very high aesthetic distraction.

None of these should be removed from the catalog on the basis of this pass.

The tiers describe likely **roles and build priority**, not scientific worth.

---

# 27. What I would not do yet

I would not yet:

- assign formal fit grades;
- verify every domain citation;
- decide the exact Reactor model for each Lab;
- resolve all DEC-1 cases locally;
- choose final Cell properties;
- design Readers;
- select validation datasets;
- write market positioning;
- optimize visualization concepts.

The next Lab batches may expose the same platform questions from completely different domains.

That cross-domain recurrence is valuable evidence.

Do not freeze the architecture before we have seen more of the sixty.

---

# 28. Questions for Claude, Gemini, and domain reviewers

For these ten Labs, I would ask reviewers to attack the briefs with questions like:

1. Where is a reducible regime being mislabeled as irreducible?
2. Where is sensitivity being confused with computational irreducibility?
3. Where does a proposed Cell state already contain the answer the mechanism claims to discover?
4. Where is a continuum process reduced to neighbor transfer beyond scientific defensibility?
5. Which proposed “external field” is actually a coupled mechanism?
6. Which alleged local rule requires global information?
7. Which Lab has a better incumbent model that makes SCR unnecessary?
8. Which validation claim relies on data that cannot actually measure the proposed emergent quantity?
9. Which Lab’s visualization would most easily be mistaken for a forecast or prediction?
10. Which Lab has a canonical CA precedent that SCR should explicitly use as a benchmark?
11. Which Lab would force a domain-specific solver into the Reactor and thereby corrupt the core architecture?
12. Which Lab is actually two Labs hidden under one title?
13. Which Cell properties are derived values rather than future-relevant state?
14. Which Study has a clear falsifiable outcome?
15. Which “open question” is actually already well answered in the literature?

For outside domain review, add:

> **What sentence here would make a competent practitioner in this field immediately distrust the rest of the document?**

That is often the most useful question.

---

# 29. Final assessment

Labs 1–10 validate the Lab concept itself.

They are already doing more than cataloging possible applications.

They are forcing SCR to answer:

- what local means;
- what a World owns;
- what counts as external forcing;
- how time works;
- how non-square and non-grid geometry works;
- how state can remain hidden from a view;
- how strong a validation claim may be;
- how visuals can mislead;
- when a canonical model makes a Lab a benchmark rather than a discovery opportunity.

The strongest overall Labs in this first batch are Wildfire, Permafrost, River Braiding, and Sea-Ice Melt Ponds.

The strongest platform demonstrators are Smoldering, Dunes, Karst, and Snow/Crystal Growth.

The biggest architectural issue exposed by the family is still the interaction between **World conditions, external inputs, and multiple mechanisms**.

The biggest epistemic issue is **validation standing**.

The biggest product risk is **beautiful output being interpreted as stronger evidence than it is**.

And the most important positive signal is this:

> The briefs are repeatedly discovering platform requirements independently.

That is exactly what should happen if the Lab system is real rather than decorative.
