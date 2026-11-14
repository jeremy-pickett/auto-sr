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
    llm_provider: str
    anthropic_model: str
    openai_model: str
    generator_model: str
    shape_model: str
    database_path: str
    firebase_project_id: str
    frontend_url: str


# Which company's model writes the rules. OpenAI is the default;
# LLM_PROVIDER=anthropic switches back to the original Claude path.
_provider = _text("LLM_PROVIDER", "openai").strip().lower()
if _provider not in ("openai", "anthropic"):
    raise ValueError(f"LLM_PROVIDER must be 'openai' or 'anthropic', got {_provider!r}")
_anthropic_model = _text("ANTHROPIC_MODEL", "claude-opus-5")
# A fast, current OpenAI model; override with OPENAI_MODEL.
_openai_model = _text("OPENAI_MODEL", "gpt-5.4-mini")
_generator_model = _openai_model if _provider == "openai" else _anthropic_model
# The small classifier call behind observed_shape (REQ-8.2.1).
_shape_default = "gpt-5.4-nano" if _provider == "openai" else "claude-haiku-4-5"

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
    llm_provider=_provider,
    anthropic_model=_anthropic_model,
    openai_model=_openai_model,
    # The model that actually writes rules, whichever provider is on.
    generator_model=_generator_model,
    shape_model=_text("SHAPE_MODEL", _shape_default),
    database_path=_text("DATABASE_PATH", "./library.db"),
    # Not a secret -- the same value that ships in the frontend's
    # public Firebase web config. Used only to check a verified
    # token's audience claim (asr/api/auth.py).
    firebase_project_id=_text("FIREBASE_PROJECT_ID", ""),
    # Where the SPA itself is served, as opposed to this API. The two
    # run on different origins in dev (Vite proxies API paths through
    # to here) -- request.base_url reflects *this* server, so anything
    # that builds a link a person should click (RSS items, share
    # links) needs this instead, or it points at a bare API host that
    # 404s on everything but the JSON routes.
    frontend_url=_text("FRONTEND_URL", "http://localhost:5173"),
)
