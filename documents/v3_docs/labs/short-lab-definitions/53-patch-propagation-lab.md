# 53. Patch Propagation Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #53, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A vendor publishes a fix. Some systems apply it within hours. Most apply it within weeks. And a long tail — machines that are offline, unmanaged, embedded in equipment nobody wants to reboot, running an unsupported version, or owned by someone who left — never applies it at all.

That tail is the security-relevant part. Aggregate patch coverage of ninety-five percent sounds excellent and means that five percent of an estate remains exploitable indefinitely. Internet-wide scans routinely find substantial populations of systems with vulnerabilities patched years earlier.

The shape of the curve is consistent across vendors and vulnerabilities: fast initial uptake, a long slow decay, and an asymptote well short of complete.

## What the domain already knows

**The measurements exist and are public.** Internet-wide scanning services enumerate reachable systems and their version banners continuously, so patch adoption curves for internet-facing software are directly observable. Vulnerability disclosure and exploitation timelines are published. Vendor telemetry provides the enterprise picture, less publicly.

**Deployment is centrally scheduled, and this is the crucial fact.** Enterprise patching runs on **deployment rings**: a pilot group, then a broader group, then general availability, each gated on the previous group not breaking. Consumer operating systems use staged rollouts with vendor-controlled percentages. Cloud services deploy region by region. **None of this is emergent** — it is a plan someone wrote, executed by management tooling.

**The known failure modes are organizational.** Systems in a management blind spot, patches deferred because of compatibility risk with legacy applications, machines that need a reboot the business will not authorize, and equipment whose vendor no longer supplies updates. These are causes of the tail and they are not dynamics.

**Dependency-driven delays are real.** A patch may require a platform upgrade, which requires an application vendor's certification. That produces a dependency chain, and chains have propagation delay.

## Where the shortcut holds, and where it breaks

**Reducible — nearly all of it.** Adoption curves are fitted empirically and the fits are good. Coverage at time *t* given a rollout schedule is arithmetic. Exposure window from disclosure to patch is a measurement. Ring-based rollout timing is planned, not predicted. Diffusion-of-innovation and epidemic-style curve fits describe the aggregate adequately, and their parameters are estimated from observation rather than derived.

**Irreducible — a genuinely short list, and thin:**

- **Dependency chains blocking cohorts.** When patching A requires B which requires C, and each hop has an approval delay, the tail's length is a composition of delays over a dependency graph. That is a propagation problem, though a mostly linear one.
- **Reboot-avoidance feedback.** Systems that cannot be rebooted accumulate pending patches, which increases the risk and disruption of the eventual reboot, which further discourages it. A genuine positive feedback loop producing a self-reinforcing tail.
- **Coupling to exploitation.** Once a vulnerability is exploited in the wild, patching accelerates sharply. Attack and defence are coupled through attention, which is a feedback across two populations.

**The lens, stated plainly.** The catalog frames this as "the defensive mirror of worm propagation, running on the same topology with different incentives." That framing is appealing and I think it is wrong in a way that matters.

**A worm propagates; a patch is distributed.** A worm's spread is genuinely emergent — each infected host independently infects others, nobody plans it, and the topology determines the curve. A patch's spread is a schedule executed by management infrastructure, plus an organizational tail. The resemblance of the curves is superficial: an S-curve arises from many processes, and matching one does not establish a shared mechanism.

This is the same error the Buldyrev critique identified in #42 — a plausible structural analogy substituting for the actual mechanism — and it is worth catching here because the analogy is seductive.

## What a Cell would carry

A system: patch level, management coverage, reboot pending, dependency state, and exposure. Bounded scalars; §13.1 met easily.

**Layout is a Network World** or, more honestly, an organizational hierarchy — deployment rings are a *management* structure rather than a network one, and the relations that matter (this system is in that ring, this application requires that platform version) are administrative.

**The scheduler problem is decisive here**, as in #39 and #44. The dominant mechanism is a central rollout plan. A local rule cannot express "the pilot ring completes, then the broad ring begins," because that is a global gate. And a model that omits the gate is not modelling patching.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak. I would grade it so, at the bottom of Family H alongside #51 — and for a cleaner reason than most weak entries.**

The mechanism is not emergent. It is a plan, executed by tooling, with an organizational tail whose causes are known and are not dynamical. The empirical curves are measured directly and fitted well. There is no live scientific controversy about how patches propagate; there is a well-understood operational problem about why some systems are never reached, and the answer is inventory and ownership rather than dynamics.

The worm analogy that motivates the entry does not survive examination.

**What is nonetheless worth taking from it.** Two things.

First, this entry adds a **fifth rejection reason** to the catalog's collection, distinct from the others: not "the mechanism is global physics" (#42, #43), not "the mathematics is closed-form and the problem is measurement" (#51), not "the substrate moves" (#49), not "the agents use global information" (#60), but **"the process is a plan, not a phenomenon."** It shares this with #39 and #44, and articulating it once, clearly, serves all three.

Second, there is a genuinely interesting question hiding here that belongs to a different Lab: **the exposure race.** How long a population remains exploitable, given a rollout schedule racing an exploitation process that accelerates when exploitation becomes known, is a two-mechanism race with feedback — and that is #52's structure and #54's subject matter. The interesting content is the coupling, not the propagation.

**The upside worth being excited about.** Modest and specific: **the reboot-avoidance feedback loop** is a real self-reinforcing mechanism with a genuine threshold — at what deferral rate does a population's pending-patch backlog become self-sustaining? That is a small, honest, answerable question, and unusually for Family H it needs no attacker at all.

Data availability is the best in Family H by a wide margin: public internet-wide version scans give real adoption curves against which any mechanism can be checked. That is worth noting because it makes this Lab an unusually good place to demonstrate that **SCR will grade a domain down even when the data is excellent** — data quality does not create an open question.

**The challenges, in order of severity.**

1. **The mechanism is a schedule**, not an emergent process — DEC-1's coordinator problem, decisively.
2. **The curves are directly measured and well fitted**; nothing needs deriving.
3. **The tail's causes are organizational**, not dynamical, so a mechanism model addresses the wrong layer.
4. **The worm analogy is superficial**, and building on it would repeat a documented class of error.
5. **Low over-claiming risk** — one of the few entries in Family H where the misuse hazard is mild, because nothing here sounds alarming.

## Non-claims

This Lab does not assess patch management or vulnerability exposure for any real organization or population, and produces nothing suitable for operational or security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
