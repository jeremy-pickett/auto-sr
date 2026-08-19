"""POST /rules/generate's request handling (Firebase auth Phase 1):
owner/visibility are resolved before the worker thread is spawned,
since the thread has no Request object to derive identity from later.
_run_pipeline is faked here so these tests exercise only the route's
own logic (parsing, the 400 case, defaulting) without running the real
generation pipeline or touching Anthropic.
"""

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

    def fake(database_path, events, owner_uid, visibility):
        calls.append({"owner_uid": owner_uid, "visibility": visibility})
        events.put(None)

    monkeypatch.setattr(stream_module, "_run_pipeline", fake)
    return calls


def test_anonymous_generate_is_public_with_no_owner(client, monkeypatch):
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate")  # exactly what the frontend sends today: no body
    assert resp.status_code == 200
    assert calls == [{"owner_uid": None, "visibility": "public"}]


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
    assert calls == [{"owner_uid": "user-a", "visibility": "public"}]


def test_signed_in_can_request_private(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"visibility": "private"})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "private"}]


def test_signed_in_can_still_explicitly_choose_public(client, monkeypatch):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": "user-a", "email": None}
    calls = _capture_run_pipeline(monkeypatch)
    resp = client.post("/rules/generate", json={"visibility": "public"})
    assert resp.status_code == 200
    assert calls == [{"owner_uid": "user-a", "visibility": "public"}]
