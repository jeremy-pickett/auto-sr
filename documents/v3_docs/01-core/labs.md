# Lab

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/labs.md`
**Identifier namespace:** `LAB-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §11, §29, §30, §30.1–§30.9, §41, §45.12; F-17 · DEC-15, DEC-20, DEC-24
**Depends on:** the whole core set. Lab papers live at `../labs/` and are Level 5.

> A **Lab** is where a subject enters the platform, and where it is held to account. The core knows about state, arrangement, mechanisms, runs, measurements, and evidence. It never learns what any of them mean.

---

## 1. What a Lab owns

**LAB-1.** A Lab owns its subject's vocabulary, its translation rules, its World templates, the meaning of Cell properties and connection classes, its permitted starting conditions, its own Readers and Study patterns, its reference cases, its fit boundaries, its accuracy obligations, its known failure modes, and its stated non-goals.

**LAB-2.** A Lab is accountable for whether its abstraction is defensible in its subject. No Lab earns credibility by successfully expressing a subject as Cells and connections. Expressibility is cheap; that is why it proves nothing.

---

## 2. What a Lab refuses

| Refused | Owner |
|---|---|
| Execution semantics of any kind | Reactor |
| Any relaxation of the mechanism contract | nobody — REACTOR-7 |
| Placing its vocabulary in core documents | nobody — LAB-3 |
| Claiming its subject's truth | the subject's own tools |

**LAB-3.** Subject vocabulary appears in Lab papers and in Lab-supplied material. It does not appear in Levels 1 through 4 of the core documentation, including this document, which is why no subject is named here.

**LAB-4.** No Lab, subject, or research purpose relaxes the contract. A Lab studying hostile behaviour receives stale observations, partial visibility, and timing differences as declared capabilities of the setting, never as extra freedom for its mechanisms (REACTOR-7, WORLD-11).

---

## 3. The fit review

**LAB-5.** A Lab is reviewed against ten questions. A Lab may fail, and **a failed review is useful evidence about where the platform stops working** — recorded and kept, not quietly retried.

1. **Subject fit.** Why is local interaction a defensible abstraction here?
2. **World fit.** What does a Cell represent? A connection? What relationships are lost? Does the state pass the semantic ceiling (CELL-5)?
3. **Mechanism fit.** Which of the subject's processes can be expressed as local mechanisms, and which cannot?
4. **Time fit.** What does one step mean? Is simultaneous update meaningful here? Are delayed observations or event ordering required (`reactor.md` §6)?
5. **Evidence fit.** Which measurements correspond to something the subject actually cares about?
6. **Accuracy.** Which reference cases, known systems, or datasets can test whether this Lab behaves plausibly?
7. **Failure boundaries.** Under what conditions would this Lab produce a convincing but misleading result?
8. **Comparison to established tools.** What already solves this better, and where is the platform complementary rather than duplicative?
9. **Transfer limits.** If a mechanism resembles observed behaviour, what further validation is needed before anyone treats it as a real hypothesis?
10. **The reducibility audit.** *Where does this subject already have a shortcut, and where has the shortcut broken?*

### 3.1 The tenth question

**LAB-6.** The reducibility audit names, separately: the regimes of the subject that have a closed-form or otherwise reducible answer, and the regimes where the only way to know is to run it. A Lab that cannot make the distinction has not established fit.

Question 10 is not a restatement of question 8. Question 8 asks what tool does this better; the answer may be another simulation. Question 10 asks whether the subject needs simulating **at all** in the regime under study — whether there is a formula.

The distinction decides whether a Lab has a product. Where a shortcut exists, the platform is laboriously rediscovering textbook content, and a beautiful result there is a demonstration that the platform works, not a finding about the subject. Where the shortcut has broken — near a threshold, in path-dependent orderings, where a process feeds back on the field that drives it — the platform is doing the only thing available.

**LAB-7.** The audit is stated per regime, never per subject. Reducibility is a property of conditions, not of a topic, and the same subject routinely has both.

This question is not in SCR-F §30. It is added here because two independently written Lab briefs invented it, in nearly the same words, without being asked — which is the strongest available evidence that a review missing it is missing something practitioners reach for anyway. **A corresponding amendment to SCR-F §30 is proposed rather than applied.**

---

## 4. Standing and status

**LAB-8. Standing is not fit.** A judgement carried by a Lab candidate — inherited from a survey, an assessment, or a prior document — is not a review outcome and never becomes one by repetition. A document that repeats a favourable standing has promoted nothing.

**LAB-9.** A Lab holds exactly one status: **candidate** (named, not reviewed), **experimental** (reviewed, in use, accuracy not established), or **confirmed** (accuracy evidence exists against stated reference cases, to a stated extent). Promotion is a human act and is recorded with its evidence.

