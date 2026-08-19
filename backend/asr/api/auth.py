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


def get_current_user(request: Request) -> dict | None:
    header = request.headers.get("authorization")
    if not header or not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    if not token:
        return None
    try:
        claims = google_id_token.verify_firebase_token(
            token, _transport, audience=settings.firebase_project_id,
        )
        expected_issuer = f"https://securetoken.google.com/{settings.firebase_project_id}"
        if claims is None or claims.get("iss") != expected_issuer or not claims.get("sub"):
            raise ValueError("issuer or subject check failed")
    except Exception as failed:
        raise HTTPException(401, f"invalid auth token: {failed}") from None
    return {"uid": claims["sub"], "email": claims.get("email")}
