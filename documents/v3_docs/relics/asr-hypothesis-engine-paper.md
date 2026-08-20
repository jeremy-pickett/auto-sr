# A Card Catalog for Emergence: Intent-Indexed Cellular Automata as a Mechanism-Hypothesis Engine

**Status:** position paper, v0.1 draft. Claims in §7 are stated so they can fail.
**Relationship to the build:** this is the long-horizon argument for decisions already
made in the visualization uplift (structure detection as comparable corpus data, not
run-view decoration). Nothing here changes the v3 requirements contract.

---

## Abstract

Practitioners who model emergent phenomena — fire fronts, crowd clogging, invasion
waves, pattern formation — face two distinct problems: hypothesizing a local mechanism
that could produce the observed behavior, and calibrating that mechanism against data.
The second problem is well served by mature, domain-specific tooling. The first is
served by intuition, literature search, and luck. We describe a system, Autonomous
Semantic Ruliology (ASR), that generates cellular-automaton rules from natural-language
behavioral intent, executes every rule to completion under a deterministic harness, and
permanently records intent, implementation, and measured outcome — including failures.
We argue that at sufficient scale this corpus becomes a queryable catalog of *mechanisms
indexed simultaneously by stated intent and by observed emergent behavior*, an artifact
that does not currently exist and that numeric rule enumeration cannot produce, because
a rule number carries no intent. The system makes no predictive claims about any
domain. Its proposed value is upstream of prediction: hypothesis supply. We survey
eighteen candidate application verticals with honest fit ratings, state the
prerequisites and falsifiable milestones the claim depends on, and give the strongest
critiques we can construct against our own position.

---

## 1. Introduction: the bottleneck is the guess

Every validated model of an emergent phenomenon began as a guess about mechanism.
Before Nagel and Schreckenberg calibrated anything, someone had to propose that
phantom traffic jams might fall out of four local rules about acceleration, braking,
randomization, and movement [1]. Before floor-field models predicted exit clogging,
someone had to guess that pedestrians might behave like particles following a
dynamically written pheromone field [2]. The calibration that followed was systematic.
The guess was not. It came from an individual's intuition about what local behavior
could possibly aggregate into the observed global pattern — and the space of candidate
local behaviors is enormous, unindexed, and mostly unexplored.

This is the gap the present paper addresses. Not "can cellular automata predict X" —
for most X the answer is no, and for the X where the answer is yes, calibrated
domain-specific models already exist and are better than anything a general system
will produce. The question is whether the *hypothesis-generation step* — the guess —
can be supported by a searchable corpus, the way a chemist's guess is supported by a
reaction database or a protein designer's guess is supported by a fold library.

Our claim: a large corpus of machine-invented cellular-automaton rules, where every
rule carries (a) a natural-language statement of behavioral intent, (b) a verified
implementation, (c) a complete, replayable execution history, and (d) mechanically
detected emergent structures, supports a query no existing resource supports:

> *"Show me every local mechanism, described in plain English, that produced
> [expanding fronts / persistent travelers / clogging arches / stable spots] —
> including the mechanisms whose authors intended something else entirely."*

A domain modeler takes the retrieved mechanisms as candidate hypotheses and performs
calibration in their own tooling. The corpus never predicts. It proposes.

---

## 2. Background

### 2.1 Cellular automata as scientific models: the precedent is real

The idea that trivially simple local rules produce operationally useful models is not
speculative. A partial inventory of CA models that crossed from curiosity into use:

- **Traffic.** The Nagel–Schreckenberg model (1992) reproduces spontaneous jam
  formation from local rules and descendants of it have been used in transport
  planning [1].
- **Pedestrian dynamics.** Floor-field CA models reproduce lane formation in
  counterflow and arch-shaped clogging at exits, and inform egress design [2].
- **Wildfire.** Lattice fire-spread models with fuel, slope, and wind as local state
  are used in coarse operational forecasting [3].
