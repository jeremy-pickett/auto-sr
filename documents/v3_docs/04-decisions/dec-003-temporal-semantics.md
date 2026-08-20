# DEC-3 — Temporal semantics

**Document class:** Level 2 — Architecture Decision · **Status:** open; placement decided
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Which execution models the Reactor offers beyond synchronous lockstep — discrete-event ordering, declared observation staleness, delayed effect application, deterministic interleaving — which Worlds may declare them, and what the scheduling contract and budgets are.

## Why it is consequential

Adversarial and operational phenomena live in temporal margins: races, stale-observation exploits, timing side effects. A strictly lockstep core excludes the Labs that need them (§45.13). But the obvious remedy — letting a Plugin manipulate its own temporal state — hands the clock to the one component §6 exists to contain.

## What is already constrained

**The placement is already foundational law and is not reopened here** (§6, §18.5): asynchrony, observation staleness, delayed effect, and interleaved application are declared capabilities of the World and Reactor. A Plugin may *propose* a future-offset effect exactly as it proposes any other state change; the Reactor owns the clock, the queue, quantization, ordering, and budgets. Scheduling proposals are writes, and writes are budgeted. Determinism and exact replay are non-negotiable under every model the Reactor offers.

What remains open is the mechanics: which models, which Worlds, what contract, what budgets.

## What this record constrains

- `../01-core/reactor.md`
- `../01-core/plugins.md`
- `../01-core/worlds.md`
- `../02-platform/execution-safety.md`
- Lab papers answering §30.4

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
