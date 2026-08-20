# 14. Invasion Ecology Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #14, Family C · **Standing:** **[strong]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A species arrives somewhere it did not evolve, establishes, and spreads. Sometimes the spread is a smooth advancing front at a steady speed. Sometimes it is nothing like that: the species sits at low density for decades and then erupts; or it jumps ahead in disconnected satellite colonies that grow and coalesce, so the range expands far faster than any front could travel; or it advances for years and then stops at an invisible line and never crosses.

Which of those you get is the question, and the answer changes what management does. A steady front can be met with a barrier. A jumping invasion cannot.

## What the domain already knows

**The front speed has a formula, and it is one of the most cited results in theoretical ecology.** Fisher and Kolmogorov–Petrovsky–Piskunov, in 1937, showed that a population with logistic growth and diffusion advances as a travelling wave at speed 2√(rD) — growth rate and diffusivity, nothing else. Skellam applied it to muskrat spread in Europe in 1951 and found the predicted linear range expansion in the historical record. This is a textbook success.

**And the domain knows exactly where the formula fails.** If the dispersal kernel has a **fat tail** — a small probability of very long jumps — the constant-speed result collapses and the invasion **accelerates without bound**. Kot, Lewis, and van den Driessche established this in the mid-1990s with integrodifference equations *(attribution from memory, verify)*, and it is now standard. Observed invasions that outran their Fisher predictions, notably gypsy moth spread in North America, are read through this lens.

**Allee effects change the answer again.** When a population grows poorly at low density — mates are hard to find, group defence fails — the front can slow, stall, or reverse. Range pinning and invasion failure follow from a mechanism that mean-field logistic growth does not contain.

**Lattice precedent is broad.** Spatially explicit invasion models, contact processes, and stochastic cellular models of colonization are standard tools in the field, and percolation-theoretic treatments of habitat connectivity are established.

## Where the shortcut holds, and where it breaks

**Reducible.** Front speed in homogeneous habitat with thin-tailed dispersal — Fisher–KPP, closed form. Whether a population establishes at all — a threshold calculation. Equilibrium range extent under a habitat suitability map — a per-cell calculation with no interaction. Acceleration rates for some analytically tractable fat-tailed kernels.

**Irreducible.** The realistic cases, all of them:

- **Stratified dispersal.** Long jumps found satellite colonies which grow and merge with the main front. The resulting spread rate depends on the *arrangement* of successful jumps, not just their frequency, and coalescence is a geometric process with no closed form.
- **Fragmented habitat.** Real landscapes are patchy. Whether an invasion crosses depends on percolation of suitable habitat, and near the connectivity threshold the outcome turns on specific arrangement.
- **Allee effects with heterogeneity.** A front that stalls in one place and leaks through in another produces pinning geometry that must be run to be known.
- **Founder effects at the expanding edge.** Gene surfing — neutral variants reaching high frequency simply by being at the front — is a real, measured phenomenon and it is pure spatial stochasticity amplified by expansion.
- **Eradication timing.** Whether an intervention succeeds depends on whether satellite colonies exist below detection. That is a hidden-state question, and it is the operational one.

**The lens, stated plainly.** This Lab has the cleanest reducible/irreducible boundary in the entire catalog, and the domain drew it itself. **Fisher–KPP owns the smooth homogeneous case; everything management actually faces is outside it.** A Lab here does not have to argue that the shortcut fails — the ecologists already published that it does, with the mechanism, in the 1990s.

## What a Cell would carry

A habitat patch: occupancy or population density, habitat suitability, established-versus-detected state, and possibly a propagule pressure or seed-bank variable. Bounded scalars; §13.1 met.

The Layout is a grid and honestly so for terrestrial spread. One important qualification: **long-distance dispersal is not a neighbour interaction.** A jump kernel with a fat tail connects distant cells directly. This is the same abstraction strain as spotting in wildfire (#1) and hopping in dunes (#4), and it recurs across the catalog — the platform will have to take a position on whether a bounded-range jump is a local mechanism.

The detected-versus-established distinction is worth naming: a cell that holds a small undetected population is computationally live and observationally silent. SCR-F §38.6 again, and here it is the operational crux.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong, and the inherited grade is well earned — this may be the best-posed Lab in Families A through C.**

Everything lines up. Spatial adjacency is physically real. The mechanism is local. The reducible core is a famous closed form with a famous, published boundary. The irreducible remainder is what management cares about. And unusually, the domain question is *ensemble-shaped* rather than prediction-shaped: nobody expects to know which field the beetle reaches next, but everyone wants to know whether a barrier strategy works across plausible dispersal mechanisms. That is a Study, not a Run.

**The upside worth being excited about.** Invasion data is exceptional by ecological standards. Gypsy moth spread in North America has been mapped annually for a century. Cheatgrass, zebra mussel, cane toad, emerald ash borer, and dozens more have documented range expansions with dates. Historical range maps let a modelled spread pattern be compared against a measured one — front position, satellite colony counts, expansion rate over time.

And the negative space matters in this domain more than most: management agencies spend real money on barrier and eradication strategies. "These eleven local dispersal mechanism families never produced containment under any barrier configuration we tried" is directly useful, and no literature publishes it.

**The challenges, in order of severity.**

1. **Long jumps are not local**, and they are the mechanism that matters most.
2. **Habitat is a second mechanism** if it changes; a static suitability map is a defensible World condition, but climate-driven range shift is not — DEC-1.
3. **One tick is a generation**, which is defensible for insects and awkward for trees.
4. **Detection bias in the data.** Historical range maps record where people looked.
5. **Over-reading risk.** A rendered invasion front sweeping a rendered map will be read as a forecast (§30.7).

## Non-claims

This Lab does not predict the spread of any real species, does not assess invasion risk, and produces nothing suitable for management, quarantine, or regulatory decisions (§41, §43).
