# Human and machine

**Document class:** Level 1 — Foundations · **Status:** draft
**Path:** `00-start-here/human-and-machine.md`
**Cites:** SCR-F v0.2 §3, §4, §16.5, §31, §43; F-3, F-4, F-6

---

## The point of the arrangement

> **Automation is not the objective. Better allocation of work is the objective.**

The distinction is not a nicety. A system built to remove people produces different software than a system built to move people onto the work that needs them, and the two are hard to convert into each other later.

Experimentation has always carried a large amount of work that is necessary, unrewarding, and easy to get wrong when tired: writing out an idea precisely, implementing it without slips, repeating it enough times to learn anything, keeping track of what was done, and finding it again afterwards. That work is where machines are genuinely good now, and where fatigue makes people genuinely bad.

The work that remains is not leftover. It is the part that decides whether any of it was worth doing.

---

## The allocation

**Machines take the mechanical load.** Turning a request into a candidate experiment. Writing routine implementations. Checking structure and contracts. Repeating runs. Exact bookkeeping. Capturing provenance. Rebuilding stored evidence. Running deterministic measurements. Searching prior work. Drafting routine summaries. Putting candidate explanations in front of a person.

**People keep the judgment.** Choosing which questions matter. Supplying context the machine does not have. Recognising a bad abstraction. Challenging an assumption. Deciding whether a mechanism is plausible. Deciding whether a result matters. Deciding whether this platform is even the right tool for the subject. Deciding whether the evidence justifies doing something in the real world, and carrying the consequence of that decision.

Nothing in the second list is a task the first list is working toward. They are different kinds of work.

### How to tell whether it is working

The claim is testable in a modest way, and should be stated modestly. Ask what a person spent their session doing. Time spent correcting transcription, re-running something by hand, or reconstructing what was done last week is time the platform failed to absorb. Time spent arguing with a result, rejecting an abstraction, or deciding what to try next is the platform working.

That is an observation about where attention went, not a measurement of productivity, and it should never be dressed up as one.

---

## Three records that are allowed to disagree

The platform keeps three separate things, and never lets one overwrite another:

**Intent** — what someone meant to try.
**Implementation** — the mechanism that was actually produced.
**Outcome** — what happened when it ran under exact conditions.

They often agree. When they do not, that is frequently the most interesting thing on the page. A mechanism meant to settle a boundary may break it up. A rule meant to hold things still may produce something that travels. A change meant to contain a spread may speed it up.

None of those is only a mistake. Each is a place where a stated idea and its actual behaviour came apart, which is exactly what an experiment is for.

So: a person's correction does not erase what the machine originally proposed. A measurement does not become the Run it measured. A mechanism that executes cleanly has not thereby been shown to implement what was asked. **The gap between the three is part of the evidence, and squashing it destroys the finding.**

---

## The machine cannot grade its own homework

A machine that writes a mechanism will also, if asked, explain that mechanism. The explanation is useful. It is not evidence.

This holds everywhere, but the clearest case is repair. When a proposed mechanism fails a check and the system fixes it, requiring a person to read the change line by line to confirm the meaning survived would push them straight back into implementation mechanics — the thing this platform exists to spare them. So a repair owes a plain-language account of what changed: *the neighbour count no longer includes the cell itself; nothing else changed.*

That account is produced by the same kind of machinery that produced the repair. It is therefore **interpretation** — versioned, arguable, and open to correction — and never proof that the repair was faithful. The change itself remains the evidence. The account is how a person decides whether to go and look.

The same rule governs summaries, generated reports, narration, and confidence statements. A machine describing its own work is a witness with an interest.

---

## Corrections count as evidence

A person who knows the subject will sometimes say things the platform cannot check:

> That relationship points the wrong way.
> Those are separate outbreaks, not one advancing front.
> Nothing in this system can observe that value directly.
> This measurement is counting retries as spread.

Each is a real contribution and each has to survive.

The platform keeps the original machine proposal, the correction, the reason where one was given, what changed as a result, who or what supplied it, and which later work depends on it.

A correction never quietly rewrites history. Disagreement stays visible, because a record showing only the final agreed answer has thrown away the part a later reader most needs: that the question was once open, and who closed it, and why.

---

## What this arrangement is not

It is not a promise that the machine is usually right. It is a division of labour that assumes the machine is often wrong in specific, catchable ways — slips, misreadings, plausible nonsense — and builds checking, execution, recording, and correction around that assumption.

It is also not a promise that the person is usually right. It is a promise that when they disagree, both positions are kept, attributed, and left where someone can look at them later.
