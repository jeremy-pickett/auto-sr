"""Inferring observed_shape from an implementation (REQ-8.2.1).

requested_shape is what Stage A was reasoning about and drives the
coverage map; observed_shape is what the code actually does. Static
inference first; a small model call only where the code is ambiguous.
A mismatch between the two is generator-quality data, not an error.
"""

import ast

from asr.generation.context import SHAPES


def infer_shape_statically(source: str) -> str | None:
    """Cheap structural reading of the implementation. Returns None
    when the code fits no clear shape and the model should be asked.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    called = set()
    compared = False
    uses_remainder = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
        if isinstance(node, ast.Compare) and any(
            isinstance(op, (ast.Gt, ast.GtE, ast.Lt, ast.LtE)) for op in node.ops
        ):
            compared = True
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            uses_remainder = True
        if isinstance(node, ast.Constant) and node.value == 2:
            pass

    if "move" in called:
        return "walker"
    if uses_remainder or "mod" in called:
        return "even_odd"
    if {"count_neighbors", "count_neighbors_where", "sum_neighbors"} & called:
        # Tallying neighbors and comparing against a cutoff is the
        # count_based/threshold family; equality-only tests read as
        # counting proper.
        return "threshold" if compared else "count_based"
    if "look" in called:
        return "copying"
    return None


SHAPE_QUESTION = (
    "Here is a cellular automaton step function. Classify its shape as "
    "exactly one word from this list: " + ", ".join(SHAPES) + ".\n"
    "Reply with the single word only.\n\nCODE\n{source}"
)


def infer_shape(source: str, ask_model=None) -> str:
    """Static first; the model only for the ambiguous remainder.
    `ask_model(prompt) -> str` is injected by the pipeline."""
    found = infer_shape_statically(source)
    if found:
        return found
    if ask_model is not None:
        try:
            answer = ask_model(SHAPE_QUESTION.replace("{source}", source))
            word = answer.strip().split()[0].strip(".,\"'").lower()
            if word in SHAPES:
                return word
        except Exception:
            pass  # shape is advisory; never fail a good rule over it
    return "other"
