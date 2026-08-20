# Visualization

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/visualization.md`
**Cites:** SCR-F v0.2 §12, §24, §24.1, §24.2, §25, §25.1–§25.6, §26, §27, §28, §38.6, §38.7; F-18, F-19

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- **The normative visualization truth contract.** §26 states explicitly that its table is an exemplar and that the complete, versioned, testable version belongs here. Extending §26's illustration in place is a mistake this document exists to prevent.
- Time navigation as a foundational instrument: scrubbing, stepping, play/pause, jump-to-event, two-point comparison, Reader and Study marks, stable time permalinks (§24.1).
- Styles as lenses over one immutable history, with the architectural test made concrete — can this style be applied later to an old Run without re-running it, and if not, what new information or execution is required (§24.2).
- The computational-versus-visual distinction carried forward: a quiet picture does not mean the computational state stopped evolving (§38.6).
- **Influence View context, not censorship** (§25.3): any specific divergence is rendered against the Run's ambient sensitivity, and uniform sensitivity is reported as a finding rather than suppressed. Applies identically to generated video (§28).
- Reporting (§27) and the automated short-form video stretch goal (§28), under the same evidence contract as the interactive product — narration, pacing, and camera may be generated; claims and depicted behavior may not.

## Decisions this document must not resolve locally

- **DEC-13 — Visualization scale.** *Open.* What evidence formats advanced 3D Views require so they do not need entire Runs replayed server-side.
- **DEC-14 — Video provenance.** *Open.* What provenance attaches to generated narration and edits so a short video can never outrun the evidence.

## Status of the §25 Views

3D World View, Time View, Influence View, Study View, Behavior Map, and Corpus View are **roadmap candidates, not commitments** (§25). This document may accept, reshape, or reject each. It may not cite them as already promised.

## Demonstrated versus specified

§24 distinguishes what 2.x demonstrably does from what the 2.2 visualization uplift specifies. Preserve that line: build status is a repository fact, not a claim this tree asserts.
