# DEC-6 — 2.x corpus migration

**Document class:** Level 2 — Architecture Decision · **Status:** partially decided
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How the existing 2.x library enters the 3.x Corpus: identifier mapping into 3.x namespaces, comparability across engine and Reactor versions, and which 2.x derived data is recomputed under 3.x Readers versus preserved as historical readings.

## Why it is consequential

For a permanence-obsessed project, v0.1's silence on this was itself a foundational unknown. The library is small today — tens of Runs — but §22.1 records a planned scale-up of several orders of magnitude, so migration will run against a substantially larger body than exists now. Deciding late means deciding against more data.

## What is already constrained

**Decided (§22.1):** the 2.x library is carried forward into the 3.x Corpus as **founding evidence**. It is not archived, not orphaned, and not a separate lineage.

**Constrained by §7:** the 2.x histories are immutable evidence. Whatever 3.x does around them, it does not rewrite them.

## What this record constrains

- `../01-core/corpus.md`
- `../02-platform/storage.md`
- `../01-core/readers.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
