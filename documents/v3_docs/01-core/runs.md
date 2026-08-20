# Run

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/runs.md`
**Identifier namespace:** `RUN-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §7, §10, §19, §24.1, §32.1, §38.5; F-10, F-21 · DEC-1, DEC-2, DEC-19, DEC-23
**Supersedes:** the first-pass seam document, preserved at `runs.seams.md`.
**Part of the core contract set:** `cells.md`, `worlds.md`, `plugins.md`, `reactor.md`. This document defines the Run Contract, which all five depend on.

> A **Run** is one exact execution, recorded permanently and never edited. It decides nothing. It is where every other component's identity meets, and it is the platform's unit of evidence.

---

## 1. Attempt and Run

The word *Run* has been doing two jobs — a planned execution and an admitted one — and the failure classes depend on telling them apart.

> **RUN-1.** An **Attempt** is the durable record of one intention to execute. Every Attempt is retained, admitted or not.
>
> **RUN-2.** A **Run** is an Attempt that passed admission and began executing. An Attempt refused at admission never becomes a Run; it retains a mismatch record instead (`reactor.md` §2).

**RUN-3.** The seven failure classes attach to Attempts, not to Runs, because two of them occur before execution begins.

This is a clarification of SCR-F §10, whose taxonomy is correct but is stated as though every failure happened to a Run. *Proposal failure* and *Reactor rejection* happen to Attempts that never became Runs. *Run failure* and *behaviour miss* happen to Runs. The distinction is filed as a proposed amendment to §10 rather than applied to it here.

**RUN-4.** No record is discarded because execution never began. A mechanism refused at the door is a finding about the mechanism, the World, or the contract — often the most informative kind, because it says precisely what was incompatible.

---

## 2. The Run Contract

This is the artifact the whole core set was missing. Five documents independently found the same chain — the World declares what exists, the Plugin declares what it uses, the Reactor enforces the match, the Run records the agreement — and found that nobody owned it. The chain does not need a new component. It needs a record.

> **RUN-5.** The **Run Contract** is the frozen, complete statement of what was agreed at admission. The Reactor produces it (`reactor.md` §2); the Run stores it permanently; nothing may alter it afterwards.

**RUN-6.** The Run Contract states at minimum:

- the World's execution identity: Cell kinds and schemas, Layout, connection classes, conditions, observation rules, external inputs, required capabilities;
- the Starting State, both the realized values and the recipe or seed that produced them (`worlds.md` §4);
- every participating Plugin, by revision, with its complete declarations — reads, writes, paths and reach, helpers, required derived values, scheduled effects;
- the composition policy, named and versioned, where more than one mechanism participates (`reactor.md` §7);
- the Reactor's version and the execution model in force;
- the derived values the Reactor undertook to supply;
- all budget limits;
- the replay promise offered (§5);
- the resolved match itself — what was requested, what was offered, and that they agreed.

**RUN-7.** The Run Contract is what determines future-relevant state, and the Reactor derives that set from it rather than from any hand-maintained list (`reactor.md` §4).

**RUN-8.** No later reader may be required to reconstruct what a Run was permitted to do by inspecting the platform as it exists at the time of reading. The agreement is stored, not inferred.

RUN-8 is the requirement that gives the rest their point. Component versions imply the agreement only while the matching procedure itself never changes. The day it changes, every prior Run becomes ambiguous about its own terms — and evidence that cannot say what it was allowed to do is evidence about nothing in particular.

---

## 3. What the Run owns

**RUN-9.** A Run owns the immutable history of one exact execution: the Run Contract, the recorded state at every captured step, every execution fact including the stopping fact, the cost record, and the identity of everything that participated.

**RUN-10.** Once a Run is complete it is never edited. Not corrected, not relabelled, not improved, not tidied. Later readings may disagree with earlier ones; the thing they disagree about does not move.

**RUN-11.** Corrections attach. A person's disagreement with a Run is recorded alongside it, with its reason and its author, and never applied to it.

