# DEC-3 — Whose clock is it, and must everything tick together?

*Formal name: temporal semantics. Cite this record as **DEC-3**.*

**Status:** open; placement decided · **Who decides:** the project owner · **Kind:** boundary — the ownership line is drawn; which clocks we offer is not

> **In one sentence:** every experiment needs a clock; we have already decided the platform owns it and the rules never do — what's still open is whether we offer anything beyond "everything updates at the same moment," and for whom.

---

## What this is about

Today every experiment runs in lockstep: at each tick, every participant looks at the world, and all their changes land at once. One clock, one beat, perfectly repeatable.

But some of the most interesting real-world behaviour lives in the gaps between clocks. Anyone in security knows the shape: a revoked badge that still opens some doors for a few minutes, because the door controllers pick up updates on a schedule. The account that keeps working after access was cut. The alert that arrives about something that finished happening. Stale information, delayed effect, things landing out of order — that is where a lot of real incidents actually live.

A platform that can only express perfect lockstep cannot express any of that. Those experiments would be impossible to even describe.

## What's already decided — and why it was the dangerous part

The tempting design was to let a rule manage its own timing. That was reviewed and rejected, and the rejection is now settled law in the core documents:

> **The platform owns the clock. A rule may *ask* for an effect to land later — the same way it asks for anything — and the platform decides what "later" means, when it lands, in what order, and whether the budget allows it.**

Why this matters: the one component we cannot fully trust is the rule, because it's written on demand, by a machine or a person, for each experiment. Handing that component its own clock would let it reshape the experiment it's supposed to be running inside. Asking is fine. Owning is not.

One more thing is settled: **any clock we offer must replay perfectly.** Run it again, get the same history. A timing model that can't be replayed doesn't get offered, no matter what it would enable.

## Why the rest is still a real question

There's a finding from the field's own literature that makes timing more than a technical preference: researchers compared the same rules under synchronized clocks versus staggered ones, and found that some of the patterns people attributed to the rules were actually artifacts of the clock. **Change how you tick, and different patterns appear — from the same rule.**

That means a timing model isn't plumbing. It is part of the experiment, it changes results, and it has to be declared and recorded like everything else that changes results.

## What's open

1. **Which timing models we offer at all** — lockstep only? Lockstep plus scheduled delays? Full event ordering?
2. **Which experiments may ask for them** — is delayed observation available everywhere, or only to settings that declare a need?
3. **The budget** — a rule that can schedule effects can schedule a flood of them; how much "later" is any one participant allowed to buy?

## What would make this easy to decide

> **Which Labs on your list actually need timing gaps — and would lockstep plus "recorded inputs on a schedule" cover them?**

The security family almost certainly needs stale observation. Most of the physical-world Labs (fire, sand, ice) are honestly served by lockstep. If the need is concentrated in one family, the answer may be: lockstep is the default, richer clocks are a declared capability that a setting must ask for — which is the shape the core documents already lean toward.

## What this is blocking right now

- Nothing is stopped today — lockstep is fully specified and everything runs on it.
- The security-family Labs cannot be *designed* honestly until this lands (their fit reviews ask "what does one step mean here?" and get no answer).
- `../01-core/reactor.md` §6 and `../01-core/plugins.md` §4 hold the door open (REACTOR-14 to REACTOR-16, PLUGIN-10, PLUGIN-11).

---

## The precise version

*This is the wording other documents cite. It says the same thing in the platform's own vocabulary.*

Which execution models the Reactor offers beyond synchronous lockstep — discrete-event ordering, declared observation staleness, delayed effect application, deterministic interleaving — which Worlds may declare them, and what the scheduling contract and budgets are.

**The placement is foundational law and is not reopened here** (SCR-F §6, §18.5): asynchrony, observation staleness, delayed effect, and interleaved application are declared capabilities of the World and Reactor. A Plugin may *propose* a future-offset effect exactly as it proposes any other state change; the Reactor owns the clock, the queue, quantization, ordering, and budgets. Scheduling proposals are writes, and writes are budgeted. Determinism and exact replay are non-negotiable under every model offered. Update timing is experimental semantics, not an implementation preference (Ingerson and Buvel, 1984 — cited in `../01-core/reactor.md` §6.1).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; the question, identifier, status, and constraints are unchanged. Prior text is in version history.
