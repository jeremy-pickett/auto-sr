"""The Dice facade (spec section 6.7) — the only randomness in a run.

A thin cover over a seeded numpy random Generator. Only whole-grid
draws are exposed, so there is no scalar draw to tempt a per-cell loop.
Every method fills the whole (height, width) grid in one call, in a
fixed order, which is what makes a run replayable from its seed.

Rule code may touch dice only inside make_start (REQ-7.4.1). After
tick 0 the only consumer is the harness's birth assignments (REQ-6.6).
"""

import numpy as np


class Dice:
    def __init__(self, seed: int, height: int, width: int):
        self._shape = (height, width)
        self._random = np.random.default_rng(seed)

    def chance(self, p) -> np.ndarray:
        """Boolean array, True with probability p."""
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be between 0 and 1, got {p!r}")
        return self._random.random(self._shape) < p

    def integers(self, low, high) -> np.ndarray:
        """Integer array, uniform in [low, high)."""
        if high <= low:
            raise ValueError(f"high must be above low, got [{low!r}, {high!r})")
        return self._random.integers(low, high, size=self._shape, dtype=np.int32)

    def choice(self, n) -> np.ndarray:
        """Integer array, uniform in [0, n)."""
        if n < 1:
            raise ValueError(f"n must be at least 1, got {n!r}")
        return self._random.integers(0, n, size=self._shape, dtype=np.int32)

    # ---- harness-private surface below.

    def _state_bytes(self) -> bytes:
        """The generator's exact internal state, as stable bytes.

        Feeds the computational fingerprint when birth draws are
        declared (REQ-9.7.1): two grids with different randomness ahead
        of them are different states, even if every array matches.
        """
        return repr(self._random.bit_generator.state).encode("utf-8")
