# Family H — Information security

**Document class:** Level 5 — Lab Papers (family index) · **Status:** draft
**Path:** `labs/h-information-security/`
**Catalog:** SCR Lab Catalog v0.1, Family H (entries 47–56)
**Cites:** SCR-F v0.2 §11, §29, §30, §36.2, §36.6, §37, §41–43; F-17
**Fit reviews (§30):** none performed for any entry in this family.

> **Stub — no Lab paper here is written or adopted.** This file exists so downstream documents have a stable citation target (§36.2) and so the tree's shape is reviewable before the papers land. A model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, and refuse to answer a DEC-owned question locally (§36.6).

---

## Entries

| # | Lab | Standing | Production report |
| :-- | :--- | :--- | :--- |
| 47 | Lateral Movement | ungraded | `family-h-report-v1.md` |
| 48 | Identity and Privilege | ungraded | `family-h-report-v1.md` |
| 49 | Prompt Injection | ungraded | `family-h-report-v1.md` |
| 50 | Agent Memory | ungraded | `family-h-report-v1.md` |
| 51 | Sensitive Data Diffusion | ungraded | `family-h-report-v1.md` |
| 52 | Ransomware Spread | ungraded | `family-h-report-v1.md` |
| 53 | Patch Propagation | ungraded | `family-h-report-v1.md` |
| 54 | Worm and Botnet | ungraded | `family-h-report-v1.md` |
| 55 | Segmentation and Containment | ungraded | `family-h-report-v1.md` |
| 56 | Software Supply Chain | ungraded | `family-h-report-v1.md` |

**SCR-F §37 correspondence:** completes the illustrative `security/` entry.

All ten entries are covered by `family-h-report-v1.md`, with **entries 47–50 written without critique coverage** (`SCR_Labs_41-50_Critique` does not exist).

**Three structural findings shape this family.** It is **one World with several mechanisms**, not ten Labs — 47, 48, 52, 54, and 55 share an enterprise-security World and differ by mechanism package and Study. Three mechanisms must not be blended: *autonomous propagation* (worms), *directed adaptive action* (lateral movement), and *coordinated deployment* (ransomware, patch scheduling) — a large share of bad "cyber contagion" modelling comes from treating all three as epidemics. And the family's **first engineering deliverable is probably not a Lab** but a versioned **synthetic enterprise reference World** with known ground truth and deliberately seeded traps.

**This family is ungraded as a whole**, and the catalog records an explicit expectation that these entries may grade weak if forced onto a lattice (Catalog §0, gap 1). If they do, that is a finding about SCR's boundary and should be published as one — not buried. It is also the family most likely to be over-claimed commercially, and **F-20 applies throughout**: hostile conditions are explicit experimental capabilities, and studying attacker behaviour never justifies a more permissive execution surface for generated code (§18.4, DEC-16).

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
