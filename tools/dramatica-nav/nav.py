"""Dramatica-nav CLI — routes 7 subcommands to lib/ontology indexes.

JSON by default; --md for human-readable tables; --full to inline prose.

Exit codes: 0 success  1 empty results  2 bad args  3 ontology load
            4 lookup not found  5 extract.py failure
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import LookupNotFoundError, OntologyError
from lib import ontology as ontology_lib
from lib.ontology import OntologyIndex

PROG = Path(__file__).name


# ---------------------------------------------------------------------------
# Shared argument parent parsers
# ---------------------------------------------------------------------------

def _output_parent() -> argparse.ArgumentParser:
    """Common output flags shared across all subcommands."""
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--full", action="store_true", help="Inline prose via extract.py.")
    p.add_argument("--md", action="store_true", help="Emit Markdown table instead of JSON.")
    return p


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _emit_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _md_single(entry: dict) -> str:
    lines = ["| key | value |", "| --- | --- |"]
    for k, v in entry.items():
        cell = json.dumps(v) if not isinstance(v, str) else v
        lines.append(f"| {k} | {cell} |")
    return "\n".join(lines)


def _md_multi(entries: list[dict]) -> str:
    if not entries:
        return "_No results._"
    lines = ["| id | kind | canonical_label |", "| --- | --- | --- |"]
    for e in entries:
        eid = e.get("id", "")
        kind = e.get("kind", "")
        label = e.get("canonical_label", "")
        lines.append(f"| {eid} | {kind} | {label} |")
    return "\n".join(lines)


def _emit(payload: Any, *, md: bool) -> None:
    if not md:
        _emit_json(payload)
        return
    if isinstance(payload, list):
        print(_md_multi(payload))
    else:
        print(_md_single(payload))


# ---------------------------------------------------------------------------
# --full prose inlining
# ---------------------------------------------------------------------------

def _inline_prose(entry: dict) -> dict:
    """Call extract.py for entry['id'] and attach its stdout as 'prose'."""
    entry_id = entry["id"]
    script = Path(__file__).resolve().parent / "extract.py"
    result = subprocess.run(
        ["python3", str(script), entry_id],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        msg = result.stderr.strip() or f"extract.py exited {result.returncode}"
        print(f"{PROG}: --full: {msg}", file=sys.stderr)
        sys.exit(5)
    return {**entry, "prose": result.stdout}


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_by_id(
    idx: OntologyIndex,
    args: argparse.Namespace,
) -> int:
    try:
        entry = idx.by_id(args.value)
    except LookupNotFoundError:
        print(f"{PROG}: by-id: no entry with id={args.value!r}", file=sys.stderr)
        return 4

    if args.include_pairs:
        pairs = idx.by_pair(args.value)
        entry = {**entry, "dynamic_pairs": pairs}

    if args.full:
        entry = _inline_prose(entry)

    _emit(entry, md=args.md)
    return 0


def cmd_by_alias(
    idx: OntologyIndex,
    args: argparse.Namespace,
) -> int:
    try:
        entry = idx.by_alias(args.value, locale=args.lang)
    except LookupNotFoundError:
        print(
            f"{PROG}: by-alias: no entry with alias={args.value!r} in locale={args.lang!r}",
            file=sys.stderr,
        )
        return 4

    if args.full:
        entry = _inline_prose(entry)

    _emit(entry, md=args.md)
    return 0


def cmd_by_scenario(idx: OntologyIndex, args: argparse.Namespace) -> int:
    results = idx.by_scenario(args.value, kind=args.kind)
    _emit(results, md=args.md)
    return 1 if not results else 0


def cmd_by_quad(idx: OntologyIndex, args: argparse.Namespace) -> int:
    results = idx.by_quad(args.value)
    if not results:
        print(f"{PROG}: by-quad: 0 members for quad_id={args.value!r}", file=sys.stderr)
    _emit(results, md=args.md)
    return 1 if not results else 0


def cmd_by_ktad(idx: OntologyIndex, args: argparse.Namespace) -> int:
    results = idx.by_ktad(args.value)
    _emit(results, md=args.md)
    return 1 if not results else 0


def cmd_by_ncp(idx: OntologyIndex, args: argparse.Namespace) -> int:
    results = idx.by_ncp(args.value)
    _emit(results, md=args.md)
    return 1 if not results else 0


def cmd_by_pair(idx: OntologyIndex, args: argparse.Namespace) -> int:
    results = idx.by_pair(args.value)
    _emit(results, md=args.md)
    return 1 if not results else 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    out = _output_parent()
    p = argparse.ArgumentParser(
        prog=PROG,
        description="Dramatica ontology navigator — query 7 lookup axes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="subcmd", required=True)

    # by-id: single-record; supports --full, --md, --include-pairs
    sp = sub.add_parser("by-id", parents=[out], help="Fetch single entry by ontology id.")
    sp.add_argument("value", help="Ontology id (e.g. el.trust).")
    sp.add_argument("--include-pairs", action="store_true", default=False,
                    help="Attach dynamic_pairs array to result.")

    # by-alias: single-record; supports --full, --md, --lang
    sp = sub.add_parser("by-alias", parents=[out], help="Fetch entry by alias in a locale.")
    sp.add_argument("value", help="Alias string to search.")
    sp.add_argument("--lang", default="en", metavar="LANG",
                    help="Locale for alias lookup (default: en).")

    # by-scenario: multi-record; supports --md, --kind
    sp = sub.add_parser("by-scenario", parents=[out],
                        help="All entries tagged with a scenario id.")
    sp.add_argument("value", help="Scenario id (e.g. novel.crucial-element-audit).")
    sp.add_argument("--kind", default=None, metavar="KIND",
                    help="Filter results to this entry kind.")

    # by-quad: multi-record; supports --md
    sp = sub.add_parser("by-quad", parents=[out], help="The 4 quad members for a quad_id.")
    sp.add_argument("value", help="Quad id (e.g. quad.logic-feeling-el).")

    # by-ktad: multi-record; supports --md
    sp = sub.add_parser("by-ktad", parents=[out],
                        help="All entries at a KTAD position (K/T/A/D).")
    sp.add_argument("value", help="KTAD position letter.")

    # by-ncp: multi-record; supports --md
    sp = sub.add_parser("by-ncp", parents=[out],
                        help="All entries with a given NCP appreciation mapping.")
    sp.add_argument("value", help="NCP appreciation string.")

    # by-pair: multi-record; supports --md
    sp = sub.add_parser("by-pair", parents=[out],
                        help="dp.* dynamic-pair entries containing member_id.")
    sp.add_argument("value", help="Member id (e.g. el.trust).")

    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

_HANDLERS = {
    "by-id": cmd_by_id,
    "by-alias": cmd_by_alias,
    "by-scenario": cmd_by_scenario,
    "by-quad": cmd_by_quad,
    "by-ktad": cmd_by_ktad,
    "by-ncp": cmd_by_ncp,
    "by-pair": cmd_by_pair,
}


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        idx = ontology_lib.load()
    except OntologyError as exc:
        print(f"{PROG}: ontology load failure: {exc}", file=sys.stderr)
        sys.exit(3)

    handler = _HANDLERS.get(args.subcmd)
    if handler is None:
        print(f"{PROG}: unknown subcommand {args.subcmd!r}", file=sys.stderr)
        sys.exit(2)

    sys.exit(handler(idx, args))


if __name__ == "__main__":
    main()
