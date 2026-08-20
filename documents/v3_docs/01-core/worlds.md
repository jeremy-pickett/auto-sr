# Worlds

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/worlds.md`
**Cites:** SCR-F v0.2 §14, §15, §18.5, §39; F-8

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The World contract: which Cells exist, how they are arranged, which Connections are possible, what conditions apply, what is observable, what the starting state is.
- **Layout as a property the World owns, not a separable component** (§14) — including why an independent Layout slot is refused, since that refusal is what makes incoherent pairings impossible by construction.
- The initial Layout families — Grid, Network, Identity, Agent — as starting families rather than a promise that every domain fits one of four boxes (§15).
- Which temporal capabilities a World may declare, given that declaration is the World's and ownership is the Reactor's (§18.5).
- The semantic World request path: how an ordinary-language World description becomes an exact, inspectable stored World (§14).
- Explicit non-inheritance of the 2.x fixed 200×200 torus and grid-only interaction (§39).

## Decisions this document must not resolve locally

- **DEC-1 — Mechanism composition.** *Open.* Includes the environment-as-mechanism boundary: whether a dynamic condition such as a current is a World property or a second participating mechanism (§14).
- **DEC-8 — World storage.** *Open.*
