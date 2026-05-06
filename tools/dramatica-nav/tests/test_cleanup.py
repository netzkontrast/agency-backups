"""Tests for tools/dramatica-nav/cleanup.py (Task 030 ST-6).

Coverage budget per the subtask brief (Acceptance Criterion 3):

- 4 rules x (check + auto-fix paths) = 8 tests
- 1 ``--baseline`` round-trip
- 1 uncategorised-friction case (a non-rule corruption surfaced as a
  manual diagnostic, not as a regex band-aid)
- 1 catalogue-cap invariant (``len(RULES) == 4``)
- A handful of CLI / idempotency smoke tests for Acceptance #1 and #5

Total: well above the >=10 floor.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# conftest.py adds tools/dramatica-nav to sys.path
import cleanup  # noqa: E402


# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------

def _make_corpus(tmp_path: Path, file_text: dict[str, str]) -> Path:
    """Create a synthetic ``references/`` tree under ``tmp_path``."""

    refs = tmp_path / "references"
    refs.mkdir()
    for name, body in file_text.items():
        (refs / name).write_text(body, encoding="utf-8")
    return refs


def _run_check(refs: Path) -> list[cleanup.Diagnostic]:
    return cleanup.run_check(files=cleanup.iter_target_files([refs]))


def _run_apply(refs: Path) -> tuple[dict[Path, str], dict[str, int]]:
    return cleanup.run_apply(files=cleanup.iter_target_files([refs]))


# -------------------------------------------------------------------------
# Catalogue invariant
# -------------------------------------------------------------------------

def test_rules_locked_at_four():
    """Catalogue cap: exactly four rules. Adding a fifth requires an ADR."""

    assert len(cleanup.RULES) == 4
    ids = {r.rule_id for r in cleanup.RULES}
    assert ids == {
        "DR-CLEAN-001",
        "DR-CLEAN-002",
        "DR-CLEAN-003",
        "DR-CLEAN-004",
    }
    # DR-CLEAN-004 stays NON-AUTO-FIX.
    by_id = {r.rule_id: r for r in cleanup.RULES}
    assert by_id["DR-CLEAN-004"].auto_fix is False
    for rid in ("DR-CLEAN-001", "DR-CLEAN-002", "DR-CLEAN-003"):
        assert by_id[rid].auto_fix is True


# -------------------------------------------------------------------------
# DR-CLEAN-001 copyright-footer
# -------------------------------------------------------------------------

DR1_FILE = """\
# Demo

Body line one.

Copyright (c) 2001 Screenplay Systems Inc. All rights reserved.

42.

Body line two.
"""


def test_dr_clean_001_check_flags_copyright(tmp_path):
    refs = _make_corpus(tmp_path, {"a.md": DR1_FILE})
    diags = _run_check(refs)
    rule_hits = [d for d in diags if d.rule_id == "DR-CLEAN-001"]
    assert len(rule_hits) == 1
    assert "Copyright (c) 2001 Screenplay Systems Inc." in rule_hits[0].excerpt


def test_dr_clean_001_apply_strips_copyright_block(tmp_path):
    refs = _make_corpus(tmp_path, {"a.md": DR1_FILE})
    _run_apply(refs)
    rewritten = (refs / "a.md").read_text(encoding="utf-8")
    assert "Copyright" not in rewritten
    assert "42." not in rewritten  # trailing page number swallowed
    assert "Body line one." in rewritten
    assert "Body line two." in rewritten
    # Idempotent.
    assert _run_check(refs) == []


# -------------------------------------------------------------------------
# DR-CLEAN-002 page-number-only
# -------------------------------------------------------------------------

DR2_FILE = """\
# Demo

Paragraph A.

26.

Paragraph B.

1. Real list item one
2. Real list item two

Paragraph C.
"""


def test_dr_clean_002_check_flags_orphan_page_number(tmp_path):
    refs = _make_corpus(tmp_path, {"b.md": DR2_FILE})
    diags = _run_check(refs)
    rule_hits = [d for d in diags if d.rule_id == "DR-CLEAN-002"]
    # Only the orphan "26." line should fire — the "1." / "2." numbered
    # list items have non-empty content after the digit and are excluded
    # by the regex itself.
    assert len(rule_hits) == 1
    assert rule_hits[0].excerpt.strip() == "26."


def test_dr_clean_002_apply_collapses_blanks(tmp_path):
    refs = _make_corpus(tmp_path, {"b.md": DR2_FILE})
    _run_apply(refs)
    rewritten = (refs / "b.md").read_text(encoding="utf-8")
    assert "26." not in rewritten
    # The numbered list survives.
    assert "1. Real list item one" in rewritten
    assert "2. Real list item two" in rewritten
    # No triple-blank sequence introduced.
    assert "\n\n\n\n" not in rewritten
    # Idempotent.
    assert _run_check(refs) == []


# -------------------------------------------------------------------------
# DR-CLEAN-003 double-apostrophe
# -------------------------------------------------------------------------

DR3_FILE = """\
# Demo

