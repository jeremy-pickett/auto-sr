# Semantic Cellular Ruliology 3.x
## Lab Knowledge Report — Labs 1–10
### Wildfire · Smouldering/Peat · Landslide · Dune/Ripple · Coastal Erosion · River Braiding · Karst · Permafrost · Melt Ponds · Snow Crystals

**Document class:** Level 5 draft (Lab Papers, pre-fit) · **Status:** draft
**Version:** v1 · **Date:** 2026-08-20
**Supersedes:** first-pass Lab Knowledge Briefs 01–10 (`labs/short-lab-definitions/`), which remain readable in place
**Responds to:** `critiques/SCR_Labs_01-10_Critique_v0.1.md`
**Applies:** `DOC_GOOD_IDEAS.md` (working notes, 2026-08-20)
**Cites:** SCR-F v0.2 §11, §13.1, §15, §18.5, §25.3, §29, §30, §38.6, §41–43, §45.12; F-7, F-9, F-14, F-17
**Fit reviews (SCR-F §30):** none performed. Nothing here establishes fit.

---

> ## ⚠ SUPERSEDED — do not cite
>
> This report predates the decision to organize production Lab papers by family (`labs/<family>/`). It straddles two families and is now **fully superseded**:
>
> | Content | Superseded by |
> | :--- | :--- |
> | Labs 1–8 | `labs/a-fire-land-and-surface/family-a-report-v1.md` |
> | Labs 9–10 | `labs/b-ice-water-and-atmosphere/family-b-report-v1.md` |
> | Part I (the shared framework) | `00-start-here/irreducibility-and-what-cellular-means.md` (Level 1) |
>
> **Retained, not deleted.** The successors correct it in several places — sensitivity was conflated with computational irreducibility in four entries, and the Nakaya diagram was oversimplified — and what changed between versions is itself informative (§7, §10). Its verified references carried forward intact.
>
> Cite the successor, never this file.

---

## What this document is

Ten Labs, examined through **computational irreducibility and cellular automata**, asking one question of each: *what does this Lab need to know?*

It is not a feature spec, a requirements document, or a fit review. It contains no requirements identifiers and proposes no implementation.

Two changes from the first pass are structural rather than cosmetic. **The shared framework is stated once** (Part I) instead of re-derived in ten places — that is where the requested concision comes from, and it is also what makes the cross-Lab pattern visible. And **every factual claim now carries a reference** (Part IV), with the verification pass recorded honestly: items marked *[V]* were checked against a primary or authoritative source during this revision; items marked *[D]* are described generically because no single citation was verified.

The verification pass changed content, not just formatting. Three examples: the peat ignition moisture limit was stated in the first pass as "a few hundred percent, fuel-specific"; it is **125 ± 10% of dry mass** [24]. Rothermel's report number was given as INT-116; it is **INT-115** [1]. The 1997 Indonesian peat fire carbon release was described as "on the scale of a large industrial economy"; the published estimate is **0.81–2.57 Gt C, equivalent to 13–40% of mean annual global fossil fuel emissions** [23].

---

## §0. Revision record — critique disposition

Recorded rather than silently applied, following the project's practice: the reasoning matters more than the edits. Numbers reference sections of `SCR_Labs_01-10_Critique_v0.1.md`.

| Critique item | Disposition | Reason |
| :--- | :--- | :--- |
| §1 Sharpen *reducible* / *irreducible* definitions | **Adopted** | The words will be attacked as vague by external reviewers, and correctly. Definitions now open Part I. |
| §2 Three driver classes: static condition / external input / interactive mechanism | **Adopted, load-bearing** | The single strongest item in the critique. It dissolves roughly half the DEC-1 blockages in this batch without pre-empting DEC-1's real question. §I.4. |
| §3 Reach taxonomy instead of one "non-local" label | **Adopted** | Independently identified in `DOC_GOOD_IDEAS.md` §2 as the strongest DEC candidate. §I.3. |
| §4 Time semantics are three problems, not one | **Adopted** | §I.5. Also adopted: the warning against per-Lab temporal workarounds. |
| §5 Standing needs dimensions, not one grade | **Adopted** | Replaces the first pass's single verdict. §I.8, and the header block of every Lab. |
| §6 Visualization risk is a review requirement | **Adopted** | §I.10, plus a credibility class per Lab. |
| §7 Lab roles (calibration / benchmark / stress test / mechanism-supply) | **Adopted** | §I.9. This is the item that makes weak-novelty Labs defensible instead of embarrassing. |
| §14 Sensitivity ≠ irreducibility | **Adopted and swept catalog-wide** | Raised against Karst; the same overreach was present in the first pass's Wildfire, Coastal, and River briefs. Corrected everywhere. §I.1. |
| §16 Helper boundary: generic primitive, not domain solver | **Adopted** | §I.7. Sharpest single architectural constraint in the critique. |
| §17 Grid World must not mean square grid | **Adopted** | §I.6. |
| §19 Cell state vs derived value | **Adopted** | Every Lab's state list is now split into persistent and derived. |
| §20 Canonical-model Labs as regression targets | **Adopted** | §III.1. |
| §25 Five template fields | **Adopted with one change** | Added as a header block. "Primary Lab role" allows multiple values, because three of these Labs genuinely have two. |
| §18 Split Dune and Ripple into separate Labs | **Adopted in the weaker form offered** | Ripples and dunes are separate instabilities at separate scales and must not share one mechanism contract — but a standalone Ripple Lab has almost no content of its own. Kept as one Lab with **two declared mechanism classes and two time fits**, which is the critique's second option. |
| §27 Do not verify citations yet | **Overridden on instruction** | The critique advises deferring verification until more of the sixty are written. The user asked for a checked, referenced v1. Verification was performed and it changed substantive content (see above), which is evidence the critique was wrong to defer it. |
| §5 / §27 Do not assign fit grades | **Honoured** | No fit grades appear. Assessments are labelled as judgment, carry no standing, and are now decomposed into four axes rather than one word. |
| §26 Suggested tiers | **Adopted with two disagreements, stated** | §III.3. |
| §28 Reviewer questions | **Adopted as a checklist** | §III.5. |

**One item added that the critique did not raise.** The critique's own §14 correction — sensitivity is not irreducibility — has a mirror image the first pass also got wrong in the other direction: *universality*. Where a mechanism belongs to a known universality class, its scaling exponents are determined before it runs, and "many different mechanisms, same measurable outcome" is a direct challenge to the corpus premise. It does not bite hard in Labs 1–10 (it dominates Labs 33 and 35), but Melt Ponds and Snow Crystals both touch it, and the framework should name it now. §I.1.

---

# Part I — The shared framework

## I.1 The reducibility audit

Every Lab in this report turns on one question, and it is the question SCR-F does not currently ask (SCR-F §30 has nine; this would be the tenth):

> **Where does this domain already have a shortcut, and where has it broken?**

The framing, stated once:

> **Computational irreducibility is not a property of a domain. It is a property of a regime.**

If a shortcut exists, SCR is worthless there — it would be laboriously rediscovering a closed form. SCR earns its keep only where the shortcut has broken.

**Reducible** does not mean simple. It means *a cheaper, established method already answers the question to the required standard* — a closed form, a regime diagram, a calibrated empirical curve, a fast exact solver, or a known universality class.

**Irreducible** does not mean mysterious. It means *the requested outcome depends on iterated state evolution, spatial arrangement, history, or coupling strongly enough that the shortcut no longer determines the answer.*

Two failure modes of this framing, both of which the first pass committed:

**Sensitivity is not irreducibility.** A system can be exquisitely sensitive to initial conditions and still have useful reduced *statistical* predictions. Karst conduit competition is the clearest case: tiny aperture differences decide which fracture becomes a cave, but that does not license a philosophical claim about irreducibility. The defensible claim is narrower and sufficient: *the exact realization depends on iterated competition and cannot be obtained from the single-element shortcut.* Say that; do not say more.

**Universality is a shortcut that survives mechanism differences.** Where a process belongs to a known universality class, its scaling exponents were determined before any mechanism ran, and a hundred distinct mechanisms yield the same number. This is a direct challenge to the corpus premise that different mechanisms are worth cataloguing separately. In this batch it touches Melt Ponds (percolation) and Snow Crystals (DLA); a Lab in that position must aim at what universality does *not* cover, or admit it has nothing.

