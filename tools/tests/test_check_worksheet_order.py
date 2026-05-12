"""Tests for tools/check-worksheet-order.py (Task 083 cluster C.1)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_TOOLS = Path(__file__).resolve().parents[1]
_LINTER = _TOOLS / "check-worksheet-order.py"
_FIXTURES = _TOOLS / "tests" / "fixtures" / "novel-architect-v111"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_worksheet_order", _LINTER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_worksheet_order"] = mod
    spec.loader.exec_module(mod)
    return mod


CWO = _load_module()


class TestValidFixture:
    def test_valid_emits_zero_diagnostics(self) -> None:
        diags = CWO.diagnostics_for(_FIXTURES / "architecture-valid.yaml")
        assert diags == [], f"expected 0, got: {diags}"

    def test_valid_main_returns_0(self) -> None:
        rc = CWO.main([str(_FIXTURES / "architecture-valid.yaml")])
        assert rc == 0


class TestViolationFixture:
    @pytest.fixture
    def diags(self) -> list[str]:
        return CWO.diagnostics_for(_FIXTURES / "architecture-violation.yaml")

    def test_emits_class_pair_violation(self, diags: list[str]) -> None:
        # MC and IC are both Universe — must trigger CLASS_PAIR
        assert any("WORKSHEET.CLASS_PAIR" in d for d in diags), f"got: {diags}"

    def test_emits_name_empty(self, diags: list[str]) -> None:
        # MC name is empty string
        assert any("WORKSHEET.NAME_EMPTY" in d and "mc.name" in d
                   for d in diags), f"got: {diags}"

    def test_emits_audit_gap(self, diags: list[str]) -> None:
        # step_7 is true but step_2/3/5/6 are false
        assert any("WORKSHEET.AUDIT_GAP" in d for d in diags), f"got: {diags}"

    def test_emits_audit_incomplete(self, diags: list[str]) -> None:
        # approved=true but step_2 is false → INCOMPLETE
        assert any("WORKSHEET.AUDIT_INCOMPLETE" in d for d in diags), f"got: {diags}"

    def test_violation_main_returns_2(self) -> None:
        rc = CWO.main([str(_FIXTURES / "architecture-violation.yaml")])
        assert rc == 2


class TestEdgeCases:
    def test_missing_path_is_warned_not_crashed(self) -> None:
        rc = CWO.main(["/nonexistent/path.yaml"])
        # Missing path → printed warning, no diagnostics → rc 0
        assert rc == 0

    def test_no_paths_returns_0(self) -> None:
        rc = CWO.main([])
        assert rc == 0

    def test_complementary_pair_constants(self) -> None:
        # Smoke test for the class-pair map.
        assert CWO.COMPLEMENT_PAIRS["Universe"] == "Mind"
        assert CWO.COMPLEMENT_PAIRS["Mind"] == "Universe"
        assert CWO.COMPLEMENT_PAIRS["Physics"] == "Psychology"
        assert CWO.COMPLEMENT_PAIRS["Psychology"] == "Physics"
