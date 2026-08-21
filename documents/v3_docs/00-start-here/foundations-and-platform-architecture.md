# Semantic Cellular Ruliology

## Foundations and Platform Architecture — v3.x

**Status:** draft — machine-written under owner direction; enters as draft and cannot self-promote (§36.3)
**Date:** 2026-08-21
**Scope:** Semantic Cellular Ruliology 3.x
**Supersedes:** v0.2, **upon adoption**. Until adopted, v0.2 remains the governing Foundations text, and the differences between the two are recorded openly in the revision record below.
**Cited as:** `SCR-F v3.x §n`; condensed rules as `F-1` … `F-23`.
**Purpose:** define what the platform is, what its major components own, how people interact with it, which principles later documents must preserve, and how the large document tree that follows stays honest.

> **This is not the implementation requirements document.** It sits above requirements. Since v0.2, the first ring of that tree has actually been written — thirty documents holding 362 numbered requirements across `documents/v3_docs/` — and this revision exists to bring Foundations back into agreement with what building that ring taught. Where a testable detail lives in the tree, this document points at it rather than repeating it; for testable contract details, the owning requirements document outranks this one (§36.4).

---

## Revision record — v0.2 → v3.x

Recorded rather than silently applied, following the project's standing practice: the reasoning matters more than the edits. Each change names where it arose; the fuller argument lives at the cited location.

| Change | Nature |
| :---- | :---- |
| **The programming-language dependence removed** (§2, §17, §36.7, §40) | Correction, raised by the owner. v0.2 stated the readability requirement correctly and then named a language in the next sentence; §17 and the glossary defined the Plugin *as* an artifact of that language. A Level 1 document that names a language has made a Level 3 decision by accident and made it permanent by placing it too high — and put an expiry date on a Corpus meant to outlive its software. The requirement that survives is the property. Argument: `v3_docs/00-start-here/what-is-scr.md`; exact change: `v3_docs/00-start-here/glossary.md`. |
| **Attempt and Run distinguished; the failure taxonomy attaches to Attempts** (§7, §10, §19) | Correction of a terminology seam found by external critique. v0.2 used "Run" for both a planned execution and an admitted one, while two of its seven failure classes occur before execution begins. An **Attempt** is now the durable record of one intention to execute; a **Run** is an Attempt that passed admission and began. Nothing refused at the door is lost. |
| **The Run Contract named** (§18, §19, §34) | Closure. All five core contract documents independently found the same unowned chain — the World declares what exists, the Plugin declares what it uses, the Reactor enforces the match, the Run records the agreement. The closure is a record, not a thirteenth component: the Reactor performs the authoritative match at admission and the Run stores the frozen result forever. Defined in `v3_docs/01-core/runs.md` §2. |
| **The replay fork resolved into two named promises; DEC-2 decided** (§19, §40) | Decision. v0.2 posed "exact or contractually equivalent" as a fork to be chosen. External critique showed the two are distinct promises that should coexist under separate names, and the owner decided the boundary on 2026-08-21: reproduction under contract by default, exact replay for Runs designated evidence-grade at run time. First registry record to reach *decided*. |
| **Starting-state ownership named as a fork** (§14, §40) | Honesty correction. v0.2 asserted that the World owns the starting state while the demonstrated 2.x system had the mechanism generate it — a live contradiction stated as settled fact. Now DEC-23, open, with a leading candidate recorded (World, Starting State, and start recipe as separate things). |
| **External inputs distinguished from reactive mechanisms** (§14) | Scope reduction for DEC-1, from external critique. A condition whose future does not depend on the simulated state is an input, not a mechanism — a recorded wind is a tape, not a second rule. The mechanically checkable test removes the easy half of the composition question from dispute; the hard half (things that change each other) remains DEC-1. |
| **Reach registered** (§15, §17, §40) | Gap closure. v0.2 never registered how far a mechanism may see or act — the question that decides where "local" stops meaning anything. Now DEC-21, open, with a leading formulation recorded: reach is authority over declared paths, never distance, and the failure mode is a mechanism touching anything it can name. |
| **Cell schema multiplicity registered; the ceiling split in two** (§13, §40) | Gap closure and refinement. Whether one World may declare several kinds of participant is now DEC-22. Separately, the quality pass found the single "computational ceiling" doing two unrelated jobs: the **semantic ceiling** is a restriction on *kind* — not a number — and is not tunable; execution budgets are counts, per deployment, at Level 3. |
| **The cellular budget** (§40, new F-23) | Standing obligation, registered as DEC-24. Four of the five properties that make this platform recognisably a local-mechanism instrument are under simultaneous, individually well-argued negotiation (DEC-1, DEC-3, DEC-21, DEC-22), and external review recommended relaxing three without noticing the aggregate. Someone must keep the ledger, and a floor must be written before those four are decided. |
| **Execution facts separated from readings** (§18.3) | Strengthening. The Reactor records facts produced by observation or comparison — *state at step 900 matched step 850* — and never conclusions — *repeating*. Names belong to versioned Readers. A wrong reading can be superseded; a wrong reading recorded inside immutable evidence cannot. |
| **Confirmation vocabulary adopted** (§30, §41, §43) | Correction. No model of a real-world system is described as *verified* or *validated* — the established argument is that natural systems are never closed and model results are never unique, so partial *confirmation* is the most that is available. A Lab's third status is **confirmed**. Basis and citation: `v3_docs/03-quality/accuracy.md` §1. |
| **The reducibility audit added as the tenth fit question** (§30.10) | Extension, from the platform's own Lab briefs. Two independently written briefs asked, unprompted and in nearly the same words, *where does this subject already have a shortcut, and where has it broken?* Irreducibility is a property of a regime, not a subject, and a Lab that cannot say which regime it is standing in has not established fit. |
| **Trust follows role, not authorship** (§6, §17) | Correction, from external critique. The first-pass reasoning — a Plugin is untrusted because a machine wrote it — does not survive a hand edit. A Plugin is variable experiment code under one contract regardless of author; a person's edit produces a new revision inheriting no privilege. |
| **The expert-reader standard absorbed** (§5) | Strengthening, set by the owner. Plain language is not simplified language: never require the reader to learn this platform's vocabulary to understand the stakes; always assume fluency in their own field. Examples are load-bearing and follow the citation rule — verified or general, never invented specifics. Standard: `v3_docs/00-start-here/language-rules.md`. |
| **Registry statuses updated; three candidates reserved** (§40) | Bookkeeping with one addition: DEC-16 and DEC-18 are narrowed; identifiers DEC-25 through DEC-27 are **reserved** for the three named unregistered candidates (exploration strategy; cost and budget; ownership of evidence), registration landing with adoption of this revision. |
| **Rendering repaired** (§35, §37, headings throughout) | Mechanical. v0.2 contained no code fences, so its two diagrams rendered as scattered paragraphs, and carried 45 headings with export artifacts. The root document of a two-hundred-document tree has to render. |
| **The documentation tree recorded as built** (§36, §37) | Status. The initial ring exists: Level 1, the twelve core documents, eight platform documents, five quality documents, and the Decision Registry in plain-question format. All draft; adoption pending. |
| **Version numbering corrected: this revision is v3.x, not v0.3** | Labeling fix, by the owner, not an amendment. The 0.x scheme was an early mistake; the Foundations of SCR 3.x carries the product line's numbering. Prior versions keep their historical labels (v0.1, v0.2) and are not retroactively relabeled. Where any document says "v0.3," it is corrected on sight — no supersede ceremony (see CLAUDE.md). |

---

## Executive summary

Semantic Cellular Ruliology (SCR) is a platform for proposing, executing, measuring, comparing, and investigating simple local mechanisms that produce larger behaviour over time.

People interact with SCR primarily through meaning. They describe a problem, a behaviour, a suspicion, a mechanism, a change, or a question in ordinary language. SCR uses language models and deterministic software to translate that intent into readable executable mechanisms, check and repair the implementation, run controlled experiments, preserve complete evidence, run repeatable analyses, and return the results in forms a person can inspect and dispute.

The purpose is not to automate people out of the process.

> **Automation is not the objective. Better allocation of work is the objective.**

Machines absorb syntax mistakes, transcription errors, repetitive implementation, bookkeeping, mechanical validation, repeated execution, exact replay, and evidence indexing — the work where fatigue and clerical error are expensive. People keep the judgment: deciding which questions matter, recognising nonsense, correcting domain assumptions, interpreting evidence, and deciding what happens next.

The word **Semantic** is an architectural constraint, not marketing. Human meaning must remain visible across the entire chain: what was asked, what mechanism was proposed, what implemented it, what experiment ran, what actually happened, what later analysis concluded, and where a person disagreed.

SCR 2.x demonstrated that the central idea works: it generates natural-language rule proposals, implements them as readable code, validates them, runs deterministic experiments, preserves immutable histories, and lets a person scrub through those histories visually. 3.x is not a larger version of that toy. It is a new product line built from what the toy proved, reconsidered from first principles — and its first ring of requirements is now written (`documents/v3_docs/`), with this document revised to agree with it.

The foundational components of SCR 3.x are twelve:

1. **Cell**
2. **World** (which owns its Layout)
3. **Generation**
4. **Plugin**
5. **Reactor**
6. **Run**
7. **Study**
8. **Reader**
9. **Corpus**
10. **Search**
11. **Visualization**
12. **Lab**

**Platform Services** support all twelve without defining any of them.

A semantic human interface governs the components rather than becoming a thirteenth subsystem. Where the work of translation actually lives is a named open decision (DEC-5), not an accident to be made during implementation.

---

# Part I — Foundational principles

## 1. Semantic first

People should normally interact with SCR through the language of the problem, not the mechanics of the implementation.

A security engineer should be able to ask:

> Test whether delayed identity updates let this account keep moving after access is revoked.

A fisheries researcher should be able to ask:

> Keep the fish behaviour the same, but increase current from the west.

A materials researcher should be able to ask:

> Find mechanisms that keep producing branching growth even when the starting defects move.

The platform may translate those requests into code, arrays, graph structures, job definitions, queries, measurements, or many experiments. Those mechanisms remain inspectable, but they are not the price of admission.

The principle applies in both directions. SCR does not accept natural language at the front and then collapse into opaque machinery. It returns meaning at every useful boundary: what was asked; what SCR understood; what mechanism it proposed; what implements it; what setting and conditions were used; what actually executed; what happened; what was measured; what a Study found; how sure the system is; and where human interpretation disagreed.

