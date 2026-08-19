"""POST /rules/generate — the pipeline as a progress stream (REQ-11.4).

The response is text/event-stream from a POST, consumed by the browser
with streaming fetch() — never EventSource, which cannot POST, and
never a POST-then-GET job model, which would reintroduce the queue
REQ-3.6 excludes (REQ-11.4.1).

The pipeline runs in a worker thread with its own database connection;
events cross to the response generator through a queue.
"""

import json
import queue
import threading

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from asr.generation.pipeline import generate_rule
from asr.storage import db

router = APIRouter()

FINAL_EVENT = "complete"


def _run_pipeline(database_path: str, events: queue.Queue) -> None:
    conn = db.connect(database_path)
    try:
        generate_rule(conn, lambda name, data: events.put((name, data)))
    except Exception as failed:  # noqa: BLE001 - the stream must always end
        events.put((FINAL_EVENT, {"status": "error", "error": str(failed)[-500:]}))
    finally:
        conn.close()
        events.put(None)


@router.post("/rules/generate")
def generate(request: Request):
    events: queue.Queue = queue.Queue()
    worker = threading.Thread(
        target=_run_pipeline,
        args=(request.app.state.database_path, events),
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
