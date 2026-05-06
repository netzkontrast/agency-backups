"""Fidelity scoring for the synthesis pipeline.

Spec anchor ADR.A.3.4. Three modes are surfaced:

  - ``bcp14-keyword`` — fraction of source-corpus BCP-14 sentences whose
    de-duplication key appears in the compressed body. Deterministic; no
    external dependencies.
  - ``adr-id-anchor`` — fraction of live ``adr_id`` values that appear in
    the compressed footer; checks "every contributing ADR is cited".
  - ``llm-pass`` — DEFERRED (OD.2). Raises ``NotImplementedError`` so
    callers get a clear signal rather than a silent zero.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
from adr.corpus import AdrRecord  # type: ignore  # noqa: E402
from adr.compress import CompressedSection  # type: ignore  # noqa: E402
from adr.extract import extract_normatives  # type: ignore  # noqa: E402
from adr.graph import AdrGraph  # type: ignore  # noqa: E402


_MODES = ("bcp14-keyword", "adr-id-anchor", "llm-pass")


def _bcp14_score(corpus: list[AdrRecord], compressed: CompressedSection,
                 graph: AdrGraph | None) -> float:
    normatives = extract_normatives(corpus, graph=graph)
    if not normatives:
        return 1.0
    body_lower = compressed.body.lower()
    hits = 0
    for n in normatives:
        key = re.sub(r"\s+", " ", n.sentence.strip().lower())
        # Strip trailing punctuation for the substring match so a sentence
        # rendered with an added "." still counts.
        key = key.rstrip(".!? ")
        if key and key in body_lower:
            hits += 1
    return hits / len(normatives)


def _anchor_score(corpus: list[AdrRecord], compressed: CompressedSection,
                  graph: AdrGraph | None) -> float:
    if graph is not None:
        live = [r for r in corpus if r.adr_id in graph.live_ids]
    else:
        live = [r for r in corpus if r.adr_status == "Accepted"]
    if not live:
        return 1.0
    cited = 0
    for rec in live:
        if rec.adr_id in compressed.body:
            cited += 1
    return cited / len(live)


def score(
    corpus: list[AdrRecord],
    compressed: CompressedSection,
    *,
    mode: str,
    graph: AdrGraph | None = None,
) -> float:
    """Return a fidelity score in ``[0.0, 1.0]`` under the selected ``mode``."""
    if mode not in _MODES:
        raise ValueError(
            f"unknown fidelity mode {mode!r}; expected one of {_MODES}"
        )
    if mode == "bcp14-keyword":
        return _bcp14_score(corpus, compressed, graph)
    if mode == "adr-id-anchor":
        return _anchor_score(corpus, compressed, graph)
    raise NotImplementedError(
        "fidelity mode 'llm-pass' is deferred (OD.2); ship --fidelity-mode "
        "bcp14-keyword or adr-id-anchor for v0"
    )
