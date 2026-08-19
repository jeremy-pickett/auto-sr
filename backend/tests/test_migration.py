"""Schema migration for owner_uid/visibility (Firebase auth Phase 1).

CREATE TABLE IF NOT EXISTS is a no-op on a table that already exists,
so the columns only reach a live database through db._ensure_columns's
idempotent ALTER TABLE step — these tests exist to prove that step
actually works, both on a brand-new database and on one built before
this feature existed.
"""

import sqlite3

from asr.storage import db

# A literal snapshot of the rules/runs schema as it existed before
# owner_uid/visibility — copied, not imported from db.py, so this test
# keeps proving the migration path even if db.py's SCHEMA changes
# later and would otherwise silently "self-heal" the old-schema case.
PRE_MIGRATION_SCHEMA = """
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
    status TEXT NOT NULL,
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
"""


def test_fresh_database_has_the_new_columns(tmp_path):
    conn = db.connect(tmp_path / "fresh.db")
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(rules)")}
    assert "owner_uid" in columns
    assert "visibility" in columns

    rule_id = db.insert_rule(
        conn,
        {
            "description": "test", "kinds": 2, "neighbors": "all_8", "reach": 1,
            "source_code": "x", "source_hash": "x", "status": "ok",
            "engine_version": "test",
        },
    )
    row = conn.execute("SELECT * FROM rules WHERE id=?", (rule_id,)).fetchone()
    assert row["visibility"] == "public"
    assert row["owner_uid"] is None
    conn.close()


def test_pre_migration_database_is_upgraded_safely(tmp_path):
    path = tmp_path / "old.db"

    # Build a database the old way, with no owner_uid/visibility.
    old_conn = sqlite3.connect(path)
    old_conn.row_factory = sqlite3.Row
    old_conn.executescript(PRE_MIGRATION_SCHEMA)
    old_conn.execute(
        """INSERT INTO rules(id, created_at, description, kinds, neighbors, reach,
               source_code, source_hash, status, engine_version)
           VALUES(1, '2026-01-01T00:00:00', 'pre-existing rule', 2, 'all_8', 1,
               'x', 'x', 'ok', 'test')"""
    )
    old_conn.commit()
    old_conn.close()

    # Now open it through the real connect() — the migration path.
    conn = db.connect(path)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(rules)")}
    assert "owner_uid" in columns
    assert "visibility" in columns

    row = conn.execute("SELECT * FROM rules WHERE id=1").fetchone()
    assert row["description"] == "pre-existing rule"  # untouched
    assert row["visibility"] == "public"  # backfilled default
    assert row["owner_uid"] is None
    conn.close()


def test_ensure_columns_is_idempotent(tmp_path):
    path = tmp_path / "reopened.db"
    db.connect(path).close()
    db.connect(path).close()  # second open must not raise (duplicate column etc.)
    conn = db.connect(path)
    columns = [row["name"] for row in conn.execute("PRAGMA table_info(rules)")]
    assert columns.count("owner_uid") == 1
    assert columns.count("visibility") == 1
    conn.close()
