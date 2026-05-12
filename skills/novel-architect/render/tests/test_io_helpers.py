"""Tests for render/io_helpers.py — Task 070 Epic test scaffold (PR #101 review §3).

Covers:
- validate_slug() — kebab-case enforcement, path-traversal defence
- utcnow_iso() — ISO-8601 Z format
- projects_root() — env-var override, fallback default
- project_workspace() — env-override propagation
- atomic_write() — file content + tempfile cleanup
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Make the render/ package importable from the test runner.
RENDER_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RENDER_DIR))

from io_helpers import (  # noqa: E402
    DEFAULT_PROJECTS_ROOT,
    SKILL_VERSION,
    atomic_write,
    project_workspace,
    projects_root,
    utcnow_iso,
    validate_slug,
)


# ─── validate_slug ──────────────────────────────────────────────────────────


class TestValidateSlug:
    @pytest.mark.parametrize(
        "good_slug",
        ["a", "abc", "kohaerenz-protokoll", "my-sf-novel-2", "x1-y2-z3"],
    )
    def test_accepts_kebab_case(self, good_slug: str) -> None:
        assert validate_slug(good_slug) == good_slug

    @pytest.mark.parametrize(
        "bad_slug",
        [
            "",
            "UPPER",
            "Camel",
            "with space",
            "with_underscore",
            "trailing-",
            "-leading",
            "double--dash",
            "../path-traversal",
            "slash/here",
        ],
    )
    def test_rejects_non_kebab(self, bad_slug: str) -> None:
        with pytest.raises(ValueError):
            validate_slug(bad_slug)

    def test_rejects_non_string(self) -> None:
        with pytest.raises(ValueError):
            validate_slug(None)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            validate_slug(123)  # type: ignore[arg-type]


# ─── utcnow_iso ─────────────────────────────────────────────────────────────


class TestUtcnowIso:
    def test_format(self) -> None:
        s = utcnow_iso()
        # Z suffix + length: YYYY-MM-DDTHH:MM:SSZ → 20 chars
        assert s.endswith("Z")
        assert len(s) == 20
        # Components are digits / separators
        assert s[4] == "-" and s[7] == "-"
        assert s[10] == "T"
        assert s[13] == ":" and s[16] == ":"


# ─── projects_root / project_workspace ──────────────────────────────────────


class TestProjectsRoot:
    def test_default_when_env_unset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("NOVEL_ARCHITECT_PROJECTS_ROOT", raising=False)
        assert projects_root() == Path(DEFAULT_PROJECTS_ROOT)

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", str(tmp_path))
        assert projects_root() == tmp_path

    def test_empty_env_falls_back(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", "")
        assert projects_root() == Path(DEFAULT_PROJECTS_ROOT)

    def test_whitespace_env_falls_back(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", "   ")
        assert projects_root() == Path(DEFAULT_PROJECTS_ROOT)


class TestProjectWorkspace:
    def test_workspace_under_projects_root(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", str(tmp_path))
        ws = project_workspace("kohaerenz-protokoll")
        assert ws == tmp_path / "kohaerenz-protokoll"

    def test_workspace_rejects_bad_slug(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        monkeypatch.setenv("NOVEL_ARCHITECT_PROJECTS_ROOT", str(tmp_path))
        with pytest.raises(ValueError):
            project_workspace("../escape")


# ─── atomic_write ───────────────────────────────────────────────────────────


class TestAtomicWrite:
    def test_writes_content(self, tmp_path: Path) -> None:
        out = tmp_path / "sub" / "file.txt"
        atomic_write(out, "hello world\n")
        assert out.read_text(encoding="utf-8") == "hello world\n"

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        out = tmp_path / "a" / "b" / "c" / "file.txt"
        atomic_write(out, "nested")
        assert out.exists()

    def test_no_tempfile_leak(self, tmp_path: Path) -> None:
        out = tmp_path / "file.txt"
        atomic_write(out, "content")
        # The function uses NamedTemporaryFile + os.replace; on success the
        # tempfile is consumed by replace, so only file.txt should remain.
        assert {p.name for p in tmp_path.iterdir()} == {"file.txt"}

    def test_overwrites_atomically(self, tmp_path: Path) -> None:
        out = tmp_path / "file.txt"
        atomic_write(out, "first")
        atomic_write(out, "second")
        assert out.read_text(encoding="utf-8") == "second"


# ─── SKILL_VERSION SSoT (Task 083 V111.US5 / M1 fix) ────────────────────────


class TestSkillVersionSsot:
    """Anchor: V111.US5. Asserts io_helpers.SKILL_VERSION matches the orchestrator
    SKILL.md metadata.version frontmatter — the two sources of truth that drifted
    apart between v1.1.0 (SKILL.md said 1.1.0, io_helpers said 1.0.0) and were
    re-aligned in v1.1.1 hardening.
    """

    def test_skill_version_matches_skill_md_frontmatter(self) -> None:
        import yaml

        skill_md_path = RENDER_DIR.parent / "SKILL.md"
        assert skill_md_path.exists(), f"SKILL.md missing at {skill_md_path}"

        text = skill_md_path.read_text(encoding="utf-8")
        # Frontmatter is the first --- ... --- block.
        assert text.startswith("---\n"), "SKILL.md must open with YAML frontmatter"
        _, fm_block, _ = text.split("---\n", 2)
        fm = yaml.safe_load(fm_block)

        skill_md_version = fm.get("metadata", {}).get("version")
        assert skill_md_version is not None, (
            "SKILL.md metadata.version missing — frontmatter schema drift"
        )
        assert SKILL_VERSION == skill_md_version, (
            f"SKILL_VERSION SSoT drift: io_helpers.py says {SKILL_VERSION!r} "
            f"but SKILL.md metadata.version says {skill_md_version!r}. "
            f"Both MUST match (Task 083 V111.US5 / M1 fix)."
        )
