# Family G — Cities and infrastructure

**Document class:** Level 5 — Lab Papers (family index) · **Status:** draft
**Path:** `labs/g-cities-and-infrastructure/`
**Catalog:** SCR Lab Catalog v0.1, Family G (entries 41–46)
**Cites:** SCR-F v0.2 §11, §29, §30, §36.2, §36.6, §37, §41–43; F-17
**Fit reviews (§30):** none performed for any entry in this family.

> **Stub — no Lab paper here is written or adopted.** This file exists so downstream documents have a stable citation target (§36.2) and so the tree's shape is reviewable before the papers land. A model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, and refuse to answer a DEC-owned question locally (§36.6).

---

## Entries

| # | Lab | Standing | Production report |
| :-- | :--- | :--- | :--- |
| 41 | Urban Growth | **[strong]** | `family-g-report-v1.md` |
| 42 | Power Grid Cascade | ungraded | `family-g-report-v1.md` |
| 43 | Water Distribution | ungraded | `family-g-report-v1.md` |
| 44 | Freight and Rail Congestion | ungraded | `family-g-report-v1.md` |
| 45 | Service Cascade | ungraded | `family-g-report-v1.md` |
| 46 | Routing Instability | ungraded | `family-g-report-v1.md` |

**SCR-F §37 correspondence:** falls under §37's trailing `...`. All six entries are covered by `family-g-report-v1.md`.

Reviewed against `SCR_Labs_41-50_Critique_v0.1.md`; the report carries a revision record for what that pass changed.

This family holds the largest concentration of the **globally-computed-driver** boundary (42 power flow, 43 hydraulics — both likely mechanism-fit failures) and, at the opposite extreme, two entries where the local rule is **specified, human-written, and running in production**: 45 retry policies and 46 the BGP decision process. Those sit in the *mechanism-analysis* mode rather than mechanism-discovery — nothing needs inferring, and the many-participant consequences still require simulation.

**Entry 45 (Service Cascade) is, in my assessment, the strongest ungraded entry in the whole catalog**; entry 46 carries its most rigorous irreducibility credential (an NP-completeness result exactly where the interesting question is). Entry 43 is a recommended rejection contributing a category distinct from 42's.

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
