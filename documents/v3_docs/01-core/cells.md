# Cell

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/cells.md`
**Identifier namespace:** `CELL-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §13, §13.1, §14, §30.2, §45.2; F-7 · DEC-22
**Supersedes:** the first-pass seam document, preserved at `cells.seams.md`.
**Part of the core contract set:** `worlds.md`, `plugins.md`, `reactor.md`, `runs.md`. The five describe one contract from five sides.

> A **Cell** is the smallest thing in an experiment that holds state and can be affected by its neighbours. It is the platform's unit of *being acted upon*. It never acts.

---

## 1. What the Cell owns

**CELL-1.** A Cell holds state, and nothing else. It has no behaviour, no schedule, no memory of its own beyond declared properties, and no ability to initiate anything.

This is the most useful fact about the component and the easiest to lose. Every other member of the core set decides something. The Cell is the one place in the platform where the answer is *nothing* — which is why the constraint it carries is the whole of its contract.

**CELL-2.** Every property a Cell holds is declared in advance, by the World, before any mechanism runs. There is no undeclared state, no property that appears during execution, and no place for a mechanism to keep something the experiment does not know about.

### 1.1 Why the constraint is scientific rather than tidy

The platform's claim is that behaviour nobody wrote can come out of small local rules repeated over time. That claim is checkable only if the behaviour could not have been carried in the state to begin with.

The founding work already respected this. Von Neumann's self-reproducing machine used a lattice of cells with **twenty-nine states** — finite, enumerated, fixed in advance — and built universal construction out of them by repetition rather than by capacity.[^vn] Wolfram's survey of one-dimensional rules found four broad behaviour classes emerging from cells holding a couple of states apiece.[^wolfram84] In both cases the interest is entirely in what the repetition produced, and that reading is only available because the state could not have hidden the answer.

Remove the bound and the claim quietly becomes unfalsifiable. A Cell able to hold an arbitrary structure, an embedded program, or unbounded history can carry a precomputed result and replay it, and no observer can tell that from emergence.

> **CELL-3.** A Cell's state must be incapable of storing a computation. This is a requirement about what the platform permits, not advice to mechanism authors.

---

## 2. What the Cell refuses

| Refused | Owner |
|---|---|
| Behaviour of any kind | Plugin |
| Where it sits, and who can reach it | World |
| When anything happens to it | Reactor |
| What its properties mean | Lab |
| What its values measure | Reader |
| Whether any of that matters | Study, and a person |

**CELL-4.** A Cell may not hold a reference to another Cell as state. Relationships between Cells are declared by the World as connections, and are visible to a mechanism only through the paths the World permits (`plugins.md`, §3). A property containing another Cell's address is a private connection the World never declared and the Reactor cannot police.

---

## 3. What the Cell requires

- **From the World:** its schema — which properties exist, of what kind, within what range.
- **From the Reactor:** enforcement of the schema at admission and during execution. A declared ceiling that nothing checks is a comment.
- **From the Run Contract:** permanent record of the schema that was actually in force (`runs.md`, §2), so a reader years later knows what the state could have held rather than inferring it from whatever the platform does today.

---

## 4. What the Cell produces

A **declared schema** — the set of properties, their kinds, and their ranges — and the **values** held against it at every recorded step.

Both are evidence. Neither is a measurement.

---

## 5. Two ceilings, for two different reasons

SCR-F §13.1 establishes a single "computational ceiling" and assigns its numbers here. Writing it revealed that one ceiling is doing two unrelated jobs, which fail differently and should be separated.

### 5.1 The semantic ceiling — a restriction on kind, not a number

The semantic ceiling exists to protect the emergence claim in §1.1. It is therefore **not a count**, which is why looking for its number was the wrong question:

> **CELL-5.** A Cell property is one of: a number, a whole number drawn from a declared finite set, or a true/false value. Nothing else.

No collections, no nested structures, no text of unbounded length, no references, no callable things. This holds identically in every World, every Lab, and every Layout family, and it is not tunable. A Lab whose participants cannot be described this way fails its fit review (SCR-F §30.2) — and that failure is useful information about where the platform stops working, not an obstacle to route around.

Stating it as a restriction on kind rather than a count is what makes it enforceable at admission and stable across World families of wildly different sizes.

