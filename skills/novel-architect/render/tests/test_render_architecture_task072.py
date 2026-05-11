"""
Tests for the Task-072 schema additions to render_architecture.py.

Covers:
- Gate-key migration (gate_2_throughlines_classes_dynamics → gate_2_classes_dynamics_storypoints)
  with backward-compat fallback for v1.0.0 workspaces.
- New schema blocks: throughline `name`, `story_points`, `crucial_element`,
  `signposts`/`journeys`, `ending_type`, `genre_mode`, `worksheet_audit`.
- Empty / missing blocks render as `—` rows, no traceback.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import render_architecture


@pytest.fixture
def slug() -> str:
    return "ra-test-consciousness-novel"


@pytest.fixture
def workspace(tmp_path: Path, slug: str, monkeypatch) -> Path:
    """Re-root project workspaces under tmp_path for the test."""
    monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", str(tmp_path))
    ws = tmp_path / slug
    ws.mkdir(parents=True, exist_ok=True)
    return ws


def _write_arch(workspace: Path, data: dict) -> None:
    (workspace / "architecture.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
    )


# ─── Schema-block rendering ────────────────────────────────────────────────


class TestThroughlineNames:
    def test_renders_throughline_names(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "storyform_count": "single",
                "narratives": [{
                    "id": "storyform_a",
                    "throughlines": {
                        "os": {"name": "The community of fragmented minds", "class": "Mind"},
                        "mc": {"name": "Lena", "class": "Psychology"},
                        "ic": {"name": "Vey", "class": "Physics"},
                        "ss": {"name": "Lena ↔ Vey", "class": "Universe"},
                    },
                }],
            },
        })
        out = render_architecture.render(slug)
        body = out.read_text(encoding="utf-8")
        assert "The community of fragmented minds" in body
        assert "Lena ↔ Vey" in body
        assert "| `OS` | The community of fragmented minds | Mind |" in body
        # Step 1 + 2 header present.
        assert "Throughlines (Steps 1 + 2)" in body

    def test_missing_throughlines_renders_dashes(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "storyform_count": "single",
                "narratives": [{"id": "storyform_a", "throughlines": {}}],
            },
        })
        out = render_architecture.render(slug)
        body = out.read_text(encoding="utf-8")
        # Should not raise, dashes present for empty slots.
        assert "| `OS` | — | — | — | — | — |" in body


class TestEndingTypeAndDynamics:
    def test_ending_type_surfaced(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "storyform_count": "single",
                "narratives": [{
                    "id": "storyform_a",
                    "dynamics": {"outcome": "Failure", "judgment": "Good"},
                    "ending_type": "Personal Triumph",
                }],
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "**Personal Triumph**" in body
        assert "ending_type" in body


class TestStoryPoints:
    def test_renders_static_driver_thematic(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "narratives": [{
                    "id": "storyform_a",
                    "story_points": {
                        "static": {"goal": "Memory", "requirements": "Each fragment witnesses"},
                        "driver": {"costs": "Personal cost X"},
                        "thematic": {"os": {"concern": "Memory"}, "mc": {"concern": "Confidence"}},
                    },
                }],
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "Story Points (Step 5)" in body
        assert "static.`goal`: Memory" in body
        assert "driver.`costs`: Personal cost X" in body
        assert "`os`" in body  # thematic per-throughline


class TestCrucialElement:
    def test_renders_crucial_element_block(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "narratives": [{
                    "id": "storyform_a",
                    "crucial_element": {
                        "element": "el.equity",
                        "dynamic_pair_partner": "el.inequity",
                        "role": "problem",
                    },
                }],
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "Crucial Element (Step 6)" in body
        assert "`element`: el.equity" in body
        assert "`dynamic_pair_partner`: el.inequity" in body
        assert "`role`: problem" in body


class TestSignpostsJourneys:
    def test_renders_4_sp_3_jny_per_throughline(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "narratives": [{
                    "id": "storyform_a",
                    "signposts": {
                        "os": ["Memory", "Preconscious", "Conscious", "Subconscious"],
                        "mc": ["Conceiving", "Being", "Becoming", "Conceptualizing"],
                        "ic": ["Understanding", "Doing", "Learning", "Obtaining"],
                        "ss": ["Past", "Progress", "Present", "Future"],
                    },
                    "journeys": {
                        "os": ["j1", "j2", "j3"],
                        "mc": ["j1", "j2", "j3"],
                        "ic": ["j1", "j2", "j3"],
                        "ss": ["j1", "j2", "j3"],
                    },
                }],
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "Signposts + Journeys (Step 7)" in body
        # Mind class type-quad ordering
        assert "Memory" in body and "Subconscious" in body
        # Header includes all 4 SP + 3 JNY columns
        assert "SP1 | J1→2 | SP2 | J2→3 | SP3 | J3→4 | SP4" in body

    def test_pads_short_lists(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {
                "narratives": [{
                    "id": "storyform_a",
                    "signposts": {"os": ["Memory"]},   # only 1 instead of 4
                    "journeys": {"os": []},
                }],
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        # Should pad the OS row in the Signposts table (8 columns: TL + 4 SP + 3 JNY).
        # Find the row by its "Memory" prefix (one literal Signpost) followed by dashes.
        signposts_section = body.split("Signposts + Journeys (Step 7)")[1]
        os_signposts_row = [
            line for line in signposts_section.split("\n")
            if line.startswith("| `OS`") and "Memory" in line
        ]
        assert os_signposts_row, "OS row in Signposts table not rendered"
        # Memory (1) + 3 SP dashes + 3 JNY dashes = 6 dashes
        assert os_signposts_row[0].count("—") == 6, \
            f"Expected 6 padded dashes, got row: {os_signposts_row[0]!r}"


class TestWorksheetAudit:
    def test_renders_all_10_audit_flags(self, workspace, slug):
        _write_arch(workspace, {
            "architecture": {"narratives": [{"id": "storyform_a"}]},
            "worksheet_audit": {
                "step_0_intent_loaded": True,
                "step_1_throughlines_named": True,
                "step_2_classes_assigned": False,
                "step_3_character_dynamics_set": False,
                "step_4_plot_dynamics_set": False,
                "step_5_story_points_set": False,
                "step_6_crucial_element_set": False,
                "step_7_signposts_set": False,
                "step_8_genre_mode_set": False,
                "validation_pass": False,
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "Worksheet Step Audit" in body
        for step in (
            "step_0_intent_loaded",
            "step_1_throughlines_named",
            "step_2_classes_assigned",
            "step_3_character_dynamics_set",
            "step_4_plot_dynamics_set",
            "step_5_story_points_set",
            "step_6_crucial_element_set",
            "step_7_signposts_set",
            "step_8_genre_mode_set",
            "validation_pass",
        ):
            assert step in body, f"Missing flag in audit table: {step}"
        # Set flags get ✓; unset get ⏳
        assert "✓" in body and "⏳" in body


# ─── Gate-key migration ────────────────────────────────────────────────────


class TestGateKeyMigration:
    def test_canonical_keys_render(self, workspace, slug):
        """Task-072 canonical gate-keys render with their approval state."""
        _write_arch(workspace, {
            "architecture": {"narratives": [{"id": "storyform_a"}]},
            "gates": {
                "gate_1_storyform_shape": {"approved": True, "edits": 1},
                "gate_2_classes_dynamics_storypoints": {"approved": True, "edits": 0},
                "gate_3_final_architecture": {"approved": False, "edits": 0},
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        assert "| `gate_1_storyform_shape` | True | 1 |" in body
        assert "| `gate_2_classes_dynamics_storypoints` | True | 0 |" in body
        assert "| `gate_3_final_architecture` | False | 0 |" in body

    def test_v100_legacy_gate_key_fallback(self, workspace, slug):
        """A v1.0.0 workspace using the old key still surfaces its state."""
        _write_arch(workspace, {
            "architecture": {"narratives": [{"id": "storyform_a"}]},
            "gates": {
                "gate_1_storyform_shape": {"approved": True, "edits": 0},
                # v1.0.0 legacy key — Task 072 schema renames to
                # gate_2_classes_dynamics_storypoints, but the renderer
                # should still surface state from the old key.
                "gate_2_throughlines_classes_dynamics": {"approved": True, "edits": 2},
                "gate_3_final_architecture": {"approved": False, "edits": 0},
            },
        })
        body = render_architecture.render(slug).read_text(encoding="utf-8")
        # Renderer surfaces under the canonical key name but reads the legacy data.
        assert "| `gate_2_classes_dynamics_storypoints` | True | 2 |" in body


# ─── End-to-end smoke ──────────────────────────────────────────────────────


class TestEndToEndSmoke:
    def test_consciousness_novel_full_render(self, workspace, slug):
        """A full Task-072-shaped architecture.yaml renders without error."""
        _write_arch(workspace, {
            "schema_version": "1.0",
            "architecture": {
                "storyform_count": "single",
                "narratives": [{
                    "id": "storyform_a",
                    "throughlines": {
                        "os": {"name": "Fragmented community", "class": "Mind"},
                        "mc": {"name": "Lena", "class": "Psychology"},
                        "ic": {"name": "Vey", "class": "Physics"},
                        "ss": {"name": "Lena↔Vey", "class": "Universe"},
                    },
                    "dynamics": {
                        "mc_resolve": "Change",
                        "mc_growth": "Start",
                        "mc_approach": "Beer",
                        "mc_mental_sex": "Holistic",
                        "plot_driver": "Decision",
                        "plot_limit": "Optionlock",
                        "outcome": "Failure",
                        "judgment": "Good",
                    },
                    "ending_type": "Personal Triumph",
                    "story_points": {
                        "static": {"goal": "Memory"},
                        "thematic": {"os": {"concern": "Memory"}},
                    },
                    "crucial_element": {
                        "element": "el.equity",
                        "dynamic_pair_partner": "el.inequity",
                        "role": "problem",
                    },
                    "signposts": {
                        "os": ["Memory", "Preconscious", "Conscious", "Subconscious"],
                    },
                    "journeys": {"os": ["j1", "j2", "j3"]},
                }],
            },
            "gates": {
                "gate_1_storyform_shape": {"approved": True, "edits": 0},
                "gate_2_classes_dynamics_storypoints": {"approved": True, "edits": 1},
                "gate_3_final_architecture": {"approved": True, "edits": 0},
            },
            "worksheet_audit": {
                "step_0_intent_loaded": True,
                "step_1_throughlines_named": True,
                "step_2_classes_assigned": True,
                "step_3_character_dynamics_set": True,
                "step_4_plot_dynamics_set": True,
                "step_5_story_points_set": True,
                "step_6_crucial_element_set": True,
                "step_7_signposts_set": True,
                "step_8_genre_mode_set": False,
                "validation_pass": True,
            },
            "ncp": {"skeleton_written": True, "ncp_file": "canon/x.ncp.json",
                    "validation_status": "passed"},
            "approved": True,
            "revisions": [],
        })
        out = render_architecture.render(slug)
        body = out.read_text(encoding="utf-8")
        # All Task-072 sections present.
        assert "Storyform Shape (Step 0" in body
        assert "Throughlines (Steps 1 + 2)" in body
        assert "Dynamics (Steps 3 + 4)" in body
        assert "Story Points (Step 5)" in body
        assert "Crucial Element (Step 6)" in body
        assert "Signposts + Journeys (Step 7)" in body
        assert "Worksheet Step Audit" in body
        assert "Gates" in body
        assert "NCP" in body
        # No leftover placeholder strings or tracebacks
        assert "<PLACEHOLDER>" not in body
        assert "Traceback" not in body
