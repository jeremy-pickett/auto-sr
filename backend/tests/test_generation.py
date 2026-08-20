"""The generation pipeline against a fake model — no network, real
validation, real child-process runs, real storage (REQ-15.1 keeps
generated rules out of harness tests; these test the pipeline itself
with hand-written stand-ins).
"""

import json
import random

import pytest

from asr.generation import context
from asr.generation.catalog import pick_modifiers_in_scope
from asr.generation.pipeline import generate_rule
from asr.generation.templates import prompt_set_hash
from asr.storage import db

STAGE_A_JSON = json.dumps({
    "mode": "new",
    "description": "A cell catches fire if any neighbor burns; fire never goes out.",
    "reasoning": "Nothing count_based has been tried at these settings.",
    "kinds": 2,
    "neighbors": "all_8",
    "reach": 1,
    "uses": [],
    "reads": [],
    "modifiers": [],
    "semantic_slots": {},
    "assign": {},
    "suggested_display": {"color": "kind", "brightness": "age"},
    "shape": "count_based",
    "concepts": ["spreads", "counts"],
})

GOOD_SOURCE = '''class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "age"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(self.dice.chance(0.1).astype(np.uint8))

    def step(self, cells):
        burning = count_neighbors(cells, "kind", 1)
        lit = (cells.kind == 1) | (burning >= 1)
        return make_cells(lit.astype(np.uint8))
'''

BROKEN_SOURCE = '''class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    USES = []
    READS = []
    MODIFIERS = []
    SEMANTIC_SLOTS = {}
    ASSIGN = {}
    SUGGESTED_DISPLAY = {"color": "kind", "brightness": "age"}

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(self.dice.chance(0.1).astype(np.uint8))

    def step(self, cells):
        while True:
            pass
'''


def fake_model(stage_b_source, repair_source=None):
    """A canned generator: Stage A JSON, then implementations."""

    def call(prompt, model=None):
        if "inventing a cellular automaton rule" in prompt:
            return STAGE_A_JSON
        if "YOUR PREVIOUS ATTEMPT" in prompt:
            return repair_source if repair_source is not None else stage_b_source
        if "Implement this rule" in prompt:
            return stage_b_source
        return "count_based"  # the shape question

    return call


@pytest.fixture
def conn():
    connection = db.connect(":memory:")
    yield connection
    connection.close()


def collect_events():
    events = []
    return events, lambda name, data: events.append((name, data))


def test_a_good_generation_lands_ok_with_a_canonical_run(conn):
    events, emit = collect_events()
    payload = generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    assert payload["status"] == "ok"
    names = [name for name, _ in events]
    for wanted in ("stage_a_started", "stage_a_complete", "stage_b_started",
                   "stage_b_complete", "validating", "running", "complete"):
        assert wanted in names, wanted
    assert "validation_failed" not in names

    rule = conn.execute("SELECT * FROM rules").fetchone()
    assert rule["status"] == "ok"
    assert rule["stage_a_rendered"] and rule["stage_b_rendered"]
    assert rule["stage_a_raw"] == STAGE_A_JSON
    assert rule["prompt_set_hash"] == prompt_set_hash()
    assert rule["observed_shape"] == "threshold"  # tallies plus a cutoff
    run = conn.execute("SELECT * FROM runs").fetchone()
    assert run["is_canonical"] == 1
    ticks = conn.execute("SELECT COUNT(*) AS n FROM ticks").fetchone()["n"]
    assert ticks == run["ticks_run"] + 1

    session = conn.execute("SELECT * FROM generation_sessions").fetchone()
    assert session["outcome"] == "ok"
    assert session["stage"] == "complete"
    assert session["rule_id"] == rule["id"]
    assert session["finished_at"] is not None


