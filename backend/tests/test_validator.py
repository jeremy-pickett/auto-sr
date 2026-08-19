"""REQ-15.5: one hand-written bad rule per rejection path. Each must
be rejected by the named check — and the good fixtures must sail
through the same gauntlet (REQ-14.3).
"""

import ast
import inspect
from pathlib import Path

import pytest

from asr.contract.validator import Rejection, validate_source
from asr.engine.declaration import Declaration
from asr.fixtures import life, majority, walker
from asr.generation.pipeline import _validate

BAD_RULES = Path(__file__).parent / "bad_rules"
SIMPLICITY_LIMIT = 40

# file -> the check that must reject it
EXPECTED = {
    "has_import.py": "static",
    "while_loop.py": "static",
    "for_over_grid.py": "static",
    "dice_in_step.py": "static",
    "assigns_self.py": "static",
    "writes_age.py": "static",
    "writes_modifier.py": "static",
    "undeclared_reads.py": "static",
    "look_outside.py": "static",
    "computed_offset.py": "static",
    "diagonal_move.py": "static",
    "too_complex.py": "static",
}


def own_declaration(source: str) -> dict:
    """The declaration a source claims for itself, read off its
    constants — so each bad rule is tested against a matching Stage A
    declaration and fails for its real sin, not for a mismatch."""
    rule = ast.parse(source).body[0]
    constants = {}
    for node in rule.body:
        if isinstance(node, ast.Assign):
            constants[node.targets[0].id] = ast.literal_eval(node.value)
    return {
        "kinds": constants["KINDS"],
        "neighbors": constants["NEIGHBORS"],
        "reach": constants["REACH"],
        "uses": constants["USES"],
        "reads": constants["READS"],
        "modifiers": constants["MODIFIERS"],
        "semantic_slots": constants["SEMANTIC_SLOTS"],
        "assign": constants["ASSIGN"],
    }


@pytest.mark.parametrize("filename", sorted(EXPECTED))
def test_each_static_bad_rule_is_rejected_by_its_check(filename):
    source = (BAD_RULES / filename).read_text()
    with pytest.raises(Rejection) as caught:
        validate_source(source, own_declaration(source), SIMPLICITY_LIMIT)
    assert caught.value.failed_check == EXPECTED[filename]


def test_input_mutation_is_caught_by_the_trial_run():
    # The write slips past every static check by design; the frozen
    # input arrays make it raise inside the child (REQ-7.5).
    source = (BAD_RULES / "mutates_input.py").read_text()
    declared = own_declaration(source)
    proposal = dict(declared)
    failure = _validate(
        source, proposal, Declaration(
            kinds=2, neighbors="all_8", reach=1,
        ), width=16, height=16,
    )
    assert failure is not None
    assert failure.failed_check == "trial_run"
    assert "read-only" in failure.message


def test_declaration_mismatch_including_reads_is_rejected():
    source = (BAD_RULES / "declaration_mismatch.py").read_text()
    honest = own_declaration(source)
    # The source itself is fine when the declarations agree.
    validate_source(source, honest, SIMPLICITY_LIMIT)
    # Stage A declared no READS; the implementation reads age (REQ-15.5).
    lying = dict(honest, reads=[])
    with pytest.raises(Rejection) as caught:
        validate_source(source, lying, SIMPLICITY_LIMIT)
    assert caught.value.failed_check == "declaration_match"
    assert "READS" in caught.value.message


@pytest.mark.parametrize("fixture", [life, majority, walker])
def test_fixtures_pass_the_full_static_gauntlet(fixture):
    source = inspect.getsource(fixture.Rule)
    declaration = Declaration.from_rule(fixture.Rule)
    validate_source(
        source,
        {
            "kinds": declaration.kinds,
            "neighbors": declaration.neighbors,
            "reach": declaration.reach,
            "uses": list(declaration.uses),
            "reads": list(declaration.reads),
            "modifiers": list(declaration.modifiers),
            "semantic_slots": declaration.semantic_slots,
            "assign": declaration.assign,
        },
        SIMPLICITY_LIMIT,
    )


def test_structure_rejects_extra_toplevel_statements():
    source = "x = 1\n" + inspect.getsource(life.Rule)
    with pytest.raises(Rejection) as caught:
        validate_source(source, {}, SIMPLICITY_LIMIT)
    assert caught.value.failed_check == "structure"


def test_structure_rejects_unknown_class_constants():
    source = inspect.getsource(life.Rule).replace(
        "KINDS = 2", "KINDS = 2\n    SECRET = 5"
    )
    with pytest.raises(Rejection) as caught:
        validate_source(source, {}, SIMPLICITY_LIMIT)
    assert caught.value.failed_check == "structure"


def test_static_rejects_numpy_outside_the_approved_surface():
    source = inspect.getsource(life.Rule).replace(
        "count_neighbors(cells, \"kind\", 1)",
        "np.argmax(cells.kind)",
    )
    with pytest.raises(Rejection) as caught:
        validate_source(
            source, own_declaration(inspect.getsource(life.Rule)), SIMPLICITY_LIMIT
        )
    assert caught.value.failed_check == "static"
    assert "argmax" in caught.value.message
