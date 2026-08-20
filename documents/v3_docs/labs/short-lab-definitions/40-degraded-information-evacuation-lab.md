# 40. Degraded-Information Evacuation Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #40, Family F · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §18.5, §29, §30, §41; F-9, F-17
**Fit review (§30):** not performed

---

## The phenomenon

Every evacuation model assumes people know where to go. Real evacuations frequently fail that assumption. Signage is obscured by smoke or by the crowd itself. An exit is locked, or opens onto a blocked stairwell, and the people at the front discover this while the people behind keep pushing. An announcement is made in one language, or is inaudible, or arrives after people have already committed to a route. Someone who knows the building leads a group the wrong way with complete confidence.

What people actually do is well documented and it is not what models assume. They **leave the way they came in**, even when a nearer exit exists. They wait for confirmation before moving, and the waiting is often the largest component of total evacuation time. They follow others. They stay with their group and will not separate.

So the variable that determines the outcome is not the geometry of the building. It is **what each person believes about the building, and when they came to believe it.**

## What the domain already knows

**The behavioural findings are established and they contradict the folk model.** Fire safety research has documented for decades that the dominant delay in real evacuations is **pre-movement time** — the interval between an alarm and people actually starting to move — and that it is driven by information seeking, ambiguity, and social confirmation rather than by panic. Panic is largely a myth in the crowd-science literature; people are more cooperative and slower than models assume, not faster and more selfish.

**Exit choice is well studied and the result is consistent:** familiarity dominates proximity. People use the entrance they know.

**Information propagation through a crowd is treated as social contagion** in some models — a person who knows spreads the knowledge to neighbours — which is a local mechanism, and it has been combined with movement models.

**Reference data is thin and structurally hard to get.** You cannot run a controlled experiment on an evacuation with degraded information: the ethics of misleading participants about a fire are prohibitive. What exists is post-incident investigation, evacuation drill data (which lacks the information failure), and a small number of virtual-reality studies.

## Where the shortcut holds, and where it breaks

**Reducible.** Almost nothing that matters. Total evacuation time if everyone knows the nearest exit and moves immediately is a flow calculation (#36). Add realistic pre-movement time distributions and it is still arithmetic. That is the entire reducible core, and it is the model of a building nobody evacuates.

**Irreducible.** Everything else, and unusually the whole Lab lives here:

- **Belief propagation coupled to movement.** What a person knows depends on who they have been near, which depends on where they moved, which depends on what they knew. The two processes are mutually dependent and cannot be separated.
- **Stale information.** Someone told five minutes ago that the north exit is clear acts on a fact that is no longer true. The gap between the world's state and an agent's model of it is the mechanism, not an approximation — and it is precisely SCR-F §18.5's observation staleness.
- **Cascading commitment.** Once a stream of people commits to a route, later arrivals follow it because it looks like knowledge. A wrong choice by a few people early is amplified into a wrong choice by many.
- **Discovery of blockage.** The front of a queue learns an exit is blocked; the information must travel backward through a crowd moving forward. Whether it arrives before the corridor packs is a race.
- **Partial information asymmetry.** Different people know different, partly-wrong things, and the aggregate outcome depends on the distribution of beliefs, not on any average.

**The lens, stated plainly.** This is the only Lab in the catalog whose **entire content is irreducible**, and the reason is structural: the state that drives behaviour is *what agents believe*, which is by construction different from the state of the world. There is no closed form for a system in which every participant is acting on a different, delayed, partly-false model of the same environment.

It is also, and this matters for the platform, **the catalog's flagship consumer of observation staleness (§18.5)**. Nearly every other Lab treats staleness as a complication; here it is the phenomenon. If DEC-3 resolves in a way that supports declared observation delay, this Lab is where that capability earns its existence.

## What a Cell would carry

This Lab strains the Cell abstraction more than most in Family F, and the strain is worth stating clearly.

A floor cell carries occupancy, hazard state, and signage. But the load-bearing state belongs to the **occupant**: what they believe about exits, when they learned it, who they are with, whether they have started moving. That is per-person state riding on a moving participant, not per-location state.

**§13.1 is the binding constraint here.** An agent's belief about the building is naturally an unbounded structure — a mental map. Bounded belief (a small set of "exit X is open / blocked / unknown" flags with timestamps) is expressible and is probably enough for the interesting questions, but it is a substantive modelling commitment and the fit review must decide whether the useful questions survive it. This is the same ceiling problem as attacker knowledge in #47, and the two Labs should be reviewed together.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible on interest, weak on validation, and the most architecturally valuable entry in Family F.**

The domain case is genuinely interesting and genuinely underserved: the models used in fire safety engineering mostly assume informed occupants, the field knows this is unrealistic, and the alternative is hard to build. But the reason it is underserved is partly that **it cannot be validated**, and that will not change. You cannot ethically run the experiment, and post-incident investigation gives you one data point with no counterfactual.

A Lab that cannot earn accuracy (§30.6) is in a weak position no matter how interesting it is.

**The upside worth being excited about.** Two things, one domain and one platform.

The domain thread: the finding that would matter is a *negative* one. If, across many candidate information-propagation and route-choice mechanisms, a particular signage or announcement strategy robustly fails, that is useful even without calibration, because it identifies a fragility rather than predicting an outcome. Robustness findings survive weak calibration better than predictions do.

The platform thread is larger. This Lab is where **belief-versus-world separation** gets built, and that separation is needed by #47, #48, #52, #55, and arguably #50 — the entire non-monotone half of Family H. Building it here, on a domain where the mechanism is sympathetic and the stakes are pedagogical rather than commercial, is a much better place to make the architectural mistakes than in the security Labs where the mistakes would be embarrassing.

**The challenges, in order of severity.**

1. **Validation is structurally unavailable.** The experiment is unethical and the incidents are unrepeatable.
2. **Bounded belief may not survive contact with the interesting questions** (§13.1), the same ceiling problem as #47.
3. **Movement plus information plus hazard is at least three mechanisms** — DEC-1, and the catalog already flags this entry as blocked on it.
4. **Depends on DEC-3** for observation staleness, which is undecided.
5. **Life-safety credibility hazard**, inherited from #36 and made worse by the absence of calibration — an uncalibrated model of a fatal scenario is the worst combination in the catalog for §30.7.

## Non-claims

This Lab does not assess evacuation from any real building, does not evaluate signage, alarm, or emergency communication strategies, and produces nothing suitable for any life-safety decision (§41, §43).
