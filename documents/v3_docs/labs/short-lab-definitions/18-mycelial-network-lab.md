# 18. Mycelial Network Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #18, Family C · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A fungus growing through soil or wood is not a shape; it is a search. Hyphal tips extend, branch, and fuse with each other. Where the network finds food, the connecting cords thicken and carry resource back. Where it finds nothing, the exploring branches are abandoned and reabsorbed.

The result is a network that continuously rebuilds itself — dense and reinforced where it pays, sparse and provisional where it does not. A single fungal individual can occupy hectares and persist for centuries, redistributing carbon and nutrients between distant points and, in mycorrhizal associations, between separate plants.

Two things make this distinctive among growth processes. The network **fuses** — branches that meet join, creating cycles — so it is not a tree. And it **withdraws**, reclaiming material from unproductive regions, so growth is not monotone.

## What the domain already knows

**The most famous demonstration is not a fungus.** The slime mould *Physarum polycephalum* was shown to connect food sources placed at the positions of cities around Tokyo with a network resembling the actual rail system in efficiency and fault tolerance *(Tero and colleagues, Science, 2010; attribution from memory, verify)*. The accompanying mathematical model — flow-reinforced tube adaptation, where tubes carrying more flow thicken and others decay — is simple, local, and has been widely reused as a network-optimization heuristic.

**Fungal network work is a real and separate literature.** Fricker, Boddy, and colleagues have imaged and quantified cord-forming fungal networks in the laboratory, measuring transport efficiency, resilience to damage, and network statistics against theoretical optima *(attribution from memory)*.

**Growth-only models are established elsewhere.** Diffusion-limited aggregation and Eden growth describe branching invasion without reinforcement or withdrawal, and hyphal growth models with tip extension and branching rules exist in mycology.

## Where the shortcut holds, and where it breaks

**Reducible.** Optimal network problems have answers: shortest path, minimum spanning tree, and Steiner tree are all solved or well-approximated by known algorithms, and the flow-reinforcement rule is understood as a heuristic that approaches such optima. If the question is "what is the best network connecting these points," algorithms answer it and the fungus is a curiosity rather than a method. Bulk growth rate from nutrient concentration is standard. Fractal dimension of unreinforced branching growth is a known DLA-class result.

**Irreducible.** The parts where the fungus is not solving a stated problem:

- **Foraging without knowing where the food is.** Optimization presumes the terminals are given. A fungus does not know; it must search, and the network it builds is a record of that search. Which regions get explored before resources run out is path-dependent.
- **Reinforcement and withdrawal together.** Adding flow-based decay makes the process non-monotone: connections that existed are removed, and removing one changes flow everywhere, which changes what decays next. That coupled feedback across a changing topology has no closed form.
- **Damage and rerouting.** Cut a cord and the network reorganizes. Whether it reroutes or fragments depends on the cycle structure that earlier growth happened to create.
- **Competition between individuals.** Two fungal networks meeting produce antagonistic interaction zones, and the boundary geometry depends on their respective histories.

**The lens, stated plainly.** The catalog says this Lab "sits awkwardly between a growth process and a network optimizer," and that is the right diagnosis. The awkwardness is informative: **when the terminals are known, the problem is reducible and algorithms win; when they must be found, it is irreducible and running is the only method.** That distinction generalizes well past fungi — it is the same boundary that separates attack-graph closure from adversarial search in #47, and route computation from route discovery in #46.

## What a Cell would carry

A patch of substrate or a segment of network: presence and thickness of hyphae or cord, local resource concentration, flow carried, and age or time since last reinforcement. Bounded scalars; §13.1 is met, though "flow carried" is the difficult one — see below.

**Layout is the real question and this Lab is a genuine boundary case (§15).** The substrate is spatial, which argues for a Grid World. The organism is a network with cycles, which argues for a Network World. And the network is *built by* the growth process rather than given in advance, which neither family cleanly accommodates: a World whose Connections are created and destroyed by the mechanism running inside it is a different thing from a World with a declared Layout.

That is worth stating plainly because it may be this Lab's most valuable contribution to the platform: **it asks whether SCR can express a mechanism that constructs its own topology.** If the answer is no, that is a real boundary, and the catalog said Labs are allowed to fail this way (§30, closing).

There is a second problem with the same flavour. **Flow is a global calculation.** Determining how much material moves through each cord requires solving a network flow problem over the whole structure — the Physarum model does exactly that at every step. A strictly local rule cannot compute it. Whether an honest local approximation exists is the Lab's central mechanism-fit question.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible as a domain, genuinely valuable as an architectural stress test.**

The domain case is thin. The audience is small, the reducible core covers the optimization framing, the famous result belongs to slime mould rather than fungi, and the interesting mechanism requires a global flow computation that violates the platform's central premise.

But the reason it fails is the interesting part, and it is a reason SCR should want documented. This Lab probes two boundaries at once: **self-constructed topology** and **globally-computed local drivers**. Both recur elsewhere in the catalog — the first in supply chains and routing, the second in coastal shadowing (#5), pond water level (#9), and stress transmission (#3, #31). Having one Lab where both are stated cleanly, with a domain that makes them concrete, is worth more than the mycology.

**The upside worth being excited about.** If a local approximation to flow reinforcement *does* work — and the Physarum literature suggests reinforcement heuristics are robust — then SCR gains the ability to express an entire class of self-organizing network mechanisms, which unlocks the harder half of Family H. That is a large payoff from a small Lab, and it is testable cheaply because the reference results (Tokyo rail comparison, fungal network resilience statistics) are published and quantitative.

Laboratory data is also unusually accessible: fungal networks grow on agar in weeks and are directly imaged. Few Labs have a benchtop reference experiment.

**The challenges, in order of severity.**

1. **Flow is global.** The reinforcement signal cannot be computed locally without approximation, and whether the approximation preserves the phenomenon is unknown.
2. **The World's Connections are created by the mechanism**, which no Layout family currently describes.
3. **Withdrawal makes the process non-monotone**, which removes most tractable analysis.
4. **The famous result is a different organism**, and borrowing its glamour would be dishonest.
5. **Small audience, no commercial path.**

## Non-claims

This Lab does not model any real fungal network, makes no claim about soil ecology or mycorrhizal function, and produces nothing suitable for agricultural, ecological, or network-engineering decisions (§41, §43).
