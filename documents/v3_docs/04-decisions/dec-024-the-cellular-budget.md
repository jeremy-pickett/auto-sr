# DEC-24 — The cellular budget

**Document class:** Level 2 — Architecture Decision · **Status:** open; no owner assigned
**Registered by:** the core contract set, 2026-08-20 (`../01-core/`), following external critique
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

How much of what makes this platform recognisably a local-mechanism instrument may be spent, who is keeping the ledger, and what is left when it is empty.

## Why it is consequential

Five properties characterise a cellular automaton: discrete cells; bounded local state; one uniform rule applied everywhere; every cell updating at once; interaction only between neighbours.

Line them up against the registry:

| Property | Status |
|---|---|
| Discrete cells, bounded state | Held. The semantic ceiling (CELL-5) is not tunable. |
| One uniform rule everywhere | **In play — DEC-1.** Several mechanisms is a non-uniform rule. |
| Everything updates at once | **In play — DEC-3.** |
| Interaction only between neighbours | **In play — DEC-21.** |
| One kind of participant | **In play — DEC-22.** Not a classical property, but it is the same kind of spend. |

Four of five are under active negotiation, and every individual argument for relaxing one is sound. That is exactly the problem. Each decision is registered separately, argued on its own merits, and decided by whoever is thinking about that component — and nobody is watching the total.

The failure mode is not a bad decision. It is a sequence of individually reasonable decisions after which the platform is a general-purpose simulator with a restrictive vocabulary, and nobody can point to the moment it stopped being what it said it was. SCR-F §45.12 asks reviewers to hunt precisely this, and gives them nothing to measure against.

An external critique of the core contract set recommended relaxations on three of the four, each well argued, and did not raise the aggregate. That is evidence the aggregate goes unnoticed by default rather than evidence the critique was careless.

## What is already constrained

**Nothing is constrained yet, and that is the finding.** This record exists to give the question an owner and a place, not to answer it.

What a decision here probably owes, beyond the usual: a statement of what remains true of every SCR experiment regardless of how the other four decisions land — the floor — and a rule requiring any future proposal to relax one of the five to state its effect on the total rather than only on its own component.

## What this record constrains

- `../00-start-here/what-is-scr.md`
- `../01-core/cells.md`
- `../01-core/worlds.md`
- `../01-core/plugins.md`
- `../01-core/reactor.md`
- every future core document

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
