# Execution safety

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/execution-safety.md`
**Cites:** SCR-F v0.2 §18.4, §33; F-20

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The execution boundary for generated code, treated as an explicit contract and execution-safety problem (§18.4).
- Resource control: memory, wall-clock, and per-participant budgets, including budgets for scheduled proposals where temporal capabilities are offered (§18.5).
- The rule that an adversarial research subject never justifies a permissive execution surface — hostile conditions are declared World and Reactor capabilities instead (§6, F-20).
- Explicit non-inheritance of the hardened-single-host 2.x assumption (§39).

## Decisions this document must not resolve locally

- **DEC-16 — Security isolation.** *Open.* What production execution boundary replaces the single-user 2.x host assumption. Owned jointly with `../01-core/reactor.md`.

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.
