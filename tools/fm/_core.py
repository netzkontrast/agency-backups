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
    if not path.exists():
        # Fall back to the ontology shipped alongside this module.
        sibling = Path(__file__).resolve().parents[1].parent / ONTOLOGY_PATH_REL
        if sibling.exists():
            path = sibling
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


def find_section_body(text: str, heading: str, *, nth: int = 1) -> str | None:
    """Return the body text of the n-th `## heading` match, or None if absent.

    Matching is case-insensitive after `normalise_heading`. `nth` is 1-indexed.
    The body extends from the line after the heading up to (but not including)
    the next `## ` heading or end-of-file. Headings inside fenced code blocks
    are ignored. SPEC §13.3 addressing."""
    bodies = find_all_section_bodies(text, heading)
    if not bodies or nth < 1 or nth > len(bodies):
        return None
    return bodies[nth - 1]


def find_all_section_bodies(text: str, heading: str) -> list[str]:
    """Return every `## heading` body in document order. Empty list if none."""
    target = normalise_heading(heading)
    _, body = split_frontmatter_and_body(text)
    lines = body.splitlines(keepends=True)
    matches: list[tuple[int, int]] = []   # (start_line, end_line)
    open_start: int | None = None
    for idx, line in _iter_lines_outside_fence(lines):
        m = HEADING_RE.match(line.rstrip("\n"))
        if not m or len(m.group(1)) != 2:
            continue
        norm = normalise_heading(m.group(2))
        if open_start is not None:
            matches.append((open_start, idx))
            open_start = None
        if norm == target:
            open_start = idx + 1
    if open_start is not None:
        matches.append((open_start, len(lines)))
    return ["".join(lines[s:e]) for s, e in matches]


@dataclass(frozen=True)
class SectionSpan:
    """Position of one `## ` section relative to the body (post-frontmatter).

    All indices are 0-based body-line offsets (matching `body.splitlines(keepends=True)`).
    `heading_line` is the index of the `## …` line itself; the body runs
    from `heading_line + 1` up to (but not including) `body_end`.
    `anchor_line` is the index of a preceding `# anchor: <id>` comment if
    any (one line above the heading), else None.
    """
    heading_line: int
    body_start: int
    body_end: int
    heading_text: str
    anchor_id: str | None
    anchor_line: int | None


def find_section_spans(text: str, heading: str) -> list[SectionSpan]:
    """Return one SectionSpan per `## heading` match in document order.

    Heading match is case-insensitive after `normalise_heading`. Headings
    inside fenced code blocks are ignored. The body span ends at the next
    `## ` heading (outside fences) or end-of-body. SPEC §13.3 addressing.
    """
    target = normalise_heading(heading)
    _, body = split_frontmatter_and_body(text)
    lines = body.splitlines(keepends=True)
    spans: list[SectionSpan] = []
    open_meta: tuple[int, str, str | None, int | None] | None = None
    for idx, line in _iter_lines_outside_fence(lines):
        m = HEADING_RE.match(line.rstrip("\n"))
        if not m or len(m.group(1)) != 2:
            continue
        head_text = m.group(2)
        norm = normalise_heading(head_text)
        if open_meta is not None:
            heading_line, ht, anch_id, anch_line = open_meta
            spans.append(SectionSpan(
                heading_line=heading_line,
                body_start=heading_line + 1,
                body_end=idx,
                heading_text=ht,
                anchor_id=anch_id,
                anchor_line=anch_line,
            ))
            open_meta = None
        if norm == target:
            anch_id, anch_line = _peek_anchor(lines, idx)
            open_meta = (idx, head_text, anch_id, anch_line)
    if open_meta is not None:
        heading_line, ht, anch_id, anch_line = open_meta
        spans.append(SectionSpan(
            heading_line=heading_line,
            body_start=heading_line + 1,
            body_end=len(lines),
            heading_text=ht,
            anchor_id=anch_id,
            anchor_line=anch_line,
        ))
    return spans


_ANCHOR_COMMENT_RE = re.compile(r"^<!--\s*anchor:\s*([^\s>]+)\s*-->\s*$")
_ANCHOR_HASH_RE = re.compile(r"^#\s*anchor:\s*([^\s]+)\s*$")


def _peek_anchor(lines: list[str], heading_idx: int) -> tuple[str | None, int | None]:
    """Look at the line immediately above `heading_idx` for an anchor marker.

    Recognises:
      - `<!-- anchor: <id> -->` (preferred markdown form)
      - `# anchor: <id>` inside a fenced block on the line above (SPEC §1)
    Returns (anchor_id, anchor_line_idx) or (None, None).
    """
    j = heading_idx - 1
    while j >= 0 and lines[j].strip() == "":
        j -= 1
    if j < 0:
        return None, None
    s = lines[j].strip()
    m = _ANCHOR_COMMENT_RE.match(s) or _ANCHOR_HASH_RE.match(s)
    if m:
        return m.group(1), j
    return None, None


