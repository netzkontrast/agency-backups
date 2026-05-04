#!/usr/bin/env python3
"""Generate slug-filename for Drive-File.

Usage:
    python3 slug.py "<title>" [--max-len 80]

Output: slug-filename string (with extension preserved).

Examples:
    python3 slug.py "Kohärenz Protokoll - Notes.md"
    → kohaerenz-protokoll-notes.md
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata

KNOWN_EXTENSIONS = (
    '.md', '.docx', '.txt', '.pdf', '.html', '.rtf', '.odt',
    '.m4a', '.mp3', '.wav', '.flac',
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg',
    '.csv', '.tsv', '.json', '.yaml', '.yml',
    '.py', '.js', '.ts', '.css',
    '.zip', '.tar', '.gz',
)


def split_extension(title: str) -> tuple[str, str]:
    """Return (base, ext) where ext is one of KNOWN_EXTENSIONS or ''."""
    lower = title.lower()
    for ext in KNOWN_EXTENSIONS:
        if lower.endswith(ext):
            return title[:-len(ext)], title[-len(ext):]
    return title, ''


def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:8]


def normalize_umlauts(s: str) -> str:
    return s.translate({
        ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', ord('ß'): 'ss',
        ord('Ä'): 'ae', ord('Ö'): 'oe', ord('Ü'): 'ue',
    })


def file_slug(title: str, max_len: int = 80) -> str:
    base, ext = split_extension(title)

    if not base.strip():
        return f"untitled-{short_hash(title)}{ext}"

    s = base.lower()
    s = normalize_umlauts(s)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')

    # Truncate (max_len ohne extension)
    if max_len > 0:
        s = s[:max_len].rstrip('-')

    if not s:
        return f"untitled-{short_hash(title)}{ext}"

    return s + ext


def main():
    parser = argparse.ArgumentParser(description="Generate slug-filename for Drive-File.")
    parser.add_argument('title', help="Original Drive-Title")
    parser.add_argument('--max-len', type=int, default=80, help="Max length of slug part (excluding extension)")
    args = parser.parse_args()

    print(file_slug(args.title, max_len=args.max_len))
    return 0


if __name__ == '__main__':
    sys.exit(main())
