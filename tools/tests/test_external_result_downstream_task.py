"""Tests for tools/check-external-result-downstream-task.py — Task 035 ST-3.

Coverage per the brief at
prompts/tooling-external-result-downstream-task-linter/brief.md
§Acceptance Criteria:

  * linked Task via ``task_affects_paths`` (pass).
  * missing Task (fail with R.6.5 diagnostic).
  * differently-slugged Task linked via ``task_affects_paths`` (pass).
  * back-link via ``task_uses_prompts`` (pass).
  * back-link via ``task_spawns_research`` (pass).
  * non-result.md inputs are silent.
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
        "check_external_result_downstream_task",
        TOOLS / "check-external-result-downstream-task.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_external_result_downstream_task"] = module
    spec.loader.exec_module(module)
    return module


cerd = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cerd.main(argv)
    return rc, out.getvalue(), err.getvalue()


_RESULT_FM = textwrap.dedent(
    """\
    ---
    type: research
    status: completed
    slug: demo-result
    summary: "External result fixture."
    created: 2026-05-07
    updated: 2026-05-07
    research_phase: complete
    research_executes_prompt: demo-result
    research_friction_level: FL0
    ---

    # Result body
    """
)


def _write_result(provider_dir: Path, slug: str = "demo-result") -> Path:
    folder = provider_dir / slug
    folder.mkdir(parents=True, exist_ok=True)
    f = folder / "result.md"
    f.write_text(_RESULT_FM, encoding="utf-8")
    return f


def _write_task(tasks_dir: Path, *, name: str, body: str) -> Path:
    folder = tasks_dir / name
    folder.mkdir(parents=True, exist_ok=True)
    tm = folder / "task.md"
    tm.write_text(body, encoding="utf-8")
    return tm


@contextlib.contextmanager
def _fake_repo():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "research" / "gemini").mkdir(parents=True)
        (root / "tasks").mkdir()
        original_root = cerd.REPO_ROOT
        cerd.REPO_ROOT = root
        cwd = os.getcwd()
        os.chdir(root)
        try:
            yield root
        finally:
            cerd.REPO_ROOT = original_root
            os.chdir(cwd)


class ExternalResultDownstreamTask(unittest.TestCase):
    def test_no_results_is_silent(self) -> None:
        with _fake_repo() as root:
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 0, err)
            self.assertEqual(err, "")

    def test_missing_task_emits_error(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 1, err)
            self.assertIn("ERROR:R.6.5:no-downstream-task", err)
            self.assertIn("research/gemini/demo-result/result.md", err)

    def test_backlink_via_task_affects_paths_path(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            _write_task(
                root / "tasks",
                name="099-demo",
                body=textwrap.dedent(
                    """\
                    ---
                    type: task
                    status: active
                    slug: demo
                    summary: "demo"
                    created: 2026-05-07
                    updated: 2026-05-07
                    task_id: "099"
                    task_status: open
                    task_affects_paths:
                      - research/gemini/demo-result/result.md
                    ---

                    # Task 099
                    """
                ),
            )
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 0, err)

    def test_backlink_via_task_affects_paths_folder(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            _write_task(
                root / "tasks",
                name="099-demo",
                body=textwrap.dedent(
                    """\
                    ---
                    type: task
                    status: active
                    slug: demo
                    summary: "demo"
                    created: 2026-05-07
                    updated: 2026-05-07
                    task_id: "099"
                    task_status: open
                    task_affects_paths:
                      - research/gemini/demo-result/
                    ---

                    # Task 099
                    """
                ),
            )
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 0, err)

    def test_backlink_via_task_uses_prompts_slug(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            _write_task(
                root / "tasks",
                name="099-other-slug",
                body=textwrap.dedent(
                    """\
                    ---
                    type: task
                    status: active
                    slug: other-slug
                    summary: "demo"
                    created: 2026-05-07
                    updated: 2026-05-07
                    task_id: "099"
                    task_status: open
                    task_uses_prompts:
                      - demo-result
                    ---

                    # Task 099
                    """
                ),
            )
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 0, err)

    def test_backlink_via_task_spawns_research(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            _write_task(
                root / "tasks",
                name="099-other-slug",
                body=textwrap.dedent(
                    """\
                    ---
                    type: task
                    status: active
                    slug: other-slug
                    summary: "demo"
                    created: 2026-05-07
                    updated: 2026-05-07
                    task_id: "099"
                    task_status: open
                    task_spawns_research:
                      - gemini/demo-result
                    ---

                    # Task 099
                    """
                ),
            )
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 0, err)

    def test_unrelated_task_does_not_satisfy(self) -> None:
        with _fake_repo() as root:
            _write_result(root / "research" / "gemini")
            _write_task(
                root / "tasks",
                name="099-unrelated",
                body=textwrap.dedent(
                    """\
                    ---
                    type: task
                    status: active
                    slug: unrelated
                    summary: "demo"
                    created: 2026-05-07
                    updated: 2026-05-07
                    task_id: "099"
                    task_status: open
                    task_uses_prompts:
                      - some-other-prompt
                    ---

                    # Task 099
                    """
                ),
            )
            rc, _, err = _capture([str(root / "research")])
            self.assertEqual(rc, 1, err)
            self.assertIn("R.6.5", err)


if __name__ == "__main__":
    unittest.main()
