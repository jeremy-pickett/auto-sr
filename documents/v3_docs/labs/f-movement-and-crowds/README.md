# Family F — Movement and crowds

**Document class:** Level 5 — Lab Papers (family index) · **Status:** draft
**Path:** `labs/f-movement-and-crowds/`
**Catalog:** SCR Lab Catalog v0.1, Family F (entries 36–40)
**Cites:** SCR-F v0.2 §11, §29, §30, §36.2, §36.6, §37, §41–43; F-17
**Fit reviews (§30):** none performed for any entry in this family.

> **Stub — no Lab paper here is written or adopted.** This file exists so downstream documents have a stable citation target (§36.2) and so the tree's shape is reviewable before the papers land. A model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, and refuse to answer a DEC-owned question locally (§36.6).

---

## Entries

| # | Lab | Standing | Production report |
| :-- | :--- | :--- | :--- |
| 36 | Crowd Egress | **[strong]** | `family-f-report-v1.md` |
| 37 | Highway Traffic | ungraded | `family-f-report-v1.md` |
| 38 | Pedestrian Flow | ungraded | `family-f-report-v1.md` |
| 39 | Warehouse Robot | **[plausible]** | `family-f-report-v1.md` |
| 40 | Degraded-Information Evacuation | ungraded | `family-f-report-v1.md` |

**SCR-F §37 correspondence:** falls under §37's trailing `...`. All five entries are covered by `family-f-report-v1.md`.

**Life-safety hazard:** entry 36 is operationally used in egress design, which makes SCR look adjacent to legitimate practice in a way it is not. Each entry declares a **supported regime** and a **boundary regime** rather than one scope — for entry 36 the dangerous high-density regime, where body-force chains dominate, is explicitly outside the abstraction. Entry 38 is the safer early public Lab, and the two are kept separate for epistemic reasons rather than merged.

**Two platform findings originate here.** Entry 39 proves **World fit and mechanism fit are independent** — a warehouse floor is a perfect discrete grid governed by a global central planner. And entry 40 makes **belief versus world** the phenomenon rather than an edge case, generalizing directly to attacker knowledge, defender visibility, stale identity state, and agent memory; it is the strongest reason to build that capability **before** Family H rather than after.

The family also proposes the **Mover** — a bounded state-bearing participant occupying a location and changing location under Reactor control — as a narrower construct than a full Agent ontology.

## What this folder holds

Production Lab papers for this family — the Level 5 documents that answer the nine §30 fit questions for a specific domain, plus the domain knowledge those answers rest on.

**It does not hold the drafting material.** The sixty first-pass Lab Knowledge Briefs live in `../short-lab-definitions/` and stay there as historical reference. They are working documents: unverified citations, single-axis assessments, and no fit review. Nothing in this folder should cite them as evidence; cite the production report that supersedes them.

## Standing

Bracketed standings in the catalog are inherited from *A Card Catalog for Emergence* v0.1 §5 and are **not** re-derived. Presence in the catalog is not fit (§30). No document in this folder may promote an ungraded entry by writing confidently about it, and none may assign a fit grade — the fit review is owned by `../../01-core/labs.md`, and Lab status vocabulary is blocked on **DEC-15**.

## Decisions this folder must not resolve locally

- **DEC-1 — Mechanism composition.** Whether a domain's forcing is a second mechanism, an external input, or a static World condition.
- **DEC-3 — Temporal semantics.** What one step means where a domain spans several natural clocks.
- **DEC-15 — Lab governance.** What evidence makes a Lab validated rather than experimental.
- **DEC-20 — External calibration.** How candidate mechanisms are packaged for domain tools without implying validity SCR has not earned.

## Non-claims

No Lab in this family forecasts, predicts, or assesses anything in any real system. Mechanisms generated here are candidate explanations requiring domain validation in domain tooling (§41, §43).
