#!/usr/bin/env python3
"""validate.py — Narrative-ontology integrity validator (CI).

Exit codes:
    0  clean (0 errors; warnings allowed unless --strict)
    1  >=1 errors (or warnings promoted by --strict)
    2  I/O failure (missing files, parse errors)

Usage:
    validate.py [--json] [--strict] [--ontology <path>]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# --- lib import ----------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ontology as _ontology_lib
from lib import frontmatter as _frontmatter_lib
from lib import OntologyError

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("ERROR: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

# -------------------------------------------------------------------------
# Type aliases
# -------------------------------------------------------------------------
Finding = dict[str, Any]

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[1]  # tools/dramatica-nav -> tools -> repo root
_SCHEMA_PATH = _REPO_ROOT / "maintenance" / "schemas" / "narrative-ontology" / "ontology.schema.json"
_VOCAB_SKIP = _frontmatter_lib.VOCAB_SKIP


def _load_json_schema(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise OntologyError(f"Schema file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise OntologyError(f"Schema file malformed: {path}: {exc}") from exc


# -------------------------------------------------------------------------
# ERROR checks
# -------------------------------------------------------------------------

def check_schema(
    entries: list[dict],
    schema: dict,
) -> list[Finding]:
    """Check 1: Per-entry JSON schema validation."""
    validator = Draft202012Validator(schema)
    errors: list[Finding] = []
    for entry in entries:
        entry_id = entry.get("id", "<no-id>")
        for error in validator.iter_errors(entry):
            pointer = error.json_path if hasattr(error, "json_path") else "/".join(
                str(p) for p in error.absolute_path
            )
            errors.append({
                "check": "schema",
                "id": entry_id,
                "pointer": pointer or ".",
                "message": error.message,
            })
    return errors


def check_dynamic_pair_reciprocity(
    entries: list[dict],
    by_id: dict[str, dict],
) -> list[Finding]:
    """Check 2: Every entry with dynamic_pair_id has a reciprocal partner."""
    errors: list[Finding] = []
    for entry in entries:
        dp_id = entry.get("dynamic_pair_id")
        if dp_id is None:
            continue
        eid = entry["id"]
        partner = by_id.get(dp_id)
        if partner is None:
            errors.append({
                "check": "reciprocity",
                "id": eid,
                "partner": dp_id,
                "issue": "missing",
            })
        elif partner.get("dynamic_pair_id") != eid:
            actual = partner.get("dynamic_pair_id")
            errors.append({
                "check": "reciprocity",
                "id": eid,
                "partner": dp_id,
                "issue": f"asymmetric→{actual}",
            })
    return errors


def check_pair_member_resolvability(
    entries: list[dict],
    by_id: dict[str, dict],
) -> list[Finding]:
    """Check 3: Both pair_member_a/_b on dynamic-pair entries resolve."""
    errors: list[Finding] = []
    for entry in entries:
        if entry.get("kind") != "dynamic-pair":
            continue
        dp_id = entry.get("id", "<no-id>")
        for field in ("pair_member_a", "pair_member_b"):
            value = entry.get(field)
            if value is None:
                # schema check will catch required-field violations
                continue
            if value not in by_id:
                errors.append({
                    "check": "pair_member",
                    "dp_id": dp_id,
                    "field": field,
                    "value": value,
                })
    return errors


def check_alias_uniqueness(entries: list[dict]) -> list[Finding]:
    """Check 4: No alias string appears in two different entries for the same locale."""
    # locale -> alias_lower -> [entry_id, ...]
    index: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for entry in entries:
        eid = entry.get("id", "<no-id>")
        for key, value in entry.items():
            if key.startswith("aliases_") and isinstance(value, list):
                locale = key[len("aliases_"):]
                for alias in value:
                    index[locale][alias.lower()].append(eid)

    errors: list[Finding] = []
    for locale, aliases in sorted(index.items()):
        for alias, entry_ids in sorted(aliases.items()):
            if len(entry_ids) > 1:
                errors.append({
                    "check": "alias-uniqueness",
                    "locale": locale,
                    "alias": alias,
                    "entries": entry_ids,
                })
    return errors


def _build_ncp_valid_set(repo_root: Path) -> set[str]:
    """Return union of all enum values from the pinned NCP schema's $defs."""
    p = repo_root / "skills" / "ncp-author" / "upstream" / "schema" / "ncp-schema.json"
    if not p.exists():
        return set()
    try:
        schema = json.loads(p.read_text())
    except json.JSONDecodeError:
        return set()
    defs = schema.get("definitions") or schema.get("$defs") or {}
    result: set[str] = set()
    for defn in defs.values():
        enum = defn.get("enum")
        if isinstance(enum, list):
            result.update(str(v) for v in enum)
    return result


