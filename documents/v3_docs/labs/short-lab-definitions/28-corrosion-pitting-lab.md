# 28. Corrosion Pitting Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #28, Family E · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Stainless steel does not rust because a passive oxide film covers it. Pitting is what happens when that film fails at a point. A tiny break lets the metal beneath dissolve; the dissolving metal makes the local chemistry inside the pit more aggressive — more acidic, more chloride-concentrated — which prevents the film from re-forming and accelerates dissolution further.

So a pit, once established, digs itself deeper. The autocatalysis is the whole mechanism, and it is why pitting is so dangerous: a component can be almost entirely intact and fail through a single pinhole. Most pits initiate and immediately die; a few become stable and grow indefinitely. Which ones is the question.

The engineering consequence is stark. Pitting causes leaks, stress corrosion cracking initiation, and failures in pipelines, heat exchangers, aircraft skins, and storage tanks — and the failure is governed by the *deepest single pit*, not by the average corrosion rate.

## What the domain already knows

**Extreme value statistics is the operational method, and it works.** Because failure is governed by the deepest pit, the field fits extreme-value distributions (Gumbel and relatives) to maximum pit depths measured on inspection coupons and extrapolates to the largest pit likely on a much larger structure. This is standard practice in pipeline and tank integrity management. It is a genuine statistical shortcut that requires no mechanism at all.

**Pit growth kinetics have power laws.** Pit depth typically grows as a power of time with an exponent commonly near one third, reflecting diffusion-limited transport out of the pit. Given an established pit, the growth trajectory is approximately known.

**The stability criterion is understood.** A pit remains active only if the product of current density and pit depth exceeds a threshold that maintains the aggressive internal chemistry — a condition well established in the electrochemistry literature. Below it, the pit repassivates and dies.

**Lattice modelling exists but is not canonical.** Cellular automaton models of pitting and passive film breakdown have been published since the 1990s *(Córdoba-Torres, di Caprio and others; attribution from memory)*, and the domain is closely related to well-studied lattice problems: invasion percolation, corrosion fronts, and etching models.

## Where the shortcut holds, and where it breaks

**Reducible.** Maximum pit depth on a structure, given inspection data — extreme value statistics, and it is the method in actual use. Growth of an established isolated pit — power law. Whether a pit is stable — the depth-current criterion. Whether an alloy pits at all in a given environment — the pitting potential, measured electrochemically and tabulated.

That is a substantial reducible core, and it covers most of what industry asks. **A Lab here must be honest that the practising engineer's question already has a serviceable answer.**

**Irreducible.** What the statistics assume away:

- **Pit interaction.** Pits are not independent. An active pit consumes the surrounding surface's cathodic capacity and changes the local chemistry, which suppresses initiation nearby — a shielding effect. That makes the spatial distribution of pits non-random, and extreme value statistics fitted on an independence assumption is estimating the wrong distribution.
- **Which pit survives.** Most initiation events die. Whether a specific one crosses into stability depends on local microstructure — an inclusion, a grain boundary, a scratch — and on the accumulating chemistry inside it. Amplified microscopic difference, again.
- **Coalescence and percolation.** Pits that meet merge into larger features, and a corroding layer can percolate through a thin section. The transition from "many small pits" to "a through-wall path" is a connectivity question with a threshold.
- **Front roughening.** General corrosion fronts roughen with scaling exponents that place them in a universality class, but real surfaces with heterogeneous microstructure deviate, and the deviation is the interesting part.

**The lens, stated plainly.** This Lab's opening is unusually specific and worth stating as the whole pitch: **the industrial method assumes pits are independent, and they are not.** Everything SCR could contribute lives in that gap. Not a better pit growth model — the growth law is fine — but an answer to what pit *populations* do when the pits interact, and whether that changes the extreme-value extrapolation that safety cases rest on.

## What a Cell would carry

A patch of surface or a volume element of metal: metal present or dissolved, passive film integrity, local aggressive-species concentration, and possibly microstructural susceptibility (inclusion present, grain boundary). Bounded scalars; §13.1 met easily.

Layout is a grid, physically honest for a surface. Two qualifications. **Pitting is three-dimensional** — pits undercut and grow laterally beneath an intact surface, producing the characteristic bottle shape, and a 2D surface model loses that. And **the electrochemistry is coupled through the electrolyte**, which is a shared, effectively non-local resource: the cathodic reaction on the whole surface supports the anodic reaction in the pit. That coupling is the mechanism behind pit shielding and it is not a neighbour interaction.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the clearest commercial framing in Family E and the widest abstraction gap.**

The position paper's grading note is exact: *"real precedent, but predictive versions need electrochemical state that strains the simplicity premise."* Corrosion is electrochemistry — potentials, currents, ion transport, pH — and abstracting it into neighbour rules discards the physics that determines everything. A cellular model of pitting is a model of a *caricature* of pitting, and the caricature may or may not preserve the population behaviour that is the target.

**The upside worth being excited about.** The independence assumption is a real, load-bearing, questionable assumption in a method used for safety-critical asset integrity decisions on pipelines and tanks. Nobody is going to replace extreme-value statistics with a cellular model — but demonstrating, across many candidate interaction mechanisms, that pit interaction systematically biases the extrapolated maximum depth in a particular direction would be genuinely useful and could be stated without any claim to predict a specific structure.

That framing has the shape the position paper recommends: not competing with the incumbent method, but characterizing an assumption the incumbent method makes.

Data is also better than most of Family E: inspection datasets with thousands of measured pit depths and locations exist in industry, and laboratory pitting experiments on coupons are standard and quantified.

**The challenges, in order of severity.**

1. **The physics is electrochemical and the abstraction discards it.** The deepest problem, and it is not fixable by care.
2. **The electrolyte couples the whole surface**, so the mechanism is not local in the way the platform assumes.
3. **The incumbent statistical method works** for the question industry asks.
4. **Safety-critical credibility hazard.** Anything resembling a corrosion prediction for a real asset is dangerous; §30.7 applies with unusual force.
5. **Pits are 3D and undercut**, which a surface lattice cannot represent.

## Non-claims

This Lab does not assess corrosion or integrity of any real component, does not predict failure, and produces nothing suitable for engineering, inspection, or safety decisions (§41, §43).
