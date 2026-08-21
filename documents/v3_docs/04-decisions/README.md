# Decision Registry

**Document class:** Level 2 — Architecture Decisions (index) · **Status:** draft
**Indexes:** SCR-F v0.2 §40 · **Cites:** SCR-F v0.2 §36.1–§36.5, §40; F-22

> **Why this directory exists.** SCR-F deliberately does not resolve every consequential choice. It insists that consequential choices be *named*, so they are decided in decision records with evidence — rather than answered accidentally during implementation, or worse, answered differently by different model-written documents that each thought the answer was obvious (§40).
>
> **Naming a fork is not deciding it.**

## How to read these records

Every record leads with the plain question — readable without knowing this platform's vocabulary — and preserves the precise internal wording under "The precise version," which is what other documents cite. Two renderings, one meaning (`../00-start-here/language-rules.md`, "Documents that leave the building"). Each record states its **kind**: a *fork* (the answers are different products), a *boundary* (where a line falls), a *placement* (who owns something), *deferred detail* (constraints registered, machinery best decided against real use), or a *standing obligation* (never closes; gets an owner and a ledger).

**Real data is coming.** After the documentation phase, every Lab receives real-world data, and these records are expected to be stressed by it. That is the plan working: real data arriving is the natural reopening trigger for most of what is recorded here, and the amendment machinery exists for exactly that moment.

## Precedence

For a decided question, the governing DEC record outranks any document's local phrasing — including SCR-F's own (§36.4.2). For conceptual meaning, Foundations still outranks everything.

## Status vocabulary

| Status | Meaning |
|---|---|
| **open** | Not decided. No document may resolve it locally (F-22). |
| **open; placement decided** | The ownership boundary is already foundational law; the mechanics are open. |
| **open; stance constrained** | Undecided, but SCR-F imposes a constraint any answer must satisfy. |
| **open; leading candidate/formulation/lean recorded** | Undecided; a concrete proposal is recorded so the decision can be made against something specific. |
| **partially decided** | Part of the question is settled and cited; the rest is open. |
| **decided** | Resolved and adopted. Adoption is a human act (§36.3). |

Identifiers are permanent and never reused. A retired decision is marked retired, with the amendment that retired it (§36.5).

## Foundational forks surfaced by SCR-F v0.2 (§40.1)

| ID | The plain question | Formal name | Status |
|---|---|---|---|
| [DEC-1](dec-001-mechanism-composition.md) | Can more than one thing happen at once? | Mechanism composition | open — *the largest unnamed decision in v0.1* |
| [DEC-2](dec-002-replay-equivalence.md) | What does "run it again and check" promise? | Replay equivalence | open; framing amended |
| [DEC-3](dec-003-temporal-semantics.md) | Whose clock is it, and must everything tick together? | Temporal semantics | open; placement decided |
| [DEC-4](dec-004-study-inference-discipline.md) | What does "confident" mean here? | Study inference discipline | open; stance constrained |
| [DEC-5](dec-005-home-of-semantic-translation.md) | Who owns the translating? | The home of semantic translation | open |
| [DEC-6](dec-006-2x-corpus-migration.md) | What happens to the old library? | 2.x corpus migration | partially decided |

## Open questions carried forward from v0.1 (§40.2)

