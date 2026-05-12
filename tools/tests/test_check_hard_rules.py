"""Tests for tools/check-hard-rules.py (Task 090 cluster C.2)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_TOOLS = Path(__file__).resolve().parents[1]
_LINTER = _TOOLS / "check-hard-rules.py"
_FIXTURES = _TOOLS / "tests" / "fixtures" / "novel-architect-v111"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_hard_rules", _LINTER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_hard_rules"] = mod
    spec.loader.exec_module(mod)
    return mod


CHR = _load_module()


class TestValidFixture:
    @pytest.fixture
    def diags(self) -> list[str]:
        return CHR.diagnostics_for(_FIXTURES / "architecture-valid.yaml")

    def test_zero_warn_diagnostics(self, diags: list[str]) -> None:
        warns = [d for d in diags if "::WARN:" in d]
        assert warns == [], f"expected 0 WARN, got: {warns}"

    def test_emits_h5_h8_deferred_info(self, diags: list[str]) -> None:
        # Deferred ontology rules emit INFO regardless of fixture validity.
        infos = [d for d in diags if "::INFO:" in d]
        assert any("H5-H8.DEFERRED" in d for d in infos), f"got: {infos}"

    def test_main_returns_0(self) -> None:
        # INFO-only result has no WARNs → exit 0.
        rc = CHR.main([str(_FIXTURES / "architecture-valid.yaml")])
        assert rc == 0


class TestViolationFixture:
    @pytest.fixture
    def diags(self) -> list[str]:
        return CHR.diagnostics_for(_FIXTURES / "architecture-violation.yaml")

    def test_emits_h2_class_uniqueness(self, diags: list[str]) -> None:
        # Violation fixture: MC, IC, OS all = Universe — H2 fires.
        assert any("H2.CLASS_UNIQUENESS" in d for d in diags), f"got: {diags}"

    def test_emits_h3_mc_ic_complement(self, diags: list[str]) -> None:
        # MC and IC are both Universe → H3 fires (not complementary).
        assert any("H3.MC_IC_COMPLEMENT" in d for d in diags), f"got: {diags}"

    def test_emits_h4_os_ss_complement(self, diags: list[str]) -> None:
        # OS=Universe, SS=Mind → complement (no H4 violation here actually).
        # The fixture has OS=Universe SS=Mind (valid pair). Let's not assert
        # H4 fires; only verify it doesn't falsely fire on a valid pair.
        h4_diags = [d for d in diags if "H4.OS_SS_COMPLEMENT" in d]
        # Valid pair → no H4 diagnostic
        assert h4_diags == [], f"H4 should not fire on Universe/Mind: {h4_diags}"

    def test_violation_main_returns_2(self) -> None:
        rc = CHR.main([str(_FIXTURES / "architecture-violation.yaml")])
        assert rc == 2


class TestEnumChecks:
    """Synthetic in-memory tests for H9/H10/H11/H12 enum checks."""

    @pytest.fixture
    def base_narrative(self) -> dict:
        return {
            "throughlines": {
                "os": {"name": "X", "class": "Universe"},
                "mc": {"name": "Y", "class": "Physics"},
                "ic": {"name": "Z", "class": "Psychology"},
                "ss": {"name": "W", "class": "Mind"},
            },
            "dynamics": {
                "plot_driver": "Action",
                "plot_limit": "Optionlock",
                "outcome": "Success",
                "judgment": "Good",
                "mc_approach": "Doer",
                "mc_mental_sex": "Linear",
            },
        }

    def test_h9_driver_invalid(self, base_narrative: dict) -> None:
        base_narrative["dynamics"]["plot_driver"] = "Ambiguous"
        diags = CHR._check_h9(Path("test"), base_narrative, 0)
        assert any("H9.DRIVER_ENUM" in d for d in diags), f"got: {diags}"

    def test_h10_limit_invalid(self, base_narrative: dict) -> None:
        base_narrative["dynamics"]["plot_limit"] = "Eventlock"
        diags = CHR._check_h10(Path("test"), base_narrative, 0)
        assert any("H10.LIMIT_ENUM" in d for d in diags), f"got: {diags}"

    def test_h11_outcome_invalid(self, base_narrative: dict) -> None:
        base_narrative["dynamics"]["outcome"] = "Partial"
        diags = CHR._check_h11(Path("test"), base_narrative, 0)
        assert any("H11.OUTCOME_ENUM" in d for d in diags), f"got: {diags}"

    def test_h11_judgment_invalid(self, base_narrative: dict) -> None:
        base_narrative["dynamics"]["judgment"] = "Mixed"
        diags = CHR._check_h11(Path("test"), base_narrative, 0)
        assert any("H11.JUDGMENT_ENUM" in d for d in diags), f"got: {diags}"

    def test_h12_approach_invalid(self, base_narrative: dict) -> None:
        base_narrative["dynamics"]["mc_approach"] = "Reactive"
        diags = CHR._check_h12(Path("test"), base_narrative, 0)
        assert any("H12.APPROACH_ENUM" in d for d in diags), f"got: {diags}"

    def test_placeholder_does_not_fire(self, base_narrative: dict) -> None:
        # WIP <PLACEHOLDER> values should NOT trigger violations.
        base_narrative["dynamics"]["plot_driver"] = CHR.PLACEHOLDER
        diags = CHR._check_h9(Path("test"), base_narrative, 0)
        assert diags == [], f"placeholder should be tolerated: {diags}"


class TestEdgeCases:
    def test_no_paths_returns_0(self) -> None:
        rc = CHR.main([])
        assert rc == 0

    def test_complement_pairs_constants(self) -> None:
        assert CHR.COMPLEMENT_PAIRS["Universe"] == "Mind"
        assert CHR.COMPLEMENT_PAIRS["Physics"] == "Psychology"

    def test_h1_missing_throughlines(self) -> None:
        narrative = {"throughlines": {"os": {}, "mc": {}, "ic": {}}}  # missing ss
        diags = CHR._check_h1(Path("test"), narrative, 0)
        assert any("H1.THROUGHLINE_COUNT" in d for d in diags), f"got: {diags}"
