# DEC-2 — Replay equivalence

**Document class:** Level 2 — Architecture Decision · **Status:** open; framing amended
**Registered by:** SCR-F v0.2 §40.1
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

Which replay promise the platform makes, for which classes of evidence, at what storage and version-discipline cost.

**The two promises are not alternatives.** An earlier framing of this record posed them as a choice; that framing is superseded (see the amendment record below). They are two distinct, separately named promises that can and should coexist:

> **Exact replay** — given the archived implementation, Reactor build, environment, random material, Starting State, and Run Contract, the recorded state is reproduced value for value. The strongest forensic claim, and the most expensive to keep, because it requires archiving the environment rather than only the inputs.

> **Reproduction under contract** — a later Reactor executes the same declared experiment and meets a stated equivalence standard, even where implementation details differ. The stronger long-term claim, because software changes and evidence is meant to outlive it.

What is open is which promise applies to which evidence, what the equivalence standard says, and what each costs.

## Why it is consequential

These are different platforms, not different phrasings of one platform. They imply different storage volumes, different version discipline in the Reactor, and different strength of evidence claims. §19 states the practical risk plainly: two downstream documents left to interpret "exact or contractually equivalent" will pick different readings within a month.

## What is already constrained

Until decided, the phrase is **cited as a fork** and never resolved locally (§19).

## What this record constrains

- `../01-core/reactor.md`
- `../01-core/runs.md`
- `../02-platform/storage.md`
- `../03-quality/repeatability.md`

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.

---

## Amendment record

**2026-08-20 — reframed from a binary choice to two coexisting promises.**

*Was:* "Bit-exact replay versus contractually equivalent replay: which the platform promises …",
phrased throughout as a choice between two mutually exclusive options.

*Now:* the wording above — two separately named promises, with the open question being which applies
where and at what cost.

*Why:* an external critique of the core contract set observed that overloading one word until every
future argument is really an argument about which meaning somebody intended is the actual hazard
here, and that both promises are independently valuable. The concrete reason they differ is also now
recorded in `../01-core/reactor.md` §9: arithmetic on real numbers in a computer is not associative,
so a change in how a value is computed can break the first promise while leaving the second intact.

*Raised by:* external critique, 2026-08-20, accepted by the project's human owner. This reframes the
question rather than answering it, which is the contribution SCR-F §45's closing paragraph asks
reviewers for.

*What did not change:* the identifier, the status, and the fact that no document may resolve this
locally. DEC-2 is still open.

*Still outstanding:* SCR-F §19 and §40.1 still phrase this as "exact or contractually equivalent"
and as a single fork. That correction is pending as an amendment to Foundations.
