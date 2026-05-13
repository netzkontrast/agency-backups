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
import fnmatch
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

# Fallback used only if tools/check-fl-declaration.py cannot be loaded.
_FL_LINE_PATTERN_FALLBACK = re.compile(
    r"(?im)^\s*\*{0,2}\s*Highest\s+Frustration\s+Level\s*:\s*\*{0,2}\s*FL[0-3]\b",
)
_FL_TOKEN_RE = re.compile(r"\bFL([0-3])\b")


def _load_fl_patterns() -> tuple[tuple[re.Pattern, ...], object | None]:
    """Reuse tools/check-fl-declaration.py's canonical FL-declaration grammar.

    Falls back to a single-pattern set on import failure so the audit still
    runs in a stripped-down environment. Without this the audit only
    recognised the canonical line and silently undercounted FL1+ sessions
    on any of the 11 other accepted variants.
    """
    candidates = (
        Path(__file__).resolve().parents[1] / "check-fl-declaration.py",
    )
    for path in candidates:
        if not path.is_file():
            continue
        spec = importlib.util.spec_from_file_location("check_fl_declaration", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue
        patterns = getattr(module, "_FL_LINE_PATTERNS", None)
        if patterns:
            return tuple(patterns), module
    return (_FL_LINE_PATTERN_FALLBACK,), None


_FL_LINE_PATTERNS, _FL_CHECK_MODULE = _load_fl_patterns()


def _detect_fl_level(text: str) -> int | None:
    """Return the highest FL[0-3] level declared on a recognised line, or None.

    Strips frontmatter before scanning so `summary: FL0` (variant 10 — the
    malformed surface) does not count as a body declaration.
    """
    if _FL_CHECK_MODULE is not None and hasattr(_FL_CHECK_MODULE, "_strip_frontmatter"):
        body = _FL_CHECK_MODULE._strip_frontmatter(text)
    else:
        body = text
        if body.startswith("---\n"):
            end = body.find("\n---\n", 4)
            if end != -1:
                body = body[end + 5 :]
    highest: int | None = None
    for pattern in _FL_LINE_PATTERNS:
        m = pattern.search(body)
        if m is None:
            continue
        tok = _FL_TOKEN_RE.search(m.group(0))
        if tok is None:
            continue
        level = int(tok.group(1))
        highest = level if highest is None else max(highest, level)
    return highest


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


_FRONTMATTER_BLOCK_RE = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)
_FRONTMATTER_DATE_RE = re.compile(
    r"^(?P<key>updated|created):\s*['\"]?(?P<date>\d{4}-\d{2}-\d{2})['\"]?\s*$",
    re.MULTILINE,
)


def _log_session_date(path: Path, text: str) -> dt.date | None:
    """Stable session date for a friction log.

    Prefer YAML frontmatter `updated:` (then `created:`) over filesystem mtime,
    which gets rewritten by clone/checkout/copy and would let historical logs
    spuriously land inside the friction window on a fresh worktree.
    """
    fm = _FRONTMATTER_BLOCK_RE.match(text)
    if fm is not None:
        keyed: dict[str, str] = {}
        for m in _FRONTMATTER_DATE_RE.finditer(fm.group(1)):
            keyed.setdefault(m.group("key"), m.group("date"))
        for key in ("updated", "created"):
            raw = keyed.get(key)
            if raw is None:
                continue
            try:
                return dt.date.fromisoformat(raw)
            except ValueError:
                continue
    return _file_mtime_date(path)


def _friction_in_window(
    repo_root: Path,
    pattern: re.Pattern,
    window_days: int,
    today: dt.date,
) -> tuple[int, list[str]]:
    """Return (session_count, citing_paths) for FL1+ friction logs that match.

    Window is `window_days` calendar dates inclusive of today (so window_days=14
    accepts [today-13, today]). Session date comes from frontmatter `updated:`
    (preferred) or `created:`; falls back to mtime only if neither is present.
    """
    threshold_date = today - dt.timedelta(days=window_days - 1)
    sessions = 0
    cited: list[str] = []
    for log in _list_friction_logs(repo_root):
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        mdate = _log_session_date(log, text)
        if mdate is None or mdate < threshold_date:
            continue
        fl_level = _detect_fl_level(text)
        if fl_level is None or fl_level < 1:
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
_NON_NEUTRAL_ROOTS: tuple[str, ...] = (
    "AGENTS.md",
    "TASK.md", "PROMPT.md", "RESEARCH.md", "FOLDERS.md",
    "PRE_COMMIT.md", "FRUSTRATED.md", "MAINTENANCE.md", "README.md",
)


