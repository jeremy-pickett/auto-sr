# Family F — Movement and crowds
## Lab Knowledge Report v1

### Crowd Egress · Highway Traffic · Pedestrian Flow · Warehouse Robot · Degraded-Information Evacuation

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/f-movement-and-crowds/family-f-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family F (entries 36–40)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md`
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 36–40 in `../short-lab-definitions/`
**Responds to:** `../../critiques/SCR_Labs_31-40_Critique_v0.1.md`
**Cites:** SCR-F v0.2 §11, §15, §18.5, §29, §30, §41–43; F-7, F-9, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-3, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

> ## Life-safety scope statement
>
> Two entries here concern emergency evacuation, and egress modelling is **operationally used** in building design — which makes SCR look adjacent to legitimate practice in a way it is not.
>
> **Nothing in this family assesses any real venue or building, evaluates any evacuation plan, or informs design, code compliance, or any life-safety decision.** Where a Lab's abstraction is weakest is precisely where the consequences are worst, and each entry below therefore declares a **supported regime** and a **boundary regime** rather than a single scope.

---

## What this family is for

Family F answers a question the earlier families kept circling: **what happens when the important state belongs to the participants rather than the places?**

Three findings, all platform findings.

### 1. World fit and mechanism fit are independent

Entry 39 is the cleanest demonstration in the catalog. A warehouse floor is almost comically perfect for SCR — discrete grid, discrete occupancy, discrete time, bounded state, deterministic movement — and the controlling mechanism is a **global central planner.** Perfect geometry, poor mechanism premise.

Entry 31 in Family E proved the opposite danger: a lattice can look natural while the physics ignores local adjacency.

Lab fit therefore needs independent axes, and every entry below reports all four:

- **World fit** — does SCR represent the environment honestly?
- **Mechanism fit** — does the behaviour arise from the kind of local rules SCR investigates?
- **Evidence fit** — can the result be checked?
- **Question fit** — is the user asking something SCR can genuinely add to?

### 2. Mechanism discovery and mechanism analysis are different modes

If the mechanism is software somebody wrote, why infer it? The answer is that you should not — **but the many-agent consequences of a known algorithm may still require simulation to establish.** Emergent behaviour of a known distributed or centralized rule is often not inferable from source code.

> **Do not require every Lab to justify itself as a mechanism-inference problem. Allow Labs whose value is systematic Study of known, readable Plugins.**

That broadens SCR without confusing the use case, and it applies directly to much of Family H.

### 3. The Mover: some state belongs to the participant, not the place

Across all five entries, location state and participant state are consistently different — a floor cell versus a pedestrian, a road cell versus a vehicle, a floor cell versus a robot with a task and a battery, a floor cell versus an evacuee's beliefs. Destination, speed, group membership, and belief **move with the participant** and a fixed cell is not their natural owner.

Before reaching for a full Agent ontology, a narrower construct may suffice:

> **Mover** — a bounded state-bearing participant occupying a World location and changing location through Reactor-controlled transitions.

The name matters less than the architectural point. This may be a World capability rather than a new top-level component, but the distinction is now hard to avoid, and it is a DEC-24 expenditure that should be made deliberately.

### 4. Belief versus world is execution semantics, not a UI feature

Entry 40 makes this the phenomenon rather than an edge case. The load-bearing state is not *the north exit is blocked* but *this participant believes the north exit is open, based on information received four steps ago.* Four distinct states:

| State | Meaning |
| :--- | :--- |
| **World truth** | What is actually true |
| **Participant belief** | What this participant currently believes |
| **Observation channel** | What information they can receive |
| **Recorded evidence** | What the Reactor knows happened |

This generalizes directly to attacker knowledge, defender visibility, stale identity state, distributed caches, routing tables, delayed telemetry, and agent memories. **Belief and seen-state should probably become a core World capability rather than a Lab-specific convention** — and entry 40 is the strongest reason to build it *before* Family H, not after.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 36 — Crowd Egress

| | |
| :--- | :--- |
| **Role** | Calibration Lab — **with aggressive scope boundaries** |
| **Standing** | [strong], inherited; not re-derived |
| **Falsifiable question** | Which local avoidance and route-choice rules make an obstacle placed before an exit increase flow rather than reduce it? |
| **World fit** | Excellent — physically motivated ~40 cm cell |
| **Mechanism fit** | **Good in the supported regime, failing in the dangerous one** |
| **Evidence fit** | **Excellent** — controlled human experiments with instrumented corridors |
| **Question fit** | Real, and hazardous |
| **Visual credibility** | **Class 1 — the highest in the catalog outside Family H** |

**The phenomenon.** People leaving through a door form an **arch** — a load-bearing structure of bodies around the opening, through which flow is intermittent rather than steady. At higher density, **faster is slower**: harder effort produces more jamming and longer total evacuation. Above a further threshold the crowd stops behaving like a flowing medium and develops involuntary shockwaves, and that is the regime in which crowd disasters kill — by compressive asphyxia rather than trampling.

**The established shortcut, and it is what codes are built on.** The pedestrian fundamental diagram and tabulated specific flow rates through doors — persons per metre of width per second — with Fruin's level-of-service classification as the practical vocabulary [11]. Total evacuation time from population and total exit width follows arithmetically, and **that is what egress engineering computes, adequately, for compliance.**

**The two model traditions.** The social force model (Helbing and Molnár, 1995) treats pedestrians as particles with goal attraction and mutual repulsion [11]. **Burstedde, Klauck, Schadschneider and Zittartz (2001)** gave the floor field CA: a maximum-speed-one model with exclusion and parallel dynamics, in which long-range interaction is mediated by a **floor field** subject to diffusion and decay and modified by pedestrian motion — an idea like chemotaxis, with people following a virtual rather than chemical trace. They showed the field alone suffices to produce collective self-organization including lane formation in counterflow [1].

**Helbing, Farkas and Vicsek (2000)** predicted the faster-is-slower effect and the value of a mixture of individualistic and herding behaviour [2].

**Correction from the first pass.** Faster-is-slower is **more nuanced and context-dependent than a universal law** — the literature contains conditions where the effect weakens or reverses, and a 2023 reappraisal of the original paper exists specifically to survey what has been learned since [2]. The deep paper needs careful referencing rather than a slogan.

**The scope split, and it is not optional.**

| Regime | Content | Status |
| :--- | :--- | :--- |
| **Supported** | Route choice, arching, intermittent flow, moderate congestion | The Lab's actual subject |
| **Boundary / unsupported** | Dense crowd turbulence, compressive-force safety prediction | **Outside the abstraction** |

At high density, body-force chains and contact mechanics dominate. A floor-field CA may produce jamming without reproducing compressive mechanics at all — **the strongest product claim lands exactly where the abstraction is weakest**, which is the same non-locality that sinks entry 31.

**Irreducible, within the supported regime.** Arch formation and intermittency, where flow is bursts and blockages with a heavy-tailed burst distribution and the tail is what matters. The geometry interaction — the repeatedly-reproduced result that **an obstacle before an exit can increase flow** by breaking up the arch is exactly this: non-obvious, geometric, and invisible to a rate calculation. Route choice under partial information, where people use the exit they came in by.

**Panic is largely a myth** in the crowd-science literature: real crowds are more cooperative and slower than models assume. A Lab generating "panic" mechanisms would be modelling folklore.

**Cell state.** *Location:* occupancy, floor field values (static distance-to-exit, dynamic traffic trace). *Mover:* desired direction, group membership, patience.

**Assessment.** *(judgment, no standing)* **Strong Lab, but not a safe flagship without aggressive scope boundaries.** The obstacle result is the perfect illustration of what SCR is for — a counterintuitive, geometry-dependent, mechanism-level finding a flow calculation cannot produce. The negative space matters too: venue designers make irreversible physical decisions, and no literature publishes layouts that failed.

---

## Lab 37 — Highway Traffic

| | |
| :--- | :--- |
| **Role** | **Top-tier calibration and flagship candidate.** Possibly the best public demonstration Lab in the catalog. |
| **Standing** | Ungraded; I would grade it **strong** |
| **Falsifiable question** | Which local driver-behaviour rules reproduce the observed hysteresis loop in the flow–density plane, and which produce only the mean fundamental diagram? |
| **World fit** | Excellent — cell size derived from vehicle spacing |
| **Mechanism fit** | Excellent — **the cleanest bounded-reach test in the catalog** |
| **Evidence fit** | **Exceptional** — continuous public loop-detector data, decades, thousands of sites |
| **Question fit** | Real, with a live controversy |
| **Visual credibility** | Class 1 for infrastructure claims; low otherwise |

**The phenomenon.** A jam appears with no accident and no bottleneck, travels backward against the flow at a consistent speed, and persists for hours while drivers passing through find nothing to explain it. The mechanism is delay: a driver reacts to the car ahead after a lag and brakes slightly harder than necessary; the driver behind does the same, amplified. Above a critical density the amplification wins.

**Two successful traditions coexist, and that is this Lab's greatest asset.** The Lighthill–Whitham–Richards kinematic wave model (1955) treats traffic as a compressible fluid and gives shock speeds — including backward jam propagation — in closed form from the fundamental diagram [11]. **Nagel and Schreckenberg (1992)** gave a stochastic discrete automaton whose Monte Carlo simulations show a transition from laminar flow to start-stop waves with increasing density, as observed in real traffic [3]. The randomization step is essential — without it there is no spontaneous jam.

Neither subsumes the other. **LWR gives shock speeds; Nagel–Schreckenberg gives spontaneous nucleation and metastability.** That gives SCR a ready-made epistemic discipline: use continuum theory where it works, use local discrete mechanism models where emergence and nucleation matter. **The rest of the catalog would benefit from imitating this.**

**Correction from the first pass.** The first pass implied Nagel–Schreckenberg reproduces real jam speed generically from four rules. The deep paper must separate **qualitative spontaneous jam reproduction** from **quantitative empirical fit**, which involves calibration and model variants.

**Reducible.** Jam propagation speed from the fundamental diagram. Road capacity. Queue lengths from deterministic queueing. Travel time under steady conditions. **Most operational traffic engineering runs on these, successfully.**

**Irreducible.** Nucleation — whether a jam forms at all from a given density and fluctuation. **Metastability and hysteresis**, where traffic sustains higher flow accelerating into a density than recovering from a jam, so the state depends on history rather than density alone — which a single-valued fundamental diagram cannot express. Lane changing, a discrete interaction-driven jam trigger. Heterogeneity of vehicles and drivers.

**On the three-phase controversy.** Kerner's argument that a distinct "synchronized flow" phase sits between free flow and jams is **a genuine, unresolved controversy** — and it needs neutral treatment. It is not automatically evidence that mechanism generation will resolve it, and a Lab that positions itself as settling the question is overreaching.

**Reach.** Vehicles move multiple cells per step, so interaction reaches ahead by the current speed — a **bounded, declared, finite reach**, and a cleaner instance of the DEC-21 question than the fat-tailed kernels in Family C.

**Cell state.** *Location:* occupancy. *Mover:* speed, and optionally driver type. Nagel–Schreckenberg uses ~7.5 m cells and integer speeds to five.

**Assessment.** *(judgment, no standing)* **Top-tier calibration and flagship candidate.** Loop-detector data means an emergent quantity from a Run — jam propagation speed, jam duration distribution, the hysteresis loop — can be compared against a measurement from a real motorway on a real Tuesday. And the phenomenon is intuitive, measurable, and comparatively low-risk: **for demonstrating the platform to someone who does not know cellular automata, this does more work than any other Lab**, because everyone has sat in a phantom jam. Rediscovery risk is high — Nagel–Schreckenberg is thirty years old and famous — which is precisely why blinded benchmarking (Family E §4) applies here too.

---

## Lab 38 — Pedestrian Flow

| | |
| :--- | :--- |
| **Role** | **Better early public crowd Lab than emergency egress** |
| **Standing** | Ungraded; I would grade it **plausible-to-strong** |
| **Falsifiable question** | Which local avoidance rules make counterflow deadlock likely in a given corridor geometry? |
| **World fit** | Excellent |
| **Mechanism fit** | **Good throughout the regime of interest** — unlike entry 36 |
| **Evidence fit** | Strong — controlled corridor experiments |
| **Question fit** | Design, not crisis |
| **Visual credibility** | Class 2 |

**The phenomenon.** Two streams walking in opposite directions separate into **lanes** — bands moving the same way, forming spontaneously, persisting, and reforming after disruption. Nobody organizes it: avoiding someone coming at you is easier if you step behind someone already going your way. At crossings the streams form diagonal stripes; at bottlenecks flow oscillates as one direction dominates then reverses; at corners people cut the inside, creating a density peak that reduces effective width.

**The distinguishing feature is that nothing has gone wrong.** Nobody is escaping, density is ordinary, and the variable of interest is **the layout**.

**The established shortcut.** The same two traditions as entry 36, with lane formation as their headline result — the floor field model was introduced specifically to show that the field alone suffices to produce it [1]. The fundamental diagram is again the reducible core, with an important wrinkle: it **differs measurably between cultures and between uni- and bidirectional flow**, and discrepancies between published diagrams are a known issue. There is no single universal curve.

**Irreducible.** Lane number and stability — a pattern-selection question of the same class as stripe selection in entry 20, and not given by linear reasoning. **Counterflow deadlock**, where two dense opposing streams in a narrow passage lock because moving requires someone else to move first. Bottleneck oscillation with a period and amplitude that reduce throughput below nominal capacity. Corner and obstacle effects. Group behaviour — people walk in twos and threes and refuse to separate.

**Why this is the better early Lab.** Entry 36 is a **life-safety** Lab with a severe misuse hazard whose dangerous regime the abstraction handles badly. This is a **design** Lab with a mild hazard whose regime the abstraction handles well throughout. **The contact-mechanics regime that breaks entry 36 does not arise at ordinary walking densities.** The modelling machinery is shared, so building this first costs little and risks much less.

**On merging with entry 36.** The overlap is substantial enough that these could be two profiles under one broader Crowd Movement Lab. **The reason to keep them separate is epistemic** — ordinary flow and design versus emergency egress and life safety have different validation standards and different product-risk rules — and that separation is worth preserving.

**Lattice anisotropy is especially serious here.** Lane direction *is* the phenomenon, and lanes forming along lattice axes may be artifacts. **An orientation-control Study is mandatory**: a diagonal corridor is not equivalent to an axis-aligned one on a square grid.

**Cell state.** *Location:* occupancy, floor field. *Mover:* desired direction, current heading, group identifier.

**Assessment.** *(judgment, no standing)* **Plausible-to-strong, and the better early public Lab.** Counterflow deadlock is a good target: a discrete identifiable failure event, geometry-dependent, reproducible in laboratory experiments, and exactly what a design review wants to know about a proposed layout. The cross-Lab link to symmetry-breaking pattern formation (entry 20) is also an interesting retrieval test between Labs that share nothing else.

---

## Lab 39 — Warehouse Robot

| | |
| :--- | :--- |
| **Role** | **Architecture and composition benchmark** — not a commercial flagship |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Under a known scheduling policy, at what fleet density does throughput collapse, and does inventory self-organization emerge as predicted? |
| **World fit** | **Excellent — not an abstraction at all.** The floor is literally a marked grid. |
| **Mechanism fit** | **Weak under centralized control** |
| **Evidence fit** | Excellent in principle; **commercially closed** in practice |
| **Question fit** | Narrow |
| **Visual credibility** | Class 3 |

**The phenomenon.** Hundreds of mobile robots drive beneath storage pods on a marked grid, in discrete steps, obeying a shared plan. Corridors saturate, robots queue at picking stations, and fleet throughput falls below what individual robots could achieve. Occasionally the system deadlocks. Separately and more quietly, the **layout of stored goods reorganizes** over time as pods return to different positions and popular items drift toward the stations.

**The established shortcut.** Multi-agent path finding is an active academic field with standard benchmarks: NP-hard to optimize in general, but conflict-based search and prioritized planning solve realistic instances well [11]. **Real systems are centrally scheduled** — a central planner assigns tasks and reserves paths, and deadlock is prevented by construction rather than resolved after the fact.

**Why the mechanism fit is weak.** With a central planner, the system's behaviour is *the plan's* behaviour. This is qualitatively different from every natural-science Lab: wildfire's mechanism is nature's and must be inferred; **this mechanism is a piece of software somebody wrote.**

**Correction from the first pass, and it matters.** "There is nothing to discover about a designed algorithm because its designers can inspect it" is too strong. **Emergent consequences of known distributed or centralized algorithms are often difficult to infer from source code.** The stronger distinction:

> **The mechanism does not need to be inferred, but its many-agent consequences may still require simulation.**

That defines a legitimate **mechanism-analysis Lab** — the second SCR mode — and it is the honest framing here.

**Irreducible.** Emergent congestion under a given policy, where a well-designed rule still produces interactions its designer did not enumerate. Deadlock in decentralized or degraded operation. **Layout self-organization** — the drift of popular inventory toward stations, driven by a simple local rule (return the pod to a nearby free slot) and *not designed*. Scaling behaviour, where the throughput-collapse threshold is not predictable from the policy alone.

The self-organization thread **may be more SCR-native than path planning**, and it is the one part of the domain nobody designed.

**The architectural value.** This is the catalog's cleanest test of whether SCR can express a system with both local mechanisms **and a global coordinator** — a combination that recurs in patch deployment, routing protocols, immune recruitment, and defender response throughout Family H. Because the coordinator is a known algorithm rather than an inferred one, it provides **unusually clean ground truth for testing composition or coordinator semantics.** A Lab where you already know the right answer is a good place to test whether the platform can express the question.

**Cell state.** *Location:* occupancy, pod present, reservation state, station designation. *Mover:* task, destination, battery.

**Assessment.** *(judgment, no standing)* **Keep as an architecture and composition benchmark, not a commercial flagship.** Operators have detailed simulators calibrated against real floor telemetry and use them for exactly these questions; throughput and layout data is a trade secret, so validation is largely unavailable outside them. The value is entirely to the platform — and the World fit being exact while the mechanism fit is weak is the lesson.

---

## Lab 40 — Degraded-Information Evacuation

| | |
| :--- | :--- |
| **Role** | **Architecturally exceptional; empirically weak.** The belief/seen-state forcing case. |
| **Standing** | Ungraded; I would grade it **plausible on interest, weak on validation** |
| **Falsifiable question** | Which signage and announcement strategies fail robustly across candidate belief-propagation and route-choice mechanisms? |
| **World fit** | Good |
| **Mechanism fit** | Good — **but requires belief/seen-state the platform does not have** |
| **Evidence fit** | **Severely weak** — the experiment is unethical and incidents are unrepeatable |
| **Question fit** | Real and underserved |
| **Visual credibility** | **Class 1**, worsened by the absence of calibration |

**The phenomenon.** Every evacuation model assumes people know where to go. Real evacuations frequently fail that assumption: signage obscured by smoke or by the crowd, an exit locked or opening onto a blocked stairwell discovered by the people at the front while those behind keep pushing, an announcement inaudible or arriving after people have committed, someone who knows the building leading a group the wrong way with complete confidence.

What people actually do is well documented and is not what models assume. They **leave the way they came in**, even when a nearer exit exists. They wait for confirmation before moving. They follow others. They stay with their group.

**So the variable that determines the outcome is not the building's geometry. It is what each person believes about the building, and when they came to believe it.**

**The established findings contradict the folk model.** Fire safety research has documented for decades that the dominant delay is **pre-movement time** — the interval between alarm and actually starting to move — driven by information seeking, ambiguity, and social confirmation rather than by panic [11]. Exit choice is dominated by familiarity over proximity.

**Correction from the first pass.** "Almost nothing that matters is reducible" is too absolute. Decision theory, network diffusion, queueing with information delay, and social-learning models cover pieces of this. The Lab does not need a claim of mathematical uniqueness. The stronger case:

> **The coupled feedback between movement, observation, belief, and route choice makes the full realization history-dependent and poorly captured by conventional egress summaries.**

**Irreducible.** Belief propagation coupled to movement — what a person knows depends on who they have been near, which depends on where they moved, which depends on what they knew. **Stale information**, where someone told five minutes ago acts on a fact no longer true. **Cascading commitment**, where a stream committing to a route is followed because it looks like knowledge, amplifying an early wrong choice. Discovery of blockage, where information must travel backward through a crowd moving forward — a race. Belief asymmetry across a population, where the aggregate depends on the distribution rather than any average.

**The §13.1 pressure, shared with entry 47.** An agent's belief about a building is naturally an unbounded structure. Bounded belief — a small set of "exit X open / blocked / unknown" flags with timestamps — is expressible and probably sufficient, but it is a substantive commitment and the fit review must decide whether the useful questions survive it. **This Lab and entry 47 share the ceiling problem and should be fit-reviewed together.**

**What the Lab may and may not claim.** Validation weakness is severe and will not improve — the experiment is ethically unavailable and each incident is a single point with no counterfactual. The value must therefore centre on **robustness, fragility discovery, mechanism comparison, and architecture validation** — explicitly **not** operational evacuation recommendations. A robustness finding survives weak calibration in a way a prediction does not.

**Cell state.** *Location:* occupancy, hazard state, signage. *Mover:* bounded belief set with timestamps, group membership, movement state, pre-movement timer. **The load-bearing state is all on the Mover.**

**Assessment.** *(judgment, no standing)* **High architecture value, weak empirical standing. Build if and when belief/seen-state becomes strategically important — and that is most likely to be *before* the security Labs, not after.** This Lab makes observation staleness, partial information, belief propagation, and social amplification the *core mechanism* rather than an edge case, on a domain where the mechanism is sympathetic and the stakes of getting the architecture wrong are pedagogical. That is a far better place to make the mistakes than in Family H, where they would be embarrassing and consequential.

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **The Mover** — bounded state-bearing participant occupying a location, moving under Reactor control | **DEC-24** | All five. Consider before reaching for a full Agent ontology. |
| **Belief and seen-state as a core World capability** — world truth / participant belief / observation channel / recorded evidence | *unregistered* — **strongest new candidate from this batch** | 40 primarily; generalizes to all of Family H |
| **World fit and mechanism fit as independent axes** | **DEC-15** via standing | 39 (perfect World, weak mechanism); 31 (natural-looking lattice, non-local physics) |
| **Mechanism discovery vs mechanism analysis as two modes** | *unregistered* | 39, and most of Family H |
| **Coordinator semantics** — local mechanisms plus a global planner | **DEC-1** | 39, with known ground truth |
| **Orientation-control Study** | *unregistered* | 38 — lane direction is the phenomenon and the grid has directions |
| **Bounded belief under the semantic ceiling** | **CELL ceiling** | 40, shared with 47 |

### Build priority within the family

**Build early.** **Highway Traffic (37)** — top calibration candidate, exceptional public data, and the best demonstration Lab in the catalog for a non-specialist audience. **Pedestrian Flow (38)** — the safer crowd Lab, good early public build.

**Strong, with boundaries.** **Crowd Egress (36)** — real value in the supported regime; must declare the unsupported one.

**Architecture value.** **Warehouse Robot (39)** — the World-fit/mechanism-fit separation, with clean ground truth. **Degraded-Information Evacuation (40)** — the belief/seen-state forcing case; build before Family H if that capability is wanted.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** Burstedde, C., Klauck, K., Schadschneider, A. & Zittartz, J. (2001). Simulation of pedestrian dynamics using a two-dimensional cellular automaton. *Physica A* **295**, 507–525. *(Floor field subject to diffusion and decay, modified by pedestrian motion — a virtual rather than chemical trace; sufficient alone to produce lane formation in counterflow.)*
2. **[V]** Helbing, D., Farkas, I. & Vicsek, T. (2000). Simulating dynamical features of escape panic. *Nature* **407**, 487–490. *(Faster-is-slower; optimal mixture of individualistic and herding behaviour.)* See also the 2023 reappraisal *Revisiting "Simulating dynamical features of escape panic": what have we learnt since then?*, arXiv:2310.20506 — **faster-is-slower is context-dependent, not a universal law.**
3. **[V]** Nagel, K. & Schreckenberg, M. (1992). A cellular automaton model for freeway traffic. *Journal de Physique I* **2**, 2221–2229. *(Stochastic discrete automaton; transition from laminar flow to start-stop waves with increasing density, as observed in real traffic.)*
4. **[D]** Helbing, D. & Molnár, P. (1995) — the social force model.
5. **[D]** Lighthill, M. J. & Whitham, G. B. (1955); Richards, P. I. (1956) — kinematic wave theory of traffic flow.
6. **[D]** Kerner, B. S. — three-phase traffic theory; a genuine and unresolved controversy.
7. **[D]** Helbing, D. et al. — analysis of crowd turbulence from video of the 2006 Hajj disaster.
8. **[D]** Fruin, J. J. (1971) — pedestrian level-of-service classification.
9. **[D]** Multi-agent path finding literature: conflict-based search, prioritized planning, and standard benchmarks; the Kiva/Amazon fulfilment architecture.
10. **[D]** Fire safety engineering on pre-movement time, information seeking, and exit choice by familiarity; the crowd-science position that panic is largely a myth.
11. **[D]** Specific flow rates through doors in egress codes; published pedestrian fundamental diagrams and their cross-cultural discrepancies; obstacle-before-exit flow-improvement experiments.

---

## Non-claims

This report performs no fit reviews and establishes no fit. **Nothing in this family assesses the safety of any real venue, building, road, or facility; evaluates any evacuation plan, signage, alarm, or emergency communication strategy; predicts congestion; or informs building design, code compliance, transport planning, infrastructure, or any life-safety decision** (§41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment, carry no standing, and do not promote any entry.
