# Visualization

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/visualization.md`
**Identifier namespace:** `VIS-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §12, §24, §24.1, §24.2, §25, §26, §27, §28, §38.6, §38.7; F-18, F-19 · DEC-13, DEC-14
**Depends on:** `runs.md`, `readers.md`, `studies.md` (§7).
**Normative home of the visualization truth contract.** SCR-F §26 states that its table is an exemplar and that the complete, versioned, testable contract belongs here. Extending §26's illustration in place is the mistake this document exists to prevent.

> **Visualization** makes evidence visible and time navigable. It may dramatize evidence. It may never invent it.

---

## 1. What Visualization owns

**VIS-1.** Views over recorded evidence and versioned Reader results, and the navigation of time within them.

**VIS-2.** Visualization is instrumentation, not decoration applied afterwards. Local-mechanism systems are temporal, and their behaviour frequently cannot be read from a final frame or a summary number. Watching is how people find structure that no available measurement was written to detect.

---

## 2. What Visualization refuses

| Refused | Owner |
|---|---|
| Producing evidence | Reactor, Run |
| Measuring | Reader |
| Claiming cause | Study, and nothing else |
| Deciding what a view means | a person |
| Rendering anything without a source | nobody — VIS-3 |

---

## 3. The truth contract

**VIS-3.** Every meaningful visual property answers one question: **what recorded or measured data produced this?** A property that cannot answer it is not shown in a view presented as evidence.

**VIS-4.** Permitted sources, by property. This table is normative and versioned; a new visual property is added to it before it is rendered, not after.

| Visual property | Permitted source |
|---|---|
| Position | World Layout; recorded Cell position; a named deterministic placement calculation |
| Height, size | a recorded value; a Reader measurement |
| Connection drawn | a connection the World declared; a recorded interaction |
| Trail | recorded positions of a Cell or structure over time |
| Brightness, glow | a recorded value or Reader measurement, with its normalisation named |
| Colour | recorded state; a Reader category; a named display mapping |
| Motion, animation | ordered recorded states |
| Divergence volume | measured difference between paired Runs, shown with ambient sensitivity (§5) |
| Cluster placement | a named similarity calculation over named data (SEARCH-6) |
| Emphasis, highlight | a recorded fact or a Reader result, named |

**VIS-5.** Transformation for legibility is permitted — scaling, smoothing, exaggeration, choice of palette, camera movement, pacing. **Implying data that does not exist is not.** The distinction is the difference between showing an effect larger than it is and showing an effect that was not there.

**VIS-6.** Where a view exaggerates for legibility, the exaggeration is stated. The measure is old and simple: the size of an effect shown, divided by the size of the effect in the data.[^tufte] A view whose ratio departs materially from one says so.

---

## 4. Styles are lenses over one history

**VIS-7.** Many styles may be applied to the same Run. Each derives from the same recorded evidence or from versioned Reader output, and none alters the Run.

**VIS-8.** The test for whether a style is a true view of evidence:

> Can this style be applied later to an old Run without executing anything?

**VIS-9.** Where the answer is no, the interface states what new information or execution is required. A style that quietly re-runs an experiment to render itself is producing new evidence and calling it a display option.

### 4.1 Quiet is not stopped

**VIS-10.** No view implies that a still picture means a settled system. A display can go quiet while state beneath it keeps changing, and a person reading stillness as completion will draw a wrong conclusion that nothing in the interface contradicts.

**VIS-11.** Where a view shows only part of the recorded state, it says which part.

---

## 5. Divergence, shown in context

**VIS-12.** A rendering of divergence between paired Runs is shown together with the Run's ambient sensitivity (STUDY-12). Neither is displayed alone.

**VIS-13.** Uniform sensitivity is rendered as a finding, not suppressed as a failure (STUDY-13).

This is the sharpest deception risk in the platform, and the remedy is context rather than refusal. In a strongly sensitive system *any* small change produces an expanding divergence; showing one change's cone alone invites the reading that this change was special. Refusing to render would be worse — derived analysis suppressing measured evidence is exactly the invisible truth layer READER-13 forbids.

Within paired deterministic Runs the divergence itself is honest: everything inside it differs because of the change. What needs context is only the implied claim that the change was unusual.

---

## 6. Time is an instrument

**VIS-14.** Every view of a Run supports: scrubbing, stepping forward and back, play and pause, jumping to a Reader-identified event, comparing two moments, marks for Study and Reader findings, and a stable reference to an exact moment.

**VIS-15.** Navigation never re-executes anything. It reads finished history (RUN-21).

The slider is not a playback control. It is how a person searches a Run.

---

## 7. Advanced views are candidates

**VIS-16.** Spatial views of Worlds and connections, time mapped into a spatial dimension, divergence volumes, multi-Run Study views, outcome surfaces, and similarity maps are **roadmap candidates**. This document may accept, reshape, or reject each. No document cites them as commitments.

**VIS-17.** The architecture avoids choices that would make them prohibitively expensive later. What evidence formats they require is DEC-13's question, and it must be answered before storage formats set.

---

## 8. Reports and generated video

**VIS-18.** A report distinguishes, visibly: the question; the setup; the mechanism; results; Reader measurements; human interpretation; uncertainty; limitations; and provenance. It reuses this contract rather than generating a separate narrative truth.

**VIS-19.** In a generated video, narration, captions, camera selection, pacing, and emphasis may be produced by machine. **Claims and depicted behaviour must trace to recorded Run, Study, Reader, or World data.** The video edits evidence; it does not compose a story.

**VIS-20.** A generated video carries provenance sufficient to check every claim it makes, and §5's ambient-sensitivity requirement applies to it exactly as to an interactive view. DEC-14 owns what that provenance contains.

A forty-second clip is the artifact most likely to travel without its Study attached. That is its value and its hazard, and VIS-20 is why the hazard is bounded.

---

## 9. What Visualization requires

- **From the Run:** complete recorded evidence and the Run Contract.
- **From Readers:** versioned results with their coverage (READER-11).
- **From Studies:** ambient sensitivity where divergence is shown.

## 10. What Visualization produces

Views, reports, and exports — each able to name the source of every meaningful thing it shows.

---

## 11. Open decisions

- **DEC-13 — Visualization scale.** What evidence formats advanced views require. VIS-17.
- **DEC-14 — Video provenance.** VIS-20.
- **DEC-22 — Cell schema multiplicity.** Several kinds of Cell changes what a single view can honestly show at once.

---

## Sources

[^tufte]: Edward R. Tufte, *The Visual Display of Quantitative Information* (Graphics Press, 1983; 2nd ed. 2001). The ratio of displayed effect to actual effect is Tufte's *lie factor*.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