**LAB-9.1.** *Confirmed* never means the Lab's abstraction is correct for its subject. Confirmation is partial by nature: agreement between a mechanism and an observation does not establish that the mechanism is the real one, because other mechanisms could produce the same agreement. The reasoning and its source are in `../03-quality/accuracy.md` §1.

**LAB-10.** No interface, report, or export describes a Lab as confirmed on the strength of anything other than a completed review under LAB-5 and evidence under LAB-9. The words *verified* and *validated* are not used of a Lab or of any model of a real-world system (ACCURACY-1).

DEC-15 owns the evidence threshold between experimental and confirmed.

---

## 5. What a Lab may claim

**LAB-11.** A Lab produces **candidate mechanisms**. A mechanism reproducing an observed pattern is a candidate explanation, never proof that the real thing works that way.

**LAB-12.** Every Lab states, in its own paper, where the platform stops and established practice begins.

**LAB-13.** A Lab's non-claims are stated in the Lab paper itself, not inherited from the core documentation, because the reader of a Lab paper is the person most likely to over-read it.

The discipline is ordinary and long-standing outside this platform: a model is not judged true or false but useful or not, and the practical question is always whether its wrongness matters for the purpose at hand.[^box] LAB-11 to LAB-13 exist so a Lab has to answer that question in writing rather than let a persuasive rendering answer it.

---

## 6. What a Lab requires

- **From the core:** stable contracts it can translate onto, and a refusal to learn its vocabulary.
- **From the Reactor:** honest capability answers at admission, so a Lab discovers an impossibility before it builds on one.
- **From Readers:** the subject-neutral set, on which its own Readers build.

## 7. What a Lab produces

World templates, Cell and connection meanings, Readers, Study patterns, reference cases, a fit review outcome, accuracy evidence, stated failure boundaries, and non-claims — plus, where a review failed, a permanent record of why.

---

## 8. Relationship to the Lab collection

**LAB-14.** The catalogue at `../labs/` names candidates. Presence in it is not fit, and no core document inherits a catalogue entry's standing as a finding (LAB-8).

**LAB-15.** Each Lab's own paper is Level 5 and owns everything in §1. This document owns the review those papers are run against, and grades nothing.

---

## 9. A Lab is where the cellular budget gets spent

**LAB-16.** A Lab requiring a relaxation of what makes the platform a local-mechanism instrument — several kinds of participant, reach beyond declared neighbours, more than one mechanism, update timing other than all-at-once — states the requirement explicitly in its fit review, against DEC-24.

Labs are where pressure to generalise arrives, and it always arrives well argued and one case at a time. LAB-16 exists so the requests are counted rather than granted individually until nothing is left of the original claim. A Lab that cannot fit without spending the last of the budget may be telling the platform something more valuable than a Lab that fits comfortably.

---

## 10. Open decisions

- **DEC-15 — Lab governance.** Constrained by LAB-9 and LAB-10.
- **DEC-20 — External calibration.** How candidate mechanisms are packaged for the subject's own tools without implying validity not earned. Constrained by LAB-11 to LAB-13.
- **DEC-24 — The cellular budget.** LAB-16 makes Labs report into it.
- **Proposed amendment to SCR-F §30:** add the reducibility audit as a tenth fit question. §3.1.

---

## Amendment record

**2026-08-20 — the third Lab status renamed from *validated* to *confirmed*.**

*Was:* LAB-9's third status was **validated**, defined as "accuracy established against stated
reference cases." LAB-10 used the same word.

*Now:* **confirmed**, defined as accuracy evidence existing to a stated extent, with LAB-9.1 added to
bound what it means, and LAB-10 extended to forbid *verified* and *validated* of any model of a
real-world system.

*Why:* writing `../03-quality/accuracy.md` surfaced a conflict this document had introduced.
Verification and validation of numerical models of natural systems is not achievable — natural
systems are never closed and model results are never unique — and the established term for what is
achievable is *confirmation*, which is partial by construction (Oreskes, Shrader-Frechette, and
Belitz, 1994; cited in that document). *Validated* is exactly the kind of word
`../00-start-here/language-rules.md` warns about: accurate-sounding, load-bearing, and claiming more
than the thing does. LAB-10 exists to stop over-reading, and it was doing so in a word that invites
it.

*Raised by:* this document set's own quality pass, 2026-08-20.

*What did not change:* the identifiers, the three-status structure, that promotion is a human act, or
anything in LAB-5's review.

*Still outstanding:* nothing in SCR-F uses these status words, so no amendment to Foundations
follows from this one.

---

## Sources

[^box]: George E. P. Box, "Science and Statistics," *Journal of the American Statistical Association* 71, no. 356 (1976): 791–799.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
