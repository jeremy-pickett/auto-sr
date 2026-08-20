# Runs

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/runs.md`
**Cites:** SCR-F v0.2 §7, §19, §24.1, §38.5; F-10

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- What a Run binds: Plugin version(s), World and Layout, Reactor version, starting conditions, controlled randomness, Lab contract, execution limits (§19).
- What a Run records, and what reconstruction from that record must guarantee.
- Immutability as an enforced property, not a convention: which endpoints or operations may touch a completed Run, and which may not (§7).
- Run-completes-before-playback as the default conceptual model, and what that buys — scrubbing, backward stepping, later Readers, repeatable views over one history (§19, §38.5).
- The failure taxonomy's Run-side entries (§10): Reactor rejection, Run failure, and behavior miss are distinct outcomes that are all retained.

## Decisions this document must not resolve locally

- **DEC-1 — Mechanism composition.** *Open.* How many mechanisms one Run admits.
- **DEC-2 — Replay equivalence.** *Open.* Until it is decided, "exact or contractually equivalent" is cited as a fork and never resolved locally (§19).
- **DEC-19 — Live work.** *Open.* How provisional live observation stays separate from a finalized immutable Run.
