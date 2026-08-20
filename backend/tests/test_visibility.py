"""Private rules and the mine=true personal library (Firebase auth
Phase 1). The default /rules listing is always public-only regardless
of who's asking; a private rule 404s -- with the exact same message
as a genuine not-found -- for anyone but its owner, across every read
endpoint that touches it.
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
            "description": f"a walker ({visibility})",
            "kinds": 2, "neighbors": "plus_4", "reach": 1,
            "uses_json": json.dumps(["heading"]),
            "source_code": inspect.getsource(walker.Rule),
            "source_hash": "walker-test", "status": "ok",
            "engine_version": "test", "owner_uid": owner_uid,
            "visibility": visibility,
        },
    )
    run_id = db.save_run(
        conn, rule_id, result,
        start_seed=1, width=10, height=6, max_ticks=20,
        guessed_behavior="repeats", guess_confidence="high",
        engine_version="test", snapshot_every=10, is_canonical=True,
    )
    return rule_id, run_id


@pytest.fixture()
def two_rules(tmp_path):
    path = tmp_path / "library.db"
    conn = db.connect(path)
    public_id, public_run_id = _insert_walker_rule(conn)
    private_id, private_run_id = _insert_walker_rule(
        conn, owner_uid="user-a", visibility="private"
    )
    conn.close()
    with TestClient(create_app(database_path=str(path))) as client:
        client.public_id, client.public_run_id = public_id, public_run_id
        client.private_id, client.private_run_id = private_id, private_run_id
        yield client
        client.app.dependency_overrides.pop(get_current_user, None)


def as_user(client, uid, email=None):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": uid, "email": email}


def anonymous(client):
    client.app.dependency_overrides.pop(get_current_user, None)


def test_default_listing_is_public_only(two_rules):
    anonymous(two_rules)
    body = two_rules.get("/rules").json()
    assert body["total"] == 1
    assert body["rules"][0]["id"] == two_rules.public_id


def test_default_listing_is_public_only_even_when_signed_in(two_rules):
    as_user(two_rules, "user-a")
    body = two_rules.get("/rules").json()
    assert body["total"] == 1
    assert body["rules"][0]["id"] == two_rules.public_id


def test_mine_requires_sign_in(two_rules):
    anonymous(two_rules)
    assert two_rules.get("/rules?mine=true").status_code == 401


def test_mine_shows_the_owners_private_rule(two_rules):
    as_user(two_rules, "user-a")
    body = two_rules.get("/rules?mine=true").json()
    assert body["total"] == 1
    rule = body["rules"][0]
    assert rule["id"] == two_rules.private_id
    assert rule["visibility"] == "private"
    assert rule["mine"] is True
    assert "owner_uid" not in rule  # never exposed, even to the owner


def test_mine_does_not_show_someone_elses_private_rule(two_rules):
    as_user(two_rules, "user-b")
    body = two_rules.get("/rules?mine=true").json()
    assert body["total"] == 0


def test_mine_does_not_show_someone_elses_public_rule(two_rules):
    # A feature-list complaint said "Mine still shows the full library" --
    # that turned out to describe a library where nearly every rule
    # happened to be owned by the one signed-in user, not an actual leak.
    # This nails down the leak case directly: user-b owns nothing, and
    # mine=true must stay empty even though a public rule (owned by
    # nobody) and another public rule exist in the library.
    conn = db.connect(two_rules.app.state.database_path)
    _insert_walker_rule(conn, owner_uid="user-c", visibility="public")
    conn.close()
    as_user(two_rules, "user-b")
    body = two_rules.get("/rules?mine=true").json()
    assert body["total"] == 0


@pytest.mark.parametrize("as_who", [None, "user-b"])
def test_private_rule_404s_for_non_owners(two_rules, as_who):
    if as_who:
        as_user(two_rules, as_who)
    else:
        anonymous(two_rules)
    rid, run_id = two_rules.private_id, two_rules.private_run_id
    not_found = two_rules.get(f"/rules/{rid}").status_code
    assert not_found == 404
    assert two_rules.get(f"/rules/{rid}").json() == two_rules.get("/rules/999999").json()
    assert two_rules.post(f"/rules/{rid}/runs", json={}).status_code == 404
    assert two_rules.get(f"/runs/{run_id}").status_code == 404
    assert two_rules.get(f"/runs/{run_id}/grids").status_code == 404
    assert two_rules.get(f"/runs/{run_id}/export").status_code == 404
    assert two_rules.get(f"/runs/{run_id}/cell/0/0").status_code == 404
    assert two_rules.get(f"/rules/{rid}/preview.png").status_code == 404
    assert two_rules.patch(f"/runs/{run_id}", json={"user_flagged": True}).status_code == 404


def test_private_rule_visible_to_its_owner(two_rules):
    as_user(two_rules, "user-a")
    rid, run_id = two_rules.private_id, two_rules.private_run_id
    assert two_rules.get(f"/rules/{rid}").status_code == 200
    assert two_rules.get(f"/runs/{run_id}").status_code == 200
    assert two_rules.get(f"/runs/{run_id}/grids").status_code == 200
    assert two_rules.get(f"/runs/{run_id}/export").status_code == 200
    assert two_rules.get(f"/runs/{run_id}/cell/0/0").status_code == 200
    assert two_rules.get(f"/rules/{rid}/preview.png").status_code == 200
    assert two_rules.patch(f"/runs/{run_id}", json={"user_flagged": True}).status_code == 200
    assert two_rules.post(f"/rules/{rid}/runs", json={}).status_code == 200


def test_public_rule_unaffected_by_ownership_checks(two_rules):
    # A public rule stays fully open to anyone, signed in or not --
    # this feature must not narrow existing public-rule behavior.
    anonymous(two_rules)
    rid, run_id = two_rules.public_id, two_rules.public_run_id
    assert two_rules.get(f"/rules/{rid}").status_code == 200
    assert two_rules.get(f"/runs/{run_id}").status_code == 200
    assert two_rules.patch(f"/runs/{run_id}", json={"user_flagged": True}).status_code == 200


def test_rss_feed_never_lists_a_private_rule(two_rules):
    anonymous(two_rules)
    body = two_rules.get("/library/feed.rss").text
    assert f"/rules/{two_rules.public_id}" in body
    assert f"/rules/{two_rules.private_id}" not in body


def test_rss_item_links_point_at_the_frontend_not_this_api(two_rules):
    # Regression: item links used to be built from request.base_url,
    # which is this API's own origin -- a bare JSON server with no
    # route at "/", so clicking through 404'd instead of opening the
    # app. They must use settings.frontend_url instead.
    from asr.config import settings

    anonymous(two_rules)
    body = two_rules.get("/library/feed.rss").text
    assert f"{settings.frontend_url}/#/rules/{two_rules.public_id}" in body
    assert "http://testserver" not in body
