"""Identifier-level invariants for the ADR corpus.

Spec anchors:
  - ADR.A.5.6 — duplicate adr_id detection.
  - ADR.A.2.7 — filename ↔ frontmatter coupling.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402
from adr.corpus import AdrRecord  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic

FILENAME_RE = re.compile(r"^(?P<num>\d{4})-(?P<slug>[a-z0-9-]+)\.md$")


def check_unique_ids(corpus: list[AdrRecord]) -> list[Diagnostic]:
    by_id: dict[str, list[AdrRecord]] = defaultdict(list)
    for rec in corpus:
        if rec.adr_id:
            by_id[rec.adr_id].append(rec)
    diags: list[Diagnostic] = []
    for aid, recs in by_id.items():
        if len(recs) > 1:
            paths = ", ".join(r.rel for r in recs)
            for r in recs:
                diags.append(Diagnostic(
                    r.rel, None, "ERROR", "ADR.A.5.6",
                    f"duplicate adr_id {aid!r} appears in: {paths}",
                ))
    return diags


def check_filename_coupling(corpus: list[AdrRecord]) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    for rec in corpus:
        m = FILENAME_RE.match(rec.path.name)
        if not m:
            diags.append(Diagnostic(
                rec.rel, None, "ERROR", "ADR.A.2.7",
                f"filename {rec.path.name!r} does not match "
                f"<NNNN>-<slug>.md pattern",
            ))
            continue
        expected_id = f"ADR-{m.group('num')}"
        expected_slug = f"{m.group('num')}-{m.group('slug')}"
        if rec.adr_id and rec.adr_id != expected_id:
            diags.append(Diagnostic(
                rec.rel, None, "ERROR", "ADR.A.2.7",
                f"filename implies adr_id={expected_id!r} but frontmatter "
                f"declares adr_id={rec.adr_id!r}",
            ))
        slug = _core.str_val(rec.frontmatter, "slug")
        if slug and slug != expected_slug:
            diags.append(Diagnostic(
                rec.rel, None, "ERROR", "ADR.A.2.7",
                f"filename implies slug={expected_slug!r} but frontmatter "
                f"declares slug={slug!r}",
            ))
    return diags
