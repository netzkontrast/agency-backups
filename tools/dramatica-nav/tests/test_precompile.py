"""Tests for precompile.py — schema validation, idempotency, benchmark sanity."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import precompile  # type: ignore  # navigator dir is on sys.path via conftest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def schema(repo_root: Path) -> dict:
    schema_path = (
        repo_root / "maintenance" / "schemas" / "narrative-ontology"
        / "precompiled.schema.json"
    )
    return json.loads(schema_path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def scenarios(repo_root: Path) -> list[dict]:
    sc_path = (
        repo_root / "maintenance" / "schemas" / "narrative-ontology" / "scenarios.json"
    )
    return json.loads(sc_path.read_text(encoding="utf-8"))["scenarios"]


@pytest.fixture(scope="module")
def precompiled_dir(repo_root: Path) -> Path:
    return repo_root / "maintenance" / "schemas" / "narrative-ontology" / "precompiled"


@pytest.fixture
def emitted_bundle(canonical_index, scenarios, tmp_path, monkeypatch):
    """Emit a single bundle into a tmp dir and return (path, parsed_json)."""
    monkeypatch.setattr(precompile, "_PRECOMPILED_DIR", tmp_path)
    target = next(s for s in scenarios if s["id"] == "novel.crucial-element-audit")
    path = precompile.emit_one(target, canonical_index, generated_at="2026-05-06")
    return path, json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Schema-validation tests
# ---------------------------------------------------------------------------

def test_schema_loads_and_is_draft_2020_12(schema):
    """Test 1: precompiled.schema.json is well-formed Draft 2020-12."""
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["title"].startswith("Narrative Ontology")
    assert schema["additionalProperties"] is False
    # Schema must validate itself against its declared meta-schema (smoke test).
    Draft202012Validator.check_schema(schema)


def test_emitted_bundle_passes_schema(schema, emitted_bundle):
    """Test 2: a freshly emitted bundle passes precompiled.schema.json."""
    _, bundle = emitted_bundle
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(bundle))
    assert not errors, f"schema errors: {[e.message for e in errors[:3]]}"
    # Required top-level keys are present.
    for key in (
        "schema_version", "scenario_id", "scenario_summary", "persona",
        "generated_from_ontology_version", "generated_at",
        "primary_terms", "primary_quads", "primary_pairs", "consumer_hints",
    ):
        assert key in bundle


def test_all_eleven_canonical_artefacts_pass_schema(schema, precompiled_dir):
    """Test 3: every canonical *.json under precompiled/ validates."""
    if not precompiled_dir.exists():
        pytest.skip("precompiled/ directory not present (run emit-all first)")
    files = sorted(precompiled_dir.glob("*.json"))
    assert len(files) == 11, f"expected 11 bundles, got {len(files)}"
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for fp in files:
        data = json.loads(fp.read_text(encoding="utf-8"))
        errs = list(validator.iter_errors(data))
        if errs:
            failures.append(f"{fp.name}: {errs[0].message}")
    assert not failures, "\n".join(failures)


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------

def test_emit_one_is_byte_identical_when_repeated(canonical_index, scenarios, tmp_path, monkeypatch):
    """Test 4: emitting the same scenario twice yields byte-identical output."""
    monkeypatch.setattr(precompile, "_PRECOMPILED_DIR", tmp_path)
    target = next(s for s in scenarios if s["id"] == "novel.act-pivot")

    p1 = precompile.emit_one(target, canonical_index, generated_at="2026-05-06")
    bytes1 = p1.read_bytes()

    p2 = precompile.emit_one(target, canonical_index, generated_at="2026-05-06")
    bytes2 = p2.read_bytes()

    assert bytes1 == bytes2
    # Hash equality belt-and-braces.
    import hashlib
    assert hashlib.sha256(bytes1).hexdigest() == hashlib.sha256(bytes2).hexdigest()


# ---------------------------------------------------------------------------
# Benchmark sanity
# ---------------------------------------------------------------------------

def test_benchmark_average_meets_60pct_gate(canonical_index, precompiled_dir):
    """Test 5: average reduction across all 11 scenarios is <=60% (binding gate)."""
    if not precompiled_dir.exists():
        pytest.skip("precompiled/ directory not present (run emit-all first)")
    rows, avg = precompile.benchmark_all(canonical_index)
    assert avg <= 60.0, f"average {avg:.1f}% exceeds 60% gate; rows={rows}"
    # Sanity: no row reports zero precompiled bytes (means file missing).
    for sid, prose, pre, ratio, gate in rows:
        assert pre > 0, f"{sid} has 0 precompiled bytes — file missing?"
        assert prose > 0, f"{sid} has 0 prose-path bytes — index lookup failed?"


def test_synthesise_encoding_hint_handles_empty_input():
    """Test 6: synthesise_encoding_hint returns None for empty / metadata-only prose."""
    assert precompile.synthesise_encoding_hint(None, "Trust") is None
    assert precompile.synthesise_encoding_hint("", "Trust") is None
    # Only headings + metadata, no prose
    metadata_only = "## Trust\n*Type: Element / Element*\n\n**Opposite**: Test\n\n---\n"
    assert precompile.synthesise_encoding_hint(metadata_only, "Trust") is None


def test_synthesise_encoding_hint_caps_at_two_sentences():
    """Test 7: hint synthesis bounds output at <=2 sentences."""
    prose = (
        "## Trust\n*Type: Element*\n\n"
        "First sentence here. Second sentence is also short. "
        "Third sentence should be dropped. Fourth too.\n"
    )
    hint = precompile.synthesise_encoding_hint(prose, "Trust")
    assert hint is not None
    # No more than 2 sentences (rough check via terminal punctuation count).
    terminators = sum(hint.count(c) for c in ".!?")
    assert terminators <= 2, f"hint contains too many sentences: {hint!r}"
    assert "Third sentence" not in hint