_YAML_INLINE_COMMENT_RE = re.compile(r"(?:^|\s)#.*$")


def _parse_affects_paths_entries(block: str) -> list[str]:
    """Pull clean string entries out of a `task_affects_paths:` YAML block.

    Prefers PyYAML for proper YAML semantics (handles quoting, escapes, inline
    comments). Falls back to line slicing + inline-comment stripping if PyYAML
    isn't installed, which preserves stdlib-only usage of this tool while
    still handling the common `- path.md # note` form.
    """
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            parsed = yaml.safe_load("task_affects_paths:\n" + block)
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            items = parsed.get("task_affects_paths") or []
            if isinstance(items, list):
                return [str(item).strip() for item in items if item is not None and str(item).strip()]
    entries: list[str] = []
    for raw in block.splitlines():
        s = raw.strip()
        if not s.startswith("- "):
            continue
        entry = _YAML_INLINE_COMMENT_RE.sub("", s[2:]).strip().strip('"').strip("'")
        if entry:
            entries.append(entry)
    return entries


def _is_narrative_skill_path(entry: str) -> bool:
    """True iff entry is a `skills/<slug>/...` path under a narrative glob."""
    if not entry.startswith("skills/"):
        return False
    parts = entry.split("/", 2)
    if len(parts) < 2 or not parts[1]:
        return False
    return any(fnmatch.fnmatchcase(parts[1], pat) for pat in NARRATIVE_SKILL_GLOBS)


def audit_0008_f4(repo_root: Path) -> dict:
    """ADR-0008 F4 — narrative-tagged Task amends a non-SKILLS root spec.

    Scans only `task_affects_paths:` YAML entries (no substring search over
    the block, no prose). A candidate fires when the entry list contains at
    least one narrative-skill path AND at least one non-neutral root spec.

    Narrative match uses the full NARRATIVE_SKILL_GLOBS set (so suno-lyric-writer
    and the-agency-system-architect are caught alongside dramatica/ncp/novel-*).
    Root-spec match is exact string equality on the entry; substring matches
    like `skills/foo/README.md` ⊃ `README.md` no longer fire.

    AGENTS.md is included as a candidate root: the ADR exempts only the
    AGENTS.md narrative section, not the entire file. Maintainer manually
    confirms (a) T3 vs T1/T2 tier and (b) whether the AGENTS.md edit was
    confined to the narrative carve-out.
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
            entries = _parse_affects_paths_entries(m.group(1))
            if not any(_is_narrative_skill_path(e) for e in entries):
                continue
            roots_touched = [r for r in _NON_NEUTRAL_ROOTS if r in entries]
            if roots_touched:
                candidates.append(f"{task_md.relative_to(repo_root)}->{','.join(roots_touched)}")
    msg = (
        f"candidates={len(candidates)} (requires manual T3-vs-T1/T2 review "
        f"and AGENTS.md narrative-section check); list={';'.join(candidates) or 'none'}"
    )
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


class IncompleteBundleError(RuntimeError):
    """Raised when measure_bundle reports missing specs — refuses to evaluate
    F2/F1 triggers on undercounted data (sparse checkout, mis-rooted run)."""


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
    missing = bundle.get("specs_missing") or []
    if missing:
        raise IncompleteBundleError(
            "adr-trigger-audit: refusing to evaluate triggers on an incomplete "
            f"bundle — measure_bundle reports {len(missing)} missing spec(s): "
            f"{', '.join(missing)}. ADR-0008.F2 / ADR-0009.F1 / ADR-0009.F2 "
            "would be evaluated on undercounted data; resolve the missing "
            "files (or run from the correct repo root) and re-invoke."
        )
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

    try:
        report = run_audit(args.repo_root, window_days=args.window_days)
    except IncompleteBundleError as exc:
        print(f"adr-trigger-audit: ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    elif args.format == "runlog":
        print(format_runlog(report))
    else:
        print(format_text(report))

    return 2 if report["any_fired"] else 0


if __name__ == "__main__":
    sys.exit(main())
