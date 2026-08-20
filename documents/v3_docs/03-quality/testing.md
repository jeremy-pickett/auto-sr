# Testing

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `03-quality/testing.md`
**Cites:** SCR-F v0.2 §16.3, §16.4, §38.3, §43

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- What the platform's own test suite covers, and the separation between testing the harness and testing generated mechanisms.
- The 2.x practice worth carrying: harness tests run against hand-written fixtures, never against generated rules, so the test suite cannot drift with the generator.
- Contract checks before expensive execution — structure, permitted capabilities, declared reads and writes, determinism (§16.3).
- Validation Runs sufficient to catch implementation defects, non-reproducibility, illegal state behavior, and obvious contract violations (§16.4).

## Decisions this document must not resolve locally

None recorded in §40 as blocking this document. If writing it surfaces a consequential choice, the choice is registered as a new DEC record — it is not answered here (F-22, §36.5).
