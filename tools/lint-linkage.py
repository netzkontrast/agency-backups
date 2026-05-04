#!/usr/bin/env python3
"""
Cross-reference linkage validator for the agency repository.

Enforces the frontmatter-graph rules from TASK.md §7 and FOLDERS.md §6:

  task_uses_prompts    — every slug MUST resolve to /prompts/<slug>/prompt.md
  task_spawns_research — every slug MUST resolve to /research/<slug>/
  prompt_relates_to_task — the named task MUST list this prompt in task_uses_prompts
  prompt_spawned_from_research — the research slug MUST exist under /research/
  research_executes_prompt — the prompt slug MUST exist under /prompts/<slug>/

Additional checks from TASK.md §7:
  - When task_status is "done", every Todo checkbox MUST be checked.
  - When task_status is "done", friction-log.md MUST exist in the task folder.

External result linkage (RESEARCH.md §6.5):
  - Every /research/<provider>/<slug>/result.md with research_executes_prompt set
    MUST have a corresponding /prompts/<slug>/ stub.
  - Every external result MUST have a downstream open Task in /tasks/ that includes
    the result.md path in task_affects_paths.

Usage:
    python3 tools/lint-linkage.py

Exits 0 on success, 1 on any diagnostic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
PROVIDER_NAMES = {"gemini", "gpt", "human", "other"}
TODO_UNCHECKED_RE = re.compile(r"^- \[ \]", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, object]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    mapping: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- "):
            if current_list_key is not None:
                mapping.setdefault(current_list_key, []).append(
                    stripped[2:].strip().strip('"')
                )
            continue
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        current_list_key = None
        if val == "":
            mapping[key] = []
            current_list_key = key
        elif val == "[]":
            mapping[key] = []
        else:
            mapping[key] = val.strip('"')
    return mapping


def read_fm(path: Path) -> dict[str, object]:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"))
    except OSError:
        return {}


def str_list(fm: dict, key: str) -> list[str]:
    v = fm.get(key, [])
    if isinstance(v, list):
        return [s for s in v if s]
    if isinstance(v, str) and v:
        return [v]
    return []


def str_val(fm: dict, key: str) -> str:
    v = fm.get(key, "")
    return v if isinstance(v, str) else ""


def lint_tasks(
    tasks_root: Path,
    prompts_root: Path,
    research_root: Path,
) -> list[str]:
    errors: list[str] = []
    for task_dir in sorted(tasks_root.iterdir()):
        task_md = task_dir / "task.md"
        if not task_md.exists():
            continue
        fm = read_fm(task_md)
        task_status = str_val(fm, "task_status")

        # task_uses_prompts must resolve
        for slug in str_list(fm, "task_uses_prompts"):
            prompt_path = prompts_root / slug / "prompt.md"
            if not prompt_path.exists():
                errors.append(
                    f"{task_md}: task_uses_prompts slug '{slug}' does not resolve "
                    f"to {prompt_path} (TASK.md §7.2)"
                )

        # task_spawns_research must resolve — only enforced when task is done
        # (open/in_progress tasks may declare future research before it is created)
        if task_status in ("done", "abandoned"):
            for slug in str_list(fm, "task_spawns_research"):
                research_path = research_root / slug
                if not research_path.is_dir():
                    errors.append(
                        f"{task_md}: task_spawns_research slug '{slug}' does not resolve "
                        f"to {research_path}/ (TASK.md §7.3)"
                    )

        # When done: all todos checked + friction-log.md exists
        if task_status == "done":
            text = task_md.read_text(encoding="utf-8")
            if TODO_UNCHECKED_RE.search(text):
                errors.append(
                    f"{task_md}: task_status is 'done' but unchecked Todo items remain "
                    f"(TASK.md §7.5)"
                )
            if not (task_dir / "friction-log.md").exists():
                errors.append(
                    f"{task_dir}: task_status is 'done' but friction-log.md is missing "
                    f"(TASK.md §7.6 / Spec-L.3.1)"
                )

    return errors


def lint_prompts(
    prompts_root: Path,
    tasks_root: Path,
    research_root: Path,
) -> list[str]:
    errors: list[str] = []
    for prompt_dir in sorted(prompts_root.iterdir()):
        prompt_md = prompt_dir / "prompt.md"
        if not prompt_md.exists():
            continue
        fm = read_fm(prompt_md)

        # prompt_relates_to_task: the task must list this prompt
        task_slug = str_val(fm, "prompt_relates_to_task")
        if task_slug:
            # find the task directory by slug (strip NNN- prefix)
            task_md = None
            for td in tasks_root.iterdir():
                if td.is_dir() and td.name.endswith(f"-{task_slug}"):
                    task_md = td / "task.md"
                    break
            if task_md is None or not task_md.exists():
                errors.append(
                    f"{prompt_md}: prompt_relates_to_task '{task_slug}' does not "
                    f"resolve to any task folder (PROMPT.md §6.6)"
                )
            else:
                task_fm = read_fm(task_md)
                if prompt_dir.name not in str_list(task_fm, "task_uses_prompts"):
                    errors.append(
                        f"{prompt_md}: prompt_relates_to_task '{task_slug}' exists "
                        f"but task does not list '{prompt_dir.name}' in "
                        f"task_uses_prompts (FOLDERS.md §6 reciprocity)"
                    )

        # prompt_spawned_from_research must resolve
        research_slug = str_val(fm, "prompt_spawned_from_research")
        if research_slug:
            if not (research_root / research_slug).is_dir():
                errors.append(
                    f"{prompt_md}: prompt_spawned_from_research '{research_slug}' "
                    f"does not resolve to /research/{research_slug}/ (PROMPT.md §6.5)"
                )

    return errors


def lint_research(
    research_root: Path,
    prompts_root: Path,
    tasks_root: Path,
) -> list[str]:
    errors: list[str] = []
    for entry in sorted(research_root.iterdir()):
        if not entry.is_dir() or entry.name == "readme.md":
            continue
        if entry.name in PROVIDER_NAMES:
            # External provider subfolder
            for slug_dir in sorted(entry.iterdir()):
                result_md = slug_dir / "result.md"
                if not result_md.exists():
                    continue
                fm = read_fm(result_md)
                prompt_slug = str_val(fm, "research_executes_prompt")
                if prompt_slug:
                    if not (prompts_root / prompt_slug / "prompt.md").exists():
                        errors.append(
                            f"{result_md}: research_executes_prompt '{prompt_slug}' "
                            f"stub prompt missing at /prompts/{prompt_slug}/prompt.md "
                            f"(RESEARCH.md §6.3)"
                        )
                # RESEARCH.md §6.5: must have a downstream open Task
                result_rel = str(result_md.relative_to(Path(".")))
                downstream = []
                for td in tasks_root.iterdir():
                    t_md = td / "task.md"
                    if not t_md.exists():
                        continue
                    tfm = read_fm(t_md)
                    paths = str_list(tfm, "task_affects_paths")
                    if any(result_rel in p or p in result_rel for p in paths):
                        downstream.append(td)
                if not downstream:
                    errors.append(
                        f"{result_md}: external result has no downstream analysis Task "
                        f"with this path in task_affects_paths (RESEARCH.md §6.5)"
                    )
            continue

        # Normal research workspace
        readme = entry / "readme.md"
        if readme.exists():
            fm = read_fm(readme)
        else:
            spec_md = entry / "output" / "SPEC.md"
            fm = read_fm(spec_md) if spec_md.exists() else {}

        prompt_slug = str_val(fm, "research_executes_prompt")
        if prompt_slug:
            if not (prompts_root / prompt_slug).is_dir():
                errors.append(
                    f"{entry}/readme.md: research_executes_prompt '{prompt_slug}' "
                    f"does not resolve to /prompts/{prompt_slug}/ (RESEARCH.md §5.2)"
                )

    return errors


def main(argv: list[str]) -> int:
    root = Path(".")
    tasks_root = root / "tasks"
    prompts_root = root / "prompts"
    research_root = root / "research"

    all_errors: list[str] = []

    if tasks_root.exists() and prompts_root.exists() and research_root.exists():
        all_errors.extend(lint_tasks(tasks_root, prompts_root, research_root))
        all_errors.extend(lint_prompts(prompts_root, tasks_root, research_root))
        all_errors.extend(lint_research(research_root, prompts_root, tasks_root))
    else:
        missing = [
            str(d)
            for d in [tasks_root, prompts_root, research_root]
            if not d.exists()
        ]
        print(f"lint-linkage: skipped — missing directories: {missing}")
        return 0

    for e in all_errors:
        print(f"ERROR {e}", file=sys.stderr)

    print(f"lint-linkage: {len(all_errors)} error(s).")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
