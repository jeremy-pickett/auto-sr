# DEC-5 — Who owns the translating?

*Formal name: the home of semantic translation. Cite this record as **DEC-5**.*

**Status:** open · **Who decides:** the project owner · **Kind:** placement — the capability exists either way; the question is who is accountable for it

> **In one sentence:** four different parts of the platform each turn human words into something exact — and right now, when a translation goes wrong, it is nobody's job.

---

## What this is about

This platform's founding promise is that people work in their own words. That means translation is happening constantly, in at least four places:

- someone describes a **setting** ("a coastal grid with a west-to-east current") and it becomes an exact stored World;
- someone asks a **question** ("does it still work from a different starting point?") and it becomes a structured Study;
- someone **searches** ("show me mechanisms that produce branching") and it becomes a query;
- the platform **explains a repair** back to a person in plain words.

Four components, each doing its own translating, no shared standard.

Hospitals learned this lesson the hard way, which is why medical interpreting is a profession with standards rather than "whoever nearby speaks the language." The issue was never whether translation happened — it was that when an untrained translation caused harm, there was no standard it had violated and no one whose job it had been. **Distributed informal translation means unaccountable translation.**

## Why it's a real question

If we leave this open, the outcome isn't disaster — it's drift. Four components each develop their own habits. The same phrase means slightly different things depending on where you typed it. Quality varies by corner. And when a bad translation ruins an experiment, the failure lands between components, where post-mortems go to die.

The founding document says one clear thing: the human interface *governs* the components rather than becoming a thirteenth one. That rules out a new tentpole. It does not say where the work lives.

## Your options

### A — Each component owns its own
No new structure. Costs: four dialects, four quality levels, and no one accountable for translation as such.

### B — One shared translation service with one contract
Every "words → exact thing" conversion goes through one door with one standard and one test suite. Costs: a new platform service to specify, and a risk it becomes a bottleneck everything queues behind.

### C — Generation owns it all
Generation already does the hardest translation (intent → mechanism). Extend its remit to Worlds, Studies, and Search. Costs: Generation's identity blurs — it stops being "the pipeline that makes mechanisms" and becomes "the place words go," which is a very different component to reason about.

## What would make this easy to decide

> **When a translation failure ruins someone's week, whose door do you want them knocking on?**

If the answer is "one door," it's B, and the remaining work is scoping the service. Worth noting: B is also the only option where "did we translate that right?" can be tested once, centrally, against real data from every Lab — which matters, because real data is coming and translation is where it will hit first.

## What this is blocking right now

- Nothing is stopped — each component translates for itself today, per option A by default.
- What accumulates is A's cost: every month of building deepens four separate habits, making B and C more expensive to reach later. This is a decision that gets harder with time, not easier.
- `../01-core/generation.md`, `worlds.md`, `studies.md`, `search.md`, and `../00-start-here/human-and-machine.md` all cite this record.

---

## The precise version

*This is the wording other documents cite.*

Translating World descriptions, Study questions, Search queries, and repair explanations is one class of capability, currently implied across four components. Which component owns it — or whether it is a Platform Service with a single contract — determines where its documents live and who is accountable for its failures. SCR-F states that a semantic human interface *governs* the components rather than becoming a thirteenth subsystem: a clear statement about what it is not, and no statement about where it lives.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