### 3.1 Integrity lives in the record

**RUN-12.** A Run's integrity is protected by cryptography over the record — content addressing, hash chains over the recorded history, and signed export bundles. The technique is long established: a tree of hashes lets any part of a large record be verified against a single root value.[^merkle]

**RUN-13.** Nothing is ever embedded into the state data to describe that data. In a platform whose premise is sensitive dependence on state, altering state to carry provenance corrupts the experiment in order to sign it, and the signature is then made of altered evidence. If a downstream process strips the record-level provenance, the honest answer is that provenance was stripped.

---

## 4. What the Run refuses

| Refused | Owner |
|---|---|
| Any claim of robustness, cause, or generality | Study |
| Measurement | Reader |
| Naming what happened | Reader |
| Deciding whether two Runs may be compared | Study (§6) |
| Its own correction | nobody — corrections attach (RUN-11) |

**RUN-14.** A Run stores the fact and not the name. *State at step 900 matched state at step 850* is recorded. *Repeating* is not. The reasoning is in `reactor.md` §5; the consequence lands here, because whatever the Reactor called it, the Run keeps permanently and immutably. A wrong reading can be superseded. A wrong reading inside immutable evidence cannot.

---

## 5. Two replay promises

**RUN-15.** Every Run records which promise it supports:

> **Exact replay** — the recorded state is reproduced value for value, given the archived implementation, Reactor build, environment, random material, Starting State, and Run Contract. The strongest forensic claim, and the most expensive to keep, because it requires archiving the environment and not merely the inputs.
>
> **Reproduction under contract** — a later Reactor executes the same declared experiment and meets a stated equivalence standard, even where implementation details differ. The stronger long-term claim, because software changes and evidence is meant to outlive it.

**RUN-16.** The two are never silently exchanged. A Run recorded under the weaker promise is never described as exactly replayable, and a Run whose environment is no longer archived has its promise downgraded **in the record**, with the downgrade dated and attributed.

They differ because arithmetic on real numbers in a computer is not associative — the same values accumulated in a different order can differ in their last digits, as a property of the representation rather than a defect.[^goldberg] Any change to how a value is computed can therefore break the first promise while leaving the second intact.

DEC-2 owns which promise applies to which classes of evidence.

---

## 6. Comparability belongs to Study

**RUN-17.** A Run does not decide whether it may be compared with another. It **exposes complete bound identity and provenance** so that a Study can decide.

There is probably no useful global answer to whether two Runs are comparable, because comparability is relative to a question. A Repeat Test deliberately varies the Starting State while holding everything else. A World Comparison deliberately varies one feature of the setting. A Plugin Comparison deliberately varies the mechanism. A Reactor regression deliberately varies the Reactor. Each is a valid comparison and each violates the others' constancy requirements.

**RUN-18.** A Study states its own **comparison contract**: which fields must match, which are deliberately varied, which differences are irrelevant to its question, and that any other difference invalidates the comparison. The Run's duty is to make every one of those fields inspectable.

This keeps the Run/Study boundary intact. The Run never acquires a general theory of comparability, and the Study never has to guess what a Run was.

---

## 7. The cost of the answer

**RUN-19.** Every Run records what it cost: steps executed, wall-clock time, processor time, peak memory, the scale of the World in Cells and connections, proposals made and accepted, and steps until any Reader-detected event where one applies.

**RUN-20.** No single one of these is reported as the difficulty of the question. Steps executed measures iterative depth and modelled duration, not computational cost: ten steps over ten million Cells with an expensive mechanism can cost far more than fifty thousand steps over a small World. Studies decide which notion of cost their question needs.

The measurements are worth keeping deliberately rather than incidentally. Where a shortcut exists, an answer is cheap; where none does, the answer costs what it costs. That is the platform's whole subject, and the numbers are already available.

---

## 8. Playback follows from immutability

**RUN-21.** A Run completes before it is viewed. Playback is navigation over a finished record, never a simulation running alongside a viewer.

