# Frontend

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/frontend.md`
**Identifier namespace:** `FRONT-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §24, §33, §39 · DEC-10 · `../01-core/visualization.md`, `../01-core/readers.md`, `02-platform/transport.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> The frontend delivers the product; it does not define what the product may show. The truth rules live in `../01-core/visualization.md` and bind every screen this document ships.

---

## 1. Division of labour

**FRONT-1.** Visualization (Level 3, core) owns *what may be shown and on what evidence* — the truth contract, the lens rules, the divergence-context requirement. This document owns *delivery*: the application shell, navigation, performance, and the surfaces where those rules become pixels. A conflict between a screen and the truth contract is a defect in the screen.

**FRONT-2.** The earlier system's shell — its framework, routing, and component structure — is inheritance, not requirement (§39). Level 3 may name its choices when made; the requirement is what survives them.

---

## 2. Time is the primary control

**FRONT-3.** The Run player implements the full navigation set as first-class interactions: scrub, step both directions, play/pause, jump-to-event, two-moment comparison, finding marks, and stable references to exact moments (VIS-14). The slider is the instrument a person searches a Run with — it gets the engineering attention an instrument deserves, within transport's immediacy budget (TRANS-1).

**FRONT-4.** No screen implies that a quiet picture is a settled system (VIS-10). Where the visible layer has gone still and recorded state is still evolving, the interface says so.

---

## 3. Attribution is a surface, not a tooltip

**FRONT-5.** Every measurement on every screen names its Reader and version; every important claim can be walked back to its evidence without leaving the interface (READER-13, READER-14). How uncertainty and coverage are presented well is DEC-10's open design question; *that* they are co-presented with the result is not open, and no screen ships without it.

**FRONT-6.** Machine interpretation — repair accounts, generated summaries — is visibly labelled as interpretation, distinct from evidence and from measurements, on the surface where it appears (GEN-14, READER-9).

---

## 4. Honest degradation

**FRONT-7.** A view that cannot run on the viewer's hardware, or that needs data the record lacks, states what it needs (VIS-9) — it never silently substitutes a lesser rendering presented as the real one (TRANS-4's rule, at the screen).

**FRONT-8.** The public-reader assumption applies to screens: labels, empty states, and error text follow the expert-reader standard (`../00-start-here/language-rules.md`) — no platform vocabulary required to understand what a screen is saying, no talking down to the professional reading it.
