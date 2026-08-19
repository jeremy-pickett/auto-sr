"""Executing a run (spec section 9).

A run is one rule, one starting grid, up to MAX_TICKS ticks, executed
to completion before playback begins (REQ-9.1). Every tick is recorded;
stopping is decided by exact recurrence of the computational
fingerprint, the tick budget, or the per-tick timeout — never by the
picture going quiet (REQ-9.8.1).
"""

import math
import time
from dataclasses import dataclass

import numpy as np

from .declaration import Declaration
from .dice import Dice
from .fingerprint import computational_fingerprint, pattern_fingerprint
from .tick import apply_tick, start_grid

STOP_REASONS = ("frozen", "looping", "ran_out", "too_slow")


@dataclass
class TickRecord:
    tick: int
    arrays: dict  # every array at this tick, by property name
    kind_counts: list
    variety: float
    cells_changed: int
    kind_quiet_for: int
    state_fingerprint: bytes
    pattern_fingerprint: bytes


@dataclass
class RunResult:
    stopped_because: str  # frozen | looping | ran_out | too_slow
    loop_length: int | None
    ticks_run: int  # the last completed tick number
    pattern_settled_at: int | None
    ticks: list  # TickRecord per tick, index == tick number


def _variety(kind: np.ndarray, kinds: int) -> float:
    """How evenly spread the kinds are: 0.0 for a single kind present,
    1.0 for a perfectly even spread (REQ-9.10). (Standard term: Shannon
    entropy over the kind distribution, divided by log(KINDS).)
    """
    counts = np.bincount(kind.ravel(), minlength=kinds)
    total = kind.size
    shares = counts[counts > 0] / total
    spread = -(shares * np.log(shares)).sum()
    return float(spread / math.log(kinds))


def _record(cells, declaration, tick, dice, previous: "TickRecord | None") -> TickRecord:
    kind = cells._arrays["kind"]
    pattern = pattern_fingerprint(cells)
    if previous is None:
        changed = 0
        quiet_for = 0
    else:
        changed = int(np.count_nonzero(kind != previous.arrays["kind"]))
        quiet_for = previous.kind_quiet_for + 1 if pattern == previous.pattern_fingerprint else 0
    return TickRecord(
        tick=tick,
        arrays=dict(cells._arrays),
        kind_counts=np.bincount(kind.ravel(), minlength=declaration.kinds).tolist(),
        variety=_variety(kind, declaration.kinds),
        cells_changed=changed,
        kind_quiet_for=quiet_for,
        state_fingerprint=computational_fingerprint(cells, declaration, tick, dice),
        pattern_fingerprint=pattern,
    )


def assemble_result(ticks: list, stopped_because: str, loop_length: int | None) -> RunResult:
    """Finish a run's bookkeeping from its tick records. Also used by
    the child-process runner when the parent had to kill the child.
    """
    return RunResult(
        stopped_because=stopped_because,
        loop_length=loop_length,
        ticks_run=ticks[-1].tick,
        pattern_settled_at=_pattern_settled_at(ticks),
        ticks=ticks,
    )


def _pattern_settled_at(ticks: list) -> int | None:
    """The earliest tick after which the pattern fingerprint never
    changes again (REQ-9.11). Computable only at run end; None when the
    pattern was still changing on the final tick.
    """
    last_change = 0
    for previous, current in zip(ticks, ticks[1:]):
        if current.pattern_fingerprint != previous.pattern_fingerprint:
            last_change = current.tick
    if ticks and last_change == ticks[-1].tick and last_change != 0:
        return None
    return last_change


def run_rule(
    rule_class,
    declaration: Declaration,
    seed: int,
    width: int,
    height: int,
    max_ticks: int,
    tick_timeout_seconds: float,
    on_tick=None,
) -> RunResult:
    """Execute one run to completion, in this process.

    Production runs go through contract.child so a runaway rule cannot
    take the server down (REQ-7.6.1); the loop itself is identical.
    `on_tick` receives each TickRecord as it is produced — that is how
    the child streams progress to its parent.
    """
    dice = Dice(seed, height, width)
    rule = rule_class(dice)
    cells = start_grid(rule, declaration, width, height, dice)

    record = _record(cells, declaration, 0, dice, previous=None)
    ticks = [record]
    if on_tick:
        on_tick(record)
    # Fingerprint -> tick map: the entire exact-loop detector (REQ-9.9).
    # Tick 0 participates (REQ-4.6.3).
    seen = {record.state_fingerprint: 0}

    stopped_because = None
    loop_length = None
    for tick in range(1, max_ticks + 1):
        started = time.perf_counter()
        cells = apply_tick(rule, declaration, cells, tick, dice)
        elapsed = time.perf_counter() - started

        record = _record(cells, declaration, tick, dice, previous=ticks[-1])
        ticks.append(record)
        if on_tick:
            on_tick(record)

        # Stopping conditions in spec precedence (REQ-9.8).
        fingerprint = record.state_fingerprint
        if fingerprint == ticks[-2].state_fingerprint:
            stopped_because = "frozen"
        elif fingerprint in seen:
            stopped_because = "looping"
            loop_length = tick - seen[fingerprint]
        elif tick == max_ticks:
            stopped_because = "ran_out"
        elif elapsed > tick_timeout_seconds:
            stopped_because = "too_slow"
        if stopped_because:
            break
        seen[fingerprint] = tick

    return assemble_result(ticks, stopped_because, loop_length)