- **Urban growth.** SLEUTH, a CA calibrated on historical land-use maps, has been
  applied to dozens of metropolitan regions [4].
- **Cardiac tissue.** Greenberg–Hastings-style excitable-media CA reproduce the spiral
  waves implicated in arrhythmia and are used as cheap surrogates for PDE tissue
  models [5].
- **Biological pattern.** CA and closely related lattice models reproduce seashell
  pigmentation (famously Rule-30-like), animal coat patterns, mussel-bed banding, and
  semi-arid vegetation stripes [6].

Two things are true at once about this list. It proves the entry point is real:
low-order emergent phenomena genuinely yield to lattice models with a handful of local
states. And it proves the competition is real: every domain on the list has calibrated,
domain-specific models built by specialists with data. A general system does not beat
them at their own game, and this paper does not propose to.

### 2.2 What enumeration cannot produce

Wolfram's program — enumerate the rule space numerically, run everything, observe [7]
— is exhaustive within its frame and produced the field's central insight,
computational irreducibility: for many simple programs there is no shortcut to knowing
what they do except running them. But a rule number is semantically silent. Rule 30
carries no statement of what it was *for*, because it was not for anything; it is a
coordinate. Consequently an enumerated corpus can be indexed by outcome but never by
intent, and the query in §1 — which explicitly requests mechanisms whose *stated
purpose* diverged from their *observed behavior* — cannot be asked of it at all.

### 2.3 The ASR system, briefly

ASR is a working system (single-user, local, contract-complete requirements) in which
a language model invents a rule in two stages — a plain-English behavioral description,
then a Python implementation of that description — and a deterministic harness
validates, executes, measures, and permanently stores the result. Properties relevant
to this paper's argument, each load-bearing:

- **Intent is captured before implementation exists.** The Stage A description is the
  hypothesis in the model's own words, recorded verbatim, with the full rendered
  prompt context that produced it.
- **Failures are corpus.** Rules that fail validation, and rules that compile but
  produce nothing, are stored with equal permanence. A mechanism catalog that silently
  discarded the mechanisms that don't work would teach its users the same
  overconfidence it taught its generator.
- **Every run is exactly reproducible.** Deterministic step function, facaded
  randomness, engine-revision stamping. A retrieved mechanism can be re-executed
  bit-identically years later, which is what makes retrieval trustworthy.
- **Concept tagging against a fixed vocabulary** (`spreads`, `resists`, `copies`,
  `decays`, `counts`, `remembers`, `moves`, `competes`, ...) makes intent queryable
  without reprocessing free text under a drifted model.
- **Mechanical structure detection** (specified; in development) labels recurring
  spatial objects — stills, repeaters, travelers, and structures whose visible shape
  recurs while hidden properties drift — making *observed behavior* queryable at the
  same granularity as intent.

The last two items together are the index. Intent on one axis, detected structure on
the other. The corpus is the join.

---

## 3. The core claim

**Claim.** At sufficient scale, an intent-indexed, behavior-indexed corpus of executed
CA rules is a useful hypothesis-supply instrument for practitioners modeling low-order
emergent phenomena — where "useful" means it retrieves candidate mechanisms a
practitioner judges worth calibrating, at a higher rate than literature search or
unaided intuition, for at least some phenomena.

Three properties distinguish this from anything currently available:

**1. The intent–outcome gap is data, not noise.** When a rule described as "cells
copy their strongest neighbor" unexpectedly produces persistent traveling structures,
that mismatch is precisely what a hypothesis engine should surface: mechanisms that
produce a behavior *for reasons their description does not advertise* are the ones a
domain expert is least likely to guess unaided. Enumerated corpora cannot represent
this gap; curated model libraries suppress it, because published models are the ones
that did what their authors intended.

**2. Negative space is mapped.** The corpus records what was attempted and failed,
per region of the rule space (kinds × neighborhood × reach × shape × modifier). A
practitioner querying for "mechanisms producing stable spots" also learns which
mechanism families were tried eleven times and never produced them — which prunes
their own search. No literature does this, because literature does not publish the
eleven attempts.

