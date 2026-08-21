# DEC-12 — Similar how, exactly?

*Formal name: Search similarity separation. Cite this record as **DEC-12**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — the separation is law; the machinery is not

> **In one sentence:** "these two are similar" means three different things here — meant to do the same job, built the same way, behaved the same way — and the settled rule is that the platform never blends them into one score; what's open is how each is actually computed.

---

## What this is about

Any investigator keeps these apart by training: same *method* across two cases is one kind of lead; same *description* of who was involved is another; same *outcome* is a third. Blur them into one "similarity" and you get connections that feel meaningful and prove nothing.

Our three, as law in the search requirements:

- **Intent similarity** — the descriptions say they were meant to do the same thing.
- **Construction similarity** — the rules are built alike.
- **Behaviour similarity** — the measurements say they acted alike.

The platform's most valuable questions live in the *gaps* between these. *Built alike, behaved differently* is the surprise worth finding. *Meant differently, behaved alike* is a discovery. One blended relevance score — the industry-standard shortcut — destroys both questions while looking better in a demo.

Also settled: any cluster, map, or neighbourhood shown to a person **names the similarity measure that made it**. Proximity on a screen is evidence of a computation, not of a relationship.

## What's open

The machinery: how each of the three is actually computed, over what data, and how well each computation works. That is empirical, and real Lab data will judge it better than we can in advance.

## What this is blocking right now

- Nothing. The constraints are registered (SEARCH-4 to SEARCH-7); the computations get built and evaluated when Search is built.

---

## The precise version

*This is the wording other documents cite.*

How intent similarity, mechanism similarity, and observed-behaviour similarity are kept distinct. Constrained by `../01-core/search.md` SEARCH-4 through SEARCH-7: computed, stored, and displayed separately; never combined into a single score; every similarity-ordered result and every cluster names its measure and data.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
