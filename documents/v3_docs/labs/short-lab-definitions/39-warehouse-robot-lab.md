# 39. Warehouse Robot Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #39, Family F · **Standing:** **[plausible]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A modern fulfilment centre runs on hundreds of mobile robots driving beneath storage pods, lifting them, and carrying them to picking stations. They move on a marked grid, in discrete steps, obeying a shared plan.

The interesting behaviour is congestion. Robots queue at picking stations, corridors saturate, and the whole fleet's throughput falls below what the individual robots could achieve. Occasionally the system deadlocks — a cycle of robots each waiting for the next to move — and needs intervention.

There is a second, subtler effect. The *layout of stored goods* changes over time as pods are returned to different positions, and popular items drift toward the stations. That reorganization is emergent and affects throughput more than the routing does.

## What the domain already knows

**This is a solved engineering problem with a solved-problem literature.** The relevant field is multi-agent path finding: given a set of agents with start and goal positions on a graph, find collision-free paths. It is NP-hard to optimize in general, but practical algorithms — conflict-based search and its descendants, prioritized planning, and windowed variants — solve realistic instances well, and there is an active academic community with standard benchmarks.

**Real systems are centrally scheduled.** The Kiva system that Amazon acquired, and its competitors, use a central planner that assigns tasks and reserves paths. Robots do not negotiate locally; they execute an allocated plan. Deadlock is prevented by construction in most deployments rather than resolved after the fact.

**The traffic analogy is real but partial.** Congestion in a robot fleet resembles the traffic phenomena of #37 — density-dependent throughput collapse, shockwaves in corridors — and traffic-CA-derived reasoning has been applied. But the driver is different: robots do not have reaction-time noise, and the randomization step that makes Nagel–Schreckenberg produce spontaneous jams has no analogue.

## Where the shortcut holds, and where it breaks

**Reducible — and this is the Lab's central difficulty.** With a central planner, the system's behaviour is *the plan's* behaviour. Throughput follows from the schedule. Deadlock does not occur if the planner prevents it. Congestion is a property of the routing policy, which is designed rather than emergent. **When the mechanism is a designed algorithm, there is nothing to discover about it by simulation that its designers do not already know** — they can inspect it.

That is a qualitatively different situation from every other Lab in this catalog. Wildfire's mechanism is nature's and must be inferred. This mechanism is a piece of software somebody wrote.

**Irreducible — the residue, and it is genuine but narrow:**

- **Emergent congestion under a given policy.** Even a well-designed policy produces interactions its designer did not enumerate. Whether a particular density and layout produces throughput collapse is an emergent property of many agents executing the policy, and it is generally established by simulation because the analysis is intractable.
- **Deadlock in decentralized or degraded operation.** If the central planner fails, or in systems that use local negotiation for tractability at scale, deadlock becomes possible and its likelihood is configuration-dependent.
- **Layout self-organization.** The drift of popular inventory toward stations is a genuine emergent process driven by simple local rules (return the pod to a nearby free slot), and it is not designed.
- **Scaling behaviour.** How throughput degrades as fleet size grows for a fixed floor area is an empirical curve with a threshold, and the threshold's location is not predictable from the policy alone.

**The lens, stated plainly.** The position paper's grading note is exactly right and worth quoting: *"discrete space is literally true here, but real fleets are centrally scheduled, which is exactly what CA lacks."* The abstraction fits the *geometry* perfectly — the floor genuinely is a grid, time genuinely is discrete, robots genuinely occupy one cell — and fails on the *mechanism*, because the controlling logic is global.

That is an unusual failure mode and worth recording as one: **a Lab can have excellent World fit and poor mechanism fit**, and the two are separable questions (§30.2 versus §30.3). This is the catalog's clearest example.

## What a Cell would carry

A floor cell: occupancy by a robot, pod present, reservation state, and station or corridor designation. Robots carry a task, a destination, and a battery level. Bounded and small; §13.1 met.

Layout is a grid, and — rare in this catalog — **it is not an abstraction at all.** The floor is literally a marked grid, robots literally occupy discrete cells, and steps are literally synchronized. The World fit is exact in a way that only #35 (adsorption sites) matches.

**The scheduler is the problem.** A central planner is a mechanism that reads the whole World and writes to many Cells — which is not a local mechanism in any sense the platform recognizes. Whether it lives as a World condition, a second Plugin, or outside the model entirely is DEC-1's question, and here it is not a marginal complication: it is the dominant driver.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, and I agree with the inherited grade — but the reason to build it is architectural, not commercial.**

The commercial framing is weak. Operators of these systems have detailed simulators of their own fleets, calibrated against telemetry from the actual floor, and they use them for exactly the congestion questions this Lab would ask. SCR would be offering a less accurate version of a tool they already run, on a system whose mechanism they wrote.

**The upside worth being excited about — and it is a real one.** This Lab is the catalog's cleanest test of **whether SCR can express a system that has both local mechanisms and a global coordinator**, and that combination recurs everywhere: patch deployment rings (#53), routing protocols (#46), immune recruitment (#26), defender response in Family H. If DEC-1 resolves in a way that permits a coordinating mechanism alongside local ones, this is the domain where the resolution can be tested cheaply and checked against ground truth, because the coordinator is a known algorithm rather than an inferred one.

That is worth something: **a Lab where you already know the right answer is a good place to test whether the platform can express the question.**

The layout self-organization thread is also genuinely emergent and under-studied, and it is the one part of this domain nobody designed.

**The challenges, in order of severity.**

1. **The mechanism is designed software**, so there is nothing to infer about it.
2. **The central scheduler is not a local mechanism** and dominates the outcome — DEC-1 in its hardest form.
3. **Operators have better simulators** calibrated on real telemetry.
4. **The domain is commercially closed** — throughput and layout data are trade secrets, so validation data is largely unavailable outside the operators.
5. **Robots do not have behavioural noise**, removing the ingredient that makes the analogous traffic model interesting.

## Non-claims

This Lab does not model any real fulfilment system, does not assess throughput or layout for any operator, and produces nothing suitable for operational or engineering decisions (§41, §43).
