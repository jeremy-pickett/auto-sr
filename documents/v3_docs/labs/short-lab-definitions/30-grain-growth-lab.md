# 30. Grain Growth Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #30, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A piece of metal is a mosaic of crystal grains, each with its own orientation, meeting at boundaries. Those boundaries carry energy, so the system can lower its energy by having fewer of them. Heat the metal and the boundaries move: large grains eat small ones, small grains shrink and vanish, and the average grain size grows.

This matters because grain size controls strength. The Hall–Petch relationship — yield strength rising as grain size falls — is one of the most-used relations in metallurgy, and controlling grain size through thermal processing is a routine industrial lever.

Occasionally the process goes wrong in an interesting way: a few grains grow enormously while the rest stay small. **Abnormal grain growth** ruins mechanical properties and is a recurring industrial problem, and it is not fully predictable.

## What the domain already knows

This is the most rigorously reduced domain in the entire catalog, and a Lab here must confront that immediately.

**Individual grain growth in two dimensions has an exact law.** The von Neumann–Mullins relation states that a two-dimensional grain's area changes at a rate proportional to (n − 6), where n is its number of sides — nothing else. Six-sided grains are stationary; grains with fewer sides shrink; grains with more grow. It is exact, it depends only on topology, and it dates to the 1950s.

**The three-dimensional generalization exists too.** MacPherson and Srolovitz published the exact 3D analogue in 2007, expressing volume change in terms of a mean width and total edge length *(attribution from memory, verify)*. So the per-grain evolution law is known exactly in both dimensions.

**Bulk kinetics follow.** Mean grain size grows as the square root of time under ideal conditions, and the normalized grain size distribution reaches a self-similar steady state — measured, simulated, and theorized consistently.

**The canonical lattice model is the Monte Carlo Potts model**, introduced for grain growth by Anderson, Srolovitz, Grest, and Sahni in the mid-1980s *(attribution from memory, verify)*. Sites carry an orientation label; boundary energy is counted between unlike neighbours; sites flip by Metropolis dynamics. It reproduces the growth exponent, the self-similar size distribution, and the topological statistics. It is textbook, it is a cellular model, and it has been running for forty years.

**Pinning is understood.** Second-phase particles exert a drag that stalls boundary motion — the Zener pinning limit — giving a predictable maximum grain size for a given particle dispersion.

## Where the shortcut holds, and where it breaks

**Reducible.** Individual grain evolution — exactly, from topology alone. Mean size growth exponent. Steady-state size distribution. Topological statistics (side-number distributions, the Aboav–Weaire relation). Zener limiting size. Hall–Petch strength from grain size. **This is close to a complete answer for normal grain growth.**

**Irreducible.** A short list, but not an empty one:

- **Abnormal grain growth.** A few grains escaping the normal distribution is a symmetry-breaking event triggered by local conditions — a particularly favourable orientation relationship, a local absence of pinning particles, a boundary with anomalously high mobility. Which grain goes abnormal, and whether the phenomenon occurs at all in a given microstructure, is not predicted by the mean-field theory. This is an active industrial problem.
- **Anisotropic boundary properties.** Real boundary energy and mobility depend strongly on the misorientation between the two grains, and special boundaries behave very differently. With anisotropic properties, the clean topological laws no longer apply and the evolution becomes genuinely arrangement-dependent.
- **Texture evolution.** The orientation distribution of the whole population evolves, and which orientations win depends on the network of boundary properties, not on any single grain.
- **Pinning breakdown.** Particles coarsen or dissolve during annealing, releasing boundaries unevenly, which is a route to abnormal growth.

**The lens, stated plainly.** This Lab is the catalog's **strongest reducibility case, and therefore its best calibration instrument.** When the domain has an exact law, a generated mechanism either reproduces it or it does not, and the check is arithmetic. That is not a research contribution — it is a *test of the platform*, and a very good one, because almost nothing else in this catalog offers an exact answer to check against.

The residual research content is real but narrow: abnormal growth under anisotropic boundary properties, where the exact laws stop applying.

## What a Cell would carry

A lattice site: a crystallographic orientation label, and possibly a pinning-particle flag or stored-energy value. This is the smallest state in the catalog — the Potts model uses a single integer. §13.1 is met more trivially than anywhere.

Layout is a grid, and lattice artifacts are a **known and documented problem here specifically**. Square-lattice Potts models produce faceted grain boundaries and can freeze at low simulation temperature because boundaries lock onto lattice directions. The field solved this decades ago by using larger neighbourhoods, finite simulation temperature, and triangular lattices. **A Lab that reproduces this artifact will be reproducing a mistake the field corrected in the 1980s**, and should know the corrections before starting.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak as research, excellent as a calibration anchor. I would build it for the second reason and say so plainly.**

There is no serious argument that SCR contributes to normal grain growth. The evolution law is exact. The bulk kinetics are settled. The canonical lattice model is forty years old, well understood, and available in several implementations. Generating rules that reproduce the square-root growth law is rediscovering a textbook.

**The upside worth being excited about — and it is genuinely valuable, just not to metallurgy.** This Lab offers something almost no other entry does: **an exact analytic answer that a generated mechanism can be checked against, cheaply, in bulk.** The von Neumann–Mullins relation is a per-grain, per-step prediction. A Run either satisfies it or does not, and the deviation is measurable.

That makes this the natural home for questions about the *platform*: does the generation pipeline produce mechanisms that respect known physics? Does the corpus's negative space match what theory says is impossible? Does a rule described in English as "boundaries move toward their centre of curvature" actually produce (n − 6) behaviour, or does the intent–outcome gap open? Wildfire is the calibration anchor for *plausibility*; grain growth could be the calibration anchor for *correctness*, which is a stronger and rarer thing.

The residual research angle — abnormal grain growth under anisotropic boundary character — is legitimate, industrially relevant, and not fully solved. It is a small target but a real one, and electron backscatter diffraction gives directly comparable data: full orientation maps of real microstructures, from which grain size distributions, topological statistics, and misorientation distributions are all measurable.

**The challenges, in order of severity.**

1. **The domain is essentially solved** for the questions normally asked.
2. **Lattice faceting is a documented artifact** with documented fixes the Lab must adopt.
3. **The canonical model is a forty-year-old cellular model** — zero methodological novelty.
4. **Orientation as a state variable** is bounded only if the orientation space is discretized, which is itself a modelling choice with consequences.
5. **Small research target** in the anisotropic/abnormal regime.

## Non-claims

This Lab does not predict microstructure in any real material, does not bear on materials qualification or processing decisions, and produces nothing suitable for engineering use (§41, §43).
