# Plugin

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/plugins.md`
**Identifier namespace:** `PLUGIN-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §2, §6, §17, §18.5, §20.1; F-2, F-9 · DEC-1, DEC-3, DEC-7, DEC-18, DEC-21
**Supersedes:** the first-pass seam document, preserved at `plugins.seams.md`.
**Part of the core contract set:** `cells.md`, `worlds.md`, `reactor.md`, `runs.md`.

> A **Plugin** is one local mechanism, written so a person can read it. Given what it is permitted to see, it decides what changes to propose. That is the whole of what it does.

---

## 1. What the Plugin owns

**PLUGIN-1.** A Plugin proposes changes to state it declared it may write, computed from state it declared it may read, reached through paths the World declared it may use.

**PLUGIN-2.** A Plugin **declares** before it runs: which properties it reads; which it writes; which connections it traverses and how far; which helpers it uses; which values it needs the Reactor to supply; and, where the World offers them, which scheduled effects it may propose.

Declarations are not decisions. They are promises, checked at admission and enforced throughout (`reactor.md` §2).

**PLUGIN-3.** A Plugin has a **readable representation**: one a competent person can read, compare across versions, copy, change, review, and hand to another person or another machine — without the platform's help, and without trusting the platform's account of what it does.

That is a requirement about a property, not about a notation. This document may name the notation it selects; the requirement it satisfies may not be stated in terms of one. The reasoning is in `../00-start-here/what-is-scr.md`; the amendment that corrected it is recorded in `../00-start-here/glossary.md` and on DEC-7.

---

## 2. What the Plugin refuses

| Refused | Owner |
|---|---|
| Randomness of its own | Reactor |
| The order in which anything is applied | Reactor |
| The clock, and what "later" means | Reactor |
| How fresh its observations are | World declares, Reactor supplies |
| Reaching a Cell it was not given a path to | World, through the Layout |
| When the Run stops | Reactor |
| The record of what happened | Run |
| State the experiment does not know about | nobody — it may not exist |

**PLUGIN-4.** A Plugin may hold no state that is not declared. Undeclared state is invisible to the Reactor's determination of what matters for the future, which means the Reactor's stopping decision is blind to it, which means a Run can be declared finished while something is still changing (`reactor.md` §4).

### 2.1 Trust follows role, not authorship

A Plugin is **variable experiment code**. Platform code — World, Reactor, Run, storage, interfaces — is the **trusted base**. The contract exists because of that division and for no other reason.

**PLUGIN-5.** Every Plugin satisfies the same contract regardless of who or what wrote it. A machine may write one. A person may edit one. A Lab may ship one. One machine may repair another's work. None of that changes what it is permitted to do.

This corrects a real error in the first pass, which grounded the contract in the fact that Plugins are machine-written. That reasoning does not survive contact with a hand edit: a person's changes are not more trustworthy, they are merely differently sourced, and a contract that relaxes for human authorship has a hole shaped exactly like the most confident contributor in the room.

**PLUGIN-6.** A direct edit produces a **new Plugin revision**. It inherits no admission, no prior agreement, and no privilege. It is matched and admitted like any other.

**PLUGIN-7.** After a direct edit, the recorded intent is **stale until confirmed**. The platform marks it so, and preserves both the previous stated intent and the new unconfirmed implementation. It does not overwrite the first with a fresh description and present the result as though nothing happened. (DEC-18 owns what happens next: confirmation, regeneration, or something else.)

---

## 3. Reach: what a mechanism may touch

The word *local* is the platform's identity, and it stops meaning anything once the arrangement leaves a lattice. On a grid, "local" can be a distance. In a World of trust relationships, distance is not defined, and a rule stated in distances is either meaningless or silently reimposing a grid.

The right formulation is not about distance at all:

> **PLUGIN-8.** A Plugin may observe or affect a Cell only by traversing connections the World declared and the Run Contract admitted. It may not name, address, read, or affect a Cell by any other means.

The failure this prevents is not a long jump. It is:

> *This mechanism may inspect or modify Cell N because it knows N exists.*

That is where the local-mechanism premise collapses, and it collapses whether N is adjacent or on the other side of the World. A mechanism that can name any Cell is not local at any distance.

### 3.1 Why this shape, and where it comes from

This is authority-by-possession, and it has a well-developed ancestry. Dennis and Van Horn described computations whose reach is defined by a list of capabilities — each one both naming an object and stating what may be done with it — so that a computation's authority is exactly what it was handed and nothing else.[^dvh] The failure mode of the alternative was named by Hardy: a component with broad authority, acting on a request it does not fully understand, uses permissions it holds for a purpose it was not given them for.[^hardy] Authority that travels with identity rather than with purpose is precisely the shape of a mechanism that may touch anything it can name.

Applied here: a mechanism does not hold permissions over the World. It holds paths, and each path says what may be done along it.

**PLUGIN-9.** A long-range effect — an ember thrown ahead of a fire front, a grain of sand landing past its neighbours, a seed carried away from its parent, a process that scans rather than spreads — is expressed as a **declared transport connection** provided by the World, not as unrestricted addressing by the mechanism. The World decides that such transport exists and what it may reach. The mechanism decides only whether to use it.

This keeps four intended Labs expressible while leaving the line intact, because the World still declares what is reachable and the Reactor still enforces it.

