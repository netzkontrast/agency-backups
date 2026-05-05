#!/usr/bin/env python3
"""fm-new — template-driven scaffolder for task / prompt / research folders.

Subcommands:
    python3 tools/fm/new.py task --slug <slug> --summary <s> [--priority P{1-3}] [--owner <name>]
    python3 tools/fm/new.py prompt --slug <slug> --summary <s> [--kind <k>] [--framework <f>] [--target-agent <a>]
    python3 tools/fm/new.py research --slug <slug> --summary <s> [--executes-prompt <p>]

Behaviour:
    - For `task`: allocates the next zero-padded id by scanning `tasks/`.
    - Refuses to clobber an existing folder (exit 4).
    - Output passes `tools/fm/validate.py` and `tools/fm/validate.py --check-body`.

Exit codes:
    0 success / 2 usage / 4 target exists.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_EXISTS = 4

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){0,5}$")


def _today() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def _validate_slug(slug: str) -> None:
    if not SLUG_RE.match(slug):
        raise SystemExit(f"fm-new: invalid slug {slug!r} — kebab-case 1-6 tokens of [a-z0-9]")


def _next_task_id(tasks_dir: Path) -> str:
    highest = -1
    if tasks_dir.is_dir():
        for child in tasks_dir.iterdir():
            if not child.is_dir():
                continue
            m = re.match(r"^(\d{3})-", child.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def _refuse_clobber(folder: Path) -> int | None:
    if folder.exists():
        print(f"fm-new: refusing to clobber existing folder {folder}", file=sys.stderr)
        return EXIT_EXISTS
    return None


def _q(s: str) -> str:
    """Quote a value for inline YAML scalar form."""
    return s.replace('"', "'")


def _make_task(args: argparse.Namespace, repo_root: Path) -> int:
    _validate_slug(args.slug)
    today = _today()
    task_id = _next_task_id(repo_root / "tasks")
    folder = repo_root / "tasks" / f"{task_id}-{args.slug}"
    if (e := _refuse_clobber(folder)) is not None:
        return e
    folder.mkdir(parents=True)

    task_md = (
        "---\n"
        "type: task\n"
        "status: active\n"
        f"slug: {args.slug}\n"
        f'summary: "{_q(args.summary)}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        f'task_id: "{task_id}"\n'
        "task_status: open\n"
        f'task_owner: "{_q(args.owner)}"\n'
        f"task_priority: {args.priority}\n"
        "task_uses_prompts: []\n"
        "task_spawns_research: []\n"
        "task_spawns_prompts: []\n"
        "task_affects_paths: []\n"
        "---\n\n"
        f"# Task {task_id} — {args.summary}\n\n"
        "## Goal\n\n"
        "Replace this paragraph with one falsifiable success condition.\n\n"
        "## Plan\n\n"
        "1. Replace this with the first execution step.\n\n"
        "## Todo\n\n"
        "- [ ] 1. Replace this with the first actionable item.\n\n"
        "## Links\n\n"
        f"- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)\n"
    )
    (folder / "task.md").write_text(task_md, encoding="utf-8")

    readme_md = (
        "---\n"
        "type: index\n"
        "status: active\n"
        f"slug: task-{task_id}-{args.slug}\n"
        f'summary: "Index for Task {task_id}: {_q(args.summary)}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "---\n\n"
        f"# Task {task_id} — Index\n\n"
        f"- [`task.md`](./task.md)\n"
    )
    (folder / "readme.md").write_text(readme_md, encoding="utf-8")
    print(f"created {folder.relative_to(repo_root)}/", file=sys.stderr)
    return EXIT_OK


def _make_prompt(args: argparse.Namespace, repo_root: Path) -> int:
    _validate_slug(args.slug)
    today = _today()
    folder = repo_root / "prompts" / args.slug
    if (e := _refuse_clobber(folder)) is not None:
        return e
    folder.mkdir(parents=True)

    prompt_md = (
        "---\n"
        "type: prompt\n"
        "status: draft\n"
        f"slug: {args.slug}\n"
        f'summary: "{_q(args.summary)}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        f"prompt_kind: {args.prompt_kind}\n"
        f"prompt_framework: {args.framework}\n"
        f'prompt_target_agent: "{_q(args.target_agent)}"\n'
        "---\n\n"
        f"# {args.summary}\n\n"
        "## Framework\n\n"
        f"Declared framework: {args.framework}. Refine this paragraph when the prompt is authored.\n\n"
        "## R — Role\n\n"
        f"Single sentence defining the executor persona. Replace this placeholder before {args.target_agent} runs the prompt.\n\n"
        "## I — Input\n\n"
        "- Replace this bullet with the first input file or URL.\n\n"
        "## S — Steps\n\n"
        "1. Replace this with the first execution step (RFC 2119 keyword required).\n"
        "2. Replace this with the second step.\n"
        "3. Replace this with the third step.\n\n"
        "## E — Expectations\n\n"
        "- Replace this bullet with the first deliverable artefact path.\n\n"
        "## Constraints\n\n"
        "- The agent MUST replace every placeholder above before executing the prompt.\n"
    )
    (folder / "prompt.md").write_text(prompt_md, encoding="utf-8")

    readme_md = (
        "---\n"
        "type: index\n"
        "status: active\n"
        f"slug: prompt-{args.slug}\n"
        f'summary: "Index for prompt: {_q(args.summary)}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "---\n\n"
        f"# /prompts/{args.slug}/\n\n"
        f"- [`prompt.md`](./prompt.md)\n"
    )
    (folder / "readme.md").write_text(readme_md, encoding="utf-8")
    print(f"created {folder.relative_to(repo_root)}/", file=sys.stderr)
    return EXIT_OK


def _make_research(args: argparse.Namespace, repo_root: Path) -> int:
    _validate_slug(args.slug)
    today = _today()
    folder = repo_root / "research" / args.slug
    if (e := _refuse_clobber(folder)) is not None:
        return e
    folder.mkdir(parents=True)

    executes = args.executes_prompt or args.slug
    readme_md = (
        "---\n"
        "type: research\n"
        "status: active\n"
        f"slug: {args.slug}\n"
        f'summary: "{_q(args.summary)}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "research_phase: kickoff\n"
        f"research_executes_prompt: {executes}\n"
        "research_friction_level: FL0\n"
        "---\n\n"
        f"# Research — {args.slug}\n\n"
        f"Workspace for the prompt at `/prompts/{executes}/`.\n"
    )
    (folder / "readme.md").write_text(readme_md, encoding="utf-8")
    print(f"created {folder.relative_to(repo_root)}/", file=sys.stderr)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fm-new")
    sub = p.add_subparsers(dest="subcommand", required=True)

    pt = sub.add_parser("task")
    pt.add_argument("--slug", required=True)
    pt.add_argument("--summary", required=True)
    pt.add_argument("--priority", default="P2", choices=["P1", "P2", "P3"])
    pt.add_argument("--owner", default="unassigned")

    pp = sub.add_parser("prompt")
    pp.add_argument("--slug", required=True)
    pp.add_argument("--summary", required=True)
    pp.add_argument("--kind", dest="prompt_kind", default="task-spec")
    pp.add_argument("--framework", default="RISEN+ReAct")
    pp.add_argument("--target-agent", default="Claude Code")

    pr = sub.add_parser("research")
    pr.add_argument("--slug", required=True)
    pr.add_argument("--summary", required=True)
    pr.add_argument("--executes-prompt", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = _core.repo_root_from_cwd()
    if args.subcommand == "task":
        return _make_task(args, repo_root)
    if args.subcommand == "prompt":
        return _make_prompt(args, repo_root)
    if args.subcommand == "research":
        return _make_research(args, repo_root)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
