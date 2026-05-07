#!/usr/bin/env python3
"""migrate-waivers — translate legacy per-file waivers to per-rule TSV.

Spec anchor: PRE_COMMIT.md §7.B (Task 037 ST-3 refactor).

Legacy format (one path-glob per line, comments allowed):

    tasks/030-*/notes.md
    research/foo/output/SPEC.md

New format (TSV, four columns):

    tasks/030-*/notes.md\\t*\\tlegacy carry-over (re-justify)\\t<+90d>
    research/foo/output/SPEC.md\\t*\\tlegacy carry-over (re-justify)\\t<+90d>

The migration is semantics-preserving: each legacy row becomes a
wildcard (`*`) per-rule entry, which silences every rule for the listed
glob — the same behaviour the legacy validator gave. The agent is
EXPECTED to walk the migrated rows and tighten each one to a specific
rule-id, per the burn-down protocol.

Usage:

    python3 tools/scripts/migrate-waivers.py             # in-place
    python3 tools/scripts/migrate-waivers.py --dry-run   # preview only
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WAIVERS = REPO / "tools" / ".frontmatter-waivers"

HEADER = """# tools/.frontmatter-waivers — per-rule waiver ledger (PRE_COMMIT.md §7.B).
#
# Migrated from legacy per-file format on {today} via
# tools/scripts/migrate-waivers.py. Each row below was a single path-glob
# in the legacy file and has been promoted to a wildcard (`*`) rule-id —
# semantically identical to the legacy "silence everything for this file"
# behaviour. The agent SHOULD tighten each row to a specific diagnostic
# code per the §7.B burn-down protocol.
#
#path-glob\trule-id\trationale\texpires
"""


def _is_legacy(raw: str) -> bool:
    return "\t" not in raw.strip()


def migrate(text: str, *, today: str) -> str:
    out_lines: list[str] = [HEADER.format(today=today).rstrip()]
    expires = (
        _dt.date.fromisoformat(today) + _dt.timedelta(days=90)
    ).isoformat()
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not _is_legacy(raw):
            # Already-migrated row — emit unchanged.
            out_lines.append(raw.rstrip())
            continue
        # Legacy single-path row → wildcard per-rule entry.
        glob = stripped
        rationale = "legacy carry-over (re-justify per §7.B burn-down)"
        out_lines.append(f"{glob}\t*\t{rationale}\t{expires}")
    out_lines.append("")  # trailing newline
    return "\n".join(out_lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Translate tools/.frontmatter-waivers from legacy per-file "
            "to per-rule TSV format. Idempotent: already-migrated files "
            "pass through unchanged."
        ),
    )
    p.add_argument("--dry-run", action="store_true",
                   help="print the migrated content to stdout; do not write.")
    args = p.parse_args(argv)

    if not WAIVERS.exists():
        print(
            f"{WAIVERS.relative_to(REPO)}: file does not exist; nothing to "
            f"migrate.",
            file=sys.stderr,
        )
        return 0

    text = WAIVERS.read_text(encoding="utf-8")
    today = _dt.date.today().isoformat()
    migrated = migrate(text, today=today)

    if args.dry_run:
        sys.stdout.write(migrated if migrated.endswith("\n") else migrated + "\n")
        return 0
    WAIVERS.write_text(migrated if migrated.endswith("\n") else migrated + "\n",
                       encoding="utf-8")
    print(f"{WAIVERS.relative_to(REPO)}: migrated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
