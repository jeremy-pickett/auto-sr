# Reader

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/readers.md`
**Identifier namespace:** `READER-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §8, §21, §24.2, §36.6; F-11 · DEC-10
**Depends on:** `runs.md` (RUN-14), `reactor.md` (§5).

> A **Reader** examines finished evidence and produces a repeatable measurement. It reads. It never rewrites.

---

## 1. What a Reader owns

**READER-1.** A Reader identifies itself completely: name, version, settings, the exact evidence examined, its output, and its completeness or confidence where either applies.

**READER-2.** A Reader is **repeatable**. The same version, with the same settings, over the same evidence, produces the same result.

**READER-3.** A Reader result is **disposable in the best sense**: it can be deleted and rebuilt from immutable evidence without history changing. Nothing downstream may depend on a Reader result that could not be recomputed.

**READER-4.** A new version of a Reader may disagree with an older version. Both results are kept, both are attributed to their versions, and neither alters the Run either one examined.

---

## 2. What a Reader refuses

| Refused | Owner |
|---|---|
| The evidence it reads | Run |
| Deciding what happened | Reactor (execution facts) |
| Claiming robustness or cause | Study |
| Whether the measurement matters | Study, and a person |
| Subject vocabulary in the core set | Lab |

**READER-5.** A Reader never writes to a Run, never annotates one in place, and never becomes a property of the evidence it examined.

---

## 3. Where the platform's own Readers stop

**READER-6.** The core platform supplies subject-neutral Readers only: spread, movement, branching, persistence, recurrence, stationary structure, travelling structure, front speed, and persistence of state that is not visible.

**READER-7.** Readers carrying subject meaning belong to Labs, are defined in Lab papers, and are named nowhere in this document or any other core document.

This section is where the platform is most likely to leak. The vivid examples are always the subject-specific ones, and SCR-F's own §21 mixed them into the core list — eleven sections after the core was forbidden from knowing that subject existed. Most of this tree will be machine-written, and a machine writing a new document takes its cue from what the existing documents demonstrate. One leak here becomes fifty.

---

## 4. Three levels that must stay apart

**READER-8.** The platform keeps three levels distinguishable at every point where a claim is displayed or exported:

> **Recorded evidence** — what happened. Immutable.
> **Derived evidence** — what a Reader computed from it. Versioned, recomputable, disposable.
> **Interpretation** — what a person or machine believes it means. Attributed, disputable.

**READER-9.** A Reader's output is derived evidence. A machine-written account of a Reader's output is interpretation, including a repair's semantic account (GEN-14) and any generated summary or narration.

**READER-10.** The stopping *fact* the Reactor recorded is recorded evidence. The *name* for it is a Reader result. *State at step 900 matched state at step 850* is evidence; *repeating* is a reading (RUN-14, `reactor.md` §5).

The most familiar such names are the four broad classes of one-dimensional cellular automaton behaviour.[^wolfram84] They are useful, widely used, and their boundaries have been argued over ever since — which is what makes them a reading, and what would have been lost had they been recorded as facts.

---

## 5. Readers are discovered shortcuts

A Reader that reliably reports *a travelling shape, moving one cell every two steps, repeating every four* has compressed thousands of recorded steps into a sentence. That compression is not bookkeeping. It is a claim that in this region, for this behaviour, the future can be described without watching it — which is precisely a shortcut in a platform built for systems that mostly do not have one.

Wolfram's own treatment allows for this: computational irreducibility is compatible with pockets in which reduction is possible, and finding them is how anything gets understood at all.[^nks]

**READER-11.** A Reader records where it worked and where it did not, across the evidence it was run over.

**READER-12.** A Reader's coverage is reported as a **map**, not as a quality score. *This Reader produced a result on six of ten Runs* is a statement about where a shortcut exists, and the four it failed on are the interesting ones.

READER-12 inverts the ordinary reading of the same number. A measurement that works everywhere has found a regime the platform did not need to be built for. A measurement that works in a bounded region has found the boundary — and a boundary is a finding a Study can pursue.

---

## 6. Readers must not become invisible truth

**READER-13.** Every assertion a person sees names the Reader and version that produced it.

**READER-14.** For any assertion that a decision might rest on, the platform can show how the assertion relates to the underlying evidence — which Run, which steps, which values.

**READER-15.** A Reader reports uncertainty and its known failure cases in ordinary language, in the same place as its result and not in separate documentation. A measurement displayed without its uncertainty reads as a fact.

DEC-10 owns how READER-15 is presented.

---

## 7. What a Reader requires

- **From the Run:** complete recorded evidence, and the Run Contract that says what the evidence could have contained.
- **From the Corpus:** its own version history, so an old result stays attributable after the Reader improves.

## 8. What a Reader produces

A versioned, attributed, recomputable measurement — and, where it could not measure, a recorded statement that it could not, with the reason. **Reader uncertainty is one of the seven failure classes** and is not silence.

---

## 9. Open decisions

- **DEC-10 — Trust presentation.** Constrained by READER-13 to READER-15.
- **DEC-22 — Cell schema multiplicity.** Several kinds of Cell in one World changes what a subject-neutral measurement can even mean.
- **DEC-12 — Search similarity separation.** Reader results are one of the three things Search must keep apart.

---

## Sources

[^wolfram84]: Stephen Wolfram, "Universality and complexity in cellular automata," *Physica D: Nonlinear Phenomena* 10, no. 1–2 (1984): 1–35.
[^nks]: Stephen Wolfram, *A New Kind of Science* (Wolfram Media, 2002), §12.6, p. 737.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
