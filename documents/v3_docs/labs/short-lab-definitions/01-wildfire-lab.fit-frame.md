# 1. Wildfire Lab — Lab Definition

**Document class:** Lab Definition (pre-fit) · **Status:** draft
**Catalog entry:** SCR Lab Catalog v0.1 #1, Family A — Fire, land, and surface processes
**Standing:** **[strong]** — inherited from *A Card Catalog for Emergence* v0.1 §5. Not re-derived here.
**Cites:** SCR-F v0.2 §11, §13.1, §15, §18.5, §30, §41; F-5, F-9, F-17
**Fit review (SCR-F v0.2 §30):** not performed

> **This document does not establish fit.** It frames the nine §30 questions so a fit review has something specific to run against. A Lab may fail that review, and a failure is useful evidence about SCR's boundary (§30, closing). Nothing below asserts that SCR models wildfire usefully.

---

## The phenomenon

Fire moves across terrain as a front. Fuel ignites, burns, and is consumed; heat passes to adjacent material; wind and slope bias the direction of spread. What emerges at landscape scale — front shape, rate of spread, fingering, spotting ahead of the main fire, patchy unburned islands, and self-extinction — is not written into any single ignition event. It follows from many local transitions repeated over time.

This is the platform's **natural calibration anchor**: wildfire is the most established cellular-automaton domain in operational use, which means a Lab here can be checked against something rather than admired in isolation.

## Why a local mechanism is a candidate abstraction here

Fire spread is physically local in a way most domains are not. Combustion propagates by contact and short-range radiant and convective transfer; a cell of fuel does not ignite because of conditions a kilometre away except through the intervening material. Adjacency in the model corresponds to adjacency in the world, which is precisely the property the position paper's selection rule identifies as predicting where this approach degrades gracefully and where it does not.

That correspondence is what a fit review must test (§30.1), not what this document may assume.

## What a Cell would carry

A terrain patch. Candidate declared scalars, all primitive and bounded, which is the §13.1 computational ceiling this Lab appears to clear comfortably:

| Property | Meaning in this domain |
|---|---|
| `fuel` | how much combustible material remains |
| `moisture` | how wet that fuel is |
| `slope` | local terrain gradient |
| `state` | unburnt / burning / burnt |
| `heat` | accumulated energy not yet sufficient to ignite |

The ceiling is worth stating explicitly even where it is easily met, because the honest failure mode of this Lab is not state complexity — it is the *meaning* of those scalars. `moisture` is a single number standing in for fuel-moisture content that real fire science tracks across multiple fuel classes with different response times. Whether that collapse is defensible is a §30.2 question.

## Layout and Connections

**Grid World (§15).** Terrain is spatial; a lattice is the honest arrangement, and this is one of the few Labs where the 2.x grid inheritance is a match rather than an accident (§39). A Connection means physical adjacency, and what passes along it is heat.

Two Layout questions a fit review owns: whether wind requires connections that are directionally asymmetric rather than merely weighted, and whether **spotting** — embers carried far ahead of the front, igniting new fires across unburnt ground — can be expressed as a local mechanism at all, or whether it is exactly the non-local behavior that defines this Lab's boundary. Spotting is named in the catalog entry as a phenomenon of interest, so this is not a hypothetical.

## What one step would mean

Unresolved, and consequential (§30.4). Fire behaviour spans minutes at the front and days across an incident. A step fine enough to represent flame-front advance may make a multi-day burn impractically long; a step coarse enough for the incident makes the front's own dynamics disappear into the step.

Whether this Lab needs anything beyond synchronous lockstep — delayed effect for spotting ignition, for instance — is a **DEC-3** question (§18.5). This document flags it rather than proposing a scheduling contract.

## Candidate mechanisms

Local rules a generator might propose, offered as illustrations of shape rather than as recommendations:

- ignition when accumulated neighbour heat exceeds a moisture-dependent threshold
- fuel consumed per step while burning, extinguishing at exhaustion
- slope and wind biasing which neighbours receive more heat
- moisture decreasing under heat from neighbours before ignition — a **pre-heating** mechanism where the visible state has not changed yet

That last one matters beyond fire. A cell whose `moisture` is dropping while its `state` still reads unburnt looks identical to inert ground in any view keyed to `state` alone. This is §38.6's distinction — a quiet picture is not a stopped computation — and it appears here as a domain fact rather than a platform curiosity.

## What would have to be observed

Candidate domain Readers, owned by this Lab and never by the core (§11):

- front position and rate of spread over time
- front roughness or fingering
- burnt fraction and the size distribution of unburnt islands
- whether extinction occurred, and whether it was patchy or complete
- spotting distance, if spotting can be represented at all

Each needs a definition precise enough to be reproducible and versioned (§21). None exists yet.

## Where this would mislead

The §30.7 question, and the sharpest risk in this Lab: **fire produces convincing pictures.** A plausible-looking front spreading across a rendered landscape invites belief in a way a graph does not, and a Lab whose output looks like a fire-behaviour forecast will be read as one no matter what the caption says.

Specific hazards a fit review should probe: lattice geometry imposing artificial spread anisotropy that a viewer reads as wind effect; rate of spread that is dimensionally meaningless until the step-duration question is settled; and the general case of §41 — a mechanism reproducing an observed pattern is a candidate explanation, never evidence of real-world causation.

## Established tools

Operational fire modelling exists and is calibrated (§30.8). SCR does not compete with it and a fit review must say where SCR stops. The plausible complementary position — untested — is the position paper's: supplying candidate local mechanisms upstream of calibration, not producing forecasts. Any claim beyond that is out of bounds under §41.

## Open decisions bearing on this Lab

- **DEC-1 (mechanism composition)** — wind and terrain acting on fire is at least two mechanisms, possibly three. Whether that is multiple Plugins, dynamic World conditions, or something else is undecided, and it shapes this Lab's World templates directly. Not resolvable here (§36.6, F-22).
- **DEC-3 (temporal semantics)** — see the step-duration question above.

## The nine questions this Lab owes

1. **Domain fit** — is contact-and-radiant spread genuinely local at the modelled scale?
2. **World fit** — does collapsing fuel-moisture classes into one scalar lose something load-bearing?
3. **Mechanism fit** — can spotting be represented locally, or does it define the boundary?
4. **Time fit** — what does one step mean, and does the front and the incident need different answers?
5. **Evidence fit** — are rate of spread and front roughness reproducibly measurable from stored Runs?
6. **Accuracy** — which documented fires or established-model outputs serve as reference cases?
7. **Failure boundaries** — when does a convincing render become a misleading one?
8. **Comparison** — what do operational tools already do better, and where is SCR complementary?
9. **Transfer limits** — what validation would a retrieved mechanism need before any real-world use?

## Non-claims

This Lab does not forecast fire behaviour, does not predict any real fire, and produces no output suitable for operational or safety decisions. Mechanisms it generates are candidate explanations requiring domain validation in domain tooling (§41, §43).
