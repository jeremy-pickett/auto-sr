# DEC-11 — When are two rules the same rule?

*Formal name: Corpus identity. Cite this record as **DEC-11**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** boundary — grouping is what makes a big library usable, and also how differences disappear

> **In one sentence:** as the library grows into thousands of machine-written rules, we'll want to shelve near-duplicates together — but two rules that look identical and behave differently are exactly the find we built this for, and shelving hides them.

---

## What this is about

Generate mechanisms in bulk and you get variations on themes: dozens of rules that are clearly *the same idea*, differing in a constant here or a phrasing there. A usable library groups them — nobody wants forty shelf entries for one idea.

But consider two knots tied so alike that only an expert can tell them apart — and one of them slips under load. A catalog that files them as "the same knot" hasn't simplified the catalog; it has hidden the only fact about them that matters.

This platform's version of that is sharp: **small differences in a rule can produce large differences in behaviour — that's the premise the whole instrument is built on.** So "these two are basically the same" is never a safe clerical judgment here. Sometimes it's true. Sometimes it's the exact discovery we're in business to surface.

## What's already decided

One constraint is law: any grouping **states the basis it was made on** and stays inspectable down to the individual rule. No silent shelving. And the search system keeps three kinds of similarity — same intent, same construction, same behaviour — permanently separate, which is what makes "built alike, behaves differently" findable at all.

## What's open

The actual grouping method: what evidence (construction? measured behaviour? both?) justifies calling rules a family, and how a family display keeps its members' differences one click from the surface.

## What this is blocking right now

- Nothing at today's library size (tens of rules). It becomes real at thousands — which the planned scale-up will produce.

---

## The precise version

*This is the wording other documents cite.*

How Same-Mechanism Families are recognized without hiding meaningful implementation differences. Constrained by `../01-core/corpus.md` CORPUS-15 (a grouping states its basis and remains inspectable at the individual level) and `../01-core/search.md` SEARCH-4/SEARCH-5 (intent, mechanism, and observed similarity are never combined into one score).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
