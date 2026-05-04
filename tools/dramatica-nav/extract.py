"""Anchor-aware prose extractor for dramatica-nav ontology files."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import LookupNotFoundError
from lib.frontmatter import slugify, slugify_keep_parens
import lib.ontology as ontology_lib

# Regex that removes the entire nav-ontology comment + fenced YAML block.
# Matches the HTML comment, the ```yaml block, and trailing blank lines.
_STRIP_YAML_RE = re.compile(
    r"<!-- nav-ontology[^>]*-->\n```yaml\n.+?\n```\n*",
    re.DOTALL,
)

# Pattern for ontology ids: <kind>.<slug> e.g. "el.trust", "vr.consider"
_ONTOLOGY_ID_RE = re.compile(r"^[a-z][a-z0-9]*\.[a-z][a-z0-9._-]*$")


def resolve_input(raw: str, repo_root: Path) -> tuple[Path, str]:
    """Return (absolute_file_path, anchor_slug) from the raw CLI argument.

    Two formats are accepted:
    - Ontology id (e.g. "el.trust"): loaded from ontology.json entry's term_file.
    - path#anchor (e.g. "skills/.../elements.md#trust"): used directly.
    """
    if _ONTOLOGY_ID_RE.match(raw):
        try:
            idx = ontology_lib.load()
            entry = idx.by_id(raw)
        except LookupNotFoundError:
            print(f"extract: unknown ontology id={raw}", file=sys.stderr)
            sys.exit(4)

        term_file: str = entry.get("term_file", "")
        if not term_file or "#" not in term_file:
            print(
                f"extract: ontology entry {raw!r} has no valid term_file",
                file=sys.stderr,
            )
            sys.exit(4)

        rel_path, anchor = term_file.rsplit("#", 1)
        file_path = repo_root / rel_path
    else:
        if "#" not in raw:
            print(
                f"extract: input must be an ontology id or path#anchor, got {raw!r}",
                file=sys.stderr,
            )
            sys.exit(2)
        rel_or_abs, anchor = raw.rsplit("#", 1)
        candidate = Path(rel_or_abs)
        file_path = candidate if candidate.is_absolute() else repo_root / candidate

    return file_path, anchor


def find_heading_range(lines: list[str], anchor: str) -> tuple[int, int]:
    """Return (start_line_idx, end_line_idx) for the section matching anchor.

    start_line_idx points at the heading line itself.
    end_line_idx points at the first line of the next same-or-higher-level heading,
    or len(lines) when no such heading follows.

    Tries both strip-parens and keep-parens slugify for matching.

    Raises SystemExit(3) if no matching heading is found.
    """
    # Detect heading level from anchor's section by scanning for a match
    match_idx: int | None = None
    match_level: int | None = None

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6}) (.+?)\s*$", line)
        if not m:
            continue
        hashes, text = m.group(1), m.group(2)
        level = len(hashes)
        if slugify(text) == anchor or slugify_keep_parens(text) == anchor:
            match_idx = i
            match_level = level
            break

    if match_idx is None or match_level is None:
        return -1, -1  # sentinel; caller handles

    # Find the next heading at the same level or higher (fewer #)
    end_idx = len(lines)
    for j in range(match_idx + 1, len(lines)):
        m = re.match(r"^(#{1,6}) ", lines[j])
        if m:
            sibling_level = len(m.group(1))
            if sibling_level <= match_level:
                end_idx = j
                break

    return match_idx, end_idx


def extract_section(file_path: Path, anchor: str, strip_yaml: bool) -> str:
    """Read file_path and extract the prose section for anchor.

    Returns the extracted text (optionally with the nav-ontology block removed).
    """
    if not file_path.exists():
        print(f"extract: file not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    start, end = find_heading_range(lines, anchor)

    if start == -1:
        print(
            f"extract: no heading matching anchor={anchor} in {file_path}",
            file=sys.stderr,
        )
        sys.exit(3)

    section = "".join(lines[start:end])

    if strip_yaml:
        section = _STRIP_YAML_RE.sub("", section)

    return section


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Extract an anchor-delimited prose section from a markdown file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "target",
        help=(
            "Ontology id (e.g. el.trust) OR path#anchor "
            "(e.g. skills/dramatica-vocabulary/references/elements.md#trust)"
        ),
    )
    p.add_argument(
        "--strip-yaml",
        dest="strip_yaml",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Strip the embedded nav-ontology YAML block (default: strip).",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Repo root: two levels above this script (tools/dramatica-nav/extract.py)
    repo_root = Path(__file__).resolve().parents[2]

    file_path, anchor = resolve_input(args.target, repo_root)
    prose = extract_section(file_path, anchor, args.strip_yaml)
    sys.stdout.write(prose)


if __name__ == "__main__":
    main()
