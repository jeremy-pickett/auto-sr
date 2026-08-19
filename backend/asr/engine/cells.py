"""The grid container (spec section 6.2).

A grid is a set of named numpy arrays that all share one shape — one
array per property, never an array of cell objects (REQ-4.1). `Cells`
is a named bag of those arrays: no arithmetic, no broadcasting, no
public constructor. Generated code builds one only through
`make_cells`; the harness attaches everything else (modifier, slot,
and derived arrays) afterward.
"""

import numpy as np

# Optional properties a rule may own, besides the required `kind`
# (spec section 4.2). heading stores HEADING constants as uint8.
OPTIONAL_CORE_PROPERTIES = {
    "energy": np.uint8,
    "heading": np.uint8,
    "memory": np.uint8,
}

# Properties the harness owns and recomputes every tick (section 4.3).
DERIVED_PROPERTIES = {
    "age": np.uint16,
    "changed_last_tick": np.bool_,
}


class Cells:
    """A named bag of same-shaped arrays. Read a property as an
    attribute: cells.kind, cells.energy. Rule code can never assign
    one (REQ-4.5); the harness writes through the private _set.
    """

    __slots__ = ("_arrays", "_rule_owned")

    def __init__(self, *_args, **_kwargs):
        raise TypeError(
            "Cells has no public constructor; build a grid with make_cells (REQ-6.2)"
        )

    @classmethod
    def _assemble(cls, arrays: dict, rule_owned: tuple) -> "Cells":
        cells = object.__new__(cls)
        object.__setattr__(cells, "_arrays", dict(arrays))
        object.__setattr__(cells, "_rule_owned", tuple(rule_owned))
        return cells

    def __getattr__(self, name):
        try:
            return self._arrays[name]
        except KeyError:
            raise AttributeError(
                f"this grid has no property named {name!r}"
            ) from None

    def __setattr__(self, name, _value):
        raise AttributeError(
            f"cell property arrays are read-only to rule code; "
            f"cannot assign {name!r} (REQ-4.5)"
        )

    # ---- harness-private surface below; rule code is statically
    # ---- forbidden from touching underscore names.

    def _set(self, name, array) -> None:
        self._arrays[name] = array

    def _has(self, name) -> bool:
        return name in self._arrays

    def _names(self) -> tuple:
        return tuple(self._arrays)

    def _shape(self) -> tuple:
        return self._arrays["kind"].shape


def make_cells(kind, **core_properties) -> Cells:
    """Build a grid from rule-owned arrays. The only way generated code
    creates a Cells (REQ-6.2).

    `kind` is required and must be a 2-D uint8 array. Each keyword must
    be one of the optional core properties (energy, heading, memory)
    with matching shape and dtype. Modifier, slot, and derived arrays
    are never passed here — the harness allocates those (REQ-4.6) and
    the rule cannot write them (REQ-4.5).
    """
    if not isinstance(kind, np.ndarray) or kind.ndim != 2:
        raise ValueError("kind must be a 2-D numpy array")
    if kind.dtype != np.uint8:
        raise ValueError(f"kind must have dtype uint8, got {kind.dtype}")

    arrays = {"kind": kind}
    for name, array in core_properties.items():
        wanted_dtype = OPTIONAL_CORE_PROPERTIES.get(name)
        if wanted_dtype is None:
            raise ValueError(
                f"{name!r} is not a core property; the choices are "
                f"{tuple(OPTIONAL_CORE_PROPERTIES)}"
            )
        if not isinstance(array, np.ndarray) or array.shape != kind.shape:
            raise ValueError(f"{name} must be a numpy array shaped like kind {kind.shape}")
        if array.dtype != wanted_dtype:
            raise ValueError(f"{name} must have dtype {np.dtype(wanted_dtype)}, got {array.dtype}")
        arrays[name] = array

    return Cells._assemble(arrays, tuple(arrays))


def merge_cells(mask, chosen_where_true: Cells, chosen_where_false: Cells) -> Cells:
    """HARNESS-PRIVATE field-by-field select across rule-owned arrays.

    Used by the rate gate (REQ-6.4 step 2): where mask is False the
    proposal is discarded outright, not blended. Cells is not an
    ndarray, so np.where cannot apply to it directly; this walks kind
    plus every rule-owned property. Everything else (modifier, slot,
    derived arrays) is carried from `chosen_where_true` untouched,
    because the rule never writes those (REQ-4.5).

    Not exposed to generated code.
    """
    if chosen_where_true._rule_owned != chosen_where_false._rule_owned:
        raise ValueError(
            "cannot merge grids that own different properties: "
            f"{chosen_where_true._rule_owned} vs {chosen_where_false._rule_owned}"
        )
    arrays = dict(chosen_where_true._arrays)
    for name in chosen_where_true._rule_owned:
        arrays[name] = np.where(
            mask, chosen_where_true._arrays[name], chosen_where_false._arrays[name]
        )
    return Cells._assemble(arrays, chosen_where_true._rule_owned)
