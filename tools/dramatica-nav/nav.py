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


def _sub(sub: Any, name: str, help_text: str) -> argparse.ArgumentParser:
    """Add a subparser pre-loaded with --full and --md output flags."""
    sp = sub.add_parser(name, help=help_text)
    sp.add_argument("value", help="Query value.")
    sp.add_argument("--full", action="store_true", help="Inline prose via extract.py.")
    sp.add_argument("--md", action="store_true", help="Emit Markdown table instead of JSON.")
    return sp


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=PROG,
        description="Dramatica ontology navigator — query 7 lookup axes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="subcmd", required=True)

    sp = _sub(sub, "by-id", "Fetch single entry by ontology id (e.g. el.trust).")
    sp.add_argument("--include-pairs", action="store_true", default=False,
                    help="Attach dynamic_pairs array to result.")

    sp = _sub(sub, "by-alias", "Fetch entry whose aliases_<lang> contains value.")
    sp.add_argument("--lang", default="en", metavar="LANG",
                    help="Locale for alias lookup (default: en).")

    sp = _sub(sub, "by-scenario", "All entries tagged with a scenario id.")
    sp.add_argument("--kind", default=None, metavar="KIND",
                    help="Filter results to this entry kind.")

    _sub(sub, "by-quad", "The 4 quad members for a quad_id.")
    _sub(sub, "by-ktad", "All entries at a KTAD position (K/T/A/D).")
    _sub(sub, "by-ncp", "All entries with a given NCP appreciation mapping.")
    _sub(sub, "by-pair", "dp.* dynamic-pair entries containing member_id.")

    return p


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
