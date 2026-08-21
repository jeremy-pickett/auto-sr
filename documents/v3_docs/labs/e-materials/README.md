# Family E — Materials

**Document class:** Level 5 — Lab Papers (family index) · **Status:** draft
**Path:** `labs/e-materials/`
**Catalog:** SCR Lab Catalog v0.1, Family E (entries 28–35)
**Cites:** SCR-F v0.2 §11, §29, §30, §36.2, §36.6, §37, §41–43; F-17
**Fit reviews (§30):** none performed for any entry in this family.

> **Stub — no Lab paper here is written or adopted.** This file exists so downstream documents have a stable citation target (§36.2) and so the tree's shape is reviewable before the papers land. A model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, and refuse to answer a DEC-owned question locally (§36.6).

---

## Entries

| # | Lab | Standing | Production report |
| :-- | :--- | :--- | :--- |
| 28 | Corrosion Pitting | **[plausible]** | `family-e-report-v1.md` |
| 29 | Dendritic Solidification | ungraded | `family-e-report-v1.md` |
| 30 | Grain Growth | ungraded | `family-e-report-v1.md` |
| 31 | Fracture Propagation | ungraded | `family-e-report-v1.md` |
| 32 | Sintering | ungraded | `family-e-report-v1.md` |
| 33 | Thin-Film Growth | ungraded | `family-e-report-v1.md` |
| 34 | Battery Dendrite | ungraded | `family-e-report-v1.md` |
| 35 | Catalytic Surface Reaction | ungraded | `family-e-report-v1.md` |

**SCR-F §37 correspondence:** completes the illustrative `materials/` entry. All eight entries are covered by `family-e-report-v1.md`.

**This family contains both the catalog's best calibration Lab and its clearest rejection**, and both are valuable for the same reason. Entry 30 has an **exact** relation — von Neumann–Mullins, generalized to three dimensions by MacPherson and Srolovitz — giving SCR a hard answer it is not allowed to negotiate with; it is the only source of **law-level correctness** in the catalog and its research weakness is irrelevant to that role. Entry 31 should probably **fail mechanism fit**: the domain-defining driver is a whole-body elasticity solve, and a neighbour-transfer surrogate produces plausible avalanche exponents alongside physically wrong crack paths. Rejected does not mean deleted — it means the Lab established a boundary.

Entry 33 is where **observable-equivalence identity** should be formalized: universality means many mechanisms collapse to the same measured exponents, which directly challenges the premise that different mechanisms are worth cataloguing separately.

**Benchmark leakage is acute here.** Potts grain growth, DLA/Eden, classical dendrites, and the ZGB model are almost certainly in foundation-model training data. Calibration Studies in this family require **blinded benchmark modes** recording what Generation was allowed to know.

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
