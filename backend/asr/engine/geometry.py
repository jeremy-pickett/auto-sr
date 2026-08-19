"""Neighborhood shapes, reach, and headings (spec section 6.3).

Grid edges always wrap: top to bottom, left to right. (Standard term:
toroidal.) An offset is a pair (down, right): rows toward the bottom of
the screen and columns toward the right.
"""

HEADING_NAMES = ("n", "ne", "e", "se", "s", "sw", "w", "nw", "none")

# Where each heading points, as (down, right). Row 0 is the top of the
# grid, so "n" points up, which is negative down.
HEADING_OFFSETS = {
    "n": (-1, 0),
    "ne": (-1, 1),
    "e": (0, 1),
    "se": (1, 1),
    "s": (1, 0),
    "sw": (1, -1),
    "w": (0, -1),
    "nw": (-1, -1),
}


class HEADING:
    """Named constants for the heading property, stored as uint8
    (REQ-5.2.1: enums are named constants, never strings, in rule code).
    """

    n = 0
    ne = 1
    e = 2
    se = 3
    s = 4
    sw = 5
    w = 6
    nw = 7
    none = 8


NEIGHBORHOOD_NAMES = ("all_8", "plus_4")
REACH_RANGE = (1, 3)


def check_geometry(neighbors: str, reach: int) -> None:
    """Reject a neighborhood declaration outside the contract."""
    if neighbors not in NEIGHBORHOOD_NAMES:
        raise ValueError(
            f"NEIGHBORS must be one of {NEIGHBORHOOD_NAMES}, got {neighbors!r}"
        )
    low, high = REACH_RANGE
    if not isinstance(reach, int) or not low <= reach <= high:
        raise ValueError(f"REACH must be an integer from {low} to {high}, got {reach!r}")


def neighbor_offsets(neighbors: str, reach: int) -> tuple[tuple[int, int], ...]:
    """Every (down, right) offset that counts as a neighbor (REQ-6.3).

    all_8 at reach r is the whole surrounding square, (2r+1)**2 - 1 cells
    (standard term: Chebyshev distance <= r), never the cell itself.
    plus_4 at reach r is the four straight rays up, down, left, right --
    4r cells, deliberately NOT the diamond (REQ-6.3.2), so "plus_4" keeps
    its plus-sign meaning at every reach.
    """
    check_geometry(neighbors, reach)
    offsets: list[tuple[int, int]] = []
    if neighbors == "all_8":
        for down in range(-reach, reach + 1):
            for right in range(-reach, reach + 1):
                if (down, right) != (0, 0):
                    offsets.append((down, right))
    else:
        for step in range(1, reach + 1):
            offsets.extend([(-step, 0), (step, 0), (0, -step), (0, step)])
    return tuple(offsets)


def allowed_move_headings(neighbors: str) -> tuple[str, ...]:
    """Which headings `move` accepts (REQ-6.3.3): the four straight ones
    for plus_4, all eight for all_8. Reach never matters -- move always
    displaces by exactly one cell (REQ-6.2.3).
    """
    if neighbors == "plus_4":
        return ("n", "e", "s", "w")
    if neighbors == "all_8":
        return ("n", "ne", "e", "se", "s", "sw", "w", "nw")
    raise ValueError(f"NEIGHBORS must be one of {NEIGHBORHOOD_NAMES}, got {neighbors!r}")
