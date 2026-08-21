# DEC-18 — When a person edits a rule by hand, what happens to its story?

*Formal name: human Plugin edits. Cite this record as **DEC-18**.*

**Status:** open; substantially narrowed · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — most of the original question is now settled law; one piece remains

> **In one sentence:** a person is always allowed to edit a rule directly — that's a founding promise — and most of what happens next is settled; what's open is only how the rule's *description* catches up with its changed reality.

---

## What this is about

Every rule carries two things: the code that runs, and the stated intent — the plain-language account of what it's supposed to do. When a person edits the code by hand, the two can come apart. The code has changed; the description hasn't.

Clinical records solved the general problem long ago: you never overwrite the original note. You add a signed addendum — dated, attributed, alongside the original. The chart tells the whole story, including the fact that the story changed.

Most of our version of this is now settled law in the core documents:

- **An edit creates a new revision.** It inherits nothing — no prior approval, no prior admission. It gets checked at the door like any other rule.
- **A human's edit earns no extra trust.** Rules are held to one contract regardless of who wrote them — machine, person, or one repairing the other. (The tempting alternative — trust the human's version more — has a hole in it shaped exactly like the most confident person in the room.)
- **The old intent is never overwritten.** After an edit, the stated intent is marked *stale until confirmed*, and both the previous intent and the new unconfirmed code are preserved.

## What's open

Just the catch-up procedure: once the intent is marked stale, what happens? Ask the editor to confirm or restate it? Have the machine draft a new description from the edited code (which is interpretation, never evidence — that classification is already law)? Hold both indefinitely with the mismatch visible? Probably some ordered combination — and the right ordering is best chosen when real hand-edits exist to look at.

## What this is blocking right now

- Nothing. The rails that prevent damage (new revision, no inherited trust, nothing overwritten) are all in force. What's missing is only convenience, not safety.

---

## The precise version

*This is the wording other documents cite.*

When a person edits a Plugin's implementation directly by hand, how intent and provenance update so the semantic chain stays honest. Substantially narrowed by `../01-core/plugins.md` PLUGIN-5 through PLUGIN-7: trust follows role, not authorship; a direct edit produces a new revision inheriting no admission or privilege; recorded intent is stale-until-confirmed with both records preserved. Open: the confirmation/regeneration procedure for stale intent.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability; status annotated as substantially narrowed.** Plain-question format. The narrowing was done by the core contract set (PLUGIN-5 to PLUGIN-7), not by this rewrite; this record now reflects it. Question, identifier, and constraints unchanged. Prior text is in version history.

**2026-08-20 — the language name removed from this record.** *Was:* "When a human directly modifies Plugin **Python** …". *Now:* the wording above. Same reasoning and same origin as the amendment on DEC-7: a Level 2 record naming a language makes a Level 3 decision by accident. The identifier, status, and question are unchanged. SCR-F §40.2's own text for this record still names the language; that correction is pending as an amendment to Foundations.
