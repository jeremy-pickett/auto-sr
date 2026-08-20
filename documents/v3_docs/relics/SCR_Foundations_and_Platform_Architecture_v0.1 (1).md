# Semantic Cellular Ruliology
## Foundations and Platform Architecture — v0.1

**Status:** Foundational design for critique  
**Date:** 2026-08-20  
**Scope:** Semantic Cellular Ruliology 3.x  
**Purpose:** Define what the platform is, what its major components own, how humans interact with it, and which principles future requirements and implementations must preserve.

> **This is not the implementation requirements document.** It sits above requirements. Its job is to establish the conceptual map so later requirements, code, Labs, interfaces, tests, and research papers have a stable place to belong.

---

## Executive summary

Semantic Cellular Ruliology (SCR) is a platform for proposing, executing, measuring, comparing, and investigating simple local mechanisms that produce larger behavior over time.

Humans interact with SCR primarily through meaning. They describe a problem, a behavior, a suspicion, a mechanism, a change, or a question in ordinary domain language. SCR uses language models and deterministic software to translate that intent into readable Python Plugins, check and repair the implementation, execute controlled experiments, preserve complete evidence, run repeatable analyses, and return the results in forms a human can inspect.

The purpose is not to automate humans out of the process.

> **Automation is not the objective. Better allocation of work is the objective.**

Machines should absorb syntax mistakes, transcription errors, repetitive implementation, bookkeeping, mechanical validation, repeated test execution, exact replay, evidence indexing, and the other forms of work where fatigue and clerical error are expensive. Humans should spend their attention on the parts that remain irreducibly human: deciding which questions matter, recognizing nonsense, correcting domain assumptions, interpreting evidence, judging usefulness, and deciding what happens next.

The word **Semantic** is therefore not marketing decoration. It is an architectural constraint. Human meaning must remain visible across the entire system: what was asked, what mechanism was proposed, what code implemented it, what experiment was run, what actually happened, what later analysis concluded, and where a human disagreed.

SCR 2.x demonstrated that the central idea works. It can generate natural-language rule proposals, implement them as readable Python, validate them, run deterministic cellular experiments, preserve immutable histories, and let a human scrub through those histories visually. 3.x is not a larger version of the toy. It is a new product line built from what the toy proved while reconsidering the architecture from first principles.

The initial foundational components of SCR 3.x are:

1. **Cell**
2. **World / World Layout**
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
13. **Platform Services**

A semantic human interface governs all thirteen rather than becoming a fourteenth subsystem.

---

# Part I — Foundational principles

## 1. Semantic first

Humans should normally interact with SCR through the language of the problem, not the mechanics of the implementation.

A security engineer should be able to ask:

> Test whether delayed identity updates let this account keep moving after access is revoked.

A fisheries researcher should be able to ask:

> Keep the fish behavior the same, but increase current from the west.

A materials researcher should be able to ask:

> Find mechanisms that keep producing branching growth even when the starting defects move.

The platform may translate those requests into Python, arrays, graph structures, job definitions, database queries, Reader execution, or many Runs. Those mechanisms remain inspectable, but they are not the price of admission.

This principle applies in both directions. SCR should not merely accept natural language at the beginning and then collapse into opaque machinery. It should return meaning at every useful boundary:

- what the human asked;
- what SCR understood;
- what mechanism it proposed;
- what Plugin implements that mechanism;
- what World and conditions were used;
- what the Reactor actually executed;
- what happened during the Run;
- what a Reader measured;
- what a Study found;
- how sure the system is;
- where human interpretation disagreed.

**Semantic is the continuity of meaning through the experimental chain.**

---

## 2. Readable and writable, always

Every generated mechanism must retain a human-readable and human-editable representation.

For executable mechanisms in the first 3.x architecture, that representation is ordinary Python.

The Python Plugin is not disposable scaffolding around a hidden model. It is part of the permanent experimental record. A human must be able to:

- read it;
- diff it;
- copy it;
- modify it;
- review it;
- comment on it;
- give it to another model;
- give it to another engineer;
- understand what capabilities it uses;
- determine whether it plausibly implements the stated intent.

SCR may later build internal optimized representations for speed or alternate execution backends. Those representations are implementation details unless and until they can preserve the same human readability contract. They must not silently replace the readable mechanism as the canonical artifact humans are expected to reason about.

A visual rule editor may exist. Direct code editing may exist. Neither defines the ordinary workflow.

The expected modern workflow is simpler:

> **The human reads the code when useful. The machine usually writes it.**

That is not “no-code.” Code remains visible because visibility supports trust, auditability, learning, portability, correction, and independent review. What disappears is the assumption that humans must manually type every implementation in order to remain in control of it.

---

## 3. Intent, implementation, and outcome are different facts

SCR must preserve three distinct records:

### 3.1 Intent
What the human or generator meant to try.

### 3.2 Implementation
What executable mechanism was actually produced.

### 3.3 Outcome
What happened when that mechanism ran under exact conditions.

These records may agree. They may also disagree in interesting ways.

A mechanism intended to stabilize a front may fragment it. A defensive access rule may unexpectedly increase privilege persistence. A rule intended to create stationary structures may produce travelers. Those disagreements are not merely failures of classification. They are potential discoveries.

SCR must therefore resist any design that overwrites one layer with another. A user correction does not erase the machine's original interpretation. A Reader's label does not become the Run. A successful execution does not prove that the Plugin faithfully represented the original intent.

The gap between intent, implementation, and outcome is part of the evidence.

---

## 4. The machine does mechanical work; humans do judgment work

SCR should aggressively use language models and deterministic tooling where they reduce mechanical burden without erasing meaning or accountability.

### Machines should preferentially handle

- translating domain requests into proposed experiment definitions;
- writing routine Plugin code;
- syntax and structural correctness;
- contract checking;
- repetitive implementation changes;
- test generation where appropriate;
- repeated Runs;
- exact bookkeeping;
- provenance capture;
- evidence reconstruction;
- deterministic analysis;
- search across prior work;
- generation of routine reports and summaries;
- presentation of candidate explanations for human review.

