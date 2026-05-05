"""Shared library for the flexible frontmatter toolchain.

Spec: /research/flexible-frontmatter-toolchain/output/SPEC.md (anchor F.5.5)

This module is the single home for:

  - frontmatter parsing (hand-rolled, no PyYAML)
  - type/path classification
  - heading walker
  - diagnostic shaping
  - ontology loading

It also preserves the legacy `tools/_frontmatter.py` API
(`FRONTMATTER_RE`, `Diag`, `parse_frontmatter`, `read_fm`, `str_val`,
`str_list`) so the legacy linters keep working until Task 017 cuts over.
"""
from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

# ---- Frontmatter parsing -----------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


class Diag(Exception):
    """Raised by parse_frontmatter(strict=True) on malformed input."""


def _looks_like_folded_or_literal(val: str) -> bool:
    return val in (">", ">-", ">+", "|", "|-", "|+")


def parse_frontmatter(text: str, *, strict: bool = True) -> dict[str, Any]:
    """Parse the YAML frontmatter block at the top of `text`.

    Constraints (per `maintenance/language-spec.md §4.1`):
      - YAML MUST NOT nest deeper than 1 level.
      - Lists MUST contain only scalars/short strings.

    In addition to the original parser, this version recognises a single
    folded/literal scalar (`>-`, `>`, `|`, etc.) so SKILL.md frontmatter
    written in Anthropic's style does not break the strict path.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        if strict:
            raise Diag("missing frontmatter block (no leading '---' fenced YAML)")
        return {}

    body = m.group(1)
    mapping: dict[str, Any] = {}
    current_list_key: str | None = None
    folded_key: str | None = None
    folded_lines: list[str] = []
    folded_kind: str | None = None  # ">" or "|"

    def _close_folded() -> None:
        nonlocal folded_key, folded_lines, folded_kind
        if folded_key is None:
            return
        if folded_kind in ("|", "|-", "|+"):
            joined = "\n".join(folded_lines).rstrip("\n")
        else:
            # Folded: paragraphs separated by blank lines, lines joined by space.
            paragraphs: list[list[str]] = [[]]
            for ln in folded_lines:
                if ln.strip() == "":
                    paragraphs.append([])
                else:
                    paragraphs[-1].append(ln.strip())
            joined = "\n\n".join(" ".join(p) for p in paragraphs if p).strip()
        mapping[folded_key] = joined
        folded_key = None
        folded_lines = []
        folded_kind = None

    for raw in body.splitlines():
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip(" "))

        # Folded/literal scalar continuation.
        if folded_key is not None:
            if raw == "" or indent >= 2:
                folded_lines.append(raw[2:] if indent >= 2 else "")
                continue
            _close_folded()

        if not stripped or stripped.startswith("#"):
            continue

        depth = indent // 2

        if stripped.startswith("- "):
            if current_list_key is None:
                if strict:
                    raise Diag(f"orphan list item: {stripped!r}")
                continue
            mapping.setdefault(current_list_key, []).append(
                stripped[2:].strip().strip('"').strip("'")
            )
            continue

        if depth >= 2:
            if strict:
                raise Diag(
                    f"YAML nested deeper than 1 level (depth={depth}) at line: {raw!r}"
                )
            continue

        if ":" not in stripped:
            if strict:
                raise Diag(f"unparseable frontmatter line: {raw!r}")
            continue

        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        current_list_key = None

        if _looks_like_folded_or_literal(val):
            folded_key = key
            folded_kind = val
            folded_lines = []
            mapping.setdefault(key, "")
            continue

        if val == "":
            mapping[key] = []
            current_list_key = key
        elif val == "[]":
            mapping[key] = []
        else:
            mapping[key] = val.strip('"').strip("'")

    _close_folded()
    return mapping


def read_fm(path: Path, *, strict: bool = False) -> dict[str, Any]:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"), strict=strict)
    except (OSError, Diag):
        return {}


def str_val(fm: dict, key: str) -> str:
    v = fm.get(key, "")
    return v if isinstance(v, str) else ""


def str_list(fm: dict, key: str) -> list[str]:
    v = fm.get(key, [])
    if isinstance(v, list):
        return [s for s in v if s]
    if isinstance(v, str) and v:
        return [v]
    return []


# ---- Ontology loading --------------------------------------------------------

ONTOLOGY_PATH_REL = Path("maintenance/schemas/header-ontology.json")


def load_ontology(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root or repo_root_from_cwd()
    path = root / ONTOLOGY_PATH_REL
    return json.loads(path.read_text(encoding="utf-8"))


def repo_root_from_cwd(start: Path | None = None) -> Path:
    """Walk upward from `start` looking for a directory containing AGENTS.md.

    Falls back to CWD if no marker is found.
    """
    p = (start or Path.cwd()).resolve()
    for candidate in [p, *p.parents]:
        if (candidate / "AGENTS.md").exists():
            return candidate
    return p


# ---- Path classification -----------------------------------------------------

OPERATIONAL_ROOTS = (
    "tasks", "prompts", "research", "skills",
    "maintenance", "tools", "templates",
)


@dataclass(frozen=True)
class Classification:
    expected_type: str | None  # None means: file is not in classifier scope
    alt_types: tuple[str, ...] = ()


def _norm_parts(path: Path, repo_root: Path) -> tuple[str, ...]:
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        rel = path
    return rel.parts


def classify_path(path: Path, repo_root: Path, ontology: dict[str, Any]) -> Classification:
    """Return what type of file this path is expected to hold.

    Uses the ontology's `path_classification.rules` table. Returns a
    `Classification` with `expected_type=None` when the file is not in the
    validator's scope.
    """
    parts = _norm_parts(path, repo_root)
    if not parts:
        return Classification(None)
    rel = "/".join(parts)
    for rule in ontology["path_classification"]["rules"]:
        if fnmatch.fnmatchcase(rel, rule["pattern"]):
            return Classification(rule["type"], tuple(rule.get("alt_types", [])))
    return Classification(None)


def iter_operational_files(
    repo_root: Path,
    *,
    scope: Iterable[str] | None = None,
) -> Iterator[Path]:
    roots = list(scope) if scope else list(OPERATIONAL_ROOTS)
    for r in roots:
        d = repo_root / r
        if not d.exists():
            continue
        if d.is_file():
            if d.suffix == ".md":
                yield d
            continue
        for f in d.rglob("*.md"):
            yield f


# ---- Heading walker ----------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def split_frontmatter_and_body(text: str) -> tuple[str, str]:
    """Return (frontmatter_block_with_fences, body) — body starts after the
    closing `---\\n`. If no frontmatter, fm is "" and body is the full text.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return text[: m.end()], text[m.end():]


