"""The system page's API: /system/status, /system/sessions, and the
colloquial HTTP session the api/app.py middleware maintains on every
request (no client-side heartbeat involved -- see api/app.py's
track_request).
"""

import queue

import pytest
from fastapi.testclient import TestClient

import asr.api.app as app_module
from asr.api import stream as stream_module
from asr.api.app import create_app
from asr.generation.pipeline import generate_rule
from asr.storage import db


@pytest.fixture()
def client(tmp_path):
    path = tmp_path / "library.db"
    db.connect(path).close()
    with TestClient(create_app(database_path=str(path))) as running:
        yield running


def test_status_shape_on_an_empty_library(client):
    resp = client.get("/system/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["in_flight"] == []
    assert body["rules_total"] == 0
    assert body["runs_total"] == 0
    # This request's own session is touched *after* the response body is
    # already computed (see track_request), so its own first-ever hit
    # never inflates the count it just asked for.
    assert body["active_sessions"] == 0
    assert body["uptime_seconds"] >= 0
    assert body["db_size_bytes"] and body["db_size_bytes"] > 0


def test_polled_endpoints_forbid_caching(client):
    # This page is a live snapshot polled every couple of seconds -- an
    # intermediary (corporate/ISP proxy, browser heuristic caching) that
    # caches a response here would silently freeze the page for anyone
    # behind it, with no client-visible error at all.
    assert client.get("/system/status").headers["cache-control"] == "no-store"
    assert client.get("/system/sessions").headers["cache-control"] == "no-store"


def test_status_reflects_an_in_flight_generation(client, tmp_path):
    conn = db.connect(tmp_path / "library.db")
    db.insert_generation_session(conn, "abc12345", None, "claude-opus-5")
    db.update_generation_session_stage(conn, "abc12345", "stage_b_started")
    conn.close()

    body = client.get("/system/status").json()
    assert len(body["in_flight"]) == 1
    assert body["in_flight"][0]["id"] == "abc12345"
    assert body["in_flight"][0]["stage"] == "stage_b_started"


def test_finished_generation_drops_out_of_in_flight(client, tmp_path):
    conn = db.connect(tmp_path / "library.db")
    db.insert_generation_session(conn, "done0001", None, "claude-opus-5")
    db.finish_generation_session(conn, "done0001", outcome="ok", rule_id=None, error_text=None)
    conn.close()

    body = client.get("/system/status").json()
    assert body["in_flight"] == []
    assert body["generations_last_hour"] == 1


def test_a_request_mints_and_reuses_a_session_cookie(client):
    first = client.get("/rules")
    assert "asr_session" in first.cookies

    # TestClient (like a real browser) persists cookies across calls on
    # the same client instance, so this reuses the session above rather
    # than minting a new one.
    client.get("/catalog/modifiers")

    body = client.get("/system/sessions").json()
    http_rows = [s for s in body["sessions"] if s["kind"] == "http"]
    assert len(http_rows) == 1
    # This /system/sessions call is itself a third request for the same
    # session, but its own touch happens after its response body is
    # already computed -- so the count reflects only the two prior calls.
    assert http_rows[0]["request_count"] == 2
    assert http_rows[0]["last_path"] == "/catalog/modifiers"
    assert http_rows[0]["signed_in"] is False
    assert "owner_uid" not in http_rows[0]


def test_x_forwarded_for_is_preferred_over_the_raw_socket_address(client):
    # In dev, every request arrives here via Vite's proxy (vite.config.js,
    # xfwd: true), so the raw socket peer is always that proxy's own
    # loopback address, not the real visitor's -- this header is how the
    # real address gets here at all.
    client.get("/rules", headers={"X-Forwarded-For": "203.0.113.7"})
    body = client.get("/system/sessions").json()
    http_rows = [s for s in body["sessions"] if s["kind"] == "http"]
    assert http_rows[0]["ip_address"] == "203.0.113.7"


def test_ipv4_mapped_ipv6_addresses_are_unwrapped_to_plain_ipv4(client):
    # Vite's dev server listens dual-stack, so Node often reports even a
    # plain IPv4 connection this way -- same address, confusing notation.
    client.get("/rules", headers={"X-Forwarded-For": "::ffff:203.0.113.7"})
    body = client.get("/system/sessions").json()
    http_rows = [s for s in body["sessions"] if s["kind"] == "http"]
    assert http_rows[0]["ip_address"] == "203.0.113.7"


def test_a_signed_in_requests_owner_uid_is_recorded(client, monkeypatch):
    monkeypatch.setattr(app_module, "try_resolve_uid", lambda request: "user-1")
    client.get("/rules")

    body = client.get("/system/sessions").json()
    http_rows = [s for s in body["sessions"] if s["kind"] == "http"]
    assert http_rows[0]["signed_in"] is True


def test_a_later_anonymous_looking_request_never_downgrades_a_known_owner(client, monkeypatch):
    monkeypatch.setattr(app_module, "try_resolve_uid", lambda request: "user-1")
    client.get("/rules")  # identified

    monkeypatch.setattr(app_module, "try_resolve_uid", lambda request: None)
    client.get("/catalog/modifiers")  # same session cookie, no resolvable token this time

    body = client.get("/system/sessions").json()
    http_rows = [s for s in body["sessions"] if s["kind"] == "http"]
    assert http_rows[0]["signed_in"] is True


def test_an_unhandled_pipeline_crash_still_finalizes_the_session(tmp_path, monkeypatch):
    """A bug in generate_rule that isn't a GenerationFailed/RuleCrashed
    (both of which already emit their own `complete` event) must not
    leave a generation_sessions row stuck "in flight" forever -- that's
    exactly the case _run_pipeline's catch-all except clause exists for.
    The crash happens inside the real generate_rule (via a model_call
    that raises something no internal except clause catches), so the
    row genuinely gets inserted first, same as a real crash would.
    """
    path = tmp_path / "library.db"
    db.connect(path).close()

    def crashing_model(prompt, model=None):
        raise RuntimeError("the model call itself blew up")

    def wrapped(conn, emit, **kwargs):
        return generate_rule(conn, emit, model_call=crashing_model, **kwargs)

    monkeypatch.setattr(stream_module, "generate_rule", wrapped)
    events = queue.Queue()
    stream_module._run_pipeline(str(path), events, None, "public", None, None)

    conn = db.connect(path)
    session = conn.execute("SELECT * FROM generation_sessions").fetchone()
    assert session["outcome"] == "generation_failed"
    assert session["finished_at"] is not None
    conn.close()


def test_sessions_pagination_matches_the_rules_convention(tmp_path):
    path = tmp_path / "library.db"
    db.connect(path).close()
    app = create_app(database_path=str(path))
    # Three independent clients against the same app -- each gets its own
    # cookie jar, so this is three distinct browser sessions, not one
    # client reused three times.
    with TestClient(app) as c1, TestClient(app) as c2, TestClient(app) as c3:
        c1.get("/rules")
        c2.get("/rules")
        c3.get("/rules")

        page1 = c1.get("/system/sessions?page=1&page_size=2").json()
        assert page1["total"] == 3
        assert page1["page"] == 1
        assert page1["page_size"] == 2
        assert len(page1["sessions"]) == 2

        page2 = c1.get("/system/sessions?page=2&page_size=2").json()
        assert len(page2["sessions"]) == 1
