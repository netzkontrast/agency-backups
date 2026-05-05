#!/usr/bin/env python3
"""fm-validate — flexible required-only frontmatter + heading validator.

Spec anchors: F.5.1, F.3.1–F.3.4, F.4.1–F.4.3.

Usage:
    python3 tools/fm/validate.py [PATH ...] \\
            [--scope=tasks,prompts,research,skills,maintenance,tools,templates] \\
            [--strict] [--format=text|json]

Exit:
    0 — no ERROR diagnostics
    1 — at least one ERROR diagnostic (or any WARN under --strict)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

# Allow running as `python3 tools/fm/validate.py` (script mode).
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

Diagnostic = _core.Diagnostic
Diag = _core.Diag

SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def _classify(path: Path, repo_root: Path, ontology: dict) -> _core.Classification:
    return _core.classify_path(path, repo_root, ontology)


def _expected_required_keys(ontology: dict, type_name: str) -> list[str]:
    return list(ontology["types"].get(type_name, {}).get("required_keys", []))


def _expected_required_headings(ontology: dict, type_name: str) -> list[str]:
    return list(ontology["types"].get(type_name, {}).get("required_headings", []))


def _all_known_required_keys(ontology: dict) -> set[str]:
    keys: set[str] = set(ontology.get("l1_required", []))
    for t in ontology["types"].values():
        keys.update(t.get("required_keys", []))
        keys.update(t.get("recommended_keys", []))
    return keys


def check_file(
    path: Path,
    repo_root: Path,
    ontology: dict,
) -> list[Diagnostic]:
    classification = _classify(path, repo_root, ontology)
    if classification.expected_type is None:
        return []

    rel = str(path.resolve().relative_to(repo_root.resolve())) \
        if path.is_absolute() else str(path)

    text = path.read_text(encoding="utf-8")

    # Frontmatter present?
    if not _core.FRONTMATTER_RE.match(text):
        return [Diagnostic(rel, None, "ERROR", "F.3.3",
                           "missing frontmatter block (no leading '---' fenced YAML)")]

    try:
        fm = _core.parse_frontmatter(text, strict=True)
    except Diag as e:
        return [Diagnostic(rel, None, "ERROR", "F.3.3", str(e))]

    diags: list[Diagnostic] = []

    # Determine the file's effective type (for type-specific checks).
    declared_type = _core.str_val(fm, "type")
    permitted = {classification.expected_type, *classification.alt_types}
    type_for_keys = classification.expected_type
    if declared_type:
        if declared_type in permitted:
            type_for_keys = declared_type
        elif declared_type not in ontology.get("type_values", []):
            diags.append(Diagnostic(
                rel, None, "ERROR", "F.3.3",
                f"type {declared_type!r} is not in the closed set {ontology['type_values']}",
            ))
        else:
            diags.append(Diagnostic(
                rel, None, "ERROR", "F.3.3",
                f"type {declared_type!r} disagrees with path-expected type "
                f"{sorted(permitted)!r}",
            ))

    # Required L1+L2 keys.
    required = _expected_required_keys(ontology, type_for_keys)
    missing = [k for k in required if k not in fm]
    if missing:
        # Split into L1 vs L2 anchor.
        l1 = set(ontology.get("l1_required", []))
        l1_missing = [k for k in missing if k in l1]
        l2_missing = [k for k in missing if k not in l1]
        if l1_missing:
            diags.append(Diagnostic(
                rel, None, "ERROR", "F.3.1",
                f"missing L1 keys {sorted(l1_missing)}",
            ))
        if l2_missing:
            diags.append(Diagnostic(
                rel, None, "ERROR", "F.3.2",
                f"missing L2 keys {sorted(l2_missing)} (type={type_for_keys})",
            ))

    # status enum.
    status = _core.str_val(fm, "status")
    if status and status not in ontology.get("status_values", []):
        diags.append(Diagnostic(
            rel, None, "ERROR", "F.3.3",
            f"status {status!r} is not in {ontology['status_values']}",
        ))

    # slug pattern.
    slug = _core.str_val(fm, "slug")
    if slug and not SLUG_RE.match(slug):
        diags.append(Diagnostic(
            rel, None, "ERROR", "F.3.3",
            f"slug {slug!r} contains characters outside [a-z0-9-]",
        ))

    # did-you-mean: unknown keys within Levenshtein distance 1 of a required key.
    known = _all_known_required_keys(ontology)
    # Treat the keys from the file's own type's required+recommended as "known"
    # plus L0 reserved (tags, aliases, cssclasses) — these are L0 per language-spec §4.2.
    l0_reserved = {"tags", "aliases", "cssclasses"}
    type_keys = set(_expected_required_keys(ontology, type_for_keys))
    type_keys.update(ontology["types"].get(type_for_keys, {}).get("recommended_keys", []))
    for fm_key in fm.keys():
        if fm_key in type_keys or fm_key in l0_reserved:
            continue
        # Suggest only when the unknown key is within distance 1 of a required key.
        for req in known:
            if fm_key == req:
                continue
            if _core.levenshtein(fm_key, req) == 1:
                diags.append(Diagnostic(
                    rel, None, "ERROR", "F.3.4",
                    f"unknown key {fm_key!r} — did you mean {req!r}?",
                ))
                break

    # Required headings.
    _, body = _core.split_frontmatter_and_body(text)
    actual_headings = {_core.normalise_heading(h) for _, h in _core.iter_h2(body)}
    for required_heading in _expected_required_headings(ontology, type_for_keys):
        norm = _core.normalise_heading(required_heading)
        if norm not in actual_headings:
            diags.append(Diagnostic(
                rel, None, "ERROR", "F.4.2",
                f"missing required heading '## {required_heading}'",
            ))

    return diags


def _iter_targets(args_paths: list[str], repo_root: Path,
                  scope: list[str] | None) -> Iterable[Path]:
    if args_paths:
        for raw in args_paths:
            p = Path(raw)
            if p.is_dir():
                yield from p.rglob("*.md")
            elif p.is_file() and p.suffix == ".md":
                yield p
        return
    yield from _core.iter_operational_files(repo_root, scope=scope)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-validate", add_help=True)
    p.add_argument("paths", nargs="*")
    p.add_argument("--scope", default=None,
                   help="comma-separated subset of operational roots")
    p.add_argument("--strict", action="store_true",
                   help="promote WARN to non-zero exit code")
    p.add_argument("--format", choices=("text", "json"), default="text")
    args = p.parse_args(argv)

    repo_root = _core.repo_root_from_cwd()
    ontology = _core.load_ontology(repo_root)

    scope: list[str] | None = (
        [s.strip() for s in args.scope.split(",") if s.strip()]
        if args.scope else None
    )

    diags: list[Diagnostic] = []
    checked = 0
    for path in _iter_targets(args.paths, repo_root, scope):
        cls = _classify(path, repo_root, ontology)
        if cls.expected_type is None:
            continue
        checked += 1
        diags.extend(check_file(path, repo_root, ontology))

    error_count = sum(1 for d in diags if d.severity == "ERROR")
    warn_count = sum(1 for d in diags if d.severity == "WARN")

    if args.format == "json":
        print(json.dumps({
            "checked": checked,
            "diagnostics": [d.to_json() for d in diags],
            "errors": error_count,
            "warnings": warn_count,
        }, indent=2))
    else:
        for d in diags:
            print(d.render(), file=sys.stderr)
        print(f"Checked {checked} files; {len(diags)} diagnostic(s).")

    if error_count > 0:
        return 1
    if args.strict and warn_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
