# 47. Lateral Movement Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #47, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

An attacker holding one host reaches another, then another. Each hop is individually unremarkable — a credential valid in more than one place, a machine account trusted further than intended, a delegation that composes with an inheritance nobody drew together. What emerges is a route from a worthless foothold to something that matters, which no single configuration decision created and no component contains.

## What the domain already knows

This is not virgin ground, and a Lab that does not know the prior art will reinvent it badly.

**Attack graphs** are a twenty-five-year literature. The early model-checking formulation (Sheyner, Wing, and colleagues, early 2000s) generated attack graphs by exploring reachable system states — and ran directly into **state-space explosion**, which is the security field's own published encounter with computational irreducibility. The field's response was a specific, documented retreat: **the monotonicity assumption** (Ammann, Wijesekera, Kaushik, 2002) — an attacker never loses a capability once gained. Under monotonicity the problem stops being a state exploration and becomes a *least-fixed-point closure*, computable in polynomial time. Modern practice runs on this. BloodHound and its descendants compute shortest paths to Domain Admin over an identity graph in milliseconds; that is a shortcut, and it works.

**Network epidemiology** supplies the other half. Worm propagation analyses (Code Red and Slammer, Staniford–Paxson–Weaver and successors) fit epidemic curves to real events. Epidemic thresholds on scale-free contact graphs (Pastor-Satorras and Vespignani, 2001) show that the topology — not the per-hop probability — dominates whether spread takes off. Both are analytic shortcuts, and both are about *populations*, not routes.

## Where the shortcut holds, and where it breaks

**This is the whole argument for the Lab, and it is unusually clean.**

**Reducible.** Static reachability over a fixed graph is transitive closure. Monotone credential accumulation — you only ever gain — is a fixpoint computation. Aggregate spread through a random contact graph has a threshold formula. If the question is "what is reachable from here, ever, assuming nothing is taken away," the answer is a graph query and SCR has nothing to add. This must be said out loud, early, because it describes most of what the commercial tooling in this space does, and it does it well.

**Irreducible.** Every assumption the shortcut needs is a real-world falsehood, and each falsehood restores irreducibility:

- **Non-monotonicity.** Detection and response *remove* attacker positions. Credentials rotate; sessions expire; an EDR kills a process. The moment capability can be lost, the fixpoint argument collapses and the reachable set becomes path- and timing-dependent.
- **Order dependence.** Harvesting credentials on arrival changes the edge set. Under monotonicity, order does not matter — that is precisely what monotonicity buys. Without it, which host you take first determines what you can take at all.
- **Concurrency and staleness.** Defensive tooling sees the environment as it was. An attacker operating inside that gap is not an edge case; it is a large fraction of the phenomenon, and it is exactly the observation-delay capability SCR-F §18.5 places on the Reactor.
- **Two adapting mechanisms.** Attacker movement and defender response are a coupled system. Neither one's outcome is a property of the topology alone.

**The lens, stated plainly.** The security field *knowingly traded away* the non-monotone, timing-dependent, adaptive parts of this problem in exchange for tractability, and has been open about it. That trade is the gap SCR could occupy: not competing with attack-path tools on reachability, but studying **what the monotonicity assumption throws away** — under what local rules does a non-monotone, response-aware execution reach conclusions a monotone closure does not? That is a real, unanswered, checkable question, and it is not a question a graph query can ask.

## What a Cell would carry

A host, or an identity, or an account — and which of the three is an open question, not a detail. Candidate bounded scalars: whether the attacker holds this position, privilege level, credentials cached here, detection state, hardening.

The §13.1 ceiling bites harder here than anywhere in Family A. An attacker's *accumulated knowledge* — what they carry, where they have been, what they have learned about the environment — is naturally unbounded and is exactly the state that drives behaviour. If the Lab needs open-ended memory to be itself, §13.1 says it fails fit. Whether the useful questions survive a bounded-state formulation is the single most important thing a fit review must test.

## Layout

**Not a grid, and this is the catalog's flagship test of that (§15).** Network World (Connections are reachability) and Identity World (Connections are trust, role, delegation, inheritance) produce different models of the same incident, and the interesting paths are frequently the ones where they disagree. Distance metaphors for trust are a common habit and a misleading one; since the World owns its Layout (§14), there is structurally no slot for a trust world governed by spatial distance.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Ungraded, most likely to be over-claimed, and — with one specific framing — the most intellectually defensible entry in Family H.**

The naive framing ("simulate attackers spreading across a network") is weak. It duplicates attack-path tooling on the part that tooling does well, depends entirely on a topology nobody has ground truth for, and renders a persuasive red path across a graph that says nothing about the real environment.

The strong framing is narrow: **SCR as an instrument for studying the failure modes of the monotonicity assumption**, on synthetic topologies where ground truth is constructed rather than discovered. That version does not need a customer's network, does not claim to find real attack paths, and asks a question the incumbents structurally cannot.

**The upside worth being excited about.** Segmentation is Study-shaped, not Run-shaped (catalog #55) — "which single connection defeats this division" is a Small-Change Test, and comparing a monotone closure's answer against a non-monotone execution's answer is a genuinely novel comparison. If SCR can show a class of topology where the two systematically diverge, that is a publishable security finding independent of whether SCR ever models a real network.

**The challenges, in order of severity.**

1. **Topology ground truth does not exist.** Enterprise trust relationships are famously undocumented. If Connections are wrong, every result is confidently wrong and the model cannot detect it. Synthetic topologies sidestep this and shrink the claim to match.
2. **"No path found" will be read as "secure."** It means no route in the modelled topology. This is the highest-consequence misreading in the catalog.
3. **The attacker is not a local rule.** A propagation rule explores; an adversary chooses by value and adapts. The Lab may describe path *existence* well while describing path *selection* badly, and must say which questions that permits.
4. **One tick has no calendar meaning.** Real intrusions are weeks of dwell punctuated by minutes of activity. Rate-of-spread claims are indefensible here (DEC-3).
5. **F-20 applies throughout.** Studying hostile behaviour never justifies a more permissive execution surface for generated code (§18.4, DEC-16).

## Non-claims

This Lab does not assess the security of any real environment, does not predict attacker behaviour, and produces nothing suitable for operational security decisions. It is ungraded, unreviewed, and may fail its fit review (§30, §41, §43).
