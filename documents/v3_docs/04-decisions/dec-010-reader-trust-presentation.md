# DEC-10 — Reader trust presentation

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How Readers expose uncertainty and known failure cases in ordinary UI language.

## Why it is consequential

§21 forbids Readers becoming invisible truth layers, and §8 requires recorded evidence, derived evidence, and interpretation to stay distinguishable. Both are interface problems before they are storage problems: a measurement rendered without its uncertainty reads as a fact.

## What this record constrains

- `../01-core/readers.md`
- `../02-platform/frontend.md`
- `../01-core/visualization.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