## I.2 What makes a system "cellular" — and what 3.x is negotiating away

A cellular automaton has five properties. Lined up against the Decision Registry:

| Property | Status in 3.x |
| :--- | :--- |
| Discrete cells | Decided (SCR-F §13) |
| Bounded local state | Decided (SCR-F §13.1) |
| **One uniform rule everywhere** | **In play — DEC-1.** Multiple Plugins is a non-uniform rule. |
| **Simultaneous update** | **In play — DEC-3.** |
| **Local interaction** | **In play — not registered anywhere.** See §I.3. |

Three of five are open, and one of the three is not even on the register. SCR-F §45.12 asks reviewers to hunt over-generalization; this is the checklist that hunt needs, and it gives an honest answer to *when does SCR stop being ruliology and become a generic simulator* — **when it has spent all five.**

Labs 1–10 spend against the third and fifth constantly. That is the batch's most important architectural finding.

## I.3 Reach classes

"Local" is doing too much work and the first pass collapsed five different things into one word. The distinction is consequential: it constrains the Plugin contract, every Layout family, and at least four Labs in this batch alone.

| Class | Meaning | This batch |
| :--- | :--- | :--- |
| **Neighbour-local** | Declared immediate neighbours only | Landslide, Permafrost, Melt Ponds (mostly) |
| **Bounded transport** | Finite hop to a non-neighbour, governed by a local rule | **Dune saltation** (~5 lattice sites [7]); wildfire ember transport |
| **Path-local** | Influence follows declared connections over bounded path length | Karst conduit competition |
| **Connected-region constraint** | Behaviour depends on all members of one connected region | **Melt ponds** — connected water shares one level |
| **Global read** | Mechanism inspects arbitrary World state | **Coastal shadowing**, if implemented naively |

The first four may fit SCR honestly. **The fifth is where the platform becomes a general simulator.** The boundary is undrawn and should be registered as a decision, not settled per Lab.

Note the important consequence: dune saltation is *non-local by design and physically correct*. Bounded transport is not a compromise — it is what the domain does.

## I.4 Driver classes — dissolving the false DEC-1 cases

The first pass called every time-varying influence a "second mechanism" and marked six of ten Labs blocked on DEC-1. Most of those blockages were an artifact of the vocabulary. Three categories are needed:

**Static World condition** — does not evolve during a Run. *Bedrock type, fixed slope, initial fracture network, prevailing wind direction.*

**External input** — changes during a Run, supplied from outside the simulated state, does not react to it. *A recorded wind series, a rainfall sequence, a prescribed wave climate, a warming trajectory.*

**Interactive mechanism** — future state depends on simulated state. *Fire altering local airflow; drainage altering future thaw; water routing altering sediment transport; vapour depletion altering crystal growth.*

This matters for Studies as much as for architecture. A Study wanting to hold the mechanism fixed and vary the forcing should not have to pretend the forcing is part of the mechanism.

> **Recommendation to the registry: resolve the external-input category *before* deciding the full multi-Plugin composition model.** It eliminates the false composition problems in Wildfire, Dune, Coastal, Landslide, and Permafrost while preserving the genuinely coupled ones — which are fewer, sharper, and worth DEC-1's attention.

## I.5 Time is three problems

The first pass repeated "one tick cannot mean all of this" ten times. It is three distinct problems:

1. **Scale span.** Smouldering: hours to decades. Permafrost: season to century. Coastal: hours to decades.
2. **Event duration mismatch.** A barrier breach in a night, inside a model otherwise advancing over months.
3. **Different process clocks.** Wind, heat, hydrology, and chemistry with different natural update rates.

These are **not** solved by giving each Plugin an arbitrary clock — that hands the clock to the component SCR-F §6 exists to contain. What is needed is a small closed set of Reactor-offered execution models (fixed-step synchronous; fixed-step phased; scheduled external inputs; bounded delayed effects; multi-rate phases with deterministic ordering). That is DEC-3's work.

> **The rule for this batch: no Lab invents its own temporal workaround.**

## I.6 Geometry families

Snow crystals settle a question that looked exotic and is not. **Six-fold symmetry is crystallography, not decoration** — and a hexagonal arrangement is therefore *more* faithful than a square one, not a special case.

The general lesson: **Grid World must not mean Cartesian grid.** The platform should support named lattice geometries — square, triangular, hexagonal, layered 3-D — or general local spatial graphs. Hard-coding square adjacency would make lattice anisotropy indistinguishable from physical anisotropy, which is fatal in any Lab whose measured output is a morphology (Snow, and later Dendrites, Biofilms, Fracture).

## I.7 The helper boundary

Melt ponds force this and it is the sharpest architectural constraint in the batch. Connected water shares one surface level; no strictly local rule computes that. The honest response is a Reactor-provided helper — but helpers are how whole domain models get smuggled into the core.

> **A helper may provide a generic execution primitive. It may not provide a domain-specific answer.**

*Connected-component equalization* is plausibly generic enough. *Melt-pond hydrology solver* is not. *Global geometric visibility* (coastal shadowing) is a genuine borderline case and should be decided deliberately rather than by whoever implements Coastal first.

The Plugin must never be handed arbitrary global geometry access. If a Lab needs a global calculation, it belongs to the World or Reactor as a **declared** capability, visible in provenance.

## I.8 Standing has four axes

A single grade compresses too much. Every Lab below reports four separately:

- **Mechanism fit** — does the local-state abstraction make sense?
- **Validation class** — *direct experimental* / *direct observational* / *indirect statistical* / *qualitative only*. These must never look equivalent in Search.
- **Rediscovery risk** — low / medium / high. Is the canonical local-rule model already known?
- **Practical need** — would anyone use the resulting mechanism catalogue?

## I.9 Lab roles

Not every Lab justifies itself with new domain science. Declaring the role up front is more credible than selling every Lab as a research frontier:

- **Calibration anchor** — good ground truth, used partly to prove SCR's evidence chain.
- **Rediscovery benchmark** — a canonical local-rule model exists; SCR should be able to recover something like it.
- **Architecture stress test** — forces the platform to confront a capability it lacks.
- **Mechanism-supply candidate** — a specific under-explored interaction problem.
- **Integrity demonstrator** — exercises the platform's honesty machinery.

**A Lab can be commercially weak and architecturally essential.** Four in this batch are.

## I.10 Visualization credibility class

A visual can be accurate as a rendering and misleading as a product claim. Each Lab reports a class:

- **Class 1 — mistakable for an operational forecast.** *Wildfire, Coastal, Permafrost.*
- **Class 2 — mistakable for scientific significance it does not have.** *Snow Crystals.*
- **Class 3 — low hazard.** *Karst, Melt Ponds, River, Dune, Landslide, Smouldering.*

The Snow Crystal Lab supplies the phrase worth keeping platform-wide:

> **Beauty is the failure mode.**

## I.11 The claim SCR should refuse to make

Wolfram's Principle of Computational Equivalence holds that most non-trivial systems are equivalently sophisticated computationally. **SCR should decline to lean on it**, and the refusal costs nothing.

If everything is equivalently irreducible, SCR loses the ability to say some Labs fit better than others — which is precisely the discrimination SCR-F §30 exists to make, and precisely the discrimination that makes this report useful.

The weaker, defensible claim is the selection rule the Wildfire brief already stated:

> **What predicts fit is not computational class. It is whether adjacency in the model corresponds to adjacency in the world — and fit degrades in proportion to how far the true interaction topology departs from the declared Layout.**

That is falsifiable. PCE is not.

---

# Part II — The ten Labs

Each entry opens with a header block, then covers the phenomenon, the established shortcut, the irreducible remainder, the Cell state, and an assessment. Assessments are **my judgment, explicitly labelled, carrying no standing** — they are not fit reviews and do not promote any entry (SCR-F §30).

---

## Lab 1 — Wildfire

