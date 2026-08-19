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
"""


def connect(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
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
