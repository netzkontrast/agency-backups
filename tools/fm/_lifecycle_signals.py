"""Five-signal lifecycle signals + classify_task() for Task 049.

Implements `research/spec-staleness-decision-formalization/output/SPEC.md`
§1 (decision tree) and §2 (signal extraction recipes). Each signal is a
pure function of repo state with no LLM judgement; the algorithm is
deterministic at a given `HEAD`.

Consumed by `tools/fm/check-task-lifecycle-classification.py`.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from fm._core import read_fm, str_list, str_val


# ---- Bucket enum -------------------------------------------------------------

@dataclass(frozen=True)
class Bucket:
    name: str
    description: str


STILL_ACCURATE = Bucket(
    "STILL_ACCURATE",
    "Goal endorsed, plan anchors live, no successor, partial Todo. No transition warranted.",
)
DRIFTED = Bucket(
    "DRIFTED",
    "Goal endorsed, but a successor exists or a plan anchor has been retired. §4.7 `updated`.",
)
COMPLETED_BY_DRIFT = Bucket(
    "COMPLETED_BY_DRIFT",
    "Every Todo satisfied and every affected path materialised. §4.6 `done` (or §4.7 `updated`).",
)
NO_LONGER_DESIRABLE = Bucket(
    "NO_LONGER_DESIRABLE",
    "No current root spec endorses the Goal. §8.3 `abandoned`.",
)


ROOT_SPECS = (
    "AGENTS.md",
    "TASK.md",
    "MAINTENANCE.md",
    "RESEARCH.md",
    "FOLDERS.md",
    "PROMPT.md",
    "PRE_COMMIT.md",
    "FRUSTRATED.md",
    "SKILLS.md",
    "CLAUDE.md",
    "README.md",
)


_TODO_LINE = re.compile(r"^\s*-\s\[([ x])\]\s", re.MULTILINE)
_HEADING = re.compile(r"^##\s+(.+?)\s*$")
_MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _section_body(task_body: str, heading: str) -> str:
    """Return the body of the `## <heading>` section, empty string if absent."""
    target = heading.strip().lower()
    lines = task_body.splitlines()
    collected: list[str] = []
    in_section = False
    for line in lines:
        m = _HEADING.match(line)
        if m:
            if in_section:
                break
            if m.group(1).strip().lower() == target:
                in_section = True
                continue
            continue
        if in_section:
            collected.append(line)
    return "\n".join(collected)


# ---- S1 — todo_satisfaction --------------------------------------------------

def signal_todo_satisfaction(task_path: Path) -> float:
    """Fraction of `## Todo` checkboxes that are `[x]`. 0.0 if no Todo."""
    body = task_path.read_text(encoding="utf-8")
    todo_body = _section_body(body, "Todo")
    if not todo_body.strip():
        return 0.0
    matches = _TODO_LINE.findall(todo_body)
    if not matches:
        return 0.0
    checked = sum(1 for c in matches if c == "x")
    return checked / len(matches)


# ---- S2 — affects_paths_present ----------------------------------------------

def _path_nonempty(repo: Path, rel: str) -> bool:
    p = (repo / rel).resolve()
    if not p.exists():
        return False
    if p.is_file():
        return True
    # Directory: non-empty
    return any(p.iterdir())


def signal_affects_paths_present(task_fm: dict, repo: Path) -> bool:
    """AND across task_affects_paths existence. False if list is empty."""
    paths = [s for s in str_list(task_fm, "task_affects_paths") if s]
    if not paths:
        return False
    return all(_path_nonempty(repo, p) for p in paths)


# ---- S3 — plan_anchors_live --------------------------------------------------

_RETIRED_PREFIXES = ("tools/legacy/",)


def _is_retired(target: str) -> bool:
    target = target.strip()
    for prefix in _RETIRED_PREFIXES:
        if target.startswith(prefix) or f"/{prefix}" in target:
            return True
    return False


def _resolve_link(task_path: Path, link: str) -> Path | None:
    """Resolve a relative Markdown link target to an absolute Path, or None for non-relative."""
    if link.startswith(("http://", "https://", "mailto:", "#")):
        return None
    base = link.split("#", 1)[0].split("?", 1)[0]
    if not base:
        return None
    return (task_path.parent / base).resolve()


def signal_plan_anchors_live(task_path: Path, repo: Path) -> bool:
    """Every relative Markdown link target in `## Plan` resolves on disk
    AND none lives under `tools/legacy/` or another retired path. True if
    `## Plan` has zero links (no anchors to retire)."""
    body = task_path.read_text(encoding="utf-8")
    plan = _section_body(body, "Plan")
    if not plan.strip():
        return True
    targets = _MD_LINK.findall(plan)
    if not targets:
        return True
    for raw in targets:
        if _is_retired(raw):
            return False
        resolved = _resolve_link(task_path, raw)
        if resolved is None:
            continue  # non-relative; ignore
        if not resolved.exists():
            return False
    return True


# ---- S4 — goal_endorsed ------------------------------------------------------

def _grep_count(repo: Path, pattern: str, paths: Iterable[str]) -> int:
    """Use `git grep -l` if available, else a Python fallback."""
    path_list = list(paths)
    if not path_list:
        return 0
    try:
        proc = subprocess.run(
            ["git", "grep", "-l", "-E", pattern, "--", *path_list],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode in (0, 1):  # 1 means no matches under git-grep
            return len([l for l in proc.stdout.splitlines() if l.strip()])
    except FileNotFoundError:
        pass
    # Fallback: scan files in Python.
    rx = re.compile(pattern)
    hits = 0
    for rel in path_list:
        full = repo / rel
        if not full.exists():
            continue
        try:
            text = full.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if rx.search(text):
            hits += 1
    return hits


def signal_goal_endorsed_by_spec(
    task_fm: dict, task_path: Path, repo: Path,
) -> bool:
    """True iff ≥1 root spec contains a reference to this Task's
    `<NNN>-<slug>` or any of its `task_affects_paths` entries. False
    absent evidence."""
    task_id = str_val(task_fm, "task_id").strip().strip('"')
    folder = task_path.parent.name
    affects = [s for s in str_list(task_fm, "task_affects_paths") if s]
    patterns: list[str] = []
    if folder:
        patterns.append(re.escape(folder))
    if task_id:
        patterns.append(rf"task_id[^\n]*{re.escape(task_id)}")
    for a in affects:
        patterns.append(re.escape(a))
    if not patterns:
        return False
    pattern = "|".join(patterns)
    existing_specs = [s for s in ROOT_SPECS if (repo / s).exists()]
    return _grep_count(repo, pattern, existing_specs) >= 1


# ---- S5 — successor_present --------------------------------------------------

def signal_successor_present(task_fm: dict, task_path: Path, repo: Path) -> bool:
    """True iff `task_superseded_by` non-empty OR any other task.md lists
    this Task's task_id/slug in `task_supersedes`."""
    superseded_by = [s for s in str_list(task_fm, "task_superseded_by") if s.strip()]
    if superseded_by:
        return True
    self_id = str_val(task_fm, "task_id").strip().strip('"')
    self_folder = task_path.parent.name
    self_slug = self_folder.split("-", 1)[1] if "-" in self_folder else self_folder
    candidates = [self_id, self_folder, self_slug]
    candidates = [c for c in candidates if c]
    if not candidates:
        return False
    tasks_root = task_path.parent.parent
    pattern_parts = [re.escape(c) for c in candidates]
    pattern = rf"task_supersedes:[^\n]*({'|'.join(pattern_parts)})"
    # Also match list-item form (one per line)
    alt_pattern = rf"^\s*-\s*\"?({'|'.join(pattern_parts)})\"?\s*$"
    for folder in sorted(tasks_root.iterdir()):
        if not folder.is_dir() or folder == task_path.parent:
            continue
        other = folder / "task.md"
        if not other.exists():
            continue
        try:
            text = other.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Find `task_supersedes:` block and inspect either inline list or
        # following indented `- "X"` entries.
        if "task_supersedes:" not in text:
            continue
        # Inline form: `task_supersedes: ["010"]` or similar
        if re.search(pattern, text):
            return True
        # Block form: lines after `task_supersedes:` up to next non-indented line
        lines = text.splitlines()
        in_block = False
        for line in lines:
            if line.startswith("task_supersedes:"):
                in_block = True
                # check inline
                rest = line.split(":", 1)[1].strip()
                if rest.startswith("[") and any(c in rest for c in candidates):
                    return True
                continue
            if in_block:
                if re.match(r"^\s+-\s+", line):
                    if re.search(alt_pattern, line):
                        return True
                else:
                    in_block = False
    return False


