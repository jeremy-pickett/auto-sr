# Semantic Cellular Ruliology 3.x
## Critique of the Core Contract Starter Set
### Cells · Worlds · Plugins · Reactor · Runs

**Status:** architectural critique of first-pass seam documents  
**Scope:** `cells.md`, `worlds.md`, `plugins.md`, `reactor.md`, `runs.md`  
**Intent:** critique the set as a connected contract, not as five finished requirements documents.

---

## Executive assessment

This is a strong starter set.

More importantly, it is strong for the right reason: the documents are not pretending to be finished requirements. They are doing the harder early job of discovering where ownership is unclear, where two components accidentally claim the same thing, where no component claims something important, and where a plausible implementation choice would quietly become an experimental assumption.

That approach is already paying off. All five documents independently discover the same declaration chain:

> **World declares what exists → Plugin declares what it uses → Reactor enforces the match → Run records the agreement.**

That is not editorial duplication. It is architectural evidence. When five component documents independently point at the same missing seam, the seam is probably real.

The set also preserves several excellent boundaries:

- A **Cell** is state, not behavior.
- A **World** defines the setting, not what occurs in it.
- A **Plugin** proposes changes but does not control execution.
- The **Reactor** owns execution semantics.
- A **Run** is immutable evidence, not an actor.
- Interpretation belongs downstream, primarily to **Readers** and **Studies**.
- Hostile or unusual conditions are modeled as declared experiment capabilities, not as excuses to let generated code escape the contract.

Those are very good foundations.

The largest issue is not that the set is missing detail. Detail is supposed to come later. The largest issue is that several of the open questions are not independent. They are different faces of one missing concept: **the frozen agreement under which a Run is admitted and executed.**

I recommend treating that as the main target of the next architectural pass.

---

# 1. The most important missing shape: the Run Contract

The documents correctly resist resolving the shared seam prematurely, but the seam is now sharp enough to name provisionally.

The platform needs an immutable artifact that says, in effect:

> **This exact World offers these properties, connections, views, and capabilities.  
> This exact Plugin requests these reads, writes, helpers, effects, and reach.  
> This exact Reactor version can supply and enforce them under these execution rules.  
> This Run was admitted under that exact agreement.**

For this critique I will call it the **Run Contract**. The name is intentionally plain and can be replaced later.

This does **not** necessarily require a sixth active component.

A clean ownership model could be:

- **World** publishes what exists and what the setting requires.
- **Plugin** publishes what it needs and what it may propose.
- **Reactor** performs the authoritative match at admission.
- **Run** stores the resulting Run Contract permanently.
- **Generation** may perform the same match earlier as a cheap preflight check, but the Reactor remains authoritative because it is the component that will actually execute the Plugin.

That distinction matters. “Generation checked it” is useful. It should never become “therefore the Reactor may assume it was checked.”

This one artifact would resolve or clarify several gaps already found by the set:

- Who performs the declaration match?
- What derived or Reactor-supplied values may a Plugin read?
- Which execution capabilities are required and offered?
- What state is future-relevant?
- What exactly was a Plugin permitted to do during an old Run?
- Whether two old Runs executed under the same contract even if implementation details later changed.
- How a hand-edited Plugin becomes a new executable artifact without silently inheriting the old agreement.

The important architectural principle is not the proposed name. It is that **the agreement should be explicit, frozen, inspectable, versioned, and stored with the Run rather than reconstructed years later from several current documents.**

---

# 2. The current replay decision looks like a false binary

`reactor.md` and `runs.md` both treat DEC-2 as a choice between exact replay to the last value and replay that honors a looser contract.

I do not think SCR should choose only one.

Those are two useful promises with different names.

### Exact replay

Given the archived implementation, Reactor build, dependency environment, random material, starting state, pending events, and every other future-relevant input, SCR reproduces the recorded state exactly.

This is the strongest forensic promise.

It may require container images, exact numeric-library versions, hardware restrictions, or other expensive provenance. That cost can be evaluated honestly.

### Reproduction under contract