### Humans should preferentially handle

- choosing important questions;
- supplying domain context;
- recognizing bad abstractions;
- challenging assumptions;
- correcting semantic misunderstandings;
- deciding whether a mechanism is plausible;
- deciding whether an observed result matters;
- judging whether SCR is an appropriate tool for the domain;
- deciding whether evidence warrants action;
- taking responsibility for real-world decisions.

SCR should be judged partly by how successfully it moves human time from the first list to the second.

---

## 5. Plain language is a system property

Code names, UI labels, stored concepts, documentation headings, logs, and error messages should use words an ordinary second-year CS student or working engineer can understand without specialist mathematics.

Standard technical terms may be documented when useful, but specialist language should not become a needless barrier to operation.

This principle does not require SCR to avoid difficult ideas. It requires difficult ideas to be named clearly.

The project name itself may be pretentious. Variables may not.

---

## 6. The Plugin proposes; the Reactor decides

This is one of the strongest principles inherited from 2.x and should survive architectural change.

A generated Plugin may propose state changes within its declared capabilities. It may not redefine the experiment in which it is running.

The Reactor owns the actual execution semantics: state application, controlled randomness, timing, observation rules, limits, and stopping behavior.

This distinction is particularly important in security research. SCR must not make generated code more powerful merely because the Lab is studying hostile behavior. Attacker behavior, stale observations, partial visibility, shared resources, timing differences, and defender constraints must be explicit capabilities of the World and Reactor.

The experimental contract can model adversarial conditions. The Plugin cannot cheat the simulator.

---

## 7. Runs are evidence

A completed Run is an immutable historical record of what occurred under exact conditions.

Human interpretation may change. Readers may improve. Labels may be corrected. New visualizations may reveal structure nobody noticed originally.

The stored Run does not change to accommodate those later interpretations.

This is what makes replay, comparison, independent analysis, and later re-reading scientifically meaningful.

---

## 8. Readers read; they do not rewrite

A Reader is a deterministic interpretation or measurement of stored evidence.

Readers may be wrong, incomplete, superseded, or highly domain-specific. Therefore Reader outputs must be versioned and reproducible.

A new Reader version may disagree with an old Reader version without altering the Run either one examined.

This creates an explicit distinction between:

- **recorded evidence** — what happened;
- **derived evidence** — measurements computed from what happened;
- **interpretation** — what a human or model believes those measurements mean.

---

## 9. One Run is an event; a Study tests a hypothesis

A single Run can demonstrate that something happened once.

It cannot by itself establish robustness, sensitivity, causation, or generality.

A **Study** is the first-class object that asks a structured question across one or more Runs.

This is a major opportunity for SCR because much ordinary operational troubleshooting is already informal hypothesis testing. A sysadmin who asks “does the failure stop if I isolate this network?” is changing one condition and testing a hypothesis, whether or not anyone uses that phrase. A security analyst who tries five starting identities is testing robustness. A researcher who varies wind speed is exploring sensitivity.

SCR should make disciplined experimentation easier without requiring users to perform academic theater.

The word **hypothesis** should be available when it clarifies the work, not required as ritual vocabulary.

---

## 10. Failures stay

Negative evidence is evidence.

SCR should preserve failed proposals, invalid Plugins, rejected operations, failed Runs, behavior misses, inconclusive Readers, and Studies that do not support the tested hypothesis.

“No result” is not one thing. The reason matters.

At minimum the platform should distinguish:

- **Proposal failure** — the proposed mechanism was invalid, incoherent, or outside the Lab contract.
- **Plugin failure** — the implementation did not validly express or execute the proposal.
- **Reactor rejection** — the Plugin attempted an operation outside the declared experiment.
- **Run failure** — execution could not complete reliably.
- **Behavior miss** — execution completed, but the requested behavior was not observed.
- **Reader uncertainty** — evidence exists, but the requested measurement cannot be made reliably.
- **Study failure** — available evidence did not answer the hypothesis with the required confidence or coverage.

A system that saves only successful mechanisms creates a misleading map of what has been explored.

---

## 11. Labs own domain assumptions

The SCR core should not know what a trout, domain controller, flame front, cloud role, prompt injection, dendrite, or tumor is.

A Lab does.

Labs contain the domain-specific assumptions, vocabulary, World templates, Readers, reference cases, fit boundaries, accuracy tests, and known failure modes required to translate a real problem into SCR experiments.

This protects both sides of the architecture:

- the core remains coherent and reusable;
- each Lab can be held accountable for whether its abstraction is actually defensible in its domain.

No Lab earns credibility merely because someone successfully expressed its domain as Cells and Connections.

---

## 12. Visuals may dramatize evidence; they may never invent evidence

Visualization is not decorative output attached after the scientific work. It is one of the main ways humans discover structure in time-varying systems.

SCR 2.x already demonstrates the value of stored playback: a completed Run can be scrubbed backward and forward like video because the history exists independently of the UI. Multiple render styles can make different behavior immediately visible without changing the underlying Run.

3.x should preserve and expand this conceit aggressively.

Lighting, depth, motion, animation, camera movement, shading, trails, temporal stacking, and cinematic presentation are allowed.

Fabricated movement, fabricated relationships, fabricated measurements, invented causal links, and decorative data that looks scientific but has no stored source are not.

Every meaningful visual element should be able to answer:

> **What real stored or measured data produced this?**

If the answer is unclear, the visual is not suitable for an evidence view.

---

# Part II — The core conceptual model

## 13. Cell

The **Cell** is SCR's smallest state-bearing participant.

A Cell may represent very different things depending on the Lab:

- a terrain patch;
- a parcel of water;
- a region of atmosphere;
- an organism;
- a host;
- a user identity;
- a cloud role;
- an AI agent;
- a service;
- a material region.

SCR does not claim these things are fundamentally equivalent. The common abstraction is narrower:

> **A Cell carries state and may affect other Cells according to declared local mechanisms.**

Keeping the term Cell is intentionally restrictive. More general terms such as *entity* or *thing* would make the architecture easier to stretch while making its reasoning harder to police.