**Semantic is the continuity of meaning through the experimental chain.**

## 2. Readable and writable, always

Every generated mechanism must retain a representation a competent person can read, compare across versions, copy, change, review, and hand to another person or another machine — **without the platform's help, and without trusting the platform's account of what the mechanism does.**

That is a requirement about a property, never about a product. Which notation satisfies it today is a real decision with real consequences, and it belongs at Level 3, where it can be revisited without disturbing anything above it. (The current choice, recorded there, is an ordinary, widely readable programming language.) A concept defined in terms of one technology has a shelf life, and everything cited from it inherits that shelf life:

> **Durability that rests on a technology choice is not durability.**

The readable mechanism is not disposable scaffolding around a hidden model. It is part of the permanent experimental record. SCR may build internal optimized representations for speed or alternate execution backends; they are implementation details unless they preserve the same readability contract, and they must never silently displace the readable mechanism as the thing people are expected to reason about.

The expected modern workflow is simple:

> **The person reads the code when useful. The machine usually writes it.**

That is not "no-code." The code stays visible because visibility supports trust, auditability, learning, portability, correction, and independent review. What disappears is the assumption that people must manually type every implementation to remain in control of it.

## 3. Intent, implementation, and outcome are different facts

SCR preserves three distinct records:

- **Intent** — what the person or generator meant to try.
- **Implementation** — what executable mechanism was actually produced.
- **Outcome** — what happened when it ran under exact conditions.

They may agree. They may also disagree in interesting ways. A mechanism intended to stabilize a boundary may fragment it. A defensive access rule may unexpectedly increase how long privilege persists. A rule intended to create stationary structures may produce travellers. Those disagreements are not merely failures of classification — they are potential discoveries.

SCR therefore resists any design that overwrites one layer with another. A user correction does not erase the machine's original interpretation. A Reader's label does not become the Run. A successful execution does not prove the implementation faithfully expressed the intent.

**The gap between intent, implementation, and outcome is part of the evidence.**

## 4. The machine does mechanical work; people do judgment work

Machines preferentially handle: translating requests into proposed experiment definitions; writing routine implementations; syntax and structural correctness; contract checking; repetitive changes; test generation where appropriate; repeated Runs; exact bookkeeping; provenance capture; evidence reconstruction; deterministic analysis; search across prior work; routine reports; and presenting candidate explanations for review.

People preferentially handle: choosing important questions; supplying domain context; recognising bad abstractions; challenging assumptions; correcting semantic misunderstandings; judging whether a mechanism is plausible; judging whether a result matters; deciding whether SCR is an appropriate tool for the domain at all; deciding whether evidence warrants action; and carrying responsibility for real-world decisions.

SCR should be judged partly by how successfully it moves human time from the first list to the second — an observation about where attention went, stated modestly and never dressed up as a productivity metric.

## 5. Plain language is a system property

Code names, interface labels, stored concepts, headings, logs, and error messages use words a working engineer or a second-year student can understand without specialist mathematics. Standard technical terms may be introduced once, in an aside, where knowing them helps a reader connect to outside work; the plain name is what everything else uses.

This principle does not require SCR to avoid difficult ideas. It requires difficult ideas to be named clearly. The project's name may be pretentious; nothing else gets to be.

v3.x sharpens the rule with the standard set by the owner, in full at `v3_docs/00-start-here/language-rules.md`:

> **Plain language is not simplified language.** The readers who matter — a fire behaviour officer, a charge nurse, a network administrator, an incident responder — are experts in their fields, not in ours. Never require them to learn this platform's vocabulary to understand the stakes; always assume fluency in their own. Writing down to a professional costs the same thing as writing over their head: the reader's trust.
>
> **Examples are load-bearing.** An illustration that gets a reader's field subtly wrong costs the reader, not the illustration — in the first paragraph, permanently. Examples follow the citation rule: verified or kept general, no invented specifics for colour, every element introduced before it is relied on.

## 6. The Plugin proposes; the Reactor decides

This is the strongest principle inherited from 2.x, and it survives every architectural change in this revision.

A generated Plugin may propose state changes within its declared capabilities. It may not redefine the experiment in which it is running. The Reactor owns the actual execution semantics: state application, controlled randomness, timing, observation rules, limits, and stopping.

Two consequences drawn since v0.2:

**Trust follows role, not authorship.** The Plugin is variable experiment code; the platform is the trusted base. A Plugin satisfies the same contract whether a machine wrote it, a person edited it, a Lab shipped it, or one machine repaired another's work. A hand edit produces a new revision that inherits no admission and no privilege — the tempting alternative, trusting the human's version more, has a hole in it shaped exactly like the most confident person in the room.

**Time is not an exception to this principle; time is its hardest test.** Adversarial and operational phenomena — races, stale-observation exploits, timing side effects — live in temporal margins, and a platform that can only express perfect lockstep excludes the Labs that need them. The resolution is not to let the Plugin manage its own temporal state, which would hand the clock to the one component this principle exists to contain. Asynchrony, observation staleness, delayed effect, and interleaved application are *declared capabilities of the World and Reactor*; a Plugin may **propose** an effect with a future offset exactly the way it proposes any other change — a proposal the Reactor admits, quantizes to its own clock, orders, and counts against ordinary budgets. Scheduling proposals are writes. Writes are budgeted. There is no recursion problem, because there is no Plugin-owned clock for recursion to live in. See §18.5 and DEC-3.

This distinction is sharpest in security research. SCR must not make generated code more powerful merely because the Lab studies hostile behaviour. Attacker conditions — stale observations, partial visibility, shared resources, timing differences — are explicit capabilities of the World and Reactor. The experimental contract can model adversarial conditions; the Plugin cannot cheat the simulator, and the mechanism modelling an attacker is not an attacker (F-20).

## 7. Runs are evidence

A completed Run is an immutable historical record of what occurred under exact conditions.

Human interpretation may change. Readers may improve. Labels may be corrected. New views may reveal structure nobody noticed originally. The stored Run does not change to accommodate any of it — corrections and readings *attach*; nothing overwrites. This is what makes replay, comparison, independent analysis, and later re-reading scientifically meaningful.

v3.x adds the distinction the failure taxonomy needs: an **Attempt** is the durable record of one intention to execute, and a **Run** is an Attempt that passed admission and began executing. An Attempt refused at the door never becomes a Run — it keeps a mismatch record instead, and it is retained on the same terms as everything else, because a refusal that says precisely what was incompatible is often the most informative record in the library.

## 8. Readers read; they do not rewrite

A Reader is a deterministic interpretation or measurement of stored evidence. Readers may be wrong, incomplete, superseded, or highly domain-specific — therefore Reader outputs are versioned and reproducible, and a new Reader version may disagree with an old one without altering the Run either examined.

Three levels stay permanently distinguishable:

- **Recorded evidence** — what happened. Immutable.
- **Derived evidence** — measurements computed from it. Versioned, recomputable, disposable in the best sense.
- **Interpretation** — what a person or model believes those measurements mean. Attributed, disputable.

One reading discipline established since v0.2 is worth stating at this level: a Reader records where it worked and where it did not, and that coverage is a **map, not a grade**. A measurement that succeeds on six of ten Runs has found the boundary of the territory where that behaviour is even measurable — and the four failures are findings (`v3_docs/01-core/readers.md`).

## 9. One Run is an event; a Study tests a hypothesis

A single Run demonstrates that something happened once. It cannot by itself establish robustness, sensitivity, causation, or generality. A **Study** is the first-class object that asks a structured question across one or more Runs.

Much ordinary operational troubleshooting is already informal hypothesis testing. A systems administrator asking "does the failure stop if I isolate this network?" is changing one condition and testing a hypothesis, whether or not anyone uses that word. SCR makes disciplined experimentation easier without requiring academic theater; the word *hypothesis* is available when it clarifies, never required as ritual.

A consequence settled since v0.2: **comparability belongs to the Study, not the Run.** Two Runs are comparable *for a question* — a Repeat Test deliberately varies what a Mechanism Comparison must hold constant. The Run's duty is to expose complete bound identity and provenance; the Study's duty is to state its comparison contract: what must match, what is deliberately varied, what is irrelevant to this question (`v3_docs/01-core/runs.md` §6).

## 10. Failures stay

Negative evidence is evidence. "No result" is not one thing; the reason matters, and SCR preserves it.

The platform distinguishes seven classes, attached where they actually occur:

**Attaching to Attempts** — these happen before or at admission, and losing them because "no Run existed" was v0.2's terminology seam:

- **Proposal failure** — the proposed mechanism was invalid, incoherent, or outside the Lab contract.
- **Plugin failure** — the implementation did not validly express or execute the proposal.
- **Reactor rejection** — the mechanism attempted, or declared, something outside the declared experiment; refused at admission with a mismatch record.

**Attaching to Runs and their readings:**

- **Run failure** — execution began and could not complete reliably.
- **Behaviour miss** — execution completed; the requested behaviour was not observed.
- **Reader uncertainty** — evidence exists; the requested measurement cannot be made reliably.
- **Study failure** — available evidence did not answer the hypothesis with the required confidence or coverage. What "required confidence" means is DEC-4, and until it is decided, documents citing this taxonomy must not invent local definitions.

A system that saves only successful mechanisms creates a misleading map of what has been explored — wrong in a specific and flattering direction.

## 11. Labs own domain assumptions

The SCR core does not know what a trout, a domain controller, a flame front, a cloud role, a prompt injection, a dendrite, or a tumour is. A Lab does.

Labs contain the domain-specific assumptions, vocabulary, World templates, Readers, reference cases, fit boundaries, accuracy obligations, and known failure modes required to translate a real problem into SCR experiments. This protects both sides: the core stays coherent and reusable; each Lab can be held accountable for whether its abstraction is defensible in its domain.

No Lab earns credibility merely because someone successfully expressed its domain as Cells and Connections. Expressibility is cheap; that is why it proves nothing.

## 12. Visuals may dramatize evidence; they may never invent evidence

Visualization is not decorative output attached after the scientific work. It is one of the main ways people discover structure in time-varying systems.

2.x demonstrated the value of stored playback: a completed Run can be scrubbed backward and forward like video because the history exists independently of the interface, and multiple render styles can make different behaviour visible without changing the underlying Run. 3.x preserves and expands this deliberately.

