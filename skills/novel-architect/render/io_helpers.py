"""
io_helpers.py — File-IO helpers for novel-architect

Mirrors the pattern from research-prompt-optimizer/render/io_helpers.py:
- File-first writes (status-views, plan-views, audit-reports)
- Append-only revisions
- Atomic writes to project workspace

Usage from phases:
    from render.io_helpers import (
        write_intent_yaml,
        write_status_view,
        write_architecture_yaml,
        append_revision,
        atomic_write,
    )
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml  # type: ignore


# ─── Slug validation ─────────────────────────────────────────────────────────


_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_slug(slug: str) -> str:
    """
    Validate project slug is kebab-case. Returns the slug unchanged.
    Raises ValueError on invalid input — fail fast at boundary.
    """
    if not isinstance(slug, str) or not slug:
        raise ValueError(f"Slug must be a non-empty string, got: {slug!r}")
    if not _SLUG_RE.match(slug):
        raise ValueError(
            f"Slug must be kebab-case (lowercase alphanumerics + hyphens), got: {slug!r}"
        )
    return slug


def utcnow_iso() -> str:
    """Return current UTC time as ISO-8601 with Z suffix (canonical form)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─── Path resolution ─────────────────────────────────────────────────────────


DEFAULT_PROJECTS_ROOT = "/home/claude/novel-projects"


def projects_root() -> Path:
    """Return the configured projects-root.

    Resolution order (Task 071 §"Config-Loading Boundary"):
      1. `NOVEL_ARCHITECT_PROJECTS_ROOT` env var, if set and non-empty.
      2. `DEFAULT_PROJECTS_ROOT` fallback.

    Per-project overrides via `project-config.yaml:project.workspace_root`
    are honoured by `project_workspace()` once the project slug is known.
    """
    env_val = os.environ.get("NOVEL_ARCHITECT_PROJECTS_ROOT", "").strip()
    return Path(env_val) if env_val else Path(DEFAULT_PROJECTS_ROOT)


def project_workspace(slug: str) -> Path:
    """Return the canonical project workspace path.

    Honours `NOVEL_ARCHITECT_PROJECTS_ROOT` env override (see `projects_root`).
    Per-project `project-config.yaml:project.workspace_root` overrides take
    effect at the call sites that load config; this function returns the
    convention path absent a project-config override.
    """
    validate_slug(slug)
    return projects_root() / slug


def ensure_workspace(slug: str) -> Path:
    """Create workspace dir if missing, return path."""
    ws = project_workspace(slug)
    ws.mkdir(parents=True, exist_ok=True)
    return ws


# ─── Atomic write ────────────────────────────────────────────────────────────


def atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically.

    Uses tempfile-in-same-directory + fsync + os.replace to guarantee:
    - readers either see the old content or the fully-written new content,
      never a half-written truncation;
    - on crash, the rename target is durable (fsync before close);
    - the rename is atomic (os.replace is atomic on POSIX when src/dst share
      a filesystem; we ensure that by placing tempfile in path.parent).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=str(path.parent), delete=False, suffix=".tmp"
    ) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


# ─── YAML / JSON helpers ─────────────────────────────────────────────────────


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write YAML with stable key ordering, atomic."""
    content = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=80)
    atomic_write(path, content)


def read_yaml(path: Path) -> dict[str, Any]:
    """Read YAML, return empty dict if missing."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_json(path: Path, data: dict[str, Any], indent: int = 2) -> None:
    """Write JSON, atomic."""
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    atomic_write(path, content)


def read_json(path: Path) -> dict[str, Any]:
    """Read JSON, return empty dict if missing."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ─── Append-only revisions ──────────────────────────────────────────────────


def append_revision(yaml_data: dict[str, Any], note: str) -> dict[str, Any]:
    """
    Append a revision entry to the `revisions[]` list.
    Returns the mutated dict (also mutates in-place).
    """
    if "revisions" not in yaml_data or not isinstance(yaml_data["revisions"], list):
        yaml_data["revisions"] = []
    yaml_data["revisions"].append({
        "timestamp": utcnow_iso(),
        "note": note,
    })
    return yaml_data


# ─── Status / plan / audit views ─────────────────────────────────────────────


def write_status_view(
    slug: str,
    phase: str,
    title: str,
    body: str,
) -> Path:
    """
    Write a status-view markdown to `<workspace>/<phase>-status-view.md`.
    Returns the path.
    """
    ws = ensure_workspace(slug)
    path = ws / f"{phase}-status-view.md"
    timestamp = utcnow_iso()
    content = (
        f"# {title}\n\n"
        f"> **Generated:** {timestamp}\n"
        f"> **Phase:** {phase}\n\n"
        f"{body}\n"
    )
    atomic_write(path, content)
    return path


def write_plan_view(
    slug: str,
    phase: str,
    title: str,
    body: str,
) -> Path:
    """Write a plan-view markdown (for Gate-3-Approval rendering)."""
    ws = ensure_workspace(slug)
    path = ws / f"{phase}-plan-view.md"
    timestamp = utcnow_iso()
    content = (
        f"# {title}\n\n"
        f"> **Generated:** {timestamp}\n"
        f"> **Phase:** {phase}\n"
        f"> **Gate:** final-approval\n\n"
        f"{body}\n"
    )
    atomic_write(path, content)
    return path


def write_audit_report(
    slug: str,
    verdict: str,  # pass / fix-recommended / fix-required
    findings: list[dict[str, str]],
) -> Path:
    """Write Phase 7 audit-report.md."""
    ws = ensure_workspace(slug)
    path = ws / "audit-report.md"
    timestamp = utcnow_iso()
    lines = [
        "# Audit Report",
        "",
        f"> **Generated:** {timestamp}",
        f"> **Verdict:** {verdict}",
        "",
        "## Findings",
        "",
    ]
    for finding in findings:
        lines.append(f"- **{finding.get('severity', 'info')}:** {finding.get('message', '')}")
        if "file" in finding:
            lines.append(f"  - File: `{finding['file']}`")
    content = "\n".join(lines) + "\n"
    atomic_write(path, content)
    return path


# ─── Project Config helpers ──────────────────────────────────────────────────


def load_project_config(slug: str) -> dict[str, Any]:
    """Load project-config.yaml from workspace."""
    return read_yaml(project_workspace(slug) / "project-config.yaml")


def save_project_config(slug: str, config: dict[str, Any]) -> None:
    """Save project-config.yaml to workspace."""
    write_yaml(project_workspace(slug) / "project-config.yaml", config)


# ─── Constants ───────────────────────────────────────────────────────────────


SKILL_VERSION = "1.1.1"
SCHEMA_VERSION_INTENT = "1.0"
SCHEMA_VERSION_ARCHITECTURE = "1.0"
SCHEMA_VERSION_CHARACTER = "1.0"
NCP_SCHEMA_VERSION = "1.3.0"