A future Lab that cannot honestly describe its participating objects as local state-bearing Cells may be telling us that SCR is a poor fit—or that a new foundational abstraction is required. That should be treated as useful architectural pressure, not an inconvenience to hide.

---

## 14. World

A **World** defines the experimental reality in which Cells exist and interact.

A World owns or references:

- Cells;
- Cell properties;
- Connections;
- Connection types;
- World Layout;
- boundaries;
- static environmental fields;
- shared resources;
- observation rules;
- observation delays;
- starting conditions;
- fixed external conditions relevant to the Run.

Humans should be able to define and modify Worlds semantically.

Examples:

> A segmented enterprise network with user, application, management, and domain-controller networks. Application servers may initiate connections to the database tier but not to user workstations.

> Twenty agents share one long-term memory service. Only the planning and deployment agents have access to production tools.

> A coastal grid with a west-to-east current, one rocky boundary, and warmer shallow water near shore.

SCR converts the semantic description into an exact stored World representation that remains inspectable.

---

## 15. World Layout

The **World Layout** describes how Cells are arranged and which local interactions are possible.

Initial layout families may include:

### Grid World
Interactions follow physical position or another meaningful lattice.

### Network World
Interactions follow communication or reachability connections.

### Identity World
Interactions follow trust, role membership, delegation, inheritance, or permission relationships.

### Agent World
Interactions follow messages, tools, memories, shared resources, and delegated work.

These are starting families, not a promise that every domain will fit one of four boxes.

The key requirement is that a Plugin can affect only what the World Layout and declared Connections permit.

3.x must not inherit 2.x's square toroidal grid merely because it was convenient for the toy. Nor should it generalize so aggressively that “World” becomes an unconstrained simulation language with no useful local-mechanism discipline.

The boundary between sufficient flexibility and loss of experimental identity should be revisited explicitly as Labs mature.

---

## 16. Generation

**Generation** turns semantic intent into a tested candidate Plugin.

Generation is a pipeline, not merely a model call.

Its core responsibility is:

> **Propose → Write → Check → Test → Repair → Deliver**

### 16.1 Propose
Interpret a human request, Lab goal, search gap, or exploration objective and propose a simple local mechanism in ordinary language.

### 16.2 Write
Produce a readable Python Plugin implementing the proposal.

### 16.3 Check
Verify structure, permitted capabilities, declared reads and writes, determinism requirements, and other contract rules before expensive execution.

### 16.4 Test
Execute controlled validation Runs sufficient to catch implementation defects, non-reproducibility, illegal state behavior, and obvious contract violations.

### 16.5 Repair
When a failure is mechanical and repairable, give the system one or more explicitly governed opportunities to fix the implementation without silently changing the intended mechanism.

Any repair must preserve provenance: original proposal, original Plugin, failure, repair instruction, repaired Plugin, and final result.

### 16.6 Deliver
Provide the validated Plugin and its complete provenance to the Reactor for actual Runs and Studies.

Generation remains a **proposal system**. It does not get to declare that a mechanism is scientifically useful merely because it successfully wrote code.

---

## 17. Plugin

A **Plugin** is the readable Python implementation of one local mechanism.

The Plugin is deliberately smaller than the full experiment.

It may:

- read declared state;
- inspect declared local connections or views;
- calculate proposed next state;
- use explicitly provided helper capabilities;
- return proposed changes.

It may not independently own:

- random number sources not supplied by the Reactor;
- execution ordering;
- global time semantics;
- observation freshness;
- permission to access arbitrary Cells;
- stopping criteria;
- immutable history;
- provenance bookkeeping;
- hidden mutable state not declared by the experiment.

The exact Plugin contract will vary as World Layouts mature, but the conceptual line should remain simple:

> **The Plugin expresses the local mechanism. The Reactor expresses the laws of the experiment.**

---

## 18. Reactor

The **Reactor** is SCR's deterministic execution authority.

The name is intentional: Plugins enter the Reactor under controlled conditions; the Reactor is where state transitions actually occur and evidence is produced.

The Reactor owns:

- state application;
- step or event ordering;
- controlled randomness;
- timing semantics;
- observation delay;
- visibility rules;
- shared-resource side effects;
- derived state required by the experiment;
- runtime limits;
- stopping conditions;
- exact replay requirements;
- evidence capture boundaries;
- version identity for execution semantics.

### 18.1 The Reactor is not the Lab
The Reactor does not know that a connection is “credential trust” or that a scalar represents “fuel moisture.” Those meanings belong to Labs and Worlds.

### 18.2 The Reactor is not Generation
It does not invent mechanisms or repair Python.

### 18.3 The Reactor is not a Reader
It records facts needed to replay the experiment. It does not decide what those facts mean beyond minimal execution facts such as completion or explicit stop conditions.

### 18.4 Security posture
The generated-code execution boundary must continue to be treated as an explicit contract and execution-safety problem. Adversarial Labs must not be allowed to use the research subject as justification for an undefined or permissive execution surface.

---

## 19. Run

A **Run** is one exact execution.

A Run binds specific versions of:

- Plugin;
- World;
- World Layout;
- Reactor;
- starting conditions;
- controlled randomness or seed material;
- relevant Lab contract;
- execution limits.

A Run records enough state to support exact or contractually equivalent reconstruction and later analysis.

The 2.x decision to complete a Run before playback is especially valuable and should remain the default conceptual model. It turns playback into pure navigation over immutable history rather than a live simulation coupled to the UI.

That produces several benefits:

- instant scrubbing;
- backward stepping without rollback logic;
- repeatable views;
- multiple visual styles over the same evidence;
- later Readers that did not exist when the Run was created;
- automated report generation after execution;
- reproducible video generation from exactly the same history.

Future products may also need live operational views. Those should not erase the distinction between a live execution stream and the finalized immutable Run.

---

## 20. Study

A **Study** is a structured question that requires one or more Runs.

Study is a major product opportunity because it packages disciplined experimentation in language ordinary practitioners already use.

