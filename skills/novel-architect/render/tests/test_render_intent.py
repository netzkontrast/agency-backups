"""
Tests for render_intent.py — covers Task 072 deliverables:

- §2.5 (slot-list consolidation): `load_slot_lists()` reads the canonical
  list from `assets/intent-template.yaml` `_meta._required` / `_meta._optional`
  at runtime, with graceful fallback when the template is missing or malformed.
- §2.7 (slot-state polish): `slot_state()` collapses the previous
  redundant `value == "<PLACEHOLDER>"` then `"<PLACEHOLDER>" in value` ordering
  into one branch.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import render_intent
from render_intent import (
    _FALLBACK_OPTIONAL,
    _FALLBACK_REQUIRED,
    load_slot_lists,
    slot_state,
)


# ─── slot_state (§2.7 polish) ──────────────────────────────────────────────


class TestSlotState:
    """The collapsed slot-state classifier."""

    def test_none_is_empty(self) -> None:
        assert slot_state(None) == "⏳ empty"

    def test_empty_string_is_empty(self) -> None:
        assert slot_state("") == "⏳ empty"

    def test_bare_placeholder_is_empty(self) -> None:
        """A bare `<PLACEHOLDER>` is empty, not partial — review §2.7."""
        assert slot_state("<PLACEHOLDER>") == "⏳ empty"

    def test_placeholder_embedded_is_partial(self) -> None:
        """`<PLACEHOLDER>` embedded in a longer string → partial."""
        assert slot_state("Hard-SF (subgenre: <PLACEHOLDER>)") == "⏳ partial"

    def test_empty_list_is_empty(self) -> None:
        assert slot_state([]) == "⏳ empty"

    def test_filled_string_is_filled(self) -> None:
        assert slot_state("Hard-SF") == "✓ filled"

    def test_filled_list_is_filled(self) -> None:
        assert slot_state(["tsdp-ifs", "big-five"]) == "✓ filled"

    def test_integer_is_filled(self) -> None:
        """chapter_count_target is an int — must not be misclassified."""
        assert slot_state(40) == "✓ filled"

    def test_dict_is_filled(self) -> None:
        """methods_preference is a dict — must classify as filled."""
        assert slot_state({"character": ["tsdp-ifs"]}) == "✓ filled"

    def test_zero_is_filled(self) -> None:
        """Falsy-but-not-None values are filled (zero is a real choice)."""
        assert slot_state(0) == "✓ filled"

    def test_false_is_filled(self) -> None:
        assert slot_state(False) == "✓ filled"

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (None, "⏳ empty"),
            ("", "⏳ empty"),
            ("<PLACEHOLDER>", "⏳ empty"),
            ([], "⏳ empty"),
            ("partial <PLACEHOLDER> here", "⏳ partial"),
            ("real value", "✓ filled"),
            (42, "✓ filled"),
            (["a"], "✓ filled"),
        ],
    )
    def test_classification_matrix(self, value, expected: str) -> None:
        """Parametrized sweep across all states."""
        assert slot_state(value) == expected


# ─── load_slot_lists (§2.5 SSoT) ───────────────────────────────────────────


class TestLoadSlotLists:
    """Slot-list loader reads from `assets/intent-template.yaml` at runtime."""

    def test_loads_from_canonical_template(self) -> None:
        """The canonical template ships with a `_meta` block."""
        required, optional = load_slot_lists()
        # The canonical list must contain the well-known Phase 1 slots.
        assert "genre" in required
        assert "core_conflict_question" in required
        assert "success_criterion" in required
        assert "philosophy_integration_level" in optional
        assert "science_integration_level" in optional

    def test_canonical_template_matches_fallback(self) -> None:
        """The fallback must agree with the canonical template — drift is a bug."""
        required, optional = load_slot_lists()
        assert required == _FALLBACK_REQUIRED
        assert optional == _FALLBACK_OPTIONAL

    def test_missing_template_uses_fallback(self, tmp_path: Path, capsys) -> None:
        """A missing template file falls back to embedded constants (warns)."""
        nonexistent = tmp_path / "nope.yaml"
        required, optional = load_slot_lists(nonexistent)
        assert required == _FALLBACK_REQUIRED
        assert optional == _FALLBACK_OPTIONAL
        # Loader returns empty dict for missing files (read_yaml contract) →
        # `_meta` block missing → fallback path. The warning fires there.
        err = capsys.readouterr().err
        assert "missing `_meta` block" in err or "embedded fallback" in err

    def test_template_without_meta_uses_fallback(self, tmp_path: Path, capsys) -> None:
        """A template that exists but lacks `_meta` falls back."""
        template = tmp_path / "intent-template.yaml"
        template.write_text(
            "schema_version: '1.0'\nintent:\n  genre: <PLACEHOLDER>\n",
            encoding="utf-8",
        )
        required, optional = load_slot_lists(template)
        assert required == _FALLBACK_REQUIRED
        assert optional == _FALLBACK_OPTIONAL
        assert "missing `_meta` block" in capsys.readouterr().err

    def test_template_malformed_required_uses_fallback(
        self, tmp_path: Path, capsys
    ) -> None:
        """`_meta._required` not a list-of-strings → fallback (warn)."""
        template = tmp_path / "intent-template.yaml"
        template.write_text(
            yaml.safe_dump({"_meta": {"_required": "not-a-list", "_optional": ["foo"]}}),
            encoding="utf-8",
        )
        required, optional = load_slot_lists(template)
        assert required == _FALLBACK_REQUIRED
        # `_optional` was a valid list, so it should NOT fall back.
        assert optional == ["foo"]
        assert "_required` malformed" in capsys.readouterr().err

    def test_template_malformed_optional_uses_fallback(
        self, tmp_path: Path, capsys
    ) -> None:
        """`_meta._optional` not a list-of-strings → fallback (warn)."""
        template = tmp_path / "intent-template.yaml"
        template.write_text(
            yaml.safe_dump(
                {
                    "_meta": {
                        "_required": ["a", "b"],
                        "_optional": [1, 2, 3],  # ints, not strings
                    }
                }
            ),
            encoding="utf-8",
        )
        required, optional = load_slot_lists(template)
        assert required == ["a", "b"]
        assert optional == _FALLBACK_OPTIONAL
        assert "_optional` malformed" in capsys.readouterr().err

    def test_template_custom_slot_set(self, tmp_path: Path) -> None:
        """Custom slot list is returned verbatim when well-formed."""
        template = tmp_path / "intent-template.yaml"
        template.write_text(
            yaml.safe_dump(
                {
                    "_meta": {
                        "_required": ["alpha", "beta", "gamma"],
                        "_optional": ["delta"],
                    }
                }
            ),
            encoding="utf-8",
        )
        required, optional = load_slot_lists(template)
        assert required == ["alpha", "beta", "gamma"]
        assert optional == ["delta"]

    def test_load_returns_fresh_lists(self) -> None:
        """Each call returns new list instances — no shared mutable state."""
        r1, o1 = load_slot_lists()
        r2, o2 = load_slot_lists()
        assert r1 == r2
        assert o1 == o2
        # Mutate one; the other must remain intact.
        r1.append("intentional-mutation")
        assert "intentional-mutation" not in r2

    def test_unparseable_yaml_uses_fallback(self, tmp_path: Path, capsys) -> None:
        """A YAML parse error is caught and falls back."""
        template = tmp_path / "intent-template.yaml"
        template.write_text(": this is not valid yaml :", encoding="utf-8")
        required, optional = load_slot_lists(template)
        assert required == _FALLBACK_REQUIRED
        assert optional == _FALLBACK_OPTIONAL
        err = capsys.readouterr().err
        assert "failed to load" in err or "missing `_meta`" in err


# ─── Module-level constants populated from loader ──────────────────────────


class TestModuleConstants:
    """REQUIRED_SLOTS / OPTIONAL_SLOTS are populated at import time."""

    def test_required_slots_populated(self) -> None:
        assert render_intent.REQUIRED_SLOTS  # non-empty
        assert "genre" in render_intent.REQUIRED_SLOTS

    def test_optional_slots_populated(self) -> None:
        assert render_intent.OPTIONAL_SLOTS  # non-empty
        assert "philosophy_integration_level" in render_intent.OPTIONAL_SLOTS

    def test_module_constants_match_loader(self) -> None:
        required, optional = load_slot_lists()
        assert render_intent.REQUIRED_SLOTS == required
        assert render_intent.OPTIONAL_SLOTS == optional
