# SCR 3.x documentation tree

**Status:** draft · **Date:** 2026-08-20, revised 2026-08-21
**Implements:** SCR-F v0.2 §37 (initial documentation tree), §36 (authority, lifecycle, citation)

This directory is the `docs/` root described in SCR-F v0.2 §37. It began (2026-08-20) as a
scaffold of stubs — stable citation targets carrying what each document owes and which DEC records
it must not resolve locally. As of 2026-08-21, **every numbered directory is written**: Level 1
foundations in `00-start-here/` — six documents, including SCR-F v3.x itself and the
irreducibility paper — production requirements across `01-core/` (twelve documents; the five
core-contract seam passes preserved as `*.seams.md`), `02-platform/` (eight), and `03-quality/`
(six, the synthetic-data suite having joined the original five), with the Decision Registry in
`04-decisions/` holding all records in the plain-question format. Everything remains **draft** — adoption is a human act (§36.3) and none has
happened yet.

The discipline the scaffold established still governs every future edit. Roughly two hundred
documents are expected in this tree, most of them machine-written, and §36 makes the failure mode
explicit: a human-written tree drifts at the leaves, a model-written tree drifts at the **root**,
silently, one plausibly-interpreted ambiguity at a time. Stable identifiers and the Decision
Registry exist so a writer arriving at any file already knows which questions are not theirs to
answer.

## Layout

```
documents/v3_docs/
├── 00-start-here/     Level 1 — Foundations, including SCR-F v3.x (draft)
├── 01-core/           the twelve components (+ preserved *.seams.md passes)
├── 02-platform/       Platform Services (§33)
├── 03-quality/        testing, repeatability, accuracy, references, human review,
│                      synthetic data
├── 04-decisions/      DEC-1 … DEC-24 (25–27 reserved), indexed by §40
├── labs/              Level 5 — the sixty-candidate catalog, nine family folders,
│                      Lab papers, the ingestion inventory (see labs/README.md)
├── surveys/           idiom surveys and other raw material for future requirements
├── critiques/         external review, retained as evidence
├── outstanding.md     the living list of what remains after the documentation phase
└── relics/            prior drafts and source material; not part of the tree
```

`labs/` is an actively written lane with its own conventions — see `labs/README.md`. `relics/`
holds prior drafts and is not part of the tree.

## Document classes (§36.1)

| Level | Class | Where |
|---|---|---|
| 1 | Foundations | `00-start-here/` |
| 2 | Architecture Decisions | `04-decisions/` |
| 3 | Requirements | `01-core/`, `02-platform/`, `03-quality/` |
| 4 | Technical Deep Dives | not yet created — implementation-level, written as built |
| 5 | Lab Papers | `labs/` |
| 6 | Operations and User Documentation | not yet created |

**The Level 3 assignment is provisional.** v0.2's §37 gives the tree without assigning levels to
it; reading `01-core/`, `02-platform/`, and `03-quality/` as Level 3 Requirements began as this
scaffold's proposal. The SCR-F v3.x draft records the assignment as built (§36.1, §37); it becomes
SCR-F's position when v3.x is adopted. Levels 4 and 6 have no
directory in §37; they are listed above so their absence is visible rather than forgotten.

## Citation (§36.2)

- Foundations: `SCR-F v0.2 §19` — v0.2 remains the governing text until v3.x is adopted, and
  v0.2 citations stay valid permanently as historical pins. Condensed rules `F-1` … `F-22`; the
  v3.x draft adds `F-23`.
- Decisions: `DEC-1` … `DEC-24`; `DEC-25` … `DEC-27` are reserved (registration lands with
  adoption of SCR-F v3.x).
- Requirements documents define their own permanent identifier namespaces, following the 2.x
  `REQ-` practice: identifiers are never reused, retirements are recorded rather than silently
  dropped, and rationale travels with the requirement. A document writing into a shared namespace
  declares its reserved identifier block.

Documents cite by identifier, never by prose paraphrase alone.

## Status lifecycle (§36.3)

Every document carries exactly one of: **draft** · **in review** · **adopted** · **superseded** ·
**withdrawn**. Model-written documents enter as drafts and cannot self-promote. **Adoption is a
human act.** DEC records use their own status vocabulary — see `04-decisions/README.md`.

## Precedence (§36.4)

1. Conceptual meaning — what a component is, what it owns: **Foundations** outranks everything, and
   a newer adopted Foundations version outranks an older one.
2. Decided questions: the governing **DEC** record outranks any document's local phrasing,
   including SCR-F's.
3. Testable contract details: the owning **Requirements** document outranks Foundations. If honoring
   a requirement would violate a foundational principle, that is not a local judgment call — it
   triggers amendment (§36.5).
4. A conflict between adopted documents is a defect in the tree: recorded and resolved by amendment,
   never by a downstream writer silently choosing a side.

## What a document written here owes (§36.6)

Cite the specific SCR-F sections and F-identifiers it depends on. Flag ambiguity rather than
resolve it. Refuse to answer a DEC-owned question locally. Keep Lab vocabulary out of Level 1–4
core documents — §21 is the worked example of how that leak happens, and the §36.6 obligation
exists because a model will otherwise do the helpful thing, smooth over the ambiguity, and leave
the tree holding an undecided decision as settled fact.

## Known state

- **SCR-F v3.x (draft) lives in this tree** at `00-start-here/foundations-and-platform-architecture.md`
  (moved 2026-08-21, replacing the former pointer; version label corrected from v0.3 per the
  standing rule in `CLAUDE.md`). **v0.2 remains the governing Foundations text** — still at
  `../SCR_Foundations_and_Platform_Architecture_v0_2.md`, status *in review* — until v3.x is
  adopted. The five recorded disagreements between them are indexed in `outstanding.md`.
- **Nothing is adopted.** Every document here is draft; adoption is a human act (§36.3), per
  document, by the owner.
- **Three unregistered candidate decisions** are flagged in the documents and listed in
  `04-decisions/README.md` — exploration strategy, cost and budget, and ownership of evidence.
- **DEC-2 is decided** (2026-08-21; replay promises), **DEC-16 is narrowed** (obligations are
  requirements in `02-platform/execution-safety.md`; the mechanism waits for a real deployment),
  and **DEC-18 is substantially narrowed** (only the stale-intent catch-up procedure remains).
- **After documentation: real data, per Lab.** These documents are expected to be stressed by it;
  amendment with the evidence attached is the intended response (§36.5), not a sign of failure.
