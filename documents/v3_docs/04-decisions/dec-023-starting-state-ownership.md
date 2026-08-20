# DEC-23 — Starting State ownership

**Document class:** Level 2 — Architecture Decision · **Status:** open; leading candidate recorded
**Registered by:** the core contract set, 2026-08-20 (`../01-core/`), following external critique
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Who owns the values an experiment starts from — the World, the mechanism, or neither.

## Why it is consequential

SCR-F §14 places the starting state inside the World. The earlier system had the mechanism generate it, in the one place a mechanism was permitted to use randomness. Both readings are present in the material and they contradict each other.

This is not cosmetic. One of the platform's own Study patterns holds the World constant and compares mechanisms. If each mechanism generates its own start, that comparison is invalid on its face: every mechanism received a different opening arrangement, and any difference in outcome could be the start rather than the mechanism.

The counter-argument is real. A mechanism often does know what a sensible opening arrangement looks like — which Cells should be alive, where a seed belongs, what density makes anything happen at all — and a generic description of a setting does not.

## What is already constrained

**A leading candidate is recorded in `../01-core/worlds.md` §4 (WORLD-4 to WORLD-6)** and is written into `../01-core/runs.md` §2. It is not adopted.

Its move is to separate rather than choose: the **World** is the durable setting, the **Starting State** is the realized opening values for one Run or family of Runs, and they are separate inputs recorded separately. A mechanism or Lab may supply a *start recipe*; the realized values are produced under the Reactor's controlled randomness and bound to the Run alongside the recipe that produced them.

This makes "hold the World constant and vary the Starting State" mean exactly what it says, and makes a Plugin Comparison checkable.

What remains open: whether a Starting State is a first-class stored object in its own right or an attribute of a Run; whether a family of Runs shares one; and how a recipe is expressed without becoming a mechanism in disguise.

## What this record constrains

- `../01-core/worlds.md`
- `../01-core/runs.md`
- `../01-core/plugins.md`
- `../01-core/studies.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