A later Reactor or backend executes the same declared experiment and satisfies a defined equivalence standard even if irrelevant implementation details differ.

This is the stronger long-term scientific/product promise because software evolves.

Both are valuable.

The mistake would be overloading the word **replay** until every future argument is really an argument about which of these somebody meant.

**Recommendation:** define exact replay and contract reproduction separately. Store enough provenance to support the strongest level practical for a given Run. Never silently downgrade one into the other.

---

# 3. Comparability is probably not a property of two Runs

`runs.md` correctly notices that “what makes two Runs comparable” is undefined.

I would push harder: there may be no useful global yes/no answer.

Two Runs are comparable **for a question**.

Examples:

- A Repeat Test may deliberately vary the start while holding Plugin, World structure, Reactor, and settings fixed.
- A World Comparison deliberately varies one World feature.
- A Plugin Comparison deliberately varies the mechanism.
- A Reactor regression test deliberately varies Reactor version.
- A security Study may deliberately vary what one participant can observe.

Therefore the Study should probably define the **comparison contract**:

> These fields must match.  
> These fields are deliberately varied.  
> These differences are irrelevant to this hypothesis.  
> Any other difference invalidates the comparison.

The Run's responsibility is simpler and stronger:

> **Expose complete bound identity and provenance so a Study can decide whether its comparison is valid.**

That preserves the excellent Run/Study boundary without forcing Run to contain a universal theory of comparability.

---

# 4. The starting-state conflict wants a separate concept

`worlds.md` finds a real contradiction: the World appears to own starting state, while the earlier system let the mechanism create it.

The proposed compromise — a Plugin may propose a start but the World adopts and records it — is reasonable, but there is an even cleaner possibility:

> **World and Starting State may be separate first-class inputs to a Run.**

### World
The durable setting: Cell schemas, Layout, connections, static conditions, observability rules, declared external inputs, and required Reactor capabilities.

### Starting State
The realized initial values for one Run or one family of Runs.

A Study can then truthfully say:

> “Hold the World constant and vary the Starting State.”

That is exactly what a Repeat Test often wants.

A Plugin or Lab may provide a **Start Recipe** or suggest a valid Starting State without owning the actual realized state.

This distinction also improves provenance. A random start is not merely “seed 1234”; the Run can bind the exact realized start and the recipe/seed that produced it.

I would strongly test this split before making starting state part of World identity.

---

# 5. Dynamic conditions need an external/reactive distinction

DEC-1 currently absorbs a very large problem: is wind/current/drift part of the World or another mechanism?

A useful distinction may be:

### External input
A value or schedule declared in advance that does **not** react to the simulated state.

Examples: recorded wind field over time, fixed tide schedule, precomputed temperature series, planned network maintenance event, scheduled credential expiry.

This can belong to the setting/Run Contract because it is an input.

### Mechanism
A process whose future behavior depends on simulated state.

Examples: fire altering local airflow in a coupled model, fish changing a resource that changes fish movement, attacker changing strategy in response to defender action, defender containment reacting to observed compromise.

That is a Plugin or composed mechanism.

This distinction avoids making every changing environmental value into a Plugin while also avoiding a World that secretly contains reactive behavior.

---

# 6. Mechanism composition is not merely “several Plugins”

The documents are right to treat composition as dangerous.

The most important observation is that if the Reactor simply chooses ordering or conflict resolution, **the Reactor has accidentally authored a mechanism nobody declared.**

If SCR permits several Plugins in one Run, composition itself must be explicit experimental semantics.

At minimum the Run Contract would need to state:

- which Plugins participate;
- whether they read the same prior state or each other's applied results;
- whether proposals are simultaneous or ordered;
- how conflicting proposals are resolved;
- how scheduled effects interact;
- how budgets are divided;
- whose proposal caused each accepted state change where provenance matters.

A particularly clean default would be:

> **All Plugins read the same current state, all produce proposals, and the Reactor applies a named, versioned conflict policy.**

Some Labs will legitimately need turns or ordered phases. Those should be explicit named execution models, not incidental list order.

**Composition policy is part of the experiment and therefore versioned provenance.**

---

