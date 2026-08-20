# DEC-8 — World storage

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What common representation handles spatial and relational Worlds without forcing one into the other's shape.

## Why it is consequential

A Grid World and an Identity World are both Worlds under §14, and a storage model built for one will quietly make the other second-class. That distortion would then propagate into Layout families, Readers, and Views without anyone deciding it.

## What this record constrains

- `../01-core/worlds.md`
- `../02-platform/storage.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
