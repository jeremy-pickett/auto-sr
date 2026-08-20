# 48. Identity and Privilege Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #48, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

Permission in a real organization is not granted; it accumulates. A person joins a team and inherits the team's role. The role was granted access to a system three years ago for a project that ended. A service account was given the ability to manage group membership so an automation could work. A group was nested inside another group by someone who has since left.

Nobody ever decided that a contractor in the marketing team should be able to reset the password of an account that administers the finance system. But the composition of a dozen individually reasonable delegations says they can, and the composition is not written down anywhere.

The characteristic property is that **the dangerous permission is not in any record.** Every individual grant is documented. The path through them is not.

## What the domain already knows

**This domain has a foundational undecidability result, and it is the most important thing in this brief.**

Harrison, Ruzzo, and Ullman proved in 1976 that for a general access-control model with commands that create subjects, objects, and rights, the **safety question — can this subject ever obtain this right — is undecidable** *(attribution from memory, verify)*. Not hard. Undecidable, by reduction from the halting problem.

That is a startling result to have at the base of a practical field, and the field's entire structure is a response to it. Restricted models were developed specifically to recover decidability: the **Take-Grant** model gives safety decidable in linear time for its restricted operations; **typed access matrix** and other formulations trade expressiveness for tractability. Every deployed authorization system is a point on that trade-off curve, chosen so the questions people need to ask can be answered.

**Modern practice computes closure and calls it reachability.** BloodHound and its successors ingest directory data, build a graph of principals and the relations between them, and answer "what is the shortest path from this user to Domain Admin" with a graph query. It works, it revolutionized enterprise security assessment, and it is fast — because the underlying question, given a static graph and monotone rights, is transitive closure.

**Cloud IAM made it worse and better simultaneously.** Policy languages with conditions, wildcards, and cross-account trust create enormous implicit permission surfaces; tooling for reasoning about them exists, including formal-methods-based analyzers that use SMT solvers to answer policy questions soundly.

## Where the shortcut holds, and where it breaks

**Reducible.** Static reachability over a fixed permission graph — transitive closure, polynomial, and it is what the tooling does. Shortest path to a target principal. Whether a specific policy grants a specific action — decidable for restricted policy languages, and solvers do it. Group membership expansion. Effective permissions for a principal at a moment in time.

**This covers most of what practitioners ask, and the tooling answers it well.** A Lab here that offers "we can find attack paths" is offering a worse version of a solved product.

**Irreducible.** Where the closure argument stops:

- **Rights that create rights.** The HRU result bites precisely when commands can grant the ability to grant. A principal who can modify group membership can grant themselves anything that group has — including, possibly, more ability to modify membership. That self-referential structure is what makes safety undecidable in general, and it is present in every real directory.
- **Time-varying permission.** Grants are added and revoked continuously by many uncoordinated actors. A path that does not exist today existed for six hours last Tuesday. Static analysis of a snapshot answers a question about a moment, and the interesting question is about a *history*.
- **Non-monotonicity.** Credentials rotate, sessions expire, accounts are disabled. Once rights can be lost, the closure argument fails and reachability becomes path- and timing-dependent.
- **Emergence of dangerous composition.** As an organization grows, new grants compose with old ones. Whether an environment tends toward or away from unintended privilege, under given delegation practices, is a question about the *process* that generates the graph, not about any graph.

**The lens, stated plainly.** This is the strongest irreducibility framing available anywhere in this catalog, and it is not an analogy: **the domain's core question is provably undecidable in the general case, and the field's entire practical apparatus consists of restrictions adopted to escape that.**

The gap is therefore precisely locatable. Tooling answers the restricted, static, monotone question extremely well. Nobody answers the unrestricted, dynamic, generative question — what *kinds* of delegation practice produce environments that accumulate unintended privilege — because it is not a question about any particular environment, and the tools are all environment-specific.

That question is ensemble-shaped, mechanism-shaped, and unclaimed.

## What a Cell would carry

A principal — user, group, role, service account, or machine: privilege level held, rights over other principals, credential state, and activity or staleness. Bounded scalars; §13.1 met, with one important caveat: **the interesting rights are relations, not scalars**, and they live on Connections rather than in Cells.

**Layout is an Identity World** (§15), which the catalog names, and it is the honest arrangement. Connections are trust, membership, delegation, inheritance, and the ability to modify others — directed, typed, and asymmetric.

The distinctive problem: **the mechanism modifies the World's Connections.** A principal exercising the right to add a group member creates a new edge. That is the self-constructed-topology question from #18, appearing here with the highest stakes in the catalog, because it is exactly the mechanism that makes the domain's safety problem undecidable. A platform that cannot express a mechanism creating Connections cannot express this Lab's central phenomenon.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible to strong, and — with the narrow framing below — I would rank it the strongest entry in Family H, ahead of #47.**

The naive framing is weak and should be rejected early: "model an organization's permissions and find attack paths" duplicates BloodHound badly, needs directory data nobody will share, and produces confident output about a topology that is probably wrong.

The strong framing is a research one: **SCR as an instrument for studying how permission structures accumulate.** Generate synthetic organizations under candidate delegation mechanisms — how teams are formed, how roles are granted, how service accounts are created and abandoned — run them forward for simulated years, and measure how unintended privilege paths accumulate. That needs no real environment, claims nothing about any customer, and asks a question the static tooling structurally cannot ask.

**The upside worth being excited about.** The finding this could produce is genuinely valuable and currently unavailable: **which delegation practices are self-limiting and which compound.** Security guidance in this area is largely folklore — "avoid nested groups," "limit service account permissions," "review access quarterly" — asserted without evidence about how much each matters. A corpus recording which local grant-and-revoke mechanisms produce environments that stay clean and which produce environments that rot, with the failures kept, would put evidence under that guidance.

And it connects to a live product category: identity governance and administration tools attempt exactly this cleanup, with little theoretical basis for their policies.

The HRU result also gives this Lab something rare — a **principled reason for the platform to exist here**. When the general question is undecidable, "run it and see" is not a fallback, it is the only remaining method, and the field's own literature says so.

**The challenges, in order of severity.**

1. **The mechanism creates Connections**, which the platform has not settled and which is the whole phenomenon.
2. **Real directory data is confidential** and will not be shared; synthetic environments are the only honest option and their realism is unverifiable.
3. **"No path found" reads as "secure"** — inherited from #47 and equally dangerous here.
4. **Static tooling already answers the question people ask**, so the Lab must argue for a different question.
5. **F-20 applies**: studying privilege escalation never justifies a more permissive execution surface (§18.4, DEC-16).
6. **Commercial over-claiming risk**, which the catalog explicitly warns about for this family.

## Non-claims

This Lab does not assess permissions in any real environment, does not identify attack paths in any organization, does not predict attacker behaviour, and produces nothing suitable for security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
