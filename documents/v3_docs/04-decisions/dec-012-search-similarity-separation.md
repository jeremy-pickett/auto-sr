# DEC-12 — Search similarity separation

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How intent similarity, mechanism similarity, and observed-behavior similarity are kept distinct.

## Why it is consequential

§23 explicitly wants queries that depend on the three coming apart — *mechanisms with similar observed behavior but very different stated intent* is only answerable if they were never collapsed into one score. §25.6 adds the presentation risk: any cluster or neighborhood must state which similarity measure created it.

## What this record constrains

- `../01-core/search.md`
- `../01-core/visualization.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
