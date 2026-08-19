"""The restricted namespace (REQ-7.9): only the approved surface
exists, and the fixtures still load and run inside it (REQ-14.3).
"""

import inspect

import numpy as np
import pytest

from asr.contract.load import build_namespace, load_rule_class
from asr.contract.namespace import approved_numpy, restricted_builtins
from asr.engine.declaration import Declaration
from asr.engine.dice import Dice
from asr.engine.run import run_rule
from asr.fixtures import life, walker


def test_dangerous_builtins_are_absent():
    allowed = restricted_builtins()
    for name in ("open", "eval", "exec", "getattr", "setattr", "__import__",
                 "type", "vars", "globals", "compile"):
        assert name not in allowed
    for name in ("len", "range", "min", "max", "abs", "int", "float", "bool"):
        assert name in allowed


def test_numpy_proxy_has_no_files_or_randomness():
    for name in ("random", "load", "save", "fromfile", "frombuffer",
                 "argmax", "roll", "ndarray"):
        assert not hasattr(approved_numpy, name), name
    assert approved_numpy.uint8 is np.uint8
    grid = approved_numpy.zeros((3, 3), dtype=approved_numpy.uint8)
    assert grid.dtype == np.uint8


def test_generated_code_cannot_reach_open():
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    source = (
        "class Rule:\n"
        "    KINDS = 2\n"
        "    probe = open  # resolved at class-body execution time\n"
    )
    with pytest.raises(NameError):
        load_rule_class(source, declaration)


def test_fixtures_load_and_run_inside_the_restricted_namespace():
    for fixture in (life, walker):
        declaration = Declaration.from_rule(fixture.Rule)
        rule_class = load_rule_class(
            inspect.getsource(fixture.Rule), declaration
        )
        result = run_rule(
            rule_class, declaration, seed=7, width=12, height=12,
            max_ticks=5, tick_timeout_seconds=5.0,
        )
        assert result.ticks_run >= 1


def test_slot_constants_appear_in_the_namespace():
    declaration = Declaration(
        kinds=2, neighbors="all_8", reach=1,
        semantic_slots={
            "mood": {"values": ["none", "restless"], "assign_when": "birth"}
        },
    )
    namespace = build_namespace(declaration)
    assert namespace["MOOD"].none == 0
    assert namespace["MOOD"].restless == 1
