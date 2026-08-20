# DEC-5 — The home of semantic translation

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Translating World descriptions, Study questions, Search queries, and repair explanations is one class of capability, currently implied across four components. Which component owns it — or whether it is a Platform Service with a single contract — determines where its documents live and who is accountable for its failures.

## Why it is consequential

SCR-F states that a semantic human interface *governs* the components rather than becoming a thirteenth subsystem. That is a clear statement about what it is not, and no statement about where it lives. Four components each doing their own translation, with no shared contract, is the default outcome of leaving this open — and it is nobody's decision when it fails.

## What this record constrains

- `../01-core/generation.md`
- `../01-core/worlds.md`
- `../01-core/studies.md`
- `../01-core/search.md`
- `../00-start-here/human-and-machine.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