| | |
| :--- | :--- |
| **Role** | Calibration anchor · mechanism-supply candidate |
| **Standing** | [strong], inherited from *A Card Catalog for Emergence* v0.1 §5; not re-derived |
| **Falsifiable question** | Which local interaction rules produce junction acceleration or spotting-driven pattern change under *fixed* wind forcing? |
| **Validation class** | Direct observational (mapped perimeters), plus operational-model comparison |
| **Rediscovery risk** | Low — lattice fire models exist but are not the operational incumbent |
| **Reach class** | Neighbour-local, plus bounded transport for embers |
| **Driver class** | Wind and terrain as **external input**; fire–atmosphere coupling as **interactive mechanism** |
| **Geometry** | Square grid, with anisotropy correction mandatory |
| **Visual credibility** | **Class 1** — mistakable for a fire behaviour forecast |
| **Platform pressure** | Bounded transport · external input vs coupling · dimensional time mapping · lattice anisotropy |

**The phenomenon.** Fire moves as a front: fuel ignites, burns, is consumed; heat passes by contact and short-range radiation; wind and slope bias direction. Landscape-scale front shape, fingering, unburnt islands, self-extinction, and spotting follow from local transitions repeated.

**The established shortcut.** **Rothermel (1972)** gives a quasi-empirical steady-state rate of spread from fuel bed properties, moisture, wind, and slope [1] — the most widely used wildfire behaviour tool in the world, embedded in dozens of operational systems [2]. **FARSITE** grows a perimeter by treating each perimeter vertex as the source of an elliptical wavelet dimensioned by Rothermel — Huygens' principle applied to fire [3]. Dead fuel moisture is not one number: it is tracked in 1-, 10-, 100-, and 1000-hour timelag classes with different response rates [D]. Separately, the **Drossel–Schwabl** lattice fire model (1992) is a canonical self-organized-criticality object producing power-law cluster size distributions [4] — established physics, and not a fire behaviour model.

**Reducible.** Steady spread through homogeneous fuel under steady wind on uniform slope. Perimeter growth under a prescribed wind field. Whether fire percolates through random fuel at a given density. Long-horizon fire-size distributions. In all four, SCR would be rediscovering closed forms — usefully as calibration, worthlessly as contribution.

**Irreducible.** Heterogeneity near the percolation threshold, where whether the fire crosses depends on the specific fuel arrangement — and real landscapes sit near-critical constantly, which is what fuel breaks are for. Junction fires, where two merging fronts accelerate beyond either front's predicted spread rate. Path dependence in burnout: which islands survive depends on the order in which the front reached their edges.

**The line this Lab must draw — the critique's sharpest point on Wildfire.** Once fire alters wind strongly, a local CA may no longer be the right abstraction at all. The fit review must separate three regimes:

1. local front mechanisms under **prescribed or weakly coupled** wind — defensible;
2. **reduced two-way coupling** SCR can represent honestly — the open question;
3. **full fire–atmosphere dynamics** requiring CFD — outside SCR.

"Candidate mechanism supply" must not become a license to imitate plume physics with arbitrary local heuristics.

**Cell state.** *Persistent:* remaining fuel, moisture, burn state, accumulated pre-heat. *Derived or World-static:* slope (static terrain data, not mutable state). One mechanism generalizes: fuel drying under neighbour heat but not yet ignited is computationally live and visually inert — SCR-F §38.6 as a domain fact, and the cleanest instance in this batch.

**Assessment.** *(judgment, no standing)* Mechanism fit high; validation direct-observational and genuinely good; rediscovery risk low; practical need real. The strongest all-around Lab in the batch and the batch's calibration anchor. The upside is specific: fire science has a gap between fast models that prescribe the wind field and expensive coupled simulations nobody runs at scale, and candidate local rules for regimes where the fast models are known to fail is defensible upstream work — provided regime 3 above stays out of bounds.

---

## Lab 2 — Smouldering and Peat Fire

| | |
| :--- | :--- |
| **Role** | Integrity/architecture demonstrator (hidden state) · weak mechanism-supply |
| **Standing** | Ungraded |
| **Falsifiable question** | What local rules for depth-resolved moisture and heat produce re-emergence far from the ignition point? |
| **Validation class** | **Qualitative only** at depth; direct experimental at laboratory scale |
| **Rediscovery risk** | Low — no canonical lattice model |
| **Reach class** | Neighbour-local in three dimensions |
| **Driver class** | Weather as **external input**; peat consumption altering drainage as **interactive mechanism** |
| **Geometry** | Layered 3-D — see below |
| **Visual credibility** | Class 3 |
| **Platform pressure** | Depth resolution · extreme scale span · hidden state views |

**The phenomenon.** Smouldering is flameless, oxygen-limited combustion on porous fuel, propagating at centimetres per hour, downward and sideways through the ground. It survives conditions that extinguish flame — rain, snow, winter — and re-emerges months later; boreal overwintering fires do exactly this. The surface can look cool and green while a front advances a metre below.

**The established shortcut.** The physics is a heat balance: exothermic char oxidation against conduction, radiation, and the latent heat of evaporating fuel moisture. Everything turns on moisture content as a fraction of dry mass, and there is a hard threshold: **smouldering ignition requires moisture below 125 ± 10% dry base** [24]. Critically, *once ignited*, a self-sustained front can dry and propagate through layers wetter than that limit [24] — a hysteresis that matters. Mineral content acts as a heat sink; bulk density controls both oxygen supply and thermal inertia non-monotonically. The consequences are not small: the 1997 Indonesian peat and forest fires released an estimated **0.81–2.57 Gt C, 13–40% of mean annual global fossil fuel emissions** [23].

**Reducible.** One-dimensional steady front velocity through homogeneous fuel. Whether a given fuel can smoulder at a given moisture and density. Total carbon released given burn depth and area.

**Irreducible.** Path selection through heterogeneous subsurface moisture — a percolation-like search whose route decides where the fire surfaces. Re-emergence location, which requires following the subsurface path. Overwintering, a marginal heat balance integrated over months of hostile conditions. Coupling back to hydrology as burnt peat lowers the surface and changes drainage.

**Correction from the first pass.** The first pass asserted "3D or nothing." That is rhetorically strong and analytically lazy. Three representations must be distinguished before the fit review, because a reduced one may be scientifically honest for some questions:

- **true volumetric 3-D** — required for re-emergence path questions;
- **layered 2.5-D** — plausibly sufficient for depth-of-burn and carbon questions;
- **reduced depth columns with lateral coupling** — sufficient for landscape-scale burn extent.

Making full volumetric simulation a precondition would foreclose testing whether the simpler abstractions preserve the mechanism of interest.

**Cell state.** *Persistent:* organic mass remaining, moisture fraction, temperature or accumulated heat, combustion state. *Static:* mineral fraction, bulk density. *Derived:* oxygen availability (from local porosity and burn state).

**Assessment.** *(judgment, no standing)* Mechanism fit good; **validation qualitative only** and structurally unlikely to improve, since subsurface fronts cannot be instrumented at the resolution a model would need; rediscovery risk low; practical need real but the audience is small. **Classify primarily as architecture and integrity value.** This is the cleanest hidden-state demonstrator in the catalog: a Run where the surface view shows nothing and the state view shows an advancing front is a two-frame argument for SCR-F §38.6, on a domain where the confusion kills people who declare fires out.

---

## Lab 3 — Landslide and Debris Flow

| | |
| :--- | :--- |
| **Role** | Mechanism-supply candidate (narrow) |
| **Standing** | Ungraded |
| **Falsifiable question** | Does local load transfer improve the spatial and size statistics of failures beyond uncoupled susceptibility mapping? |
| **Validation class** | **Indirect statistical** — post-storm inventories, strong spatial statistics |
| **Rediscovery risk** | Medium — the sandpile precedent exists and is physically unfaithful |
| **Reach class** | Neighbour-local (contested — see below) |
| **Driver class** | Rainfall and shaking as **external input** |
| **Geometry** | Square grid |
| **Visual credibility** | Class 3 |
| **Platform pressure** | Continuum stress vs neighbour transfer · rare discrete events under uniform stepping |

**The phenomenon.** A slope holds until it does not, and the failed mass loads what is below it. At one extreme a single slump; at the other a debris flow that entrains material and travels kilometres. The population-level fact is as interesting: landslide areas from a triggering event are well described by a three-parameter inverse-gamma distribution — a power-law decay with exponent about **−2.40** for medium and large slides, and an exponential **roll-over** at small areas [5].

