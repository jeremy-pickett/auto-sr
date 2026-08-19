"""Rule naming (title/slug) and favorites (documents/new-features-v1.md).

Title/slug: an overlay over the AI-generated description, the same
relationship user_behavior already has to guessed_behavior -- the
description itself never changes. Ownerless (anonymous-generated)
rules can be titled by anyone, matching how they're already open to
everyone for running/correcting; an owned rule can only be retitled
by its owner.

Favorites: a private per-user signal, not a public comment.
"""

import json

import pytest
from fastapi.testclient import TestClient

from asr.api.app import create_app
from asr.api.auth import get_current_user
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
    anon_id = _insert_walker_rule(conn)
    owned_id = _insert_walker_rule(conn, owner_uid="user-a")
    conn.close()
    with TestClient(create_app(database_path=str(path))) as running:
        running.anon_id, running.owned_id = anon_id, owned_id
        yield running
        running.app.dependency_overrides.pop(get_current_user, None)


def as_user(client, uid):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": uid, "email": None}


def anonymous(client):
    client.app.dependency_overrides.pop(get_current_user, None)


def test_anyone_can_title_an_ownerless_rule(client):
    anonymous(client)
    resp = client.patch(f"/rules/{client.anon_id}", json={"title": "The Walker"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "The Walker"
    assert body["slug"] == "the-walker"
    assert body["description"] == "a walker"  # untouched, still canon


def test_only_the_owner_can_title_an_owned_rule(client):
    as_user(client, "user-b")
    resp = client.patch(f"/rules/{client.owned_id}", json={"title": "Nope"})
    assert resp.status_code == 403

    as_user(client, "user-a")
    resp = client.patch(f"/rules/{client.owned_id}", json={"title": "My Walker"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "My Walker"


def test_clearing_the_title_clears_the_slug(client):
    anonymous(client)
    client.patch(f"/rules/{client.anon_id}", json={"title": "Something"})
    resp = client.patch(f"/rules/{client.anon_id}", json={"title": None})
    assert resp.json()["title"] is None
    assert resp.json()["slug"] is None


def test_duplicate_titles_get_a_unique_slug(client):
    anonymous(client)
    client.patch(f"/rules/{client.anon_id}", json={"title": "Same Name"})
    as_user(client, "user-a")
    resp = client.patch(f"/rules/{client.owned_id}", json={"title": "Same Name"})
    assert resp.json()["slug"] == "same-name-2"


def test_rule_reachable_by_slug(client):
    anonymous(client)
    client.patch(f"/rules/{client.anon_id}", json={"title": "Findable"})
    resp = client.get("/rules/by-slug/findable")
    assert resp.status_code == 200
    assert resp.json()["id"] == client.anon_id
    assert client.get("/rules/by-slug/does-not-exist").status_code == 404


def test_favorite_add_remove_and_filter(client):
    as_user(client, "user-a")
    assert client.post(f"/rules/{client.anon_id}/favorite").status_code == 200
    body = client.get(f"/rules/{client.anon_id}").json()
    assert body["favorited"] is True

    listed = client.get("/rules?favorited=true").json()
    assert listed["total"] == 1
    assert listed["rules"][0]["id"] == client.anon_id

    assert client.delete(f"/rules/{client.anon_id}/favorite").status_code == 200
    assert client.get("/rules?favorited=true").json()["total"] == 0


def test_favorite_requires_sign_in(client):
    anonymous(client)
    assert client.post(f"/rules/{client.anon_id}/favorite").status_code == 401
    assert client.get("/rules?favorited=true").status_code == 401


def test_sort_most_liked(client):
    as_user(client, "user-a")
    client.post(f"/rules/{client.owned_id}/favorite")
    body = client.get("/rules?sort=most_liked").json()
    assert body["rules"][0]["id"] == client.owned_id