# 7. The Cell heterogeneity issue is genuinely foundational

`cells.md` correctly identifies multi-shape Cells as its largest gap.

This is not a storage detail.

A terrain grid can plausibly use one Cell schema everywhere. An Identity World cannot honestly pretend that a user account, group, role, permission, service account, and resource all carry the same meaningful properties.

Forcing a universal superset schema creates meaningless empty fields and subtly biases the platform toward lattice-style Worlds.

I would therefore lean toward **multiple declared Cell schemas within one World**, while keeping every individual schema strictly bounded.

That does make matching, Readers, storage, and visualization harder. The cost is real.

But the alternative risks making Network, Identity, and Agent Worlds nominally supported while architecturally second-class.

One caution: do not let “multiple schemas” turn into arbitrary object graphs. A good implementation can still be columnar and bounded, with each Cell type owning a fixed small property set and connections identifying compatible source/target types.

---

# 8. “Bounded” needs several ceilings, not one number

`cells.md` asks whether bounded means per property, per Cell, per World, or per Run.

The likely answer is: **all of them, for different reasons.**

Separate at least:

### Semantic ceiling
Prevents a Cell from becoming an embedded program or unbounded memory store.

### Execution budget
Prevents an otherwise valid experiment from exhausting practical resources.

Possible separate limits include property count per Cell schema, value types, bytes per Cell, Cell count, connection count, Plugin-owned state, pending effects, pending events, and total Run state.

The Reactor may enforce both, but they exist for different reasons and should fail differently.

---

# 9. Plugin trust should be author-independent

`plugins.md` says the Plugin cannot be trusted by construction because it is the only component written by a machine on demand.

The asymmetry is real, but I would change the reason.

A Plugin should be treated as untrusted experimental code **regardless of who wrote it**.

Generation may write it. A person may edit it. A Lab author may ship one. A future API client may submit one. One model may repair code written by another.

The more durable rule is:

> **Platform code is part of the trusted execution base. A Plugin is variable experiment code and must satisfy the same contract regardless of author.**

This also solves DEC-18 conceptually. A hand edit creates a new Plugin revision. It does not become more privileged because a person touched it.

The semantic description may now be stale, so the platform should mark that fact and either ask for confirmation, regenerate a description from the edited code, or preserve both the previous intent and the new unconfirmed implementation.

---

# 10. Mechanical compatibility and domain fitness are different

`plugins.md` asks how a Plugin says which Worlds it can act on.

There are really two questions.

### Mechanical compatibility
Does the World provide what the Plugin declares it needs?

Examples: required property exists, type/range is compatible, needed connection class exists, requested reach is allowed, needed Reactor capability is available.

This should be derived automatically from declarations wherever possible.

### Domain fitness
Does using this mechanism in this World make sense?

A Plugin might mechanically fit two Worlds whose properties happen to have the same shape while being scientifically nonsensical in one.

That belongs to the Lab, Study, or human/domain review.

Do not create one `compatible_worlds` label and pretend it answers both.

---

# 11. Reach should be defined by allowed paths, not only distance

`plugins.md` is right that “local” becomes dangerous once the platform leaves the lattice.

A useful generalization is:

> **A Plugin may only affect or observe Cells reachable through explicitly declared local operations.**

For a grid, that may be bounded geometric neighbors. For a Network World, one or a few declared connection hops. For an Identity World, membership/trust relationships.

For wind-blown embers, seed dispersal, scanning, or other jumps, the long-range effect should ideally happen through a named transport capability or declared connection mechanism rather than arbitrary address access.

The dangerous endpoint is not “a jump of length 8.” It is:

> **Plugin may inspect or modify arbitrary Cell N because it knows N exists.**

That is where the local-mechanism premise collapses.

---

# 12. Observability needs three states, not one noun

`worlds.md` correctly says observability is currently only named.

This deserves early treatment because security and agent Labs will depend on it.

A useful model from the earlier 3.x architecture discussion is:

### World State
What is actually true in the experiment.

### Seen State
What a particular Cell/participant/Plugin is allowed to observe at that point in execution.

