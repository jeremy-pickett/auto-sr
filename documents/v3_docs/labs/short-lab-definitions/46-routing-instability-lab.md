# 46. Routing Instability Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #46, Family G · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

The internet's inter-domain routing runs on BGP, in which each autonomous system tells its neighbours which destinations it can reach and through what path, and each recipient applies its own local policy to decide which announcement to believe and whether to pass it on. There is no central authority and no global view. Every router's picture of the internet is assembled from what its neighbours told it, some time ago.

When something changes — a link fails, a policy is edited, a prefix is withdrawn — the news propagates hop by hop. During propagation, different parts of the network hold inconsistent views, and routers may try a succession of alternative paths before settling. This **path exploration** can take minutes, during which traffic is dropped or looped.

Sometimes it does not settle. Certain combinations of local policies, each individually sensible, have no consistent global solution, and the network oscillates indefinitely — routes flapping between alternatives forever.

## What the domain already knows

**The instability has been proven, not merely observed, and this is the domain's most important fact for SCR's purposes.** Griffin, Shepherd, and Wilfong formalized BGP policy routing as the **Stable Paths Problem** and showed that a system of local policies may have no stable solution, may have multiple, and that **deciding whether a given policy configuration has a stable solution is NP-hard** *(around 2002; attribution from memory, verify)*. Their "Bad Gadget" is a small, concrete configuration of three or four autonomous systems whose policies guarantee permanent oscillation.

This is a rare and valuable thing: **the domain has a hardness theorem sitting exactly where the irreducibility is.** Not "we cannot compute it in practice" but "deciding it is NP-hard," proven.

**Convergence delay is measured.** Labovitz and colleagues showed around 2000 that BGP convergence after a withdrawal can take minutes rather than seconds, because routers explore many alternative paths in sequence before concluding a destination is unreachable, and that the delay grows with the network's path diversity *(attribution from memory, verify)*.

**Sufficient conditions for stability are known.** The Gao–Rexford conditions — if every autonomous system follows the customer-provider-peer valley-free policy hierarchy, the system converges — give a practical guarantee that most of the internet approximately satisfies. This is the reducible answer that makes the internet work despite the hardness result.

**Measurement infrastructure is excellent and public.** RouteViews and RIPE RIS collect BGP announcements from hundreds of vantage points continuously and have done for over twenty years. Every route flap, leak, and hijack is in the archive.

## Where the shortcut holds, and where it breaks

**Reducible.** Whether a policy configuration satisfying the Gao–Rexford hierarchy converges — yes, by theorem. Shortest-path routing without policy — Dijkstra. Steady-state route selection given a converged state. Reachability given a routing table. Detecting a specific known misconfiguration pattern.

**Irreducible, and provably so:**

- **Whether an arbitrary policy configuration converges.** NP-hard to decide. This is not a modelling limitation; it is a theorem about the problem.
- **The transient.** Even when a configuration converges, the path it takes — which routes are tried, in what order, how long it takes, what traffic is lost — depends on message timing and ordering across the network. The same configuration converges differently depending on which router heard what first.
- **Interaction of independently-edited policies.** Thousands of organizations edit their policies without coordination or visibility into each other's. Whether the composition remains stable is exactly the undecidable-in-practice question, and nobody can check it.
- **Route leaks and their blast radius.** An autonomous system announcing routes it should not can redirect large fractions of internet traffic, and how far the leak spreads depends on the policies of everyone downstream.

**The lens, stated plainly.** This Lab has the catalog's most rigorous irreducibility credential: **a published NP-hardness result covering exactly the question of interest.** Where wildfire has "the closed form breaks down near the percolation threshold," routing has "deciding this is NP-hard, here is the proof, and here is a four-node counterexample."

It also has the catalog's cleanest instance of message-passing asynchrony being the mechanism rather than a complication. Routers act on what neighbours told them, when they told them. Different orderings give different transients. That is SCR-F §18.5's observation staleness as the load-bearing element, and it is not optional here.

## What a Cell would carry

An autonomous system or router: its currently selected route to each destination of interest, the routes its neighbours have announced, its local preference policy, and pending announcements. Bounded — if the number of tracked destinations is bounded and small, which it must be. §13.1 is met with that restriction, but the restriction is substantive: real routers hold nearly a million prefixes, and a Lab studying one prefix at a time is studying a different thing than the operational reality.

**Layout is a Network World**, correctly, and the topology is public: the autonomous-system-level graph is inferred continuously from BGP data and published.

The mechanism is **genuinely local and genuinely known** — the BGP decision process is specified in an RFC, and each router applies it to information from its neighbours only. Like #45, this is a domain where the local rule is not an abstraction of the real mechanism; it *is* the real mechanism, written down by humans, running in production.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible to strong — and intellectually the most rigorous entry in the catalog. I would rank it second in Family G behind #45, and above most of Family H.**

The distinguishing assets: a proven hardness result at the exact point of interest; a specified, local, human-written mechanism; a public topology; twenty years of public measurement data; and asynchrony as the load-bearing element rather than an inconvenience.

The catalog's own framing — "genuinely a network domain with a protocol attached, and whether the protocol survives abstraction is the whole question" — is the right question. My answer is that it *might*: BGP's decision process is short enough to express as a local rule, and the Stable Paths Problem literature already treats it that way successfully.

**The upside worth being excited about.** The genuinely exciting thread is **policy composition**. Nobody can check whether the internet's current global policy configuration is stable, because nobody can see all the policies and the decision is NP-hard anyway. But asking "which *classes* of local policy, composed at scale, produce oscillation, and how does the probability of a Bad Gadget appearing scale with network size and policy diversity" is a statistical question about mechanism space — and it is precisely what a corpus of many generated local policies, each run to convergence or not, would answer.

That is a real, open, unanswerable-by-analysis question with a large practical stake, and it is not being systematically attacked because doing so requires running many mechanisms.

The other attraction is pedagogical for the platform: this Lab makes **stale observation** unavoidable and therefore forces DEC-3 to be exercised properly rather than approximated away.

**The challenges, in order of severity.**

1. **Asynchronous message passing is the mechanism**, so this Lab is blocked on DEC-3 in a hard way — lockstep would model a protocol that does not exist.
2. **Protocol fidelity is all-or-nothing.** BGP's decision process has many tie-breaking steps; a simplified version may be stable where the real one is not, or vice versa, and the whole point is the fine structure of policy interaction.
3. **Scale mismatch.** Real routing tables hold hundreds of thousands of prefixes; a bounded-state Cell handles a handful.
4. **Internet-infrastructure sensitivity.** Work that identifies destabilizing policy configurations has dual-use character and should be handled with the same care as Family H (F-20).
5. **Small expert audience**, though a highly capable and well-instrumented one.

## Non-claims

This Lab does not model the real internet, does not assess routing stability for any network or operator, does not identify vulnerabilities in deployed systems, and produces nothing suitable for operational or security decisions (§41, §43).
