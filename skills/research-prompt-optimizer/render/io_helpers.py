#!/usr/bin/env python3
"""
research-prompt-optimizer · io_helpers

Centralised file-IO for Phase 1, 2, 3, 4 of the pipeline. Everything
that would otherwise be printed into chat as YAML/Markdown blocks is
written via these helpers to /mnt/user-data/outputs/. The skill's
chat output stays minimal (only ask_user prompts + present_files
calls); the substance lives in files the user can open or ignore.

Design principles:
  - Pure stdlib + pyyaml. No templating engines.
  - Atomic writes: write to .tmp, rename. Avoids partial files on
    crash mid-write.
  - Idempotent timestamps: caller provides ISO-8601 strings; no
    hidden datetime.now() calls.
  - Every helper returns the absolute Path it wrote, for use with
    present_files.

Public API:
  - write_yaml(path, data)
  - write_text(path, content)
  - write_intent_yaml(output_dir, slug, intent_data)
  - write_status_view(output_dir, slug, slot_states)
  - write_metaprompt_yaml(output_dir, slug, meta_prompt_data)
  - write_planview_md(output_dir, slug, plan_data)
  - write_audit_md(output_dir, slug, audit_data)
  - append_revision(yaml_path, revision_entry)
  - next_versioned_path(output_dir, slug, kind, ext)
  - make_provenance(...)
  - zip_workspace(output_dir, slug, paths)
"""
from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "io_helpers requires pyyaml. Install with: pip install pyyaml"
    ) from e


# =============================================================================
# Low-level atomic write
# =============================================================================


