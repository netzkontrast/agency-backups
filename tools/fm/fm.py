#!/usr/bin/env python3
"""fm — single-entry dispatcher for the flexible-frontmatter toolchain.

Subcommands:
    fm validate ...   delegate to tools.fm.validate.main
    fm extract ...    delegate to tools.fm.extract.main
    fm edit ...       delegate to tools.fm.edit.main
    fm query ...      delegate to tools.fm.query.main
    fm section ...    delegate to tools.fm.section.main
    fm rename ...     delegate to tools.fm.rename.main
    fm graph ...      delegate to tools.fm.graph.main
    fm new ...        delegate to tools.fm.new.main
    fm fix ...        delegate to tools.fm.fix.main

Each subcommand module is imported only when its name is invoked
(lazy dispatch); per-invocation import latency stays scoped to the
target module.

Each subcommand module continues to work standalone via
`python3 tools/fm/<name>.py …` — this wrapper is additive.
"""
from __future__ import annotations

import difflib
import importlib
import sys
from pathlib import Path

EXIT_USAGE = 2

# subcommand name → module name (relative). One-line summary populated
# lazily from the module docstring when --help asks.
_SUBCOMMANDS: dict[str, str] = {
    "validate": "validate",
    "extract": "extract",
    "edit": "edit",
    "query": "query",
    "section": "section",
    "rename": "rename",
    "graph": "graph",
    "new": "new",
    "fix": "fix",
}


def _import_subcommand(name: str):
    """Import tools.fm.<name> (or, when run as a script, plain <name>).

    Returns the module's `main` callable.
    """
    if __package__:
        mod = importlib.import_module(f".{name}", package=__package__)
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        mod = importlib.import_module(name)
    return mod.main


def _summary(module_path: Path) -> str:
    """Return the first line of the module's docstring, or ''."""
    try:
        text = module_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for i, line in enumerate(text):
        if line.startswith('"""'):
            first = line[3:].strip()
            if first.endswith('"""'):
                first = first[:-3].strip()
            if first:
                return first
            # Multi-line docstring — first non-empty line below.
            for j in range(i + 1, min(i + 5, len(text))):
                if text[j].strip():
                    return text[j].strip()
            break
    return ""


def _print_help() -> int:
    here = Path(__file__).resolve().parent
    print("usage: fm <subcommand> [args...]")
    print("")
    print("subcommands:")
    width = max(len(s) for s in _SUBCOMMANDS) + 2
    for sub, modname in sorted(_SUBCOMMANDS.items()):
        s = _summary(here / f"{modname}.py")
        print(f"  {sub:<{width}} {s}")
    print("")
    print("each subcommand also runs standalone: python3 tools/fm/<name>.py")
    return 0


def _did_you_mean(name: str) -> str:
    matches = difflib.get_close_matches(name, list(_SUBCOMMANDS), n=3, cutoff=0.6)
    return f" Did you mean: {', '.join(matches)}?" if matches else ""


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args or args[0] in ("-h", "--help"):
        return _print_help()
    sub = args[0]
    if sub not in _SUBCOMMANDS:
        print(f"fm: unknown subcommand {sub!r}.{_did_you_mean(sub)}", file=sys.stderr)
        return EXIT_USAGE
    main_fn = _import_subcommand(_SUBCOMMANDS[sub])
    return main_fn(args[1:])


if __name__ == "__main__":
    sys.exit(main())
