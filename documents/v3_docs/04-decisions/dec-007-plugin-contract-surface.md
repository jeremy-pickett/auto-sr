# DEC-7 — Plugin contract surface

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What set of capabilities a Plugin may use — what it may read, what it may propose, what helpers it is given — that is expressive enough for Grid, Network, Identity, and Agent Worlds while remaining readable by a person and enforceable by the Reactor.

**This record covers the contract, not the notation.** Which language expresses that contract is a separate, Level 3 decision, and separating the two is the point of the amendment recorded below. The contract question is about *what a mechanism is permitted to do*. The language question is about *how it is written down*. They have different owners, different lifetimes, and different consequences when they change.

## Why it is consequential

The two properties pull against each other. A surface wide enough for four Layout families is hard to enforce; a surface narrow enough to enforce cleanly may exclude Labs that otherwise fit.

One practice from the earlier system is worth carrying whatever surface is chosen: **additions to the set of permitted operations are contract changes, decided and recorded as such — never implementation decisions made in passing.** A capability that arrives because someone needed it once is a capability nobody agreed to.

Two open questions press directly on this one. If more than one mechanism can participate in a Run (DEC-1), the contract must say how they see each other. If the Reactor offers anything beyond simultaneous update (DEC-3), the contract must say how a mechanism proposes an effect for later without owning a clock.

## What this record constrains

- `../01-core/plugins.md`
- `../01-core/reactor.md`
- `../02-platform/execution-safety.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.

---

## Amendment record

**2026-08-20 — the language name removed from this record.**

*Was:* "What exact **Python** surface is expressive enough for Grid, Network, Identity, and Agent
Worlds while remaining readable and enforceable." Supporting text referred to the approved
language-specific operation lists by their language-specific names.

*Now:* the wording above — the contract stated as a set of capabilities, with the choice of language
separated out and pushed to Level 3.

*Why:* naming a language in a Level 1 or Level 2 document makes a Level 3 decision by accident and
makes it permanent by placing it too high. The requirement that survives at this level is a
property — a representation a competent person can read, change, and hand to someone else without
the platform's help. The full argument is in `../00-start-here/what-is-scr.md`; the rule is in
`../00-start-here/language-rules.md`; the parallel proposed amendment to SCR-F §2, §17, and §36.7 is
recorded in `../00-start-here/glossary.md`.

*Raised by:* the project's human owner, 2026-08-20. Applied here rather than deferred, because a
record that governs the Plugin contract is exactly where the defect would have done the most damage
before anyone noticed.

*What did not change:* the identifier, the status, the decision. DEC-7 is still open, still owns the
same question, and is still cited the same way. Identifiers are permanent and never reused (§36.5).

*Still outstanding:* SCR-F v0.2 §2, §17, §36.7, and §40.2's own text for this record all still name
the language. This amendment does not reach into SCR-F — that is an amendment to Foundations, and it
is pending.
