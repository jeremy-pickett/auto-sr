"""Optional Firebase ID-token verification (Phase 1: Email/Password
only). A missing Authorization header is anonymous, never an error —
every route this is used on must keep working with no header sent,
exactly as it did before this feature existed. A present-but-invalid
token is always an error; that's the one case this must never
silently resolve to "treat as anonymous."

No service-account secret is involved: verify_firebase_token checks a
token's signature against Google's public keys and confirms it names
this project, using only the (non-secret) project ID.
"""

from fastapi import HTTPException, Request
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from asr.config import settings

# Reused across requests; the underlying library keeps its own small
# in-memory cache of Google's public certs.
_transport = google_requests.Request()


def _bearer_token(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if not header or not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    return token or None


def _verify(token: str) -> dict:
    """Raises on any failure -- signature, issuer, or missing subject."""
    claims = google_id_token.verify_firebase_token(
        token, _transport, audience=settings.firebase_project_id,
    )
    expected_issuer = f"https://securetoken.google.com/{settings.firebase_project_id}"
    if claims is None or claims.get("iss") != expected_issuer or not claims.get("sub"):
        raise ValueError("issuer or subject check failed")
    return claims


def get_current_user(request: Request) -> dict | None:
    token = _bearer_token(request)
    if token is None:
        return None
    try:
        claims = _verify(token)
    except Exception as failed:
        raise HTTPException(401, f"invalid auth token: {failed}") from None
    return {"uid": claims["sub"], "email": claims.get("email")}


def try_resolve_uid(request: Request) -> str | None:
    """Best-effort identity for session bookkeeping ONLY -- never use this
    to gate access to anything. Unlike get_current_user, a present-but-
    invalid token here is not an error: this runs on every request via
    the session middleware (api/app.py), and a stale token must not 401
    the entire site just to update a "last seen" timestamp.
    """
    token = _bearer_token(request)
    if token is None:
        return None
    try:
        return _verify(token)["sub"]
    except Exception:
        return None
