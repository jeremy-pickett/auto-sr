"""The profile mechanism (documents/new-features-2.md, items 5/11): a
signed-in user's one editable bit of public identity, a display name
that overrides their comment pseudonym.
"""

import pytest
from fastapi.testclient import TestClient

from asr.api.app import create_app
from asr.api.auth import get_current_user
from asr.api.profile import DISPLAY_NAME_MAX_LENGTH, clean_display_name
from asr.storage import db


@pytest.fixture()
def client(tmp_path):
    path = tmp_path / "library.db"
    db.connect(path).close()
    with TestClient(create_app(database_path=str(path))) as running:
        yield running
        running.app.dependency_overrides.pop(get_current_user, None)


def as_user(client, uid):
    client.app.dependency_overrides[get_current_user] = lambda: {"uid": uid, "email": f"{uid}@example.com"}


def anonymous(client):
    client.app.dependency_overrides.pop(get_current_user, None)


def test_clean_display_name_strips_control_chars_and_collapses_whitespace():
    assert clean_display_name("bad\x00name") == "badname"
    assert clean_display_name("  lots   of   space  ") == "lots of space"


def test_anonymous_cannot_view_or_set_profile(client):
    anonymous(client)
    assert client.get("/profile").status_code == 401
    assert client.put("/profile", json={"display_name": "x"}).status_code == 401


def test_profile_defaults_to_no_override(client):
    as_user(client, "user-a")
    assert client.get("/profile").json() == {"display_name": None}


def test_set_and_read_back_display_name(client):
    as_user(client, "user-a")
    resp = client.put("/profile", json={"display_name": "Alice"})
    assert resp.status_code == 200
    assert resp.json() == {"display_name": "Alice"}
    assert client.get("/profile").json() == {"display_name": "Alice"}


def test_clearing_display_name_falls_back_to_none(client):
    as_user(client, "user-a")
    client.put("/profile", json={"display_name": "Alice"})
    resp = client.put("/profile", json={"display_name": "   "})
    assert resp.json() == {"display_name": None}
    assert client.get("/profile").json() == {"display_name": None}


def test_display_name_over_max_length_rejected(client):
    as_user(client, "user-a")
    resp = client.put("/profile", json={"display_name": "x" * (DISPLAY_NAME_MAX_LENGTH + 1)})
    assert resp.status_code == 422


def test_profile_is_scoped_per_user(client):
    as_user(client, "user-a")
    client.put("/profile", json={"display_name": "Alice"})
    as_user(client, "user-b")
    assert client.get("/profile").json() == {"display_name": None}
