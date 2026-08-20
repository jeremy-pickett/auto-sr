# Reactor

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/reactor.md`
**Cites:** SCR-F v0.2 §6, §18, §18.1–§18.5, §38.2; F-9, F-20

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- Everything §18 lists as Reactor-owned, as a testable contract: state application, ordering, controlled randomness, timing, observation delay, visibility, shared-resource effects, required derived state, limits, stopping, replay, evidence capture, and version identity for execution semantics.
- The three boundaries — the Reactor is not the Lab, not Generation, not a Reader (§18.1–§18.3) — expressed as things the Reactor is forbidden to know or decide.
- Execution-semantics versioning, and the rule inherited from 2.x that identical source under a different execution revision is a different experiment.
- The temporal capabilities the Reactor offers beyond lockstep, if any, under the non-negotiable constraint that determinism and exact replay hold for every model offered (§18.5).
- The security posture: hostile conditions are declared experimental capabilities, and an adversarial Lab never justifies a permissive execution surface (§18.4, F-20).

## Decisions this document must not resolve locally

- **DEC-2 — Replay equivalence.** *Open.* Bit-exact versus contractually equivalent replay changes this document's storage and versioning obligations outright.
- **DEC-3 — Temporal semantics.** *Open; placement decided.*
- **DEC-16 — Security isolation.** *Open.* Owned jointly with `../02-platform/execution-safety.md`.
