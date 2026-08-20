# Irreducibility, and what "cellular" means

**Document class:** Level 1 — Foundations · **Status:** draft
**Path:** `00-start-here/irreducibility-and-what-cellular-means.md`
**Cites:** SCR-F v0.2 §6, §13, §13.1, §15, §18.5, §25.3, §30, §36.4, §36.5, §36.6, §40, §41–43, §45.12; F-7, F-9, F-17
**Derived from:** the reducibility framework in `../SCR_Labs_01-10_Knowledge_Report_v1.md` Part I, extracted here because it is platform-level rather than Lab-level.

> **Draft — not adopted.** Per §36.3 a draft may not be relied upon by downstream documents. Per §36.4.1 an *adopted* Level 1 document outranks everything for conceptual meaning; this one is not there yet, and it should be read as a proposal for the tree's missing intellectual spine rather than as settled law.

---

## Why this document exists

The documentation tree explains what the components are. It does not explain **why local mechanisms are the right instrument at all** — or, more importantly, when they are not.

That gap has a cost. Without an answer, every Lab argues its own case from scratch, "complex" gets used as though it were a justification, and the platform has no principled way to say that some domains fit better than others. SCR-F §45.12 asks reviewers to hunt over-generalization; this document is the checklist that hunt needs.

Ten Lab briefs arrived at the same framing independently. That recurrence is the evidence that it belongs at the root rather than in ten places.

---

## 1. The load-bearing reframe

> **Computational irreducibility is not a property of a domain. It is a property of a regime.**

Every domain has a part with a closed form, a regime diagram, a calibrated empirical curve, a fast exact solver, or a known universality class — and a part where the only way to know the answer is to run it.

The consequence is blunt and should be stated as such:

> **If a shortcut exists, SCR is worthless there.**

Producing a result the domain can already compute is not a contribution; it is rediscovery wearing a discovery's clothes. SCR earns its keep only where the shortcut has broken.

This is the platform's actual value proposition, and it cuts both ways: it is a reason to build some Labs and a reason to refuse others.

### 1.1 Definitions

**Reducible** does not mean simple. It means *a cheaper, established method already answers the question to the required standard.*

**Irreducible** does not mean mysterious. It means *the requested outcome depends on iterated state evolution, spatial arrangement, history, or coupling strongly enough that the shortcut no longer determines the answer.*

Both words will be attacked by external reviewers as too broad. These definitions are the answer, and they should be quoted rather than paraphrased.

### 1.2 Two ways to get this wrong

**Sensitivity is not irreducibility.** A system can be exquisitely sensitive to initial conditions and still admit useful reduced *statistical* predictions. Sensitive dependence licenses a narrow claim — *the exact realization cannot be obtained from the single-element shortcut* — and no more. Any broader claim invites a philosophical argument the platform will lose and does not need to have.

**Universality is a shortcut that survives mechanism differences.** Where a process belongs to a known universality class, its scaling exponents were fixed before any mechanism ran, and a hundred distinct mechanisms yield the same number. This is a direct challenge to the premise that different mechanisms are worth cataloguing separately, and it is a real one. A Lab in that position must aim at what universality does *not* cover, or admit it has nothing to add.

---

## 2. What makes a system "cellular"

A cellular automaton has five defining properties. Lined up against the Decision Registry:

| Property | Status in 3.x |
| :--- | :--- |
| Discrete cells | Decided — §13 |
| Bounded local state | Decided — §13.1 |
| **One uniform rule everywhere** | **In play — DEC-1.** Multiple Plugins is a non-uniform rule. |
| **Simultaneous update** | **In play — DEC-3.** |
| **Local interaction** | **In play — registered nowhere.** See §3. |

**Three of five are open, and one is not on the register.**

This table is the honest answer to the question SCR-F §45.12 asks reviewers to press:

> **When does SCR stop being ruliology and become a generic simulator?**
> **When it has spent all five.**

Nothing here argues that the three open properties must be preserved. Composition, asynchrony, and extended reach may all be worth having. The argument is that they should be spent **deliberately, one decision record at a time**, with the cost recorded — not drifted through because no document was counting.

### 2.1 The §13.1 ceiling is an irreducibility guarantee

The bounded-state ceiling reads as tidiness. It is not. Unbounded Cell state is how you smuggle the answer into the initial conditions and then report emergence you did not actually compute. A Lab whose Cell needs open-ended memory to be itself is often a Lab whose interesting behaviour was placed there by hand.

The same test applies within a bounded Cell: **does this value need to persist to determine the future, or is it cheaply derived from other state?** The more derived conveniences get stored, the easier it becomes to hide mechanism complexity in state.

---

## 3. Reach classes — what "local" means

"Local" is doing too much work. Five distinct things hide under it, and the distinction constrains the Plugin contract, every Layout family, and a large number of candidate Labs.

| Class | Meaning |
| :--- | :--- |
| **Neighbour-local** | Declared immediate neighbours only |
| **Bounded transport** | A finite hop to a non-neighbour, governed by a local rule |
| **Path-local** | Influence follows declared connections over bounded path length |
| **Connected-region constraint** | Behaviour depends on all members of one connected region |
| **Global read** | The mechanism inspects arbitrary World state |

