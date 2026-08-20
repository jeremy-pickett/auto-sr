# 47. Lateral Movement Lab — Lab Definition

**Document class:** Lab Definition (pre-fit) · **Status:** draft
**Catalog entry:** SCR Lab Catalog v0.1 #47, Family H — Information security
**Standing:** **ungraded.** Family H carries no verdict from *A Card Catalog for Emergence* v0.1, and the catalog records an explicit expectation that these entries may grade weak if forced onto a lattice (Catalog §0, gap 1). Nothing below should be read as evidence that this Lab fits.
**Cites:** SCR-F v0.2 §11, §13.1, §15, §18.5, §30, §41; F-9, F-17, F-20
**Fit review (SCR-F v0.2 §30):** not performed

> **This document does not establish fit, and this Lab is ungraded.** It is also the entry most likely to be over-claimed, because it is the most commercially attractive one in the catalog. The catalog is direct about this: if Family H grades weak, that is a finding about SCR's boundary and should be published as one (Catalog, open item 2). This document is written to make that outcome sayable, not to argue against it.

---

## The phenomenon

An attacker who has compromised one host moves to another, then another. Each hop is individually unremarkable — a credential that works in more than one place, a trust relationship between machines, a service account with wider reach than anyone intended, a path that exists because two reasonable configurations compose. What emerges is a route from a low-value foothold to something that matters, which nobody designed and no single configuration decision created.

The interesting property is that the route is not visible in any component. It is a consequence of the whole, and finding it generally means traversing it.

## Why a local mechanism is a candidate abstraction here

The case is genuinely arguable, which is different from being established. Each hop *is* local: an attacker on host A reaches host B because a specific relation between A and B permits it. Reachability, credential validity, and trust are edge properties, and movement is the repeated local application of "can I use what I have here to arrive there."

The case against — which a fit review must take seriously rather than dismiss (§30.1) — is that a real attacker is not a local mechanism. They hold global knowledge, choose targets by value, and adapt. A cell-local propagation rule may describe *what paths exist* while badly misdescribing *which path is taken*. Whether that distinction matters depends on the question being asked, and stating which questions this Lab can and cannot address is the fit review's job.

## What a Cell would carry

A host, or an identity, or an account — and **which of those it should be is itself an open question**, not a detail. Candidate declared scalars:

| Property | Meaning in this domain |
|---|---|
| `compromised` | whether the attacker holds this position |
| `privilege` | the level of access held here |
| `credentials_present` | what is cached or usable from this position |
| `detected` | whether defensive tooling has noticed |
| `hardened` | resistance to a given technique |

These are bounded primitive scalars and appear to clear the §13.1 ceiling. But the ceiling has a sharper edge here than in a spatial Lab: an attacker's *accumulated knowledge* — what they have learned, what they are carrying, where they have already been — is naturally unbounded, and it is exactly the state that determines behaviour. If this Lab needs open-ended memory to be itself, §13.1 says it fails fit. Whether the useful questions survive a bounded-state formulation is unresolved and is the single most important thing a fit review should test.

## Layout and Connections

**Not a Grid World.** This is the catalog's flagship test of non-grid Layouts (Catalog #47), and forcing it onto a lattice is the named failure mode to watch for (Catalog, Family H preamble).

The honest arrangement is **Network** or **Identity** (§15), and which one is a real question rather than a labelling preference:

- **Network World** — Connections are reachability. Movement follows what can talk to what.
- **Identity World** — Connections are trust, role membership, delegation, inheritance. Movement follows what can *authenticate* to what.

These produce different models of the same incident, and the interesting paths are frequently ones where the two disagree — a host unreachable by network but reachable by an inherited role, or the reverse. Whether a single World can carry both relations, or whether they are separate Worlds compared under a Study, touches **DEC-8** (World storage) and is not resolvable here.

Since the World owns its Layout (§14), there is no slot for a trust-relationship world governed by spatial distance. That is a helpful constraint in this Lab specifically, because distance metaphors for trust are a common and misleading habit.

## What one step would mean

Genuinely unclear (§30.4), and the clarity problem is not cosmetic. Real intrusions unfold over weeks with long dwell periods punctuated by rapid activity. A uniform step is a poor representation of that, and a rate of spread measured in steps has no defensible translation into calendar time.

