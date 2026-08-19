"""Tick-0 initialization (spec section 4.6) and the tick order (6.4)."""

import numpy as np

from asr.engine.cells import make_cells
from asr.engine.declaration import Declaration
from asr.engine.dice import Dice
from asr.engine.tick import apply_tick, start_grid

SIZE = 6


def declaration(**overrides):
    base = dict(kinds=2, neighbors="all_8", reach=1)
    base.update(overrides)
    return Declaration(**base)


class FlipEveryTick:
    """Every cell alternates kind 0 and 1 — a maximal churn rule."""

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        return make_cells((1 - cells.kind).astype(np.uint8))


class NeverChanges:
    """A completely static rule."""

    def __init__(self, dice):
        self.dice = dice

    def make_start(self, width, height):
        return make_cells(np.zeros((height, width), dtype=np.uint8))

    def step(self, cells):
        return make_cells(cells.kind.copy())


def fresh(rule_class, decl):
    dice = Dice(seed=11, height=SIZE, width=SIZE)
    rule = rule_class(dice)
    return rule, dice, start_grid(rule, decl, SIZE, SIZE, dice)


# ---- tick 0 ----------------------------------------------------------------


def test_tick_zero_is_unaged_and_unchanged():
    # REQ-4.6.2: even with birth assignments applied at tick 0.
    decl = declaration(
        modifiers=("weight",),
        assign={"weight": {"value": 4, "chance": 1.0}},
    )
    _, _, cells = fresh(NeverChanges, decl)
    assert (cells.age == 0).all()
    assert not cells.changed_last_tick.any()


def test_in_scope_modifiers_start_at_identity():
    decl = declaration(modifiers=("stubbornness",))
    _, _, cells = fresh(NeverChanges, decl)
    assert (cells.stubbornness == 0).all()
    assert cells.stubbornness.dtype == np.uint8


def test_birth_assignments_treat_every_starting_cell_as_born():
    # REQ-4.6 step 4: weight is birth-assigned, chance 1.0 covers all.
    decl = declaration(
        modifiers=("weight",),
        assign={"weight": {"value": 3, "chance": 1.0}},
    )
    _, _, cells = fresh(NeverChanges, decl)
    assert (cells.weight == 3).all()


def test_semantic_slot_allocated_and_assigned_at_start():
    decl = declaration(
        semantic_slots={
            "mood": {
                "values": ["none", "restless"],
                "assign_when": "birth",
                "assign": {"value": "restless", "chance": 1.0},
            }
        },
    )
    _, _, cells = fresh(NeverChanges, decl)
    assert (cells.mood == 1).all()  # index of "restless"


# ---- advancing ticks --------------------------------------------------------


def test_a_change_resets_age_and_sets_the_birth_flag():
    decl = declaration()
    rule, dice, cells = fresh(FlipEveryTick, decl)
    after = apply_tick(rule, decl, cells, tick=1, dice=dice)
    assert (after.kind == 1).all()
    assert after.changed_last_tick.all()
    assert (after.age == 0).all()


def test_no_change_ages_every_cell():
    decl = declaration()
    rule, dice, cells = fresh(NeverChanges, decl)
    for tick in (1, 2, 3):
        cells = apply_tick(rule, decl, cells, tick, dice)
    assert (cells.age == 3).all()
    assert not cells.changed_last_tick.any()


def test_rate_gate_discards_the_whole_proposal_on_off_ticks():
    # All cells at rate 2: flips land only on even ticks, and gated
    # ticks do not count as changes (REQ-6.4 step 2).
    decl = declaration(
        modifiers=("rate",),
        assign={"rate": {"value": 2, "chance": 1.0}},
    )
    rule, dice, cells = fresh(FlipEveryTick, decl)
    tick1 = apply_tick(rule, decl, cells, 1, dice)
    assert (tick1.kind == 0).all()  # not scheduled
    assert not tick1.changed_last_tick.any()
    assert (tick1.age == 1).all()  # skipped cells still age (REQ-4.3.1)
    tick2 = apply_tick(rule, decl, tick1, 2, dice)
    assert (tick2.kind == 1).all()  # scheduled, flip applies


def test_stubbornness_refuses_changes_until_age_catches_up():
    decl = declaration(
        modifiers=("stubbornness",),
        assign={"stubbornness": {"value": 3, "chance": 1.0}},
    )
    rule, dice, cells = fresh(FlipEveryTick, decl)
    assert (cells.stubbornness == 3).all()
    for tick in (1, 2, 3):  # pre-tick ages 0, 1, 2: all refused
        cells = apply_tick(rule, decl, cells, tick, dice)
        assert (cells.kind == 0).all()
    cells = apply_tick(rule, decl, cells, 4, dice)  # pre-tick age 3
    assert (cells.kind == 1).all()
    assert (cells.age == 0).all()


def test_stubbornness_at_identity_is_bit_identical_to_absent():
    # REQ-15.2 in miniature for the engine layer.
    bare_decl = declaration()
    stub_decl = declaration(modifiers=("stubbornness",))
    bare_rule, bare_dice, bare = fresh(FlipEveryTick, bare_decl)
    stub_rule, stub_dice, stub = fresh(FlipEveryTick, stub_decl)
    for tick in range(1, 6):
        bare = apply_tick(bare_rule, bare_decl, bare, tick, bare_dice)
        stub = apply_tick(stub_rule, stub_decl, stub, tick, stub_dice)
    assert bare.kind.tobytes() == stub.kind.tobytes()
    assert bare.age.tobytes() == stub.age.tobytes()


def test_no_births_means_no_draw_at_all():
    # REQ-5.6.2: a static grid must not advance the RNG even when birth
    # assignments are declared.
    decl = declaration(
        modifiers=("weight",),
        assign={"weight": {"value": 2, "chance": 0.5}},
    )
    rule, dice, cells = fresh(NeverChanges, decl)
    before = dice._state_bytes()
    for tick in (1, 2, 3):
        cells = apply_tick(rule, decl, cells, tick, dice)
    assert dice._state_bytes() == before


def test_births_redraw_only_the_born_cells():
    decl = declaration(
        modifiers=("weight",),
        assign={"weight": {"value": 4, "chance": 1.0}},
    )

    class FlipOneCell:
        def __init__(self, dice):
            self.dice = dice

        def make_start(self, width, height):
            return make_cells(np.zeros((height, width), dtype=np.uint8))

        def step(self, cells):
            kind = cells.kind.copy()
            kind[0, 0] = 1 - kind[0, 0]
            return make_cells(kind)

    rule, dice, cells = fresh(FlipOneCell, decl)
    # Tick 0 set everyone's weight to 4; hand-reset it to identity so
    # the redraw is visible.
    cells._set("weight", np.ones((SIZE, SIZE), dtype=np.uint8))
    after = apply_tick(rule, decl, cells, 1, dice)
    assert after.weight[0, 0] == 4  # reborn cell redrawn
    assert after.weight[1, 1] == 1  # everyone else untouched


def test_harness_arrays_carry_forward_through_the_proposal():
    decl = declaration(
        modifiers=("weight",),
        assign={"weight": {"value": 2, "chance": 1.0}},
    )
    rule, dice, cells = fresh(NeverChanges, decl)
    after = apply_tick(rule, decl, cells, 1, dice)
    assert after._has("weight")
    assert np.array_equal(after.weight, cells.weight)
