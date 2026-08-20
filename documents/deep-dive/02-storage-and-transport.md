# Storage & Transport

> **Release 2.2.1** · documented 2026-08-20 · **updated for 2.2.1.**
> `db.py` gained three session tables and four functions that write them, all serving the
> system page. Nothing about tick encoding, reconstruction, the cache, or binary framing
> changed — §3 through §8 below are unchanged from 2.2.0 and were re-verified against the
> source. The new material is §1's "The session tables" and a qualification added to §2,
> because the release introduces the first `UPDATE` statements in this module that fire on
> ordinary traffic, and the immutability argument has to account for them.

This is part two of a six-part deep-technical series on Autonomous Semantic Ruliology (ASR), a single-user local app where an LLM invents cellular-automaton rules and a harness validates, runs, and permanently archives them. This document covers the subsystem that makes the archive durable and playback fast: the SQLite library (`backend/asr/storage/db.py`), tick payload encoding (`backend/asr/storage/encoding.py`), reconstruction and its cache (`backend/asr/storage/reconstruct.py`), and the binary wire framing that carries grids to the browser (`backend/asr/api/framing.py`).

The governing idea, stated in `backend/asr/storage/db.py:1-6`, is that **recorded history is immutable**:

```python
"""The library database (spec section 12): SQLite, single file, WAL.

Recorded history is immutable — nothing here updates a tick row, and
the only run columns ever updated are the user's behavior override and
flag (REQ-11.3, applied at the API layer).
"""
```

Every design decision in this document — the schema, the encoding scheme, the cache, the wire format — exists in service of that sentence and of one performance constraint: a run can be tens of thousands of ticks over a large grid, and the frontend needs to scrub through it at 30fps without re-deriving the world from tick zero every time.

---

## 1. Schema and WAL

The whole library lives in one SQLite file, opened by `connect()` in `backend/asr/storage/db.py:173-184`:

```python
def connect(path) -> sqlite3.Connection:
    # check_same_thread off: FastAPI may run a request's dependency
    # setup, endpoint body, and teardown on different threadpool
    # threads. Every request still gets its own private connection, so
    # the connection is never used by two threads at once.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    _ensure_columns(conn)
    return conn
```

Two details here matter more than they look. First, `check_same_thread=False` is not a concurrency shortcut — the comment is explicit that this is about FastAPI's threadpool moving a *single* request's connection across threads during its lifecycle, not about sharing one connection between requests. Every route gets its own connection via a dependency (`get_db` in `backend/asr/api/routes.py:30-35`), opened and closed per request. Second, `PRAGMA journal_mode=WAL` — Write-Ahead Logging — is what lets that per-request-connection model actually perform: WAL lets readers proceed concurrently with a writer instead of blocking behind SQLite's default rollback-journal exclusive lock. Given that a run save (`save_run`) can insert hundreds of tick rows in one transaction while other requests are concurrently listing the library or fetching playback grids, WAL is the difference between a responsive app and one that serializes on every write.

### The five tables

The full DDL is in `SCHEMA` at `backend/asr/storage/db.py:15-142`. Reading it top to bottom:

**`rules`** (`db.py:16-50`) is the generated-artifact record — one row per invented rule, whether it worked or not:

```sql
CREATE TABLE IF NOT EXISTS rules(
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    mode TEXT NOT NULL DEFAULT 'new',
    parent_rule_id INTEGER REFERENCES rules(id),
    change_note TEXT,
    description TEXT NOT NULL,
    reasoning TEXT,
    kinds INTEGER NOT NULL,
    neighbors TEXT NOT NULL,
    reach INTEGER NOT NULL,
    uses_json TEXT NOT NULL DEFAULT '[]',
    reads_json TEXT NOT NULL DEFAULT '[]',
    modifiers_json TEXT NOT NULL DEFAULT '[]',
    semantic_slots_json TEXT NOT NULL DEFAULT '{}',
    assign_json TEXT NOT NULL DEFAULT '{}',
    suggested_display_json TEXT NOT NULL DEFAULT '{}',
    requested_shape TEXT,
    observed_shape TEXT,
    concepts_json TEXT NOT NULL DEFAULT '[]',
    source_code TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    status TEXT NOT NULL,               -- ok | broken
    failed_check TEXT,
    error_text TEXT,
    engine_version TEXT NOT NULL,
    prompt_set_hash TEXT,
    modifier_catalog_hash TEXT,
    helper_version INTEGER,
    model_id TEXT,
    model_params_json TEXT,
    stage_a_rendered TEXT, stage_a_raw TEXT,
    stage_b_rendered TEXT, stage_b_raw TEXT,
    repair_rendered TEXT, repair_raw TEXT
);
```

Note that `status` is `ok | broken`, not `ok | rejected | deleted` — a rule that fails validation is still stored, with `failed_check` and `error_text` recording why. This is the storage-layer half of "every result, including failures, accumulates in a permanent library": there is no code path that discards a generation attempt. The `stage_a_rendered` / `stage_a_raw`, `stage_b_rendered` / `stage_b_raw`, and `repair_rendered` / `repair_raw` columns store the fully rendered prompts and the model's raw responses for all three generation phases — this is REQ-12.4.1's requirement that a template *hash* is not enough, because it can't reconstruct the exact coverage summary that was injected into Stage A at generation time, and that summary is itself the interesting research artifact.

**`runs`** (`db.py:52-70`) is one execution of a rule to completion:

```sql
CREATE TABLE IF NOT EXISTS runs(
    id INTEGER PRIMARY KEY,
    rule_id INTEGER NOT NULL REFERENCES rules(id),
    created_at TEXT NOT NULL,
    start_seed INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    max_ticks INTEGER NOT NULL,
    ticks_run INTEGER NOT NULL,
    is_canonical INTEGER NOT NULL DEFAULT 0,
    stopped_because TEXT NOT NULL,      -- frozen | looping | ran_out | too_slow
    loop_length INTEGER,
    pattern_settled_at INTEGER,
    guessed_behavior TEXT NOT NULL,
    guess_confidence TEXT NOT NULL,
    user_behavior TEXT,
    user_flagged INTEGER NOT NULL DEFAULT 0,
    engine_version TEXT NOT NULL
);
```

`user_behavior` and `user_flagged` are the two columns that ever get updated after insert — everything else on this row is written once, at `save_run` time, and never touched again. `is_canonical` marks a rule's first run, the only one that counts toward the Stage A coverage map (REQ-8.6) — reruns from `POST /rules/{id}/runs` are never canonical, per the route table in the spec.

**`ticks`** (`db.py:72-84`) is the actual archived history, one row per tick per run:

```sql
CREATE TABLE IF NOT EXISTS ticks(
    run_id INTEGER NOT NULL REFERENCES runs(id),
    tick INTEGER NOT NULL,
    payload_encoding TEXT NOT NULL,     -- snapshot | sparse | dense
    payload_blob BLOB NOT NULL,
    variety REAL NOT NULL,
    cells_changed INTEGER NOT NULL,
    kind_quiet_for INTEGER NOT NULL,
    kind_counts_json TEXT NOT NULL,
    state_fingerprint BLOB NOT NULL,
    pattern_fingerprint BLOB NOT NULL,
    PRIMARY KEY (run_id, tick)
);
```

`payload_blob` is the compressed, framed array data discussed in depth in section 3. `state_fingerprint` and `pattern_fingerprint` are the blake2b-128 hashes described in REQ-9.7.1–9.7.5 — the computational fingerprint (everything future-relevant: rule-owned arrays, modifier arrays, the derived-array dependency set, scheduler phase, RNG state where applicable) and the pattern fingerprint (`kind` only, observation-only, never used to stop a run). Storing both per tick, rather than deriving them on read, is what lets the run loop and any later auditing tool answer "did this loop, and when" without re-simulating.

**`modifier_catalog`** (`db.py:86-95`) and **`rejections`** (`db.py:97-109`) round out the original schema: the read-only catalog of harness-applied modifiers (`weight`, `stubbornness`, `rate`, …), and a record of every Stage A/B/C rejection that never became a stored rule at all — `rejections` exists specifically so a validation failure that happened *before* a `rules` row could be created (e.g., Stage A produced an unparseable declaration) still leaves a trace.