### Recorded State
What the omniscient Reactor records as evidence.

These must not be conflated.

Seen State may be partial, delayed, filtered, stale, role-dependent, or connection-dependent. Recorded State should remain sufficient for replay and later Readers.

This lets SCR model stale identity data, delayed telemetry, partial attacker knowledge, hidden defender state, and similar conditions without cheating.

---

# 13. Future-relevant state needs a formal closure rule

`reactor.md` correctly calls this its largest gap.

This is not merely a fingerprint implementation detail.

For deterministic recurrence and stopping, the Reactor needs the complete state from which the future is determined.

That may include:

- Plugin-readable and Plugin-writable Cell properties;
- Reactor-owned derived values that may affect future Plugin output;
- scheduled events;
- execution phase;
- pending effects;
- external-input position;
- random generator state if later draws remain possible;
- composition phase/order state;
- any other declared state that can influence a future step.

The principle should be:

> **If changing a value could change any future accepted proposal or Reactor action, that value is future-relevant.**

And its complement:

> **If changing a value cannot affect any future execution, it must not prevent recurrence.**

The earlier 2.x behavior around skipped random draws is a very good warning: a seemingly harmless bookkeeping action can become execution semantics if it changes future state.

I would require the Reactor to build the future-relevant state definition from the frozen Run Contract rather than from hand-maintained special cases.

---

# 14. Stopping facts versus Reader conclusions is an excellent correction

The strongest conceptual correction in the set may be:

> *State at step 900 matched state at step 850* is a fact.  
> *This is a stable oscillator* is a reading.

Keep this.

The Reactor may record facts such as execution budget exhausted, no accepted proposal changed future-relevant state, state exactly matched a previous state, external stop received, resource limit triggered, or an execution error occurred.

Readers may label those facts settled, repeating, oscillator, deadlocked, stable, noisy, structured, and so on.

This protects old evidence from later improvements in interpretation and preserves the earlier 2.x lesson that visual quiet and computational quiet are not the same thing.

---

# 15. Steps-to-outcome is valuable, but do not call it question hardness

`runs.md` proposes steps-to-outcome as a rough measure of how hard the question was.

Keep the measurement. Change the claim.

Number of simulated steps tells us something important about modeled process duration and iterative depth. It does **not** by itself measure computational difficulty.

A 10-step Run over ten million Cells with an expensive Plugin may cost more computation than a 50,000-step Run over a tiny World.

Preserve at least steps executed, wall time, CPU/GPU time where useful, peak memory, Cell/connection scale, accepted effects/changes, and steps until a named Reader event where applicable.

Then Studies can decide what notion of “cost” matters.

---

# 16. A rejected admission may not be a Run

`runs.md` says “A failed Run is a Run” and then discusses a mechanism refused at the door.

There is a terminology seam here.

If the Reactor refuses admission before execution starts, either:

### Option A
A Run identity already exists and can end in `not_admitted`.

### Option B
A Run begins only after admission, and the rejected item is an Attempt or Admission Failure.

Either design can work.

What should not happen is using “Run” sometimes to mean a planned attempt and sometimes to mean an admitted execution.

Because failures are first-class evidence, SCR probably needs a durable umbrella record for attempts whether or not they became Runs.

---

# 17. Lab identity should be provenance, not necessarily execution state

`runs.md` lists the Lab contract among what a Run binds.

That may be correct, but distinguish two cases.

If Lab code or Lab-defined semantics directly affect execution, their exact version is part of the Run Contract.

If the Lab is only the domain organization that produced the World, Plugin, and Readers, then the exact low-level artifacts may already be sufficient for replay, while Lab identity is provenance/context.

That matters because future work may move the same mechanism between Labs, let one Study use Readers from several Labs, or discover that a general mechanism belongs to no single Lab.

Avoid making “one Run belongs to exactly one Lab” an accidental execution constraint unless that is actually intended.

---

# 18. World storage must not make relational Worlds pretend to be grids

`worlds.md` already warns that storage can bias the entire platform.

This deserves a concrete warning for reviewers who know only the 2.x implementation.

