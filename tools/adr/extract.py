"""Extract normative statements from Accepted ADRs.

Spec anchor ADR.A.3.1 — "the synthesis pipeline MUST extract normative
content exclusively from the 'Decision Outcome' and 'Consequences'
sections of ADRs whose ``adr_status`` is ``Accepted``."

Each extracted statement is a single sentence carrying exactly one BCP-14
keyword. The extractor is deterministic and language-agnostic — it does
not paraphrase; it only normalises whitespace.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402
from adr.corpus import AdrRecord  # type: ignore  # noqa: E402
from adr.graph import AdrGraph  # type: ignore  # noqa: E402

# RFC 2119 / BCP 14 normative keyword set. Order matters for first-match
# detection: longer phrases first to avoid "MUST" eating "MUST NOT".
BCP14_KEYWORDS = (
    "MUST NOT", "SHOULD NOT", "SHALL NOT", "NOT RECOMMENDED",
    "MUST", "SHALL", "REQUIRED", "SHOULD", "RECOMMENDED", "MAY", "OPTIONAL",
)
_KEYWORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in BCP14_KEYWORDS) + r")\b"
)

# Sentence boundary heuristic: split on '.', '!', or '?' followed by whitespace
# or end-of-string. This is intentionally simple — ADR bodies are short.
_SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)")

# Consequence kind hints — case-insensitive prefix match against the line
# or list-item that contains the sentence.
_KIND_PATTERNS = {
    "positive": re.compile(r"\b(positive|good|benefit|pro)\b", re.IGNORECASE),
    "negative": re.compile(r"\b(negative|bad|cost|risk|drawback|con)\b", re.IGNORECASE),
    "neutral":  re.compile(r"\b(neutral|tradeoff|note)\b", re.IGNORECASE),
}


@dataclass(frozen=True)
class Normative:
    adr_id: str
    keyword: str
    sentence: str
    consequence_kind: str | None
    line: int


def _split_sentences(text: str) -> list[str]:
    out: list[str] = []
    for m in _SENTENCE_RE.finditer(text):
        s = m.group(0).strip()
        if s:
            out.append(s)
    return out


def _classify_consequence(body: str, sentence: str) -> str | None:
    """Return the consequence kind for ``sentence`` if one is implied.

    The classifier inspects (a) the line that holds ``sentence`` itself
    (catches "- Negative: …" bullets and "**Positive**: …" definitions)
    then (b) the closest preceding non-blank line (catches
    "### Negative" sub-headings followed by a paragraph).
    """
    idx = body.find(sentence)
    if idx == -1:
        return None
    line_start = body.rfind("\n", 0, idx) + 1
    line_end = body.find("\n", idx)
    if line_end == -1:
        line_end = len(body)
    line = body[line_start:line_end]
    for kind, patt in _KIND_PATTERNS.items():
        if patt.search(line):
            return kind
    j = line_start - 1
    while j > 0:
        prev_start = body.rfind("\n", 0, j) + 1
        prev = body[prev_start:j]
        j = prev_start - 1
        if not prev.strip():
            continue
        for kind, patt in _KIND_PATTERNS.items():
            if patt.search(prev):
                return kind
        break
    return None


def _line_of(body: str, sentence: str) -> int:
    idx = body.find(sentence)
    if idx == -1:
        return 1
    return body.count("\n", 0, idx) + 1


def _extract_section(rec: AdrRecord, heading: str, *, mark_consequences: bool
                    ) -> list[Normative]:
    section = _core.find_section_body(rec.text, heading)
    if not section:
        return []
    out: list[Normative] = []
    for sent in _split_sentences(section):
        m = _KEYWORD_RE.search(sent)
        if not m:
            continue
        kind = _classify_consequence(section, sent) if mark_consequences else None
        out.append(Normative(
            adr_id=rec.adr_id,
            keyword=m.group(1),
            sentence=" ".join(sent.split()),
            consequence_kind=kind,
            line=_line_of(rec.body, sent),
        ))
    return out


def extract_normatives(
    corpus: list[AdrRecord],
    *,
    graph: AdrGraph | None = None,
) -> list[Normative]:
    """Return the BCP-14-bearing sentences from every live Accepted ADR.

    A "live" ADR is Accepted and not superseded; if ``graph`` is supplied,
    its ``live_ids`` set is the authoritative filter (per ADR.A.4.4).
    """
    out: list[Normative] = []
    for rec in corpus:
        if rec.adr_status != "Accepted":
            continue
        if graph is not None and rec.adr_id not in graph.live_ids:
            continue
        out.extend(_extract_section(rec, "Decision Outcome", mark_consequences=False))
        out.extend(_extract_section(rec, "Consequences", mark_consequences=True))
    out.sort(key=lambda n: (n.adr_id, n.line))
    return out
