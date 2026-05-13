"""Tests for tools/maintenance/adr-trigger-audit.py.

Spec anchors:
    decisions/0008-narrative-skills-status-quo.md F1-F5.
    decisions/0009-root-spec-no-consolidation.md F1-F3.

The audit must:
  1. Classify each of the eight triggers correctly (mechanical / semi-mechanical / manual).
  2. Compose tools/maintenance/bundle-size-snapshot.py (never duplicate its logic).
  3. Emit canonical <path>::<level>:<code>:<msg> diagnostics.
  4. Exit 0 on no fires, 2 on advisory fires, 1 on usage error.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO / "tools" / "maintenance" / "adr-trigger-audit.py"
BUNDLE_MODULE_PATH = REPO / "tools" / "maintenance" / "bundle-size-snapshot.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("adr_trigger_audit", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def audit():
    return _load_module()


def _seed_bundle(repo: Path, per_spec_chars: int = 4_400) -> None:
    """Materialise the 11 root specs at synthetic sizes.

    Default 4,400 chars/spec → ~1,100 tokens/spec, just over the ADR-0009 F2
    `tokens < 1000` floor, so PRE_COMMIT.md / FRUSTRATED.md don't accidentally
    fire F2 during clean-state tests. Tests that target F1/F2 deliberately
    pass a different size.
    """
    spec = importlib.util.spec_from_file_location("bundle_size_snapshot", BUNDLE_MODULE_PATH)
    bss = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bss)
    for rel in bss.BUNDLE_SPECS:
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x" * per_spec_chars, encoding="utf-8")


def _seed_friction_log(
    repo: Path,
    task_slug: str,
    body: str,
    *,
    mtime_offset_days: int = 0,
) -> Path:
    """Drop a tasks/<slug>/friction-log.md with controllable mtime."""
    task_dir = repo / "tasks" / task_slug
    task_dir.mkdir(parents=True, exist_ok=True)
    log = task_dir / "friction-log.md"
    log.write_text(body, encoding="utf-8")
    if mtime_offset_days:
        target = (dt.datetime.now() - dt.timedelta(days=mtime_offset_days)).timestamp()
        import os
        os.utime(log, (target, target))
    return log


def test_mechanical_clean_no_triggers_fire(audit, tmp_path):
    """All thresholds satisfied → every mechanical trigger is `ok`.

    Synthetic specs must be large enough to clear ADR-0009 F2's 1000-token
    floor (PRE_COMMIT.md / FRUSTRATED.md). Default 4,400-char seed yields
    ~1,100 tokens per spec.
    """
    _seed_bundle(tmp_path)
    (tmp_path / "skills").mkdir()
    (tmp_path / "skills" / "dramatica-theory").mkdir()
    (tmp_path / "skills" / "ncp-author").mkdir()
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report["any_fired"] is False, (
        f"unexpected fires: "
        f"{[k for k, r in report['results'].items() if r['fired']]}"
    )
    for key in ("ADR-0008.F1", "ADR-0008.F2", "ADR-0009.F1", "ADR-0009.F2"):
        assert report["results"][key]["fired"] is False, f"{key} unexpectedly fired"


def test_mechanical_fires_adr0008_f1_skill_count(audit, tmp_path):
    """11 narrative skills (> 10 threshold) MUST fire ADR-0008 F1."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    # 11 narrative directories (1 dramatica + 1 ncp + 9 novel-architect-*)
    (skills_dir / "dramatica-theory").mkdir()
    (skills_dir / "ncp-author").mkdir()
    for i in range(9):
        (skills_dir / f"novel-architect-x{i}").mkdir()
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f1 = report["results"]["ADR-0008.F1"]
    assert f1["fired"] is True
    assert f1["level"] == "WARN"
    assert "count=11" in f1["msg"]
    assert report["any_fired"] is True


def test_mechanical_fires_adr0009_f1_bundle_tokens(audit, tmp_path):
    """Bundle ≥ 100,000 tokens MUST fire ADR-0009 F1."""
    # 110K tokens × 4 chars / 11 specs ≈ 40,000 chars each → cross threshold.
    _seed_bundle(tmp_path, per_spec_chars=40_000)
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f1 = report["results"]["ADR-0009.F1"]
    assert f1["fired"] is True
    assert report["bundle_tokens"] >= audit.ADR_0009_F1_BUNDLE_TOKEN_THRESHOLD
    # ADR-0008 F2 (60K threshold) ALSO fires since the bundle blew past it.
    assert report["results"]["ADR-0008.F2"]["fired"] is True


