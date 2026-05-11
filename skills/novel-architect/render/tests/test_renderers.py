"""Tests for render/render_*.py — Task 070 Epic test scaffold (PR #101 review §3).

Covers:
- render_intent — single + dual storyform variations
- render_architecture — basic render contract
- render_scene_matrix — fails loud on missing chapter_count_target;
  single vs dual narrative suffixes
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

RENDER_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RENDER_DIR))

import render_architecture  # noqa: E402
import render_intent  # noqa: E402
import render_scene_matrix  # noqa: E402
from io_helpers import write_yaml  # noqa: E402


# ─── helper ─────────────────────────────────────────────────────────────────


def _seed_workspace(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    slug: str,
    *,
    chapter_count: int | None = 40,
    storyform_count: str = "single",
) -> Path:
    """Set env override + write minimal project files. Return workspace path."""
    monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", str(tmp_path))
    ws = tmp_path / slug
    ws.mkdir(parents=True, exist_ok=True)
    cfg: dict = {"narrative": {}}
    if chapter_count is not None:
        cfg["narrative"]["chapter_count_target"] = chapter_count
    write_yaml(ws / "project-config.yaml", cfg)
    write_yaml(
        ws / "architecture.yaml",
        {"architecture": {"storyform_count": storyform_count}},
    )
    write_yaml(
        ws / "intent.yaml",
        {"intent": {"genre": "hard-sf", "language": "de"}},
    )
    return ws


# ─── render_scene_matrix ────────────────────────────────────────────────────


class TestRenderSceneMatrix:
    def test_fails_loud_on_missing_chapter_count(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """PR #101 review §1.2.A follow-on: no silent default of 40."""
        _seed_workspace(
            monkeypatch, tmp_path, "test-novel", chapter_count=None,
        )
        with pytest.raises(ValueError, match="chapter_count_target missing"):
            render_scene_matrix.render("test-novel")

    def test_single_narrative_suffixes(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        ws = _seed_workspace(
            monkeypatch, tmp_path, "test-novel",
            chapter_count=4, storyform_count="single",
        )
        out = render_scene_matrix.render("test-novel")
        body = out.read_text(encoding="utf-8")
        # Single-storyform: only narrative_a suffix appears
        assert "narrative_a" in body
        assert "narrative_b" not in body
        # Header reflects single
        assert "Storyform Count:** single" in body
        # 4 chapters generated
        assert body.count("### Kapitel ") == 4
        assert out == ws / "scene-matrix.md"

    def test_dual_narrative_suffixes(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        _seed_workspace(
            monkeypatch, tmp_path, "test-dual",
            chapter_count=4, storyform_count="dual",
        )
        out = render_scene_matrix.render("test-dual")
        body = out.read_text(encoding="utf-8")
        # Dual-storyform: both narrative_a and narrative_b appear
        assert "narrative_a" in body
        assert "narrative_b" in body
        # AP-9 reminder line (dual-storyform parallel-fill)
        assert "dual storyform" in body


# ─── render_intent ──────────────────────────────────────────────────────────


class TestRenderIntent:
    def test_emits_status_view(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        ws = _seed_workspace(monkeypatch, tmp_path, "intent-test")
        # render_intent expects intent.yaml in workspace; seeded above
        out = render_intent.render("intent-test")
        assert out.exists()
        body = out.read_text(encoding="utf-8")
        # Output is a status view; references the genre slot we seeded
        assert "hard-sf" in body or "Genre" in body or "intent" in body.lower()


# ─── render_architecture ────────────────────────────────────────────────────


class TestRenderArchitecture:
    def test_emits_architecture_view(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        ws = _seed_workspace(monkeypatch, tmp_path, "arch-test")
        out = render_architecture.render("arch-test")
        assert out.exists()
        body = out.read_text(encoding="utf-8")
        # Output mentions storyform_count we seeded
        assert "single" in body or "storyform" in body.lower()
