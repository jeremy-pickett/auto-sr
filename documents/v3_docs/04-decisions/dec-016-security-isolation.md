# DEC-16 — Security isolation

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What production execution boundary replaces the hardened single-user 2.x host assumption.

## Why it is consequential

§18.4 requires the generated-code boundary to stay an explicit contract and execution-safety problem, and F-20 forbids an adversarial Lab from justifying a permissive surface. The 2.x answer — a child process with resource limits on a single trusted host — was appropriate for a toy and is listed in §39 as inheritance, not requirement.

## What this record constrains

- `../02-platform/execution-safety.md`
- `../01-core/reactor.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
