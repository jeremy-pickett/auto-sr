"""The restricted execution namespace (spec section 7.9).

Generated code runs with an explicit builtins dictionary and a NumPy
proxy exposing only the approved surface. This is contract enforcement,
not security (REQ-3.10, REQ-16.8) — full NumPy includes file access and
the ordinary builtins include open, eval, exec, and getattr; keeping
them out keeps a generated rule inside the language the experiment is
defined over. Additions to either list are a spec change requiring a
new REQ identifier (REQ-7.9.3).
"""

import builtins as _python_builtins

import numpy as np

# REQ-7.9.1 — the whole approved builtin list.
APPROVED_BUILTINS = ("len", "range", "min", "max", "abs", "int", "float", "bool")

# REQ-7.9.2 — the whole approved NumPy surface.
APPROVED_NUMPY_FUNCTIONS = (
    "zeros", "ones", "full", "zeros_like", "ones_like", "full_like",
    "where", "minimum", "maximum", "clip", "abs", "sign", "mod",
    "floor_divide", "logical_and", "logical_or", "logical_not",
    "logical_xor", "sum", "count_nonzero",
)
APPROVED_NUMPY_DTYPES = ("uint8", "uint16", "int32", "float32", "bool_")

# Array methods generated code may call (REQ-7.9.2). Arrays are real
# ndarrays, so this list is enforced by the static validator, not here.
APPROVED_ARRAY_METHODS = ("astype", "copy", "sum")

# np.random is deliberately absent (REQ-7.9.4): randomness reaches
# generated code only through the Dice facade, only in make_start.


class ApprovedNumpy:
    """Only the approved names respond; everything else raises the
    ordinary AttributeError a missing name would.
    """

    __slots__ = ()

    def __repr__(self):
        return "<approved numpy surface (spec section 7.9)>"


for _name in APPROVED_NUMPY_FUNCTIONS + APPROVED_NUMPY_DTYPES:
    setattr(ApprovedNumpy, _name, staticmethod(getattr(np, _name)))

approved_numpy = ApprovedNumpy()


def restricted_builtins() -> dict:
    """The explicit __builtins__ dict for executing rule source.

    __build_class__ is the interpreter's own machinery for the `class`
    statement — without it `class Rule:` cannot execute at all. It is
    not exposed to rule logic; the static validator rejects any dunder
    reference in rule source.
    """
    allowed = {name: getattr(_python_builtins, name) for name in APPROVED_BUILTINS}
    allowed["__build_class__"] = _python_builtins.__build_class__
    return allowed
