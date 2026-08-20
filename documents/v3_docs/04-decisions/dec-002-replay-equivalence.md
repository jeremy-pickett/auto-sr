# DEC-2 — Replay equivalence

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Bit-exact replay versus contractually equivalent replay: which the platform promises, for which evidence classes, with what storage and Reactor-versioning obligations.

## Why it is consequential

These are different platforms, not different phrasings of one platform. They imply different storage volumes, different version discipline in the Reactor, and different strength of evidence claims. §19 states the practical risk plainly: two downstream documents left to interpret "exact or contractually equivalent" will pick different readings within a month.

## What is already constrained

Until decided, the phrase is **cited as a fork** and never resolved locally (§19).

## What this record constrains

- `../01-core/reactor.md`
- `../01-core/runs.md`
- `../02-platform/storage.md`
- `../03-quality/repeatability.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
