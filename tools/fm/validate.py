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

# ADR-0011 D.1/D.2: imported skill corpora live under skills/<vendor>-<slug>/
# and carry the L2 key `skill_source: "<vendor>@v<semver>"`.
VENDOR_PREFIXES = ("sc-", "superpowers-")
SKILL_SOURCE_RE = re.compile(r"^(superclaude|superpowers)@v\d+\.\d+\.\d+$")

# Task 094 ST-1 (T3 carry-forward from Task 092 PR #120 review A1): the
# `skill_kind` L2 key is a closed 9-value enum. See SKILLS.md §3.3.
SKILL_KIND_ENUM = frozenset({
    "domain", "tool", "orchestrator", "meta",
    "discipline", "workflow", "persona", "analysis", "agent-template",
})


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


def _check_skill_bundles(
    fm: dict, rel: str, repo_root: Path,
) -> list[Diagnostic]:
    """Validate skill_bundles_tools per ADR-0007.

    Emits:
      - F.B.5 when an entry is malformed (wrong type, missing tools/ prefix,
        contains '..', duplicated, or does not resolve to a tools/<slug>/ dir).
      - F.B.6 when a declared bundle's transitive dependency (per
        `_core.BUNDLE_DEPS`) is missing from the same list.
    """
    out: list[Diagnostic] = []
    if "skill_bundles_tools" not in fm:
        return out
    bundles = fm.get("skill_bundles_tools")
    if not isinstance(bundles, list):
        out.append(Diagnostic(
            rel, None, "ERROR", "F.B.5",
            "skill_bundles_tools MUST be a YAML list of strings",
        ))
        return out

    seen: set[str] = set()
    valid: list[str] = []
    for entry in bundles:
        if not isinstance(entry, str) or not entry:
            out.append(Diagnostic(
                rel, None, "ERROR", "F.B.5",
                f"skill_bundles_tools entry must be a non-empty string, got {entry!r}",
            ))
            continue
        if not entry.startswith("tools/"):
            out.append(Diagnostic(
                rel, None, "ERROR", "F.B.5",
                f"skill_bundles_tools entry {entry!r} MUST start with 'tools/'",
            ))
            continue
        if ".." in Path(entry).parts:
            out.append(Diagnostic(
                rel, None, "ERROR", "F.B.5",
                f"skill_bundles_tools entry {entry!r} contains '..' — path traversal forbidden",
            ))
            continue
        if entry in seen:
            out.append(Diagnostic(
                rel, None, "ERROR", "F.B.5",
                f"skill_bundles_tools entry {entry!r} is duplicated",
            ))
            continue
        seen.add(entry)
        if not (repo_root / entry).is_dir():
            out.append(Diagnostic(
                rel, None, "ERROR", "F.B.5",
                f"skill_bundles_tools entry {entry!r} does not resolve to an existing directory under repo root",
            ))
            continue
        valid.append(entry)

    # Transitive dependency closure (F.B.6).
    valid_set = set(valid)
    for entry in valid:
        for dep in _core.BUNDLE_DEPS.get(entry, ()):
            if dep not in valid_set:
                out.append(Diagnostic(
                    rel, None, "ERROR", "F.B.6",
                    f"skill_bundles_tools entry {entry!r} requires transitive bundle {dep!r}; add it to the list",
                ))
    return out


def _check_skill_source(fm: dict, rel: str) -> list[Diagnostic]:
    """Validate skill_source per ADR-0011.

    Emits:
      - F.B.8 when `skill_source` is set on a bare-slug (Agency-native) skill
        folder (ADR-0011 D.1 violation).
      - F.B.9 when `skill_source` is not a string matching
        `^(superclaude|superpowers)@v\\d+\\.\\d+\\.\\d+$` (ADR-0011 D.2 violation).

    Codes F.B.8/F.B.9 are used (not F.B.7/F.B.8 as the §10.2 design draft
    suggested) because F.B.7 is already in use by the task_list completion
    WARN check in `_check_body_for_type`; see friction-log.md FL1.
    """
    out: list[Diagnostic] = []
    if "skill_source" not in fm:
        return out  # absence is fine for Agency-native skills

    parts = rel.replace("\\", "/").split("/")
    folder = parts[1] if len(parts) >= 3 and parts[0] == "skills" else ""
    is_vendor_prefixed = folder.startswith(VENDOR_PREFIXES)
    if not is_vendor_prefixed:
        out.append(Diagnostic(
            rel, None, "ERROR", "F.B.8",
            "skill_source is reserved for vendor-prefixed imports "
            "(skills/{sc,superpowers}-<slug>/) per ADR-0011 D.1",
        ))

    value = fm.get("skill_source")
    if not isinstance(value, str) or not SKILL_SOURCE_RE.match(value):
        out.append(Diagnostic(
            rel, None, "ERROR", "F.B.9",
            f"skill_source value {value!r} does not match "
            f"'<vendor>@v<semver>' (e.g. 'superclaude@v4.3.0') per ADR-0011 D.2",
        ))
    return out