**Status.** DEC-21 owns this. PLUGIN-8 and PLUGIN-9 state the leading formulation so the decision can be made against something concrete.

---

## 4. Scheduled effects

**PLUGIN-10.** Where the World declares a capability for it, a Plugin may propose an effect to take place at a stated offset. It does so exactly as it proposes anything else.

**PLUGIN-11.** The Reactor decides what the offset means, quantizes it to its own clock, orders it, admits or refuses it under the same contract as any other proposal, and counts it against the mechanism's budget. Scheduling is a write. Writes are budgeted.

There is no recursion problem here, because there is no mechanism-owned clock for recursion to live in.

---

## 5. Which Worlds a mechanism can act on

Two different questions have been travelling under one name, and answering them together produces a label that is wrong twice.

> **PLUGIN-12. Mechanical compatibility** — does this World supply what this Plugin declared it needs? Required properties exist, kinds and ranges are compatible, required connection classes exist, requested reach is permitted, required capabilities are available.
>
> This is **derived from declarations** wherever possible and decided by the Reactor at admission. It is not a label anyone writes by hand.

> **PLUGIN-13. Domain fitness** — does running this mechanism in this World make any sense?
>
> This belongs to the Lab, the Study, or a person. The platform does not decide it and must not imply that it has.

A mechanism can be mechanically compatible with two Worlds whose properties happen to share a shape while being scientifically absurd in one of them. A single `works with` marker collapses the two and reports the absurd case as fine.

---

## 6. What the Plugin requires

- **From the World:** its Cell schemas, what may be read, which paths exist and where they lead, what it is permitted to see (Seen State, `worlds.md` §6).
- **From the Reactor:** every helper it uses, all randomness, every derived value it declared a need for, and a decision on each proposal.
- **From the Run Contract:** the frozen record of what it was permitted to do, so a later reader never has to infer old permissions from current platform behaviour.

---

## 7. What the Plugin produces

**Proposals** — nothing else. Not state, not history, not conclusions. A proposal is a request; whether it becomes a change is the Reactor's to decide.

And, permanently: its **readable representation**, its **declarations**, and its **stated intent** — all three carried in the record, all three able to disagree with each other, and none of them permitted to overwrite another.

---

## 8. Why the contract is this tight

It would be easy to read §2 as excessive caution about generated code. The better reason is that mechanism size is no guide to mechanism consequence. Rule 110 decides each cell from itself and its two neighbours, holds two states, and is capable of universal computation.[^cook] A mechanism small enough to read in one screen can produce behaviour that no analysis short of running it will predict.

A contract that relies on a mechanism being simple enough to be harmless has no basis. The contract has to hold regardless of how small the mechanism looks.

---

## 9. Open decisions

- **DEC-7 — Plugin contract surface.** This document is what that record governs. Recently amended to cover capabilities rather than notation.
- **DEC-21 — Locality and reach.** §3 states the leading formulation.
- **DEC-1 — Mechanism composition.** If several mechanisms act in one Run, this contract gains a dimension it does not have: whether they read the same prior state or each other's results, whether proposals are simultaneous or ordered, and how conflicts resolve. Every one of those is experimental semantics, and none of them belongs to a Plugin. Whatever the Reactor does there is a mechanism nobody declared — see `reactor.md` §7.
- **DEC-3 — Temporal semantics.** PLUGIN-10 and PLUGIN-11 are settled as placement; the mechanics are open.
- **DEC-18 — Direct edits.** PLUGIN-6 and PLUGIN-7 settle the parts that follow from PLUGIN-5. What happens to stale intent is still open.

---

## Amendment record

**2026-08-20 — first-pass seam document replaced by this requirements document.** The seam pass is preserved unchanged at `plugins.seams.md`.

Changed as a result of external critique (`../critiques/SCR_Core_Starter_Docs_Critique_v0.1.md`):

- *Trust grounded in role, not authorship* (§2.1). The seams pass argued the Plugin cannot be trusted because it is the only machine-written component. The critique correctly identified that as the wrong reason, since a hand edit does not confer trust. PLUGIN-5 to PLUGIN-7 are new, and they dissolve most of DEC-18.
- *Reach reformulated from distance to permitted paths* (§3). The seams pass described a spectrum from neighbours to a jump to everything. The critique identified the real endpoint — a mechanism touching any Cell it can name — which is a question about authority, not distance, and which works in relational Worlds where distance does not exist. PLUGIN-8 and PLUGIN-9 are new, with the capability-security ancestry cited.
- *Mechanical compatibility separated from domain fitness* (§5). New, from the critique. PLUGIN-12 and PLUGIN-13.
- *Rule 110 argument added* (§8) to justify the contract's tightness on grounds that survive the trust correction.

Unchanged: the narrow scope in §1, the refusal table, scheduled effects as ordinary proposals, and the readability requirement stated as a property.

---

## Sources

[^dvh]: Jack B. Dennis and Earl C. Van Horn, "Programming semantics for multiprogrammed computations," *Communications of the ACM* 9, no. 3 (1966): 143–155.
[^hardy]: Norm Hardy, "The Confused Deputy: (or why capabilities might have been invented)," *ACM SIGOPS Operating Systems Review* 22, no. 4 (October 1988): 36–38.
[^cook]: Matthew Cook, "Universality in Elementary Cellular Automata," *Complex Systems* 15, no. 1 (2004): 1–40. The conjecture is Wolfram's, from 1985.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