Lighting, depth, motion, animation, camera movement, shading, trails, temporal stacking, and cinematic presentation are allowed. Fabricated movement, fabricated relationships, fabricated measurements, invented causal links, and decorative data that looks scientific but has no stored source are not.

Every meaningful visual element must be able to answer:

> **What real stored or measured data produced this?**

If the answer is unclear, the visual is not suitable for an evidence view. The complete, versioned, testable form of this contract lives at `v3_docs/01-core/visualization.md` (§26).

---

# Part II — The core conceptual model

## 13. Cell

The **Cell** is SCR's smallest state-bearing participant. It holds state and can be affected; it never acts. Behaviour belongs to the mechanism, arrangement to the World, order to the Reactor, meaning to the Lab.

A Cell may represent very different things depending on the Lab: a terrain patch, a parcel of water, an organism, a host, a user identity, a cloud role, an agent, a service, a material region. SCR does not claim these are fundamentally equivalent. The common abstraction is narrower:

> **A Cell carries state and may affect other Cells according to declared local mechanisms.**

Keeping the term Cell is intentionally restrictive. More general words — *entity*, *thing* — would make the architecture easier to stretch and its reasoning harder to police. A Lab that cannot honestly describe its participants as local state-bearing Cells may be telling us SCR is a poor fit; that is useful architectural pressure, not an inconvenience to hide.

### 13.1 The computational ceiling

The pressure above is an enforceable test, and v3.x records what writing the requirements revealed: the single "ceiling" of v0.2 was doing two unrelated jobs, which fail differently.

**The semantic ceiling is a restriction on kind, not a count:**

> **A Cell property is one of: a number, a whole number from a declared finite set, or a true/false value. Nothing else — no collections, no nested structures, no references, no embedded programs. Declared in advance, in every World, in every Lab, not tunable.**

This is what protects the platform's central claim. Behaviour that emerges from repeated local steps is only checkable as emergence if the state could not have carried the answer in. A Cell able to hold unbounded structure can smuggle a precomputed result and replay it, and no observer can tell that from discovery. If a Lab cannot express its participants this way, it fails the fit review (§30) — which keeps SCR recognisably a local-mechanism instrument rather than an unconstrained general simulator, the over-generalisation §45 asks reviewers to hunt.

**Execution budgets are counts** — properties per schema, bytes per Cell, Cells per World, total state per Run — and they are Level 3, per deployment, recorded per Run, failing as *resource* limits rather than contract violations. The two failures stay distinguishable: "the platform does not offer that" is not "this machine was too small." Both ceilings: `v3_docs/01-core/cells.md` §5.

**One question v0.2 did not ask is now registered as DEC-22:** whether one World may declare more than one *kind* of Cell. A terrain grid is honestly one kind of thing; a World of accounts, groups, roles, and resources is not, and a universal superset schema would make three of the four Layout families second-class while appearing to support them. Open, with a recorded lean toward several bounded kinds — under the semantic ceiling regardless.

## 14. World

A **World** is the complete experimental environment: which Cells exist (and, pending DEC-22, of which kinds), how they are arranged, which Connections are possible, what conditions apply, what is observable, and which execution capabilities the experiment requires.

A person should be able to request a World semantically —

> A coastal grid with a west-to-east current, one rocky boundary, and warmer shallow water near shore.

— and SCR converts the description into an exact stored World that remains inspectable.

**The World owns its Layout.** How Cells are arranged and which local interactions are possible is a property *of* the experimental environment, never a sibling concern to be mixed and matched against it. This subordination makes incoherent pairings — a trust-relationship world governed by a spatial distance metric — impossible by construction: there is no independent slot for a Layout that contradicts its World.

**A World may require an execution capability; it may never provide one.** Requiring delayed observation is a statement about what this experiment needs. Supplying it is execution, and execution has one owner (§18).

Three matters at this boundary, sharpened since v0.2:

**External inputs are not mechanisms.** The example above contains a *current* — and the useful cut is not what kind of thing it is but what its future depends on. A value or schedule declared in advance whose future does **not** depend on the simulated state — a recorded wind played back, a fixed tide table, a scheduled credential expiry — is an **external input** and belongs to the World. Anything whose future behaviour depends on the simulated state is a **mechanism**, whatever it is named. The test is mechanically checkable, and it removes the easy half of DEC-1 from dispute; the genuinely coupled cases — fire altering the wind that drives it — remain DEC-1's open question.

**Who owns the starting state is a named fork, not a settled fact.** v0.2 placed the starting state inside the World; the demonstrated 2.x system had the mechanism generate it. Both readings cannot stand, because a Mechanism Comparison that lets each mechanism set up its own board has compared nothing. This is now **DEC-23**, open, with a leading candidate recorded: the World (the durable setting), the **Starting State** (the realized opening values, recorded exactly), and the **start recipe** (a described procedure a mechanism or Lab may supply) as three separate things, with the recipe executed under the Reactor's controlled randomness and both recipe and realized values bound to the Run.

**Observation has three states that must never be conflated.** **World State** — what is actually true. **Seen State** — what a given participant is permitted to observe at that point: possibly partial, delayed, filtered, role-dependent. **Recorded State** — what is captured as evidence: complete enough for replay and for measurements invented later, never limited to what any participant could see. A mechanism reads Seen State and only Seen State. This is what lets SCR model stale identity data, delayed telemetry, and partial attacker knowledge honestly — as declared properties of the setting, never as extra freedom for the mechanism (`v3_docs/01-core/worlds.md` §6).

## 15. World Layout (a property of the World)

The **Layout** describes how a World's Cells are arranged and which local interactions are possible. A Connection is a *declared possibility of local interaction*, not a distance.

Initial layout families:

- **Grid World** — interactions follow physical position or another meaningful lattice.
- **Network World** — interactions follow communication or reachability connections.
- **Identity World** — interactions follow trust, role membership, delegation, inheritance, or permission relationships.
- **Agent World** — interactions follow messages, tools, memories, shared resources, and delegated work.

These are starting families, not a promise that every domain fits one of four boxes. **Only the first has ever been built.** Everything the platform currently believes about arrangement, connection, and reach is better tested against a lattice than against the three families where most intended Labs live — a statement about earned confidence that travels with these requirements.

