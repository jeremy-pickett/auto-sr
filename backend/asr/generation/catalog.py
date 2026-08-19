"""Generation-time view of the modifier catalog (spec section 5).

Availability gating happens here, once per generation: at most one
non-always modifier is in scope (REQ-5.7 — the experimental control),
and Stage A sees only in-scope modifiers, described by their blurbs
verbatim (REQ-5.3.3, REQ-5.3.4). Semantic slots are gated
independently and are always offered in v1 (REQ-5.8).
"""

import hashlib
import random
import re

from asr.engine.modifiers import MODIFIER_CATALOG


def pick_modifiers_in_scope(chooser: random.Random | None = None) -> list:
    """Evaluate each modifier's availability for one generation.

    `always` modifiers are always in scope (none exist in v1); of the
    `sometimes(p)` ones, at most one joins them (REQ-5.7). `off`
    modifiers never appear.
    """
    chooser = chooser or random
    in_scope = []
    candidates = []
    for spec in MODIFIER_CATALOG.values():
        if spec.availability == "always":
            in_scope.append(spec.name)
        elif spec.availability.startswith("sometimes("):
            chance = float(re.fullmatch(r"sometimes\(([\d.]+)\)", spec.availability)[1])
            candidates.append((spec.name, chance))
    chooser.shuffle(candidates)
    for name, chance in candidates:
        if chooser.random() < chance:
            in_scope.append(name)
            break
    return in_scope


def modifier_blurbs(in_scope: list) -> str:
    """The Stage A description of the in-scope modifiers — each blurb
    verbatim, nothing else (REQ-5.3.4).
    """
    if not in_scope:
        return "None are available for this rule."
    lines = []
    for name in in_scope:
        spec = MODIFIER_CATALOG[name]
        lines.append(
            f"- {name} (whole numbers {spec.lowest} to {spec.highest}, "
            f"default {spec.identity}, assigned at {spec.assign_when}): {spec.blurb}"
        )
    return "\n".join(lines)


def catalog_hash() -> str:
    """A stable stamp of the catalog's exact semantics (REQ-12.4)."""
    text = "\n".join(
        f"{s.name}|{s.lowest}|{s.highest}|{s.identity}|{s.assign_when}|"
        f"{s.effect}|{s.availability}|{s.blurb}"
        for s in sorted(MODIFIER_CATALOG.values(), key=lambda s: s.name)
    )
    return hashlib.blake2b(text.encode(), digest_size=16).hexdigest()
