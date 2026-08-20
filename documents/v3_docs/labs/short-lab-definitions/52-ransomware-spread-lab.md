# 52. Ransomware Spread Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #52, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §18.5, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

An operator with access to an enterprise network deploys encryption across as many systems as they can reach, as fast as they can, usually at a time chosen so nobody is watching. Deployment is often via the same management tooling the organization uses for legitimate software distribution, which is why it can cover thousands of machines in under an hour.

The defender's problem is a race with a very unforgiving clock. Detection, decision, and containment must all happen inside the encryption window. Containment usually means disconnecting network segments or shutting systems down — actions with their own large costs, taken under uncertainty, by people who have been woken up.

What determines the outcome is not primarily whether the malware is sophisticated. It is **how much of the environment was reachable from the deployment point**, whether backups were reachable too, and whether the defender acted before the reachable set was exhausted.

## What the domain already knows

**Incident reporting is extensive and largely narrative.** Response firms publish annual reports with dwell times, initial access vectors, and time-to-encryption statistics, and individual incidents are written up in detail. The aggregate picture — initial access, credential harvesting, lateral movement, staging, then mass deployment — is consistent and well documented.

**The reachability question is #47's and #48's.** How far encryption spreads is determined by what the deploying account can reach, which is the lateral movement and privilege problem. This Lab does not have a separate answer to that; it inherits one.

**Backup practice has a settled prescription and a well-known failure mode.** Offline or immutable backups are the recommended defence, and the recurring reason recovery fails is that backups were reachable with the same credentials as the systems they protected.

**Epidemic modelling has been applied and it fits badly.** Ransomware deployment is not a random-contact epidemic; it is a directed, deliberate, single-source push over an access graph, executed in minutes. The SIR-style framing that suits worms (#54) does not suit this.

## Where the shortcut holds, and where it breaks

**Reducible.** The extent question: given an access graph and a starting position, what is reachable — transitive closure, as in #47 and #48. Encryption throughput given system count and data volume — arithmetic. Recovery time from backups given their scope and restore rate — arithmetic, and it is what business continuity planning computes.

**Irreducible.** The race, which is the actual phenomenon:

- **Detection against propagation.** Both are processes with timing. Whether detection fires before the reachable set is exhausted depends on what triggers the detection, how quickly the signal reaches a human, and how long the human takes to decide. This is a genuine race between two mechanisms and its outcome is not a property of either.
- **Containment under stale information.** The defender sees the environment as it was — telemetry has latency, dashboards refresh, and the picture assembled during an incident is minutes old. Segmenting a network based on a stale picture may cut the wrong link. This is SCR-F §18.5 with a stopwatch attached.
- **Non-monotone dynamics.** Containment removes reachability; systems are shut down; accounts are disabled. Capability is lost, which is exactly the condition that breaks the monotone closure argument (see #47) and makes the outcome path-dependent.
- **Containment cost.** Disconnecting a segment stops the spread and stops the business. The defender is optimizing under a cost the attacker does not bear, and the decision threshold matters as much as the detection.

**The lens, stated plainly.** Every reducible question here belongs to another Lab. What is distinctively this Lab's is **the race**, and a race between two timed mechanisms with delayed observation is one of the cleanest irreducibility structures available: the outcome depends on the interleaving, and the interleaving depends on timing that no static analysis contains.

That makes this Lab, more than #47, the natural home for the **defender** half of Family H. #47 asks what an attacker can reach. This one asks whether anyone stops them in time.

## What a Cell would carry

A host or system: encrypted state, reachable-from-deployment state, backup role, detection instrumentation present, and operational status. Bounded scalars; §13.1 met.

**Layout is a Network or Identity World**, inherited from #47 and #48 — Connections are what the deploying credential can reach.

The distinctive requirement: **two mechanisms with independent clocks**. Encryption spreads; detection and response act. Neither is a modifier on the other; they are separate processes racing. That is DEC-1 in its clearest and least avoidable form — this Lab cannot be expressed as a single mechanism without discarding the phenomenon — and it needs DEC-3 for the observation delay that makes the defender's picture stale.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, and I would rank it third in Family H behind #48 and #47 — with the important qualification that it is blocked on two open decisions and cannot be built first.**

The distinctive value is clear: this is the Lab where the **defender is a mechanism rather than a parameter**. Everywhere else in Family H the defence is a static property of the environment — segmentation exists or it does not. Here the defence is an actor with its own timing, its own information delay, and its own costs, racing the attack. That is a genuinely different question and it is the one operators care about, because they cannot change what an attacker can reach nearly as easily as they can change how fast they respond.

**The upside worth being excited about.** The **response-time threshold** is a real, unanswered, decision-relevant question: how much faster does detection have to be, for a given environment's reachability structure, to change the outcome? Organizations spend heavily on detection and response, largely without evidence about where the threshold sits or how it depends on their topology.

That question is a Study: hold the spread mechanism constant, vary detection latency and containment aggressiveness, and measure the encrypted fraction across many runs. The output is a curve, not a prediction, and a curve about *classes* of environment can be published without touching any real network. That is the position paper's framing applied cleanly.

The negative space is valuable too: "these containment strategies never reduced impact under any spread mechanism we tried" would be a genuinely useful finding, and no vendor publishes strategies that failed.

**The challenges, in order of severity.**

1. **Blocked on DEC-1** — the attacker and the defender are unambiguously two mechanisms, and this Lab is meaningless without both.
2. **Blocked on DEC-3** — the defender's stale picture is the mechanism, not a refinement.
3. **Reachability is inherited**, so this Lab's realism is bounded by #47's, which is bounded by topology data nobody has.
4. **Real incident data is not reproducible** — narratives, not measurements, and the counterfactual is never available.
5. **Highest commercial over-claiming pressure in the catalog.** Ransomware sells; a plausible-looking containment model would be marketed instantly, and the catalog explicitly warns about this family (§30.7).
6. **F-20 applies**: studying attacker timing never justifies a more permissive execution surface (§18.4, DEC-16).

## Non-claims

This Lab does not assess ransomware risk or resilience for any real organization, does not evaluate detection or response products, does not predict attacker behaviour, and produces nothing suitable for security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
