"""The library database (spec section 12): SQLite, single file, WAL.

Recorded history is immutable — nothing here updates a tick row, and
the only run columns ever updated are the user's behavior override and
flag (REQ-11.3, applied at the API layer).
"""

import json
import sqlite3
from datetime import datetime, timezone

from asr.engine.run import RunResult
from asr.storage import encoding

SCHEMA = """
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

CREATE TABLE IF NOT EXISTS modifier_catalog(
    name TEXT PRIMARY KEY,
    type_spec TEXT NOT NULL,
    default_value TEXT NOT NULL,
    applied_by TEXT NOT NULL,
    effect TEXT NOT NULL,
    assign_when TEXT NOT NULL,
    availability TEXT NOT NULL,
    blurb TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rejections(
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    rule_id INTEGER REFERENCES rules(id),
    failed_check TEXT NOT NULL,
    stage_a_description TEXT,
    concepts_json TEXT NOT NULL DEFAULT '[]',
    requested_shape TEXT,
    kinds INTEGER,
    neighbors TEXT,
    reach INTEGER,
    modifier_in_scope TEXT
);

CREATE INDEX IF NOT EXISTS rules_by_status_shape ON rules(status, requested_shape);
CREATE INDEX IF NOT EXISTS runs_by_rule_canonical ON runs(rule_id, is_canonical);

-- A brand-new table, never existed before -- CREATE TABLE IF NOT
-- EXISTS is exactly the right idempotent mechanism here, unlike a
-- column added to a table that already exists (see _ensure_columns).
CREATE TABLE IF NOT EXISTS favorites(
    user_uid TEXT NOT NULL,
    rule_id INTEGER NOT NULL REFERENCES rules(id),
    created_at TEXT NOT NULL,
    PRIMARY KEY (user_uid, rule_id)
);

CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY,
    rule_id INTEGER NOT NULL REFERENCES rules(id),
    user_uid TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL,
    edited_at TEXT
);
CREATE INDEX IF NOT EXISTS comments_by_rule ON comments(rule_id);

-- One optional, self-chosen field per signed-in user: a display name
-- that overrides their comment pseudonym everywhere it's shown. Never
-- holds an email or anything else Firebase knows about the person --
-- see asr/api/profile.py for why.
CREATE TABLE IF NOT EXISTS user_profiles(
    uid TEXT PRIMARY KEY,
    display_name TEXT
);

-- The system page's two kinds of session. generation_sessions turns the
-- gen_id that already existed purely for log correlation (pipeline.py)
-- into a persisted, queryable record of one POST /rules/generate call.
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

-- Presence, first attempt: one row per browser tab, updated by a client
-- heartbeat. Retired in favor of http_sessions below (a real HTTP session
-- needs no client cooperation at all -- the request traffic that already
-- happens is enough). Left in the schema, unused, rather than dropped.
CREATE TABLE IF NOT EXISTS app_sessions(
    id TEXT PRIMARY KEY,
    owner_uid TEXT,
    started_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    current_view TEXT,
    status TEXT NOT NULL DEFAULT 'active'
);
CREATE INDEX IF NOT EXISTS app_sessions_by_last_seen ON app_sessions(last_seen_at);

-- The colloquial HTTP session: one row per session cookie, updated by the
-- session middleware (api/app.py) on every request -- no client
-- cooperation required, so no client bug can leave it stale or wrong.
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
CREATE INDEX IF NOT EXISTS http_sessions_by_last_seen ON http_sessions(last_seen_at);
"""


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

    app_session_columns = {row["name"] for row in conn.execute("PRAGMA table_info(app_sessions)")}
    if "status" not in app_session_columns:
        conn.execute("ALTER TABLE app_sessions ADD COLUMN status TEXT NOT NULL DEFAULT 'active'")

    conn.commit()


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


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def insert_rule(conn, values: dict) -> int:
    """Insert a rule row from a partial dict; everything the caller
    does not supply falls to the schema default or NULL.
    """
    values = dict(values)
    values.setdefault("created_at", now())
    columns = ", ".join(values)
    slots = ", ".join("?" for _ in values)
    cursor = conn.execute(
        f"INSERT INTO rules({columns}) VALUES({slots})", list(values.values())
    )
    conn.commit()
    return cursor.lastrowid


