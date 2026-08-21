# DEC-23 — Who sets up the board?

*Formal name: Starting State ownership. Cite this record as **DEC-23**.*

**Status:** open; leading candidate recorded · **Who decides:** the project owner · **Kind:** boundary — it decides whether our comparisons are fair tests

> **In one sentence:** every experiment starts from some arrangement, and two parts of our own history disagree about who creates it — which matters because a comparison where each contestant set up their own board is not a comparison.

---

## What this is about

Put two cooks in the same kitchen to settle whose technique is better. If each brings their own ingredients, you've settled nothing — any difference on the plate might be the groceries. A fair test means same kitchen, same ingredients, technique varies.

Our founding document says the experimental setting owns the starting arrangement. But the earlier working system did it the other way: the *rule* generated its own starting arrangement (it was the one place a rule could use randomness). Both readings sit in the record, and they can't both stand — because one of our flagship experiment types is exactly the two-cooks test: **hold everything constant, vary only the mechanism.** If each mechanism sets up its own board, that experiment is invalid on its face.

The counter-argument is real: the rule often *knows* what a sensible setup looks like — what density of starting material makes anything happen at all. A generic setting description doesn't know that.

## The leading candidate — recorded, not adopted

Separate three things that were being conflated:

> **The setting** (the kitchen): durable — what exists, how it's arranged, what's possible.
> **The starting arrangement** (the ingredients on the counter): the actual opening values for one experiment, recorded exactly, owned by the experiment record.
> **The recipe**: a *described procedure* for producing a valid starting arrangement. A rule or Lab may supply one — that's where the knowledge lives — but the recipe is not the arrangement. The platform executes the recipe under its own controlled randomness, records the exact result, and binds *both* to the experiment.

This keeps the fair test fair (same kitchen, same ingredients, technique varies — checkable, because the arrangement is recorded separately), keeps the knowledge where it lives (rules may still say how to set up), and improves the record (not just "random seed 1234" but the exact arrangement *and* the recipe that produced it).

## What's genuinely open

1. Is a starting arrangement a first-class stored object (reusable across experiments by name) or a per-experiment attribute?
2. When a family of experiments shares one, who owns the family?
3. How is a recipe expressed so it stays a setup instruction and doesn't become a second mechanism in disguise?

Question 3 is the sharp one — a recipe with enough expressive power *is* a rule, and then it needs the whole rule contract.

## What this is blocking right now

- Formal validity of the mechanism-comparison Study pattern (`../01-core/studies.md` STUDY-6 refuses the pattern where the split doesn't hold).
- `../01-core/worlds.md` §4 and `../01-core/runs.md` RUN-6 are written to the candidate and labelled as such — if this decision goes another way, those sections change shape, not just wording.

---

## The precise version

*This is the wording other documents cite.*

Who owns the values an experiment starts from — the World, the mechanism, or neither. Leading candidate recorded in `../01-core/worlds.md` §4 (WORLD-4 to WORLD-6) and written into `../01-core/runs.md` §2: World and Starting State as separate inputs; a mechanism or Lab may supply a start recipe; realized values are produced under the Reactor's controlled randomness and bound to the Run alongside the recipe. Open: whether a Starting State is a first-class stored object or a Run attribute; family sharing; and how a recipe is expressed without becoming a mechanism in disguise.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and the recorded candidate unchanged. Prior text is in version history.
