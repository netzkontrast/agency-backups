"""Frontmatter-aware parsers for repo entity directories.

All parsers are pure: they take a repo root, walk the relevant glob, and
return plain dicts shaped to match the frontend's `AGENCY_DATA` contract.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import frontmatter


# ─── helpers ─────────────────────────────────────────────────────────────

def _walk(root: Path, *patterns: str) -> Iterable[Path]:
    """Yield files under root matching any of the glob patterns."""
    if not root.exists():
        return
    seen: set[Path] = set()
    for pat in patterns:
        for p in root.glob(pat):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def _read_fm(path: Path) -> dict[str, Any]:
    """Load frontmatter (returns {} if file is malformed or absent)."""
    try:
        post = frontmatter.load(path)
        data: dict[str, Any] = dict(post.metadata)
        # Stash the body so callers can opt in to it
        data["_body"] = post.content
        data["_path"] = str(path)
        return data
    except Exception:
        return {"_path": str(path), "_body": ""}


def _coerce_list(v: Any) -> list[Any]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


# ─── tasks ───────────────────────────────────────────────────────────────

def parse_tasks(repo: Path) -> list[dict[str, Any]]:
    """Parse `tasks/{id}-{slug}/TASK.md` (or `tasks/*.md` fallback)."""
    out: list[dict[str, Any]] = []
    root = repo / "tasks"
    for path in _walk(root, "*/TASK.md", "*.md"):
        fm = _read_fm(path)
        if not fm.get("id") and not fm.get("slug"):
            continue
        out.append({
            "id":             str(fm.get("id", "")),
            "slug":           fm.get("slug") or path.parent.name,
            "status":         fm.get("status", "open"),
            "priority":       fm.get("priority", "P2"),
            "owner":          fm.get("owner"),
            "summary":        fm.get("summary", ""),
            "created":        str(fm.get("created", "")),
            "updated":        str(fm.get("updated", "")),
            "uses_prompts":   _coerce_list(fm.get("uses_prompts")),
            "spawns_research":_coerce_list(fm.get("spawns_research")),
            "blocked_by":     _coerce_list(fm.get("blocked_by")),
            "supersedes":     fm.get("supersedes"),
            "superseded_by":  fm.get("superseded_by"),
        })
    out.sort(key=lambda t: t["id"])
    return out


# ─── prompts ─────────────────────────────────────────────────────────────

def parse_prompts(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    root = repo / "prompts"
    for path in _walk(root, "*.md", "**/*.md"):
        fm = _read_fm(path)
        slug = fm.get("slug") or path.stem
        out.append({
            "slug":             slug,
            "kind":             fm.get("kind", "task-spec"),
            "relates_to_task":  fm.get("relates_to_task"),
            "summary":          fm.get("summary", ""),
            "created":          str(fm.get("created", "")),
            "updated":          str(fm.get("updated", "")),
        })
    out.sort(key=lambda p: p["slug"])
    return out


# ─── research ────────────────────────────────────────────────────────────

def parse_research(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    root = repo / "research"
    for path in _walk(root, "*/RESEARCH.md", "*.md", "**/*.md"):
        fm = _read_fm(path)
        slug = fm.get("slug") or (path.parent.name if path.name in ("RESEARCH.md",) else path.stem)
        if not slug:
            continue
        out.append({
            "slug":             slug,
            "phase":            fm.get("phase", "in_progress"),
            "executes_prompt":  fm.get("executes_prompt"),
            "summary":          fm.get("summary", ""),
            "created":          str(fm.get("created", "")),
            "updated":          str(fm.get("updated", "")),
        })
    out.sort(key=lambda r: r["slug"])
    return out


# ─── friction logs ───────────────────────────────────────────────────────

def parse_friction_logs(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    root = repo / "friction-logs"
    for path in _walk(root, "*/*.md", "*.md", "**/*.md"):
        fm = _read_fm(path)
        out.append({
            "task":     str(fm.get("task", "")),
            "level":    fm.get("level", "FL0"),
            "session":  str(fm.get("session", "")),
            "agent":    fm.get("agent", "claude-code"),
            "duration": fm.get("duration", ""),
            "tokens":   int(fm.get("tokens", 0) or 0),
            "note":     (fm.get("note") or fm.get("_body", "")).strip()[:600],
        })
    out.sort(key=lambda f: f["session"], reverse=True)
    return out


# ─── pre-commit runs ─────────────────────────────────────────────────────

def parse_precommit_runs(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    root = repo / "precommit" / "runs"
    if not root.exists():
        return out
    for path in sorted(root.glob("*.json"), reverse=True):
        try:
            out.append(json.loads(path.read_text()))
        except Exception:
            continue
    return out


# ─── coherence runs ──────────────────────────────────────────────────────

def parse_coherence_runs(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    root = repo / "coherence" / "runs"
    for path in _walk(root, "*.md"):
        fm = _read_fm(path)
        out.append({
            "date":     str(fm.get("date", path.stem)),
            "status":   fm.get("status", "pass"),
            "issues":   int(fm.get("issues", 0) or 0),
            "deferred": int(fm.get("deferred", 0) or 0),
            "note":     (fm.get("note") or fm.get("_body", "")).strip()[:400],
        })
    out.sort(key=lambda c: c["date"], reverse=True)
    return out


# ─── graph ───────────────────────────────────────────────────────────────

def build_graph(
    tasks: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    research: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    for t in tasks:
        nodes.append({"id": f"task/{t['id']}", "type": "task",
                      "label": t["slug"], "raw": t})
    for p in prompts:
        nodes.append({"id": f"prompt/{p['slug']}", "type": "prompt",
                      "label": p["slug"], "raw": p})
    for r in research:
        nodes.append({"id": f"research/{r['slug']}", "type": "research",
                      "label": r["slug"], "raw": r})

    edges: list[dict[str, Any]] = []
    for t in tasks:
        for ps in t.get("uses_prompts", []):
            edges.append({"from": f"task/{t['id']}", "to": f"prompt/{ps}",
                          "rel": "uses_prompt"})
        for rs in t.get("spawns_research", []):
            edges.append({"from": f"task/{t['id']}", "to": f"research/{rs}",
                          "rel": "spawns_research"})
    for p in prompts:
        if p.get("relates_to_task"):
            edges.append({"from": f"prompt/{p['slug']}",
                          "to": f"task/{p['relates_to_task']}",
                          "rel": "relates_to_task"})
    for r in research:
        if r.get("executes_prompt"):
            edges.append({"from": f"research/{r['slug']}",
                          "to": f"prompt/{r['executes_prompt']}",
                          "rel": "executes_prompt"})
    return {"nodes": nodes, "edges": edges}
