# 10. Snow and Crystal Growth Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #10, Family B · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A snow crystal grows by vapour depositing on ice. Water molecules diffuse toward the crystal, and a protruding tip intercepts more of them than a flat face does, so it grows faster and protrudes more. That instability is what produces branches, and repeated on the branches, sidebranches.

The result is the familiar six-fold dendrite — but also plates, columns, needles, sectored plates, capped columns, and a dozen other named morphologies. Which one you get depends almost entirely on two numbers: temperature and supersaturation.

## What the domain already knows

**The morphology diagram is the reducible answer, and it is old.** Nakaya's mid-twentieth-century work mapped crystal habit against temperature and supersaturation, and the resulting diagram — plates near −2 °C, columns near −5 °C, plates again near −15 °C, and dendrites at high supersaturation — is a textbook result *(Nakaya, 1954; attribution from memory)*. Given the conditions, the habit class is known. Why the habit alternates with temperature remains genuinely open, which is worth noting: the *diagram* is settled, the *explanation* is not.

**The instability has an analytic onset.** The Mullins–Sekerka analysis (1964) gives the linear stability condition for a growing interface against perturbations — the point at which a smooth front starts to finger. Related solvability theory predicts dendrite tip velocity and radius from the undercooling. These are real closed-form results covering the onset and the tip.

**The lattice precedent is exceptional.** Gravner and Griffeath built a three-dimensional cellular model of snow crystal growth (published around 2008) with local rules for vapour diffusion, freezing, and attachment, and produced a catalogue of forms that look convincingly like real snow crystals and span the observed morphology classes *(attribution from memory, verify)*. It is one of the most visually compelling CA results in existence. Kenneth Libbrecht's experimental programme is the corresponding physics reference.

Related and equally relevant: diffusion-limited aggregation (Witten and Sander, 1981) is the minimal lattice model of the same instability and produces fractal dendritic clusters from a rule with one line of content.

## Where the shortcut holds, and where it breaks

**Reducible.** Habit class from temperature and supersaturation — read the diagram. Onset of the branching instability — Mullins–Sekerka. Dendrite tip speed and radius — solvability theory. Fractal dimension of a DLA cluster — measured to high precision decades ago and universal.

**Irreducible.** What survives:

- **The specific crystal.** Two crystals grown side by side in the same chamber are not identical. Their shared history of conditions makes them similar; the fine structure is set by fluctuation amplified through an unstable interface. This is the source of the folk claim that no two snowflakes are alike, and it is true for the honest reason: the growth is an amplifier.
- **Sidebranch statistics.** Where and how often sidebranches appear along a growing arm is not given by tip theory; it is noise selected by the interface and is an active research question.
- **Symmetry.** Real crystals are often strikingly six-fold symmetric even though the six arms grow independently. The standard explanation — all six arms share the same environmental history — is plausible and hard to make quantitative. Whether local rules reproduce the observed *degree* of symmetry is a genuine open question and a good one.
- **Habit transitions during growth.** A crystal falling through changing conditions changes habit mid-growth, producing capped columns and similar composites. The record of the atmosphere is written into the crystal, and reading it backward is an inverse problem.

**The lens, stated plainly.** This domain is the catalog's purest illustration of **"class is predictable, instance is not."** Nakaya tells you it will be a dendrite. Nothing tells you which dendrite. The position paper's grade — *"gorgeous fit, tiny audience"* — is exactly right, and a Lab here must be honest that the gorgeousness is the risk: this is the single easiest place in the catalog to produce spectacular images that add nothing.

## What a Cell would carry

A lattice site: ice or vapour state, local vapour density, attached mass, and possibly a boundary-layer or quasi-liquid-layer variable. Very small state; §13.1 trivially met.

Layout has a real subtlety: **the honest lattice is triangular or hexagonal, not square.** Six-fold symmetry is a property of the ice crystal structure, and imposing it via lattice geometry is legitimate here in a way it is not elsewhere — the anisotropy is physical, not an artifact. This is the one Lab where lattice anisotropy is a feature. Gravner–Griffeath use a hexagonal arrangement for precisely this reason.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible on fit, weak on need, and dangerous on aesthetics.**

Everything about the mechanism suits the platform. Everything about the situation argues against building it for domain value: the reducible core is settled, the canonical cellular model exists and is excellent, the audience is a handful of researchers, and the commercial application is essentially zero.

**The upside worth being excited about — and it is real, just not about snow.** This Lab is the best available **demonstrator of the platform's honesty machinery**, for one reason: it is the domain where beautiful output is most obviously not evidence. If SCR can run this Lab and consistently say "this is a lovely picture and it tells you nothing you did not know from the Nakaya diagram," the platform has demonstrated the discipline that SCR-F §12 and §26 demand, on the hardest case. Every other Lab's visualization-deception risk is easier than this one.

There is also a real open question — sidebranch statistics and the origin of symmetry — where mechanism supply is a defensible contribution, and where the experimental data (Libbrecht-style controlled-chamber growth) is genuinely excellent.

**The challenges, in order of severity.**

1. **Beauty is the failure mode.** Convincing images with no informational content, produced effortlessly.
2. **Rediscovery.** Gravner–Griffeath did this, thoroughly.
3. **The reducible core covers most questions anyone asks.**
4. **Tiny audience, no commercial path.**
5. **Vapour diffusion is a second field** the crystal both reads and depletes — DEC-1 in a mild form.

## Non-claims

This Lab makes no claim about atmospheric processes, precipitation, or crystal physics beyond generating candidate mechanisms, and produces nothing suitable for meteorological or scientific decisions without domain validation (§41, §43).
