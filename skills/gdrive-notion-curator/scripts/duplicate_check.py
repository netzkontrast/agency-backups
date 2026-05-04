#!/usr/bin/env python3
"""Check if a Drive-File is a duplicate based on Title-Patterns + MD5.

NOTE: This script implements rules 2-5 from references/duplicate-handling.md.
Rule 1 (Original Drive ID schon in Notion-DB) muss separate via Notion-Lookup
geprüft werden — das passiert direkt im MCP-Workflow ohne Python.

Usage:
    python3 duplicate_check.py \\
      --title "<title>" \\
      [--mime "<mime>"] \\
      [--md5 "<md5>"] \\
      [--size <bytes>] \\
      [--known-md5s "<md5_1>,<md5_2>,..."] \\
      [--known-titles "<t1>|<t2>|..."]

Output (JSON):
    {
      "is_duplicate": bool,
      "skip_copy": bool,
      "create_entry_with_duplicate_status": bool,
      "reason": "string",
      "manual_action_hint": "string or null"
    }
"""
from __future__ import annotations

import argparse
import json
import re
import sys


def check(args) -> dict:
    title = args.title
    title_lower = title.lower()

    known_md5s = set(args.known_md5s.split(',')) if args.known_md5s else set()
    known_titles = set(args.known_titles.split('|')) if args.known_titles else set()
    known_titles_lower = {t.lower() for t in known_titles}

    # Regel 2 — Title-Prefix "Kopie/Copy"
    if title_lower.startswith("kopie von ") or title_lower.startswith("copy of "):
        return {
            "is_duplicate": True,
            "skip_copy": True,
            "create_entry_with_duplicate_status": True,
            "reason": "title-prefix-copy",
            "manual_action_hint": None,
        }

    # Regel 3 — Numerierter Suffix " (1)", " (Kopie)", etc.
    m = re.search(r'\s\((\d+|kopie|copy)\)(\.\w+)?$', title_lower, flags=re.IGNORECASE)
    if m:
        ext = m.group(2) or ""
        # Stripe den Suffix raus
        base_lower = re.sub(r'\s\((\d+|kopie|copy)\)' + re.escape(ext) + r'$', ext, title_lower, flags=re.IGNORECASE)
        if base_lower in known_titles_lower:
            return {
                "is_duplicate": True,
                "skip_copy": True,
                "create_entry_with_duplicate_status": True,
                "reason": "numbered-copy-of-existing",
                "manual_action_hint": None,
            }

    # Regel 4 — MD5-Match (nur Binary)
    if args.md5 and args.md5 in known_md5s:
        return {
            "is_duplicate": True,
            "skip_copy": True,
            "create_entry_with_duplicate_status": True,
            "reason": f"md5-match",
            "manual_action_hint": None,
        }

    # Regel 5 — Title+Size für Google Docs
    if args.mime and args.mime.startswith("application/vnd.google-apps.") and args.size and title in known_titles:
        return {
            "is_duplicate": False,
            "skip_copy": False,
            "create_entry_with_duplicate_status": False,
            "reason": "title-match-similar-size-for-google-doc",
            "manual_action_hint": "Verify if duplicate — same title and similar size as existing entry",
        }

    # Kein Duplikat
    return {
        "is_duplicate": False,
        "skip_copy": False,
        "create_entry_with_duplicate_status": False,
        "reason": "no-duplicate-pattern-matched",
        "manual_action_hint": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Check duplicate via title-patterns + md5.")
    parser.add_argument('--title', required=True)
    parser.add_argument('--mime', default=None)
    parser.add_argument('--md5', default=None)
    parser.add_argument('--size', type=int, default=None)
    parser.add_argument('--known-md5s', default='', help="Comma-separated md5-checksums of existing files")
    parser.add_argument('--known-titles', default='', help="Pipe-separated titles of existing files")
    args = parser.parse_args()

    print(json.dumps(check(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
