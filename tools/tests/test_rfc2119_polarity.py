"""Tests for tools/check-rfc2119-polarity.py (Task 032 ST-3)."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# The script's filename contains hyphens, so import it via spec_from_file_location.
_SPEC = importlib.util.spec_from_file_location(
    "check_rfc2119_polarity",
    REPO / "tools" / "check-rfc2119-polarity.py",
)
assert _SPEC and _SPEC.loader, "could not locate check-rfc2119-polarity.py"
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["check_rfc2119_polarity"] = _MOD
_SPEC.loader.exec_module(_MOD)  # type: ignore[union-attr]


def _write(tmpdir: Path, name: str, body: str) -> Path:
    p = tmpdir / name
    p.write_text(body, encoding="utf-8")
    return p


class TestPolarityHeuristic(unittest.TestCase):
    """End-to-end behaviour: catches inversions, ignores benign cases."""

    def test_synthetic_inversion_is_caught(self) -> None:
        """Two clauses on the same subject with opposite polarity → flag."""
        body = (
            "# Spec\n\n"
            "Agents MUST validate input payloads before dispatch.\n"
            "Agents MUST NOT validate input payloads before dispatch.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            pairs = _MOD.find_pairs(clauses, threshold=0.6)
            self.assertEqual(len(pairs), 1, msg=f"clauses={clauses}")
            pair = pairs[0]
            self.assertEqual(pair.must.polarity, "MUST")
            self.assertEqual(pair.must_not.polarity, "MUST NOT")
            diag = pair.diagnostic()
            # Both poles' file:line MUST appear, plus subject (AC #3).
            self.assertIn(f"{f}:3", diag)
            self.assertIn(f"{f}:4", diag)
            self.assertIn("WARN:RFC2119.POLARITY", diag)
            self.assertIn("validate", diag)

    def test_legitimate_negation_not_flagged(self) -> None:
        """Different subjects (validate X / log Y) → no pair emitted."""
        body = (
            "# Spec\n\n"
            "The agent MUST validate every input payload.\n"
            "The agent MUST NOT log secret credentials in plaintext.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            pairs = _MOD.find_pairs(clauses, threshold=0.6)
            self.assertEqual(pairs, [], msg=f"unexpected pairs: {pairs}")

    def test_keyword_inside_fenced_codeblock_skipped(self) -> None:
        """MUST/MUST NOT inside ``` fences is ignored (false-positive vector)."""
        body = (
            "# Spec\n\n"
            "```\n"
            "if cond: MUST validate input payloads now\n"
            "else: MUST NOT validate input payloads now\n"
            "```\n"
            "Body prose continues with no normative keywords.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            self.assertEqual(clauses, [], msg=f"clauses leaked: {clauses}")

    def test_tilde_fence_also_skipped(self) -> None:
        body = (
            "~~~yaml\n"
            "rule: MUST do thing\n"
            "anti: MUST NOT do thing\n"
            "~~~\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            self.assertEqual(clauses, [])

    def test_table_row_is_skipped(self) -> None:
        """Glossary tables list MUST/MUST NOT side-by-side legitimately."""
        body = (
            "| Keyword | Meaning |\n"
            "| --- | --- |\n"
            "| MUST | absolute requirement on the rule |\n"
            "| MUST NOT | absolute prohibition on the rule |\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            self.assertEqual(clauses, [])

    def test_rfc2119_boilerplate_skipped(self) -> None:
        body = (
            "The key words MUST, MUST NOT, SHOULD are to be interpreted\n"
            "as described in BCP 14 RFC 2119 RFC 8174.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            self.assertEqual(clauses, [])


class TestSubjectExtraction(unittest.TestCase):
    def test_normalise_strips_markdown_and_stopwords(self) -> None:
        tokens = _MOD._normalise_tokens("**The** `agent` MUST validate the input")
        # 'the', 'must' (uppercase only matched in keyword regex) — and the
        # word 'must' here, lowercased, is NOT in stopwords on purpose. We
        # check the load-bearing tokens survive.
        self.assertIn("agent", tokens)
        self.assertIn("validate", tokens)
        self.assertIn("input", tokens)
        self.assertNotIn("the", tokens)

    def test_jaccard_threshold_below_does_not_pair(self) -> None:
        body = (
            "Agents MUST validate one specific edge case here.\n"
            "Agents MUST NOT cache totally unrelated downstream results.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            clauses = _MOD.scan_file(f)
            pairs = _MOD.find_pairs(clauses, threshold=0.6)
            self.assertEqual(pairs, [])


class TestCli(unittest.TestCase):
    def test_main_exits_zero_with_findings(self) -> None:
        """The linter is advisory; even with WARN findings exit is 0 (AC)."""
        body = (
            "Agents MUST validate input payloads.\n"
            "Agents MUST NOT validate input payloads.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            f = _write(Path(td), "spec.md", body)
            rc = _MOD.main([str(f)])
            self.assertEqual(rc, 0)

    def test_main_exits_one_on_missing_target(self) -> None:
        rc = _MOD.main(["/nonexistent/path/that/does/not/exist.md"])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
