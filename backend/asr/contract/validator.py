"""Stage C validation, steps 1–3 (REQ-7.8): structure, static checks,
and declaration match. Steps 4–7 (load, trial run, reproducibility,
repair) live in the generation pipeline, which calls these first.

Every rejection carries the failing check by name plus the specific
error text — that pair is what the repair prompt gets (REQ-10.4) and
what the rejections table records (REQ-7.11).
"""

import ast
from dataclasses import dataclass

from asr.contract.namespace import (
    APPROVED_ARRAY_METHODS,
    APPROVED_NUMPY_DTYPES,
    APPROVED_NUMPY_FUNCTIONS,
)
from asr.engine.cells import DERIVED_PROPERTIES, OPTIONAL_CORE_PROPERTIES
from asr.engine.geometry import HEADING_NAMES, allowed_move_headings, neighbor_offsets
from asr.engine.modifiers import MODIFIER_CATALOG

DECLARED_CONSTANTS = (
    "KINDS", "NEIGHBORS", "REACH", "USES", "READS", "MODIFIERS",
    "SEMANTIC_SLOTS", "ASSIGN", "SUGGESTED_DISPLAY",
)
REQUIRED_METHODS = ("__init__", "make_start", "step")

# Branch, loop, and comprehension node types the simplicity limit
# counts (REQ-7.6).
COUNTED_NODES = (
    ast.If, ast.IfExp, ast.For, ast.While,
    ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
)

# Helpers whose second argument names a property; reads through them
# are checked against the declaration just like attribute reads.
PROPERTY_HELPERS = ("look", "move", "count_neighbors", "sum_neighbors")


@dataclass
class Rejection(Exception):
    """One failed validation check: the check's name and the specific
    error, exactly what repair and the rejections table need.
    """

    failed_check: str
    message: str

    def __str__(self):
        return f"{self.failed_check}: {self.message}"


