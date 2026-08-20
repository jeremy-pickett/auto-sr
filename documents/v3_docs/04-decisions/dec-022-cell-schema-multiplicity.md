# DEC-22 — Cell schema multiplicity

**Document class:** Level 2 — Architecture Decision · **Status:** open; lean recorded
**Registered by:** the core contract set, 2026-08-20 (`../01-core/`), following external critique
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Whether one World may declare more than one kind of Cell, each with its own bounded set of properties.

## Why it is consequential

A grid of terrain patches is honestly one kind of thing. A World built on relationships is not: an account, a group, a role, and a resource are four different kinds of participant carrying four different sets of meaningful properties, and no honest single schema covers all four.

*If one kind:* the schema is trivial to enforce, storage is uniform, measurement is straightforward — and three of the four named Layout families receive a superset schema in which most properties are meaningless for most Cells. That is a way of supporting them in name.

*If several kinds:* relational Worlds become honestly expressible, and matching, storage, measurement, and display all become materially harder. A real hazard appears: several schemas can drift toward an arbitrary object graph, at which point the semantic ceiling is the only thing still holding the line.

## What is already constrained

**Constrained regardless of the answer:** the semantic ceiling (CELL-5) holds for every schema. A property is a number, a whole number from a declared finite set, or a true/false value. Multiplicity of schemas never becomes freedom of kind.

**Lean recorded, not adopted.** The reviewed critique leans toward several bounded schemas, with connection classes declaring which kinds of Cell they may join, and with the representation staying columnar and bounded rather than becoming a graph of objects.

## What this record constrains

- `../01-core/cells.md`
- `../01-core/worlds.md`
- `../02-platform/storage.md`
- `../01-core/readers.md`
- `../01-core/visualization.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