def test_mechanical_fires_adr0009_f2_short_spec_low_deps(audit, tmp_path):
    """FRUSTRATED.md < 1000 tokens AND < 50 dependents MUST fire ADR-0009 F2."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    # 100 chars / spec → ~25 tokens, well below the 1000-token floor.
    # No inbound refs in tmp_path → 0 dependents.
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f2 = report["results"]["ADR-0009.F2"]
    assert f2["fired"] is True
    assert "FRUSTRATED.md" in f2["msg"]


def test_semi_mechanical_friction_aggregation_fires(audit, tmp_path):
    """Three FL1+ friction logs citing NO.5 in the window MUST fire ADR-0008 F3."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    today = dt.date(2026, 5, 13)
    for i, slug in enumerate(["070-a", "071-b", "072-c"]):
        _seed_friction_log(
            tmp_path,
            slug,
            f"# Friction\n\nHighest Frustration Level: FL2\n\nThe NO.5 workaround is awkward (run {i}).\n",
            mtime_offset_days=i,
        )
    report = audit.run_audit(tmp_path, today=today, window_days=14)
    f3 = report["results"]["ADR-0008.F3"]
    assert f3["fired"] is True
    assert "sessions in last 14d = 3" in f3["msg"]


def test_semi_mechanical_friction_outside_window_does_not_fire(audit, tmp_path):
    """Logs older than window_days MUST NOT contribute to the count."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    today = dt.date(2026, 5, 13)
    for i, slug in enumerate(["073-a", "074-b", "075-c"]):
        _seed_friction_log(
            tmp_path,
            slug,
            f"Highest Frustration Level: FL2\nNO.5 trouble (run {i})",
            mtime_offset_days=30,
        )
    report = audit.run_audit(tmp_path, today=today, window_days=14)
    assert report["results"]["ADR-0008.F3"]["fired"] is False


def test_manual_trigger_is_reported_but_does_not_fire(audit, tmp_path):
    """ADR-0008 F5 (third-party adopter) MUST be reported as MANUAL, never as fired."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f5 = report["results"]["ADR-0008.F5"]
    assert f5.get("manual") is True
    assert f5["fired"] is False
    assert f5["level"] == "INFO"


def test_exit_code_matrix(audit, tmp_path, capsys):
    """Exit codes: 0=no fires; 2=at least one fire; 1=usage error (handled separately)."""
    _seed_bundle(tmp_path)
    # Clean repo, no fires → exit 0.
    code_clean = audit.main([
        "--format", "json",
        "--repo-root", str(tmp_path),
    ])
    capsys.readouterr()
    assert code_clean == 0

    # Trigger ADR-0008 F1 by adding 11 narrative skill dirs.
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir(exist_ok=True)
    for i in range(11):
        (skills_dir / f"dramatica-flavor-{i}").mkdir()
    code_fire = audit.main([
        "--format", "json",
        "--repo-root", str(tmp_path),
    ])
    capsys.readouterr()
    assert code_fire == 2


def test_diagnostic_lines_use_canonical_format(audit, tmp_path, capsys):
    """Every diagnostic line MUST follow <path>::<level>:<code>:<msg>."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    audit.main(["--format", "text", "--repo-root", str(tmp_path)])
    captured = capsys.readouterr()
    diag_lines = [
        ln for ln in captured.out.splitlines()
        if ln.startswith("decisions/")
    ]
    assert len(diag_lines) == 8, "MUST emit exactly 8 trigger lines (5 + 3)"
    for ln in diag_lines:
        # path::level:code:msg
        path, rest = ln.split("::", 1)
        level, code, msg = rest.split(":", 2)
        assert path.endswith(".md")
        assert level in {"INFO", "WARN"}
        assert code.startswith("ADR-000")
        assert msg.strip() != ""


def test_runlog_projection_is_single_line(audit, tmp_path, capsys):
    """--format runlog MUST be a single line and tag any fired codes."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    audit.main(["--format", "runlog", "--repo-root", str(tmp_path)])
    captured = capsys.readouterr()
    line = captured.out.rstrip("\n")
    assert "\n" not in line
    assert "adr-trigger-audit" in line
    assert "8 triggers" in line


