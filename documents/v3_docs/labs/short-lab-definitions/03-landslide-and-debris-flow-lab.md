# 3. Landslide and Debris Flow Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #3, Family A · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A slope holds until it does not. Material loses strength — rain raises pore water pressure, a toe is undercut, an earthquake shakes it — and fails. The failed mass loads what is downslope of it, which may then fail in turn. At one extreme this is a single discrete slump; at the other it is a debris flow that entrains material as it runs and travels kilometres beyond the source.

The population-level fact is as interesting as any single event: landslide inventories from a triggering storm show a **size-frequency distribution with a heavy power-law tail** above a rollover at small sizes, reported across many regions and triggers *(Malamud and colleagues, mid-2000s; attribution from memory)*. Most failures are small; the rare large ones dominate the volume moved.

## What the domain already knows

**Slope stability has a closed form for the simple case.** The infinite-slope factor of safety — cohesion, friction angle, slope, and pore pressure combined into a single ratio — is taught in every geotechnical course and is what practising engineers actually use. Failure is predicted when the ratio crosses one. Coupled to a hydrological model this becomes the operational tool (the SHALSTAB and SINMAP lineage), and it works: it maps relative susceptibility across terrain reasonably well.

**Runout has its own reduced models.** Empirical relations between landslide volume and travel distance — the angle-of-reach or Heim ratio — predict how far a mass of given size will go, well enough for hazard zoning.

**Lattice precedent is famous and, importantly, contested.** The Bak–Tang–Wiesenfeld sandpile (1987) is the founding model of self-organized criticality: local toppling rules, avalanche sizes distributed as a power law, no tuning required. It is the reason anyone reaches for a cellular model of landslides at all. But laboratory granular piles largely **failed** to reproduce clean SOC — the well-known rice-pile experiments found the behaviour depended strongly on grain shape, and rounded grains produced no scale-free avalanches. The sandpile is a beautiful theory of criticality and a poor theory of sand.

That failure is the most valuable thing this Lab can know.

## Where the shortcut holds, and where it breaks

**Reducible.** Whether a *given* slope with *known* properties fails is arithmetic. Susceptibility mapping across terrain is a per-cell calculation with no interaction at all — every operational tool computes it that way, and the absence of interaction is precisely why it is cheap. Runout distance from volume is an empirical curve. Regional magnitude-frequency is a fitted power law.

**Irreducible.** What the reduced models discard is the interaction, and the interaction is where the catastrophes live:

- **Load transfer cascades.** A failing block loads its neighbours. Whether that arrests after one cell or propagates across a whole hillside depends on the specific arrangement of marginal cells. This is the cascade question, and cascade outcomes on heterogeneous substrates have no closed form.
- **Progressive failure and strain softening.** Real soils lose strength *after* they begin to deform. A cell that fails is weaker than it was, which is a non-monotone feedback the static factor-of-safety calculation cannot represent by construction.
- **Entrainment.** A debris flow that scours its channel grows as it travels, so runout depends on path, which depends on runout. Self-referential, path-dependent, no shortcut.
- **Rainfall sequencing.** Antecedent moisture matters enormously. Two storms of identical total depth in different order produce different failure populations.

**The lens, stated plainly.** The reducible core here is unusually complete — this is one of the few Labs where the incumbent method is a *per-cell formula with no neighbours*, which means SCR's entire potential contribution is the coupling term. That is a clean, narrow, testable position: **does adding local load transfer to a susceptibility map change which slopes fail, and does it do so in a way that matches observed inventories better than the uncoupled calculation?** That question is answerable and currently under-answered.

## What a Cell would carry

A terrain patch with slope, cohesion or strength, saturation or pore pressure, accumulated load from upslope failures, and failure state. Bounded scalars throughout; §13.1 is comfortably met.

The honest difficulty is that **stress is not local.** Soil transmits load through a continuum, and a lattice with nearest-neighbour transfer is a strong approximation whose defensibility varies with slope geometry. This is the same objection that damages the Fracture Lab (#31) and it should be stated in both.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with an unusually clear statement of what it would have to beat.**

The strength is that the incumbent is a *non-interacting* calculation, which leaves an obvious gap. The weakness is that the most famous cellular model of this domain — the sandpile — is known to be physically unfaithful, and any lattice landslide model inherits suspicion from it. A Lab here must open by distinguishing itself from BTW rather than borrowing its glamour.

**The upside worth being excited about.** Landslide inventories are real, abundant, mapped from satellite and aerial imagery after major storms, and published. That is a genuine reference dataset — better than most of Family A. A mechanism that reproduces both the observed size-frequency rollover *and* the spatial clustering of failures, from local rules, would be a checkable result. And the negative space is valuable in the position paper's exact sense: knowing which load-transfer rule families never produce the observed rollover prunes a real search.

**The challenges, in order of severity.**

1. **The sandpile's reputation.** Physically unfaithful, universally known, and the first thing any reviewer will think of.
2. **Stress is a continuum, not a neighbour relation.** The central abstraction gap, and it is wide.
3. **The trigger is external.** Rainfall or shaking drives everything and is not a local mechanism — at least two mechanisms, blocked on DEC-1.
4. **Susceptibility is already solved well enough.** Beating "good enough and cheap" is harder than beating "wrong."
5. **Failure is rare and discrete.** Long quiet periods punctuated by events strain the meaning of a uniform step.

## Non-claims

This Lab does not assess the stability of any real slope, does not predict any landslide, and produces nothing suitable for hazard zoning, engineering, or public safety decisions (§41, §43).
