# API & Authentication

> **Release 2.2.1** · documented 2026-08-20 · **updated for 2.2.1.**
> This subsystem changed more than any other in this release. New: `system.py` and its two
> routes (§11), a session-tracking middleware that replaced the timing-only one (§10), and
> `try_resolve_uid` — a second, deliberately non-failing identity path in `auth.py` (§6).
> One claim in §2's original text needed qualifying and is marked where it appears. The
> routes in §1's `routes.py`, `comments.py`, and `profile.py` tables, the SSE design (§2–3),
> binary framing (§4), and the immutability endpoint (§5) are unchanged and re-verified.

This is part five of a six-part deep-technical-documentation series on Autonomous Semantic Ruliology (ASR), covering the subsystem at `backend/asr/api/`: the HTTP surface FastAPI exposes, the SSE-streamed generation endpoint, the binary grid-transport plumbing at the route level, Firebase Authentication Phase 1 (optional Email/Password sign-in layered on a single-user local app), and the system-observability routes. Every claim below is sourced from the actual files in that directory, quoted with `file:line` citations, plus the requirements spec (`documents/asr-requirements-v3.md`) and `documents/architecture.md`'s phase log.

The directory holds six route-bearing files plus one wiring file:

```
backend/asr/api/
├── app.py        101 lines  — FastAPI app factory, session middleware, router wiring
├── auth.py        67 lines  — Firebase ID-token verification (two entry points)
├── routes.py     781 lines  — rules, runs, catalog, library, RSS
├── stream.py     122 lines  — POST /rules/generate (SSE)
├── system.py     126 lines  — /system/status, /system/sessions
├── comments.py   173 lines  — comments on rules
└── profile.py     69 lines  — display-name override
```

Total: 1,439 lines of route code (plus a 46-line `framing.py` module used by `routes.py`), up from 1,229 at 2.2.0. This doc covers all of it except the deep internals of grid reconstruction and Zstandard tick encoding, which belong to the storage doc — here you get the route-level handoff only.

---

## 1. Route inventory

Every route in the app, by file, with method, path, and what it does. Auth state is `Depends(get_current_user)` on nearly all of them — a `dict | None`, never a hard-required dependency — which is the mechanism Section 6 explains in detail.

### `routes.py` — rules, runs, catalog, library

| Method | Path | Function | Purpose |
|---|---|---|---|
| GET | `/rules` | `list_rules` (routes.py:186) | Paged library list. Filters: `status`, `behavior`, `concept`, `flagged`, `mine`, `favorited`; sorts: `newest`, `most_liked`, `most_discussed`, `most_looped`. |
| GET | `/rules/{rule_id}` | `get_rule` (routes.py:321) | Full rule detail: source, provenance, every run. |
| GET | `/rules/by-slug/{slug}` | `get_rule_by_slug` (routes.py:329) | Same detail, resolved by the human-readable slug instead of the numeric id — the clean-URL route the frontend's `#/r/:slug` uses. |
| PATCH | `/rules/{rule_id}` | `set_rule_title` (routes.py:346) | The one rule mutation: set or clear a display title (and its derived slug). |
| POST | `/rules/{rule_id}/favorite` | `add_favorite` (routes.py:377) | Favorite a rule (requires sign-in). |
| DELETE | `/rules/{rule_id}/favorite` | `remove_favorite` (routes.py:392) | Unfavorite. |
| GET | `/rules/{rule_id}/preview.png` | `rule_preview_image` (routes.py:411) | A static PNG of the canonical run's final frame, for social-card previews. |
| POST | `/rules/{rule_id}/runs` | `rerun_rule` (routes.py:454) | Run the rule again with a new (or caller-supplied) seed. Never canonical. |
| GET | `/runs/{run_id}` | `get_run` (routes.py:504) | Run metadata plus per-tick summary numbers (`variety`, `cells_changed`, `kind_quiet_for`, `kind_counts`). |
| GET | `/runs/{run_id}/grids` | `get_grids` (routes.py:528) | Packed binary grid frames for a tick range (REQ-11.5). |
| GET | `/runs/{run_id}/export` | `export_run` (routes.py:587) | The same tick range as plain, uncapped JSON — for scripts, not the player. |
| GET | `/runs/{run_id}/cell/{y}/{x}` | `get_cell_history` (routes.py:638) | One cell's full property history across the run. |
| PATCH | `/runs/{run_id}` | `correct_run` (routes.py:670) | The only mutation on a stored run: `user_behavior`, `user_flagged`. |
| GET | `/catalog/modifiers` | `get_modifier_catalog` (routes.py:705) | The modifier catalog, read-only in v1. |
| GET | `/library/summary` | `library_summary` (routes.py:711) | Totals, coverage map, rejection tally — the same object Stage A's context is built from. |
| GET | `/library/feed.rss` | `library_feed` (routes.py:729) | RSS 2.0 feed of newly invented public rules. |

### `stream.py` — generation

| Method | Path | Function | Purpose |
|---|---|---|---|
| POST | `/rules/generate` | `generate` (stream.py:66) | The full Stage A → B → C pipeline, streamed as `text/event-stream`. |

### `comments.py` — comments on rules

| Method | Path | Function | Purpose |
|---|---|---|---|
| GET | `/rules/{rule_id}/comments` | `list_comments` (comments.py:102) | List comments on a rule. |
| POST | `/rules/{rule_id}/comments` | `create_comment` (comments.py:113) | Post a comment (requires sign-in, rate-limited). |
| PATCH | `/comments/{comment_id}` | `edit_comment` (comments.py:136) | Edit your own comment. |
| DELETE | `/comments/{comment_id}` | `delete_comment` (comments.py:160) | Delete your own comment (idempotent). |

### `profile.py` — the one editable identity bit

| Method | Path | Function | Purpose |
|---|---|---|---|
| GET | `/profile` | `get_profile` (profile.py:48) | Read your display-name override. |
| PUT | `/profile` | `set_profile` (profile.py:55) | Set (or clear) it. |

### `system.py` — observability (new in 2.2.1)

| Method | Path | Function | Purpose |
|---|---|---|---|
| GET | `/system/status` | `system_status` (system.py:38) | Live snapshot: generations in flight, corpus totals, error and throughput counts, active/idle session counts, database size, process uptime. |
| GET | `/system/sessions` | `system_sessions` (system.py:91) | Paged, merged history of both session kinds — generation sessions and HTTP sessions — newest first. |

