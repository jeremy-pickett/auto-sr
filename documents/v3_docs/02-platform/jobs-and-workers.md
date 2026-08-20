# Jobs and workers

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `02-platform/jobs-and-workers.md`
**Cites:** SCR-F v0.2 §33, §39

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- How Generation, Runs, and Studies are scheduled and executed once they no longer fit in a single synchronous request.
- Failure, retry, and partial-completion semantics that do not corrupt the failure taxonomy (§10) — an infrastructure retry is not a Run failure.
- Fan-out for Studies, which multiply Runs by design (§20.1).
- Explicit non-inheritance of 2.x's no-job-queue and single-execution-host assumptions (§39).

## Decisions this document must not resolve locally

None recorded in §40 as blocking this document. If writing it surfaces a consequential choice, the choice is registered as a new DEC record — it is not answered here (F-22, §36.5).

## Standing constraint on this directory

§33 is explicit: Platform Services support the conceptual platform and **must not define its scientific assumptions accidentally**. The 2.x choices — SQLite, synchronous generation over a streamed HTTP request, local execution, a React frontend — are evidence about what worked at toy scale, not constraints on 3.x (§33, §39). Every conceptual contract in SCR-F must remain meaningful after this directory's answers change.

## An unregistered concern

Nothing in SCR-F names a **cost or budget model**, and §22.1 plans a scale-up of several orders of magnitude. Model calls per Generation, repair attempts, and Study fan-out all have real cost. If writing this document requires an answer, register a DEC rather than deciding it here (§36.5, F-22).
