# 49. Prompt Injection Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #49, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

A language model reads text and acts on it. When some of that text comes from a source the system's designers do not control — a web page it fetched, a document a user uploaded, an email in an inbox it has access to, the output of another agent — instructions embedded in that content can be followed as though they came from the operator.

The structural cause is that models process instructions and data in the same channel. There is no separator that reliably means "everything after this is data, not orders." Defences are mitigations rather than fixes: system prompts asserting priority, input filtering, output constraints, privilege separation around what tools the model may call.

The property that makes it a spread phenomenon rather than a single-request bug is **propagation**. An agent that reads poisoned content may write a summary, file a ticket, update a document, or send a message — and that output becomes input for the next agent or the next session. Contamination moves along a graph of what reads what.

## What the domain already knows

**The problem is named and characterized; it is not solved.** Direct prompt injection (the user attacks the model they are talking to) and indirect prompt injection (attacker-controlled content reaches the model through a retrieval or tool path) are distinguished, and the indirect case is the security-relevant one. The framing dates to around 2022–2023 and is now standard in AI security guidance.

**The consensus is that it is not fixable at the model layer alone.** The recommended architecture is to assume injection succeeds and constrain the blast radius: least-privilege tool access, human confirmation for consequential actions, separating the component that reads untrusted content from the component that holds authority.

**Benchmarks exist and are young.** There are public evaluation suites for injection susceptibility and for agent security. They measure per-request susceptibility of a given model to a given attack, which is a different question from propagation through a system.

**There is no mechanism literature to speak of.** Nothing here plays the role that Nagel–Schreckenberg plays for traffic. The domain is two or three years old, moves fast, and its published work is mostly attack demonstrations and mitigation proposals rather than models of system-level behaviour.

## Where the shortcut holds, and where it breaks

**Reducible.** Almost nothing, but for an unusual reason: not because the questions are hard, but because **the domain lacks the stable quantitative structure that reduction requires.** There is no rate constant. There is no measured susceptibility that stays valid for six months. There is no equivalent of a fundamental diagram.

What *is* reducible: the static data-flow question. Given a system architecture, which components can receive attacker-influenced content and which tools can they reach — that is a reachability computation over a known graph, and it is exactly the analysis the recommended mitigations are based on. Like #48, the static closure question is tractable and the tooling for it is essentially architecture review.

**Irreducible.** The dynamics, if they are real:

- **Multi-hop propagation.** Content flows through summarization, storage, and retrieval. Whether an injected instruction survives being summarized, re-embedded, retrieved days later, and read by a different agent is a path-dependent question — and each hop is lossy and stochastic.
- **Persistence and re-emergence.** Poisoned content written to a shared store can be retrieved long after the original interaction, by a different agent, in a different context. This is the same structure as #2 and #50: a quiet system with live state.
- **Trust topology nobody drew.** The graph of what reads what in an agent system is emergent from configuration, not designed. Retrieval indexes, shared memory, ticket systems, and inter-agent messages create paths the architects did not enumerate.
- **Amplification versus decay.** Whether contamination dies out or spreads depends on per-hop survival probability against branching factor — a branching-process structure with a threshold.

**The lens, stated plainly — and this is the Lab's fundamental problem.** Every other Lab in this catalog models a substrate that holds still. Fire chemistry does not change. Kirchhoff's laws do not change. BGP's decision process changes on a timescale of years.

**Here the substrate is a language model, and it changes every few months.** Susceptibility to a given injection technique is a property of a specific model version, and it is deliberately being reduced by the model's developers. A mechanism calibrated against today's behaviour describes a system that will not exist next year.

That is not a difficulty to be managed. It is a challenge to the platform's core commitment: SCR-F §7 makes Runs immutable evidence about a system, and evidence about a non-stationary substrate has a short half-life. A Lab here would be accumulating a corpus of findings about systems that are being actively rebuilt.

## What a Cell would carry

A component that reads and writes content — an agent, a document, an index entry, a memory record: contamination state, trust level, what tools or authority it holds, and content provenance. Bounded scalars; §13.1 met at this level of abstraction.

But the abstraction is doing a great deal of work. **"Contaminated" is a binary standing in for a text payload that may be transformed at every hop**, and whether an injection survives summarization is a property of the text and the model, not of a flag. The Lab's central modelling question is whether a scalar contamination state preserves anything real, and I do not think that has an obvious answer.

**Layout is a Network or Agent World** — Connections are read/write relationships between components — and the catalog is right that this is not a grid.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak on rigour, high on timeliness, and I would grade it weak while acknowledging that is an uncomfortable verdict for the most commercially fashionable entry in the catalog.**

The reasons are structural rather than fixable:

- **The substrate is non-stationary.** This is disqualifying for a platform built on permanent evidence, and no amount of care fixes it.
- **The per-hop mechanism is a text transformation**, and abstracting it to a scalar discards the thing that determines whether propagation happens.
- **There is no reference data.** No documented multi-hop propagation incidents with enough detail to check a model against, no measured per-hop survival rates, no established topology.
- **The static analysis already gives the actionable answer.** "Untrusted content reaches a component with tool authority" is the finding, and it is obtainable by architecture review.

**The upside worth being excited about — and it is real, if narrower than the excitement around this topic suggests.** The **branching-process threshold** question is genuine and topology-driven rather than model-driven: given a per-hop survival probability *p* and a graph of what reads what, does contamination die out or persist? That question has the same shape as epidemic thresholds on networks, is answerable in the abstract, and does not depend on which model version is deployed. Framed that way — **as a study of contamination dynamics on agent trust topologies, parameterized by a survival probability nobody has to measure** — the Lab becomes stationary again, because the topology is the subject and the model is a parameter.

That framing is defensible, useful, and considerably less exciting than what people would want this Lab to be. It also connects cleanly to #50, #51, and #54, all of which are contamination-on-a-graph problems.

**The challenges, in order of severity.**

1. **Non-stationary substrate.** Findings decay in months; the platform's evidence model assumes they do not.
2. **The mechanism is text transformation**, poorly represented by a state flag.
3. **No reference data** for multi-hop propagation.
4. **Dual-use character is direct.** This Lab studies how attacks propagate through systems people are deploying now. F-20 applies, and so does ordinary caution about what gets published.
5. **Maximum over-claiming pressure.** This is the most fashionable topic in the catalog and the one where a plausible demo would attract the most unwarranted belief (§30.7).

## Non-claims

This Lab does not assess the security of any real AI system, does not evaluate any model's susceptibility to attack, does not produce attacks, and produces nothing suitable for security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
