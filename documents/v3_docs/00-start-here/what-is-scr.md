# What SCR is

**Document class:** Level 1 — Foundations · **Status:** draft
**Path:** `00-start-here/what-is-scr.md`
**Cites:** SCR-F v0.2 Executive summary, §1, §2, §7, §22, §41–43, §44
**Read first.** Everything else in this tree assumes this page.

---

## In one paragraph

Semantic Cellular Ruliology is an instrument for proposing simple local mechanisms, running them under controlled conditions, and keeping everything that happens. A person describes a problem, a behaviour, a suspicion, or a question in ordinary language. The platform turns that into a mechanism it can execute, checks the implementation, runs the experiment, measures the result, and keeps the whole chain — what was asked, what was built, what actually ran, what happened, and where a person disagreed with any of it. Failures are kept on the same terms as successes.

---

## The bet

### Simple local rules can produce behaviour nobody put there

This is not a hope. It is the oldest settled result in the field.

Von Neumann built a self-reproducing machine out of a grid of cells with twenty-nine states, using a cellular framework suggested to him by Stanisław Ulam; the work was completed and published after his death.[^vn] Conway's Life takes it further with almost nothing: four rules about how many live neighbours a cell has, on a square grid.[^life] Out of those four rules come shapes that hold still, shapes that blink, and shapes that travel across the grid indefinitely. None of them is written in the rules. There is no line that says *glider*.

That gap — between the size of the rule and the size of what the rule does — is the reason this platform exists.

### And sometimes there is no way to skip ahead

The strongest version of the point comes from a rule so small it barely qualifies as one. Rule 110 decides each cell from itself and its two neighbours, with two states. Wolfram conjectured in 1985 that it can compute anything any computer can compute; Cook proved it.[^cook] The standard term is *universal*.

For a system like that, there is no general method for answering questions about its distant behaviour that is faster than watching it happen. You cannot look at the rule and reason your way to tick ten thousand. You have to run ten thousand ticks. Wolfram named the general phenomenon **computational irreducibility**.[^nks]

### Which tells you exactly when this platform is worth anything

Take the consequence seriously and it cuts both ways, hard.

> **Where a shortcut exists, SCR is worthless. Use the shortcut.**

If a formula answers the question, the formula is faster, cheaper, better understood, and already trusted. A platform that reproduces a known closed-form result has demonstrated that the platform works. It has not learned anything about the subject. Mistaking one for the other is the most likely way this project embarrasses itself.

SCR earns its keep in the other case: where the shortcut has broken down, where the only honest way to find out is to run it, and where running it is currently too expensive or too fiddly for anyone to do at scale.

One refinement matters more than it looks:

> **Irreducibility is a property of a regime, not of a subject.**

The same subject can be reducible in one condition and irreducible in another. A fire spreading through even fuel under steady wind has a rate formula. The same fire crossing a patchy landscape near the density where it stops crossing at all does not — whether it gets through depends on the specific arrangement, and the only way to know is to run it. A Lab's most important job is knowing which regime it is standing in.

---

## What the platform is made of

Twelve parts. Each one owns something and is refused something.

1. **Cell** — the smallest thing that holds state and can affect its neighbours.
2. **World** — the complete setting for an experiment: which Cells exist, how they are arranged, what can reach what, what conditions apply, what is visible, and how it starts.
3. **Generation** — the pipeline that turns a request into a checked, tested mechanism.
4. **Plugin** — one local mechanism, written so a person can read it.
5. **Reactor** — the execution authority. It decides what actually happens.
6. **Run** — one exact execution, kept permanently, never edited.
7. **Study** — a structured question that takes more than one Run to answer.
8. **Reader** — a repeatable measurement taken from a finished Run.
9. **Corpus** — everything the platform has ever done, and the links between the parts.
10. **Search** — how accumulated work gets found again.
11. **Visualization** — evidence made visible, and time made navigable.
12. **Lab** — where a subject and its assumptions enter, and where they are held to account.

**Platform Services** — storage, execution, interfaces, delivery, operations — support all twelve and define none of them.

