# Transport

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/transport.md`
**Cites:** SCR-F v0.2 §24, §33, §39

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- How Run evidence reaches a viewer efficiently enough for scrubbing to feel instant.
- Streaming for long-running Generation and Study work.
- What advanced Views require of the wire format, so 3D and time-mapped Views do not force server-side re-execution.

## Decisions this document must not resolve locally

- **DEC-13 — Visualization scale.** *Open.* Its answer largely determines this document.

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.
