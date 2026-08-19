"""POST /rules/generate's request handling (Firebase auth Phase 1):
owner/visibility are resolved before the worker thread is spawned,
since the thread has no Request object to derive identity from later.
_run_pipeline is faked here so these tests exercise only the route's
own logic (parsing, the 400 case, defaulting) without running the real
generation pipeline or touching Anthropic.
"""

import queue

import pytest
from fastapi.testclient import TestClient

from asr.api import stream as stream_module
from asr.api.app import create_app
from asr.api.auth import get_current_user
from asr.storage import db


@pytest.fixture()
def client(tmp_path):
    path = tmp_path / "library.db"
    db.connect(path).close()
    with TestClient(create_app(database_path=str(path))) as running:
        yield running
        running.app.dependency_overrides.pop(get_current_user, None)


def _capture_run_pipeline(monkeypatch):
    calls = []

    def fake(database_path, events, owner_uid, visibility, spark, title):
        calls.append({"owner_uid": owner_uid, "visibility": visibility, "spark": spark, "title": title})
        events.put(None)

    monkeypatch.setattr(stream_module, "_run_pipeline", fake)
    return calls


def test_anonymous_generate_is_public_with_no_owner(client, monkeypatch):
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate")  # exactly what the frontend sends today: no body
    assert resp.status_code == 200
    assert calls == [{"owner_uid": None, "visibility": "public", "spark": None, "title": None}]


def test_anonymous_cannot_request_private(client, monkeypatch):
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"visibility": "private"})
    assert resp.status_code == 400
    assert calls == []  # rejected before the pipeline ever starts


def test_signed_in_defaults_to_public(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate")
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "public", "spark": None, "title": None}]


def test_signed_in_can_request_private(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"visibility": "private"})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "private", "spark": None, "title": None}]


def test_signed_in_can_still_explicitly_choose_public(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"visibility": "public"})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "public", "spark": None, "title": None}]


def test_anonymous_cannot_add_a_spark(client, monkeypatch):
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"spark": "wraps like a snake"})
    assert resp.status_code == 400
    assert calls == []


def test_signed_in_spark_is_cleaned_and_threaded_through(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"spark": "  wraps\nlike a snake  "})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "public", "spark": "wraps like a snake", "title": None}]


def test_signed_in_overlong_spark_is_rejected(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"spark": "x" * 65})
    assert resp.status_code == 400
    assert calls == []


def test_spark_over_the_coarse_pydantic_limit_is_rejected(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"spark": "x" * 300})
    assert resp.status_code == 422  # pydantic's own Field(max_length=256), before clean_spark runs
    assert calls == []


def test_run_pipeline_applies_the_title_after_a_successful_generation(monkeypatch, tmp_path):
    # _run_pipeline itself, not the route -- the route-level fake above
    # replaces _run_pipeline entirely, so it can't exercise the actual
    # glue between generate_rule's payload and _apply_title.
    path = tmp_path / "library.db"
    db.connect(path).close()

    applied = []
    monkeypatch.setattr(
        stream_module, "generate_rule",
        lambda conn, emit, **kw: {"status": "ok", "rule_id": 42},
    )
    monkeypatch.setattr(
        stream_module, "_apply_title",
        lambda conn, rule_id, title: applied.append((rule_id, title)),
    )
    events = queue.Queue()
    stream_module._run_pipeline(str(path), events, None, "public", None, "A Given Name")
    assert applied == [(42, "A Given Name")]


def test_run_pipeline_skips_title_when_generation_failed(monkeypatch, tmp_path):
    path = tmp_path / "library.db"
    db.connect(path).close()

    applied = []
    monkeypatch.setattr(
        stream_module, "generate_rule",
        lambda conn, emit, **kw: {"status": "generation_failed"},  # no rule_id at all
    )
    monkeypatch.setattr(
        stream_module, "_apply_title",
        lambda conn, rule_id, title: applied.append((rule_id, title)),
    )
    events = queue.Queue()
    stream_module._run_pipeline(str(path), events, None, "public", None, "Should Not Land")
    assert applied == []


def test_title_at_creation_needs_no_sign_in(client, monkeypatch):
    # An anonymous request can only ever produce an ownerless rule, and
    # ownerless rules are already titlable by anyone -- no auth gate
    # here, unlike spark/private.
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"title": "My First Rule"})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": None, "visibility": "public", "spark": None, "title": "My First Rule"}]