def test_main_usage_error_window_days(audit, tmp_path):
    """--window-days outside [1, 365] MUST exit 1 (usage error)."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    assert audit.main([
        "--window-days", "0",
        "--repo-root", str(tmp_path),
    ]) == 1
    assert audit.main([
        "--window-days", "999",
        "--repo-root", str(tmp_path),
    ]) == 1


def test_json_format_is_valid_and_complete(audit, tmp_path, capsys):
    """--format json MUST emit parseable JSON with all 8 trigger keys."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    audit.main(["--format", "json", "--repo-root", str(tmp_path)])
    parsed = json.loads(capsys.readouterr().out)
    assert set(parsed["results"].keys()) == {
        "ADR-0008.F1", "ADR-0008.F2", "ADR-0008.F3", "ADR-0008.F4", "ADR-0008.F5",
        "ADR-0009.F1", "ADR-0009.F2", "ADR-0009.F3",
    }
    assert parsed["window_days"] == audit.FRICTION_WINDOW_DAYS_DEFAULT


def test_composes_bundle_size_snapshot_does_not_duplicate(audit, tmp_path):
    """The audit MUST call bundle-size-snapshot.measure_bundle, not reimplement it."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    bss = audit._load_bundle_module(tmp_path)
    direct = bss.measure_bundle(tmp_path, include_dependents=True)
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report["bundle_tokens"] == direct["total_tokens"]
    assert report["bundle_specs_measured"] == direct["specs_measured"]


def test_discover_repo_root_prefers_git_toplevel(audit, tmp_path, monkeypatch):
    """`--repo-root` auto-discovery MUST prefer `git rev-parse --show-toplevel`
    over the first ancestor with an AGENTS.md, because fixture AGENTS.md files
    (e.g. tests/integration/fixtures/seed/AGENTS.md) would otherwise bind the
    audit to a nested subtree and fail with IncompleteBundleError."""
    import subprocess as _sp

    # Real repo root (has 11 bundle specs).
    repo_root = tmp_path / "agency"
    repo_root.mkdir()
    _seed_bundle(repo_root, per_spec_chars=100)
    # Nested fixture root with its own AGENTS.md but no real bundle.
    fixture_root = repo_root / "tests" / "integration" / "fixtures" / "seed"
    fixture_root.mkdir(parents=True)
    (fixture_root / "AGENTS.md").write_text("fixture stub", encoding="utf-8")
    # `git rev-parse --show-toplevel` returns the real repo root regardless
    # of cwd within the worktree.
    _sp.run(["git", "init", "-q"], cwd=repo_root, check=True)
    found = audit._discover_repo_root(fixture_root)
    assert found == repo_root


def test_discover_repo_root_falls_back_to_marker_walk(audit, tmp_path, monkeypatch):
    """If `git` isn't reachable, ancestor-walk fallback still locates AGENTS.md."""
    import subprocess as _sp

    repo_root = tmp_path / "agency"
    repo_root.mkdir()
    (repo_root / "AGENTS.md").write_text("real root", encoding="utf-8")
    nested = repo_root / "tasks" / "099-x"
    nested.mkdir(parents=True)

    def _no_git(*_args, **_kwargs):
        raise OSError("git not installed")

    monkeypatch.setattr(_sp, "run", _no_git)
    monkeypatch.setattr(audit, "subprocess", _sp, raising=False)
    found = audit._discover_repo_root(nested)
    assert found == repo_root


def test_fl_detector_uses_highest_across_all_matches(audit, tmp_path):
    """A log with FL0 followed by FL2 MUST report FL2 (highest), not FL0
    (first match). Previously _detect_fl_level used .search() per pattern
    and stopped at the first hit."""
    body = (
        "## Frustration Log\n\n"
        "**FL0** — early checkpoint, plan held.\n"
        "**FL2** — later, NO.5 friction surfaced.\n"
    )
    fm = "---\nupdated: 2026-05-13\n---\n\n"
    level = audit._detect_fl_level(fm + body)
    assert level == 2


def test_f4_accepts_inline_yaml_list(audit, tmp_path):
    """`task_affects_paths: [a, b]` inline form MUST be parsed equivalently
    to the block form."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "106-inline-list"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths: [skills/novel-architect/SKILL.md, MAINTENANCE.md]\n"
        "---\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f4 = report["results"]["ADR-0008.F4"]
    assert f4["fired"] is True
    assert "MAINTENANCE.md" in f4["msg"]


def test_f4_handles_non_contiguous_block_list(audit, tmp_path):
    """Block list entries separated by blank lines or YAML comments MUST
    still be picked up — previously the contiguous-run regex bailed."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "107-non-contiguous"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/SKILL.md\n"
        "  # documented carve-out for the §3.6 wiring\n"
        "\n"
        "  - MAINTENANCE.md\n"
        "task_owner: claude\n"
        "---\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f4 = report["results"]["ADR-0008.F4"]
    assert f4["fired"] is True
    assert "MAINTENANCE.md" in f4["msg"]


