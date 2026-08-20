# Decision Registry

**Document class:** Level 2 — Architecture Decisions (index) · **Status:** draft
**Indexes:** SCR-F v0.2 §40
**Cites:** SCR-F v0.2 §36.1, §36.2, §36.4, §36.5, §40; F-22

> **Why this directory exists.** SCR-F deliberately does not resolve every consequential choice. It
> insists that consequential choices be *named*, so they are decided in decision records with
> evidence — rather than answered accidentally during implementation, or worse, answered
> differently by different model-written documents that each thought the answer was obvious (§40).
>
> **Naming a fork is not deciding it.**

## Precedence

For a decided question, the governing DEC record outranks any document's local phrasing —
including SCR-F's own (§36.4.2). For conceptual meaning, Foundations still outranks everything.

## Status vocabulary

DEC records use their own status words, distinct from the §36.3 document lifecycle:

| Status | Meaning |
|---|---|
| **open** | Not decided. No document may resolve it locally (F-22). |
| **open; placement decided** | The ownership boundary is already foundational law; the mechanics are open. |
| **open; stance constrained** | Undecided, but SCR-F imposes a constraint any answer must satisfy. |
| **partially decided** | Part of the question is settled and cited; the rest is open. |
| **decided** | Resolved and adopted. Adoption is a human act (§36.3). |

Identifiers are permanent and never reused. A retired decision is marked retired, with the
amendment that retired it (§36.5).

## Foundational forks surfaced by v0.2 (§40.1)

| ID | Title | Status |
|---|---|---|
| [DEC-1](dec-001-mechanism-composition.md) | Mechanism composition | open — *the largest unnamed decision in v0.1* |
| [DEC-2](dec-002-replay-equivalence.md) | Replay equivalence | open |
| [DEC-3](dec-003-temporal-semantics.md) | Temporal semantics | open; placement decided |
| [DEC-4](dec-004-study-inference-discipline.md) | Study inference discipline | open; stance constrained |
| [DEC-5](dec-005-home-of-semantic-translation.md) | The home of semantic translation | open |
| [DEC-6](dec-006-2x-corpus-migration.md) | 2.x corpus migration | partially decided |

## Open questions carried forward from v0.1 (§40.2)

| ID | Title | Status |
|---|---|---|
| [DEC-7](dec-007-plugin-contract-surface.md) | Plugin contract surface | open |
| [DEC-8](dec-008-world-storage.md) | World storage | open |
| [DEC-9](dec-009-study-planner-autonomy.md) | Study planner autonomy | open |
| [DEC-10](dec-010-reader-trust-presentation.md) | Reader trust presentation | open |
| [DEC-11](dec-011-corpus-identity.md) | Corpus identity | open |
| [DEC-12](dec-012-search-similarity-separation.md) | Search similarity separation | open |
| [DEC-13](dec-013-visualization-scale.md) | Visualization scale | open |
| [DEC-14](dec-014-video-provenance.md) | Video provenance | open |
| [DEC-15](dec-015-lab-governance.md) | Lab governance | open |
| [DEC-16](dec-016-security-isolation.md) | Security isolation | open |
| [DEC-17](dec-017-model-independence.md) | Model independence | open |
| [DEC-18](dec-018-human-plugin-edits.md) | Human Plugin edits | open |
| [DEC-19](dec-019-live-work.md) | Live work | open |
| [DEC-20](dec-020-external-calibration.md) | External calibration | open |

**Status note.** §40.2 states no per-entry status for DEC-7 through DEC-20. *Open* is inferred from
the section heading — "open questions carried forward from v0.1" — and is recorded here as an
inference rather than a quotation.

## Candidates not yet registered

SCR-F §45.16 asks reviewers which consequential choice is still being made by accident. Three
appear in the stub tree as flagged concerns rather than registered records, because registering a
DEC is an amendment to §40 (§36.5) and not a local edit:

- **Exploration strategy** — nothing among the twelve components owns *deciding what to generate
  next*. Flagged in `../01-core/generation.md`.
- **Cost and budget** — no principle covers the economics of generation, repair, or Study fan-out,
  against a planned scale-up of several orders of magnitude (§22.1). Flagged in
  `../02-platform/jobs-and-workers.md`.
- **Ownership of evidence** — the Corpus is described as one durable body with no notion of whose
  evidence it is. Flagged in `../02-platform/identity-and-access.md`.

## Adding a record

New identifiers continue the sequence and are never reused. A record is added by amendment to
SCR-F §40, with the evidence attached (§36.5) — a downstream document that discovers a fork flags
it here; it does not decide it.
