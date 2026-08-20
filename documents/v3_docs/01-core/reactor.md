# Reactor

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/reactor.md`
**Identifier namespace:** `REACTOR-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §6, §18, §18.1–§18.5, §38.2, §38.6; F-9, F-20 · DEC-1, DEC-2, DEC-3, DEC-16
**Supersedes:** the first-pass seam document, preserved at `reactor.seams.md`.
**Part of the core contract set:** `cells.md`, `worlds.md`, `plugins.md`, `runs.md`.

> The **Reactor** is the execution authority. It decides what actually happens. It is the only component that can determine an execution fact at the moment it occurs, and it can only determine it by running.

---

## 1. What the Reactor owns

**REACTOR-1.** The Reactor decides: which proposals are admitted and which refused; the order in which anything is applied; every random draw and when it is taken; what one step means, and what *later* means where later exists; which values a mechanism may read but did not compute; how much time, memory, and effect each participant receives; when the Run stops and on what fact; what must be captured for the Run to be replayable; and its own version identity.

**REACTOR-2.** Where a shortcut existed, this component would not be needed. That is not a limitation to engineer around — it is the platform's premise. Some systems' distant behaviour cannot be determined by any method faster than running them.[^nks] The Reactor is what running them is.

---

## 2. Admission, and the contract it produces

**REACTOR-3.** Before any execution, the Reactor performs the **authoritative match**: what the World offers against what the Plugin requires against what this Reactor supplies.

**REACTOR-4.** A successful match produces the **Run Contract** — the frozen, complete statement of what was agreed (defined in `runs.md` §2). A failed match produces a **mismatch record**, which is evidence and is retained.

**REACTOR-5.** Generation may perform the same match earlier as an inexpensive preflight check. That check never substitutes for this one.

> "Generation checked it" is useful. It must never become "therefore the Reactor may assume it was checked."

The distinction is not bureaucratic. The Reactor is the component that will actually execute the mechanism, which makes it the only component whose assessment cannot be stale. Anything checked earlier was checked against an earlier World, an earlier Reactor, or an earlier revision of the mechanism.

**REACTOR-6.** Mismatch classes are distinguishable in the record: a missing property, an incompatible kind or range, an absent connection class, reach beyond what the World permits, a required capability this Reactor does not supply, and a semantic-ceiling violation are six different findings, and reporting them as one word destroys the information.

---

## 3. What the Reactor refuses

| Refused | Owner |
|---|---|
| What a property or connection means | Lab |
| Inventing or repairing a mechanism | Generation |
| What the result signifies | Reader, Study |
| Naming what it observed (§5) | Reader |
| Whether the outcome is interesting | a person |

### 3.1 Hostile conditions are not an exception

A Lab studying adversarial behaviour receives stale observations, partial visibility, shared-resource effects, and timing differences as **declared capabilities of the setting** — never as a loosened contract for the mechanism.

**REACTOR-7.** No Lab, subject, or research purpose relaxes the Plugin contract. A mechanism studying an attacker is not an attacker and does not receive an attacker's access.

This paragraph exists because the pressure to break it is real and always arrives with a good reason attached.

---

## 4. Future-relevant state

A Run stops when nothing further can change, or when the state has been seen before. Deciding either requires knowing exactly which state determines what comes next. This is the subtlest requirement in the core set, and it reads like an implementation detail.

> **REACTOR-8.** A value is **future-relevant** if changing it could change any future accepted proposal or any future Reactor action.
>
> **REACTOR-9.** A value that cannot affect any future execution must not prevent recurrence from being detected.

Both halves are load-bearing. The first, applied too narrowly, produces a platform that announces a finished Run while something is still moving. The second, ignored, produces a platform where nothing ever settles because some irrelevant counter keeps advancing.

**REACTOR-10.** Future-relevant state includes at least: Cell properties a mechanism may read or write; Reactor-maintained values that can affect a future proposal; scheduled effects not yet applied; the execution phase; the position of every external input; the state of the random source *where a further draw remains possible*; and any composition ordering state.

**REACTOR-11.** The Reactor determines future-relevant state **from the frozen Run Contract**, not from hand-maintained special cases.

### 4.1 Why REACTOR-11 is stated as a requirement

