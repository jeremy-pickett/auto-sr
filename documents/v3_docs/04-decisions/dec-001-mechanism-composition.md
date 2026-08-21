# DEC-1 — Can more than one thing happen at once?

*Formal name: mechanism composition. Cite this record as **DEC-1**.*

**Status:** open · **Who decides:** the project owner · **Kind:** fork — the two answers are different products

> **In one sentence:** when we run an experiment, is there exactly one process going on, or can several processes run side by side and affect each other?

---

## What this is about

The platform works by writing down a **rule** — a short description of what happens to one small piece of the world, based on what's next to it. Run that rule over and over, everywhere at once, and you get behaviour.

Today, one experiment gets one rule.

Now picture a wildfire on a hillside. What's really happening is at least three separate things:

- fire spreading from burning ground to unburnt ground
- wind pushing it in a direction
- dry grass getting drier from the heat next to it

Those are three different processes. They affect each other.

**The question is whether we write that as one rule, or three rules running together.**

The same shape shows up everywhere. An infection moving through a hospital ward is one process; staff walking between rooms is another; the cleaning schedule is a third. Three things, one situation.

---

## Why it's a real question

If you allow three rules at once, you immediately have to answer five things that simply cannot come up with one rule:

**1. Do they see each other's work?**
Does the wind rule look at the hillside as it was at the start of this moment, or after the fire has already moved? Both are reasonable. They give different answers.

**2. Who goes first?**
If the order matters, then whoever picked the order has changed the outcome.

**3. What if two rules disagree?**
Suppose the experiment also includes rainfall. The fire rule says *this patch is now burning.* The rain rule says *this same patch is now soaked.* Same patch, same moment. Who wins?

**4. How is effort divided?**
There's a limit on how much work a rule may do. With three rules, does each get a third, or does each get the full amount?

**5. Who did it?**
When a patch changes, which rule changed it? We need that for the record.

### The part that actually matters

Look at question 3 again.

*"Fire beats rain"* is a rule about how the world works. It is not the fire rule. It is not the rain rule. It is a **third rule**, and somebody has to write it down.

If the software just quietly picks one — say, whichever rule happened to run last — then **the software has invented a rule nobody wrote, nobody reviewed, and nobody can see.** It changes every result. It appears in no record. Two people comparing experiments would be comparing an invisible rule neither of them knew about.

That is why this is a decision and not a detail.

---

## Your options

### A — One rule per experiment

**What it means:** to model fire properly you write one large rule that handles spreading, wind, and drying all together.

**What you get:** simplicity. No ordering, no conflicts, no invisible rules. Everything about how an experiment runs is already settled.

**What it costs:** the one big rule is hard to read and impossible to reuse. And you lose the experiment people most want to run — *keep the fire rule exactly the same, change only the wind* — because there is no separate wind rule to change.

### B — Several rules per experiment

**What it means:** fire, wind, and drying are three separate rules that run together.

**What you get:** rules that match how people actually think about their subject, are readable on their own, can be reused, and can be swapped one at a time.

**What it costs:** all five questions above become permanent parts of the platform. Every one of them changes results, so every one has to be written down, named, and recorded with each experiment. This is not a one-time cost; it is a permanent increase in how much the platform has to explain about itself.

### C — Mostly A, using recorded inputs instead

**What it means:** ask what the wind actually *is* in the experiment.

If it's a recorded wind measurement being played back — it blows, the fire responds, the wind doesn't care what the fire does — then **the wind is not a rule at all.** It's an input. Like a weather tape.

No second rule. No ordering question. No conflicts. Nothing to invent.

Several rules are only genuinely needed when two things **change each other** — a fire hot enough to alter the wind that is driving it.

**What you get:** most of B's benefit at almost none of B's cost, for most cases.

**What it costs:** the genuinely coupled cases — fire changing its own wind, an attacker reacting to a defender who is reacting to the attacker — are still unavailable, and those are often the interesting ones.

---

## What would make this easy to decide

The whole question comes down to one thing you already know more about than I do:

> **Do the Labs you care about need two things that change each other — or is one rule plus recorded inputs enough?**

That's a question about your subjects, not about software. If most Labs are fine with recorded inputs, option C is nearly free. If the interesting cases are all mutual — fire and its own wind, attacker and defender — then B is the real answer and its costs are worth paying.

Worth noting: the test for which case you're in is already written down. *Does this thing's future behaviour depend on what's happening in the experiment?* No → it's an input. Yes → it's a rule.

---

## What this is blocking right now

Five documents hold two futures open instead of one:

- `../01-core/plugins.md` — what a rule is allowed to do
- `../01-core/reactor.md` — ordering, conflicts, and effort limits
- `../01-core/runs.md` — whether the record names one rule or several
- `../01-core/worlds.md` — whether wind belongs to the setting or is a rule
- every Lab that needs more than one process, which is most of them

The wildfire Lab brief already says so in as many words: *"Wind, terrain, and fire are at least two mechanisms. Blocked on DEC-1."*

---

## The precise version

*This is the wording other documents cite. It says the same thing in the platform's own vocabulary.*

How many mechanisms participate in one Run, and in what relation: multiple Plugins, dynamic World conditions, layered mechanism stacks, or a deliberate refusal to compose. Includes the environment-as-mechanism boundary — whether a condition such as a current is a World property or a second participating mechanism (SCR-F §14).

The answer reshapes the Plugin contract, the Reactor, provenance, and every Lab template.

**Already constrained, whatever the answer:**

- The single-mechanism reading is recorded as **inheritance from the earlier system, not a decision** (SCR-F §19, §39, §45.11). It carries no standing and must not be cited as settled.
- If composition is permitted, the composition policy is declared, named, versioned, and recorded with each Run — never an incidental result of implementation order (`../01-core/reactor.md` REACTOR-17, REACTOR-18).
- The input-versus-rule test is already written (`../01-core/worlds.md` WORLD-7, WORLD-8) and stands regardless.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change from *open* to *decided*, recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** The record previously opened in platform vocabulary and was, in the project owner's words, cryptic to anyone not already inside the project. Rewritten so the stakes are legible without prior reading. **Nothing about the question changed** — the precise wording is preserved above under "The precise version", and the identifier, status, and constraints are untouched. Prior text is in version history.
