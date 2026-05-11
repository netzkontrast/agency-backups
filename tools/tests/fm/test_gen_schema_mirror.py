"""Tests for tools/fm/gen_schema_mirror.py (Task 023)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft7Validator

REPO = Path(__file__).resolve().parents[3]
GEN = REPO / "tools" / "fm" / "gen_schema_mirror.py"
SCHEMAS_DIR = REPO / "maintenance" / "schemas"

L2_TYPES = ["task", "prompt", "research", "skill", "adr"]
MIRROR_NAMES = ["l1-vault-core"] + [f"l2-{t}" for t in L2_TYPES]


def _load_fm(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"no frontmatter in {path}"
    body = text.split("---\n", 2)[1]
    fm = yaml.safe_load(body)
    return json.loads(json.dumps(fm, default=str))


def test_generator_outputs_six_files():
    for name in MIRROR_NAMES:
        path = SCHEMAS_DIR / f"{name}.schema.json"
        assert path.exists(), f"missing mirror {path}"


def test_each_mirror_is_valid_draft7_schema():
    for name in MIRROR_NAMES:
        schema = json.loads((SCHEMAS_DIR / f"{name}.schema.json").read_text())
        Draft7Validator.check_schema(schema)


def test_check_mode_passes_after_generate():
    result = subprocess.run(
        [sys.executable, str(GEN), "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"--check failed after generate; stderr=\n{result.stderr}"
    )


def test_check_mode_detects_divergence(tmp_path: Path):
    target = SCHEMAS_DIR / "l1-vault-core.schema.json"
    original = target.read_text(encoding="utf-8")
    try:
        mutated = json.loads(original)
        mutated["title"] = "mutated"
        target.write_text(json.dumps(mutated) + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(GEN), "--check"],
            cwd=REPO, capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "diverge" in result.stderr.lower()
    finally:
        target.write_text(original, encoding="utf-8")


@pytest.mark.parametrize("sample", [
    "tasks/006-surface-skills-architecture/task.md",
    "tasks/023-header-ontology-and-schema-mirror/task.md",
])
def test_task_mirror_accepts_real_task_md(sample: str):
    schema = json.loads((SCHEMAS_DIR / "l2-task.schema.json").read_text())
    fm = _load_fm(REPO / sample)
    errs = list(Draft7Validator(schema).iter_errors(fm))
    assert errs == [], [(list(e.path), e.message) for e in errs]


def test_prompt_mirror_accepts_a_real_prompt_md():
    schema = json.loads((SCHEMAS_DIR / "l2-prompt.schema.json").read_text())
    samples = list((REPO / "prompts").glob("*/prompt.md"))
    assert samples, "expected at least one prompt.md in /prompts/"
    sample = samples[0]
    fm = _load_fm(sample)
    errs = list(Draft7Validator(schema).iter_errors(fm))
    assert errs == [], (sample, [(list(e.path), e.message) for e in errs])


def test_adr_mirror_accepts_a_real_adr():
    adrs = sorted((REPO / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md"))
    if not adrs:
        pytest.skip("no ADR files present yet")
    schema = json.loads((SCHEMAS_DIR / "l2-adr.schema.json").read_text())
    fm = _load_fm(adrs[0])
    errs = list(Draft7Validator(schema).iter_errors(fm))
    assert errs == [], (adrs[0], [(list(e.path), e.message) for e in errs])


def test_l2_task_rejects_bad_status():
    schema = json.loads((SCHEMAS_DIR / "l2-task.schema.json").read_text())
    bad = {
        "type": "task", "status": "active", "slug": "x", "summary": "x",
        "created": "2026-01-01", "updated": "2026-01-01",
        "task_id": "999", "task_status": "not-a-real-status",
        "task_owner": "x", "task_priority": "P1",
        "task_uses_prompts": [], "task_spawns_research": [],
        "task_spawns_prompts": [], "task_affects_paths": [],
    }
    errs = list(Draft7Validator(schema).iter_errors(bad))
    assert any("not-a-real-status" in e.message or "enum" in e.message for e in errs)