Examples:

> Does the same compromise path work from five different developer identities?

> Which single access change prevents administrator privilege?

> Does the walker still travel when starting position changes?

> At what wind range does this front stop branching?

> Is the result robust to a different random starting state?

> Which of these three mechanisms best reproduces the observed behavior?

### 20.1 Initial Study patterns

**Repeat Test**  
Repeat the same mechanism across different permitted starting conditions or seeds.

**Small-Change Test**  
Change one declared condition and determine what later evidence changes.

**Try Many Settings**  
Systematically vary one or more declared settings under a controlled protocol.

**World Comparison**  
Hold the Plugin constant while comparing World conditions or layouts.

**Plugin Comparison**  
Hold the World and protocol constant while comparing mechanisms.

### 20.2 Study as hypothesis machinery

A Study should be able to state, in plain language:

- the question;
- the hypothesis where useful;
- what is being held constant;
- what is being changed;
- what evidence would support or weaken the hypothesis;
- which Runs were performed;
- what Readers were used;
- what the Study found;
- what remains uncertain.

Users need not formulate formal hypotheses manually. SCR can infer and propose them from ordinary troubleshooting language, then expose the proposed hypothesis for confirmation.

This makes the product rigorous without making it pompous.

---

## 21. Reader

A **Reader** examines completed evidence and produces a reproducible measurement or derived interpretation.

Potential Readers include:

- spread;
- movement;
- branching;
- persistence;
- recurrence;
- stationary structure;
- traveler detection;
- front speed;
- containment speed;
- compromise spread;
- privilege reached;
- reinfection;
- memory persistence;
- instruction survival;
- origin survival;
- hidden-path indicators.

A Reader must identify at minimum:

- its name;
- version;
- settings;
- exact evidence examined;
- output;
- completeness or confidence where applicable.

A Reader result should be disposable in the best possible sense: it can be deleted and recomputed from immutable evidence without changing history.

Readers should not become invisible truth layers. The UI should make it possible to understand which Reader produced an assertion and, for important claims, how that assertion relates to underlying evidence.

---

## 22. Corpus

The **Corpus** is the durable body of SCR evidence and meaning.

It is not synonymous with the database.

A database is an implementation choice. The Corpus is the asset the implementation protects.

The Corpus links:

- human requests;
- semantic proposals;
- Plugin implementations;
- Plugin versions;
- Worlds;
- World Layouts;
- Runs;
- Study definitions;
- Reader outputs;
- failures;
- repairs;
- model provenance;
- Reactor versions;
- Lab versions;
- human corrections;
- findings;
- annotations;
- relationships among related mechanisms.

The 2.x architecture already demonstrated two essential Corpus principles that should survive:

1. individual generated rules matter less than the accumulated library connecting intent, implementation, trajectories, measurements, failures, ancestry, and corrections;
2. operational telemetry is conceptually different from permanent experimental history.

3.x should preserve that distinction even if storage moves from local SQLite to PostgreSQL, object storage, distributed workers, or future systems.

---

## 23. Search

**Search** turns accumulated evidence back into useful human work.

The long-term product is not merely a gallery of simulations. It is a searchable catalog of mechanisms, evidence, and failed attempts.

Users should eventually be able to ask questions such as:

> Show me simple mechanisms that produce branching fronts.

> Find mechanisms that unexpectedly increased privilege persistence.

> Find cases that behave like this uploaded pattern.

> Show mechanisms with similar observed behavior but very different stated intent.

> Which mechanisms survive Repeat Tests across the most starting conditions?

> Find experiments where adding containment made the outcome worse.

Search may combine:

- semantic similarity;
- Plugin structure;
- World properties;
- Reader measurements;
- Study results;
- outcome history;
- intent/outcome disagreement;
- known failures;
- human annotations.

The query language exposed to ordinary users should remain semantic even if advanced structured search also exists.

---

# Part III — Visualization as evidence instrumentation

## 24. Visualization is its own vertical

Visualization deserves a first-class architecture and roadmap rather than being treated as a frontend styling concern.

The reason is scientific before it is commercial: cellular and local-rule systems are fundamentally temporal. Their behavior often cannot be understood from a final frame or summary number. Humans discover important structure by watching movement, persistence, recurrence, branching, clustering, fronts, boundaries, and state transitions over time.

SCR 2.x proved this at small scale. Stored Runs can be played, paused, stepped, and scrubbed through time. Different render styles expose different properties of the same immutable data. Activity highlighting, stable kind coloring, trails, relief, and related styles can make behavior “pop” without modifying the Run.

That interaction model should be preserved as a core conceit of 3.x.

### 24.1 Time navigation is foundational

Every visual Run experience should assume that time is directly navigable.

At minimum:

- slider scrubbing;
- frame stepping;
- play/pause;
- jump-to-event where Readers identify events;
- comparison of two points in time;
- visual marks for Study or Reader findings;
- stable permalink or report references to exact times where practical.

The slider is not merely a playback control. It is an experimental instrument.

### 24.2 Styles are lenses, not alternate realities

A single Run may support many render styles:

- kind coloring;
- activity emphasis;
- changed-cell highlighting;
- stationary-cell emphasis;
- traveler or walker emphasis;
- trails;
- scalar relief;
- hidden-state views;
- connection activity;
- observation delay;
- Reader overlays.

These styles may emphasize different facts but must derive from the same stored evidence or versioned Reader output.

A useful architectural test is:

> Can this style be applied later to an old Run without re-running the experiment?

When the answer is yes, it is probably a true evidence View. When the answer is no, the system should be explicit about what new information or execution is required.

---

## 25. High-value 3D Views

SCR should explicitly support a future advanced visualization program. It is not a day-one requirement, but the architecture should avoid decisions that make it prohibitively expensive later.

Candidate high-value Views include:

### 25.1 3D World View
Cells and Connections become navigable geometry. State is represented through evidence-backed combinations of position, size, height, opacity, material, motion, or light.

A Network or Agent World can become a live spatial representation of propagation. A Grid World can become a surface or volume. The exact visual grammar should be Lab-aware.

