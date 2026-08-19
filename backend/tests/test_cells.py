"""The Cells container contract (spec section 6.2)."""

import numpy as np
import pytest

from asr.engine.cells import Cells, make_cells, merge_cells


def small_kind():
    return np.arange(9, dtype=np.uint8).reshape(3, 3)


def test_cells_has_no_public_constructor():
    with pytest.raises(TypeError):
        Cells()


def test_make_cells_exposes_properties_as_attributes():
    energy = np.full((3, 3), 7, dtype=np.uint8)
    cells = make_cells(small_kind(), energy=energy)
    assert cells.kind[1, 1] == 4
    assert cells.energy[0, 0] == 7
    assert cells._rule_owned == ("kind", "energy")


def test_rule_code_cannot_assign_a_property():
    cells = make_cells(small_kind())
    with pytest.raises(AttributeError):
        cells.kind = np.zeros((3, 3), dtype=np.uint8)


def test_unknown_property_read_is_a_clear_error():
    cells = make_cells(small_kind())
    with pytest.raises(AttributeError):
        _ = cells.energy


def test_make_cells_rejects_bad_input():
    with pytest.raises(ValueError):
        make_cells(np.zeros((3, 3), dtype=np.int32))  # wrong dtype
    with pytest.raises(ValueError):
        make_cells(np.zeros(9, dtype=np.uint8))  # not 2-D
    with pytest.raises(ValueError):
        make_cells(small_kind(), mood=np.zeros((3, 3), dtype=np.uint8))  # not core
    with pytest.raises(ValueError):
        make_cells(small_kind(), energy=np.zeros((2, 2), dtype=np.uint8))  # shape
    with pytest.raises(ValueError):
        make_cells(small_kind(), energy=np.zeros((3, 3), dtype=np.int32))  # dtype


def test_merge_selects_field_by_field():
    a = make_cells(np.ones((2, 2), dtype=np.uint8),
                   energy=np.full((2, 2), 10, dtype=np.uint8))
    b = make_cells(np.zeros((2, 2), dtype=np.uint8),
                   energy=np.full((2, 2), 20, dtype=np.uint8))
    mask = np.array([[True, False], [False, True]])
    merged = merge_cells(mask, a, b)
    assert merged.kind.tolist() == [[1, 0], [0, 1]]
    assert merged.energy.tolist() == [[10, 20], [20, 10]]
    assert merged.kind.dtype == np.uint8


def test_merge_carries_harness_arrays_from_the_true_side_untouched():
    # The rate gate merges a proposal against the previous grid; the
    # proposal already carries modifier arrays forward (REQ-6.2).
    a = make_cells(np.ones((2, 2), dtype=np.uint8))
    b = make_cells(np.zeros((2, 2), dtype=np.uint8))
    weight = np.full((2, 2), 3, dtype=np.uint8)
    a._set("weight", weight)
    merged = merge_cells(np.array([[True, False], [False, True]]), a, b)
    assert merged.weight is weight


def test_merge_rejects_grids_owning_different_properties():
    a = make_cells(np.ones((2, 2), dtype=np.uint8),
                   energy=np.zeros((2, 2), dtype=np.uint8))
    b = make_cells(np.zeros((2, 2), dtype=np.uint8))
    with pytest.raises(ValueError):
        merge_cells(np.ones((2, 2), dtype=bool), a, b)