def test_a_failed_repair_lands_broken_and_in_rejections(conn):
    events, emit = collect_events()
    payload = generate_rule(
        conn, emit, model_call=fake_model(BROKEN_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    assert payload["status"] == "broken"
    assert payload["failed_check"] == "static"
    names = [name for name, _ in events]
    assert names.count("validation_failed") >= 2
    assert "repairing" in names

    rule = conn.execute("SELECT * FROM rules").fetchone()
    assert rule["status"] == "broken"
    assert rule["repair_rendered"] is not None  # the repair prompt is stored
    rejection = conn.execute("SELECT * FROM rejections").fetchone()
    assert rejection["rule_id"] == rule["id"]
    assert rejection["failed_check"] == "static"
    assert rejection["stage_a_description"]  # the description survives (REQ-7.11)

    session = conn.execute("SELECT * FROM generation_sessions").fetchone()
    assert session["outcome"] == "broken"
    assert session["rule_id"] == rule["id"]


def test_a_successful_repair_recovers_the_rule(conn):
    events, emit = collect_events()
    payload = generate_rule(
        conn, emit,
        model_call=fake_model(BROKEN_SOURCE, repair_source=GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    assert payload["status"] == "ok"
    names = [name for name, _ in events]
    assert "repairing" in names
    rule = conn.execute("SELECT * FROM rules").fetchone()
    assert rule["status"] == "ok"
    assert rule["repair_raw"] == GOOD_SOURCE


def test_unparseable_stage_a_is_a_generation_failure_not_a_rule(conn):
    events, emit = collect_events()

    payload = generate_rule(
        conn, emit, model_call=lambda prompt, model=None: "I would rather write a poem.",
        width=24, height=24, max_ticks=40,
    )
    assert payload["status"] == "generation_failed"
    assert conn.execute("SELECT COUNT(*) AS n FROM rules").fetchone()["n"] == 0
    rejection = conn.execute("SELECT * FROM rejections").fetchone()
    assert rejection["failed_check"] == "stage_a_unparseable"
    assert rejection["rule_id"] is None

    session = conn.execute("SELECT * FROM generation_sessions").fetchone()
    assert session["outcome"] == "generation_failed"
    assert session["rule_id"] is None


def test_coverage_counts_the_canonical_run_only(conn):
    # One rule, one vote (REQ-8.6): rerunning a rule twenty times must
    # not reweight the distribution Stage A reasons over.
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    before = context.coverage_map(conn)
    (cell,) = before.values()
    assert cell == {
        "attempts": 1, "successes": 1, "rejections": 0,
        "outcomes": dict(cell["outcomes"]),
    }

    rule_id = conn.execute("SELECT id FROM rules").fetchone()["id"]
    for extra_seed in (5, 6, 7):
        conn.execute(
            """INSERT INTO runs(rule_id, created_at, start_seed, width, height,
                   max_ticks, ticks_run, is_canonical, stopped_because,
                   guessed_behavior, guess_confidence, engine_version)
               VALUES(?,?,?,?,?,?,?,0,'ran_out','noisy','high','test')""",
            (rule_id, db.now(), extra_seed, 24, 24, 40, 40),
        )
    conn.commit()

    after = context.coverage_map(conn)
    assert after == before  # the reruns changed nothing


def test_stage_a_context_stays_in_budget_and_names_examples(conn):
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    text, shown = context.library_summary_for_stage_a(conn)
    assert shown  # the generated rule appears as an example
    assert "COVERAGE MAP" in text
    # REQ-8.3: 2,000-3,000 tokens; ~4 characters per token leaves a
    # generous ceiling this small library must sit far under.
    assert len(text) < 12000


def test_owner_and_visibility_land_on_the_stored_rule(conn):
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
        owner_uid="user-x", visibility="private",
    )
    rule = conn.execute("SELECT * FROM rules").fetchone()
    assert rule["owner_uid"] == "user-x"
    assert rule["visibility"] == "private"


def test_default_generation_is_still_anonymous_and_public(conn):
    # No owner_uid/visibility passed at all -- every pre-existing
    # caller of generate_rule must keep producing today's exact
    # anonymous/global result.
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    rule = conn.execute("SELECT * FROM rules").fetchone()
    assert rule["owner_uid"] is None
    assert rule["visibility"] == "public"


def test_spark_lands_in_the_prompt_and_the_stored_row(conn):
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
        spark="wraps like a snake",
    )
    rule = conn.execute("SELECT spark, stage_a_rendered FROM rules").fetchone()
    assert rule["spark"] == "wraps like a snake"
    assert '"wraps like a snake"' in rule["stage_a_rendered"]
    assert "cannot change the JSON schema" in rule["stage_a_rendered"]


def test_no_spark_leaves_no_literal_placeholder_in_the_prompt(conn):
    # render() only substitutes keys it's given -- forgetting to pass
    # spark_hint at all would leave the literal "{spark_hint}" text
    # sitting in the prompt. This is the regression that check guards.
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    rule = conn.execute("SELECT stage_a_rendered FROM rules").fetchone()
    assert "{spark_hint}" not in rule["stage_a_rendered"]
    assert "HINT FROM THE PERSON" not in rule["stage_a_rendered"]


def test_private_rules_never_reach_stage_a_context(conn):
    # Firebase auth Phase 1: a private rule must not just be excluded
    # from what's displayed, but from what gets rendered into the
    # prompt at all -- the strongest form of the exclusion guarantee.
    _, emit = collect_events()
    generate_rule(
        conn, emit, model_call=fake_model(GOOD_SOURCE),
        width=24, height=24, max_ticks=40,
    )
    marker = "ZZ-PRIVATE-MARKER-do-not-leak-into-stage-a-ZZ"
    conn.execute(
        """UPDATE rules SET description = ? WHERE id = (
               SELECT id FROM rules ORDER BY id DESC LIMIT 1
           )""",
        (marker,),
    )
    conn.commit()
    private_id = conn.execute("SELECT id FROM rules ORDER BY id DESC LIMIT 1").fetchone()["id"]
    conn.execute("UPDATE rules SET visibility = 'private' WHERE id = ?", (private_id,))
    conn.commit()

    text, shown_ids = context.library_summary_for_stage_a(conn)
    assert marker not in text
    assert private_id not in shown_ids

    coverage = context.coverage_map(conn)
    assert sum(cell["attempts"] for cell in coverage.values()) == 0

    totals = context.totals(conn)
    assert totals["rules"] == 0


def test_at_most_one_modifier_is_ever_in_scope():
    for seed in range(50):
        in_scope = pick_modifiers_in_scope(random.Random(seed))
        assert len(in_scope) <= 1
