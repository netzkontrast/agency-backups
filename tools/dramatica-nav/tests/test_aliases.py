"""Tests for tools/dramatica-nav/aliases.py — Task 030 ST-7.

Coverage matrix (Acceptance §6, ≥6 tests):

  Parse (1):
    - test_parse_synonym_lookup_extracts_rows

  Resolve (2):
    - test_resolve_unique_label_to_oid
    - test_resolve_alias_uniqueness_conflict_surfaces_not_resolves

  Project (2):
    - test_load_en_projects_into_table_and_frontmatter
    - test_load_de_projects_from_json

  Idempotency (1):
    - test_load_en_idempotent_on_rerun

  Conflict report (1):
    - test_conflict_report_lists_blocking_rows

  CRUD (1):
    - test_add_then_remove_round_trip

The harness builds a tiny self-contained ontology + vocabulary tree under
``tmp_path`` and monkeypatches the module-level path constants so the loader
operates on it without touching the canonical corpus.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

NAV_DIR = Path(__file__).resolve().parent.parent

# Load aliases.py as a module — its parent has a hyphen so it isn't a valid
# Python package name. ``conftest.py`` already places NAV_DIR on sys.path.
spec = importlib.util.spec_from_file_location("aliases_module", NAV_DIR / "aliases.py")
aliases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aliases)  # type: ignore[union-attr]


SYNONYM_FIXTURE = """\
# Synonym Lookup

Common everyday words → canonical Dramatica term and where it's defined.

---

## A

- `accept` → **Trust** (in `elements.md`)
- `audit` → **Test** (in `elements.md`)
- `arc` → **see Resolve / Growth** (in `dramatica-fundamentals.md`)
- `archetype` → **Archetype** (in `archetypes.md`)
- `ability to consider` → **Conscience** (in `elements.md`) / **Contagonist** (in `archetypes.md`)

## B

- `back` → **Support** (in `elements.md`)

## V

