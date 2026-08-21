# DEC-7 — What is a rule allowed to do?

*Formal name: Plugin contract surface. Cite this record as **DEC-7**.*

**Status:** open · **Who decides:** the project owner · **Kind:** boundary — the shape of the contract every generated rule signs

> **In one sentence:** every rule that runs here operates under a written agreement — what it may look at, what it may change, what tools it gets — and we have not yet fixed the exact list, only the discipline around it.

---

## What this is about

A rule is the one part of the platform written fresh for each experiment — by a machine, usually. So it works like a contractor's badge, not an employee's trust: access to declared rooms, declared tools, nothing else, and the list is written down before work starts.

The rule declares in advance: what it reads, what it changes, how far it can see, which helpers it uses. The platform checks the declaration at the door and enforces it throughout. All of that machinery is specified and settled.

What's open is the **list itself**: which capabilities exist to be declared. Too small a list, and rules for network-shaped or relationship-shaped worlds can't be written at all. Too large, and enforcement gets porous while readability collapses — a rule nobody can read is a rule nobody can check.

## What's already decided

Two disciplines, both firm:

1. **Adding a capability is a contract change, never a convenience.** No capability arrives because someone needed it once and it seemed harmless. It gets proposed, recorded, and decided — because a capability nobody agreed to is how contracts rot.
2. **The contract is about what a rule may *do*, not the language it's written in.** Those were tangled together in this record's original wording; they've been separated (see the record history), because the capability list and the notation have different owners and different lifetimes.

## Why it can't be finished yet

Two other open decisions reach directly into this contract:

- If more than one rule can run at once (**DEC-1**), the contract must say how rules see each other.
- If the platform offers timing beyond lockstep (**DEC-3**), the contract must say how a rule asks for "later" without owning a clock — the asking mechanism is settled; the vocabulary for it is not.

So this record closes *after* those two, by design. Deciding it first would mean deciding them by accident.

## What this is blocking right now

- The final written contract in `../01-core/plugins.md` — which currently specifies everything except the closed capability list (PLUGIN-2 names the categories; the entries await this record plus DEC-1 and DEC-3).
- Nothing else. Rules run today under the earlier system's list, which is inherited practice, not the decision.

---

## The precise version

*This is the wording other documents cite.*

What set of capabilities a Plugin may use — what it may read, what it may propose, what helpers it is given — that is expressive enough for Grid, Network, Identity, and Agent Worlds while remaining readable by a person and enforceable by the Reactor.

**This record covers the contract, not the notation.** Which language expresses the contract is a separate, Level 3 decision. The contract question is about what a mechanism is permitted to do; the language question is about how it is written down. They have different owners, different lifetimes, and different consequences when they change.

Additions to the set of permitted operations are contract changes, decided and recorded as such — never implementation decisions made in passing. DEC-1 and DEC-3 press directly on this record, as above.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.

**2026-08-20 — the language name removed from this record.**

*Was:* "What exact **Python** surface is expressive enough for Grid, Network, Identity, and Agent Worlds while remaining readable and enforceable." Supporting text referred to the approved language-specific operation lists by their language-specific names.

*Now:* the contract stated as a set of capabilities, with the choice of language separated out and pushed to Level 3.

*Why:* naming a language in a Level 1 or Level 2 document makes a Level 3 decision by accident and makes it permanent by placing it too high. The requirement that survives at this level is a property — a representation a competent person can read, change, and hand to someone else without the platform's help. The full argument is in `../00-start-here/what-is-scr.md`; the rule is in `../00-start-here/language-rules.md`; the parallel proposed amendment to SCR-F §2, §17, and §36.7 is recorded in `../00-start-here/glossary.md`.

*Raised by:* the project's human owner, 2026-08-20. Applied here rather than deferred, because a record that governs the Plugin contract is exactly where the defect would have done the most damage before anyone noticed.

*What did not change:* the identifier, the status, the decision. DEC-7 is still open, still owns the same question, and is still cited the same way. Identifiers are permanent and never reused (§36.5).

*Still outstanding:* SCR-F v0.2 §2, §17, §36.7, and §40.2's own text for this record all still name the language. This amendment does not reach into SCR-F — that is an amendment to Foundations, and it is pending.
