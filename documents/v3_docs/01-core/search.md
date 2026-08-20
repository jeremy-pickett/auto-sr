# Search

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/search.md`
**Cites:** SCR-F v0.2 §23, §42; F-16

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- What Search retrieves and over which Corpus surfaces — semantic similarity, Plugin structure, World properties, Reader measurements, Study results, outcome history, intent/outcome disagreement, known failures, human annotations (§23).
- The rule that the ordinary user's query language stays semantic even where structured search also exists (§23).
- How retrieved results carry their provenance, so a mechanism found by Search arrives with the evidence that justifies it rather than as a bare recommendation.
- The §42 non-claim enforced at the interface: what Search covers is the space SCR has explored, never the space of all possible local mechanisms.

## Decisions this document must not resolve locally

- **DEC-12 — Search similarity separation.** *Open.* How intent similarity, mechanism similarity, and observed-behavior similarity stay distinct rather than collapsing into one score.
