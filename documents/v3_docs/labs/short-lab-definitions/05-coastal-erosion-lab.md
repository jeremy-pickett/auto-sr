# 5. Coastal Erosion Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #5, Family A · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §30.4, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Waves arriving at an angle drive sand along the shore. Where transport converges the beach grows; where it diverges the beach retreats. Over decades this redistributes enormous volumes of sediment, builds spits and capes, migrates barrier islands landward, opens and closes tidal inlets, and drowns or accretes coastline that people have built on.

Two timescales that are not the same phenomenon: a single storm can breach a barrier island overnight, and ordinary fair-weather drift reshapes a shoreline over a human lifetime.

## What the domain already knows

**Longshore transport has a formula.** The CERC equation relates alongshore sediment flux to breaking wave height and the angle between wave crests and the shoreline. Coastal engineering runs on it and its descendants. Combined with a sediment continuity equation, this gives the "one-line" shoreline model — the shoreline as a single evolving curve — which is the operational workhorse.

**Shoreline retreat under sea-level rise has a formula, and it is contested.** The Bruun rule predicts retreat as a simple ratio of sea-level rise to nearshore slope. It is widely used and widely criticized as over-simple; a Lab here should know that the criticism is mainstream rather than fringe.

**The cellular precedent is excellent and underappreciated.** Ashton and Murray, with Arnault, published a cellular shoreline model around 2001 and developed it through the 2000s *(attribution from memory, verify)*. Its central result is striking: when waves approach at **high angle** — more than roughly 45 degrees to the shore normal — the standard transport relation makes a straight shoreline *unstable*. Perturbations grow. The model spontaneously produces capes, spits, flying spits, and cuspate forelands resembling the Carolina capes, from nothing but local transport rules and a wave climate. This is a first-rate example of a simple local rule generating large-scale geomorphology that people had attributed to inherited geology.

## Where the shortcut holds, and where it breaks

**Reducible.** Transport rate from wave conditions. Shoreline change under a *low-angle* wave climate, where the system is stable and diffusive — a straight coast stays straight, perturbations decay, and a diffusion equation describes it. Equilibrium beach profiles. Volume budgets. All standard.

**Irreducible.** The high-angle regime is where the domain becomes interesting and where closed forms stop:

- **Instability growth and pattern selection.** Once perturbations grow rather than decay, which features survive, what spacing emerges, and whether capes merge or persist is a nonlinear interaction problem. The linear stability analysis tells you it becomes unstable; it does not tell you what you get.
- **Shadowing.** A cape blocks waves from reaching the shoreline behind it, so the wave field a cell experiences depends on the shape of the whole coast. The "local" rule reads a non-local geometry, which is an honest and interesting strain on the abstraction.
- **Breaching and inlet dynamics.** A barrier island breach is a discrete threshold event that permanently changes the system's connectivity. Whether it happens depends on storm sequencing and antecedent state.
- **Storm sequencing.** Two identical storms in different order leave different coasts, because recovery between them is incomplete.

**The lens, stated plainly.** This domain has a **named instability threshold** separating a reducible regime from an irreducible one, and the threshold is a wave angle. That is unusually crisp. Below it, diffusion; above it, pattern formation with no shortcut. A Lab that knows which side of 45 degrees it is standing on knows whether it has anything to contribute.

## What a Cell would carry

A shoreline cell or a coastal plan-view cell: sediment volume or shoreline position, elevation, sediment type, and possibly dune or barrier state. Bounded and simple; §13.1 is met easily.

The Layout question is genuine. Ashton–Murray-class models use a plan-view grid with the shoreline as an interface, but the *one-line* tradition treats the coast as a 1-D curve. These are different Worlds with different mechanisms available, and shadowing requires the 2-D version.

## What one step would mean

The catalog already flags this as the entry's sharpest problem, and it is right. Wave conditions vary hourly; drift accumulates over decades; a breach happens in a night. There is no single tick duration that represents all three, and the standard field practice — driving a shoreline model with a synthetic wave climate at some averaging interval — is a modelling choice with known consequences. Whether SCR needs anything beyond lockstep here is a DEC-3 question and should not be answered locally.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, and stronger than the catalog entry suggests — for one specific reason.**

The catalog frames this Lab mainly as a time-fit stress test. That undersells it. Coastal erosion has what most Family A entries lack: **a documented case where a simple local rule overturned a domain assumption.** Attributing the Carolina capes to wave-driven self-organization rather than antecedent geology is exactly the kind of result the position paper claims this class of model can produce. That precedent gives the Lab a story, a benchmark, and a reason to believe.

**The upside worth being excited about.** Shoreline position is measured — satellite-derived shoreline time series now cover global coasts at annual or better resolution, and historical maps and aerial photography extend the record back a century. Few Labs in this catalog have observational data that good. And the stakes are high and rising: coastal management decisions are being made now on models whose critics are numerous. A cheap source of candidate mechanisms for the unstable regime is genuinely useful upstream work.

**The challenges, in order of severity.**

1. **Step duration has no defensible answer yet**, and every rate claim depends on it.
2. **Shadowing is non-local.** The rule reads global geometry. Honest, but it strains the local-mechanism identity §45.12 asks reviewers to police.
3. **Waves are a second mechanism.** DEC-1.
4. **Rediscovery risk in the unstable regime.** Ashton–Murray got there first.
5. **Engineering credibility hazard.** A rendered shoreline retreating past a rendered house is the most consequential §30.7 misreading in Family A, and coastal decisions carry real money.

## Non-claims

This Lab does not predict shoreline change at any real location, does not assess coastal hazard, and produces nothing suitable for planning, insurance, engineering, or property decisions (§41, §43).