def _check_skill_readme(path: Path, rel: str) -> list[Diagnostic]:
    """Enforce SKILLS.md §9.6 Readme Audit: every skills/<slug>/ folder MUST
    carry a readme.md. Fired once per SKILL.md whose sibling readme.md is
    absent. CLAUDE.md §7 + SKILLS.md §2."""
    out: list[Diagnostic] = []
    parent = path.parent
    if (parent / "readme.md").is_file():
        return out
    skill_folder = parent.name
    out.append(Diagnostic(
        rel, None, "ERROR", "F.S.1",
        f"skill folder skills/{skill_folder}/ is missing required readme.md "
        f"(SKILLS.md §2 + §9.6; CLAUDE.md §7)",
    ))
    return out


def _check_skill_kind_enum(fm: dict, rel: str) -> list[Diagnostic]:
    """Validate skill_kind ∈ SKILL_KIND_ENUM per SKILLS.md §3.3.

    Emits:
      - F.B.11 when `skill_kind` is set but the value is not in the 9-value
        closed enum ratified by Task 094 ST-1 (T3 carry-forward from
        Task 092 PR #120 review A1).

    Absence of the key is permitted (some SKILL.md authors omit it pending
    classification); only out-of-enum values fail. Index routing depends on
    a valid value, so this is ERROR-tier.
    """
    out: list[Diagnostic] = []
    if "skill_kind" not in fm:
        return out
    value = fm.get("skill_kind")
    if not isinstance(value, str) or value not in SKILL_KIND_ENUM:
        sorted_enum = ", ".join(sorted(SKILL_KIND_ENUM))
        out.append(Diagnostic(
            rel, None, "ERROR", "F.B.11",
            f"skill_kind value {value!r} is not in the 9-value enum "
            f"{{{sorted_enum}}} (SKILLS.md §3.3; Task 094 ST-1)",
        ))
    return out


def _check_body_for_type(
    text: str, ontology: dict, type_for_keys: str, rel: str,
) -> list[Diagnostic]:
    """Apply SPEC §12 body-schema constraints for the file's type."""
    out: list[Diagnostic] = []
    body_schema = ontology["types"].get(type_for_keys, {}).get("body_schema") or {}
    for section_name, section_schema in body_schema.items():
        if section_name.startswith("_"):
            continue  # informational notes (e.g., "_note")
        body = _core.find_section_body(text, section_name)
        if body is None:
            # Heading absence is an F.4.2 ERROR; we don't double-count.
            continue
        for severity, code, message in _core.validate_section_body(
            body, section_schema,
        ):
            out.append(Diagnostic(
                rel, None, severity, code,
                f"section '## {section_name}': {message}",
            ))
        # F.B.7 task_list completion ↔ frontmatter status (informational WARN).
        completion_field = section_schema.get("completion_field")
        if (completion_field
                and section_schema.get("shape") == "task_list"
                and _core.detect_shape(body) == "task_list"):
            items = _core._list_items(body)
            if items and all(_core.TASK_LIST_RE.match(line)
                             and "[x]" in line.lower()
                             for line in body.splitlines()
                             if _core.TASK_LIST_RE.match(line)):
                fm = _core.parse_frontmatter(text, strict=False)
                actual = _core.str_val(fm, completion_field)
                if actual and actual != "done":
                    out.append(Diagnostic(
                        rel, None, "WARN", "F.B.7",
                        f"section '## {section_name}' all checked but "
                        f"{completion_field}={actual!r} (expected 'done')",
                    ))
    return out


def check_file(
    path: Path,
    repo_root: Path,
    ontology: dict,
    classification: _core.Classification | None = None,
    check_body: bool = False,
) -> list[Diagnostic]:
    if classification is None:
        classification = _core.classify_path(path, repo_root, ontology)
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

    # SPEC §12: opt-in per-section body schema check.
    if check_body:
        diags.extend(_check_body_for_type(text, ontology, type_for_keys, rel))

    # ADR-0007: skill_bundles_tools validation (only for SKILL.md files).
    if type_for_keys == "skill":
        diags.extend(_check_skill_bundles(fm, rel, repo_root))
        # ADR-0011: skill_source validation for imported corpora.
        diags.extend(_check_skill_source(fm, rel))
        # Task 094 ST-1: skill_kind closed-enum validation.
        diags.extend(_check_skill_kind_enum(fm, rel))
        # Task 093: SKILLS.md §9.6 readme-audit (F.S.1).
        diags.extend(_check_skill_readme(path, rel))

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


# ---- --type-check (Task 019 ST-5) -------------------------------------------