def _atomic_write(path: Path, content: str) -> Path:
    """Write content to path atomically (write to temp, then rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path.resolve()


def write_yaml(path: Path, data: dict) -> Path:
    """Write a dict as YAML to path. Returns resolved absolute path."""
    content = yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False
    )
    return _atomic_write(path, content)


def write_text(path: Path, content: str) -> Path:
    """Write text content to path. Returns resolved absolute path."""
    return _atomic_write(path, content)


# =============================================================================
# Provenance block — used by Phase 1, 2, 3 outputs
# =============================================================================


def make_provenance(
    *,
    timestamp: str,
    skill_version: str,
    phase: str,
    slug: str,
    output_filename: str,
    category_signal: str | None = None,
    selected_methods: list[str] | None = None,
    selected_framework_structural: str | None = None,
    cross_pollination_pair: list[str] | None = None,
    previous_version: str | None = None,
    revision_count: int = 0,
) -> dict:
    """Build a normalised provenance block.

    Required for every YAML/MD artefact the skill writes. Every artefact's
    provenance has the same shape so Phase 2/3/4 can read upstream
    provenance without case-handling per-phase.

    `revisions` is a separate top-level field on the host document
    (intent.yaml / meta-prompt.yaml) — appended via append_revision(),
    not embedded here.
    """
    block: dict[str, Any] = {
        "created": timestamp,
        "skill_version": skill_version,
        "phase": phase,
        "slug": slug,
        "output_filename": output_filename,
    }
    if category_signal is not None:
        block["category_signal"] = category_signal
    if selected_methods is not None:
        block["selected_methods"] = list(selected_methods)
    if selected_framework_structural is not None:
        block["selected_framework_structural"] = selected_framework_structural
    if cross_pollination_pair is not None:
        block["cross_pollination_pair"] = list(cross_pollination_pair)
    if previous_version is not None:
        block["previous_version"] = previous_version
    if revision_count:
        block["revision_count"] = revision_count
    return block


# =============================================================================
# Versioned path resolution — append, never overwrite
# =============================================================================


_KIND_TO_STEM: dict[str, str] = {
    "intent": "intent",
    "metaprompt": "meta-prompt",
    "planview": "meta-prompt-planview",
    "statusview": "intent-status",
    "audit": "research-prompt-audit",
    "rendered": "research-prompt",
}


def next_versioned_path(
    output_dir: Path, slug: str, kind: str, ext: str = "md"
) -> tuple[Path, int, Path | None]:
    """Resolve the next free versioned path for a (slug, kind).

    First version: <stem>_<slug>.<ext>
    Subsequent:    <stem>_<slug>_v2.<ext>, _v3.<ext>, ...

    Returns (next_path, revision_count, previous_path_or_None).
    revision_count == 0 means this is the first write.
    """
    if kind not in _KIND_TO_STEM:
        raise ValueError(f"unknown kind: {kind!r} (allowed: {sorted(_KIND_TO_STEM)})")
    stem = _KIND_TO_STEM[kind]
    base = output_dir / f"{stem}_{slug}.{ext}"
    if not base.exists():
        return base, 0, None

    # Find the highest existing _vN
    pattern = re.compile(rf"^{re.escape(stem)}_{re.escape(slug)}_v(\d+)\.{re.escape(ext)}$")
    highest = 1
    last_existing = base
    for p in output_dir.iterdir():
        m = pattern.match(p.name)
        if m:
            n = int(m.group(1))
            if n > highest:
                highest = n
                last_existing = p
    next_v = highest + 1
    next_path = output_dir / f"{stem}_{slug}_v{next_v}.{ext}"
    return next_path, next_v - 1, last_existing


# =============================================================================
# Phase 1 outputs
# =============================================================================


def write_intent_yaml(
    output_dir: Path, slug: str, intent_data: dict
) -> tuple[Path, int]:
    """Write intent_<slug>.yaml (or _vN.yaml if exists). Returns (path, revision_count)."""
    out_path, rev_count, prev = next_versioned_path(output_dir, slug, "intent", "yaml")
    if prev is not None and "provenance" in intent_data:
        intent_data["provenance"]["previous_version"] = prev.name
        intent_data["provenance"]["revision_count"] = rev_count
    write_yaml(out_path, intent_data)
    return out_path, rev_count


def write_status_view(
    output_dir: Path,
    slug: str,
    slot_states: dict[str, tuple[str, str]],
    intent_so_far: dict | None = None,
) -> Path:
    """Write a human-readable status view for Phase 1 askuser turns.

    slot_states: {slot_name: (state, value_or_reason)}
                 state ∈ {'filled', 'partial', 'missing'}
    intent_so_far: optional already-extracted intent block to show below
                   the status table.

    Always overwrites — this is a transient view, not an artefact.
    """
    out_path = output_dir / f"intent-status_{slug}.md"
    filled = [(k, v) for k, (s, v) in slot_states.items() if s == "filled"]
    partial = [(k, v) for k, (s, v) in slot_states.items() if s == "partial"]
    missing = [(k, v) for k, (s, v) in slot_states.items() if s == "missing"]

    lines = [f"# Intent Capture Status — {slug}", ""]
    lines.append(f"**Slots filled:** {len(filled)} · **partial:** {len(partial)} · **missing:** {len(missing)}")
    lines.append("")

    if filled:
        lines.append("## ✓ Filled")
        lines.append("")
        for k, v in filled:
            lines.append(f"- **{k}:** {_truncate(v, 200)}")
        lines.append("")

    if partial:
        lines.append("## ⚠ Partial (ambiguous / under-specified)")
        lines.append("")
        for k, v in partial:
            lines.append(f"- **{k}:** {_truncate(v, 200)}")
        lines.append("")

    if missing:
        lines.append("## ✗ Missing")
        lines.append("")
        for k, _ in missing:
            lines.append(f"- **{k}**")
        lines.append("")

    if intent_so_far:
        lines.append("## Intent assembled so far")
        lines.append("")
        lines.append("```yaml")
        lines.append(yaml.safe_dump(intent_so_far, sort_keys=False, allow_unicode=True).rstrip())
        lines.append("```")
        lines.append("")

    return write_text(out_path, "\n".join(lines))


# =============================================================================
# Phase 2 outputs
# =============================================================================


def write_metaprompt_yaml(
    output_dir: Path, slug: str, meta_prompt_data: dict
) -> tuple[Path, int]:
    """Write meta-prompt_<slug>.yaml. Returns (path, revision_count)."""
    out_path, rev_count, prev = next_versioned_path(output_dir, slug, "metaprompt", "yaml")
    if prev is not None and "provenance" in meta_prompt_data:
        meta_prompt_data["provenance"]["previous_version"] = prev.name
        meta_prompt_data["provenance"]["revision_count"] = rev_count
    write_yaml(out_path, meta_prompt_data)
    return out_path, rev_count


def write_planview_md(
    output_dir: Path, slug: str, plan_summary: dict
) -> Path:
    """Write a human-readable plan view for Phase 2 approval gates.

    plan_summary expected keys (all optional):
      - gate: 'routing' | 'modules' | 'seeds' | 'final'
      - category: {'signal': 'A'|'B'|'C', 'rationale': '...'}
      - methods: [{'id': 'M01', 'reason': 'default for Cat-A'}, ...]
      - framework_structural: 'risen' | 'tidd-ec' | ...
      - cross_pollination: ['b-into-a', 'c-into-a']
      - constraint_blocks: [{'id': 'CB1', 'title': '...', 'summary': '...'}]
      - batches: [{'id': 'per-item', 'cardinality': 5}]
      - seed_queries: ['...', '...']
      - orthogonal_lens: '...'
      - pre_mortem: ['...', '...', '...']
      - integrity_check: {'react': True, 'm0': True, ...}

    Always overwrites — transient view, not an artefact.
    """
    out_path = output_dir / f"meta-prompt-planview_{slug}.md"
    gate = plan_summary.get("gate", "final")
    lines = [f"# Plan View — {slug} (gate: {gate})", ""]

    if "category" in plan_summary:
        c = plan_summary["category"]
        lines.append(f"## Category routing")
        lines.append("")
        lines.append(f"- **Signal:** {c.get('signal', '?')}")
        lines.append(f"- **Rationale:** {c.get('rationale', '—')}")
        lines.append("")

    if "methods" in plan_summary:
        lines.append("## Methods")
        lines.append("")
        for m in plan_summary["methods"]:
            reason = m.get("reason", "")
            reason_str = f" — _{reason}_" if reason else ""
            lines.append(f"- **{m['id']}**{reason_str}")
        lines.append("")

    if "framework_structural" in plan_summary:
        lines.append(f"## Framework (structural)")
        lines.append("")
        lines.append(f"- **{plan_summary['framework_structural']}** (ReAct always agentic)")
        lines.append("")

    if "cross_pollination" in plan_summary:
        lines.append("## Cross-pollination")
        lines.append("")
        for cp in plan_summary["cross_pollination"]:
            lines.append(f"- {cp}")
        lines.append("")

    if "constraint_blocks" in plan_summary:
        lines.append("## Constraint blocks")
        lines.append("")
        for cb in plan_summary["constraint_blocks"]:
            lines.append(f"- **{cb['id']} — {cb.get('title', '')}**")
            if cb.get("summary"):
                lines.append(f"  {cb['summary']}")
        lines.append("")

    if "batches" in plan_summary:
        lines.append("## Batches")
        lines.append("")
        for b in plan_summary["batches"]:
            lines.append(f"- **{b['id']}** (cardinality: {b.get('cardinality', '?')})")
        lines.append("")

    if "seed_queries" in plan_summary:
        lines.append("## Seed queries")
        lines.append("")
        for s in plan_summary["seed_queries"]:
            lines.append(f"- `{s}`")
        lines.append("")

    if "orthogonal_lens" in plan_summary:
        lines.append("## Orthogonal lens")
        lines.append("")
        lines.append(f"- {plan_summary['orthogonal_lens']}")
        lines.append("")

    if "pre_mortem" in plan_summary:
        lines.append("## Pre-mortem (predicted failure modes)")
        lines.append("")
        for i, pm in enumerate(plan_summary["pre_mortem"], 1):
            lines.append(f"{i}. {pm}")
        lines.append("")

    if "integrity_check" in plan_summary:
        lines.append("## Integrity check (M4)")
        lines.append("")
        for k, v in plan_summary["integrity_check"].items():
            mark = "✓" if v else "✗"
            lines.append(f"- {mark} {k}")
        lines.append("")

    return write_text(out_path, "\n".join(lines))


# =============================================================================
# Phase 4 outputs
# =============================================================================


def write_audit_md(
    output_dir: Path, slug: str, audit_data: dict
) -> Path:
    """Write a human-readable Phase-4 reader-test audit.

    audit_data expected keys:
      - rendered_path: str (path to research-prompt being audited)
      - reader_questions: list[{'q': str, 'predicted_answer': str,
                                'doc_provides': bool, 'finding': str}]
      - ambiguities: list[{'location': str, 'issue': str}]
      - assumptions: list[str]
      - contradictions: list[{'a': str, 'b': str}]
      - verdict: 'pass' | 'fix-recommended' | 'fix-required'
    """
    out_path = output_dir / f"research-prompt-audit_{slug}.md"
    lines = [f"# Reader-Test Audit — {slug}", ""]
    lines.append(f"**Audited file:** `{audit_data.get('rendered_path', '?')}`")
    verdict = audit_data.get("verdict", "?")
    lines.append(f"**Verdict:** {verdict}")
    lines.append("")

    rqs = audit_data.get("reader_questions", [])
    if rqs:
        lines.append("## Reader questions vs. doc")
        lines.append("")
        for i, rq in enumerate(rqs, 1):
            lines.append(f"### {i}. {rq.get('q', '?')}")
            lines.append("")
            covered = "✓ doc answers this" if rq.get("doc_provides") else "✗ doc does not answer"
            lines.append(f"- **{covered}**")
            if rq.get("predicted_answer"):
                lines.append(f"- Predicted answer: {rq['predicted_answer']}")
            if rq.get("finding"):
                lines.append(f"- Finding: {rq['finding']}")
            lines.append("")

    ambig = audit_data.get("ambiguities", [])
    if ambig:
        lines.append("## Ambiguities")
        lines.append("")
        for a in ambig:
            lines.append(f"- **{a.get('location', '?')}:** {a.get('issue', '?')}")
        lines.append("")

    assum = audit_data.get("assumptions", [])
    if assum:
        lines.append("## Assumptions about reader knowledge")
        lines.append("")
        for s in assum:
            lines.append(f"- {s}")
        lines.append("")

    contras = audit_data.get("contradictions", [])
    if contras:
        lines.append("## Contradictions")
        lines.append("")
        for c in contras:
            lines.append(f"- A: {c.get('a', '?')}")
            lines.append(f"  B: {c.get('b', '?')}")
        lines.append("")

    return write_text(out_path, "\n".join(lines))


# =============================================================================
# Append-only revision tracking
# =============================================================================


def append_revision(
    yaml_path: Path,
    revision_entry: dict,
) -> Path:
    """Append a revision entry to a YAML file's `revisions` list.

    revision_entry expected keys:
      - timestamp: ISO-8601 str
      - phase: str (which phase made the edit)
      - field_path: str (dotted path to the changed field)
      - before: any
      - after: any
      - rationale: str (optional, free text)

    The host file MUST already exist and be valid YAML. Creates the
    `revisions` key if missing. Never overwrites existing entries.
    """
    if not yaml_path.exists():
        raise FileNotFoundError(f"cannot append revision: {yaml_path} does not exist")
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    revisions = data.setdefault("revisions", [])
    revisions.append(revision_entry)
    if "provenance" in data and isinstance(data["provenance"], dict):
        data["provenance"]["revision_count"] = len(revisions)
    write_yaml(yaml_path, data)
    return yaml_path.resolve()


# =============================================================================
# Workspace packaging (Phase 5 — Finalize)
# =============================================================================


def zip_workspace(
    output_dir: Path | str,
    slug: str,
    paths: list[Path | str] | None = None,
) -> Path:
    """Bundle workspace artefacts into ``workspace_<slug>.zip``.

    Used by Phase 5 to package every file produced for a given slug
    (intent.yaml, status views, meta-prompt.yaml, plan view, rendered
    prompt + any versioned revisions, audit if produced) for download
    or onward upload (e.g. Google Drive).

    Args:
        output_dir: Pipeline output directory (typically
            /mnt/user-data/outputs).
        slug: Slug used by the rest of the pipeline.
        paths: Explicit list of files to include. If ``None``, every
            file in ``output_dir`` whose name contains ``slug`` is
            included (excluding any prior workspace_*.zip to avoid
            recursion).

    Returns:
        Absolute Path of the written zip.

    Notes:
        Atomic semantics: builds the archive at ``<final>.tmp`` then
        renames. Idempotent — re-running overwrites prior workspace
        zip for the same slug.
    """
    import zipfile

    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"workspace_{slug}.zip"
    tmp = out / f"workspace_{slug}.zip.tmp"

    if paths is None:
        candidates = [
            p for p in out.iterdir()
            if p.is_file()
            and slug in p.name
            and not p.name.startswith("workspace_")
            and p.suffix != ".tmp"
        ]
    else:
        candidates = [Path(p) for p in paths]

    if not candidates:
        raise FileNotFoundError(
            f"zip_workspace: no files matched slug={slug!r} in {out}"
        )

    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(candidates):
            p = Path(p)
            if not p.is_file():
                continue
            zf.write(p, arcname=p.name)

    os.replace(tmp, target)
    return target.resolve()


# =============================================================================
# Internal helpers
# =============================================================================


def _truncate(s: Any, n: int) -> str:
    s = str(s)
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"