- `valid` → **Trust** (in `elements.md`)
"""


def _build_fake_repo(tmp_path: Path) -> Path:
    """Build a self-contained ontology + vocab tree.

    Layout mirrors what aliases.py expects:
      maintenance/schemas/narrative-ontology/{ontology,term-frontmatter}.json
      skills/dramatica-vocabulary/references/{elements,archetypes}.md
    """
    onto_dir = tmp_path / "maintenance/schemas/narrative-ontology"
    onto_dir.mkdir(parents=True)
    vocab = tmp_path / "skills/dramatica-vocabulary/references"
    vocab.mkdir(parents=True)

    ontology_doc = {
        "schema_version": "1.0.0",
        "ontology_version": "0.0.1",
        "entries": [
            {
                "id": "el.trust",
                "kind": "element",
                "canonical_label": "Trust",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/elements.md#trust",
            },
            {
                "id": "el.test",
                "kind": "element",
                "canonical_label": "Test",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/elements.md#test",
            },
            {
                "id": "el.support",
                "kind": "element",
                "canonical_label": "Support",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/elements.md#support",
            },
            {
                "id": "el.conscience",
                "kind": "element",
                "canonical_label": "Conscience",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/elements.md#conscience",
            },
            {
                "id": "arc.contagonist",
                "kind": "archetype",
                "canonical_label": "Contagonist",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/archetypes.md#contagonist",
            },
        ],
    }
    (onto_dir / "ontology.json").write_text(
        json.dumps(ontology_doc, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Minimal but real schema: only checks pattern + alias type/unique.
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["id", "kind", "canonical_label", "provenance"],
        "properties": {
            "id": {"type": "string"},
            "kind": {"type": "string"},
            "canonical_label": {"type": "string"},
            "provenance": {"type": "string"},
            "term_file": {"type": "string"},
        },
        "patternProperties": {
            "^aliases_[a-z]{2}$": {
                "type": "array",
                "items": {"type": "string", "minLength": 1, "maxLength": 80},
                "uniqueItems": True,
            }
        },
        "additionalProperties": True,
    }
    (onto_dir / "term-frontmatter.schema.json").write_text(
        json.dumps(schema), encoding="utf-8"
    )

    elements_md = (
        "# Elements\n\n"
        "## Trust\n"
        "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->\n"
        "```yaml\n"
        "id: el.trust\n"
        "kind: element\n"
        "canonical_label: Trust\n"
        "provenance: source-original\n"
        "```\n\n"
        "Body of trust.\n\n"
        "## Test\n"
        "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->\n"
        "```yaml\n"
        "id: el.test\n"
        "kind: element\n"
        "canonical_label: Test\n"
        "provenance: source-original\n"
        "```\n\n"
        "## Support\n"
        "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->\n"
        "```yaml\n"
        "id: el.support\n"
        "kind: element\n"
        "canonical_label: Support\n"
        "provenance: source-original\n"
        "```\n\n"
        "## Conscience\n"
        "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->\n"
        "```yaml\n"
        "id: el.conscience\n"
        "kind: element\n"
        "canonical_label: Conscience\n"
        "provenance: source-original\n"
        "```\n"
    )
    (vocab / "elements.md").write_text(elements_md, encoding="utf-8")

    archetypes_md = (
        "# Archetypes\n\n"
        "## Contagonist\n"
        "<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->\n"
        "```yaml\n"
        "id: arc.contagonist\n"
        "kind: archetype\n"
        "canonical_label: Contagonist\n"
        "provenance: source-original\n"
        "```\n"
    )
    (vocab / "archetypes.md").write_text(archetypes_md, encoding="utf-8")

    return tmp_path


@pytest.fixture
def fake_repo(tmp_path: Path, monkeypatch) -> Path:
    repo = _build_fake_repo(tmp_path)
    # Redirect the module-level path constants to the fake repo.
    monkeypatch.setattr(aliases, "REPO_ROOT", repo)
    monkeypatch.setattr(
        aliases,
        "ONTOLOGY_PATH",
        repo / "maintenance/schemas/narrative-ontology/ontology.json",
    )
    monkeypatch.setattr(
        aliases,
        "TERM_SCHEMA_PATH",
        repo / "maintenance/schemas/narrative-ontology/term-frontmatter.schema.json",
    )
    monkeypatch.setattr(
        aliases,
        "VOCAB_DIR",
        repo / "skills/dramatica-vocabulary/references",
    )
    monkeypatch.setattr(
        aliases,
        "SYNONYM_LOOKUP",
        repo / "skills/dramatica-vocabulary/references/_synonym-lookup.md",
    )
    return repo


@pytest.fixture
def synonym_file(fake_repo: Path) -> Path:
    p = fake_repo / "skills/dramatica-vocabulary/references/_synonym-lookup.md"
    p.write_text(SYNONYM_FIXTURE, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Pass 1 — parse
# ---------------------------------------------------------------------------


def test_parse_synonym_lookup_extracts_rows():
    rows = aliases.parse_synonym_lookup(SYNONYM_FIXTURE)
    aliases_seen = {r["alias"] for r in rows}
    # `arc` resolves to a `see ...` cross-reference; should be skipped.
    assert "arc" not in aliases_seen
    assert {"accept", "audit", "archetype", "ability to consider", "back", "valid"} <= aliases_seen
    # The multi-target row keeps both targets.
    multi = next(r for r in rows if r["alias"] == "ability to consider")
    assert len(multi["targets"]) == 2
    assert ("Conscience", "elements.md") in multi["targets"]
    assert ("Contagonist", "archetypes.md") in multi["targets"]


# ---------------------------------------------------------------------------
# Pass 2 — resolve
# ---------------------------------------------------------------------------


def test_resolve_unique_label_to_oid(fake_repo: Path):
    entries = aliases._load_ontology_entries()
    li = aliases.build_label_index(entries)
    status, oids = aliases.resolve_target("Trust", "elements.md", li)
    assert status == "ok"
    assert oids == ["el.trust"]


def test_resolve_alias_uniqueness_conflict_surfaces_not_resolves(fake_repo: Path):
    """`ability to consider` resolves to two distinct ontology IDs — a
    classic alias-uniqueness conflict. The resolver MUST surface it as a
    conflict and project nothing for that row.
    """
    rows = aliases.parse_synonym_lookup(SYNONYM_FIXTURE)
    entries = aliases._load_ontology_entries()
    li = aliases.build_label_index(entries)
    res = aliases.build_reserved_alias_index(entries, "en")
    proj, conflicts, _ = aliases.resolve_rows(rows, li, res)
    conflict_aliases = {c["alias"] for c in conflicts if not c.get("partial")}
    assert "ability to consider" in conflict_aliases
    assert "ability to consider" not in {a for s in proj.values() for a in s}


# ---------------------------------------------------------------------------
# Pass 3 — project (load-en + load-de)
# ---------------------------------------------------------------------------


def test_load_en_projects_into_table_and_frontmatter(fake_repo: Path, synonym_file: Path):
    rc = aliases.main(["load-en", "--source", str(synonym_file)])
    assert rc == 0

    # Ontology table updated.
    doc = json.loads((fake_repo / "maintenance/schemas/narrative-ontology/ontology.json").read_text())
    by_id = {e["id"]: e for e in doc["entries"]}
    assert "accept" in by_id["el.trust"].get("aliases_en", [])
    assert "valid" in by_id["el.trust"].get("aliases_en", [])
    assert "audit" in by_id["el.test"].get("aliases_en", [])
    assert "back" in by_id["el.support"].get("aliases_en", [])
    # Conflicting row produced no projection.
    assert "ability to consider" not in by_id["el.conscience"].get("aliases_en", [])
    assert "ability to consider" not in by_id["arc.contagonist"].get("aliases_en", [])

    # Per-term frontmatter updated.
    text = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    assert "- accept" in text
    assert "- audit" in text


def test_load_de_projects_from_json(fake_repo: Path):
    de_src = fake_repo / "aliases_de_starter.json"
    de_src.write_text(json.dumps({"el.trust": ["Vertrauen"], "el.test": ["Prüfung"]}), encoding="utf-8")

    rc = aliases.main(["load-de", "--source", str(de_src)])
    assert rc == 0

    doc = json.loads((fake_repo / "maintenance/schemas/narrative-ontology/ontology.json").read_text())
    by_id = {e["id"]: e for e in doc["entries"]}
    assert "Vertrauen" in by_id["el.trust"].get("aliases_de", [])
    assert "Prüfung" in by_id["el.test"].get("aliases_de", [])

    text = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    assert "Vertrauen" in text
    assert "Prüfung" in text


def test_load_de_rejects_unknown_oid(fake_repo: Path):
    de_src = fake_repo / "bad_de.json"
    de_src.write_text(json.dumps({"el.bogus": ["Erfunden"]}), encoding="utf-8")
    rc = aliases.main(["load-de", "--source", str(de_src)])
    assert rc == 1


def test_load_de_skips_underscore_metadata(fake_repo: Path):
    """Top-level keys starting with `_` (e.g. `_comment`) are tolerated as
    JSON metadata and never treated as ontology IDs.
    """
    de_src = fake_repo / "with_meta.json"
    de_src.write_text(
        json.dumps({"_comment": "hand-curated; see notes", "el.trust": ["Vertrauen"]}),
        encoding="utf-8",
    )
    rc = aliases.main(["load-de", "--source", str(de_src)])
    assert rc == 0


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_load_en_idempotent_on_rerun(fake_repo: Path, synonym_file: Path):
    rc = aliases.main(["load-en", "--source", str(synonym_file)])
    assert rc == 0

    onto = fake_repo / "maintenance/schemas/narrative-ontology/ontology.json"
    elements = fake_repo / "skills/dramatica-vocabulary/references/elements.md"
    onto_before = onto.read_bytes()
    elements_before = elements.read_bytes()

    rc = aliases.main(["load-en", "--source", str(synonym_file)])
    assert rc == 0
    assert onto.read_bytes() == onto_before
    assert elements.read_bytes() == elements_before


# ---------------------------------------------------------------------------
# Conflict report
# ---------------------------------------------------------------------------


def test_conflict_report_lists_blocking_rows(
    fake_repo: Path, synonym_file: Path, capsys
):
    rc = aliases.main(["conflict-report", "--source", str(synonym_file)])
    # Exit 1 because we have a blocking alias-uniqueness conflict.
    assert rc == 1
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["conflict_count"] >= 1
    aliases_in_conflict = {c["alias"] for c in payload["conflicts"]}
    assert "ability to consider" in aliases_in_conflict


# ---------------------------------------------------------------------------
# CRUD (add/remove/list)
# ---------------------------------------------------------------------------


def test_add_then_remove_round_trip(fake_repo: Path):
    onto_path = fake_repo / "maintenance/schemas/narrative-ontology/ontology.json"

    rc = aliases.main(
        ["add", "--id", "el.trust", "--locale", "en", "--value", "rely on"]
    )
    assert rc == 0
    doc = json.loads(onto_path.read_text())
    by_id = {e["id"]: e for e in doc["entries"]}
    assert "rely on" in by_id["el.trust"]["aliases_en"]

    rc = aliases.main(
        ["remove", "--id", "el.trust", "--locale", "en", "--value", "rely on"]
    )
    assert rc == 0
    doc = json.loads(onto_path.read_text())
    by_id = {e["id"]: e for e in doc["entries"]}
    # Either the field is gone (empty list cleaned up) or the value is gone.
    assert "rely on" not in by_id["el.trust"].get("aliases_en", [])


def test_list_emits_locale_filtered_aliases(fake_repo: Path, capsys):
    rc = aliases.main(
        ["add", "--id", "el.trust", "--locale", "de", "--value", "Vertrauen"]
    )
    assert rc == 0
    capsys.readouterr()  # drain

    rc = aliases.main(["list", "--id", "el.trust", "--locale", "de"])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload == {"aliases_de": ["Vertrauen"]}
