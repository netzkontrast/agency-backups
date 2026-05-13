"""Tests for tools/maintenance/bundle-size-snapshot.py.

Spec anchor: decisions/0009-root-spec-no-consolidation.md F1 trigger.

The bundle-size snapshot must:
  1. Measure every spec in BUNDLE_SPECS that exists on disk.
  2. Detect missing specs (configuration drift) and report them.
  3. Surface the F1 (>= 100,000 tokens) trigger boundary.
  4. Emit a stable one-line runlog projection appendable to maintenance/run-log.md.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO / "tools" / "maintenance" / "bundle-size-snapshot.py"


def _load_module():
    """Load the bundle-size-snapshot module from disk (dashed filename)."""
    spec = importlib.util.spec_from_file_location("bundle_size_snapshot", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def bss():
    return _load_module()


def test_measure_bundle_empty_repo_yields_missing_list(bss, tmp_path):
    """All specs are missing → specs_missing is fully populated."""
    snapshot = bss.measure_bundle(tmp_path)
    assert snapshot["specs_measured"] == 0
    assert set(snapshot["specs_missing"]) == set(bss.BUNDLE_SPECS)
    assert snapshot["total_bytes"] == 0
    assert snapshot["total_tokens"] == 0
    assert snapshot["f1_triggered"] is False


def test_measure_bundle_synthetic_under_threshold(bss, tmp_path):
    """A synthetic small bundle stays under F1 and reports correctly."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x" * 100, encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path)
    assert snapshot["specs_measured"] == len(bss.BUNDLE_SPECS)
    assert snapshot["specs_missing"] == []
    assert snapshot["total_bytes"] == 100 * len(bss.BUNDLE_SPECS)
    assert snapshot["total_tokens"] == (100 * len(bss.BUNDLE_SPECS)) // bss.CHARS_PER_TOKEN
    assert snapshot["f1_triggered"] is False


