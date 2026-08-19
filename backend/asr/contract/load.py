"""Loading rule source into its execution namespace (REQ-6.1, REQ-7.2).

Rule source — generated or fixture — is a single `class Rule:` that
uses only pre-bound names: the approved NumPy surface as np (REQ-7.9),
make_cells, the spatial helpers bound to its declaration, and the
HEADING constants. Restricted builtins keep the source inside the
contract's language — enforcement of the contract, not a sandbox
(REQ-3.10).
"""

from asr.contract.namespace import approved_numpy, restricted_builtins
from asr.engine.cells import make_cells
from asr.engine.declaration import Declaration
from asr.engine.geometry import HEADING
from asr.engine.helpers import bind_helpers


def build_namespace(declaration: Declaration) -> dict:
    namespace = {
        "__builtins__": restricted_builtins(),
        "__name__": "generated_rule",  # class creation reads this for __module__
        "np": approved_numpy,
        "make_cells": make_cells,
        "HEADING": HEADING,
    }
    namespace.update(bind_helpers(declaration.neighbors, declaration.reach))
    for slot_name, slot in declaration.semantic_slots.items():
        # Slot values are named constants, never strings (REQ-5.2.1):
        # MOOD.restless for a slot called "mood".
        constants = type(slot_name.upper(), (), {
            value: index for index, value in enumerate(slot["values"])
        })
        namespace[slot_name.upper()] = constants
    return namespace


def load_rule_class(source: str, declaration: Declaration):
    """Execute rule source in its namespace and hand back the class."""
    namespace = build_namespace(declaration)
    exec(compile(source, "<rule>", "exec"), namespace)  # noqa: S102 - the whole product
    rule_class = namespace.get("Rule")
    if rule_class is None:
        raise ValueError("the source did not define a class named Rule")
    return rule_class
