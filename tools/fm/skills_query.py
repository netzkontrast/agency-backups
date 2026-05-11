#!/usr/bin/env python3
"""skills-query — thin convenience wrapper that answers the ten canonical
questions from `tasks/010-skills-frontmatter-index-suite/task.md §Plan` by
composing the stateless `fm-query`, `fm-extract`, and `fm-graph` CLIs.

Successor to Task 010 (the persistent-index strategy is explicitly
superseded by the stateless toolchain — see
`research/flexible-frontmatter-toolchain/output/SPEC.md` §2 and §16). No
JSON cache file is built; every invocation walks the live filesystem
through the canonical tools.

Usage:
    skills-query summary <slug>
    skills-query skills --kind <skill_kind>
    skills-query skills --target-agent <agent>
    skills-query references <slug>
    skills-query orphans
    skills-query stale --since <N>d
    skills-query path <slug>
    skills-query header <slug> <header>
    skills-query graph --type task [--status STATUS]
    skills-query manifest

All commands cap output at 1 KB (fm-query convention). All commands are
read-only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

REPO_ROOT = _core.repo_root_from_cwd()
PY = sys.executable
OUTPUT_CAP_BYTES = 1024


def _run_tool(name: str, *args: str, scope: str | None = None,
              fmt: str | None = None, allow_nonzero: bool = False) -> str:
    cmd = [PY, str(REPO_ROOT / "tools" / "fm" / f"{name}.py"), *args]
    if scope:
        cmd += ["--scope", scope]
    if fmt:
        cmd += ["--format", fmt]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if res.returncode != 0 and not allow_nonzero:
        sys.stderr.write(res.stderr)
        raise SystemExit(res.returncode)
    return res.stdout if res.stdout else res.stderr


_FILE_PRIORITY = (
    "/task.md", "/SKILL.md", "/output/SPEC.md", "/prompt.md", "/readme.md",
)


def _resolve_slug_to_path(slug: str) -> Path | None:
    out = _run_tool("query", f"slug={slug}", fmt="paths").strip()
    if not out:
        return None
    candidates = [line.strip() for line in out.splitlines()
                  if line.strip() and not line.startswith("…")]
    if not candidates:
        return None
    for suffix in _FILE_PRIORITY:
        for c in candidates:
            if c.endswith(suffix):
                return REPO_ROOT / c
    return REPO_ROOT / candidates[0]


def _cap(text: str) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= OUTPUT_CAP_BYTES:
        return text
    cut = raw[:OUTPUT_CAP_BYTES].decode("utf-8", errors="ignore")
    if "\n" in cut:
        cut = cut[: cut.rfind("\n") + 1]
    return cut + "… [truncated; cap=1024B]\n"


def cmd_summary(args: argparse.Namespace) -> int:
    path = _resolve_slug_to_path(args.slug)
    if not path:
        sys.stderr.write(f"skills-query: no file with slug={args.slug!r}\n")
        return 1
    out = _run_tool(
        "extract", "--frontmatter", "summary", str(path.relative_to(REPO_ROOT))
    )
    sys.stdout.write(_cap(out))
    return 0


def cmd_skills(args: argparse.Namespace) -> int:
    if args.kind:
        out = _run_tool(
            "query", "has-key=skill_kind", scope="skills", fmt="paths"
        )
        filtered = []
        for path_str in out.splitlines():
            if not path_str.strip() or path_str.startswith("…"):
                continue
            try:
                fm = _core.read_fm(REPO_ROOT / path_str.strip(), strict=False)
            except Exception:
                continue
            if fm.get("skill_kind") == args.kind:
                filtered.append(path_str.strip())
        sys.stdout.write(_cap("\n".join(filtered) + ("\n" if filtered else "")))
        return 0
    if args.target_agent:
        out = _run_tool(
            "query", "has-key=skill_target_agents", scope="skills", fmt="paths"
        )
        filtered = []
        for path_str in out.splitlines():
            if not path_str.strip() or path_str.startswith("…"):
                continue
            try:
                fm = _core.read_fm(REPO_ROOT / path_str.strip(), strict=False)
            except Exception:
                continue
            targets = fm.get("skill_target_agents") or []
            if args.target_agent in targets:
                filtered.append(path_str.strip())
        sys.stdout.write(_cap("\n".join(filtered) + ("\n" if filtered else "")))
        return 0
    out = _run_tool("query", "has-key=name", scope="skills", fmt="paths")
    sys.stdout.write(_cap(out))
    return 0


def cmd_references(args: argparse.Namespace) -> int:
    forward = _run_tool("query", f"refers-to={args.slug}", fmt="paths")
    reverse = _run_tool("query", f"referenced-by={args.slug}", fmt="paths")
    body = (
        "## refers-to (this slug appears in their lists)\n"
        f"{forward}"
        "\n## referenced-by (the named slug's lists name this file)\n"
        f"{reverse}"
    )
    sys.stdout.write(_cap(body))
    return 0


def cmd_orphans(args: argparse.Namespace) -> int:
    out = _run_tool("graph", "--detect", "orphans,dangling", allow_nonzero=True)
    sys.stdout.write(_cap(out))
    return 0


def cmd_stale(args: argparse.Namespace) -> int:
    if not re.match(r"^\d+d$", args.since):
        sys.stderr.write("skills-query: --since must be in <N>d form (e.g. 30d)\n")
        return 2
    out = _run_tool("query", f"stale-since={args.since}", fmt="paths")
    sys.stdout.write(_cap(out))
    return 0


def cmd_path(args: argparse.Namespace) -> int:
    out = _run_tool("query", f"slug={args.slug}", fmt="paths")
    sys.stdout.write(_cap(out))
    return 0


def cmd_header(args: argparse.Namespace) -> int:
    path = _resolve_slug_to_path(args.slug)
    if not path:
        sys.stderr.write(f"skills-query: no file with slug={args.slug!r}\n")
        return 1
    out = _run_tool(
        "extract", "--section", args.header, str(path.relative_to(REPO_ROOT))
    )
    sys.stdout.write(_cap(out))
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    selector = f"type={args.type}"
    out = _run_tool("query", selector, fmt="paths")
    if args.status is None:
        sys.stdout.write(_cap(out))
        return 0
    filtered: list[str] = []
    for path_str in out.splitlines():
        if not path_str.strip() or path_str.startswith("…"):
            continue
        try:
            fm = _core.read_fm(REPO_ROOT / path_str.strip(), strict=False)
        except Exception:
            continue
        if args.type == "task" and fm.get("task_status") == args.status:
            filtered.append(path_str.strip())
        elif args.type != "task" and fm.get("status") == args.status:
            filtered.append(path_str.strip())
    sys.stdout.write(_cap("\n".join(filtered) + ("\n" if filtered else "")))
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    out = _run_tool("query", "has-key=name", scope="skills", fmt="paths")
    entries: list[dict] = []
    for path_str in out.splitlines():
        if not path_str.strip() or path_str.startswith("…"):
            continue
        path = REPO_ROOT / path_str.strip()
        try:
            fm = _core.read_fm(path, strict=False)
        except Exception:
            continue
        entries.append({
            "slug": fm.get("slug") or fm.get("name") or path.parent.name,
            "name": fm.get("name"),
            "path": str(path.relative_to(REPO_ROOT)),
            "description": (fm.get("description") or "")[:200],
        })
    body = json.dumps({"skills": entries}, indent=2)
    sys.stdout.write(_cap(body + "\n"))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="skills-query", description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("summary", help="print L1 summary of a slug")
    s.add_argument("slug")
    s.set_defaults(func=cmd_summary)

    s = sp.add_parser("skills", help="filter skills by metadata")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--kind")
    g.add_argument("--target-agent")
    s.set_defaults(func=cmd_skills)

    s = sp.add_parser("references", help="forward + reverse references for a slug")
    s.add_argument("slug")
    s.set_defaults(func=cmd_references)

    s = sp.add_parser("orphans", help="list orphan / dangling slugs from fm-graph")
    s.set_defaults(func=cmd_orphans)

    s = sp.add_parser("stale", help="list files older than <N>d")
    s.add_argument("--since", required=True, help="cutoff in <N>d form (e.g. 30d)")
    s.set_defaults(func=cmd_stale)

    s = sp.add_parser("path", help="resolve a slug to its absolute repo-relative path")
    s.add_argument("slug")
    s.set_defaults(func=cmd_path)

    s = sp.add_parser("header", help="emit a single ## section body for a slug")
    s.add_argument("slug")
    s.add_argument("header")
    s.set_defaults(func=cmd_header)

    s = sp.add_parser("graph", help="filter operational files by type + status")
    s.add_argument("--type", required=True,
                   choices=["task", "prompt", "research", "skill", "adr",
                            "spec", "readme", "index", "note"])
    s.add_argument("--status",
                   help="task_status (for type=task) or status (other types)")
    s.set_defaults(func=cmd_graph)

    s = sp.add_parser("manifest", help="emit a minimal skills manifest as JSON")
    s.set_defaults(func=cmd_manifest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
