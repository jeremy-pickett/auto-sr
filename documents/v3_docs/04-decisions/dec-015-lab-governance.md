# DEC-15 — Lab governance

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What minimum evidence is required before a Lab is described as validated rather than experimental.

## Why it is consequential

§30 lets Labs fail their fit review and calls a rejected Lab useful evidence about SCR's boundary. That only works if *passing* means something specific. The Lab catalog already carries inherited bracketed standings that are explicitly not fit findings — the gap between the two is what this record closes.

## What this record constrains

- `../01-core/labs.md`
- `../03-quality/accuracy.md`
- `../labs/`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.

---

## Note on vocabulary

SCR-F §40.2 registered this record as asking when a Lab may be "described as **validated** rather
than experimental." The core documents no longer use that word: `../01-core/labs.md` LAB-9 names the
third status **confirmed**, and LAB-10 forbids *verified* and *validated* of any model of a
real-world system. The reasoning is in `../03-quality/accuracy.md` §1 — verification and validation
of numerical models of natural systems is not achievable, and confirmation is partial by
construction.

The question this record asks is unchanged: what minimum evidence is required before a Lab is
described as more than experimental. Only the word for the destination has changed. The original
wording is preserved above and in SCR-F §40.2, which has not been amended.
