#!/usr/bin/env python3
"""
Maintenance bypass checker for the agency repository.

Returns 0 if all errors from the linters are covered by an open Task whose
`task_affects_paths` covers the offending file.
Returns 1 otherwise.
"""

import sys
import subprocess
from pathlib import Path
from _frontmatter import read_fm, str_list, str_val

def get_open_tasks():
    tasks = []
    tasks_dir = Path("tasks")
    if not tasks_dir.exists(): return []

    for task_dir in tasks_dir.iterdir():
        if not task_dir.is_dir(): continue
        task_md = task_dir / "task.md"
        if not task_md.exists(): continue

        fm = read_fm(task_md)
        if str_val(fm, "task_status") == "open":
            paths = str_list(fm, "task_affects_paths")
            if paths:
                tasks.append({"dir": task_dir.name, "paths": paths})
    return tasks

def main():
    linters = [
        ["python3", "tools/validate-frontmatter.py"],
        ["python3", "tools/lint-structure.py"],
        ["python3", "tools/lint-linkage.py"]
    ]

    error_files = set()
    for cmd in linters:
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Parse files from ERROR lines
        for line in result.stderr.splitlines():
            if line.startswith("ERROR "):
                # Format is usually "ERROR path/to/file: message"
                parts = line.split(":", 1)
                if len(parts) > 1:
                    filepath = parts[0].replace("ERROR ", "").strip()
                    error_files.add(filepath)

    if not error_files:
        return 0

    open_tasks = get_open_tasks()

    # Check if every error file is covered by at least one open task
    for error_file in error_files:
        covered = False
        for task in open_tasks:
            for path in task["paths"]:
                if path in error_file or error_file in path:
                    covered = True
                    break
            if covered:
                break

        if not covered:
            print(f"Bypass denied: Error in {error_file} is not covered by any open Task's task_affects_paths", file=sys.stderr)
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
