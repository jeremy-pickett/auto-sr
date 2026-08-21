# Storage

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/storage.md`
**Identifier namespace:** `STORE-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §22, §32.1, §33, §39 · DEC-2 (decided), DEC-6, DEC-8, DEC-13 · `../01-core/corpus.md`, `../01-core/runs.md`, `../01-core/worlds.md`, `../03-quality/repeatability.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally. Every contract cited here must remain meaningful after this document's answers change.

> Storage keeps two very different things: **evidence**, which must outlive the software that wrote it, and **operational telemetry**, which is disposable by design. Everything in this document follows from refusing to confuse the two.

---

## 1. Two stores in concept, whatever the arrangement

**STORE-1.** The Corpus — evidence and meaning — and operational telemetry are separate in concept, permanently. They may share infrastructure; they never share rules. Deleting telemetry never touches evidence. Retention policies apply to telemetry only (CORPUS-3, `observability.md`).

**STORE-2.** Evidence storage is designed to outlive its own implementation. Formats are versioned, self-describing enough that a record's meaning does not depend on the code that wrote it, and every migration preserves the original readable in history. A record whose interpretation requires today's software has a shelf life, and everything citing it inherits that shelf life.

**STORE-3.** Evidence is write-once. A completed Attempt or Run is never updated in place — corrections attach, readings attach, nothing overwrites (RUN-10, RUN-11). The storage layer enforces this rather than trusting callers to observe it.

---

## 2. What is stored per Run — under DEC-2, decided

DEC-2 is decided (2026-08-21): **reproduction under contract is the default promise; exact replay is reserved for Runs designated evidence-grade at run time.** Storage is where that decision becomes machinery.

**STORE-4.** Every Run stores: its Run Contract (RUN-6), its recorded history, its execution facts including the stopping fact, its cost record (RUN-19), and its replay promise (RUN-15).

**STORE-5.** A Run designated **evidence-grade** additionally has its full environment archived **at run time**: the implementation, the execution authority's build, and the dependency environment, sufficient for value-for-value replay. There is no retroactive path — an environment not archived when the Run executed can never be archived later, which is why designation is checked before execution starts, not after results look interesting.

**STORE-6.** The **equivalence standard** — the written definition of "close enough" for reproduction under contract (REPEAT-7) — is stored as a versioned record. Every reproduction claim cites the standard version it was made under.

**STORE-7.** A downgrade — an archived environment that is no longer available — is recorded against the Run, dated and attributed, and the Run's stated promise changes with it (RUN-16, REPEAT-4). Silent downgrades are the failure this requirement exists to prevent.

---

## 3. History encoding

**STORE-8.** Recorded history is stored as periodic full snapshots plus the changes between them, compressed. Values the platform can rebuild from the record are rebuilt on demand rather than stored at every step. This is carried forward as demonstrated practice from the earlier system — where it held up well — and remains revisable as long as STORE-2 and the reconstruction budget hold.

**STORE-9.** Reconstruction of any step completes fast enough that playback feels like navigation, not loading (`transport.md`). The snapshot interval is a tuning knob for exactly this budget and is recorded per Run.

**STORE-10.** History is encoded to be readable forward: a measurement invented years from now runs against old records without re-executing anything (RUN-21, READER-3). What the planned advanced views require of these encodings is DEC-13's question, and it must be answered **before** the large-scale format is frozen — after freezing, a missing format means re-running everything to draw a picture.

---

## 4. Integrity

**STORE-11.** Evidence integrity lives in cryptography over the record: content addressing, hash chains over recorded histories, and signed export bundles, so any part of a large record verifies against a single root value.[^merkle]

**STORE-12.** Nothing is ever embedded into experimental state to describe that state — no watermark, no signature woven into recorded values. The full argument is CORPUS-9's and is permanent: altering evidence to sign it corrupts the experiment in order to certify it.

---

## 5. Representation

**STORE-13.** Storage may not assume every participant has roughly the same number of connections unless the World family guarantees it (WORLD-15). Relational worlds have hubs — the account everything touches, the shared resource everyone reaches — and a fixed-slots layout sized for either the hubs or the typical participant fails, differently, both ways.

**STORE-14.** The working lean, recorded as engineering rather than decision (DEC-8): map-shaped worlds store as dense arrays, which the earlier system proved fast at toy scale; relationship-shaped worlds store each connection as its own entry — from, to, kind, bounded connection state — with indexes for fast neighbour lookup. Building against real Lab data will confirm or replace this.

**STORE-15.** The earlier system's single-file embedded database (SQLite, write-ahead mode) is recorded as evidence of what worked for one user at toy scale — listed in §39 as inheritance, not requirement. The planned scale-up of several orders of magnitude is the reconsideration trigger, and STORE-2 is what makes the move survivable whenever it comes.

---

## 6. The old library

**STORE-16.** Migration of the earlier library observes CORPUS-12 through CORPUS-14: carried forward as founding evidence, histories never rewritten, recomputed readings kept alongside historical ones with versions attached.

**STORE-17.** Migration runs **before** the scale-up (DEC-6's timing note): against tens of Runs it is an afternoon; against the post-scale-up library it is a project.

---

## Sources

[^merkle]: Ralph C. Merkle, "A Digital Signature Based on a Conventional Encryption Function," in *Advances in Cryptology — CRYPTO '87*, Lecture Notes in Computer Science 293 (Springer, 1988): 369–378.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
