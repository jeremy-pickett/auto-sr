"""The engine revision stamp (REQ-12.4.2).

Two runs of byte-identical rule source under different harness
revisions are different experiments, so every rule and run records the
git revision that produced it.
"""

import functools
import subprocess
from pathlib import Path

HELPER_VERSION = 1  # bump when any section-6 helper changes behavior


@functools.lru_cache(maxsize=1)
def engine_version() -> str:
    repo_root = Path(__file__).resolve().parents[2]
    try:
        finished = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if finished.returncode == 0:
            return finished.stdout.strip()
    except OSError:
        pass
    return "unknown"
