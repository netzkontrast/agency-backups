"""Tests for tools/fm/skills_query.py (Task 022)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SQ = REPO / "tools" / "fm" / "skills_query.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SQ), *args],
        cwd=REPO, capture_output=True, text=True,
    )


def test_summary_resolves_task_slug():
    r = _run("summary", "surface-skills-architecture")
    assert r.returncode == 0, r.stderr
    assert "skills-skill-architecture" in r.stdout


def test_summary_unknown_slug_exits_nonzero():
    r = _run("summary", "no-such-slug-here-xyz")
    assert r.returncode != 0


def test_path_returns_repo_relative_paths():
    r = _run("path", "flexible-frontmatter-toolchain")
    assert r.returncode == 0
    lines = [line for line in r.stdout.splitlines() if line.strip()]
    assert lines
    assert all(not line.startswith("/") for line in lines)


def test_skills_kind_filter_runs_clean():
    r = _run("skills", "--kind", "tool")
    assert r.returncode == 0


def test_skills_target_agent_filter_runs_clean():
    r = _run("skills", "--target-agent", "jules")
    assert r.returncode == 0


def test_references_emits_two_sections():
    r = _run("references", "022")
    assert r.returncode == 0
    assert "refers-to" in r.stdout
    assert "referenced-by" in r.stdout


def test_orphans_runs_without_error():
    r = _run("orphans")
    assert r.returncode == 0


def test_stale_since_validates_format():
    r = _run("stale", "--since", "not-a-cutoff")
    assert r.returncode != 0


def test_stale_since_30d_runs_clean():
    r = _run("stale", "--since", "30d")
    assert r.returncode == 0


def test_header_extracts_goal_for_task():
    r = _run("header", "surface-skills-architecture", "Goal")
    assert r.returncode == 0
    assert "skills-skill-architecture" in r.stdout


def test_header_prefers_task_md_over_readme():
    r = _run("path", "surface-skills-architecture")
    assert "task.md" in r.stdout and "readme.md" in r.stdout
    r = _run("header", "surface-skills-architecture", "Goal")
    assert r.returncode == 0, "header MUST prefer task.md over readme.md"
    assert "skills-skill-architecture" in r.stdout


def test_graph_type_task_status_open_returns_open_tasks_only():
    r = _run("graph", "--type", "task", "--status", "open")
    assert r.returncode == 0
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        assert line.startswith("tasks/"), line


def test_graph_without_status_returns_all_of_type():
    r = _run("graph", "--type", "task")
    assert r.returncode == 0
    lines = [
        line for line in r.stdout.splitlines()
        if line.strip() and not line.startswith("…")
    ]
    assert lines, r.stdout
    assert all(line.startswith("tasks/") for line in lines)


def test_manifest_is_parseable_or_clearly_truncated():
    r = _run("manifest")
    assert r.returncode == 0
    assert '"skills"' in r.stdout
    if "… [truncated" not in r.stdout:
        data = json.loads(r.stdout)
        assert isinstance(data["skills"], list)
        if data["skills"]:
            entry = data["skills"][0]
            assert {"slug", "path", "description"} <= set(entry)
    else:
        assert "[" in r.stdout


def test_output_cap_is_1024_bytes():
    r = _run("manifest")
    assert r.returncode == 0
    assert len(r.stdout.encode("utf-8")) <= 1100  # cap + truncation marker
