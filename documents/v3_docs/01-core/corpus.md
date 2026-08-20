# Corpus

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/corpus.md`
**Cites:** SCR-F v0.2 §22, §22.1, §31, §32, §32.1, §38.8; F-15, F-21

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- What the Corpus links (§22's list), and the rule that the Corpus is the asset while the database is an implementation choice.
- The provenance chain of §32, made boringly complete — including rendered model inputs, model identity, repair history with its semantic accounts, versions of every participating component, and human corrections.
- The distinction between permanent experimental history and operational telemetry, preserved regardless of where either is stored (§22).
- **Evidence integrity over the record, never in the data** (§32.1): content addressing, hash chains, signed export manifests — and the permanent rejection of watermarks, statistical residues, or any provenance embedded into Cell state.
- Failure retention as a Corpus obligation across all seven failure classes (§10, F-14).

## Decisions this document must not resolve locally

- **DEC-6 — 2.x corpus migration.** *Partially decided.* Decided: the 2.x library carries forward as founding evidence (§22.1). Open: identifier mapping, cross-version comparability, and which derived data is recomputed under 3.x Readers versus preserved as historical readings. Constrained by §7 — migration never rewrites 2.x histories.
- **DEC-11 — Corpus identity.** *Open.* How Same-Mechanism Families are recognized without hiding meaningful implementation differences.
