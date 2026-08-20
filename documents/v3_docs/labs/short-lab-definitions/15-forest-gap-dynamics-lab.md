# 15. Forest Gap Dynamics Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #15, Family C · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §30.4, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A canopy tree dies and falls. Light reaches the forest floor for the first time in a century. What was a shaded understorey becomes a competitive scramble: suppressed saplings release, pioneer species germinate from the seed bank, and vines exploit the opening. One stem eventually wins the gap and closes it, and the forest returns to shade.

A mature forest is a mosaic of such gaps at every stage of recovery. The **gap-phase dynamic** — patch death, colonization, competition, closure, repeat — is the standard account of how old-growth forests maintain species diversity without any species winning outright.

Gap size matters and the dependence is sharp. Small gaps favour shade-tolerant species that were already present; large gaps favour fast-growing pioneers that were not. So the *distribution* of disturbance sizes determines the species composition, which is a statement about a size distribution, not about any individual gap.

## What the domain already knows

**Gap models are a mature, forty-year modelling tradition.** JABOWA (Botkin, Janak, and Wallis, 1972) and its descendant FORET established the form: a small patch, individual trees with growth limited by light, temperature, and moisture, stochastic mortality and establishment *(attribution from memory)*. Later spatially explicit versions such as SORTIE track individual crown positions and light interception. These are the incumbents, they are calibrated to real forest inventory data, and they work.

**Succession theory supplies the reducible framework.** Species are ordered along a shade-tolerance axis, and successional trajectories after disturbance follow predictably from that ordering plus growth rates. Chronosequence studies confirm the broad pattern across biomes.

**The size distribution is measured.** Gap size–frequency distributions have been mapped in many forests, typically heavily skewed toward small gaps with a long tail from storm and blowdown events.

## Where the shortcut holds, and where it breaks

**Reducible.** Successional sequence from shade tolerance ordering. Mean stand basal area and biomass at equilibrium. Time to canopy closure for a gap of given size. Species composition as a function of the disturbance regime — this is the classic result, and it is a statistical argument, not a spatial one. Carbon stocks from stand tables. Most forestry questions live here.

**Irreducible.** What the non-spatial account discards:

- **Gap coalescence.** When adjacent trees fall in the same storm the resulting opening behaves unlike the sum of separate gaps, because interior conditions differ. Whether gaps merge depends on spatial arrangement of mortality.
- **Neighbourhood-dependent mortality.** A tree exposed by an adjacent fall is more likely to fall next. Windthrow is contagious, and contagion is the mechanism that turns scattered mortality into blowdown patches.
- **Seed shadow geometry.** Which species can colonize a gap depends on which adults are within dispersal range of it — a specific, local, arrangement-dependent fact.
- **Spatial storage of diversity.** Species persist by being in the right patch at the right time. Whether a rare species survives a century depends on the sequence of gap openings near its remaining individuals.

**The lens, stated plainly.** This domain is a strong test of a distinction worth naming: **aggregate composition is reducible; persistence of the rare is not.** If the question is "what is the biomass and species mix at equilibrium," a non-spatial model answers it. If the question is "does this species still exist in two hundred years," the answer depends on a specific sequence of local events and cannot be shortcut.

There is a second, more uncomfortable observation. The incumbent gap models are *already* patch-based individual-based simulations. They are not analytic shortcuts that SCR would supersede — they are simulations of much the same kind, with forty years of calibration behind them. SCR is not entering an unmodelled domain; it is entering one where a very similar modelling approach is already standard practice.

## What a Cell would carry

A patch of forest floor, roughly the footprint of one canopy tree: canopy state, dominant occupant's species and size, light availability, seed bank composition, and time since disturbance. Bounded, though species identity as a small enumerated set is the natural representation, and the number of species is a modelling decision with consequences. §13.1 is met if species count stays bounded and small.

Layout is a grid and defensibly so. One qualification: **crowns are not square and light is not vertical.** Real light interception depends on crown geometry and sun angle, which a lattice with a fixed neighbourhood represents crudely — SORTIE-class models exist precisely because that crudeness mattered.

## What one step would mean

The catalog flags this entry for time fit and is right. Tree lifespans are centuries; gap closure is decades; a windthrow is an afternoon. A step of one year is the natural choice and makes storms instantaneous events rather than mechanisms, which is a modelling commitment rather than a neutral choice.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the catalog's clearest case of an incumbent that is the same kind of thing SCR is.**

The mechanism is genuinely local and the emergent property — diversity maintained by disturbance — is a real and important result. But the honest position is uncomfortable: this domain's standard tool is already a spatially explicit patch simulation, calibrated against forest inventory plots that have been remeasured for decades. SCR would not be supplying mechanism to a field that lacks it. It would be supplying *more* mechanisms to a field with a good one.

That is not worthless, but it is a weaker pitch than in domains where the incumbent is an analytic shortcut with known limits.

**The upside worth being excited about.** Forest inventory data is remarkable — permanent plots remeasured every five years for many decades, some over a century, with individual stems tagged and mapped. Barro Colorado Island and the wider forest-dynamics plot network give stem-mapped censuses of hundreds of thousands of individual trees. For a platform that wants to check whether an emergent spatial statistic matches a measured one, this is among the best datasets in the catalog.

The genuinely novel angle is the **negative space**: which local competition and dispersal rule families *fail* to maintain diversity. Coexistence theory is a contested field, and a corpus recording that eleven mechanism families never sustained a rare species would be a real contribution to a live argument.

**The challenges, in order of severity.**

1. **The incumbent is a peer, not a shortcut.** Forty years of calibrated gap models.
2. **Timescale is centuries**; a run is long and validation is longer.
3. **Disturbance is external** — storms, fire, drought are second mechanisms (DEC-1).
4. **Species identity strains bounded state** if the Lab wants realistic diversity.
5. **Light geometry is poorly represented by a lattice neighbourhood.**

## Non-claims

This Lab does not model any real forest, does not predict succession or carbon dynamics, and produces nothing suitable for forestry, conservation, or carbon accounting decisions (§41, §43).