### 25.2 Time View
Time is mapped into a spatial dimension.

A persistent stationary pattern becomes a column. A traveler creates a diagonal path. A branching front creates branching geometry. Oscillation creates repeated structure. The goal is not merely visual spectacle; it is to let temporal behavior become an object that can be inspected from multiple angles.

### 25.3 Influence View
A Small-Change Test can show where later state diverges from a baseline after one controlled change.

The resulting space-time difference can be rendered as an expanding influence volume, cone, path, or field derived from actual paired Run evidence.

### 25.4 Study View
Many Runs from one Study can be compared in one visual environment. Outcome families, failures, robust regions, and outliers can become visible without opening each Run individually.

### 25.5 Behavior Map
Try Many Settings can produce a terrain or other spatial surface where geometry represents measured outcomes. Every coordinate must trace back to actual Study settings and Reader results.

### 25.6 Corpus View
Mechanisms can be positioned using semantic and measured similarity. This is the most marketing-friendly concept and also one of the easiest to abuse. Any “galaxy,” cluster, distance, or neighborhood must state what similarity measure created it and which data were used.

---

## 26. Visualization truth contract

Advanced presentation may be cinematic. The truth contract remains strict.

For any significant visual property, the system should be able to identify its source:

| Visual property | Permitted source examples |
|---|---|
| Position | World Layout, stored Cell location, deterministic layout algorithm |
| Height | stored scalar property, Reader measurement |
| Connection | declared World connection, recorded interaction |
| Trail | stored Cell/structure positions over time |
| Glow intensity | normalized stored activity or Reader measurement |
| Color | stored state, Reader category, selected style mapping |
| Animation | ordered stored Run states |
| Divergence volume | measured difference between paired Runs |
| Cluster placement | declared similarity calculation and input data |

The visual system may transform evidence for legibility. It may not imply data that do not exist.

This principle allows SCR to pursue spectacular presentation without degrading scientific credibility.

---

## 27. Reporting

Reports are a baseline product capability, not a stretch goal.

A Study or important Run should eventually be able to produce at least:

- interactive UI report;
- printable/exportable report, including PDF;
- machine-readable evidence export;
- stable references to relevant Runs, Readers, and settings.

A report should distinguish clearly among:

- question or hypothesis;
- experimental setup;
- mechanism;
- results;
- Reader-derived measurements;
- human interpretation;
- uncertainty;
- limitations;
- provenance.

Reports should reuse the same evidence and visualization contracts as the interactive product rather than generating a separate narrative truth.

---

## 28. Stretch goal: automatically generated short-form Study videos

A future SCR system should be able to generate concise video summaries directly from real Lab Run and Study data.

This is a stretch goal, but it is worth considering now because the architecture required for trustworthy automated video overlaps heavily with good provenance and visualization design.

A generated video might automatically:

1. identify the Study question;
2. show the initial World;
3. animate the relevant portion of one or more Runs;
4. switch Views when a different visual lens reveals an important event;
5. pause or zoom at Reader-detected findings;
6. compare baseline and changed Runs;
7. display concise evidence-backed annotations;
8. state the outcome and uncertainty;
9. end with links or identifiers for the full Study and report.

Examples:

> **“Why did segmentation fail?” — 42 seconds**  
> Show the baseline propagation, apply the network change, highlight the surviving path, show the Study comparison, then identify the shared identity connection responsible.

> **“This walker survives 19 of 20 starts” — 28 seconds**  
> Show several Runs rapidly, then a Study summary with the one failure and the conditions that distinguish it.

> **“A one-cell change reshaped the entire front” — 35 seconds**  
> Show baseline and Small-Change Run side-by-side, then the Influence View growing through time.

The crucial requirement is the same as for all Visualization:

> **The video edits evidence. It does not fabricate a story.**

Narration, captions, camera selection, pacing, and visual emphasis may be generated. Claims and depicted behavior must trace back to real Run, Study, Reader, or World data.

This capability has obvious communication and marketing value, but it also has practical value: a domain practitioner can send a 40-second evidence summary to a colleague who will not open a full interactive Study.

---

# Part IV — Labs

## 29. Lab

A **Lab** is a problem-focused working environment built on SCR.

A Lab is where domain meaning enters the platform.

The core SCR platform knows how to represent Cells, Worlds, Plugins, Runs, Studies, Readers, and evidence. The Lab knows what those things mean in a specific problem domain.

A mature Lab may define:

- domain vocabulary;
- semantic translation rules;
- World templates;
- Cell property meanings;
- Connection types;
- permitted starting conditions;
- allowed or discouraged Plugin patterns;
- Lab-specific Readers;
- recommended Study patterns;
- reference cases;
- benchmark data where available;
- fit criteria;
- accuracy expectations;
- known abstraction failures;
- known non-goals;
- example hypotheses;
- reporting conventions;
- visualization presets appropriate to the domain.

Examples include:

- Lateral Movement Lab;
- Identity and Privilege Lab;
- Prompt Injection Lab;
- Agent Memory Lab;
- Sensitive Data Lab;
- Wildfire Lab;
- Weather Lab;
- Fish Movement Lab;
- Materials and Microstructure Labs;
- additional ecology, pattern-formation, and physical-process Labs.

The Lab collection is intentionally expected to grow.

---

## 30. Every Lab must earn its fit

Each serious Lab should eventually receive its own technical deep dive and review package.

At minimum that package should answer:

### 30.1 Domain fit
Why is local interaction a defensible abstraction here?

### 30.2 World fit
What does a Cell represent? What do Connections represent? What important relationships are lost?

### 30.3 Mechanism fit
Which domain mechanisms can reasonably be represented as local Plugins, and which cannot?

### 30.4 Time fit
What does one Reactor step mean? Is synchronous stepping meaningful? Are delayed observations needed?

### 30.5 Evidence fit
What Readers correspond to meaningful domain measurements?

### 30.6 Accuracy
Which reference cases, known systems, synthetic benchmarks, or external datasets can test whether the Lab behaves plausibly?

