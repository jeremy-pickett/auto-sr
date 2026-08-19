"""Fingerprints of a run's state (spec section 9.7).

Two different things, deliberately:

- The COMPUTATIONAL fingerprint covers everything that determines the
  future — every array the rule or the harness will consult, the
  scheduler phase when `rate` is in scope, and the RNG state when birth
  draws are declared. Loop detection compares these and nothing else.
- The PATTERN fingerprint covers `kind` only. It is an observation of
  the picture, never a stopping condition (REQ-9.7.5, REQ-9.8.1).

Both hash exact bytes — floats are never quantized (REQ-9.7.2) — with
blake2b-128, arrays taken in name-sorted order and each preceded by its
name and dtype so the hash never depends on allocation order (REQ-9.7.4).
"""

import hashlib

import numpy as np

from .cells import Cells
from .declaration import Declaration
from .dice import Dice

# Twelve is the least common multiple of the permitted rates 1-4:
# two identical grids at different points in the rate cycle have
# different futures (REQ-9.7.1).
SCHEDULER_CYCLE = 12

# The harness only ever asks `age >= stubbornness` and stubbornness
# tops out at 3, so ages above 3 are indistinguishable to the future.
# Clamping is what lets a stubbornness rule ever report frozen
# (REQ-9.7.6).
STUBBORNNESS_AGE_CLAMP = 3


def _add_array(digest, name: str, array: np.ndarray) -> None:
    digest.update(name.encode("utf-8"))
    digest.update(array.dtype.str.encode("utf-8"))
    digest.update(np.ascontiguousarray(array).tobytes())


def computational_fingerprint(
    cells: Cells, declaration: Declaration, tick: int, dice: Dice
) -> bytes:
    """Everything that determines the future, in 16 bytes."""
    arrays: dict[str, np.ndarray] = {}

    for name in declaration.rule_owned():
        arrays[name] = cells._arrays[name]
    for name in declaration.modifiers:
        arrays[name] = cells._arrays[name]
    for name in declaration.semantic_slots:
        arrays[name] = cells._arrays[name]

    # Derived state enters when any consumer — the rule or an active
    # harness semantic — can see it (REQ-9.7.6).
    if "age" in declaration.reads:
        arrays["age"] = cells._arrays["age"]
    elif "stubbornness" in declaration.modifiers:
        arrays["age"] = np.minimum(cells._arrays["age"], STUBBORNNESS_AGE_CLAMP)
    if "changed_last_tick" in declaration.reads:
        arrays["changed_last_tick"] = cells._arrays["changed_last_tick"]

    digest = hashlib.blake2b(digest_size=16)
    for name in sorted(arrays):
        _add_array(digest, name, arrays[name])

    if "rate" in declaration.modifiers:
        digest.update(b"scheduler_phase")
        digest.update(str(tick % SCHEDULER_CYCLE).encode("utf-8"))

    if declaration.declares_birth_draws():
        digest.update(b"rng_state")
        digest.update(dice._state_bytes())

    return digest.digest()


def pattern_fingerprint(cells: Cells) -> bytes:
    """The pattern of kinds, in 16 bytes. An observation only — it never
    stops a run and never joins the computational fingerprint.
    """
    digest = hashlib.blake2b(digest_size=16)
    _add_array(digest, "kind", cells._arrays["kind"])
    return digest.digest()