Two indexes back the query patterns the API actually runs:

```sql
CREATE INDEX IF NOT EXISTS rules_by_status_shape ON rules(status, requested_shape);
CREATE INDEX IF NOT EXISTS runs_by_rule_canonical ON runs(rule_id, is_canonical);
```

which is REQ-12.3's requirement that `ticks(run_id, tick)`, `rules(status, requested_shape)`, and `runs(rule_id, is_canonical)` all be indexed — the first is free because it's the `ticks` primary key.

### Schema evolution: `CREATE TABLE IF NOT EXISTS` isn't enough

Below the original five tables, `SCHEMA` also declares `favorites`, `comments`, and `user_profiles` — added later, in the Firebase Authentication and social-features work. The comment directly above `favorites` (`db.py:114-116`) explains why a brand-new table can just use `CREATE TABLE IF NOT EXISTS` while a *column* added to an existing table cannot:

```sql
-- A brand-new table, never existed before -- CREATE TABLE IF NOT
-- EXISTS is exactly the right idempotent mechanism here, unlike a
-- column added to a table that already exists (see _ensure_columns).
```

Editing the `CREATE TABLE rules(...)` text to add a column does nothing to a database file that already exists on disk — `IF NOT EXISTS` means SQLite sees the table is already there and skips the whole statement, columns and all. So additive schema changes to *existing* tables go through a second mechanism, `_ensure_columns` (`db.py:145-170`), run on every `connect()`:

```python
def _ensure_columns(conn) -> None:
    """Additive-only schema evolution beyond CREATE TABLE ... IF NOT
    EXISTS, which is a no-op on a table that already exists — editing
    the CREATE TABLE text above does nothing for a live database, it
    only affects brand-new ones. Each new column is guarded by a
    PRAGMA table_info check, so this is safe and cheap to run on every
    connect(). This function, not the CREATE TABLE text, is the source
    of truth for schema changes made after a table's first release.
    """
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(rules)")}
    if "owner_uid" not in existing:
        conn.execute("ALTER TABLE rules ADD COLUMN owner_uid TEXT")
    if "visibility" not in existing:
        conn.execute(
            "ALTER TABLE rules ADD COLUMN visibility TEXT NOT NULL DEFAULT 'public'"
        )
    if "spark" not in existing:
        conn.execute("ALTER TABLE rules ADD COLUMN spark TEXT")
    if "title" not in existing:
        conn.execute("ALTER TABLE rules ADD COLUMN title TEXT")
    if "slug" not in existing:
        conn.execute("ALTER TABLE rules ADD COLUMN slug TEXT")
    conn.execute("CREATE INDEX IF NOT EXISTS rules_by_owner ON rules(owner_uid)")
    conn.execute("CREATE INDEX IF NOT EXISTS rules_by_visibility ON rules(visibility)")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS rules_by_slug ON rules(slug)")
    conn.commit()
```

Each new column is guarded by an explicit `PRAGMA table_info` membership check before the `ALTER TABLE`, so running this against an already-migrated database is a cheap no-op, and running it against a pre-Firebase database (from before `owner_uid`/`visibility`/`spark`/`title`/`slug` existed) migrates it in place. This function — not the `CREATE TABLE` text above it — is the actual source of truth for what happened to a table's shape after its first release. `owner_uid` and `visibility` are the Firebase-auth-phase columns (personal library, public/private choice at creation); `spark`, `title`, and `slug` are later naming/creative-hint features, added the same way.

### The session tables (new in 2.2.1)

Release 2.2.1 added three more tables, all of them feeding the system page (`#/system`, documented in parts 5 and 6). They are a different *kind* of data from everything above, and the distinction is the most important thing in this subsection: **`rules`, `runs`, and `ticks` are recorded history; these are operational telemetry.** History is immutable and permanent (REQ-11.3). Telemetry is mutable by design — every row here is written to be overwritten — and losing all three tables would cost the system page its contents and cost the library nothing. Nothing in the corpus, the coverage map, Stage A context, or any fingerprint reads them.

**`generation_sessions`** (`db.py:146-157`) is one row per `POST /rules/generate`:

```sql
CREATE TABLE IF NOT EXISTS generation_sessions(
    id TEXT PRIMARY KEY,
    owner_uid TEXT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    stage TEXT NOT NULL,
    outcome TEXT,                       -- ok | broken | generation_failed
    rule_id INTEGER REFERENCES rules(id),
    error_text TEXT,
    model_id TEXT
);
CREATE INDEX IF NOT EXISTS gen_sessions_by_started ON generation_sessions(started_at);
```

The `id` is not new. It is the eight-hex-character `gen_id` that already existed inside `generation/pipeline.py` purely to correlate log lines from concurrent generations; 2.2.1 promotes it from a logging convenience to a persisted primary key, which is why the table's own comment describes it as turning that id "into a persisted, queryable record of one `POST /rules/generate` call." How the rows get filled — a single wrapper around `emit()` rather than a write at each pipeline stage — is part 4's territory.

Note `outcome`'s three values against `rules.status`'s two. A rule row is `ok` or `broken`; a *generation* can also end as `generation_failed`, which is the case where no rule row was ever created at all (Stage A returned something unparseable, the model refused, the API call itself failed). That third outcome is precisely the case the older `rejections` table exists for, and the two are complementary rather than redundant: `rejections` records *what was rejected and why*, as generator-quality corpus data; `generation_sessions` records *that an attempt happened, when, and how long it took*, as operational data.

**`app_sessions`** (`db.py:163-171`) is in the schema and unused. It was the first presence design — one row per browser tab, updated by a client-side heartbeat — and its comment says what happened to it:

```sql
-- Presence, first attempt: one row per browser tab, updated by a client
-- heartbeat. Retired in favor of http_sessions below (a real HTTP session
-- needs no client cooperation at all -- the request traffic that already
-- happens is enough). Left in the schema, unused, rather than dropped.
```

Leaving a dead table in the schema rather than dropping it is a deliberate call worth naming, because the alternative looks tidier and is worse. Dropping it would mean either a destructive migration against a live database that already has rows, or a `DROP TABLE IF EXISTS` that silently discards data on every single `connect()` — and the table costs nothing to keep: no code queries it, no index is maintained on write because nothing writes. The `_ensure_columns` step even carries a migration for it (`db.py:216-218`, adding a `status` column) from the brief window when it was live, which is a small honest artifact of the retirement rather than something to clean up.

**`http_sessions`** (`db.py:176-186`) is what replaced it — the colloquial HTTP session, one row per session cookie:

```sql
CREATE TABLE IF NOT EXISTS http_sessions(
    id TEXT PRIMARY KEY,
    owner_uid TEXT,
    ip_address TEXT,
    user_agent TEXT,
    started_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    last_path TEXT,
    request_count INTEGER NOT NULL DEFAULT 0
);
```

The design argument is in the comment: this one is "updated by the session middleware (api/app.py) on every request — no client cooperation required, so no client bug can leave it stale or wrong." That is the whole lesson of the retirement. A heartbeat is a promise the client makes and can break in a dozen ways (a backgrounded tab throttled by the browser, an unmount that never fires, a network blip, a bug in the hook); request traffic is something the server observes directly and cannot be lied to about. The trade is resolution — ordinary browsing produces requests far sparser than a fixed 20-second heartbeat did, which is why the system page's "active" window is two minutes rather than something tight (part 5, §11).

**The four writer functions** (`db.py:320-380`) are small, and two of them carry defensive SQL worth reading closely.

`finish_generation_session` (`db.py:334-350`) ends its `UPDATE` with `WHERE id=? AND finished_at IS NULL`:

```sql
UPDATE generation_sessions
   SET finished_at=?, stage='complete', outcome=?, rule_id=?, error_text=?
 WHERE id=? AND finished_at IS NULL
```

