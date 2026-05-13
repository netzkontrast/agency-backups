"""Integration-test fixture for Task 061 — TASK.md §7.0 linter coverage."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED = Path(__file__).resolve().parent / "fixtures" / "seed"
SCHEMA_FILES = (
    "header-ontology.json",
    "diagnostic-explanations.json",
    "l1-vault-core.schema.json",
    "l2-task.schema.json",
    "l2-prompt.schema.json",
    "l2-research.schema.json",
    "l2-skill.schema.json",
    "l2-adr.schema.json",
)


def _materialise(dest: Path) -> Path:
    shutil.copytree(SEED, dest, dirs_exist_ok=True)
    schemas = dest / "maintenance" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    for name in SCHEMA_FILES:
        src = REPO_ROOT / "maintenance" / "schemas" / name
        if src.exists():
            shutil.copy2(src, schemas / name)
    subprocess.run(
        ["git", "init", "-q", "-b", "main"], cwd=dest, check=True,
    )
    return dest


@pytest.fixture
def triptych_fixture(tmp_path: Path) -> Path:
    """Materialise the seed triptych into a fresh tmp_path and return it."""
    return _materialise(tmp_path / "fixture")
