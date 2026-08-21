# API

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/api.md`
**Identifier namespace:** `API-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §33, §39 · `../01-core/runs.md`, `../01-core/corpus.md`, `../01-core/readers.md`, `../01-core/generation.md`, `../01-core/search.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> The API is where every promise in the core documents either gets enforced or quietly dies. Its job is to be the edge that makes the promises structural.

---

## 1. The surface

**API-1.** The service surface covers: mechanisms and their revisions, Attempts and Runs, Studies, Reader results, Search, the modifier and Lab catalogs, corrections, and exports. Each is served with its provenance attached, never as a bare object.

**API-2.** The earlier system's route structure is inheritance, not requirement (§39). What is required is the obligations below, which survive any restructuring.

---

## 2. Immutability is enforced at the edge

**API-3.** No endpoint mutates recorded history. There is no update, no delete, and no "fix" operation on any Attempt, Run, Study result, or Reader result — structurally absent, not permission-gated. An edge that merely forbids mutation invites the day someone with enough permissions is very sure of themselves.

**API-4.** The mutations that legitimately exist all *attach*: corrections (CORPUS-10, CORPUS-11), user signals such as flags and behaviour overrides, annotations. Each is a new record with author and reason, alongside what it concerns.

**API-5.** User signals never enter generation context (GEN-22). The edge keeps the two flows separate: what a person marked interesting is served to people, and is structurally absent from what the generator sees.

---

## 3. Long-running work

**API-6.** Work that takes real time — Generation above all — streams its progress to the caller from the request that started it. Progress events are operational telemetry: they inform the watcher, they are not the record. The permanent outcome lands in the Corpus regardless of whether anyone watched.

**API-7.** A dropped connection never orphans work. Whether the work is request-scoped or queued (`jobs-and-workers.md`), its outcome and provenance are recorded identically — the watcher was a convenience, not a dependency.

---

## 4. Errors carry the taxonomy

**API-8.** The edge reports failures in the platform's own failure classes — proposal failure, implementation failure, admission refusal with its mismatch class (REACTOR-6), Run failure, behaviour miss, Reader uncertainty, Study failure — never a generic error where a specific one exists. "Invalid" is not a result, at the edge or anywhere.

**API-9.** An admission refusal returns the mismatch record itself: what was requested, what was offered, where they disagreed. The caller learns what to fix, and the refusal is retained as evidence either way (RUN-4).

---

## 5. Everything served carries its authority

**API-10.** Every measurement served names the Reader and version that produced it; every claim served is traceable to its evidence (READER-13, READER-14). The API never strips attribution to make a payload smaller — a compact lie is still a lie.

**API-11.** Exports are signed bundles (STORE-11) carrying the mechanism or finding *with* its provenance, confirmation status, and non-claims (ACCURACY-14). What the bundle contains beyond that is DEC-20's open question; that it is never a bare mechanism is settled.
