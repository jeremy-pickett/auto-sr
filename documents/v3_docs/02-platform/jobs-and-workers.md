# Jobs and workers

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/jobs-and-workers.md`
**Identifier namespace:** `JOBS-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §33, §39 · `../01-core/runs.md`, `../01-core/studies.md`, `../01-core/generation.md`, `../01-core/reactor.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> This document owns how work gets scheduled and executed at scale. Its one non-negotiable: **scheduling is operational, never experimental** — nothing about when or where a Run executes may change what the Run does.

---

## 1. The units of work

**JOBS-1.** The platform schedules three kinds of work: Generation pipelines (propose through deliver), Runs (admission through completion), and Studies (which fan out into many Runs by design). Each is trackable individually from request to completion or recorded failure.

**JOBS-2.** The earlier system ran everything inside one synchronous streamed request, with no queue and one host — recorded as evidence of what worked at toy scale, and listed in §39 as inheritance, not requirement. The planned scale-up assumes queued work on multiple workers; every conceptual contract must survive that change unbothered (§33).

---

## 2. Infrastructure failure is not experimental failure

The failure taxonomy distinguishes seven ways to have no result, and the reason is the information (`../01-core/runs.md` §1). Infrastructure can silently corrupt that taxonomy, and this section exists to prevent it.

**JOBS-3.** An infrastructure retry is not a Run failure. A worker crash, a lost connection, a host reboot — where execution never validly began, the work is retried below the evidence layer and no failure record is minted for the experiment.

**JOBS-4.** The line is admission. Once the execution authority admits an Attempt and execution begins, the experiment exists as evidence-in-progress: a Run that dies with its worker is recorded as *Run failure* with its infrastructure cause, never silently re-run as though the first execution hadn't happened.

**JOBS-5.** One Attempt, one admission. Retry machinery may re-submit work that never reached admission; it never causes the same Attempt to be admitted twice. Two executions of the same declared experiment are two Runs, deliberately created, never an accident of the queue.

---

## 3. Scheduling never touches semantics

**JOBS-6.** Experimental ordering belongs to the execution authority alone (REACTOR-1). Worker count, queue order, host assignment, and parallelism are invisible to every Run's recorded history: the same admitted experiment produces the same history whether it ran first or last, alone or beside a hundred others.

**JOBS-7.** Concurrent Runs share nothing mutable. Isolation between simultaneously executing experiments is the boundary's obligation (SAFE-4); the scheduler's obligation is never to create sharing the boundary would have to catch.

---

## 4. Study fan-out

**JOBS-8.** A Study's Runs are scheduled as a tracked family: the Study knows which of its Runs completed, failed, or never ran, at every moment.

**JOBS-9.** A partially completed Study reports honestly: which Runs are missing and why, in the finding itself (STUDY-8's discipline). Missing Runs are never silently dropped from the comparison — a Study of twenty that quietly reports twelve has fabricated a sample.

**JOBS-10.** Fan-out is bounded before it starts: a Study declares its Run count at confirmation time (STUDY-16), and the scheduler refuses open-ended fan-out rather than discovering it in production.

---

## 5. The unregistered decision this document keeps hitting

Nothing in the platform owns **cost**. Generation calls a paid model; repair multiplies calls; Study fan-out multiplies Runs; the planned scale-up multiplies everything. Budgets exist per-experiment (SAFE-8) but nothing owns the economics of the whole: who may spend how much on what, and what happens when the answer is no.

Flagged here and in the Decision Registry's candidates list; registering it (DEC-25) is an amendment to SCR-F §40, which is the owner's call. Until then, this document states the mechanical minimum:

**JOBS-11.** Every unit of work records what it consumed — model calls, compute time, storage written — in operational telemetry, so that when the cost question is decided there is data to decide it against.