This Lab is also a likely consumer of **observation staleness** (§18.5): defensive tooling sees the environment as it was, not as it is, and an attacker operating inside that gap is not an edge case — it is a substantial part of the phenomenon. That capability is World- and Reactor-owned; a Plugin proposing effects at a future offset is proposing a write like any other (§6, F-9). The scheduling contract is **DEC-3**'s and is not answered here.

## Candidate mechanisms

Illustrations of shape only:

- move to a connected position when held credentials satisfy that position's requirement
- harvest credentials on arrival, expanding what subsequent hops permit
- privilege escalating locally when a position yields a stronger credential than the one used to reach it
- detection probability accumulating with activity, with response removing positions

The second is where irreducibility bites hardest. Each hop changes what the next hop can do, so reachability is a function of the path taken rather than a property of the graph. There is no evident shortcut to "which positions are reachable" that does not amount to traversing the possibilities — which is the property that makes this a candidate for an execution-based instrument rather than a static analysis, and equally the property that makes results sensitive to starting assumptions.

## What would have to be observed

Candidate Lab-owned Readers (§11 — these names must never appear in core documents):

- whether a designated position was reached, and in how many hops
- the set of positions reachable from a given foothold
- how many distinct paths reach a target, and whether they share a common edge
- whether privilege strictly increased along the path
- how far movement proceeded before detection

## Where this would mislead

The §30.7 question, and this Lab carries the catalog's highest deception risk.

A rendered graph with a red path spreading across it is extraordinarily persuasive and says nothing about whether the modelled topology matches the real environment. Three specific hazards:

- **Topology error dominates everything.** If the Connections are wrong — and enterprise trust relationships are famously undocumented — every result is confidently wrong. The model cannot detect this.
- **Absence of a path is not evidence of safety.** A model that finds no route has found no route *in the modelled topology*, which is a much weaker statement and will not be heard as one.
- **Attacker rationality is unmodelled.** A local propagation rule explores; an adversary chooses. Results describing what is reachable may be read as predictions of what will happen.

§F-20 applies throughout: hostile conditions are explicit experimental capabilities, and studying attacker behaviour never justifies a more permissive execution surface for generated code (§18.4).

## Established tools

Attack-path analysis, identity-graph tooling, and adversary emulation already exist and operate on real environment data (§30.8). This Lab's plausible — untested — complementary position is mechanism supply: asking which *classes* of local permission rule produce unintended reachability, rather than mapping a specific customer's network. A fit review must state that boundary explicitly, and any commercial positioning that leans on this Lab before the review exists is exactly what the catalog warns against.

## Open decisions bearing on this Lab

- **DEC-3 (temporal semantics)** — observation staleness above.
- **DEC-8 (World storage)** — whether Network and Identity relations coexist in one World.
- **DEC-16 (security isolation)** — the execution boundary for adversarial Labs.
- **DEC-1 (mechanism composition)** — attacker movement plus defender response is arguably two mechanisms.

None is resolvable in this document (§36.6, F-22).

## The nine questions this Lab owes

1. **Domain fit** — does local propagation describe path *existence* well enough to be useful despite describing attacker *choice* badly?
2. **World fit** — is a Cell a host, an identity, or an account, and does bounded state (§13.1) survive the loss of attacker memory?
3. **Mechanism fit** — which techniques are expressible as local rules, and which require global reasoning?
4. **Time fit** — what does one step mean when dwell time dominates the real phenomenon?
5. **Evidence fit** — are reachability and path-count reproducibly measurable, and what does "reachable" mean when it is path-dependent?
6. **Accuracy** — which documented intrusions or synthetic environments serve as reference cases?
7. **Failure boundaries** — how is "no path found" prevented from being read as "secure"?
8. **Comparison** — what do existing attack-path tools do better, and where is SCR complementary rather than duplicative?
9. **Transfer limits** — what validation before any retrieved mechanism informs a real security decision?

## Non-claims

This Lab does not assess the security of any real environment, does not predict attacker behaviour, and produces nothing suitable for operational security decisions. It is ungraded, unreviewed, and may fail its fit review (§30, §41, §43).
