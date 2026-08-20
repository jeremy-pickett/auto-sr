# Cells

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/cells.md`
**Cites:** SCR-F v0.2 §13, §13.1, §30.2; F-7

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The Cell state contract: what a Cell declares in advance, and how declarations are expressed and checked.
- **The computational ceiling's exact numbers.** §13.1 establishes that a ceiling exists and that Cell state must be a bounded set of primitive scalars declared in advance; it explicitly assigns the numbers to a requirements document. This is that document.
- How the ceiling is enforced — at declaration, at Lab fit review (§30.2), or at execution — and what a violation produces.
- What a Cell does *not* own: domain meaning, execution order, global behavior (§34).

## Decisions this document must not resolve locally

None recorded in §40 as blocking this document. If writing it surfaces a consequential choice, the choice is registered as a new DEC record — it is not answered here (F-22, §36.5).
