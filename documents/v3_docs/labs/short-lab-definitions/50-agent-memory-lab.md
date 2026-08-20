# 50. Agent Memory Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #50, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §38.6, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

Agents that persist across sessions keep notes. They write summaries of what happened, store facts they learned, and retrieve them later to avoid rediscovering everything. When several agents share a store — a common vector index, a knowledge base, a project workspace — one agent's notes become another agent's context.

Two failure modes follow, and they are different from each other.

**Contamination**: something false or hostile enters the store — from a poisoned source, from a mistaken inference, from an attacker — and is subsequently retrieved as established fact. It may be re-summarized and re-stored, launderd of its provenance in the process, so the false claim acquires the appearance of having been independently confirmed.

**Drift**: nothing hostile happens at all. Repeated summarization of summaries compounds small distortions. Facts lose their qualifiers. Uncertain claims become certain ones. The store slowly diverges from what actually happened, and no single step was wrong.

Both share a property: **the store outlives the interaction.** An agent that behaves perfectly today may be acting on a corruption introduced months ago by a process nobody remembers.

## What the domain already knows

**Very little, formally.** This is the least established domain in the catalog. Persistent agent memory is an engineering practice a few years old, its architectures are unsettled, and there is no body of measured phenomena.

**Adjacent literatures are relevant and worth knowing.**

Retrieval-augmented generation has an established failure literature — retrieval of irrelevant or contradictory context degrading output — and data poisoning of retrieval corpora has been demonstrated in research settings.

**Model collapse** is the closest thing to a theoretical result: training successively on model-generated output degrades a model's distribution, losing the tails first. The papers on this from around 2023–2024 concern training rather than retrieval, but the structure — recursive self-consumption compounding distortion — is exactly the drift mechanism above *(attribution from memory, verify)*.

**Provenance and lineage tracking** is a mature field in databases and scientific computing, and it is the standard answer to "where did this claim come from." Notably, SCR's own foundations take a strong position on exactly this problem (SCR-F §32) — which makes this Lab unusually reflexive.

## Where the shortcut holds, and where it breaks

**Reducible.** If provenance is tracked, the contamination question is a lineage query: which stored items derive from a compromised source. That is a graph traversal and it is solved technology. The static architectural question — which agents can write to stores that which other agents read — is a reachability computation, as in #48 and #49.

**Irreducible.** What lineage tracking does not cover:

- **Drift without a source.** No item is contaminated; the distortion is distributed across many summarization steps. There is nothing to trace back to, because the error was introduced by the *process* rather than by an item. Provenance answers "where did this come from" and is silent on "how much was lost on the way."
- **Compounding through re-summarization.** Each pass is individually reasonable. The composition is not. Whether the store converges to a stable (if lossy) representation or diverges depends on the retrieval and summarization dynamics — a fixpoint question with no obvious answer.
- **Selective reinforcement.** Retrieval is not uniform: frequently-retrieved items get re-summarized and re-stored more often, so the store's evolution is biased toward what has already been retrieved. That is a positive feedback loop and it is the mechanism by which a plausible falsehood becomes the store's most confident claim.
- **Laundering of confidence.** A hedged claim summarized becomes an unhedged one; unhedged claims are retrieved more readily. Uncertainty is systematically stripped, and the loss is not recoverable from the store itself.

**The lens, stated plainly.** This is a **hidden-state Lab**, and the catalog says so: it is the pattern-versus-computational-state distinction (SCR-F §38.6) applied to information systems. The agents look fine. Their outputs are fluent. The store beneath them is drifting, and nothing in the visible behaviour reveals it.

The irreducible content is specifically the **recursive self-consumption**: a store whose contents are produced by processes that read the store. That structure has no closed form and it is the same structure as model collapse, gene surfing at an expanding front (#25), and reinforcement in mycelial networks (#18) — positive feedback selecting on its own output.

## What a Cell would carry

A memory item or an agent: for an item, contamination or distortion level, confidence, retrieval count, derivation depth, and age; for an agent, what it has recently read and what it is about to write. Bounded scalars; §13.1 met at this abstraction.

The abstraction problem is the same as #49's and slightly milder: **"distortion level" is a scalar standing in for semantic drift in text.** That is a stronger simplification than "contaminated / not," because drift is continuous and directional, and a single number may genuinely capture the accumulation even if it captures nothing about the content. Whether it does is the Lab's central mechanism-fit question.

**Layout is an Agent World or a Network World** — Connections are read and write relationships between agents and stores. The catalog is right that this is not a grid.

The distinctive feature: **items are created and destroyed by the mechanism.** The World's population changes as agents write. That is the changing-participant-count problem from #20's growing domains and #18's self-constructed topology, appearing again.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible, with the same non-stationarity problem as #49 but noticeably less of it — and one genuinely distinctive attraction.**

The case against is largely #49's: young domain, unsettled architectures, no measured phenomena, no reference incidents, and a semantic mechanism abstracted into a scalar.

The case for is that **the drift mechanism is more stationary than the injection mechanism.** Whether a summarization pipeline loses information at each pass is a property of the pipeline's structure, not of which model version runs it. Every model summarizes lossily; the interesting question — does repeated retrieval-and-resummarization converge or diverge, and how does that depend on retrieval bias and derivation depth — is about the *architecture*, and architectures change on a slower clock than model behaviour.

That is a meaningfully better position than #49 occupies.

**The upside worth being excited about.** Two things.

The **retrieval-reinforcement feedback loop** is a real, specific, under-examined mechanism with a clear question attached: does a shared store under retrieval-biased re-summarization reach a stable state, or does it concentrate on a shrinking set of increasingly confident claims? That is answerable in the abstract, it does not require knowing anything about a particular model, and the answer would inform how these systems should be built — which is a decision people are making right now with no evidence.

And there is a **reflexive value** worth naming: SCR itself is a system with a corpus, machine-written documents, and a stated worry (SCR-F §36) about a mostly model-written document tree drifting at the root. This Lab studies the mechanism of that worry. A platform that models its own failure mode, honestly, is a stronger platform — and the finding would apply to SCR's own document tree as much as to anyone's agent system.

**The challenges, in order of severity.**

1. **No reference data.** Nothing to check against; the phenomenon has not been measured.
2. **Semantic drift as a scalar** is a large simplification and may discard the mechanism.
3. **Architectures are unsettled**, so the World has no stable shape to model.
4. **The World's population changes** as items are written — unresolved in the platform.
5. **Over-claiming pressure** is high, as throughout Family H, and this topic attracts speculation easily (§30.7).

## Non-claims

This Lab does not assess any real agent system, does not measure memory corruption or drift in any deployed product, and produces nothing suitable for engineering or security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
