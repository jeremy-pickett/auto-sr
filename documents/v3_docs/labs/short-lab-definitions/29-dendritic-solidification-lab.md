# 29. Dendritic Solidification Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #29, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

When molten metal freezes, the solid does not advance as a flat front. A protrusion into the liquid finds itself surrounded by cooler, less solute-rich melt, so it grows faster and protrudes more. The front breaks into an array of tree-like crystals — dendrites — with primary arms, side arms, and side-arms on the side arms.

The resulting structure is the **microstructure**, and it determines the metal's mechanical properties. Arm spacing controls how finely alloying elements are distributed; segregation between arms creates chemical inhomogeneity that persists through subsequent processing; the transition from columnar dendrites growing inward from the mould wall to equiaxed dendrites nucleating in the melt determines whether a casting has directional or isotropic properties. Every cast component in existence has its properties set by this process.

## What the domain already knows

**The instability has a closed-form onset.** Mullins and Sekerka (1964) gave the linear stability analysis of a solidifying interface against perturbations, balancing the destabilizing effect of the diffusion field against the stabilizing effect of surface tension. It yields a critical wavelength and it is one of the foundational results in materials science.

**Tip behaviour is solved, with an important subtlety.** Ivantsov's solution gives the shape of a steadily growing needle crystal but leaves a degeneracy: it fixes the product of tip velocity and tip radius, not each separately. **Microscopic solvability theory** resolved this in the 1980s by showing that crystalline anisotropy in the surface energy selects a unique operating point *(attribution from memory, verify)*. Anisotropy is not a detail here — without it there is no dendrite, only unstable fingers.

**Arm spacing has engineering correlations.** Primary and secondary dendrite arm spacing scale with cooling rate and solidification time through well-established power laws, used routinely in foundry practice to infer thermal history from a micrograph.

**The incumbent is phase-field, and it is strong.** Karma and Rappel's work in the late 1990s made quantitative phase-field simulation of dendritic growth tractable, and it is now the standard computational tool: it resolves the interface without tracking it, handles anisotropy properly, and has been validated against experiment.

**Cellular automaton models of solidification exist and are used industrially.** The CA–finite element approach for predicting grain structure in castings is an established commercial technique. This matters: SCR would not be introducing cellular modelling to this field — the field already has it.

## Where the shortcut holds, and where it breaks

**Reducible.** Onset of interface instability. Tip velocity and radius given undercooling and anisotropy. Primary and secondary arm spacing from cooling rate. Solute partitioning at the interface. Whether growth is columnar or equiaxed under given thermal conditions — approximately, via established criteria.

**Irreducible.** What survives, and it is less than in most Labs:

- **Sidebranch statistics.** Where side arms appear along a primary arm, at what spacing, and how their amplitude grows is driven by selective amplification of thermal noise. The mean spacing is known; the realization is not, and sidebranching controls the fine structure of segregation.
- **Arm competition and coarsening.** Dendrite arms compete for solute and space; small ones remelt and vanish while large ones thicken. The evolution of the arm population over solidification time is a coarsening process.
- **Grain competition.** Neighbouring grains with different crystallographic orientations grow toward each other; the one better aligned with the thermal gradient wins the region. Which grains dominate a casting is decided by initial nucleation positions and orientations — amplified initial difference again.
- **The columnar-to-equiaxed transition.** Whether nucleated crystals ahead of the columnar front survive and block it is a threshold crossing that depends on local conditions and is genuinely hard to predict.

**The lens, stated plainly.** This domain is unusually *well* reduced. Onset, tip selection, and arm spacing — the three things anyone asks about — all have theory. What remains irreducible is real but fine-grained: sidebranch realization, grain competition, transition thresholds. **The reducible core here is larger, relative to the questions asked, than in almost any other Lab in the catalog**, and that is the central fact a fit review must weigh.

## What a Cell would carry

A volume element: solid or liquid state (or a solid fraction), temperature, solute concentration, and crystallographic orientation for the grain-competition question. Bounded scalars; §13.1 met.

Layout is a grid, and here the anisotropy problem is at its worst in the whole catalog — worse even than in #23 and #25 — for a specific and instructive reason. **Real dendrites grow along preferred crystal directions, and a square lattice also has preferred directions.** The two are easy to confuse. A lattice model can produce four-fold dendrites that look correct while merely displaying its own grid, and distinguishing physical anisotropy from lattice anisotropy is a known, hard, documented problem in the CA-solidification literature. Grain orientation makes it worse: a grain oriented at 30 degrees to the lattice must not grow differently from one aligned with it, and on a naive lattice it will.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible, and I would grade it below the catalog's silence would suggest. This is not where SCR should start in Family E.**

The reasons compound. The theory covers the main questions. Phase-field is a strong, validated, quantitative incumbent. Cellular automaton solidification models are *already industrial practice*, so SCR offers no methodological novelty. And the lattice anisotropy problem is not a caveat here but a direct threat to the headline output, because dendrite morphology is the thing being measured and the grid produces morphology of its own.

**The upside worth being excited about.** One genuine thing: **grain competition is a selection process on initial conditions**, and selection processes are what this platform is good at studying in ensemble. Which nucleation events dominate a casting, across many runs from statistically identical starting states, is a distribution question, and the resulting texture is measurable by electron backscatter diffraction on real castings. That is a checkable ensemble result.

The cross-Lab connection is also notable: this is the fourth appearance of the same diffusion-limited fingering instability, after tumour margins (#23), wound edges (#24), and biofilms (#25). Dendritic solidification is where that instability is best understood theoretically. If SCR wants to demonstrate mechanism transfer between Labs, this is the one with the rigorous theory attached — the physics Lab that explains the biology Labs.

**The challenges, in order of severity.**

1. **Lattice anisotropy is indistinguishable from crystal anisotropy** on a naive grid, and morphology is the output.
2. **Phase-field is a strong quantitative incumbent** for exactly these questions.
3. **CA solidification is already industrial practice** — no methodological novelty.
4. **The reducible core covers most real questions.**
5. **Temperature and solute are diffusing fields** the mechanism modifies — DEC-1 in its mild form, but two of them.

## Non-claims

This Lab does not predict microstructure in any real casting, does not bear on materials qualification or component performance, and produces nothing suitable for engineering decisions (§41, §43).