def test_count_dependents_rejects_hyphen_suffix(audit, tmp_path):
    """`PRE_COMMIT.md-§2` MUST NOT count as an inbound reference."""
    bss_spec = importlib.util.spec_from_file_location("bundle_size_snapshot", BUNDLE_MODULE_PATH)
    bss = importlib.util.module_from_spec(bss_spec)
    bss_spec.loader.exec_module(bss)
    (tmp_path / "PRE_COMMIT.md").write_text("spec", encoding="utf-8")
    (tmp_path / "prose.md").write_text("see PRE_COMMIT.md-§2 for the rule\n", encoding="utf-8")
    (tmp_path / "link.md").write_text("[gate](PRE_COMMIT.md)\n", encoding="utf-8")
    assert bss.count_dependents(tmp_path, "PRE_COMMIT.md") == 1


def test_incomplete_bundle_raises_and_main_exits_1(audit, tmp_path, capsys):
    """Missing bundle specs MUST hard-fail rather than evaluate F1/F2 on
    undercounted data (sparse checkout, mis-rooted run)."""
    # Don't seed the bundle — measure_bundle reports all 11 specs missing.
    with pytest.raises(audit.IncompleteBundleError):
        audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    code = audit.main(["--repo-root", str(tmp_path), "--format", "json"])
    captured = capsys.readouterr()
    assert code == 1
    assert "incomplete bundle" in captured.err.lower()


def test_fl_parser_recognises_variant_forms(audit, tmp_path):
    """Audit MUST share check-fl-declaration.py's variant grammar so logs
    using `**FL2** — ...` or `## Frustration Level: FL2` are counted."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    today = dt.date(2026, 5, 13)
    variants = [
        ("080-v1", "**FL2** — narrative ontology ergonomics issue"),
        ("081-v2", "## Frustration Level: FL2\n\nNO.5 friction described below."),
        ("082-v3", "- **Friction Level:** FL2 — NO.5 carve-out churn"),
    ]
    for slug, body in variants:
        _seed_friction_log(
            tmp_path,
            slug,
            f"---\nupdated: {today.isoformat()}\n---\n\n{body}\nMentions narrative-ontology\n",
        )
    report = audit.run_audit(tmp_path, today=today, window_days=14)
    assert report["results"]["ADR-0008.F3"]["fired"] is True


def test_f4_strips_yaml_inline_comments(audit, tmp_path):
    """`- MAINTENANCE.md # touched` MUST equal MAINTENANCE.md after parse."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "105-inline-comment"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/SKILL.md\n"
        "  - MAINTENANCE.md  # touched only the §3.6 wiring\n"
        "---\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f4 = report["results"]["ADR-0008.F4"]
    assert f4["fired"] is True
    assert "MAINTENANCE.md" in f4["msg"]


def test_count_dependents_excludes_substring_false_positives(audit, tmp_path):
    """count_dependents MUST not count `PRE_COMMIT.md.bak` or `XPRE_COMMIT.mdY`
    as inbound references to root `PRE_COMMIT.md`."""
    bss_spec = importlib.util.spec_from_file_location("bundle_size_snapshot", BUNDLE_MODULE_PATH)
    bss = importlib.util.module_from_spec(bss_spec)
    bss_spec.loader.exec_module(bss)
    (tmp_path / "PRE_COMMIT.md").write_text("real spec", encoding="utf-8")
    (tmp_path / "noise1.md").write_text("see PRE_COMMIT.md.bak instead\n", encoding="utf-8")
    (tmp_path / "noise2.md").write_text("XPRE_COMMIT.mdY is unrelated\n", encoding="utf-8")
    (tmp_path / "real_ref.md").write_text("[gate](PRE_COMMIT.md)\n", encoding="utf-8")
    assert bss.count_dependents(tmp_path, "PRE_COMMIT.md") == 1


def test_count_dependents_prunes_skip_dirs_without_descent(audit, tmp_path):
    """DEPENDENT_SCAN_SKIP_DIRS MUST be pruned at walk-time, not post-filtered."""
    bss_spec = importlib.util.spec_from_file_location("bundle_size_snapshot", BUNDLE_MODULE_PATH)
    bss = importlib.util.module_from_spec(bss_spec)
    bss_spec.loader.exec_module(bss)
    (tmp_path / "PRE_COMMIT.md").write_text("spec", encoding="utf-8")
    git_dir = tmp_path / ".git" / "deep" / "nested"
    git_dir.mkdir(parents=True)
    # If `.git` were traversed, this file would count as a dependent.
    (git_dir / "log.md").write_text("references PRE_COMMIT.md\n", encoding="utf-8")
    assert bss.count_dependents(tmp_path, "PRE_COMMIT.md") == 0


