"""FastAPI wiring. Run from backend/ with:

    .venv/bin/uvicorn asr.api.app:app --reload
"""

from fastapi import FastAPI

from asr.api.routes import router
from asr.api.stream import router as generation_router
from asr.config import settings
from asr.storage.reconstruct import ReconstructionCache


def create_app(database_path: str | None = None) -> FastAPI:
    app = FastAPI(title="Autonomous Semantic Ruliology")
    app.state.database_path = database_path or settings.database_path
    # The cache budget is in bytes, not runs (REQ-11.2.1).
    app.state.cache = ReconstructionCache(settings.run_cache_budget_mb * 1024 * 1024)
    app.include_router(router)
    app.include_router(generation_router)
    return app


app = create_app()
