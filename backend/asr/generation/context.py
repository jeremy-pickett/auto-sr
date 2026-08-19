"""The coverage map and the Stage A context (spec section 8).

Stage A is never sent a list of rules — it is sent a coverage map that
stays the same size forever (REQ-8.1), a handful of examples, and the
recent failure modes. Everything here is built from machine-derived
outcomes only: user overrides and flags never enter generation context
(REQ-8.5), and only canonical runs are counted — one rule, one vote
(REQ-8.6).
"""

import json

# The fixed concept vocabulary (REQ-8.7). Fixed in v1; changing it is
# a prompt-set change, versioned through prompt_set_hash.
CONCEPT_VOCABULARY = (
    "spreads", "resists", "copies", "decays",
    "counts", "remembers", "moves", "competes",
)

SHAPES = (
    "count_based", "threshold", "even_odd", "lookup_table",
    "copying", "walker", "other",
)

MOST_COVERAGE_LINES = 60
MOST_EXAMPLES_PER_GROUP = 3


def cell_key(kinds, neighbors, reach, shape, modifier, slots_used) -> str:
    """One coverage-map cell along the REQ-8.2 axes."""
    return f"{kinds}|{neighbors}|{reach}|{shape}|{modifier}|{int(bool(slots_used))}"


def coverage_map(conn) -> dict:
    """Every touched cell with its three counts (REQ-8.8): attempts,
    successful canonical runs, and rejections. Outcomes are tallied
    over successful canonical runs only.
    """
    coverage = {}

    def cell(key):
        return coverage.setdefault(
            key, {"attempts": 0, "successes": 0, "rejections": 0, "outcomes": {}}
        )

    for row in conn.execute(
        """SELECT rules.kinds, rules.neighbors, rules.reach,
                  rules.requested_shape, rules.modifiers_json,
                  rules.semantic_slots_json, canon.guessed_behavior
           FROM rules
           LEFT JOIN runs canon
             ON canon.rule_id = rules.id AND canon.is_canonical = 1"""
    ):
        modifiers = json.loads(row["modifiers_json"])
        entry = cell(cell_key(
            row["kinds"], row["neighbors"], row["reach"],
            row["requested_shape"] or "other",
            modifiers[0] if modifiers else "none",
            json.loads(row["semantic_slots_json"]) != {},
        ))
        entry["attempts"] += 1
        if row["guessed_behavior"]:
            entry["successes"] += 1
            entry["outcomes"][row["guessed_behavior"]] = (
                entry["outcomes"].get(row["guessed_behavior"], 0) + 1
            )

    # Rejections that never became a rule row still count as attempts
    # in their cell (REQ-8.8.1). Rejections tied to a broken rule are
    # already counted through the rules pass above, so only rule-less
    # rows are added here.
    for row in conn.execute(
        """SELECT kinds, neighbors, reach, requested_shape,
                  modifier_in_scope, COUNT(*) AS n
           FROM rejections WHERE rule_id IS NULL AND kinds IS NOT NULL
           GROUP BY kinds, neighbors, reach, requested_shape, modifier_in_scope"""
    ):
        entry = cell(cell_key(
            row["kinds"], row["neighbors"], row["reach"],
            row["requested_shape"] or "other",
            row["modifier_in_scope"] or "none",
            False,  # the rejections table does not record slot use
        ))
        entry["attempts"] += row["n"]
        entry["rejections"] += row["n"]

    # Broken rules are rejections in their own cell's tally.
    for row in conn.execute(
        """SELECT kinds, neighbors, reach, requested_shape,
                  modifiers_json, semantic_slots_json, COUNT(*) AS n
           FROM rules WHERE status = 'broken'
           GROUP BY kinds, neighbors, reach, requested_shape,
                    modifiers_json, semantic_slots_json"""
    ):
        modifiers = json.loads(row["modifiers_json"])
        entry = cell(cell_key(
            row["kinds"], row["neighbors"], row["reach"],
            row["requested_shape"] or "other",
            modifiers[0] if modifiers else "none",
            json.loads(row["semantic_slots_json"]) != {},
        ))
        entry["rejections"] += row["n"]

    return coverage


def totals(conn) -> dict:
    """Library-wide counts. Behaviors come from canonical runs'
    machine guesses only (REQ-8.5)."""
    result = {"rules": 0, "broken": 0, "behaviors": {}}
    for row in conn.execute(
        """SELECT rules.status, canon.guessed_behavior
           FROM rules
           LEFT JOIN runs canon
             ON canon.rule_id = rules.id AND canon.is_canonical = 1"""
    ):
        result["rules"] += 1
        if row["status"] == "broken":
            result["broken"] += 1
        if row["guessed_behavior"]:
            result["behaviors"][row["guessed_behavior"]] = (
                result["behaviors"].get(row["guessed_behavior"], 0) + 1
            )
    return result


def rejection_tally(conn) -> dict:
    tally = {}
    for row in conn.execute(
        "SELECT failed_check, COUNT(*) AS n FROM rejections GROUP BY failed_check"
    ):
        tally[row["failed_check"]] = row["n"]
    return tally


# ---- the Stage A library summary --------------------------------------


