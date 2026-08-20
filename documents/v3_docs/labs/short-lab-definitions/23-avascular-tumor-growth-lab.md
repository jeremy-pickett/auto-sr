# 23. Avascular Tumor Growth Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #23, Family D · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A small tumour with no blood supply of its own lives on diffusion. Oxygen and nutrients reach it from surrounding tissue, and the distance they penetrate is short — on the order of a hundred to a few hundred micrometres. So a spheroid past a certain size develops a layered structure: proliferating cells at the rim, quiescent cells beneath, and a necrotic core where nothing survives.

That geometry imposes a hard ceiling. An avascular tumour cannot exceed roughly one to two millimetres in diameter; growth stalls when the proliferating rim's production balances core loss. Escaping that ceiling requires recruiting blood vessels, which is a different phenomenon and a different Lab.

Within the ceiling, the interesting variable is **margin morphology**. Some tumours grow as smooth compact spheroids. Others develop fingers and invasive protrusions. The distinction matters clinically far out of proportion to its subtlety, because an infiltrative margin is what makes complete surgical removal impossible.

## What the domain already knows

**Growth curves have closed forms.** Gompertz and logistic curves fit tumour growth well and have for a century. Given a growth rate and a carrying capacity, the trajectory is known.

**The size limit is a diffusion calculation.** The critical radius at which the core goes hypoxic follows from oxygen diffusivity and consumption rate — a classical result, essentially the same mathematics as the Thiele modulus in catalysis.

**The instability has an analytic onset.** A growing front fed by an external diffusing nutrient is subject to the same instability as a solidifying crystal (#29): protrusions reach fresher nutrient and grow faster. This is the Mullins–Sekerka structure, and it has been applied to tumour margins explicitly.

**Lattice models are a large, established literature.** Eden growth is the minimal model of compact tumour expansion; diffusion-limited aggregation is the minimal model of the fingered extreme; and hybrid cellular automaton models with explicit nutrient fields have been standard in mathematical oncology since the 1990s. Cellular Potts and agent-based tumour models are routine.

**Lattice artifacts are a known, managed problem in that field** — as the position paper's grading note says. This is worth emphasizing because it is unusual: the domain has already learned that square lattices bias growth morphology and has developed practices around it. SCR would inherit both the problem and the field's awareness of it.

**Spatial evolutionary dynamics are the live frontier.** Work in the mid-2010s showed that spatial structure fundamentally changes how mutations spread within a tumour — clones surf on expanding fronts, and the resulting genetic heterogeneity differs sharply from well-mixed predictions *(Waclaw and colleagues, around 2015; attribution from memory, verify)*.

## Where the shortcut holds, and where it breaks

**Reducible.** Growth curve to the size ceiling. Critical radius for necrosis. Layer thicknesses at steady state. Onset condition for margin instability. Bulk cell kill from a uniform treatment. Most of what a first-pass calculation asks.

**Irreducible.** What remains:

- **Which morphology develops.** The stability analysis says a smooth margin becomes unstable; it does not say what shape results. Finger spacing, branching, and whether protrusions fragment into disconnected islands are nonlinear outcomes.
- **Clonal competition in space.** Which mutant lineage dominates depends on whether it happened to be near the expanding front. This is gene surfing in a tumour, it is measurable by sequencing, and it is not predictable from fitness values alone.
- **Treatment response with spatial refuges.** Hypoxic cells are less sensitive to radiation and to many drugs, and they are hypoxic *because of where they are*. Whether a treatment clears a tumour depends on the geometry of the sanctuary, and the survivors are not a random sample.
- **Heterogeneous tissue.** Real tumours grow into structured tissue with variable stiffness and vasculature, and the margin follows the path of least resistance.

**The lens, stated plainly.** The catalog entry insists the fit review "must be blunt that this is morphology, not prognosis," and that is exactly right — but the sharper statement is available. **Everything about tumour *size* is reducible; everything about tumour *shape and composition* is not.** And clinical consequence attaches mostly to shape and composition: margin infiltration, hypoxic refuge, clonal heterogeneity. So the irreducible half is the important half, which is a good position — provided the Lab never lets a rendered spheroid imply anything about a patient.

## What a Cell would carry

A tissue site: occupancy state (empty, proliferating, quiescent, necrotic), local nutrient or oxygen concentration, division timer, and possibly a clonal identity tag and treatment-damage counter. Bounded if clone identity is a small enumerated set; §13.1 met with that qualification.

Layout is a grid, and the field's own experience says the grid bites: square lattices bias growth toward the axes and change measured margin roughness. Hexagonal or off-lattice arrangements exist for exactly this reason. **A Lab that reports a roughness exponent from a square lattice without addressing anisotropy is reporting an artifact**, and the domain will know it.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the catalog's most crowded incumbent field and its most dangerous audience.**

Mathematical oncology is a substantial, funded, active discipline that has been running hybrid cellular automaton tumour models for thirty years. SCR arrives not as a new approach but as a bulk generator of variants of an approach the field already uses well. That is a weaker pitch than in domains where the incumbent is an analytic shortcut.

**The upside worth being excited about.** The honest opening is the *ensemble*, not the model. Mathematical oncology publishes individual mechanisms; it does not systematically publish which mechanism families fail. A corpus recording that thirty local growth rules produced compact margins and eleven produced infiltrative ones, with the boundary between them characterized, is the negative-space argument in a field that would recognize its value. Spatial evolutionary dynamics — which mutant lineages survive an expansion, and under which local competition rules — is the most active question and is intrinsically ensemble-shaped, since the outcome is stochastic and the interesting quantity is a distribution.

Reference data exists and is quantitative: tumour spheroid experiments are a standard benchtop assay with measurable growth curves, layer thicknesses, and margin morphology, and multi-region tumour sequencing gives spatial clonal maps.

**The challenges, in order of severity.**

1. **Cancer credibility hazard, the most severe in the catalog outside Family H.** Any rendered tumour will be read as clinically meaningful by someone. The catalog's "morphology, not prognosis" line is necessary and probably insufficient; this Lab should carry the strongest non-claims language in Family D.
2. **Lattice anisotropy directly corrupts the headline measurement** (margin roughness), and the field knows it.
3. **Crowded incumbent field** using the same class of model.
4. **The ceiling is real**: the avascular phase is a small, early, clinically limited slice, and the interesting disease is what happens after.
5. **Nutrient diffusion is a second mechanism** — DEC-1, though a diffusing field is a defensible World condition.

## Non-claims

This Lab does not model any patient's disease, does not bear on diagnosis, prognosis, or treatment, makes no claim about any therapy, and produces nothing suitable for any medical decision (§41, §43).
