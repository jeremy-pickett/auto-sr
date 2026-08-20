# Glossary

**Document class:** Level 1 — Foundations · **Status:** draft
**Path:** `00-start-here/glossary.md`
**Cites:** SCR-F v0.2 §36.7 (source of the rename table), §2, §3, §8, §10, §13.1, §17, §25.3, §30, §33, §36.1, §40

This is the single place the platform's vocabulary is defined. Documents cite it. They do not re-derive it, and they do not quietly redefine a term to make a sentence work.

---

## Core terms

The renames from the earlier system are deliberate. The right-hand column records what the same idea was called before, so a reader meeting old vocabulary in old material can resolve it.

| Term | What it means, in one line | In the earlier system |
|---|---|---|
| **Cell** | The smallest thing that holds state and can affect its neighbours, within the computational ceiling | Cell |
| **World** | The complete setting for an experiment, which owns its Layout | the grid plus its configuration, never named as one thing |
| **Layout** | How a World's Cells are arranged, and which local interactions are possible | a fixed 200×200 grid that wrapped at every edge |
| **Connection** | A declared possible local interaction between Cells | the neighbourhood, implied rather than stated |
| **Generation** | The pipeline that turns intent into a checked, tested Plugin | the three-stage propose / implement / validate pipeline |
| **Plugin** | The readable implementation of one local mechanism | a generated rule and its per-tick step |
| **Reactor** | The deterministic execution authority | the engine, or the harness |
| **Run** | One exact execution, kept permanently and never edited | a run |
| **Study** | A structured question spanning one or more Runs | — (new) |
| **Reader** | A versioned, repeatable reading of stored evidence | classifier, detector, analyzer |
| **Corpus** | The durable body of evidence and meaning | the library |
| **Search** | Finding things again across the Corpus | — (new) |
| **Lab** | A subject-owned working environment | — (new) |
| **Visualization** | Evidence-backed views, and time made navigable | the run player and its render styles |

---

## Terms in use without an entry until now

These appear throughout SCR-F and the documents below it. They were never collected.

**Intent, Implementation, Outcome** — the three records the platform keeps separate: what someone meant to try, what mechanism was actually produced, and what happened when it ran. They are allowed to disagree, and the disagreement is evidence.

**Computational ceiling** — the limit on what a Cell may hold: a bounded set of simple values, declared in advance. A subject whose participants cannot be described this way fails its fit review. The exact limits belong to a requirements document; that a limit exists belongs here.

**Computational irreducibility** — the property that a system's distant behaviour cannot be worked out faster than by running it. Named by Wolfram (see `what-is-scr.md`). It is a property of a *regime*, not of a subject: the same subject can have a shortcut in one condition and none in another.

**Evidence, derived evidence, interpretation** — three levels that must stay distinguishable. Evidence is what was recorded. Derived evidence is what a Reader computed from it. Interpretation is what a person or machine believes it means. Only the first is immutable.

**Semantic account** — the plain-language statement of what a repair changed mechanically. Required of every repair, and classified as interpretation, never as proof the repair was faithful.

**Failure classes** — the platform distinguishes seven ways there can be no result, because the reason is the information: *proposal failure* (the idea was invalid or outside the Lab's contract), *Plugin failure* (the implementation did not express or execute it), *Reactor rejection* (the mechanism tried something outside the declared experiment), *Run failure* (execution could not complete reliably), *behaviour miss* (it ran, and the requested behaviour did not appear), *Reader uncertainty* (evidence exists but the measurement cannot be made reliably), and *Study failure* (the evidence did not answer the question). All seven are kept.

**Fit review** — the review a Lab must pass before its abstraction is treated as defensible. A Lab may fail, and a failure is useful information about where this platform stops working.

**Standing** — a graded judgement carried by a Lab candidate. Standing is not fit: a candidate can carry a favourable standing and still fail its review, and an inherited standing is never re-derived by a document that merely repeats it.

**Ambient sensitivity** — how much a Run's later state diverges across a sample of comparable small changes. Any single change's effect is shown against it, so that "this change mattered unusually" and "this system diverges from any change at all" are visibly different statements. Uniform sensitivity is a finding, not a rendering failure.

**Provenance** — the full chain from a person's request to a result: what was asked, what was sent to any machine, what came back, what was built, what ran, under which versions, what measured it, and who corrected what.

**Platform Services** — the ordinary infrastructure that keeps the product running. It supports all twelve components and defines none of them.

**Decision Registry / DEC** — the index of consequential choices this platform has deliberately not made yet, each one a numbered record. An open decision is cited, never answered locally.

**Foundational rule / F-n** — the condensed, permanently numbered form of a foundational principle, so a document can cite the rule without citing a section number that may move.

**Document class / Level** — where a document sits and how much authority it carries, from Foundations at Level 1 down to operations documentation at Level 6. See the tree's `README.md`.

---

## Pending amendment: the Plugin definition

SCR-F v0.2 §36.7 defines a Plugin as the readable implementation of one local mechanism *in a named programming language*, and §2 and §17 do the same. The table above deliberately does not.

**The change, stated exactly.** Remove the language name from the definition of Plugin in §2, §17, §36.7, and from the title and text of the open decision covering the Plugin's contract surface. The requirement that survives is the property: a representation a competent person can read, change, and hand to someone else without the platform's help.

**Why.** Which language is used is a real and consequential choice — but it is a Level 3 choice, revisable without disturbing anything above it. Defining the Plugin *as* a language artifact makes that choice permanent by placing it too high, and it puts an expiry date on a Corpus that is supposed to outlive its software. The argument is in `what-is-scr.md`; the general rule is in `language-rules.md`.

**Status.** This is a proposed amendment to SCR-F, raised by the project's human owner, not a correction a downstream document is entitled to make on its own. Foundations outranks this document on conceptual meaning, so until SCR-F revs, the two texts disagree in the open and this note is the record of it. The documents in `00-start-here/` are written to the corrected form because they exist to set the direction the rest of the tree follows.

---

## How this glossary changes

- A new term is added with a one-line meaning and its earlier name, or an explicit note that it has none.
- A retired term stays, marked retired, with the amendment that retired it. Nothing is deleted.
- **A changed meaning is an amendment, not an edit.** A term whose definition shifts quietly is worse than a term nobody defined, because everything that cited it now says something else.
