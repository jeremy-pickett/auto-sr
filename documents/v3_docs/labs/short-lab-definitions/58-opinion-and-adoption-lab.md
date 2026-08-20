# 58. Opinion and Adoption Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #58, Family I · **Standing:** **[weak]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

People's views and choices are influenced by the people around them. From that, at population scale, come consensus, persistent disagreement, regional blocs holding different views, minorities that never disappear, and adoption curves for products and practices that take off suddenly after a long quiet period.

The questions asked are whether a population converges, how long it takes, whether minority positions survive, and what makes an adoption cascade start.

## What the domain already knows

**The lattice models are old, canonical, and — crucially — exactly solvable in low dimensions.**

The **voter model** is the minimal version: each individual adopts a randomly chosen neighbour's opinion. Its behaviour on lattices is understood rigorously. In one and two dimensions the system coarsens to consensus, with domain sizes growing as a known power of time and consensus time scaling with system size in a known way; in three dimensions and above it does not reach consensus in the infinite system. These are theorems, not simulation results.

**Related models are equally well studied.** The Ising model with zero-temperature dynamics is the physics parent. The Sznajd model, the majority-rule model, bounded-confidence models (Deffuant, Hegselmann–Krause), and Axelrod's culture model all have substantial literatures with analytic and numerical results, and the statistical physics of social dynamics has been reviewed comprehensively — Castellano, Fortunato, and Loreto's review around 2009 is the standard reference *(attribution from memory, verify)*.

**Threshold models cover adoption.** Granovetter's threshold model (1978) and Watts's global cascade model on random networks (2002) give the conditions under which a cascade occurs, including the counterintuitive result that cascades are possible only in a window of connectivity — too sparse and nothing spreads, too dense and everyone's threshold is stabilized by their many unconvinced neighbours *(attribution from memory, verify)*.

**Empirical validation is the field's persistent weakness**, and this is widely acknowledged. The models are elegant; connecting them to measured opinion change in real populations is very hard, and the literature is repeatedly criticized on exactly this point.

## Where the shortcut holds, and where it breaks

**Reducible — extensively, and by theorem rather than by approximation.** Voter model coarsening exponents and consensus times on lattices. Ising universality. Cascade windows on random graphs. Bounded-confidence fragmentation thresholds. **The lattice versions of these models are among the most completely solved objects in this entire catalog.**

That is the decisive fact. A Lab generating opinion-dynamics mechanisms on a grid would be exploring a space whose central examples have been solved analytically for decades.

**Irreducible.** What remains:

- **Behaviour on real social topologies** — clustered, heavy-tailed, assortative, with community structure — where the lattice results do not transfer.
- **Coupled multi-issue dynamics** where opinions on different topics correlate and reinforce, which is closer to Axelrod's model and less tractable.
- **Co-evolution of opinion and network.** People change who they talk to based on what those people think. That is self-constructed topology (#18, #48, #56), it produces fragmentation into disconnected like-minded groups, and it is not analytically solved.
- **Media and algorithmic influence**, which is a broadcast rather than a local mechanism and dominates in practice.

**The lens, stated plainly.** The position paper's diagnosis is *"the real influence structure is a social network wearing a grid costume,"* which is exactly right, and there is a second problem stacked on top of it.

Even granting the grid, **the grid version is solved.** So the Lab fails twice: the abstraction is wrong for the domain, and where the abstraction is right, the answer is already a theorem. That is a stronger rejection than #57's, which at least has a genuine irreducible residue in superspreading.

## What a Cell would carry

An individual: current opinion or adoption state, threshold or stubbornness, and possibly confidence. Extremely small state; §13.1 met trivially.

**Layout is emphatically not a grid.** Social influence follows a social network, and social networks are structurally unlike lattices in every property that matters to these dynamics — degree distribution, clustering, path length, community structure.

There is a further and deeper problem worth naming. **These models represent people as scalar-valued automata**, and the mapping from "opinion" to a scalar is a modelling assumption with no measurement behind it. Physics Labs can point to a thermometer. This Lab cannot point to anything, and the field's own literature says so.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak, the inherited grade is right, and I would rank it below #57 — this is the weaker of the two [weak] entries.**

The reasoning: #57 has a genuinely irreducible residue (superspreading, stochastic extinction) and an enormous body of real measurement to be checked against, even though the lattice framing is wrong. This entry has neither. The lattice framing is wrong, the lattice results are theorems, and the empirical grounding is contested within the field itself.

**And the catalog already anticipated this.** Its §0 says economic and organizational domains are nearly absent *"because on the position paper's own criteria they tend to fail the same way opinion dynamics does."* Opinion dynamics is the named exemplar of a whole class of exclusions. That gives this entry a specific job — it is the reference case that justifies keeping a large family of domains out — and it should be written to do that job well.

**The upside worth being excited about — and it is entirely about the platform, not the domain.** Two things.

First, **co-evolving opinion and network** is the clearest, simplest, lowest-stakes instance of the self-constructed-topology problem that appears in #18, #48, #55, and #56. If the platform needs to test whether it can express a mechanism that rewires its own World, this is the cheapest domain to do it in: the state is one variable, the rule is two lines, and nobody will be harmed by getting it wrong. That is a real argument for building a small version.

Second, this Lab is a **calibration case for the fit review's ability to say no twice.** Most rejections in this catalog have one reason. This one has two independent ones — wrong substrate *and* already solved — and a review process that can articulate both, separately, is a better instrument than one that stops at the first.

**A caution the catalog does not raise.** Opinion dynamics output is politically legible in a way most of this catalog is not. A rendered simulation showing "how minorities become majorities" or "how consensus fragments" will be read as a claim about actual political processes, by people with strong priors, regardless of caveats. That is #57's decontextualization hazard in a domain where the audience is even less patient. It is a reason for restraint in presentation, not only in claims.

**The challenges, in order of severity.**

1. **The lattice results are theorems.** Nothing to discover in the grid version.
2. **The substrate is a social network**, not a lattice, and the difference changes every result.
3. **No measurement.** Opinion as a scalar has no instrument behind it, and the field acknowledges this.
4. **Political legibility** makes decontextualized misreading likely.
5. **Broadcast and algorithmic influence** dominate real dynamics and are not local mechanisms.

## Non-claims

This Lab does not model any real population, does not describe or predict opinion change, adoption, or political processes, and produces nothing suitable for social, commercial, or policy conclusions (§41, §43).
