#!/usr/bin/env python3
"""Convert a PDF to Markdown using PyMuPDF4LLM.

Usage:
    python convert.py <input.pdf> <output.md>

Library defaults are used intentionally (single .md per PDF, no image
extraction, no chunking). To expose more options, edit this file directly
rather than reaching for a different skill — this is the documented escape
hatch.

Exit codes:
    0  success
    1  runtime failure (missing input, conversion error, install failure)
    2  usage error (wrong number of arguments)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _ensure_pymupdf4llm():
    """Import pymupdf4llm, attempting a one-shot install if missing.

    No silent fallback to other libraries — if this fails, the caller needs
    to know, because the user chose this skill specifically for PyMuPDF4LLM's
    structural output.
    """
    try:
        import pymupdf4llm  # noqa: F401
        return
    except ImportError:
        pass

    print("pymupdf4llm not found, installing...", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pymupdf4llm",
         "--break-system-packages", "--quiet"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: pip install failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        import pymupdf4llm  # noqa: F401
    except ImportError as e:
        print(f"ERROR: pymupdf4llm still not importable after install: {e}",
              file=sys.stderr)
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input.pdf> <output.md>",
              file=sys.stderr)
        sys.exit(2)

    pdf_path = Path(sys.argv[1])
    md_path = Path(sys.argv[2])

    if not pdf_path.exists():
        print(f"ERROR: input file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    if not pdf_path.is_file():
        print(f"ERROR: input is not a file: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    _ensure_pymupdf4llm()
    import pymupdf4llm  # noqa: E402  (import after ensure)

    try:
        markdown_text = pymupdf4llm.to_markdown(str(pdf_path))
    except Exception as e:
        print(f"ERROR: conversion failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        sys.exit(1)

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown_text, encoding="utf-8")

    n_chars = len(markdown_text)
    n_lines = markdown_text.count("\n") + (1 if markdown_text else 0)
    stripped = markdown_text.strip()
    warning = ""
    if len(stripped) < 200:
        warning = ("  WARNING: output is very short — the PDF may have no "
                   "text layer (scanned image). Consider OCR via the "
                   "pdf-reading skill.")
    print(f"OK: wrote {md_path} ({n_chars:,} chars, {n_lines:,} lines){warning}")


if __name__ == "__main__":
    main()
