# DEC-11 — Corpus identity

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How Same-Mechanism Families are recognized without hiding meaningful implementation differences.

## Why it is consequential

Grouping near-identical mechanisms is what makes a large Corpus navigable. It is also how a meaningful difference disappears — two Plugins that look alike and behave differently are exactly the case worth finding, and exactly the case a family view suppresses.

## What this record constrains

- `../01-core/corpus.md`
- `../01-core/search.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