**The established shortcut.** The **infinite-slope factor of safety** — cohesion, friction angle, slope, pore pressure combined into one ratio — is what practising engineers use, and coupled to a hydrological model it becomes the operational susceptibility tool (the SHALSTAB/SINMAP lineage) [D]. Runout distance is predicted from volume by empirical angle-of-reach relations [D].

**The precedent that must be confronted first.** The **Bak–Tang–Wiesenfeld sandpile** (1987) is the founding model of self-organized criticality and the reason anyone reaches for a cellular model here [6]. But laboratory granular piles largely failed to reproduce clean SOC: the rice-pile experiments found power-law avalanches **only for elongated grains**, with rounded grains showing a characteristic scale [8]. That result showed SOC is not insensitive to system details — its occurrence depends on the mechanism of energy dissipation. **The sandpile is a good theory of criticality and a poor theory of sand.** A Lab here must open by distinguishing itself from BTW rather than borrowing its glamour.

**Reducible.** Whether a *given* slope with known properties fails — arithmetic, and notably a **per-cell calculation with no interaction at all**. Susceptibility mapping. Runout from volume. Regional magnitude–frequency.

**Irreducible.** Load transfer cascades, where a failing block loads neighbours and whether that arrests depends on the arrangement of marginal cells. Progressive failure and strain softening, a non-monotone feedback the static factor-of-safety calculation cannot represent by construction. Entrainment, where runout depends on path and path depends on runout. Rainfall sequencing, where identical totals in different order produce different failure populations.

**The claim this Lab must choose — the critique's harshest point.** Stress redistribution in real slope materials depends on geometry, constitutive behaviour, and continuum mechanics. A local transfer rule may be a useful toy mechanism, a defensible reduced model, or physically misleading. **The Lab must state which claim it is making, before it runs anything.** The narrow, defensible version: SCR's entire potential contribution is the *coupling term*, because the incumbent is a non-interacting per-cell calculation.

**Cell state.** *Persistent:* saturation or pore pressure, accumulated load from upslope failures, failure state, accumulated damage. *Static:* slope, cohesion, strength. *Derived:* factor of safety.

