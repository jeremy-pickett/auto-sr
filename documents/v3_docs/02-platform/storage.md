# Storage

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/storage.md`
**Cites:** SCR-F v0.2 §22, §32.1, §33, §39

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The durable store for the Corpus, and the separate store — if separate — for operational telemetry (§22).
- Run and tick representation, retention, and reconstruction cost, under whatever DEC-2 decides about replay.
- Content addressing and hash chains over immutable histories as a storage-layer obligation (§32.1, F-21).
- Explicit non-inheritance of SQLite as the long-term store (§39), while preserving what the 2.x storage model actually proved.

## Decisions this document must not resolve locally

- **DEC-2 — Replay equivalence.** *Open.* This record sets this document's storage obligations.
- **DEC-6 — 2.x corpus migration.** *Partially decided.*
- **DEC-8 — World storage.** *Open.* A common representation for spatial and relational Worlds without forcing one into the other's shape.

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.
