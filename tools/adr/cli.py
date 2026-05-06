#!/usr/bin/env python3
"""agency-adr — ADR governance CLI.

Spec anchors: ADR.A.5.1, ADR.A.5.2, ADR.A.5.3, ADR.A.5.5, ADR.A.5.8.

Usage:
    python3 tools/adr/cli.py validate [PATH ...] [--scope=decisions]
                                       [--strict] [--format=text|json]
    python3 tools/adr/cli.py synthesize [--token-limit=N] [--fidelity-floor=F]
                                         [--fidelity-mode=...] [--dry-run]
                                         [--format=text|json]

Exit:
    0 — no ERROR diagnostics
    1 — at least one ERROR diagnostic (or any WARN under --strict)
    2 — usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402
from adr import body as adr_body  # type: ignore  # noqa: E402
from adr import schema as adr_schema  # type: ignore  # noqa: E402
from adr import corpus as adr_corpus  # type: ignore  # noqa: E402
from adr import graph as adr_graph  # type: ignore  # noqa: E402
from adr import ids as adr_ids  # type: ignore  # noqa: E402
from adr.synthesize import synthesize as run_synthesize  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic


def _validate_corpus(
    corpus: list[adr_corpus.AdrRecord],
    ontology: dict,
) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    diags.extend(adr_corpus.parse_diagnostics(corpus))
    for rec in corpus:
        if rec.parse_error:
            continue
        diags.extend(adr_schema.validate_frontmatter(
            rec.frontmatter, ontology=ontology, rel=rec.rel,
        ))
        diags.extend(adr_body.validate_body(rec.text, rec.rel))
    diags.extend(adr_ids.check_unique_ids(corpus))
    diags.extend(adr_ids.check_filename_coupling(corpus))
    g = adr_graph.build_graph(corpus)
    diags.extend(adr_graph.check_cycles(g))
    diags.extend(adr_graph.check_reciprocity(g))
    diags.extend(adr_graph.check_orphans(g))
    return diags


def _emit(diags: list[Diagnostic], fmt: str, *, checked: int, stream=sys.stderr) -> None:
    error_count = sum(1 for d in diags if d.severity == "ERROR")
    warn_count = sum(1 for d in diags if d.severity == "WARN")
    if fmt == "json":
        print(json.dumps({
            "checked": checked,
            "diagnostics": [d.to_json() for d in diags],
            "errors": error_count,
            "warnings": warn_count,
        }, indent=2))
    else:
        for d in diags:
            print(d.render(), file=stream)
        print(f"Checked {checked} ADR(s); {len(diags)} diagnostic(s).")


def _exit_code(diags: list[Diagnostic], strict: bool) -> int:
    if any(d.severity == "ERROR" for d in diags):
        return 1
    if strict and any(d.severity == "WARN" for d in diags):
        return 1
    return 0


def run_validate(
    paths: list[str] | None = None,
    *,
    strict: bool = False,
    fmt: str = "text",
    repo_root: Path | None = None,
) -> int:
    repo = repo_root or _core.repo_root_from_cwd()
    ontology = _core.load_ontology(repo)
    decisions = repo / "decisions"
    if not decisions.exists() or not any(decisions.glob("*.md")):
        # ADR.A.5.x graceful no-op: empty / absent corpus exits clean.
        if fmt == "json":
            print(json.dumps({
                "checked": 0,
                "diagnostics": [],
                "errors": 0,
                "warnings": 0,
            }, indent=2))
        else:
            print("Checked 0 ADR(s); 0 diagnostic(s).")
        return 0
    corpus = adr_corpus.load_corpus(repo_root=repo)
    if paths:
        targets = {Path(p).resolve() for p in paths}
        corpus = [r for r in corpus if r.path.resolve() in targets]
    diags = _validate_corpus(corpus, ontology)
    _emit(diags, fmt, checked=len(corpus))
    return _exit_code(diags, strict)


def run_synthesize_cmd(args: argparse.Namespace) -> int:
    repo = _core.repo_root_from_cwd()
    agents_md = repo / "AGENTS.md"
    result = run_synthesize(
        agents_md=agents_md,
        decisions_root=repo / "decisions",
        token_limit=args.token_limit,
        fidelity_floor=args.fidelity_floor,
        fidelity_mode=args.fidelity_mode,
        dry_run=args.dry_run,
        repo_root=repo,
    )
    diags = list(result.diagnostics)
    if args.format == "json":
        payload = {
            "checked": 1,
            "diagnostics": [d.to_json() for d in diags],
            "errors": sum(1 for d in diags if d.severity == "ERROR"),
            "warnings": sum(1 for d in diags if d.severity == "WARN"),
            "fidelity": result.fidelity,
            "token_count": (
                result.section.token_count if result.section else 0
            ),
            "written": result.written,
            "dry_run": args.dry_run,
            "contributing_adr_ids": list(
                result.section.contributing_adr_ids if result.section else ()
            ),
        }
        if args.dry_run and result.section:
            payload["dry_run_body"] = result.section.body
        print(json.dumps(payload, indent=2))
    else:
        for d in diags:
            print(d.render(), file=sys.stderr)
        if result.section:
            print(
                f"Synthesised {len(result.section.contributing_adr_ids)} ADR(s) "
                f"into {result.section.token_count} tokens "
                f"(fidelity={result.fidelity:.4f}); "
                f"{'dry-run' if args.dry_run else ('rewrote' if result.written else 'unchanged')} "
                f"AGENTS.md."
            )
        else:
            print(
                f"Synthesis aborted; {len(diags)} diagnostic(s).",
                file=sys.stderr,
            )
    return result.exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agency-adr", add_help=True)
    sub = parser.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="check ADR corpus against the JSON-Schema")
    v.add_argument("paths", nargs="*")
    v.add_argument("--scope", default="decisions",
                   help="(reserved; only 'decisions' is supported)")
    v.add_argument("--strict", action="store_true",
                   help="promote WARN diagnostics to a non-zero exit")
    v.add_argument("--format", choices=("text", "json"), default="text")

    s = sub.add_parser("synthesize", help="rewrite the guarded section in AGENTS.md")
    s.add_argument("--token-limit", type=int, default=2000)
    s.add_argument("--fidelity-floor", type=float, default=0.95)
    s.add_argument("--fidelity-mode",
                   choices=("bcp14-keyword", "adr-id-anchor", "llm-pass"),
                   default="bcp14-keyword")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args(argv)
    if args.command == "validate":
        return run_validate(
            paths=list(args.paths) if args.paths else None,
            strict=args.strict,
            fmt=args.format,
        )
    if args.command == "synthesize":
        return run_synthesize_cmd(args)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
