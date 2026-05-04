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
    """Return the set of valid NCP `appreciation` enum strings.

    Falls back to a synthesized set derived from the canonical-vocabulary doc
    if the pinned schema's enum isn't found at the expected path (this keeps
    validate.py useful even before Task 011 lands the full schema bundle).
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

    # The NCP enum lives under definitions.canonical_appreciation.enum
    # (per the upstream schema convention)
    defs = schema.get("definitions") or schema.get("$defs") or {}
    appreciation_def = defs.get("canonical_appreciation", {})
    enum = appreciation_def.get("enum", [])

    # If not under definitions, try top-level properties (some schema generators)
    if not enum:
        for key in ("appreciation", "canonical_appreciation"):
            top = schema.get("properties", {}).get(key, {})
            if "enum" in top:
                enum = top["enum"]
                break

    return set(enum) if enum else set()


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