def check_ncp_enum_closure(
    entries: list[dict],
    ncp_valid: set[str],
) -> tuple[list[Finding], bool]:
    """Check 5: ncp_appreciation is grounded in the NCP enum.

    Passes when: (a) exact match, (b) value is a prefix of some enum string
    (v0.1 entries use Dramatica shorthand like "Influence Character" that
    prefix "Influence Character Throughline"), or (c) partial=True
    (explicit roll-up). Returns (errors, skipped=True when enum empty).
    """
    if not ncp_valid:
        return [], True
    errors: list[Finding] = []
    for entry in entries:
        ncp = entry.get("ncp_appreciation")
        if ncp is None or entry.get("ncp_appreciation_partial", False):
            continue
        if ncp not in ncp_valid and not any(ev.startswith(ncp) for ev in ncp_valid):
            errors.append({"check": "ncp-enum", "id": entry.get("id", "<no-id>"), "value": ncp})
    return errors, False


# -------------------------------------------------------------------------
# WARNING checks
# -------------------------------------------------------------------------

def check_quad_membership(
    entries: list[dict],
    by_id: dict[str, dict],
) -> list[Finding]:
    """Check 6 (warning): quad entries should have exactly 4 KTAD members."""
    # Build quad_id -> [member entries]
    quad_members: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        qid = entry.get("quad_id")
        if qid:
            quad_members[qid].append(entry)

    warnings: list[Finding] = []
    expected_ktad = {"K", "T", "A", "D"}
    for entry in entries:
        if entry.get("kind") != "quad":
            continue
        qid = entry["id"]
        members = quad_members.get(qid, [])
        ktad_positions = [m.get("ktad_position") for m in members if m.get("ktad_position")]
        ktad_set = set(ktad_positions)
        if len(members) != 4 or ktad_set != expected_ktad:
            warnings.append({
                "check": "quad-membership",
                "quad_id": qid,
                "members": len(members),
                "ktad_positions": sorted(ktad_set),
                "expected": "4 members + KTAD",
            })
    return warnings


def check_term_file_anchors(
    entries: list[dict],
    repo_root: Path,
) -> list[Finding]:
    """Check 7 (warning): term_file anchors resolve to real ## headings."""
    warnings: list[Finding] = []
    file_cache: dict[Path, str] = {}

    for entry in entries:
        tf = entry.get("term_file")
        if not tf or "#" not in tf:
            continue
        file_part, anchor = tf.split("#", 1)
        fpath = repo_root / file_part

        if fpath not in file_cache:
            if not fpath.exists():
                warnings.append({
                    "check": "term_file-anchor",
                    "id": entry.get("id", "<no-id>"),
                    "term_file": tf,
                    "issue": "file not found",
                })
                continue
            file_cache[fpath] = fpath.read_text()

        text = file_cache[fpath]
        headings = _frontmatter_lib.find_heading_anchors(text)
        slug_set = {s for _, s in headings}
        slug2_set = {_frontmatter_lib.slugify_keep_parens(h) for h, _ in headings}

        if anchor not in slug_set and anchor not in slug2_set:
            warnings.append({
                "check": "term_file-anchor",
                "id": entry.get("id", "<no-id>"),
                "term_file": tf,
                "issue": "heading not found",
            })
    return warnings


