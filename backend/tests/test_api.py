"""The HTTP API (spec section 11) against a small seeded library."""

import json
import struct

import numpy as np
import pytest
from fastapi.testclient import TestClient

from asr.api.app import create_app
from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import walker
from asr.seed import seed_catalog
from asr.storage import db

import inspect


@pytest.fixture()
def client(tmp_path):
    path = tmp_path / "library.db"
    conn = db.connect(path)
    seed_catalog(conn)
    declaration = Declaration.from_rule(walker.Rule)
    result = run_rule(
        walker.Rule, declaration, seed=1, width=10, height=6,
        max_ticks=50, tick_timeout_seconds=2.0,
    )
    rule_id = db.insert_rule(
        conn,
        {
            "description": "a walker",
            "kinds": 2,
            "neighbors": "plus_4",
            "reach": 1,
            "uses_json": json.dumps(["heading"]),
            "source_code": inspect.getsource(walker.Rule),
            "source_hash": "walker-test",
            "status": "ok",
            "engine_version": "test",
            "requested_shape": "walker",
            "concepts_json": json.dumps(["moves"]),
        },
    )
    db.save_run(
        conn, rule_id, result,
        start_seed=1, width=10, height=6, max_ticks=50,
        guessed_behavior="repeats", guess_confidence="high",
        engine_version="test", snapshot_every=10, is_canonical=True,
    )
    conn.close()
    with TestClient(create_app(database_path=str(path))) as running:
        running.walker_result = result
        yield running


def test_rules_list_carries_the_canonical_run(client):
    body = client.get("/rules").json()
    assert body["total"] == 1
    rule = body["rules"][0]
    assert rule["description"] == "a walker"
    assert rule["canonical_run"]["guessed_behavior"] == "repeats"
    assert client.get("/rules?concept=moves").json()["total"] == 1
    assert client.get("/rules?concept=decays").json()["total"] == 0


def test_rule_detail_includes_source_and_runs(client):
    rule = client.get("/rules/1").json()
    assert "class Rule" in rule["source_code"]
    assert rule["runs"][0]["stopped_because"] == "looping"
    assert rule["provenance"]["engine_version"] == "test"


def test_run_detail_carries_the_numbers_panel(client):
    run = client.get("/runs/1").json()
    assert run["loop_length"] == 10
    numbers = run["numbers"]
    assert len(numbers["variety"]) == run["ticks_run"] + 1
    assert numbers["cells_changed"][0] == 0
    assert numbers["cells_changed"][1] == 2  # the walker leaves and arrives


def test_grids_arrive_in_the_specified_binary_frame(client):
    raw = client.get("/runs/1/grids?from=0&to=5&props=kind,age").content
    (head_length,) = struct.unpack_from("<I", raw, 0)
    header = json.loads(raw[4 : 4 + head_length])
    assert header["ticks"] == [0, 5]
    assert header["shape"] == [6, 10]
    names = [p["name"] for p in header["properties"]]
    assert names == ["age", "kind"]  # name-sorted
    payload = raw[4 + head_length :]
    for prop in header["properties"]:
        block = payload[prop["offset"] : prop["offset"] + prop["length"]]
        stack = np.frombuffer(block, prop["dtype"]).reshape(6, 6, 10)
        live = client.walker_result.ticks
        for tick in range(6):
            assert np.array_equal(stack[tick], live[tick].arrays[prop["name"]])


def test_grids_reject_oversized_and_unknown_requests(client):
    assert client.get("/runs/1/grids?from=9&to=3").status_code == 400
    assert client.get("/runs/1/grids?props=voltage").status_code == 400
    assert client.get("/runs/999/grids").status_code == 404


def test_export_returns_the_whole_run_as_plain_json(client):
    body = client.get("/runs/1/export?props=kind,age").json()
    assert body["run_id"] == 1
    assert body["shape"] == [6, 10]
    assert body["ticks"][0] == 0
    live = client.walker_result.ticks
    assert body["ticks"][1] == len(live) - 1  # no 250-tick cap here
    kind_stack = body["properties"]["kind"]
    assert len(kind_stack) == len(live)  # every tick, not just a chunk
    for tick in range(len(live)):
        assert kind_stack[tick] == live[tick].arrays["kind"].tolist()


def test_preview_png_is_a_real_image_at_the_final_tick(client):
    resp = client.get("/rules/1/preview.png")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert resp.content[:8] == b"\x89PNG\r\n\x1a\n"  # the PNG file signature
    assert client.get("/rules/999/preview.png").status_code == 404


def test_export_respects_visibility_and_range(client):
    assert client.get("/runs/999/export").status_code == 404
    assert client.get("/runs/1/export?from=9&to=3").status_code == 400
    partial = client.get("/runs/1/export?from=0&to=2").json()
    assert partial["ticks"] == [0, 2]
    assert len(partial["properties"]["kind"]) == 3


def test_cell_history_reads_one_position_across_the_run(client):
    body = client.get("/runs/1/cell/3/0?props=kind").json()
    kinds = body["history"]["kind"]
    live = client.walker_result.ticks
    assert kinds == [int(t.arrays["kind"][3, 0]) for t in live]
    assert client.get("/runs/1/cell/99/0").status_code == 400


def test_patch_sets_only_the_two_user_columns(client):
    updated = client.patch(
        "/runs/1", json={"user_behavior": "structured", "user_flagged": True}
    ).json()
    assert updated["user_behavior"] == "structured"
    assert updated["user_flagged"] is True
    assert updated["guessed_behavior"] == "repeats"  # the guess survives
    assert client.patch("/runs/1", json={"user_behavior": "amazing"}).status_code == 400
    cleared = client.patch("/runs/1", json={"user_behavior": None}).json()
    assert cleared["user_behavior"] is None
    assert cleared["user_flagged"] is True  # untouched when absent


def test_flag_filter_finds_the_flagged_rule(client):
    client.patch("/runs/1", json={"user_flagged": True})
    assert client.get("/rules?flagged=true").json()["total"] == 1


def test_rss_feed_lists_public_rules(client):
    resp = client.get("/library/feed.rss")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/rss+xml")
    body = resp.text
    assert "<rss version=\"2.0\">" in body
    assert "<item>" in body
    assert "a walker" in body  # the seeded rule's description, escaped into the item


def test_modifier_catalog_is_served(client):
    names = {m["name"] for m in client.get("/catalog/modifiers").json()["modifiers"]}
    assert names == {"weight", "stubbornness", "rate"}


def test_library_summary_counts_canonical_runs_once(client):
    summary = client.get("/library/summary").json()
    assert summary["totals"]["rules"] == 1
    assert summary["totals"]["behaviors"] == {"repeats": 1}
    (cell,) = summary["coverage"].values()
    assert cell == {
        "attempts": 1, "successes": 1, "rejections": 0,
        "outcomes": {"repeats": 1},
    }


def test_rerun_is_never_canonical_and_stays_out_of_coverage(client):
    fresh = client.post("/rules/1/runs", json={"seed": 77}).json()
    assert fresh["is_canonical"] is False
    assert fresh["stopped_because"] == "looping"
    assert fresh["loop_length"] == 10
    # REQ-8.6: the extra run must not reweight the coverage map.
    summary = client.get("/library/summary").json()
    (cell,) = summary["coverage"].values()
    assert cell["successes"] == 1