Both are read-only, both are polled every two seconds by the frontend, and both are **unauthenticated** — see §9 and §11.

REQ-11.1's table in the spec lists a smaller core set (`/rules/generate`, `/rules`, `/rules/{id}`, `/rules/{id}/runs`, `/runs/{id}`, `/runs/{id}/grids`, `/runs/{id}/cell/{y}/{x}`, `PATCH /runs/{id}`, `/catalog/modifiers`, `/library/summary`) — everything else (slugs, favorites, previews, export, RSS, comments, profile) is a later addition layered on top without breaking that original contract.

---

## 2. The generate endpoint's streaming design

`POST /rules/generate` is the one place in the API that isn't a plain request/response. The docstring at the top of `stream.py` states the constraint outright:

```python
"""POST /rules/generate — the pipeline as a progress stream (REQ-11.4).

The response is text/event-stream from a POST, consumed by the browser
with streaming fetch() — never EventSource, which cannot POST, and
never a POST-then-GET job model, which would reintroduce the queue
REQ-3.6 excludes (REQ-11.4.1).

The pipeline runs in a worker thread with its own database connection;
events cross to the response generator through a queue.
"""
```
(stream.py:1-10)

**Why `EventSource` is off the table.** The browser's native `EventSource` API only issues GET requests — it has no method for attaching a request body, and generation needs one (`visibility`, `spark`, `title`). The spec is explicit about this being a hard platform limitation, not a design preference: "The browser's native `EventSource` **cannot issue a POST.** The frontend must consume this with streaming `fetch()` and a `ReadableStream` reader." (asr-requirements-v3.md:999-1000). So the backend emits a normal `text/event-stream` body from a POST handler, and the frontend has to hand-roll SSE parsing over `fetch()`'s streaming body reader instead of getting it for free from `EventSource`.

**Why a job-queue model was explicitly rejected.** The obvious alternative — `POST /rules/generate` kicks off a background job and returns a job id, the client polls or opens a `GET /jobs/{id}` `EventSource` — was considered and ruled out at the spec level. REQ-3.6 states the constraint the whole app is built around: "Generation is synchronous — one click, one rule. No job queue, no background workers. Progress is streamed within the single request." (asr-requirements-v3.md:119-120). REQ-11.4.1 then closes the door on smuggling a queue back in through the transport layer: "Do not 'fix' this by converting the API into an asynchronous POST-then-GET job model — that reintroduces exactly the queue REQ-3.6 excludes." (asr-requirements-v3.md:1000-1002). `stream.py`'s docstring echoes the same reasoning inline at the point of implementation, which is the strongest evidence this isn't just spec ceremony — it shaped the actual code.

What a job queue would cost architecturally, beyond violating REQ-3.6 on principle: this is a **single-user, local app** (REQ-3.4) with no need for concurrent job scheduling, retry semantics, or worker-pool management — introducing a queue would add an entire subsystem (persistence for job state, a polling or second-stream endpoint, cancellation semantics) to solve a problem that doesn't exist here. It would also blur the one-shot nature of generation: REQ-8.6 ("One rule, one vote") already has to work to keep a single canonical run's outcome from being double-counted; a queue that could enqueue multiple in-flight generations, or that let a client walk away and reconnect to a stale job, opens exactly the kind of indirect-influence-on-Stage-A surface that REQ-8.5 and REQ-8.6 are built to close (user signals never enter generation context, and only a canonical run counts). Keeping generation synchronous and single-request means the whole lifecycle lives inside one HTTP request's queue-drain loop.

> **Qualified in 2.2.1.** The 2.2.0 text of this paragraph ended by claiming there is "no external state describing 'a generation in progress' for anything else in the app to observe, correlate with, or be biased by." That is no longer literally true: `generation_sessions` is exactly such state, and the system page observes it (§11). The architectural argument survives, but it has to be made more precisely now, so it is worth separating the two claims that were previously bundled together.
>
> What made a job queue objectionable was never *observability* — it was **ownership of the work**. A queue means the request that starts generation is not the thing that performs it: work outlives its request, something else must claim it, and the client's connection becomes incidental to whether the rule gets made. That is what REQ-3.6 forbids and what 2.2.1 does not do. A `generation_sessions` row is a *record that a request is running*, written by that request, in that request's own thread and connection; nothing claims it, nothing resumes it, and if the process dies the work is simply gone (document 4, §10).
>
> The "biased by" half of the original claim does still hold in full, and it is the half that matters most: nothing in generation context reads this table. See document 4, §10, "What this does *not* do."

**The actual streaming implementation.** The pipeline itself (`asr.generation.pipeline.generate_rule`) runs synchronously, but it can't run on FastAPI's async event loop thread without blocking every other request for the length of a full Stage A/B/C round trip (which includes real network calls to Anthropic and a full-grid trial run). So it's pushed onto a worker thread with its own SQLite connection, and events cross back to the HTTP response generator through a thread-safe `queue.Queue`:

```python
def _run_pipeline(database_path: str, events: queue.Queue, owner_uid, visibility, spark, title) -> None:
    conn = db.connect(database_path)
    try:
        payload = generate_rule(
            conn, lambda name, data: events.put((name, data)),
            owner_uid=owner_uid, visibility=visibility, spark=spark,
        )
        if title and payload.get("rule_id") is not None:
            _apply_title(conn, payload["rule_id"], title)
    except Exception as failed:  # noqa: BLE001 - the stream must always end
        # The browser only sees the tail; the server log keeps the
        # whole story so a transient API failure is diagnosable later.
        logger.exception("generation pipeline failed")
        events.put((FINAL_EVENT, {"status": "error", "error": str(failed)[-500:]}))
    finally:
        conn.close()
        events.put(None)
```
(stream.py:47-63)

Note the `except Exception` guard is deliberately broad (`# noqa: BLE001`) with a comment explaining why: whatever else happens, **the stream must always end**. A generator function backing a `StreamingResponse` that never terminates its underlying iterator leaves the HTTP connection open forever; the `finally: events.put(None)` is the sentinel the consumer loop below watches for, guaranteeing termination even on an unhandled failure deep in the pipeline. The exception's own text is logged in full server-side (`logger.exception`) but truncated to 500 characters before it ever reaches the browser (`str(failed)[-500:]`) — the last 500 characters specifically, so a long traceback-derived message still surfaces the actionable tail rather than getting cut off mid-sentence at the front.