**3. Retrieval is executable.** A retrieved hypothesis is not a citation; it is a
runnable, deterministic artifact with its complete behavioral history attached. The
practitioner's first calibration step — "does this mechanism family even produce the
qualitative behavior under perturbation of scale and seed" — can be answered before
any domain data is touched.

**Non-claim, stated as strongly as the claim.** Nothing retrieved from this corpus
predicts anything about any physical system. A mechanism producing lane formation on
a 200×200 torus shares a *qualitative behavior* with pedestrian counterflow; it shares
no calibrated relationship with any hallway on earth. The corpus proposes candidate
rule *forms*. Domain fit, parameter estimation, topology correction, and validation
are the practitioner's job, done in the practitioner's tools, against the
practitioner's data. Any future version of this system that blurs that line should be
considered to have failed in the way that matters most.

---

## 4. The low-end entry, taken seriously

The pattern this paper bets on is the standard disruption trajectory [8]: entrants
establish themselves in applications the incumbents consider beneath them — smaller,
cheaper, "worse" on the incumbent's metrics — and mature upward from a base the
incumbent never contests. Honda's entry into the American motorcycle market is the
canonical case: not head-to-head against large touring bikes, but the Super Cub, a
small cheap machine sold through sporting-goods stores to people who were not
motorcycle customers at all. The incumbents' metrics said it wasn't competition. It
was a new market that grew until it wasn't.

The mapping here is specific, not decorative. The incumbents are calibrated
domain-specific modeling stacks — computational fluid dynamics, agent-based simulation
suites, PDE solvers — and on their own metric, predictive accuracy in-domain, this
system will never compete and never tries. The under-served market is the step those
stacks all assume has already happened: someone arrived carrying a mechanism worth
calibrating. The customers are practitioners at the guessing stage — a fire ecologist
wondering what local rule structure could produce the spotting pattern in their data, a
venue designer wondering what family of local behaviors produces arch clogging, a
graduate student who needs six candidate mechanisms by Friday. "Worse but accessible"
is the whole pitch: a query against a corpus is cheaper than a literature review and
enormously cheaper than a simulation campaign, and it does not need to be right — it
needs to make the practitioner's next week more productive than their current tools do.

The discipline the analogy imposes: do not move upmarket early. The failure mode is
announcing prediction before hypothesis supply is proven — claiming the Gold Wing
while shipping the Super Cub. §7 defines what "proven" means.

---

## 5. Candidate verticals

Eighteen candidates, rated for lattice fit (does the phenomenon live naturally on a
grid with local state), precedent (does CA modeling of it already exist), and honest
standing. Ratings: **strong** (pursue), **plausible** (pursue with stated caveats),
**weak** (qualitative insight only), **insane** (listed to mark the boundary).

