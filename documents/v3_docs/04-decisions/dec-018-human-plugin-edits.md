# DEC-18 — Human Plugin edits

**Document class:** Level 2 — Architecture Decision · **Status:** open
**Registered by:** SCR-F v0.2 §40.2
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

When a person edits a Plugin's implementation directly by hand, how intent and provenance update so the semantic chain stays honest.

## Why it is consequential

§2 requires that a human can read, diff, modify, and review the Plugin — and §3 requires intent, implementation, and outcome to stay separate records. A hand edit is the moment those two requirements meet: the implementation changed, and nothing has yet updated what the mechanism is claimed to be.

## What this record constrains

- `../01-core/plugins.md`
- `../00-start-here/human-and-machine.md`
- `../01-core/corpus.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.

---

## Amendment record

**2026-08-20 — the language name removed from this record.** *Was:* "When a human directly modifies
Plugin **Python** …". *Now:* the wording above. Same reasoning and same origin as the amendment on
DEC-7: a Level 2 record naming a language makes a Level 3 decision by accident. The identifier,
status, and question are unchanged. SCR-F §40.2's own text for this record still names the language;
that correction is pending as an amendment to Foundations.