The route handler wires the thread and the response together:

```python
@router.post("/rules/generate")
def generate(
    request: Request,
    body: GenerateRequest | None = Body(default=None),
    user: dict | None = Depends(get_current_user),
):
    ...
    events: queue.Queue = queue.Queue()
    worker = threading.Thread(
        target=_run_pipeline,
        args=(request.app.state.database_path, events, owner_uid, visibility, spark, title),
        daemon=True,
    )
    worker.start()

    def event_stream():
        while True:
            item = events.get()
            if item is None:
                break
            name, data = item
            yield f"event: {name}\ndata: {json.dumps(data)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```
(stream.py:66-111, abridged)

`event_stream()` is a plain generator that blocks on `events.get()` — a synchronous blocking call — inside what's otherwise an async request handler. FastAPI/Starlette runs a generator-based `StreamingResponse` body iterator in a thread pool automatically when it's a regular (non-async) generator, so this blocking `.get()` doesn't stall the event loop; it's exactly the same mechanism that lets the synchronous pipeline thread and the response iterator hand off cleanly without any asyncio-specific plumbing in `stream.py` itself. Two response headers matter operationally: `Cache-Control: no-cache` (an SSE stream must never be cached or replayed by an intermediary) and `X-Accel-Buffering: no` (tells an nginx-style reverse proxy not to buffer the response body before forwarding it, which would defeat the whole point of streaming progress to the browser in near-real-time).

---

## 3. SSE event framing

Each event is written to the wire in the standard SSE two-line-plus-blank-line shape — `event: <name>\ndata: <json>\n\n` — built directly in `event_stream()` (stream.py:105): `yield f"event: {name}\ndata: {json.dumps(data)}\n\n"`. The event names themselves are not enumerated in `stream.py` (that file just forwards whatever `(name, data)` tuples the pipeline callback produces); the spec is the source of truth for the vocabulary:

> `POST /rules/generate` responds `text/event-stream` and emits `stage_a_started`, `stage_a_complete`, `stage_b_started`, `stage_b_complete`, `validating`, `validation_failed`, `repairing`, `running`, `tick_progress`, and `complete`. (asr-requirements-v3.md:994-996)

`stream.py` hard-codes exactly one of these names as a constant, because it's the one the route itself needs to recognize on the error path:

```python
FINAL_EVENT = "complete"
```
(stream.py:30)

Every other event name is opaque to `stream.py` — it's just forwarding `(name, data)` pairs the callback passed to `generate_rule` produces, and `generate_rule` lives in `asr/generation/pipeline.py` (this doc's subsystem is the transport, not the pipeline's internal stage machine — see the generation-pipeline deep-dive for the emitting side in full). What's visible and load-bearing here is the *contract*: whatever stage names the pipeline emits, they all arrive at the client as `event: <name>` lines, and the pipeline is guaranteed to eventually emit one `complete` event (`FINAL_EVENT`) — either the pipeline's own success payload, or, on an unhandled exception, the synthesized `{"status": "error", "error": ...}` payload constructed in `_run_pipeline`'s except block (stream.py:60). This is why the frontend can treat `complete` as the definitive "the stream is done, render one final state" signal regardless of which path produced it.

---

## 4. Binary framing touchpoints

Grid data — the per-tick, per-cell arrays that drive playback — never travels as JSON. REQ-11.5 states the reasoning: "Grid payloads are packed binary, never nested JSON arrays. Twenty million JSON integers per property per run is not a viable transport for 30fps playback." (asr-requirements-v3.md:1004-1006). The actual byte layout (REQ-11.5.1) is a 4-byte little-endian header-length prefix, a UTF-8 JSON header describing tick range/shape/per-property offsets, then a flat payload region of C-order array blocks — fully specified in `framing.py`:

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
(framing.py:1-11)

The full depth of *how* those arrays get reconstructed from stored snapshots and deltas belongs to the storage-layer doc in this series. What belongs here is the route-level handoff — how `GET /runs/{run_id}/grids` turns a tick range into that byte stream:

```python
@router.get("/runs/{run_id}/grids")
def get_grids(
    run_id: int,
    request: Request,
    from_tick: int = Query(0, alias="from", ge=0),
    to_tick: int | None = Query(None, alias="to", ge=0),
    props: str = "kind",
    user: dict | None = Depends(get_current_user),
    conn=Depends(get_db),
):
    row = conn.execute(
        """SELECT runs.ticks_run, rules.visibility AS rule_visibility, rules.owner_uid AS rule_owner_uid
           FROM runs JOIN rules ON rules.id = runs.rule_id WHERE runs.id = ?""",
        (run_id,),
    ).fetchone()
    if row is None or _rule_hidden_from(row["rule_visibility"], row["rule_owner_uid"], user):
        raise HTTPException(404, "no such run")
    last = row["ticks_run"] if to_tick is None else min(to_tick, row["ticks_run"])
    if from_tick > last:
        raise HTTPException(400, "empty tick range")
    if last - from_tick + 1 > MOST_TICKS_PER_GRID_REQUEST:
        raise HTTPException(
            400, f"ask for at most {MOST_TICKS_PER_GRID_REQUEST} ticks per request"
        )
    names = [p.strip() for p in props.split(",") if p.strip()]
    cache = request.app.state.cache
    try:
        stacks = {
            name: cache.property_history(conn, run_id, name)[from_tick : last + 1]
            for name in names
        }
    except KeyError as missing:
        raise HTTPException(400, f"this run has no property named {missing}")
    from asr.api.framing import frame_grids

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
(routes.py:528-584)

The route's own job, layered on top of the binary format itself, is small but specific: enforce the visibility check before touching any data (same `_rule_hidden_from` 404-shaped gate used everywhere else — Section 5 covers it), clamp the requested range to what actually ran, cap the request at `MOST_TICKS_PER_GRID_REQUEST = 250` ticks (routes.py:27) so one request can't demand an unbounded slab of memory, pull each requested property out of `request.app.state.cache` (the `ReconstructionCache` instance created once in `create_app` — app.py:31), hand the resulting `{name: array}` stacks to `frame_grids` to pack, and optionally gzip the packed bytes if the client's `Accept-Encoding` says it can decompress — a comment at routes.py:571-574 notes this is pure wire compression layered *outside* the REQ-11.5.1 framing, cutting transfer size roughly 20x on the highly repetitive grid data without changing the framing contract itself; "the browser undoes transport encoding before the decoder ever sees the bytes." `GET /runs/{run_id}/cell/{y}/{x}` (routes.py:638) reuses the same cache for a single-position history slice, returned as plain JSON rather than binary framing since one cell's series is small; `GET /runs/{run_id}/export` (routes.py:587) deliberately sidesteps the binary format entirely, returning the same tick range as uncapped plain JSON for scripts that would rather `json.loads` a response than implement a binary parser.

---

## 5. The immutability endpoint

`PATCH /runs/{run_id}` is the only endpoint in the entire API that mutates a previously stored run, and the constraint is stated three times independently — in the requirements spec, in `routes.py`'s module docstring, and again on the handler itself — which is a strong signal of how deliberately this boundary is being protected:

- REQ-11.3: "No endpoint may modify a stored run other than `PATCH /runs/{id}` setting `user_behavior` and `user_flagged`. Recorded history is immutable." (asr-requirements-v3.md:1028-1029)
- `routes.py`'s module docstring: "Recorded history is immutable: the only write this API performs on a stored run is the PATCH setting user_behavior and user_flagged (REQ-11.3)." (routes.py:4-6)
- The handler's own docstring, quoted below.

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
(routes.py:665-702)

Two implementation details enforce the "never overwrites the guess" property structurally rather than by convention. First, `user_behavior` and `guessed_behavior` are separate columns — the `UPDATE` statement only ever touches `user_behavior`; `guessed_behavior` (the machine classifier's original verdict, written once at run-save time) is never targeted by any `UPDATE` in this file. Second, the handler checks `body.model_fields_set` rather than truthiness of the fields — `provided = body.model_fields_set` (routes.py:687) — which is a Pydantic v2 mechanism for distinguishing "the client explicitly sent `user_behavior: null`" (clear the override) from "the client didn't mention `user_behavior` at all" (leave it untouched). Without that distinction a `PATCH` that only wants to set `user_flagged` would silently null out any previously-set `user_behavior`, because both fields default to `None` on the Pydantic model.

What this endpoint deliberately does **not** allow changing: the rule's `description`, `source_code`, `reasoning`, any provenance field, the run's `seed`/`width`/`height`/`max_ticks`/`ticks_run`/`stopped_because`/`loop_length`, the classifier's own `guessed_behavior`/`guess_confidence`, or `is_canonical`. There is no endpoint anywhere in `routes.py` that deletes a run or a rule. The only other place any row in `rules` or `runs` changes after creation is `PATCH /rules/{rule_id}` (`set_rule_title`, routes.py:346), which is scoped just as narrowly — it only ever writes `title` and its derived `slug`, never the AI-generated `description` those fields sit alongside. Section 8's Stage A exclusion depends on exactly this boundary holding: `user_behavior` and `user_flagged` are "stored and displayed but never enter the generation context" per REQ-8.5, and the reason that's actually true and not just a policy statement is that `generation/context.py`'s queries simply never select those two columns.

---

## 6. Firebase auth — Phase 1

### How an ID token gets verified server-side

The entire verification surface is `auth.py` — 67 lines as of 2.2.1, with two public entry points over one shared verifier. Its docstring frames the design intent precisely:

```python
"""Optional Firebase ID-token verification (Phase 1: Email/Password
only). A missing Authorization header is anonymous, never an error —
every route this is used on must keep working with no header sent,
exactly as it did before this feature existed. A present-but-invalid
token is always an error; that's the one case this must never
silently resolve to "treat as anonymous."

No service-account secret is involved: verify_firebase_token checks a
token's signature against Google's public keys and confirms it names
this project, using only the (non-secret) project ID.
"""
```
(auth.py:1-11)

```python
_transport = google_requests.Request()