| # | Vertical | Phenomenon of interest | Fit | Precedent | Standing |
|---|---|---|---|---|---|
| 1 | Wildfire | Front propagation, spotting, burnout | Excellent | Operational [3] | **Strong** |
| 2 | Crowd egress | Clogging arches, lane formation, density waves | Good | Operational [2] | **Strong** |
| 3 | Invasion ecology | Colonization fronts, patchy establishment | Good | Established | **Strong** |
| 4 | Urban growth | Edge growth, leapfrog sprawl, corridor spread | Good | Operational [4] | **Strong** |
| 5 | Excitable media | Spiral waves, wave break, re-entry | Excellent | Established [5] | **Strong** |
| 6 | Biological pattern formation | Spots, stripes, banding, shell pigmentation | Excellent | Established [6] | **Strong** |
| 7 | Corrosion / material fronts | Pitting, front roughening, percolation | Good | Literature-stage | **Plausible** — real precedent, but predictive versions need electrochemical state that strains the simplicity premise |
| 8 | Sand ripples / dunes | Ripple spacing, dune migration | Good | Established (Werner-class models) | **Plausible** |
| 9 | Snow/crystal growth | Dendrite morphology | Excellent | Established (Gravner–Griffeath) | **Plausible** — gorgeous fit, tiny audience |
| 10 | Tumor growth (avascular) | Margin morphology, necrotic core formation | Moderate | Large literature | **Plausible** — lattice artifacts are a known, managed problem in the field |
| 11 | Biofilm / colony morphology | Branching, fronting, sectoring | Good | Established | **Plausible** |
| 12 | Sea-ice melt ponds | Pond geometry, percolation transition | Good | Literature-stage | **Plausible** |
| 13 | Warehouse robot traffic | Deadlock, corridor congestion | Moderate | Adjacent (traffic CA) | **Plausible** — discrete space is literally true here, but real fleets are centrally scheduled, which is exactly what CA lacks |
| 14 | Epidemic spread | Wave speed, cluster sizes | Moderate | Large literature | **Weak** — contact networks are not lattices; wrong topology gives wrong wave speeds. Qualitative only, and say so |
| 15 | Opinion / adoption dynamics | Consensus domains, stable minorities | Moderate | Established (voter models) | **Weak** — same topology objection as 14 |
| 16 | Ant trails / stigmergy | Trail formation and decay | Moderate | Established | **Weak** in pure-CA form — it is an agent-plus-field system, and flattening the agents into cell state contorts the mechanism |
| 17 | Retail foot-traffic layout | Dwell clustering, choke points | Poor | Thin | **Weak→insane** — the interesting behavior is goal-directed and global |
| 18 | Parking-lot dynamics | Occupancy waves | Poor | None serious | **Insane** — decisions depend on global information (entrance location, visible vacancy); a CA of it is a diorama. Retained as the boundary marker |

Two observations about the table's shape. The strong rows are strong precisely
*because* incumbent models exist there — precedent is what certifies the phenomenon as
lattice-native, and the incumbents are calibrators, which is the customer this system
serves rather than the competitor it fights. And the weak rows share one diagnosis:
the substrate is a network or an agent population wearing a grid costume. That
suggests a falsifiable selection rule — **this approach serves phenomena whose spatial
adjacency is physically real, and degrades in proportion to how much the true
interaction topology departs from the lattice** — which is itself a testable claim,
and better than a vibe.

---

## 6. What a query actually looks like

Concreteness check, because "queryable corpus" is easy to say. A fire ecologist's
session:

1. **Behavioral query.** "Structures: expanding fronts. Front roughness: high.
   Extinction: spontaneous, patchy." Executed against detected-structure rows and
   per-run measurement series — not against descriptions.
2. **Result set.** Forty-one rules whose canonical runs contain matching structures.
   Each row: the Stage A description, concept tags, the structure census, a preview
   image, links to source and full replay.
3. **The interesting cut.** Sort by intent–outcome divergence. Top of the list:
   a rule described as "cells resist change in proportion to how long they have held
   their kind" — nothing about fire, spread, or fronts in its stated intent — that
   produced rough, patchily extinguishing fronts. This is the retrieval a literature
   search structurally cannot perform, because no paper's abstract describes a
   mechanism by what it failed to intend.
4. **Executable follow-up.** Re-run the retrieved rule at three seeds. Front roughness
   persists across seeds; patchy extinction does not. The ecologist discards the
   extinction hypothesis and takes the roughness mechanism — persistence-weighted
   resistance — into their own calibrated tooling as a candidate term.

Total cost to the corpus: three replays. Total claim made by the corpus: zero. The
mechanism may calibrate into nothing; the session was still cheaper than the
alternative ways of arriving at the same candidate.

---

## 7. What must be true, stated so it can fail

The claim in §3 rests on prerequisites, none currently satisfied. In dependency order:

**P1 — Scale.** The corpus must be large enough that behavioral queries return
non-trivial result sets across the coverage map. The system's own requirements gate
corpus-level features at roughly 300 rules; the hypothesis-supply claim plausibly needs
an order of magnitude more. *Current status: the corpus is seed fixtures plus early
generations. Nothing in this paper is testable today, and pretending otherwise would
be the first failure.*

**P2 — Structure detection at corpus grain.** Detected structures must be comparable
across runs — deterministic detection, versioned detector, stable signatures — or the
behavioral axis of the index is mush. *Status: specified to contract depth in the
current uplift; the design choice this paper depends on (detector rows as queryable
corpus data, not view decoration) is already made.*

**P3 — Behavioral vocabulary beyond structures.** Fronts, roughness, extinction
patchiness, domain coarsening — the query in §6 needs measured series and derived
descriptors, not just the structure census. *Status: partially available
(per-tick variety, change, quiet-streak series); mostly future work.*

**P4 — Diversity under a fixed generator.** If the generator's priors collapse the
corpus into a few mechanism families, retrieval returns the same five ideas in
different words. The coverage map exists to fight this; whether it fights hard enough
at scale is an open empirical question, and the attempts/rejections accounting is the
instrument for answering it.

**Falsifiable milestones.**

- **M1.** At ~3,000 rules, behavioral queries for five qualitatively distinct targets
  (fronts, travelers, spots, spirals, clogging) each return ≥ 20 mechanistically
  distinct rules. *Failure: the generator is not diverse enough, and P4 is the
  bottleneck.*
- **M2.** Blinded practitioner test: domain modelers given retrieval sessions rate
  ≥ 10% of retrieved mechanisms "worth a calibration attempt." *Failure: the corpus is
  a museum, not an instrument.*
- **M3.** Intent–outcome divergence is informative: divergent retrievals are rated
  worth-calibrating at a rate ≥ non-divergent ones. *Failure: the "semantic" in the
  system's name is ergonomics only — which would not kill the catalog, but would kill
  this paper's central distinction, and the abstract would need rewriting.*
- **M4.** One retrieved mechanism, in any vertical, survives independent calibration
  into a domain model that a practitioner keeps. One. *This is the Super Cub
  milestone, and no upmarket claim is made before it.*

---

## 8. Threats to validity — the strongest critiques we can construct

**T1 — The abstraction-boundary objection.** All eighteen verticals share one CA
formalism, so the corpus's mechanisms may cluster at a level of abstraction too generic
to help any single domain: "cells resist change proportional to age" is retrievable,
but the ecologist needed "fuel moisture memory," and the translation gap between them
may be exactly where the hard intellectual work lives — in which case the catalog
saves practitioners nothing. This is the most serious threat, it is what M2 measures,
and there is no argument against it. Only the experiment.

**T2 — The generator-prior objection.** An LLM's priors about "interesting rules" are
trained on the same literature the practitioner already read. The corpus may be a
noisy mirror of known mechanism space rather than a search of it, differing from a
textbook mainly in confidence. The intent–outcome gap (§3.1) is the counterargument —
surprise is generated by execution, not by the model — but whether surprises are
*useful* surprises is M3's question, not a foregone conclusion.

**T3 — The topology objection, generalized.** §5 flags networks-in-grid-costume per
vertical, but the deeper version cuts wider: even lattice-native phenomena have
continuous fields, long-range coupling, or global constraints that a strictly local,
discrete formalism cannot express, and mechanisms that depend on what the formalism
*can't* say will never appear in the corpus at any scale. The catalog's negative space
(§3.2) is then partly an artifact of the formalism, not a map of mechanism space — and
a practitioner who reads "tried eleven times, never worked" as evidence about the
world rather than about the lattice has been actively misled. Mitigation: the corpus
must label its own expressiveness boundary as loudly as its coverage.