def check_unmapped_headings(
    entries: list[dict],
    repo_root: Path,
) -> list[Finding]:
    """Check 8 (warning): every ## heading in vocab refs maps to an entry."""
    # Build set of (file_rel, anchor) pairs that are mapped
    mapped: set[tuple[str, str]] = set()
    for entry in entries:
        tf = entry.get("term_file")
        if tf and "#" in tf:
            file_part, anchor = tf.split("#", 1)
            mapped.add((file_part, anchor))

    base = repo_root / "skills" / "dramatica-vocabulary" / "references"
    warnings: list[Finding] = []

    for md_file in sorted(base.glob("*.md")):
        if md_file.name in _VOCAB_SKIP:
            continue
        text = md_file.read_text()
        rel = str(md_file.relative_to(repo_root))
        for heading, slug in _frontmatter_lib.find_heading_anchors(text):
            slug2 = _frontmatter_lib.slugify_keep_parens(heading)
            if (rel, slug) not in mapped and (rel, slug2) not in mapped:
                warnings.append({
                    "check": "unmapped-heading",
                    "file": md_file.name,
                    "heading": heading,
                    "anchor": slug,
                })
    return warnings


# -------------------------------------------------------------------------
# Formatting
# -------------------------------------------------------------------------

def _fmt_error(f: Finding) -> str:
    check = f["check"]
    if check == "schema":
        return f"[schema] {f['id']} @ {f['pointer']}: {f['message']}"
    if check == "reciprocity":
        return f"[reciprocity] {f['id']} → {f['partner']} : {f['issue']}"
    if check == "pair_member":
        return f"[pair_member] {f['dp_id']}.{f['field']} : {f['value']} (not in ontology)"
    if check == "alias-uniqueness":
        return f"[alias-uniqueness] locale={f['locale']} alias={f['alias']!r} entries={f['entries']}"
    if check == "ncp-enum":
        return f"[ncp-enum] {f['id']} : {f['value']!r} not in NCP enum"
    return json.dumps(f)


def _fmt_warning(f: Finding) -> str:
    check = f["check"]
    if check == "quad-membership":
        return (
            f"[quad-membership] {f['quad_id']} : {f['members']} members"
            f", ktad={f['ktad_positions']} (expected 4)"
        )
    if check == "term_file-anchor":
        return f"[term_file-anchor] {f['id']} : {f['term_file']} ({f['issue']})"
    if check == "unmapped-heading":
        return (
            f"[unmapped-heading] {f['file']} : {f['heading']!r}"
            f" (anchor={f['anchor']})"
        )
    return json.dumps(f)


def _human_output(
    errors: list[Finding],
    warnings: list[Finding],
    by_check: dict[str, int],
    ncp_skipped: bool,
) -> None:
    n_err = len(errors)
    n_warn = len(warnings)
    print(f"== validate.py: {n_err} error{'s' if n_err != 1 else ''}"
          f" / {n_warn} warning{'s' if n_warn != 1 else ''} ==")

    if errors:
        print("\nERRORS:")
        for f in errors:
            print(f"  {_fmt_error(f)}")

    if warnings:
        print("\nWARNINGS:")
        for f in warnings:
            print(f"  {_fmt_warning(f)}")

    print("\nSUMMARY:")
    error_line = (
        f"  schema: {by_check.get('schema', 0)}"
        f" / dynamic-pair-reciprocity: {by_check.get('reciprocity', 0)}"
        f" / pair_member: {by_check.get('pair_member', 0)}"
        f" / alias-uniqueness: {by_check.get('alias-uniqueness', 0)}"
        f" / ncp-enum: {by_check.get('ncp-enum', 0)}"
    )
    if ncp_skipped:
        error_line += " (ncp-enum skipped: schema unavailable)"
    print(error_line)
    print(
        f"  quad-membership-partial: {by_check.get('quad-membership', 0)}"
        f" / term_file-anchor-mismatch: {by_check.get('term_file-anchor', 0)}"
        f" / unmapped-heading: {by_check.get('unmapped-heading', 0)}"
    )


