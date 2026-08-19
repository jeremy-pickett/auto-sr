"""get_current_user (asr/api/auth.py): optional, never-erroring-on-
absence Firebase token verification. The Step 0 spike already proved
verify_firebase_token itself behaves correctly against a real Firebase
project (a real token accepted with correct claims, a tampered one
rejected) -- these tests keep the test suite fast and offline by
faking that one call, and instead cover get_current_user's own logic:
missing/malformed headers are anonymous, a present-but-invalid token
is always a hard error, never silently downgraded.
"""

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from asr.api import auth


class FakeRequest:
    def __init__(self, authorization=None):
        self.headers = {"authorization": authorization} if authorization else {}


def test_no_header_is_anonymous():
    assert auth.get_current_user(FakeRequest()) is None


def test_header_without_bearer_prefix_is_anonymous():
    assert auth.get_current_user(FakeRequest("not-a-bearer-token")) is None


def test_empty_bearer_token_is_anonymous():
    assert auth.get_current_user(FakeRequest("Bearer ")) is None


def test_valid_token_returns_uid_and_email(monkeypatch):
    # settings is a frozen dataclass instance -- swap the module-level
    # name auth.py imported, rather than mutating the real singleton.
    monkeypatch.setattr(auth, "settings", SimpleNamespace(firebase_project_id="test-project"))
    monkeypatch.setattr(
        auth.google_id_token,
        "verify_firebase_token",
        lambda token, transport, audience: {
            "sub": "uid-123",
            "email": "jane@example.com",
            "iss": "https://securetoken.google.com/test-project",
            "aud": "test-project",
        },
    )
    user = auth.get_current_user(FakeRequest("Bearer real-token"))
    assert user == {"uid": "uid-123", "email": "jane@example.com"}


def test_invalid_token_is_a_hard_401_not_anonymous(monkeypatch):
    def boom(token, transport, audience):
        raise ValueError("bad signature")

    monkeypatch.setattr(auth.google_id_token, "verify_firebase_token", boom)
    with pytest.raises(HTTPException) as excinfo:
        auth.get_current_user(FakeRequest("Bearer garbage"))
    assert excinfo.value.status_code == 401


def test_wrong_issuer_is_rejected_even_if_the_library_accepts_it(monkeypatch):
    # Defensive check beyond whatever verify_firebase_token itself
    # enforces internally -- a token for a different Firebase project
    # must never be accepted just because the signature checks out.
    monkeypatch.setattr(auth, "settings", SimpleNamespace(firebase_project_id="test-project"))
    monkeypatch.setattr(
        auth.google_id_token,
        "verify_firebase_token",
        lambda token, transport, audience: {
            "sub": "uid-123",
            "email": "jane@example.com",
            "iss": "https://securetoken.google.com/SOME-OTHER-PROJECT",
            "aud": "test-project",
        },
    )
    with pytest.raises(HTTPException) as excinfo:
        auth.get_current_user(FakeRequest("Bearer token-for-a-different-project"))
    assert excinfo.value.status_code == 401
