# Search

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/search.md`
**Identifier namespace:** `SEARCH-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §23, §25.6, §42; F-16 · DEC-11, DEC-12
**Depends on:** `corpus.md`, `readers.md`, `runs.md`.

> **Search** turns accumulated evidence back into useful work. It is what a platform does when it cannot derive the answer: you cannot compute the mechanism that produces branching, so you find one that did.

---

## 1. What Search owns

**SEARCH-1.** Retrieval across the Corpus, over: stated intent; mechanism structure; declarations; World and Layout properties; Reader measurements; Study findings; outcome history; disagreement between intent and outcome; failures; and human annotations.

**SEARCH-2.** The ordinary query stays in ordinary language, whatever structured querying also exists.

**SEARCH-3.** Every result arrives with its provenance. A retrieved mechanism carries the evidence that justifies it, never a bare recommendation.

---

## 2. What Search refuses

| Refused | Owner |
|---|---|
| Generating anything | Generation |
| Executing anything | Reactor |
| Measuring anything | Reader |
| Deciding relevance is correctness | a person |
| Implying it searched what it did not | nobody — SEARCH-8 |

---

## 3. Three kinds of similarity, kept apart

**SEARCH-4.** Three similarities are computed, stored, and displayed separately, and are never combined into a single score:

> **Intent similarity** — these were meant to do the same thing.
> **Mechanism similarity** — these are built the same way.
> **Observed similarity** — these behaved the same way.

**SEARCH-5.** Any result ordered by similarity states which of the three ordered it.

The platform's most valuable queries depend entirely on the three coming apart. *Mechanisms with similar behaviour but very different stated intent* is answerable only if behaviour and intent were never collapsed. So is *mechanisms built almost identically that behave differently*, which is the case a family view is most likely to hide (CORPUS-15).

A single blended relevance score destroys both queries and looks better while doing it. DEC-12 owns this.

---

## 4. Clusters and neighbourhoods

**SEARCH-6.** Any grouping, cluster, distance, neighbourhood, or map presented to a person states the similarity measure that produced it and the data it was computed over.

**SEARCH-7.** Proximity in any such display is never presented as evidence of a relationship. It is evidence of a computation, and the computation is named.

This is the platform's most presentable capability and its easiest to abuse. A scatter of mechanisms arranged by an unnamed similarity looks like a discovered structure and is a rendering choice.

---

## 5. What Search does not cover

**SEARCH-8.** Search covers what the platform has explored. Interfaces state this where a person could reasonably read absence as evidence of absence.

*No mechanism in the Corpus produced this behaviour* means nobody generated one that did. It does not mean none exists, and the difference is the whole of §42's non-claim (GEN-20, GEN-21). An empty result is a fact about the library, not about the world.

---

## 6. What Search requires

- **From the Corpus:** links, versions, and provenance.
- **From Readers:** versioned measurements, so a search over behaviour can say which version of "travelling" it matched.
- **From Runs:** bound identity, so a result can be checked for relevance to the asker's actual question.

## 7. What Search produces

Retrieved records with their evidence, an ordering that names its basis, and an honest statement of what was searched.

---

## 8. Open decisions

- **DEC-12 — Similarity separation.** Constrained by SEARCH-4 to SEARCH-7.
- **DEC-11 — Corpus identity.** Determines what a family result may hide.
- **Unregistered — exploration strategy.** Search knows what has been tried and is the natural source for what to try next, but owns no such responsibility (`generation.md` §9).
