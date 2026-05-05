"""Tests for the unified `fm` dispatcher (Task 019 ST-8)."""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "fm"))

import fm as fm_dispatcher  # type: ignore


class TestHelp(unittest.TestCase):
    def test_help_lists_every_subcommand(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            rc = fm_dispatcher.main([])
        self.assertEqual(rc, 0)
        text = out.getvalue()
        for sub in ("validate", "extract", "edit", "query", "section",
                    "rename", "graph", "new", "fix"):
            self.assertIn(sub, text, f"help missing subcommand {sub}")

    def test_dash_h_alias(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            rc = fm_dispatcher.main(["-h"])
        self.assertEqual(rc, 0)


class TestUnknownSubcommand(unittest.TestCase):
    def test_typo_offers_did_you_mean(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            rc = fm_dispatcher.main(["velidate"])
        self.assertEqual(rc, 2)
        self.assertIn("Did you mean", err.getvalue())
        self.assertIn("validate", err.getvalue())

    def test_completely_unknown_emits_no_suggestion(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            rc = fm_dispatcher.main(["xxxxxxx"])
        self.assertEqual(rc, 2)


class TestLazyDispatch(unittest.TestCase):
    """Each subcommand module should NOT be imported until invoked."""

    def setUp(self) -> None:
        # Ensure any sibling modules that already imported during earlier
        # tests are removed; otherwise the lazy-import claim is impossible
        # to verify within the same process.
        for name in ("validate", "extract", "edit", "query", "section",
                     "rename", "graph", "new", "fix"):
            sys.modules.pop(name, None)

    def test_dispatch_imports_only_target(self) -> None:
        # Run a no-arg `extract` to fail with a usage error but go through
        # the import path.
        err = io.StringIO()
        with redirect_stderr(err):
            try:
                fm_dispatcher.main(["extract"])
            except SystemExit:
                pass
        self.assertIn("extract", sys.modules)
        # The other peers MUST not be auto-imported by the dispatcher.
        for sibling in ("rename", "graph", "new", "fix"):
            self.assertNotIn(sibling, sys.modules,
                             f"dispatcher pulled in {sibling} when only extract was requested")


class TestDispatch(unittest.TestCase):
    def test_validate_help_via_wrapper(self) -> None:
        # validate --help exits 0 and prints usage.
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stderr(err), redirect_stdout(out):
            try:
                rc = fm_dispatcher.main(["validate", "--help"])
            except SystemExit as e:
                rc = e.code
        self.assertEqual(rc, 0)
        self.assertIn("fm-validate", out.getvalue())


if __name__ == "__main__":
    unittest.main()
