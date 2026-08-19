"""Comments (documents/new-features-v1.md): create, edit/delete own,
rate limiting. Deliberately no report/moderation queue -- see
documents/feature-run-log.md for why. Authors are shown as a
deterministic pseudonym derived from the Firebase uid, never the
login email.
"""

import json

import pytest
from fastapi.testclient import TestClient

from asr.api import comments as comments_module
from asr.api.app import create_app
from asr.api.auth import get_current_user
from asr.api.comments import _RATE_LIMIT, clean_comment, pseudonym
from asr.engine.declaration import Declaration
from asr.engine.run import run_rule
from asr.fixtures import walker
from asr.storage import db

import inspect


def _insert_walker_rule(conn, *, owner_uid=None, visibility="public"):
    declaration = Declaration.from_rule(walker.Rule)
    result = run_rule(
        walker.Rule, declaration, seed=1, width=10, height=6,
        max_ticks=20, tick_timeout_seconds=2.0,
    )
    rule_id = db.insert_rule(
        conn,
        {
            "description": "a walker", "kinds": 2, "neighbors": "plus_4", "reach": 1,
            "uses_json": json.dumps(["heading"]),
            "source_code": inspect.getsource(walker.Rule),
            "source_hash": "walker-test", "status": "ok",
            "engine_version": "test", "owner_uid": owner_uid, "visibility": visibility,
        },
    )
    db.save_run(
        conn, rule_id, result,
        start_seed=1, width=10, height=6, max_ticks=20,
        guessed_behavior="repeats", guess_confidence="high",
        engine_version="test", snapshot_every=10, is_canonical=True,
    )
    return rule_id


@pytest.fixture()
def client(tmp_path):
    path = tmp_path / "library.db"
    conn = db.connect(path)
    public_id = _insert_walker_rule(conn)
    private_id = _insert_walker_rule(conn, owner_uid="user-a", visibility="private")
    conn.close()
    comments_module._recent_comments.clear()  # tests share this process-level dict
    with TestClient(create_app(database_path=str(path))) as running:
        running.public_id, running.private_id = public_id, private_id
        yield running
        running.app.dependency_overrides.pop(get_current_user, None)


def as_user(client, uid):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": uid, "email": f"{uid}@example.com"}


def anonymous(client):
    client.app.dependency_overrides.pop(get_current_user, None)


def test_pseudonym_is_stable_and_never_the_email():
    name = pseudonym("some-uid")
    assert name == pseudonym("some-uid")
    assert "@" not in name
    assert "some-uid" not in name


def test_clean_comment_keeps_newlines_but_strips_control_chars():
    assert clean_comment("line one\nline two") == "line one\nline two"
    assert clean_comment("bad\x00char") == "badchar"


def test_clean_comment_collapses_long_blank_runs():
    assert clean_comment("a\n\n\n\n\nb") == "a\n\nb"


def test_anonymous_cannot_comment(client):
    anonymous(client)
    resp = client.post(f"/rules/{client.public_id}/comments", json={"body": "hi"})
    assert resp.status_code == 401


def test_create_list_edit_delete_own_comment(client):
    as_user(client, "user-a")
    created = client.post(f"/rules/{client.public_id}/comments", json={"body": "neat rule"}).json()
    assert created["body"] == "neat rule"
    assert created["mine"] is True
    assert "@" not in created["author"]

    listed = client.get(f"/rules/{client.public_id}/comments").json()["comments"]
    assert len(listed) == 1
    assert listed[0]["author"] == created["author"]

    # A different signed-in user sees the same author label, and it's
    # not their own.
    as_user(client, "user-b")
    listed_as_b = client.get(f"/rules/{client.public_id}/comments").json()["comments"]
    assert listed_as_b[0]["mine"] is False

    as_user(client, "user-a")
    edited = client.patch(f"/comments/{created['id']}", json={"body": "actually, neat rule!"})
    assert edited.status_code == 200
    assert edited.json()["edited_at"] is not None

    assert client.delete(f"/comments/{created['id']}").status_code == 200
    assert client.get(f"/rules/{client.public_id}/comments").json()["comments"] == []


def test_only_the_author_can_edit_or_delete(client):
    as_user(client, "user-a")
    created = client.post(f"/rules/{client.public_id}/comments", json={"body": "mine"}).json()

    as_user(client, "user-b")
    assert client.patch(f"/comments/{created['id']}", json={"body": "hijack"}).status_code == 403
    assert client.delete(f"/comments/{created['id']}").status_code == 403


def test_comments_respect_rule_visibility(client):
    anonymous(client)
    assert client.get(f"/rules/{client.private_id}/comments").status_code == 404
    as_user(client, "user-b")
    assert client.post(f"/rules/{client.private_id}/comments", json={"body": "x"}).status_code == 404
    as_user(client, "user-a")  # the owner
    assert client.post(f"/rules/{client.private_id}/comments", json={"body": "x"}).status_code == 200


def test_rate_limit(client):
    as_user(client, "user-a")
    for _ in range(_RATE_LIMIT):
        resp = client.post(f"/rules/{client.public_id}/comments", json={"body": "spam"})
        assert resp.status_code == 200
    over_limit = client.post(f"/rules/{client.public_id}/comments", json={"body": "one more"})
    assert over_limit.status_code == 429


def test_empty_and_oversized_comments_rejected(client):
    as_user(client, "user-a")
    assert client.post(f"/rules/{client.public_id}/comments", json={"body": "   "}).status_code == 400
    assert client.post(f"/rules/{client.public_id}/comments", json={"body": "x" * 1001}).status_code == 422
