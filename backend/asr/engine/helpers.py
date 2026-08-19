"""Spatial helpers, bound to one rule's declaration (REQ-6.2.1).

`bind_helpers(neighbors, reach)` bakes the declared neighborhood into
every helper before rule code ever sees them, so a rule can never look
or reach farther than its declaration — and its coverage entry — claims.
There is no unbound shift anywhere (REQ-6.2.3).

Generated code never implements neighbor lookup or edge wrapping itself
(REQ-6.1). Every helper wraps around the grid edges.
"""

import numpy as np

from .geometry import (
    HEADING_NAMES,
    HEADING_OFFSETS,
    allowed_move_headings,
    neighbor_offsets,
)


def bind_helpers(neighbors: str, reach: int) -> dict:
    """Build the helper functions for one declaration. Returns a dict
    of {name: function} ready to drop into a rule's namespace.
    """
    offsets = neighbor_offsets(neighbors, reach)
    offset_set = set(offsets)
    move_headings = allowed_move_headings(neighbors)

    def _property_array(cells, prop):
        if not isinstance(prop, str):
            raise ValueError("prop must be a property name like 'kind'")
        if not cells._has(prop):
            raise ValueError(f"this grid has no property named {prop!r}")
        return cells._arrays[prop]

    def _weight(cells):
        # When `weight` is in scope each neighbor contributes its own
        # weight instead of 1 — the only thing weight does (REQ-5.4.1).
        # Rules do not opt in.
        return cells._arrays["weight"] if cells._has("weight") else 1

    def _tally(cells, counts_as):
        # Each neighbor's contribution lands on the cell it neighbors.
        # A cell is never its own neighbor: (0, 0) is not an offset.
        total = np.zeros(cells._shape(), dtype=np.int32)
        for down, right in offsets:
            total += np.roll(counts_as, (-down, -right), axis=(0, 1))
        return total

    def look(cells, prop, down, right):
        """One property array as seen from an offset neighbor, wrapping.

        (down, right) must be inside the declared neighborhood
        (REQ-6.3) — anything else raises. Positive `down` brings the
        UPSTAIRS neighbor's value into this cell's position.
        """
        if (down, right) not in offset_set:
            raise ValueError(
                f"offset ({down}, {right}) is outside the declared "
                f"neighborhood {neighbors} at reach {reach} (REQ-6.2.1)"
            )
        return np.roll(_property_array(cells, prop), (down, right), axis=(0, 1))

    def move(cells, prop, direction):
        """One property array displaced exactly one cell in `direction`.

        `direction` is a HEADING constant, and must be one the declared
        NEIGHBORS permits — plus_4 rules cannot move diagonally
        (REQ-6.3.3). Displacement is always one cell regardless of
        REACH, so movement never inflates the declared reach (REQ-6.2.3).
        """
        if not isinstance(direction, int) or not 0 <= direction < len(HEADING_NAMES):
            raise ValueError("direction must be a HEADING constant, like HEADING.e")
        name = HEADING_NAMES[direction]
        if name not in move_headings:
            raise ValueError(
                f"move toward {name!r} is not allowed under {neighbors}; "
                f"the choices are {move_headings} (REQ-6.3.3)"
            )
        return np.roll(_property_array(cells, prop), HEADING_OFFSETS[name], axis=(0, 1))

    def count_neighbors(cells, prop, value):
        """How many of each cell's neighbors have `prop` equal to `value`.

        Neighborhood shape and reach come from the declaration, not from
        arguments, so a rule cannot widen its reach at the call site.
        """
        match = _property_array(cells, prop) == value
        return _tally(cells, match.astype(np.int32) * _weight(cells))

    def count_neighbors_where(cells, mask):
        """Same, over an arbitrary boolean array — "neighbors with energy
        above 5". Same automatic weighting and self-exclusion.
        """
        if not isinstance(mask, np.ndarray) or mask.dtype != np.bool_:
            raise ValueError("mask must be a boolean numpy array")
        if mask.shape != cells._shape():
            raise ValueError(f"mask must be shaped like the grid {cells._shape()}")
        return _tally(cells, mask.astype(np.int32) * _weight(cells))

    def sum_neighbors(cells, prop):
        """Total of each cell's neighbors' values for `prop`. Same
        weighting and self-exclusion as count_neighbors.
        """
        values = _property_array(cells, prop).astype(np.int32)
        return _tally(cells, values * _weight(cells))

    return {
        "look": look,
        "move": move,
        "count_neighbors": count_neighbors,
        "count_neighbors_where": count_neighbors_where,
        "sum_neighbors": sum_neighbors,
    }
