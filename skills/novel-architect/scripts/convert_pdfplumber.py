#!/usr/bin/env python3
"""Fallback PDF→Markdown converter for novel-architect ingest.

Uses pdfplumber (preinstalled) since PyPI is blocked and pymupdf4llm cannot
be installed at runtime. Output quality is lower than pymupdf4llm — no
heading-hierarchy detection, simple paragraph reflow only — but adequate
for prose-heavy Gemini Deep Research outputs.

Usage:
    python convert_pdfplumber.py <input.pdf> <output.md>
"""
from __future__ import annotations

import sys
from pathlib import Path

import pdfplumber


def page_to_markdown(page) -> str:
    text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
    # collapse triple+ blank lines, keep paragraph breaks
    lines = [ln.rstrip() for ln in text.split("\n")]
    out = []
    blank_run = 0
    for ln in lines:
        if not ln.strip():
            blank_run += 1
            if blank_run <= 1:
                out.append("")
        else:
            blank_run = 0
            out.append(ln)
    return "\n".join(out).strip()


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python convert_pdfplumber.py <input.pdf> <output.md>",
              file=sys.stderr)
        sys.exit(2)

    pdf_path = Path(sys.argv[1])
    md_path = Path(sys.argv[2])

    if not pdf_path.is_file():
        print(f"ERROR: input file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    parts: list[str] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            n_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages, start=1):
                page_md = page_to_markdown(page)
                if page_md:
                    parts.append(page_md)
    except Exception as e:
        print(f"ERROR: conversion failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        sys.exit(1)

    md = "\n\n".join(parts) + "\n"

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md, encoding="utf-8")

    n_chars = len(md)
    n_lines = md.count("\n") + 1
    warning = ""
    if len(md.strip()) < 200:
        warning = "  WARNING: very short output — possibly scanned PDF (no text layer)."
    print(f"OK: {md_path} | {n_pages} pages | {n_chars:,} chars | {n_lines:,} lines{warning}")


if __name__ == "__main__":
    main()
