#!/usr/bin/env python3
"""
Run-log validator for the agency repository.

Validates `maintenance/run-log.md` records to ensure:
- single hash per `end_commit`
- ISO date formats in headers
- required fields are present
"""

import sys
import re
from pathlib import Path

REQUIRED_FIELDS = [
    "agent", "start_commit", "end_commit", "baseline_commit",
    "files_in_delta", "files_scanned", "t1_fixes", "t2_fixes",
    "t3_tasks_created", "t4_skipped", "issues_skipped", "notes"
]

def check_runlog():
    try:
        with open("maintenance/run-log.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return ["maintenance/run-log.md not found"]

    errors = []

    # Extract records which start with "### Run "
    records_part = content.split("## Run Records")[1]
    runs = re.finditer(r'^### Run (.*?)\n((?:(?!\n### Run ).)*)', records_part, re.MULTILINE | re.DOTALL)

    run_count = 0
    for match in runs:
        run_count += 1
        header_text = match.group(1).strip()
        run_text = match.group(2)

        # Validate ISO date format YYYY-MM-DD
        if not re.match(r'^\d{4}-\d{2}-\d{2} — .+', header_text):
            errors.append(f"Run '{header_text}': Header missing valid ISO date format 'YYYY-MM-DD — <routine-type>'")

        # Check required fields
        for field in REQUIRED_FIELDS:
            if not re.search(rf'^- {field}:', run_text, re.MULTILINE):
                errors.append(f"Run '{header_text}': Missing required field '- {field}:'")

        # Check single hash per end_commit
        end_commit_match = re.search(r'^- end_commit:\s+(.*)$', run_text, re.MULTILINE)
        if end_commit_match:
            end_commit_val = end_commit_match.group(1).strip()
            hashes = end_commit_val.split()
            if len(hashes) > 1:
                errors.append(f"Run '{header_text}': end_commit has multiple hashes or extra text: '{end_commit_val}'")

    if run_count == 0:
        errors.append("No run records found in maintenance/run-log.md")

    return errors

def main():
    errors = check_runlog()
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
