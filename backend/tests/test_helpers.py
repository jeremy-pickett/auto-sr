"""Bound spatial helpers (spec sections 6.1-6.3)."""

import numpy as np
import pytest

from asr.engine.cells import make_cells
from asr.engine.geometry import HEADING
from asr.engine.helpers import bind_helpers


def grid_3x3():
    return make_cells(np.arange(9, dtype=np.uint8).reshape(3, 3))


# ---- look ----------------------------------------------------------------


def test_look_brings_the_upstairs_value_down_with_positive_down():
    # Spec sentence, verbatim: positive `down` brings the UPSTAIRS
    # neighbor's value into this cell's position.
    helpers = bind_helpers("all_8", 1)
    seen = helpers["look"](grid_3x3(), "kind", 1, 0)
    kind = grid_3x3().kind
    assert seen[1, 1] == kind[0, 1]
    assert np.array_equal(seen, np.roll(kind, (1, 0), axis=(0, 1)))


def test_look_wraps_around_the_edges():
    helpers = bind_helpers("all_8", 1)
    seen = helpers["look"](grid_3x3(), "kind", 1, 0)
    # Row 0 now sees what the bottom row held (wrap, top to bottom).
    assert seen[0].tolist() == [6, 7, 8]


def test_look_rejects_offsets_outside_the_declaration():
    helpers = bind_helpers("all_8", 1)
    with pytest.raises(ValueError):
        helpers["look"](grid_3x3(), "kind", 0, 2)  # beyond reach 1
    with pytest.raises(ValueError):
        helpers["look"](grid_3x3(), "kind", 0, 0)  # self is not a neighbor
    plus = bind_helpers("plus_4", 1)
    with pytest.raises(ValueError):
        plus["look"](grid_3x3(), "kind", 1, 1)  # diagonal under plus_4


def test_look_rejects_unknown_properties():
    helpers = bind_helpers("all_8", 1)
    with pytest.raises(ValueError):
        helpers["look"](grid_3x3(), "energy", 1, 0)


# ---- move ----------------------------------------------------------------


def test_move_displaces_exactly_one_cell_with_wrap():
    helpers = bind_helpers("plus_4", 3)
    kind = np.zeros((3, 3), dtype=np.uint8)
    kind[1, 2] = 5
    moved = helpers["move"](make_cells(kind), "kind", HEADING.e)
    assert moved[1, 0] == 5  # wrapped from the right edge
    assert moved.sum() == 5  # nothing duplicated, nothing lost


def test_move_is_one_cell_even_at_high_reach():
    # REQ-6.2.3: displacement never inflates the declared reach.
    helpers = bind_helpers("plus_4", 3)
    kind = np.zeros((5, 5), dtype=np.uint8)
    kind[2, 2] = 1
    moved = helpers["move"](make_cells(kind), "kind", HEADING.s)
    assert moved[3, 2] == 1


def test_move_rejects_diagonals_under_plus_4():
    helpers = bind_helpers("plus_4", 1)
    with pytest.raises(ValueError):
        helpers["move"](grid_3x3(), "kind", HEADING.ne)


def test_move_allows_diagonals_under_all_8():
    helpers = bind_helpers("all_8", 1)
    kind = np.zeros((3, 3), dtype=np.uint8)
    kind[1, 1] = 9
    moved = helpers["move"](make_cells(kind), "kind", HEADING.ne)
    assert moved[0, 2] == 9


def test_move_rejects_non_heading_directions():
    helpers = bind_helpers("all_8", 1)
    with pytest.raises(ValueError):
        helpers["move"](grid_3x3(), "kind", "east")
    with pytest.raises(ValueError):
        helpers["move"](grid_3x3(), "kind", HEADING.none)


# ---- neighbor tallies -----------------------------------------------------


def test_count_neighbors_on_a_known_pattern():
    helpers = bind_helpers("all_8", 1)
    kind = np.zeros((5, 5), dtype=np.uint8)
    kind[2, 1] = 1
    kind[2, 3] = 1
    counts = helpers["count_neighbors"](make_cells(kind), "kind", 1)
    assert counts[2, 2] == 2  # between the two live cells
    assert counts[1, 1] == 1  # touches only the left live cell
    assert counts[2, 1] == 0  # the other live cell is beyond reach 1
    assert counts.dtype == np.int32


def test_count_neighbors_excludes_self():
    helpers = bind_helpers("all_8", 1)
    kind = np.zeros((5, 5), dtype=np.uint8)
    kind[2, 2] = 1
    counts = helpers["count_neighbors"](make_cells(kind), "kind", 1)
    assert counts[2, 2] == 0


def test_count_neighbors_wraps():
    helpers = bind_helpers("all_8", 1)
    kind = np.ones((3, 3), dtype=np.uint8)
    counts = helpers["count_neighbors"](make_cells(kind), "kind", 1)
    assert (counts == 8).all()


def test_weight_substitutes_for_one_in_every_tally():
    # REQ-5.4.1: each neighbor contributes its weight instead of 1, and
    # rules do not opt in.
    helpers = bind_helpers("all_8", 1)
    kind = np.zeros((5, 5), dtype=np.uint8)
    kind[2, 1] = 1
    cells = make_cells(kind)
    weight = np.ones((5, 5), dtype=np.uint8)
    weight[2, 1] = 3
    cells._set("weight", weight)
    counts = helpers["count_neighbors"](cells, "kind", 1)
    assert counts[2, 2] == 3


def test_weight_at_its_identity_default_changes_nothing():
    # REQ-5.1 in miniature: weight all ones is bit-identical to absent.
    helpers = bind_helpers("all_8", 1)
    kind = (np.arange(25, dtype=np.uint8) % 2).reshape(5, 5)
    bare = make_cells(kind.copy())
    weighted = make_cells(kind.copy())
    weighted._set("weight", np.ones((5, 5), dtype=np.uint8))
    assert np.array_equal(
        helpers["count_neighbors"](bare, "kind", 1),
        helpers["count_neighbors"](weighted, "kind", 1),
    )


def test_count_neighbors_where_takes_a_computed_condition():
    helpers = bind_helpers("plus_4", 1)
    energy = np.zeros((5, 5), dtype=np.uint8)
    energy[2, 1] = 9
    cells = make_cells(np.zeros((5, 5), dtype=np.uint8), energy=energy)
    counts = helpers["count_neighbors_where"](cells, cells.energy > 5)
    assert counts[2, 2] == 1
    assert counts[2, 0] == 1
    with pytest.raises(ValueError):
        helpers["count_neighbors_where"](cells, energy)  # not boolean


def test_sum_neighbors_does_not_overflow_uint8():
    helpers = bind_helpers("all_8", 1)
    energy = np.full((3, 3), 200, dtype=np.uint8)
    cells = make_cells(np.zeros((3, 3), dtype=np.uint8), energy=energy)
    totals = helpers["sum_neighbors"](cells, "energy")
    assert (totals == 1600).all()  # 8 neighbors x 200, wrapped grid


def test_plus_4_reach_2_sees_the_second_ring_on_the_rays():
    helpers = bind_helpers("plus_4", 2)
    kind = np.zeros((7, 7), dtype=np.uint8)
    kind[3, 1] = 1  # two to the left of center: on the ray at reach 2
    counts = helpers["count_neighbors"](make_cells(kind), "kind", 1)
    assert counts[3, 3] == 1
