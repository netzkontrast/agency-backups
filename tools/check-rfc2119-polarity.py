#!/usr/bin/env python3
"""
RFC 2119 polarity-inversion linter (Task 032 ST-3, ASM-001 mitigation).

Scans a file or directory for adjacent ``MUST`` / ``MUST NOT`` clauses on the
same subject — candidates for human review of accidental polarity inversion.

The linter mitigates the polarity-inversion blind spot identified in
``research/adr-assumption-audit/output/REPORT.md §1 ASM-001``: a stripped or
inverted ``NOT`` qualifier survives ``bcp14-keyword`` fidelity checks and now,
post-Task 031, may silently invert governance language in ``AGENTS.md`` on the
next ``tools/adr/synthesize.py`` run. This linter is the missing semantic guard
rail (the ADR validator catches structural errors but not polarity inversions).

Usage::

    python3 tools/check-rfc2119-polarity.py <file-or-dir> [<file-or-dir> ...]
        [--threshold 0.6]

Diagnostic shape (one per pair, both poles reported)::

    <file>:<line>::WARN:RFC2119.POLARITY:<message>

Exit codes:
    0  — scan completed (even when WARN diagnostics were emitted: this is an
         advisory linter; humans review the candidate pairs).
    1  — fatal parse error (e.g. unreadable file, invalid CLI args).

Heuristic (kept deliberately simple):
    1. First pass — collect every (file, line, "MUST"|"MUST NOT", subject)
       tuple. The subject is the next ~5-10 cleaned tokens after the keyword
       (lowercased, markdown-stripped, stopwords removed).
    2. Second pass — for every MUST keyword, find every MUST NOT in the same
       file whose subject Jaccard-overlaps ≥ threshold (default 0.6). Report
       both poles + the matched subject as a candidate inversion.

Skips:
    * lines inside fenced code blocks (``` or ~~~);
    * lines whose first non-whitespace char is ``|`` (table cells frequently
      list MUST and MUST NOT side-by-side as glossary rows);
    * the canonical RFC 2119 declaration boilerplate (lines that mention
      ``BCP 14`` or both ``RFC 2119`` and ``RFC 8174``).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# --- Regexes ----------------------------------------------------------------

# Match MUST NOT first (longer match wins). The keyword MUST appear as a
# whole word (word-boundary on both sides). We tolerate either uppercase
# spelling (the canonical normative form) since the spec corpus mixes
# `MUST`/`MUST NOT` in body prose only when normative.
_KEYWORD_RE = re.compile(r"\b(MUST\s+NOT|MUST)\b")

# Markdown decoration to strip from the subject phrase before tokenising.
_MARKDOWN_NOISE_RE = re.compile(r"[`*_~\[\]()<>]")

# Token splitter: anything that is not a word character or hyphen is a sep.
_TOKEN_SPLIT_RE = re.compile(r"[^\w\-]+")

# Fenced code-block fences (``` or ~~~ optionally followed by language tag).
_FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Canonical RFC 2119 boilerplate sniffer — present in language-spec.md.
_BOILERPLATE_RE = re.compile(r"\bBCP\s*14\b|\bRFC\s*2119\b.*\bRFC\s*8174\b")

# Stopwords removed from the subject phrase before Jaccard comparison. Kept
# small and conservative; expanding it risks collapsing distinct subjects.
_STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "the",
        "be",
        "is",
        "are",
        "was",
        "were",
        "to",
        "of",
        "in",
        "on",
        "at",
        "by",
        "for",
        "with",
        "from",
        "as",
        "and",
        "or",
        "but",
        "any",
        "all",
        "every",
        "each",
        "no",
        "not",
        "this",
        "that",
        "these",
        "those",
        "its",
        "their",
        "his",
        "her",
        "our",
        "your",
        "it",
        "they",
        "them",
        "we",
        "you",
        "i",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "been",
        "being",
        "will",
        "shall",
        "can",
        "may",
    }
)

# Number of tokens after the keyword to treat as "the subject phrase".
_SUBJECT_WINDOW = 10


# --- Data types -------------------------------------------------------------


@dataclass(frozen=True)
class Clause:
    """A single MUST or MUST NOT occurrence with its subject phrase."""

    file: Path
    line: int
    polarity: str  # "MUST" or "MUST NOT"
    subject_raw: str
    subject_tokens: frozenset[str]

    @property
    def location(self) -> str:
        return f"{self.file}:{self.line}"


# --- Subject extraction -----------------------------------------------------


def _normalise_tokens(text: str) -> list[str]:
    """Lowercase, strip markdown decoration, split on non-word chars."""
    cleaned = _MARKDOWN_NOISE_RE.sub(" ", text).lower()
    raw = [t for t in _TOKEN_SPLIT_RE.split(cleaned) if t]
    return [t for t in raw if t not in _STOPWORDS and not t.isdigit()]


def _extract_subject(line: str, keyword_end: int) -> tuple[str, frozenset[str]]:
    """Return (raw_subject, normalised_token_set) from the keyword's tail.

    The raw subject is the verbatim ~10 words after the keyword (for human
    diagnostic display); the token set is the cleaned/stopworded version used
    for Jaccard comparison.
    """
    tail = line[keyword_end:].strip()
    # Truncate at the next sentence terminator if present — keeps the subject
    # local to this clause when multiple MUSTs share a line.
    for terminator in (". ", "; ", " — ", ". \n"):
        idx = tail.find(terminator)
        if idx != -1:
            tail = tail[:idx]
            break
    raw_words = tail.split()
    raw_subject = " ".join(raw_words[:_SUBJECT_WINDOW]).strip()
    tokens = _normalise_tokens(raw_subject)[:_SUBJECT_WINDOW]
    return raw_subject, frozenset(tokens)


# --- Scanner ----------------------------------------------------------------


def _is_skipped_line(stripped: str) -> bool:
    """Skip table rows. (Boilerplate is handled with a windowed check.)"""
    if stripped.startswith("|"):
        return True
    return False


# Window radius (in lines) around any BCP 14 / RFC 2119 marker within which
# MUST/MUST NOT keywords are treated as the canonical declaration boilerplate.
# RFC 2119/8174 declarations frequently span 2-3 lines (the keyword list on
# one line, the citation on the next), so we need a small but non-zero radius.
_BOILERPLATE_RADIUS = 3


def _boilerplate_lines(lines: list[str]) -> set[int]:
    """Return the 1-indexed line numbers within boilerplate blast radius."""
    flagged: set[int] = set()
    for idx, line in enumerate(lines, start=1):
        if _BOILERPLATE_RE.search(line):
            for offset in range(-_BOILERPLATE_RADIUS, _BOILERPLATE_RADIUS + 1):
                target = idx + offset
                if target >= 1:
                    flagged.add(target)
    return flagged


def scan_file(path: Path) -> list[Clause]:
    """Walk ``path`` line by line, returning every (in-prose) MUST/MUST NOT."""
    clauses: list[Clause] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:  # pragma: no cover - I/O edge
        raise RuntimeError(f"cannot read {path}: {exc}") from exc

    lines = text.splitlines()
    boilerplate = _boilerplate_lines(lines)

    in_fence = False
    for lineno, raw_line in enumerate(lines, start=1):
        if _FENCE_RE.match(raw_line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = raw_line.lstrip()
        if _is_skipped_line(stripped):
            continue
        if lineno in boilerplate:
            continue

        for match in _KEYWORD_RE.finditer(raw_line):
            polarity = "MUST NOT" if "NOT" in match.group(1) else "MUST"
            raw_subject, tokens = _extract_subject(raw_line, match.end())
            if not tokens:
                # No usable subject (keyword at end of line or only stopwords).
                continue
            clauses.append(
                Clause(
                    file=path,
                    line=lineno,
                    polarity=polarity,
                    subject_raw=raw_subject,
                    subject_tokens=tokens,
                )
            )
    return clauses


# --- Pair detection ---------------------------------------------------------


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


@dataclass(frozen=True)
class PolarityPair:
    must: Clause
    must_not: Clause
    overlap: float

    def diagnostic(self) -> str:
        subject = self.must.subject_raw or "(empty)"
        msg = (
            f"candidate polarity inversion: MUST at {self.must.location} "
            f"vs MUST NOT at {self.must_not.location} "
            f"(jaccard={self.overlap:.2f}, subject={subject!r})"
        )
        # Emit the diagnostic anchored on the MUST pole; the message body
        # carries the MUST NOT pole's location too, satisfying AC #3.
        return f"{self.must.location}::WARN:RFC2119.POLARITY:{msg}"


def find_pairs(clauses: list[Clause], threshold: float) -> list[PolarityPair]:
    """Pair every MUST with every same-file MUST NOT above the threshold."""
    by_file: dict[Path, list[Clause]] = {}
    for c in clauses:
        by_file.setdefault(c.file, []).append(c)

    pairs: list[PolarityPair] = []
    for file_clauses in by_file.values():
        musts = [c for c in file_clauses if c.polarity == "MUST"]
        not_musts = [c for c in file_clauses if c.polarity == "MUST NOT"]
        for m in musts:
            for n in not_musts:
                overlap = _jaccard(m.subject_tokens, n.subject_tokens)
                if overlap >= threshold:
                    pairs.append(PolarityPair(must=m, must_not=n, overlap=overlap))
    # Stable order: file, MUST line, MUST NOT line.
    pairs.sort(key=lambda p: (str(p.must.file), p.must.line, p.must_not.line))
    return pairs


# --- File discovery ---------------------------------------------------------


def _iter_targets(targets: list[Path]) -> list[Path]:
    """Expand directories to *.md files; pass files through as-is."""
    out: list[Path] = []
    for t in targets:
        if t.is_dir():
            out.extend(sorted(t.rglob("*.md")))
        elif t.is_file():
            out.append(t)
        else:
            raise RuntimeError(f"target does not exist: {t}")
    return out


# --- CLI --------------------------------------------------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-rfc2119-polarity",
        description=(
            "Advisory linter for RFC 2119 polarity inversions "
            "(Task 032 ST-3, ASM-001 mitigation)."
        ),
    )
    parser.add_argument(
        "targets",
        nargs="+",
        type=Path,
        help="Files or directories to scan (directories recurse to *.md).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.6,
        help="Jaccard subject-overlap threshold for pairing (default 0.6).",
    )
    args = parser.parse_args(argv)

    try:
        files = _iter_targets(args.targets)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    all_clauses: list[Clause] = []
    for f in files:
        try:
            all_clauses.extend(scan_file(f))
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    pairs = find_pairs(all_clauses, threshold=args.threshold)
    for p in pairs:
        print(p.diagnostic())

    summary = (
        f"check-rfc2119-polarity: scanned {len(files)} file(s), "
        f"{len(all_clauses)} keyword(s), {len(pairs)} candidate pair(s)."
    )
    print(summary, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
