# DEC-13 — Visualization scale

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What evidence formats advanced 3D Views require so they do not need entire Runs replayed server-side.

## Why it is consequential

The §25 Views — Time View, Influence View, Study View, Behavior Map, Corpus View — are roadmap candidates, and §25's own framing asks only that the architecture avoid decisions making them prohibitively expensive later. That is a storage and transport question that has to be answered before the storage format sets.

## What this record constrains

- `../01-core/visualization.md`
- `../02-platform/transport.md`
- `../02-platform/storage.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