def _build_slug_index(repo_root: Path, ontology: dict
                      ) -> tuple[dict[str, dict], dict[tuple[str, str], dict],
                                  list[Diagnostic]]:
    """Return (any_index, by_type_index, parse_warnings).

    `any_index` maps slug → first entry (used for dangling-ref resolution
    when the caller doesn't care about type).
    `by_type_index` maps (slug, type) → entry, so reciprocity rules and
    task_id resolution can disambiguate when a slug is shared between
    a task.md and its sibling prompt.md.
    `parse_warnings` carries WARN-tier F.3.3 diagnostics for files whose
    leading `---` fence is present but whose YAML fails to parse — see
    `read_fm_with_diag` (Task 058).
    """
    any_index: dict[str, dict] = {}
    by_type: dict[tuple[str, str], dict] = {}
    warnings: list[Diagnostic] = []
    for path in _core.iter_operational_files(repo_root):
        cls = _core.classify_path(path, repo_root, ontology)
        if cls.expected_type is None:
            continue
        rel_path = path.resolve().relative_to(repo_root.resolve()).as_posix()
        fm, diag = _core.read_fm_with_diag(path, strict=False)
        if diag is not None:
            warnings.append(Diagnostic(
                rel_path, diag.line, diag.severity, diag.code, diag.message,
            ))
        if not fm:
            continue
        slug = _core.str_val(fm, "slug")
        if not slug:
            continue
        declared = _core.str_val(fm, "type") or cls.expected_type
        entry = {"path": rel_path, "type": declared, "fm": fm}
        by_type.setdefault((slug, declared), entry)
        any_index.setdefault(slug, entry)
    return any_index, by_type, warnings


def _build_task_id_index(by_type: dict[tuple[str, str], dict]) -> dict[str, str]:
    """Return {task_id: slug} for tasks that declare task_id."""
    out: dict[str, str] = {}
    for (slug, declared), entry in by_type.items():
        if declared != "task":
            continue
        tid = _core.str_val(entry["fm"], "task_id")
        if tid:
            out[tid] = slug
    return out


_LIST_REF_FIELDS = (
    "task_uses_prompts",
    "task_spawns_research",
    "task_spawns_prompts",
    "task_blocked_by",
    "task_supersedes",
    "task_superseded_by",
)


def _resolve_ref(ref: str, any_index: dict[str, dict],
                 task_id_index: dict[str, str]) -> str | None:
    """Resolve a slug-or-task-id reference to its canonical slug, or None."""
    if ref in any_index:
        return ref
    if ref in task_id_index:
        return task_id_index[ref]
    return None


def type_check(repo_root: Path, ontology: dict) -> list[Diagnostic]:
    """SPEC §5.1 + Task 019 ST-5: emit F.T.1 (dangling) and F.T.2 (reciprocity)
    diagnostics across the slug graph."""
    diags: list[Diagnostic] = []
    any_index, by_type, parse_warnings = _build_slug_index(repo_root, ontology)
    diags.extend(parse_warnings)
    task_id_index = _build_task_id_index(by_type)

    for (slug, declared), entry in by_type.items():
        fm = entry["fm"]
        path = entry["path"]
        for field in _LIST_REF_FIELDS:
            for ref in _core.str_list(fm, field):
                if not ref or ref.startswith("REPLACE"):
                    continue
                if _resolve_ref(ref, any_index, task_id_index) is None:
                    diags.append(Diagnostic(
                        path, None, "ERROR", "F.T.1",
                        f"dangling reference {field}={ref!r} (slug/task_id has no matching file)",
                    ))
        # Scalar reference fields.
        for field in ("prompt_relates_to_task", "prompt_spawned_from_research",
                       "research_executes_prompt"):
            ref = _core.str_val(fm, field)
            if not ref or ref.startswith("REPLACE"):
                continue
            if _resolve_ref(ref, any_index, task_id_index) is None:
                diags.append(Diagnostic(
                    path, None, "ERROR", "F.T.1",
                    f"dangling reference {field}={ref!r} (slug/task_id has no matching file)",
                ))

    # Reciprocity rules.
    for rule in ontology.get("reciprocity", {}).get("rules", []):
        fwd_type = rule["forward"]["type"]
        fwd_field = rule["forward"]["field"]
        back_type = rule["back"]["type"]
        back_field = rule["back"]["field"]
        back_scalar = rule["back"].get("scalar", False)

        for (slug, declared), entry in by_type.items():
            if declared != fwd_type:
                continue
            for ref in _core.str_list(entry["fm"], fwd_field):
                if not ref or ref.startswith("REPLACE"):
                    continue
                resolved = _resolve_ref(ref, any_index, task_id_index)
                if resolved is None:
                    continue  # dangling; F.T.1 covers it
                target = by_type.get((resolved, back_type))
                if target is None:
                    continue
                if back_scalar:
                    back_val = _core.str_val(target["fm"], back_field)
                    # Empty string is "shared / general" (used by multiple
                    # forwards); skip the reciprocity assertion for that case.
                    if back_val == "":
                        continue
                    matched = back_val == slug
                else:
                    matched = slug in _core.str_list(target["fm"], back_field)
                if not matched:
                    diags.append(Diagnostic(
                        target["path"], None, "ERROR", "F.T.2",
                        f"reciprocity break: {entry['path']} declares "
                        f"{fwd_field} contains {ref!r} but {back_field} on "
                        f"this file does not name back to {slug!r}",
                    ))
    return diags


