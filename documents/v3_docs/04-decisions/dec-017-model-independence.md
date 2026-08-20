# DEC-17 — Model independence

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Which parts of Generation are provider-neutral, and how model changes appear in provenance.

## Why it is consequential

§32 requires future reviewers to distinguish *"we cannot reproduce this because the model is stochastic"* from *"we failed to record what we asked the model."* That distinction only survives a provider or version change if model identity and rendered inputs were recorded as first-class provenance rather than as configuration.

## What this record constrains

- `../01-core/generation.md`
- `../01-core/corpus.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