### 30.7 Failure boundaries
Under which conditions would SCR produce a visually convincing but scientifically misleading result?

### 30.8 Comparison to established tools
What existing domain tools already solve this problem better? Where is SCR complementary rather than duplicative?

### 30.9 Transfer limits
If a simple mechanism resembles observed domain behavior, what additional validation is required before treating it as a useful real-world hypothesis?

Labs should be allowed to fail these reviews. A rejected Lab is useful evidence about SCR's boundary.

---

# Part V — Human correction and provenance

## 31. Human corrections are first-class evidence

Humans are not merely consumers at the end of the pipeline.

A domain expert may say:

> That trust direction is backwards.

> Those are disconnected bursts, not one propagating front.

> The fish would never observe that variable directly.

> This Reader is counting retry storms as compromise spread.

SCR should preserve:

- the original machine proposal or interpretation;
- the human correction;
- the reason where provided;
- the resulting change;
- who or what supplied the correction;
- which later Runs, Studies, or Reader results depend on it.

A correction should not silently rewrite history.

The platform should make disagreement inspectable.

---

## 32. Provenance should be boringly complete

Every important result should be traceable to the inputs and software that produced it.

The exact technical schema belongs in later requirements, but the conceptual provenance chain includes:

- human request or generation objective;
- rendered model inputs where models are used;
- model identity and relevant parameters;
- raw model outputs where appropriate;
- proposed mechanism;
- Plugin source;
- repair history;
- Plugin validation results;
- World and World version;
- Reactor version;
- Run settings;
- seeds or controlled randomness state as required;
- Reader identity and version;
- Study definition;
- human corrections;
- report and visualization versions where they make interpretive claims.

The provenance system should be designed so future reviewers can distinguish “we cannot reproduce this because the model is stochastic” from “we failed to record what we asked the model.”

---

# Part VI — Platform services

## 33. Platform Services

Conventional software infrastructure supports the conceptual platform but must not define its scientific assumptions accidentally.

Platform Services include:

- jobs and workers;
- persistent storage;
- object storage where needed;
- API;
- identity;
- authorization;
- execution isolation and resource control;
- transport;
- frontend delivery;
- observability;
- configuration;
- backup and recovery;
- deployment;
- migration and version management.

The 2.x product deliberately used a simple local architecture: SQLite, synchronous generation over a streamed HTTP request, local execution, and a React frontend. Those choices were appropriate for the toy and should be treated as evidence, not constraints on 3.x.

The conceptual contracts in this document should remain meaningful if the implementation later uses queued jobs, distributed workers, PostgreSQL, object storage, GPU-backed visualization, or other production infrastructure.

---

# Part VII — Conceptual boundaries

## 34. Component ownership map

### Cell
Owns: local state-bearing participant.  
Does not own: domain meaning, execution order, global behavior.

### World / World Layout
Owns: experimental environment, Cells, Connections, visibility, starting conditions.  
Does not own: generated mechanism, interpretation of results.

### Generation
Owns: propose, write, check, test, repair, deliver.  
Does not own: execution truth or scientific validity.

### Plugin
Owns: readable implementation of a local mechanism.  
Does not own: experimental law outside its declared capabilities.

### Reactor
Owns: execution semantics and authoritative state transitions.  
Does not own: domain meaning or post-hoc interpretation.

### Run
Owns: immutable history of one exact execution.  
Does not own: claims of robustness or causation.

### Study
Owns: structured multi-Run question or hypothesis.  
Does not own: domain truth beyond the evidence it actually collected.

### Reader
Owns: reproducible derived measurement or interpretation.  
Does not own: underlying Run history.

### Corpus
Owns: durable relationships among meaning, mechanisms, evidence, failures, and corrections.  
Does not own: operational telemetry merely because it is stored somewhere.

### Search
Owns: retrieval across the Corpus.  
Does not own: generation or execution.

### Visualization
Owns: evidence-backed visual representations and time navigation.  
Does not own: fabricated scientific claims.

### Lab
Owns: domain assumptions, vocabulary, fit, accuracy, specialized Readers and Studies.  
Does not own: core execution semantics.

### Platform Services
Owns: reliable operation of the product.  
Does not own: the conceptual scientific model.

---

## 35. Conceptual flow

A simplified mental model is:

```text
                         HUMAN
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
        WORLD          GENERATION               READERS
                          │                        ▲
                    propose / write                │
                    check / repair                 │
                          │                        │
                          ▼                        │
                        PLUGIN                     │
                          │                        │
                          ▼                        │
                       REACTOR                     │
                          │                        │
                          ▼                        │
                         RUN ──────────────────────┘
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
                         HUMAN
```

This is not intended as a call graph or final package structure. It is the conceptual map people should be able to hold in their heads.

---

# Part VIII — Repository and documentation architecture

## 36. Documentation hierarchy

The 3.x repository should distinguish several kinds of documentation rather than allowing one omnibus to become permanent doc hell.

### Level 1 — Foundations
What the system is and what major concepts mean.

This document belongs here.

### Level 2 — Architecture Decisions
Small records explaining consequential choices, alternatives, and reconsideration triggers.

Examples:

- keep Cell as the basic state-bearing unit;
- use Lab as the domain boundary;
- keep Plugin source human-readable;
- Readers never alter Runs;
- Runs are immutable;
- generated Plugins cannot exceed declared World capabilities;
- Visualization must trace meaningful properties to evidence;
- Study is a first-class object.

### Level 3 — Requirements
Stable, testable product and subsystem contracts with permanent identifiers.

### Level 4 — Technical Deep Dives
Implementation-level descriptions of each subsystem as built.

### Level 5 — Lab Papers
Domain-specific fit, accuracy, limitations, references, benchmarks, and evidence.

### Level 6 — Operations and User Documentation
Deployment, administration, API use, Lab operation, and human workflows.

---

## 37. Initial documentation tree

A reasonable starting structure is:

```text
docs/
├── 00-start-here/
│   ├── what-is-scr.md
│   ├── foundations-and-platform-architecture.md
│   ├── human-and-machine.md
│   ├── language-rules.md
│   └── glossary.md
│
├── 01-core/
│   ├── cells.md
│   ├── worlds.md
│   ├── generation.md
│   ├── plugins.md
│   ├── reactor.md
│   ├── runs.md
│   ├── studies.md
│   ├── readers.md
│   ├── corpus.md
│   ├── search.md
│   ├── visualization.md
│   └── labs.md
│
├── 02-platform/
│   ├── jobs-and-workers.md
│   ├── storage.md
│   ├── api.md
│   ├── identity-and-access.md
│   ├── execution-safety.md
│   ├── frontend.md
│   ├── transport.md
│   └── observability.md
│
├── 03-quality/
│   ├── testing.md
│   ├── repeatability.md
│   ├── accuracy.md
│   ├── reference-cases.md
│   └── human-review.md
│
├── 04-decisions/
│   └── ...
│
└── labs/
    ├── security/
    ├── weather/
    ├── ecology/
    ├── wildfire/
    ├── materials/
    └── ...
```

The source tree should be designed after these ownership boundaries are reviewed, rather than mechanically mirroring this documentation tree.

---

# Part IX — What 2.x proved, and what 3.x must not accidentally inherit

## 38. Proven ideas worth carrying forward

The current 2.x implementation demonstrates several valuable principles:

### 38.1 Semantic proposal before implementation
The generation pipeline separates an English proposal from Python implementation and validates the result before admitting it as a working rule.

### 38.2 Generated code is constrained by fixed execution machinery
The generated rule proposes state while the fixed engine controls randomness, bookkeeping, derived state, and stopping.

### 38.3 Reproducibility is tested
The existing validation pipeline includes deterministic trial execution and reproducibility checks.

### 38.4 Failures are retained
Broken implementations and rejected generation attempts remain durable records with provenance.

### 38.5 Runs complete before playback
Playback is navigation over stored history rather than a coupled live simulation.

### 38.6 Computational state and visual appearance are not the same thing
A quiet-looking picture does not necessarily mean the computational state has stopped evolving.

### 38.7 Visualization can reveal different truths without changing the Run
Multiple render styles can be applied to the same stored history.

### 38.8 The library/corpus is more important than any one rule
The durable value comes from linking stated intent, implementation, execution, measurements, failures, ancestry, and human corrections.

---

## 39. 2.x assumptions that are not automatically 3.x requirements

The following should be treated as implementation history rather than sacred architecture:

- fixed 200×200 grids;
- toroidal boundaries;
- only grid-neighborhood interaction;
- synchronous local HTTP generation;
- no job queue;
- SQLite as the long-term store;
- a single local execution host;
- the exact current optional Cell properties;
- exact existing classification labels;
- the current REST route structure;
- the current frontend routing system;
- the current limited visual renderer;
- the current exact validation limits;
- the current model provider and prompt structure.

3.x should preserve lessons, not accidents.

---

# Part X — Questions deliberately left open

## 40. Open architecture questions

This document intentionally does not resolve every implementation choice.

Questions for subsequent critique and decision records include:

1. **Plugin contract:** What exact Python surface is expressive enough for Grid, Network, Identity, and Agent Worlds while remaining readable and enforceable?
2. **World storage:** What common representation can handle spatial and relational Worlds without forcing one into the other's shape?
3. **Execution model:** Which Worlds remain synchronous-step systems, and where do timed or event-like semantics become necessary?
4. **Study planner:** How much should SCR infer automatically from a semantic question before requiring human confirmation?
5. **Reader trust:** How should Readers expose uncertainty and known failure cases in ordinary UI language?
6. **Corpus identity:** How are Same-Mechanism Families recognized without hiding meaningful implementation differences?
7. **Search:** How should intent similarity, mechanism similarity, and observed-behavior similarity be kept distinct?
8. **Visualization scale:** What evidence formats are required so advanced 3D Views do not require replaying entire Runs server-side?
9. **Video generation:** What provenance must be attached to generated narration and visual edits so a short video can never outrun the evidence?
10. **Lab governance:** What minimum evidence is required before a Lab is described as validated rather than experimental?
11. **Security isolation:** What production execution boundary replaces the local 2.x assumption of a hardened single-user host?
12. **Model independence:** Which parts of Generation should be provider-neutral, and how should model changes be represented in provenance?
13. **Human edits:** When a human directly modifies Plugin Python, how should intent and provenance be updated so the semantic chain remains honest?
14. **Live work:** If future Labs need live streams, how are provisional live observations separated from finalized immutable Runs?
15. **External calibration:** How should SCR package candidate mechanisms for serious domain tools without implying domain validity it has not earned?

These questions should become explicit architecture decisions or requirements rather than being answered accidentally during implementation.

---

# Part XI — Non-claims and discipline

## 41. SCR does not claim that simple cellular mechanisms predict arbitrary domains

A mechanism that reproduces an observed pattern is a candidate explanation, not proof of real-world causation.

The system's proposed value is upstream of domain prediction: it can supply, test, index, and compare candidate mechanisms cheaply and reproducibly.

Domain calibration and validation remain domain problems.

A Lab paper must say explicitly where SCR stops and established domain tooling begins.

---

## 42. SCR does not claim exhaustive rule-space exploration

Language-model generation samples according to model priors, prompts, Corpus history, Lab vocabulary, and exploration strategy.

Coverage measurements may describe the space SCR has defined for itself. They must not be misrepresented as exhaustive coverage of all possible local mechanisms.

---

## 43. SCR does not treat model fluency as scientific authority

A model can write persuasive explanations that are wrong.

Therefore:

- code is checked;
- Runs provide evidence;
- Readers are deterministic where feasible;
- provenance is retained;
- human corrections remain visible;
- Labs carry their own accuracy obligations;
- claims should cite external evidence where domain validity is at issue.

Language models are high-leverage contributors to the workflow. They are not an oracle layer above it.

---

# Part XII — Foundational rules, condensed

## 44. The compact version