def save_run(
    conn,
    rule_id: int,
    result: RunResult,
    *,
    start_seed: int,
    width: int,
    height: int,
    max_ticks: int,
    guessed_behavior: str,
    guess_confidence: str,
    engine_version: str,
    snapshot_every: int,
    is_canonical: bool,
) -> int:
    """Store a finished run and every tick payload, in one transaction.

    A rule's first run is canonical; only canonical runs count toward
    the coverage map (REQ-8.6) — the caller decides.
    """
    cursor = conn.execute(
        """INSERT INTO runs(rule_id, created_at, start_seed, width, height,
               max_ticks, ticks_run, is_canonical, stopped_because, loop_length,
               pattern_settled_at, guessed_behavior, guess_confidence,
               engine_version)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            rule_id, now(), start_seed, width, height,
            max_ticks, result.ticks_run, int(is_canonical),
            result.stopped_because, result.loop_length,
            result.pattern_settled_at, guessed_behavior, guess_confidence,
            engine_version,
        ),
    )
    run_id = cursor.lastrowid

    rows = []
    previous_arrays = None
    for record in result.ticks:
        if record.tick % snapshot_every == 0:
            payload_encoding = "snapshot"
            blob = encoding.encode_snapshot(record.arrays)
        else:
            payload_encoding, blob = encoding.encode_delta(previous_arrays, record.arrays)
        previous_arrays = record.arrays
        rows.append(
            (
                run_id, record.tick, payload_encoding, blob,
                record.variety, record.cells_changed, record.kind_quiet_for,
                json.dumps(record.kind_counts),
                record.state_fingerprint, record.pattern_fingerprint,
            )
        )
    conn.executemany(
        """INSERT INTO ticks(run_id, tick, payload_encoding, payload_blob,
               variety, cells_changed, kind_quiet_for, kind_counts_json,
               state_fingerprint, pattern_fingerprint)
           VALUES(?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )
    conn.commit()
    return run_id


def insert_generation_session(conn, gen_id: str, owner_uid: str | None, model_id: str | None) -> None:
    conn.execute(
        """INSERT INTO generation_sessions(id, owner_uid, started_at, stage, model_id)
           VALUES(?,?,?,?,?)""",
        (gen_id, owner_uid, now(), "stage_a_started", model_id),
    )
    conn.commit()


def update_generation_session_stage(conn, gen_id: str, stage: str) -> None:
    conn.execute("UPDATE generation_sessions SET stage=? WHERE id=?", (stage, gen_id))
    conn.commit()


def finish_generation_session(
    conn, gen_id: str, *, outcome: str, rule_id: int | None, error_text: str | None
) -> None:
    # finished_at IS NULL guards against a second finalize on the same
    # session -- stream.py's catch-all exception handler calls this as a
    # safety net for failures generate_rule() didn't already turn into a
    # `complete` event, and must never clobber a row that already has a
    # real outcome (e.g. a failure while applying the title, after a
    # perfectly good generation already finished).
    conn.execute(
        """UPDATE generation_sessions
           SET finished_at=?, stage='complete', outcome=?, rule_id=?, error_text=?
           WHERE id=? AND finished_at IS NULL""",
        (now(), outcome, rule_id, error_text, gen_id),
    )
    conn.commit()


def touch_http_session(
    conn,
    session_id: str,
    owner_uid: str | None,
    ip_address: str | None,
    user_agent: str | None,
    path: str,
) -> None:
    """Called once per request by the session middleware (api/app.py) --
    the entire mechanism, no client cooperation involved. A request that
    happens to carry no/an unresolvable auth token must never downgrade a
    session that a previous request already identified, hence COALESCE
    rather than a flat overwrite on owner_uid.
    """
    conn.execute(
        """INSERT INTO http_sessions(
               id, owner_uid, ip_address, user_agent, started_at, last_seen_at,
               last_path, request_count
           ) VALUES(?,?,?,?,?,?,?,1)
           ON CONFLICT(id) DO UPDATE SET
               owner_uid=COALESCE(excluded.owner_uid, http_sessions.owner_uid),
               ip_address=excluded.ip_address,
               user_agent=excluded.user_agent,
               last_seen_at=excluded.last_seen_at,
               last_path=excluded.last_path,
               request_count=http_sessions.request_count + 1""",
        (session_id, owner_uid, ip_address, user_agent, now(), now(), path),
    )
    conn.commit()