The key requirement is that a Plugin can affect only what the World's Layout and declared Connections permit. **How far that permission extends is now registered as DEC-21** — v0.2's largest unregistered gap. Real subjects keep producing honest exceptions to nearest-neighbour interaction: embers lofted ahead of a fire front, sand hopping past its neighbours, seeds carried far from the parent, processes that scan rather than spread. The leading formulation, recorded and not adopted: reach is **authority over declared paths, never distance** — a long jump is legitimate where the World declares the transport, and the failure mode at any distance is a mechanism touching a Cell merely because it knows it exists. (§45.12's over-generalisation hunt gets its measuring line from this decision and from DEC-24.)

3.x must not inherit 2.x's fixed square wrap-around grid merely because it was convenient for the toy. Nor may "World" generalize into an unconstrained simulation language with no local-mechanism discipline. That boundary is revisited explicitly as Labs mature — and counted, in aggregate, under DEC-24.

## 16. Generation

**Generation** turns semantic intent into a tested candidate Plugin. It is a pipeline, not merely a model call:

> **Propose → Write → Check → Test → Repair → Deliver**

- **16.1 Propose.** Interpret a request, Lab goal, search gap, or exploration objective, and state a simple local mechanism in ordinary language — a permanent record separate from any implementation.
- **16.2 Write.** Produce a readable implementation satisfying §2, with the complete declarations §17 requires.
- **16.3 Check.** Verify structure, permitted capabilities, declared reads and writes, and the semantic ceiling, before anything expensive runs.
- **16.4 Test.** Execute controlled validation Runs sufficient to catch implementation defects, non-reproducibility, and contract violations — at real scale, not a reduced one.
- **16.5 Repair.** Where a failure is mechanical, a bounded number of governed attempts to fix the implementation without changing the proposed mechanism. Repair preserves the whole chain: original proposal, original implementation, failure, repair instruction, repaired implementation, final result — nothing overwritten by what came after.
- **16.6 Deliver.** Hand the validated candidate and its complete provenance onward. Delivery is not endorsement.

**A repair owes the person meaning, not just a difference listing.** Requiring someone to read code changes line by line to verify a repair preserved the mechanism is a semantic leak — the failure §1 forbids. Every repair therefore carries a plain-language account of what changed mechanically ("the neighbour count now excludes the cell itself; nothing else changed"). One caveat attaches permanently: that account is produced by the same class of machinery that produced the repair — the machine grading its own homework. It is classified as **interpretation** — versioned, disputable, Reader-class — never as evidence the repair was faithful. The change itself remains the evidence; the account is how a person decides whether to look closer.

Generation's checks are a **preflight, never a substitute for admission** (§18): "Generation checked it" must never become "therefore the Reactor may assume it was checked." And Generation remains a proposal system — it does not get to declare a mechanism scientifically useful because it successfully wrote code.

## 17. Plugin

A **Plugin** is the readable implementation of one local mechanism — deliberately smaller than the full experiment.

It may: read declared state through the views it is permitted; inspect declared local connections; calculate proposed next state; use explicitly provided helper capabilities; and return proposed changes — including, where the World declares temporal capabilities, changes proposed for a future offset (§18.5).

It may not independently own: random sources not supplied by the Reactor; execution ordering; global time semantics; observation freshness; access to any Cell it was not given a path to; stopping criteria; immutable history; provenance bookkeeping; or hidden mutable state the experiment has not declared — that last one may simply not exist, because undeclared state is invisible to the stopping logic, and a Run could be declared finished while something was still changing.

**One contract, every author.** A Plugin is variable experiment code whether a machine wrote it, a person edited it, a Lab shipped it, or one model repaired another's work (§6). A direct edit produces a new revision inheriting no admission and no privilege, and leaves the recorded intent *stale until confirmed* — with both the previous intent and the new unconfirmed implementation preserved (DEC-18, narrowed).

The exact capability set is DEC-7's question, deliberately sequenced after DEC-1 and DEC-3. The conceptual line does not move:

> **The Plugin expresses the local mechanism. The Reactor expresses the laws of the experiment.**

## 18. Reactor

The **Reactor** is SCR's deterministic execution authority. The name is intentional: Plugins enter the Reactor under controlled conditions; the Reactor is where state transitions actually occur and evidence is produced.

The Reactor owns: state application; step or event ordering; controlled randomness; timing semantics; observation delay and visibility; shared-resource side effects; derived state the experiment requires; runtime limits and budgets; stopping; exact replay requirements; evidence capture boundaries; and version identity for execution semantics.

**Admission is the Reactor's, and it is authoritative.** Before execution, the Reactor performs the match — what the World offers, against what the Plugin requires, against what this Reactor supplies. A successful match produces the frozen **Run Contract** (§19); a failed match produces a retained mismatch record that says precisely what was incompatible. Anything checked earlier was checked against an earlier World, Reactor, or revision; only the component that will actually execute the mechanism has an assessment that cannot be stale.

### 18.1 The Reactor is not the Lab

It does not know that a connection is "credential trust" or that a value is "fuel moisture." Meanings belong to Labs and Worlds.

### 18.2 The Reactor is not Generation

It does not invent mechanisms or repair implementations.

### 18.3 The Reactor is not a Reader

The Reactor records **execution facts** — produced by observation or comparison, incapable of being wrong later: *the state at step 900 matched the state at step 850; no accepted proposal changed future-relevant state; the step budget was exhausted; an execution error occurred.* It never records **conclusions** — *settled, repeating, oscillator, stable* — which are readings, belong to versioned Readers, and can be disagreed with later without disturbing the evidence. The asymmetry is the reason: a wrong reading can be superseded; a wrong reading recorded inside immutable evidence cannot. This also preserves the 2.x lesson that a quiet picture does not mean a settled computation.

### 18.4 Security posture

The generated-code execution boundary is an explicit contract *and* an execution-safety problem, and the two are never confused: the contract says what a mechanism may do; the boundary is what holds when the contract fails, and it assumes the code it contains is hostile regardless of authorship. Adversarial Labs must not be allowed to use the research subject as justification for a permissive execution surface — the pressure will arrive well-argued, from legitimate Labs, one case at a time, and the answer does not change with the quality of the argument (F-20; obligations at `v3_docs/02-platform/execution-safety.md`; mechanism open as DEC-16, narrowed).

### 18.5 Time semantics are a Reactor capability

The Reactor may support execution models beyond synchronous lockstep — discrete-event ordering, declared observation staleness, delayed effect application, deterministic interleaving. Where a World declares such capabilities, they remain Reactor-owned in every respect: the Reactor's clock is the only clock; scheduled proposals are quantized to its resolution, admitted under the same contract as any other proposal, and counted against ordinary budgets. Determinism and exact replay are non-negotiable properties of every model offered.

Timing is experimental semantics, not an implementation preference — the field's own literature shows update timing can manufacture apparent structure from the same rule, which settles the ownership question by itself (cited at `v3_docs/01-core/reactor.md` §6.1). Which models are offered, to which Worlds, under what budgets, is DEC-3's open remainder.

## 19. Run

An **Attempt** is the durable record of one intention to execute. A **Run** is an Attempt that passed admission and began: one exact execution, recorded permanently, never edited. The Run is where every other component's identity meets — which makes it the one place that can notice when anything changed.

**The Run Contract.** At admission the Reactor freezes the complete agreement: the World's execution identity; the Starting State and the recipe that produced it; every participating Plugin by revision, with its full declarations; the composition policy where more than one mechanism participates; the Reactor's version and execution model; the derived values undertaken; all budget limits; the replay promise; and the resolved match itself. The Run stores it forever, and no later reader is ever required to reconstruct what a Run was permitted to do by inspecting the platform as it exists at the time of reading. Evidence that cannot state its own terms is evidence about nothing in particular. (Full contents: `v3_docs/01-core/runs.md` §2.)

**Two replay promises — DEC-2, decided 2026-08-21.** v0.2 posed "exact or contractually equivalent reconstruction" as a fork to choose. It is two promises that coexist under separate names, never silently exchanged:

> **Exact replay** — with the archived implementation, build, environment, random material, Starting State, and Run Contract, the recorded state reproduces value for value. The strongest forensic claim, and the most expensive, because it archives the environment and not merely the inputs.
>
> **Reproduction under contract** — a later Reactor executes the same declared experiment and meets a stated, versioned equivalence standard. The claim that survives time, because software changes and evidence is meant to outlive it.

The decided boundary: reproduction under contract is the default for every Run; exact replay is reserved for Runs **designated evidence-grade at run time** — never retroactively, because an environment not archived when the Run executed can never be archived later. Designation, alternatives, and reopening triggers: DEC-2's record.

**The 2.x decision to complete a Run before playback remains the default conceptual model.** Playback is navigation over immutable history, never a live simulation coupled to the interface. That buys instant scrubbing; backward stepping without undo machinery; repeatable views; many visual styles over one history; Readers that did not exist when the Run was recorded; and reproducible reports and video from exactly the same evidence. Future products may need live operational views; those must never erase the line between a live stream — provisional, and marked provisional at the moment of observation — and the finalized immutable Run (DEC-19).

## 20. Study

A **Study** is a structured question that requires one or more Runs — the object that packages disciplined experimentation in language practitioners already use.

> Does the same compromise path work from five different developer identities?
> Which single access change prevents administrator privilege?
> Does the walker still travel when the starting position changes?
> At what wind range does this front stop branching?
> Is the result robust to a different random starting state?
> Which of these three mechanisms best reproduces the observed behaviour?

### 20.1 Initial Study patterns

**Repeat Test** — same mechanism across different permitted starting conditions. **Small-Change Test** — change one declared condition; observe what later evidence changes. **Try Many Settings** — vary declared settings systematically under a stated protocol. **World Comparison** — hold the mechanism constant; compare settings. **Mechanism Comparison** — hold the World and protocol constant; compare mechanisms (valid only where the Starting State is separable from the mechanism — DEC-23's stake in every comparison).

### 20.2 Study as hypothesis machinery

A Study states, in plain language: the question; the hypothesis where useful; what is held constant; what is varied; what evidence would support or weaken it; which Runs were performed; which Readers were used; what was found; and what remains uncertain. It also states its **comparison contract** — which fields must match, which are deliberately varied, which differences are irrelevant to this question — because comparability is relative to a question and the Run merely exposes the identity that lets the Study check it (§9).

Users need not formulate formal hypotheses. SCR can propose them from ordinary troubleshooting language — and always shows the proposed question, hypothesis, and comparison contract for confirmation before anything runs (DEC-9 owns how much is inferred first). Rigorous without being pompous.

### 20.3 Study's inference discipline is owned, and deliberately modest

The failure taxonomy and the machinery above lean on an undefined phrase — "required confidence" — owned by DEC-4. This document constrains whatever DEC-4 decides: **Study's statistical stance is modest and plainspoken** — counts, proportions, distributions, and paired comparisons, in ordinary language, with what was *not* tested stated alongside what was. Significance theater, invented precision, and confidence numbers nobody can trace to a computation violate §5 and §43 at once. A Study that says "19 of 20 starts produced a traveller; the one failure started inside the obstacle" has said more, more honestly, than one reporting a significance figure against an unstated comparison — a caution the professional statistics bodies themselves publish (cited at `v3_docs/01-core/studies.md`).

One capability deserves its positive statement: a Small-Change Test, run against a sample of comparable changes, measures the Run's **ambient sensitivity** — and uniform sensitivity is a *finding*, not a failed measurement. A system that diverges from any small change is a system with no shortcut, which is the property this platform's whole value rests on, measured directly from evidence already recorded (§25.3 carries the presentation duty).

## 21. Reader

A **Reader** examines completed evidence and produces a reproducible measurement or derived interpretation.

Platform-neutral Reader examples — the kind the core may reasonably know about: spread; movement; branching; persistence; recurrence; stationary structure; traveller detection; front speed; persistence of state that is not visible.

Lab-supplied Readers carry domain meaning the core never learns. *Illustrations only, owned entirely by their Labs:* a security Lab might define compromise-spread or privilege-reached Readers; an ecology Lab might define schooling-cohesion Readers. Their definitions, vocabulary, accuracy obligations, and failure modes live in Lab papers (§29–§30), and nothing about them belongs in core documents. This separation is policed deliberately, because v0.1 mixed the two lists — and in a mostly machine-written tree, downstream documents reproduce whatever mixing the root document models.

A Reader identifies at minimum: name; version; settings; exact evidence examined; output; and completeness or confidence where applicable. A Reader result is disposable in the best sense — deletable and recomputable from immutable evidence without changing history. Readers must not become invisible truth layers: every assertion a person sees names the Reader and version that produced it, important claims trace to underlying evidence, and uncertainty appears with the result, in ordinary language, not in documentation nobody opens (DEC-10 owns the presentation).

## 22. Corpus

The **Corpus** is the durable body of SCR evidence and meaning. It is not synonymous with the database: a database is an implementation choice; the Corpus is the asset the implementation protects.

The Corpus links: requests; proposals; implementations and revisions; Worlds and Starting States; Attempts and Runs with their Run Contracts; Study definitions and findings; Reader outputs by version; failures of every class; repairs with their semantic accounts; model identity and rendered inputs; Reactor versions; Lab versions; human corrections; annotations; and relationships among related mechanisms.

Two principles proven in 2.x survive unchanged: the individual mechanism matters less than the accumulated library connecting intent, implementation, trajectories, measurements, failures, ancestry, and corrections; and operational telemetry is conceptually different from permanent experimental history — a distinction that survives any storage arrangement.

### 22.1 The 2.x corpus is founding evidence

The existing 2.x library — rules, runs, failures, provenance — is **carried forward into the 3.x Corpus as founding evidence**: not archived, not orphaned, not a separate lineage. It is small at the time of writing, and a deliberate scale-up by orders of magnitude is planned, which is why migration runs before the scale-up — against tens of Runs it is an afternoon; after, a project.

What carries forward is decided. *How* is DEC-6's open remainder: identifier mapping, cross-version comparability, and which derived data is recomputed under 3.x Readers versus preserved as historical readings (where recomputed, both are kept, each attributed to its version). The constraint on every answer: migration never rewrites 2.x histories (§7).

## 23. Search

**Search** turns accumulated evidence back into useful work. It is what a platform does where derivation is unavailable: you cannot compute the mechanism that produces branching, so you find one that did. The long-term product is not a gallery of simulations; it is a searchable catalog of mechanisms, evidence, and failed attempts.

> Show me simple mechanisms that produce branching fronts.
> Find mechanisms that unexpectedly increased privilege persistence.
> Find cases that behave like this uploaded pattern.
> Show mechanisms with similar observed behaviour but very different stated intent.
> Which mechanisms survive Repeat Tests across the most starting conditions?
> Find experiments where adding containment made the outcome worse.

Three similarities are kept permanently distinct, never blended into one score: **intent** (meant to do the same), **mechanism** (built the same), **observed behaviour** (acted the same) — because the most valuable queries live in the gaps between them, and a single relevance score destroys exactly those queries while looking better in a demonstration (DEC-12). Any cluster or neighbourhood shown to a person names the similarity measure and data that made it; proximity on a screen is evidence of a computation, not of a relationship.

The query language exposed to ordinary users remains semantic even where structured search also exists. And Search covers what the platform has explored, never the space of possible mechanisms: an empty result is a fact about the library, not about the world (§42).

---

# Part III — Visualization as evidence instrumentation

## 24. Visualization is its own vertical

Visualization deserves a first-class architecture rather than treatment as a styling concern. The reason is scientific before it is commercial: cellular and local-rule systems are fundamentally temporal, and their behaviour often cannot be understood from a final frame or a summary number. People discover structure by watching movement, persistence, recurrence, branching, clustering, fronts, boundaries, and transitions over time — including structure no existing measurement was written to detect.

2.x demonstrates the foundation at small scale: completed Runs play, pause, step, and scrub, with render styles applied over one immutable history. Where a planning document additionally *specifies* styles beyond what is demonstrably built, the two are kept distinct — build status is a repository fact this document does not assert.

### 24.1 Time navigation is foundational

Every visual Run experience assumes time is directly navigable: slider scrubbing; frame stepping; play and pause; jump-to-event where Readers identify events; comparison of two points in time; visual marks for Study and Reader findings; and stable references to exact moments.

The slider is not merely a playback control. It is an experimental instrument — the thing a person searches a Run with.

### 24.2 Styles are lenses, not alternate realities

A single Run may support many render styles — kind colouring, activity emphasis, changed-cell highlighting, stationary-structure emphasis, traveller emphasis, trails, relief, hidden-state views, connection activity, observation delay, Reader overlays. All derive from the same stored evidence or versioned Reader output.

The architectural test:

> Can this style be applied later to an old Run without re-running the experiment?

Yes: it is probably a true evidence view. No: the system states explicitly what new information or execution it requires — a style that quietly re-executes to render itself is producing new evidence and calling it a display option.

## 25. High-value 3D Views — roadmap candidates, not commitments

SCR explicitly supports a future advanced visualization program. It is not a day-one requirement, but the architecture avoids decisions that would make it prohibitively expensive later — which is a storage-format question with a deadline (DEC-13), because records are written once and read forever.

**Everything in this section is a candidate.** A downstream document may cite these as prior discussion, never as commitments.

- **25.1 3D World View.** Cells and Connections become navigable geometry; state is represented through evidence-backed position, size, height, opacity, material, motion, or light. A Network or Agent World becomes a spatial representation of propagation; a Grid World becomes a surface or volume.
- **25.2 Time View.** Time mapped into a spatial dimension: a persistent stationary pattern becomes a column, a traveller a diagonal path, a branching front branching geometry, oscillation repeated structure — temporal behaviour as an object inspectable from multiple angles.
- **25.3 Influence View.** A Small-Change Test rendered as an expanding divergence volume derived from actual paired-Run evidence. **This view carries the document's sharpest deception risk, and the remedy is context, never censorship.** In a strongly sensitive system *any* change produces an expanding divergence; rendering one flip's cone alone invites the reading that the flip was special. A gate that refuses to render is worse — derived analysis suppressing measured evidence is the invisible truth layer §21 forbids. So: any specific divergence is presented against the Run's **ambient sensitivity** (§20.3), uniform sensitivity is itself reported as the finding, and within paired deterministic Runs the divergence itself is honestly counterfactual — everything in the cone differs because of the change; what needs context is only the implied claim that the change was *special*.
- **25.4 Study View.** Many Runs from one Study compared in one visual environment: outcome families, failures, robust regions, outliers.
- **25.5 Behaviour Map.** Try Many Settings as a terrain whose geometry represents measured outcomes; every coordinate traces to actual settings and Reader results.
- **25.6 Corpus View.** Mechanisms positioned by semantic and measured similarity — the most marketing-friendly concept and the easiest to abuse. Any "galaxy," cluster, distance, or neighbourhood states what similarity measure created it and from which data (§23).

## 26. Visualization truth contract

Advanced presentation may be cinematic. The truth contract remains strict: for any significant visual property, the system can identify its source.

**The normative version of this contract — complete, versioned, and testable — lives at `v3_docs/01-core/visualization.md`,** where a visual property is added to the table *before* it is rendered. The shape, by illustration: position from Layout or a named deterministic placement; height from a stored value or Reader measurement; a drawn connection from a declared connection or recorded interaction; trails from stored positions over time; glow from a named normalisation of stored activity; animation from ordered stored states; a divergence volume from measured paired-Run difference with its ambient-sensitivity context; cluster placement from a named similarity calculation.

The visual system may transform evidence for legibility — scale, smooth, exaggerate, pace. It may not imply data that do not exist. Where a view exaggerates, the exaggeration is stated; the measure is the old, simple one — the size of the effect shown against the size of the effect in the data. This is what lets SCR pursue spectacular presentation without degrading scientific credibility.

## 27. Reporting

Reports are a baseline capability, not a stretch goal. A Study or important Run can produce: an interactive report; a printable and exportable report; a machine-readable evidence export; and stable references to the exact Runs, Readers, and settings behind every claim.

A report distinguishes clearly among: question or hypothesis; experimental setup; mechanism; results; Reader-derived measurements; human interpretation; uncertainty; limitations; and provenance. Reports reuse the same evidence and visualization contracts as the interactive product — never a separate narrative truth.

## 28. Stretch goal: automatically generated short-form Study videos

A future SCR generates concise video summaries directly from real Run and Study data — worth designing for now because trustworthy automated video overlaps almost entirely with good provenance and visualization design.

A generated video might: identify the Study question; show the initial World; animate the relevant portion of one or more Runs; switch views where a different lens reveals an event; pause at Reader-detected findings; compare baseline and changed Runs; display evidence-backed annotations; state outcome and uncertainty; and end with identifiers for the full Study.

The crucial requirement is the same as for all visualization:

> **The video edits evidence. It does not fabricate a story.**

Narration, captions, camera selection, pacing, and emphasis may be generated. Claims and depicted behaviour must trace to real Run, Study, Reader, or World data — and the ambient-sensitivity context of §25.3 applies to video exactly as to the interactive view. A forty-second clip is the artifact most likely to travel without its Study attached; that is its value and its hazard, and the provenance welded to it (DEC-14) is what bounds the hazard.

---

# Part IV — Labs

## 29. Lab

A **Lab** is a problem-focused working environment built on SCR — where domain meaning enters the platform, and where it is held to account.

A mature Lab may define: domain vocabulary; semantic translation rules; World templates; Cell property meanings; Connection types; permitted starting conditions; allowed or discouraged mechanism patterns; Lab-specific Readers; recommended Study patterns; reference cases; benchmark data where available; fit criteria; accuracy expectations; known abstraction failures; known non-goals; example hypotheses; reporting conventions; and visualization presets appropriate to the domain.

The Lab collection is expected to grow — a catalog of candidates exists in the tree, and presence in it is not fit.

## 30. Every Lab must earn its fit

Each serious Lab receives its own review package, answering **ten** questions. A Lab may fail, and a rejected Lab is useful evidence about SCR's boundary — recorded and kept.

- **30.1 Domain fit.** Why is local interaction a defensible abstraction here?
- **30.2 World fit.** What does a Cell represent? A Connection? What important relationships are lost? Does the state pass the semantic ceiling (§13.1)?
- **30.3 Mechanism fit.** Which domain mechanisms can be represented as local mechanisms, and which cannot?
- **30.4 Time fit.** What does one step mean? Is synchronous stepping meaningful? Are delayed observations or event semantics (§18.5) needed?
- **30.5 Evidence fit.** Which Readers correspond to meaningful domain measurements?
- **30.6 Accuracy.** Which reference cases, known systems, synthetic benchmarks, or external datasets can test whether the Lab behaves plausibly?
- **30.7 Failure boundaries.** Under which conditions would SCR produce a visually convincing but scientifically misleading result — stated concretely: which regime, which visual, which reading a viewer would plausibly take?
- **30.8 Comparison to established tools.** What already solves this better? Where is SCR complementary rather than duplicative — argued, not asserted?
- **30.9 Transfer limits.** If a simple mechanism resembles observed behaviour, what additional validation is required before treating it as a real-world hypothesis?
- **30.10 The reducibility audit.** *Where does this subject already have a shortcut, and where has the shortcut broken?* Named separately, per regime: the regimes with a closed-form or otherwise reducible answer — where SCR would laboriously rediscover textbook content, useful as calibration and worthless as contribution — and the regimes where the only way to know is to run it. Irreducibility is a property of a *regime*, never of a subject; the same subject routinely has both, and a Lab that cannot say which regime it is standing in has not established fit. *(New in this revision. Two independently written Lab briefs asked this question unprompted, in nearly the same words — the strongest available evidence that a review missing it is missing something practitioners reach for anyway.)*

Lab status is a ladder — **candidate** (named), **experimental** (reviewed, in use, accuracy not established), **confirmed** (accuracy evidence against stated reference cases, to a stated extent) — climbed by recorded human acts, never by repetition of an inherited standing. The evidence threshold for the top rung is DEC-15. *Confirmed* never means the abstraction is correct for its subject (§41).

---

# Part V — Human correction and provenance

## 31. Human corrections are first-class evidence

People are not merely consumers at the end of the pipeline. A domain expert may say:

> That trust direction is backwards.
> Those are disconnected bursts, not one propagating front.
> The fish would never observe that variable directly.
> This Reader is counting retry storms as compromise spread.

SCR preserves: the original machine proposal or interpretation; the correction; the reason where provided; the resulting change; who or what supplied it; and which later Runs, Studies, or Reader results depend on it.

A correction never silently rewrites history — the platform makes disagreement inspectable, because a record showing only the final agreed answer has discarded what a later reader most needs: that the question was once open, who closed it, and on what grounds. A person's correction is itself evidence of expert disagreement, not automatically the truth; what the platform guarantees is that both positions survive, attributed, with their reasons.

## 32. Provenance should be boringly complete

Every important result traces to the inputs and software that produced it. The conceptual chain: the request or generation objective; **fully rendered model inputs, stored — never reconstructed later from templates that may have changed**; model identity and relevant parameters; raw model outputs where appropriate; the proposed mechanism; the implementation source and revision; repair history including each semantic account (§16.5); validation results; World and version; **the Run Contract**; Reactor version; Run settings; seeds or controlled-randomness state; Reader identity and version; Study definition; human corrections; and the versions of any report or view that made an interpretive claim.

The system is designed so future reviewers can distinguish *"we cannot reproduce this because the model is stochastic"* from *"we failed to record what we asked the model."* The first is an honest limitation of the world; the second is a platform defect, and it must never be reported as the first.

### 32.1 Evidence integrity lives in the record, never in the data

When evidence leaves SCR — exports, reports, machine-readable bundles, downstream pipelines — its origin and integrity are protected by **cryptography over the record**: content addressing, hash chains over immutable histories, and signed export manifests. Boring, standard, and correct.

What is permanently rejected is the alternative that periodically sounds clever: embedding provenance *into the experimental data itself* — watermarks, statistical residues, steganographic signatures woven into Cell state. In a platform whose scientific premise is sensitive dependence on state, modifying state to carry metadata corrupts the experiment in order to sign it; the signature would be made of altered evidence. And no such embedding both survives arbitrary lossy transformation and constitutes cryptographic proof — those are different, largely incompatible goals. If a downstream pipeline strips record-level provenance, the honest answer is that provenance was stripped, not that the data secretly still contains it.

**State data is evidence. Evidence is never modified to describe itself.**

---

# Part VI — Platform services

## 33. Platform Services

Conventional software infrastructure supports the conceptual platform and must not define its scientific assumptions accidentally.

Platform Services include: jobs and workers; persistent storage; object storage where needed; the service interface; identity and authorization; execution isolation and resource control; transport; frontend delivery; observability; configuration; backup and recovery; deployment; and migration and version management. Each now has its own requirements document under `v3_docs/02-platform/`, and for testable detail those documents outrank this one (§36.4).

The 2.x product deliberately used a simple local architecture: a single-file embedded database, synchronous generation over one streamed request, local execution, a browser frontend. Those choices were appropriate for the toy and are treated as **evidence, not constraints** on 3.x. The conceptual contracts in this document remain meaningful if the implementation later uses queued jobs, distributed workers, a server database, object storage, or accelerated rendering — that survivability is itself a stated requirement of the storage design.

Two Platform-Services boundaries earned foundational statement since v0.2: **an infrastructure retry is not a Run failure** — the line is admission, and scheduling never touches experimental semantics; and **operational telemetry never becomes evidence by being stored nearby** — the crossing rule is whether an event touched an experiment's outcome.

---

# Part VII — Conceptual boundaries

## 34. Component ownership map

**Cell** — owns: local state-bearing participation, under the semantic ceiling. Does not own: domain meaning, execution order, global behaviour, behaviour of any kind.

**World** — owns: the experimental environment — Cells and their kinds, Layout, Connections, conditions, observability, external inputs, required capabilities. Does not own: the mechanism, the realized Starting State (DEC-23, open), interpretation of results, or any execution capability it requires.

**Generation** — owns: propose, write, check, test, repair (with its semantic account), deliver. Does not own: execution truth, admission, or scientific validity.

**Plugin** — owns: the readable implementation of one local mechanism, under one contract regardless of author. Does not own: experimental law outside its declared capabilities — including the clock, and including any Cell it can merely name.

**Reactor** — owns: execution semantics and authoritative state transitions; the authoritative admission match that produces the Run Contract; every declared temporal capability; execution facts. Does not own: domain meaning, mechanism repair, or the *names* of outcomes — those are readings.

**Run** — owns: the immutable history of one exact execution, and the frozen Run Contract it was admitted under; an Attempt owns the record of an intention that may never have become a Run. Does not own: claims of robustness or causation, measurement, comparability, or its own correction.

**Study** — owns: the structured multi-Run question, its comparison contract, and a modest, plainspoken inference stance. Does not own: domain truth beyond the evidence it actually collected.

**Reader** — owns: reproducible derived measurement or interpretation, versioned, with its coverage map. Does not own: the underlying history, or the right to become invisible.

**Corpus** — owns: durable relationships among meaning, mechanisms, evidence, failures, and corrections — including the carried-forward 2.x library as founding evidence. Does not own: operational telemetry merely because it is stored somewhere.

**Search** — owns: retrieval across the Corpus, with three similarities kept distinct. Does not own: generation, execution, or the claim that absence of evidence is evidence of absence.

**Visualization** — owns: evidence-backed visual representations, the truth contract, and time navigation. Does not own: fabricated scientific claims, or the right to render what has no stored source.

**Lab** — owns: domain assumptions, vocabulary, fit, accuracy, specialized Readers and Studies, its own non-claims. Does not own: core execution semantics, any relaxation of the contract, or vocabulary inside core documents.

**Platform Services** — own: reliable operation of the product. Do not own: the conceptual scientific model, or any decision that quietly becomes experimental semantics.

## 35. Conceptual flow

A simplified mental model — not a call graph, not a package structure; the map people should be able to hold in their heads:

```
                        PERSON
                          │
                   ordinary language
                          │
                          ▼
                         LAB
                          │
         translates domain meaning into SCR concepts
                          │
         ┌────────────────┼──────────────────────┐
         ▼                ▼                      ▼
       WORLD          GENERATION              READERS
                          │                      ▲
                    propose / write              │
                    check / repair               │
                          │                      │
                          ▼                      │
                       PLUGIN                    │
                          │                      │
              admission → Run Contract           │
                          │                      │
                          ▼                      │
                       REACTOR                   │
                          │                      │
                          ▼                      │
                         RUN ────────────────────┘
                          │
                          ▼
                        STUDY
                          │
                  ┌───────┴────────┐
                  ▼                ▼
               CORPUS        VISUALIZATION
                  │                │
                  ▼                │
                SEARCH             │
                  │                │
                  └────────┬───────┘
                           ▼
                        PERSON
```

---

# Part VIII — The document system

## 36. Documentation hierarchy, authority, and lifecycle

Roughly two hundred documents are expected in this tree, most written by language models under human direction. That changes the failure mode: a human-written tree drifts at the leaves; a model-written tree drifts at the **root**, silently, one plausibly-interpreted ambiguity at a time. The hierarchy therefore carries not just levels but citation, precedence, and amendment discipline — and since v0.2, the machinery has been exercised for real: documents have been amended with prior wording preserved, forks have been caught being resolved locally and reverted to citations, and one registry record has been decided by the owner.

### 36.1 Document classes

- **Level 1 — Foundations.** What the system is and what major concepts mean. This document, and the four orientation documents in `v3_docs/00-start-here/`.
- **Level 2 — Architecture Decisions.** Records of consequential choices: alternatives, reasoning, reconsideration triggers. The Decision Registry (§40) is the index; every record leads with its question in plain language and preserves the precise wording other documents cite.
- **Level 3 — Requirements.** Stable, testable contracts with permanent identifiers. The practice proven by the 2.x omnibus continues: identifiers are never reused, retirements are recorded, rationale travels with the requirement. The 3.x tree reserves per-document namespaces (`CELL-`, `WORLD-`, `PLUGIN-`, `REACTOR-`, `RUN-`, `STUDY-`, `READER-`, and so on).
- **Level 4 — Technical Deep Dives.** Implementation-level descriptions of each subsystem as built. Written as building happens; none exist yet for 3.x, deliberately.
- **Level 5 — Lab Papers.** Domain-specific fit, accuracy, limitations, references, benchmarks, and evidence, in `v3_docs/labs/`.
- **Level 6 — Operations and User Documentation.** Deployment, administration, interface use, Lab operation, human workflows.

**Levels 1 and 2 name no technology** — no language, library, database, or vendor. A foundational statement that cannot be made without one is a requirement wearing the wrong clothes and belongs a level down, where it can be revisited without disturbing anything above it. Level 3 and below name technology freely, and mark inherited 2.x choices as evidence rather than requirements.

### 36.2 Citation

Documents cite each other by stable identifier, never by prose paraphrase alone. This document is cited as **SCR-F**, with version and section: `SCR-F v3.x §19`. The condensed rules carry permanent identifiers **F-1** through **F-23**. Decision records are **DEC-n**. Requirements identifiers are permanent within their reserved namespaces, and a document writing into a shared namespace declares its reserved block.

Citations to external literature are **verified against the published source before use, never recalled** — in a mostly machine-written tree, a fabricated citation is the most damaging thing a document can carry: confident, specific, indistinguishable from diligence until the one reader who checks arrives. Where a detail is from memory, the text says so at that point. The tree's requirements documents carry their verified external citations; Foundations remains deliberately citation-light.

### 36.3 Status lifecycle

Every document carries exactly one status: **draft** (open to change without ceremony), **in review** (circulating for critique), **adopted** (downstream documents may rely on it), **superseded** (replaced by a named successor), or **withdrawn** (retired without successor, reason recorded). Model-written documents enter as drafts and cannot self-promote; **adoption is a human act** — and silence is not adoption, nor is time passing. This revision enters as a draft, exactly per this rule.

### 36.4 Precedence

When documents conflict:

1. For **conceptual meaning** — what a component is, what it owns — Foundations outranks everything, and a newer adopted Foundations version outranks an older one.
2. For **decided questions**, the governing DEC record outranks any document's local phrasing, including this one's.
3. For **testable contract details**, the owning Requirements document outranks Foundations; if honouring a requirement would violate a foundational principle, that is not a local judgment call — it triggers amendment.
4. A conflict between adopted documents is a defect in the tree: recorded and resolved by amendment, never by a downstream writer silently choosing a side. Where a known conflict is not yet resolved, both documents carry a note pointing at the other.

### 36.5 Amendment

When any document — or any Run, Study, or Lab review — demonstrates that this document is wrong, the discovery is filed as a proposed amendment with the evidence attached. If adopted, Foundations revs its version, records the change in its revision record, and the superseded text remains readable in history. Foundational identifiers (F-n, DEC-n) are permanent and never reused; a retired principle is marked retired, with the amendment that retired it.

The working practice, established since v0.2 and followed by every amendment so far: an amendment record states *what it was, what it is now, why, who raised it, what did not change, and what remains outstanding*.

> Being wrong is recoverable. Being silently reinterpreted is not.

**Real data is the expected stress.** After the documentation phase, real-world data enters every Lab, and these documents are expected to misbehave on contact. That is the plan working: the response is amendment with the evidence attached, not surprise.

### 36.6 What machine-written documents owe this one

A model writing into this tree must: cite the specific SCR-F sections and F-identifiers it depends on; flag, rather than resolve, any ambiguity it finds; refuse to answer a DEC-owned question locally; keep Lab vocabulary out of Level 1–4 core documents; keep technology names out of Levels 1–2; verify every citation; and follow the expert-reader standard (§5). These obligations exist because a model will otherwise do the helpful thing — smooth over the ambiguity — and the tree will inherit an undecided decision as settled fact. Reviewing such a document means checking it against these obligations specifically; the checklist is at `v3_docs/03-quality/human-review.md`.

### 36.7 Canonical glossary

The 2.x → 3.x renames are deliberate, and this table is their single source of truth. Downstream documents cite it; they do not re-derive it. (Extended working vocabulary — the failure classes, ambient sensitivity, the ceilings, and the rest — lives in `v3_docs/00-start-here/glossary.md`, which hosts this table when this revision is adopted.)

| 3.x term | Meaning in one line | 2.x ancestor, where one exists |
| :---- | :---- | :---- |
| **Cell** | Smallest state-bearing participant, under the semantic ceiling | Cell |
| **World** | The complete experimental environment, owning its Layout | grid + config (implicit) |
| **Layout** | The World's arrangement and permitted local interactions | 200×200 wrap-around grid (fixed) |
| **Connection** | A declared possible local interaction between Cells | neighbourhood (implicit) |
| **Generation** | Pipeline turning intent into a tested Plugin | Stage A / B / C pipeline |
| **Plugin** | Readable implementation of one local mechanism | generated rule / step function |
| **Reactor** | Deterministic execution authority | engine / harness |
| **Attempt** | Durable record of one intention to execute | — (new in v3.x) |
| **Run** | One exact immutable execution, with its Run Contract | run |
| **Run Contract** | The frozen agreement a Run was admitted under | — (new in v3.x) |
| **Starting State** | The realized opening values, recorded exactly | — (new in this revision; DEC-23 pending) |
| **Study** | Structured question across one or more Runs | — (new) |
| **Reader** | Versioned, reproducible reading of stored evidence | classifier, detector, analyzer |
| **Corpus** | The durable body of evidence and meaning | library |
| **Search** | Retrieval across the Corpus | — (new; position-paper concept) |
| **Lab** | Domain-owned working environment | — (new) |
| **Visualization** | Evidence-backed views and time navigation | frontend player + render styles |

The Plugin row deliberately names no programming language — the v0.2 definition did, and the change is the first entry in this revision's record.

## 37. The documentation tree, as built

v0.2 proposed an initial structure; the first ring now exists at `documents/v3_docs/`:

```
documents/v3_docs/
├── 00-start-here/          Level 1 — what SCR is, human and machine,
│                           language rules, glossary, Foundations pointer
├── 01-core/                Level 3 — the twelve components
│                           (core-contract seam passes preserved as *.seams.md)
├── 02-platform/            Level 3 — jobs, storage, api, identity,
│                           execution safety, transport, frontend, observability
├── 03-quality/             Level 3 — testing, repeatability, accuracy,
│                           reference cases, human review
├── 04-decisions/           Level 2 — DEC records, plain-question format,
│                           indexed by §40
├── labs/                   Level 5 — the candidate catalog and Lab briefs,
│                           organized by family
├── critiques/              external review, retained as evidence
├── outstanding.md          the living list of what remains
└── relics/                 prior drafts and source material; not part of the tree
```

Everything in the numbered directories is **draft**; adoption is pending, per document, by the owner. The source tree for the 3.x implementation is designed after these ownership boundaries are reviewed, rather than mechanically mirroring the documentation.

---

# Part IX — What 2.x proved, and what 3.x must not accidentally inherit

## 38. Proven ideas worth carrying forward

The 2.x implementation demonstrates:

- **38.1** Semantic proposal before implementation, validated before admission as a working rule.
- **38.2** Generated code constrained by fixed execution machinery: the rule proposes state; the fixed engine controls randomness, bookkeeping, derived state, and stopping.
- **38.3** Reproducibility tested, not assumed: deterministic trial execution and reproducibility checks in the validation pipeline.
- **38.4** Failures retained: broken implementations and rejected attempts remain durable records with provenance.
- **38.5** Runs complete before playback: navigation over stored history rather than a live simulation coupled to the interface.
- **38.6** Computational state and visual appearance are not the same thing: a quiet-looking picture does not mean the state has stopped evolving.
- **38.7** Visualization can reveal different truths without changing the Run.
- **38.8** The library matters more than any one rule: the durable value is the linkage of intent, implementation, execution, measurement, failure, ancestry, and correction.

## 39. 2.x assumptions that are not automatically 3.x requirements

Implementation history, not sacred architecture — with the ones promoted into named decisions marked:

- fixed 200×200 grids; wrap-around boundaries; grid-neighbourhood-only interaction (**reach now DEC-21**);
- **one rule per world** (now DEC-1);
- **strictly synchronous lockstep stepping** (now DEC-3);
- **one kind of participant per world** (now DEC-22);
- **the mechanism generating its own starting state** (now DEC-23);
- synchronous local generation over one request; no job queue; a single execution host; the single-file embedded database as long-term store;
- the exact current optional Cell properties; the existing classification labels; the current route structure, frontend routing, renderer, and validation limits;
- the current model provider and prompt structure.

3.x preserves lessons, not accidents.

---

# Part X — The Decision Registry

## 40. Decisions this document refuses to make by accident

Consequential choices are *named*, so they are decided in decision records with evidence — never answered accidentally during implementation, or answered differently by different model-written documents that each thought the answer was obvious. **Naming a fork is not deciding it.**

Since v0.2, every record has been rewritten to lead with its question in plain language — readable without this platform's vocabulary — with the precise wording preserved for citation, the kind of decision stated (fork, boundary, placement, deferred detail, standing obligation), and an honest account of what each record actually blocks today, which for most of them is nothing. The records live in `v3_docs/04-decisions/`; this section is their index, with status at v3.x.

### 40.1 Foundational forks surfaced by v0.2

| ID | The plain question | Status at v3.x |
| :---- | :---- | :---- |
| **DEC-1** | Can more than one thing happen at once? | Open — the largest fork on the board. Narrowed by the external-input test (§14); constrained: any composition policy is declared, named, versioned, and recorded, never an accident of implementation order. |
| **DEC-2** | What does "run it again and check" promise? | **Decided, 2026-08-21** — the registry's first. Reproduction under contract by default; exact replay for Runs designated evidence-grade at run time, never retroactively. Alternatives and reopening triggers in the record. |
| **DEC-3** | Whose clock is it, and must everything tick together? | Open; placement decided (§6, §18.5). The Reactor owns every clock; which models are offered, to whom, under what budgets, is open. |
| **DEC-4** | What does "confident" mean here? | Open; stance constrained by §20.3 — modest, plainspoken, no significance theater. |
| **DEC-5** | Who owns the translating? | Open. Four components each translate today; drift compounds monthly, and this decision gets harder with time, not easier. |
| **DEC-6** | What happens to the old library? | Partially decided: carried forward as founding evidence, histories never rewritten. Open: identifier mapping, comparability, recompute-versus-preserve. Timing note: migrate before the scale-up. |

### 40.2 Open questions carried forward from v0.1

| ID | The plain question | Status at v3.x |
| :---- | :---- | :---- |
| **DEC-7** | What is a rule allowed to do? | Open; covers the contract, not the notation (amended 2026-08-20). Sequenced after DEC-1 and DEC-3, by design. |
| **DEC-8** | One filing system for two shapes of world? | Open; constrained — no near-uniform-connections assumption (hubs are real). |
| **DEC-9** | How much may the platform guess before asking? | Open; the confirmation rail is already law. |
| **DEC-10** | How does a measurement admit its doubts? | Open; the obligations are law, the presentation is design work. |
| **DEC-11** | When are two rules the same rule? | Open; every grouping states its basis and stays inspectable. |
| **DEC-12** | Similar how, exactly? | Open; the three-way separation is law, the machinery is not. |
| **DEC-13** | What must we keep so the pictures never need a re-run? | Open, with a deadline: before large-scale storage formats freeze. |
| **DEC-14** | What travels with a forty-second clip? | Open; settled before the first video ships. |
| **DEC-15** | When is a Lab more than an experiment? | Open; the ladder exists, the top rung's height doesn't. Best decided against the first Labs to approach it. |
| **DEC-16** | How do we contain code we didn't write? | Open; **narrowed 2026-08-21** — the obligations are requirements now; the mechanism waits for a real deployment. |
| **DEC-17** | What changes when we change the AI? | Open; the bookkeeping that makes it answerable is already law. |
| **DEC-18** | When a person edits a rule by hand, what happens to its story? | Open; **substantially narrowed** — new revision, no inherited privilege, intent stale-until-confirmed. Only the catch-up procedure remains. |
| **DEC-19** | Watching live versus the permanent record | Open; the dangerous failure is fenced — provisional is marked provisional at the moment of observation. |
| **DEC-20** | How do we hand results to the real experts without overclaiming? | Open; non-claims travel with the mechanism, and the package is designed with its first real recipient. |

### 40.3 Registered since v0.2, from building the core

| ID | The plain question | Status at v3.x |
| :---- | :---- | :---- |
| **DEC-21** | How far can a rule reach? | Open; leading formulation recorded — authority over declared paths, never distance. The line that decides where "local" stops meaning anything. |
| **DEC-22** | Must every participant be the same kind of thing? | Open; lean recorded — several bounded kinds, under the semantic ceiling regardless. |
| **DEC-23** | Who sets up the board? | Open; leading candidate recorded — World, Starting State, and start recipe as three separate things. |
| **DEC-24** | How much can we bend before it isn't the same instrument? | Open; a standing obligation, not a one-time choice. Owes the **floor** — what stays true of every experiment regardless of how DEC-1, 3, 21, and 22 land — written *before* those four are decided, and a ledger rule making every future relaxation state its effect on the total. |

### 40.4 Reserved

Identifiers **DEC-25 through DEC-27** are reserved for three candidates named in the tree and not yet registered — **exploration strategy** (nothing owns deciding what to generate next), **cost and budget** (nothing owns the economics of generation, repair, and fan-out against a planned scale-up; consumption is being recorded now so the eventual decision has data), and **ownership of evidence** (the Corpus is one durable body with no notion of whose; partitioning is frozen until this is decided, because a Search speaking for a silent slice would make absence of evidence mean absence of permission). Registration lands with adoption of this revision.

---

# Part XI — Non-claims and discipline

## 41. SCR does not claim that simple cellular mechanisms predict arbitrary domains

A mechanism that reproduces an observed pattern is a **candidate explanation**, not proof of real-world causation — several different mechanisms can reproduce the same observation, and the platform's ability to produce candidates cheaply is exactly why none of them is thereby shown to be right.

For the same reason, no model of a real-world system is described as *verified* or *validated* — natural systems are never closed and model results are never unique, so partial **confirmation** against named reference cases, per regime, is the most the platform ever claims (basis and citation: `v3_docs/03-quality/accuracy.md`). The system's proposed value is upstream of domain prediction: supplying, testing, indexing, and comparing candidate mechanisms cheaply and reproducibly. Domain calibration and validation remain domain problems, and a Lab paper says explicitly where SCR stops and established tooling begins. That proposed value is itself an untested, falsifiable claim, and no document presents it as established.

## 42. SCR does not claim exhaustive rule-space exploration

Language-model generation samples according to model priors, prompts, Corpus history, Lab vocabulary, and exploration strategy. Coverage measurements describe the space SCR has defined for itself; they are never represented as coverage of all possible local mechanisms — exhaustive enumeration is available only for the very smallest rule spaces, and nothing this platform generates lives there. User signals — flags, overrides, reruns — never enter generation context: a generator steered by what a person marked interesting is learning that person's taste and reporting it as exploration.

## 43. SCR does not treat model fluency as scientific authority

A model can write persuasive explanations that are wrong. Therefore: code is checked; Runs provide evidence; Readers are deterministic where feasible; provenance is retained; human corrections remain visible; Labs carry their own accuracy obligations; claims cite external evidence where domain validity is at issue; and machine explanations of machine actions — repair accounts, generated summaries, narration — are **interpretation, never evidence**. Reviewing them means checking them against the evidence they describe, not reading them for plausibility, because plausibility is what the machinery is best at and therefore worthless as a signal.

Language models are high-leverage contributors to the workflow. They are not an oracle layer above it.

---

# Part XII — Foundational rules, condensed

## 44. The compact version

Permanent identifiers; cite as F-n. Never reused; retirement requires amendment (§36.5). F-2's text is amended in this revision, and F-23 is new; both changes are in the revision record.

1. **F-1 — Semantic first.** People work primarily through meaning.
2. **F-2 — Readable and writable, always.** Generated mechanisms remain readable and editable by a competent person, without the platform's help. *(Amended in v3.x: the property, with no notation named.)*
3. **F-3 — Automation is not the objective. Better allocation of work is the objective.**
4. **F-4 — People do judgment work. Machines absorb mechanical work.**
5. **F-5 — Plain language is a system property.** And plain is not simplified: the expert reader's fluency is assumed, ours is never required.
6. **F-6 — Intent, implementation, and outcome remain separate.**
7. **F-7 — Cells are the basic state-bearing participant, under the semantic ceiling.**
8. **F-8 — Worlds define experimental reality and own their Layout.**
9. **F-9 — The Plugin proposes. The Reactor decides. Time is not an exception, and neither is authorship.**
10. **F-10 — Runs are immutable evidence.** Attempts are evidence too, admitted or not.
11. **F-11 — Readers read; they do not rewrite.**
12. **F-12 — A Run shows what happened once. A Study tests a hypothesis.**
13. **F-13 — Study statistics are modest and plainspoken.**
14. **F-14 — Failures stay.**
15. **F-15 — The Corpus is the durable asset, and the 2.x corpus is its founding evidence.**
16. **F-16 — Search returns evidence and mechanisms to human questions.**
17. **F-17 — Labs own domain assumptions and must earn their fit.**
18. **F-18 — Visualizations may dramatize evidence; they may never invent it — and divergence is shown in context, never censored.**
19. **F-19 — Reports and videos must trace claims back to evidence.**
20. **F-20 — Security exceptions are not exceptions; hostile conditions are explicit experimental capabilities.**
21. **F-21 — Evidence integrity lives in the record, never in the data.**
22. **F-22 — Consequential choices are named in the Decision Registry, decided in decision records, and never resolved locally by a downstream document.**
23. **F-23 — The cellular budget is kept.** *(New in this revision.)* What makes this platform a local-mechanism instrument is spent only knowingly: relaxations of its defining properties are weighed in aggregate against a written floor, never granted only one well-argued case at a time.

SCR proposes mechanisms and preserves evidence. Domain truth requires domain validation.

---

# Part XIII — Review targets for external critique

## 45. Questions for reviewers

Reviewers should challenge this document on architecture rather than prose polish. Please look specifically for:

1. **Missing foundational components.** Is an important concept hidden inside another component that deserves its own ownership boundary?
2. **False separations.** Are two components actually one responsibility with different names?
3. **Semantic leaks.** Where does the architecture force a person back into implementation mechanics unnecessarily?
4. **Opacity risk.** Where could an optimized or machine-internal representation displace the readable human artifact?
5. **Reactor boundary failures.** Are there mechanisms a Plugin would need that cannot be modelled without letting it redefine the experiment?
6. **Study weakness.** Does Study have enough conceptual weight for real hypothesis testing rather than batch Runs?
7. **Reader truth confusion.** Where might derived analysis become indistinguishable from immutable evidence?
8. **Lab leakage.** Which domain assumptions have entered the platform core?
9. **Visualization deception risk.** Which views could look causal or scientific while representing only correlation, similarity, or presentation choices?
10. **Corpus provenance gaps.** What future question could not be answered because the right source information was not preserved?
11. **2.x inheritance.** Which assumptions persist merely because the prototype used them?
12. **Over-generalization.** Where is SCR becoming a generic simulator instead of recognisably a local-mechanism instrument? The measuring line is DEC-24's ledger and, when written, its floor.
13. **Under-generalization.** Which promising Labs would be excluded by an unnecessarily grid-shaped or synchronous core?
14. **Product clarity.** Can a practitioner understand the relationship among Lab, Study, Run, Reader, Plugin, Reactor, and Corpus without reading implementation documents?
15. **Falsifiability.** Which claims about SCR's value could be tested and fail?
16. **Registry completeness.** Which consequential choice is still being made by accident — present in assumptions but absent from the registry?
17. **Document-system realism.** Will the citation, precedence, and amendment rules of §36 survive two hundred mostly machine-written documents, or is there a drift path they fail to close?
18. **Aggregate spend.** *(New in this revision.)* Does any combination of individually-approved relaxations — composition, timing, reach, participant kinds — exceed what the platform's identity can survive, even though each passed review on its own?

Reviewers are encouraged to propose deletions and boundary changes, not merely additions — a review that finds only additions has not tried to break anything. A reviewer who resolves a DEC-owned question inline has answered a question this document deliberately left open; critique the framing instead.

---

# Source basis and references

This document is the second revision of the 3.x foundational design. Evidence for what the existing system demonstrably does, and for which design lessons have survived contact with real writing:

1. **The 2.x deep-dive set** — engine internals, storage and transport, contract enforcement, generation pipeline, interface and identity, frontend (Release 2.2.1 documents). The demonstrated-behaviour basis.
2. **ASR Omnibus Requirements v3** — the 2.x contract and its stable-identifier practice, treated as prior-art evidence, not as the 3.x contract.
3. **The 3.x documentation tree** (`documents/v3_docs/`, 2026-08-20/21) — Level 1 orientation documents; the twelve core requirements documents with the five preserved seam passes; eight platform documents; five quality documents; the Decision Registry in plain-question format. This revision's largest single source: where v0.2 reasoned forward from principles, v3.x also reasons backward from what writing the contracts revealed.
4. **External critiques** (`v3_docs/critiques/`, third-party models, 2026-08) — the core-contract critique that produced the Run Contract closure, the two-promise replay framing, the Attempt/Run distinction, trust-follows-role, and the input/mechanism test; and the Lab-catalog critiques. Each adopted item is credited at its point of use; each rejected item's rejection is recorded where it was rejected.
5. **The Lab briefs** (`v3_docs/labs/`) — source of the reducibility audit, which two briefs invented independently before any core document asked for it.
6. **A Card Catalog for Emergence** (position paper) — the prior mechanism-hypothesis framing and the Corpus/Search argument.

External technical citations are carried by the tree's requirements documents, each verified against its published source before use (§36.2). This foundations document intentionally makes few claims about external domains; Lab papers carry the domain evidence.

SCR continues to credit Stephen Wolfram's work on cellular automata and ruliology as inspiration while making no claim that SCR reproduces or improves on that work. The 3.x line is a distinct semantic, experimental, and product direction built from that inspiration.

---

## Closing statement

Semantic Cellular Ruliology begins from a simple observation: the bottleneck in experimentation is often not running one more computation. It is translating a human question into a precise experiment, implementing it without clerical mistakes, repeating it enough times to learn anything, preserving what actually happened, and returning the result in a form a person can understand and dispute.

Language models substantially change the cost of that translation and implementation work. They do not remove the need for controlled execution, provenance, human judgment, or domain validation. They make it possible to spend those scarce human resources where they matter more.

SCR therefore treats semantics, executable mechanisms, deterministic evidence, structured Studies, and human interpretation as parts of one continuous system — and, since v0.2, treats its own documentation the same way: written mostly by machines, checked against evidence, amended in the open, and adopted only by a person.

The ambition is not to build a machine that replaces the person asking the question.

It is to build a machine that makes asking — and actually testing — the next good question dramatically cheaper.
