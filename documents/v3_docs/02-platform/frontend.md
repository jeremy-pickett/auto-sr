# Frontend

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/frontend.md`
**Cites:** SCR-F v0.2 §24, §24.1, §33, §39

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- Frontend delivery and the application shell, distinct from `../01-core/visualization.md`, which owns the evidence contract those views must satisfy.
- The playback interaction model as a first-class product surface: time is directly navigable in every visual Run experience (§24.1).
- Attribution surfaces — which Reader produced an assertion, and how a claim relates to underlying evidence (§21).
- Explicit non-inheritance of the current frontend routing system and the current limited renderer (§39).

## Decisions this document must not resolve locally

None recorded in §40 as blocking this document. If writing it surfaces a consequential choice, the choice is registered as a new DEC record — it is not answered here (F-22, §36.5).

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.
