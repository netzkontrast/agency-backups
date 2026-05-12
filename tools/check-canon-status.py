#!/usr/bin/env python3
"""check-canon-status — validate canon-meta.md inline status fields.

Spec anchor:
    skills/novel-architect/assets/canon-meta-schema.md §1-§3 (Task 076)

Usage:
    python3 tools/check-canon-status.py [PATH ...]

PATHs may be individual canon-meta.md files or directories. Directories are
walked recursively for any file literally named `canon-meta.md`. With no
PATH supplied, the linter scans nothing (returns 0); the smoke-test target
in tools/check-governance.sh is `tools/tests/fixtures/novel-architect-v111/`.

Checks (all WARN-tier — Task 086-promotion-candidate but not gating yet):
  CANON.MISSING_FIELD     — required inline field absent (canon_id /
                            canon_status / canon_added_phase /
                            canon_added_at / canon_added_by)
  CANON.STATUS_ENUM       — canon_status not in
                            {proposed, accepted, contested, superseded, archived}
  CANON.PHASE_PATTERN     — canon_added_phase does not match `phase[1-7]`
  CANON.TIMESTAMP_FORMAT  — canon_added_at not ISO-8601 with Z suffix
  CANON.CONFLICT_EMPTY    — canon_status=contested but
                            canon_conflicts_with absent / empty
  CANON.SUPERSEDED_NO_RES — canon_status=superseded but
                            canon_resolved_by absent
  CANON.RECIPROCITY       — A lists B in canon_conflicts_with but B
                            does not list A back

Exit codes:
    0 — clean
    1 — usage error
    2 — at least one WARN diagnostic surfaced
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

VALID_STATUS = {"proposed", "accepted", "contested", "superseded", "archived"}
PHASE_RE = re.compile(r"^phase[1-7]$")
ISO_8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)
# Match a blockquote-delimited inline field of the form:
#   > - `canon_id`: value
INLINE_FIELD_RE = re.compile(
    r"^>\s*-\s*`(?P<key>[a-z_]+)`:\s*(?P<value>.+?)\s*$"
)
HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")


def parse_entries(text: str) -> list[dict[str, object]]:
    """Parse a canon-meta.md body into a list of entries, each a dict.

    An entry is a section starting with `##` whose first blockquote contains
    the inline fields. Returns one dict per entry with parsed key/value
    plus `_heading` (str) and `_line` (int — heading line, 1-indexed).
    """
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for lineno, line in enumerate(text.splitlines(), start=1):
        m_h = HEADING_RE.match(line)
        if m_h:
            if current is not None:
                entries.append(current)
            current = {"_heading": m_h.group("title"), "_line": lineno}
            continue
        if current is None:
            continue
        m_f = INLINE_FIELD_RE.match(line)
        if m_f:
            key = m_f.group("key")
            val = m_f.group("value").strip()
            # Strip surrounding backticks if present (list values like
            # `[id1, id2]` come through unchanged).
            current[key] = val.strip("`")
    if current is not None:
        entries.append(current)
    return entries


def _required_fields() -> list[str]:
    return ["canon_id", "canon_status", "canon_added_phase",
            "canon_added_at", "canon_added_by"]


def _parse_id_list(value: str) -> list[str]:
    """Parse a value like `[canon-foo-001, canon-bar-002]` → ["canon-foo-001",
    "canon-bar-002"]. Leading/trailing brackets optional."""
    v = value.strip().strip("[]")
    if not v:
        return []
    return [token.strip().strip("`") for token in v.split(",") if token.strip()]


def diagnostics_for(path: Path) -> list[str]:
    diags: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}::WARN:CANON.READ:cannot read file ({exc})"]

    entries = parse_entries(text)
    # Build id-index for reciprocity check.
    by_id: dict[str, dict[str, object]] = {}
    for e in entries:
        cid = e.get("canon_id")
        if isinstance(cid, str):
            by_id[cid] = e

    for entry in entries:
        line = entry["_line"]
        heading = entry["_heading"]
        loc = f"{path}:{line}"

        # CANON.MISSING_FIELD
        for field in _required_fields():
            if field not in entry:
                diags.append(
                    f"{loc}::WARN:CANON.MISSING_FIELD:"
                    f"entry `{heading}` missing required inline field `{field}`"
                )

        status = entry.get("canon_status")
        if isinstance(status, str):
            # CANON.STATUS_ENUM
            if status not in VALID_STATUS:
                diags.append(
                    f"{loc}::WARN:CANON.STATUS_ENUM:"
                    f"canon_status={status!r} not in {sorted(VALID_STATUS)}"
                )
            # CANON.CONFLICT_EMPTY
            if status == "contested":
                conflicts = entry.get("canon_conflicts_with")
                if not isinstance(conflicts, str) or not _parse_id_list(conflicts):
                    diags.append(
                        f"{loc}::WARN:CANON.CONFLICT_EMPTY:"
                        f"canon_status=contested but canon_conflicts_with absent/empty"
                    )
            # CANON.SUPERSEDED_NO_RES
            if status == "superseded" and "canon_resolved_by" not in entry:
                diags.append(
                    f"{loc}::WARN:CANON.SUPERSEDED_NO_RES:"
                    f"canon_status=superseded but canon_resolved_by absent"
                )

        # CANON.PHASE_PATTERN
        phase = entry.get("canon_added_phase")
        if isinstance(phase, str) and not PHASE_RE.match(phase):
            diags.append(
                f"{loc}::WARN:CANON.PHASE_PATTERN:"
                f"canon_added_phase={phase!r} does not match `phase[1-7]`"
            )

        # CANON.TIMESTAMP_FORMAT
        ts = entry.get("canon_added_at")
        if isinstance(ts, str) and not ISO_8601_RE.match(ts):
            diags.append(
                f"{loc}::WARN:CANON.TIMESTAMP_FORMAT:"
                f"canon_added_at={ts!r} not ISO-8601 with Z suffix"
            )

    # CANON.RECIPROCITY — second pass after id-index is built.
    for entry in entries:
        if entry.get("canon_status") != "contested":
            continue
        cid = entry.get("canon_id")
        conflicts_raw = entry.get("canon_conflicts_with")
        if not isinstance(cid, str) or not isinstance(conflicts_raw, str):
            continue
        for partner_id in _parse_id_list(conflicts_raw):
            partner = by_id.get(partner_id)
            if partner is None:
                continue  # Dangling reference is a different defect class.
            partner_conflicts_raw = partner.get("canon_conflicts_with")
            partner_conflicts = (
                _parse_id_list(partner_conflicts_raw)
                if isinstance(partner_conflicts_raw, str) else []
            )
            if cid not in partner_conflicts:
                diags.append(
                    f"{path}:{entry['_line']}::WARN:CANON.RECIPROCITY:"
                    f"entry {cid!r} lists {partner_id!r} in canon_conflicts_with "
                    f"but {partner_id!r} does not list {cid!r} back"
                )

    return diags


def _iter_canon_meta_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        # Explicit file argument is always processed (allows fixture corpora
        # like `canon-meta-stale.md` to be linted by name).
        yield target
        return
    if target.is_dir():
        # Directory walk only matches the canonical filename `canon-meta.md`.
        for p in sorted(target.rglob("canon-meta.md")):
            yield p


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-canon-status",
        description=(
            "Advisory linter for canon-meta.md inline status fields "
            "(skills/novel-architect/assets/canon-meta-schema.md)."
        ),
    )
    parser.add_argument("paths", nargs="*", help="canon-meta.md files or dirs")
    args = parser.parse_args(argv)

    targets = [Path(p) for p in args.paths]
    diags: list[str] = []
    for t in targets:
        if not t.exists():
            print(
                f"check-canon-status: warning: path does not exist: {t}",
                file=sys.stderr,
            )
            continue
        for f in _iter_canon_meta_files(t):
            diags.extend(diagnostics_for(f))

    for d in diags:
        print(d)
    print(
        f"check-canon-status: {len(diags)} WARN diagnostic(s) "
        f"across {len(targets)} target path(s).",
        file=sys.stderr,
    )
    return 2 if diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
