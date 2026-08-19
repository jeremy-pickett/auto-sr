"""Computational and pattern fingerprints (spec section 9.7)."""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.declaration import Declaration
from asr.engine.dice import Dice
from asr.engine.fingerprint import computational_fingerprint, pattern_fingerprint

SIZE = 4


def declaration(**overrides):
    base = dict(kinds=2, neighbors="all_8", reach=1)
    base.update(overrides)
    return Declaration(**base)


def grid(kind_value=0, **extra):
    kind = np.full((SIZE, SIZE), kind_value, dtype=np.uint8)
    cells = make_cells(kind)
    cells._set("age", np.zeros((SIZE, SIZE), dtype=np.uint16))
    cells._set("changed_last_tick", np.zeros((SIZE, SIZE), dtype=bool))
    for name, array in extra.items():
        cells._set(name, array)
    return cells


def dice():
    return Dice(seed=5, height=SIZE, width=SIZE)


def test_identical_state_hashes_identically():
    decl = declaration()
    assert computational_fingerprint(
        grid(), decl, 3, dice()
    ) == computational_fingerprint(grid(), decl, 3, dice())


def test_a_kind_difference_changes_both_fingerprints():
    decl = declaration()
    a, b = grid(0), grid(1)
    assert computational_fingerprint(a, decl, 1, dice()) != computational_fingerprint(
        b, decl, 1, dice()
    )
    assert pattern_fingerprint(a) != pattern_fingerprint(b)


def test_pattern_fingerprint_sees_kind_only():
    # Hidden state (memory) changes the computational fingerprint but
    # never the pattern one — the heart of REQ-9.8.1's refusal to stop.
    decl = declaration(uses=("memory",))
    quiet = make_cells(
        np.zeros((SIZE, SIZE), dtype=np.uint8),
        memory=np.zeros((SIZE, SIZE), dtype=np.uint8),
    )
    counting = make_cells(
        np.zeros((SIZE, SIZE), dtype=np.uint8),
        memory=np.full((SIZE, SIZE), 7, dtype=np.uint8),
    )
    assert pattern_fingerprint(quiet) == pattern_fingerprint(counting)
    assert computational_fingerprint(
        quiet, decl, 1, dice()
    ) != computational_fingerprint(counting, decl, 1, dice())


def test_hash_ignores_allocation_order():
    # REQ-9.7.4: arrays are hashed in name-sorted order.
    decl = declaration(uses=("energy", "memory"))
    energy = np.full((SIZE, SIZE), 3, dtype=np.uint8)
    memory = np.full((SIZE, SIZE), 9, dtype=np.uint8)
    kind = np.zeros((SIZE, SIZE), dtype=np.uint8)
    first = make_cells(kind, energy=energy, memory=memory)
    second = make_cells(kind, memory=memory, energy=energy)
    assert computational_fingerprint(
        first, decl, 1, dice()
    ) == computational_fingerprint(second, decl, 1, dice())


def test_scheduler_phase_matters_only_when_rate_is_in_scope():
    with_rate = declaration(modifiers=("rate",))
    without = declaration()
    rated = grid(rate=np.full((SIZE, SIZE), 2, dtype=np.uint8))
    # Same grid, different point in the rate cycle: different futures.
    assert computational_fingerprint(
        rated, with_rate, 1, dice()
    ) != computational_fingerprint(rated, with_rate, 2, dice())
    # Cycle repeats every 12 ticks.
    assert computational_fingerprint(
        rated, with_rate, 1, dice()
    ) == computational_fingerprint(rated, with_rate, 13, dice())
    # No rate in scope: the tick number is irrelevant.
    assert computational_fingerprint(
        grid(), without, 1, dice()
    ) == computational_fingerprint(grid(), without, 2, dice())


def test_age_clamp_under_stubbornness():
    # REQ-9.7.6: with stubbornness in scope and age unread, ages above 3
    # are indistinguishable — that is what lets such a rule freeze.
    decl = declaration(modifiers=("stubbornness",))
    stub = np.zeros((SIZE, SIZE), dtype=np.uint8)
    young = grid(stubbornness=stub)
    young._set("age", np.full((SIZE, SIZE), 5, dtype=np.uint16))
    old = grid(stubbornness=stub)
    old._set("age", np.full((SIZE, SIZE), 500, dtype=np.uint16))
    assert computational_fingerprint(
        young, decl, 1, dice()
    ) == computational_fingerprint(old, decl, 1, dice())
    # But ages at or below the clamp still distinguish states.
    fresh = grid(stubbornness=stub)
    fresh._set("age", np.full((SIZE, SIZE), 2, dtype=np.uint16))
    assert computational_fingerprint(
        fresh, decl, 1, dice()
    ) != computational_fingerprint(old, decl, 1, dice())


def test_age_at_full_precision_when_the_rule_reads_it():
    decl = declaration(reads=("age",))
    young = grid()
    young._set("age", np.full((SIZE, SIZE), 5, dtype=np.uint16))
    old = grid()
    old._set("age", np.full((SIZE, SIZE), 500, dtype=np.uint16))
    assert computational_fingerprint(
        young, decl, 1, dice()
    ) != computational_fingerprint(old, decl, 1, dice())


def test_changed_last_tick_enters_only_when_read():
    reading = declaration(reads=("changed_last_tick",))
    ignoring = declaration()
    calm = grid()
    churned = grid()
    churned._set("changed_last_tick", np.ones((SIZE, SIZE), dtype=bool))
    assert computational_fingerprint(
        calm, reading, 1, dice()
    ) != computational_fingerprint(churned, reading, 1, dice())
    assert computational_fingerprint(
        calm, ignoring, 1, dice()
    ) == computational_fingerprint(churned, ignoring, 1, dice())


def test_rng_state_enters_only_when_birth_draws_are_declared():
    drawing = declaration(
        modifiers=("weight",), assign={"weight": {"value": 2, "chance": 0.5}}
    )
    silent = declaration(modifiers=("weight",))
    ones = np.ones((SIZE, SIZE), dtype=np.uint8)
    consumed = dice()
    consumed.chance(0.5)  # advance the generator
    a = grid(weight=ones)
    b = grid(weight=ones)
    assert computational_fingerprint(
        a, drawing, 1, dice()
    ) != computational_fingerprint(b, drawing, 1, consumed)
    consumed_again = dice()
    consumed_again.chance(0.5)
    assert computational_fingerprint(
        a, silent, 1, dice()
    ) == computational_fingerprint(b, silent, 1, consumed_again)
