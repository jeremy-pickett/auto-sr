# Readers

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/readers.md`
**Cites:** SCR-F v0.2 §8, §21, §24.2; F-11

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The Reader contract: name, version, settings, exact evidence examined, output, and completeness or confidence where applicable (§21).
- Recompute-from-evidence as a property: a Reader result can be deleted and rebuilt from immutable history without changing history (§21).
- The three-way distinction between recorded evidence, derived evidence, and interpretation (§8), and how the system keeps them visibly separate.
- The platform-neutral Reader set the core may know about — spread, movement, branching, persistence, recurrence, stationary structure, traveler detection, front speed, hidden-state persistence — with Lab-specific Readers explicitly excluded from this document (§21).
- How a Reader's output is attributed in the interface, so Readers never become invisible truth layers (§21).

## Decisions this document must not resolve locally

- **DEC-10 — Reader trust presentation.** *Open.* How Readers expose uncertainty and known failure cases in ordinary language.

## A note this document must not lose

§21 is where v0.1's Lab leak occurred: security-Lab vocabulary appeared in a core Reader list eleven sections after the core was forbidden to know what a domain controller is. This document is the most likely place for that failure to recur, because Lab Readers are the vivid examples. Keep them out (§36.6).
