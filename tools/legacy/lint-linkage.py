#!/usr/bin/env python3
"""
DEPRECATED — moved to tools/legacy/ by Task 017.

The cross-reference graph this linter walks (task_uses_prompts /
task_spawns_research / prompt_relates_to_task) is now queryable via
fm-query. A delta-aware linkage check on top of fm-query is the
intended successor; until that lands, this linter is retained as the
authoritative graph validator.

Will move out of tools/legacy/ if a successor isn't shipped before the
Task 017 cleanup commit.

Original docstring follows.

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

from _frontmatter import read_fm, str_list, str_val

PROVIDER_NAMES = {"gemini", "gpt", "human", "other"}
TODO_UNCHECKED_RE = re.compile(r"^- \[ \]", re.MULTILINE)


def _find_task_by_id_or_slug(tasks_root: Path, ref: str) -> Path | None:
    """Resolve a task_id (e.g. '010') or slug to its /tasks/<NNN>-<slug>/ folder.

    Used by the 'updated' lifecycle reciprocity check (TASK.md §4.7, §7.10):
    a successor reference may be either a zero-padded id or the kebab-case slug
    of the target Task. Returns None if no folder matches.
    """
    if not ref:
        return None
    ref = ref.strip()
    for task_dir in tasks_root.iterdir():
        if not task_dir.is_dir():
            continue
        name = task_dir.name
        if "-" not in name:
            continue
        nnn, _, slug = name.partition("-")
        if ref == nnn or ref == slug or ref == name:
            return task_dir
    return None


def research_slug_resolves(research_root: Path, slug: str) -> bool:
    """A research slug resolves if /research/<slug>/ exists OR a provider
    subfolder /research/<provider>/<slug>/ exists. The provider case covers
    external research executions (RESEARCH.md §6) which are valid spawn sources
    for follow-up prompts."""
    if (research_root / slug).is_dir():
        return True
    for provider in PROVIDER_NAMES:
        if (research_root / provider / slug).is_dir():
            return True
    return False


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
                if not research_slug_resolves(research_root, slug):
                    errors.append(
                        f"{task_md}: task_spawns_research slug '{slug}' does not resolve "
                        f"to research/{slug}/ or any research/<provider>/{slug}/ "
                        f"(TASK.md §7.3)"
                    )

            for slug in str_list(fm, "task_spawns_prompts"):
                prompt_path = prompts_root / slug / "prompt.md"
                if not prompt_path.exists():
                    errors.append(
                        f"{task_md}: task_spawns_prompts slug '{slug}' does not resolve "
                        f"to {prompt_path}"
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

        # When updated: friction-log.md MUST exist with a Supersession Rationale,
        # and task_superseded_by MUST resolve reciprocally to a successor that
        # carries this task's id in task_supersedes (TASK.md §4.7, §7.10).
        if task_status == "updated":
            log_path = task_dir / "friction-log.md"
            if not log_path.exists():
                errors.append(
                    f"{task_dir}: task_status is 'updated' but friction-log.md is missing "
                    f"(TASK.md §4.7 / §7.7)"
                )
            else:
                log_text = log_path.read_text(encoding="utf-8")
                if "Supersession Rationale" not in log_text:
                    errors.append(
                        f"{log_path}: 'updated' closure requires a "
                        f"'## Supersession Rationale' section (TASK.md §4.7)"
                    )

            successors = str_list(fm, "task_superseded_by")
            if not successors:
                errors.append(
                    f"{task_md}: task_status is 'updated' but task_superseded_by is empty "
                    f"(TASK.md §7.10)"
                )
            else:
                this_id = str_val(fm, "task_id")
                for succ in successors:
                    succ_dir = _find_task_by_id_or_slug(tasks_root, succ)
                    if succ_dir is None:
                        errors.append(
                            f"{task_md}: task_superseded_by '{succ}' does not resolve "
                            f"to any /tasks/<NNN>-<slug>/ folder (TASK.md §7.10)"
                        )
                        continue
                    succ_fm = read_fm(succ_dir / "task.md")
                    succ_supersedes = str_list(succ_fm, "task_supersedes")
                    if this_id and this_id not in succ_supersedes and \
                            str_val(fm, "slug") not in succ_supersedes:
                        errors.append(
                            f"{succ_dir / 'task.md'}: task_supersedes is missing "
                            f"reciprocal entry for predecessor '{this_id}' "
                            f"(TASK.md §7.10)"
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
                if (prompt_dir.name not in str_list(task_fm, "task_uses_prompts") and
                    prompt_dir.name not in str_list(task_fm, "task_spawns_prompts")):
                    errors.append(
                        f"{prompt_md}: prompt_relates_to_task '{task_slug}' exists "
                        f"but task does not list '{prompt_dir.name}' in "
                        f"task_uses_prompts or task_spawns_prompts (FOLDERS.md §6 reciprocity)"
                    )

        # prompt_spawned_from_research must resolve (top-level or provider subfolder)
        research_slug = str_val(fm, "prompt_spawned_from_research")
        if research_slug:
            if not research_slug_resolves(research_root, research_slug):
                errors.append(
                    f"{prompt_md}: prompt_spawned_from_research '{research_slug}' "
                    f"does not resolve to /research/{research_slug}/ or any "
                    f"/research/<provider>/{research_slug}/ (PROMPT.md §6.5)"
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


def lint_tasks_index(tasks_root: Path) -> list[str]:
    """Enforce TASK.md §4.8 / §7.11: tasks/readme.md MUST list every
    tasks/<NNN>-<slug>/ folder on disk, and every bullet pointer MUST
    resolve to an existing folder. The index is the human-readable surface
    every agent consults before opening a Task body; a stale index is a
    session-continuity failure.
    """
    errors: list[str] = []
    index_path = tasks_root / "readme.md"
    if not index_path.exists():
        errors.append(f"{index_path}: missing tasks/readme.md (TASK.md §4.8)")
        return errors

    index_text = index_path.read_text(encoding="utf-8")

    # Membership: every tasks/<NNN>-<slug>/ folder MUST appear in the index.
    folder_re = re.compile(r"^[0-9]{3}-[a-z0-9-]+$")
    on_disk = [
        p.name for p in tasks_root.iterdir()
        if p.is_dir() and folder_re.match(p.name)
    ]
    referenced_re = re.compile(r"\(\./([0-9]{3}-[a-z0-9-]+)/\)")
    referenced = set(referenced_re.findall(index_text))

    for folder in sorted(on_disk):
        if folder not in referenced:
            errors.append(
                f"{index_path}: missing bullet for tasks/{folder}/ "
                f"(TASK.md §4.8 / §7.11)"
            )

    for ref in sorted(referenced):
        if ref not in on_disk:
            errors.append(
                f"{index_path}: bullet references tasks/{ref}/ which does "
                f"not exist on disk (TASK.md §4.8 / §7.11)"
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
        all_errors.extend(lint_tasks_index(tasks_root))
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
