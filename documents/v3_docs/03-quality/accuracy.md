# Accuracy

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `03-quality/accuracy.md`
**Identifier namespace:** `ACCURACY-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §30.6, §30.7, §30.9, §41, §42, §43; F-17 · DEC-15, DEC-20 · `../01-core/labs.md`

> Accuracy here does not mean *this platform predicts the subject*. It means *this Lab has evidence for the claims it actually makes*, and those claims are deliberately modest.

---

## 1. The word this document will not use

**ACCURACY-1.** No Lab, report, interface, or export describes a model of a real-world system as **verified** or **validated**.

This prohibition is about claims concerning the world. It does not touch the ordinary software sense in which a generated mechanism is *validated* against the contract it must satisfy (GEN-7) — that is checking an artifact against a written specification, and it is achievable.

This is not squeamishness. The argument against those words is well made and long established: verification and validation of numerical models of natural systems is impossible, because natural systems are never closed and model results are never unique. A model that agrees with observation may be **confirmed**, and confirmation is always partial — agreement between prediction and observation never establishes that the model's mechanism is the real one, because other mechanisms could produce the same agreement.[^oreskes]

That is precisely SCR's position, arrived at from the other direction. The platform's output is a **candidate** mechanism. Several candidates can reproduce the same observation, and the platform's whole value is that it can produce many of them cheaply — which is also exactly why none of them is thereby shown to be right.

**ACCURACY-2.** The permitted vocabulary is: *confirmed against* a named reference case, to a stated extent; or *not confirmed*; or *not yet tested*. Each names what it was tested against.

**ACCURACY-3.** A Lab status of *confirmed* means accuracy evidence exists against stated reference cases. It never means the Lab's abstraction is correct for its subject. **`../01-core/labs.md` LAB-9 was amended for this reason, renaming its third status from *validated* to *confirmed*;** the amendment record is on that document.

---

## 2. What each Lab owes

**ACCURACY-4.** Every Lab states its accuracy obligations in its own paper: what would count as evidence that it behaves plausibly, what it has been tested against, what it has not, and what the results were — including the unfavourable ones.

**ACCURACY-5.** Accuracy claims are stated per **regime**, never per subject. A Lab confirmed in one regime is untested in every other, and the platform says so rather than letting a single favourable result travel.

**ACCURACY-6.** A Lab that has not been tested says *not yet tested*. Silence is read as a favourable result and must never be available as an option.

---

## 3. Failure boundaries

This is the highest-value obligation in this document and the easiest to write dishonestly, because it requires a Lab to describe the conditions under which its own output should be disbelieved.

**ACCURACY-7.** Every Lab states the conditions under which it would produce a **convincing but misleading result**: a rendering that looks right, reads as authoritative, and is wrong.

**ACCURACY-8.** Failure boundaries are stated concretely — which regime, which visual, which measurement, which reading a viewer would plausibly take — not as a general caution that models have limits.

**ACCURACY-9.** Where a Lab's most persuasive output is also its least checkable, the Lab says so in the same place the output appears.

ACCURACY-9 exists because the two properties correlate. The subjects that render most beautifully are frequently the ones where nobody can tell whether the picture is right, and a caption at the bottom of a report does not travel with a shared image.

---

## 4. Rediscovery is not accuracy

**ACCURACY-10.** Reproducing a result the subject already has in closed form is a **test of the platform**, and is reported as one.

**ACCURACY-11.** A Lab's accuracy evidence states, for each reference case, whether the case falls in a regime the subject can already solve without simulation (`../01-core/labs.md` §3.1, the reducibility audit).

This distinction decides how much a confirmation is worth. Agreement in a regime with a formula shows the platform can be made to agree with a formula. Agreement in a regime with no shortcut is the only kind that says anything about the subject — and it is also the harder kind to obtain, because reference data is scarcer exactly where the formulas ran out.

---

## 5. Transfer limits

**ACCURACY-12.** A Lab states what further work is required before a mechanism resembling observed behaviour may be treated as a real hypothesis about the subject — by whom, using which of the subject's own tools, against what data.

**ACCURACY-13.** No output is presented as suitable for an operational, safety, financial, or policy decision. Where a Lab's subject invites that reading, the Lab states the non-claim in its own paper, in the reader's own vocabulary.

**ACCURACY-14.** Where the platform hands a candidate mechanism to the subject's own tooling, it travels with its non-claims and its confirmation status attached, not as a bare mechanism. DEC-20 owns the form this takes.

---

## 6. Where accuracy is not the platform's problem

**ACCURACY-15.** Calibration against the real world is the subject's problem, solved with the subject's instruments and data. The platform's proposed contribution sits upstream of it: supplying, testing, indexing, and comparing candidate mechanisms cheaply and repeatably.

**ACCURACY-16.** That proposed contribution is itself untested. It is a claim about the platform's usefulness, it is falsifiable, and no Lab paper may present it as established.

---

## Sources

[^oreskes]: Naomi Oreskes, Kristin Shrader-Frechette, and Kenneth Belitz, "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences," *Science* 263, no. 5147 (February 4, 1994): 641–646.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
