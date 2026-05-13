#!/usr/bin/env python3
"""adr-trigger-audit — measure the ADR-0008 / ADR-0009 falsifier triggers.

Spec anchors:
    decisions/0008-narrative-skills-status-quo.md §"Falsifier triggers" F1-F5.
    decisions/0009-root-spec-no-consolidation.md §"Falsifier triggers" F1-F3.

Surface:
    python3 tools/maintenance/adr-trigger-audit.py [--format text|json|runlog]
                                                   [--repo-root PATH]
                                                   [--window-days N]

Behaviour:
    Classifies each of the eight triggers as `mechanical` (computable),
    `semi-mechanical` (computable but aggregates prose), or `manual` (requires
    a human signal). Emits one diagnostic per trigger in canonical
    <path>::<level>:<code>:<msg> form. Composes bundle-size-snapshot.py for
    ADR-0009 F1 and ADR-0008 F2 (overlapping bundle measurement); never
    duplicates its logic.

Exit codes:
    0 — no trigger fired (manual triggers reported as MANUAL, not as a fire).
    1 — usage error.
    2 — at least one mechanical or semi-mechanical trigger fired (advisory).

The audit is part of the Nightly Maintenance Run cadence (MAINTENANCE.md §3.6);
it MUST NOT be wired into the default governance gate.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

# ----- bundle-size-snapshot composition -----

def _load_bundle_module(repo_root: Path):
    """Load bundle-size-snapshot.py as a module.

    Prefers the script colocated with this file (the canonical install path);
    falls back to repo_root/tools/maintenance/ for unusual layouts.
    """
    candidates = (
        Path(__file__).resolve().parent / "bundle-size-snapshot.py",
        repo_root / "tools" / "maintenance" / "bundle-size-snapshot.py",
    )
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("bundle_size_snapshot", path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError(
        f"adr-trigger-audit: cannot locate bundle-size-snapshot.py near {candidates[0]} or {candidates[1]}"
    )


# ----- ADR-0008 trigger thresholds -----

NARRATIVE_SKILL_GLOBS: tuple[str, ...] = (
    "dramatica-*",
    "ncp-*",
    "novel-architect*",
    "suno-lyric-writer",
    "the-agency-system-architect",
)
ADR_0008_F1_SKILL_COUNT_THRESHOLD = 10
ADR_0008_F2_BUNDLE_TOKEN_THRESHOLD = 60_000

# ----- ADR-0009 trigger thresholds -----

ADR_0009_F1_BUNDLE_TOKEN_THRESHOLD = 100_000
ADR_0009_F2_SPECS: tuple[str, ...] = ("PRE_COMMIT.md", "FRUSTRATED.md")
ADR_0009_F2_TOKEN_THRESHOLD = 1_000
ADR_0009_F2_DEPENDENT_THRESHOLD = 50

# ----- shared friction-window threshold (F3/F8) -----

FRICTION_WINDOW_DAYS_DEFAULT = 14
FRICTION_SESSION_THRESHOLD = 3

NARRATIVE_FRICTION_PATTERN = re.compile(r"\bNO\.5\b|narrative[- ]ontology", re.IGNORECASE)
BUNDLE_FRICTION_PATTERN = re.compile(
    r"\bbundle[- ]size\b|root[- ]spec[- ]count|\b11[- ]spec[- ]bundle\b",
    re.IGNORECASE,
)
FL_LINE_PATTERN = re.compile(r"Highest Frustration Level:\s*FL([0-3])", re.IGNORECASE)


# ----- diagnostic helpers -----

def _diag(path: str, level: str, code: str, msg: str) -> str:
    return f"{path}::{level}:{code}:{msg}"


def _ok(code: str, msg: str) -> dict:
    return {"level": "INFO", "code": code, "msg": msg, "fired": False}


def _fire(code: str, msg: str) -> dict:
    return {"level": "WARN", "code": code, "msg": msg, "fired": True}


def _manual(code: str, msg: str) -> dict:
    return {"level": "INFO", "code": code, "msg": msg, "fired": False, "manual": True}


# ----- mechanical predicates -----

def count_narrative_skills(repo_root: Path) -> tuple[int, list[str]]:
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return 0, []
    found: set[str] = set()
    for pattern in NARRATIVE_SKILL_GLOBS:
        for entry in skills_dir.glob(pattern):
            if entry.is_dir():
                found.add(entry.name)
    return len(found), sorted(found)


def audit_0008_f1(repo_root: Path) -> dict:
    n, names = count_narrative_skills(repo_root)
    msg = (
        f"narrative-skill count={n} (threshold>{ADR_0008_F1_SKILL_COUNT_THRESHOLD}); "
        f"skills={','.join(names) or 'none'}"
    )
    return _fire("ADR-0008.F1", msg) if n > ADR_0008_F1_SKILL_COUNT_THRESHOLD else _ok("ADR-0008.F1", msg)


def audit_0008_f2(bundle_snapshot: dict) -> dict:
    tokens = bundle_snapshot["total_tokens"]
    msg = f"bundle-tokens={tokens} (threshold>{ADR_0008_F2_BUNDLE_TOKEN_THRESHOLD})"
    return _fire("ADR-0008.F2", msg) if tokens > ADR_0008_F2_BUNDLE_TOKEN_THRESHOLD else _ok("ADR-0008.F2", msg)


def audit_0009_f1(bundle_snapshot: dict) -> dict:
    tokens = bundle_snapshot["total_tokens"]
    msg = f"bundle-tokens={tokens} (threshold>={ADR_0009_F1_BUNDLE_TOKEN_THRESHOLD})"
    return _fire("ADR-0009.F1", msg) if tokens >= ADR_0009_F1_BUNDLE_TOKEN_THRESHOLD else _ok("ADR-0009.F1", msg)


def audit_0009_f2(bundle_snapshot: dict) -> dict:
    by_path = {rec["path"]: rec for rec in bundle_snapshot["per_spec"]}
    fired_specs: list[str] = []
    details: list[str] = []
    for rel in ADR_0009_F2_SPECS:
        rec = by_path.get(rel)
        if rec is None:
            details.append(f"{rel}=missing")
            continue
        tokens = rec.get("tokens", 0)
        deps = rec.get("dependents", -1)
        details.append(f"{rel}(tokens={tokens},deps={deps})")
        if tokens < ADR_0009_F2_TOKEN_THRESHOLD and 0 <= deps < ADR_0009_F2_DEPENDENT_THRESHOLD:
            fired_specs.append(rel)
    msg = f"{'; '.join(details)} (fire when tokens<{ADR_0009_F2_TOKEN_THRESHOLD} AND deps<{ADR_0009_F2_DEPENDENT_THRESHOLD})"
    if fired_specs:
        return _fire("ADR-0009.F2", f"specs={','.join(fired_specs)} {msg}")
    return _ok("ADR-0009.F2", msg)


# ----- semi-mechanical predicates -----

def _list_friction_logs(repo_root: Path) -> list[Path]:
    out: list[Path] = []
    tasks_dir = repo_root / "tasks"
    if tasks_dir.is_dir():
        out.extend(tasks_dir.glob("*/friction-log.md"))
    research_dir = repo_root / "research"
    if research_dir.is_dir():
        out.extend(research_dir.glob("*/reflection/friction-log.md"))
    return out


def _file_mtime_date(path: Path) -> dt.date | None:
    try:
        return dt.date.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None


def _friction_in_window(
    repo_root: Path,
    pattern: re.Pattern,
    window_days: int,
    today: dt.date,
) -> tuple[int, list[str]]:
    """Return (session_count, citing_paths) for FL1+ friction logs that match.

    A "session" here is one friction-log.md file whose mtime falls inside the
    window AND whose body declares FL1+ AND whose body mentions the pattern.
    """
    threshold_date = today - dt.timedelta(days=window_days)
    sessions = 0
    cited: list[str] = []
    for log in _list_friction_logs(repo_root):
        mdate = _file_mtime_date(log)
        if mdate is None or mdate < threshold_date:
            continue
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fl_match = FL_LINE_PATTERN.search(text)
        if fl_match is None or int(fl_match.group(1)) < 1:
            continue
        if not pattern.search(text):
            continue
        sessions += 1
        cited.append(str(log.relative_to(repo_root)))
    return sessions, cited


def audit_0008_f3(repo_root: Path, window_days: int, today: dt.date) -> dict:
    sessions, cited = _friction_in_window(repo_root, NARRATIVE_FRICTION_PATTERN, window_days, today)
    msg = (
        f"NO.5-cited FL1+ sessions in last {window_days}d = {sessions} "
        f"(threshold>={FRICTION_SESSION_THRESHOLD}); cited={','.join(cited) or 'none'}"
    )
    return _fire("ADR-0008.F3", msg) if sessions >= FRICTION_SESSION_THRESHOLD else _ok("ADR-0008.F3", msg)


def audit_0009_f3(repo_root: Path, window_days: int, today: dt.date) -> dict:
    sessions, cited = _friction_in_window(repo_root, BUNDLE_FRICTION_PATTERN, window_days, today)
    msg = (
        f"bundle-cited FL1+ sessions in last {window_days}d = {sessions} "
        f"(threshold>={FRICTION_SESSION_THRESHOLD}); cited={','.join(cited) or 'none'}"
    )
    return _fire("ADR-0009.F3", msg) if sessions >= FRICTION_SESSION_THRESHOLD else _ok("ADR-0009.F3", msg)


_TASK_AFFECTS_BLOCK_RE = re.compile(
    r"^task_affects_paths:\s*\n((?:[ \t]+-\s.*\n)+)",
    re.MULTILINE,
)
_NARRATIVE_PATH_RE = re.compile(r"skills/(dramatica|ncp|novel)[-\w/]*")
_NON_NEUTRAL_ROOTS: tuple[str, ...] = (
    "TASK.md", "PROMPT.md", "RESEARCH.md", "FOLDERS.md",
    "PRE_COMMIT.md", "FRUSTRATED.md", "MAINTENANCE.md", "README.md",
)


def audit_0008_f4(repo_root: Path) -> dict:
    """ADR-0008 F4 — narrative-tagged Task amends a non-SKILLS root spec.

    Scans only the `task_affects_paths:` YAML block, not arbitrary prose. A
    candidate fires when the block lists at least one narrative path AND at
    least one non-neutral root spec (everything except AGENTS.md/SKILLS.md,
    per the ADR's "other than `SKILLS.md` or the AGENTS.md narrative
    section" carve-out). Manual review still needed to confirm T3 vs T1/T2
    tier; the heuristic flags candidates for inspection.
    """
    tasks_dir = repo_root / "tasks"
    candidates: list[str] = []
    if tasks_dir.is_dir():
        for task_md in tasks_dir.glob("*/task.md"):
            try:
                text = task_md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            m = _TASK_AFFECTS_BLOCK_RE.search(text)
            if m is None:
                continue
            block = m.group(1)
            if not _NARRATIVE_PATH_RE.search(block):
                continue
            roots_touched = [r for r in _NON_NEUTRAL_ROOTS if r in block]
            if roots_touched:
                candidates.append(f"{task_md.relative_to(repo_root)}->{','.join(roots_touched)}")
    msg = f"candidates={len(candidates)} (requires manual T3-vs-T1/T2 review); list={';'.join(candidates) or 'none'}"
    return _fire("ADR-0008.F4", msg) if candidates else _ok("ADR-0008.F4", msg)


# ----- manual predicates -----

def audit_0008_f5() -> dict:
    return _manual(
        "ADR-0008.F5",
        "third-party-adopter blocker — no in-repo signal; maintainer review required",
    )


# ----- audit orchestration -----

TRIGGER_ORDER: tuple[tuple[str, str], ...] = (
    ("decisions/0008-narrative-skills-status-quo.md", "F1"),
    ("decisions/0008-narrative-skills-status-quo.md", "F2"),
    ("decisions/0008-narrative-skills-status-quo.md", "F3"),
    ("decisions/0008-narrative-skills-status-quo.md", "F4"),
    ("decisions/0008-narrative-skills-status-quo.md", "F5"),
    ("decisions/0009-root-spec-no-consolidation.md", "F1"),
    ("decisions/0009-root-spec-no-consolidation.md", "F2"),
    ("decisions/0009-root-spec-no-consolidation.md", "F3"),
)


def run_audit(
    repo_root: Path,
    *,
    window_days: int = FRICTION_WINDOW_DAYS_DEFAULT,
    today: dt.date | None = None,
) -> dict:
    if today is None:
        today = dt.date.today()
    bss = _load_bundle_module(repo_root)
    bundle = bss.measure_bundle(repo_root, include_dependents=True)
    results: dict[str, dict] = {
        "ADR-0008.F1": audit_0008_f1(repo_root),
        "ADR-0008.F2": audit_0008_f2(bundle),
        "ADR-0008.F3": audit_0008_f3(repo_root, window_days, today),
        "ADR-0008.F4": audit_0008_f4(repo_root),
        "ADR-0008.F5": audit_0008_f5(),
        "ADR-0009.F1": audit_0009_f1(bundle),
        "ADR-0009.F2": audit_0009_f2(bundle),
        "ADR-0009.F3": audit_0009_f3(repo_root, window_days, today),
    }
    any_fired = any(r["fired"] for r in results.values())
    return {
        "date": today.isoformat(),
        "window_days": window_days,
        "bundle_tokens": bundle["total_tokens"],
        "bundle_specs_measured": bundle["specs_measured"],
        "any_fired": any_fired,
        "results": results,
    }


# ----- formatters -----

def format_text(report: dict) -> str:
    lines = [
        f"# adr-trigger-audit ({report['date']}; window={report['window_days']}d)",
        f"# bundle: {report['bundle_specs_measured']} specs / ~{report['bundle_tokens']} tokens",
        "",
    ]
    for adr_path, trigger in TRIGGER_ORDER:
        prefix = "ADR-0008" if "0008-" in adr_path else "ADR-0009"
        r = report["results"][f"{prefix}.{trigger}"]
        tag = "MANUAL" if r.get("manual") else ("FIRED" if r["fired"] else "ok")
        lines.append(_diag(adr_path, r["level"], r["code"], f"[{tag}] {r['msg']}"))
    lines.append("")
    lines.append(
        f"# summary: any_fired={report['any_fired']}; manual triggers are reported but do NOT fire automatically"
    )
    return "\n".join(lines)


def format_runlog(report: dict) -> str:
    """One-line projection appendable to maintenance/run-log.md (per Task 069)."""
    fired_codes = [r["code"] for r in report["results"].values() if r["fired"]]
    manual_codes = [r["code"] for r in report["results"].values() if r.get("manual")]
    status = "FIRED:" + ",".join(fired_codes) if fired_codes else "ok"
    return (
        f"{report['date']} | adr-trigger-audit | "
        f"8 triggers / window={report['window_days']}d / "
        f"bundle~{report['bundle_tokens']} tokens | "
        f"{status} | manual={','.join(manual_codes)}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit ADR-0008 / ADR-0009 falsifier triggers; back the Nightly Maintenance Run."
    )
    parser.add_argument("--format", choices=("text", "json", "runlog"), default="text")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(
        "--window-days",
        type=int,
        default=FRICTION_WINDOW_DAYS_DEFAULT,
        help=f"Friction-window for F3/F3-style semi-mechanical triggers (default {FRICTION_WINDOW_DAYS_DEFAULT}).",
    )
    args = parser.parse_args(argv)

    if args.window_days < 1 or args.window_days > 365:
        print(
            f"adr-trigger-audit: ERROR: --window-days must be in [1, 365]; got {args.window_days}",
            file=sys.stderr,
        )
        return 1

    if args.repo_root is None:
        cur = Path.cwd().resolve()
        while cur != cur.parent:
            if (cur / "AGENTS.md").is_file():
                args.repo_root = cur
                break
            cur = cur.parent
        if args.repo_root is None:
            print(
                "adr-trigger-audit: ERROR: could not locate repo root (no AGENTS.md found in ancestors)",
                file=sys.stderr,
            )
            return 1

    report = run_audit(args.repo_root, window_days=args.window_days)

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    elif args.format == "runlog":
        print(format_runlog(report))
    else:
        print(format_text(report))

    return 2 if report["any_fired"] else 0


if __name__ == "__main__":
    sys.exit(main())
