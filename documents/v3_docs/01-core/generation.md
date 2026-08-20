# Generation

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/generation.md`
**Identifier namespace:** `GEN-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §16, §16.1–§16.6, §32, §38.1, §42, §43; F-2, F-3 · DEC-5, DEC-17
**Depends on the core contract set:** `cells.md`, `worlds.md`, `plugins.md`, `reactor.md`, `runs.md`.

> **Generation** turns intent into a candidate mechanism that has survived checking. It is a proposal system. It never decides that anything it produced is worth having.

---

## 1. What Generation owns

**GEN-1.** The pipeline, in order: **propose → write → check → test → repair → deliver.** Each stage has an outcome that is recorded whether or not the next stage runs.

**GEN-2. Propose.** Interpret a request, a Lab goal, a gap, or an exploration objective, and state a simple local mechanism in ordinary language — before any implementation exists. The proposal is a separate, permanent record from the implementation that follows it.

**GEN-3. Write.** Produce a readable implementation satisfying PLUGIN-3, together with the complete declarations required by PLUGIN-2.

**GEN-4. Check.** Verify structure, permitted capabilities, declared reads and writes, and the semantic ceiling — before anything expensive runs.

**GEN-5. Test.** Execute controlled validation Runs sufficient to catch implementation defects, failures to reproduce, contract violations, and mechanisms that cannot start at all.

**GEN-6. Repair.** Where a failure is mechanical, make an explicitly bounded number of attempts to fix the implementation without changing the proposed mechanism.

**GEN-7. Deliver.** Hand a validated candidate and its complete provenance onward. Delivery is not endorsement.

---

## 2. What Generation refuses

| Refused | Owner |
|---|---|
| Deciding a mechanism is scientifically useful | Study, Reader, a person |
| Admission to a Run | Reactor (REACTOR-3) |
| Execution semantics of any kind | Reactor |
| What the mechanism means in a subject | Lab |
| Whether the question was worth asking | a person |

**GEN-8.** Generation's checks are a **preflight**, never a substitute for admission. The Reactor performs the authoritative match (REACTOR-5). A preflight is checked against the World, Reactor, and revision that existed at the time, and any of the three may have moved since.

**GEN-9.** A mechanism that Generation produced is variable experiment code and carries no additional trust because Generation validated it (PLUGIN-5).

---

## 3. What Generation requires

- **From the Lab:** vocabulary, permitted patterns, World templates, and the fit boundaries a proposal must respect.
- **From the World:** what exists, so a proposal can be written against something real.
- **From the Corpus:** what has already been tried, including what failed.
- **From the Reactor:** validation execution under the same contract as any other Run.

## 4. What Generation produces

A candidate mechanism, its stated intent, its declarations, its complete provenance — and, on every path that did not reach delivery, a recorded failure with its reason.

---

## 5. Repair

**GEN-10.** Repair attempts are bounded by a declared number, recorded in the provenance whether or not the bound was reached.

**GEN-11.** A repair may correct an implementation. It may not change the proposed mechanism. A change to the mechanism is a new proposal, with a new record, not a repair.

**GEN-12.** Repair preserves the whole chain: original proposal, original implementation, the failure, the repair instruction, the repaired implementation, and the final outcome. Nothing in that chain is overwritten by what came after it.

### 5.1 The semantic account

**GEN-13.** Every repair is accompanied by a plain-language statement of what changed mechanically — *the neighbour count no longer includes the cell itself; nothing else changed.*

Requiring a person to read the implementation line by line to confirm the meaning survived would push them back into implementation mechanics, which is the specific thing this platform exists to spare them.

**GEN-14.** That statement is **interpretation** — versioned, disputable, Reader-class — and never evidence that the repair was faithful. The change itself is the evidence. The account is how a person decides whether to look closer.

The reason is permanent and does not improve with better models: the account is produced by the same kind of machinery that produced the repair. It is a witness with an interest.

---

## 6. Provenance

**GEN-15.** Generation records: the request or objective; the fully rendered inputs sent to any machine; the identity and relevant settings of that machine; its raw outputs where they bear on the result; every stage outcome; and the timing of each.

**GEN-16.** Rendered inputs are **stored**, never reconstructed later from templates and parameters. A template that has since changed makes the reconstruction a fiction, and a plausible fiction in a provenance record is worse than an absence.

**GEN-17.** The record distinguishes *we cannot reproduce this because the machine's output varies* from *we failed to record what we asked it*. Those are different findings and only one of them is a limitation of the world.

---

## 7. Failure is output

**GEN-18.** Every stage failure is retained with its reason and its stage. Proposal failure and implementation failure are different findings, and neither is discarded because it produced nothing runnable.

**GEN-19.** A record of failure is generator-quality evidence. A platform that stores only what worked cannot tell anyone how often it works, and produces a map of explored ground that is wrong in a specific and flattering direction.

---

## 8. Coverage, and what it is not

**GEN-20.** Where Generation is guided by a record of what has been tried, that record describes **the space the platform has defined for itself** — shaped by the generator, the prompts, the Corpus, and the Lab's vocabulary.

**GEN-21.** No coverage measurement is presented as coverage of the possible mechanisms. Interfaces and reports state the qualification, not only the documentation.

The scale makes the point without argument. Exhaustive enumeration is possible for the very smallest rule spaces — the 256 one-dimensional rules that take a cell and its two neighbours were surveyed completely, and yielded four broad behaviour classes.[^wolfram84] Add one state or one neighbour and the space stops being enumerable by any method. Everything this platform generates is a sample drawn by a machine with priors, and saying otherwise would be the platform's easiest and most damaging lie.

**GEN-22.** User signals — behaviour overrides, flags, reruns — never enter the context that guides proposals. Coverage counts canonical Runs only. A generator steered by what a person marked interesting is a generator learning that person's taste and reporting it as exploration.

---

## 9. Who decides what to generate next

Nothing among the twelve components owns **exploration strategy**. Generation owns propose-through-deliver. Search owns retrieval. A Study asks a question someone already has. The decision *which experiment is worth running next, given everything already known* has no home, and §42's non-claim assumes it exists without saying where.

This is recorded as an unregistered candidate decision (`../04-decisions/README.md`), not answered here.

---

## 10. Open decisions

- **DEC-5 — The home of semantic translation.** Generation is one of four components currently doing its own.
- **DEC-17 — Model independence.** Which parts are provider-neutral, and how a change of machine appears in provenance. GEN-15 to GEN-17 constrain any answer.
- **Unregistered — exploration strategy.** §9 above.

---

## Sources

[^wolfram84]: Stephen Wolfram, "Universality and complexity in cellular automata," *Physica D: Nonlinear Phenomena* 10, no. 1–2 (1984): 1–35.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
