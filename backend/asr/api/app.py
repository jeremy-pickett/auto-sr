"""FastAPI wiring. Run from backend/ with:

    .venv/bin/uvicorn asr.api.app:app --reload
"""

import logging
import time

from fastapi import FastAPI, Request

from asr.api.comments import router as comments_router
from asr.api.routes import router
from asr.api.stream import router as generation_router
from asr.config import settings
from asr.storage.reconstruct import ReconstructionCache

# Basic, deliberately unfancy: plain log lines, not a metrics stack.
# Without this, the root logger's default level (WARNING) would
# silently swallow the INFO-level timing lines below and in
# generation/pipeline.py -- there was no logging config anywhere in
# the app before this, so nothing was actually visible.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


def create_app(database_path: str | None = None) -> FastAPI:
    app = FastAPI(title="Autonomous Semantic Ruliology")
    app.state.database_path = database_path or settings.database_path
    # The cache budget is in bytes, not runs (REQ-11.2.1).
    app.state.cache = ReconstructionCache(settings.run_cache_budget_mb * 1024 * 1024)
    app.include_router(router)
    app.include_router(generation_router)
    app.include_router(comments_router)

    @app.middleware("http")
    async def log_request_timing(request: Request, call_next):
        # One line per request: method, path, status, wall time. The
        # whole point is being able to tell, from the log alone, which
        # endpoint got slow when several people are using the app at
        # once -- not a profiler, just a paper trail.
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %d (%.1fms)",
            request.method, request.url.path, response.status_code, elapsed_ms,
        )
        return response

    return app


app = create_app()
