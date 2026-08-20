# DEC-20 — External calibration

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How SCR packages candidate mechanisms for serious domain tools without implying domain validity it has not earned.

## Why it is consequential

§41 is unambiguous: a mechanism reproducing an observed pattern is a candidate explanation, not proof of causation, and domain calibration remains a domain problem. The export format is where that non-claim either travels with the mechanism or gets left behind.

## What this record constrains

- `../03-quality/accuracy.md`
- `../03-quality/reference-cases.md`
- `../01-core/labs.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