The earlier system offers a warning worth carrying permanently. It skipped a random draw entirely on steps where nothing was born — and that skip is exactly what allowed a mechanism using randomness to reach a settled state at all. Had the draw happened regardless, the random source would have advanced every step, the state would never have repeated, and no mechanism using randomness could ever have finished.

A decision that looks like an optimisation was load-bearing experimental semantics. There are almost certainly others of the same shape, and hand-maintained lists of special cases are precisely how they stay undiscovered. Deriving the set from a frozen contract is what makes the derivation auditable years later, against the contract that was actually in force rather than against whatever the code does now.

---

## 5. Facts, not names

**REACTOR-12.** The Reactor records **execution facts**. It does not record conclusions.

An execution fact is produced by observation or comparison and cannot be wrong later:

- the state at step 900 matched the state at step 850;
- no accepted proposal changed future-relevant state;
- the step budget was exhausted;
- a resource limit was reached;
- an execution error occurred;
- an external stop was received.

A conclusion is a reading. *Settled*, *repeating*, *oscillator*, *stable*, *chaotic* — these are labels applied to facts, they are contestable, and they belong to Readers, which carry versions so that a later reading may disagree with an earlier one without disturbing the evidence.

The most familiar such labels are Wolfram's four classes of one-dimensional cellular automaton behaviour.[^wolfram84] They are useful, they are widely used, and their boundaries have been argued over ever since — which is exactly what makes them a reading rather than a fact, and exactly why the platform must not let its execution authority publish that kind of judgement.

**REACTOR-13.** A fact recorded by the Reactor enters immutable evidence. A reading does not. This asymmetry is the reason for REACTOR-12: a wrong reading can be superseded, and a wrong reading stored inside immutable evidence cannot.

The platform already knows the cost of confusing the two. A display can go quiet while the state beneath it keeps changing; a stopping rule that trusted the picture would be wrong in a way nobody would notice.

---

## 6. Time is an experimental variable

**REACTOR-14.** The Reactor owns the clock entirely. Its resolution, its ordering, and the meaning of any offset are its to define, and no mechanism may hold a clock of its own.

**REACTOR-15.** Every execution model the Reactor offers must be replayable and deterministic. A model that cannot be replayed is not one the Reactor may provide, whatever else it enables.

### 6.1 Why timing cannot be an implementation detail

The temptation is to treat update timing as an efficiency choice. It is not, and the field has known so for forty years: Ingerson and Buvel compared synchronous updating against cells updating at random and against cells on clocks of slightly different periods, and found that **some of the apparent self-organisation in cellular automata is an artifact of clock synchronisation.**[^ib] Structure that looked like a property of the rule turned out to be a property of updating everything at once.

That result decides the ownership question on its own. If update timing can manufacture structure, then timing is part of the experiment, and a component that changed it quietly would be changing results while appearing to optimise. It belongs to the Reactor, it is declared, and it is recorded.

**REACTOR-16.** Where the Reactor offers ordering beyond simultaneous update, the ordering is defined in terms of what may influence what — not in terms of any real-world clock — and the definition is part of the Run Contract. The discipline of ordering events by influence rather than by wall time is long established.[^lamport]

---

## 7. Composition is experimental semantics

**REACTOR-17.** If more than one mechanism participates in a Run, the composition policy is **declared, named, versioned, and recorded in the Run Contract**. It is never an incidental consequence of implementation order.

The reason is sharp: if the Reactor simply picks an ordering or resolves a conflict as it sees fit, **the Reactor has authored a mechanism that nobody declared and nobody reviewed.** That mechanism affects every result and appears in no record.

**REACTOR-18.** A composition policy states at minimum: which mechanisms participate; whether they read the same prior state or one another's applied results; whether proposals are simultaneous or ordered; how conflicting proposals to the same property resolve; how scheduled effects interleave; how budgets divide; and, where provenance requires it, which mechanism caused each accepted change.

DEC-1 decides whether composition exists at all. REACTOR-17 and REACTOR-18 constrain any answer that permits it.

---

## 8. Budgets

**REACTOR-19.** Every kind of effect is budgeted, not only scheduled ones: proposals per step, accepted changes, scheduled effects outstanding, helper invocations, wall-clock time per step, total time, and memory.

**REACTOR-20.** Budget limits are recorded in the Run Contract, and budget exhaustion is an execution fact (§5) distinguishable from every other stopping fact.

---

## 9. Replay, and why it has two meanings

