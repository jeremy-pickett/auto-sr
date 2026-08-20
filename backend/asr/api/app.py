"""FastAPI wiring. Run from backend/ with:

    .venv/bin/uvicorn asr.api.app:app --reload
"""

import logging
import secrets
import time

from fastapi import FastAPI, Request

from asr.api.auth import try_resolve_uid
from asr.api.comments import router as comments_router
from asr.api.profile import router as profile_router
from asr.api.routes import router
from asr.api.stream import router as generation_router
from asr.api.system import router as system_router
from asr.config import settings
from asr.storage import db
from asr.storage.reconstruct import ReconstructionCache

SESSION_COOKIE = "asr_session"
SESSION_MAX_AGE_SECONDS = 24 * 3600  # a sliding window, refreshed every request

# Basic, deliberately unfancy: plain log lines, not a metrics stack.
# Without this, the root logger's default level (WARNING) would
# silently swallow the INFO-level timing lines below and in
# generation/pipeline.py -- there was no logging config anywhere in
# the app before this, so nothing was actually visible.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


def _client_ip(request: Request) -> str | None:
    # In dev, browser traffic reaches this process through Vite's proxy
    # (vite.config.js), which makes its own outbound connection here --
    # without this, request.client.host is the proxy's own loopback
    # address for every visitor, not theirs. xfwd: true on that proxy
    # sets X-Forwarded-For to the real address; prefer it when present,
    # falling back to the raw socket address for direct requests (tests,
    # or hitting :8000 without the frontend proxy in front of it).
    forwarded = request.headers.get("x-forwarded-for")
    ip = forwarded.split(",")[0].strip() if forwarded else None
    if not ip:
        ip = request.client.host if request.client else None
    # Vite's dev server listens dual-stack (server.host: true), so Node
    # often reports even a plain IPv4 connection as an IPv4-mapped IPv6
    # address ("::ffff:203.0.113.7") -- that's the same address, just in
    # a form that reads as IPv6. Unwrap it back to plain IPv4.
    if ip and ip.startswith("::ffff:"):
        ip = ip[len("::ffff:"):]
    return ip


def create_app(database_path: str | None = None) -> FastAPI:
    app = FastAPI(title="Autonomous Semantic Ruliology")
    app.state.database_path = database_path or settings.database_path
    # The cache budget is in bytes, not runs (REQ-11.2.1).
    app.state.cache = ReconstructionCache(settings.run_cache_budget_mb * 1024 * 1024)
    app.include_router(router)
    app.include_router(generation_router)
    app.include_router(comments_router)
    app.include_router(profile_router)
    app.include_router(system_router)

    @app.middleware("http")
    async def track_request(request: Request, call_next):
        # One line per request (method, path, status, wall time) plus the
        # colloquial HTTP session: a cookie identifies the browser, and
        # every request -- not just ones a client remembers to report --
        # touches that session's "last seen." No heartbeat, no client
        # bookkeeping, nothing to go stale if the client misbehaves.
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %d (%.1fms)",
            request.method, request.url.path, response.status_code, elapsed_ms,
        )

        session_id = request.cookies.get(SESSION_COOKIE) or secrets.token_urlsafe(24)
        conn = db.connect(app.state.database_path)
        try:
            db.touch_http_session(
                conn, session_id, try_resolve_uid(request),
                _client_ip(request),
                request.headers.get("user-agent"),
                request.url.path,
            )
        finally:
            conn.close()
        response.set_cookie(
            SESSION_COOKIE, session_id, max_age=SESSION_MAX_AGE_SECONDS,
            httponly=True, samesite="lax",
        )
        return response

    return app


app = create_app()
