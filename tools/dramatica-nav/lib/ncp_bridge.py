"""NCP enum closure helper.

Loads the pinned NCP schema and exposes the set of valid `appreciation`
enum values for validate.py's NCP-closure check.

The pinned schema lives at:
    skills/ncp-author/upstream/schema/ncp-schema.json

The relevant subschema is `definitions.canonical_appreciation.enum`
(per ncp-author/references/canonical-vocabulary.md, which describes the
463-value enum).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from . import OntologyError


def load_ncp_appreciations(repo_root: Optional[Path] = None) -> set[str]:
    """Return the union of all valid NCP enum-string surfaces an ontology
    `ncp_appreciation` field may legitimately reference.

    Per kickoff SPEC §2.5, the ontology's `ncp_appreciation` maps to multiple
    NCP enum surfaces depending on the entity kind:
      - throughlines → NCP `throughline` enum (4 values: "Main Character", ...)
      - storypoint appreciations → `canonical_appreciation` enum (463 values)
      - narrative functions → `canonical_narrative_function` enum (144 values)

    Returns the union of all three. character-dynamics and plot-dynamics
    don't have a clean NCP mapping (they map to slot-name patterns that
    compose with the throughline) and SHOULD have `ncp_appreciation` absent
    rather than partial — those entries are corrected at the data layer.
    """
    if repo_root is None:
        here = Path(__file__).resolve()
        repo_root = here.parents[3]

    schema_path = repo_root / "skills" / "ncp-author" / "upstream" / "schema" / "ncp-schema.json"
    if not schema_path.exists():
        # Defensive fallback: empty set means "no closure check"
        return set()

    try:
        schema = json.loads(schema_path.read_text())
    except json.JSONDecodeError as e:
        raise OntologyError(f"ncp-schema.json malformed: {e}") from e

    valid: set[str] = set()

    # 1. Top-level $defs / definitions enums
    defs = schema.get("$defs") or schema.get("definitions") or {}
    for key in ("canonical_appreciation", "canonical_narrative_function"):
        enum = defs.get(key, {}).get("enum", [])
        if enum:
            valid.update(enum)

    # 2. Inline throughline enum (buried in the storypoints subschema)
    # Walk the schema looking for any enum that includes throughline names
    def walk(node):
        if isinstance(node, dict):
            if "enum" in node and isinstance(node["enum"], list):
                yield node["enum"]
            for v in node.values():
                yield from walk(v)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v)

    throughline_marker = "Main Character"
    for enum in walk(schema):
        if throughline_marker in enum:
            valid.update(enum)
            break  # throughline enum found

    return valid


def is_valid_appreciation(appreciation: str, valid_set: Optional[set[str]] = None) -> bool:
    """Check if `appreciation` is in the valid NCP enum set.

    If valid_set is None, loads the default set. If the loaded set is empty
    (no NCP schema available), returns True (defensive — don't fail closed
    when the closure source is unavailable).
    """
    if valid_set is None:
        valid_set = load_ncp_appreciations()
    if not valid_set:
        return True
    return appreciation in valid_set
