#!/usr/bin/env python3
"""Maintenance bypass checker for the agency repository.

Returns 0 if every linter ERROR is covered by an open Task whose
`task_affects_paths` covers the offending file. Returns 1 otherwise.

Task 017 re-pointed this checker at fm-validate's diagnostic format
(`<path>::<level>:<code>:<msg>`, per SPEC §5.1) and folded the
remaining structural and linkage checks in via tools/legacy/. The
fm-validate output is the canonical source; the legacy linters cover
the structural/cross-ref gaps until those land in the fm- toolchain.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "fm"))
import _core  # type: ignore  # noqa: E402

read_fm = _core.read_fm
str_list = _core.str_list
str_val = _core.str_val


def get_open_tasks() -> list[dict]:
    tasks: list[dict] = []
    tasks_dir = Path("tasks")
    if not tasks_dir.exists():
        return []
    for task_dir in sorted(tasks_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        task_md = task_dir / "task.md"
        if not task_md.exists():
            continue
        fm = read_fm(task_md)
        if str_val(fm, "task_status") == "open":
            paths = str_list(fm, "task_affects_paths")
            if paths:
                tasks.append({"dir": task_dir.name, "paths": paths})
    return tasks


def _files_from_fm_validate() -> set[str]:
    """Run fm-validate and harvest error file paths."""
    result = subprocess.run(
        ["python3", "tools/fm/validate.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    files: set[str] = set()
    for line in result.stdout.splitlines():
        if "::ERROR:" not in line:
            continue
        path, _ = line.split("::", 1)
        files.add(path.strip())
    return files


def _files_from_legacy_linters() -> set[str]:
    """Cover structural + linkage gaps until they fold into fm-*."""
    files: set[str] = set()
    env = {**os.environ, "FM_LEGACY_QUIET": "1"}
    for cmd in (
        ["python3", "tools/legacy/lint-structure.py"],
        ["python3", "tools/legacy/lint-linkage.py"],
    ):
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
        for line in result.stderr.splitlines():
            if line.startswith("ERROR "):
                payload = line[len("ERROR "):].split(":", 1)[0].strip()
                if payload:
                    files.add(payload)
    return files


def main() -> int:
    error_files = _files_from_fm_validate() | _files_from_legacy_linters()
    if not error_files:
        return 0

    open_tasks = get_open_tasks()

    for error_file in sorted(error_files):
        covered = False
        for task in open_tasks:
            for path in task["paths"]:
                if path in error_file or error_file in path:
                    covered = True
                    break
            if covered:
                break
        if not covered:
            print(
                f"Bypass denied: Error in {error_file} is not covered by any "
                "open Task's task_affects_paths",
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