### 5.2 The execution budget — counts, and they vary

Everything numeric is a resource limit, and resource limits exist for a completely different reason: to stop a legitimate experiment from consuming more than it has been given.

**CELL-6.** The execution budget bounds at least: properties per Cell schema, bytes per Cell, Cells per World, connections per World, and total state per Run.

**CELL-7.** Budget limits are set per World family and per deployment. They are recorded in the Run Contract, not fixed platform-wide.

**CELL-8.** The two ceilings fail differently, and must be distinguishable in the record. A semantic-ceiling violation is a **contract failure** — the mechanism or World asked for something the platform does not offer, and no budget increase would ever make it admissible. A budget violation is a **resource failure** — the experiment was legitimate and this deployment could not run it. Reporting the second as the first would tell a researcher their idea was invalid when the true answer was that the machine was too small.

---

## 6. One kind of Cell, or several

**This is an open decision (DEC-22) and this document does not resolve it.** It is recorded here because it determines what a schema can express, and because writing this document is what surfaced it.

A grid of terrain patches is honestly one kind of thing. Every Cell is a patch; every patch has fuel and moisture and slope. The moment the arrangement stops being a lattice, that stops being true. In a World built on relationships, an account, a group, a role, and a resource are four different kinds of participant carrying four different sets of meaningful properties, and there is no honest schema that covers all four.

**If a World declares exactly one kind of Cell:** the schema is trivial to enforce, storage is uniform, and measurement is straightforward. Three of the four named Layout families get a superset schema in which most properties are meaningless for most Cells, which is a way of saying they are supported in name.

**If a World may declare several kinds:** relational Worlds become honestly expressible. Matching, storage, measurement, and display all get harder, and a real hazard appears — several schemas can drift into an arbitrary object graph, at which point CELL-5 is the only thing left holding the line.

The reviewed critique leans toward several bounded schemas with connections declaring which kinds they may join. That lean is recorded, not adopted. See DEC-22.

---

## 7. Identity

**CELL-9.** Every Cell has an identity that is stable for the whole of a Run and meaningful in the Run Contract.

**CELL-10.** A Cell's identity is not an address a mechanism may use. Knowing that a Cell exists confers no ability to read or affect it; that comes only from paths the World declared. This is stated fully, with its reasoning and its formal ancestry, in `plugins.md` §3.

---

## 8. Open decisions

- **DEC-22 — Cell schema multiplicity.** Whether a World may declare more than one kind of Cell. §6 above.
- **DEC-24 — The cellular budget.** Multi-schema Cells is one of several proposed relaxations that individually make sense and collectively change what "cellular" means. This document supplies one entry to that ledger.
- **DEC-1 — Mechanism composition.** Touches this document only if several mechanisms share Cell state, in which case the record may need to say which one wrote what.

---

## Amendment record

**2026-08-20 — first-pass seam document replaced by this requirements document.** The seam pass is preserved unchanged at `cells.seams.md`; it is the record of what was found and how, and it is not superseded as evidence.

Changed as a result of external critique (`../critiques/SCR_Core_Starter_Docs_Critique_v0.1.md`):

- *The single ceiling is split into two* (§5). The critique observed that a semantic ceiling and an execution budget exist for different reasons and should fail differently. Acting on that produced a further correction of the seams document's own framing: the semantic ceiling is a restriction on **kind**, not a count, which is why the seams pass could not find its number. CELL-5 through CELL-8 are new.
- *Ownership table wording tightened.* The seams pass assigned "what the state is worth" to Reader. A Reader measures; significance belongs to a Study or a person. Corrected in §2.
- *Multi-schema Cells registered* as DEC-22 rather than left as an unregistered gap.

Unchanged: the "a Cell decides nothing" framing, the emergence argument, and the refusal table's substance.

---

## Sources

[^vn]: John von Neumann, *Theory of Self-Reproducing Automata*, edited and completed by Arthur W. Burks (University of Illinois Press, 1966). The cellular framework was suggested to von Neumann by Stanisław Ulam.
[^wolfram84]: Stephen Wolfram, "Universality and complexity in cellular automata," *Physica D: Nonlinear Phenomena* 10, no. 1–2 (1984): 1–35.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