def _totals_line(counts: dict) -> str:
    total = counts["rules"]
    if total == 0:
        return "The library is empty. Everything is unexplored."
    ran = sum(counts["behaviors"].values())
    parts = []
    for behavior, n in sorted(counts["behaviors"].items(), key=lambda kv: -kv[1]):
        share = round(100 * n / ran) if ran else 0
        parts.append(f"{share}% {behavior}")
    broken = counts["broken"]
    return (
        f"{total} rules so far ({broken} broken)"
        + (": " + ", ".join(parts) if parts else "")
        + "."
    )


def _coverage_lines(coverage: dict) -> str:
    if not coverage:
        return "(no cells attempted yet)"
    header = "kinds|neighbors|reach|shape|modifier|slots -> attempts/successes/rejections [outcomes]"
    lines = [header]
    busiest = sorted(coverage.items(), key=lambda kv: -kv[1]["attempts"])
    for key, cell in busiest[:MOST_COVERAGE_LINES]:
        outcomes = " ".join(
            f"{name}:{n}" for name, n in sorted(cell["outcomes"].items())
        )
        lines.append(
            f"{key} -> {cell['attempts']}/{cell['successes']}/{cell['rejections']}"
            + (f" [{outcomes}]" if outcomes else "")
        )
    hidden = len(coverage) - min(len(coverage), MOST_COVERAGE_LINES)
    if hidden:
        lines.append(f"(and {hidden} more attempted cells)")
    lines.append("Every cell not listed has never been attempted.")
    return "\n".join(lines)


def _example_line(row) -> str:
    description = " ".join((row["description"] or "").split())
    if len(description) > 160:
        description = description[:157] + "..."
    modifiers = json.loads(row["modifiers_json"])
    facts = (
        f"{row['kinds']} kinds, {row['neighbors']} reach {row['reach']}, "
        f"shape {row['requested_shape']}, "
        f"modifier {modifiers[0] if modifiers else 'none'}"
    )
    if row["status"] == "broken":
        outcome = f"broken ({row['failed_check']})"
    elif row["guessed_behavior"]:
        outcome = row["guessed_behavior"]
        if row["loop_length"]:
            outcome += f" (repeats every {row['loop_length']})"
    else:
        outcome = "never ran"
    return f"- rule {row['id']} [{facts}] -> {outcome}: {description}"


_EXAMPLE_SELECT = """
    SELECT rules.id, rules.description, rules.status, rules.failed_check,
           rules.kinds, rules.neighbors, rules.reach, rules.requested_shape,
           rules.modifiers_json, rules.semantic_slots_json,
           canon.guessed_behavior, canon.loop_length
    FROM rules
    LEFT JOIN runs canon
      ON canon.rule_id = rules.id AND canon.is_canonical = 1
"""


def _example_groups(conn) -> tuple:
    """Recent, notable, and thinly-attempted examples (REQ-8.3).
    "Notable" is computed from machine signals only (REQ-8.5.1)."""
    recent = conn.execute(
        _EXAMPLE_SELECT + " ORDER BY rules.id DESC LIMIT ?",
        (MOST_EXAMPLES_PER_GROUP,),
    ).fetchall()
    notable = conn.execute(
        _EXAMPLE_SELECT
        + """ WHERE canon.guessed_behavior = 'structured'
                 OR canon.loop_length > 4
              ORDER BY canon.loop_length DESC LIMIT ?""",
        (MOST_EXAMPLES_PER_GROUP,),
    ).fetchall()

    coverage = coverage_map(conn)
    thin_keys = {key for key, cell in coverage.items() if cell["attempts"] == 1}
    thin = []
    for row in conn.execute(_EXAMPLE_SELECT + " ORDER BY rules.id"):
        modifiers = json.loads(row["modifiers_json"])
        key = cell_key(
            row["kinds"], row["neighbors"], row["reach"],
            row["requested_shape"] or "other",
            modifiers[0] if modifiers else "none",
            json.loads(row["semantic_slots_json"]) != {},
        )
        if key in thin_keys:
            thin.append(row)
            if len(thin) >= MOST_EXAMPLES_PER_GROUP:
                break
    return recent, notable, thin


def library_summary_for_stage_a(conn) -> tuple:
    """The {library_summary} block of the Stage A prompt, within the
    REQ-8.3 budget, plus the IDs of every example shown — the only
    legal parent_rule_id values in variation mode (REQ-7.10.1).
    """
    counts = totals(conn)
    coverage = coverage_map(conn)
    recent, notable, thin = _example_groups(conn)

    shown_ids = []
    blocks = [
        "TOTALS\n" + _totals_line(counts),
        "COVERAGE MAP\n" + _coverage_lines(coverage),
    ]
    for title, rows in (
        ("MOST RECENT", recent),
        ("MOST NOTABLE (machine signals only)", notable),
        ("FROM THINLY ATTEMPTED CELLS", thin),
    ):
        if rows:
            lines = []
            for row in rows:
                if row["id"] not in shown_ids:
                    shown_ids.append(row["id"])
                lines.append(_example_line(row))
            blocks.append(f"{title}\n" + "\n".join(lines))

    tally = rejection_tally(conn)
    if tally:
        worst = sorted(tally.items(), key=lambda kv: -kv[1])[:6]
        blocks.append(
            "RECENT FAILURE MODES\n"
            + "\n".join(f"- {check}: {n} rejections" for check, n in worst)
        )

    return "\n\n".join(blocks), shown_ids
