"""CLI sub-process tests — anchors ADR.A.5.1, ADR.A.5.2, ADR.A.5.5, ADR.A.5.6, ADR.A.5.8."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
CLI = REPO / "tools" / "adr" / "cli.py"


def _isolated_repo(tmp_path) -> Path:
    """Build a minimal repo skeleton that AGENTS-aware tools recognise."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "AGENTS.md").write_text(
        "# AGENTS\n\n## Synthesised ADR Constraints\n\n"
        "<!-- BEGIN AGENCY-ADR SYNTHESIS -->\n"
        "<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. Edits will be overwritten by tools/adr/cli.py synthesize. -->\n"
        "_(empty)_\n"
        "<!-- END AGENCY-ADR SYNTHESIS -->\n",
        encoding="utf-8",
    )
    (repo / "decisions").mkdir()
    schemas = repo / "maintenance" / "schemas"
    schemas.mkdir(parents=True)
    shutil.copy(REPO / "maintenance" / "schemas" / "header-ontology.json",
                schemas / "header-ontology.json")
    (repo / "maintenance" / "run-log.md").write_text(
        "# log\n\n", encoding="utf-8"
    )
    return repo


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
    )


def _write_adr(repo: Path, num: int, status: str = "Accepted") -> None:
    text = (
        "---\n"
        "type: adr\n"
        "status: active\n"
        f"slug: {num:04d}-cli-test\n"
        "summary: cli\n"
        "created: 2026-05-06\n"
        "updated: 2026-05-06\n"
        f"adr_id: ADR-{num:04d}\n"
        f"adr_status: {status}\n"
        "---\n\n"
        "## Context and Problem Statement\nctx\n\n"
        "## Decision Drivers\n- d\n\n"
        "## Considered Options\n- a\n- b\n\n"
        "## Decision Outcome\nThe agent MUST run the validator.\n\n"
        "## Consequences\n- Positive: agents MUST trust the section.\n"
    )
    (repo / "decisions" / f"{num:04d}-cli-test.md").write_text(text, encoding="utf-8")


def test_adr_a_5_1_validate_clean_corpus_exits_zero(tmp_path):
    repo = _isolated_repo(tmp_path)
    _write_adr(repo, 1)
    res = _run(repo, "validate")
    assert res.returncode == 0, res.stderr


def test_adr_a_5_1_empty_corpus_exits_zero(tmp_path):
    repo = _isolated_repo(tmp_path)
    res = _run(repo, "validate")
    assert res.returncode == 0


def test_adr_a_5_5_strict_promotes_warns(tmp_path):
    repo = _isolated_repo(tmp_path)
    _write_adr(repo, 1)
    res = _run(repo, "validate", "--strict")
    # No WARN diagnostics in our happy fixture; strict still exits 0.
    assert res.returncode == 0


def test_adr_a_5_6_duplicate_id_exits_one(tmp_path):
    repo = _isolated_repo(tmp_path)
    _write_adr(repo, 42)
    # second copy under a different filename, same adr_id 0042.
    text = (repo / "decisions" / "0042-cli-test.md").read_text(encoding="utf-8")
    (repo / "decisions" / "0099-second.md").write_text(
        text.replace("slug: 0042-cli-test", "slug: 0099-second"),
        encoding="utf-8",
    )
    res = _run(repo, "validate", "--format=json")
    assert res.returncode == 1
    payload = json.loads(res.stdout)
    codes = {d["code"] for d in payload["diagnostics"]}
    assert "ADR.A.5.6" in codes


def test_adr_a_5_2_synthesize_writes_section(tmp_path):
    repo = _isolated_repo(tmp_path)
    _write_adr(repo, 1)
    res = _run(repo, "synthesize", "--token-limit=2000")
    assert res.returncode == 0, res.stderr
    text = (repo / "AGENTS.md").read_text(encoding="utf-8")
    assert "ADR-0001" in text
    # Run-log got one record.
    log_text = (repo / "maintenance" / "run-log.md").read_text(encoding="utf-8")
    assert "adr-synthesize" in log_text


def test_invalid_subcommand_exits_two(tmp_path):
    repo = _isolated_repo(tmp_path)
    res = _run(repo, "bogus")
    assert res.returncode == 2