**T4 — The two-audiences objection.** The system was designed as an open-ended
exploration instrument; this paper retasks it as a retrieval instrument, and the two
pull on the generator differently. Exploration wants the coverage map to push toward
the untried; retrieval wants density around behaviorally rich regions. Serving
retrieval by steering generation would violate the system's own firewall between
observation and generation context — the same firewall that keeps user flags out of
Stage A — so retrieval must take the corpus as exploration leaves it. If exploration's
distribution is retrieval-poor, that is a finding, not a knob to turn.

**T5 — The "so what" objection, kept deliberately.** Perhaps hypothesis generation was
never the bottleneck; perhaps domain experts are already excellent guessers and the
scarce resource is calibration labor and data, in which case this entire instrument
optimizes the cheap step. The honest response: the premise that guessing is hard is
itself an empirical claim about modeling practice, M2 is its test, and the system's
primary purpose — the exploration corpus — survives even if this paper's thesis does
not. The paper is a bet placed on top of the system, not the system's justification.

---

## 9. Related work

Numeric enumeration of rule spaces [7] produces outcome-indexed corpora with no intent
axis (§2.2). Domain-specific CA models [1–6] are calibrated single points, published
without their failed siblings. Program-synthesis and genetic-programming searches for
CA rules with target behaviors (e.g., evolved density-classification rules) optimize
toward a specified outcome and discard the trajectory; this corpus's value is the
trajectory, failures included. Model repositories in systems biology and agent-based
modeling (BioModels, CoMSES) index *validated, human-authored* models by domain
metadata — the opposite selection rule from ours, which indexes unvalidated,
machine-authored mechanisms by behavior. To our knowledge no existing corpus indexes
executable mechanisms simultaneously by natural-language intent and by mechanically
detected emergent behavior, with the intent–outcome divergence preserved as a query
axis. That absence is either an opportunity or a verdict; §7 is designed to find out
which.

---

## 10. Roadmap

Deliberately short, because most of it is "run the existing system for a long time."

1. **Now:** structure detection lands per the current uplift, with detector rows
   stored as versioned, deterministic, corpus-comparable data (P2). This is already
   the plan and needs no new decisions.
2. **Corpus accumulation** to the 300-rule gate, then onward. No retrieval features
   before there is something to retrieve.
3. **Behavioral descriptor layer** (P3): derived per-run descriptors beyond the
   structure census. Specified as a v4 omnibus section when the time comes, not
   bolted on.
4. **M1 diversity audit** at ~3,000 rules, using the coverage map's
   attempts/rejections accounting.
5. **M2/M3 practitioner study.** Small, blinded, honest. Published either way.
6. **Upmarket claims: none** until M4.

---

## References

[1] Nagel, K., Schreckenberg, M. (1992). A cellular automaton model for freeway
traffic. *Journal de Physique I*, 2(12).
[2] Burstedde, C., Klauck, K., Schadschneider, A., Zittartz, J. (2001). Simulation of
pedestrian dynamics using a two-dimensional cellular automaton. *Physica A*, 295.
[3] Sullivan, A. (2009). Wildland surface fire spread modelling, 1990–2007. Part 3:
simulation and mathematical analogue models. *International Journal of Wildland
Fire*, 18.
[4] Clarke, K., Hoppen, S., Gaydos, L. (1997). A self-modifying cellular automaton
model of historical urbanization in the San Francisco Bay area. *Environment and
Planning B*, 24.
[5] Greenberg, J., Hastings, S. (1978). Spatial patterns for discrete models of
diffusion in excitable media. *SIAM Journal on Applied Mathematics*, 34.
[6] Meinhardt, H. (1995). *The Algorithmic Beauty of Sea Shells.* Springer.
[7] Wolfram, S. (2002). *A New Kind of Science.* Wolfram Media.
[8] Christensen, C. (1997). *The Innovator's Dilemma.* Harvard Business School Press.

---

*Draft prepared against the ASR v3 requirements and the frontend visualization uplift
2.2. The system described makes no predictive claims; see §3, non-claim, which the
authors consider the most important paragraph in the paper.*