def _json_output(
    errors: list[Finding],
    warnings: list[Finding],
    by_check: dict[str, int],
) -> None:
    payload = {
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "errors_total": len(errors),
            "warnings_total": len(warnings),
            "by_check": by_check,
        },
    }
    print(json.dumps(payload, indent=2))


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Narrative-ontology integrity validator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="emit_json",
        help="Emit structured JSON output instead of human-readable text.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit code 1 if any warnings exist).",
    )
    parser.add_argument(
        "--ontology",
        metavar="PATH",
        help="Override path to ontology.json (default: maintenance/.../ontology.json).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    # --- resolve ontology path -------------------------------------------
    if args.ontology:
        ontology_path = Path(args.ontology).resolve()
    else:
        ontology_path = _REPO_ROOT / "maintenance" / "schemas" / "narrative-ontology" / "ontology.json"

    # --- load ontology ---------------------------------------------------
    try:
        idx = _ontology_lib.OntologyIndex(ontology_path)
    except OntologyError as exc:
        print(f"I/O ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    entries = idx.entries
    by_id = idx._by_id  # direct access to internal dict for speed

    # --- load JSON schema ------------------------------------------------
    try:
        schema = _load_json_schema(_SCHEMA_PATH)
    except OntologyError as exc:
        print(f"I/O ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    # --- load NCP enum (union of all def enums in the pinned schema) -----
    ncp_valid = _build_ncp_valid_set(_REPO_ROOT)

    # =====================================================================
    # Run all 8 checks
    # =====================================================================

    # --- 5 ERROR checks --------------------------------------------------
    schema_errors = check_schema(entries, schema)
    reciprocity_errors = check_dynamic_pair_reciprocity(entries, by_id)
    pair_member_errors = check_pair_member_resolvability(entries, by_id)
    alias_errors = check_alias_uniqueness(entries)
    ncp_errors, ncp_skipped = check_ncp_enum_closure(entries, ncp_valid)

    if ncp_skipped and not args.emit_json:
        print("INFO: ncp-enum check skipped (NCP schema unavailable)", file=sys.stderr)

    all_errors: list[Finding] = (
        schema_errors
        + reciprocity_errors
        + pair_member_errors
        + alias_errors
        + ncp_errors
    )

    # --- 3 WARNING checks ------------------------------------------------
    quad_warnings = check_quad_membership(entries, by_id)
    term_file_warnings = check_term_file_anchors(entries, _REPO_ROOT)
    unmapped_warnings = check_unmapped_headings(entries, _REPO_ROOT)

    all_warnings: list[Finding] = quad_warnings + term_file_warnings + unmapped_warnings

    # --- tally by check --------------------------------------------------
    by_check: dict[str, int] = {
        "schema": len(schema_errors),
        "reciprocity": len(reciprocity_errors),
        "pair_member": len(pair_member_errors),
        "alias-uniqueness": len(alias_errors),
        "ncp-enum": len(ncp_errors),
        "quad-membership": len(quad_warnings),
        "term_file-anchor": len(term_file_warnings),
        "unmapped-heading": len(unmapped_warnings),
    }

    # =====================================================================
    # Output
    # =====================================================================
    if args.emit_json:
        _json_output(all_errors, all_warnings, by_check)
    else:
        _human_output(all_errors, all_warnings, by_check, ncp_skipped)

    # =====================================================================
    # Exit code
    # =====================================================================
    if all_errors:
        sys.exit(1)
    if args.strict and all_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
