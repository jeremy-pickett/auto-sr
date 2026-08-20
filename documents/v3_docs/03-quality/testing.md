# Testing

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `03-quality/testing.md`
**Identifier namespace:** `TEST-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §16.3, §16.4, §38.3, §43 · `../01-core/plugins.md` (PLUGIN-5), `../01-core/generation.md` (GEN-4, GEN-5), `../01-core/reactor.md`

> Testing here has an unusual problem: for the thing the platform exists to study, **there is no expected answer to compare against.** If the outcome could be predicted without running it, the platform would not be needed.

---

## 1. Two subjects, tested differently

**TEST-1.** The platform distinguishes testing the **trusted base** from validating **variable experiment code**, and never lets one stand in for the other.

| | Trusted base | Variable experiment code |
|---|---|---|
| What | World, Reactor, Run, Corpus, storage, interfaces | Plugins, of any authorship |
| Tested by | the platform's own suite | Generation's checks and validation Runs (GEN-4, GEN-5) |
| A defect means | recorded evidence may be wrong, retroactively | this mechanism is invalid |
| Fixed by | a platform change and a version bump | a repair, or rejection |

**TEST-2.** A defect in the trusted base is treated as an evidence incident, not only a bug. Every Run executed under the affected version is identified, and the defect is recorded against that version so a later reader encounters it rather than trusting the evidence blindly.

TEST-2 has no equivalent on the right-hand column. A broken mechanism is a finding. A broken Reactor silently corrupts findings that already exist.

---

## 2. The platform's suite never runs against generated mechanisms

**TEST-3.** The platform's own tests run against **hand-written fixtures** — mechanisms written by people, reviewed by people, and changed deliberately. They never run against generated mechanisms.

This is the single most important requirement in this document, and the reason is not obvious.

A suite that tested the harness using whatever the generator most recently produced would drift with the generator. When the generator's habits changed, the tests would change with them, and the suite would keep passing while measuring something different each time. Worse, a generated mechanism that happened to exercise a bug would silently become the definition of correct behaviour.

Fixtures are stable, small, and understood. They are the control.

**TEST-4.** The fixture set includes at least one mechanism that is deliberately slow to settle, one that never settles, and one that fails — so the suite exercises the stopping paths and the failure paths, not only the happy one.

---

## 3. Testing without an expected answer

For a mechanism whose behaviour is not predictable in advance, there is nothing to assert the output against. This is the platform's own thesis arriving in its test suite, and it is a well-studied problem in software testing generally: where no oracle exists, one tests **relations between outputs** rather than outputs themselves.[^mt]

**TEST-5.** The platform's correctness properties are stated as relations that must hold between Runs, independently of what any Run produced.

**TEST-6.** At minimum, these relations hold and are tested:

| Relation | What it catches |
|---|---|
| Same mechanism, World, Starting State, and Reactor, run twice → identical recorded history | non-determinism anywhere in the trusted base |
| An optional capability at its default, present versus absent → identical to the last value | defaults that are not truly inert |
| A starting pattern moved, in a World whose arrangement is uniform → the result moved by the same amount | arrangement handling that depends on absolute position |
| Cell identities relabelled without changing structure → structurally identical result | logic that depends on identity rather than on declared paths |
| A Cell added that no declared path can reach → no change to any reachable outcome | reach violations, and state leaking outside declared connections |
| A budget raised without being reached → identical result | limits that alter behaviour before they bind |

**TEST-7.** Every declared option, capability, or modifier has a test showing that its default is **indistinguishable from its absence, to the last value**. A default that changes anything is not a default; it is an undeclared part of the mechanism.

The last row of TEST-6 and TEST-7 exist because this class of defect is invisible in ordinary use. Nothing looks wrong. The results are simply not the results of the experiment anyone thought they ran.

---

## 4. Contract checks before execution

**TEST-8.** Structure, permitted capabilities, declared reads and writes, reach, and the semantic ceiling are checked before any expensive execution (GEN-4).

**TEST-9.** Each check reports which check failed and why, distinguishably (REACTOR-6). "Invalid" is not a result.

**TEST-10.** A Generation check is a preflight and never substitutes for the Reactor's admission match (GEN-8, REACTOR-5). Both run. They may disagree, and a disagreement between them is itself a defect in the trusted base under TEST-2.

---

## 5. Validation Runs

**TEST-11.** Before delivery, a candidate mechanism is executed under the same contract as any other Run — same admission, same limits, same recording — at the scale it will actually be used, not a reduced one.

**TEST-12.** Validation covers at minimum: that it starts at all; that it executes without contract violation; that it reproduces (§`repeatability.md`); and that it does not exhaust its budget merely by starting.

**TEST-13.** A mechanism that passes validation has been shown to be a valid mechanism. It has **not** been shown to be a useful one, a correct implementation of its stated intent, or a good idea. Validation is a floor.

---

## 6. What testing cannot do here

**TEST-14.** No test establishes that a mechanism implements the intent it claims. Intent, implementation, and outcome are separate records precisely because nothing automatic reconciles them.

**TEST-15.** No test establishes that a result means anything about a subject. That is a Lab's obligation (`accuracy.md`) and it is not a testing problem.

---

## Sources

[^mt]: Tsong Yueh Chen, Fei-Ching Kuo, Huai Liu, Pak-Lok Poon, Dave Towey, T. H. Tse, and Zhi Quan Zhou, "Metamorphic Testing: A Review of Challenges and Opportunities," *ACM Computing Surveys* 51, no. 1 (2018): article 4.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