The original toy gained major performance benefits from fixed grid-shaped NumPy arrays. That should not become a default representation for relational Worlds.

In particular, avoid representing connections as `number_of_cells × maximum_degree` unless the World family truly has bounded near-uniform degree.

Identity and network systems commonly have high-degree hubs: identity providers, large groups, service accounts, shared services, routing nodes.

A compact edge representation is likely a better starting point: source Cell, target Cell, connection type, optional bounded connection state, and offsets/indexes for fast neighbor lookup.

The implementation can still be vectorized and deterministic without pretending every World is a lattice.

---

# 19. The five documents are strongest when they describe refusals

The repeated “What it refuses, and who owns it instead” section is excellent.

I would preserve this template throughout the core documentation.

For the deep pass, consider requiring each component document to contain four permanent sections:

1. **Owns**
2. **Refuses**
3. **Requires**
4. **Produces**

The current drafts mostly contain those already under slightly different headings.

This becomes especially valuable when Claude or another coding agent works on one subsystem in isolation. It gives the model explicit negative constraints instead of forcing it to infer boundaries from prose.

---

# 20. The set needs one vocabulary decision around mechanism / Plugin / rule

The starter docs consistently use **Plugin** as the executable mechanism, which is good.

But future Lab papers and the older 2.x corpus will inevitably use rule, mechanism, Plugin, behavior, and model.

A useful distinction could be:

- **Mechanism** — the idea expressed semantically.
- **Plugin** — one executable implementation of that mechanism.
- **Rule** — legacy 2.x term or narrow cellular-automaton term, not the general 3.x architecture noun.
- **Behavior** — what is observed.
- **Reader result** — a measured interpretation of behavior.

This matters for manual edits and repairs. Two Plugins may implement the same intended mechanism. One Plugin revision may cease to represent the same mechanism after a human edit.

---

# 21. Context from SCR 2.x that reviewers should know

These five starter documents are easier to critique correctly if the reviewer knows what was already demonstrated in the 2.x toy.

### 2.x separated proposal from execution

Generated rule code proposed the next state. Fixed engine code owned random draws, modifiers, derived properties, tick semantics, and stopping.

That is the ancestor of:

> **The Plugin proposes. The Reactor decides.**

### 2.x generation already used a semantic-to-code-to-proof pipeline

The working pipeline was broadly:

> semantic proposal → readable Python → static/contract checks → trial execution → reproducibility check → one repair attempt → canonical Run

This is why 3.x can reasonably treat Generation as more than a text generator.

### 2.x stored failures deliberately

Broken implementations and proposal failures were retained with provenance instead of disappearing.

### 2.x separated computational state from visible pattern

A picture could become visually quiet while hidden or derived state still changed.

That is the historical reason the Reactor/Reader boundary around stopping vocabulary matters so much.

### 2.x playback was navigation over immutable history

Runs completed before playback. The UI scrubbed stored evidence rather than controlling a live simulation.

That is why backwards stepping, alternate render styles, future Readers, and later visualizations can all operate on the same evidence.

### 2.x was grid-first and should not dictate 3.x

The old implementation used a 2-D grid, bounded neighborhood helpers, and parallel NumPy arrays. Those were excellent decisions for the toy.

3.x explicitly intends to support relational Worlds, so those implementation details are evidence of what worked in one World family, not universal platform law.

---

# 22. Context from the 3.x rethink that reviewers should know

Several architectural intentions may not be obvious from these five files alone.

### “Semantic” is literal

The normal human interface is meaning first.

People describe Worlds, mechanisms, tests, changes, and questions in ordinary language. LLMs remove mechanical work such as implementation, checking, repair, repetition, bookkeeping, and transcription.

The goal is not to hide code.

> **Automation is not the objective. Better allocation of work is the objective.**

### Plugins remain readable and writable

The canonical executable mechanism is intended to remain inspectable and editable by a competent person.

### Study is a major first-class object

A Run says what happened once.

A Study asks whether it matters.

Repeat Tests, Small-Change Tests, Try Many Settings, World comparisons, and Plugin comparisons belong here.

