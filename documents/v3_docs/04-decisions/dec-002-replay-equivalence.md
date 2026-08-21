# DEC-2 — What does "run it again and check" promise?

*Formal name: replay equivalence. Cite this record as **DEC-2**.*

**Status:** decided (2026-08-21) · **Decided by:** the project owner · **Kind:** boundary — both answers coexist; the decision is where the line falls

> **In one sentence:** when someone re-runs one of our experiments to check it, there are two different promises they could be relying on — and they are not the same promise, they do not cost the same, and one must never quietly stand in for the other.

---

## The decision

**Reproduction under contract is the default promise for every Run. Exact replay is reserved for Runs designated evidence-grade, and designation happens at run time — never retroactively.**

**The designation rule (initial):** a Run is designated evidence-grade at creation when any of these holds —

- it belongs to a Study intended for export or publication;
- its Lab marks it evidence-grade;
- the owner flags it.

Default: not designated. A designated Run gets its full environment archived at run time; an undesignated Run records what the equivalence standard requires and nothing more. The two promises are never silently exchanged, and a downgrade (an environment no longer archived) is recorded, dated, and attributed — those rails predate this decision and stand.

**Alternatives considered and rejected:**

- *Exact replay for everything* — rejected on cost: archiving a full software environment per Run, forever, across a planned scale-up of orders of magnitude, paid mostly for Runs nobody will ever audit.
- *Contract for everything* — rejected on irreversibility: the Runs that end up mattering would carry only the weaker claim, and an environment never archived can never be archived later.

**Reasoning:** the cost of the strong promise lands only where the strong claim is needed, and the one-way door (no retroactive strengthening) is handled by making designation cheap and available at run time rather than by paying for everything.

**What would reopen this:**

1. An audit need arrives for a Run that could not have been designated in advance — evidence the designation rule or the default is wrong.
2. Designation ends up applied to nearly every Run — the split has failed in practice; reconsider archiving everything.
3. Environment archival proves far cheaper at scale than assumed — the cost argument against exact-for-everything weakens.

