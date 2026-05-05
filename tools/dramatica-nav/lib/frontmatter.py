"""Per-term YAML frontmatter extraction from markdown.

The per-term blocks are NOT file-head L1 frontmatter. They are embedded
fenced YAML inserted immediately after every ## <Term> heading by
ontology-build.py, marked with an HTML comment for idempotent detection.

Block shape:
    ## Trust
    <!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->
    ```yaml
    id: el.trust
    kind: element
    ...
    ```
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

import yaml


YAML_BLOCK_RE = re.compile(
    r"<!-- nav-ontology[^>]*-->\n```yaml\n(.+?)\n```",
    re.DOTALL,
)

VOCAB_SKIP = {"_synonym-lookup.md", "dynamic-pairs-index.md"}


def extract_blocks(text: str) -> list[dict]:
    """Return all parsed nav-ontology YAML blocks from a markdown string."""
    out: list[dict] = []
    for body in YAML_BLOCK_RE.findall(text):
        data = yaml.safe_load(body)
        if isinstance(data, dict):
            out.append(data)
    return out


def walk_vocab_blocks(repo_root: Path) -> Iterator[tuple[Path, dict]]:
    """Yield (file_path, block_dict) for every nav-ontology block in vocab files."""
    base = repo_root / "skills" / "dramatica-vocabulary" / "references"
    for path in sorted(base.glob("*.md")):
        if path.name in VOCAB_SKIP:
            continue
        for block in extract_blocks(path.read_text()):
            yield path, block


def walk_theory_chunks(repo_root: Path) -> Iterator[tuple[Path, dict]]:
    """Yield (file_path, frontmatter_dict) for theory chapters' file-head YAML."""
    base = repo_root / "skills" / "dramatica-theory" / "references"
    head_re = re.compile(r"^---\n(.+?)\n---\n", re.DOTALL)
    for path in sorted(base.glob("*.md")):
        text = path.read_text()
        m = head_re.match(text)
        if not m:
            continue
        data = yaml.safe_load(m.group(1))
        if isinstance(data, dict) and data.get("type") == "theory-chunk":
            yield path, data


def slugify(name: str) -> str:
    """Heading → anchor slug. Strips parens, lowercases, hyphenates non-alnum."""
    s = name.lower()
    s = re.sub(r"\s*\([^)]*\)", "", s)
    s = re.sub(r"['\"]+", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def slugify_keep_parens(name: str) -> str:
    """GitHub-style anchor — preserves paren content as part of the slug."""
    s = name.lower()
    s = re.sub(r"['\"]+", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def find_heading_anchors(text: str) -> list[tuple[str, str]]:
    """Return [(heading_text, anchor_slug), ...] for every ## heading in text.

    Uses paren-strip slugify (matches the convention in ontology.json term_file
    pointers for ~85% of entries; the navigator falls back to keep-parens for
    the remaining ~15%).
    """
    out = []
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m and m.group(1) != "Contents":
            heading = m.group(1)
            out.append((heading, slugify(heading)))
    return out