# ---- classify_task -----------------------------------------------------------

@dataclass(frozen=True)
class ClassificationResult:
    bucket: Bucket
    signals: dict
    trace: str


def classify_task(
    task_path: Path,
    repo: Path,
    today,  # datetime.date
    stale_days: int = 7,
) -> ClassificationResult:
    """Run §1 decision tree against `task_path`. Returns the bucket plus
    signal vector for diagnostic emission."""
    fm = read_fm(task_path, strict=False) or {}

    # Gate: only audit candidates older than the staleness window.
    created = str_val(fm, "created").strip()
    from datetime import date
    try:
        created_date = date.fromisoformat(created)
    except ValueError:
        created_date = today  # treat unparseable as "today" → gate fires
    age_days = (today - created_date).days
    if age_days <= stale_days:
        return ClassificationResult(
            bucket=STILL_ACCURATE,
            signals={"age_days": age_days, "stale_days": stale_days},
            trace=f"gate: age_days={age_days} <= stale_days={stale_days} -> STILL_ACCURATE",
        )

    s1 = signal_todo_satisfaction(task_path)
    s2 = signal_affects_paths_present(fm, repo)
    s3 = signal_plan_anchors_live(task_path, repo)
    s4 = signal_goal_endorsed_by_spec(fm, task_path, repo)
    s5 = signal_successor_present(fm, task_path, repo)
    signals = {
        "todo_satisfaction": s1,
        "affects_paths_present": s2,
        "plan_anchors_live": s3,
        "goal_endorsed": s4,
        "successor_present": s5,
    }

    if not s4:
        return ClassificationResult(
            NO_LONGER_DESIRABLE, signals,
            "Level 1: goal_endorsed=False -> NO_LONGER_DESIRABLE",
        )
    if s1 >= 1.0 and s2:
        return ClassificationResult(
            COMPLETED_BY_DRIFT, signals,
            f"Level 2: todo_satisfaction={s1:.2f}>=1.0 AND affects_paths_present=True -> COMPLETED_BY_DRIFT",
        )
    if s5 or not s3:
        return ClassificationResult(
            DRIFTED, signals,
            f"Level 3: successor_present={s5} OR plan_anchors_live={s3} (NOT live) -> DRIFTED",
        )
    return ClassificationResult(
        STILL_ACCURATE, signals,
        f"Default: goal_endorsed=True, todo={s1:.2f}<1.0, no successor, anchors live -> STILL_ACCURATE",
    )