def validate_source(source: str, declared: dict, simplicity_limit: int) -> None:
    """Run structure, static, and declaration-match checks in order
    (REQ-7.8 steps 1–3). Raises Rejection on the first failure.

    `declared` is what Stage A declared, as plain values: kinds,
    neighbors, reach, uses, reads, modifiers, semantic_slots, assign.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as bad:
        raise Rejection("structure", f"the source does not parse: {bad}") from None
    rule = _check_structure(tree)
    constants = _read_constants(rule)
    _check_static(rule, constants, simplicity_limit)
    _check_declaration_match(constants, declared)


# ---- step 1: structure ------------------------------------------------


def _check_structure(tree: ast.Module) -> ast.ClassDef:
    """Exactly one top-level `class Rule:` with no bases, decorators,
    or metaclass; a class body of approved constants and the three
    methods (REQ-7.1).
    """
    statements = [
        node for node in tree.body
        if not _is_docstring(node)
    ]
    if len(statements) != 1 or not isinstance(statements[0], ast.ClassDef):
        raise Rejection(
            "structure",
            "the module must contain exactly one top-level class definition "
            "and nothing else",
        )
    rule = statements[0]
    if rule.name != "Rule":
        raise Rejection("structure", f"the class must be named Rule, not {rule.name}")
    if rule.bases or rule.keywords or rule.decorator_list:
        raise Rejection(
            "structure", "Rule may not have base classes, decorators, or a metaclass"
        )

    seen_methods = []
    for node in rule.body:
        if _is_docstring(node):
            continue
        if isinstance(node, ast.FunctionDef):
            if node.name not in REQUIRED_METHODS:
                raise Rejection(
                    "structure",
                    f"unexpected method {node.name!r}; only "
                    f"{REQUIRED_METHODS} are allowed",
                )
            if node.decorator_list:
                raise Rejection("structure", f"{node.name} may not have decorators")
            seen_methods.append(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if not isinstance(target, ast.Name) or target.id not in DECLARED_CONSTANTS:
                    raise Rejection(
                        "structure",
                        "class-body assignments are limited to the declared "
                        f"constants {DECLARED_CONSTANTS}",
                    )
        else:
            raise Rejection(
                "structure",
                f"unexpected statement in the class body: {ast.dump(node)[:80]}",
            )
    missing = [name for name in REQUIRED_METHODS if name not in seen_methods]
    if missing:
        raise Rejection("structure", f"Rule is missing methods: {missing}")
    return rule


def _is_docstring(node) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _read_constants(rule: ast.ClassDef) -> dict:
    """The declared constants as plain Python values."""
    constants = {}
    for node in rule.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            try:
                literal = ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError):
                raise Rejection(
                    "structure",
                    f"{targets[0].id} must be a literal value",
                ) from None
            for target in targets:
                constants[target.id] = literal
    missing = [
        name for name in DECLARED_CONSTANTS
        if name != "SUGGESTED_DISPLAY" and name not in constants
    ]
    if missing:
        raise Rejection("structure", f"Rule is missing constants: {missing}")
    return constants


# ---- step 2: static checks --------------------------------------------


def _check_static(rule: ast.ClassDef, constants: dict, simplicity_limit: int) -> None:
    uses = list(constants.get("USES", []))
    reads = list(constants.get("READS", []))
    modifiers = list(constants.get("MODIFIERS", []))
    slot_names = list(constants.get("SEMANTIC_SLOTS", {}) or {})
    try:
        offsets = set(neighbor_offsets(constants["NEIGHBORS"], constants["REACH"]))
        move_headings = allowed_move_headings(constants["NEIGHBORS"])
    except (ValueError, KeyError) as bad:
        raise Rejection("static", f"unusable geometry declaration: {bad}") from None

    methods = {
        node.name: node for node in rule.body if isinstance(node, ast.FunctionDef)
    }

    for node in ast.walk(rule):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise Rejection("static", "imports are not allowed (REQ-7.2)")
        if isinstance(node, ast.While):
            raise Rejection("static", "while loops are banned outright (REQ-7.6.1)")
        if isinstance(node, ast.For):
            _check_for_loop(node)
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                raise Rejection(
                    "static",
                    f"underscore attribute access ({node.attr!r}) is not allowed",
                )
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise Rejection("static", f"the name {node.id!r} is not allowed")

    # Property discipline over the whole class: reads must be declared.
    for node in ast.walk(rule):
        for prop in _properties_touched(node):
            _check_property_read(prop, uses, reads, modifiers)

    # The approved surface: np.<name> and array methods (REQ-7.9.2).
    for node in ast.walk(rule):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "np":
                approved = APPROVED_NUMPY_FUNCTIONS + APPROVED_NUMPY_DTYPES
                if node.attr not in approved:
                    raise Rejection(
                        "static",
                        f"np.{node.attr} is outside the approved NumPy surface "
                        "(REQ-7.9.2)",
                    )

    # Writes: no assignment may target a derived, modifier, or slot
    # array (REQ-7.7) — as an attribute or through a subscript on one.
    protected = set(DERIVED_PROPERTIES) | set(MODIFIER_CATALOG) | set(slot_names)
    for node in ast.walk(rule):
        for target in _assignment_targets(node):
            named = _attribute_behind(target)
            if named is not None and named.attr in protected:
                raise Rejection(
                    "static",
                    f"{named.attr!r} is read-only to rule code (REQ-7.7)",
                )

    # Spatial helper calls: literal offsets inside the declared
    # neighborhood; moves along permitted headings only (REQ-6.2.2).
    for node in ast.walk(rule):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "look":
                _check_look_call(node, offsets, constants)
            elif node.func.id == "move":
                _check_move_call(node, move_headings, constants)

    # step-only rules (REQ-7.4, REQ-7.4.1, REQ-7.6).
    step = methods["step"]
    for node in ast.walk(step):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "self" and node.attr == "dice":
                raise Rejection(
                    "static", "self.dice may appear only in make_start (REQ-7.4.1)"
                )
        for target in _assignment_targets(node):
            named = _attribute_behind(target)
            if (
                named is not None
                and isinstance(named.value, ast.Name)
                and named.value.id == "self"
            ):
                raise Rejection(
                    "static", "step may not assign to self (REQ-7.4)"
                )
    counted = sum(
        isinstance(node, COUNTED_NODES) for node in ast.walk(step)
    )
    if counted > simplicity_limit:
        raise Rejection(
            "static",
            f"step has {counted} branch/loop/comprehension nodes; the "
            f"simplicity limit is {simplicity_limit} (REQ-7.6)",
        )

    # Array methods anywhere: astype, copy, sum only — any other method
    # call on a non-np, non-self object is off the approved surface.
    for node in ast.walk(rule):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id in ("np", "self"):
                continue
            if node.func.attr not in APPROVED_ARRAY_METHODS + ("chance", "integers", "choice"):
                raise Rejection(
                    "static",
                    f"method .{node.func.attr}() is outside the approved "
                    "array surface (REQ-7.9.2)",
                )


def _check_for_loop(node: ast.For) -> None:
    """for loops only over range(n) with literal n <= 8, or a literal
    tuple or list — never a grid dimension (REQ-7.6.1).
    """
    iterated = node.iter
    if isinstance(iterated, ast.Call) and isinstance(iterated.func, ast.Name):
        if iterated.func.id == "range" and len(iterated.args) == 1:
            bound = iterated.args[0]
            if isinstance(bound, ast.Constant) and isinstance(bound.value, int):
                if bound.value <= 8:
                    return
                raise Rejection(
                    "static", f"range({bound.value}) exceeds the literal limit of 8"
                )
        raise Rejection(
            "static",
            "for loops may only iterate range(n) with a literal n <= 8, "
            "or a literal tuple or list (REQ-7.6.1)",
        )
    if isinstance(iterated, (ast.Tuple, ast.List)):
        for element in iterated.elts:
            if not isinstance(element, (ast.Constant, ast.Attribute)):
                raise Rejection(
                    "static", "loop tuples/lists must hold literal values"
                )
        return
    raise Rejection(
        "static",
        "for loops may only iterate range(n) with a literal n <= 8, or a "
        "literal tuple or list — never a grid dimension (REQ-7.6.1)",
    )


def _properties_touched(node) -> list:
    """Property names this node reads: attribute reads that name a
    known cell property, plus property-name strings passed to spatial
    helpers.
    """
    known = (
        set(OPTIONAL_CORE_PROPERTIES) | set(DERIVED_PROPERTIES) | set(MODIFIER_CATALOG)
    )
    touched = []
    if isinstance(node, ast.Attribute) and node.attr in known:
        # self.KINDS etc. are constants, not properties; anything else
        # holding a property name is (or aliases) the grid.
        if not (isinstance(node.value, ast.Name) and node.value.id in ("self", "np")):
            touched.append(node.attr)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in PROPERTY_HELPERS and len(node.args) >= 2:
            prop = node.args[1]
            if isinstance(prop, ast.Constant) and isinstance(prop.value, str):
                if prop.value in known:
                    touched.append(prop.value)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "make_cells":
            for keyword in node.keywords:
                if keyword.arg in OPTIONAL_CORE_PROPERTIES:
                    touched.append(keyword.arg)
    return touched


def _check_property_read(prop, uses, reads, modifiers) -> None:
    if prop in OPTIONAL_CORE_PROPERTIES and prop not in uses:
        raise Rejection(
            "static", f"core property {prop!r} is not declared in USES"
        )
    if prop in DERIVED_PROPERTIES and prop not in reads:
        raise Rejection(
            "static", f"derived property {prop!r} is not declared in READS (REQ-7.7)"
        )
    if prop in MODIFIER_CATALOG and prop not in modifiers:
        raise Rejection(
            "static", f"modifier {prop!r} is not declared in MODIFIERS"
        )


def _assignment_targets(node) -> list:
    if isinstance(node, ast.Assign):
        return node.targets
    if isinstance(node, (ast.AugAssign, ast.AnnAssign)):
        return [node.target]
    return []


def _attribute_behind(target):
    """The Attribute node an assignment ultimately writes through:
    `x.age = v`, `x.age[mask] = v`, and `x.age += v` all resolve to the
    `.age` attribute.
    """
    while isinstance(target, ast.Subscript):
        target = target.value
    return target if isinstance(target, ast.Attribute) else None


def _literal_int(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, int)
    ):
        return -node.operand.value
    return None


def _check_look_call(node: ast.Call, offsets: set, constants: dict) -> None:
    if len(node.args) != 4:
        raise Rejection("static", "look takes (cells, prop, down, right)")
    down = _literal_int(node.args[2])
    right = _literal_int(node.args[3])
    if down is None or right is None:
        raise Rejection(
            "static", "look offsets must be literal integers (REQ-6.2.2)"
        )
    if (down, right) not in offsets:
        raise Rejection(
            "static",
            f"look offset ({down}, {right}) is outside the declared "
            f"{constants['NEIGHBORS']} neighborhood at reach {constants['REACH']}",
        )


def _check_move_call(node: ast.Call, move_headings, constants: dict) -> None:
    if len(node.args) != 3:
        raise Rejection("static", "move takes (cells, prop, direction)")
    direction = node.args[2]
    if not (
        isinstance(direction, ast.Attribute)
        and isinstance(direction.value, ast.Name)
        and direction.value.id == "HEADING"
        and direction.attr in HEADING_NAMES
    ):
        raise Rejection(
            "static", "move's direction must be a HEADING constant (REQ-6.2.2)"
        )
    if direction.attr not in move_headings:
        raise Rejection(
            "static",
            f"move toward {direction.attr!r} is not allowed under "
            f"{constants['NEIGHBORS']} (REQ-6.3.3)",
        )


# ---- step 3: declaration match ----------------------------------------


def _check_declaration_match(constants: dict, declared: dict) -> None:
    """The implementation's constants must exactly match what Stage A
    declared — a mismatch means the implementation silently rewrote the
    experiment (REQ-7.8 step 3). READS included.
    """
    pairs = (
        ("KINDS", "kinds"),
        ("NEIGHBORS", "neighbors"),
        ("REACH", "reach"),
        ("USES", "uses"),
        ("READS", "reads"),
        ("MODIFIERS", "modifiers"),
        ("SEMANTIC_SLOTS", "semantic_slots"),
        ("ASSIGN", "assign"),
    )
    for constant_name, declared_name in pairs:
        implemented = constants.get(constant_name)
        wanted = declared.get(declared_name)
        if constant_name in ("USES", "READS", "MODIFIERS"):
            implemented = list(implemented or [])
            wanted = list(wanted or [])
        elif constant_name in ("SEMANTIC_SLOTS", "ASSIGN"):
            implemented = dict(implemented or {})
            wanted = dict(wanted or {})
        if implemented != wanted:
            raise Rejection(
                "declaration_match",
                f"{constant_name} is {implemented!r} but Stage A declared "
                f"{wanted!r}",
            )