**Assessment.** *(judgment, no standing)* Mechanism fit **contested** — the stress non-locality objection is real and shared with Fracture (#31); validation indirect-statistical but with genuinely good inventory data; rediscovery risk medium; practical need real. **Plausible only if narrowly targeted at cascade structure rather than general slope stability.**

---

## Lab 4 — Dune and Ripple

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · architecture stress test (bounded transport) |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Can Generation recover a Werner-class mechanism family from a semantic request, without being handed the implementation? |
| **Validation class** | **Direct observational** — satellite imagery of dune fields worldwide |
| **Rediscovery risk** | **High** — the canonical model exists and is excellent |
| **Reach class** | **Bounded transport** — the defining case |
| **Driver class** | Wind regime as **external input** |
| **Geometry** | Square grid with directionally asymmetric connections |
| **Visual credibility** | Class 3 |
| **Platform pressure** | **Bounded transport (the reach question)** · two-scale mechanism separation |

**The phenomenon.** Wind moves sand in hops — saltation. Out of that come structures at two widely separated scales: **ripples**, centimetres apart, forming in minutes; and **dunes**, tens to hundreds of metres, migrating over years. Dune types classify by wind regime — barchans under unidirectional wind, linear under bimodal, star under multidirectional.

**The established shortcut.** **Bagnold (1941)** established the physics of blown sand, saltation thresholds, and transport rate scaling [D]. **Werner (1995)** introduced the first cellular-automaton dune model: sand slabs on a lattice, picked up and moved downwind a fixed distance (typically five sites), deposited with probability depending on whether the landing site is already sandy, plus an avalanche rule enforcing the angle of repose [7]. That handful of rules reproduces barchans, transverse, linear, and star dunes in three dimensions [7]. Ripple wavelength at onset follows from saltation trajectory length via linear stability [D]; dune migration speed is inversely proportional to height [D].

**Reducible.** Saltation threshold, transport rate, initial ripple wavelength, dune celerity, and the wind-regime-to-dune-type classification. A CA reproducing these has reproduced textbook content.

**Irreducible.** Pattern coarsening — dune fields do not settle at the initially selected wavelength; spacing grows through a history of merges and splits. Dune collisions, where the outcome (absorption, breeding, ejection) depends on size ratio and offset. Barchan field persistence, unexplained by the single-dune solution. Sand supply, vegetation, and topography.

**The split, resolved in the weaker form.** The critique proposed splitting this into a Ripple Lab and a Dune Lab. **Adopted as one Lab with two declared mechanism classes and two time fits**, because the danger the critique identified is real — one Plugin contract must not be forced to explain both instabilities merely because the words share a domain — but a standalone Ripple Lab has almost no content of its own. Declaring the pairing explicitly closes the hazard at lower cost.

**Cell state.** *Persistent:* sand height or slab count. *Derived:* local slope, shadow state (both computable from height). This is the smallest state in the batch — Werner's model runs on height plus rules.

**Assessment.** *(judgment, no standing)* Mechanism fit excellent; validation direct-observational and free; **rediscovery risk high**; practical need low. **Role is benchmark, not frontier — and that is a legitimate role.** Its architectural value is disproportionate: dune fields are one of the few natural systems where a non-local transport hop is *physically correct*, so this Lab is the honest test of whether SCR can express bounded transport without collapsing into a general simulator. That answer matters to wildfire spotting, ecological dispersal, and scanning worms.

---

## Lab 5 — Coastal Erosion

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · architecture stress test (global-read boundary) |
| **Standing** | Ungraded |
| **Falsifiable question** | In the high-angle unstable regime, which local transport rules reproduce observed cape spacing and spit geometry? |
| **Validation class** | **Direct observational** — satellite shoreline time series, century of aerial photography |
| **Rediscovery risk** | Medium-high in the unstable regime |
| **Reach class** | Neighbour-local for transport; **global read** for shadowing unless mediated |
| **Driver class** | Wave climate as **external input** |
| **Geometry** | Plan-view grid (2-D) or shoreline curve (1-D) — different Worlds |
| **Visual credibility** | **Class 1** — retreat past rendered property is the batch's most consequential misreading |
| **Platform pressure** | **Helper boundary for visibility geometry** · severe scale span |

**The phenomenon.** Waves at an angle drive sand along the shore; convergence builds, divergence erodes. Over decades this builds spits and capes, migrates barrier islands, and opens inlets. A storm can breach an island overnight; ordinary drift reshapes a coast over a lifetime.

**The established shortcut.** The CERC equation relates alongshore sediment flux to breaking wave height and wave-shoreline angle; with sediment continuity it gives the "one-line" shoreline model, the coastal engineering workhorse [D]. Shoreline retreat under sea-level rise is predicted by the **Bruun rule** — and a Lab here must know that its criticism is mainstream, not fringe: Cooper and Pilkey (2004) argued it has no predictive power and should be abandoned [10], and more recent work recommends limiting its use for policy [10].

**The cellular precedent is excellent and under-appreciated.** Ashton, Murray and Arnoult (2001) showed that when waves approach at sufficiently large angle, the standard transport relation makes a straight shoreline **unstable** — perturbations grow, and a simple cellular model spontaneously produces capes, spits, and cuspate forelands resembling the Carolina capes [9]. That is a first-rate case of a simple local rule generating large-scale geomorphology previously attributed to inherited geology. *(The third author's name was misspelled "Arnault" in the original and corrected by erratum [9a] — the first pass reproduced the error.)*

**Reducible.** Transport rate from wave conditions. Shoreline change in the **low-angle** regime, where the system is diffusive, perturbations decay, and a straight coast stays straight. Equilibrium beach profiles. Volume budgets.

**Irreducible.** The high-angle regime: instability growth tells you the coast becomes unstable, not what you get. Which features survive, at what spacing, and whether capes merge is nonlinear. Breaching, a discrete threshold event that permanently changes connectivity. Storm sequencing, where recovery between events is incomplete.

**The architectural point.** Shadowing — a cape blocking waves from reaching the coast behind it — is not a "strain on locality." Depending on implementation it is a **global geometric visibility calculation**, which is the fifth reach class. If it is needed, it belongs to the World or Reactor as a declared capability, never as arbitrary global access granted to a Plugin. Whether visibility is *generic enough* to be a helper (§I.7) is a genuine open question and this Lab is where it must be answered.

**Cell state.** *Persistent:* sediment volume or shoreline position, barrier or dune state. *Static:* elevation, sediment type. *Derived:* shadow state, local shoreline orientation.

**Assessment.** *(judgment, no standing)* Mechanism fit good in the unstable regime; validation direct-observational and unusually strong; rediscovery risk medium-high; practical need high and rising. Stronger than the catalog entry's framing as a time-fit stress test suggests, because it has what most of Family A lacks: **a documented case where a simple local rule overturned a domain assumption.** Requires unusually strict visualization labelling.

---

## Lab 6 — River Braiding

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · calibration candidate |
| **Standing** | Ungraded |
| **Falsifiable question** | Which local rule structures control avulsion timing and channel capture? |
| **Validation class** | **Direct experimental** (flume) **and direct observational** (satellite) — the strongest stack in the batch |
| **Rediscovery risk** | **High** |
| **Reach class** | Neighbour-local with state-dependent connection weights |
| **Driver class** | Discharge and sediment supply as **external input**; bed evolution as **interactive mechanism** |
| **Geometry** | Square grid |
| **Visual credibility** | Class 3 |
| **Platform pressure** | **Dynamic connection strength vs dynamic connection existence** |

**The phenomenon.** A river carrying more sediment than it can move deposits some; the deposit splits the flow; the split channels deposit and split again. The result reorganizes continuously — even under constant discharge and sediment supply. That restlessness under steady forcing is the phenomenon.

**The established shortcut.** Whether a river braids at all has a reduced answer: the **Leopold–Wolman** slope–discharge threshold (1957) separates braided from meandering channels, with braided rivers steeper at the same discharge [11]. Sediment transport has empirical formulas (Meyer-Peter–Müller and descendants) [D]. Hydraulic geometry relations give equilibrium channel form [D].

**The cellular precedent is a landmark.** **Murray and Paola (1994)** routed water downslope across a grid of bed elevations by simple discharge-partitioning rules, transported sediment as a nonlinear function of local discharge, and updated the bed — producing braiding, bar formation, migration, and avulsion [12]. Their conclusion is the load-bearing one: *the only factors essential for braiding are bedload transport and laterally unconstrained free-surface flow* [12]. A landform previously explained through detailed fluid mechanics falls out of local rules.

**Reducible.** Braided-versus-meandering classification. Bulk sediment flux. Equilibrium channel geometry. Average braiding intensity.

**Irreducible.** Avulsion — when and where a channel abandons its course, a threshold crossed by accumulated deposition history, with no formula for the date or the location. Bar and channel identity, decided by small differences amplified through flow partitioning. Bifurcation instability, where small asymmetries grow and one branch captures the flow. Response to changed supply over years.

**The reusable phrase this Lab contributes:** *classification is reducible, realization is not.*

**Correction from the first pass.** The first pass said connections are directed and the direction depends on state, implying a changing graph. That is probably the wrong abstraction and it would make dynamic connections far more complicated than necessary. **Distinguish dynamic connection *existence* from dynamic connection *strength or direction*.** In a grid, all adjacent edges can exist permanently while the Reactor or Plugin computes which carry flow, from elevation. Only the second is needed here.

**Cell state.** *Persistent:* bed elevation, sediment availability. *Derived:* water depth, discharge share, flow direction — all computable from elevation and routing, and storing them would hide mechanism complexity in state.

**Assessment.** *(judgment, no standing)* Mechanism fit excellent; **validation the strongest in the batch** — flume experiments reproduce braiding at tabletop scale under controlled conditions, *and* satellite imagery gives multi-decade time series of real braid plains, *and* a canonical cellular baseline exists to compare against; rediscovery risk high; practical need modest with a small audience. A superb platform benchmark with one real open question (avulsion timing) attached.

---

## Lab 7 — Karst Dissolution

| | |
| :--- | :--- |
| **Role** | Architecture stress test (Network World) · sensitivity demonstrator |
| **Standing** | Ungraded |
| **Falsifiable question** | Which local competition rules produce observed conduit network topology statistics from plausible fracture populations? |
| **Validation class** | **Qualitative only** — direct observation structurally unavailable |
| **Rediscovery risk** | Low |
| **Reach class** | **Path-local** — influence follows the fracture graph |
| **Driver class** | Recharge and base level as **external input**; aperture widening as **interactive mechanism** |
| **Geometry** | **Network** — inherited fracture geometry, not a lattice |
| **Visual credibility** | Class 3 |
| **Platform pressure** | **Network World** · extreme time horizon |

**The phenomenon.** Water charged with carbon dioxide dissolves limestone. It enters through a dense network of nearly identical hairline fractures. Over 10⁴ to 10⁶ years, a handful become caves and the rest become nothing. That selection is the phenomenon.

**The established shortcut, and it is counterintuitive.** Calcite dissolution is first-order far from equilibrium but switches near saturation to a **slow fourth-order rate law**, F ∝ (c_eq − c)⁴ [13]. The consequence, developed by Dreybrodt and colleagues, is that nearly-saturated water dissolves slowly rather than stopping, penetrating deep into a fracture while still slightly aggressive and widening it along its whole length. Without that nonlinearity, caves would not form. With it, there is a **breakthrough time** after which flow increases dramatically through positive feedback, and analytical expressions for it exist; depending on fracture length and hydraulic gradient, breakthrough ranges from **10⁴ to several 10⁶ years** [13].

**Reducible.** Breakthrough time for a single fracture of known geometry under known gradient. Whether a water chemistry is aggressive. Bulk dissolution rate. Onset of the reactive-infiltration fingering instability, which is a linear stability question.

**Irreducible.** Which fracture wins — the domain's defining question. Network topology: whether the result is a single trunk, a maze, or a dendritic pattern. Capture events, where one conduit intersects another and steals its flow, abruptly changing the whole system's hydraulics. Base level changes moving the outlet during formation.

**Correction from the first pass — and it applies catalog-wide.** The first pass treated extreme sensitivity to tiny initial differences as sufficient evidence of computational irreducibility. **It is not.** A system can be highly sensitive and still admit useful reduced statistical predictions. The defensible claim, which is enough:

> Exact conduit realization depends on the iterated competition among fractures and cannot be obtained from the single-fracture breakthrough shortcut.

No philosophical claim is needed and none should be made.

**Cell state.** *Persistent:* aperture or void fraction, water saturation state relative to equilibrium. *Static:* rock solubility, initial fracture geometry. *Derived:* local flow (from aperture and gradient).

**Assessment.** *(judgment, no standing)* Mechanism fit excellent and the strongest **Network World** argument in the batch — using a grid here would be actively dishonest, since dissolution follows joints and bedding planes inherited from tectonics. But **validation is qualitative only and will not improve**: nobody will watch a cave form, and cave surveys are biased toward passages humans can enter. Rediscovery risk low; practical need small and academic. **Keep for architecture and demonstration value; weak candidate for early external validation.**

---

## Lab 8 — Permafrost Thaw

| | |
| :--- | :--- |
| **Role** | Mechanism-supply candidate (strongest in the batch) |
| **Standing** | Ungraded |
| **Falsifiable question** | What local coupling rules produce the wetting-versus-draining connectivity transition under fixed warming? |
| **Validation class** | **Direct observational** — InSAR subsidence, multi-decade imagery, documented polygon succession |
| **Rediscovery risk** | Low — no canonical lattice model |
| **Reach class** | Neighbour-local |
| **Driver class** | Warming as **external input**; drainage reorganization as **interactive mechanism** |
| **Geometry** | Grid, with inherited polygon structure as a World template |
| **Visual credibility** | **Class 1** — mistakable for a climate projection |
| **Platform pressure** | Connectivity transitions · season-to-century scale span · inherited geometry |

**The phenomenon.** Frozen ground contains ice; when it thaws the ice volume is lost and the surface **collapses**. Thermokarst is not gradual warming but abrupt, localized subsidence producing pits, troughs, and thaw lakes. Depressions collect water, which conducts heat better than air and absorbs more radiation, so they thaw faster — *or* connected troughs drain the surface and dry it, slowing thaw. Which happens is a connectivity question.

**The established shortcut.** Vertical thaw depth has a closed form: the Stefan solution gives thaw depth growing as the square root of accumulated degree-days [D]. Regional carbon feedback is carried in land-surface models at coarse scale.

**The gap, stated carefully.** The first pass claimed abrupt thaw is under-represented in models generally. The safer and now-citable claim: Turetsky et al. (2020) state that **large-scale models currently simulate only gradual changes in seasonally thawed soil**, and estimate that abrupt thaw will occur in **under 20% of the permafrost zone but could affect half of permafrost carbon** [15]. That is a specific, sourced, defensible statement of the gap, and it should replace the general one.

**The observational anchor.** Liljedahl et al. (2016) documented pan-Arctic ice-wedge degradation since 1950 across ten localities, and described exactly the sequence this Lab is about: **initial thaw drains polygon centres and forms disconnected troughs holding isolated ponds; continued melting increases trough connectivity and drains the landscape overall** [14]. The connectivity transition is not hypothesized — it is observed.

**Reducible.** One-dimensional thaw depth from surface temperature. Bulk carbon release given thawed volume and carbon density. Equilibrium permafrost extent for a given climate.

**Irreducible.** Drainage connectivity — a percolation transition whose crossing flips the landscape between wetting and drying trajectories with opposite carbon consequences. Neighbour-driven thaw, where a collapsed cell warms its neighbours and thaw spreads laterally, which no column model represents. Thaw lake lifecycle, including catastrophic drainage when a lake intersects a drainage path. Irreversibility: ice lost is not recovered, so the system has memory the forcing does not.

**Cell state.** *Persistent:* ice content, thaw depth, surface elevation, water accumulation, soil carbon. *Derived:* albedo (from water and vegetation state), thermal conductivity.

One subtlety worth stating: polygonal cracking is **inherited geometry**, not emergent from this mechanism. It has its own pattern-formation literature and conflating the two would misrepresent the domain — it belongs as a World template.

**Assessment.** *(judgment, no standing)* Mechanism fit good; **validation direct-observational and the best in the batch for a climate-adjacent domain** — subsidence, lake area, and trough connectivity are all directly measurable; rediscovery risk low; practical need high. The scientific gap is real and sourced. **Strong candidate for an early serious Lab, with unusually strict non-claim and visualization controls** — output will be read as a carbon-feedback projection, and the topic is publicly charged.

---

## Lab 9 — Sea-Ice Melt Ponds

| | |
| :--- | :--- |
| **Role** | Architecture stress test (connected-region constraint) · mechanism-supply candidate (narrow) |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | What local rules reproduce pond morphology when the ice substrate itself evolves and drainage can reset the system? |
| **Validation class** | **Direct observational** — hundreds of thousands of measured ponds |
| **Rediscovery risk** | Medium — statistical physics has the headline result |
| **Reach class** | **Connected-region constraint** — the defining case |
| **Driver class** | Melt forcing as **external input**; ice ablation under ponds as **interactive mechanism** |
| **Geometry** | Grid |
| **Visual credibility** | Class 3 (Class 1 if framed as albedo feedback) |
| **Platform pressure** | **Helper boundary** — connected-component level equalization |

**The phenomenon.** Arctic sea ice melts from the top; meltwater collects in depressions. Ice is bright, ponded water dark, so a pond warms, deepens, and grows while surrounding ice stays bright. Pond fraction is therefore a dominant control on summer Arctic solar absorption. Early ponds are small and round; later they elongate, connect, and — once connected to the floe edge or a drainage hole — drain abruptly, resetting albedo.

**The established shortcut.** Analysis of area–perimeter data from hundreds of thousands of ponds found an unexpected separation of scales: pond **fractal dimension transitions from 1 to 2 around a critical area of 100 m²** [16]. This is read as a percolation transition — small ponds are isolated clusters, large ponds are the connected cluster. Lattice modelling followed: a two-dimensional **random field Ising model** identifies ponds as metastable states and exhibits a second-order phase transition from isolated to clustered ponds [17].

**Reducible.** Albedo from pond fraction — a weighted average. Flooded area from a fixed topography and water volume — a level-set calculation with no dynamics. Percolation threshold and near-critical size-distribution scaling — **universal exponents, tabulated in advance.** That last point cuts against the Lab: if the phenomenon is a percolation transition, reproducing its statistics demonstrates only membership in a universality class (§I.1).

**Irreducible.** The **evolving substrate** — ice topography is not fixed; ponds ablate the ice beneath them, so the occupation probability is a function of the pattern's own history, which is exactly what static percolation assumes away. Drainage events, which reset the system on a threshold crossing over a heterogeneous field. Refreezing lids, which change albedo without changing pond extent — hidden state again. Melt-through, a different regime.

**The architectural point this Lab owns.** Water finds level: a connected pond has one surface elevation throughout, however large. No strictly local rule computes that. This may reveal a useful class of **declared physical constraints the Reactor solves deterministically** — but the boundary must hold: *connected-component equalization* is plausibly a generic execution primitive; *a melt-pond hydrology solver* is a domain answer smuggled into the core (§I.7).

**Cell state.** *Persistent:* ice thickness or surface elevation, water depth, frozen-lid state. *Derived:* albedo, drainage connectivity, pond membership.

**Assessment.** *(judgment, no standing)* Mechanism fit good with a named architectural dependency; **validation direct-observational and quantitative** — pond size distributions, fractal dimension, and pond fraction are all measured and published; rediscovery risk medium; practical need real but the field is small and already occupied by capable people with the right tools. The opening SCR has is narrow and specific — the co-evolving substrate, which percolation universality does not cover — and the first pass was right to attack its own value proposition here.

---

## Lab 10 — Snow and Crystal Growth

| | |
| :--- | :--- |
| **Role** | Integrity demonstrator · rediscovery benchmark |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Which local attachment and noise mechanisms reproduce measured sidebranch statistics or degree of six-fold symmetry? |
| **Validation class** | **Direct experimental** — controlled-chamber growth at known conditions |
| **Rediscovery risk** | **High** |
| **Reach class** | Neighbour-local |
| **Driver class** | Vapour field as **interactive mechanism** (the crystal depletes what it reads) |
| **Geometry** | **Hexagonal/triangular — physical, not exotic** |
| **Visual credibility** | **Class 2** — beauty is the failure mode |
| **Platform pressure** | **Named lattice geometries** · aesthetic distraction |

**The phenomenon.** A snow crystal grows by vapour deposition. A protruding tip intercepts more diffusing molecules than a flat face, grows faster, and protrudes more. That instability produces branches, and repeated, sidebranches. The result spans plates, columns, needles, sectored plates, capped columns, and dendrites.

**The established shortcut.** The **Nakaya morphology diagram** maps habit against temperature and supersaturation — small plates and stars near 0 to −3 °C, needles and columns from −3 to −10 °C, plates at low supersaturation and branched forms at high from −10 to about −22 °C [18]. The **Mullins–Sekerka** analysis (1964) gives the linear stability condition for a growing interface, and solvability theory shows that crystalline anisotropy selects a unique tip operating point — without anisotropy there is no dendrite, only unstable fingers [D]. **Diffusion-limited aggregation** (Witten and Sander, 1981) is the minimal lattice model of the same instability [D].

**The cellular precedent is exceptional.** **Gravner and Griffeath (2009)** built a three-dimensional mesoscopic cellular model based on vapour diffusion, anisotropic attachment, and a boundary layer, and faithfully replicated most observed snow-crystal morphology — an unusual achievement for a mathematical model, and a spectacular demonstration of the expressive power of cellular automata [19].

**Correction from the first pass.** "Read the diagram" oversimplifies. The Nakaya diagram is a strong empirical guide for crystals growing in air near 1 atm [18], but habit depends on more than two idealized variables and the transitions — particularly the alternation of plate and column habits with temperature — remain mechanistically open, addressed by surface-kinetics models [D]. The *diagram* is settled; the *explanation* is not.

**Reducible.** Habit class from temperature and supersaturation, to the diagram's accuracy. Onset of branching. Dendrite tip speed and radius. DLA fractal dimension — universal and measured decades ago.

**Irreducible.** The specific crystal: two grown side by side are not identical, because the growth is an amplifier of fluctuation. Sidebranch statistics — where and how often branches appear along an arm, not given by tip theory, and an active research question. Symmetry: real crystals are often strikingly six-fold although the arms grow independently, and whether local rules reproduce the observed *degree* of symmetry is genuinely open. Habit transitions during growth, which write the atmosphere's history into the crystal.

**The architectural point.** A hexagonal or triangular lattice here is **not an exotic exception** — it is evidence that Grid World must not mean square grid (§I.6). Six-fold symmetry is a property of the ice crystal structure, so the anisotropy is physical rather than artifact. This is the one Lab in the batch where lattice anisotropy is a feature, and it establishes the general requirement.

**Cell state.** *Persistent:* ice or vapour state, attached mass, boundary-layer water. *Derived:* local vapour density gradient, attachment probability.

**Assessment.** *(judgment, no standing)* Mechanism fit superb; **validation direct-experimental and excellent**; **rediscovery risk high**; **practical need very low**. That combination is exactly why the Lab is valuable — as an **integrity test**. This is the domain where beautiful output is most obviously not evidence, and if SCR can run it and say plainly *"this is a lovely picture and it tells you nothing the Nakaya diagram did not"*, the platform has demonstrated the discipline SCR-F §12 and §26 demand, on the hardest case. **Keep as a benchmark and honesty Lab, not as a flagship science opportunity.**

---

# Part III — Cross-Lab findings

## III.1 Regression targets

Four Labs have famous local-rule precedents. **Do not merely cite them — use them.** Each becomes a platform regression question that tests SCR rather than the domain:

| Lab | Benchmark | Regression question |
| :--- | :--- | :--- |
| Dune | Werner (1995) [7] | Can Generation, without being handed the implementation, produce a mechanism family whose behaviour falls in the known morphology classes? |
| River braiding | Murray & Paola (1994) [12] | Same, for braiding from bedload transport plus unconstrained flow. |
| Snow crystals | Gravner & Griffeath (2009) [19] | Same, for the observed habit range. |
| Coastal | Ashton et al. (2001) [9] | Does the high-angle instability emerge, or must it be prescribed? |

Two further tests apply to all four:

- **Search:** when asked for the observed behaviour, does the Corpus retrieve those mechanisms?
- **Negative space:** does the record show *failed* mechanism families, or only noise?

These Labs may tell us more about SCR's quality than about their domains. That is a reason to build them, stated honestly.

## III.2 The strongest falsifiable questions in this batch

Collected from the header blocks, because they are more useful together than apart, and because they should eventually appear near the *top* of each Lab document rather than buried in an upside section:

1. **Wildfire** — which local interaction rules produce junction acceleration or spotting-driven pattern change under fixed forcing?
2. **Landslide** — does local load transfer improve the spatial and size statistics of failures beyond uncoupled susceptibility?
3. **River** — which local rule structures control avulsion timing and channel capture?
4. **Permafrost** — what local coupling rules produce the wetting-versus-draining connectivity transition under fixed warming?
5. **Melt ponds** — what local rules reproduce pond morphology when the substrate evolves and drainage resets the system?
6. **Snow** — which local attachment and noise mechanisms reproduce measured sidebranch statistics or degree of symmetry?
7. **Karst** — which local competition rules produce observed network topology statistics from plausible fracture populations?
8. **Smouldering** — what local rules for depth-resolved moisture and heat produce re-emergence far from ignition?

Each names a measurable quantity and a mechanism class. None says "simulate X."

## III.3 Build priority

Roles and sequencing, **not** scientific worth, and **not** fit grades. Two disagreements with the critique's tiering are stated rather than smoothed over.

**Tier A — build first.**
**Wildfire** (calibration anchor; best combined case). **Permafrost** (real sourced gap, strong data, clean Study structure). **River braiding** (best validation stack in the batch; one real open question).

**Tier B — build for a stated role.**
**Melt ponds** (strong measurable statistics; narrow but real gap; forces the helper boundary). **Coastal erosion** (good instability regime and data; forces the global-read boundary). **Dune** (benchmark and the reach test). **Landslide** (good coupling question, substantial abstraction risk).

**Tier C — architecture and integrity value.**
**Smouldering** (best hidden-state demonstrator; validation qualitative only). **Karst** (Network World stress test; validation unavailable). **Snow crystals** (benchmark and honesty test; very low practical need).

**Disagreement 1 — Melt ponds: Tier B, not Tier A.** The critique places it in Tier A on rigour and measurability, both of which are real. But percolation universality already supplies the headline statistics, so the Lab's contribution is confined to the co-evolving substrate — genuinely narrow — and it carries an unresolved architectural dependency (connected-region levelling) that Tier A Labs should not be blocked on.

**Disagreement 2 — Coastal erosion: higher than the critique's placement implies.** The critique treats it mainly as a shadowing/non-locality caution. It also has the batch's second-best documented case of a simple local rule overturning a domain assumption [9], century-scale shoreline data, and a *named instability threshold* cleanly separating the reducible and irreducible regimes. That is more than a stress test.

## III.4 Feedback to the Decision Registry

The critique's central observation deserves repeating because it is the batch's strongest signal:

> **These are not requirements invented by architecture speculation. The Labs independently demanded them.**

Eight platform questions, plus two additions from `DOC_GOOD_IDEAS.md`:

| # | Question | Raised by |
| :--- | :--- | :--- |
| **P1** | External input versus interactive mechanism versus static condition | Six of ten Labs. **Highest leverage — resolve before DEC-1's full composition model.** |
| **P2** | **Reach classes** — neighbour / bounded transport / path / connected-region / global read | Dune, Wildfire, Coastal, Melt ponds, Karst |
| **P3** | Spatial geometry families — square, hexagonal, triangular, layered 3-D, network | Snow, Karst, Smouldering |
| **P4** | Dynamic connection *existence* versus dynamic *strength or direction* | River braiding |
| **P5** | Multi-rate temporal semantics — a small closed set, not per-Lab workarounds | Whole batch (DEC-3) |
| **P6** | Generic physical helpers versus domain solvers | Melt ponds, Coastal |
| **P7** | Validation standing as a first-class, searchable property | Whole batch |
| **P8** | Visualization credibility class | Wildfire, Coastal, Permafrost, Snow |
| **P9** | **A tenth §30 question: the reducibility audit.** *Where does this domain already have a shortcut?* §30.8 (comparison to established tools) is adjacent but not the same — the established tool may be another simulation. Amending §30 is an SCR-F amendment, so this is a DEC-shaped move, not an edit. | Every Lab, independently |
| **P10** | Reader coverage as a **research finding** rather than a QA metric — where a Reader stops working is the boundary of a discovered pocket of reducibility | `DOC_GOOD_IDEAS.md` §3 |

**P2 is the strongest new DEC candidate.** It is the only one of the five cellular properties (§I.2) not registered anywhere, it constrains the Plugin contract and every Layout family, and four Labs in this batch alone sit on different points of the spectrum.

## III.5 Review checklist

For domain reviewers and for the eventual fit reviews, the fifteen questions the critique proposed, condensed to the eight that bit hardest in this revision:

1. Where is a **reducible** regime being mislabelled as irreducible?
2. Where is **sensitivity** being confused with irreducibility? *(Caught in four Labs.)*
3. Where does a proposed Cell state already **contain the answer** the mechanism claims to discover?
4. Where is a **continuum process** reduced to neighbour transfer beyond scientific defensibility?
5. Which alleged **local rule requires global information**?
6. Which "external field" is actually a **coupled mechanism** — and which supposed coupling is merely an external input?
7. Which Lab would force a **domain-specific solver** into the Reactor?
8. Which Lab's **visualization** would most easily be mistaken for a forecast?

And for outside domain review, the one question worth more than the rest:

> **What sentence here would make a competent practitioner in this field immediately distrust the rest of the document?**

## III.6 What v1 deliberately does not do

Following the critique's §27, and because the remaining fifty Labs will expose the same platform questions from different domains — cross-domain recurrence is the evidence that makes a decision legitimate:

No fit grades. No Reactor model chosen per Lab. No DEC-owned question resolved locally (SCR-F §36.6, F-22). No final Cell properties. No Readers designed. No validation datasets selected. No market positioning. No visualization concepts.

**Do not freeze the architecture before more of the sixty have been seen.**

---

# Part IV — References

Verification status: **[V]** checked against a primary or authoritative source during this revision. **[D]** described generically because no single citation was verified; treat as background, not as a citable claim.

1. **[V]** Rothermel, R. C. (1972). *A mathematical model for predicting fire spread in wildland fuels.* Res. Pap. **INT-115**. Ogden, UT: USDA Forest Service, Intermountain Forest and Range Experiment Station. 40 p. — https://research.fs.usda.gov/treesearch/32533 *(The first pass cited INT-116. Corrected.)*
2. **[V]** USDA Forest Service, Missoula Fire Sciences Laboratory. *The Rothermel Fire Spread Model: A 50-year milestone in fire research* (2022). — https://research.fs.usda.gov/firelab/projects/rothermelfirespread
3. **[V]** Finney, M. A. (1998). *FARSITE: Fire Area Simulator — model development and evaluation.* Res. Pap. RMRS-RP-4. USDA Forest Service. — https://research.fs.usda.gov/download/treesearch/4617.pdf *(Elliptical wavelet propagation from perimeter vertices, after Richards 1990.)*
4. **[V]** Drossel, B. & Schwabl, F. (1992). Self-organized critical forest-fire model. *Physical Review Letters* **69**(11), 1629–1632. — https://link.aps.org/doi/10.1103/PhysRevLett.69.1629
5. **[V]** Malamud, B. D., Turcotte, D. L., Guzzetti, F. & Reichenbach, P. (2004). Landslide inventories and their statistical properties. *Earth Surface Processes and Landforms* **29**, 687–711. — https://onlinelibrary.wiley.com/doi/abs/10.1002/esp.1064 *(Inverse-gamma distribution; power-law exponent −2.40; exponential roll-over at small areas.)*
6. **[D]** Bak, P., Tang, C. & Wiesenfeld, K. (1987). Self-organized criticality: an explanation of 1/f noise. *Physical Review Letters* **59**, 381.
7. **[V]** Werner, B. T. (1995). Eolian dunes: computer simulation and attractor interpretation. *Geology* **23**, 1107–1110. *(Slab transport ~5 lattice sites; deposition probability depends on landing site; reproduces barchan, transverse, linear, star dunes in 3-D.)*
8. **[V]** Frette, V., Christensen, K., Malthe-Sørenssen, A., Feder, J., Jøssang, T. & Meakin, P. (1996). Avalanche dynamics in a pile of rice. *Nature* **379**, 49–52. — https://www.nature.com/articles/379049a0 *(Power-law avalanches for elongated grains only; rounded grains show a characteristic scale.)*
9. **[V]** Ashton, A., Murray, A. B. & Arnoult, O. (2001). Formation of coastline features by large-scale instabilities induced by high-angle waves. *Nature* **414**, 296–300. — https://www.nature.com/articles/35104541
   **9a. [V]** Erratum (2002), *Nature* **415**, 666 — third author's name corrected from "Arnault" to "Arnoult". — https://www.nature.com/articles/415666a *(The first pass reproduced the original misspelling.)*
   See also Ashton & Murray (2006), *J. Geophys. Res. Earth Surface* **111**, parts 1 and 2.
10. **[V]** Cooper, J. A. G. & Pilkey, O. H. (2004). Sea-level rise and shoreline retreat: time to abandon the Bruun Rule. *Global and Planetary Change* **43**, 157–171. — https://www.sciencedirect.com/science/article/abs/pii/S0921818104001195
11. **[V]** Leopold, L. B. & Wolman, M. G. (1957). *River channel patterns: braided, meandering and straight.* USGS Professional Paper **282-B**.
12. **[V]** Murray, A. B. & Paola, C. (1994). A cellular model of braided rivers. *Nature* **371**, 54–57. — https://www.nature.com/articles/371054a0 *("The only factors essential for braiding are bedload sediment transport and laterally unconstrained free-surface flow.")*
13. **[V]** Dreybrodt, W. (1996). Principles of early development of karst conduits under natural and man-made conditions revealed by mathematical analysis of numerical models. *Water Resources Research* **32**(9). — https://agupubs.onlinelibrary.wiley.com/doi/10.1029/96WR01332 *(Fourth-order rate law near equilibrium; breakthrough times 10⁴–10⁶ years.)* See also Dreybrodt (1990), *Journal of Geology* **98**(5).
14. **[V]** Liljedahl, A. K. et al. (2016). Pan-Arctic ice-wedge degradation in warming permafrost and its influence on tundra hydrology. *Nature Geoscience* **9**, 312–318. — https://www.nature.com/articles/ngeo2674
15. **[V]** Turetsky, M. R. et al. (2020). Carbon release through abrupt permafrost thaw. *Nature Geoscience* **13**(2), 138–143. — https://www.nature.com/articles/s41561-019-0526-0 *(Large-scale models simulate only gradual thaw; abrupt thaw in <20% of the zone could affect half of permafrost carbon.)*
16. **[V]** Hohenegger, C., Alali, B., Steffen, K. R., Perovich, D. K. & Golden, K. M. (2012). Transition in the fractal geometry of Arctic melt ponds. *The Cryosphere* **6**, 1157–1162. — https://tc.copernicus.org/articles/6/1157/2012/ *(Fractal dimension transitions from 1 to 2 near a critical area of 100 m².)*
17. **[V]** Ma, Y.-P., Sudakov, I., Strong, C. & Golden, K. M. (2019). Ising model for melt ponds on Arctic sea ice. *New Journal of Physics* **21**. — https://iopscience.iop.org/article/10.1088/1367-2630/ab26db *(Random field Ising model; second-order transition from isolated to clustered ponds.)*
18. **[V]** Nakaya, U. (1954). *Snow Crystals: Natural and Artificial.* Harvard University Press. *(Morphology diagram; applies to crystals growing in air near 1 atm.)* See also Libbrecht, K. G. (2005), The physics of snow crystals, *Reports on Progress in Physics* **68**, 855. — https://www.its.caltech.edu/~atomic/publist/rpp5_4_R03.pdf
19. **[V]** Gravner, J. & Griffeath, D. (2009). Modeling snow-crystal growth: a three-dimensional mesoscopic approach. *Physical Review E* **79**, 011601. — https://pubmed.ncbi.nlm.nih.gov/19257039/
20. **[D]** Mullins, W. W. & Sekerka, R. F. (1964). Stability of a planar interface during solidification of a dilute binary alloy. *Journal of Applied Physics* **35**, 444.
21. **[D]** Witten, T. A. & Sander, L. M. (1981). Diffusion-limited aggregation, a kinetic critical phenomenon. *Physical Review Letters* **47**, 1400.
22. **[D]** Bagnold, R. A. (1941). *The Physics of Blown Sand and Desert Dunes.* Methuen.
23. **[V]** Page, S. E., Siegert, F., Rieley, J. O., Boehm, H.-D. V., Jaya, A. & Limin, S. (2002). The amount of carbon released from peat and forest fires in Indonesia during 1997. *Nature* **420**, 61–65. — https://www.nature.com/articles/nature01131 *(0.81–2.57 Gt C; 13–40% of mean annual global fossil fuel emissions.)*
24. **[V]** Rein, G. et al. (2008), on the critical moisture content for peat smouldering ignition: **125 ± 10% dry base**; once ignited, a self-sustained front can dry and propagate through wetter layers. See also Frandsen (1997). — summarized at https://www.frames.gov/catalog/17735 *(The first pass gave no figure and guessed "a few hundred percent". Corrected.)*
25. **[D]** SHALSTAB / SINMAP lineage of shallow-landslide susceptibility mapping (Montgomery & Dietrich 1994; Pack, Tarboton & Goodwin 1998).
26. **[D]** Dead fuel moisture timelag classes (1-, 10-, 100-, 1000-hour); CERC alongshore transport formula (US Army Corps of Engineers *Shore Protection Manual*); Stefan solution for phase-change front depth; Meyer-Peter–Müller bedload transport.

---

## Non-claims

This report performs no fit reviews and establishes no fit. None of these Labs forecasts, predicts, or assesses anything in any real system. No output described here is suitable for operational, safety, engineering, clinical, environmental, or policy decisions. Mechanisms these Labs would generate are candidate explanations requiring domain validation in domain tooling (SCR-F §41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments in Part II are the author's judgment, carry no standing, and do not promote any entry.
