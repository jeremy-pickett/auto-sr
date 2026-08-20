# Corpus

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/corpus.md`
**Identifier namespace:** `CORPUS-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §7, §10, §22, §22.1, §31, §32, §32.1, §38.8; F-15, F-21 · DEC-6, DEC-11
**Depends on:** `runs.md` (§2, §3.1), `readers.md`, `generation.md`.

> The **Corpus** is the durable body of evidence and meaning. It is not the database. A database is a choice; the Corpus is what the choice is protecting.

---

## 1. What the Corpus owns

**CORPUS-1.** The Corpus holds and links: requests; proposals; mechanisms and their revisions; Worlds and Starting States; Attempts and Runs with their Run Contracts; Study definitions and findings; Reader results and versions; failures of every class; repairs; machine identity and settings; Reactor versions; Lab versions; human corrections; annotations; and the relationships among related mechanisms.

**CORPUS-2.** The individual mechanism is not the asset. The asset is the accumulated set of links between intent, implementation, execution, measurement, failure, ancestry, and correction. A library of mechanisms with no links is a directory.

---

## 2. What the Corpus refuses

| Refused | Owner |
|---|---|
| Altering any recorded history | nobody — history is immutable |
| Deciding what a record means | Reader, Study, a person |
| Operational telemetry | Platform Services |
| Discarding a failure | nobody |

**CORPUS-3.** Operational telemetry — process health, queue depth, request rates, error counts — is not Corpus data, and does not become Corpus data by being stored nearby. The distinction is conceptual and survives any storage arrangement.

**CORPUS-4.** All seven failure classes are retained permanently, with their reasons and their stage. A Corpus holding only successes produces a map of explored ground that is wrong in a flattering direction, and cannot answer how often anything works.

---

## 3. Provenance

**CORPUS-5.** Every result traces to the inputs and software that produced it: the request or objective; the fully rendered machine inputs; machine identity and settings; raw outputs where they bear on the result; the proposal; the implementation and its revision; repair history including each semantic account; validation outcomes; the World and Starting State; the Reactor version; the Run Contract; Reader identities and versions; Study definitions; human corrections; and the versions of any report or view that made an interpretive claim.

**CORPUS-6.** Provenance is recorded as a graph of things, the activities that produced them, and who or what was responsible. This is a solved modelling problem with a published standard, and the platform's identifiers should map onto it rather than inventing a private vocabulary that no external tool can read.[^prov]

**CORPUS-7.** The record distinguishes *the machine's output varies* from *we failed to record what we asked it* (GEN-17).

---

## 4. Integrity lives in the record

**CORPUS-8.** Integrity is protected by cryptography **over the record**: content addressing, hash chains over recorded histories, and signed export bundles. Verifying part of a large record against a single root value is long-established practice.[^merkle]

**CORPUS-9.** Nothing is ever embedded into experimental state to describe that state. No watermark, no statistical residue, no signature woven into Cell values.

CORPUS-9 is permanent and is not a matter of technique. In a platform whose premise is sensitive dependence on state, altering state to carry provenance corrupts the experiment in order to sign it, and the signature is then made of altered evidence. No such embedding both survives arbitrary later processing and constitutes proof; those are different and largely incompatible goals. Where a downstream process strips record-level provenance, the honest answer is that provenance was stripped.

> **State data is evidence. Evidence is never modified to describe itself.**

---

## 5. Corrections

**CORPUS-10.** A human correction is a first-class record holding: the original machine proposal or interpretation, the correction, the reason where given, what changed as a result, who supplied it, and which later Runs, Studies, or Reader results depend on it.

**CORPUS-11.** A correction never rewrites what it corrects. Disagreement stays inspectable.

A record showing only the final agreed answer has discarded what a later reader most needs — that the question was once open, who closed it, and on what grounds.

---

## 6. The earlier library

**CORPUS-12.** The earlier system's library — its mechanisms, Runs, failures, and provenance — is carried forward as **founding evidence**. It is not archived, not orphaned, and not a separate lineage.

**CORPUS-13.** Migration never rewrites those histories. Whatever mapping is applied around them, the recorded evidence is immutable and stays so.

**CORPUS-14.** Where an earlier derived result is recomputed under a current Reader, both are kept and both are attributed to their versions (READER-4). Where it is not recomputed, it is preserved and labelled as a historical reading.

DEC-6 owns identifier mapping and cross-version comparability. CORPUS-12 to CORPUS-14 constrain any answer.

---

## 7. Families of mechanisms

**CORPUS-15.** Where the Corpus groups mechanisms it judges to be the same, the grouping states the basis on which it was made and remains inspectable at the level of the individual mechanism.

Grouping near-identical mechanisms is what makes a large Corpus navigable, and it is also how a meaningful difference disappears. Two mechanisms that look alike and behave differently are exactly the case worth finding, and exactly the case a family view hides. DEC-11 owns this.

---

## 8. What the Corpus requires

- **From every component:** version identity precise enough to be linked rather than guessed.
- **From the Run:** the Run Contract, which is what makes an old record self-describing (RUN-8).

## 9. What the Corpus produces

Durable links, and the ability to answer a question nobody had when the evidence was recorded. That last is the whole point of keeping it.

---

## 10. Open decisions

- **DEC-6 — Migration of the earlier library.** Partially decided; constrained by CORPUS-12 to CORPUS-14.
- **DEC-11 — Corpus identity.** Constrained by CORPUS-15.
- **DEC-2 — Replay.** Determines how much must be kept per Run.
- **Unregistered — ownership of evidence.** The Corpus is described as one durable body with no notion of whose evidence it is. Flagged in `../02-platform/identity-and-access.md`.

---

## Sources

[^prov]: *PROV-DM: The PROV Data Model*, W3C Recommendation, 30 April 2013. Models provenance as entities, the activities that generated them, and the agents responsible.
[^merkle]: Ralph C. Merkle, "A Digital Signature Based on a Conventional Encryption Function," in *Advances in Cryptology — CRYPTO '87*, Lecture Notes in Computer Science 293 (Springer, 1988): 369–378.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