def test_friction_window_prefers_frontmatter_updated_over_mtime(audit, tmp_path):
    """Session date MUST come from frontmatter `updated:` so clone/checkout
    mtime resets don't make a 30-day-old log look 0-day-old."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    today = dt.date(2026, 5, 13)
    # Three FL1+ logs whose mtime is fresh (today) but whose frontmatter
    # `updated:` is 30 days ago — outside the 14-day window.
    for slug in ("070-a", "071-b", "072-c"):
        log = _seed_friction_log(
            tmp_path,
            slug,
            "---\n"
            "type: note\n"
            "updated: 2026-04-13\n"
            "---\n\n"
            "Highest Frustration Level: FL2\nNO.5 trouble.\n",
            mtime_offset_days=0,
        )
        assert log.exists()
    report = audit.run_audit(tmp_path, today=today, window_days=14)
    assert report["results"]["ADR-0008.F3"]["fired"] is False


def test_friction_window_off_by_one_boundary(audit, tmp_path):
    """`window_days=14` MUST accept exactly 14 calendar dates (today plus 13
    prior), not 15. A log dated today-14 MUST be excluded."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    today = dt.date(2026, 5, 13)
    boundary = today - dt.timedelta(days=14)  # one day too old
    for slug in ("073-a", "074-b", "075-c"):
        _seed_friction_log(
            tmp_path,
            slug,
            f"---\nupdated: {boundary.isoformat()}\n---\n\n"
            "Highest Frustration Level: FL2\nNO.5 trouble.\n",
        )
    report = audit.run_audit(tmp_path, today=today, window_days=14)
    assert report["results"]["ADR-0008.F3"]["fired"] is False


def test_f4_substring_match_does_not_false_fire(audit, tmp_path):
    """Narrative path ending in `README.md` MUST NOT be treated as touching
    the root `README.md`. F4 only fires on exact root-spec entries."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "100-readme-substring"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/README.md\n"
        "---\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report["results"]["ADR-0008.F4"]["fired"] is False


def test_f4_matches_all_narrative_skill_globs(audit, tmp_path):
    """F4 narrative match MUST cover the full NARRATIVE_SKILL_GLOBS set,
    including suno-lyric-writer and the-agency-system-architect."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    for i, narrative_slug in enumerate(("suno-lyric-writer", "the-agency-system-architect")):
        tasks_dir = tmp_path / "tasks" / f"10{i + 1}-narr"
        tasks_dir.mkdir(parents=True)
        (tasks_dir / "task.md").write_text(
            "---\n"
            "type: task\n"
            "task_affects_paths:\n"
            f"  - skills/{narrative_slug}/SKILL.md\n"
            "  - MAINTENANCE.md\n"
            "---\n",
            encoding="utf-8",
        )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    f4 = report["results"]["ADR-0008.F4"]
    assert f4["fired"] is True
    assert "candidates=2" in f4["msg"]


def test_f4_includes_agents_md_as_candidate(audit, tmp_path):
    """ADR-0008 F4 carve-out exempts only the AGENTS.md narrative section,
    not the entire file. AGENTS.md MUST be a candidate root spec; the
    maintainer manually confirms section-scope post-fire."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "104-agents-touch"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/SKILL.md\n"
        "  - AGENTS.md\n"
        "---\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report["results"]["ADR-0008.F4"]["fired"] is True
    assert "AGENTS.md" in report["results"]["ADR-0008.F4"]["msg"]


def test_f4_only_inspects_task_affects_paths_block(audit, tmp_path):
    """F4 MUST NOT fire on prose mentions of root specs — only on task_affects_paths entries."""
    _seed_bundle(tmp_path, per_spec_chars=100)
    tasks_dir = tmp_path / "tasks" / "099-prose-only"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/SKILL.md\n"
        "---\n"
        "\n"
        "Prose references MAINTENANCE.md and PRE_COMMIT.md for context but does NOT mutate them.\n",
        encoding="utf-8",
    )
    report = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report["results"]["ADR-0008.F4"]["fired"] is False

    # Now flip: actually list MAINTENANCE.md in the block.
    (tasks_dir / "task.md").write_text(
        "---\n"
        "type: task\n"
        "task_affects_paths:\n"
        "  - skills/novel-architect/SKILL.md\n"
        "  - MAINTENANCE.md\n"
        "---\n"
        "\n"
        "Real T3 amendment.\n",
        encoding="utf-8",
    )
    report2 = audit.run_audit(tmp_path, today=dt.date(2026, 5, 13))
    assert report2["results"]["ADR-0008.F4"]["fired"] is True