1. **Semantic first.** Humans work primarily through meaning.
2. **Readable and writable, always.** Generated mechanisms remain inspectable Python.
3. **Automation is not the objective. Better allocation of work is the objective.**
4. **Humans do judgment work. Machines absorb mechanical work.**
5. **Plain language is a system property.**
6. **Intent, implementation, and outcome remain separate.**
7. **Cells are the basic state-bearing participant.**
8. **Worlds define experimental reality.**
9. **The Plugin proposes. The Reactor decides.**
10. **Runs are immutable evidence.**
11. **Readers read; they do not rewrite.**
12. **A Run shows what happened once. A Study tests a hypothesis.**
13. **Failures stay.**
14. **The Corpus is the durable asset.**
15. **Search returns evidence and mechanisms to human questions.**
16. **Labs own domain assumptions and must earn their fit.**
17. **Visualizations may dramatize evidence; they may never invent it.**
18. **Reports and videos must trace claims back to evidence.**
19. **Security exceptions are not exceptions; hostile conditions are explicit experimental capabilities.**
20. **SCR proposes mechanisms and preserves evidence. Domain truth requires domain validation.**

---

# Part XIII — Review targets for external critique

## 45. Questions for reviewers

Reviewers should challenge this document on architecture rather than prose polish.

Please look specifically for:

1. **Missing foundational components.** Is an important concept being hidden inside another component that deserves its own ownership boundary?
2. **False separations.** Are two components actually the same responsibility with different names?
3. **Semantic leaks.** Where does the architecture force a human back into implementation mechanics unnecessarily?
4. **Opacity risk.** Where could an optimized or AI-generated internal representation displace the readable human artifact?
5. **Reactor boundary failures.** Are there mechanisms a Plugin would need that cannot be modeled cleanly without letting it redefine the experiment?
6. **Study weakness.** Does Study have enough conceptual weight to support real hypothesis testing rather than merely batch Runs?
7. **Reader truth confusion.** Where might derived analysis become indistinguishable from immutable evidence?
8. **Lab leakage.** Which domain assumptions have accidentally entered the platform core?
9. **Visualization deception risk.** Which proposed Views could look causal or scientific while representing only correlation, similarity, or presentation choices?
10. **Corpus provenance gaps.** What future question could not be answered because this architecture failed to preserve the right source information?
11. **2.x inheritance.** Which assumptions are being preserved merely because the prototype happened to use them?
12. **Over-generalization.** Where is SCR becoming a generic simulator instead of remaining recognizably cellular/local-mechanism ruliology?
13. **Under-generalization.** Which promising Labs would be excluded by an unnecessarily grid-shaped or synchronous core?
14. **Product clarity.** Can a practitioner understand the relationship among Lab, Study, Run, Reader, Plugin, Reactor, and Corpus without reading implementation docs?
15. **Falsifiability.** Which claims about SCR's value could be tested and fail?

Reviewers are encouraged to propose deletions and boundary changes, not merely additions.

---

# Source basis and references

This document is a new 3.x foundational design. It is not a rewrite of the 2.x requirements. The following internal project documents were used as evidence for what the existing system demonstrably does and which design lessons have already survived implementation.

1. **Engine Internals — Release 2.2.1.** Documents the `Cells` state model, declarations, geometry, helpers, controlled randomness, tick order, fingerprints, run loop, classifier, and the principle that generated rules propose while fixed engine code applies modifiers, randomness, derived state, and stopping behavior.
2. **Storage & Transport — Release 2.2.1.** Documents immutable recorded history, stored Runs and ticks, reconstruction, playback transport, and the distinction between permanent Corpus/history data and mutable operational telemetry.
3. **Contract Enforcement — Release 2.2.1.** Documents the restricted generated-code language, static and runtime checks, child-process limits, reproducibility checks, and retention of rejected/broken generation attempts.
4. **Generation Pipeline — Release 2.2.1.** Documents the Stage A semantic proposal, Stage B readable Python implementation, Stage C validation/trial/reproducibility process, repair attempt, provenance, and coverage history.
5. **API & Authentication — Release 2.2.1.** Documents the existing HTTP and streaming surface, run access, immutable correction boundary, identity support, and system observability.
6. **Frontend — Release 2.2.1.** Documents the stored-history playback model, slider/scrubbing interaction, multiple render styles, visualization design, and the deliberate distinction between visible pattern and full computational state.
7. **ASR Omnibus Requirements v3.** Provides the existing plain-language requirement, stable requirement practice, exact current contract, and rationale for many 2.x decisions. It is treated here as prior-art evidence, not as the 3.x contract.
8. **A Card Catalog for Emergence: Intent-Indexed Cellular Automata as a Mechanism-Hypothesis Engine — position paper v0.1.** Provides the prior mechanism-hypothesis framing, Corpus/search argument, and explicit non-claim that retrieved mechanisms are domain predictions.

### External references

No external technical citations are required to justify the conceptual boundaries in this foundations document. It intentionally makes few claims about external domains. Lab papers, accuracy reviews, benchmark documents, and claims about scientific or security applicability should use extensive external references and should distinguish established domain knowledge from SCR-generated evidence.

SCR should continue to credit Stephen Wolfram's work on cellular automata and ruliology as inspiration while making no claim that SCR reproduces or improves that work. The 3.x line is a distinct semantic, experimental, and product direction built from that inspiration.

---

## Closing statement

Semantic Cellular Ruliology begins from a simple observation: the bottleneck in experimentation is often not running one more computation. It is translating a human question into a precise experiment, implementing it without introducing clerical mistakes, repeating it enough times to learn anything, preserving what actually happened, and returning the result in a form a human can understand.

Language models substantially change the cost of that translation and implementation work. They do not remove the need for controlled execution, provenance, human judgment, or domain validation. They make it possible to spend those scarce human resources where they matter more.

SCR therefore treats semantics, executable mechanisms, deterministic evidence, structured Studies, and human interpretation as parts of one continuous system.

The ambition is not to build a machine that replaces the person asking the question.

It is to build a machine that makes asking—and actually testing—the next good question dramatically cheaper.
