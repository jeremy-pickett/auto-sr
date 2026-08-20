# 13. Plankton Patchiness Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #13, Family B · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Plankton is not spread evenly through the ocean. It occurs in patches — from centimetres to hundreds of kilometres — and the patchiness is not simply inherited from the physical environment. Blooms appear, spread, and collapse; satellite chlorophyll images show filaments, swirls, and eddies of colour with structure at every scale.

Two questions have driven the field for decades. Why does patchiness exist at all, given that turbulence should mix it away? And how do so many plankton species coexist in a well-mixed medium with few limiting resources — Hutchinson's "paradox of the plankton" (1961), which patchiness is one candidate answer to.

## What the domain already knows

**There is a minimum patch size, and it has a formula.** The KISS result — from Kierstead, Slobodkin, and Skellam around 1953 — gives the critical patch radius below which diffusive loss exceeds growth and a bloom cannot persist, as a function of growth rate and diffusivity *(attribution from memory, verify)*. It is the plankton analogue of a critical mass and it is genuinely closed-form.

**Turbulent stirring theory is well developed.** Physical oceanography can describe how a tracer field is stretched and folded by a turbulent flow, producing filamentary structure and a characteristic spectral slope. Much observed patchiness at large scales is explained as **stirring of a passive tracer**, not as biological self-organization at all. Distinguishing the two is the field's central methodological problem, and it has a name — the biological versus physical contribution to the variance spectrum.

**The incumbents are serious.** Coupled physical–biogeochemical ocean models (the NPZD lineage embedded in circulation models) are the operational tool. They resolve the flow and carry biology as tracers.

Lattice-CA precedent specific to plankton is thin. There is a reaction–diffusion literature and an individual-based-model literature, but nothing canonical in the way Nagel–Schreckenberg is canonical for traffic.

## Where the shortcut holds, and where it breaks

**Reducible.** Critical patch size (KISS). Bloom timing from the classical mixed-layer arguments (Sverdrup's critical depth). Bulk productivity from light, nutrients, and temperature. Tracer variance spectra under known stirring. Predator–prey oscillation periods from mean-field models. A large fraction of what practitioners ask is on this list.

**Irreducible.** What is left:

- **Excitability.** Plankton systems can behave as excitable media: a perturbation past threshold triggers a large bloom excursion followed by a refractory period. That is a local mechanism producing travelling and spiral structure, and it has been proposed for plankton fields specifically.
- **Coexistence through spatial structure.** The paradox-of-the-plankton answer that depends on space — species persisting because competition is local and dispersal limited — is a spatial-arrangement question with no mean-field answer.
- **Predator–prey pattern formation.** Spatial predator–prey systems generate patterns and chaos that the well-mixed equations do not, and the spatial versions are not analytically tractable in the interesting regime.
- **Bloom collapse.** Whether a bloom ends by grazing, nutrient exhaustion, or viral lysis, and whether collapse propagates spatially, is history-dependent.

**The lens, stated plainly.** This Lab has a problem the others in Family B do not: **the dominant source of the observed structure is probably not the mechanism SCR would model.** Large-scale plankton patchiness is substantially advection — the ocean stirring a tracer. A lattice with local growth and diffusion, and no realistic flow, reproduces neither the spectrum nor the geometry, and any resemblance to a satellite chlorophyll image would be superficial and misleading.

The catalog's own entry says this: *"the vertical dimension and advection are the parts a lattice will handle badly, and the fit review should say so early."* That is correct and it is the most important sentence about this Lab.

## What a Cell would carry

A parcel of surface water: phytoplankton biomass, zooplankton biomass, one or two nutrients, and possibly light or mixed-layer depth. Bounded scalars; §13.1 met trivially.

Two Layout problems, both serious. **The ocean is three-dimensional and the vertical is not symmetric with the horizontal** — light comes from above, nutrients from below, and the mixed-layer depth is a controlling variable. A two-dimensional surface grid discards the axis that matters most. And **the medium moves**. A Cell in this Lab is a fixed patch of ocean through which water flows, or a parcel of water that moves — and those are different Worlds with different Connections.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak, and I would grade it so rather than leaving it silent.**

This entry shares its diagnosis with the catalog's declared weak family: the substrate is not a lattice. Here the substrate is a moving fluid, which is worse than a network wearing a grid costume — it is a grid whose cells do not stay put. Every one of the position paper's selection-rule criteria points the wrong way: spatial adjacency is not stable, the interaction range is set by flow rather than proximity, and the dominant structuring process is non-local.

**What would salvage it, and it is narrow.** Drop the ambition to reproduce ocean patchiness, and treat this as an **excitable-medium and spatial-coexistence Lab that happens to use plankton vocabulary**. The questions "does local excitability produce travelling blooms" and "does limited dispersal permit coexistence that mean-field forbids" are legitimate, lattice-appropriate, and have real ecological content — they simply do not require, or license, any claim about the actual ocean. That is a much smaller Lab and an honest one.

**The upside worth being excited about.** Satellite ocean colour is a spectacular dataset — daily global coverage since the late 1990s, quantitative, free. If a Lab here could ever separate the biological from the physical contribution to observed structure, that would be a genuine contribution. But separating them is the hard part, and a model without realistic advection cannot even attempt it. The honest excitement is smaller: this Lab is a good place to demonstrate that **SCR will grade a domain down when the substrate does not fit**, on a phenomenon that photographs beautifully.

**The challenges, in order of severity.**

1. **Advection dominates and is not local.** The core objection, and probably fatal to the ambitious version.
2. **The vertical dimension carries the controlling gradients** and a surface grid discards it.
3. **Satellite imagery invites a false match.** Model output will look like ocean colour without sharing a mechanism — a serious §30.7 hazard.
4. **Strong incumbents** in coupled physical–biogeochemical modelling.
5. **Biology and physics are separate mechanisms** — DEC-1.

## Non-claims

This Lab does not model ocean ecosystems, does not predict blooms or fishery conditions, and produces nothing suitable for marine management, fisheries, or environmental decisions (§41, §43).