def _bearer_token(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if not header or not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    return token or None


def _verify(token: str) -> dict:
    """Raises on any failure -- signature, issuer, or missing subject."""
    claims = google_id_token.verify_firebase_token(
        token, _transport, audience=settings.firebase_project_id,
    )
    expected_issuer = f"https://securetoken.google.com/{settings.firebase_project_id}"
    if claims is None or claims.get("iss") != expected_issuer or not claims.get("sub"):
        raise ValueError("issuer or subject check failed")
    return claims


def get_current_user(request: Request) -> dict | None:
    token = _bearer_token(request)
    if token is None:
        return None
    try:
        claims = _verify(token)
    except Exception as failed:
        raise HTTPException(401, f"invalid auth token: {failed}") from None
    return {"uid": claims["sub"], "email": claims.get("email")}
```
(auth.py:21-52)

**What changed in 2.2.1 and what didn't.** Header parsing and claim verification were extracted into `_bearer_token` and `_verify` so a second caller could reuse them. `get_current_user`'s behavior is byte-for-byte what it was: no header is anonymous, a bad token is a hard 401. The extraction exists to serve `try_resolve_uid`, below.

Mechanically: `verify_firebase_token` (from `google.oauth2.id_token`, part of the `google-auth` package) validates the JWT's signature against Google's published public keys for Firebase-issued tokens, fetched over HTTPS and cached in-process by the underlying `google.auth.transport.requests.Request` transport (`_transport`, reused module-wide at auth.py:21 rather than re-created per request). No Firebase Admin SDK service-account key is needed anywhere in this app — only the Firebase project ID, which is not a secret and is passed as the expected `audience`. On top of the library's own signature check, `get_current_user` layers two of its own: the token's issuer (`iss` claim) must be exactly `https://securetoken.google.com/{firebase_project_id}`, and it must carry a non-empty `sub` (subject) claim, which becomes the stable per-user id (`uid`) the rest of the app keys everything on.

### Anonymous path vs. hard failure

The docstring's central design rule shows up as the function's very first branch: no `Authorization` header, or a header that isn't a `Bearer` token, returns `None` — not an exception. `None` here means "anonymous," and it is a completely ordinary, successful return value, which is what lets `get_current_user` be used as a plain FastAPI `Depends()` on routes that must keep working with zero auth machinery involved at all. But the moment a token *is* present and fails verification for any reason — bad signature, wrong project, expired, tampered — the function raises `HTTPException(401, ...)` unconditionally. There is no code path where a bad token quietly degrades to "treated as anonymous." `architecture.md`'s phase-log entry confirms this was verified live, not just asserted in code: "a garbage token still hard-401s rather than silently passing as anonymous." (architecture.md:224-225)

### `try_resolve_uid`: the second identity path, and why it must never gate anything (new in 2.2.1)

The session middleware (§10) needs to know *who* a request belongs to, if anyone, in order to record it against an `http_sessions` row. It cannot use `get_current_user`, and the reason is the rule just described: `get_current_user` raises a hard 401 on a bad token, and the middleware runs on **every request to every route**. A user whose token expired in a background tab would get a 401 on the CSS file, the library listing, and everything else — the entire site would fail, to update a "last seen" timestamp.

So 2.2.1 adds a second entry point with the opposite failure posture (`auth.py:54-67`):

```python
def try_resolve_uid(request: Request) -> str | None:
    """Best-effort identity for session bookkeeping ONLY -- never use this
    to gate access to anything. Unlike get_current_user, a present-but-
    invalid token here is not an error: this runs on every request via
    the session middleware (api/app.py), and a stale token must not 401
    the entire site just to update a "last seen" timestamp.
    """
    token = _bearer_token(request)
    if token is None:
        return None
    try:
        return _verify(token)["sub"]
    except Exception:
        return None
```

This is a genuinely dangerous function to have in a codebase, and the docstring's shouted "**never use this to gate access to anything**" is proportionate rather than decorative. It is the single function in this app that does what every other layer is built to prevent: silently treating an invalid token as anonymous. Given a route that used it for authorization, an attacker with any malformed token would be handed the anonymous view rather than a 401 — which for public content looks like success, and is exactly the "silently downgraded" behavior the Firebase phase went out of its way to make impossible.

Three things keep that from happening, and it is worth being explicit that they are conventions rather than type-level guarantees:

1. **It returns a bare `str | None`, not the `dict` shape** every access check consumes. `_rule_hidden_from(visibility, owner_uid, user)` expects the `{"uid": ..., "email": ...}` dict; handing it a string would not silently authorize anything, it would misbehave immediately.
2. **It is not a FastAPI dependency.** It takes a `Request` directly and is never written as `Depends(try_resolve_uid)`, so it cannot be attached to a route the way `get_current_user` routinely is.
3. **It has exactly one caller** — the middleware in `app.py` — which is the property to check if this function ever appears in a diff.

The shared `_verify` between the two paths is what makes the pairing safe rather than duplicative: both do identical cryptographic verification against the same issuer and audience. They differ in one respect only — what to do when that verification fails — and that difference is the entire reason both exist.

### The per-route access-check pattern

Nearly every handler in `routes.py`, `comments.py`, and `profile.py` takes `user: dict | None = Depends(get_current_user)` and then branches on it in one of two shapes. The first shape guards an action that plainly requires an identity — no ambiguity about visibility, just "you must be signed in to do this":

```python
@router.post("/rules/{rule_id}/favorite")
def add_favorite(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    if user is None:
        raise HTTPException(401, "sign in to favorite a rule")
    ...
```
(routes.py:377-380)

The second shape is the one that recurs on almost every rule- and run-scoped GET: a helper that decides whether the *content itself* is visible to whoever's asking, independent of whether they're signed in at all:

```python
def _rule_hidden_from(visibility: str, owner_uid: str | None, user: dict | None) -> bool:
    """A private rule is invisible to everyone except its owner. Every
    caller of this raises the exact same 404 message as a genuine
    not-found, so the response never distinguishes "doesn't exist"
    from "exists but isn't yours."
    """
    return visibility == "private" and (user is None or user["uid"] != owner_uid)
```
(routes.py:38-44)

used, for example, in `get_rule`:

```python
@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    row = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    return _full_rule_detail(row, user, conn)
```
(routes.py:321-326)

The deliberate choice here is that a hidden private rule and a rule that genuinely doesn't exist return the *identical* 404 — same status code, same message string ("no such rule" / "no such run" depending on the resource) — so the API surface never leaks the existence of a private rule to someone who isn't its owner. This same helper gates `get_rule_by_slug`, `set_rule_title`, `add_favorite`/`remove_favorite`, `rule_preview_image`, `rerun_rule`, `get_run`, `get_grids`, `export_run`, `get_cell_history`, `correct_run`, and `list_comments`/`create_comment` — every single resource-scoped read or write in the app funnels through this one function, which is what makes the visibility guarantee uniform rather than something re-derived ad hoc per route.

### The personal library layered on the global one

Concretely, "layered on" means one additional SQL predicate on the existing `rules` table, gated by an existing query parameter, not a separate table or a separate endpoint. `GET /rules` (`list_rules`, routes.py:186) takes a `mine: bool = Query(False)` parameter — this is the `mine=true` seen in traces like `GET /rules?sort=newest&mine=true&page=1`. The branch that implements it:

```python
    # The default listing is always the public/global library, no
    # matter who's asking. mine=true is the personal library --
    # everything you own, public or private -- and requires sign-in.
    if mine:
        if user is None:
            raise HTTPException(401, "sign in to view your personal library")
        clauses.append("rules.owner_uid = ?")
        params.append(user["uid"])
    else:
        clauses.append("rules.visibility = 'public'")
```
(routes.py:219-228)

So the two libraries are the same table, the same route, the same pagination and sort machinery — only the `WHERE` clause differs. The default (global) library is always `visibility = 'public'` regardless of whether the caller is signed in; the personal library (`mine=true`) is every rule the caller owns, `owner_uid = <their uid>`, public or private alike, and requires sign-in (401 otherwise) since there's no meaningful "mine" for an anonymous caller. `architecture.md`'s phase-log entry for this describes the frontend side of the same idea: "a `mine` prop reusing `Library.jsx` for `#/mine` rather than forking the view" (architecture.md:202-203) — one component, one backend route, a boolean flag threading through both layers instead of a parallel personal-library implementation.

---

## 7. Public/private choice at rule-creation time

Server-side, visibility is a plain column on the `rules` table — `rules.visibility`, a string (`'public'` or `'private'`), added by the Phase 1 migration alongside `rules.owner_uid`, both introduced via "a two-column additive migration ... via a new idempotent `db._ensure_columns` step" (architecture.md:171-174). The column defaults to `'public'`, and every pre-existing rule was backfilled to `visibility='public'`, `owner_uid=NULL` when the migration ran against the live database (architecture.md:217-218) — so nothing about existing data changed shape or meaning.

The choice is made at the moment of generation, via `POST /rules/generate`'s request body:

```python
class GenerateRequest(BaseModel):
    visibility: Literal["public", "private"] = "public"
```
(stream.py:33-34)

and the handler enforces the actual policy — private requires sign-in, and an anonymous request can never smuggle itself into private no matter what it asks for:

```python
    visibility = body.visibility if body else "public"
    if visibility == "private" and user is None:
        raise HTTPException(400, "sign in to create a private rule")
    owner_uid = user["uid"] if user else None
    if user is None:
        visibility = "public"  # anonymous requests are always public/global
```
(stream.py:75-80)

Note the body itself is optional — `body: GenerateRequest | None = Body(default=None)` (stream.py:69) — specifically so the endpoint keeps accepting the exact bare, bodyless POST the frontend has always sent; `architecture.md` calls this out as the specific mechanism: "`Body(default=None)`, not a defaulted model instance, is what keeps accepting today's bare bodyless POST unchanged." (architecture.md:187-189) This is the concrete form of CLAUDE.md's "Rules stay public/anonymous by default" — the default is enforced at three independent layers: the Pydantic field default (`"public"`), the column default in the schema migration, and the explicit anonymous-forces-public override in the route handler, so there's no path (missing body, missing auth, or an explicit-but-unauthenticated `"private"` request) that produces a private, ownerless rule.

---

## 8. Stage A exclusion for authenticated users

"Stage A exclusion" refers to a blanket filter applied everywhere `asr/generation/context.py` builds anything that will be rendered into a Stage A prompt or displayed as the shared library summary: every query in that module that touches the `rules` table adds `WHERE rules.visibility = 'public'` (or an equivalent join condition). The module's own docstring states the principle explicitly:

```python
"""...
Every query here also excludes private rules entirely (Firebase auth
Phase 1) -- not just from what's displayed, but from what gets
rendered into the prompt at all, extending REQ-8.5's principle
("user-specific signal never enters generation context") to another
user's private content. This module is also what GET /library/summary
serves, so the same filter keeps a private rule out of the public
library-summary display too -- one implementation, one guarantee.
"""
```
(context.py:1-17)

and the filter itself appears repeatedly, e.g. in `coverage_map`:

```python
    for row in conn.execute(
        """SELECT rules.kinds, rules.neighbors, rules.reach,
                  rules.requested_shape, rules.modifiers_json,
                  rules.semantic_slots_json, canon.guessed_behavior
           FROM rules
           LEFT JOIN runs canon
             ON canon.rule_id = rules.id AND canon.is_canonical = 1
           WHERE rules.visibility = 'public'"""
    ):
```
(context.py:54-62)

The same `WHERE rules.visibility = 'public'` clause recurs at context.py:100 (recent failure modes / rejection-adjacent broken-rule query) and context.py:125 and context.py:216 (the example-selection queries — most recent, most notable, thinly-attempted-cell examples). Why this matters architecturally: REQ-8.5 already establishes that "Stage A context is built exclusively from machine-derived outcomes" and that user behavior overrides and flags are "stored and displayed but never enter the generation context" (asr-requirements-v3.md:700-703) — that closed one back door (a user's *opinion* about a rule leaking into generation). The Firebase auth phase opened a second, structurally different back door — one user's *private content* leaking into what another (or an anonymous) generation run sees — and this filter closes it by construction: a private rule contributes nothing to the coverage map's counts, nothing to the totals, and nothing to the example blocks Stage A reads, regardless of who eventually generates the next rule. `architecture.md`'s phase-log entry notes this was verified beyond just code review: "verified by asserting a marked-private rule's description never appears in the rendered Stage A prompt text at all, not just hidden from a UI." (architecture.md:192-194) — i.e. there's a test that renders an actual Stage A prompt and greps for the excluded content, not just a check that a list endpoint omits it.

One deliberate asymmetry, called out as a known limitation rather than an oversight: a *failed* private generation attempt still increments the shared rejection tally as an anonymous count. `architecture.md`: "A private generation attempt that fails still nudges the shared coverage map as an anonymous count (no text, no attribution) via the pre-existing rejections table, which has no owner/visibility concept in this phase — judged consistent with 'content excluded,' not a violation of it, but a judgment call rather than a settled question." (architecture.md:230-235)

---

## 9. Explicitly out of scope for this phase

CLAUDE.md states the phase's scope boundary directly: "See `documents/architecture.md`'s phase log for the full design ... and what's still out of scope (OAuth providers, per-user run corrections, TLS)." `architecture.md`'s own phrasing of the same boundary, from the top of the Phase 8 entry: "optional multi-user support layered on the single-user app, deliberately conservative — added, not decided by, this phase: OAuth providers, per-user run corrections, TLS." (architecture.md:165-168)

- **OAuth providers.** Only Email/Password sign-in exists. The phase log's "Step 0 spike" explains the concrete reason it wasn't OAuth: "Firebase Email/Password was chosen over OAuth specifically because the droplet has no domain or TLS yet — OAuth's redirect flow needs a domain on Firebase's authorized-domains allowlist (bare IPs aren't accepted there), while Email/Password is a direct API call with no such check." (architecture.md:206-211) This was confirmed empirically, not just reasoned about: "Confirmed by creating a real throwaway account via the Identity Toolkit REST API and feeding the token to `verify_firebase_token` two ways: a real token accepted with correct `aud`/`iss`/`sub` claims, a hand-tampered one rejected outright." (architecture.md:211-214)
- **Per-user run corrections.** `PATCH /runs/{id}` (Section 5) is unauthenticated in the sense that it doesn't check who's setting `user_behavior`/`user_flagged` — there's no per-user attribution or exclusivity on a correction; a correction is a fact about the run, not a fact about who made it. Making corrections per-user (e.g. showing "your" flag distinct from someone else's) was left out of this phase.
- **TLS.** The app runs over plain HTTP, and Bearer tokens travel over that same plain HTTP connection. `architecture.md`'s "known limitations, carried forward deliberately" section is explicit: "Bearer tokens travel over plain HTTP until TLS exists — dev/trusted-network auth only, not yet safe for a hostile network." (architecture.md:228-230)
- **An access check on `/system/*`** (new in 2.2.1). The system routes are unauthenticated and globally visible, the same as every other route in this single-user app — but they expose more than the others do (IP addresses, User-Agents, visited paths, generation error text). `system.py`'s own docstring carries the condition for revisiting it: "If it ever goes multi-user, `/system/*` needs an access check the same way `#/mine` does today." See §11.

---

## 10. The session-tracking middleware

`app.py` installs one piece of HTTP middleware, applied to every request regardless of route or auth state. At 2.2.0 it was `log_request_timing` and did only the logging described below; 2.2.1 renamed it to `track_request` and gave it a second job — maintaining the `http_sessions` row that the system page reads (`app.py:66-96`):

```python
    @app.middleware("http")
    async def track_request(request: Request, call_next):
        # One line per request (method, path, status, wall time) plus the
        # colloquial HTTP session: a cookie identifies the browser, and
        # every request -- not just ones a client remembers to report --
        # touches that session's "last seen." No heartbeat, no client
        # bookkeeping, nothing to go stale if the client misbehaves.
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %d (%.1fms)",
            request.method, request.url.path, response.status_code, elapsed_ms,
        )

        session_id = request.cookies.get(SESSION_COOKIE) or secrets.token_urlsafe(24)
        conn = db.connect(app.state.database_path)
        try:
            db.touch_http_session(
                conn, session_id, try_resolve_uid(request),
                _client_ip(request),
                request.headers.get("user-agent"),
                request.url.path,
            )
        finally:
            conn.close()
        response.set_cookie(
            SESSION_COOKIE, session_id, max_age=SESSION_MAX_AGE_SECONDS,
            httponly=True, samesite="lax",
        )
        return response
```

### The session half

The cookie is `asr_session`, a 24-byte `secrets.token_urlsafe` value with a 24-hour `max_age` (`app.py:22-23`) that is re-set on every response, making it a sliding window rather than a fixed expiry. It is `httponly` (no JavaScript access — the frontend never reads or needs it) and `samesite="lax"`.

Two properties of the design are worth drawing out, because they are the entire reason this replaced the heartbeat that preceded it (document 2, §1):

**It cannot be starved by client behavior.** The session is touched by traffic that is already happening for other reasons. There is no interval to miss, no unmount handler to fire, no throttled background tab. The one thing a client must do — send back a cookie — is done by the browser itself.

**It runs after `call_next`, so it records outcomes rather than intentions.** The row is written once the response exists, which means a request that 404s or 401s still counts as activity.

The cost is honest and worth naming: a fresh SQLite connection is opened, written, and closed on **every single HTTP request**, including static assets. That is a real per-request cost accepted deliberately for a single-user local app, and it is the first thing to revisit if this ever serves meaningful traffic. WAL mode (document 2, §1) is what keeps it from serializing against readers.

### Why the client IP needs a helper

`_client_ip` (`app.py:34-52`) exists because the obvious `request.client.host` is wrong in this app's normal configuration:

```python
def _client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    ip = forwarded.split(",")[0].strip() if forwarded else None
    if not ip:
        ip = request.client.host if request.client else None
    if ip and ip.startswith("::ffff:"):
        ip = ip[len("::ffff:"):]
    return ip
```

In development, browser traffic reaches this process through Vite's proxy, which makes its own outbound connection — so `request.client.host` is the proxy's loopback address for every visitor alike. The comment records that this was not theoretical: it "is what api/app.py's session tracking was silently recording until this was added." The fix has a frontend half (`xfwd: true` on every proxy entry, document 6, §11) that sets `X-Forwarded-For`; this function prefers that header's first entry and falls back to the socket address for direct requests such as tests.

The `::ffff:` unwrapping handles the other half of the same confusion. Vite's dev server listens dual-stack, so Node commonly reports a plain IPv4 connection as an IPv4-mapped IPv6 address — `::ffff:203.0.113.7` is the same address as `203.0.113.7`, written in a form that reads as IPv6 to anyone scanning the system page. Stripping the prefix is presentation, not normalization of anything semantic.

**A caution this code does not need but a future version would:** `X-Forwarded-For` is a client-settable header, trustworthy only when something you control sets it. Here that is Vite's proxy in dev, and the values are used for nothing but display on an unauthenticated debug page, so trusting it costs nothing. If this app ever puts a real reverse proxy in front of itself — or uses these addresses for rate limiting, blocking, or any decision at all — the header must be trusted only from known proxy addresses.

### The logging half (unchanged from 2.2.0)

The log line format that produces is `asr.api.app <METHOD> <PATH> -> <STATUS> (<MS>ms)` — the `asr.api.app` prefix comes from the module-level `logger = logging.getLogger(__name__)` (app.py:24) combined with the format string configured just above it:

```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
```
(app.py:23)

so a real line reads something like `2026-08-20 14:03:11,204 asr.api.app GET /rules?sort=newest&mine=true&page=1 -> 200 (12.4ms)`. The comment above `logging.basicConfig` explains why this call exists at all: "Without this, the root logger's default level (WARNING) would silently swallow the INFO-level timing lines below and in generation/pipeline.py -- there was no logging config anywhere in the app before this, so nothing was actually visible." (app.py:19-22) `time.perf_counter()` is used rather than `time.time()` because it's a monotonic clock meant for measuring elapsed intervals, immune to system clock adjustments mid-request. This is explicitly not a metrics/profiling subsystem — the comment calls it "a paper trail," useful for eyeballing which endpoint got slow, not for aggregation, percentiles, or alerting.

---

## 11. The system routes (new in 2.2.1)

`system.py` serves the `#/system` dashboard. Its module docstring states both what it is for and the boundary it sits on:

```python
"""The system page: live pipeline activity plus a browsable history of
both kinds of session this app has ("what the hell is going on" per the
request that started this) -- generation_sessions (one row per
POST /rules/generate, written by generation/pipeline.py) and http_sessions
(the colloquial HTTP session: one row per session cookie, touched by every
request via the middleware in api/app.py -- no client cooperation needed).

Deliberately unauthenticated and globally visible for now, same as every
other route -- this app is single-user. If it ever goes multi-user,
/system/* needs an access check the same way #/mine does today (see
CLAUDE.md).
"""
```
(system.py:1-12)

### `GET /system/status` — the live snapshot

`system_status` (`system.py:38-87`) runs six small aggregate queries and returns one flat object: in-flight generations (`WHERE finished_at IS NULL`), rules and runs totals, errors in the last 24 hours, generations in the last hour, active and idle session counts, database file size, and process uptime.

**The `no-store` header is the one non-obvious line in the file** (`system.py:45`):

```python
    response.headers["Cache-Control"] = "no-store"
```

The comment explains the exposure: every response here is a live snapshot polled every couple of seconds, and FastAPI sets no `Cache-Control` by default, which leaves an intermediary — a corporate or ISP proxy — free to serve whatever it first saw for as long as it likes. On a page whose entire purpose is showing what is happening *now*, a cached response is not a stale nicety; it is a page that lies while looking healthy. `no-store` forbids storing the response at all.

**The active/idle windows are two minutes and thirty minutes** (`system.py:29-30`), and their comment records that they are a consequence of the heartbeat's retirement:

```python
# Wider than a fixed heartbeat interval would need: ordinary browsing
# produces requests far sparser than a 20s heartbeat did, so a tight
# window would show nearly everyone as gone between clicks.
ACTIVE_WITHIN_SECONDS = 2 * 60
IDLE_WITHIN_SECONDS = 30 * 60
```

This is the trade the cookie-plus-middleware design accepted in exchange for not depending on the client (document 2, §1): a heartbeat gives you tight, uniform resolution and can lie; request traffic cannot lie and gives you whatever resolution the user's browsing happens to produce. Widening the window is how you absorb the difference.

`uptime_seconds` is measured from a module-level `START_TIME = time.time()` (`system.py:24`), so it is the age of the *worker process*, not of the deployment — it resets on reload, including a dev-server autoreload.

### `GET /system/sessions` — merging two unlike tables

`system_sessions` (`system.py:91-126`) presents both session kinds in one reverse-chronological, paged list. Since the two tables share only `id`, `owner_uid`, and `started_at`, the query pads each side with typed `NULL`s and tags the rows with a literal discriminator:

```sql
SELECT * FROM (
    SELECT 'gen' AS kind, id, owner_uid, started_at, finished_at,
           stage, outcome, rule_id, error_text, model_id,
           NULL AS ip_address, NULL AS user_agent,
           NULL AS last_path, NULL AS request_count, NULL AS last_seen_at
    FROM generation_sessions
    UNION ALL
    SELECT 'http' AS kind, id, owner_uid, started_at, NULL AS finished_at,
           NULL AS stage, NULL AS outcome, NULL AS rule_id,
           NULL AS error_text, NULL AS model_id,
           ip_address, user_agent, last_path, request_count, last_seen_at
    FROM http_sessions
)
ORDER BY started_at DESC
LIMIT ? OFFSET ?
```

`UNION ALL` rather than `UNION` because the two sides cannot produce duplicate rows and there is no reason to pay for a distinct pass. `page_size` is clamped to at most 200 (`system.py:94`), the same defensive clamp the library listing uses.

**`owner_uid` never leaves the server.** The route converts it to a boolean before responding (`system.py:121-125`):

```python
        session["signed_in"] = session.pop("owner_uid") is not None
```

The comment names the convention and where it comes from: guest-vs-signed-in is what the page needs, "the raw `owner_uid` does not need to leave the server to say that — same 'derived boolean, not the identifier' convention `routes.py`'s `_rule_summary` already uses for `has_owner`." On an unauthenticated endpoint this is the difference between a debug page and an enumeration of every user id that has ever touched the app.

### The access-control boundary, stated plainly

`/system/*` is unauthenticated, and what it exposes is broader than anything else in the API: IP addresses, User-Agent strings, per-session request counts, the paths people last visited, and error text from failed generations. For a single-user local app that is the same posture as the rest of the app (§9). It is also the single most important thing in this document to re-examine before this app is ever exposed to a network with strangers on it, and the docstring, `CLAUDE.md`, and this section all say so deliberately rather than leaving it to be discovered.

Note that the `signed_in` conversion above means the page is *already* built not to leak identifiers even though nothing forces it to be. That is the right instinct and not a substitute for the access check.

---

## Summary

The API layer's shape follows directly from two hard constraints elsewhere in the spec: REQ-3.6's ban on background jobs forces `POST /rules/generate` into a synchronous-with-progress design, which forces SSE-over-POST via `StreamingResponse` plus a worker thread and a `queue.Queue` handoff (Sections 2–3); REQ-11.3's immutability guarantee forces every route but one (`PATCH /runs/{id}`) to be either purely additive or purely read-only, and even that one route is scoped to exactly two columns by construction, not convention (Section 5). Firebase auth Phase 1 was grafted onto this without touching either constraint: `get_current_user` is a `dict | None` dependency that every route already using `Depends(get_db)` could adopt without changing its no-auth behavior at all, visibility is one additional boolean-ish column plus one predicate reused everywhere through `_rule_hidden_from`, and the personal library is the existing `/rules` listing with one more `WHERE` clause behind a query flag — not a parallel API surface. The generation-context exclusion (Section 8) is the one place the auth phase reached back into an earlier subsystem (`generation/context.py`) rather than staying self-contained, and it did so by extending an existing principle (REQ-8.5) rather than inventing a new one.

Release 2.2.1's observability work (Sections 10–11) followed the same grafting discipline, with one exception worth carrying forward. It reused the existing middleware rather than adding a second one, reused `emit` as the pipeline's instrumentation seam rather than editing call sites (document 4, §10), and reused `_rule_summary`'s derived-boolean convention so an unauthenticated page never emits a user id. The exception is `try_resolve_uid` (Section 6): a function whose *entire purpose* is to do what the rest of the auth layer forbids — treat an invalid token as anonymous rather than failing. It is correct here, it is confined to one non-routing caller, and it is the one piece of this subsystem where the safety property is a convention rather than a structural guarantee. If a future release wires that function into anything that decides what a caller may see, the Firebase phase's central promise — that a bad token is never silently downgraded — is gone, and nothing in the type system will say so.
