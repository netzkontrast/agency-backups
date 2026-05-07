"""Tests for tools/check-trust-audit.py — Task 035 ST-4.

Coverage per the brief at
prompts/tooling-trust-audit-gate/brief.md §Acceptance Criteria:

  * passing workspace — exit 0.
  * schema-fail — exit 1, TRUST.SCHEMA diagnostic.
  * behavioral-fail — exit 1, TRUST.BEHAVIORAL diagnostic.
  * governance-fail — exit 1, TRUST.GOVERNANCE diagnostic.
  * DIAGNOSTIC_SCHEMA exported with the documented thresholds.
  * Multi-workspace invocation rejected with TRUST.PARTITION.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_trust_audit",
        TOOLS / "check-trust-audit.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_trust_audit"] = module
    spec.loader.exec_module(module)
    return module


cta = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cta.main(argv)
    return rc, out.getvalue(), err.getvalue()


_README_FM = textwrap.dedent(
    """\
    ---
    type: research
    status: completed
    slug: demo
    summary: "Demo workspace."
    created: 2026-05-07
    updated: 2026-05-07
    research_phase: complete
    research_executes_prompt: demo
    research_friction_level: FL0
    ---

    # Demo workspace
    """
)

_OUTPUT_FM = textwrap.dedent(
    """\
    ---
    type: research
    status: completed
    slug: demo
    summary: "Demo SPEC."
    created: 2026-05-07
    updated: 2026-05-07
    research_phase: complete
    research_executes_prompt: demo
    research_friction_level: FL0
    ---

    # Demo SPEC
    """
)


def _seed_passing_workspace(root: Path) -> Path:
    ws = root / "research" / "demo"
    for sub in ("workspace", "synthesis", "reflection", "output"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
        (ws / sub / "readme.md").write_text(f"# {sub} readme\n", encoding="utf-8")
    (ws / "readme.md").write_text(_README_FM, encoding="utf-8")
    (ws / "workspace" / "session.log").write_text("trace\n", encoding="utf-8")
    (ws / "synthesis" / "post-synthesis-log.md").write_text(
        "merge-log\n", encoding="utf-8"
    )
    (ws / "synthesis" / "state.md").write_text("- [x] step\n", encoding="utf-8")
    (ws / "synthesis" / "methodology.md").write_text("M06\n", encoding="utf-8")
    (ws / "reflection" / "friction-log.md").write_text(
        "Highest Frustration Level: FL0\n", encoding="utf-8"
    )
    (ws / "reflection" / "M06-discussion.md").write_text(
        "discussion\n", encoding="utf-8"
    )
    (ws / "output" / "SPEC.md").write_text(_OUTPUT_FM, encoding="utf-8")

    # Stub prompt so the prompt-linkage governance check passes.
    (root / "prompts" / "demo").mkdir(parents=True, exist_ok=True)
    (root / "prompts" / "demo" / "prompt.md").write_text("# stub\n", encoding="utf-8")

    return ws


@contextlib.contextmanager
def _fake_repo():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        original_root = cta.REPO_ROOT
        cta.REPO_ROOT = root
        cwd = os.getcwd()
        os.chdir(root)
        try:
            yield root
        finally:
            cta.REPO_ROOT = original_root
            os.chdir(cwd)


class TrustAudit(unittest.TestCase):
    def test_diagnostic_schema_thresholds(self) -> None:
        self.assertEqual(
            cta.DIAGNOSTIC_SCHEMA["thresholds"],
            {"schema": 0.80, "behavioral": 0.90, "governance": 0.95},
        )
        self.assertEqual(cta.DIAGNOSTIC_SCHEMA["namespace"], "TRUST")

    def test_passing_workspace_exits_zero(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 0, err)

    def test_schema_fail_missing_subdir(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            # Remove output dir entirely so two schema items fail
            # (output-subdir, output-doc, output-fm). And subdir readme.
            for f in (ws / "output").rglob("*"):
                f.unlink()
            (ws / "output").rmdir()
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("TRUST.SCHEMA", err)

    def test_behavioral_fail_empty_session_log(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            # Empty session.log -> session-log-nonempty fails (-1/5 = 80%).
            (ws / "workspace" / "session.log").write_text("", encoding="utf-8")
            # Remove methodology.md so two checks fail (-2/5 = 60%).
            (ws / "synthesis" / "methodology.md").unlink()
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("TRUST.BEHAVIORAL", err)

    def test_governance_fail_missing_friction_log(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            (ws / "reflection" / "friction-log.md").unlink()
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("TRUST.GOVERNANCE", err)

    def test_multi_workspace_partition_rejected(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            ws2 = root / "research" / "demo2"
            ws2.mkdir()
            rc, _, err = _capture([str(ws), str(ws2)])
            self.assertEqual(rc, 1, err)
            self.assertIn("TRUST.PARTITION:single-workspace-only", err)

    def test_external_provider_path_rejected(self) -> None:
        """research/gemini/<slug>/ is external — not an in-house workspace."""
        with _fake_repo() as root:
            ext = root / "research" / "gemini" / "demo"
            ext.mkdir(parents=True)
            rc, _, err = _capture([str(ext)])
            self.assertEqual(rc, 1, err)
            self.assertIn("TRUST.INPUT:not-a-workspace", err)

    def test_invalid_phase_value_flagged(self) -> None:
        with _fake_repo() as root:
            ws = _seed_passing_workspace(root)
            broken_fm = _README_FM.replace(
                "research_phase: complete", "research_phase: bogus"
            )
            (ws / "readme.md").write_text(broken_fm, encoding="utf-8")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("phase-enum", err)


if __name__ == "__main__":
    unittest.main()