| ID | The plain question | Formal name | Status |
|---|---|---|---|
| [DEC-7](dec-007-plugin-contract-surface.md) | What is a rule allowed to do? | Plugin contract surface | open |
| [DEC-8](dec-008-world-storage.md) | One filing system for two shapes of world? | World storage | open |
| [DEC-9](dec-009-study-planner-autonomy.md) | How much may the platform guess before asking? | Study planner autonomy | open |
| [DEC-10](dec-010-reader-trust-presentation.md) | How does a measurement admit its doubts? | Reader trust presentation | open |
| [DEC-11](dec-011-corpus-identity.md) | When are two rules the same rule? | Corpus identity | open |
| [DEC-12](dec-012-search-similarity-separation.md) | Similar how, exactly? | Search similarity separation | open |
| [DEC-13](dec-013-visualization-scale.md) | What must we keep so the pictures never need a re-run? | Visualization scale | open |
| [DEC-14](dec-014-video-provenance.md) | What travels with a forty-second clip? | Video provenance | open |
| [DEC-15](dec-015-lab-governance.md) | When is a Lab more than an experiment? | Lab governance | open |
| [DEC-16](dec-016-security-isolation.md) | How do we contain code we didn't write? | Security isolation | open |
| [DEC-17](dec-017-model-independence.md) | What changes when we change the AI? | Model independence | open |
| [DEC-18](dec-018-human-plugin-edits.md) | When a person edits a rule by hand, what happens to its story? | Human Plugin edits | open; substantially narrowed |
| [DEC-19](dec-019-live-work.md) | Watching live versus the permanent record | Live work | open |
| [DEC-20](dec-020-external-calibration.md) | How do we hand results to the real experts without overclaiming? | External calibration | open |

## Raised by the core contract set (2026-08-20)

Registered while writing `../01-core/`, after external critique. These were not in SCR-F §40; adding them is a pending amendment to that section (§36.5).

| ID | The plain question | Formal name | Status |
|---|---|---|---|
| [DEC-21](dec-021-locality-and-reach.md) | How far can a rule reach? | Locality and reach | open; leading formulation recorded |
| [DEC-22](dec-022-cell-schema-multiplicity.md) | Must every participant be the same kind of thing? | Cell schema multiplicity | open; lean recorded |
| [DEC-23](dec-023-starting-state-ownership.md) | Who sets up the board? | Starting State ownership | open; leading candidate recorded |
| [DEC-24](dec-024-the-cellular-budget.md) | How much can we bend before it isn't the same instrument? | The cellular budget | open; no owner assigned |

**DEC-24 is different in kind from every other record here.** The others ask what the platform should do. DEC-24 asks who is counting what the others cost in aggregate — four of the five properties that make this recognisably a local-mechanism instrument are currently under negotiation, each argued soundly on its own, with no one watching the total. Its own record proposes starting with the floor: what stays true regardless of how DEC-1, 3, 21, and 22 land.

## Which records actually gate work

Not all 24 block anything today. The ones that do:

- **DEC-1, DEC-21, DEC-22** gate honest design of most non-grid Labs, and DEC-1 gates the final Plugin/Reactor contracts.
- **DEC-2 (with DEC-8, DEC-13)** gates `../02-platform/storage.md`.
- **DEC-16** gates `../02-platform/execution-safety.md` and any multi-user deployment.
- **DEC-7** closes after DEC-1 and DEC-3, by design.
- Everything else is either constrained-and-waiting (safe rails already in the requirements) or explicitly best decided against real use.

## Candidates not yet registered

SCR-F §45.16 asks which consequential choice is still being made by accident. Three are flagged in the tree but not registered, because registering a DEC is an amendment to §40 (§36.5):

- **Exploration strategy** — nothing among the twelve components owns *deciding what to generate next*. Flagged in `../01-core/generation.md` §9.
- **Cost and budget** — no principle covers the economics of generation, repair, or Study fan-out, against a planned scale-up of several orders of magnitude (§22.1). Flagged in `../02-platform/jobs-and-workers.md`.
- **Ownership of evidence** — the Corpus is described as one durable body with no notion of whose evidence it is. Flagged in `../02-platform/identity-and-access.md` and `../01-core/corpus.md`.

## Closed by the core contract set

The declaration chain — found independently by all five core documents and left unowned by the seams pass — is **closed, not registered**. It needed a record rather than a component: the **Run Contract**, produced by the Reactor at admission and stored permanently by the Run. Defined in `../01-core/runs.md` §2.

## Adding a record

New identifiers continue the sequence and are never reused. A record is added by amendment to SCR-F §40, with the evidence attached (§36.5) — a downstream document that discovers a fork flags it here; it does not decide it.