def normalise_heading(name: str) -> str:
    """Case-insensitive comparable form: strip surrounding whitespace and
    trailing punctuation (colons, em-dashes, en-dashes, hyphens) so that
    `## Goal:`, `## Goal —`, and `## Goal — :` all match `## Goal`.
    Embedded em-dashes (e.g., `I — Input`) are preserved verbatim."""
    s = name.strip()
    while s and s[-1] in ":—–- \t":
        s = s[:-1]
    return s.casefold()


def _iter_lines_outside_fence(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    """Yield (zero-based-index, line) for every line NOT inside a triple-
    backtick or triple-tilde fenced code block. Fence lines themselves are
    not yielded. The closing fence must use the same marker character as
    the opening fence (``` ↔ ```, ~~~ ↔ ~~~)."""
    in_fence = False
    fence_marker: str | None = None
    for idx, line in enumerate(lines):
        s = line.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            marker = s[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        yield idx, line


def iter_h2(body: str) -> Iterator[tuple[int, str]]:
    """Yield (line_number, heading_text) for every `## ` heading in `body`,
    skipping headings inside fenced code blocks. Line numbers are 1-based."""
    for idx, line in _iter_lines_outside_fence(body.splitlines()):
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:
            yield idx + 1, m.group(2)


def find_section_body(text: str, heading: str) -> str | None:
    """Return the body text of the named `## heading`, or None if absent.

    Matching is case-insensitive after `normalise_heading`. The body extends
    from the line after the heading up to (but not including) the next `## `
    heading or end-of-file. Headings inside fenced code blocks are ignored."""
    target = normalise_heading(heading)
    _, body = split_frontmatter_and_body(text)
    lines = body.splitlines(keepends=True)
    start_line: int | None = None
    end_line = len(lines)
    for idx, line in _iter_lines_outside_fence(lines):
        m = HEADING_RE.match(line.rstrip("\n"))
        if not m or len(m.group(1)) != 2:
            continue
        norm = normalise_heading(m.group(2))
        if start_line is None:
            if norm == target:
                start_line = idx + 1
        else:
            end_line = idx
            break
    if start_line is None:
        return None
    return "".join(lines[start_line:end_line])


# ---- Diagnostics -------------------------------------------------------------

@dataclass(frozen=True)
class Diagnostic:
    path: str
    line: int | None
    severity: str  # "ERROR" or "WARN"
    code: str
    message: str

    def render(self) -> str:
        line = "" if self.line is None else str(self.line)
        return f"{self.path}:{line}:{self.severity}:{self.code}:{self.message}"

    def to_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }


# ---- Levenshtein for did-you-mean -------------------------------------------

def levenshtein(a: str, b: str) -> int:
    """Optimal String Alignment distance (Damerau–Levenshtein restricted edit
    distance). Adjacent-character transposition costs 1, matching the
    "did-you-mean" intent of SPEC §3.4 (e.g., `tpye` → `type` is distance 1).
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    # Two-row DP plus a "row before previous" for the transposition step.
    prev_prev = [0] * (len(b) + 1)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr[j] = min(
                curr[j - 1] + 1,        # insertion
                prev[j] + 1,            # deletion
                prev[j - 1] + cost,     # substitution
            )
            if (i > 1 and j > 1
                    and ca == b[j - 2]
                    and a[i - 2] == cb):
                curr[j] = min(curr[j], prev_prev[j - 2] + 1)
        prev_prev = prev
        prev = curr
    return prev[-1]


# ---- File locking ------------------------------------------------------------

class FileLock:
    """Best-effort exclusive OS file lock for read-modify-write.

    Uses fcntl.flock on POSIX. On Windows / non-POSIX, degrades to a no-op
    (the test harness is POSIX-only, per CI assumptions).
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fh = None

    def __enter__(self):
        try:
            import fcntl
            self._fh = open(self.path, "r+b")
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX)
        except (ImportError, OSError):
            self._fh = None
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._fh is not None:
            try:
                import fcntl
                fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
            self._fh.close()
            self._fh = None
