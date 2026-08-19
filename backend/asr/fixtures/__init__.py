"""Hand-written reference rules (spec section 14).

These exist so the harness can be tested independently of the
generator — without them, a harness bug and a bad generation are
indistinguishable (REQ-14.1). Each module's class body obeys the full
plugin contract, so they double as worked examples for the Stage B
prompt if few-shot proves necessary (REQ-14.3). The module-level
imports are the fixtures' loading mechanism, not part of the contract
example; generated code gets everything pre-bound instead (REQ-7.2).
"""

from . import life, majority, walker

FIXTURES = {
    "life": life.Rule,
    "majority": majority.Rule,
    "walker": walker.Rule,
}
