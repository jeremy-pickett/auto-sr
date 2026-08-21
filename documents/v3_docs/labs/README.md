# Labs

**Document class:** Level 5 — Lab Papers (root index) · **Status:** draft
**Path:** `labs/`
**Implements:** SCR-F v0.2 §37 (`labs/` subtree)
**Cites:** SCR-F v0.2 §11, §29, §30, §36.2, §36.6, §37, §41–43; F-17
**Fit reviews (§30):** none performed for any of the sixty candidates.

> This directory is the `labs/` subtree of SCR-F v0.2 §37. It holds **production Lab papers**, organized by domain family. It does not hold drafting material.

---

## Families

SCR-F §37 lists `security/`, `weather/`, `ecology/`, `wildfire/`, `materials/` and then `...`. The nine families below complete that list; five correspond to §37's named entries and four fall under its trailing ellipsis.

| Folder | Family | Catalog entries | §37 name |
| :--- | :--- | :--- | :--- |
| `a-fire-land-and-surface/` | A — Fire, land, and surface processes | 1–8 | `wildfire/` |
| `b-ice-water-and-atmosphere/` | B — Ice, water, and atmosphere | 9–13 | `weather/` |
| `c-ecology/` | C — Ecology | 14–19 | `ecology/` |
| `d-cells-tissue-and-disease/` | D — Cells, tissue, and disease | 20–27 | — |
| `e-materials/` | E — Materials | 28–35 | `materials/` |
| `f-movement-and-crowds/` | F — Movement and crowds | 36–40 | — |
| `g-cities-and-infrastructure/` | G — Cities and infrastructure | 41–46 | — |
| `h-information-security/` | H — Information security | 47–56 | `security/` |
| `i-boundary-markers/` | I — Weak fits and boundary markers | 57–60 | — |

Letter prefixes are for stable ordering and traceability to the catalog. They carry no precedence.

## What lives where

| Path | Holds | Status |
| :--- | :--- | :--- |
| `scr-lab-catalog-v0.1.md` | The sixty candidates, named and briefly described | Draft, cited by every family |
| `ingestion-inventory.md` | Every dataset the sixty Labs name, sorted into the four ingestion pipelines | Draft — the finding is that **~two-thirds are comparison targets that never enter a Run** |
| `<family>/` | Production Lab papers and family reports | Being written |
| `short-lab-definitions/` | **Historical reference.** The sixty first-pass Lab Knowledge Briefs | Frozen — see below |

### `short-lab-definitions/` is historical reference

The sixty first-pass briefs stay where they are and are not maintained. They were drafting material: unverified citations, single-axis assessments, no fit review, and at least one error class since corrected across the board (sensitivity was conflated with computational irreducibility in four of the first ten).

**Nothing in this tree should cite them as evidence.** Cite the production report that supersedes them. They are kept because SCR-F §7 and §10 apply to documents as much as to Runs: the earlier reading stays readable, and what changed between versions is itself informative.

## Two tensions flagged, not resolved

Per §36.6, a document writing into this tree flags ambiguity rather than smoothing it over.

**1. The catalog says families are not a package structure.** `scr-lab-catalog-v0.1.md` §0 states plainly: *"Families are an organizing convenience. They are not a proposed package structure and they are not Layout assignments."* This directory has now made them one. That is a defensible reading of SCR-F §37 — which does organize `labs/` by domain — but it contradicts the catalog's own caveat, and the contradiction should be resolved by amendment rather than by silence. Two specific risks it creates:

- **Families are not Layout assignments.** SCR-F §15's four Layout families cut *across* these folders. Karst (Family A) wants a Network World; Lateral Movement (Family H) wants Network or Identity. A reader must not infer Layout from folder.
- **Mechanism families cut across too.** The same diffusion-limited fingering instability appears in entries 10, 23, 24, 25, 29, and 34 — four folders, four disciplines, one mechanism. Cross-family mechanism retrieval is the Corpus's most distinctive capability, and a folder tree is exactly the structure that hides it.

**2. Production reports are not yet family-aligned.** `../SCR_Labs_01-10_Knowledge_Report_v1.md` covers entries 1–10, which spans Family A entirely and Family B partially. Whether production reports are batched by family or by arbitrary tens is an open question, and it determines both where that report lives and how the remaining fifty are written. The family README files link to it as *pending* where it does not yet reach.

## How Lab papers report standing

Conventions for this subtree. The conceptual framework these rest on is `../00-start-here/irreducibility-and-what-cellular-means.md`; the fit review procedure is `../01-core/labs.md`.

### Four axes, not one grade

A single word compresses too much. Every Lab paper reports these separately:

- **Mechanism fit** — does the local-state abstraction make sense for this domain?
- **Validation class** — *direct experimental* / *direct observational* / *indirect statistical* / *qualitative only*. These must never look equivalent in Search.
- **Rediscovery risk** — low / medium / high. Is the canonical local-rule model already known?
- **Practical need** — would anyone use the resulting mechanism catalogue?

None of these is a fit grade. Fit is decided by review (§30), not by a paper about itself.

### Lab roles

Not every Lab justifies itself with new domain science, and pretending otherwise is less credible than declaring the role:

- **Calibration anchor** — good ground truth, used partly to prove SCR's evidence chain works at all.
- **Rediscovery benchmark** — a canonical local-rule model exists; SCR should be able to recover something like it. This is a legitimate role, not a consolation.
- **Architecture stress test** — forces the platform to confront a capability it lacks.
- **Mechanism-supply candidate** — a specific under-explored interaction problem.
- **Integrity demonstrator** — exercises the platform's honesty machinery.

**A Lab can be commercially weak and architecturally essential.**

### Visualization credibility class

A visual can be accurate as a rendering and misleading as a product claim (§12, §26). Every Lab paper declares one:

- **Class 1 — mistakable for an operational forecast.** Strictest labelling; output must never appear without Study context.
- **Class 2 — mistakable for scientific significance it does not have.** *Beauty is the failure mode.*
- **Class 3 — low hazard.**

### Falsifiable question

Every Lab paper states, in one sentence near the top, the strongest question it could ask that could come back negative. "Simulate X" is not one.

## Decisions this subtree must not resolve locally

- **DEC-1** mechanism composition · **DEC-3** temporal semantics · **DEC-8** World storage · **DEC-15** Lab governance · **DEC-16** security isolation · **DEC-20** external calibration.

The fit review procedure itself is owned by `../01-core/labs.md`, not by any Lab paper.

## Non-claims

Presence in the catalog is not fit (§30). Bracketed standings are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived. No Lab in this subtree forecasts, predicts, or assesses anything in any real system (§41, §43).