**REACTOR-21.** The Reactor supports two distinct promises, named separately and never silently exchanged:

> **Exact replay** — given the archived implementation, this Reactor build, the same environment, the same random material, the same Starting State and Run Contract, the recorded state is reproduced value for value.
>
> **Reproduction under contract** — a later Reactor executes the same declared experiment and satisfies a stated equivalence standard, even where implementation details differ.

They differ for a concrete and unavoidable reason. Arithmetic on real numbers in a computer is not associative: the same values summed in a different order can give a different result, and this is a property of the representation rather than a defect to be fixed.[^goldberg] Any change to how a value is computed — a different order of accumulation, a different underlying numeric implementation, different hardware — can therefore change the last digits, and the first promise is broken while the second is untouched.

**REACTOR-22.** The Reactor states which promise a given Run supports, and never downgrades one into the other silently.

DEC-2 owns which promise the platform makes for which classes of evidence, and at what storage cost. Its original framing as a choice between the two is superseded; see the amendment on that record.

---

## 10. What the Reactor requires

- **From the World:** what exists, who may reach whom, what conditions apply, what each participant may see, and which capabilities are required.
- **From the Plugin:** complete and honest declarations. The contract is enforceable only against what was declared.
- **From the Run Contract:** everything it needs to determine future-relevant state (REACTOR-11).

## 11. What the Reactor produces

The Run Contract or a mismatch record; the recorded history; execution facts including the stopping fact; the cost record (`runs.md` §7); and its own version identity.

---

## 12. Open decisions

- **DEC-2 — Replay.** Reframed by §9 as two promises rather than a choice. Which is offered for which evidence, at what cost, is open.
- **DEC-3 — Temporal semantics.** Which models are offered. REACTOR-15 constrains every answer.
- **DEC-1 — Mechanism composition.** REACTOR-17 and REACTOR-18 constrain any permitting answer.
- **DEC-16 — Execution boundary.** Shared with `../02-platform/execution-safety.md`.

---

## Amendment record

**2026-08-20 — first-pass seam document replaced by this requirements document.** The seam pass is preserved unchanged at `reactor.seams.md`.

Changed as a result of external critique (`../critiques/SCR_Core_Starter_Docs_Critique_v0.1.md`):

- *Admission made explicit and authoritative* (§2). New. Resolves the seams pass's "check nobody performs" gap: the Reactor matches, Generation may preflight, and a preflight is never a substitute. REACTOR-3 to REACTOR-6.
- *Future-relevant state given a closure rule* (§4). The seams pass identified this as its largest gap and could not close it. The critique supplied the rule and its complement, and the requirement that it be derived from the frozen contract rather than from special cases. REACTOR-8 to REACTOR-11.
- *Replay split into two promises* (§9). The seams pass framed DEC-2 as a binary. The critique showed it is two useful promises with different names. REACTOR-21 and REACTOR-22.
- *Composition policy required to be declared* (§7). Sharpened from the seams pass's observation into REACTOR-17 and REACTOR-18.
- *Budgets generalised* (§8) from scheduled effects to every kind of effect.
- *Opening claim corrected.* The seams pass said the Reactor "is the only component that knows what happened." After completion the Run also knows, because the Reactor captured it. REACTOR-2's framing is narrowed to what is actually true: only the Reactor can determine an execution fact at the moment it occurs.
- *Three published results now carry arguments that were previously assertions*: timing as experimental semantics, classification as a reading, and the fragility of exact replay.

Unchanged: the hostile-conditions paragraph, which the critique recommended survive nearly untouched; the facts-versus-names correction; the execution-authority framing.

---

## Sources

[^nks]: Stephen Wolfram, *A New Kind of Science* (Wolfram Media, 2002), §12.6, p. 737, on computational irreducibility.
[^wolfram84]: Stephen Wolfram, "Universality and complexity in cellular automata," *Physica D: Nonlinear Phenomena* 10, no. 1–2 (1984): 1–35.
[^ib]: Thomas E. Ingerson and Raymond L. Buvel, "Structure in asynchronous cellular automata," *Physica D: Nonlinear Phenomena* 10, no. 1–2 (1984): 59–68.
[^lamport]: Leslie Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System," *Communications of the ACM* 21, no. 7 (1978): 558–565.
[^goldberg]: David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys* 23, no. 1 (March 1991): 5–47.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