# ---- --explain (Task 019 ST-5) ----------------------------------------------


def _load_explanations(repo_root: Path) -> dict:
    candidates = [
        repo_root / "maintenance" / "schemas" / "diagnostic-explanations.json",
        Path(__file__).resolve().parents[1].parent
            / "maintenance" / "schemas" / "diagnostic-explanations.json",
    ]
    for p in candidates:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return {"codes": {}}


def _annotate(d: Diagnostic, explanations: dict) -> str:
    code = explanations.get("codes", {}).get(d.code)
    base = d.render()
    if not code:
        return base
    trailer = (
        f"  what: {code['what']}\n"
        f"  why:  {code['why']}\n"
        f"  fix:  {code['fix']}"
    )
    return f"{base}\n{trailer}"


# ---- --baseline (Task 019 ST-5) ---------------------------------------------


def _diags_for_baseline(ref: str, paths: list[Path], repo_root: Path,
                        ontology: dict, *, check_body: bool) -> set[tuple]:
    """Return {(path, line, code, message)} for the snapshot at <ref>."""
    import subprocess
    out: set[tuple] = set()
    for path in paths:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
        result = subprocess.run(
            ["git", "show", f"{ref}:{rel}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            continue
        # Run check_file against an in-memory snapshot via a temp file.
        import tempfile
        with tempfile.NamedTemporaryFile(
                "w", suffix=".md", dir=repo_root, delete=False, encoding="utf-8") as tf:
            tf.write(result.stdout)
            tmp_path = Path(tf.name)
        try:
            cls = _core.classify_path(path, repo_root, ontology)
            if cls.expected_type is None:
                continue
            for d in check_file(tmp_path, repo_root, ontology,
                                classification=cls, check_body=check_body):
                out.add((rel, d.line, d.code, d.message))
        finally:
            tmp_path.unlink(missing_ok=True)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-validate", add_help=True)
    p.add_argument("paths", nargs="*")
    p.add_argument("--scope", default=None,
                   help="comma-separated subset of operational roots")
    p.add_argument("--strict", action="store_true",
                   help="promote WARN to non-zero exit code")
    p.add_argument("--check-body", action="store_true",
                   help="also enforce SPEC §12 per-section body schemas "
                        "(opt-in for v1; default off)")
    p.add_argument("--type-check", action="store_true",
                   help="emit F.T.* diagnostics for dangling slug references "
                        "and reciprocity breaks (Task 019 ST-5)")
    p.add_argument("--explain", action="store_true",
                   help="annotate each diagnostic with what/why/fix from "
                        "maintenance/schemas/diagnostic-explanations.json")
    p.add_argument("--baseline", default=None, metavar="GIT_REF",
                   help="emit only diagnostics introduced since <GIT_REF>")
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
    walked: list[Path] = []
    for path in _iter_targets(args.paths, repo_root, scope):
        cls = _core.classify_path(path, repo_root, ontology)
        if cls.expected_type is None:
            continue
        checked += 1
        walked.append(path)
        diags.extend(check_file(path, repo_root, ontology,
                                classification=cls,
                                check_body=args.check_body))

    if args.type_check:
        diags.extend(type_check(repo_root, ontology))

    if args.baseline:
        baseline_set = _diags_for_baseline(
            args.baseline, walked, repo_root, ontology,
            check_body=args.check_body,
        )
        diags = [
            d for d in diags
            if (d.path, d.line, d.code, d.message) not in baseline_set
        ]

    # PRE_COMMIT.md §7.B per-rule waivers (Task 037 ST-3).
    try:
        waivers = _core.load_waivers(repo_root)
    except _core.Diag as exc:
        print(f"fm-validate: waiver load failed: {exc}", file=sys.stderr)
        return 1
    if waivers:
        import datetime as _dt
        diags = _core.apply_waivers(
            diags, waivers, today=_dt.date.today().isoformat(),
        )

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
        explanations = _load_explanations(repo_root) if args.explain else {"codes": {}}
        for d in diags:
            line = _annotate(d, explanations) if args.explain else d.render()
            print(line, file=sys.stderr)
        print(f"Checked {checked} files; {len(diags)} diagnostic(s).")

    if error_count > 0:
        return 1
    if args.strict and warn_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