The character''s motivation drives the plot.

Another character''s growth is the crux.
"""


def test_dr_clean_003_check_flags_double_apostrophe(tmp_path):
    refs = _make_corpus(tmp_path, {"c.md": DR3_FILE})
    diags = _run_check(refs)
    rule_hits = [d for d in diags if d.rule_id == "DR-CLEAN-003"]
    assert len(rule_hits) == 2


def test_dr_clean_003_apply_replaces_double_apostrophe(tmp_path):
    refs = _make_corpus(tmp_path, {"c.md": DR3_FILE})
    _run_apply(refs)
    rewritten = (refs / "c.md").read_text(encoding="utf-8")
    assert "''" not in rewritten
    assert "character's" in rewritten
    assert _run_check(refs) == []


# -------------------------------------------------------------------------
# DR-CLEAN-004 see-x-empty-redirect
# -------------------------------------------------------------------------

DR4_FILE = """\
# Demo

## Female Mental Sex

See Intuitive Problem Solving Style

## Real Term

Substantive paragraph one explaining the term carefully.

Substantive paragraph two extending the explanation.

Substantive paragraph three with additional detail.
"""


def test_dr_clean_004_check_flags_empty_redirect(tmp_path):
    refs = _make_corpus(tmp_path, {"d.md": DR4_FILE})
    diags = _run_check(refs)
    rule_hits = [d for d in diags if d.rule_id == "DR-CLEAN-004"]
    assert len(rule_hits) == 1
    assert "Female Mental Sex" in rule_hits[0].excerpt
    assert "See Intuitive" in rule_hits[0].excerpt


def test_dr_clean_004_apply_does_not_auto_fix(tmp_path):
    refs = _make_corpus(tmp_path, {"d.md": DR4_FILE})
    before = (refs / "d.md").read_text(encoding="utf-8")
    _run_apply(refs)
    after = (refs / "d.md").read_text(encoding="utf-8")
    # NON-AUTO-FIX: file is untouched on the see-redirect axis.
    assert before == after
    # The diagnostic is still present after --apply.
    diags = _run_check(refs)
    rule_hits = [d for d in diags if d.rule_id == "DR-CLEAN-004"]
    assert len(rule_hits) == 1


# -------------------------------------------------------------------------
# --baseline round-trip
# -------------------------------------------------------------------------

def test_baseline_round_trip(tmp_path, monkeypatch):
    """``--baseline`` writes a JSON file matching ``run_check`` output."""

    refs = _make_corpus(tmp_path, {
        "a.md": DR1_FILE,
        "b.md": DR2_FILE,
        "c.md": DR3_FILE,
        "d.md": DR4_FILE,
    })
    monkeypatch.setattr(cleanup, "VOCAB_DIR", refs)
    monkeypatch.setattr(cleanup, "THEORY_DIR", tmp_path / "missing")

    out = tmp_path / "baseline.json"
    rc = cleanup.main(["--baseline", "--output", str(out)])
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    # DR1_FILE contributes one DR-CLEAN-001 + one orphan "42." page-number;
    # DR2_FILE contributes one orphan "26.". DR3 contributes 2 apostrophes;
    # DR4 contributes 1 see-redirect.
    assert payload["per_rule"]["DR-CLEAN-001"] == 1
    assert payload["per_rule"]["DR-CLEAN-002"] == 2
    assert payload["per_rule"]["DR-CLEAN-003"] == 2
    assert payload["per_rule"]["DR-CLEAN-004"] == 1
    assert payload["total"] == 6

    # Round-trip: re-run check and compare counts.
    diags = _run_check(refs)
    counts: dict[str, int] = {}
    for d in diags:
        counts[d.rule_id] = counts.get(d.rule_id, 0) + 1
    assert counts == payload["per_rule"]


# -------------------------------------------------------------------------
# Uncategorised friction
# -------------------------------------------------------------------------

def test_uncategorised_corruption_does_not_silently_match(tmp_path):
    """A novel corruption class (broken-paren heading) MUST NOT be silently
    matched by any of the four locked rules.

    Per the subtask brief: cleanup.py refuses to grow without an ADR.
    Surfacing such cases as ``DR-CLEAN-UNCATEGORISED`` is the documented
    path; emitting a regex band-aid is forbidden. This test guards against
    accidentally inheriting a broken heading via a too-broad rule.
    """

    text = """\