def list_h2_headings(text: str) -> list[str]:
    """Return every `## ` heading in document order, raw text (not normalised).
    SPEC §14.1 fm-extract --toc."""
    _, body = split_frontmatter_and_body(text)
    return [h for _, h in iter_h2(body)]


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


# ---- Body shape detection + validation (SPEC §12) ---------------------------

ORDERED_LIST_RE = re.compile(r"^\s*\d+[.)]\s+")
TASK_LIST_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+")
UNORDERED_LIST_RE = re.compile(r"^\s*[-*]\s+(?!\[[ xX]\])")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
DEFINITION_RE = re.compile(r"^\*\*[^*]+\*\*\s*:\s+\S")


def _strip_fences(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Return (lines_outside_fences, fenced_blocks).

    fenced_blocks is a list of (lang_tag, body_lines) tuples; the lang_tag is
    whatever follows the opening ``` (empty string when absent).
    """
    outside: list[str] = []
    blocks: list[tuple[str, list[str]]] = []
    in_fence = False
    fence_marker: str | None = None
    current_lang = ""
    current_body: list[str] = []
    for line in lines:
        s = line.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            marker = s[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
                current_lang = s[3:].strip()
                current_body = []
            elif fence_marker == marker:
                blocks.append((current_lang, current_body))
                in_fence = False
                fence_marker = None
                current_lang = ""
                current_body = []
            continue
        if in_fence:
            current_body.append(line)
        else:
            outside.append(line)
    return outside, blocks


def detect_shape(section_body: str) -> str:
    """Return the closed-vocabulary shape name for `section_body`.

    Detection is deterministic and uses §12.1 rules. Lines inside fenced
    code blocks do not influence shape (except to flag code_block /
    gherkin_block when no other shape applies). Empty input → 'mixed'.
    """
    lines = section_body.splitlines()
    if not any(l.strip() for l in lines):
        return "mixed"

    outside, blocks = _strip_fences(lines)
    has_gherkin = any(lang.lower() == "gherkin" for lang, _ in blocks)
    has_code = bool(blocks)

    nonblank_outside = [l for l in outside if l.strip()]

    # If the section is *only* fenced blocks (no prose outside), classify by block.
    if not nonblank_outside and blocks:
        return "gherkin_block" if has_gherkin else "code_block"

    if not nonblank_outside:
        return "mixed"

    # Walk top-level lines. Lines indented past column 4 are continuations.
    top_lines = [l for l in nonblank_outside
                 if (len(l) - len(l.lstrip(" "))) < 4]
    if not top_lines:
        return "mixed"

    is_task = all(TASK_LIST_RE.match(l) for l in top_lines)
    is_ordered = all(ORDERED_LIST_RE.match(l) for l in top_lines)
    is_unordered = all(UNORDERED_LIST_RE.match(l) for l in top_lines)
    is_definition = all(DEFINITION_RE.match(l.strip()) for l in top_lines)

    if is_task:
        return "task_list"
    if is_ordered:
        return "ordered_list"
    if is_unordered:
        items_have_links = all(LINK_RE.search(l) for l in top_lines)
        return "link_list" if items_have_links else "unordered_list"
    if is_definition:
        return "definition_list"
    if any(ORDERED_LIST_RE.match(l) or TASK_LIST_RE.match(l)
           or UNORDERED_LIST_RE.match(l) for l in top_lines):
        return "mixed"
    if has_gherkin:
        return "gherkin_block"
    if has_code:
        return "code_block"
    return "paragraph"


def _list_items(section_body: str) -> list[str]:
    """Return the top-level list items (text after the marker) of section_body
    as a list of strings. Works for ordered, unordered, task, and link lists."""
    outside, _ = _strip_fences(section_body.splitlines())
    items: list[str] = []
    for line in outside:
        if not line.strip():
            continue
        if (len(line) - len(line.lstrip(" "))) >= 4:
            continue  # continuation of the previous item
        m = (ORDERED_LIST_RE.match(line) or TASK_LIST_RE.match(line)
             or UNORDERED_LIST_RE.match(line))
        if m:
            items.append(line[m.end():].strip())
    return items


def _paragraphs(section_body: str) -> list[str]:
    """Split section_body into paragraphs separated by blank lines, ignoring
    fenced code blocks."""
    outside, _ = _strip_fences(section_body.splitlines())
    paragraphs: list[list[str]] = [[]]
    for line in outside:
        if not line.strip():
            if paragraphs[-1]:
                paragraphs.append([])
        else:
            paragraphs[-1].append(line)
    return ["\n".join(p) for p in paragraphs if p]


def validate_section_body(
    section_body: str,
    schema: dict[str, Any],
) -> list[tuple[str, str, str]]:
    """Apply §12 schema constraints to one section's body.

    Returns a list of (severity, code, message) tuples. Empty list means clean.
    Caller wraps these in `Diagnostic` for emission.
    """
    diags: list[tuple[str, str, str]] = []
    expected_shape = schema.get("shape")
    if not expected_shape:
        return diags

    detected = detect_shape(section_body)
    if expected_shape != "mixed" and detected != expected_shape:
        # Allow link_list when ontology asks for unordered_list (link_list ⊂).
        if not (expected_shape == "unordered_list" and detected == "link_list"):
            diags.append((
                "ERROR", "F.B.1",
                f"shape mismatch: expected {expected_shape}, found {detected}",
            ))
            return diags  # downstream constraints assume the shape is correct

    list_shapes = ("ordered_list", "unordered_list", "task_list", "link_list")
    if expected_shape in list_shapes:
        items = _list_items(section_body)
        min_items = schema.get("min_items")
        max_items = schema.get("max_items")
        if min_items is not None and len(items) < min_items:
            diags.append((
                "ERROR", "F.B.2",
                f"item count {len(items)} below min_items={min_items}",
            ))
        if max_items is not None and len(items) > max_items:
            diags.append((
                "ERROR", "F.B.2",
                f"item count {len(items)} above max_items={max_items}",
            ))
        item_pattern = schema.get("item_pattern")
        if item_pattern:
            severity = schema.get("item_pattern_severity", "ERROR").upper()
            patt = re.compile(item_pattern)
            for i, item in enumerate(items, start=1):
                if not patt.search(item):
                    diags.append((
                        severity, "F.B.3",
                        f"item {i} does not match pattern {item_pattern!r}",
                    ))

    if expected_shape == "link_list":
        link_pattern = schema.get("link_pattern")
        if link_pattern:
            patt = re.compile(link_pattern)
            for i, item in enumerate(_list_items(section_body), start=1):
                urls = LINK_RE.findall(item)
                if not urls:
                    diags.append((
                        "ERROR", "F.B.6",
                        f"item {i}: no markdown link found",
                    ))
                    continue
                for url in urls:
                    if not patt.match(url):
                        diags.append((
                            "ERROR", "F.B.6",
                            f"item {i}: url {url!r} does not match link_pattern "
                            f"{link_pattern!r}",
                        ))

    if expected_shape == "paragraph":
        paragraphs = _paragraphs(section_body)
        max_p = schema.get("max_paragraphs")
        if max_p is not None and len(paragraphs) > max_p:
            diags.append((
                "ERROR", "F.B.4",
                f"paragraph count {len(paragraphs)} above max_paragraphs={max_p}",
            ))
        min_chars = schema.get("min_chars")
        if min_chars is not None:
            length = len("".join(p.strip() for p in paragraphs))
            if length < min_chars:
                diags.append((
                    "ERROR", "F.B.4",
                    f"body length {length} below min_chars={min_chars}",
                ))

    if expected_shape in ("gherkin_block", "code_block"):
        _, blocks = _strip_fences(section_body.splitlines())
        min_blocks = schema.get("min_blocks")
        if min_blocks is not None and len(blocks) < min_blocks:
            diags.append((
                "ERROR", "F.B.4",
                f"block count {len(blocks)} below min_blocks={min_blocks}",
            ))

    must_contain = schema.get("must_contain")
    if must_contain and must_contain.lower() not in section_body.lower():
        diags.append((
            "ERROR", "F.B.5",
            f"section body missing required substring {must_contain!r}",
        ))

    return diags


# ---- File locking ------------------------------------------------------------

try:
    import fcntl as _fcntl  # POSIX
except ImportError:  # pragma: no cover — non-POSIX (Windows, sandboxes)
    _fcntl = None


class FileLock:
    """Best-effort exclusive OS file lock for read-modify-write.

    Uses fcntl.flock on POSIX (the standard CI platform for this repo).
    On Windows or any environment without fcntl, the lock degrades to a
    no-op — fm-edit's idempotency guarantees still hold across single
    invocations, but two simultaneous writers would race. Real
    concurrency safety is a POSIX-only contract.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fh = None

    def __enter__(self):
        if _fcntl is None:
            return self
        try:
            self._fh = open(self.path, "r+b")
            _fcntl.flock(self._fh.fileno(), _fcntl.LOCK_EX)
        except OSError:
            self._fh = None
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._fh is None:
            return
        try:
            if _fcntl is not None:
                _fcntl.flock(self._fh.fileno(), _fcntl.LOCK_UN)
        finally:
            self._fh.close()
            self._fh = None