The first four may fit SCR honestly. **The fifth is where the platform becomes a general simulator.**

Two points that are easy to miss. **Bounded transport is not a compromise** — in wind-blown sand it is what the physics does, and a model without it is wrong. And **a connected-region constraint is not a local rule**, however natural it looks: water sharing one level across a connected pond cannot be computed by any cell from its neighbours.

> The boundary between these classes is undrawn, consequential, and belongs in a decision record rather than in whichever Lab document reaches it first.

---

## 4. Driver classes — environment is not always a mechanism

A recurring error is to call every time-varying influence a second mechanism, which manufactures composition problems that do not exist and blocks Labs on DEC-1 unnecessarily. Three categories:

**Static World condition** — does not evolve during a Run. *Bedrock type, fixed slope, an initial fracture network.*

**External input** — changes during a Run, supplied from outside the simulated state, does not react to it. *A recorded wind series, a rainfall sequence, a prescribed warming trajectory.*

**Interactive mechanism** — future state depends on simulated state. *Fire altering local airflow; drainage altering future thaw; a crystal depleting the vapour it grows from.*

This matters to Studies as much as to architecture. A Study that holds a mechanism fixed while varying the forcing should not have to pretend the forcing is part of the mechanism.

> **Resolving the external-input category is separable from, and should precede, the full multi-mechanism composition question (DEC-1).** It eliminates the false composition cases and leaves the genuinely coupled ones — which are fewer, sharper, and worth deciding carefully.

---

## 5. Time is three problems

"One tick cannot mean all of this" conflates three separate difficulties:

1. **Scale span.** A process whose natural rates differ by orders of magnitude.
2. **Event duration mismatch.** A discrete event in minutes inside a model advancing over months.
3. **Different process clocks.** Coupled processes with different natural update rates.

These are **not** solved by giving each Plugin its own clock. That hands the clock to the component SCR-F §6 exists to contain, and §18.5 already places temporal capability with the World and Reactor. What is needed is a small closed set of Reactor-offered execution models — DEC-3's work.

> **No Lab invents its own temporal workaround.** A domain that cannot be represented under any offered model has produced a finding about the platform's boundary, which is useful (§30), rather than a licence to improvise.

---

## 6. Grid World must not mean Cartesian grid

Lattice geometry is not always an artifact to be minimized. Sometimes it is the physics: six-fold symmetry in ice is crystallography, and a hexagonal arrangement is therefore *more* faithful than a square one.

The requirement follows directly. The platform should support **named lattice geometries** — square, triangular, hexagonal, layered three-dimensional — or general local spatial graphs. Hard-coding square adjacency would make lattice anisotropy indistinguishable from physical anisotropy, which is fatal in any Lab whose measured output is a morphology, and quietly misleading everywhere else.

---

## 7. The helper boundary

Some honest mechanisms need a calculation no local rule can perform. The correct response is a Reactor-provided helper — and helpers are also how a whole domain model gets smuggled into a core that is supposed to know nothing about domains (§11).

> **A helper may provide a generic execution primitive. It may not provide a domain-specific answer.**

*Connected-component equalization* is plausibly generic. *A hydrology solver* is not. Borderline cases — global geometric visibility, network flow — should be decided deliberately, in the open, rather than by whichever implementation reaches them first.

A Plugin must never be handed arbitrary global World access. Where a global calculation is genuinely required it belongs to the World or Reactor as a **declared** capability, visible in provenance (F-9).

---

## 8. The claim SCR refuses to make

Wolfram's Principle of Computational Equivalence holds that most non-trivial systems are computationally equivalent in sophistication. It is a serious idea and SCR should decline to lean on it.

The reason is practical rather than philosophical. **If everything is equivalently irreducible, SCR cannot say that some domains fit better than others** — which is exactly the discrimination §30 exists to make, and exactly what makes a Lab catalog worth having.

The weaker claim is the one to hold:

> **What predicts fit is not computational class. It is whether adjacency in the model corresponds to adjacency in the world — and fit degrades in proportion to how far the true interaction topology departs from the declared Layout.**

That is falsifiable. It can be tested Lab by Lab and it can turn out to be wrong. The Principle of Computational Equivalence cannot do either, and a platform that stakes its selection rule on it has stopped being able to be corrected.

SCR should continue to credit Wolfram's work as inspiration while making no claim to reproduce or extend it (SCR-F, source basis).

---

## 9. What this document does not do

**It does not amend SCR-F.** §30 currently asks nine fit questions, none of which is *"where does this domain already have a shortcut?"* — §30.8 (comparison to established tools) is adjacent but different, because the established tool may itself be another simulation. Adding a tenth question is an SCR-F amendment under §36.5 and must be filed as a decision record with evidence attached. **This document proposes it; it does not perform it.**

**It does not resolve DEC-owned questions.** The reach boundary (§3), composition (§4), and temporal semantics (§5) are named here so that Lab papers can cite a shared framing instead of inventing nine incompatible ones. Naming a fork is not deciding it (§40, F-22).

**It does not grade any Lab.** Fit is owned by the review procedure in `../01-core/labs.md`; assessment conventions for Lab papers are in `../labs/README.md`.
