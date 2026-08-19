"""Rebuilding grids from stored payloads (REQ-11.2, REQ-12.6).

Stored properties decode from the nearest snapshot at or before the
requested range, walking deltas forward — at most one snapshot interval.
Derived properties are rebuilt, never read from deltas:

- `changed_last_tick` at tick t is `kind[t] != kind[t-1]` (False at 0).
- `age` starts from the copy kept in each snapshot (REQ-12.6.2) and
  walks forward with the kind history.

The cache holds one full-run stack per (run id, property), budgeted in
bytes, not runs (REQ-11.2.1), evicting least-recently-used.
"""

from collections import OrderedDict

import numpy as np

from asr.storage import encoding

AGE_CEILING = 65535


def _snapshot_at_or_before(conn, run_id: int, tick: int) -> int:
    row = conn.execute(
        """SELECT MAX(tick) AS tick FROM ticks
           WHERE run_id = ? AND tick <= ? AND payload_encoding = 'snapshot'""",
        (run_id, tick),
    ).fetchone()
    if row["tick"] is None:
        raise ValueError(f"run {run_id} has no snapshot at or before tick {tick}")
    return row["tick"]


def _walk(conn, run_id: int, first_tick: int, last_tick: int):
    """Yield (tick, arrays) for a contiguous range, starting the decode
    at the nearest snapshot so the caller never pays more than one
    snapshot interval of extra decoding.
    """
    start = _snapshot_at_or_before(conn, run_id, first_tick)
    arrays = None
    for row in conn.execute(
        """SELECT tick, payload_encoding, payload_blob FROM ticks
           WHERE run_id = ? AND tick BETWEEN ? AND ? ORDER BY tick""",
        (run_id, start, last_tick),
    ):
        arrays = encoding.decode(row["payload_encoding"], row["payload_blob"], arrays)
        yield row["tick"], arrays


def reconstruct_range(conn, run_id: int, properties: list, first_tick: int, last_tick: int) -> dict:
    """Rebuild the requested properties for a tick range. Returns
    {name: array stacked (ticks, height, width)}, index 0 = first_tick.
    """
    wants_changed = "changed_last_tick" in properties
    wants_age = "age" in properties
    stored = [p for p in properties if p not in encoding.NEVER_IN_DELTAS]

    # changed_last_tick at the first tick needs the kind one tick back.
    walk_from = max(0, first_tick - 1) if wants_changed else first_tick
    # age walks forward from the snapshot's stored copy.
    if wants_age:
        walk_from = min(walk_from, _snapshot_at_or_before(conn, run_id, first_tick))

    span = last_tick - first_tick + 1
    stacks = {name: [None] * span for name in properties}
    age = None
    previous_kind = None
    for tick, arrays in _walk(conn, run_id, walk_from, last_tick):
        if wants_age:
            if "age" in arrays and (age is None or tick <= first_tick):
                age = arrays["age"]  # a snapshot carries age (REQ-12.6.2)
            elif age is not None and previous_kind is not None:
                born = arrays["kind"] != previous_kind
                grown = np.minimum(age.astype(np.uint32) + 1, AGE_CEILING).astype(np.uint16)
                age = np.where(born, np.uint16(0), grown)
        position = tick - first_tick
        if 0 <= position < span:
            for name in stored:
                stacks[name][position] = arrays[name]
            if wants_age:
                stacks["age"][position] = age
            if wants_changed:
                if tick == 0:
                    stacks["changed_last_tick"][position] = np.zeros(
                        arrays["kind"].shape, dtype=bool
                    )
                else:
                    stacks["changed_last_tick"][position] = arrays["kind"] != previous_kind
        previous_kind = arrays["kind"]
    return {name: np.stack(stack) for name, stack in stacks.items()}


class ReconstructionCache:
    """Full-run property stacks, evicted least-recently-used against a
    byte budget (REQ-11.2)."""

    def __init__(self, budget_bytes: int):
        self.budget_bytes = budget_bytes
        self._held = OrderedDict()  # (run_id, property) -> stack
        self._held_bytes = 0

    def property_history(self, conn, run_id: int, name: str) -> np.ndarray:
        """Every tick of one property, shaped (ticks_run + 1, h, w)."""
        key = (run_id, name)
        if key in self._held:
            self._held.move_to_end(key)
            return self._held[key]
        last = conn.execute(
            "SELECT MAX(tick) AS tick FROM ticks WHERE run_id = ?", (run_id,)
        ).fetchone()["tick"]
        if last is None:
            raise ValueError(f"run {run_id} has no ticks")
        stack = reconstruct_range(conn, run_id, [name], 0, last)[name]
        self._held[key] = stack
        self._held_bytes += stack.nbytes
        while self._held_bytes > self.budget_bytes and len(self._held) > 1:
            _, evicted = self._held.popitem(last=False)
            self._held_bytes -= evicted.nbytes
        return stack
