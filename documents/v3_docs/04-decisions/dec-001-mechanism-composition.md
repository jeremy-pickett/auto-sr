# DEC-1 — Mechanism composition

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.1 — *"the largest unnamed decision in v0.1"*
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How many mechanisms participate in one Run, and in what relation: multiple Plugins, dynamic World conditions, layered mechanism stacks, or a deliberate refusal to compose. Includes the environment-as-mechanism boundary — whether a condition like a west-to-east current is a World property or a second participating mechanism (§14).

## Why it is consequential

2.x bound one rule to one world, and SCR-F v0.1 inherited that phrasing — while every Lab example in the document quietly assumes composition. Fish behavior plus a current plus a temperature gradient is at least two mechanisms, arguably three. The wildfire Lab brief already records itself as blocked here: wind, terrain, and fire are at least two mechanisms.

The answer reshapes the Plugin contract, the Reactor, provenance, and every Lab template. Documents written before it lands will need rewriting after.

## What is already constrained

The single-Plugin reading is recorded as **2.x inheritance, not a decision** (§19, §39, §45.11). It carries no standing and must not be cited as settled.

## What this record constrains

- `../01-core/plugins.md`
- `../01-core/reactor.md`
- `../01-core/runs.md`
- `../01-core/worlds.md`
- `../02-platform/storage.md`
- every Lab paper under `../labs/`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
