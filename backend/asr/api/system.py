"""The system page: live pipeline activity plus a browsable history of
both kinds of session this app has ("what the hell is going on" per the
request that started this) -- generation_sessions (one row per
POST /rules/generate, written by generation/pipeline.py) and http_sessions
(the colloquial HTTP session: one row per session cookie, touched by every
request via the middleware in api/app.py -- no client cooperation needed).

Deliberately unauthenticated and globally visible for now, same as every
other route -- this app is single-user. If it ever goes multi-user,
/system/* needs an access check the same way #/mine does today (see
CLAUDE.md).
"""

import os
import time
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request, Response

from asr.api.routes import get_db

router = APIRouter(prefix="/system")

START_TIME = time.time()

# Wider than a fixed heartbeat interval would need: ordinary browsing
# produces requests far sparser than a 20s heartbeat did, so a tight
# window would show nearly everyone as gone between clicks.
ACTIVE_WITHIN_SECONDS = 2 * 60
IDLE_WITHIN_SECONDS = 30 * 60


def _cutoff(seconds_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds_ago)).isoformat()


@router.get("/status")
def system_status(request: Request, response: Response, conn=Depends(get_db)):
    # Every response here is a live snapshot, polled every couple of
    # seconds -- unlike the rest of the API, it must never be cached by
    # anything sitting between the browser and this process (a corporate
    # or ISP proxy, in particular). FastAPI sets no Cache-Control here by
    # default, so an intermediary is free to reuse whatever it first saw
    # forever; no-store forbids that outright.
    response.headers["Cache-Control"] = "no-store"
    in_flight = [
        dict(row)
        for row in conn.execute(
            """SELECT id, stage, started_at FROM generation_sessions
               WHERE finished_at IS NULL ORDER BY started_at"""
        )
    ]
    rules_total = conn.execute("SELECT COUNT(*) AS n FROM rules").fetchone()["n"]
    runs_total = conn.execute("SELECT COUNT(*) AS n FROM runs").fetchone()["n"]
    errors_recent = conn.execute(
        """SELECT COUNT(*) AS n FROM generation_sessions
           WHERE outcome IN ('broken', 'generation_failed') AND started_at > ?""",
        (_cutoff(24 * 3600),),
    ).fetchone()["n"]
    generations_last_hour = conn.execute(
        "SELECT COUNT(*) AS n FROM generation_sessions WHERE started_at > ?",
        (_cutoff(3600),),
    ).fetchone()["n"]
    active_sessions = conn.execute(
        "SELECT COUNT(*) AS n FROM http_sessions WHERE last_seen_at > ?",
        (_cutoff(ACTIVE_WITHIN_SECONDS),),
    ).fetchone()["n"]
    idle_sessions = conn.execute(
        "SELECT COUNT(*) AS n FROM http_sessions WHERE last_seen_at <= ? AND last_seen_at > ?",
        (_cutoff(ACTIVE_WITHIN_SECONDS), _cutoff(IDLE_WITHIN_SECONDS)),
    ).fetchone()["n"]
    try:
        db_size_bytes = os.path.getsize(request.app.state.database_path)
    except OSError:
        db_size_bytes = None

    return {
        "uptime_seconds": time.time() - START_TIME,
        "in_flight": in_flight,
        "rules_total": rules_total,
        "runs_total": runs_total,
        "errors_recent_24h": errors_recent,
        "generations_last_hour": generations_last_hour,
        "active_sessions": active_sessions,
        "idle_sessions": idle_sessions,
        "db_size_bytes": db_size_bytes,
    }


@router.get("/sessions")
def system_sessions(response: Response, page: int = 1, page_size: int = 50, conn=Depends(get_db)):
    response.headers["Cache-Control"] = "no-store"  # see system_status
    page = max(page, 1)
    page_size = max(1, min(page_size, 200))
    total = conn.execute(
        """SELECT (SELECT COUNT(*) FROM generation_sessions)
                 + (SELECT COUNT(*) FROM http_sessions) AS n"""
    ).fetchone()["n"]
    rows = conn.execute(
        """SELECT * FROM (
               SELECT 'gen' AS kind, id, owner_uid, started_at, finished_at,
                      stage, outcome, rule_id, error_text, model_id,
                      NULL AS ip_address, NULL AS user_agent,
                      NULL AS last_path, NULL AS request_count, NULL AS last_seen_at
               FROM generation_sessions
               UNION ALL
               SELECT 'http' AS kind, id, owner_uid, started_at, NULL AS finished_at,
                      NULL AS stage, NULL AS outcome, NULL AS rule_id,
                      NULL AS error_text, NULL AS model_id,
                      ip_address, user_agent, last_path, request_count, last_seen_at
               FROM http_sessions
           )
           ORDER BY started_at DESC
           LIMIT ? OFFSET ?""",
        (page_size, (page - 1) * page_size),
    ).fetchall()
    # Guest vs. signed-in matters for this page (per the request that
    # started it); the raw owner_uid does not need to leave the server to
    # say that -- same "derived boolean, not the identifier" convention
    # routes.py's _rule_summary already uses for "has_owner".
    sessions = []
    for row in rows:
        session = dict(row)
        session["signed_in"] = session.pop("owner_uid") is not None
        sessions.append(session)
    return {"total": total, "page": page, "page_size": page_size, "sessions": sessions}
