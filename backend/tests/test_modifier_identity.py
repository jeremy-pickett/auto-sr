"""REQ-15.2 as an executable check: every modifier at its identity
default produces output bit-identical to the same rule with the
modifier absent. Stop TICKS may differ (a modifier in scope changes
the fingerprint's contents, e.g. scheduler phase), but the grids the
two runs produce must match tick for tick as far as both ran.
"""

import numpy as np
import pytest

from asr.engine.declaration import Declaration
from asr.engine.modifiers import MODIFIER_CATALOG
from asr.engine.run import run_rule
from asr.fixtures import FIXTURES


@pytest.mark.parametrize("modifier", sorted(MODIFIER_CATALOG))
def test_identity_default_is_bit_identical_to_absent(modifier):
    rule_class = FIXTURES["life"]
    bare_declaration = Declaration.from_rule(rule_class)
    scoped_declaration = Declaration(
        kinds=bare_declaration.kinds,
        neighbors=bare_declaration.neighbors,
        reach=bare_declaration.reach,
        modifiers=(modifier,),  # in scope, never assigned: identity
    )
    common = dict(seed=5, width=14, height=14, max_ticks=60, tick_timeout_seconds=2.0)
    bare = run_rule(rule_class, bare_declaration, **common)
    scoped = run_rule(rule_class, scoped_declaration, **common)
    overlap = min(len(bare.ticks), len(scoped.ticks))
    assert overlap > 10
    for i in range(overlap):
        assert np.array_equal(
            bare.ticks[i].arrays["kind"], scoped.ticks[i].arrays["kind"]
        ), f"{modifier} at identity changed the grid at tick {i}"
        assert bare.ticks[i].pattern_fingerprint == scoped.ticks[i].pattern_fingerprint
