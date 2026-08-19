"""Neighborhood geometry (spec section 6.3)."""

import pytest

from asr.engine.geometry import (
    HEADING,
    HEADING_NAMES,
    allowed_move_headings,
    neighbor_offsets,
)


def test_all_8_counts_match_the_spec_table():
    # REQ-6.3.1: 8, 24, 48 neighbors for reach 1, 2, 3.
    assert len(neighbor_offsets("all_8", 1)) == 8
    assert len(neighbor_offsets("all_8", 2)) == 24
    assert len(neighbor_offsets("all_8", 3)) == 48


def test_plus_4_counts_match_the_spec_table():
    # REQ-6.3.2: 4, 8, 12 neighbors for reach 1, 2, 3.
    assert len(neighbor_offsets("plus_4", 1)) == 4
    assert len(neighbor_offsets("plus_4", 2)) == 8
    assert len(neighbor_offsets("plus_4", 3)) == 12


def test_a_cell_is_never_its_own_neighbor():
    for neighbors in ("all_8", "plus_4"):
        for reach in (1, 2, 3):
            assert (0, 0) not in neighbor_offsets(neighbors, reach)


def test_plus_4_is_rays_not_a_diamond():
    offsets = set(neighbor_offsets("plus_4", 2))
    assert (0, 2) in offsets and (-2, 0) in offsets
    # The diamond would include these; the rays must not (REQ-6.3.2).
    assert (1, 1) not in offsets and (-1, 1) not in offsets


def test_all_8_reaches_the_square_corners():
    assert (2, 2) in set(neighbor_offsets("all_8", 2))


def test_offset_sets_are_symmetric():
    # The neighbor tally rolls in either direction interchangeably only
    # because every offset's mirror is also an offset.
    for neighbors in ("all_8", "plus_4"):
        for reach in (1, 2, 3):
            offsets = set(neighbor_offsets(neighbors, reach))
            assert {(-d, -r) for d, r in offsets} == offsets


def test_bad_declarations_are_rejected():
    with pytest.raises(ValueError):
        neighbor_offsets("hex_6", 1)
    with pytest.raises(ValueError):
        neighbor_offsets("all_8", 0)
    with pytest.raises(ValueError):
        neighbor_offsets("all_8", 4)


def test_move_headings_per_neighborhood():
    # REQ-6.3.3.
    assert allowed_move_headings("plus_4") == ("n", "e", "s", "w")
    assert allowed_move_headings("all_8") == ("n", "ne", "e", "se", "s", "sw", "w", "nw")


def test_heading_constants_line_up_with_names():
    for index, name in enumerate(HEADING_NAMES):
        assert getattr(HEADING, name) == index
