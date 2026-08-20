# Plugins

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/plugins.md`
**Cites:** SCR-F v0.2 §2, §6, §17, §18.5, §38.2; F-2, F-9

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The Plugin contract surface: declarations, what may be read, what may be proposed, which helper capabilities are provided, and how each is checked.
- The prohibitions in §17 made enforceable — no independent randomness, execution ordering, global time semantics, observation freshness, arbitrary Cell access, stopping criteria, history, provenance, or undeclared mutable state.
- The readability contract (§2), stated as the property rather than as a language: the Plugin is a permanent experimental artifact that a competent person can read, change, and hand to someone else without the platform's help. Any internal optimized representation is an implementation detail and must not silently displace it as the thing humans are expected to reason about. *(This document may name the language it chooses — Level 3 may. The requirement it satisfies may not be stated in terms of one.)*
- How a Plugin proposes a future-offset effect where the World declares temporal capabilities — as an ordinary proposal, budgeted like any write, with no Plugin-owned clock (§18.5).

## Decisions this document must not resolve locally

- **DEC-7 — Plugin contract surface.** *Open.* This is the document that record governs.
- **DEC-1 — Mechanism composition.** *Open.* Whether one Run admits one Plugin or several reshapes this contract directly.
- **DEC-3 — Temporal semantics.** *Open; placement decided.* The scheduling contract and budgets are DEC-3's; the placement (§6, §18.5) is already foundational law.
- **DEC-18 — Human Plugin edits.** *Open.*
