# Generation

**Document class:** Level 3 — Requirements (provisional: §37 assigns no level; see `../README.md`) · **Status:** draft
**Path:** `01-core/generation.md`
**Cites:** SCR-F v0.2 §16, §16.1–§16.6, §38.1, §42, §43; F-2

> **Stub — not written, not adopted.** This file exists so downstream documents have a stable citation target (SCR-F v0.2 §36.2) and so the tree's shape is reviewable before two hundred documents land in it. Per §36.3 a draft may not be relied upon by downstream documents. Per §36.6 a model writing here must cite the specific SCR-F sections it depends on, flag ambiguity rather than smooth it over, refuse to answer a DEC-owned question locally, and keep Lab vocabulary out of this document.

---

## What this document owes

- The Propose → Write → Check → Test → Repair → Deliver pipeline as a testable contract, stage by stage (§16.1–§16.6).
- Repair governance: how many attempts, what a repair may and may not change, and the provenance a repair must preserve (§16.5).
- **The semantic repair account** — a plain-language statement of what changed mechanistically — together with its permanent caveat that the account is interpretation, Reader-class and disputable, never evidence that the repair was faithful (§16.5, §43).
- Prompt and template versioning, and the rule that fully rendered model inputs are stored (§32) rather than reconstructed later.
- Coverage and exploration inputs, stated so that §42's non-claim holds: coverage describes the space SCR defined for itself, never the space of all local mechanisms.
- The boundary Generation does not cross: it is a proposal system and does not get to declare a mechanism scientifically useful because the code compiled (§16, §34).

## Decisions this document must not resolve locally

- **DEC-5 — The home of semantic translation.** *Open.*
- **DEC-17 — Model independence.** *Open.*

## An ownership question this document should not answer alone

Nothing among the twelve components clearly owns **exploration strategy** — deciding which experiment is worth generating next. In 2.x that role belonged to the coverage map feeding Stage A. Generation owns propose-through-deliver, Search owns retrieval, Study owns a question someone already has. If writing this document requires an answer, register it as a new DEC rather than settling it here (§36.5, F-22).
