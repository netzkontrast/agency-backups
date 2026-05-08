#!/usr/bin/env python3
"""staleness-audit — mechanise MAINTENANCE.md §3.4 stale-task classification.

Spec anchors:
    MAINTENANCE.md §3.4 (four-bucket symptom table + decision algorithm prose)
    research/spec-staleness-decision-formalization/output/SPEC.md §1
        (deterministic decision tree — authoritative pseudocode)
    research/spec-staleness-decision-formalization/output/SPEC.md §2
        (signal extraction recipes S1..S5)
    research/spec-staleness-decision-formalization/output/SPEC.md §4
        (MAINT_STALE_DAYS configuration mechanism — env-var, default 7)

Surface (per Task 039 ST-3 brief):
    python3 tools/maintenance/staleness-audit.py [--stale-days N]
                                                 [--format {markdown,json}]
                                                 [--today YYYY-MM-DD]
                                                 [--repo-root PATH]
                                                 [PATH ...]

Behaviour:
    Walks every Task whose `task_status` is `open` or `in_progress`. For each
    Task older than the staleness window (default 7 days, configurable via
    MAINT_STALE_DAYS), classifies it into one of:

        still_accurate
        drifted
        completed_by_drift
        no_longer_desirable

    per the §1 decision tree. Emits one diagnostic line per Task in the
    `<path>::<level>:<code>:<msg>` format consumed by
    tools/check-maintenance-bypass.py and the coherence run-log.

Exit codes:
    0 — every audited Task lands in `still_accurate`, OR every Task is
        younger than the staleness window (the audit is a no-op).
    2 — at least one Task lands in {drifted, completed_by_drift,
        no_longer_desirable}; advisory diagnostics emitted.
    1 — usage error (unrecognised --format, malformed --today,
        bad MAINT_STALE_DAYS).

The linter is advisory-tier; `check-governance.sh` swallows exit 2 with
`|| true`. Promotion to gating requires a follow-up Task that resolves any
pre-existing repo drift the linter flags.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

# Reuse the canonical frontmatter library — do NOT duplicate the YAML parser.
_TOOLS = Path(__file__).resolve().parent.parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
_FM = _TOOLS / "fm"
if str(_FM) not in sys.path:
    sys.path.insert(0, str(_FM))

try:
    import _core  # type: ignore  # noqa: E402  (runtime import after sys.path twiddle)
except ImportError:
    print(
        "staleness-audit: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)


# ---- Constants -------------------------------------------------------------

DIAG_PREFIX = "MAINT.STALE"

# §3.4 bucket vocabulary (1:1 with TASK.md §4.7 lifecycle outcomes).
BUCKET_STILL_ACCURATE = "still_accurate"
BUCKET_DRIFTED = "drifted"
BUCKET_COMPLETED_BY_DRIFT = "completed_by_drift"
BUCKET_NO_LONGER_DESIRABLE = "no_longer_desirable"

ALL_BUCKETS = (
    BUCKET_STILL_ACCURATE,
    BUCKET_DRIFTED,
    BUCKET_COMPLETED_BY_DRIFT,
    BUCKET_NO_LONGER_DESIRABLE,
)

# A Task participates in the audit only if its status is one of these.
ACTIVE_TASK_STATUSES = frozenset({"open", "in_progress"})

# The eight root specs S4 walks (per SPEC §2 + AGENTS.md §1).
ROOT_SPECS = (
    "AGENTS.md",
    "TASK.md",
    "PROMPT.md",
    "RESEARCH.md",
    "FOLDERS.md",
    "PRE_COMMIT.md",
    "FRUSTRATED.md",
    "MAINTENANCE.md",
)

# Plan-anchor liveness retired prefixes (per SPEC §2 S3 + MAINTENANCE.md §1.1).
RETIRED_PATH_PREFIXES = ("tools/legacy/",)

# Configuration defaults (per SPEC §4.1).
DEFAULT_STALE_DAYS = 7
MAX_STALE_DAYS = 365  # SPEC §4.2 sanity bound.

# Task-link grep patterns.
_NNN_RE = re.compile(r"^(\d{3})$")
_TASK_DIR_RE = re.compile(r"^(\d{3})-([a-z0-9][a-z0-9-]*)$")
_PLAN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_TODO_TASK_RE = re.compile(r"^\s*[-*]\s+\[(.)\]\s*", re.IGNORECASE)


# ---- Data carriers ---------------------------------------------------------


@dataclass
class TaskRecord:
    """One row in the audit table."""

    task_id: str
    slug: str
    path: Path
    fm: dict
    status: str
    bucket: str = BUCKET_STILL_ACCURATE
    evidence: list[str] = field(default_factory=list)
    age_days: int | None = None
    skipped: bool = False  # True if the staleness gate excluded this Task

    @property
    def folder_label(self) -> str:
        """`<NNN>-<slug>` — the canonical task-folder identifier."""
        return f"{self.task_id}-{self.slug}" if self.task_id and self.slug else self.path.parent.name


@dataclass
class SignalVector:
    """The five signals from SPEC §2; carried alongside the bucket assignment."""

    todo_satisfaction: float
    affects_paths_present: bool
    plan_anchors_live: bool
    goal_endorsed: bool
    successor_present: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "todo_satisfaction": round(self.todo_satisfaction, 4),
            "affects_paths_present": self.affects_paths_present,
            "plan_anchors_live": self.plan_anchors_live,
            "goal_endorsed": self.goal_endorsed,
            "successor_present": self.successor_present,
        }


# ---- Configuration resolution ---------------------------------------------


def resolve_stale_days(cli_value: int | None, env: dict[str, str] | None = None) -> int:
    """Return the resolved MAINT_STALE_DAYS value.

    Precedence: CLI flag > environment > default. Rejects non-positive
    integers and values >365 with `ValueError` (SPEC §4.2).
    """
    env = os.environ if env is None else env
    if cli_value is not None:
        value = cli_value
        source = "--stale-days"
    else:
        raw = env.get("MAINT_STALE_DAYS")
        if raw is None:
            return DEFAULT_STALE_DAYS
        try:
            value = int(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"MAINT_STALE_DAYS must be a positive integer; got {raw!r}"
            ) from exc
        source = "MAINT_STALE_DAYS"
    if value < 1:
        raise ValueError(f"{source} must be ≥ 1; got {value}")
    if value > MAX_STALE_DAYS:
        raise ValueError(
            f"{source} must be ≤ {MAX_STALE_DAYS}; got {value} "
            f"(SPEC §4.2 sanity bound)"
        )
    return value


# ---- Frontmatter helpers --------------------------------------------------


def _parse_iso_date(value: str | None) -> dt.date | None:
    """Tolerant ISO-8601 (`YYYY-MM-DD`) parser. Strips quotes; returns None
    if `value` is empty or malformed."""
    if not value:
        return None
    v = value.strip().strip('"').strip("'")
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


# ---- Signal extractors (SPEC §2) ------------------------------------------


def signal_todo_satisfaction(text: str) -> float:
    """S1 — Parse `## Todo` checkbox lines; return checked / total in [0, 1].

    Default under ambiguity (no `## Todo` section, or section has zero
    checkbox items): 0.0 (per SPEC §2 "Defaults under ambiguity").
    """
    todo_bodies = _core.find_all_section_bodies(text, "Todo")
    if not todo_bodies:
        return 0.0
    body = todo_bodies[0]
    total = 0
    checked = 0
    for raw in body.splitlines():
        m = _TODO_TASK_RE.match(raw)
        if not m:
            continue
        total += 1
        marker = m.group(1).lower()
        if marker == "x":
            checked += 1
    if total == 0:
        return 0.0
    return checked / total


def signal_affects_paths_present(
    affects: list[str], repo_root: Path
) -> bool:
    """S2 — Logical AND over `task_affects_paths`: True iff every path exists.

    Default under ambiguity (`task_affects_paths` is `[]` or missing): False.
    """
    if not affects:
        return False
    for rel in affects:
        target = repo_root / rel
        if not target.exists():
            return False
        if target.is_dir():
            # SPEC §2 S2: "non-empty dir" — match the SPEC's contract.
            if not any(target.iterdir()):
                return False
    return True


def signal_plan_anchors_live(text: str, repo_root: Path) -> bool:
    """S3 — Every relative-Markdown link target in `## Plan` resolves AND none
    points under tools/legacy/ or any path tagged "retired".

    Default under ambiguity (Plan section absent OR has zero links): True
    (per SPEC §2 "Defaults under ambiguity").
    """
    plan_bodies = _core.find_all_section_bodies(text, "Plan")
    if not plan_bodies:
        return True
    body = plan_bodies[0]
    targets = _PLAN_LINK_RE.findall(body)
    if not targets:
        return True
    for raw in targets:
        # Strip URL fragments + drop URL-encoded query strings.
        url = raw.split("#", 1)[0].split("?", 1)[0].strip()
        if not url:
            continue
        # Skip absolute / external URLs — only file targets count for liveness.
        if url.startswith(("http://", "https://", "mailto:")):
            continue
        # Resolve relative paths from the task.md's directory; fall through to
        # repo-root when leading slashes are used.
        if url.startswith("/"):
            candidate = (repo_root / url.lstrip("/")).resolve()
        else:
            # Plan links live in task.md whose directory we don't have here;
            # callers pass `repo_root / 'tasks' / '<NNN>-<slug>'` via
            # _resolve_plan_target. To stay self-contained we accept either
            # repo-root-relative or task-folder-relative forms — most plan
            # links use `../../<spec>` form to traverse up to repo root.
            candidate = url  # type: ignore[assignment]
        # Defer the actual existence check to `_resolve_plan_target` since
        # the path semantics depend on the task folder.
        # ⚠ This branch is exercised by `_check_plan_links` below; we never
        # reach here with `candidate` as a string in production.
        return False
    return True


def _resolve_plan_links(text: str, task_dir: Path, repo_root: Path) -> tuple[list[Path], list[str]]:
    """Return (resolved_paths, retired_url_strings) for the Plan section.

    `resolved_paths` is the set of Path objects every plan link points to,
    with task-folder-relative resolution. `retired_url_strings` is the set
    of plan-link URLs whose resolved path lives under a `RETIRED_PATH_PREFIXES`
    entry. External URLs are skipped (not counted for liveness).
    """
    plan_bodies = _core.find_all_section_bodies(text, "Plan")
    if not plan_bodies:
        return [], []
    targets = _PLAN_LINK_RE.findall(plan_bodies[0])
    paths: list[Path] = []
    retired: list[str] = []
    for raw in targets:
        url = raw.split("#", 1)[0].split("?", 1)[0].strip()
        if not url:
            continue
        if url.startswith(("http://", "https://", "mailto:")):
            continue
        if url.startswith("/"):
            candidate = (repo_root / url.lstrip("/")).resolve()
        else:
            candidate = (task_dir / url).resolve()
        # Determine repo-relative form for retired-prefix check.
        try:
            rel = candidate.relative_to(repo_root.resolve())
        except ValueError:
            rel = candidate
        rel_str = str(rel).replace(os.sep, "/")
        if any(rel_str.startswith(prefix) for prefix in RETIRED_PATH_PREFIXES):
            retired.append(url)
        paths.append(candidate)
    return paths, retired


def _check_plan_links(text: str, task_dir: Path, repo_root: Path) -> tuple[bool, list[str]]:
    """S3 (proper). Return `(live, retired_urls)`.

    `live` is True iff every plan link resolves on disk AND none lives under
    a retired prefix. Plan section absent / zero file links => live = True.
    """
    paths, retired = _resolve_plan_links(text, task_dir, repo_root)
    if not paths:
        return True, []
    if retired:
        return False, retired
    for p in paths:
        if not p.exists():
            return False, []
    return True, []


def signal_goal_endorsed(
    task_id: str, slug: str, affects: list[str], repo_root: Path
) -> bool:
    """S4 — At least one current root spec mentions either the Task's
    `<NNN>-<slug>` OR any of its `task_affects_paths` entries.

    Implementation walks the eight root specs and substring-matches; this is
    behaviour-equivalent to the SPEC's `git grep -l` recipe over the same
    file set, but avoids forking `git` (so the linter remains pure Python).

    Default under ambiguity: False (refuses to claim endorsement absent
    evidence).
    """
    if not (task_id or slug or affects):
        return False
    needles: list[str] = []
    if task_id and slug:
        needles.append(f"{task_id}-{slug}")
    if slug:
        needles.append(slug)
    needles.extend(p for p in affects if p)
    if not needles:
        return False
    for spec in ROOT_SPECS:
        path = repo_root / spec
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for needle in needles:
            if needle and needle in text:
                return True
    return False


def signal_successor_present(
    task_id: str, fm: dict, all_task_paths: Iterable[Path]
) -> tuple[bool, list[str]]:
    """S5 — `task_superseded_by` non-empty OR another open task lists this
    task in its `task_supersedes` array.

    Returns `(present, evidence_list)` so the audit can record the supersession
    chain in the diagnostic.

    Default under ambiguity: False.
    """
    evidence: list[str] = []
    superseded_by = _core.str_list(fm, "task_superseded_by")
    if superseded_by:
        evidence.append(f"task_superseded_by={superseded_by}")
    if task_id:
        for other in all_task_paths:
            try:
                other_fm = _core.read_fm(other)
            except OSError:
                continue
            other_id = _core.str_val(other_fm, "task_id")
            if not other_id or other_id == task_id:
                continue
            supersedes = _core.str_list(other_fm, "task_supersedes")
            # Match either bare `<NNN>` or `<NNN>-<slug>`.
            for entry in supersedes:
                bare = entry.split("-", 1)[0]
                if bare == task_id:
                    evidence.append(
                        f"{other_id} task_supersedes lists {task_id}"
                    )
                    break
    return bool(evidence), evidence


# ---- Decision tree (SPEC §1) ----------------------------------------------


def classify(
    record: TaskRecord,
    signals: SignalVector,
) -> str:
    """Apply SPEC §1 decision tree. Returns a bucket name.

    Levels:
        L1 — Goal endorsement → NO_LONGER_DESIRABLE if not endorsed.
        L2 — Completion-by-drift → COMPLETED_BY_DRIFT if Todo 100% AND
             affects-paths-present.
        L3 — Drift vs still-accurate → DRIFTED if successor present OR plan
             anchors retired.
        Default → STILL_ACCURATE.
    """
    if not signals.goal_endorsed:
        return BUCKET_NO_LONGER_DESIRABLE
    if signals.todo_satisfaction >= 1.0 and signals.affects_paths_present:
        return BUCKET_COMPLETED_BY_DRIFT
    if signals.successor_present or not signals.plan_anchors_live:
        return BUCKET_DRIFTED
    return BUCKET_STILL_ACCURATE


# ---- Audit driver ---------------------------------------------------------


def _iter_task_files(tasks_root: Path) -> list[Path]:
    """Yield every `tasks/<NNN>-<slug>/task.md` directly under `tasks_root`."""
    if not tasks_root.is_dir():
        return []
    out: list[Path] = []
    for child in sorted(tasks_root.iterdir()):
        if not child.is_dir():
            continue
        if not _TASK_DIR_RE.match(child.name):
            continue
        task_md = child / "task.md"
        if task_md.is_file():
            out.append(task_md)
    return out


def _audit_one(
    task_md: Path,
    today: dt.date,
    stale_days: int,
    repo_root: Path,
    all_task_paths: list[Path],
) -> tuple[TaskRecord, SignalVector | None]:
    """Audit one Task. Returns (record, signal_vector_or_None).

    `signal_vector_or_None` is None when the staleness gate excluded the Task
    (i.e. it is younger than `stale_days`). In that case `record.skipped` is
    True and `record.bucket` is `still_accurate` (the SPEC's gate-default).
    """
    text = task_md.read_text(encoding="utf-8", errors="replace")
    fm = _core.parse_frontmatter(text, strict=False)

    task_id = _core.str_val(fm, "task_id")
    slug = _core.str_val(fm, "slug")
    status = _core.str_val(fm, "task_status") or "unknown"

    record = TaskRecord(
        task_id=task_id,
        slug=slug,
        path=task_md,
        fm=fm,
        status=status,
    )

    created = _parse_iso_date(_core.str_val(fm, "created"))
    if created is not None:
        record.age_days = (today - created).days
        if record.age_days <= stale_days:
            record.skipped = True
            record.bucket = BUCKET_STILL_ACCURATE
            record.evidence.append(
                f"age={record.age_days}d ≤ stale_days={stale_days} "
                f"(within audit window — gate skip)"
            )
            return record, None

    affects = _core.str_list(fm, "task_affects_paths")

    s1 = signal_todo_satisfaction(text)
    s2 = signal_affects_paths_present(affects, repo_root)
    s3, retired = _check_plan_links(text, task_md.parent, repo_root)
    s4 = signal_goal_endorsed(task_id, slug, affects, repo_root)
    s5, succ_evidence = signal_successor_present(task_id, fm, all_task_paths)

    signals = SignalVector(
        todo_satisfaction=s1,
        affects_paths_present=s2,
        plan_anchors_live=s3,
        goal_endorsed=s4,
        successor_present=s5,
    )

    record.bucket = classify(record, signals)

    # Build human-readable evidence.
    record.evidence.append(f"S1 todo_satisfaction={s1:.2f}")
    record.evidence.append(f"S2 affects_paths_present={s2}")
    if not s3 and retired:
        record.evidence.append(
            f"S3 plan_anchors_live=False retired={retired}"
        )
    else:
        record.evidence.append(f"S3 plan_anchors_live={s3}")
    record.evidence.append(f"S4 goal_endorsed={s4}")
    if s5:
        record.evidence.append(
            f"S5 successor_present=True ({'; '.join(succ_evidence)})"
        )
    else:
        record.evidence.append("S5 successor_present=False")
    if record.age_days is not None:
        record.evidence.append(f"age={record.age_days}d")

    return record, signals


def audit_tasks(
    repo_root: Path,
    today: dt.date,
    stale_days: int,
    tasks_root: Path | None = None,
) -> list[tuple[TaskRecord, SignalVector | None]]:
    """Run the full audit. Returns one (record, signals) tuple per Task with
    `task_status` ∈ ACTIVE_TASK_STATUSES."""
    tasks_root = tasks_root or (repo_root / "tasks")
    candidates = _iter_task_files(tasks_root)
    # Drop closed tasks from the audited corpus.
    audited: list[Path] = []
    for path in candidates:
        fm = _core.read_fm(path)
        status = _core.str_val(fm, "task_status")
        if status in ACTIVE_TASK_STATUSES:
            audited.append(path)
    out: list[tuple[TaskRecord, SignalVector | None]] = []
    for task_md in audited:
        record, signals = _audit_one(
            task_md, today, stale_days, repo_root, candidates
        )
        out.append((record, signals))
    return out


# ---- Output formatting ----------------------------------------------------


def render_diagnostic(record: TaskRecord) -> str:
    """Render one `<path>::<level>:<code>:<msg>` line for the run-log /
    coherence consumers."""
    rel = record.path
    level = "WARN" if record.bucket != BUCKET_STILL_ACCURATE else "INFO"
    code = f"{DIAG_PREFIX}.{record.bucket.upper()}"
    evidence = "; ".join(record.evidence) if record.evidence else "(no signals)"
    return f"{rel}::{level}:{code}:{evidence}"


def render_markdown(
    records: list[tuple[TaskRecord, SignalVector | None]],
    today: dt.date,
    stale_days: int,
) -> str:
    """Render the audit table as a markdown report."""
    lines: list[str] = []
    lines.append(f"# Stale-Task Audit — {today.isoformat()}")
    lines.append("")
    lines.append(
        f"`MAINT_STALE_DAYS={stale_days}`. "
        f"Audited {len(records)} active task(s); "
        f"non-`still_accurate` outcomes per `MAINTENANCE.md §3.4`."
    )
    lines.append("")
    lines.append("| task_id | status | bucket | evidence |")
    lines.append("|---|---|---|---|")
    for record, _ in records:
        ev = "; ".join(record.evidence)
        # Pipe-escape for markdown table.
        ev = ev.replace("|", "\\|")
        lines.append(
            f"| `{record.task_id or '???'}` "
            f"| `{record.status}` "
            f"| `{record.bucket}` "
            f"| {ev} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json(
    records: list[tuple[TaskRecord, SignalVector | None]],
    today: dt.date,
    stale_days: int,
) -> str:
    payload = {
        "today": today.isoformat(),
        "maint_stale_days": stale_days,
        "task_count": len(records),
        "tasks": [
            {
                "task_id": rec.task_id,
                "slug": rec.slug,
                "path": str(rec.path),
                "status": rec.status,
                "bucket": rec.bucket,
                "skipped_by_gate": rec.skipped,
                "age_days": rec.age_days,
                "signals": (sig.as_dict() if sig is not None else None),
                "evidence": rec.evidence,
            }
            for rec, sig in records
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


# ---- CLI ------------------------------------------------------------------


def _parse_today(value: str | None, today_default: dt.date) -> dt.date:
    if value is None:
        return today_default
    parsed = _parse_iso_date(value)
    if parsed is None:
        raise ValueError(
            f"--today must be YYYY-MM-DD; got {value!r}"
        )
    return parsed


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="staleness-audit",
        description=(
            "Mechanise MAINTENANCE.md §3.4: classify each open Task into one "
            "of {still_accurate, drifted, completed_by_drift, "
            "no_longer_desirable} per the deterministic decision tree in "
            "research/spec-staleness-decision-formalization/output/SPEC.md §1."
        ),
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=None,
        help=(
            "Override MAINT_STALE_DAYS for this run. "
            f"Default: {DEFAULT_STALE_DAYS} days."
        ),
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "diagnostic"),
        default="diagnostic",
        help=(
            "Output shape. `diagnostic` (default) emits one "
            "`<path>::<level>:<code>:<msg>` line per Task for "
            "tools/check-maintenance-bypass.py consumption. `markdown` "
            "renders a human-readable table. `json` emits structured "
            "records for downstream tooling."
        ),
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Pin the audit clock (ISO-8601 YYYY-MM-DD). Default: today.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Default: walk upward from CWD looking for AGENTS.md.",
    )
    parser.add_argument(
        "tasks_root",
        nargs="?",
        type=Path,
        default=None,
        help="Optional explicit `tasks/` directory. Default: <repo-root>/tasks.",
    )
    args = parser.parse_args(argv)

    try:
        stale_days = resolve_stale_days(args.stale_days)
    except ValueError as exc:
        print(f"staleness-audit: {exc}", file=sys.stderr)
        return 1

    try:
        today = _parse_today(args.today, dt.date.today())
    except ValueError as exc:
        print(f"staleness-audit: {exc}", file=sys.stderr)
        return 1

    repo_root = (args.repo_root or _core.repo_root_from_cwd()).resolve()
    tasks_root = args.tasks_root.resolve() if args.tasks_root else None

    print(
        f"staleness-audit: MAINT_STALE_DAYS={stale_days} today={today.isoformat()} "
        f"repo_root={repo_root}",
        file=sys.stderr,
    )

    records = audit_tasks(
        repo_root=repo_root,
        today=today,
        stale_days=stale_days,
        tasks_root=tasks_root,
    )

    if args.format == "markdown":
        print(render_markdown(records, today, stale_days))
    elif args.format == "json":
        print(render_json(records, today, stale_days))
    else:  # diagnostic
        for record, _ in records:
            # Suppress gate-skipped Tasks in diagnostic mode — they're not
            # audit candidates and would only add noise to the run-log.
            if record.skipped:
                continue
            print(render_diagnostic(record))

    # Exit code semantics:
    #   0 — every audited Task is still_accurate (or every Task is gate-skipped).
    #   2 — at least one Task lands in a non-still_accurate bucket.
    flagged = sum(
        1
        for rec, _ in records
        if (not rec.skipped) and rec.bucket != BUCKET_STILL_ACCURATE
    )
    audited = sum(1 for rec, _ in records if not rec.skipped)
    print(
        f"staleness-audit: {flagged} flagged, "
        f"{audited - flagged} still_accurate, "
        f"{len(records) - audited} gate-skipped "
        f"(of {len(records)} active task(s)).",
        file=sys.stderr,
    )
    return 2 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
