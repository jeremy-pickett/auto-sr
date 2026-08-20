# Identity and access

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/identity-and-access.md`
**Cites:** SCR-F v0.2 §33, §22, §31

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- Identity and authorization as platform services that never become scientific assumptions (§33).
- Attribution: who or what supplied a correction, a Study, a Plugin, or a Lab judgment (§31).
- Whether and how the Corpus partitions evidence by owner, and what that means for Search and for the claim that the Corpus is one durable body of evidence (§22).

## Decisions this document must not resolve locally

None recorded in §40 as blocking this document. If writing it surfaces a consequential choice, the choice is registered as a new DEC record — it is not answered here (F-22, §36.5).

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.

## An unregistered concern

SCR-F describes the Corpus as one durable body of evidence without a notion of *whose* evidence it is. That is comfortable for a single-user platform and uncomfortable the moment a Lab models a real organization's data. No DEC currently covers it; if writing this document requires an answer, register one (§36.5, F-22).
