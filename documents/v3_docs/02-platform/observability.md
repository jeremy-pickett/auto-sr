# Observability

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/observability.md`
**Identifier namespace:** `OBS-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §22, §33 · `../01-core/corpus.md`, `02-platform/execution-safety.md`, `02-platform/jobs-and-workers.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> Operators need to see what the platform is doing. Scientists need the record of what experiments did. This document exists to keep those two kinds of seeing from contaminating each other.

---

## 1. The boundary

**OBS-1.** Operational telemetry — process health, queue depth, request rates, error counts, model-call outcomes, resource consumption (JOBS-11) — is not evidence and never becomes evidence by being stored nearby (CORPUS-3). The distinction is conceptual and survives any storage arrangement (STORE-1).

**OBS-2.** Telemetry is disposable by design: retention policies, sampling, and deletion apply to it freely and never touch evidence. If deleting a record would damage the scientific history, it was never telemetry, and its being in the telemetry store is the defect.

**OBS-3.** The crossing rule is the one already set at the boundary (SAFE-10), generalised: **an operational event that affected an experiment's outcome is an execution fact in that Run's record; one that did not is telemetry.** A worker crash that killed a Run is in the Run's permanent record as its failure cause; a worker crash that killed nothing is a graph on an operator's screen.

---

## 2. Operator surfaces

**OBS-4.** An operator can see, live: pipeline progress per unit of work, queue depth and worker health, containment events, failure rates by class, and consumption (calls, compute, storage). None of it requires touching evidence to render.

**OBS-5.** Operator views are visibly not evidence views. A dashboard is never mistakable for a finding — different surface, different framing, and no operator number is exportable as though it were a measurement of an experiment.

**OBS-6.** Telemetry about the generation pipeline — timings, failure rates, repair frequency — may be *aggregated* into durable quality statistics, and those aggregates are then interpretation about the platform, attributed and versioned like any interpretation, never retroactive evidence about any individual Run.

---

## 3. What operators may not see by accident

**OBS-7.** Telemetry never carries evidence content as payload: not recorded state, not mechanism source, not rendered prompts. It references records by identifier; the records live where evidence lives, behind whatever access the evidence requires (IDENT-4's future answer applies there, not here).

**OBS-8.** The earlier system's live process map and session tracking are recorded as evidence that lightweight operational visibility is worth having from day one — and as inheritance in their details (§39). What is required is OBS-1 through OBS-7, under any implementation.
