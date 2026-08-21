# Transport

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/transport.md`
**Identifier namespace:** `TRANS-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §33, §39 · DEC-13 · `../01-core/runs.md`, `../01-core/visualization.md`, `02-platform/storage.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> Transport's one product is a feeling: that scrubbing through a finished experiment is **navigation, not loading.** Everything here serves that, or serves getting long-running work's progress to a watcher honestly.

---

## 1. Playback

**TRANS-1.** Stepping, scrubbing, and jumping through a completed Run feel immediate. The budget is shared with storage (STORE-9): reconstruction plus delivery, together, inside the threshold where a person perceives response rather than wait.

**TRANS-2.** Playback transport reads finished history and nothing else (RUN-21). No playback interaction executes anything server-side — a view that would need to is flagged by the view layer (VIS-9), not smuggled through transport.

**TRANS-3.** State payloads use a compact, versioned, framed binary encoding. The earlier system demonstrated both sides of this: framed binary held up; state nested inside general-purpose text encoding did not survive contact with real payload sizes. Recorded as evidence; the specific framing is revisable behind the version field.

**TRANS-4.** Wide payloads degrade deliberately: a client that cannot take a full-resolution frame gets a declared reduction (subsampling, region, fewer properties) that names itself — never a silently degraded frame presented as the record.

---

## 2. Progress

**TRANS-5.** Long-running work streams progress to its watcher (API-6). Progress events are operational telemetry with one job — keeping a person informed — and the permanent record is identical whether anyone watched or not (API-7).

**TRANS-6.** Whether work rides one long-lived request or a queued job with a subscribed watcher is `jobs-and-workers.md`'s concern, not a transport commitment. The earlier system's single-streamed-request design is inheritance (§39); transport owes progress delivery under either shape.

---

## 3. The formats deadline

**TRANS-7.** What the planned advanced views require on the wire — time-mapped geometry, multi-Run comparison payloads, similarity-map data — is DEC-13's question, and transport shares its deadline: answered before the large-scale formats freeze. A view too expensive to feed is a view that never ships, and the expense is set here and in storage, now.
