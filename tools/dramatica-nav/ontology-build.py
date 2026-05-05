#!/usr/bin/env python3
"""One-pass projection from per-term frontmatter blocks into ontology.json.

Merge mode (default): overwrite only entries whose ID appears in per-term
blocks; preserve all other entries unchanged.

From-scratch mode (--from-scratch): rebuild from blocks alone. Drops entries
not covered by blocks. Use only when corpus has 100% per-term coverage.

Usage:
    ontology-build.py [--output <path>] [--check-only] [--from-scratch]

Exit codes:
    0  success / byte-identical (--check-only)
    1  drift detected (--check-only)
    2  file I/O error
    3  YAML parse error in a block
    5  schema validation failure
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Iterator

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib import frontmatter  # noqa: E402
from lib.frontmatter import slugify  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "maintenance/schemas/narrative-ontology/ontology.json"
SCHEMA_PATH = REPO_ROOT / "maintenance/schemas/narrative-ontology/ontology.schema.json"
VOCAB_SKIP = {"_synonym-lookup.md", "dynamic-pairs-index.md"}
MARKER_PREFIX = "<!-- nav-ontology"
BLOCK_RE = re.compile(
    r"<!-- nav-ontology[^>]*-->\n```yaml\n(.+?)\n```",
    re.DOTALL,
)
HEADING_RE = re.compile(r"^## (.+?)\s*$")
ONTOLOGY_META = {
    "schema_version": "1.0",
    "ontology_version": "0.1",
    "created": "2026-05-04",
}

# ---------------------------------------------------------------------------
# Walking blocks with heading context
# ---------------------------------------------------------------------------


def walk_blocks_with_headings(
    repo_root: Path,
) -> Iterator[tuple[Path, str, dict]]:
    """Yield (file_path, heading_text, block_dict) for every nav-ontology block.

    Captures the ## heading immediately preceding each block.  YAML parse
    errors are re-raised as ValueError with file context included.
    """
    base = repo_root / "skills" / "dramatica-vocabulary" / "references"
    for path in sorted(base.glob("*.md")):
        if path.name in VOCAB_SKIP:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise OSError(f"cannot read {path}: {exc}") from exc

        lines = text.splitlines()
        heading: str | None = None
        i = 0
        while i < len(lines):
            line = lines[i]
            m = HEADING_RE.match(line)
            if m and m.group(1) != "Contents":
                heading = m.group(1)

            if line.strip().startswith(MARKER_PREFIX):
                # Reconstruct the local chunk starting at this marker line so
                # BLOCK_RE can match the fenced yaml that follows.
                chunk = "\n".join(lines[i:])
                bm = BLOCK_RE.match(chunk)
                if bm:
                    raw = bm.group(1)
                    try:
                        data = yaml.safe_load(raw)
                    except yaml.YAMLError as exc:
                        raise ValueError(
                            f"ontology-build: malformed block in {path}: {exc}"
                        )
                    if isinstance(data, dict):
                        yield path, heading or "", data
                # Advance past the closing ``` of this block.
                while i < len(lines) and not lines[i].startswith("```yaml"):
                    i += 1
                while i < len(lines) and lines[i] != "```":
                    i += 1
            i += 1


# ---------------------------------------------------------------------------
# Building the entry map from blocks
# ---------------------------------------------------------------------------


def build_block_entries(
    repo_root: Path,
    existing: dict[str, dict] | None = None,
) -> dict[str, dict]:
    """Return {id: entry_dict} for every per-term block found in vocab files.

    In merge mode (``existing`` supplied) the returned dict for each entry is
    seeded from the existing ontology record so that key insertion order is
    preserved.  Block values overwrite existing values field-by-field, keeping
    the JSON output byte-identical to what a human-authored file would look like.

    ``term_file`` resolution priority (highest to lowest):
      1. Explicit ``term_file`` key inside the block YAML.
      2. ``term_file`` carried by the existing ontology entry (merge mode).
      3. Computed from ``skills/.../references/<file>.md#<heading-slug>``.

    Priority 2 preserves slugs authored with ``slugify_keep_parens`` (e.g.
    headings like "Direction (Overall Story Throughline)") without requiring
    those headings to embed a ``term_file`` override in the block.
    """
    entries: dict[str, dict] = {}
    for path, heading, block in walk_blocks_with_headings(repo_root):
        bid = block.get("id")

        if existing and bid in existing:
            # Seed from the existing record to preserve key order, then overlay
            # every field the block defines.
            entry: dict = dict(existing[bid])
            entry.update(block)
        else:
            entry = dict(block)

        if "term_file" not in entry:
            # Priority 2: inherit from existing ontology if present.
            existing_tf = (existing or {}).get(bid, {}).get("term_file")
            if existing_tf:
                entry["term_file"] = existing_tf
            elif heading:
                # Priority 3: compute from heading slug.
                slug = slugify(heading)
                entry["term_file"] = (
                    f"skills/dramatica-vocabulary/references/{path.name}#{slug}"
                )

        if bid:
            entries[bid] = entry
    return entries


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def load_schema(schema_path: Path) -> dict:
    try:
        return json.loads(schema_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise OSError(f"cannot read schema {schema_path}: {exc}") from exc


def validate_entry(entry: dict, schema: dict) -> list[str]:
    """Return a list of validation error messages (empty = valid).

    Uses jsonschema when available; falls back to required-field check only.
    """
    try:
        import jsonschema  # type: ignore

        validator = jsonschema.Draft202012Validator(schema)
        return [e.message for e in validator.iter_errors(entry)]
    except ImportError:
        errors: list[str] = []
        for field in schema.get("required", []):
            if field not in entry:
                errors.append(f"missing required field '{field}'")
        return errors


# ---------------------------------------------------------------------------
# JSON serialisation helpers
# ---------------------------------------------------------------------------


def serialise(doc: dict) -> str:
    """Serialise ``doc`` to a canonical JSON string (2-space indent, no trailing newline).

    Matches the existing ontology.json format exactly: ``json.dumps`` with
    ``indent=2`` and ``ensure_ascii=False``, no appended newline.
    """
    return json.dumps(doc, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Core build logic
# ---------------------------------------------------------------------------


def build_ontology(
    repo_root: Path,
    existing_path: Path,
    from_scratch: bool,
) -> dict:
    """Build the full ontology document in memory and return it."""
    if from_scratch:
        block_entries = build_block_entries(repo_root, existing=None)
        merged: list[dict] = list(block_entries.values())
    else:
        # Load the existing file to preserve non-block entries and to supply
        # term_file values for block entries that don't set it explicitly.
        # If the file does not exist yet (first-time write), start from an
        # empty base so block entries are the sole population.
        existing_entries: dict[str, dict] = {}
        if existing_path.exists():
            try:
                existing_doc = json.loads(existing_path.read_text(encoding="utf-8"))
            except OSError as exc:
                raise OSError(f"cannot read {existing_path}: {exc}") from exc
            except json.JSONDecodeError as exc:
                raise OSError(f"invalid JSON in {existing_path}: {exc}") from exc
            existing_entries = {
                e["id"]: e for e in existing_doc.get("entries", [])
            }

        block_entries = build_block_entries(repo_root, existing=existing_entries)
        # Overwrite block-covered entries; keep the rest verbatim.
        existing_entries.update(block_entries)
        merged = list(existing_entries.values())

    # Deterministic sort.
    merged.sort(key=lambda e: (e.get("kind", ""), e.get("id", "")))

    return {**ONTOLOGY_META, "entries": merged}


# ---------------------------------------------------------------------------
# Validation pass
# ---------------------------------------------------------------------------


def validate_all(entries: list[dict], schema: dict) -> bool:
    """Validate every entry; print errors to stderr.  Return True if all pass."""
    ok = True
    for entry in entries:
        eid = entry.get("id", "<unknown>")
        errors = validate_entry(entry, schema)
        for msg in errors:
            print(
                f"ontology-build: validation failed for entry {eid}: {msg}",
                file=sys.stderr,
            )
            ok = False
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild ontology.json from per-term frontmatter blocks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination path (default: maintenance/schemas/narrative-ontology/ontology.json)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Build in memory, diff against existing file; exit 0 if identical, 1 if drift.",
    )
    parser.add_argument(
        "--from-scratch",
        action="store_true",
        help=(
            "Rebuild from blocks alone, dropping non-block entries. "
            "Safe only when corpus has 100%% per-term coverage (currently false)."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:  # noqa: C901
    args = parse_args(argv)
    output_path: Path = args.output

    # --- Build in memory -------------------------------------------------
    try:
        doc = build_ontology(REPO_ROOT, output_path, from_scratch=args.from_scratch)
    except ValueError as exc:
        # YAML parse error
        print(str(exc), file=sys.stderr)
        return 3
    except OSError as exc:
        print(f"ontology-build: I/O error: {exc}", file=sys.stderr)
        return 2

    # --- Schema validation -----------------------------------------------
    try:
        schema = load_schema(SCHEMA_PATH)
    except OSError as exc:
        print(f"ontology-build: I/O error: {exc}", file=sys.stderr)
        return 2

    if not validate_all(doc["entries"], schema):
        return 5

    # --- Serialise -------------------------------------------------------
    built_text = serialise(doc)

    # --- Check-only mode -------------------------------------------------
    if args.check_only:
        try:
            existing_text = output_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ontology-build: I/O error reading {output_path}: {exc}", file=sys.stderr)
            return 2

        if built_text == existing_text:
            return 0

        # Compute a rough diff summary.
        built_lines = built_text.splitlines()
        existing_lines = existing_text.splitlines()
        diff = list(
            difflib.unified_diff(
                existing_lines, built_lines, fromfile="existing", tofile="built", lineterm=""
            )
        )
        added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        print(
            f"ontology-build: drift detected — {added} lines added, {removed} lines removed",
            file=sys.stderr,
        )
        return 1

    # --- Write mode ------------------------------------------------------
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(built_text, encoding="utf-8")
    except OSError as exc:
        print(f"ontology-build: I/O error writing {output_path}: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