This is not a convenience. It is what makes stepping backwards free rather than requiring the ability to undo; what lets a measurement invented years later run against evidence recorded before it existed; what lets several people look at the same moment and see the same thing; and what lets alternate views be applied to old evidence without re-executing anything.

**RUN-22.** If the platform ever streams a live execution, provisional observations are marked provisional at the moment they are made. An unmarked provisional observation becomes evidence by default, and nobody notices when it happens. (DEC-19.)

---

## 9. What a Run binds, and what is merely context

**RUN-23.** A Run binds everything in the Run Contract (RUN-6). Those are its execution identity.

**RUN-24.** Lab identity is recorded as provenance. Where Lab-defined material directly affects execution, that material is part of the Run Contract by RUN-6 and is bound as such. Where the Lab is only the organisation that produced the World, the mechanism, and the measurements, its identity is context.

RUN-24 exists to avoid making *one Run belongs to exactly one Lab* an accidental execution constraint. The same mechanism may move between Labs, a Study may draw measurements from several, and a sufficiently general mechanism may belong to none.

---

## 10. What the Run requires

- **From the Reactor:** the Run Contract or mismatch record, the recorded history, the execution facts, the cost record, and the Reactor's version.
- **From the World and each Plugin:** execution identity precise enough that a later reader can tell what was in force.

## 11. What the Run produces

Immutable evidence, and the identity that lets a Study decide what may be done with it.

---

## 12. Open decisions

- **DEC-2 — Replay.** Reframed as two promises (§5). Which applies where is open.
- **DEC-1 — Mechanism composition.** Determines whether RUN-6's Plugin entry is one or several, and whether provenance must attribute each accepted change.
- **DEC-19 — Live work.** RUN-22 states the constraint any answer must satisfy.
- **DEC-23 — Starting State ownership.** RUN-6 records the Starting State separately, following `worlds.md` §4's leading candidate.
- **Proposed amendment to SCR-F §10:** the failure taxonomy should attach to Attempts rather than Runs. See RUN-3.

---

## Amendment record

**2026-08-20 — first-pass seam document replaced by this requirements document.** The seam pass is preserved unchanged at `runs.seams.md`, including its collected statement of the shared seam, which this document now closes.

Changed as a result of external critique (`../critiques/SCR_Core_Starter_Docs_Critique_v0.1.md`):

- *The Run Contract defined* (§2). The critique's central contribution. Five documents had found the declaration chain and left it unowned; the critique showed it needs a record rather than a component, with existing owners. RUN-5 to RUN-8 are new, and the shared-seam sections in the other four documents are retired as a result.
- *Attempt separated from Run* (§1). The seams pass wrote "a failed Run is a Run" and then discussed a mechanism refused before execution — using one word for two things. RUN-1 to RUN-4 correct it, and a matching amendment to SCR-F §10 is proposed rather than applied.
- *Comparability moved to Study* (§6). The seams pass listed comparability as an undefined Run property. The critique showed it is relative to a question and therefore belongs to the Study. RUN-17 and RUN-18.
- *Replay split into two promises* (§5), matching `reactor.md` §9.
- *Cost claim corrected* (§7). The seams pass called steps-to-outcome "a rough, honest measure of how hard the question was." That is wrong, and the critique's counterexample stands. The measurement is kept and widened; the claim is withdrawn. RUN-19 and RUN-20.
- *Lab identity distinguished from execution state* (§9). New, from the critique. RUN-24.

Unchanged: immutability as absolute, the Run as the meeting point of all identities, the fact-versus-name rule, and playback as navigation over finished history.

---

## Sources

[^merkle]: Ralph C. Merkle, "A Digital Signature Based on a Conventional Encryption Function," in *Advances in Cryptology — CRYPTO '87*, Lecture Notes in Computer Science 293 (Springer, 1988): 369–378. The construction now generally called a hash tree.
[^goldberg]: David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys* 23, no. 1 (March 1991): 5–47.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
