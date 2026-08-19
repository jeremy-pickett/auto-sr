"""POST /rules/generate — the pipeline as a progress stream (REQ-11.4).

The response is text/event-stream from a POST, consumed by the browser
with streaming fetch() — never EventSource, which cannot POST, and
never a POST-then-GET job model, which would reintroduce the queue
REQ-3.6 excludes (REQ-11.4.1).

The pipeline runs in a worker thread with its own database connection;
events cross to the response generator through a queue.
"""

import json
import logging
import queue
import threading
from typing import Literal

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from asr.api.auth import get_current_user
from asr.api.routes import _apply_title
from asr.generation.pipeline import clean_spark, generate_rule
from asr.storage import db

router = APIRouter()
logger = logging.getLogger(__name__)

FINAL_EVENT = "complete"


class GenerateRequest(BaseModel):
    visibility: Literal["public", "private"] = "public"
    # A short creative hint at invention time (asr.generation.pipeline
    # .clean_spark does the real cleaning/64-char enforcement; this is
    # only a coarse, cheap pre-limit against a genuinely huge payload).
    spark: str | None = Field(default=None, max_length=256)
    # Naming a rule at the moment it's invented, not just afterward --
    # _apply_title (routes.py) does the real cleaning/slug generation,
    # same as PATCH /rules/{id}. No auth gate: an anonymous request
    # can only ever produce an ownerless rule, and ownerless rules are
    # already titlable by anyone (see set_rule_title's docstring).
    title: str | None = Field(default=None, max_length=256)


def _run_pipeline(database_path: str, events: queue.Queue, owner_uid, visibility, spark, title) -> None:
    conn = db.connect(database_path)
    try:
        payload = generate_rule(
            conn, lambda name, data: events.put((name, data)),
            owner_uid=owner_uid, visibility=visibility, spark=spark,
        )
        if title and payload.get("rule_id") is not None:
            _apply_title(conn, payload["rule_id"], title)
    except Exception as failed:  # noqa: BLE001 - the stream must always end
        # The browser only sees the tail; the server log keeps the
        # whole story so a transient API failure is diagnosable later.
        logger.exception("generation pipeline failed")
        events.put((FINAL_EVENT, {"status": "error", "error": str(failed)[-500:]}))
    finally:
        conn.close()
        events.put(None)


@router.post("/rules/generate")
def generate(
    request: Request,
    body: GenerateRequest | None = Body(default=None),
    user: dict | None = Depends(get_current_user),
):
    # body defaults to None (not a GenerateRequest()) so this keeps
    # accepting the exact request the frontend has always sent: a bare
    # POST with no body and no Content-Type at all.
    visibility = body.visibility if body else "public"
    if visibility == "private" and user is None:
        raise HTTPException(400, "sign in to create a private rule")
    owner_uid = user["uid"] if user else None
    if user is None:
        visibility = "public"  # anonymous requests are always public/global

    try:
        spark = clean_spark(body.spark) if body else None
    except ValueError as bad:
        raise HTTPException(400, str(bad)) from None
    if spark and user is None:
        raise HTTPException(400, "sign in to add a spark")

    title = body.title if body else None

    events: queue.Queue = queue.Queue()
    worker = threading.Thread(
        target=_run_pipeline,
        args=(request.app.state.database_path, events, owner_uid, visibility, spark, title),
        daemon=True,
    )
    worker.start()

    def event_stream():
        while True:
            item = events.get()
            if item is None:
                break
            name, data = item
            yield f"event: {name}\ndata: {json.dumps(data)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
