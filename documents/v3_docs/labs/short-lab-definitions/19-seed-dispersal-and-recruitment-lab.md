# 19. Seed Dispersal and Recruitment Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #19, Family C · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A plant cannot move, so its entire spatial strategy is executed once, by its seeds. Where they land determines everything: whether they germinate, whether they survive, and where the next generation's seeds will be released from.

The landing distribution — the **dispersal kernel** — is usually sharply peaked near the parent with a long tail. Most seeds fall close. A few go far, carried by wind, water, or an animal that ate the fruit.

That geometry sets up a tension the field has argued about for fifty years. Near the parent, seed density is highest — and so is mortality, because specialized herbivores, seed predators, and pathogens concentrate where their host is dense. So the best place to land is neither at the parent's feet nor arbitrarily far, but somewhere in between. This is the **Janzen–Connell hypothesis** (independently proposed by both around 1970), and it is the standard candidate explanation for why tropical forests hold so many tree species rather than being dominated by whichever competes best.

## What the domain already knows

**Kernels are measured and fitted.** Seed trap arrays, seed tracking, and genetic parentage assignment produce empirical dispersal kernels for many species. Their functional forms — exponential, Gaussian, power-law, and mixtures — are catalogued, and the distinction between thin and fat tails is understood to matter enormously (this is the same fact that drives invasion acceleration in #14).

**Expected recruitment is a convolution.** Given a map of adults and a kernel, the expected seed rain at any point is a straightforward calculation. Multiply by a survival function and you have expected recruitment. No simulation is needed.

**Janzen–Connell has substantial empirical support and remains contested in its strong form.** Distance- and density-dependent mortality is repeatedly measured; whether it is sufficient to maintain observed diversity is the argued part.

**Spatially explicit neighbourhood models are the incumbent.** The forest-dynamics-plot tradition fits neighbourhood competition and survival models to stem-mapped census data directly — a statistical rather than mechanistic approach, and a good one.

## Where the shortcut holds, and where it breaks

**Reducible.** Expected seed shadow from a known adult distribution — convolution. Expected recruitment given survival functions — arithmetic. Mean dispersal distance, tail behaviour, and colonization probability at distance — closed-form for standard kernels. Equilibrium spatial pattern of a single species under simple assumptions — analytically approachable through spatial point-process theory, which is a well-developed field with real results.

That last point deserves emphasis. **Spatial statistics already has a mathematics for this.** Point-process theory handles clustered patterns, pair correlation functions, and inhibition processes analytically. A lattice simulation of seed rain is often reproducing something a point process describes in closed form.

**Irreducible.** What survives that:

- **Multi-generation feedback.** This generation's recruits become next generation's parents, so the adult map that determines the seed shadow is itself produced by earlier seed shadows. Iterate for centuries with density-dependent mortality and the resulting spatial genetic and species structure has no closed form.
- **Multi-species Janzen–Connell.** With many species each suppressing their own recruits locally, coexistence becomes a spatially-mediated dynamic outcome. Whether it holds depends on the arrangement of everything, and the sufficiency question — the contested one — is precisely a question about the dynamics rather than the equilibrium.
- **Disperser behaviour.** Animal-dispersed seeds do not follow a kernel; they follow an animal, which visits fruiting trees, moves along routes, and defecates at perches. The resulting deposition is clustered in a structured, non-random way that no kernel captures.
- **Rare long-distance events founding new populations**, again the fat-tail problem, and again arrangement-dependent.

**The lens, stated plainly.** This Lab's honest position is uncomfortable and should be stated first: **for the single-generation question, the shortcut is complete.** A convolution answers it. The irreducible content only appears across many generations with feedback and multiple species — which is to say, this Lab is only interesting when it becomes a *different* Lab, closely resembling #15 and #14.

## What a Cell would carry

A patch of ground: occupancy and species of any established plant, seed bank contents by species, local pathogen or seed-predator pressure, and habitat suitability. Bounded if species count is bounded and small; §13.1 met with that qualification.

Layout is a grid. The recurring qualification is stronger here than anywhere: **dispersal is definitionally non-local**, and the fat tail is the part that matters. A Lab whose central mechanism is a long-range kernel is not obviously a local-mechanism Lab at all, and that tension should be stated rather than smoothed over.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak as a standalone Lab. I would not build it separately.**

The catalog distinguishes this from invasion ecology by saying "the mechanism of interest is reproductive rather than frontal," which is a real distinction but not, I think, enough to justify a separate Lab. The reducible core covers the single-generation question completely. The irreducible content is multi-generational feedback and multi-species coexistence — which is #15's territory — and the spread content is #14's. What remains that is uniquely this Lab's is the dispersal kernel itself, and a kernel is a World property, not a mechanism.

There is also a structural objection worth taking seriously: point-process theory and neighbourhood statistical models are established, well-suited, and used by the people who have the data. This is not an underserved question.

**The upside worth being excited about — and it is a platform point, not a domain one.** This Lab is the sharpest available test of a question the catalog raises repeatedly and never resolves: **is a long-range dispersal kernel a local mechanism?** Spotting in wildfire, saltation hops in dunes, satellite colonies in invasion, long-distance beetle flight, and scanning worms all have the same shape, and every one of those Labs punts on it. Here it is not a complication at the edge of the phenomenon — it *is* the phenomenon, so the question cannot be avoided.

If SCR wants one small Lab whose purpose is to force a decision about reach and non-local connection, this is the cheapest one to build and the hardest to fudge.

**The challenges, in order of severity.**

1. **The single-generation question is fully reducible.** Convolution.
2. **Substantial overlap with #14 and #15**, both of which are stronger.
3. **The central mechanism is non-local by construction**, which strains the platform's identity.
4. **Animal dispersers are agents**, not kernels — DEC-1 and possibly an Agent World.
5. **Timescale is generations**, so validation requires decades of census data that only a few sites have.

## Non-claims

This Lab does not model any real plant population, makes no claim about diversity maintenance in any real forest, and produces nothing suitable for conservation or forestry decisions (§41, §43).