### Labs own domain meaning

The core platform should not know what wildfire, fish, lateral movement, prompt injection, IAM privilege, or crystal growth mean.

Labs translate domain meaning into Worlds, Plugins, Readers, Studies, fit checks, and accuracy expectations.

### Visualization is intended to be real instrumentation

SCR will eventually need dramatic 2-D and 3-D views, but every visual property must come from real Run, Study, or Reader data.

Visuals may dramatize evidence. They may not invent it.

---

# 23. Recommended decision order

Not every open decision has equal blocking power.

## Tier 1 — blocks the contract itself

1. **Run Contract / declaration-chain ownership**
2. **Cell schema multiplicity**
3. **Starting State ownership**
4. **Reach/locality**
5. **Composition semantics**

## Tier 2 — blocks strong evidence claims

6. **Future-relevant state**
7. **Exact replay versus contract reproduction** — preferably define both
8. **Fact versus Reader interpretation**
9. **Study comparison contracts**

## Tier 3 — can be detailed after the model is stable

10. **Specific Cell ceilings**
11. **Effect budgets**
12. **Storage encodings**

---

# 24. Per-document critique

## `cells.md`

### Strongest parts

The opening “Cell decides nothing” is excellent.

The bounded-state argument is also unusually important. It correctly connects implementation restraint to the scientific claim of emergence: if arbitrary programs or unbounded memory can hide inside a Cell, the platform can fake complexity in state rather than produce it through repeated local interaction.

### Main issues

The multi-schema problem must be registered as a real decision immediately.

The document should distinguish semantic ceilings from execution budgets before assigning numbers.

“What the state is worth → Reader” is slightly odd wording. A Reader measures state; a person or Study may decide significance. Minor, but worth tightening because the rest of the ownership table is precise.

---

## `worlds.md`

### Strongest parts

“The World decides everything about the setting, and nothing about what happens in it” is a very good boundary.

Making Layout owned by World rather than a freely swappable sibling is also a good anti-invalid-state design.

The document correctly spots that three of four proposed Layout families are still theoretical and should not receive confidence merely because Grid World worked.

### Main issues

Starting State probably deserves separation from World identity.

Dynamic conditions need the external-input versus reactive-mechanism distinction.

Observability needs a full model of World State, Seen State, and Recorded State.

“Two Worlds that differ in any declared way are different Worlds” may be too strict if World versions contain metadata that does not affect execution. Better to distinguish execution identity from descriptive metadata identity.

---

## `plugins.md`

### Strongest parts

The Plugin's scope is beautifully narrow:

> given what it is permitted to see, what changes to propose.

The refusal table is strong.

Treating delayed/scheduled effects as proposals rather than a Plugin-owned clock is also exactly the right direction.

### Main issues

Trust should follow role, not machine authorship.

Mechanical compatibility should be derived from declarations while domain fitness remains separate.

Reach/locality is a first-order product-definition decision and should enter the Decision Registry immediately.

The readability section should make explicit that the higher-level requirement is representation-independent while the current 3.x implementation may still deliberately choose readable Python as the canonical Plugin notation.

---

## `reactor.md`

### Strongest parts

This is probably the strongest single document of the five.

“Everything that actually happens” is a useful framing so long as it is read as execution authority, not semantic ownership.

The hostile-conditions paragraph should survive nearly unchanged into the final requirements. It protects the scientific contract from security-domain exceptionalism.

The future-relevant-state section is exactly the kind of subtle issue that would otherwise become a late bug with enormous evidentiary consequences.

### Main issues

The Reactor should not own interpretive stop labels, only stop facts.

The admission check should be explicitly authoritative here even if Generation performs an earlier check.

Budgets need to become a general capability/effect model.

“The Reactor is the only component that knows what happened” is rhetorically strong but should be phrased carefully in final requirements: after completion, the Run record also knows what happened because the Reactor captured it. The deeper point is that only the Reactor can determine execution facts at the moment they occur.

---

## `runs.md`

### Strongest parts

The Run as the meeting point of all identities is exactly right.

The immutability language is strong and appropriately absolute.

