# 38. Pedestrian Flow Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #38, Family F · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Two streams of people walking in opposite directions along a corridor do not interpenetrate randomly. They separate into **lanes** — bands of people moving the same way — which form spontaneously, persist, and reform after being disrupted. Nobody organizes this. It emerges because avoiding someone coming at you is easier if you step behind someone already going your way.

The same self-organization appears at crossings, where two perpendicular streams form alternating diagonal stripes, and at bottlenecks, where flow oscillates: one direction dominates the opening for a while, then the pressure from the other side reverses it. Around corners, people cut the inside, creating a density peak on the inner wall that reduces effective corridor width.

The distinguishing feature relative to egress (#36) is that nothing has gone wrong. Nobody is escaping; the crowd is at ordinary density; and the variable of interest is the **layout**, not the emergency.

## What the domain already knows

**The same two model families as #36 apply**, and lane formation is their headline result: both the social force model and floor field CA produce it, and it was one of the first emergent behaviours demonstrated in each. Lane formation is to pedestrian modelling what the phantom jam is to traffic modelling — the phenomenon that proves the approach.

**The fundamental diagram is the reducible core, again**, with an important wrinkle: the pedestrian fundamental diagram differs measurably between cultures and between uni- and bidirectional flow, and the discrepancies between published diagrams are a known issue in the field. There is no single universal curve of the kind traffic enjoys.

**Controlled experiments exist in quantity.** Laboratory studies with instrumented corridors, tracked participants, and varied geometry have been run repeatedly, particularly in Germany and China, producing trajectory-level data for uni- and bidirectional flow, bottlenecks, and crossings. This is the same strength as #36, and it is a real one.

**Lane count is not fully predicted.** How many lanes form for a given corridor width and flow ratio is a selection question that the models produce but do not derive, and it is measured with substantial scatter.

## Where the shortcut holds, and where it breaks

**Reducible.** Corridor capacity from width and specific flow rate. Travel time under steady uniform flow. Level-of-service classification. Queue length at a bottleneck. **Facility design mostly runs on these numbers**, and for ordinary sizing decisions they are sufficient.

**Irreducible.** What the capacity number cannot express:

- **Lane number and stability.** How many lanes form, whether they persist, and whether they reorganize under fluctuation is a pattern-selection question — the same class of question as stripe selection in #20, and equally not given by linear reasoning.
- **Deadlock in counterflow.** Two dense opposing streams in a narrow passage can lock: nobody can move because moving requires someone else to move first. Whether a given geometry and density deadlocks is an arrangement question, and it is the failure mode that matters.
- **Bottleneck oscillation.** The alternating dominance at a doorway has a period and an amplitude that depend on geometry and density, and it reduces throughput below the nominal capacity.
- **Corner and obstacle effects.** Inside-corner crowding, column wakes, and the way a slight geometric asymmetry breaks a symmetric flow pattern are all local, geometric, and invisible to a rate calculation.
- **Group behaviour.** People walk in twos and threes and refuse to separate, which changes effective density and lane structure in ways single-pedestrian models miss.

**The lens, stated plainly.** This Lab shares its mechanism and its incumbents with #36 and differs in the question asked: **egress asks whether people get out, pedestrian flow asks whether a layout works.** That difference matters more than it looks, because it moves the Lab out of the life-safety regime and into the design regime — lower stakes, lower hazard, and a question that is genuinely about geometry rather than about crisis behaviour.

It also removes the worst technical problem. The contact-mechanics regime that makes #36's dangerous behaviour non-local does not arise at ordinary walking densities. **Pedestrian flow is a Lab where the local-mechanism abstraction actually holds throughout the regime of interest**, which is not true of its more famous sibling.

## What a Cell would carry

A floor cell: occupancy, and for the occupant, desired direction and current heading. Optionally a group identifier and a floor field trace. Bounded and small; §13.1 met.

Layout is a grid, at the standard 40 cm cell size, and it is physically motivated as in #36.

The recurring qualification: **movement on a lattice is anisotropic**, and in a Lab whose central phenomenon is directional self-organization, that bites harder than usual. Lanes forming along lattice axes may be lattice artifacts rather than behaviour, and a diagonal corridor is not equivalent to an axis-aligned one on a square grid. A Lab that reports lane structure without testing orientation dependence is reporting the grid.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible to strong, and I would place it just below #36 and #37 — with the honest caveat that it overlaps #36 enough that building both needs a reason.**

The reason exists and is worth stating: #36 is a **life-safety** Lab with a severe misuse hazard and a regime the abstraction handles badly. #38 is a **design** Lab with a mild hazard and a regime the abstraction handles well. If SCR wants to demonstrate crowd behaviour without inheriting the duty of care that comes with evacuation modelling, this is the entry to build, and the modelling machinery is shared.

**The upside worth being excited about.** Counterflow deadlock is a genuinely good target. It is a discrete, identifiable failure event; it depends on geometry and local behaviour rather than on aggregate density; it is reproducible in laboratory experiments; and it is exactly the sort of thing a design review would want to know about a proposed layout. Asking which local avoidance rules make deadlock likely, across many corridor geometries, is a Study with a clear answer and directly comparable experimental data.

The other attraction is **cross-Lab connection to an unlikely partner**. Lane formation in counterflow is a symmetry-breaking pattern-selection problem with the same abstract shape as stripe formation in #20 and lane-like structures in driven granular systems. Whether the corpus retrieves related mechanisms across those is a real test of mechanism-level indexing.

**The challenges, in order of severity.**

1. **Lattice anisotropy directly threatens the headline phenomenon.** Lanes are directional; grids are directional.
2. **Substantial overlap with #36** — the marginal value of the second Lab must be argued.
3. **Behaviour is cultural and variable**, and the fundamental diagram is not universal, so calibration targets disagree with each other.
4. **Groups and social structure** are a first-order effect that single-agent local rules miss.
5. **Facility design credibility hazard**, though milder than #36's.

## Non-claims

This Lab does not assess any real facility, does not inform architectural or circulation design, and produces nothing suitable for building design or safety decisions (§41, §43).
