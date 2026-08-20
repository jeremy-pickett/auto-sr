# 35. Catalytic Surface Reaction Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #35, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A catalyst works by letting reactants adsorb onto its surface, meet, react, and leave. On a platinum surface oxidizing carbon monoxide — the reaction in every car's catalytic converter — CO adsorbs as a molecule, oxygen adsorbs by splitting into two atoms on two adjacent empty sites, and when a CO and an O sit next to each other they combine and the CO₂ desorbs immediately, freeing both sites.

That requirement — oxygen needs *two* adjacent vacancies while CO needs only one — makes the surface competitive in an interesting way. Too much CO and the surface poisons: it is covered, oxygen cannot find a pair of adjacent sites, and the reaction stops. Too much oxygen and the surface saturates the other way. Only in between does the reaction run.

Under the right conditions the surface does not settle at all. It produces travelling waves, rotating spirals, standing patterns, and global oscillations in reaction rate — visible in real time, at micrometre resolution, on real platinum crystals.

## What the domain already knows

**The experimental work is Nobel-recognized.** Gerhard Ertl's group imaged these patterns on Pt(110) using photoemission electron microscopy, showing spirals and target patterns propagating across a catalyst surface, and Ertl received the 2007 Nobel Prize in Chemistry for the study of chemical processes on solid surfaces. The mechanism behind the oscillation is a **surface reconstruction**: the platinum surface switches between two atomic arrangements depending on CO coverage, and the two arrangements have different oxygen sticking probabilities. That gives the feedback with delay that an oscillator needs.

**The canonical lattice model is the ZGB model.** Ziff, Gulari, and Barshad (1986) wrote down exactly the rules described above — CO adsorbs on one site, O₂ on two adjacent sites, adjacent CO and O react — with a single parameter, the CO fraction in the gas *(attribution from memory, verify)*. It produces two kinetic phase transitions: a continuous one into the oxygen-poisoned state at low CO fraction, and an abrupt one into the CO-poisoned state at high CO fraction, with a reactive window between them.

The ZGB model is a genuinely important object in statistical physics. Its continuous transition belongs to the directed percolation universality class, which is one of the most robust universality classes known, and the model became a standard test case for absorbing-state phase transitions.

**Mean-field kinetics gets much of the rest.** Langmuir–Hinshelwood rate expressions describe the reaction rate from coverages and are standard in catalysis. Reaction–diffusion models of the pattern-forming regime are established.

## Where the shortcut holds, and where it breaks

**Reducible.** Mean-field reaction rate from coverages. The phase diagram of the ZGB model — computed, published, and studied for forty years. Critical exponents at the continuous transition — directed percolation, universal, tabulated. Wave speed in the pattern-forming regime — a reaction–diffusion result. Onset of oscillation from the reconstruction feedback.

**Irreducible.** What remains:

- **Pattern selection.** Spirals, targets, standing waves, and turbulent regimes all occur, and which appears depends on conditions and history in ways that reaction–diffusion analysis constrains but does not determine.
- **Poisoning as an absorbing state.** Once a surface poisons, it does not spontaneously recover — the state is absorbing, which means the system has irreversible history. Whether a given surface poisons depends on fluctuation, and near the transition the outcome for a specific run is genuinely undetermined.
- **Surface structure effects.** Real catalysts are nanoparticles with facets, edges, and steps, not infinite single crystals. Reactivity varies enormously between site types, and how a nanoparticle's mixture of site types produces its overall behaviour is a live question in the field.
- **Fluctuation-dominated behaviour on small particles.** A nanoparticle has few hundred surface sites. Mean-field kinetics assumes many; at these sizes the reaction can oscillate or switch states from stochastic fluctuation alone, which has been observed.

**The lens, stated plainly.** This Lab is unusual in Family E: **the canonical model of the domain is already exactly the kind of object SCR generates** — a handful of local rules with one parameter, producing phase transitions and patterns. There is no abstraction gap to argue about. The rules *are* the chemistry, at the level of description used.

The corresponding weakness is equally clean: because the model is so canonical, forty years of people have studied it, and its phase diagram and universality class are settled. Rediscovery risk is at its maximum.

## What a Cell would carry

A surface site: occupancy (empty, CO, O), and for the oscillating case a surface reconstruction state. Possibly a site-type label for the nanoparticle question. This is the smallest state in the catalog — one small enumerated value. §13.1 is met about as trivially as it can be.

Layout is a grid and the grid *is* the physics: a crystal surface is a lattice of adsorption sites. Along with #10 and #33, this is one of the few Labs where lattice discreteness is not an approximation. The honest lattice is the crystallography — square for Pt(100), hexagonal for Pt(111) — and the choice matters, because the two-adjacent-site requirement for oxygen depends on the neighbour structure.

That is a notable and rare property: **changing the lattice here changes the chemistry, correctly.**

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible on fit — genuinely the best mechanism-to-reality correspondence in Family E — and weak on contribution, because the canonical model is already the answer.**

The fit deserves emphasis because it is unusual. In most Labs, "a Cell is a patch of terrain" or "a Cell is a host" is an abstraction with real losses. Here a Cell is an adsorption site, and an adsorption site is a real, discrete, countable thing with a small number of possible states. The correspondence is nearly exact. If a fit review wants a worked example of what a *good* World fit looks like (§30.2), this is it.

**The upside worth being excited about.** Two threads.

First, the **nanoparticle regime is under-explored and matters commercially.** Real catalysts are small particles where mean-field kinetics fails, site heterogeneity dominates, and fluctuations are large. Asking which local rule structures produce robust reactivity versus fluctuation-driven poisoning, across many candidate mechanisms and many particle geometries, is an ensemble question in a field that mostly does careful single-system studies.

Second, and more valuable to the platform: this Lab has an **exact, published, forty-year-old reference phase diagram**. Like grain growth (#30), it can serve as a *correctness* anchor — does generation, asked in English for "a surface reaction where one species needs two adjacent free sites," produce something with the ZGB phase structure? That is a sharp test of the whole Stage A to Stage C chain, checkable against a known answer.

Experimental comparison is also exceptional: PEEM imaging produces movies of the patterns, at real spatial and temporal resolution, which is the same data type a Run stores.

**The challenges, in order of severity.**

1. **Rediscovery is nearly certain.** ZGB is canonical and thoroughly studied.
2. **Universality again flattens differences** near the continuous transition (see #33).
3. **The oscillating case needs surface reconstruction**, which is a second coupled mechanism (DEC-1).
4. **Small audience** in surface science, though the commercial catalysis industry behind it is large.
5. **Real catalysts operate at pressures far above the ultra-high vacuum where the beautiful experiments were done** — the "pressure gap" is a known and serious issue in translating these results.

## Non-claims

This Lab does not model any real catalyst, does not bear on catalyst design, performance, or emissions, and produces nothing suitable for chemical or engineering decisions (§41, §43).
