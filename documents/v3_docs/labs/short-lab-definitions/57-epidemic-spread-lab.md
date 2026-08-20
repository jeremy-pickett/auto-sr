# 57. Epidemic Spread Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #57, Family I · **Standing:** **[weak]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

An infectious disease passes between people who come into contact. From that entirely local transmission event, repeated, come epidemic curves, waves, spatial spread, herd immunity thresholds, and the extinction or persistence of the pathogen.

The quantities practitioners care about are the growth rate early on, the eventual attack rate, whether an intervention pushes transmission below the self-sustaining threshold, and how fast the disease moves geographically.

## What the domain already knows

**This is one of the most mathematically developed applied fields in existence, and that is the entire problem with the Lab.**

The compartmental framework — susceptible, infectious, recovered — dates to Kermack and McKendrick in 1927 and gives the epidemic curve, the final size relation, and the threshold condition in closed form. The **basic reproduction number** R₀ is the field's central quantity: above one the epidemic grows, below one it dies out, and the herd immunity threshold is 1 − 1/R₀. These are exact results for the well-mixed case.

**The network version is also largely solved analytically.** Epidemic thresholds on contact networks depend on the degree distribution, and the striking result — that the threshold **vanishes** on scale-free networks with a heavy enough tail, so any transmissibility can sustain an epidemic — is a closed-form result *(Pastor-Satorras and Vespignani, 2001)*. Percolation theory maps epidemics on networks to bond percolation, giving final sizes and thresholds analytically.

**And the field knows contact networks are not lattices.** Contact structure is heavy-tailed, clustered, assortative by age, and has long-range links from travel. The last of these is decisive: metapopulation models coupling local transmission to air travel networks reproduce global spread timing well, and the reason they work is that **long-range mixing dominates the geography.**

**The incumbents are formidable.** National-scale agent-based epidemic models with realistic demography, household and workplace structure, and mobility data are built by well-funded groups and used in policy. Whatever criticism they attract, they are not naive and they do not use square lattices.

## Where the shortcut holds, and where it breaks

**Reducible.** Growth rate from R₀. Final attack rate. Herd immunity threshold. Epidemic threshold on a network of given degree distribution. Effect of a uniform reduction in transmission. Time to peak. **This is the great majority of what anyone asks, and it has closed-form answers.**

**Irreducible.** Genuinely:

- **Spatial spread through structured populations** where the network is neither well-mixed nor a lattice.
- **Superspreading.** Transmission is highly overdispersed — a small fraction of cases cause most infections — and overdispersion makes early outbreak outcomes bimodal and stochastic in a way mean R₀ does not capture. Whether a chain takes off or dies is genuinely uncertain.
- **Behavioural feedback.** People change contact behaviour in response to perceived risk, which changes transmission, which changes perceived risk. Coupled and not closed-form.
- **Intervention timing on heterogeneous structures**, where who is reached matters more than how many.

**The lens, stated plainly — and it is the position paper's diagnosis, which I endorse.** The weakness here is precise: **a lattice gives the wrong wave speed, because the real interaction topology is not spatial.** Disease does not spread from a town to the adjacent town; it spreads from a town to a city on the other side of the country because someone flew. A grid model produces a smooth advancing front, which is a picture of a process that does not occur.

Worse, the grid model produces a *convincing* front. Epidemic wave animations on maps are visually persuasive and were widely circulated during recent public health events, frequently by people who did not understand what the model assumed.

## What a Cell would carry

An individual or a population patch: infection state, immunity, contact rate, and possibly behaviour or intervention status. Bounded and small; §13.1 met about as easily as anywhere.

**Layout is the whole problem.** The honest Layout is a Network World with a measured contact structure — which is #47's Layout family, and it is what the serious models use. A Grid World is defensible only for a genuinely spatial process, and human disease transmission is not one at any scale above a household.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak, and the inherited grade is correct. I would additionally argue this is the catalog's most *dangerous* weak entry, and that it should be treated with more care than a simple "poor fit" implies.**

The technical case is straightforward and the catalog states it: wrong topology, wrong wave speeds, qualitative only, and say so loudly.

But there is a second consideration that the catalog does not raise and that I think should be raised explicitly. **Epidemic modelling output has an extraordinary capacity to escape its caveats.** During public health emergencies, model output circulates far beyond the people who understand it, is quoted in policy argument, and is used to support positions its authors did not hold. A visually compelling lattice epidemic animation produced by a mechanism-exploration platform, with a caption saying it predicts nothing, would be screenshotted without the caption within a day.

That is a §30.7 failure mode of a different kind from the rest of the catalog: not "a practitioner over-trusts it" but "it leaves the practitioner's hands entirely."

**The upside worth being excited about — narrow, and I would keep it narrow.** The **superspreading and stochastic extinction** thread is genuinely interesting and is not well served by mean-field reasoning: whether an introduced chain takes off is a branching process with high overdispersion, the outcome is bimodal, and the interesting quantity is a distribution rather than an expectation. That is ensemble-shaped and suits the platform.

But it is also entirely solvable with branching process theory for the abstract case, and the interesting version requires realistic contact structure, which returns to the Network World. There is no version of this Lab where a grid earns its place.

**The recommendation implicit in all of that:** if SCR wants to demonstrate contagion mechanisms, it should do so in a domain where nobody will mistake the output for public health advice — #54's worms, #25's bacterial colonies, or #14's invasion fronts — all of which share the mechanism class without the hazard.

**The challenges, in order of severity.**

1. **Public health credibility hazard, and it is the catalog's most likely to cause real harm** through decontextualized circulation rather than through direct misuse.
2. **The topology is not spatial**, so a lattice models a different process.
3. **The domain is analytically mature** and its residual questions are attacked with better tools.
4. **Strong, well-funded incumbents** using realistic contact structure.
5. **The output is unusually persuasive** relative to its content.

## Non-claims

This Lab does not model any real disease, does not predict transmission or outbreak dynamics, does not evaluate any intervention, and produces nothing suitable for public health, clinical, or policy decisions. Any grid-based result is qualitative only and does not correspond to any real population (§41, §43).
