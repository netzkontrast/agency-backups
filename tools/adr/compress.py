"""MDL-style compression of extracted normatives into a guarded section.

Spec anchors:
  - ADR.A.3.2 — rule deduplication, BCP-14 normalisation, footer-anchor
    citation.
  - ADR.A.3.3 — token-limit overflow halts the pipeline.
"""
from __future__ import annotations

import re
import sys
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
from adr.extract import Normative  # type: ignore  # noqa: E402


@dataclass(frozen=True)
class CompressedSection:
    body: str
    contributing_adr_ids: tuple[str, ...]
    token_count: int


def count_tokens(text: str) -> int:
    """Whitespace-split heuristic token count.

    Per ``implementation-plan.md §6 OD.7``, this initial heuristic is
    sufficient; a precise tokeniser can be slotted in later without
    altering the public ``count_tokens`` signature.
    """
    return len(text.split())


def _normalise(sentence: str) -> str:
    """Collapse whitespace and ensure a trailing period for stable de-dup."""
    s = " ".join(sentence.split())
    if s and s[-1] not in ".!?":
        s = s + "."
    return s


def _dedupe_key(sentence: str) -> str:
    return re.sub(r"\s+", " ", sentence.strip().lower())


def compress(
    normatives: list[Normative],
    *,
    token_limit: int = 2000,
) -> CompressedSection:
    """Return a deterministic ``CompressedSection`` summarising ``normatives``.

    The body is grouped by BCP-14 keyword (in declaration order). Each
    sentence is suffixed with the contributing ``adr_id`` in brackets so
    the synthesis is fully traceable. Duplicate sentences (after
    normalisation) are dropped; the earlier-listed ADR wins citation.

    Raises ``TokenLimitExceeded`` when the rendered body exceeds
    ``token_limit`` tokens.
    """
    grouped: "OrderedDict[str, list[tuple[str, list[str]]]]" = OrderedDict()
    seen_keys: dict[str, tuple[str, list[str]]] = {}
    contributing: list[str] = []
    for n in normatives:
        sent = _normalise(n.sentence)
        key = _dedupe_key(sent)
        if key in seen_keys:
            _existing_sent, ids = seen_keys[key]
            if n.adr_id not in ids:
                ids.append(n.adr_id)
        else:
            ids: list[str] = [n.adr_id]
            seen_keys[key] = (sent, ids)
            grouped.setdefault(n.keyword.upper(), []).append((sent, ids))
        if n.adr_id not in contributing:
            contributing.append(n.adr_id)

    lines: list[str] = []
    for kw, items in grouped.items():
        lines.append(f"### {kw}")
        for sent, ids in items:
            citation = ", ".join(ids)
            lines.append(f"- {sent} [{citation}]")
        lines.append("")

    if contributing:
        lines.append("**Contributing ADRs:** " + ", ".join(contributing) + ".")

    body = "\n".join(lines).rstrip() + "\n"
    tokens = count_tokens(body)
    if tokens > token_limit:
        raise TokenLimitExceeded(
            tokens=tokens,
            limit=token_limit,
            contributing=tuple(contributing),
        )
    return CompressedSection(
        body=body,
        contributing_adr_ids=tuple(contributing),
        token_count=tokens,
    )


class TokenLimitExceeded(Exception):
    def __init__(self, *, tokens: int, limit: int, contributing: tuple[str, ...]):
        super().__init__(
            f"compressed section is {tokens} tokens, exceeding limit {limit}"
        )
        self.tokens = tokens
        self.limit = limit
        self.contributing = contributing
