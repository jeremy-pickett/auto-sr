# 4. Dune and Ripple Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #4, Family A · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Wind moves sand in hops. A grain lifted by the wind lands, ejects other grains, and the process cascades — saltation. Out of that microscopic transport come structures at two very separate scales: **ripples**, centimetres apart, forming in minutes; and **dunes**, tens to hundreds of metres, migrating over years. Dune fields organize further into patterns with characteristic spacing, and dune types are classified by wind regime — barchans under unidirectional wind, linear dunes under bimodal, star dunes under multidirectional.

The scales do not blend into each other. Ripples and dunes are separate instabilities with separate mechanisms, and the gap between them is one of the domain's known facts.

## What the domain already knows

**Bagnold (1941)** is the foundation — the physics of blown sand, saltation thresholds, and transport rate scaling with roughly the cube of shear velocity. It remains the reference.

**Werner (1995)** built the canonical cellular dune model *(attribution from memory, verify)*: slabs of sand are picked up, transported a fixed distance, and deposited with a probability depending on whether the landing site is already sandy, plus an avalanche rule enforcing the angle of repose. That handful of rules produces barchans, linear dunes, star dunes, and transverse ridges depending on wind regime. It is one of the strongest existing demonstrations in any domain that a trivially simple local rule reproduces a real morphological classification.

**Ripple wavelength has a linear-stability answer.** The initial spacing selected from a flat bed follows from the saltation trajectory length, and analytical treatments of the instability date to at least the 1980s. Dune migration speed is inversely proportional to dune height — a robust, measured, near-analytic relation.

## Where the shortcut holds, and where it breaks

**Reducible.** Saltation threshold, transport rate from wind speed, initial ripple wavelength, dune celerity from height, and the wind-regime-to-dune-type classification are all established and mostly closed-form or empirical-curve. A CA that reproduces them has reproduced textbook content.

**Irreducible.** The parts that resist:

- **Pattern coarsening.** Dune fields do not settle at the initially selected wavelength. Dunes merge, split, and exchange sand, and the field's characteristic spacing grows over time in a way that depends on the history of interactions. Coarsening laws are studied empirically and by simulation, not derived.
- **Dune collisions.** When a small fast barchan overtakes a large slow one the outcome varies — absorption, breeding of new dunes, ejection — and which occurs depends on the size ratio and offset. This is a genuinely irreducible interaction and an active research question.
- **Barchan field stability.** Isolated barchans are unstable in theory (they should grow or vanish), yet real fields persist. Reconciling that requires the interaction dynamics, not the single-dune solution.
- **Boundary and supply effects.** Sand supply, vegetation, topography, and bedrock exposure change everything and are not in any tidy formula.

**The lens, stated plainly.** This Lab has the catalog's clearest **rediscovery risk**. Werner already did the thing SCR proposes to do, and did it well enough that the result is textbook. If SCR generates a mechanism that produces barchans, the honest reading is "the platform works," not "we learned something about sand." The catalog's [plausible] grade reflects exactly this: excellent fit, real precedent, limited headroom.

That is not fatal. It makes this Lab an unusually good **validation instrument**: a domain where we know what the answer looks like and can check whether generation finds it, whether the negative space matches what the field knows is impossible, and whether the corpus surfaces Werner-class rules when asked for migrating periodic structures. A Lab whose job is to test the platform rather than the domain is a legitimate Lab.

## What a Cell would carry

A patch of bed: sand height or slab count, and possibly local slope, shadow state, and vegetation cover. Extremely low state complexity — Werner's model gets by on height alone plus rules. This is the cheapest §13.1 case in the catalog.

Two Layout notes. Wind direction makes Connections **directionally asymmetric**, which is a real requirement rather than a preference. And transport is **non-local by design** — a slab hops a fixed distance, not to a neighbour — which stretches the definition of a local mechanism in an interesting and honest way. Whether a fixed-length hop counts as local is a genuine boundary question, and this Lab is the cleanest place to ask it.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible as domain science, strong as a platform test.**

The domain gap is small. The field has a working cellular model, understands the reducible parts analytically, and studies the irreducible parts (coarsening, collisions) actively with tools already suited to them. SCR would enter a field that is not stuck.

**The upside worth being excited about.** Two things. First, the reach question: dune fields are one of the few natural systems where a *non-local transport hop* is physically correct, so this Lab tests whether SCR's abstraction can express something other than nearest-neighbour interaction honestly. That answer matters far beyond sand — spotting in wildfire, dispersal in ecology, and scanning worms all have the same shape. Second, the imagery is exceptional and the data is free: satellite imagery of dune fields worldwide, with measurable spacing, orientation, and migration rates over decades. Few Labs can be checked so cheaply.

**The challenges, in order of severity.**

1. **Rediscovery, not discovery.** Werner-class models exist and are good.
2. **Scale separation.** Ripples and dunes are different mechanisms at different rates. One step cannot mean both.
3. **The hop is not a neighbour interaction.** Honest, interesting, and a real strain on the abstraction.
4. **Wind is a second mechanism** — DEC-1 again, though a fixed wind regime is a defensible World condition.

## Non-claims

This Lab does not predict the evolution of any real dune field and produces nothing suitable for engineering, land management, or hazard decisions (§41, §43).