def test_measure_bundle_synthetic_over_threshold(bss, tmp_path):
    """A synthetic large bundle crosses F1 and flips the trigger."""
    # 100K tokens × 4 chars = 400K chars across 11 specs → ~36,364 chars each.
    per_spec_chars = (bss.F1_THRESHOLD_TOKENS * bss.CHARS_PER_TOKEN // len(bss.BUNDLE_SPECS)) + 100
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x" * per_spec_chars, encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path)
    assert snapshot["f1_triggered"] is True
    assert snapshot["total_tokens"] >= bss.F1_THRESHOLD_TOKENS


def test_measure_bundle_on_real_repo(bss):
    """The on-disk measurement MUST reproduce ADR-0009's recorded baseline shape.

    Exact byte count drifts as specs evolve; the invariants are:
      - All 11 specs measured (no spec missing).
      - Token count is between the ADR baseline (~70K) and the F1 threshold (100K),
        i.e. the bundle has not silently breached F1 without an ADR update.
    """
    snapshot = bss.measure_bundle(REPO)
    assert snapshot["specs_measured"] == len(bss.BUNDLE_SPECS), (
        f"expected all {len(bss.BUNDLE_SPECS)} bundle specs to exist; "
        f"missing={snapshot['specs_missing']}"
    )
    assert 50_000 <= snapshot["total_tokens"] <= bss.F1_THRESHOLD_TOKENS, (
        f"bundle token count {snapshot['total_tokens']} is outside the expected "
        f"[50K, 100K] window — if this is genuine spec growth, file an ADR-0009 "
        f"successor; if not, find what just landed."
    )


def test_runlog_format_is_single_line(bss, tmp_path):
    """runlog projection MUST be a single line for append-to-run-log usage."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("hello", encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path)
    line = bss.format_runlog(snapshot)
    assert "\n" not in line, "runlog projection must be a single line"
    assert "ADR-0009-F1=ok" in line
    assert "11 specs" in line


def test_runlog_format_marks_triggered_state(bss, tmp_path):
    """F1-triggered runs MUST be visibly tagged in the runlog projection."""
    per_spec_chars = (bss.F1_THRESHOLD_TOKENS * bss.CHARS_PER_TOKEN // len(bss.BUNDLE_SPECS)) + 100
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x" * per_spec_chars, encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path)
    line = bss.format_runlog(snapshot)
    assert "ADR-0009-F1=F1-TRIGGERED" in line


def test_main_json_output_is_valid_json(bss, tmp_path, capsys):
    """--format json MUST emit parseable JSON to stdout."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("hi", encoding="utf-8")
    exit_code = bss.main(["--format", "json", "--repo-root", str(tmp_path)])
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["specs_measured"] == len(bss.BUNDLE_SPECS)
    assert exit_code == 0


def test_main_exits_2_when_threshold_crossed(bss, tmp_path):
    """--format runlog MUST exit 2 when the F1 threshold is breached."""
    per_spec_chars = (bss.F1_THRESHOLD_TOKENS * bss.CHARS_PER_TOKEN // len(bss.BUNDLE_SPECS)) + 100
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x" * per_spec_chars, encoding="utf-8")
    exit_code = bss.main(["--format", "runlog", "--repo-root", str(tmp_path)])
    assert exit_code == 2


def test_main_exits_1_on_missing_specs(bss, tmp_path):
    """--format runlog MUST exit 1 if any spec in BUNDLE_SPECS is missing."""
    exit_code = bss.main(["--format", "runlog", "--repo-root", str(tmp_path)])
    assert exit_code == 1


def test_measure_bundle_dependents_off_by_default(bss, tmp_path):
    """`dependents` MUST NOT appear when include_dependents=False (the default)."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("hi", encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path)
    for rec in snapshot["per_spec"]:
        assert "dependents" not in rec


def test_measure_bundle_dependents_counts_inbound_refs(bss, tmp_path):
    """ADR-0009 F2 needs an inbound-reference count per spec basename."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("body", encoding="utf-8")
    # Three files reference PRE_COMMIT.md; one references FRUSTRATED.md.
    (tmp_path / "refs1.md").write_text("see PRE_COMMIT.md", encoding="utf-8")
    (tmp_path / "refs2.md").write_text("[link](./PRE_COMMIT.md)", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "ref.sh").write_text("# PRE_COMMIT.md note", encoding="utf-8")
    (tmp_path / "refs4.md").write_text("FRUSTRATED.md is short", encoding="utf-8")
    snapshot = bss.measure_bundle(tmp_path, include_dependents=True)
    by_path = {rec["path"]: rec for rec in snapshot["per_spec"]}
    assert by_path["PRE_COMMIT.md"]["dependents"] == 3
    assert by_path["FRUSTRATED.md"]["dependents"] == 1
    assert by_path["AGENTS.md"]["dependents"] == 0


def test_count_dependents_skips_excluded_dirs(bss, tmp_path):
    """The dependent scan MUST NOT descend into .git or other excluded trees."""
    (tmp_path / "PRE_COMMIT.md").write_text("body", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "hidden.md").write_text("PRE_COMMIT.md", encoding="utf-8")
    (tmp_path / "real.md").write_text("PRE_COMMIT.md", encoding="utf-8")
    assert bss.count_dependents(tmp_path, "PRE_COMMIT.md") == 1


def test_main_include_dependents_flag(bss, tmp_path, capsys):
    """--include-dependents MUST surface the dependents count via --format json."""
    for rel in bss.BUNDLE_SPECS:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("body", encoding="utf-8")
    (tmp_path / "consumer.md").write_text("AGENTS.md mention", encoding="utf-8")
    exit_code = bss.main([
        "--format", "json",
        "--include-dependents",
        "--repo-root", str(tmp_path),
    ])
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    by_path = {rec["path"]: rec for rec in parsed["per_spec"]}
    assert by_path["AGENTS.md"]["dependents"] == 1
    assert exit_code == 0
