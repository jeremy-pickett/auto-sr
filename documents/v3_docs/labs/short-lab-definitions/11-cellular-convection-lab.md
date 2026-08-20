# 11. Cellular Convection Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #11, Family B · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Heat a fluid layer from below and, past a threshold, it stops conducting and starts overturning in organized cells. In the laboratory this is Rayleigh–Bénard convection with its hexagonal or roll patterns. In the atmosphere it produces **mesoscale cellular convection** in marine stratocumulus — the honeycomb cloud patterns visible from orbit over cold ocean, tens of kilometres across.

Two states exist and they look like photographic negatives of each other. **Closed cells**: cloudy centres, clear rims, high albedo. **Open cells**: clear centres, cloudy rims, low albedo. The same air mass can hold both, and boundaries between them are sharp. Because these decks cover large fractions of the subtropical oceans and the albedo difference is large, which state prevails matters to the planetary energy budget.

The transition is driven substantially by **drizzle**. Rain in a cell depletes the cloud, cools the sub-cloud layer by evaporation, and generates outflow that lifts air at the cell edges — sustaining the rim cloud while the centre clears. This is a local rule with a delay and a feedback, and the result is an oscillating, propagating, self-organizing field.

## What the domain already knows

**The onset is a closed-form result.** Convection begins when the Rayleigh number exceeds a critical value — roughly 1708 for rigid boundaries in the classical problem. The initially selected cell size is close to the layer depth, from linear stability. This is one of the oldest and cleanest results in fluid dynamics.

**Open/closed transitions have been modelled with simple systems.** Work in the late 2000s and around 2010 showed that the drizzle–cloud–outflow feedback in stratocumulus behaves like a coupled oscillator system and produces open-cell patterns with realistic scales from relatively minimal representations *(Feingold, Koren and colleagues, around 2010; attribution from memory, verify)*. That is genuine precedent that this phenomenon does not require full fluid dynamics to reproduce qualitatively.

**The incumbent is enormous.** Large-eddy simulation is the standard tool, resolves the actual turbulence, and is expensive but trusted. Global climate models parameterize the whole thing crudely, and stratocumulus is a well-known source of inter-model spread in climate sensitivity.

## Where the shortcut holds, and where it breaks

**Reducible.** Onset threshold. Initial cell aspect ratio. Bulk heat flux scaling with Rayleigh number (Nusselt–Rayleigh relations, well characterized). Cloud albedo from cloud fraction and thickness. Radiative cooling rates. None needs a simulation.

**Irreducible.** The pattern's life, not its birth:

- **Open/closed transitions.** Which state a deck occupies, when it flips, and where the boundary sits are history-dependent. Both states can persist under similar large-scale conditions, which is a bistability, and bistable systems do not reveal which basin they are in from their parameters alone.
- **Pattern defects and rearrangement.** Real cellular patterns are not perfect lattices. They contain pentagon–heptagon defects that migrate and annihilate, and the coarsening dynamics have no closed form.
- **Precipitation feedback timing.** Drizzle takes time to form, fall, and evaporate. The delay is what makes the system oscillate rather than settle, and delay-driven oscillation is a mechanism that a steady-state analysis cannot see.
- **Cell propagation and triggering.** Open cells trigger neighbours through outflow, producing travelling patterns. That is a local excitable-medium mechanism embedded in a fluid.

**The lens, stated plainly.** This is the only Family B entry where **the real phenomenon is visibly cellular at the scale of interest** — you can see the cells from a satellite. That is a genuinely unusual property in this catalog and it makes the abstraction less of a leap than almost anywhere else. But it comes with a matching trap: **looking cellular and being governed by cell-local rules are different claims.** Rayleigh–Bénard cells are the output of a continuum fluid, not of neighbour interactions, and a lattice model that reproduces the picture has not thereby reproduced the mechanism.

The defensible position is narrow and specific: treat the *cells* as the participants, not the fluid. The open-cell system behaves like an excitable medium of interacting cells with a refractory period after rain — and that is a local mechanism, at that level of description, with published support.

## What a Cell would carry

At the honest level of description, a Cell is a convective cell or a patch of boundary layer: cloud liquid or thickness, moisture, sub-cloud energy, precipitation state, and a refractory or recovery timer. Bounded scalars; §13.1 met.

Layout is a grid, defensibly. The subtlety is that convective cells have a **characteristic size set by the layer depth**, so the grid spacing is not free — it has a physical meaning and choosing it wrong changes the answer. That is a stronger constraint than in most Grid Worlds.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the best "the phenomenon is already cellular" argument in the catalog and the worst incumbent.**

The appeal is immediate: real cells, real local triggering, real bistability, satellite imagery covering the globe every day for forty years. The problem is that the field's incumbent tool resolves the actual physics and the field knows exactly how much a simplified model gives up. Coming in with a lattice model of convection invites the response that this was solved properly decades ago — and for onset and heat flux, it was.

**The upside worth being excited about.** The excitable-media reframing is genuinely promising and connects this Lab to #21 (Excitable Media) in a way the catalog's family grouping hides. If open-cell stratocumulus really is a rain-driven excitable medium, then the same mechanism families that produce spiral waves in cardiac tissue may produce open-cell patterns in cloud — and the corpus is exactly the instrument for noticing that two Labs in different families retrieve the same mechanism. **Cross-Lab mechanism transfer is the platform's most distinctive potential capability, and this pair is the best candidate for demonstrating it.**

Data availability is also outstanding: MODIS and successors have imaged these decks continuously since 2000, transitions are visible, and pattern statistics are quantifiable.

**The challenges, in order of severity.**

1. **The mechanism is a fluid, and the fluid is not local.** Pressure is instantaneous across the domain. This is the deepest abstraction gap.
2. **LES is a strong, trusted incumbent** for exactly these questions.
3. **Climate credibility hazard.** Stratocumulus feedback is a headline uncertainty in climate sensitivity and any output will be over-read.
4. **Grid spacing carries physical meaning**, unlike most Grid Worlds.
5. **Radiation, moisture, and precipitation are separate mechanisms** — DEC-1.

## Non-claims

This Lab does not model or project cloud feedback, does not forecast weather, and produces nothing suitable for climate assessment or meteorological decisions (§41, §43).
