# 45. Service Cascade Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #45, Family G · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A microservice architecture is a graph of services calling each other over the network. One service slows down — a dependency is degraded, a cache is cold, a deployment is bad. Its callers wait, and while waiting they hold connections and threads. When they time out, they **retry**, which sends more load to the already-struggling service. The callers' callers now see slowness too, and they retry.

Within a minute the retry traffic dwarfs the original traffic, every service is saturated with work that will be thrown away, and the whole system is down. Then the original trigger is removed — and the system stays down, because the retry load is now self-sustaining. Restoring service requires shedding load, which usually means turning something off.

This has a name in the distributed systems literature: a **metastable failure**. The system has two stable states — healthy and collapsed — and a trigger can push it from one to the other, after which removing the trigger does not bring it back.

## What the domain already knows

**Metastable failure was named and characterized recently.** A 2021 HotOS paper by Bronson and colleagues at Meta articulated the pattern explicitly: a sustaining effect (usually retries or queue buildup) that keeps the system in the bad state after the trigger is gone, and a vulnerable state that exists before any trigger arrives *(attribution from memory, verify)*. It gave the industry vocabulary for something operators had been living with for a decade.

**The mitigations are known and deployed.** Circuit breakers (stop calling a failing dependency), exponential backoff with jitter (spread retries out), load shedding (reject work early rather than queue it), bulkheads (isolate resource pools), and retry budgets (cap the total retry rate) are all standard, well-documented, and widely implemented. Google's SRE materials and AWS's architecture guidance are the reference literature and are public.

**Queueing theory supplies the reducible framework**, as in #44: utilization, Little's law, and the sharp rise in latency as capacity is approached.

**The observability situation is exceptional.** Modern distributed systems emit distributed traces, per-service latency and error metrics, and dependency graphs, continuously. Companies publish detailed public post-incident reports. This is, along with #37, the best telemetry situation in the catalog — and unlike traffic loop detectors, it includes the *dependency topology* directly.

## Where the shortcut holds, and where it breaks

**Reducible.** Steady-state latency and throughput at a given utilization — queueing theory. Capacity planning. Whether a service can absorb a given traffic increase. Timeout budget arithmetic across a call chain. The existence of the bistability, once the retry amplification factor is written down — a mean-field argument gives you the two fixed points.

**Irreducible.** Which state the system is in, and how it got there:

- **The vulnerable state is invisible.** A system can be operating normally, meeting every SLO, and be one trigger away from collapse — because the margin between healthy load and the retry-amplified load it would face has narrowed. No metric shows this directly. It is a property of the whole graph's configuration.
- **Which trigger tips it.** A trigger that is absorbed on Tuesday collapses the system on Thursday because a deployment changed a timeout somewhere unrelated. Whether a specific perturbation propagates depends on the current configuration of every timeout, retry policy, and capacity in the graph.
- **Cascade path.** Which services fail, in what order, is a specific traversal of a specific dependency graph under a specific load pattern. Post-incident reports read like traversals because that is what they are.
- **Interaction of mitigations.** Circuit breakers and retries interact non-trivially; a breaker opening sheds load onto a fallback path that may itself saturate. Whether a set of individually-correct mitigations composes into a stable system is not derivable from each in isolation, and this is where real outages live.

**The lens, stated plainly.** This is a **metastability domain**, and metastability is the purest computational-irreducibility structure in the catalog after karst (#7). The mean-field argument tells you two stable states exist. Nothing tells you which one you are in, how close you are to the edge, or which path a collapse takes — because those depend on the accumulated configuration of a graph that dozens of teams change daily.

And crucially: **the mechanism here is genuinely local.** A service knows only its own queue, its own timeouts, and the responses from its immediate dependencies. It retries based on local information. That is a real, honest, local rule — not an abstraction of one. Very few Labs in this catalog can say that.

## What a Cell would carry

A service: queue depth, in-flight requests, capacity, timeout setting, retry policy state, circuit breaker state, and current health. Bounded scalars; §13.1 met comfortably, and the state is *literally* what a service's runtime holds.

**Layout is a Network World** — the dependency graph — and it is documented, observable, and machine-readable in real systems. Service meshes emit it automatically. That is an unusual gift: a domain where the World's topology can be imported from production telemetry rather than guessed.

The one genuine subtlety: **requests flow along edges and return**, so a Connection carries a call in one direction and a response in the other, with a delay. That is a directed, latency-bearing connection, and the delay is load-bearing — it is what makes timeouts and retries meaningful. Whether the platform can express that is a real mechanism-fit question and touches DEC-3.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong — and I would grade it the strongest ungraded entry in this catalog, ahead of most of Family H and most of Family G.**

The case is unusually complete and I want to state it clearly, because the catalog buries this entry in the middle of an infrastructure family:

- **The mechanism is genuinely local and genuinely known.** A retry policy is a local rule someone wrote down. Unlike wildfire, nothing has to be inferred from physics; unlike #39, the coordination is not global.
- **The topology is real, documented, and importable** from production telemetry.
- **The phenomenon is metastable**, which is the irreducibility structure this platform is best suited to.
- **The data is exceptional** — traces, metrics, dependency graphs, and detailed public post-incident narratives with timestamps.
- **The question is Study-shaped**, not Run-shaped: nobody wants to know what happens in one outage; they want to know whether a configuration is safe across plausible triggers.
- **There is no dominant incumbent modelling tool.** Chaos engineering injects faults into production, which is empirical rather than predictive. Queueing models cover the reducible half. Nothing systematically explores mechanism space.

**The upside worth being excited about.** The headline capability is the one operators actually want and cannot get: **is my system currently in a vulnerable state?** That is a question about the whole configuration, and answering it requires exploring what a trigger would do — which is exactly running the mechanism. A Small-Change Test over a production-derived topology, asking which single timeout change moves the system from resilient to fragile, is the platform's Study machinery aimed at a real operational question with a real budget behind it.

The negative space is directly valuable too: "these mitigation combinations never prevented collapse under any retry mechanism we tried" is the kind of finding that would change architecture guidance, and no literature publishes failed configurations.

And there is a defensibility bonus: this domain's practitioners are software engineers who read post-incident reports for entertainment. They are unusually well equipped to evaluate whether a mechanism is plausible, which lowers the risk of the credibility failure that afflicts #42.

**The challenges, in order of severity.**

1. **Load and latency are somewhat global.** Shared infrastructure — a database, a network fabric, a cloud availability zone — couples services that are not adjacent in the dependency graph, and shared-resource contention is a real cascade path.
2. **Timing is the mechanism.** Timeouts, backoff intervals, and latency are the substance, so lockstep with a uniform tick is a poor fit — this Lab needs DEC-3 more than it needs anything else.
3. **Real topologies are proprietary**, though public post-incident reports and open-source reference architectures partly compensate.
4. **The substrate changes constantly** — a production system's configuration is not stationary, so a calibrated model decays.
5. **Operational credibility hazard** is real but milder than most: nobody dies, and the audience is technically literate.

## Non-claims

This Lab does not assess the reliability of any real system, does not predict outages, and produces nothing suitable for operational or architectural decisions without domain validation (§41, §43).
