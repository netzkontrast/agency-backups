"""Tests for tools/check-canon-status.py (Task 083 cluster C.3 / V111.US3-adjacent).

Loaded via importlib because the linter module name has a hyphen.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_TOOLS = Path(__file__).resolve().parents[1]
_LINTER = _TOOLS / "check-canon-status.py"
_FIXTURES = _TOOLS / "tests" / "fixtures" / "novel-architect-v111"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_canon_status", _LINTER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_canon_status"] = mod
    spec.loader.exec_module(mod)
    return mod


CCS = _load_module()


class TestParseEntries:
    def test_valid_fixture_parses_two_entries(self) -> None:
        text = (_FIXTURES / "canon-meta-valid.md").read_text(encoding="utf-8")
        entries = CCS.parse_entries(text)
        assert len(entries) == 2
        assert entries[0]["canon_id"] == "canon-dkt-physik-001"
        assert entries[0]["canon_status"] == "accepted"
        assert entries[1]["canon_id"] == "canon-stil-001"

    def test_inline_field_regex_matches_blockquote(self) -> None:
        text = "## Foo\n\n> - `canon_id`: abc-001\n> - `canon_status`: accepted\n"
        entries = CCS.parse_entries(text)
        assert len(entries) == 1
        assert entries[0]["canon_id"] == "abc-001"
        assert entries[0]["canon_status"] == "accepted"


class TestDiagnosticsValid:
    def test_valid_fixture_emits_zero_diagnostics(self) -> None:
        diags = CCS.diagnostics_for(_FIXTURES / "canon-meta-valid.md")
        assert diags == [], f"expected 0 diagnostics, got: {diags}"


class TestDiagnosticsStale:
    @pytest.fixture
    def diags(self) -> list[str]:
        return CCS.diagnostics_for(_FIXTURES / "canon-meta-stale.md")

    def test_emits_missing_field(self, diags: list[str]) -> None:
        assert any("CANON.MISSING_FIELD" in d and "canon_added_by" in d
                   for d in diags), f"got: {diags}"

    def test_emits_status_enum(self, diags: list[str]) -> None:
        assert any("CANON.STATUS_ENUM" in d and "unconfirmed" in d
                   for d in diags), f"got: {diags}"

    def test_emits_phase_pattern(self, diags: list[str]) -> None:
        assert any("CANON.PHASE_PATTERN" in d and "phase42" in d
                   for d in diags), f"got: {diags}"

    def test_emits_timestamp_format(self, diags: list[str]) -> None:
        assert any("CANON.TIMESTAMP_FORMAT" in d for d in diags), f"got: {diags}"

    def test_emits_conflict_empty(self, diags: list[str]) -> None:
        assert any("CANON.CONFLICT_EMPTY" in d for d in diags), f"got: {diags}"

    def test_emits_superseded_no_res(self, diags: list[str]) -> None:
        assert any("CANON.SUPERSEDED_NO_RES" in d for d in diags), f"got: {diags}"

    def test_emits_reciprocity(self, diags: list[str]) -> None:
        assert any("CANON.RECIPROCITY" in d for d in diags), f"got: {diags}"


class TestExitCodes:
    def test_clean_returns_0(self) -> None:
        rc = CCS.main([str(_FIXTURES / "canon-meta-valid.md")])
        assert rc == 0

    def test_diagnostics_return_2(self) -> None:
        rc = CCS.main([str(_FIXTURES / "canon-meta-stale.md")])
        assert rc == 2

    def test_no_paths_returns_0(self) -> None:
        rc = CCS.main([])
        assert rc == 0
