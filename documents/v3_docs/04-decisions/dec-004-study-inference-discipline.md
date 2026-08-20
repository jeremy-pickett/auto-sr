# DEC-4 — Study inference discipline

**Document class:** Level 2 — Architecture Decision · **Status:** open; stance constrained
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What "required confidence" means, who requires it, and what a Study is permitted to claim.

## Why it is consequential

The phrase appears in two load-bearing places — the failure taxonomy's Study-failure entry (§10) and the hypothesis machinery (§20.2) — and is defined in neither. §10 explicitly warns that documents citing the taxonomy must not invent local definitions, which is precisely what a model-written document will otherwise do.

## What is already constrained

**The stance is constrained in advance by §20.3.** Study's statistics must be modest and plainspoken: counts, proportions, distributions, and paired comparisons, in ordinary language, with what was *not* tested stated alongside what was. Significance theater, invented precision, and confidence numbers no one can trace to a computation violate F-5 and §43 at once.

The worked example §20.3 gives: *"19 of 20 starts produced a traveler; the one failure started inside the obstacle"* says more, more honestly, than a p-value against an unstated null.

## What this record constrains

- `../01-core/studies.md`
- `../03-quality/accuracy.md`
- `../00-start-here/language-rules.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
