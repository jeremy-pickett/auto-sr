# 12. Vegetation Banding Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #12, Family B · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

In semi-arid landscapes, vegetation does not thin out evenly as rainfall declines. It organizes. Aerial photographs of the Sahel, the Horn of Africa, and arid Australia show regular stripes of dense vegetation alternating with bare ground — "tiger bush" — with spacing of tens to hundreds of metres, running along contours, often migrating slowly upslope.

The mechanism is a short-range positive and long-range negative feedback. Plants improve the soil beneath them: roots open infiltration paths, litter shades and slows runoff, so water entering a vegetated patch stays there. That same capture starves the ground downslope. Local facilitation, distant competition — the classic pattern-forming combination.

As aridity increases, the pattern sequence is consistent and observed: uniform cover, then gaps in cover, then labyrinths, then isolated spots, then bare desert. That sequence is one of the most reproducible large-scale self-organization results in ecology.

## What the domain already knows

**Turing's mechanism applies, and the field says so explicitly.** The pattern arises from an activator–inhibitor structure in a reaction–diffusion–advection setting. **Klausmeier's 1999 model** is the canonical minimal formulation: plant biomass with local growth and mortality, water with rainfall input, downslope flow, and uptake concentrated under plants. From two equations it produces banded vegetation on slopes with the right spacing and upslope migration *(attribution from memory, verify)*. Rietkerk, van de Koppel, and colleagues extended this substantially through the 2000s.

**Linear stability gives the wavelength.** The spacing at pattern onset is predictable analytically from the model parameters, as is the existence condition and the migration speed. This is a genuine closed-form result for the most visually striking feature.

**The pattern sequence is proposed as an early-warning signal.** A significant literature argues that the progression from gaps to labyrinth to spots indicates approach to a catastrophic desertification transition, and that spatial statistics can warn before the shift *(Rietkerk, Scheffer, Kéfi and colleagues, mid-2000s onward)*. This claim is influential, actively debated, and not settled — critics question whether the indicators are reliable enough in noisy real data to be useful.

## Where the shortcut holds, and where it breaks

**Reducible.** Band wavelength at onset. Whether patterns form at all, given rainfall, slope, and plant parameters. Migration direction and approximate speed. The ordering of the morphology sequence with aridity. All available from stability analysis and bifurcation theory of the continuum models.

**Irreducible.** The parts the bifurcation diagram cannot reach:

- **Multistability and history.** In much of the parameter range, several patterns are simultaneously stable. Which one the landscape holds depends on how it got there, not on where it is. This is a well-recognized feature of the models ("the Busse balloon" of coexisting stable states) and it means the current pattern encodes history rather than only conditions.
- **Hysteresis and recovery.** Losing vegetation at one rainfall and regaining it at the same rainfall are not symmetric. Where a landscape lands on the way back depends on the path.
- **Pattern defects and transitions.** How a labyrinth becomes spots — through what defect dynamics, at what rate, and whether uniformly across the landscape — is not given by linear theory, and it is exactly what an early-warning indicator would need.
- **Heterogeneous terrain.** Real slopes vary. Where bands break, reconnect, or pin against topography is arrangement-dependent.

**The lens, stated plainly.** This domain divides cleanly and usefully: **linear theory owns onset; nonlinear history owns everything after.** The scientifically live question — can spatial pattern warn of desertification — sits entirely on the irreducible side, because it is a question about *transitions between multistable states under noise*, not about which state is stable. That is a question best attacked with many runs rather than one analysis, which is precisely this platform's shape.

## What a Cell would carry

A patch of ground: plant biomass or cover, soil water, infiltration capacity, and slope. Bounded and few; §13.1 met easily.

The Layout is a grid and it is defensible, with one important qualification: **the mechanism is directional.** Water runs downhill, so Connections are asymmetric, and the asymmetry is what makes bands rather than spots. This is one of the clearest cases in the catalog where a symmetric neighbourhood would destroy the phenomenon.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong — arguably stronger than several graded entries, and I would rate it above the catalog's silence.**

The case is unusually complete. The mechanism is genuinely local and physically grounded. The pattern is measured from aerial and satellite imagery across multiple continents. The reducible core is well-characterized, so the boundary of SCR's contribution is knowable rather than guessed. The irreducible remainder — multistability, hysteresis, transition dynamics — is where the field's live controversy sits. And the stakes are real: desertification affects large populations, and early-warning indicators are being proposed for actual use.

**The upside worth being excited about.** The early-warning debate is a hypothesis-supply problem in the exact sense the position paper describes. The question "which spatial statistic reliably precedes collapse, under which mechanism families" cannot be settled analytically because it depends on the transition dynamics, and it is expensive to settle with careful bespoke models. Generating many candidate local mechanisms, running each to collapse under varied noise, and recording which indicators fired — including the eleven mechanism families where no indicator worked — is a genuinely useful contribution, and the negative space is as valuable as the positive.

Long-term satellite records (Landsat back to the 1970s) let modelled pattern sequences be compared against observed ones over decades in real landscapes.

**The challenges, in order of severity.**

1. **Water flow is a second mechanism** — arguably the primary one. DEC-1 blocks the clean formulation, and the catalog flags this entry accordingly.
2. **Rediscovery risk on onset.** Klausmeier-class results are established; anything about wavelength is already known.
3. **Grazing, fire, and land use** are the real drivers in many banded landscapes and are not local plant–water mechanisms.
4. **Timescale is decades**, so a step is a season at best.
5. **Policy hazard.** Desertification claims carry weight; §30.7 applies.

## Non-claims

This Lab does not assess desertification risk at any real location, does not validate or invalidate early-warning indicators for operational use, and produces nothing suitable for land management or policy decisions (§41, §43).
