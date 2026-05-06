"""JSON-Schema validation of ADR YAML frontmatter.

Spec anchors: ADR.A.2.2, ADR.A.5.4. The binding schema lives in
``maintenance/schemas/header-ontology.json`` under ``types.adr.json_schema``;
this module loads it once and applies it to a parsed frontmatter dict.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402

try:
    import jsonschema  # type: ignore
except ImportError:  # pragma: no cover — surfaced via diagnostic
    jsonschema = None  # type: ignore

Diagnostic = _core.Diagnostic


def _adr_json_schema(ontology: dict[str, Any]) -> dict[str, Any] | None:
    return ontology.get("types", {}).get("adr", {}).get("json_schema")


def validate_frontmatter(
    fm: dict[str, Any],
    *,
    ontology: dict[str, Any],
    rel: str = "<frontmatter>",
) -> list[Diagnostic]:
    """Validate ``fm`` against ``types.adr.json_schema``.

    Each violation becomes one ``Diagnostic`` with code ``ADR.A.2.2`` (or
    ``ADR.A.5.4`` for missing required keys, since that is the variant the
    spec calls out explicitly). Returns ``[]`` on success.
    """
    schema = _adr_json_schema(ontology)
    if schema is None:
        return [Diagnostic(
            rel, None, "ERROR", "ADR.A.5.4",
            "header-ontology.json is missing types.adr.json_schema",
        )]
    if jsonschema is None:
        return [Diagnostic(
            rel, None, "ERROR", "ADR.A.5.4",
            "jsonschema module not importable; install tools/requirements.txt",
        )]

    validator = jsonschema.Draft7Validator(schema)
    diags: list[Diagnostic] = []
    for err in sorted(validator.iter_errors(fm), key=lambda e: list(e.absolute_path)):
        path_parts = list(err.absolute_path)
        loc = ".".join(str(p) for p in path_parts) or "<root>"
        # The spec separates the "missing required key" case as ADR.A.5.4.
        is_required_miss = (
            err.validator == "required"
            and not path_parts
        )
        code = "ADR.A.5.4" if is_required_miss else "ADR.A.2.2"
        diags.append(Diagnostic(
            rel, None, "ERROR", code,
            f"frontmatter schema violation at {loc}: {err.message}",
        ))
    return diags
