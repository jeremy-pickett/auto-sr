# Repeatability

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `03-quality/repeatability.md`
**Identifier namespace:** `REPEAT-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §7, §19, §32, §38.3; F-10 · DEC-2 · `../01-core/reactor.md` (§9), `../01-core/runs.md` (§5)

> Three different things get called *repeating an experiment*. They are not interchangeable, they cost different amounts, and confusing them is how an evidence claim quietly becomes stronger than the evidence.

---

## 1. Three levels, named separately

**REPEAT-1.** The platform names three levels and never lets one stand for another.

> **Exact replay** — same inputs, same implementation, same environment, reproduced value for value.
> **Reproduction under contract** — same declared experiment, possibly a different implementation, meeting a stated equivalence standard.
> **Repetition under variation** — the same question asked again with something deliberately changed, to see whether the finding survives.

**REPEAT-2.** Every Run records which of the first two it supports (RUN-15). The third is a Study pattern, not a property of a Run.

The first two are the platform's own vocabulary and map onto established terminology only partly. *Reproducibility* in the wider scientific sense means obtaining consistent results using the same input data, computational steps, and conditions — which is exact replay. *Replicability* means obtaining consistent results across separate studies each collecting its own data — which is closest to a Repeat Test.[^nas] Reproduction under contract sits between the two and has no standard name, which is precisely why REPEAT-1 gives it one here rather than letting it borrow either.

---

## 2. Exact replay

**REPEAT-3.** Exact replay requires archiving the **environment**, not only the inputs: the implementation, the Reactor build, the numeric behaviour of the platform it ran on, and everything in the Run Contract.

**REPEAT-4.** Where any archived component is no longer available, the Run's promise is downgraded **in the record**, dated and attributed. It is never silently reduced, and never described afterwards as though it had always been the weaker promise.

**REPEAT-5.** Exact replay is the strongest forensic claim and the most expensive to maintain. It is not the default for all evidence merely because it is the strongest.

### 2.1 Why it is fragile

Arithmetic on real numbers in a computer is not associative: the same values accumulated in a different order can differ in their final digits, as a property of the representation rather than a defect.[^goldberg] A change in the order of a sum, a different numeric implementation, or different hardware can therefore break exact replay while changing nothing anyone would call the experiment.

**REPEAT-6.** Exact replay is a claim about a preserved environment, never a claim about the mechanism being deterministic. A perfectly deterministic mechanism can fail exact replay for reasons that have nothing to do with it.

---

## 3. Reproduction under contract

**REPEAT-7.** Reproduction under contract requires a written **equivalence standard**: what must match, to what tolerance, for the same declared experiment to count as reproduced on a different implementation.

**REPEAT-8.** The equivalence standard is versioned and is recorded with any claim that relies on it. A claim of reproduction that does not name its standard is not a claim.

**REPEAT-9.** The equivalence standard is stated in terms of the experiment, not the implementation — recorded state at named steps, execution facts, and Reader results, rather than internal values no contract mentions.

This is the promise that lets software improve without invalidating history, which makes it the stronger long-term claim. It is also the one that can be argued about, which is why REPEAT-7 requires the argument to be settled in advance and in writing.

DEC-2 owns which promise applies to which classes of evidence.

---

## 4. Reproducibility as a gate

**REPEAT-10.** A candidate mechanism is executed at least twice under identical conditions before delivery. Differing results are a validation failure, recorded with both histories.

**REPEAT-11.** A mechanism that fails to reproduce is retained as a failure with its reason, not discarded (GEN-18).

**REPEAT-12.** Reproducibility is checked again after any change to the trusted base, against a standing set of fixtures (TEST-3). A silent loss of reproducibility is the defect class most likely to invalidate evidence retroactively.

---

## 5. Version discipline

**REPEAT-13.** The same mechanism executed under a different Reactor version is a **different experiment**, and the record says so rather than presenting the two as repetitions of one another.

**REPEAT-14.** Every component version that could affect execution is in the Run Contract (RUN-6). Version identity is recorded, never inferred from a timestamp.

---

## 6. Two failures that look identical and are not

**REPEAT-15.** The record distinguishes:

> *We cannot reproduce this because the machine that produced it does not produce identical output.*
> *We cannot reproduce this because we did not record what we asked it.*

The first is a property of the world and is honest. The second is a defect in the platform, and it is the one that must never be reported as the first.

**REPEAT-16.** Generation stores fully rendered machine inputs rather than reconstructing them (GEN-16). A reconstruction from a template that has since changed is a plausible fiction, which in a provenance record is worse than an absence.

---

## Sources

[^nas]: National Academies of Sciences, Engineering, and Medicine, *Reproducibility and Replicability in Science* (Washington, DC: The National Academies Press, 2019).
[^goldberg]: David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys* 23, no. 1 (March 1991): 5–47.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