# Demo

## Sex)

Body content describing a broken heading parenthesis. This is the
ST-2 corruption class; it is NOT covered by the v0.1 catalogue.
"""
    refs = _make_corpus(tmp_path, {"e.md": text})
    diags = _run_check(refs)
    # Zero hits — the catalogue is intentionally narrow.
    assert diags == [], (
        "An uncategorised corruption was matched by one of the locked "
        "rules. Adding coverage for it requires an agency-adr ADR."
    )


# -------------------------------------------------------------------------
# CLI surface + idempotency (Acceptance #1 + #5)
# -------------------------------------------------------------------------

CLEANUP_PY = (
    Path(__file__).resolve().parents[1] / "cleanup.py"
)


def _run_cli(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLEANUP_PY), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )


def test_cli_check_clean_corpus_exits_zero():
    """Post-Phase-A the canonical corpus is clean — ``--check`` exit 0."""

    proc = _run_cli(["--check"])
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_cli_explain_prints_rationale():
    proc = _run_cli(["--explain", "DR-CLEAN-002"])
    assert proc.returncode == 0
    assert "DR-CLEAN-002" in proc.stdout
    assert "page-number-only" in proc.stdout
    assert "rationale" in proc.stdout


def test_cli_explain_unknown_rule_errors():
    proc = _run_cli(["--explain", "DR-CLEAN-999"])
    assert proc.returncode == 2
    assert "unknown rule" in proc.stderr


def test_cli_apply_dry_run_does_not_write(tmp_path, monkeypatch):
    """``--apply --dry-run`` emits a diff but leaves files untouched."""

    refs = _make_corpus(tmp_path, {"a.md": DR1_FILE})
    monkeypatch.setattr(cleanup, "VOCAB_DIR", refs)
    monkeypatch.setattr(cleanup, "THEORY_DIR", tmp_path / "missing")

    before = (refs / "a.md").read_text(encoding="utf-8")
    rc = cleanup.main(["--apply", "--dry-run"])
    after = (refs / "a.md").read_text(encoding="utf-8")
    assert before == after
    # Exit 0 because no NON-AUTO-FIX hits remain (DR-CLEAN-004 absent).
    assert rc == 0


def test_apply_then_check_is_idempotent(tmp_path, monkeypatch):
    """Acceptance #5: ``--apply`` followed by ``--check`` -> zero hits."""

    refs = _make_corpus(tmp_path, {
        "a.md": DR1_FILE,
        "b.md": DR2_FILE,
        "c.md": DR3_FILE,
    })
    monkeypatch.setattr(cleanup, "VOCAB_DIR", refs)
    monkeypatch.setattr(cleanup, "THEORY_DIR", tmp_path / "missing")

    rc_apply = cleanup.main(["--apply"])
    assert rc_apply == 0
    diags = cleanup.run_check(files=cleanup.iter_target_files([refs]))
    assert diags == []
    rc_check = cleanup.main(["--check"])
    # main() walks the canonical roots — but VOCAB_DIR is monkeypatched, so
    # this --check now also walks the synthetic refs and confirms zero.
    assert rc_check == 0


def test_dry_run_requires_apply(tmp_path):
    """``--dry-run`` standalone is rejected (mutex with --check etc.)."""

    proc = _run_cli(["--check", "--dry-run"])
    assert proc.returncode != 0
    assert "--dry-run requires --apply" in proc.stderr


def test_excluded_files_are_skipped(tmp_path, monkeypatch):
    """``_synonym-lookup.md`` and ``dynamic-pairs-index.md`` are excluded."""

    refs = _make_corpus(tmp_path, {
        "_synonym-lookup.md": DR3_FILE,
        "dynamic-pairs-index.md": DR3_FILE,
        "real-file.md": DR3_FILE,
    })
    files = cleanup.iter_target_files([refs])
    names = {p.name for p in files}
    assert names == {"real-file.md"}
