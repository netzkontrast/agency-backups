"""Orchestrator for ``agency-adr synthesize``.

Pipeline:
    corpus → graph filter (live IDs) → extract → compress → fidelity gate
    → guarded-section write → run-log append.

Spec anchors: ADR.A.3.5, ADR.A.3.6, ADR.A.3.7.
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
from adr.corpus import load_corpus  # type: ignore  # noqa: E402
from adr.graph import build_graph  # type: ignore  # noqa: E402
from adr.extract import extract_normatives  # type: ignore  # noqa: E402
from adr.compress import compress, CompressedSection, TokenLimitExceeded  # type: ignore  # noqa: E402
from adr.fidelity import score as fidelity_score  # type: ignore  # noqa: E402
from adr.runlog import append_run_record  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic

BEGIN_MARKER = "<!-- BEGIN AGENCY-ADR SYNTHESIS -->"
END_MARKER = "<!-- END AGENCY-ADR SYNTHESIS -->"
WARNING_LINE = (
    "<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. "
    "Edits will be overwritten by tools/adr/cli.py synthesize. -->"
)

_GUARDED_RE = re.compile(
    re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
    re.DOTALL,
)


@dataclass(frozen=True)
class SynthesizeResult:
    section: CompressedSection | None
    fidelity: float
    written: bool
    diagnostics: tuple[Diagnostic, ...]
    exit_code: int


def _render_block(section: CompressedSection) -> str:
    return (
        f"{BEGIN_MARKER}\n"
        f"{WARNING_LINE}\n"
        f"{section.body}"
        f"{END_MARKER}"
    )


def synthesize(
    *,
    agents_md: Path,
    decisions_root: Path | None = None,
    token_limit: int = 2000,
    fidelity_floor: float = 0.95,
    fidelity_mode: str = "bcp14-keyword",
    dry_run: bool = False,
    repo_root: Path | None = None,
    run_log: Path | None = None,
) -> SynthesizeResult:
    repo = repo_root or _core.repo_root_from_cwd()
    if not agents_md.is_absolute():
        agents_md = repo / agents_md
    if decisions_root is None:
        decisions_root = repo / "decisions"
    diags: list[Diagnostic] = []

    corpus = load_corpus(decisions_root, repo_root=repo)
    graph = build_graph(corpus)

    # Marker presence check (ADR.A.3.5) before anything else.
    if not agents_md.exists():
        diags.append(Diagnostic(
            agents_md.name, None, "ERROR", "ADR.A.3.5",
            f"target file {agents_md.name!r} does not exist",
        ))
        return SynthesizeResult(None, 0.0, False, tuple(diags), 1)

    text = agents_md.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text or END_MARKER not in text:
        diags.append(Diagnostic(
            agents_md.name, None, "ERROR", "ADR.A.3.5",
            "AGENTS.md is missing the BEGIN/END AGENCY-ADR SYNTHESIS markers; "
            "synthesis refuses to run",
        ))
        return SynthesizeResult(None, 0.0, False, tuple(diags), 1)

    normatives = extract_normatives(corpus, graph=graph)
    try:
        section = compress(normatives, token_limit=token_limit)
    except TokenLimitExceeded as e:
        # Lowest-priority deprecation candidate is the latest contributing ADR.
        candidates = list(e.contributing[-3:]) if e.contributing else []
        diags.append(Diagnostic(
            agents_md.name, None, "ERROR", "ADR.A.3.3",
            f"synthesis would emit {e.tokens} tokens (limit {e.limit}); "
            f"deprecation candidates: {candidates or 'none'}",
        ))
        return SynthesizeResult(None, 0.0, False, tuple(diags), 1)

    fid = fidelity_score(corpus, section, mode=fidelity_mode, graph=graph)
    if fid < fidelity_floor:
        diags.append(Diagnostic(
            agents_md.name, None, "ERROR", "ADR.A.3.4",
            f"fidelity score {fid:.4f} below floor {fidelity_floor:.4f} "
            f"under mode {fidelity_mode!r}",
        ))
        return SynthesizeResult(section, fid, False, tuple(diags), 1)

    new_block = _render_block(section)
    new_text = _GUARDED_RE.sub(lambda _m: new_block, text, count=1)

    written = False
    if not dry_run and new_text != text:
        with _core.FileLock(agents_md):
            agents_md.write_text(new_text, encoding="utf-8")
        written = True

    if run_log is None:
        run_log = repo / "maintenance" / "run-log.md"
    if not dry_run:
        append_run_record(
            run_log=run_log,
            contributing_adr_ids=section.contributing_adr_ids,
            token_count=section.token_count,
            fidelity=fid,
            fidelity_mode=fidelity_mode,
            written=written,
            dry_run=dry_run,
        )

    return SynthesizeResult(
        section=section,
        fidelity=fid,
        written=written,
        diagnostics=tuple(diags),
        exit_code=0,
    )