The playback consequence is also important: finished-history navigation is not merely a UI convenience; it enables future Readers and repeatable inspection.

The fact-versus-name correction for stopping should become a platform-wide principle.

### Main issues

Comparability belongs primarily to Study.

The replay decision should be split into exact replay and contract reproduction.

Steps-to-outcome should be retained but not described as computational hardness.

Clarify whether admission failures are Runs or a broader Attempt record.

The Run should store the frozen Run Contract rather than infer old permissions from component versions.

---

# 25. What I would not change yet

Because these are first-pass seam documents, several tempting rewrites should wait.

I would **not** yet choose exact Cell limits, design the relational storage schema, decide the full Reader catalog, define every temporal model, select GPU versus CPU backends, specify the final Python Plugin API, write every failure enum, decide how 3-D visualization consumes Run history, optimize for SaaS deployment, or fully specify Labs.

The current set is doing ontology and contract work.

Let it finish that job before implementation detail starts pulling the architecture toward whatever is easiest to code first.

---

# 26. Suggested next-pass deliverable

Before expanding these five into deep requirements, I would add one short cross-cutting document:

## `run-contract.md` or equivalent

It should answer only:

1. What does a World offer?
2. What does a Plugin request?
3. What does the Reactor offer?
4. Who performs the authoritative match?
5. What does a successful match produce?
6. What exactly is frozen for the Run?
7. What mismatch classes exist?
8. Which pieces define future-relevant state?
9. What gets recorded so later code never has to reconstruct the agreement from today's implementation?
10. Which parts are semantic facts versus implementation details?

Then return to the five component documents.

If that document is coherent, most of the shared seam sections should shrink naturally rather than multiply.

---

# 27. Questions for Claude, Gemini, or another reviewer

Do not ask merely whether the architecture “makes sense.” Ask them to attack it.

1. Find any state that can influence future execution but is not clearly owned or recorded.
2. Find any decision the Reactor could make that would silently become part of the mechanism.
3. Find any place a relational World is being forced into a grid-shaped assumption.
4. Find any result currently described as a fact that is actually an interpretation.
5. Find any semantic/domain decision that has leaked into the core platform instead of a Lab.
6. Find any mechanical compatibility test that is being confused with scientific/domain fitness.
7. Find any way a Plugin could gain hidden state that stopping/replay does not capture.
8. Find any Study pattern that cannot state exactly what is held constant and what is varied.
9. Find any failure category that would be lost because execution never began.
10. Find any place manual Plugin editing breaks semantic provenance.
11. Find any World capability that requires nondeterminism or unreplayable behavior.
12. Find any composition rule that is really an undeclared mechanism.
13. Find any reason exact replay and contract reproduction cannot coexist as separate promises.
14. Find any reason the Run Contract should be a full component rather than an immutable artifact assembled by the Reactor.
15. Find the strongest argument that SCR has generalized “local” so far that it is no longer meaningfully a local-mechanism system.

---

# Final assessment

The five documents hang together unusually well for a first requirements pass.

Their biggest success is not that they answer the hard questions. It is that they repeatedly locate the same hard questions from different component boundaries.

That is exactly what this pass should do.

The main architectural move I recommend is to make the declaration chain explicit as a frozen **Run Contract** or equivalent, with the Reactor performing the authoritative admission match and the Run retaining the result forever.

Around that, the next most important clarifications are:

- separate exact replay from contract reproduction;
- make Study responsible for question-specific comparability;
- strongly consider separating World from realized Starting State;
- distinguish external time-varying inputs from reactive mechanisms;
- allow multiple bounded Cell schemas if relational Worlds are truly first-class;
- define locality as permitted interaction rather than only geometric distance;
- formalize World State, Seen State, and Recorded State;
- derive future-relevant state from the frozen execution contract;
- keep Reactor facts separate from Reader conclusions;
- treat Plugins as untrusted experimental code regardless of who wrote them.

None of those observations require the starter docs to become large today.

They tell us what the detailed pass must eventually make impossible to misunderstand.

That is a very good place for a new repository to be.
