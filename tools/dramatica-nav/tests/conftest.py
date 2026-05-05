"""Shared pytest fixtures for the dramatica-nav suite.

Adds the navigator dir to sys.path so test files can `from lib import …` —
the directory has a hyphen so it isn't a valid Python package name.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
NAV_DIR = REPO_ROOT / "tools" / "dramatica-nav"

# sys.path manipulation MUST happen before any `from lib …` import
sys.path.insert(0, str(NAV_DIR))

import pytest  # noqa: E402

from lib import ontology  # noqa: E402


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def nav_dir() -> Path:
    return NAV_DIR


@pytest.fixture(scope="session")
def canonical_ontology_path(repo_root: Path) -> Path:
    return repo_root / "maintenance" / "schemas" / "narrative-ontology" / "ontology.json"


@pytest.fixture(scope="session")
def canonical_index(canonical_ontology_path: Path):
    return ontology.OntologyIndex(canonical_ontology_path)


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "gherkin(anchor): Maps test to a Gherkin acceptance scenario anchor (e.g., NO.1.1)",
    )
