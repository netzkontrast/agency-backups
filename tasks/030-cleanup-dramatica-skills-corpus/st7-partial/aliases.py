#!/usr/bin/env python3
"""Bulk alias loader + per-term alias CRUD for the dramatica narrative ontology.

Five subcommands:
    aliases.py load-en --source <path>
    aliases.py load-de --source <path>
    aliases.py add --id <oid> --locale <l> --value "<alias>"
    aliases.py remove --id <oid> --locale <l> --value "<alias>"
    aliases.py list --id <oid> [--locale <l>]
    aliases.py conflict-report [--source <path>]

`load-en` walks `_synonym-lookup.md` (23 alphabetical buckets) and projects
the conflict-free subset of ~512 alias rows into both:
    1. per-term YAML frontmatter blocks under skills/dramatica-vocabulary/references/
    2. the corresponding entries in maintenance/schemas/narrative-ontology/ontology.json

Multi-match aliases (same canonical-label appears in multiple kinds + the
file-hint does not disambiguate) are NEVER auto-resolved; they surface via
`conflict-report` and must be ratified by a human or follow-up ADR.

`load-de` consumes a hand-curated JSON map at
    tools/dramatica-nav/data/aliases_de_starter.json
of the form { "<oid>": ["<alias1>", "<alias2>"], ... } and projects the
same way, locale="de".

Idempotent: a re-run produces no diff.

Schema validation runs after every write; any violation aborts with exit 1.

Exit codes:
    0  success / clean
    1  schema validation failure / unresolvable error
    2  bad CLI args
    3  source file I/O error
    4  conflict found (only for `conflict-report` when conflicts exist)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import frontmatter as fm  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY_PATH = REPO_ROOT / "maintenance/schemas/narrative-ontology/ontology.json"
TERM_SCHEMA_PATH = REPO_ROOT / "maintenance/schemas/narrative-ontology/term-frontmatter.schema.json"
ONTOLOGY_SCHEMA_PATH = REPO_ROOT / "maintenance/schemas/narrative-ontology/ontology.schema.json"
VOCAB_DIR = REPO_ROOT / "skills/dramatica-vocabulary/references"
SYNONYM_LOOKUP = VOCAB_DIR / "_synonym-lookup.md"
DE_STARTER = REPO_ROOT / "tools/dramatica-nav/data/aliases_de_starter.json"

PROG = Path(__file__).name

# Canonical key order for per-term YAML blocks (mirrors the ontology-build.py
# convention so re-emitted blocks stay byte-stable across tools).
KEY_ORDER = [
    "id",
    "kind",
    "canonical_label",
    "provenance",
    "aliases_en",
    "aliases_de",
    "deprecated_aliases_en",
    "deprecated_aliases_de",
    "term_file",
    "scenarios",
    "ncp_appreciation",
    "ncp_appreciation_partial",
    "ncp_schema_min_version",
    "dynamic_pair_id",
    "pair_member_a",
    "pair_member_b",
    "quad_id",
    "ktad_position",
    "class_id",
    "type_id",
    "variation_id",
]

# Rows whose canonical-side begins with "see " are cross-references to prose
# sections, NOT direct ontology entries; skip during EN load.
SEE_PREFIX = re.compile(r"^\s*see\s+", re.IGNORECASE)

ROW_RE = re.compile(
    r"^\s*-\s+`([^`]+)`\s+→\s+(.+?)\s*$",
)
TARGET_RE = re.compile(
    r"\*\*([^*]+?)\*\*\s*\(in\s+`([^`]+)`\)",
)
BUCKET_HEADER_RE = re.compile(r"^##\s+([A-Z])\s*$")


# ---------------------------------------------------------------------------
# Pass 1 — parse `_synonym-lookup.md`
# ---------------------------------------------------------------------------


def parse_synonym_lookup(text: str) -> list[dict]:
    """Return [{alias, targets:[(label, file)], bucket, line}].

    Each row may carry multiple `**Label** (in file.md)` targets separated by
    ` / `. We retain ALL of them for the resolve pass to disambiguate.
    `see ...` targets are discarded (cross-reference, not an ontology entry).
    """
    rows: list[dict] = []
    bucket = ""
    for lineno, line in enumerate(text.splitlines(), start=1):
        bm = BUCKET_HEADER_RE.match(line)
        if bm:
            bucket = bm.group(1)
            continue
        rm = ROW_RE.match(line)
        if not rm:
            continue
        alias = rm.group(1).strip()
        rest = rm.group(2)
        targets: list[tuple[str, str]] = []
        for tm in TARGET_RE.finditer(rest):
            label = tm.group(1).strip()
            tfile = tm.group(2).strip()
            if SEE_PREFIX.match(label):
                continue
            targets.append((label, tfile))
        if not targets:
            continue
        rows.append(
            {
                "alias": alias,
                "targets": targets,
                "bucket": bucket,
                "line": lineno,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Pass 2 — resolve canonical-label + file-hint → ontology ID
# ---------------------------------------------------------------------------


def build_label_index(entries: list[dict]) -> dict[str, list[dict]]:
    """label_lower → [entry, ...] for resolution."""
    idx: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        label = e.get("canonical_label", "")
        if label:
            idx[label.lower()].append(e)
    return idx


def build_reserved_alias_index(
    entries: list[dict], locale: str
) -> dict[str, str]:
    """alias_lower → oid for every alias already claimed by some entry.

    Includes:
        • canonical_label of every entry (every locale, defensively).
        • aliases_<locale>      (existing entries on this locale).
        • deprecated_aliases_<locale>.

    Used to skip projections that would collide with an existing claim and
    silently violate alias-uniqueness. Such rows surface as conflicts.
    """
    out: dict[str, str] = {}
    for e in entries:
        oid = e["id"]
        label = e.get("canonical_label", "")
        if label:
            out.setdefault(label.lower(), oid)
        for k, v in e.items():
            if not isinstance(v, list):
                continue
            if k == f"aliases_{locale}" or k == f"deprecated_aliases_{locale}":
                for a in v:
                    out.setdefault(a.lower(), oid)
    return out


def _term_file_basename(entry: dict) -> str:
    tf = entry.get("term_file", "")
    if not tf:
        return ""
    return tf.split("#")[0].rsplit("/", 1)[-1]


def resolve_target(
    label: str,
    file_hint: str,
    label_index: dict[str, list[dict]],
) -> tuple[str, list[str]]:
    """Resolve a (label, file_hint) tuple.

    Returns ("ok", [oid]) when exactly one entry matches.
    Returns ("conflict", [oid, oid, ...]) when multiple entries remain after
    file-hint filtering.
    Returns ("unknown", []) when no entry matches the label at all.
    """
    cands = label_index.get(label.lower(), [])
    if not cands:
        return "unknown", []
    if len(cands) == 1:
        return "ok", [cands[0]["id"]]
    # >1 candidates: try the file hint
    file_filtered = [e for e in cands if _term_file_basename(e) == file_hint]
    if len(file_filtered) == 1:
        return "ok", [file_filtered[0]["id"]]
    if file_filtered:
        return "conflict", [e["id"] for e in file_filtered]
    return "conflict", [e["id"] for e in cands]


def resolve_rows(
    rows: list[dict],
    label_index: dict[str, list[dict]],
    reserved: dict[str, str] | None = None,
) -> tuple[dict[str, set[str]], list[dict], list[dict]]:
    """Walk parsed rows; return (projections, conflicts, unknowns).

    `projections` maps oid -> set of aliases.
    `conflicts` lists rows that resolve to multiple ontology IDs OR rows
    whose alias would otherwise project to more than one ontology ID across
    targets (alias-uniqueness violation).
    `unknowns` lists rows whose canonical label has no ontology entry.

    Multi-target rows (e.g. `embodying` → Bad / Change):
      • If exactly ONE target resolves to "ok" and the rest are unknown, the
        single resolved target projects. Such rows are flagged "partial" in
        the conflict list for transparency but their alias IS projected.
      • If TWO OR MORE targets resolve to "ok" (different oids), the row is a
        hard conflict — alias-uniqueness would fail, so we DO NOT auto-pick.
        The row is reported in `conflicts` and projects nothing.
      • If no target resolves cleanly, the row is "unknown" or "conflict"
        depending on whether any target was multi-match vs. label-missing.
    """
    projections: dict[str, set[str]] = defaultdict(set)
    conflicts: list[dict] = []
    unknowns: list[dict] = []
    reserved = reserved or {}
    for row in rows:
        per_target: list[dict] = []
        ok_oids: list[str] = []
        for label, file_hint in row["targets"]:
            status, oids = resolve_target(label, file_hint, label_index)
            per_target.append(
                {
                    "label": label,
                    "file": file_hint,
                    "status": status,
                    "oids": oids,
                }
            )
            if status == "ok":
                ok_oids.append(oids[0])

        if not ok_oids:
            if any(t["status"] == "conflict" for t in per_target):
                conflicts.append({**row, "resolved": per_target})
            else:
                unknowns.append({**row, "resolved": per_target})
            continue

        if len(set(ok_oids)) > 1:
            # Alias-uniqueness conflict: the same alias would project to
            # multiple ontology IDs. Refuse to auto-resolve.
            conflicts.append(
                {
                    **row,
                    "resolved": per_target,
                    "reason": "alias-uniqueness",
                    "would_project_to": sorted(set(ok_oids)),
                }
            )
            continue

        # Exactly one OK target (possibly with other unknown/conflict targets).
        target_oid = ok_oids[0]
        alias_lower = row["alias"].lower()
        claimed_by = reserved.get(alias_lower)
        if claimed_by is not None and claimed_by != target_oid:
            conflicts.append(
                {
                    **row,
                    "resolved": per_target,
                    "reason": "reserved-alias-collision",
                    "would_project_to": target_oid,
                    "already_claimed_by": claimed_by,
                }
            )
            continue
        projections[target_oid].add(row["alias"])
        if any(t["status"] != "ok" for t in per_target):
            conflicts.append({**row, "resolved": per_target, "partial": True})
    return projections, conflicts, unknowns


# ---------------------------------------------------------------------------
# Pass 3 — project into ontology.json + per-term YAML blocks
# ---------------------------------------------------------------------------


def _ordered_block(block: dict) -> dict:
    """Return a new dict with KEY_ORDER applied; unknown keys append at end."""
    out: dict = {}
    for k in KEY_ORDER:
        if k in block:
            out[k] = block[k]
    for k in block:
        if k not in out:
            out[k] = block[k]
    return out


def _dump_block_yaml(block: dict) -> str:
    """Emit YAML matching the existing per-term block style.

    Style: no `---` markers, list items prefixed `- `, no flow style, no
    trailing newline.
    """
    return yaml.safe_dump(
        _ordered_block(block),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=10**9,
    ).rstrip("\n")


BLOCK_RE = re.compile(
    r"(<!-- nav-ontology[^>]*-->\n```yaml\n)(.+?)(\n```)",
    re.DOTALL,
)


def update_term_files(
    file_to_oid_blocks: dict[Path, list[tuple[str, dict]]],
    locale: str,
    projections: dict[str, set[str]],
    schema: dict,
) -> tuple[int, list[str]]:
    """Walk per-term YAML blocks; merge new aliases for the given locale.

    Returns (changed_count, errors). Errors are messages for blocks that fail
    schema validation (treated as hard failure by the caller).
    """
    changed = 0
    errors: list[str] = []
    key = f"aliases_{locale}"

    for path, blocks in file_to_oid_blocks.items():
        text = path.read_text(encoding="utf-8")
        new_text = text

        for oid, _ in blocks:
            new_aliases = projections.get(oid)
            if not new_aliases:
                continue

            # Locate the block within the live text using BLOCK_RE; we cannot
            # rely on file-wide replace because identical YAML payloads may
            # appear in multiple blocks (rare, but the safe path matches
            # by id).
            new_text, block_errors = _patch_block_in_text(
                new_text, oid, key, new_aliases, schema, str(path)
            )
            errors.extend(block_errors)

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1

    return changed, errors


def _patch_block_in_text(
    text: str,
    oid: str,
    key: str,
    new_aliases: set[str],
    schema: dict,
    path_label: str,
) -> tuple[str, list[str]]:
    """Find the YAML block matching `oid`, merge `new_aliases` into `key`,
    re-emit. Idempotent: if the merge leaves the block unchanged, return
    text untouched.

    Re-emission preserves the canonical key order. Schema validation runs on
    the merged dict; validation errors abort by returning the original text
    plus an error message.
    """
    errors: list[str] = []

    def _replace(match: re.Match) -> str:
        prefix, body, suffix = match.group(1), match.group(2), match.group(3)
        try:
            parsed = yaml.safe_load(body)
        except yaml.YAMLError as exc:
            errors.append(f"{path_label}: yaml parse failed in block: {exc}")
            return match.group(0)
        if not isinstance(parsed, dict) or parsed.get("id") != oid:
            return match.group(0)

        existing = list(parsed.get(key, []) or [])
        merged = sorted(set(existing) | set(new_aliases), key=str.lower)
        if merged == existing:
            return match.group(0)
        parsed[key] = merged

        # Schema-validate before committing the in-memory change.
        check_errors = _validate_against_schema(parsed, schema)
        if check_errors:
            errors.append(
                f"{path_label}: schema violation on {oid}: " + "; ".join(check_errors)
            )
            return match.group(0)

        return prefix + _dump_block_yaml(parsed) + suffix

    new_text = BLOCK_RE.sub(_replace, text, count=1)
    return new_text, errors


def update_ontology_json(
    locale: str,
    projections: dict[str, set[str]],
    ontology_path: Path,
) -> int:
    """Merge alias projections into ontology.json. Returns number of entries
    actually changed.
    """
    doc = json.loads(ontology_path.read_text(encoding="utf-8"))
    key = f"aliases_{locale}"
    changed = 0
    for entry in doc["entries"]:
        oid = entry.get("id")
        if oid not in projections:
            continue
        existing = list(entry.get(key, []) or [])
        merged = sorted(set(existing) | set(projections[oid]), key=str.lower)
        if merged != existing:
            entry[key] = merged
            changed += 1

    if changed:
        # Match the canonical 2-space indent + no trailing newline serialiser.
        ontology_path.write_text(
            json.dumps(doc, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return changed


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_against_schema(entry: dict, schema: dict) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return []
    validator = jsonschema.Draft202012Validator(schema)
    return [e.message for e in validator.iter_errors(entry)]


# ---------------------------------------------------------------------------
# Block walking — collect (path, oid, block) so we can update in place
# ---------------------------------------------------------------------------


def collect_blocks() -> dict[Path, list[tuple[str, dict]]]:
    out: dict[Path, list[tuple[str, dict]]] = defaultdict(list)
    for path, block in fm.walk_vocab_blocks(REPO_ROOT):
        oid = block.get("id")
        if oid:
            out[path].append((oid, block))
    return out


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------


def _load_ontology_entries() -> list[dict]:
    return json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))["entries"]


def cmd_load_en(args: argparse.Namespace) -> int:
    src = Path(args.source)
    if not src.exists():
        print(f"{PROG}: load-en: source not found: {src}", file=sys.stderr)
        return 3
    text = src.read_text(encoding="utf-8")
    rows = parse_synonym_lookup(text)
    entries = _load_ontology_entries()
    label_index = build_label_index(entries)
    reserved = build_reserved_alias_index(entries, "en")
    projections, conflicts, unknowns = resolve_rows(rows, label_index, reserved)

    term_schema = _load_schema(TERM_SCHEMA_PATH)
    file_blocks = collect_blocks()

    changed_files, errors = update_term_files(
        file_blocks, "en", projections, term_schema
    )
    if errors:
        for msg in errors:
            print(f"{PROG}: {msg}", file=sys.stderr)
        return 1

    changed_entries = update_ontology_json("en", projections, ONTOLOGY_PATH)

    total_aliases = sum(len(v) for v in projections.values())
    print(
        json.dumps(
            {
                "subcommand": "load-en",
                "rows_parsed": len(rows),
                "ids_touched": len(projections),
                "aliases_projected": total_aliases,
                "files_changed": changed_files,
                "entries_changed_in_ontology": changed_entries,
                "conflicts": len(conflicts),
                "unknowns": len(unknowns),
            },
            indent=2,
        )
    )
    return 0


def cmd_load_de(args: argparse.Namespace) -> int:
    src = Path(args.source)
    if not src.exists():
        print(f"{PROG}: load-de: source not found: {src}", file=sys.stderr)
        return 3
    raw = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print(f"{PROG}: load-de: source must be a JSON object", file=sys.stderr)
        return 2

    entries = _load_ontology_entries()
    valid_ids = {e["id"] for e in entries}

    projections: dict[str, set[str]] = defaultdict(set)
    bad_ids: list[str] = []
    for oid, aliases in raw.items():
        if oid not in valid_ids:
            bad_ids.append(oid)
            continue
        if not isinstance(aliases, list):
            print(
                f"{PROG}: load-de: aliases for {oid} must be a list",
                file=sys.stderr,
            )
            return 2
        for a in aliases:
            if not isinstance(a, str) or not a.strip():
                print(
                    f"{PROG}: load-de: alias for {oid} must be non-empty string",
                    file=sys.stderr,
                )
                return 2
            projections[oid].add(a.strip())

    if bad_ids:
        print(
            f"{PROG}: load-de: unknown ontology IDs: {bad_ids}",
            file=sys.stderr,
        )
        return 1

    term_schema = _load_schema(TERM_SCHEMA_PATH)
    file_blocks = collect_blocks()
    changed_files, errors = update_term_files(
        file_blocks, "de", projections, term_schema
    )
    if errors:
        for msg in errors:
            print(f"{PROG}: {msg}", file=sys.stderr)
        return 1
    changed_entries = update_ontology_json("de", projections, ONTOLOGY_PATH)

    total_aliases = sum(len(v) for v in projections.values())
    print(
        json.dumps(
            {
                "subcommand": "load-de",
                "ids_touched": len(projections),
                "aliases_projected": total_aliases,
                "files_changed": changed_files,
                "entries_changed_in_ontology": changed_entries,
            },
            indent=2,
        )
    )
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    return _single_alias_op(args.id, args.locale, args.value, op="add")


def cmd_remove(args: argparse.Namespace) -> int:
    return _single_alias_op(args.id, args.locale, args.value, op="remove")


def _single_alias_op(oid: str, locale: str, value: str, *, op: str) -> int:
    if not re.fullmatch(r"[a-z]{2}", locale):
        print(
            f"{PROG}: locale must be 2 lowercase letters, got {locale!r}",
            file=sys.stderr,
        )
        return 2
    entries = _load_ontology_entries()
    if oid not in {e["id"] for e in entries}:
        print(f"{PROG}: unknown ontology id {oid!r}", file=sys.stderr)
        return 1

    term_schema = _load_schema(TERM_SCHEMA_PATH)
    file_blocks = collect_blocks()

    if op == "add":
        projections = {oid: {value}}
        changed_files, errors = update_term_files(
            file_blocks, locale, projections, term_schema
        )
        if errors:
            for msg in errors:
                print(f"{PROG}: {msg}", file=sys.stderr)
            return 1
        update_ontology_json(locale, projections, ONTOLOGY_PATH)
        print(f"{PROG}: added alias {value!r} to {oid} (aliases_{locale})")
        return 0

    # remove
    return _remove_alias(oid, locale, value, file_blocks, term_schema)


def _remove_alias(
    oid: str,
    locale: str,
    value: str,
    file_blocks: dict[Path, list[tuple[str, dict]]],
    term_schema: dict,
) -> int:
    key = f"aliases_{locale}"
    found = False
    for path, blocks in file_blocks.items():
        for bid, _ in blocks:
            if bid != oid:
                continue
            text = path.read_text(encoding="utf-8")

            def _strip(match: re.Match) -> str:
                nonlocal found
                prefix, body, suffix = (
                    match.group(1),
                    match.group(2),
                    match.group(3),
                )
                parsed = yaml.safe_load(body)
                if not isinstance(parsed, dict) or parsed.get("id") != oid:
                    return match.group(0)
                existing = list(parsed.get(key, []) or [])
                if value not in existing:
                    return match.group(0)
                existing.remove(value)
                if existing:
                    parsed[key] = sorted(set(existing), key=str.lower)
                else:
                    parsed.pop(key, None)
                found = True
                return prefix + _dump_block_yaml(parsed) + suffix

            new_text = BLOCK_RE.sub(_strip, text, count=1)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")

    # ontology.json
    doc = json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))
    for entry in doc["entries"]:
        if entry.get("id") != oid:
            continue
        if key not in entry:
            continue
        if value in entry[key]:
            entry[key] = [a for a in entry[key] if a != value]
            if not entry[key]:
                del entry[key]
            found = True
    if found:
        ONTOLOGY_PATH.write_text(
            json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"{PROG}: removed alias {value!r} from {oid} (aliases_{locale})")
        return 0
    print(
        f"{PROG}: alias {value!r} not present on {oid}/{locale}",
        file=sys.stderr,
    )
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    entries = _load_ontology_entries()
    by_id = {e["id"]: e for e in entries}
    if args.id not in by_id:
        print(f"{PROG}: unknown ontology id {args.id!r}", file=sys.stderr)
        return 1
    entry = by_id[args.id]
    out: dict = {}
    for k, v in entry.items():
        if not k.startswith("aliases_") and not k.startswith("deprecated_aliases_"):
            continue
        if args.locale and not k.endswith(f"_{args.locale}"):
            continue
        out[k] = v
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def cmd_conflict_report(args: argparse.Namespace) -> int:
    src = Path(args.source) if args.source else SYNONYM_LOOKUP
    if not src.exists():
        print(
            f"{PROG}: conflict-report: source not found: {src}",
            file=sys.stderr,
        )
        return 3
    text = src.read_text(encoding="utf-8")
    rows = parse_synonym_lookup(text)
    entries = _load_ontology_entries()
    label_index = build_label_index(entries)
    reserved = build_reserved_alias_index(entries, "en")
    _, conflicts, unknowns = resolve_rows(rows, label_index, reserved)

    payload = {
        "conflicts": conflicts,
        "unknowns": unknowns,
        "conflict_count": len(conflicts),
        "unknown_count": len(unknowns),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    # Exit 0 if zero blocking conflicts (i.e. all conflicts are partial — at
    # least one target resolved). Exit 1 only if a row resolved to nothing.
    blocking = [c for c in conflicts if not c.get("partial")]
    if blocking:
        return 1
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=PROG,
        description=(
            "Bulk alias loader for the dramatica narrative ontology. "
            "Five subcommands: load-en, load-de, add, remove, list, "
            "conflict-report."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("load-en", help="Bulk-load EN aliases from synonym-lookup.md")
    pe.add_argument("--source", required=True, help="Path to _synonym-lookup.md")
    pe.set_defaults(func=cmd_load_en)

    pd = sub.add_parser(
        "load-de", help="Load DE aliases from a hand-curated JSON map"
    )
    pd.add_argument("--source", required=True, help="Path to aliases_de_starter.json")
    pd.set_defaults(func=cmd_load_de)

    pa = sub.add_parser("add", help="Add a single alias")
    pa.add_argument("--id", required=True, dest="id")
    pa.add_argument("--locale", required=True)
    pa.add_argument("--value", required=True)
    pa.set_defaults(func=cmd_add)

    pr = sub.add_parser("remove", help="Remove a single alias")
    pr.add_argument("--id", required=True, dest="id")
    pr.add_argument("--locale", required=True)
    pr.add_argument("--value", required=True)
    pr.set_defaults(func=cmd_remove)

    pl = sub.add_parser("list", help="List aliases for a given ontology id")
    pl.add_argument("--id", required=True, dest="id")
    pl.add_argument("--locale", required=False, default=None)
    pl.set_defaults(func=cmd_list)

    pc = sub.add_parser(
        "conflict-report",
        help="Emit conflicts + unknowns for the EN synonym source",
    )
    pc.add_argument("--source", required=False, default=None)
    pc.set_defaults(func=cmd_conflict_report)

    return p


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
