"""Tests for tools/maintenance/trust-audit.py — Task 039 ST-5 AGGREGATOR.

Coverage per the brief at
prompts/tooling-trust-audit-integration/brief.md §Acceptance Criteria:

  * 0 workspaces — empty rollup, exit 0.
  * 3 clean workspaces — all pass, exit 0 in both modes.
  * 1 failing workspace — strict exits 1; advisory exits 0; FL classified.
  * mixed pass/fail — totals + per-dimension counts correct.
  * Schema lock-step (regression): the AGGREGATOR's thresholds are read
    from the GATE's DIAGNOSTIC_SCHEMA — not hard-coded — so any future
    threshold change in the GATE flows through automatically.
  * JSON output shape — totals + workspaces present.
  * Run-log append — best-effort; no-op when file missing.
  * Partition guard — the AGGREGATOR module exposes no per-workspace
    helper that would re-implement the GATE; everything routes through
    the imported ``audit()`` callable.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "tools"


def _load_aggregator():
    spec = importlib.util.spec_from_file_location(
        "trust_audit_aggregator",
        TOOLS / "maintenance" / "trust-audit.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["trust_audit_aggregator"] = module
    spec.loader.exec_module(module)
    return module


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "check_trust_audit",
        TOOLS / "check-trust-audit.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_trust_audit"] = module
    spec.loader.exec_module(module)
    return module


AGG = _load_aggregator()
GATE = _load_gate()


_README_FM_TEMPLATE = textwrap.dedent(
    """\
    ---
    type: research
    status: completed
    slug: {slug}
    summary: "Demo workspace {slug}."
    created: 2026-05-07
    updated: 2026-05-07
    research_phase: complete
    research_executes_prompt: {slug}
    research_friction_level: FL0
    ---

    # {slug}
    """
)

_OUTPUT_FM_TEMPLATE = textwrap.dedent(
    """\
    ---
    type: research
    status: completed
    slug: {slug}
    summary: "Demo SPEC {slug}."
    created: 2026-05-07
    updated: 2026-05-07
    research_phase: complete
    research_executes_prompt: {slug}
    research_friction_level: FL0
    ---

    # {slug} SPEC
    """
)


def _seed_passing_workspace(repo_root: Path, slug: str) -> Path:
    ws = repo_root / "research" / slug
    for sub in ("workspace", "synthesis", "reflection", "output"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
        (ws / sub / "readme.md").write_text(
            f"# {slug}/{sub} readme\n", encoding="utf-8"
        )
    (ws / "readme.md").write_text(
        _README_FM_TEMPLATE.format(slug=slug), encoding="utf-8"
    )
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
    (ws / "output" / "SPEC.md").write_text(
        _OUTPUT_FM_TEMPLATE.format(slug=slug), encoding="utf-8"
    )

    # Stub prompt so the prompt-linkage governance check passes.
    prompt_dir = repo_root / "prompts" / slug
    prompt_dir.mkdir(parents=True, exist_ok=True)
    (prompt_dir / "prompt.md").write_text("# stub\n", encoding="utf-8")
    return ws


@contextlib.contextmanager
def _fake_repo():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cwd = os.getcwd()
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(cwd)


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = AGG.main(argv)
    return rc, out.getvalue(), err.getvalue()


# ---- Tests -----------------------------------------------------------------


class SchemaLockStep(unittest.TestCase):
    """Regression: AGGREGATOR thresholds MUST come from the GATE."""

    def test_gate_diagnostic_schema_imported(self) -> None:
        # The aggregator's _classify_failures path reaches into the GATE
        # module via importlib.spec_from_file_location at the same path
        # used by the in-tree GATE test harness. We assert the AGGREGATOR
        # sees a DIAGNOSTIC_SCHEMA structurally identical to the GATE's
        # — the schema-lock contract that prevents the AGGREGATOR from
        # drifting when the GATE's thresholds change.
        gate_via_agg = AGG._load_gate_module()
        self.assertEqual(
            gate_via_agg.DIAGNOSTIC_SCHEMA,
            GATE.DIAGNOSTIC_SCHEMA,
        )
        # Both modules MUST resolve to the GATE source file on disk.
        self.assertEqual(
            Path(gate_via_agg.__file__).resolve(),
            (TOOLS / "check-trust-audit.py").resolve(),
        )

    def test_thresholds_drive_classification(self) -> None:
        # Round-trip: a TrustResult constructed from the GATE's class with
        # scores at exactly the threshold MUST classify as passing.
        t = GATE.DIAGNOSTIC_SCHEMA["thresholds"]
        result = GATE.TrustResult(
            schema_score=t["schema"],
            behavioral_score=t["behavioral"],
            governance_score=t["governance"],
            diagnostics=(),
        )
        failed, fl = AGG._classify_failures(result)
        self.assertEqual(failed, ())
        self.assertEqual(fl, 0)

    def test_below_threshold_classifies_failure(self) -> None:
        t = GATE.DIAGNOSTIC_SCHEMA["thresholds"]
        result = GATE.TrustResult(
            schema_score=t["schema"] - 0.01,
            behavioral_score=t["behavioral"],
            governance_score=t["governance"],
            diagnostics=(),
        )
        failed, fl = AGG._classify_failures(result)
        self.assertEqual(failed, ("schema",))
        self.assertEqual(fl, 1)


class ZeroWorkspaces(unittest.TestCase):
    def test_empty_research_dir_is_clean_rollup(self) -> None:
        with _fake_repo() as root:
            (root / "research").mkdir()
            rc, stdout, _ = _capture(
                ["--root", str(root), "--threshold-mode", "strict"]
            )
            self.assertEqual(rc, 0)
            self.assertIn("0 / 0", stdout)
            self.assertIn("nothing to roll up", stdout.lower())

    def test_no_research_dir_at_all(self) -> None:
        with _fake_repo() as root:
            # No research/ directory; aggregator MUST still succeed.
            rc, _, _ = _capture(["--root", str(root)])
            self.assertEqual(rc, 0)


class AllPassing(unittest.TestCase):
    def test_three_clean_workspaces_pass_strict(self) -> None:
        with _fake_repo() as root:
            for slug in ("alpha", "beta", "gamma"):
                _seed_passing_workspace(root, slug)
            rc, stdout, _ = _capture(
                ["--root", str(root), "--threshold-mode", "strict"]
            )
            self.assertEqual(rc, 0, stdout)
            self.assertIn("3 / 3", stdout)
            # No friction recommendations on an all-pass corpus.
            self.assertNotIn("MAINT.TRUST.FRICTION", stdout)

    def test_three_clean_workspaces_pass_advisory(self) -> None:
        with _fake_repo() as root:
            for slug in ("alpha", "beta", "gamma"):
                _seed_passing_workspace(root, slug)
            rc, _, _ = _capture(
                ["--root", str(root), "--threshold-mode", "advisory"]
            )
            self.assertEqual(rc, 0)


class FailingWorkspace(unittest.TestCase):
    def test_one_failing_workspace_strict_exits_1(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "alpha")
            ws_b = _seed_passing_workspace(root, "broken")
            # Break governance: remove friction-log.md (drops governance score).
            (ws_b / "reflection" / "friction-log.md").unlink()
            # Also break prompt linkage so a second governance dim fails too.
            (root / "prompts" / "broken" / "prompt.md").unlink()
            rc, stdout, _ = _capture(
                ["--root", str(root), "--threshold-mode", "strict"]
            )
            self.assertEqual(rc, 1, stdout)
            self.assertIn("research/broken", stdout)
            self.assertIn("MAINT.TRUST.FRICTION:FL", stdout)
            # The good workspace still appears as PASS.
            self.assertIn("PASS", stdout)
            self.assertIn("FAIL", stdout)

    def test_one_failing_workspace_advisory_exits_0(self) -> None:
        with _fake_repo() as root:
            ws_b = _seed_passing_workspace(root, "broken")
            (ws_b / "reflection" / "friction-log.md").unlink()
            (root / "prompts" / "broken" / "prompt.md").unlink()
            rc, stdout, _ = _capture(
                ["--root", str(root), "--threshold-mode", "advisory"]
            )
            # Advisory ALWAYS exits 0 even with failing workspaces.
            self.assertEqual(rc, 0)
            self.assertIn("recommend-task", stdout)


class MixedCorpus(unittest.TestCase):
    def test_mixed_totals_correct(self) -> None:
        with _fake_repo() as root:
            for slug in ("ok1", "ok2"):
                _seed_passing_workspace(root, slug)
            ws_bad = _seed_passing_workspace(root, "bad1")
            # Two governance failures (friction + prompt-linkage) -> 1 dim fail.
            (ws_bad / "reflection" / "friction-log.md").unlink()
            (root / "prompts" / "bad1" / "prompt.md").unlink()

            rc, stdout, _ = _capture(["--root", str(root), "--format", "json"])
            self.assertEqual(rc, 0)
            payload = json.loads(stdout)
            totals = payload["totals"]
            self.assertEqual(totals["workspaces_total"], 3)
            self.assertEqual(totals["workspaces_passed"], 2)
            self.assertEqual(totals["workspaces_failed"], 1)
            self.assertEqual(totals["fl_buckets"]["fl0"], 2)
            self.assertEqual(totals["fl_buckets"]["fl1"], 1)
            self.assertEqual(totals["failed_dimensions"]["governance"], 1)
            self.assertEqual(totals["failed_dimensions"]["schema"], 0)
            self.assertEqual(totals["failed_dimensions"]["behavioral"], 0)
            self.assertEqual(totals["friction_count"], 1)
            self.assertEqual(len(payload["workspaces"]), 3)
            self.assertEqual(len(payload["friction"]), 1)
            self.assertIn("research/bad1", payload["friction"][0])

    def test_external_provider_dirs_skipped(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "real")
            # Provider folders are filtered by the GATE's _is_research_workspace.
            for provider in ("gemini", "gpt", "human", "other"):
                provider_dir = root / "research" / provider / "external"
                provider_dir.mkdir(parents=True)
                (provider_dir / "readme.md").write_text(
                    "research_phase: complete\n", encoding="utf-8"
                )

            rc, stdout, _ = _capture(["--root", str(root), "--format", "json"])
            self.assertEqual(rc, 0)
            payload = json.loads(stdout)
            self.assertEqual(payload["totals"]["workspaces_total"], 1)
            self.assertEqual(payload["workspaces"][0]["workspace"], "research/real")

    def test_non_complete_workspaces_skipped(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "complete-one")
            # In-progress workspace — readme.md does NOT declare phase: complete.
            ws_progress = root / "research" / "in-progress"
            ws_progress.mkdir(parents=True)
            (ws_progress / "readme.md").write_text(
                "research_phase: synthesis\n", encoding="utf-8"
            )
            rc, stdout, _ = _capture(["--root", str(root), "--format", "json"])
            self.assertEqual(rc, 0)
            payload = json.loads(stdout)
            self.assertEqual(payload["totals"]["workspaces_total"], 1)


class FLClassification(unittest.TestCase):
    def test_fl3_when_all_three_dimensions_fail(self) -> None:
        """A workspace failing all three dimensions classifies as FL3."""
        report = AGG.AggregateReport()
        report.workspaces.append(
            AGG.WorkspaceReport(
                workspace="research/broken",
                schema_score=0.0,
                behavioral_score=0.0,
                governance_score=0.0,
                failed_dimensions=("schema", "behavioral", "governance"),
                fl_level=3,
                diagnostics=(),
            )
        )
        totals = report.totals
        self.assertEqual(totals["fl_buckets"]["fl3"], 1)
        self.assertEqual(totals["friction_count"], 1)
        rendered = AGG.render_text(report)
        self.assertIn("FL3", rendered)
        self.assertIn("recommend-task", rendered)


class RunLogIntegration(unittest.TestCase):
    def test_write_runlog_noops_when_file_missing(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "alpha")
            # No maintenance/run-log.md in the fake repo.
            rc, _, _ = _capture(
                ["--root", str(root), "--write-runlog"]
            )
            self.assertEqual(rc, 0)
            self.assertFalse((root / "maintenance" / "run-log.md").exists())

    def test_write_runlog_appends_record(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "alpha")
            (root / "maintenance").mkdir()
            run_log = root / "maintenance" / "run-log.md"
            seed = "# Run log\n\n## Run Records\n\n"
            run_log.write_text(seed, encoding="utf-8")
            rc, _, _ = _capture(
                ["--root", str(root), "--write-runlog"]
            )
            self.assertEqual(rc, 0)
            tail = run_log.read_text(encoding="utf-8")
            self.assertIn("trust-audit-aggregator", tail)
            self.assertIn("routine_type: nightly-maintenance", tail)
            self.assertIn("files_scanned: 1", tail)


class JSONOutputShape(unittest.TestCase):
    def test_json_payload_has_required_keys(self) -> None:
        with _fake_repo() as root:
            _seed_passing_workspace(root, "alpha")
            rc, stdout, _ = _capture(["--root", str(root), "--format", "json"])
            self.assertEqual(rc, 0)
            payload = json.loads(stdout)
            self.assertIn("schema", payload)
            self.assertEqual(payload["schema"], "MAINT.TRUST.AGGREGATE.v1")
            self.assertIn("workspaces", payload)
            self.assertIn("totals", payload)
            self.assertIn("friction", payload)


class PartitionGuard(unittest.TestCase):
    """Falsification: AGGREGATOR MUST NOT re-implement per-workspace logic.

    The C3 partition holds iff the AGGREGATOR routes ALL per-workspace
    work through the GATE's ``audit()`` callable. We assert this by
    inspecting the AGGREGATOR module's symbol table for re-implementations
    of the GATE's private scoring helpers (``_score_schema``,
    ``_score_behavioral``, ``_score_governance``).
    """

    def test_no_redefined_score_helpers(self) -> None:
        forbidden = ("_score_schema", "_score_behavioral", "_score_governance")
        for name in forbidden:
            self.assertFalse(
                hasattr(AGG, name),
                f"AGGREGATOR re-implements GATE helper {name!r}; "
                "violates the C3 partition (Task 039 ST-5 Falsification).",
            )

    def test_aggregator_uses_gate_audit_callable(self) -> None:
        # The aggregator's `aggregate` function MUST call gate.audit. We
        # verify by stubbing audit and confirming it's invoked.
        gate = AGG._load_gate_module()
        original_audit = gate.audit
        calls: list[Path] = []

        def fake_audit(ws: Path):
            calls.append(ws)
            return gate.TrustResult(
                schema_score=1.0,
                behavioral_score=1.0,
                governance_score=1.0,
                diagnostics=(),
            )

        gate.audit = fake_audit
        try:
            with _fake_repo() as root:
                _seed_passing_workspace(root, "alpha")
                _seed_passing_workspace(root, "beta")
                report = AGG.aggregate(root)
        finally:
            gate.audit = original_audit
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(report.workspaces), 2)
        self.assertTrue(all(w.passed for w in report.workspaces))


if __name__ == "__main__":
    unittest.main()
