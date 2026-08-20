# 56. Software Supply Chain Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #56, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

Modern software is assembled. An application declares a few dozen direct dependencies; those declare their own; and the transitive closure runs to hundreds or thousands of packages written by people the application's authors have never heard of. Compromise any one of them and the malicious code is built into everything downstream, signed by the downstream project's own release process, and distributed through channels everyone trusts.

The documented cases are instructive because they are all different. A maintainer handed a popular package to a stranger who added malicious code (event-stream, 2018). A build system was compromised so that the vendor shipped a backdoor to its own customers (SolarWinds, 2020). A widely-used logging library had a vulnerability whose blast radius nobody could enumerate, because nobody knew where it was included (Log4Shell, 2021). A multi-year social engineering campaign gave an attacker maintainer status on a compression library used in a critical authentication path, discovered by accident (xz/liblzma, 2024).

The property they share is **transitive trust that nobody audits**, and a blast radius that is a graph traversal nobody has run.

## What the domain already knows

**The reachability question is solved and productized.** Software composition analysis tools resolve dependency trees, match against vulnerability databases, and report what is affected. Software bills of materials exist as a standard artifact for exactly this. The response to Log4Shell drove enormous investment here, and enumerating "what depends on this package" is now largely a solved data problem for open ecosystems.

**The registries are fully observable.** Package registries publish every package, version, and dependency declaration, openly. The dependency graph of the npm, PyPI, Maven, and crates ecosystems is downloadable. This is a **complete, public, machine-readable topology** — a thing no other Lab in Family H has and few in the catalog have at all.

**Graph structure has been measured.** Studies of ecosystem dependency graphs report highly skewed dependent counts — a small number of packages that essentially everything depends on — and deep transitive chains. The structural fragility this implies is documented rather than theorized.

**Defences are structural, not dynamic.** Reproducible builds, artifact signing and provenance attestation, dependency pinning, and vendoring all aim to make the graph auditable or to remove trust from it. The direction of travel is toward verification rather than toward modelling.

## Where the shortcut holds, and where it breaks

**Reducible — and it is a large fraction of the domain.** Blast radius of a compromised package: transitive closure on a directed acyclic graph, computable exactly, and computed daily by commercial tools. Which packages are most critical by dependent count: a graph measurement. Whether a vulnerable version is in a given build: resolved by the package manager. Time-to-remediate given a dependency depth: arithmetic over release cadences.

If the question is "what would be affected," the answer is a query against a public dataset.

**Irreducible.** What the closure does not cover:

- **Propagation timing.** A fix in a deep dependency does not reach applications until each intermediate package releases a version that adopts it, and each maintainer does that on their own schedule — or not at all, if pinned. The lag through a chain is a composition of independent human delays, and whether a fix ever reaches the leaves is genuinely uncertain. Log4Shell's long tail was this, not the closure.
- **The maintainer layer.** The event-stream and xz cases were social, not technical: the mechanism was trust transfer between people. Maintainer burnout, handover, and the concentration of critical packages on single unpaid individuals is the actual risk surface, and it is a social process with its own dynamics.
- **Adoption of defences.** Whether signing, pinning, or reproducible builds spread through an ecosystem depends on maintainers adopting them, which depends on their dependents asking, which is a diffusion process on the same graph.
- **Detection latency.** xz was found by chance, by someone investigating a performance anomaly. How long a well-crafted compromise persists before discovery is not a graph property.

**The lens, stated plainly.** This Lab has an unusually clean division and it points somewhere specific: **the graph is solved; the humans and the clock are not.** Every documented major incident turned on something outside the dependency graph — a maintainer handover, a build system, a release cadence, an accidental discovery.

That means an SCR Lab modelling propagation *through the graph* would be recomputing what commercial tooling already reports. The open questions all live on the layer above, where the participants are maintainers rather than packages.

## What a Cell would carry

If a Cell is a package: compromised state, version, release cadence, maintainer count, and adoption of verification practices. If a Cell is a maintainer: activity, capacity, number of packages held, and trust relationships. Bounded scalars; §13.1 met either way, but **the choice between the two determines whether the Lab is interesting**, and I think the maintainer framing is the live one.

**Layout is a Network World, specifically a directed acyclic graph** — and the catalog is right that this makes it a distinct Layout case from lateral movement's mesh. Dependency edges point one way and cycles are (mostly) prohibited by construction, which is a genuinely different structure with different propagation properties.

The distinctive feature: **the graph changes as the mechanism runs.** Maintainers add and remove dependencies, packages are deprecated, forks appear. That is self-constructed topology again (#18, #48), and here it is the medium-term dynamic that determines ecosystem fragility.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the best data situation in Family H after #54's telescope traces — and a strong argument only under the maintainer framing.**

The package framing is weak: it recomputes solved closures over a public graph.

The maintainer framing is genuinely interesting and, as far as I know, under-attacked. **What ecosystem-level dynamics produce dangerous concentration?** Packages accumulate dependents; maintainers accumulate packages; unmaintained packages accumulate dependents faster than they accumulate maintainers. Whether an ecosystem tends toward or away from single-point fragility, under given local behaviours (how developers choose dependencies, how maintainers hand over projects, how forks succeed), is a generative question about a process — the same shape as #48's delegation question and #55's segmentation-decay question.

That question needs no attacker, claims nothing about any specific package, and is checkable against twenty years of real registry history.

**The upside worth being excited about.** This is the strongest empirical position in Family H for a specific reason: **the World's topology is public, complete, machine-readable, and has a full historical record.** Registry data includes every version, every dependency change, and every maintainer event, going back years. A generated mechanism for how developers choose dependencies can be run forward and compared against how the real ecosystem actually evolved — not qualitatively, but against the measured degree distribution, the measured concentration, and the measured growth of transitive depth.

That is a genuine accuracy test (§30.6), and it is the only entry in Family H where I think one is straightforwardly available. If Family H needs to demonstrate that its Labs can be *graded* rather than merely argued about, this is the second candidate alongside #54.

The negative space is also directly actionable: "these dependency-selection behaviours never produced an ecosystem without single-point concentration" would inform package-management design, which is a thing people are actively building.

**The challenges, in order of severity.**

1. **The package-level question is solved** and productized; only the maintainer layer is open.
2. **The graph changes as the mechanism runs** — self-constructed topology, unresolved in the platform.
3. **The pivotal incidents were social engineering**, which is not a mechanism a bounded-state Cell represents well.
4. **Dual-use sensitivity**: research identifying which packages are most fragile is a target list. F-20 applies, and publication discipline matters here more than the technical risk suggests.
5. **Ecosystem findings do not transfer** — npm, PyPI, and Maven have very different cultures and structures, so a mechanism fitted to one may say nothing about another.

## Non-claims

This Lab does not assess the security of any real package, project, ecosystem, or organization, does not identify vulnerable or fragile dependencies, and produces nothing suitable for security or engineering decisions. It is ungraded and may fail its fit review (§30, §41, §43).
