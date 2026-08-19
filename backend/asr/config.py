"""Settings for the whole system (spec section 3.9).

Every value can be overridden by an environment variable of the same
name. backend/.env is loaded first, so local overrides live there and
stay out of version control.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _int(name: str, fallback: int) -> int:
    return int(os.environ.get(name, fallback))


def _float(name: str, fallback: float) -> float:
    return float(os.environ.get(name, fallback))


def _text(name: str, fallback: str) -> str:
    return os.environ.get(name, fallback)


@dataclass(frozen=True)
class Settings:
    grid_width: int
    grid_height: int
    max_ticks: int
    snapshot_every: int
    tick_timeout_seconds: float
    run_memory_limit_mb: int
    simplicity_limit: int
    lineage_chance: float
    run_cache_budget_mb: int
    anthropic_model: str
    shape_model: str
    database_path: str


settings = Settings(
    grid_width=_int("GRID_WIDTH", 200),
    grid_height=_int("GRID_HEIGHT", 200),
    max_ticks=_int("MAX_TICKS", 500),
    snapshot_every=_int("SNAPSHOT_EVERY", 50),
    tick_timeout_seconds=_float("TICK_TIMEOUT_SECONDS", 2.0),
    run_memory_limit_mb=_int("RUN_MEMORY_LIMIT_MB", 2048),
    simplicity_limit=_int("SIMPLICITY_LIMIT", 40),
    lineage_chance=_float("LINEAGE_CHANCE", 0.0),
    run_cache_budget_mb=_int("RUN_CACHE_BUDGET_MB", 512),
    anthropic_model=_text("ANTHROPIC_MODEL", "claude-opus-5"),
    # The small classifier call behind observed_shape (REQ-8.2.1).
    shape_model=_text("SHAPE_MODEL", "claude-haiku-4-5"),
    database_path=_text("DATABASE_PATH", "./library.db"),
)
