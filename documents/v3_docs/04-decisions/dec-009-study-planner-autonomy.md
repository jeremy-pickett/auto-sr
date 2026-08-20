# DEC-9 — Study planner autonomy

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How much SCR infers automatically from a semantic question before requiring human confirmation.

## Why it is consequential

§20.2 wants users to state questions in ordinary troubleshooting language and have SCR propose the hypothesis for confirmation. Too little inference and the product demands academic theater; too much and the machine has quietly chosen the experiment, which is F-4's line.

## What this record constrains

- `../01-core/studies.md`
- `../00-start-here/human-and-machine.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
