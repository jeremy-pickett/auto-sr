# Repeatability

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `03-quality/repeatability.md`
**Cites:** SCR-F v0.2 §7, §19, §38.3; F-10

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- What replay guarantees the platform actually promises, for which evidence classes.
- The reproducibility check as a gate in Generation, and as an ongoing property of the Corpus rather than a one-time test (§38.3).
- Execution-semantics versioning: identical source under a different Reactor revision is a different experiment, and the record must show it (§19).
- How the platform distinguishes "we cannot reproduce this because the model is stochastic" from "we failed to record what we asked the model" (§32).

## Decisions this document must not resolve locally

- **DEC-2 — Replay equivalence.** *Open.* Bit-exact versus contractually equivalent replay is this document's central undecided question, and §19 forbids resolving it locally.
