#!/usr/bin/env python3
"""fm-extract — read a single section, the frontmatter, or a frontmatter key.

Spec anchor: F.5.2.

Usage:
    fm-extract <path> --section <heading-name>
    fm-extract <path> --frontmatter
    fm-extract <path> --frontmatter <key>
    fm-extract <path> --whole-file

Token caps (per SPEC §5.2):
    --section : ≤ 4096 bytes; oversize emits the first 4 KB plus a
                "… [truncated; original N bytes]" trailer.
    --frontmatter : ≤ 2048 bytes (no truncation marker; an oversize file
                    is itself a violation, but we still emit the head).
    --whole-file : no cap.

Exit codes:
    0 — output emitted
    2 — usage error
    3 — heading or key not found
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

SECTION_CAP = 4096
FRONTMATTER_CAP = 2048
TRUNCATION_FMT = "\n… [truncated; original {n} bytes]\n"


def _truncate(payload: str, cap: int) -> str:
    raw = payload.encode("utf-8")
    if len(raw) <= cap:
        return payload
    marker = TRUNCATION_FMT.format(n=len(raw))
    head_budget = cap - len(marker.encode("utf-8"))
    if head_budget < 0:
        head_budget = 0
    head = raw[:head_budget].decode("utf-8", errors="ignore")
    return head + marker


def extract_section(path: Path, heading: str) -> tuple[str, int]:
    text = path.read_text(encoding="utf-8")
    found = _core.find_section_body(text, heading)
    if found is None:
        return "", 3
    body, _, _ = found
    return _truncate(body, SECTION_CAP), 0


def extract_frontmatter(path: Path, key: str | None) -> tuple[str, int]:
    text = path.read_text(encoding="utf-8")
    fm_block, _ = _core.split_frontmatter_and_body(text)
    if not fm_block:
        return "", 3
    if key is None:
        return _truncate(fm_block, FRONTMATTER_CAP), 0
    fm = _core.parse_frontmatter(text, strict=False)
    if key not in fm:
        return "", 3
    val = fm[key]
    if isinstance(val, list):
        out = "\n".join(val)
    else:
        out = str(val)
    return _truncate(out + ("\n" if not out.endswith("\n") else ""),
                     FRONTMATTER_CAP), 0


def extract_whole_file(path: Path) -> tuple[str, int]:
    return path.read_text(encoding="utf-8"), 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-extract", add_help=True)
    p.add_argument("path", type=Path)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--section", metavar="HEADING")
    g.add_argument("--frontmatter", nargs="?", const="", metavar="KEY",
                   help="emit the frontmatter block, or one key when KEY given")
    g.add_argument("--whole-file", action="store_true")
    args = p.parse_args(argv)

    if not args.path.exists():
        print(f"fm-extract: no such file: {args.path}", file=sys.stderr)
        return 2

    if args.section is not None:
        out, rc = extract_section(args.path, args.section)
        if rc != 0:
            print(f"fm-extract: heading '## {args.section}' not found in {args.path}",
                  file=sys.stderr)
            return rc
        sys.stdout.write(out)
        if not out.endswith("\n"):
            sys.stdout.write("\n")
        return 0

    if args.frontmatter is not None:
        key = args.frontmatter or None
        out, rc = extract_frontmatter(args.path, key)
        if rc != 0:
            target = f"key {key!r}" if key else "frontmatter block"
            print(f"fm-extract: {target} not found in {args.path}",
                  file=sys.stderr)
            return rc
        sys.stdout.write(out)
        if not out.endswith("\n"):
            sys.stdout.write("\n")
        return 0

    if args.whole_file:
        out, rc = extract_whole_file(args.path)
        sys.stdout.write(out)
        return rc

    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
