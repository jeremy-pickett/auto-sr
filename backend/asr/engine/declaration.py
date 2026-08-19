"""What a rule declares about itself (spec section 7.1).

The declaration is the experiment's label: which properties exist,
how far the rule can see, which modifier is in scope, and which draws
the harness performs. Stage C rejects any implementation whose class
attributes do not match what Stage A declared (REQ-7.8 step 3); the
engine trusts a Declaration it is handed.
"""

from dataclasses import dataclass, field

from .cells import DERIVED_PROPERTIES, OPTIONAL_CORE_PROPERTIES
from .geometry import check_geometry
from .modifiers import MODIFIER_CATALOG

KINDS_RANGE = (2, 8)


@dataclass(frozen=True)
class Declaration:
    kinds: int
    neighbors: str
    reach: int
    uses: tuple = ()
    reads: tuple = ()
    modifiers: tuple = ()
    semantic_slots: dict = field(default_factory=dict)
    assign: dict = field(default_factory=dict)

    def __post_init__(self):
        low, high = KINDS_RANGE
        if not isinstance(self.kinds, int) or not low <= self.kinds <= high:
            raise ValueError(f"KINDS must be an integer from {low} to {high}, got {self.kinds!r}")
        check_geometry(self.neighbors, self.reach)
        for name in self.uses:
            if name not in OPTIONAL_CORE_PROPERTIES:
                raise ValueError(f"USES names an unknown core property {name!r}")
        for name in self.reads:
            if name not in DERIVED_PROPERTIES:
                raise ValueError(f"READS names an unknown derived property {name!r}")
        for name in self.modifiers:
            if name not in MODIFIER_CATALOG:
                raise ValueError(f"MODIFIERS names an unknown modifier {name!r}")
        for name, slot in self.semantic_slots.items():
            values = slot.get("values", [])
            if len(values) < 2:
                raise ValueError(f"semantic slot {name!r} needs at least an identity and one value")
            if slot.get("assign_when") not in ("start", "birth"):
                raise ValueError(f"semantic slot {name!r} needs assign_when of start or birth")
        if len(self.semantic_slots) > 2:
            raise ValueError("at most two semantic slots per rule (REQ-5.5)")

    @classmethod
    def from_rule(cls, rule_class) -> "Declaration":
        """Read the declaration off a rule class's constants."""
        return cls(
            kinds=rule_class.KINDS,
            neighbors=rule_class.NEIGHBORS,
            reach=rule_class.REACH,
            uses=tuple(rule_class.USES),
            reads=tuple(rule_class.READS),
            modifiers=tuple(rule_class.MODIFIERS),
            semantic_slots=dict(rule_class.SEMANTIC_SLOTS),
            assign=dict(rule_class.ASSIGN),
        )

    def rule_owned(self) -> tuple:
        """The arrays the rule itself builds and rewrites every tick."""
        return ("kind",) + tuple(self.uses)

    def declares_birth_draws(self) -> bool:
        """Whether any draw happens after tick 0 — the condition for the
        RNG state joining the computational fingerprint (REQ-9.7.1).
        """
        for name in self.modifiers:
            if MODIFIER_CATALOG[name].assign_when == "birth" and name in self.assign:
                return True
        for slot in self.semantic_slots.values():
            if slot.get("assign_when") == "birth" and slot.get("assign"):
                return True
        return False
