"""Tests for tools/fm/_core.py per-rule waiver mechanism (Task 037 ST-3).

Acceptance Criteria from
prompts/tooling-per-rule-waiver-mechanism/brief.md:
  - per-rule match
  - wildcard match (`*`)
  - expired waiver no longer applies
  - malformed row raises Diag
  - mixed legacy + new format rejected
  - migrate-waivers.py converts legacy → wildcard rows

Run: python3 -m pytest tools/tests/fm/test_per_rule_waivers.py
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import _core  # noqa: E402


def _load_migrate():
    spec = importlib.util.spec_from_file_location(
        "migrate_waivers",
        REPO / "tools" / "scripts" / "migrate-waivers.py",
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["migrate_waivers"] = mod
    spec.loader.exec_module(mod)
    return mod


migrate_mod = _load_migrate()


class _Tmp:
    """Temp repo with a tools/.frontmatter-waivers we control."""

    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "tools").mkdir()

    def write(self, content: str) -> Path:
        p = self.root / "tools" / ".frontmatter-waivers"
        p.write_text(content, encoding="utf-8")
        return p

    def __enter__(self) -> "_Tmp":
        return self

    def __exit__(self, *a) -> None:
        self.tmp.cleanup()


def _diag(path: str, code: str, severity: str = "ERROR") -> _core.Diagnostic:
    return _core.Diagnostic(
        path=path, line=1, severity=severity, code=code, message="x",
    )


class WaiverLoaderTests(unittest.TestCase):

    def test_absent_file_returns_empty(self) -> None:
        with _Tmp() as t:
            # No file written.
            self.assertEqual(_core.load_waivers(t.root), [])

    def test_per_rule_row_parses(self) -> None:
        with _Tmp() as t:
            t.write(
                "# header comment\n"
                "tasks/030-*/notes.md\tF.4.2\tTask 030 tracks repair\t2026-08-01\n"
            )
            ws = _core.load_waivers(t.root)
            self.assertEqual(len(ws), 1)
            self.assertEqual(ws[0].rule_id, "F.4.2")
            self.assertEqual(ws[0].path_glob, "tasks/030-*/notes.md")
            self.assertEqual(ws[0].expires, "2026-08-01")

    def test_wildcard_row_parses(self) -> None:
        with _Tmp() as t:
            t.write("research/x/output/SPEC.md\t*\trationale\t-\n")
            ws = _core.load_waivers(t.root)
            self.assertEqual(ws[0].rule_id, "*")
            self.assertEqual(ws[0].expires, "-")

    def test_header_row_skipped(self) -> None:
        with _Tmp() as t:
            t.write(
                "path-glob\trule-id\trationale\texpires\n"
                "a/b.md\tF.4.2\trat\t2026-12-31\n"
            )
            ws = _core.load_waivers(t.root)
            self.assertEqual(len(ws), 1)

    def test_malformed_column_count_raises(self) -> None:
        with _Tmp() as t:
            t.write("a\tb\tc\n")  # only 3 columns
            with self.assertRaises(_core.Diag):
                _core.load_waivers(t.root)

    def test_malformed_expiry_raises(self) -> None:
        with _Tmp() as t:
            t.write("a/b.md\tF.4.2\tr\tnext-tuesday\n")
            with self.assertRaises(_core.Diag):
                _core.load_waivers(t.root)

    def test_mixed_legacy_and_new_rejected(self) -> None:
        with _Tmp() as t:
            t.write(
                "legacy/path.md\n"
                "new/path.md\tF.4.2\trat\t2026-12-31\n"
            )
            with self.assertRaises(_core.Diag) as cm:
                _core.load_waivers(t.root)
            self.assertIn("mixed legacy", str(cm.exception))

    def test_legacy_only_rejected_with_migration_pointer(self) -> None:
        with _Tmp() as t:
            t.write("legacy/path.md\n")
            with self.assertRaises(_core.Diag) as cm:
                _core.load_waivers(t.root)
            self.assertIn("migrate-waivers.py", str(cm.exception))


class WaiverApplyTests(unittest.TestCase):

    def test_per_rule_match_drops_diag(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/b.md", rule_id="F.4.2",
            rationale="r", expires="-", line=1,
        )
        diags = [_diag("a/b.md", "F.4.2"), _diag("a/b.md", "F.5.1")]
        kept = _core.apply_waivers(diags, [w])
        self.assertEqual([d.code for d in kept], ["F.5.1"])

    def test_wildcard_drops_all_codes(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/b.md", rule_id="*",
            rationale="r", expires="-", line=1,
        )
        diags = [_diag("a/b.md", "F.4.2"), _diag("a/b.md", "F.5.1")]
        kept = _core.apply_waivers(diags, [w])
        self.assertEqual(kept, [])

    def test_path_glob_must_match(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/*.md", rule_id="F.4.2",
            rationale="r", expires="-", line=1,
        )
        # Wrong path: not matched.
        kept = _core.apply_waivers(
            [_diag("c/d.md", "F.4.2")], [w],
        )
        self.assertEqual(len(kept), 1)

    def test_expired_waiver_does_not_apply(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/b.md", rule_id="F.4.2",
            rationale="r", expires="2024-01-01", line=1,
        )
        diags = [_diag("a/b.md", "F.4.2")]
        # today > expires → waiver inactive
        kept = _core.apply_waivers(diags, [w], today="2026-01-01")
        self.assertEqual(len(kept), 1)

    def test_unexpired_waiver_applies(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/b.md", rule_id="F.4.2",
            rationale="r", expires="2099-01-01", line=1,
        )
        diags = [_diag("a/b.md", "F.4.2")]
        kept = _core.apply_waivers(diags, [w], today="2026-01-01")
        self.assertEqual(kept, [])

    def test_no_expiry_dash_always_applies(self) -> None:
        w = _core.WaiverEntry(
            path_glob="a/b.md", rule_id="F.4.2",
            rationale="r", expires="-", line=1,
        )
        diags = [_diag("a/b.md", "F.4.2")]
        kept = _core.apply_waivers(diags, [w], today="2099-12-31")
        self.assertEqual(kept, [])

    def test_adr_diagnostic_codes_accepted(self) -> None:
        # Per ST-3 brief: ADR.A.* codes from §7.C must be valid rule-ids.
        w = _core.WaiverEntry(
            path_glob="decisions/0001-*.md", rule_id="ADR.A.3.5",
            rationale="r", expires="-", line=1,
        )
        diags = [
            _diag("decisions/0001-foo.md", "ADR.A.3.5"),
            _diag("decisions/0001-foo.md", "ADR.A.4.5"),
        ]
        kept = _core.apply_waivers(diags, [w])
        self.assertEqual([d.code for d in kept], ["ADR.A.4.5"])


class MigrateWaiversTests(unittest.TestCase):

    def test_legacy_row_promoted_to_wildcard(self) -> None:
        legacy = "legacy/path.md\nresearch/foo/output/SPEC.md\n"
        out = migrate_mod.migrate(legacy, today="2026-05-07")
        # Legacy rows became wildcards.
        self.assertIn("legacy/path.md\t*\t", out)
        self.assertIn("research/foo/output/SPEC.md\t*\t", out)
        # 90-day expiry computed.
        self.assertIn("2026-08-05", out)

    def test_already_migrated_row_passes_through(self) -> None:
        already = "a/b.md\tF.4.2\trat\t2026-12-31\n"
        out = migrate_mod.migrate(already, today="2026-05-07")
        self.assertIn("a/b.md\tF.4.2\trat\t2026-12-31", out)

    def test_comments_dropped_from_migration(self) -> None:
        text = "# old comment\nlegacy/path.md\n"
        out = migrate_mod.migrate(text, today="2026-05-07")
        self.assertNotIn("old comment", out)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
