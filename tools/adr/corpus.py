"""Discover and parse every ADR file in ``decisions/``.

Spec anchors: ADR.A.2.7 (filename ↔ frontmatter coupling), ADR.A.5.9
(reuse ``tools/fm/_core.py`` for parsing).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic


@dataclass(frozen=True)
class AdrRecord:
    path: Path
    rel: str
    frontmatter: dict[str, Any]
    body: str
    text: str
    adr_id: str
    adr_status: str
    adr_supersedes: tuple[str, ...]
    adr_superseded_by: tuple[str, ...]
    parse_error: str | None = None


def _coerce_list(fm: dict[str, Any], key: str) -> tuple[str, ...]:
    raw = fm.get(key)
    if isinstance(raw, list):
        return tuple(str(x) for x in raw if x)
    if isinstance(raw, str) and raw:
        return (raw,)
    return ()


def _rel_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def parse_record(path: Path, *, repo_root: Path | None = None) -> AdrRecord:
    """Parse a single ADR markdown file into an ``AdrRecord``.

    A file with malformed frontmatter still yields a record (with empty
    string fields) so the validator can surface the parse error rather
    than crash the whole corpus walk.
    """
    root = repo_root or _core.repo_root_from_cwd()
    rel = _rel_path(path, root)
    text = path.read_text(encoding="utf-8")
    parse_error: str | None = None
    try:
        fm = _core.parse_frontmatter(text, strict=True)
    except _core.Diag as e:
        fm = {}
        parse_error = str(e)
    _, body = _core.split_frontmatter_and_body(text)
    return AdrRecord(
        path=path,
        rel=rel,
        frontmatter=fm,
        body=body,
        text=text,
        adr_id=_core.str_val(fm, "adr_id"),
        adr_status=_core.str_val(fm, "adr_status"),
        adr_supersedes=_coerce_list(fm, "adr_supersedes"),
        adr_superseded_by=_coerce_list(fm, "adr_superseded_by"),
        parse_error=parse_error,
    )


def load_corpus(
    root: Path = Path("decisions"),
    *,
    repo_root: Path | None = None,
) -> list[AdrRecord]:
    """Return one ``AdrRecord`` per ``decisions/<NNNN>-*.md`` file.

    The walk ignores ``decisions/readme.md`` (an index file, not an ADR)
    and any nested directories. The result is sorted by path so callers
    get deterministic ordering.
    """
    repo = repo_root or _core.repo_root_from_cwd()
    target = root if root.is_absolute() else (repo / root)
    if not target.exists() or not target.is_dir():
        return []
    records: list[AdrRecord] = []
    for path in sorted(target.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        records.append(parse_record(path, repo_root=repo))
    return records


def parse_diagnostics(corpus: list[AdrRecord]) -> list[Diagnostic]:
    """Convert any frontmatter parse errors into diagnostics."""
    out: list[Diagnostic] = []
    for rec in corpus:
        if rec.parse_error:
            out.append(Diagnostic(
                rec.rel, None, "ERROR", "ADR.A.2.2",
                f"frontmatter parse error: {rec.parse_error}",
            ))
    return out
