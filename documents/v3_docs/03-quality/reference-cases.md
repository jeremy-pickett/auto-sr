# Reference cases

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `03-quality/reference-cases.md`
**Identifier namespace:** `REFCASE-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §30.6, §30.8, §41 · `accuracy.md`, `../01-core/labs.md`

> A **reference case** is something the platform can be wrong about detectably. Without one, a Lab can only be admired.

---

## 1. What makes a reference case

**REFCASE-1.** A reference case states: what is being compared; the source of the comparison data and its provenance; which regime it falls in; what agreement would look like; what disagreement would look like; and what neither would prove.

**REFCASE-2.** A reference case is recorded so the comparison is repeatable by someone else. A remembered agreement with a published figure is an anecdote.

**REFCASE-3.** Reference data is cited to its source, and its bibliographic details are verified rather than recalled (`../00-start-here/language-rules.md`). A fabricated reference in an accuracy claim is the most damaging thing a Lab can publish: it is specific, confident, and checked by nobody until it is checked by exactly the reader who can destroy the Lab's credibility.

---

## 2. Kinds of reference case

**REFCASE-4.** Four kinds are useful, and they are not interchangeable:

> **Observed cases** — recorded real events with measurable properties.
> **Experimental cases** — controlled work in the subject's own literature.
> **Established results** — closed-form or otherwise settled answers within the subject.
> **Known-impossible cases** — behaviours the subject holds cannot occur.

**REFCASE-5.** A Lab that has only established results as references has confirmed that it can agree with a formula (ACCURACY-10). That is worth doing once and worth nothing repeated.

### 2.1 Known-impossible cases carry unusual weight

**REFCASE-6.** Where a subject holds that some behaviour cannot occur, a Lab tests that its mechanisms do not produce it, and records the result.

A platform that generates in bulk will produce things the subject says are impossible. That is a finding either way: the Lab's abstraction admits something it should forbid, or the subject's confidence is narrower than stated. Both are worth more than another agreement, and neither is reachable from favourable cases alone.

---

## 3. Calibration anchors

**REFCASE-7.** A **calibration anchor** is a subject where the platform's output is checkable against something external — where being wrong is detectable rather than merely arguable.

**REFCASE-8.** The platform maintains at least one anchor, and its purpose is to test the evidence chain itself: that generation, execution, recording, measurement, and reporting hold together on a subject where a wrong answer can be recognised.

**REFCASE-9.** An anchor's results are reported as evidence about the **platform**, not about the anchor's subject, unless it also satisfies ACCURACY-11 by falling in a regime with no shortcut.

The distinction matters because an anchor is chosen for checkability, and checkability correlates with the subject already being well solved. A Lab whose job is to test the platform rather than its subject is a legitimate Lab, and should be labelled as one rather than quietly promoted.

---

## 4. Where the subject's own tools already win

**REFCASE-10.** Every Lab names the established tooling in its subject, states what that tooling does better, and states where this platform is complementary rather than duplicative.

**REFCASE-11.** "Complementary" is argued, not asserted. A Lab claiming a complementary position states what specifically it would supply that the incumbent does not, and acknowledges that the claim is untested (ACCURACY-16).

---

## 5. Recording a comparison

**REFCASE-12.** A comparison against a reference case records: the reference case, the Runs compared, the Readers and versions used, the measured agreement or disagreement, and the regime.

**REFCASE-13.** Disagreements are retained on the same terms as agreements, and a Lab's accuracy evidence reports both. Selecting which comparisons to publish is the failure this requirement exists to prevent.

**REFCASE-14.** A reference case that later turns out to be wrong is marked, with what replaced it, and every claim resting on it is identified. It is not removed.
