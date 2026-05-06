"""Tests for tools/dramatica-nav/term.py — Task 030 ST-5.

Coverage matrix (Acceptance §2):

  Happy paths (4):
    - test_create_happy
    - test_edit_happy
    - test_move_happy
    - test_deprecate_alias_on_happy

  Edge cases (4):
    - test_create_duplicate_id            (refused without --force)
    - test_create_missing_file            (exit 3)
    - test_move_no_clean_break            (refused on collision without --force)
    - test_deprecate_without_alias_on     (schema-bump-required exit 5)

  Integration (1):
    - test_integration_sequence           (create → edit → move → deprecate)

The post-mutation gate (which spawns ``ontology-build.py --check-only`` +
``validate.py``) is monkeypatched to a no-op in every test so the tests work
against a self-contained tmp repo without dragging in the canonical corpus.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

NAV_DIR = Path(__file__).resolve().parent.parent

# Load term.py as a module — the parent has a hyphen so it isn't importable as
# a package. ``conftest.py`` already inserts NAV_DIR on sys.path.
spec = importlib.util.spec_from_file_location("term_module", NAV_DIR / "term.py")
term = importlib.util.module_from_spec(spec)
spec.loader.exec_module(term)  # type: ignore[union-attr]


@pytest.fixture
def fake_repo(tmp_path: Path, monkeypatch) -> Path:
    """A self-contained mini repo with the layout term.py expects.

    Writes:
      - skills/dramatica-vocabulary/references/elements.md     (one term)
      - skills/dramatica-vocabulary/references/variations.md   (one term)
      - skills/dramatica-vocabulary/references/character-dynamics.md (canonical successor)
      - maintenance/schemas/narrative-ontology/ontology.json   (3 entries)

    Also monkeypatches ``term._post_mutation_gate`` to a no-op so we don't try
    to spawn the real ontology-build / validate scripts against this fake tree.
    """
    repo = tmp_path
    vocab = repo / "skills/dramatica-vocabulary/references"
    vocab.mkdir(parents=True)
    onto_dir = repo / "maintenance/schemas/narrative-ontology"
    onto_dir.mkdir(parents=True)

    elements_md = (
        "# Elements\n\n"
        "## Trust\n"
        f"{term.NAV_MARKER}\n"
        "```yaml\n"
        "id: el.trust\n"
        "kind: element\n"
        "canonical_label: Trust\n"
        "provenance: source-original\n"
        "```\n"
        "\n"
        "Body of trust.\n"
    )
    (vocab / "elements.md").write_text(elements_md, encoding="utf-8")

    variations_md = (
        "# Variations\n\n"
        "## Confidence\n"
        f"{term.NAV_MARKER}\n"
        "```yaml\n"
        "id: var.confidence\n"
        "kind: variation\n"
        "canonical_label: Confidence\n"
        "provenance: source-original\n"
        "```\n"
        "\n"
        "Body of confidence.\n"
    )
    (vocab / "variations.md").write_text(variations_md, encoding="utf-8")

    cdyn_md = (
        "# Character Dynamics\n\n"
        "## Problem-solving Style\n"
        f"{term.NAV_MARKER}\n"
        "```yaml\n"
        "id: character-dynamic.problem-solving-style\n"
        "kind: character-dynamic\n"
        "canonical_label: Problem-solving Style\n"
        "provenance: source-original\n"
        "```\n"
        "\n"
        "Body.\n"
    )
    (vocab / "character-dynamics.md").write_text(cdyn_md, encoding="utf-8")

    ontology = {
        "schema_version": "1.0",
        "ontology_version": "0.1",
        "created": "2026-05-04",
        "entries": [
            {
                "id": "character-dynamic.problem-solving-style",
                "kind": "character-dynamic",
                "canonical_label": "Problem-solving Style",
                "provenance": "source-original",
                "term_file": (
                    "skills/dramatica-vocabulary/references/character-dynamics.md"
                    "#problem-solving-style"
                ),
            },
            {
                "id": "el.trust",
                "kind": "element",
                "canonical_label": "Trust",
                "provenance": "source-original",
                "term_file": "skills/dramatica-vocabulary/references/elements.md#trust",
            },
            {
                "id": "var.confidence",
                "kind": "variation",
                "canonical_label": "Confidence",
                "provenance": "source-original",
                "term_file": (
                    "skills/dramatica-vocabulary/references/variations.md#confidence"
                ),
            },
        ],
    }
    (onto_dir / "ontology.json").write_text(
        json.dumps(ontology, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    monkeypatch.setattr(term, "_post_mutation_gate", lambda _: (0, []))
    return repo


def _read_ontology(repo: Path) -> dict:
    return json.loads(
        (repo / "maintenance/schemas/narrative-ontology/ontology.json").read_text(
            encoding="utf-8"
        )
    )


# --- happy paths -------------------------------------------------------------


def test_create_happy(fake_repo: Path):
    """create mints a heading + YAML block + ontology entry."""
    rc = term.cmd_create(
        oid="el.smoke",
        kind="element",
        label="Smoke",
        file=None,
        scenarios=["novel.crucial-element-audit"],
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    elements = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    assert "## Smoke" in elements
    assert "id: el.smoke" in elements
    assert "novel.crucial-element-audit" in elements

    onto = _read_ontology(fake_repo)
    ids = {e["id"] for e in onto["entries"]}
    assert "el.smoke" in ids
    [smoke] = [e for e in onto["entries"] if e["id"] == "el.smoke"]
    assert smoke["term_file"] == (
        "skills/dramatica-vocabulary/references/elements.md#smoke"
    )
    assert smoke["scenarios"] == ["novel.crucial-element-audit"]


def test_edit_happy(fake_repo: Path):
    """edit --add-alias mutates block + projects into ontology."""
    rc = term.cmd_edit(
        oid="el.trust",
        add_alias=["en:Reliance", "de:Vertrauen"],
        remove_alias=[],
        set_scenario=["novel.character-arc"],
        refresh=False,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    md = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    assert "aliases_en:" in md
    assert "- Reliance" in md
    assert "aliases_de:" in md
    assert "- Vertrauen" in md
    assert "scenarios:" in md
    assert "- novel.character-arc" in md

    onto = _read_ontology(fake_repo)
    [trust] = [e for e in onto["entries"] if e["id"] == "el.trust"]
    assert trust.get("aliases_en") == ["Reliance"]
    assert trust.get("aliases_de") == ["Vertrauen"]
    assert trust.get("scenarios") == ["novel.character-arc"]


def test_move_happy(fake_repo: Path):
    """move physically transplants heading + body + YAML, rewrites term_file."""
    rc = term.cmd_move(
        oid="el.trust",
        to_file="skills/dramatica-vocabulary/references/variations.md",
        rename_anchor=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    src = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    dst = (fake_repo / "skills/dramatica-vocabulary/references/variations.md").read_text()
    assert "## Trust" not in src
    assert "## Trust" in dst
    assert "id: el.trust" in dst

    onto = _read_ontology(fake_repo)
    [trust] = [e for e in onto["entries"] if e["id"] == "el.trust"]
    assert trust["term_file"] == (
        "skills/dramatica-vocabulary/references/variations.md#trust"
    )


def test_deprecate_alias_on_happy(fake_repo: Path):
    """deprecate --alias-on folds the label onto a successor and removes source."""
    rc = term.cmd_deprecate(
        oid="el.trust",
        reason="folded onto canonical character-dynamic",
        alias_on="character-dynamic.problem-solving-style",
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    src = (fake_repo / "skills/dramatica-vocabulary/references/elements.md").read_text()
    assert "## Trust" not in src

    onto = _read_ontology(fake_repo)
    ids = {e["id"] for e in onto["entries"]}
    assert "el.trust" not in ids
    [succ] = [
        e
        for e in onto["entries"]
        if e["id"] == "character-dynamic.problem-solving-style"
    ]
    assert "Trust" in succ.get("deprecated_aliases_en", [])

    succ_md = (
        fake_repo / "skills/dramatica-vocabulary/references/character-dynamics.md"
    ).read_text()
    assert "deprecated_aliases_en" in succ_md
    assert "- Trust" in succ_md


# --- edge cases --------------------------------------------------------------


def test_create_duplicate_id(fake_repo: Path):
    """create refuses an existing id without --force."""
    rc = term.cmd_create(
        oid="el.trust",
        kind="element",
        label="Trust",
        file=None,
        scenarios=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_REFUSED


def test_create_missing_file(fake_repo: Path, tmp_path: Path):
    """create fails when --file points at a non-existent target."""
    rc = term.cmd_create(
        oid="el.smoke",
        kind="element",
        label="Smoke",
        file=str(tmp_path / "does-not-exist.md"),
        scenarios=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_NOT_FOUND


def test_move_no_clean_break(fake_repo: Path):
    """move refuses a heading-collision target without --force."""
    # Pre-seed the target file with a colliding heading.
    target = fake_repo / "skills/dramatica-vocabulary/references/variations.md"
    text = target.read_text()
    target.write_text(
        text + "\n## Trust\n(placeholder collision)\n", encoding="utf-8"
    )
    rc = term.cmd_move(
        oid="el.trust",
        to_file="skills/dramatica-vocabulary/references/variations.md",
        rename_anchor=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_REFUSED


def test_deprecate_without_alias_on(fake_repo: Path):
    """deprecate without --alias-on hits the schema-bump exit-5 friction path."""
    rc = term.cmd_deprecate(
        oid="el.trust",
        reason="superseded with no clean alias target",
        alias_on=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_SCHEMA_BUMP


# --- integration -------------------------------------------------------------


def test_integration_sequence(fake_repo: Path):
    """create → edit → move → deprecate produces a stable terminal state."""
    # create
    rc = term.cmd_create(
        oid="el.flow",
        kind="element",
        label="Flow",
        file=None,
        scenarios=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    # edit (alias + scenario)
    rc = term.cmd_edit(
        oid="el.flow",
        add_alias=["en:Stream"],
        remove_alias=[],
        set_scenario=["novel.diagnose-flat-draft"],
        refresh=False,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK

    # idempotent --refresh: second run is a no-op
    onto_before = _read_ontology(fake_repo)
    rc = term.cmd_edit(
        oid="el.flow",
        add_alias=[],
        remove_alias=[],
        set_scenario=None,
        refresh=True,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK
    onto_after = _read_ontology(fake_repo)
    assert onto_before == onto_after

    # move
    rc = term.cmd_move(
        oid="el.flow",
        to_file="skills/dramatica-vocabulary/references/variations.md",
        rename_anchor=None,
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK
    onto = _read_ontology(fake_repo)
    [flow] = [e for e in onto["entries"] if e["id"] == "el.flow"]
    assert flow["term_file"].endswith("variations.md#flow")

    # deprecate (alias-on)
    rc = term.cmd_deprecate(
        oid="el.flow",
        reason="superseded by canonical Trust line",
        alias_on="el.trust",
        repo_root=fake_repo,
    )
    assert rc == term.EXIT_OK
    onto = _read_ontology(fake_repo)
    ids = {e["id"] for e in onto["entries"]}
    assert "el.flow" not in ids
    [trust] = [e for e in onto["entries"] if e["id"] == "el.trust"]
    assert "Flow" in trust.get("deprecated_aliases_en", [])