**Documents to revise now that this is decided:** `../02-platform/storage.md` (unblocked — owes the archival machinery for designated Runs and the equivalence-standard record-keeping); `../03-quality/repeatability.md` (REPEAT-7's equivalence standard now has a home: it is requirements work owed by storage and repeatability, no longer waiting on a decision); `../01-core/reactor.md` and `../01-core/runs.md` (REACTOR-21/22, RUN-15/16 already state both promises; their "DEC-2 owns which applies where" lines now point at a decided record).

---

## What this is about

Every experiment here is recorded completely, so it can be checked later. But "checked" hides two different things, and both show up in ordinary professional life.

**A hospital lab has both.** Run the same blood sample through the same analyzer again: you should get the same numbers. That checks the machine and the record. Send a second sample to a different laboratory for confirmatory testing: you expect results that agree within the accepted margin — not identical digits. That checks the *finding*. The first can fail while the finding stands (the analyzer was replaced last month). The second can fail while the record is flawless (the finding was wrong).

**Digital evidence has both.** A forensic disk image with a matching checksum proves the copy is exact, bit for bit — that is the first kind. An independent examiner reaching the same conclusion from their own tools is the second kind. Nobody in that field confuses the two, because a courtroom will ask which one you are claiming.

Our two promises, named:

> **Exact replay** — re-run it with everything preserved, get the same values to the last digit. The strongest claim, and the most expensive: it means archiving not just the experiment but the exact software environment it ran in.

> **Reproduction under contract** — a later, improved version of the platform runs the same declared experiment and matches the result *within a written standard of "close enough."* The claim that survives time, because software changes and evidence is meant to outlive it.

---

## Why it's a real question

**Exact replay is fragile for a boring reason.** Computers doing arithmetic on decimal numbers can produce answers that differ in the last decimal places depending on the order things were added up — like rounding pennies at different points in a long calculation. Change the software, the hardware, or the order of one sum, and the final digits can shift while nothing about the experiment has changed. So keeping this promise means freezing and archiving the whole environment, forever, per experiment.

**Reproduction under contract is arguable for a boring reason.** "Close enough" has to be written down in advance — what must match, within what margin — or every future check becomes an argument about what somebody meant. Someone has to write that standard, and it has to be versioned.

If we do not say which promise a given experiment carries, people will assume the stronger one. Then one day a check fails on last-digit differences that mean nothing, or worse — a real discrepancy gets waved off as rounding. Both failures come from the same cause: two promises wearing one name.

---

## Your options

The promises coexist. What is undecided is where each applies.

### A — Exact replay for everything

**What you get:** the strongest possible claim on every experiment.
**What it costs:** archiving a full software environment for every Run, forever. At the planned scale, this is the most expensive option on the table, paid mostly for Runs nobody will ever audit.

### B — Reproduction under contract for everything

**What you get:** durability. Every result checkable against every future version of the platform.
**What it costs:** the Runs that end up mattering — the ones behind a published finding, a dispute, a hearing — carry only the weaker claim, and that cannot be fixed afterwards. You cannot retroactively archive an environment you didn't keep.

### C — Contract by default, exact replay for designated evidence

**What you get:** the cost lands only where the strong claim is needed.
**What it costs:** someone has to designate which Runs get the strong promise, at the time they run — and the written "close enough" standard still has to exist for everything else. Two obligations instead of one, each smaller.

---

## What would make this easy to decide

One question, and it is about how the evidence will be used, not about software:

> **Which of this platform's results will ever need to survive a hostile audit — and can you tell at the time they run?**

If yes: option C is the natural shape, and the remaining work is writing the designation rule and the equivalence standard. If you can't tell in advance which Runs will matter, that is an argument pushing toward A for some whole class of work, with the storage bill accepted knowingly.

---

## What this is blocking right now

- `../02-platform/storage.md` — how much must be kept per Run is *the* open question of that document
- `../01-core/reactor.md` and `../01-core/runs.md` — both hold the two promises open (REACTOR-21, RUN-15)
- `../03-quality/repeatability.md` — the equivalence standard it requires (REPEAT-7) has no owner until this is decided

**Already settled, whatever the answer:** every Run records which promise it carries; the two are never silently exchanged; a downgrade (an environment no longer archived) is recorded, dated, and attributed (RUN-16).

---

## The precise version

*This is the wording other documents cite. It says the same thing in the platform's own vocabulary.*

Which replay promise the platform makes, for which classes of evidence, at what storage and version-discipline cost.

**The two promises are not alternatives.** An earlier framing of this record posed them as a choice; that framing is superseded (see the record history below). They are two distinct, separately named promises that can and should coexist:

> **Exact replay** — given the archived implementation, Reactor build, environment, random material, Starting State, and Run Contract, the recorded state is reproduced value for value. The strongest forensic claim, and the most expensive to keep, because it requires archiving the environment rather than only the inputs.

> **Reproduction under contract** — a later Reactor executes the same declared experiment and meets a stated equivalence standard, even where implementation details differ. The stronger long-term claim, because software changes and evidence is meant to outlive it.

What is open is which promise applies to which evidence, what the equivalence standard says, and what each costs. Until decided, the phrase "exact or contractually equivalent" is **cited as a fork** and never resolved locally (SCR-F §19).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change from *open* to *decided*, recorded rather than assumed.

---

## Record history

**2026-08-21 — decided.** Option C adopted by the project owner in session: reproduction under contract as default, exact replay for Runs designated evidence-grade at run time, with the initial designation rule, rejected alternatives, and reopening triggers recorded above. First record in the registry to reach *decided*.

**2026-08-21 — rewritten for readability.** Restructured into the plain-question format (stakes first, precise wording preserved above). Nothing about the question, the identifier, the status, or the constraints changed. Prior text is in version history.

**2026-08-20 — reframed from a binary choice to two coexisting promises.**

*Was:* "Bit-exact replay versus contractually equivalent replay: which the platform promises …", phrased throughout as a choice between two mutually exclusive options.

*Now:* two separately named promises, with the open question being which applies where and at what cost.

*Why:* an external critique of the core contract set observed that overloading one word until every future argument is really an argument about which meaning somebody intended is the actual hazard here, and that both promises are independently valuable. The concrete reason they differ is recorded in `../01-core/reactor.md` §9: arithmetic on real numbers in a computer is not associative, so a change in how a value is computed can break the first promise while leaving the second intact.

*Raised by:* external critique, 2026-08-20, accepted by the project's human owner. This reframes the question rather than answering it, which is the contribution SCR-F §45's closing paragraph asks reviewers for.

*What did not change:* the identifier, the status, and the fact that no document may resolve this locally. DEC-2 is still open.

*Still outstanding:* SCR-F §19 and §40.1 still phrase this as "exact or contractually equivalent" and as a single fork. That correction is pending as an amendment to Foundations.