One line does most of the architectural work: **the Plugin proposes, and the Reactor decides.** A mechanism may suggest what should change. It may never redefine the experiment it is running inside.

---

## What this platform is not made of

A foundational document should be able to describe SCR completely without naming one programming language, library, database, model vendor, or framework. This one can, and does.

That is not fussiness. It follows directly from the platform's own promise. Runs are immutable evidence. The Corpus is the durable asset. Evidence is meant to outlive the software that produced it, be read by people who were not there, and be measured later by methods that did not exist when it was recorded.

> **Durability that rests on a technology choice is not durability.**

So the foundational requirement is a property, never a product:

> **Every mechanism the platform executes must have a representation a competent person can read, change, and hand to someone else — without the platform's help.**

That is testable. A representation passes if a person can read it, compare two versions of it, copy it, change it, review it, hand it to another person or another machine, see which capabilities it uses, and judge whether it plausibly does what it claims. It fails if any of those needs the platform running, or needs trusting the platform's own account of what the mechanism does.

Which language satisfies that property today is a real decision with real consequences. It belongs in a requirements document, where it can be revisited without disturbing anything above it. The same is true of storage, transport, interface, and execution technology: important, replaceable, and not foundational.

**What *is* foundational about technology** is two claims about capability, neither of which names a product. First, that machines can now translate meaning into mechanism cheaply — the premise the whole platform rests on, and without which there is no platform. Second, that machine translation cannot be trusted on its own, which is why everything downstream of it is checked, executed, recorded, and left open to human correction.

> **A correction to record.** SCR-F v0.2 does not hold this line. §2 states the property correctly and then names a language in the very next sentence; §17 and the §36.7 glossary go further and define the Plugin *as* an artifact of that language, and the naming has since spread through the document. A Level 1 document that names a language has made a Level 3 decision by accident and made it permanent by placing it too high. Filed as a pending amendment — see `glossary.md`.

---

## What SCR does not claim

**It does not predict anything.** A mechanism that reproduces an observed pattern is a candidate explanation. It is not proof that the real thing works that way. Calibration and validation remain the subject's own problem, solved with the subject's own tools.

**It does not explore all possible mechanisms.** What gets proposed depends on the generator, the prompt, the history already in the Corpus, and the Lab's vocabulary. Any coverage measurement describes the space SCR has defined for itself — never the space of everything a local mechanism could be.

**It does not treat fluency as authority.** A machine can write a persuasive explanation of something that did not happen. So code is checked, mechanisms are run, measurements are repeatable, provenance is kept, human corrections stay visible, and every machine account of a machine's own work is treated as interpretation rather than evidence.

**It does not claim novelty for rediscovery.** Reproducing a result the field already has in closed form is a test of the platform, and should be reported as one.

---

## Where the earlier system fits

An earlier working system demonstrated that the central idea holds: it could propose a mechanism in English, implement it, check it, run it deterministically, keep immutable histories, and let a person scrub through those histories. That is evidence, and it is why 3.x exists at all.

It is not a specification. Its grid shape, its update timing, its storage, its interfaces, and its limits were the conveniences of a small single-user tool. What carries forward is the lessons and the accumulated evidence. What does not carry forward is the accidents.

---

## Sources

[^vn]: John von Neumann, *Theory of Self-Reproducing Automata*, edited and completed by Arthur W. Burks (University of Illinois Press, 1966).
[^life]: Martin Gardner, "Mathematical Games: The fantastic combinations of John Conway's new solitaire game 'life'," *Scientific American* 223, no. 4 (October 1970): 120–123.
[^cook]: Matthew Cook, "Universality in Elementary Cellular Automata," *Complex Systems* 15, no. 1 (2004): 1–40. The conjecture is Wolfram's, from 1985.
[^nks]: Stephen Wolfram, *A New Kind of Science* (Wolfram Media, 2002), §12.6, p. 737.

Bibliographic details above were checked against published sources rather than recalled. Anything added later must meet the same standard — see `language-rules.md`.
