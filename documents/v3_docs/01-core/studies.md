# Study

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/studies.md`
**Identifier namespace:** `STUDY-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §9, §10, §20, §20.1–§20.3, §25.3; F-12, F-13 · DEC-4, DEC-9
**Depends on:** `runs.md` (RUN-17, RUN-18), `readers.md`, `worlds.md`.

> A **Study** is a structured question that takes more than one Run to answer. A Run shows that something happened once. A Study asks whether it means anything.

---

## 1. What a Study owns

**STUDY-1.** A Study states, in plain language: the question; the hypothesis where one clarifies matters; what is held constant; what is varied; what evidence would support or weaken it; which Runs were performed; which measurements were used; what was found; and what remains uncertain.

**STUDY-2.** A Study owns its **comparison contract** (RUN-18): which fields must match across its Runs, which are deliberately varied, which differences are irrelevant to this question, and the rule that any other difference invalidates the comparison.

Comparability is not a property two Runs have. It is relative to a question, which is why it lives here and not in the Run.

**STUDY-3.** A Study owns what it claims. A Run cannot claim robustness, cause, or generality; a Study may claim only what its own comparison contract and evidence support.

---

## 2. What a Study refuses

| Refused | Owner |
|---|---|
| Producing evidence | Reactor, Run |
| Measuring | Reader |
| Editing anything it examined | nobody — history is immutable |
| Truth about a subject beyond its evidence | Lab, and the subject's own tools |

**STUDY-4.** A Study never revises a Run to fit its conclusion, and never excludes a Run without recording the exclusion and its reason in the Study itself.

---

## 3. What a Study requires

- **From Runs:** complete bound identity and provenance, so the comparison contract can be checked rather than assumed (RUN-17).
- **From Readers:** measurements with versions, so a later disagreement is traceable.
- **From the World and Starting State:** separability, so *hold the setting and vary the opening values* is expressible (WORLD-4, WORLD-5).

## 4. What a Study produces

A stated question, a comparison contract, a set of Runs, the measurements taken, a finding, and an explicit account of what was not tested.

---

## 5. The patterns

**STUDY-5.** Five patterns are supported directly. Each states its own constants and variables, and each is checked against its comparison contract.

| Pattern | Held constant | Varied |
|---|---|---|
| **Repeat Test** | World, mechanism, Reactor, settings | Starting State |
| **Small-Change Test** | everything | one declared condition |
| **Try Many Settings** | World, mechanism | one or more declared settings, under a stated protocol |
| **World Comparison** | mechanism, Starting State recipe, protocol | one feature of the setting |
| **Mechanism Comparison** | World, Starting State, protocol | the mechanism |

**STUDY-6.** Mechanism Comparison is only valid where the Starting State is separable from the mechanism (`worlds.md` §4). Where it is not, the pattern is refused rather than run with a caveat.

---

## 6. What a Study may say

**STUDY-7.** Findings are stated in counts, proportions, distributions, and side-by-side comparisons, in ordinary sentences.

> Nineteen of twenty starting positions produced a travelling shape. The one that did not started inside the obstacle.

**STUDY-8.** What was *not* tested is stated alongside what was, in the finding itself and not in an appendix.

**STUDY-9.** No number appears that cannot be traced to a computation over named evidence. No precision is implied beyond what the method has.

**STUDY-10.** A Study does not report a significance figure against an unstated comparison. The professional statistical bodies' own position is that such figures are routinely misread as measuring the probability that a hypothesis is true, or the size of an effect, and that they measure neither.[^asa] A platform whose users are practitioners rather than statisticians has no business producing a number whose most common reading is wrong.

**STUDY-11. Study failure is a recorded outcome**, distinct from every other failure class: evidence exists, and it did not answer the question. Its reason is recorded — insufficient coverage, contradictory results, a comparison contract that could not be satisfied.

What "enough confidence" means is DEC-4's question. STUDY-7 through STUDY-10 constrain any answer.

---

## 7. Small-Change Tests measure something real

The Small-Change Test is usually described defensively — as the pattern that risks implying a change was special when the system diverges from any change. That is true and it is not the whole story.

**STUDY-12.** A Small-Change Test is run against a sample of comparable changes, and the divergence from the specific change is reported against the divergence across that sample — the Run's **ambient sensitivity**.

**STUDY-13.** Uniform sensitivity is a **finding**, not a failed measurement, and is reported as one.

That finding is worth naming plainly. A system in which any small change reshapes the outcome is a system with no shortcut: you cannot know where it goes without running it. This is the property the platform's whole value rests on, and STUDY-12 measures it directly, cheaply, from evidence already recorded.

The phenomenon is old and well documented outside this platform. Lorenz found that a set of deterministic equations for atmospheric flow produced solutions in which slightly different starting states evolved into considerably different ones — and drew the practical consequence, that prediction beyond a horizon was not merely difficult but unavailable.[^lorenz] A Study reporting uniform ambient sensitivity has found the same thing about its own subject, and should say so rather than treating it as noise.

**STUDY-14.** Neither a specific divergence nor an ambient-sensitivity result is rendered or reported without the other (`visualization.md` §5).

---

## 8. Inferring the question

**STUDY-15.** A Study may be proposed from ordinary language — *does the failure stop if I isolate this network?* is a Small-Change Test whether or not anyone says so.

**STUDY-16.** A proposed question, hypothesis, and comparison contract are shown for confirmation before Runs are executed. The platform does not choose the experiment and then report the result as though it had been asked for.

DEC-9 owns how much is inferred before confirmation is required.

---

## 9. Open decisions

- **DEC-4 — Inference discipline.** Constrained by §6.
- **DEC-9 — Planner autonomy.** Constrained by STUDY-16.
- **DEC-1 — Mechanism composition.** Determines whether Mechanism Comparison compares one mechanism or a composition.
- **DEC-23 — Starting State ownership.** STUDY-6 depends on its resolution.

---

## Sources

[^asa]: Ronald L. Wasserstein and Nicole A. Lazar, "The ASA's Statement on p-Values: Context, Process, and Purpose," *The American Statistician* 70, no. 2 (2016): 129–133.
[^lorenz]: Edward N. Lorenz, "Deterministic Nonperiodic Flow," *Journal of the Atmospheric Sciences* 20, no. 2 (1963): 130–141.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
