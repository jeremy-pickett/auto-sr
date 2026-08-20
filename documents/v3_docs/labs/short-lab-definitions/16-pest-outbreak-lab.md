# 16. Pest Outbreak Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #16, Family C · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Bark beetles live in most conifer forests continuously, at densities so low nobody notices, breeding in scattered dying trees. Then, in some years and some stands, the population crosses a line and begins killing healthy trees across millions of hectares. The mountain pine beetle outbreak in western North America through the 2000s killed pine across an area larger than many countries.

The mechanism behind the threshold is **mass attack**. A healthy conifer defends itself by flooding a boring beetle out with resin. One beetle loses. But attacking beetles release aggregation pheromone, recruiting others; past some number of simultaneous attackers the tree's defence is exhausted and all of them succeed, breed in the phloem, and emerge multiplied. So the per-capita success rate *increases* with density — a strong Allee effect running the wrong way from the tree's point of view.

That produces bistability. Below the threshold, the population stays endemic indefinitely. Above it, it erupts and sustains itself as long as susceptible host remains. The interesting question is never the equilibrium; it is the crossing.

## What the domain already knows

**The threshold structure is understood and modelled.** Mass-attack dynamics with aggregation pheromone, tree defensive capacity, and host susceptibility produce a well-characterized bistability, and the outbreak/endemic distinction is standard in the forest entomology literature. Drought and stand age reduce tree defence; cold winters kill overwintering larvae; both shift the threshold.

**Spread has been treated with both reaction–diffusion and dispersal-kernel approaches**, and the same Fisher-versus-fat-tail issue as invasion ecology (#14) applies: beetle flight includes rare long-distance dispersal above the canopy, which produces satellite outbreaks far ahead of any front.

**Aerial detection surveys are annual and spatially explicit.** Forest health agencies in Canada and the United States map red-attack and grey-attack tree mortality from aircraft and, increasingly, satellite, yearly, over decades. This is a genuinely good dataset.

**Lattice precedent exists but is not canonical.** Spatially explicit outbreak models are used; there is no single reference CA in the way there is for traffic or grain growth.

## Where the shortcut holds, and where it breaks

**Reducible.** The endemic/outbreak bistability itself — a well-mixed model gives the threshold and the two stable states. Host susceptibility from stand age and species composition — a per-cell map with no interaction. Winter mortality from temperature. Rough spread speed under diffusive dispersal. Total mortality given outbreak duration and host availability.

**Irreducible.** The crossing and the spatial structure of it:

- **Where the eruption starts.** Bistable systems tip locally first. Which stand crosses depends on the coincidence of a susceptible patch, a drought-weakened neighbourhood, and enough local beetles — an arrangement question. Once one stand erupts it exports beetles, so the first crossing determines the geography of everything after.
- **Propagating bistable fronts.** A bistable system in space does not simply switch everywhere; it forms a front between the two states which can advance, retreat, or pin depending on local conditions. Front pinning on heterogeneous host is a genuine irreducible phenomenon and directly relevant to whether an outbreak stops at a valley.
- **Satellite outbreak coalescence.** Long-distance dispersal founds new eruption centres, and whether they merge with the main outbreak or burn out separately depends on arrangement.
- **Feedback onto the host.** The outbreak consumes its own host. Post-outbreak stands are non-susceptible for decades, so the system carries memory that steers the next outbreak.
- **Management interaction.** Sanitation felling and trap trees are interventions targeted using incomplete information; whether they matter depends on where the sub-detection population actually is.

**The lens, stated plainly.** This is a **tipping-and-front** domain, and it shares that structure with vegetation banding (#12) and coral reefs (#17). The reducible part is the existence of two states. The irreducible part is which state a specific landscape is in, when it flips, and how the boundary between flipped and unflipped moves. **Bistability is easy to establish analytically and nearly impossible to localize analytically**, and localization is the whole management question.

## What a Cell would carry

A forest stand: host density or basal area, tree defensive capacity, beetle population, attack state, and time since mortality. Bounded scalars; §13.1 met easily.

Layout is a grid, defensibly — stands are spatial and beetle flight is mostly short-range. The recurring qualification applies: long-distance dispersal is not a neighbour interaction, and here it founds the satellite outbreaks that make containment fail.

The hidden-state point is again operationally central. An endemic population is present, viable, and invisible; aerial survey detects trees that are already dead, which means the observation lags the mechanism by a year. A view keyed to visible mortality shows a landscape that was true last season. That is SCR-F §38.6 with a management consequence attached, and it is arguably a cleaner example than wildfire's.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible to strong — I would place it above several graded [plausible] entries, mainly on data quality and question shape.**

The domain question is genuinely ensemble-shaped. Nobody credible claims to predict which stand erupts next year. What agencies want to know is whether a containment strategy works across the range of plausible dispersal and attack mechanisms — which is a Study over many Runs, not a forecast. That is the shape this platform fits best.

**The upside worth being excited about.** Annual, spatially explicit, multi-decade mortality maps over enormous areas, with a documented major outbreak whose full spatial history is recorded. Very few Labs can compare a modelled front's shape, speed, and satellite-colony structure against a measured one at landscape scale over twenty years. This one can.

There is also a live and unresolved scientific question with real stakes: **why do outbreaks stop?** They do not simply exhaust host — they collapse while susceptible trees remain, and the reasons are debated (cold events, natural enemies, dispersal failure, stand-level defensive recovery). Supplying candidate local mechanisms for outbreak collapse, in bulk, with the failures kept, is a defensible contribution to an open question.

**The challenges, in order of severity.**

1. **Climate is the driver and it is external** — drought and winter cold set the threshold. At least two mechanisms (DEC-1), and arguably the dominant one is not local at all.
2. **Long-distance dispersal** founds the satellites that matter, and it is not a neighbour interaction.
3. **Observation lags the state by a year**, so even the reference data is delayed relative to the mechanism.
4. **One tick is one generation**, which is annual for most bark beetles — workable, but it makes within-season attack dynamics invisible.
5. **Forest management credibility hazard.** Real money is spent on felling and spraying; §30.7 applies.

## Non-claims

This Lab does not predict outbreaks, does not assess forest health at any real location, and produces nothing suitable for forest management, quarantine, or investment decisions (§41, §43).
