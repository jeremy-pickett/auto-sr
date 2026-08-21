# Family G — Cities and infrastructure
## Lab Knowledge Report v1

### Urban Growth · Power Grid Cascade · Water Distribution · Freight and Rail Congestion · Service Cascade · Routing Instability

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/g-cities-and-infrastructure/family-g-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family G (entries 41–46)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md`
**Responds to:** `../../critiques/SCR_Labs_41-50_Critique_v0.1.md`
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 41–46 in `../short-lab-definitions/`
**Cites:** SCR-F v0.2 §11, §15, §18.5, §29, §30, §41–43; F-7, F-9, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-3, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

## Revision record — v1 first draft → v1 reviewed

The first draft of this report was written before `SCR_Labs_41-50_Critique_v0.1.md` existed, and said so. The critique arrived afterward and this revision incorporates it. Recorded rather than silently applied.

| Change | Nature |
| :--- | :--- |
| **The Network World fit test is two questions, not one** (§What this family is for) | The batch's central lesson. *Is the graph real?* and *does each transition depend on bounded relational information?* are independent, and this family answers them differently in different entries. |
| **Water Distribution's rejection reason sharpened** (43) | The first draft grouped it loosely with entry 42. It fails for a **different** reason than Fracture, and the distinction is cleaner: not that the physics is non-local, but that **"needs computation" is not the same as "needs SCR."** |
| **Power Grid reclassified from weak to dangerous** (42) | The first draft called it weak. The critique is right that it is worse: an abstract cascade model produces convincing shapes, heavy-tailed distributions, and apparently scientific conclusions **while representing the wrong causal system.** A visualization policy is now attached. |
| **Service Cascade promoted to flagship** (45) | The first draft called it the strongest ungraded entry. The critique goes further and I have adopted it: a plausible **near-term commercial** Lab, and possibly better than the security-branded ones. |
| **Routing named as an acceptance-test Lab** (46) | Not merely blocked on DEC-3 — the cleanest acceptance case *for* it. |
| **DEC-3 given an execution vocabulary** (§findings) | Step / delayed effect / message / scheduled event / phase. **Do not resolve DEC-3 with a boolean such as "supports async."** |
| **Urban Growth reframed as a benchmark** (41) | Against a mature operational CA tradition, not as a new methodology. Its open questions are now stated as benchmark questions. |
| **Multiple Connection classes per World** (41, §findings) | Urban Growth needs spatial adjacency *and* road connectivity *and* jurisdiction membership. The answer is not a HybridWorld abstraction but **a World declaring more than one Connection class**, with a Plugin declaring which it reads. |
| **Connection state as first-class and bounded** (§findings) | Direction, type, latency, capacity, visibility, state — under the same readable, bounded, declared discipline as Cell state. |

---

## What this family is for

Family G is where the **globally-computed-driver boundary** — established decisively by Fracture in Family E — meets its largest concentration of test cases, and where two entries turn out to be among the strongest ungraded Labs in the catalog for exactly the opposite reason.

### The Network World fit test is two questions

This family makes a recurring mistake impossible to ignore: **a graph being the correct World Layout does not tell you whether local propagation is the correct mechanism.** The contrast within these six entries is stark.

| Entry | Is the graph real? | Does each transition depend on bounded relational information? |
| :--- | :--- | :--- |
| 42 Power grid | Yes — the transmission graph is engineered | **No.** Line loading comes from a whole-network electrical solve. |
| 43 Water | Yes — the pipe graph is documented | **No.** Flow is a simultaneous hydraulic solution over the whole network. |
| 45 Service cascade | Yes — emitted by telemetry | **Yes.** A service decides from its own queue, its timeout, replies from immediate dependencies, and its local breaker state. |
| 46 Routing | Yes — the AS graph is public | **Yes.** Each participant selects and advertises from local policy and neighbour announcements. |

> **A Network World fit review must answer both questions separately.** They are different requirements, and this is one of the most important lessons of the sixty-Lab exercise.

The family splits cleanly:

| Driver class | Entries | Consequence |
| :--- | :--- | :--- |
| **Domain-defining global solve** | 42 power flow, 43 hydraulics | The local Plugin becomes ceremonial. **Likely mechanism-fit failure.** |
| **Planned / coordinated process** | 44 timetabling and dispatch | The dominant dynamics are scheduled, not emergent. |
| **Genuinely local, genuinely known** | **45 retry policies, 46 the BGP decision process** | The rule is a local rule a human wrote and it runs in production. |

That last row is unusual enough to state plainly. In most of this catalog the local mechanism is nature's and must be inferred. In entries 45 and 46 **the mechanism is specified, human-written, local, and deployed** — which places them in the *mechanism-analysis* mode rather than the *mechanism-discovery* mode identified in Family F. Generation is not the star; Study is.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 41 — Urban Growth

| | |
| :--- | :--- |
| **Role** | Calibration Lab · policy counterfactual Studies |
| **Standing** | [strong], inherited; not re-derived |
| **Falsifiable question** | Does a green belt reduce sprawl or displace it, and under which local development mechanisms? |
| **World fit** | Excellent — land cover arrives as a raster, so the World matches the data |
| **Mechanism fit** | Good, with a caveat: the rule is a statistical regularity of human decisions, not a physical law |
| **Evidence fit** | **Excellent** — historical land-use maps, with an established goodness-of-fit practice |
| **Question fit** | Real and contested |
| **Visual credibility** | **Class 1** — land use decisions are litigated |

**The phenomenon.** Cities grow at their edges, along roads, and in scattered patches that later fill in. **Leapfrog development** — a subdivision appearing well beyond the built edge with farmland between — is the signature of late-twentieth-century sprawl, and it arises from parcel-by-parcel decisions by people who are not coordinating.

**The established shortcut, and it is a cellular automaton.** **Clarke, Hoppen and Gaydos (1997)** built a CA of historical urbanization in the San Francisco Bay Area whose rules combine topography, road networks, and existing settlement, and whose control parameters **self-modify** — the automaton adapts itself to the circumstances it generates, during periods of rapid growth or stagnation [1]. That became SLEUTH, applied to dozens of metropolitan regions and used in planning contexts.

Urban scaling relations give infrastructure and socioeconomic quantities as systematic powers of population, with no spatial mechanism at all [11]. Fractal analysis of urban form is mature.

**Reducible.** Total developed area from population and density trends — arithmetic, and what most planning forecasts actually use. Infrastructure demand from scaling relations. Aggregate land consumption. Fractal dimension of an existing footprint, which is a measurement.

**Irreducible.** Leapfrog placement and whether the gaps later fill. **Road–development coupling** — roads attract development, development justifies roads, so which corridors form depends on which got built first: path dependence with a fifty-year memory. Infill versus expansion at a given growth rate. Boundary and policy effects, where growth suppressed here appears there and the displacement geometry is not predictable from the policy.

**What makes this Lab unusual.** Most [strong] entries are strong because the mechanism is physically local. This one is strong because **an operational precedent proves the modelling approach clears a real accuracy bar.** Land development is human decision-making, and there is no principle requiring it to be well described by neighbour rules. That it is, empirically, over decades, in dozens of cities, is a fact about the world and an asset to any argument SCR wants to make.

The corresponding weakness: a calibrated coefficient is a regularity of a particular era's economics and policy, not a law, and it is not stable across eras.

**Cell state.** *Persistent:* developed state, land use class, time since development. *Static:* slope, exclusion status. *Derived:* road access, neighbourhood development pressure.

**Frame it as a benchmark, not a new methodology.** The strongest argument for this Lab is **not** that local development decisions imply a CA — human decision-making is not inherently local, and the brief concedes it. The argument is empirical: *a cellular model in this domain has already been calibrated against historical maps and used operationally.* SCR therefore does not have to win the philosophical argument first; it can be benchmarked against a working modelling tradition. The open questions become benchmark questions:

- Can SCR generate mechanism variants whose map-level fit is competitive?
- Can it identify **alternate rule families with equal aggregate fit but different policy sensitivity**?
- Can it expose which assumptions drive leapfrog versus infill?
- Does it systematically retain the failed rule families?

**A hybrid Layout, and the cheap answer to it.** The World is raster-like, roads are network-like, and developers and planning authorities act at different scales again. This does not need a HybridWorld abstraction. It needs **a World that declares more than one Connection class** — spatial adjacency, road connectivity, jurisdiction membership, service reach — with a Plugin declaring which relation it reads. That likely resolves several Labs without inventing a World type per combination, and it helps entry 47, where network reachability and identity trust coexist.

**Assessment.** *(judgment, no standing)* **Calibration is genuinely achievable here, which is rare.** A Run's output is a map, the reference is a map, and the SLEUTH community already has goodness-of-fit measures. This may be the best domain in the catalog for showing that generated mechanisms can be **scored against real data quantitatively** rather than qualitatively. The policy counterfactual is a clean Small-Change Test on a question planners argue about with limited evidence.

---

## Lab 42 — Power Grid Cascade

| | |
| :--- | :--- |
| **Role** | Boundary case — **domain-defining global solve** |
| **Standing** | Ungraded; I would grade it **weak for core mechanism fit** |
| **Falsifiable question** | Under which local load-redistribution rules do blackout size distributions match, and does matching the exponent tell you anything about mechanism? |
| **World fit** | Good — a Network World with a real, engineered topology |
| **Mechanism fit** | **Failing.** Power flow is Kirchhoff's laws over the whole network. |
| **Evidence fit** | Good for events; topology is security-restricted |
| **Question fit** | The tail only; operators own the rest |
| **Visual credibility** | **Class 1** — critical infrastructure |

**The phenomenon.** A line trips. Its power does not vanish; it redistributes across the remaining network instantaneously and globally. Some other line, now overloaded, heats, sags, and trips. Most such events stop after one or two trips. Occasionally they do not, and a continent-scale blackout follows in minutes. Blackout sizes across decades of records follow a heavy-tailed distribution.

**The established shortcut, and it is complete for the case it covers.** N-1 security analysis — check the system survives the loss of any single element — is computed continuously by operators, and the DC power flow approximation makes it linear algebra fast enough to sweep thousands of contingencies. Cascade research models such as the OPA lineage reproduce power-law blackout distributions as a self-organized critical phenomenon [11].

**The cautionary tale this Lab must know.** A widely-publicized 2010 paper on interdependent networks argued for catastrophic grid vulnerability using a coupled power–communication model, and was heavily criticized by power systems engineers on the grounds that the network model bore little resemblance to a real grid — random topology, no electrical physics, unrealistic interdependence [11]. **A topologically plausible model of an engineered system, published by people who did not consult the engineers, produced conclusions the engineers considered meaningless.** That is precisely the failure §30.8 and §41 exist to prevent, and it happened in this exact domain, in a top journal.

**Why the mechanism fit fails.** Getting the Layout right is necessary and nowhere near sufficient. **The World's Connections describe what is physically wired; they do not describe how power flows**, which is determined by impedances and generation across the entire network. A Plugin reading only its neighbours cannot know its own loading. This is the domain-defining global solve in its clearest form — and unlike entry 34, there is no plausible local surrogate on offer.

**Irreducible, if the solve is admitted.** N-k sequences, where the combinatorics explode and only a vanishing fraction are dangerous. **Hidden failures** — protection equipment misoperating, tripping a healthy line — a documented contributor to real cascades and by definition outside the intended model. Timing and operator action under stale information: the 2003 Northeast blackout's alarm failure is the canonical case, where the mechanism raced an observer who did not know what was happening.

**Cell state.** *Persistent:* tripped state, protection state. *Static:* capacity. *Globally computed:* loading — which is the entire problem.

**This entry is more dangerous than merely weak, and that is the critique's sharpest point about it.** The hazard is not that an abstract local cascade model is inaccurate. It is that such a model produces **convincing cascade shapes, heavy-tailed blackout distributions, plausible network visualizations, and apparently scientific conclusions — while representing the wrong causal system.** That is precisely the failure §12 and §26 exist to prevent, and the Buldyrev episode is the documented precedent.

> **Power Grid must not become a brochure visualization Lab.** Either the execution includes physically valid power flow, or the visualization is **explicitly labelled as an abstract cascade experiment.** There is no third option that is honest.

And if power flow *is* included, SCR's role must be reframed accordingly: Study orchestration, failure-sequence exploration, operator-information experiments, and comparison of protection and response policies. **Not "local rules explain the grid."**

**Assessment.** *(judgment, no standing)* **Weak for core local-mechanism fit, and hazardous rather than merely weak.** Two honest positions exist. Study the **cascade statistics question as a methodological one** — since both real grids and abstract sandpiles produce heavy tails, does matching an exponent tell you anything about mechanism? Probably not, and demonstrating that clearly would serve a literature that has repeatedly over-read exponent matches. Or admit the global solve explicitly and treat the Lab as a test of whether SCR can express that division — DEC-1 territory.

The genuinely under-modelled thread is **hidden failures and operator stale information**, which fall between the power engineers' tools and the network scientists', and which are local, discrete, and documented in public post-incident reports.

---

## Lab 43 — Water Distribution

| | |
| :--- | :--- |
| **Role** | **Rejected fit** — a distinct rejection reason worth recording |
| **Standing** | Ungraded; I would grade it **rejected** |
| **Falsifiable question** | None that is open. |
| **World fit** | Good — a documented Network World |
| **Mechanism fit** | **Failing** — hydraulics is a simultaneous solve |
| **Evidence fit** | Good and irrelevant |
| **Question fit** | **None** |
| **Visual credibility** | Class 1 — public health |

**The phenomenon.** A municipal network of pipes, junctions, tanks, valves, and pumps. Practice asks two questions: does everyone get enough pressure, and if something enters the network where does it go and when does it arrive.

**The established shortcut.** Hydraulic network analysis computes steady and extended-period flow and pressure from conservation and head-loss equations. **EPANET is free, standard, and has been for thirty years**, computing hydraulics and water quality including contaminant transport, decay, and water age, and forming the basis of most commercial water modelling [11]. Utilities calibrate models of their own systems against field measurements. Sensor placement is an optimization over simulated scenarios.

**The rejection reason, and it is not the same as entry 42's.** There is no closed-form equation here — but there is something stronger for SCR's purposes: **a fast, exact, free, standard numerical solver that answers the questions practitioners ask.** The absence of a formula does not mean irreducibility; it means the computation is a solve that takes milliseconds.

> **"There is no formula" and "it is irreducible" are different statements, and the difference disqualifies this Lab.**

**The rejection reason differs from entry 42's and from Fracture's, and the distinction is worth preserving.** Fracture fails because the actual physics is non-local in a way a local mechanism cannot preserve honestly. Water Distribution fails on a shorter list: the hydraulic equations are known, the numerical solution is standard, the solver is free, practitioners already use it, and the questions are operationally answered. That is **an even cleaner disqualification**, and it yields a methodological lesson the omnibus should state explicitly:

> **"Needs computation" is not the same thing as "needs SCR."** A deterministic solver may require iteration, simulation, or numerical methods and still leave no useful mechanism-supply problem.

Every criterion points down: hydraulic coupling is global rather than adjacent; the phenomenon is the solution of a determinate system rather than emergent; the incumbent is exact, free, and standard; and there is no live scientific controversy about the mechanism.

**The narrow residue, which belongs elsewhere.** Biofilm and disinfectant residual in stagnant low-flow zones is a genuine local biological process on a substrate whose flow field is *given* rather than computed by the mechanism. That connects to entry 25 and belongs to the biofilm Lab with a water-network World — not to a water distribution Lab.

**Assessment.** *(judgment, no standing)* **Reject, and record the reason.** This entry contributes a rejection category distinct from the others: not *the agents use global information* (entry 60), not *the driving physics is a global solve* alone (entry 42), but **the mathematics is already solved by a mature free tool and the real problem is not open.** A catalog that can articulate distinct rejection reasons is a better instrument than one that only says "poor fit". Also worth noting: network topology and contamination modelling are security-restricted in many jurisdictions, so a public Lab here carries dual-use concerns independent of its fit.

---

## Lab 44 — Freight and Rail Congestion

| | |
| :--- | :--- |
| **Role** | Boundary case — planned process; **DEC-3 forcing case** |
| **Standing** | Ungraded; I would grade it **weak** |
| **Falsifiable question** | At what utilization does a network deadlock, and why does recovery take so much longer than congestion? |
| **World fit** | Good — a documented Network World |
| **Mechanism fit** | **Weak** — dispatch and timetabling are coordinators |
| **Evidence fit** | Good for passenger rail; **freight data is proprietary** |
| **Question fit** | Narrow |
| **Visual credibility** | Class 2 |

**The phenomenon.** A train arrives at a full yard and waits on a siding; the siding is now unavailable; the next train stops on the main line; a junction blocks; trains on an unrelated route are delayed. The network has a **capacity cliff** — below a utilization threshold delays absorb into schedule buffer, above it they amplify and the network locks up, sometimes for weeks.

**The established shortcut.** Queueing theory describes the cliff — Little's law, the sharp rise in waiting time as utilization approaches one, and the effect of variability — with railway-specific formulations for line capacity [11]. Timetabling and real-time rescheduling are optimization problems with a large, applied operations research literature and mature solvers. Delay propagation is modelled on explicit activity-dependency graphs.

**Why the fit is weak, on two independent grounds.**

*The mechanism is a plan.* Dispatch decisions and timetables are coordinators, and the dominant dynamics are scheduled rather than emergent — the same rejection category as entries 39 and 53.

*Time is clock-driven, not tick-driven.* Trains run on **schedules**: events happen at specified clock times rather than uniform intervals. A lockstep model must either make the tick tiny (expensive, most cells idle) or quantize the schedule — **which changes the conflicts, and the conflicts are the phenomenon.** This Lab is therefore blocked in a way most are not: a lockstep-only platform probably cannot represent the domain honestly at all, which makes it the clearest **DEC-3 forcing case** in the catalog.

**The genuinely interesting residue.** Deadlock, where trains cannot move because moving requires someone else to move first — the same structure as counterflow deadlock (38) and robot deadlock (39). **Recovery hysteresis**, where a congested network unwinds far more slowly than it congested, and the path depends on the specific arrangement of stranded equipment and expired crews.

**Assessment.** *(judgment, no standing)* **Keep as a DEC-3 and discrete-event stress case; do not prioritize as a Lab build.** The residual questions are real but appear more cleanly elsewhere — deadlock in entries 38 and 39, metastability in 45, scheduling and asynchrony in 46. **Its architecture lessons can be harvested without making rail a product commitment.**

---

## Lab 45 — Service Cascade

| | |
| :--- | :--- |
| **Role** | **Flagship** — mechanism-analysis Lab; strongest ungraded entry in the catalog |
| **Standing** | Ungraded; I would grade it **strong** |
| **Falsifiable question** | Which single timeout or retry-policy change moves a given dependency graph from resilient to metastable? |
| **World fit** | **Excellent** — the dependency graph is emitted by production telemetry |
| **Mechanism fit** | **Excellent, and unusually so** — a retry policy is a local rule someone wrote |
| **Evidence fit** | **Exceptional** — traces, metrics, and detailed public post-incident reports |
| **Question fit** | Real, operational, and unserved |
| **Visual credibility** | Class 3 — nobody dies, and the audience is technically literate |

**The phenomenon.** One service slows. Its callers wait, holding threads; when they time out they **retry**, sending more load to the struggling service; their callers see slowness and retry too. Within a minute retry traffic dwarfs real traffic, every service is saturated with work that will be discarded, and the system is down. Remove the original trigger and it **stays** down, because the retry load is now self-sustaining. Recovery requires shedding load.

**The established shortcut, and the naming is recent.** Bronson, Aghayev, Charapko and Zhu (2021) articulated **metastable failure** explicitly: a sustaining effect — usually retries or queue buildup — keeps the system in the bad state after the trigger is gone, and a vulnerable state exists before any trigger arrives. They note such failures manifest as black swan events: nothing in the past points to their possibility, the impact is severe, and they are far easier to explain in hindsight than to predict [2]. The mitigations are known and deployed — circuit breakers, exponential backoff with jitter, load shedding, bulkheads, retry budgets — and documented publicly. Queueing theory covers the reducible half.

**Reducible.** Steady-state latency and throughput at a given utilization. Capacity planning. Timeout budget arithmetic across a call chain. **The existence of the bistability**, once the retry amplification factor is written down — a mean-field argument gives the two fixed points.

**Irreducible.** **The vulnerable state is invisible** — a system can meet every objective and be one trigger from collapse, because the margin between healthy load and retry-amplified load has narrowed. No metric shows it; it is a property of the whole graph's configuration. Which trigger tips it, when a trigger absorbed on Tuesday collapses the system on Thursday because an unrelated deployment changed a timeout. The cascade path, which is why post-incident reports read like traversals. **Interaction of mitigations** — a circuit breaker opening sheds load onto a fallback that may itself saturate, and whether individually-correct mitigations compose into a stable system is not derivable from each in isolation. That is where real outages live.

**Why this is the flagship.** The mechanism is genuinely local **and genuinely known**; the topology is importable from production telemetry rather than guessed; metastability is the irreducibility structure SCR suits best; the data is exceptional; the question is Study-shaped; and **there is no dominant incumbent modelling tool** — chaos engineering injects faults into production, which is empirical rather than predictive, and queueing models cover only the reducible half.

This is the catalog's clearest instance of the **mechanism-analysis mode**: nothing needs inferring, and the many-service consequences still require simulation to establish.

**Cell state.** *Location (service):* queue depth, in-flight requests, circuit breaker state, health. *Static:* capacity, timeout, retry policy. Connections are **directed and latency-bearing** — a call one way, a response the other, with a delay that is load-bearing because it is what makes timeouts meaningful.

**On mechanism-analysis mode, made concrete.** A user might literally paste a retry policy, a timeout, and circuit breaker rules, and ask *under what dependency topologies does this become metastable?* **That is SCR even if Generation writes nothing** — which is why the platform's identity should not be defined too narrowly around mechanism generation. Study orchestration over known mechanisms is equally native.

**Assessment.** *(judgment, no standing)* **Flagship candidate — and plausibly a better near-term commercial Lab than the explicitly security-branded ones.** Operators have budget, the domain is measurable, misuse risk is low, the causal semantics are clear, and — unusually — **the audience is capable of critiquing the model**, which lowers the credibility risk that afflicts entry 42. The headline capability is what operators want and cannot get: *is my system currently in a vulnerable state?* Answering requires exploring what a trigger would do, which is running the mechanism. A Small-Change Test over a production-derived topology, asking which single timeout moves the system from resilient to fragile, is SCR's Study machinery aimed at a real operational question with a budget behind it.

Two caveats. Shared infrastructure — a database, a network fabric, an availability zone — couples services that are not adjacent in the dependency graph, which is a partial global-driver problem. And **timing is the mechanism**, so lockstep with a uniform tick fits poorly: this Lab needs DEC-3 more than it needs anything else.

---

## Lab 46 — Routing Instability

| | |
| :--- | :--- |
| **Role** | Mechanism-analysis Lab; **the catalog's most rigorous irreducibility credential** |
| **Standing** | Ungraded; I would grade it **plausible-to-strong** |
| **Falsifiable question** | How does the probability of a divergent policy configuration scale with network size and policy diversity? |
| **World fit** | Excellent — the autonomous-system graph is public |
| **Mechanism fit** | **Excellent** — the BGP decision process is specified, local, and running in production |
| **Evidence fit** | **Exceptional** — twenty years of public BGP measurement archives |
| **Question fit** | Real and unanswerable analytically |
| **Visual credibility** | Class 2, with dual-use sensitivity |

**The phenomenon.** Each autonomous system tells its neighbours which destinations it can reach and by what path; each recipient applies its own local policy to decide what to believe and what to pass on. No central authority, no global view — every router's picture of the internet is assembled from what neighbours said, some time ago. When something changes, the news propagates hop by hop, and during propagation different parts hold inconsistent views. Sometimes it does not settle at all: certain combinations of individually sensible policies have no consistent global solution, and routes flap indefinitely.

**The established shortcut — and this Lab has a hardness theorem exactly where the irreducibility is.** Griffin, Shepherd and Wilfong formalized policy routing as the **Stable Paths Problem** and showed that **determining whether an instance has a solution is NP-complete** [3]. They defined SPVP, a distributed algorithm capturing BGP's dynamic behaviour abstractly, and proved it converges to the unique solution when **no dispute wheel exists** — and can only diverge when one does. Crucially, **SPVP can diverge even when a solution exists** [3].

Convergence delay is measured: BGP can take minutes rather than seconds after a withdrawal because routers explore many alternative paths in sequence [11]. The Gao–Rexford conditions give a practical sufficiency guarantee — if every system follows the customer–provider–peer valley-free hierarchy, the system converges — which is why the internet works despite the hardness result [11].

**Reducible.** Convergence under Gao–Rexford, by theorem. Shortest-path routing without policy. Steady-state selection given a converged state. Reachability from a routing table.

**Irreducible, and provably so.** Whether an arbitrary policy configuration converges — NP-complete to decide, a theorem about the problem rather than a modelling limitation. **The transient**: even when a configuration converges, which routes are tried, in what order, how long it takes, and what traffic is lost depends on message timing and ordering across the network, so the same configuration converges differently depending on who heard what first. Interaction of independently-edited policies, which thousands of organizations change without coordination or visibility. Route leaks and their blast radius.

**Why this is the strongest irreducibility credential in the catalog.** Where wildfire has *the closed form breaks near the percolation threshold*, routing has *deciding this is NP-complete, here is the proof, and here is a small counterexample*. It also has the cleanest instance of **message-passing asynchrony as the mechanism** rather than a complication — routers act on what neighbours told them, when they told them, and different orderings give different transients. That is SCR-F §18.5 as the load-bearing element, not optional.

**Cell state.** *Persistent:* selected route per tracked destination, routes announced by neighbours, pending announcements. *Static:* local preference policy. Bounded **only if the number of tracked destinations is small** — a substantive restriction, since real routers hold near a million prefixes.

**Assessment.** *(judgment, no standing)* **Plausible-to-strong, and intellectually the most rigorous entry in the catalog.** The exciting thread is **policy composition**: nobody can check whether the internet's current global configuration is stable, because nobody sees all the policies and the decision is NP-complete anyway. But asking *which classes of local policy, composed at scale, produce oscillation, and how the probability of a dispute wheel scales with size and diversity* is a statistical question about mechanism space — open, practically consequential, and unattacked because it requires running many mechanisms.

**This is the strongest acceptance case for asynchronous Reactor semantics in the catalog** — cleaner than rail, because the local protocol is explicitly specified, the topology is relational, message semantics are natural, and public historical data exists. Asynchrony here is not realism garnish; **it is the mechanism**, and a lockstep approximation risks changing exactly the behaviour under Study.

> **If SCR implements asynchronous or discrete-event Reactor semantics, Routing Instability should be one of the acceptance-test Labs.**

Blocked hard on **DEC-3**: lockstep would model a protocol that does not exist. And dual-use care applies — work identifying destabilizing policy configurations warrants the same handling as Family H (F-20).

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Globally-computed drivers** — the boundary established by entry 31 | *unregistered* | 42 and 43 are its largest concentration; 45 partially, via shared infrastructure |
| **Rejection reasons recorded, not just grades** | **DEC-15** | 43 contributes a category distinct from 42's and 60's |
| **Asynchronous message passing and clock-scheduled events** | **DEC-3** | 46 (the protocol *is* asynchrony), 44 (timetables), 45 (timeouts). **The densest DEC-3 cluster in the catalog.** |
| **Mechanism analysis as a distinct mode** | *unregistered* | 45 and 46 — the rule is known, the consequences are not |
| **Coordinator semantics** | **DEC-1** | 44 dispatch |
| **Bounded state under realistic scale** | **CELL ceiling** | 46 — a real routing table is a million prefixes |
| **Global-driver dependency declared in fit review** | *unregistered* | 42, 43. A Lab must state whether critical transition values come from bounded local information, a generic global helper, or a **subject-specific global solver** — and if the last, justify what SCR adds beyond orchestrating that solver. |
| **Multiple Connection classes in one World** | *unregistered* | 41 (spatial + road + jurisdiction). Treat Grid, Network, Identity, and Agent as common *patterns* rather than mutually exclusive boxes. |
| **Connection state as first-class and bounded** | *unregistered* | 45 (latency, direction, in-flight), 46 (announcement delay). Same readable-bounded-declared discipline as Cell state; a Connection must not become an object with unlimited hidden logic. |

### DEC-3 needs a vocabulary, not a boolean

Five entries in this family and Family F pressure temporal semantics, and they need different things. **Do not resolve DEC-3 with a single flag such as "supports async."** The Reactor needs a small, explicit, still-deterministic execution vocabulary:

| Term | Meaning |
| :--- | :--- |
| **Step** | All current participants evaluate against one declared view of state |
| **Delayed effect** | A proposal becomes eligible after a declared offset |
| **Message** | A bounded payload traverses a Connection with deterministic delay |
| **Scheduled event** | A World- or Study-owned event occurs at a defined logical time |
| **Phase** | A named execution mode changes which transitions or inputs apply |

Entry 46 is the natural acceptance case for *message*; entry 44 for *scheduled event*; entry 34 in Family E for *phase*.

### Build priority within the family

**Tier A.** **Service Cascade (45)** — the strongest ungraded entry in the catalog; local known mechanism, importable topology, exceptional data, no incumbent. **Urban Growth (41)** — the best quantitative calibration opportunity outside Family E.

**Tier B.** **Routing Instability (46)** — the most rigorous irreducibility case, blocked on DEC-3.

**Boundary and rejection value.** **Power Grid (42)** — a documented cautionary tale about topologically plausible models of engineered systems. **Freight and Rail (44)** — the clearest DEC-3 forcing case. **Water Distribution (43)** — reject, and record the reason.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** Clarke, K. C., Hoppen, S. & Gaydos, L. (1997). A self-modifying cellular automaton model of historical urbanization in the San Francisco Bay area. *Environment and Planning B* **24**, 247–261. *(Control parameters self-modify — the automaton adapts to the circumstances it generates during rapid growth or stagnation. Basis of SLEUTH.)*
2. **[V]** Bronson, N., Aghayev, A., Charapko, A. & Zhu, T. (2021). Metastable failures in distributed systems. *HotOS '21*, 221–227. *(A sustaining effect keeps the system in the bad state after the trigger is gone; a vulnerable state exists before any trigger. Manifest as black swan events — easier to explain in hindsight than to predict.)*
3. **[V]** Griffin, T. G., Shepherd, F. B. & Wilfong, G. (2002). The stable paths problem and interdomain routing. *IEEE/ACM Transactions on Networking*. *(Determining whether an instance has a solution is **NP-complete**. SPVP converges if no dispute wheel exists, can only diverge when one does, and can diverge even when a solution exists.)*
4. **[D]** Labovitz, C. et al. (2000) — delayed BGP convergence and path exploration; Gao, L. & Rexford, J. (2001) — sufficient conditions for stable interdomain routing.
5. **[D]** Dobson, I., Carreras, B. A., Newman, D. E. et al. — the OPA model and power-law blackout size distributions; Buldyrev, S. V. et al. (2010) on interdependent networks and the power-systems criticism of its grid model.
6. **[D]** EPANET (US EPA) hydraulic and water quality network solver; the Hardy Cross method (1936).
7. **[D]** Google SRE and AWS architecture guidance on circuit breakers, backoff with jitter, load shedding, bulkheads, and retry budgets.
8. **[D]** Bettencourt, L. & West, G. — urban scaling relations; Batty, M. & Longley, P. — fractal analysis of urban form.
9. **[D]** UIC compression method for railway line capacity; Kingman's approximation for waiting time in a general queue; railway timetabling and real-time rescheduling as integer programmes.
10. **[D]** Public post-incident reports for the 2003 Northeast and Italian blackouts, including the alarm-system failure and operator situational awareness findings.
11. **[D]** N-1 contingency analysis and the DC power flow approximation as continuous operational practice.

---

## Non-claims

This report performs no fit reviews and establishes no fit. Nothing here projects growth for any city, assesses grid reliability or vulnerability, models any water system, evaluates rail capacity, predicts outages for any service, or assesses routing stability for any network or operator. **No output described here is suitable for planning, investment, operational, engineering, public health, or security decisions** (§41, §43). Assessments are the author's judgment, carry no standing, and do not promote any entry.
