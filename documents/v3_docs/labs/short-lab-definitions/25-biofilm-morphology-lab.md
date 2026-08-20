# 25. Biofilm Morphology Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #25, Family D · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Put bacteria on a nutrient plate and the colony that grows is not always a disc. Depending on how hard the agar is and how much food is in it, the same species produces compact round colonies, fractal branching structures resembling frost, dense concentric rings, or chiral pinwheels with all the arms curling the same way.

The morphology is not species-specific decoration; it is a response to two conditions. When nutrients are scarce, growth is limited by diffusion to the colony edge, and protruding tips get more food than valleys — so branches form and sharpen. When the surface is hard, cells cannot spread easily, which sharpens branching further. Soft agar plus rich nutrient gives compact spreading.

There is a second, quieter phenomenon at the front. As a colony expands, lineages get pushed outward and separated. Neutral genetic variants that happen to be at the growing edge can end up occupying entire sectors of the final colony — visible as coloured wedges when strains are fluorescently labelled — purely by position, with no fitness difference at all.

## What the domain already knows

**The morphology diagram is mapped.** Work through the late 1980s and 1990s, particularly by Matsushita and Fujikawa in Japan and Ben-Jacob and colleagues in Israel, established the phase diagram of colony morphology against agar hardness and nutrient concentration, and identified the regimes: compact Eden-like growth, DLA-like fractal branching, dense branching morphology, concentric rings, and chiral forms *(attributions from memory, verify)*. This is a genuinely reduced answer: given the two conditions, the morphology class is predictable.

**The branching is a known instability.** Diffusion-limited growth produces fingering by the same mechanism as crystals (#29) and tumours (#23): the tip reaches fresh resource. DLA and its variants are the minimal models, and Eden growth is the compact limit.

**Range expansion genetics is a beautiful, quantitative result.** Hallatschek, Nelson, and colleagues showed around 2007 that expanding microbial colonies produce sector patterns from neutral drift at the front, with measurable statistics that match a theory of fluctuating boundaries *(attribution from memory, verify)*. The experiment is a plate photograph; the theory is stochastic front dynamics; the agreement is quantitative.

**Comparison images are abundant and standardized.** As the catalog says, this is unusually testable — plate photographs of colony morphology are published in quantity, at known conditions, with measurable fractal dimension, branch spacing, and sector statistics.

## Where the shortcut holds, and where it breaks

**Reducible.** Morphology class from agar hardness and nutrient concentration — read the phase diagram. Fractal dimension in the DLA limit — a known universal number. Colony radius growth rate in the nutrient-rich compact regime — linear, from the front's growth. Sector count scaling in neutral range expansion — the Hallatschek theory gives it.

**Irreducible.** The rest:

- **Branch geometry in the intermediate regime.** Between compact and fractal lies dense branching morphology, where branch width, spacing, and tip-splitting frequency are not given by either limiting theory. This is most of the interesting parameter space.
- **Which lineage wins a sector.** The identity of the surviving sectors is amplified fluctuation. The *statistics* are predicted; the *realization* is not, and when a mutation is involved rather than a neutral marker, the realization is what matters.
- **Multi-species interaction.** Colonies of competing or cooperating strains produce interpenetrating structures, and whether a slower-growing strain survives at the front depends on the geometry of the interface.
- **Antibiotic and stress response with spatial structure.** Cells in the colony interior are metabolically inactive and drug-tolerant *because of where they are*. Survivors of treatment are a spatially selected subset, and this is the clinically relevant fact.

**The lens, stated plainly.** This Lab illustrates a pattern this catalog keeps finding and which is worth naming as a general principle: **limiting regimes have universal answers; the middle does not.** DLA has an exponent. Eden has an exponent. The dense branching regime between them — where real colonies mostly live — has neither, and that is where a corpus of candidate mechanisms is worth having.

## What a Cell would carry

A lattice site: occupancy by cells, cell density or biomass, local nutrient concentration, metabolic state (active or dormant), and possibly a lineage tag. Bounded and small; §13.1 met, with the usual caveat that lineage identity must stay a small enumerated set.

Layout is a grid and physically honest — a colony grows on a flat plate. The recurring anisotropy warning applies with force: **branch orientation on a square lattice tends toward the axes**, and branch geometry is the headline measurement. The field already knows this from the DLA literature, and reporting a branching statistic without addressing lattice bias would not survive review.

Nutrient diffusion is a field the colony both reads and depletes, which is a mild DEC-1 case — though a diffusing consumable is arguably a World condition rather than a second mechanism.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible to strong — and I would rank it the best-validated Lab in Family D, ahead of its inherited grade on testability alone.**

The unusual property here is that **the reference experiment is cheap, fast, and controlled.** A colony grows overnight on a plate at a known agar concentration and known nutrient level, and the result is a photograph with measurable fractal dimension, branch spacing, and sector statistics. Very few Labs in this catalog can have their emergent output compared against a controlled experiment that costs a few pounds and takes a day. Wildfire cannot. Karst cannot. This one can, repeatedly, across a mapped parameter space.

That makes it a strong candidate for the platform's **second calibration anchor** alongside wildfire — and a better one in some respects, since the experiment is repeatable at will rather than observed opportunistically.

**The upside worth being excited about.** The spatially-structured drug tolerance question is real, clinically relevant, and underserved: biofilms are a major reason infections persist, and the mechanism is substantially geometric rather than genetic. Asking what local growth and dormancy rules produce tolerant interiors, across many candidate mechanisms, is defensible upstream work with a plausible route to mattering.

The cross-Lab connection is again strong: the same instability produces fingers here, in tumour margins (#23), in wound-edge leaders (#24), and in dendrites (#29). Four Labs, four fields, one mechanism family — if the corpus surfaces that, the platform has demonstrated something no domain model library does.

**The challenges, in order of severity.**

1. **Lattice anisotropy corrupts the headline measurement**, exactly as in #23.
2. **The phase diagram already answers the first question anyone asks.**
3. **Small basic-science audience** unless the tolerance angle is pursued.
4. **Nutrient depletion couples the mechanism to a field it modifies** — mild DEC-1.
5. **Medical framing risk** if biofilm-infection language is used loosely (§30.7).

## Non-claims

This Lab does not model any real infection, does not bear on antimicrobial treatment, and produces nothing suitable for clinical or industrial decisions (§41, §43).
