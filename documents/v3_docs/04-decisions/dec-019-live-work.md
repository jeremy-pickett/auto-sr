# DEC-19 — Live work

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

If future Labs need live streams, how provisional live observations are separated from finalized immutable Runs.

## Why it is consequential

§19 is explicit that future products may need live operational views and that those must not erase the distinction between a live execution stream and a finalized Run. The failure mode is quiet: a provisional observation that is never marked provisional becomes evidence by default.

## What this record constrains

- `../01-core/runs.md`
- `../01-core/visualization.md`
- `../02-platform/observability.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
