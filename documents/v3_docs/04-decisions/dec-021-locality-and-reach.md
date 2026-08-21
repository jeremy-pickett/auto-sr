# DEC-21 — How far can a rule reach?

*Formal name: locality and reach. Cite this record as **DEC-21**.*

**Status:** open; leading formulation recorded · **Who decides:** the project owner · **Kind:** boundary — this line is part of what the product *is*

> **In one sentence:** this platform's identity is that everything happens through local interaction — neighbour affecting neighbour — but real subjects keep producing honest exceptions, and somewhere between "next door only" and "anything can touch anything" the word *local* stops meaning something.

---

## What this is about

The platform studies what happens when small local rules repeat: fire igniting the patch beside it, one account's compromise reaching the accounts it connects to. *Local* is the discipline that makes results interpretable — behaviour emerges from chains of small steps you can trace.

Then the real subjects arrive with exceptions:

- Wildfire has what firefighters call **spotting** — embers lofted a kilometre ahead of the front, starting new fires across unburnt ground. Not neighbour-to-neighbour. Real, and decisive in real fires.
- Wind-blown sand moves in hops that land past the neighbours. Seeds ride animals far from the parent plant. A scanning process probes across a network rather than spreading through it.

Four Labs, one shape: a jump. If we refuse jumps, those Labs can't be honest. If we allow arbitrary jumps, we're not a local-mechanism instrument anymore — we're a general simulator with a restrictive vocabulary.

## The leading formulation — recorded, not adopted

The insight that reframed this: **the danger was never distance. It's addressing.**

Network people will recognize it instantly, because it's segmentation. On a well-run network, a workstation reaches a server only if a route and a credential exist — reachability is *declared*. The disaster case is the flat network: anything can reach anything it can name. The distance between two machines was never the point.

Applied here:

> **A rule may observe or affect only what it can reach through connections the experimental setting has declared.** A long jump is fine *if the setting declares the transport* — an ember-transport connection, a dispersal connection — because then the setting still defines what's reachable and the platform still enforces it. What's forbidden, at any distance, is a rule touching a participant just because it knows it exists.

By that light, the fire Lab's spotting isn't a violation of locality. It's a declared connection with a long throw — and it stays inspectable, budgeted, and on the record like every other interaction.

This formulation has fifty years of pedigree in computer security (authority travels with the handed-over path, not with knowing a name), cited in the Plugin requirements.

## What's genuinely open

1. Whether declared long-range transport is a legitimate expression of locality — or a loophole that lets any World define "local" into meaninglessness by declaring everything connected.
2. Whether any limit on reach applies beyond what the setting declares (per-rule, per-World, or none).
3. Who polices a World whose declared connections amount to a flat network.

Question 3 is the sharp one: the formulation moves the burden from the rule to the World, and nothing yet audits Worlds.

## What this is blocking right now

- The final reach vocabulary in `../01-core/plugins.md` (PLUGIN-8 and PLUGIN-9 record the formulation as leading, not adopted).
- Honest design of the wildfire, dune, dispersal, and scanning-behaviour Labs — each names this need explicitly.

---

## The precise version

*This is the wording other documents cite.*

What a mechanism is entitled to observe and affect — and therefore where the word *local* stops meaning anything and the platform stops being a local-mechanism instrument. Leading formulation in `../01-core/plugins.md` §3 (PLUGIN-8, PLUGIN-9): reach as authority rather than distance — a mechanism may observe or affect a Cell only by traversing connections the World declared and the Run Contract admitted; long-range effects are declared transport connections, never unrestricted addressing. Ancestry in capability-based protection (Dennis and Van Horn, 1966; Hardy, 1988 — cited there). Open: whether declared transport is legitimate locality or a loophole; reach limits beyond the World's declaration; and what audits a World whose declarations amount to a flat network. SCR-F §45.12 asks reviewers to hunt exactly this over-generalisation.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and the recorded leading formulation unchanged. Prior text is in version history.