That guard exists because this function has two callers racing to be the one that finalizes a row — the pipeline's own `complete` event, and a catch-all exception handler in `stream.py` that acts as a safety net for failures the pipeline didn't already turn into a `complete`. Without the guard, a failure occurring *after* a perfectly successful generation (the code comment's example: applying a title) would overwrite a real `ok` outcome with a failure. The guard makes the second finalize a silent no-op instead, so the first writer wins and the row keeps the truthful outcome.

`touch_http_session` (`db.py:352-380`) uses an upsert whose `owner_uid` handling is the interesting part:

```sql
ON CONFLICT(id) DO UPDATE SET
    owner_uid=COALESCE(excluded.owner_uid, http_sessions.owner_uid),
    ...
    request_count=http_sessions.request_count + 1
```

Every other column is a flat overwrite; `owner_uid` is a `COALESCE`. The docstring gives the reason: "A request that happens to carry no/an unresolvable auth token must never downgrade a session that a previous request already identified." A browser session mixes authenticated and unauthenticated requests constantly — a static asset fetch, a poll that raced a token refresh — and a flat overwrite would flip a known user back to `NULL` on the next such request, making the system page's "signed in" column flicker for reasons that have nothing to do with the user's actual state. `COALESCE` makes identification sticky: once a session is known, it stays known.

---

## 2. Immutability: how it's enforced, and where it would break

REQ-11.3 states it plainly: "No endpoint may modify a stored run other than `PATCH /runs/{id}` setting `user_behavior` and `user_flagged`. Recorded history is immutable." This isn't enforced by a database trigger or a permissions layer inside SQLite — there's no `REVOKE UPDATE` on the `ticks` table. It's enforced entirely by *discipline in the query surface*: nothing in `backend/asr/storage/db.py` issues an `UPDATE` against `ticks` or against any `rules`/`runs` column other than the two named above, and the one `UPDATE` statement that exists in the API layer is scoped to exactly those two columns.

**A qualification added in 2.2.1.** As of this release `db.py` *does* contain `UPDATE` statements that fire constantly — `update_generation_session_stage` on every pipeline stage transition, and `touch_http_session` on literally every HTTP request. The sentence above survives intact because of what they target: `generation_sessions` and `http_sessions` are telemetry tables (§1), not recorded history. No `UPDATE` in this module touches `ticks`, and none touches a `rules` or `runs` column other than the two REQ-11.3 names.

This is worth stating rather than leaving implicit, because "no `UPDATE`s in the storage layer" was previously a property you could verify with a single grep, and after 2.2.1 it is not. The invariant is now *scoped* — mutation is confined to tables that carry no history — which is a weaker thing to check and an easier thing to erode. The check that replaces the grep: an `UPDATE` in this module is legitimate only if its target table is one whose complete loss would cost the library nothing. `ticks` fails that test absolutely; `generation_sessions` and `http_sessions` pass it trivially.

That single mutating endpoint is `PATCH /runs/{run_id}` in `backend/asr/api/routes.py:670-702`:

```python
class RunCorrection(BaseModel):
    user_behavior: str | None = None
    user_flagged: bool | None = None


@router.patch("/runs/{run_id}")
def correct_run(
    run_id: int, body: RunCorrection,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    """The only mutation recorded history permits (REQ-11.3): the
    user's behavior override (never overwriting the guess, REQ-9.14)
    and the interesting-flag (REQ-12.7). Neither ever enters generation
    context (REQ-8.5).
    """
    row = conn.execute(
        """SELECT runs.id, rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
        raise HTTPException(404, "no such run")
    provided = body.model_fields_set
    if "user_behavior" in provided:
        if body.user_behavior is not None and body.user_behavior not in BEHAVIOR_NAMES:
            raise HTTPException(400, f"behavior must be one of {BEHAVIOR_NAMES}")
        conn.execute(
            "UPDATE runs SET user_behavior = ? WHERE id = ?",
            (body.user_behavior, run_id),
        )
    if "user_flagged" in provided and body.user_flagged is not None:
        conn.execute(
            "UPDATE runs SET user_flagged = ? WHERE id = ?",
            (int(body.user_flagged), run_id),
        )
    conn.commit()
    fresh = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    return _run_summary(fresh)
```

A few things worth calling out about how carefully this is scoped. It uses `body.model_fields_set` (Pydantic's tracking of which fields were actually present in the request body) rather than just checking `is not None` — that's deliberate, because `user_behavior: None` is a meaningful value (clearing a previous override back to the machine guess, per REQ-9.14's rule that the override "never overwrites the guess" — the guess stays in `guessed_behavior`, `user_behavior` layers on top and can be nulled back out). The `UPDATE` statements are hardcoded to name exactly `user_behavior` and `user_flagged` — there's no generic "patch these fields" helper that a future endpoint could accidentally point at `ticks` or at `source_code`. And per the docstring, neither field ever enters generation context (REQ-8.5, REQ-8.6): the Stage A coverage map that primes rule invention counts only canonical runs' *machine-guessed* behavior, never a user's correction or flag. That's what keeps the corpus's "canonical" signal free of feedback loops — if a user's flags could bias what the generator invents next, the library would stop being a faithful record of unprompted generation.

Where would this be violated? Structurally, the failure mode would be a new route calling `conn.execute("UPDATE ticks ...")` or `conn.execute("UPDATE runs SET stopped_because = ...")` — nothing in the schema or connection setup would stop it. The invariant lives entirely in code review discipline and in the fact that `db.py`'s only write-after-insert helpers are the two `UPDATE runs SET user_behavior/user_flagged` lines above. A defense-in-depth option (SQLite triggers that raise on `UPDATE`/`DELETE` against `ticks`, or a read-only view) isn't used here; the immutability guarantee is a code-level contract, not a database-level one.

---

## 3. Tick encoding

This is the density-critical part of the system. A run can be hundreds or thousands of ticks over a grid that's tens of thousands of cells; storing every tick as a full grid snapshot would make the library balloon and make "scrub to any tick" scale with total run size instead of with a bounded window. `backend/asr/storage/encoding.py` solves this with three payload shapes — `snapshot`, `sparse`, `dense` — chosen per-tick, all Zstandard-compressed, sharing one framing convention.

The module docstring (`encoding.py:1-14`) states the scheme and its rationale up front:

```python
"""Tick payload encoding (REQ-12.5).

A snapshot is written every SNAPSHOT_EVERY ticks. Between snapshots,
each tick stores either a changed-index list (`sparse`) or a raw XOR
against the previous tick (`dense`) — whichever is smaller for that
tick. All payloads are Zstandard-compressed.

Derived arrays are never stored in deltas: `age` changes on nearly
every cell every tick and would make every settled tick dense
(REQ-12.6). `age` IS included in snapshots so reconstruction walks
forward at most one snapshot interval instead of from tick 0
(REQ-12.6.2). `changed_last_tick` is never stored at all — it is the
kind difference of adjacent ticks.
"""
```

`SNAPSHOT_EVERY` is a config value (`backend/asr/config.py`, default `50` via `_int("SNAPSHOT_EVERY", 50)`), not hardcoded in the encoding module — `save_run` in `db.py:244-250` decides per-tick which encoding function to call:

```python
rows = []
previous_arrays = None
for record in result.ticks:
    if record.tick % snapshot_every == 0:
        payload_encoding = "snapshot"
        blob = encoding.encode_snapshot(record.arrays)
    else:
        payload_encoding, blob = encoding.encode_delta(previous_arrays, record.arrays)
    previous_arrays = record.arrays
```

So tick 0, tick 50, tick 100, … are always full snapshots (with `SNAPSHOT_EVERY=50`); every other tick is a delta against the immediately preceding tick's *decoded* arrays, encoded as whichever of sparse/dense comes out smaller.

### What's stored, and what's deliberately excluded

Two module-level tuples in `encoding.py:22-24` govern which array names ever get written, and where:

```python
# Derived properties, reconstructed rather than stored (REQ-12.6).
NEVER_IN_DELTAS = ("age", "changed_last_tick")
SNAPSHOT_ALSO_KEEPS = ("age",)
```

and the helper that applies them, `_stored_names` (`encoding.py:50-54`):

```python
def _stored_names(arrays: dict, snapshot: bool) -> list:
    names = [n for n in sorted(arrays) if n not in NEVER_IN_DELTAS]
    if snapshot:
        names += [n for n in SNAPSHOT_ALSO_KEEPS if n in arrays]
    return names
```

Sorting the names is what backs REQ-9.7.4's requirement that fingerprint hashing (a related but separate concern) sees arrays in a stable, name-sorted order — the same sorting habit is applied here for the same reason: byte-stable output regardless of dict insertion order.

The asymmetry — `age` excluded from `NEVER_IN_DELTAS`'s effect on snapshots but not on deltas — is the crux of REQ-12.6/12.6.1/12.6.2, and it's worth spelling out concretely why. `age` is a derived array: it's how many ticks a cell has held its current `kind` without being reborn, and the harness increments it on essentially every cell, every tick, for any settled or slow-moving pattern. If `age` were stored in *delta* payloads, then even a tick where nothing interesting happened at all — the `kind` grid is bit-identical to the previous tick — would still produce a payload where every single `age` value changed by one. That destroys the entire point of sparse encoding (a changed-index list is only cheap when few indices changed) and pushes every settled tick into the `dense` path, at full-grid-size cost, forever. Per REQ-12.6.1, at the app's configured dimensions this alone would cost roughly 40 MB per run. So `age` is simply never written into a delta at all — it's excluded from `_stored_names(..., snapshot=False)`, full stop, and reconstruction rebuilds it (see section 5) from the one thing that *is* cheap to store: which cells changed `kind`.

But `age` can't be omitted from snapshots too, or reconstruction would have to start from `age = 0` at whatever the nearest snapshot's decoded `kind` says and walk `kind` history all the way back to tick 0 to know each cell's true age — because a cell's age can exceed the snapshot interval (a cell born at tick 3 and never reborn has age 47 at tick 50, unrelated to `SNAPSHOT_EVERY`). So `age` **is** kept in every snapshot (REQ-12.6.2), which bounds the reconstruction walk to at most one snapshot interval instead of the entire run, at a stated cost of roughly 0.8 MB per run — three orders of magnitude cheaper than storing it in every delta.

`changed_last_tick`, meanwhile, is in `NEVER_IN_DELTAS` but conspicuously absent from `SNAPSHOT_ALSO_KEEPS` — it is never stored anywhere, in any payload shape, including snapshots. That's because it needs nothing extra to reconstruct: by definition it's `kind[t] != kind[t-1]`, and `kind` is *already* stored in every payload (it's never in `NEVER_IN_DELTAS`). Storing it would be pure redundancy.

### The wire format: `_frame` / `_unframe`

Every encoded payload — snapshot, sparse, or dense — shares one small header convention before compression, `_frame`/`_unframe` (`encoding.py:37-47`):

```python
def _frame(header: dict, payload: bytes) -> bytes:
    """Length-prefixed JSON header, then a payload region — the same
    shape as the wire framing (REQ-11.5.1)."""
    head = json.dumps(header, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head)) + head + payload


def _unframe(blob: bytes):
    (head_length,) = struct.unpack_from("<I", blob, 0)
    header = json.loads(blob[4 : 4 + head_length].decode("utf-8"))
    return header, blob[4 + head_length :]
```

Byte-for-byte: a little-endian unsigned 32-bit integer (`struct.pack("<I", ...)`, always exactly 4 bytes) giving the length of the JSON header in bytes, then that many bytes of UTF-8 JSON, then the raw payload region. This is deliberately the *same shape* as the REQ-11.5.1 wire framing used for the `/runs/{id}/grids` HTTP response (section 7) — one mental model for "length-prefixed JSON header describing an array blob region" is reused for both the at-rest disk format and the over-the-wire format, even though they're two different call sites (`encoding.py`'s `_frame`, and `framing.py`'s `frame_grids`, which inlines the same `struct.pack("<I", len(header)) + header + ...` pattern rather than importing `_frame` — they're independent implementations of one documented shape, not a shared function).

The whole framed blob — header plus payload — is then Zstandard-compressed as a single unit before it's written to the `ticks.payload_blob` column, via `_compressor().compress(...)`.

### `encode_snapshot`

```python
def encode_snapshot(arrays: dict) -> bytes:
    """The full grid, every stored property plus age."""
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(arrays, snapshot=True):
        array = np.ascontiguousarray(arrays[name])
        shape = list(array.shape)
        raw = array.tobytes()
        entries.append(
            {"name": name, "dtype": array.dtype.str, "offset": offset, "length": len(raw)}
        )
        chunks.append(raw)
        offset += len(raw)
    header = {"shape": shape, "arrays": entries}
    return _compressor().compress(_frame(header, b"".join(chunks)))
```

For each stored property (sorted names, plus `age`), it forces C-contiguous memory layout (`np.ascontiguousarray`, so `.tobytes()` gives a predictable flat byte order regardless of how numpy happened to lay the array out in memory), records its `dtype.str` (e.g. `"|u1"` for uint8 `kind`, `"<u2"` for uint16 `age`), its byte offset within the concatenated payload region, and its byte length. The header ends up something like `{"shape": [16, 16], "arrays": [{"name": "age", "dtype": "<u2", "offset": 0, "length": 512}, {"name": "kind", "dtype": "|u1", "offset": 512, "length": 256}, ...]}`. Every array's raw bytes are concatenated into one `chunks` list, joined, framed with that header, and compressed as one unit — so Zstandard can find redundancy *across* properties too, not just within one.

### `encode_delta`, `_encode_sparse`, `_encode_dense`

`encode_delta` (`encoding.py:76-84`) is the dispatcher — it computes both delta forms and keeps whichever compresses smaller:

```python
def encode_delta(previous: dict, current: dict):
    """Difference against the previous tick: whichever of the two delta
    forms is smaller for this tick. Returns (encoding_name, blob).
    """
    sparse = _encode_sparse(previous, current)
    dense = _encode_dense(previous, current)
    if len(sparse) <= len(dense):
        return "sparse", _compressor().compress(sparse)
    return "dense", _compressor().compress(dense)
```

Note the comparison happens on the *uncompressed* framed bytes (`len(sparse) <= len(dense)`), not on compressed size — computing two full Zstandard compressions just to throw one away would be wasted work, and uncompressed size is a reliable enough proxy for which form will compress smaller (sparse's cost scales with the number of changed cells; dense's cost is always full-grid-size regardless of how many cells changed).

`_encode_sparse` (`encoding.py:87-118`) stores, per property, only the flat indices that changed and their new values:

```python
def _encode_sparse(previous: dict, current: dict) -> bytes:
    """Per property: the flat indices that changed, and their new
    values. A property with no changes is omitted entirely.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(current, snapshot=False):
        now = np.ascontiguousarray(current[name])
        before = np.ascontiguousarray(previous[name])
        shape = list(now.shape)
        changed = np.flatnonzero(now.reshape(-1) != before.reshape(-1))
        if changed.size == 0:
            continue
        indices = changed.astype(np.uint32).tobytes()
        values = now.reshape(-1)[changed].tobytes()
        entries.append(
            {
                "name": name,
                "dtype": now.dtype.str,
                "count": int(changed.size),
                "offset": offset,
                "index_length": len(indices),
                "value_length": len(values),
            }
        )
        chunks.append(indices)
        chunks.append(values)
        offset += len(indices) + len(values)
    header = {"kind_of_delta": "sparse", "shape": shape, "arrays": entries}
    return _frame(header, b"".join(chunks))
```

`np.flatnonzero(now.reshape(-1) != before.reshape(-1))` gives the flat (row-major) indices of every cell whose value changed for that property. If nothing changed for a given property, that property is skipped entirely (`if changed.size == 0: continue`) — a tick where `kind` is static but `heading` moved would only carry a `heading` entry. The indices are stored as `uint32` (enough headroom for any grid this system runs at) immediately followed by the changed cells' new values in the array's native dtype; the header records `index_length` and `value_length` separately so the decoder knows exactly where the index block ends and the value block begins within that property's region.

`_encode_dense` (`encoding.py:121-143`) is the fallback for a tick where *most* cells changed, where a per-cell index list would cost more than just storing the whole grid:

```python
def _encode_dense(previous: dict, current: dict) -> bytes:
    """Per property: the raw bytes XORed against the previous tick.
    Unchanged regions become zeros, which Zstandard flattens.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(current, snapshot=False):
        now = np.ascontiguousarray(current[name])
        before = np.ascontiguousarray(previous[name])
        shape = list(now.shape)
        mixed = np.bitwise_xor(
            np.frombuffer(now.tobytes(), np.uint8),
            np.frombuffer(before.tobytes(), np.uint8),
        ).tobytes()
        entries.append(
            {"name": name, "dtype": now.dtype.str, "offset": offset, "length": len(mixed)}
        )
        chunks.append(mixed)
        offset += len(mixed)
    header = {"kind_of_delta": "dense", "shape": shape, "arrays": entries}
    return _frame(header, b"".join(chunks))
```

Rather than storing the new values outright, it XORs the current tick's raw bytes against the previous tick's raw bytes (both reinterpreted as flat `uint8` buffers so the XOR is byte-for-byte regardless of the array's actual dtype). Any byte position that's unchanged between ticks becomes `0x00`; only genuinely different bytes are nonzero. The comment explains why this is worth doing instead of just storing the new bytes directly: "unchanged regions become zeros, which Zstandard flattens" — a long run of `0x00` compresses far better than a long run of arbitrary-but-repeated values, so even in the dense path, most of the win still comes from the *compressor*, not from the XOR itself; the XOR's job is just to maximize how compressible the byte stream is by turning "no change" into the most compression-friendly possible byte.

### `decode`

`decode` (`encoding.py:146-193`) is the single entry point that reverses all three encodings, given the previous tick's already-decoded arrays where applicable:

```python
def decode(encoding: str, blob: bytes, previous: dict | None) -> dict:
    """Rebuild one tick's stored arrays. `previous` is the already-
    decoded prior tick for sparse/dense; snapshots stand alone.
    """
    header, payload = _unframe(_decompressor().decompress(blob))
    shape = tuple(header["shape"])
    if encoding == "snapshot":
        arrays = {}
        for entry in header["arrays"]:
            raw = payload[entry["offset"] : entry["offset"] + entry["length"]]
            arrays[entry["name"]] = np.frombuffer(raw, entry["dtype"]).reshape(shape).copy()
        return arrays

    if previous is None:
        raise ValueError(f"a {encoding} tick cannot be decoded without the previous tick")
    arrays = {
        name: array for name, array in previous.items() if name not in NEVER_IN_DELTAS
    }
    if encoding == "sparse":
        for entry in header["arrays"]:
            start = entry["offset"]
            indices = np.frombuffer(
                payload[start : start + entry["index_length"]], np.uint32
            )
            values = np.frombuffer(
                payload[
                    start + entry["index_length"]
                    : start + entry["index_length"] + entry["value_length"]
                ],
                entry["dtype"],
            )
            fresh = arrays[entry["name"]].copy().reshape(-1)
            fresh[indices] = values
            arrays[entry["name"]] = fresh.reshape(shape)
        return arrays
    if encoding == "dense":
        for entry in header["arrays"]:
            raw = payload[entry["offset"] : entry["offset"] + entry["length"]]
            before = arrays[entry["name"]]
            mixed = np.bitwise_xor(
                np.frombuffer(before.tobytes(), np.uint8), np.frombuffer(raw, np.uint8)
            )
            arrays[entry["name"]] = np.frombuffer(
                mixed.tobytes(), entry["dtype"]
            ).reshape(shape)
        return arrays
    raise ValueError(f"unknown payload encoding {encoding!r}")
```

For `snapshot`, every entry in the header is sliced straight out of the payload region at its recorded `offset`/`length`, reinterpreted with `np.frombuffer(raw, entry["dtype"])`, and reshaped. The `.copy()` matters — `np.frombuffer` returns a read-only view into the decompressed bytes, and the caller needs a writable, independent array (this becomes important a moment later, when `previous` gets mutated on top of).

For `sparse` and `dense`, decoding starts by seeding `arrays` with the *previous* tick's decoded arrays, filtered to exclude anything in `NEVER_IN_DELTAS` — i.e., start from what was true a moment ago, then apply just the differences. For sparse, each stored property's index block and value block are sliced out (in the same `offset`/`index_length`/`value_length` layout `_encode_sparse` wrote), and `fresh[indices] = values` scatter-writes the new values at exactly the positions that changed, leaving everything else exactly as it was in `previous`. For dense, each stored property's XOR bytes are re-XORed against the corresponding bytes of `arrays[entry["name"]]` (still holding the previous tick's value) — XOR is its own inverse, so `before XOR (before XOR now) == now`, which recovers the current tick's raw bytes, reinterpreted with the recorded dtype and reshaped.

Because `decode` for sparse/dense always requires the immediately preceding tick's decoded state, decoding a run's history is inherently sequential from the nearest snapshot forward — which is exactly the walk `reconstruct.py` implements (section 5).

---

## 4. Case study: the module-level Zstandard context that could take down the whole server

This is worth documenting in detail, because it's a textbook example of a bug class that's easy to introduce and hard to diagnose from the outside: a native-extension object that looks like a harmless, stateless-safe singleton, shared across a threadpooled service.

### What the code looked like

Until this session, `backend/asr/storage/encoding.py` constructed its Zstandard compressor and decompressor once, at import time, as module-level singletons:

```python
_compressor = zstandard.ZstdCompressor()
_decompressor = zstandard.ZstdDecompressor()
```

and every call site used them directly — `_compressor.compress(...)` in `encode_snapshot` and `encode_delta`, `_decompressor.decompress(...)` in `decode`. This reads as completely idiomatic Python: `ZstdCompressor`/`ZstdDecompressor` construction has some fixed cost, `.compress()`/`.decompress()` look like pure functions that take bytes in and return bytes out, and reusing one instance across calls is the obvious "don't pay setup cost twice" move. Nothing about the Python-level API signals that these objects carry internal, mutable, non-thread-safe state in their C extension (`backend_c`).

### What broke, and what it looked like from the outside

FastAPI runs synchronous route handlers — which `GET /runs/{id}/grids` and friends are — in a threadpool, not on the single asyncio event-loop thread. That's normally invisible to route code, because each request typically only touches objects it constructs itself, or a database connection scoped per-request (as described in section 1). But `encoding.decode`, called from `reconstruct.py`'s walk on every playback request, was reaching into the *same* module-level `_decompressor` object from every thread simultaneously. `/library` and `/mine` each fire off a burst of parallel thumbnail-grid requests on page load — exactly the concurrency pattern needed to have multiple threadpool workers call `.decompress()` on the same `ZstdDecompressor` at the same moment.

The visible symptom was intermittent and, at first glance, apparently unrelated to storage at all: **502s on completely unrelated routes, including plain `/library` listing requests that don't even touch tick payloads.** That's the detail that makes this bug genuinely hard to place from symptoms alone — a request to list rules doesn't decode any grid data, so a report of "`/library` is throwing 502s" points everywhere *except* the encoding module. The reason it happened anyway is that ASR runs as a single uvicorn process (no per-worker isolation) — when the native corruption below actually crashed the process, *every* in-flight request died with it, regardless of which route it was on.

Underneath the 502s, two related failure modes showed up depending on how badly the concurrent calls interleaved:

- Intermittent `zstandard.backend_c.ZstdError: decompression error: Data corruption detected` and `"Destination buffer is too small"` — the decompressor's internal state (its streaming buffers, frame-parsing position) got corrupted by two threads advancing it at once, so it read the compressed bytes as if they were a different, invalid stream.
- Under worse interleaving, actual native memory corruption: a segfault (general protection fault) inside `backend_c.cpython-312-x86_64-linux-gnu.so` itself, killing the entire single-process uvicorn server outright.

### How it was diagnosed

The path to the root cause went through three layers of evidence, each one narrowing the hypothesis:

1. **The uvicorn traceback.** The first, most direct signal was a Python-level traceback in the uvicorn log pointing at `encoding.py:143`, inside `decode` — a `ZstdError` raised out of `.decompress()`. That placed the failure in the right module, but a single stack trace from one thread doesn't explain *why* a `.decompress()` call on valid, previously-written compressed bytes would ever fail — the bytes on disk hadn't changed, so if this were a data-corruption-at-rest problem it would fail deterministically and every time, not intermittently.
2. **`dmesg` confirming the segfault.** The intermittent-and-then-total nature of the failures (some requests get a clean `ZstdError`, then eventually the whole server dies) pointed at something worse than a logic bug — and checking `dmesg` confirmed it: `traps: python[PID] general protection fault ... in backend_c...so`, a kernel-level record of the Python process taking a hardware fault inside the Zstandard C extension. That's the signature of memory corruption inside native code, not a Python-level exception — it rules out "some edge case in the framing header" and points squarely at the C extension's internal state being torn.
3. **Recognizing the module-level singleton + threadpool combination.** With "corrupted native state inside the zstd C extension, intermittent, worse under load" as the shape of the bug, the fix was to ask what state that extension owns that could be touched from two threads at once — and the answer was sitting in plain sight: `_compressor`/`_decompressor` were constructed exactly once, at import time, and every request-handling thread in FastAPI's threadpool called methods on those same two objects. `/library` and `/mine` each triggering a burst of parallel `/runs/*/grids` thumbnail fetches on load is precisely the traffic pattern that would put multiple threadpool workers inside `.decompress()` on the same context concurrently.

### The fix

The singletons were replaced with per-call factory functions that construct a fresh context every time, so no two calls ever share mutable native state, whether or not they happen to run concurrently:

```python
def _compressor() -> zstandard.ZstdCompressor:
    # A fresh context per call: ZstdCompressor/ZstdDecompressor are not
    # safe for concurrent use, and route handlers run in a threadpool.
    return zstandard.ZstdCompressor()


def _decompressor() -> zstandard.ZstdDecompressor:
    return zstandard.ZstdDecompressor()
```

and every call site was updated from `_compressor.compress(...)` to `_compressor().compress(...)` (and the decompressor equivalently) — visible in `encode_snapshot`, both branches of `encode_delta`, and `decode`, all quoted in full in section 3 above. The diff is small and mechanical — five call sites, each gaining one pair of parentheses — but the semantic change is exactly the fix: construction cost is paid per call instead of once, in exchange for eliminating any possibility of two threads sharing one context's internal buffers.

This is a reasonable trade for this codebase specifically: `ZstdCompressor()`/`ZstdDecompressor()` construction is cheap relative to the actual compress/decompress work on grid-sized payloads, and correctness under FastAPI's threadpool concurrency model matters far more here than shaving a small constant-time allocation. (A dictionary-based or thread-local pool of reusable contexts would also work and would recover some of that construction cost, but wasn't necessary to fix the bug, and the per-call factory is the simplest thing that is unconditionally correct.)

### The general lesson

The pattern to watch for: **a native-extension object whose Python-level API reads as stateless-safe (bytes in, bytes out, no visible mutation) is not automatically thread-safe, even though the equivalent pure-Python code often would be.** `ZstdCompressor`/`ZstdDecompressor` hold internal C-level buffers and streaming state that the Python API doesn't surface — there's nothing in `help(zstandard.ZstdDecompressor.decompress)` that visually warns you two threads sharing one instance will corrupt memory. The module-level singleton pattern is completely correct for a genuinely stateless pure-Python helper; it becomes a live bug the moment the object underneath has native, mutable, unsynchronized state and the surrounding service can call it from more than one thread.

Concretely, the audit this bug should prompt for any threadpooled service (which every synchronous-route FastAPI app is, by default) is: **anything constructed at module scope and shared across requests needs an explicit thread-safety check**, not an assumption based on how the Python-level call signature looks. Database connections in this codebase already got this right by construction — `get_db` in `routes.py` opens one connection per request rather than sharing a module-level connection, specifically because SQLite connections have exactly this kind of native-level statefulness. The Zstandard contexts were the one place that pattern wasn't followed, and the failure mode — silent-until-concurrent, then catastrophic and seemingly-everywhere — is exactly what makes this class of bug worth calling out by name rather than filing as "flaky test, retried and moved on."

---

## 5. Reconstruction: walking forward from the nearest snapshot

`backend/asr/storage/reconstruct.py` answers the question every playback request actually asks: "give me these properties, for this tick range, as arrays." Its docstring (`reconstruct.py:1-13`) states the contract:

```python
"""Rebuilding grids from stored payloads (REQ-11.2, REQ-12.6).

Stored properties decode from the nearest snapshot at or before the
requested range, walking deltas forward — at most one snapshot interval.
Derived properties are rebuilt, never read from deltas:

- `changed_last_tick` at tick t is `kind[t] != kind[t-1]` (False at 0).
- `age` starts from the copy kept in each snapshot (REQ-12.6.2) and
  walks forward with the kind history.

The cache holds one full-run stack per (run id, property), budgeted in
bytes, not runs (REQ-11.2.1), evicting least-recently-used.
"""
```

### Finding the starting point

`_snapshot_at_or_before` (`reconstruct.py:24-32`) is the query that makes "at most one snapshot interval" true:

```python
def _snapshot_at_or_before(conn, run_id: int, tick: int) -> int:
    row = conn.execute(
        """SELECT MAX(tick) AS tick FROM ticks
           WHERE run_id = ? AND tick <= ? AND payload_encoding = 'snapshot'""",
        (run_id, tick),
    ).fetchone()
    if row["tick"] is None:
        raise ValueError(f"run {run_id} has no snapshot at or before tick {tick}")
    return row["tick"]
```

Given any requested tick, this finds the closest snapshot at or before it. Since snapshots are written every `SNAPSHOT_EVERY` ticks (tick 0 is always a snapshot, so the query can never come up empty for a valid tick), the gap between this snapshot and the requested tick is bounded by `SNAPSHOT_EVERY - 1` at most — that's the whole reason snapshot cadence exists: it caps how many sequential delta-decodes any single reconstruction ever has to perform, regardless of how far into a multi-thousand-tick run the requested tick is.

### `_walk`: sequential decode from that point

```python
def _walk(conn, run_id: int, first_tick: int, last_tick: int):
    """Yield (tick, arrays) for a contiguous range, starting the decode
    at the nearest snapshot so the caller never pays more than one
    snapshot interval of extra decoding.
    """
    start = _snapshot_at_or_before(conn, run_id, first_tick)
    arrays = None
    for row in conn.execute(
        """SELECT tick, payload_encoding, payload_blob FROM ticks
           WHERE run_id = ? AND tick BETWEEN ? AND ? ORDER BY tick""",
        (run_id, start, last_tick),
    ):
        arrays = encoding.decode(row["payload_encoding"], row["payload_blob"], arrays)
        yield row["tick"], arrays
```

This is a generator that fetches every tick row from the nearest snapshot through the requested end tick, in tick order, and feeds each one through `encoding.decode` — passing the *previous* iteration's freshly-decoded `arrays` as the `previous` argument each time (`arrays` starts `None` for the first row, which is always a snapshot and so doesn't need it). Because `decode` for sparse/dense mutates forward from whatever `previous` it's handed, this loop is literally replaying the sequence of encode operations in reverse: snapshot, then apply delta, then apply delta, … up to the target tick.

### `reconstruct_range`: assembling requested properties, including derived ones

```python
def reconstruct_range(conn, run_id: int, properties: list, first_tick: int, last_tick: int) -> dict:
    """Rebuild the requested properties for a tick range. Returns
    {name: array stacked (ticks, height, width)}, index 0 = first_tick.
    """
    wants_changed = "changed_last_tick" in properties
    wants_age = "age" in properties
    stored = [p for p in properties if p not in encoding.NEVER_IN_DELTAS]

    # changed_last_tick at the first tick needs the kind one tick back.
    walk_from = max(0, first_tick - 1) if wants_changed else first_tick
    # age walks forward from the snapshot's stored copy.
    if wants_age:
        walk_from = min(walk_from, _snapshot_at_or_before(conn, run_id, first_tick))

    span = last_tick - first_tick + 1
    stacks = {name: [None] * span for name in properties}
    age = None
    previous_kind = None
    for tick, arrays in _walk(conn, run_id, walk_from, last_tick):
        if wants_age:
            if "age" in arrays and (age is None or tick <= first_tick):
                age = arrays["age"]  # a snapshot carries age (REQ-12.6.2)
            elif age is not None and previous_kind is not None:
                born = arrays["kind"] != previous_kind
                grown = np.minimum(age.astype(np.uint32) + 1, AGE_CEILING).astype(np.uint16)
                age = np.where(born, np.uint16(0), grown)
        position = tick - first_tick
        if 0 <= position < span:
            for name in stored:
                stacks[name][position] = arrays[name]
            if wants_age:
                stacks["age"][position] = age
            if wants_changed:
                if tick == 0:
                    stacks["changed_last_tick"][position] = np.zeros(
                        arrays["kind"].shape, dtype=bool
                    )
                else:
                    stacks["changed_last_tick"][position] = arrays["kind"] != previous_kind
        previous_kind = arrays["kind"]
    return {name: np.stack(stack) for name, stack in stacks.items()}
```

There's a subtlety in how far back the walk actually has to start, separate from the snapshot cadence: if the caller wants `changed_last_tick` (which needs `kind` at `first_tick - 1` to compute the very first requested tick's value) or `age` (which needs the nearest snapshot's carried `age`, which may be *before* `first_tick`'s own nearest snapshot if `first_tick` isn't itself a snapshot tick), `walk_from` is pulled backward accordingly — `max(0, first_tick - 1)` for the changed-flag case, and further clamped down to `_snapshot_at_or_before(conn, run_id, first_tick)` if age is wanted, since age's only valid starting point is a snapshot's carried copy.

The `age` reconstruction inside the loop directly encodes the harness rule from the module docstring: pull the snapshot's carried `age` array whenever one is available at or before `first_tick`, and on every subsequent tick, compute `born = arrays["kind"] != previous_kind` (a cell whose `kind` changed since last tick was reborn) and then `age = np.where(born, 0, min(age + 1, AGE_CEILING))` — reborn cells reset to 0, everyone else increments, capped at `AGE_CEILING = 65535` (matching the uint16 storage width and the REQ-9.7.6 clamp discussion for stubbornness-scope fingerprinting, though the clamp used for fingerprinting itself, `minimum(age, 3)`, is a separate, tighter clamp applied at the engine layer, not here). `changed_last_tick` is computed identically simply: `False` at tick 0 by definition, and `arrays["kind"] != previous_kind` for every tick after.

Only positions actually inside the requested `[first_tick, last_tick]` window get written into the output `stacks` — the extra ticks walked purely to seed `age`/`changed_last_tick` correctly are computed but not returned, via the `if 0 <= position < span` guard. The final return stacks each requested property into one array of shape `(ticks, height, width)` via `np.stack`, with index 0 corresponding to `first_tick`.

---

## 6. The reconstruction cache

Decoding a run's full history from its stored payloads is real work — every scrub, loop, or rerun of a range would otherwise pay to walk from the nearest snapshot and replay deltas again. `ReconstructionCache` (`reconstruct.py:94-121`) exists so that cost is paid once per (run, property) pair, not once per request:

```python
class ReconstructionCache:
    """Full-run property stacks, evicted least-recently-used against a
    byte budget (REQ-11.2)."""

    def __init__(self, budget_bytes: int):
        self.budget_bytes = budget_bytes
        self._held = OrderedDict()  # (run_id, property) -> stack
        self._held_bytes = 0

    def property_history(self, conn, run_id: int, name: str) -> np.ndarray:
        """Every tick of one property, shaped (ticks_run + 1, h, w)."""
        key = (run_id, name)
        if key in self._held:
            self._held.move_to_end(key)
            return self._held[key]
        last = conn.execute(
            "SELECT MAX(tick) AS tick FROM ticks WHERE run_id = ?", (run_id,)
        ).fetchone()["tick"]
        if last is None:
            raise ValueError(f"run {run_id} has no ticks")
        stack = reconstruct_range(conn, run_id, [name], 0, last)[name]
        self._held[key] = stack
        self._held_bytes += stack.nbytes
        while self._held_bytes > self.budget_bytes and len(self._held) > 1:
            _, evicted = self._held.popitem(last=False)
            self._held_bytes -= evicted.nbytes
        return stack
```

The cache key is `(run_id, property_name)` — not the whole run, and not a tick-range slice. On a miss, `property_history` reconstructs the *entire* run's history for that one property (`reconstruct_range(conn, run_id, [name], 0, last)`) and holds the full stack. This is deliberate: REQ-11.2's own framing is "cell history requires one position across every tick, which means reconstructing the run" — a query for a single cell's value across time (`GET /runs/{id}/cell/{y}/{x}`, `backend/asr/api/routes.py:638-662`) touches every tick regardless of range, so there's no benefit to caching partial ranges; caching the whole property stack once means every subsequent cell-history query, and every subsequent grids request that reuses the same property, is a pure slice out of memory (`cache.property_history(...)[from_tick : last + 1]`, as used in `GET /runs/{id}/grids` at `routes.py:562`) with no further decode work at all.

Eviction is LRU, implemented with `OrderedDict`: a cache hit calls `move_to_end` to mark it most-recently-used, and eviction (`popitem(last=False)`) always removes the *least*-recently-used entry first, repeated until the held byte total is back under budget (or only one entry is left — the cache never evicts its way down to zero, so a single very large property stack that alone exceeds the budget is still held rather than thrashed on every call). The budget is tracked in **bytes** (`stack.nbytes`), not in number of entries or number of runs — REQ-11.2.1 spells out why that distinction matters concretely: "For 500 ticks at 200×200: a uint8 property is 20 MB, `age` at uint16 is 40 MB, a float32 property is 80 MB." An entry-count-based cache would treat a 20 MB `kind` stack and an 80 MB float property identically, which could blow well past any reasonable memory ceiling; a byte budget makes the cache's actual memory footprint predictable regardless of which properties or how many runs get requested. The budget itself comes from `RUN_CACHE_BUDGET_MB` (`backend/asr/config.py`, default `512`), wired into `app.state.cache = ReconstructionCache(settings.run_cache_budget_mb * 1024 * 1024)` at app startup (`backend/asr/api/app.py`).

There is no explicit invalidation logic anywhere in this class — and that's correct, not an oversight. Because recorded history is immutable (section 2), a run's tick payloads never change after `save_run` commits them, so a cached property stack for a given `(run_id, name)` can never go stale. The only two run columns that ever mutate after insert (`user_behavior`, `user_flagged`) aren't part of any property stack this cache holds — they're plain row columns read straight from `runs`, never reconstructed. So the cache's correctness rests entirely on the immutability invariant from section 2; if that invariant were ever violated by a future endpoint mutating `ticks`, this cache would silently start serving stale data with no mechanism to notice.

This is exactly the piece CLAUDE.md's "storage/ (SQLite WAL, tick encoding, reconstruction + cache)" summary points at, and exactly why playback performance holds up under scrubbing: the first `/runs/{id}/grids` request for a run pays the full-run decode cost once per requested property; every later request — a scrub, a loop, a rerun of the same range, or a different tick window over an already-cached property — is a slice of an in-memory numpy array.

---

## 7. Binary framing over the wire (REQ-11.5.1)

`backend/asr/api/framing.py` is the module that implements the actual HTTP response body for `GET /runs/{id}/grids`. Its docstring restates the "why" directly from the spec (REQ-11.5):

```python
"""The grid wire format (REQ-11.5, REQ-11.5.1).

Grid payloads are packed binary, never nested JSON arrays — twenty
million JSON integers per property per run is not a viable transport
for 30fps playback. The exact framing is specified so both ends cannot
invent incompatible protocols:

    bytes 0..3   uint32, little-endian: byte length of the JSON header
    bytes 4..N   UTF-8 JSON header
    bytes N..    payload region: C-order array blocks at stated offsets
"""
```

The spec's own REQ-11.5.1 (`documents/asr-requirements-v3.md:1008-1021`) gives the precise header shape:

```
bytes 0..3     uint32, little-endian: byte length of the JSON header
bytes 4..N     UTF-8 JSON header:
                 { "ticks": [from, to],
                   "shape": [height, width],
                   "properties": [
                     {"name": "kind", "dtype": "uint8",
                      "offset": <bytes from start of payload region>,
                      "length": <bytes>}
                   ] }
bytes N..       payload region: C-order array blocks at the stated offsets
```

And `frame_grids` (`framing.py:19-46`) is the implementation:

```python
def frame_grids(first_tick: int, last_tick: int, stacks: dict) -> bytes:
    """Pack {property name: (ticks, height, width) array stack} for the
    inclusive tick range. Each property is one contiguous C-order block
    covering every tick in the range.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in sorted(stacks):
        stack = np.ascontiguousarray(stacks[name])
        shape = list(stack.shape[1:])
        raw = stack.tobytes()
        entries.append(
            {
                "name": name,
                "dtype": stack.dtype.name,
                "offset": offset,
                "length": len(raw),
            }
        )
        chunks.append(raw)
        offset += len(raw)
    header = json.dumps(
        {"ticks": [first_tick, last_tick], "shape": shape, "properties": entries},
        separators=(",", ":"),
    ).encode("utf-8")
    return struct.pack("<I", len(header)) + header + b"".join(chunks)
```

Concretely, to parse this on a client (this is exactly what a JavaScript frontend does, per CLAUDE.md's note that grid payloads "use the binary framing in REQ-11.5.1, never nested JSON" and that this is why the frontend needs `ArrayBuffer`/`DataView` handling rather than `response.json()`):

1. Read the first 4 bytes as a little-endian `uint32` — that's the header's byte length, `head_length`.
2. Read the next `head_length` bytes as UTF-8, `JSON.parse` it. This gives `{"ticks": [from, to], "shape": [height, width], "properties": [{"name", "dtype", "offset", "length"}, ...]}`.
3. Everything from byte `4 + head_length` onward is the payload region. For each entry in `properties`, slice out `payload[offset : offset + length]` and interpret it as a typed array of `dtype` (e.g. a JS `Uint8Array` for `"uint8"`, a `Uint16Array` for `"uint16"` — note `dtype` here is numpy's `.dtype.name`, e.g. `"uint8"`/`"uint16"`/`"float32"`, not the `.dtype.str` short codes like `"|u1"` that `encoding.py`'s at-rest framing uses; the two framings share a *shape*, not a byte-identical header vocabulary).
4. Each property's slice is one contiguous C-order block covering every tick in `[ticks[0], ticks[1]]` inclusive, at the recorded `shape` (height × width) per tick — so a `Uint8Array` for `kind` over a 10-tick, 16×16 range is 10×16×16 = 2560 bytes, reshapable by the client into whatever per-tick view it needs.

Note this endpoint's framing does not itself apply Zstandard compression the way the at-rest `payload_blob` does — instead, `GET /runs/{id}/grids` (`routes.py:528-584`) applies ordinary HTTP `gzip` transport compression when the client advertises `Accept-Encoding: gzip`, on top of the *already-decoded, uncompressed* framed bytes:

```python
body = frame_grids(from_tick, last, stacks)
headers = {}
if "gzip" in (request.headers.get("accept-encoding") or ""):
    import gzip

    body = gzip.compress(body, compresslevel=1)
    headers["Content-Encoding"] = "gzip"
return Response(
    content=body,
    media_type="application/octet-stream",
    headers=headers,
)
```

The comment at `routes.py:571-574` is explicit that this is a transport-layer concern layered on top of, not a replacement for, the framing: "Grid stacks are huge but repetitive; wire compression cuts them ~20x and playback smoothness lives or dies on transfer time. The framing itself (REQ-11.5.1) is unchanged — the browser undoes transport encoding before the decoder ever sees the bytes." So the client's parsing logic (steps 1–4 above) is unaffected by whether gzip was used — the browser's own HTTP stack transparently decompresses the response body before any application code (or `fetch()` caller) ever sees it, exactly like it does for any other gzip-encoded HTTP response.

---

## 8. Engine revision stamping (REQ-12.4.2)

Every `rules` row and every `runs` row carries an `engine_version` column (visible in the DDL in section 1). It's populated by `engine_version()` in `backend/asr/version.py`:

```python
"""The engine revision stamp (REQ-12.4.2).

Two runs of byte-identical rule source under different harness
revisions are different experiments, so every rule and run records the
git revision that produced it.
"""

import functools
import subprocess
from pathlib import Path

HELPER_VERSION = 1  # bump when any section-6 helper changes behavior


@functools.lru_cache(maxsize=1)
def engine_version() -> str:
    repo_root = Path(__file__).resolve().parents[2]
    try:
        finished = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if finished.returncode == 0:
            return finished.stdout.strip()
    except OSError:
        pass
    return "unknown"
```

It shells out to `git rev-parse HEAD` in the repository root (computed as `Path(__file__).resolve().parents[2]` — two directories up from `backend/asr/version.py`, i.e. the repo root, `/root/projects/auto-sr`), and returns the current commit hash as a string. `@functools.lru_cache(maxsize=1)` means this subprocess only actually runs once per process lifetime — the git revision doesn't change while the server is running, so every subsequent call is a cached return. If `git` itself is unavailable or the call fails for any reason (`OSError`, or a non-zero return code), it falls back to the literal string `"unknown"` rather than raising — provenance stamping degrades gracefully rather than blocking rule generation or run execution.

The call sites confirm this is applied consistently everywhere a rule or run is written: `backend/asr/seed.py:105` (seeded reference rules), `backend/asr/seed.py:131` (their seed runs), `backend/asr/generation/pipeline.py:256` and `:350` (generated rules and their canonical runs), and `backend/asr/api/routes.py:496` (reruns via `POST /rules/{id}/runs`).

Why this matters, per REQ-12.4.2's own framing: `source_hash` (also stored on every rule) catches byte-identical *regenerations* — the same Stage B code produced twice — but it cannot tell you that `count_neighbors` (a harness helper) changed behavior, that a prompt template was reworded in a way that would change what a re-run of Stage A produces, or that modifier semantics moved. All of those are harness-side changes, invisible to a hash of the rule's own source. So two runs of byte-identical rule source, executed under two different git revisions of the harness, are treated as **different experiments** — not because the rule changed, but because the *thing that ran it* changed, and the corpus needs to be able to tell those apart when someone later asks "why did this rule behave differently the second time." `HELPER_VERSION` (also in `version.py`, currently `1`) is the finer-grained companion to this: it's meant to be bumped specifically "when any section-6 helper changes behavior" — the geometry/neighbor-counting helpers a rule's `step` method can call — giving a narrower signal than a full git revision for the one class of change (bound-helper semantics) that's common enough and consequential enough to warrant its own version number, stored separately in the `rules.helper_version` column.

---

## Summary

The storage layer's shape follows directly from two constraints stated at the top of this document: history must never be mutated once recorded, and playback must scrub smoothly over runs far too large to hold or transmit as full grids per tick. Everything else is a consequence — WAL mode so per-request connections don't serialize behind a writer; a five-table (plus later additions) schema where only two columns on one table are ever updated post-insert, enforced by a single narrowly-scoped `PATCH` handler; snapshot-plus-delta tick encoding with derived arrays deliberately excluded from deltas and selectively kept in snapshots; a byte-budgeted LRU cache that's correct without any invalidation logic *because* history is immutable; a length-prefixed-JSON-then-binary wire format shared conceptually between the at-rest and over-the-wire representations; and a git-revision stamp on every row because the harness itself is part of what defines an experiment. The one place this system got bitten — the shared Zstandard contexts — is a reminder that "looks stateless" and "is thread-safe" are different claims, and that a threadpooled service owes every module-level object an explicit check of which one it's actually making.
