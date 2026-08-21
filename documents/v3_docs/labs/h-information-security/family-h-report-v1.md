# Family H — Information security
## Lab Knowledge Report v1

### Lateral Movement · Identity and Privilege · Prompt Injection · Agent Memory · Sensitive Data Diffusion · Ransomware Spread · Patch Propagation · Worm and Botnet · Segmentation and Containment · Software Supply Chain

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/h-information-security/family-h-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family H (entries 47–56)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md`
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, LAB-4 (no relaxation for hostile subjects), LAB-6/LAB-7
**Supersedes:** first-pass briefs 47–56 in `../short-lab-definitions/`, and `47-lateral-movement-lab.fit-frame.md`
**Responds to:** `../../critiques/SCR_Labs_51-60_Critique_v0.1.md` (entries 51–56)
**Cites:** SCR-F v0.2 §11, §15, §18.4, §18.5, §20.1, §25.3, §29, §30, §41–43; F-9, F-14, F-17, **F-20** · LAB-4 to LAB-8, LAB-16 · DEC-1, DEC-3, DEC-16, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

> ## ⚠ Partial critique coverage
>
> Entries **51–56** are reviewed against `SCR_Labs_51-60_Critique_v0.1.md`. Entries **47–50 have no critique** — `SCR_Labs_41-50_Critique` does not exist. Their assessments are first opinions and should be revised when it lands.

> ## Security scope statement
>
> **F-20 applies throughout: hostile conditions are explicit experimental capabilities, and studying attacker behaviour never justifies a more permissive execution surface for generated code** (§18.4, LAB-4, DEC-16).
>
> Nothing in this family assesses the security of any real environment, identifies attack paths in any organization, predicts attacker behaviour, or supports compliance or audit claims. **No mechanism-generation objective in this family may optimize propagation efficiency or offensive effectiveness.** The family is ungraded, and the catalog records an explicit expectation that these entries may grade weak if forced onto a lattice — **if they do, that is a finding about SCR's boundary and should be published as one.**

---

## What this family is for

Family H is the catalog's most commercially attractive family and its most over-claimable. Six findings organize it, and most are structural rather than per-Lab.

### 1. This is one World with several mechanisms, not ten Labs

Entries 47, 48, 52, 54, and 55 do not need different Worlds. They need **different mechanism packages and Studies over a shared enterprise-security World** containing hosts, identities, credential relations, network reachability, zones, management systems, backup roles, observation channels, and defensive controls. Then:

| Entry | Mechanism over the shared World |
| :--- | :--- |
| 47 Lateral Movement | Directed adaptive movement |
| 48 Identity and Privilege | Processes modifying trust and delegation edges over longer time |
| 52 Ransomware | Mass deployment racing defender response |
| 54 Worm | Autonomous self-propagation |
| 55 Segmentation | Small-Change Tests against those mechanisms |

**Lab is a semantic problem-space boundary; Plugin is a mechanism; a World template may be shared across Labs.** Do not duplicate a World merely because the interface has several Lab names.

### 2. Three mechanisms that must not be blended

A large portion of bad "cyber contagion" modelling comes from treating all three as epidemics:

- **Autonomous propagation** — each acquired position becomes a source of further spread under the same rule. *Worms.*
- **Directed adaptive action** — a mechanism selects among opportunities, accumulates state, and may change behaviour from what it learned. *Lateral movement.*
- **Coordinated deployment or control** — a coordinator addresses many positions directly. *Ransomware mass deployment, patch scheduling.*

These imply different World, Plugin, and Reactor semantics.

### 3. The family's first engineering deliverable is probably not a Lab

Five entries need a topology and none should depend on real customer networks. That argues for a **versioned synthetic enterprise reference World** with known ground truth, reproducibility, no customer data, no accidental real attack-path claims, direct mechanism comparison, and stable demonstrations — deliberately seeded with known traps: one hidden cross-zone management path, one expired credential, one delayed detection channel, one high-privilege shared service, one unreachable crown-jewel path.

> **This may be a better first Family H deliverable than any individual security Lab.**

### 4. Security visuals need provenance inside the frame

A luminous path to Domain Admin or an animated encryption wave looks operational even when it is synthetic, and both crop beautifully. For high-risk Views the rendered evidence should carry — not merely sit beside — synthetic/reference World status, Study identifier, mechanism version, and non-operational status. **This is evidence labelling, not decorative watermarking**, and it is the lesson already learned from public-health visualization.

### 5. Question fit, not just Lab fit

Every entry here has supported and unsupported question classes, and the distinction does more work than a single verdict:

| Entry | Fits | Does not add value |
| :--- | :--- | :--- |
| 51 Sensitive data | Deletion versus re-derivation feedback | Copy-count prediction |
| 52 Ransomware | The timed response race | Reachability |
| 53 Patch | Reboot-deferral feedback | The propagation curve |
| 54 Worm | Segmented-propagation comparison | The historical S-curve |
| 55 Segmentation | Timed containment Study | Static bridge and min-cut |
| 56 Supply chain | Maintainer ecosystem evolution | Dependency closure |

### 6. Two anti-patterns this family names

**Operational difficulty is not irreducibility.** A domain is not a mechanism-supply opportunity merely because organizations cannot measure the real state. Simulation cannot repair missing observation.

**Same curve is not same mechanism.** Outcome resemblance never establishes mechanism-family identity; that requires correspondence in the causal transition structure, not merely matching Reader output.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 47 — Lateral Movement *(no critique coverage)*

| | |
| :--- | :--- |
| **Role** | Directed-adaptive-action mechanism over the shared World |
| **Standing** | Ungraded |
| **Falsifiable question** | Under what local rules does a non-monotone, response-aware execution reach conclusions a monotone closure does not? |
| **Mechanism fit** | Conditional — see the ceiling problem |
| **Evidence fit** | **Weak** — topology ground truth does not exist |
| **Question fit** | Narrow and real under the reframing |
| **Visual credibility** | Class 1 |

**The phenomenon.** An attacker holding one host reaches another, then another. Each hop is unremarkable — a credential valid in more than one place, a machine account trusted further than intended, a delegation composing with an inheritance nobody drew together. What emerges is a route from a worthless foothold to something that matters, which no component contains.

**The established shortcut, and the field's documented retreat.** Early model-checking attack graphs ran into state-space explosion — the security field's own encounter with computational irreducibility. **Ammann, Wijesekera and Kaushik (2002)** escaped it with an explicit **monotonicity assumption**: the precondition of an exploit is never invalidated by the successful application of another, so **the attacker never needs to backtrack**. That reduced the computational cost to polynomial [1], and modern practice runs on it — attack-path tools compute shortest paths over an identity graph in milliseconds.

**Reducible.** Static reachability over a fixed graph. Monotone credential accumulation — a fixpoint computation. This describes most of what the commercial tooling does, and it does it well.

**Irreducible.** Every assumption the shortcut needs is a real-world falsehood, and each restores irreducibility. **Non-monotonicity** — detection and response *remove* positions, credentials rotate, sessions expire — collapses the fixpoint argument. **Order dependence**: harvesting credentials on arrival changes the edge set, and under monotonicity order does not matter, which is exactly what monotonicity buys. Concurrency and staleness. Two adapting mechanisms.

**The reframing that makes it defensible.** Not competing with attack-path tools on reachability, but studying **what the monotonicity assumption throws away** — on synthetic topologies where ground truth is constructed rather than discovered. That version needs no customer network and asks something a graph query structurally cannot.

**The ceiling problem, shared with entry 40.** An attacker's accumulated knowledge is naturally unbounded and is exactly the state driving behaviour. If the Lab needs open-ended memory to be itself, §13.1 says it fails. **Fit-review this together with Degraded-Information Evacuation** — they share the bounded-belief question.

**Assessment.** *(first opinion, no critique review, no standing)* Second-strongest in the family under the narrow framing. Three standing hazards: topology ground truth does not exist and the model cannot detect its absence; **"no path found" reads as "secure"** when it means *no route in the modelled topology*; and a propagation rule explores while an adversary chooses.

---

## Lab 48 — Identity and Privilege *(no critique coverage)*

| | |
| :--- | :--- |
| **Role** | **Strongest in the family** — generative process Lab |
| **Standing** | Ungraded |
| **Falsifiable question** | Which delegation practices are self-limiting, and which compound into unintended privilege over simulated years? |
| **Mechanism fit** | Good, but **requires dynamic Connections** |
| **Evidence fit** | Synthetic only; real directory data is confidential |
| **Question fit** | Genuinely unclaimed |
| **Visual credibility** | Class 1 |

**The phenomenon.** Permission accumulates rather than being granted. A person joins a team and inherits its role; the role was granted access for a project that ended; a service account can manage group membership so an automation works; a group was nested inside another by someone who has left. Nobody decided the marketing contractor should be able to reset the finance administrator's password. **The dangerous permission is in no record** — every individual grant is documented, the path through them is not.

**The foundational result, stated precisely.** Harrison, Ruzzo and Ullman (1976) formalized the access matrix and analyzed safety — *can this subject ever obtain this right*. Their finding is that the model has extremely weak safety properties: **different natural formulations of the safety problem are NP-complete or undecidable**, and safety is undecidable for most policies of practical interest [2]. *(The first pass stated a flat "undecidable"; the precise claim is that it depends on the formulation, and restricted models such as Take-Grant recover decidability deliberately.)*

**The entire practical field is a response to that result.** Restricted models were developed to recover tractability, and every deployed authorization system is a point on that trade-off curve.

**Reducible.** Static reachability over a permission graph. Shortest path to a target principal. Effective permissions at a moment. Whether a restricted policy grants an action — decidable, and solvers do it.

**Irreducible.** **Rights that create rights** — the HRU result bites where commands can grant the ability to grant, and a principal who can modify group membership can grant themselves what that group has, including possibly more ability to modify membership. Time-varying permission, where a path that does not exist today existed for six hours last Tuesday. Non-monotonicity. **Emergence of dangerous composition** as an organization grows.

**The reframing.** Not *find attack paths in this environment* — that duplicates shipping products badly on data nobody will share. Instead: **generate synthetic organizations under candidate delegation mechanisms, run them forward for simulated years, and measure how unintended privilege paths accumulate.** Security guidance here is largely folklore — avoid nested groups, limit service accounts, review access quarterly — asserted without evidence about how much each matters.

**The architectural requirement.** **The mechanism modifies the World's Connections.** A principal exercising the right to add a member creates an edge. That is the same dynamic-topology need as entries 18, 56, and 58 — and here it is the mechanism that makes the domain's safety problem hard in the first place. A platform that cannot express a mechanism creating Connections cannot express this Lab.

**Assessment.** *(first opinion, no critique review, no standing)* **Strongest in Family H.** The HRU result gives a principled reason for the platform to exist here: when the general question is undecidable, *run it and see* is not a fallback but the only remaining method, and the field's own literature says so.

---

## Lab 49 — Prompt Injection *(no critique coverage)*

| | |
| :--- | :--- |
| **Role** | Contamination-on-a-trust-graph; **substrate ages faster than generalization** |
| **Standing** | Ungraded; I would grade it **weak** |
| **Falsifiable question** | Given a per-hop survival probability, does contamination die out or persist on a given agent trust topology? |
| **Mechanism fit** | **Poor** — the per-hop mechanism is a text transformation |
| **Evidence fit** | **None** — no documented multi-hop propagation with measurable rates |
| **Question fit** | Narrow under the branching reframe |
| **Visual credibility** | Class 1 — maximum over-claiming pressure |

**The phenomenon.** A model reads text and acts on it. When some text comes from a source the designers do not control, instructions embedded there can be followed as though they came from the operator. Propagation makes it a spread phenomenon: an agent that reads poisoned content writes a summary, files a ticket, updates a document — and that output becomes the next agent's input.

**Reducible.** The static data-flow question: which components can receive attacker-influenced content and which tools can they reach. That is reachability over a known graph, and it is exactly what the recommended mitigations are based on — assume injection succeeds and constrain blast radius.

**Irreducible in principle.** Multi-hop propagation through summarization, storage, and retrieval. Persistence and re-emergence from a shared store. Trust topology nobody drew. Amplification versus decay — a branching-process structure with a threshold.

**Why it grades weak, and the reason is a category the catalog now names.** **The substrate is non-stationary**: susceptibility to a technique is a property of a model version being actively reduced by its developers. Stated carefully — as the critique framing requires — historical evidence remains valid; **what decays is external validity.** For a platform built on permanent evidence, findings whose generalization has a months-long half-life are a poor investment.

Compounding it: **representation destroys the mechanism.** "Contaminated" as a scalar stands in for a text payload transformed at every hop, and whether an injection survives summarization is a property of the text and the model, not of a flag.

**The narrow salvage.** Framed as **contamination dynamics on agent trust topologies, parameterized by a survival probability nobody has to measure**, the Lab becomes stationary again — the topology is the subject and the model is a parameter. That is defensible, useful, and considerably less exciting than what people would want this Lab to be.

**Assessment.** *(first opinion, no critique review, no standing)* **Weak — an uncomfortable verdict for the most fashionable entry in the catalog.** Dual-use character is direct; publication discipline matters more than the technical risk suggests.

---

## Lab 50 — Agent Memory *(no critique coverage)*

| | |
| :--- | :--- |
| **Role** | Recursive-drift mechanism Lab; reflexive value |
| **Standing** | Ungraded; **weak-to-plausible** |
| **Falsifiable question** | Does a shared store under retrieval-biased re-summarization converge, or concentrate on a shrinking set of increasingly confident claims? |
| **Mechanism fit** | Fair — better than 49 |
| **Evidence fit** | **None yet** — the phenomenon has not been measured |
| **Question fit** | Real and current |
| **Visual credibility** | Class 2 |

**The phenomenon.** Agents that persist keep notes, and when several share a store one agent's notes become another's context. Two failure modes. **Contamination**: something false enters and is retrieved as fact, possibly re-summarized and laundered of provenance so it acquires the appearance of independent confirmation. **Drift**: nothing hostile happens at all — repeated summarization compounds small distortions, facts lose qualifiers, uncertain claims become certain, and no single step was wrong. Both share a property: **the store outlives the interaction.**

**Reducible.** With provenance tracked, contamination is a lineage query — a graph traversal, solved technology. The static architectural question is reachability, as in 48 and 49.

**Irreducible.** **Drift without a source** — no item is contaminated; the distortion is distributed across many summarization steps, so there is nothing to trace back to. Provenance answers *where did this come from* and is silent on *how much was lost on the way*. Compounding through re-summarization, a fixpoint question. **Selective reinforcement** — frequently-retrieved items are re-summarized and re-stored more often, biasing the store's evolution toward what has already been retrieved, which is how a plausible falsehood becomes the store's most confident claim. Laundering of confidence.

**Why it is stronger than entry 49.** The drift mechanism is **more stationary than the injection mechanism**. Whether a summarization pipeline loses information per pass is a property of the pipeline's structure, not of which model runs it. Every model summarizes lossily; the interesting question is about the *architecture*, which changes on a slower clock. **Recursive drift remains a stronger AI mechanism question than per-technique prompt injection.**

**The reflexive value, worth stating.** SCR itself has a corpus, machine-written documents, and a stated worry (§36) about a mostly model-written tree drifting at the root. This Lab studies that mechanism. **A platform that models its own failure mode, honestly, is a stronger platform** — and the finding would apply to SCR's own tree as much as to anyone's.

**Assessment.** *(first opinion, no critique review, no standing)* **Weak-to-plausible**, and the better of the two AI entries. The retrieval-reinforcement feedback loop is specific, under-examined, answerable in the abstract, and would inform how these systems are built — a decision people are making now with no evidence.

---

## Lab 51 — Sensitive Data Diffusion

| | |
| :--- | :--- |
| **Role** | **Rejected fit** — the measurement-versus-dynamics boundary Lab |
| **Standing** | Ungraded; **reject as a standalone Lab** |
| **Rejection reason** | **Solved dynamics; the real problem is observation** |
| **Visual credibility** | Class 2 |

**The phenomenon.** A file is created; a link is shared; someone downloads and emails it; it is attached to a ticket, exported to a spreadsheet, backed up nightly, replicated, indexed, and synced to three laptops. Two years later nobody can say where it lives — which matters, because deletion-on-request presupposes knowing where the copies are.

**Why this is a rejection, and the reason is precise.** The brief separates two things the domain conflates:

- **The propagation dynamics** — largely branching-process and reachability mathematics. Expected copies after *n* generations, extinction probability, and the critical threshold at reproduction number one all have closed forms dating to the nineteenth century.
- **The actual operational problem** — incomplete instrumentation and discovery.

> **Simulation cannot repair missing observation.**

That yields a reusable rule with reach far beyond privacy:

> **A domain is not a mechanism-supply opportunity merely because organizations cannot measure the real state.**

The same caution applies to asset inventory, shadow IT, configuration drift, and undocumented dependencies. Some are excellent security problems. They are not necessarily SCR problems.

**The one genuine residue.** **Deletion racing re-derivation** — a copy deleted from a warehouse is regenerated by the pipeline that produced it. That non-monotone feedback loop is not covered by branching-process theory, has real regulatory consequence, and belongs in a Lab about pipeline lineage rather than about diffusion.

**Assessment.** **Reject as a standalone Lab. Preserve deletion-versus-re-derivation as a possible subproblem elsewhere.**

---

## Lab 52 — Ransomware Spread

| | |
| :--- | :--- |
| **Role** | **Timed attacker/defender race Lab** — later reference Study, not an early build |
| **Standing** | Ungraded; **plausible but blocked** |
| **Falsifiable question** | How much faster must detection be, for a given environment's reachability structure, to change the encrypted fraction? |
| **Mechanism fit** | Good — **but requires two mechanisms and delayed observation** |
| **Evidence fit** | Weak — incident narratives are not measurements and have no counterfactual |
| **Question fit** | The race only |
| **Visual credibility** | **Class 1 — highest commercial over-claiming pressure in the catalog** |

**The phenomenon.** An operator with access deploys encryption across everything reachable, as fast as possible, usually when nobody is watching — often through the organization's own management tooling, which is why it can cover thousands of machines in under an hour. The defender's problem is a race with an unforgiving clock: detection, decision, and containment must all fit inside the encryption window, and containment means disconnecting segments or shutting systems down, at large cost, under uncertainty, by people who have been woken up.

**Everything reducible here belongs to another Lab.** The extent question is transitive closure (entries 47, 48). Encryption throughput is arithmetic. Recovery time from backups is business-continuity planning. Epidemic framing fits badly: this is a **coordinated deployment**, not autonomous propagation — a directed single-source push over an access graph executed in minutes.

**What is distinctively this Lab's is the race.** Detection against propagation, where whether detection fires before the reachable set is exhausted depends on what triggers it, how quickly the signal reaches a human, and how long the human takes. **Containment under stale information** — the picture assembled during an incident is minutes old, so segmenting on it may cut the wrong link. **Non-monotone dynamics**, since containment removes reachability and disables accounts, which is exactly what breaks the monotone closure argument. Containment cost, where the defender optimizes under a cost the attacker does not bear.

> **A race between two timed mechanisms with delayed observation is one of the cleanest irreducibility structures available: the outcome depends on the interleaving, and the interleaving depends on timing no static analysis contains.**

**This is where the defender becomes a mechanism rather than a parameter** — everywhere else in Family H the defence is a static property of the environment.

**Blocked on both DEC-1 and DEC-3.** Attacker and defender are unambiguously two mechanisms and the Lab is meaningless without both; the defender's stale picture is the mechanism, not a refinement.

**Assessment.** **Keep as a later reference Study, not an early Lab implementation.** Its best result is a family of **response-threshold curves over synthetic environments** — never a prediction for a real organization. That framing is publishable, decision-relevant (organizations spend heavily on detection without evidence about where the threshold sits), and claims nothing about anyone's network.

---

## Lab 53 — Patch Propagation

| | |
| :--- | :--- |
| **Role** | **Rejected fit** — the plan-versus-phenomenon boundary Lab |
| **Standing** | Ungraded; **reject the propagation framing** |
| **Rejection reason** | **Planned/coordinated process rather than emergent process** |
| **Visual credibility** | Class 3 — the mildest hazard in the family |

**The phenomenon.** A vendor publishes a fix. Some systems apply it in hours, most in weeks, and a long tail — offline, unmanaged, embedded, unsupported, or owned by someone who left — never does. That tail is the security-relevant part: ninety-five percent coverage means five percent remains exploitable indefinitely.

**Why the framing is rejected.** The catalog entry calls this "the defensive mirror of worm propagation, running on the same topology with different incentives." That analogy is seductive and wrong in a way that matters.

> **A worm propagates because every newly infected host becomes a new propagation source. A patch in a managed environment is deployed because a central process scheduled it.**

Those are fundamentally different causal structures. Enterprise patching runs on **deployment rings** gated on the previous group not breaking; consumer rollouts are vendor-controlled percentages; cloud deploys region by region. **None of this is emergent.** Both can produce S-shaped curves, and that is not enough:

> **Same curve is not same mechanism. Outcome resemblance never establishes mechanism-family identity** — that requires correspondence in the causal transition structure, not merely matching Reader output.

This is the same discipline the catalog applied to morphology in Family D, generalized.

**The residues, both belonging elsewhere.** **Reboot-avoidance feedback** — systems that cannot reboot accumulate pending patches, which increases the risk and disruption of the eventual reboot, further discouraging it — is a genuine self-reinforcing loop with a threshold, and unusually for this family it needs no attacker. And the **attack-versus-rollout race** is entry 52's structure with different actors.

**Worth noting:** data availability here is the best in Family H — public internet-wide version scans give real adoption curves. **Good data does not create an open question**, and this entry is a useful demonstration that SCR will grade a domain down even when the measurement situation is excellent.

**Assessment.** **Reject as a standalone propagation Lab. Salvage reboot-deferral feedback or the attack-versus-rollout race under a different framing.**

---

## Lab 54 — Worm and Botnet

| | |
| :--- | :--- |
| **Role** | **Family H calibration anchor** — the only entry with real propagation evidence |
| **Standing** | Ungraded; **weak research, strong calibration** |
| **Falsifiable question** | At what degree of segmentation does the well-mixed epidemic approximation stop describing propagation? |
| **Mechanism fit** | Good — autonomous propagation, cleanly |
| **Evidence fit** | **Exceptional and unique in this family** — archived network telescope traces |
| **Question fit** | The structured case only |
| **Visual credibility** | Class 1 |

**The phenomenon.** Self-propagating code finds vulnerable hosts and uses each to find more, with no human in the loop, growing exponentially until the vulnerable population is exhausted or the network itself becomes the limit. Code Red in 2001 reached hundreds of thousands of hosts in a day; Slammer in 2003 was a single UDP packet requiring no handshake and saturated most of its vulnerable population in about ten minutes, limited by the bandwidth it consumed.

**The established shortcut, and it fits the data well.** **Staniford, Paxson and Weaver (2002)** analyzed worm propagation via the logistic equation and developed faster designs — **hit-list scanning** (the "Warhol worm") and localized scanning as used in Code Red II [3]. The estimates were, uncomfortably, borne out by Slammer months later. Epidemic thresholds on scale-free contact graphs are a known analytic result [11].

**A generating an S-curve proves almost nothing** — the classic random-scanning case is analytically covered and largely extinct, since address translation, firewalls, faster patching, and cloud hosting removed the flat reachable address space it depended on.

**Irreducible.** Topological propagation on real enterprise structures, which are heterogeneous and clustered in ways no random graph captures. Interaction with defence — takedowns and sinkholing racing propagation. **Segmented environments**, which make it a percolation question on a specific structure rather than a well-mixed epidemic.

**Why it is the family's calibration anchor.** Historical traces give something almost no other Family H entry provides: **real, timestamped propagation evidence from a real process with a known qualitative mechanism.** Every other security Lab faces the objection that its topology is unverifiable and its outcomes unmeasurable. This one can check a generated mechanism's infection curve against a measured one.

Calibration Studies available: recover the observed growth curve from a known historical mechanism; validate timing and saturation Readers; **deliberately fit a wrong epidemic or local mechanism and measure where it diverges**; quantify the transition from well-mixed to segmented synthetic networks; test detection and containment race semantics without any offensive tooling.

**Assessment.** **Build only as a defensive calibration and abstraction benchmark.** The dual-use content here is the most direct in the catalog — the 2002 paper's most-cited section is about worm design efficiency. **Avoid any mechanism-generation objective that optimizes propagation efficiency** (F-20, §18.4).

---

## Lab 55 — Segmentation and Containment

| | |
| :--- | :--- |
| **Role** | **Flagship Study and Small-Change-Test demonstrator** |
| **Standing** | Ungraded; **strongest demonstrator in the family** |
| **Falsifiable question** | Which segmentation architectures survive operational pressure as necessary exceptions accumulate? |
| **Mechanism fit** | Good for the timed version; the static version is solved |
| **Evidence fit** | Synthetic reference World |
| **Question fit** | The timed containment Study only |
| **Visual credibility** | **Class 1** — compliance auditors are attached |

**The phenomenon.** An organization divides its network so a compromise in one part cannot reach another. Then someone builds a monitoring server that reaches every zone, because monitoring has to. Or a backup system with credentials everywhere. Or a jump host, a directory service, a certificate authority. Each is necessary and justified, and each spans the division. **The question is not "is this segmented" but "which single connection defeats it"** — and that connection is usually something the security team knows about and considers necessary.

**The static question is solved.** Whether removing an edge disconnects two regions, which edges are bridges, and the minimum cut separating them are classical polynomial problems, and attack-path tooling computes exactly this. **That must be confronted first**, because it is what the Lab's name suggests.

**Why it is nonetheless the family's best demonstrator.** The platform demonstration is not the graph query. It is:

> **Hold everything constant. Remove or alter one declared connection. Re-run the same mechanism family. Compare the outcome against ambient sensitivity.**

That exercises Study, the Small-Change Test, the Repeat Test, Reader comparison, failure retention (F-14), visualization discipline, non-monotone execution, and eventually attacker/defender composition. **This is probably the cleanest place in the catalog to show what SCR means by *what mattered?***

**The visualization requirement, and it is not optional here.** A dramatic divergence after changing one edge **proves nothing if every comparable edge produces dramatic divergence.** §25.3's ambient-sensitivity context is required rather than advisory:

> **Ambient sensitivity should become a required part of Small-Change Test interpretation whenever the system is naturally unstable** — and that is not only for security.

**Irreducible.** Containment as a *timed* action, where cutting a connection stops propagation only if it happens first. Non-monotone reachability, where capability is gained by traversal and lost by response, so min-cut answers a question about a graph that does not describe the system. What the defender can actually cut, since some connections cannot be severed without stopping the business. **Segmentation decay** — divisions erode as necessary exceptions accumulate, which is a question about a *process*, and the same generative shape as entry 48.

**Assessment.** **Flagship demonstrator; blocked on DEC-1 and DEC-3 for the version that constitutes the real content.** The genuinely open question is generative: which architectures decay gracefully and which collapse after a handful of exceptions. That needs only synthetic environments and would put evidence under guidance that is currently asserted. Two standing hazards: **"segmentation held" reads as "secure"**, and compliance over-claiming is severe because segmentation is a regulatory requirement.

---

## Lab 56 — Software Supply Chain

| | |
| :--- | :--- |
| **Role** | **Maintainer / ecosystem dynamic-topology Lab** |
| **Standing** | Ungraded; **plausible only under the maintainer framing** |
| **Falsifiable question** | Can a bounded local maintainer mechanism reproduce observed ecosystem statistics without smuggling in global popularity or external organizational state? |
| **Mechanism fit** | **The reframing's central open question** |
| **Evidence fit** | **The best in Family H after entry 54** — public registries with full history |
| **Question fit** | The social layer only |
| **Visual credibility** | Class 2, with dual-use sensitivity |

**The phenomenon.** Modern software is assembled: an application declares dozens of direct dependencies whose transitive closure runs to thousands of packages by people the authors have never heard of. Compromise one and the malicious code is built into everything downstream, signed by the downstream project's own release process. The documented cases differ instructively — a maintainer handing a popular package to a stranger; a build system compromised so a vendor shipped its own backdoor; a logging library whose blast radius nobody could enumerate; a multi-year social engineering campaign granting maintainer status on a compression library, discovered by accident.

**The package framing is background, not opportunity.** Dependency closure is solved and productized; software composition analysis resolves trees and reports what is affected; bills of materials exist for exactly this. **The registries are fully observable** — the dependency graph of major ecosystems is downloadable, with complete version and maintainer history.

**The reframing, and it is the most important in the batch.** Package dependency closure is solved; **the interesting process is the social and organizational layer that changes the graph.** State: maintainer capacity, packages controlled, inactivity, handover pressure, dependency-selection habits, provenance and signing adoption, release cadence. Mechanisms: package adoption, maintainer departure, project handoff, dependency accumulation, fork creation, defence adoption.

That turns *what depends on package X?* into:

> **What local ecosystem practices produce dangerous concentration or fragility over time?**

**The caution that must travel with it.** A maintainer is a person, and their decisions are not necessarily local in the graph — they may use reputation, global popularity, organizational policy, external communication, personal economics, or a security incident. **The fact that the package graph is complete does not prove the maintainer mechanism is local.** This is the World-fit/mechanism-fit separation from entry 39 again. The data makes the test possible; it does not guarantee the answer, and if a bounded local mechanism cannot reproduce the observed statistics without global inputs, **the reframing still fails.**

**Irreducible.** Propagation *timing*, where a fix in a deep dependency reaches applications only as each intermediate maintainer releases — Log4Shell's long tail was this, not the closure. The maintainer layer, where the pivotal incidents were social. Diffusion of defensive practices on the same graph. Detection latency.

**Architecture.** A **directed acyclic graph**, a distinct Layout case from lateral movement's mesh. And **the graph changes as the mechanism runs** — dynamic Connections again.

**Assessment.** **Keep as plausible, with maintainer and ecosystem dynamics as the primary fit candidate and package reachability as incumbent territory.** Dual-use care: research identifying which packages are most fragile is a target list, and publication discipline matters more than the technical risk suggests.

---

## Family findings

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Dynamic Connections** — Plugin proposes, Reactor validates and applies under a declared contract | *unregistered* — **now likely foundational rather than speculative** | 48, 56; with 18, 50, 58 elsewhere. Needs allowed source/target types, connection types, creation and removal budgets, duplicate-relation rules, reversibility, complete history, and future-relevant-state inclusion. |
| **Seen State versus World State** | *unregistered* | 47, 52, 55. Entry 40 in Family F is the cheaper place to build it first. |
| **Multi-mechanism composition** | **DEC-1** | 52 and 55 are meaningless without attacker and defender both |
| **Temporal semantics** | **DEC-3** | 52 (the race), 55 (timed containment) |
| **Shared Domain World templates distinct from Labs** | *unregistered* | 47, 48, 52, 54, 55 — one World, several mechanisms |
| **Rejection reasons recorded, not just grades** | **DEC-15** | 51 (observation), 53 (planned process) — two distinct categories |
| **Provenance inside high-risk Views** | *unregistered* | 52, 55 |
| **Execution boundary for adversarial Labs** | **DEC-16** | The whole family (F-20, §18.4, LAB-4) |

### Build priority within the family

**First deliverable — probably not a Lab.** The **versioned synthetic enterprise reference World**, seeded with known traps.

**Tier A.** **Segmentation (55)** — flagship Study demonstrator. **Worm (54)** — the only calibration anchor with real traces; defensive framing only. **Identity and Privilege (48)** — strongest research question, needs dynamic Connections. **Supply Chain (56)** — under the maintainer framing.

**Tier B — blocked.** **Ransomware (52)** — excellent timed-race question, blocked on DEC-1 and DEC-3. **Lateral Movement (47)** — narrow reframing, weak topology evidence.

**Tier C — weak or rejected.** **Agent Memory (50)** — the better AI entry. **Prompt Injection (49)** — weak; substrate ages faster than generalization. **Sensitive Data (51)** and **Patch Propagation (53)** — rejected, and each contributes a distinct rejection category.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** Ammann, P., Wijesekera, D. & Kaushik, S. (2002). Scalable, graph-based network vulnerability analysis. *Proc. 9th ACM Conference on Computer and Communications Security*. *(Explicit monotonicity assumption: the precondition of an exploit is never invalidated by another's success — the attacker never needs to backtrack — reducing computational cost to polynomial.)*
2. **[V]** Harrison, M. A., Ruzzo, W. L. & Ullman, J. D. (1976). Protection in operating systems. *Communications of the ACM* **19**, 461–471. *(The access matrix has extremely weak safety properties; different natural formulations of the safety problem are NP-complete or undecidable, and safety is undecidable for most policies of practical interest.)*
3. **[V]** Staniford, S., Paxson, V. & Weaver, N. (2002). How to 0wn the Internet in your spare time. *Proc. 11th USENIX Security Symposium.* *(Logistic-equation worm propagation; hit-list scanning — the "Warhol worm"; localized scanning as in Code Red II.)*
4. **[D]** Sheyner, O., Wing, J. et al. (early 2000s) — model-checking attack graphs and state-space explosion; Take-Grant and typed access matrix models recovering decidability.
5. **[D]** BloodHound and successors — identity-graph attack-path computation; software composition analysis and SBOM practice.
6. **[D]** Pastor-Satorras, R. & Vespignani, A. (2001) — epidemic thresholds on scale-free networks; CAIDA analyses of the Code Red and Slammer events from network telescope data.
7. **[D]** Model collapse literature on recursive training over model-generated output (2023–2024) — structurally analogous to the drift mechanism in entry 50.
8. **[D]** Indirect prompt injection framing and blast-radius mitigation guidance (2022 onward); public agent-security evaluation suites.
9. **[D]** Branching process theory — extinction probability and the critical threshold at reproduction number one.
10. **[D]** Documented supply chain incidents: event-stream (2018), SolarWinds (2020), Log4Shell (2021), xz/liblzma (2024).
11. **[D]** Reproducible builds, artifact signing and provenance attestation, dependency pinning; zero-trust and microsegmentation guidance; minimum cut via maximum flow.

---

## Non-claims

This report performs no fit reviews and establishes no fit. **Nothing in this family assesses the security of any real environment, organization, network, package, ecosystem, or AI system; identifies attack paths, vulnerable dependencies, or fragile components; predicts attacker behaviour; evaluates detection or response products; or supports compliance, audit, or regulatory claims** (§41, §43). F-20 applies throughout: studying hostile behaviour never justifies a more permissive execution surface for generated code (§18.4, LAB-4, DEC-16). No mechanism-generation objective here may optimize propagation efficiency or offensive effectiveness. Entries 47–50 have received no critique review; their assessments are first opinions. The family is ungraded and may fail its fit review.
