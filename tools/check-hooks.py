#!/usr/bin/env python3
"""check-hooks — Task 094 ST-3 governance check.

Verifies bidirectional consistency between the hook scripts under
`tools/hooks/` and the registrations in `.claude/settings.json`. Also
enforces ADR-0011 D.7: no hook MAY be registered on the `SessionStart`
event.

Diagnostic codes
----------------

  * `H.1.1` — Orphan script: `tools/hooks/<name>.sh` exists but is not
              registered in `.claude/settings.json`.
  * `H.1.2` — Orphan registration: `.claude/settings.json` references a
              script that does not exist (or is not executable).
  * `H.1.3` — SessionStart violation: a hook is registered on
              `SessionStart` (ADR-0011 D.7 forbids).

Diagnostic shape mirrors the other linters in `tools/`:
  ``<surface>::<level>:<code>:<message>``

Exit codes
----------

  * 0 — clean (no diagnostics).
  * 1 — one or more ERROR diagnostics.

Usage
-----

    python3 tools/check-hooks.py [--settings PATH] [--hooks-dir PATH]

The defaults assume the script runs from the repo root. The flags exist
so the pytest fixture can point at a temp directory.

Spec anchors
------------

  * Task 094 ST-3 subtask spec — acceptance criterion `T094.3.2`.
  * ADR-0011 D.7 — SessionStart prohibition.
  * CLAUDE.md §14 — hooks framework documentation.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FAIL = 1

FORBIDDEN_EVENTS = ("SessionStart",)


def _iter_hook_scripts(hooks_dir: Path) -> list[Path]:
    """Return the sorted list of `*.sh` files in hooks_dir."""
    if not hooks_dir.is_dir():
        return []
    return sorted(p for p in hooks_dir.glob("*.sh") if p.is_file())


def _load_settings(settings_path: Path) -> dict:
    if not settings_path.is_file():
        return {}
    try:
        return json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _iter_registrations(settings: dict) -> list[tuple[str, str]]:
    """Yield (event, command) tuples for every registration block."""
    out: list[tuple[str, str]] = []
    hooks = settings.get("hooks", {})
    if not isinstance(hooks, dict):
        return out
    for event, blocks in hooks.items():
        if not isinstance(event, str):
            continue
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            inner = block.get("hooks", [])
            if not isinstance(inner, list):
                continue
            for entry in inner:
                if not isinstance(entry, dict):
                    continue
                command = entry.get("command", "")
                if not isinstance(command, str) or not command:
                    continue
                out.append((event, command))
    return out


def _emit(diagnostics: list[str], surface: str, code: str, message: str) -> None:
    diagnostics.append(f"{surface}::ERROR:{code}:{message}")


def audit(repo: Path, settings_path: Path, hooks_dir: Path) -> list[str]:
    """Return the list of ERROR diagnostics. Empty list = clean."""
    diagnostics: list[str] = []
    settings = _load_settings(settings_path)
    registrations = _iter_registrations(settings)

    # H.1.3 — SessionStart violation (D.7).
    for event, command in registrations:
        if event in FORBIDDEN_EVENTS:
            _emit(
                diagnostics,
                surface=settings_path.as_posix(),
                code="H.1.3",
                message=(
                    f"hook registered on forbidden event '{event}' "
                    f"(command: {command}); ADR-0011 D.7 prohibits "
                    "SessionStart-hook injection — use UserPromptSubmit, "
                    "PreToolUse, PostToolUse, Stop, or SubagentStop instead."
                ),
            )

    # H.1.2 — Orphan registration: registered script missing or not executable.
    seen_commands: set[str] = set()
    for event, command in registrations:
        seen_commands.add(command)
        # Resolve relative paths against the repo root.
        cmd_path = Path(command)
        if not cmd_path.is_absolute():
            cmd_path = (repo / cmd_path).resolve()
        if not cmd_path.is_file():
            _emit(
                diagnostics,
                surface=settings_path.as_posix(),
                code="H.1.2",
                message=(
                    f"registration on event '{event}' points at "
                    f"missing script: {command}"
                ),
            )
            continue
        if not os.access(cmd_path, os.X_OK):
            _emit(
                diagnostics,
                surface=settings_path.as_posix(),
                code="H.1.2",
                message=(
                    f"registered script is not executable: {command} "
                    "(run `chmod +x` to fix)"
                ),
            )

    # H.1.1 — Orphan script: tools/hooks/*.sh not registered anywhere.
    for script in _iter_hook_scripts(hooks_dir):
        rel = script.relative_to(repo).as_posix() if script.is_absolute() else script.as_posix()
        # Match registrations whose command resolves to this script.
        registered = False
        for command in seen_commands:
            cmd_path = Path(command)
            if not cmd_path.is_absolute():
                cmd_path = (repo / cmd_path).resolve()
            if cmd_path == script.resolve():
                registered = True
                break
        if not registered:
            _emit(
                diagnostics,
                surface=rel,
                code="H.1.1",
                message=(
                    "hook script is not registered in .claude/settings.json; "
                    "either register it or delete the script."
                ),
            )

    return diagnostics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify hooks/* ↔ .claude/settings.json bidirectional consistency.",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        default=None,
        help="Path to .claude/settings.json (default: <repo>/.claude/settings.json).",
    )
    parser.add_argument(
        "--hooks-dir",
        type=Path,
        default=None,
        help="Path to the hooks directory (default: <repo>/tools/hooks).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo root (default: parent of tools/).",
    )
    args = parser.parse_args(argv)

    repo = args.repo_root or Path(__file__).resolve().parents[1]
    settings_path = args.settings or (repo / ".claude" / "settings.json")
    hooks_dir = args.hooks_dir or (repo / "tools" / "hooks")

    diagnostics = audit(repo, settings_path, hooks_dir)
    for line in diagnostics:
        print(line, file=sys.stderr)

    if diagnostics:
        return EXIT_FAIL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
