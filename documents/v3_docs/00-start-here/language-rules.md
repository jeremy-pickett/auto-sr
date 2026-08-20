# Language rules

**Document class:** Level 1 — Foundations · **Status:** draft
**Path:** `00-start-here/language-rules.md`
**Cites:** SCR-F v0.2 §5, §20.3, §36.2, §36.6, §41–43; F-5, F-13

---

## The rule

> **Use words a working engineer or a second-year student can understand without specialist mathematics.**

This applies to code names, stored field names, interface labels, headings, log messages, error text, commit messages, and every document in this tree.

It does not mean avoiding hard ideas. Hard ideas are the subject. It means hard ideas get named clearly instead of being named impressively.

The project's own name is pretentious. Nothing else gets to be.

---

## What a violation looks like

The failure is rarely a long word. It is a word that carries authority the thing has not earned, or that requires a background the reader was never promised.

| Instead of | Write |
|---|---|
| toroidal boundary | wraps top to bottom and side to side |
| stochastic | random |
| perturbation | change |
| non-ergodic | it does not reach every state |
| isomorphic to | the same shape as |
| Jacobian | *nothing — the thing has no derivative to take* |

The last row is not a joke. A borrowed term can smuggle in an assumption that is false about the actual system, and then a later document reasons from the assumption rather than the system.

**A standard term may be introduced once, in an aside, where knowing it helps a reader connect to outside work.** "Wraps top to bottom (the standard term is *toroidal*)." Once. Then the plain name is what the codebase, the interface, and the rest of the tree use.

---

## Words that claim more than the thing does

Some words are accurate-sounding and load-bearing wrong. They are worth naming individually because they recur.

- **Do not call an enforced contract a sandbox.** Running generated code inside a restricted set of permitted operations, with resource limits, is contract enforcement. "Sandbox" implies a security boundary of a specific and much stronger kind, and someone will eventually rely on the implication.
- **Do not call a measurement a classification, or a classification a finding.** A measurement produced a number. A classification applied a label. A finding is a claim someone is prepared to defend.
- **Do not call an interpretation evidence.** Anything a machine says about a machine's own work is interpretation, including repair explanations, summaries, and narration.
- **Do not call the picture the state.** A display can go quiet while the underlying state keeps changing. Language that treats what is visible as what is happening will produce wrong stopping rules and wrong conclusions.
- **Do not say "proved" for "demonstrated."** A thing that ran once has been demonstrated.

---

## Technology names

**Levels 1 and 2 name no technology.** No programming language, library, database, framework, model vendor, or product. If a foundational statement cannot be made without one, the statement is a requirement wearing the wrong clothes and belongs a level down.

**Level 3 and below name technology freely,** because that is where a choice can be made, revisited, and replaced without disturbing anything above it.

The reason is the platform's own promise of permanence. Evidence is supposed to outlive the software that made it. A concept defined in terms of a language version or one vendor's product has a shelf life, and everything cited from it inherits that shelf life. See `what-is-scr.md` for the full argument, and `glossary.md` for the pending amendment where SCR-F v0.2 breaks this rule.

Two things about technology *are* foundational, because they are about capability rather than product: that machines can translate meaning into mechanism cheaply, and that they cannot be trusted to do it correctly on their own.

---

## Subject vocabulary

**Levels 1 through 4 stay subject-neutral.** The core knows about state, arrangement, mechanisms, runs, measurements, and evidence. It does not know what a fish, a fire front, a permission, a crystal, or a network account is. Those meanings belong to Labs, and Lab papers are where they live.

The worked example is in SCR-F itself. §21 lists what measurements the core may reasonably know about — and v0.1 mixed a specific subject's vocabulary into that list, eleven sections after the core had been forbidden from knowing that subject existed. It was not carelessness; those examples are simply the vivid ones.

This matters more than usual here, because most of this tree will be machine-written, and a machine writing a new document takes its cue from what the existing documents demonstrate. Leaked vocabulary in one core document becomes leaked vocabulary in fifty.

**Flag, do not smooth.** A writer who finds an ambiguity in a document above them records it as an ambiguity. A writer who finds a question the Decision Registry owns cites the open question and stops. The tempting move — pick the reading that makes the sentence work and carry on — is how a tree of two hundred documents ends up holding an undecided question as settled fact, with no record of anyone deciding it.

---

## Numbers

Say what was counted.

> Nineteen of twenty starting positions produced a travelling shape. The one that did not started inside the obstacle.

That sentence reports the result, the sample, and the exception. It is more informative and more honest than a significance figure computed against an unstated comparison.

The rules:

- Counts, proportions, distributions, and side-by-side comparisons, in ordinary sentences.
- State what was **not** tested next to what was.
- Never present a number nobody can trace back to a computation.
- Never imply precision the method does not have. Three decimal places on a measurement with two conditions is a claim about accuracy.

What "enough confidence" means for a Study is an open question in the Decision Registry (DEC-4). Until it is decided, no document invents a local definition of it.

---

## Citations

In a tree written mostly by machines, **a fabricated citation is the most damaging thing that can go into a document.** It is confident, it is specific, it looks exactly like diligence, and it survives review because checking it is boring. One invented reference in a Lab paper can put the platform's credibility below zero with the only readers who could tell.

So:

1. **Cite only sources you have verified.** Author, title, publication, year — checked, not recalled.
2. **If a detail is from memory, say so in the text, at that point.** `*(attribution from memory, verify)*` is a complete and acceptable solution. An existing Lab brief already does this on a model attribution, and it should be copied everywhere.
3. **Never invent a page number, volume, or date to make a citation look complete.** An incomplete citation is fine. A wrong one is not.
4. **Distinguish what the field established from what this platform produced.** A Lab paper making a claim about its subject cites the subject's literature. Evidence generated here is labelled as evidence generated here.
5. **Cite documents in this tree by identifier, never by paraphrase.** `SCR-F v0.2 §19`, `F-9`, `DEC-1`. A paraphrase drifts; an identifier does not.

---

## Why this document exists at all

Plain language is usually treated as a courtesy. Here it is a working requirement, for a specific reason: the platform's entire claim is that meaning survives from a person's question through to the evidence and back. Jargon is where meaning stops travelling. A term that only the writer's discipline understands breaks the chain at exactly the point the platform says it protects.
