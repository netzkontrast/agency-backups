#!/usr/bin/env python3
"""precompile.py — Persona-scenario JSON precompiler for the narrative ontology.

Reads ontology.json + scenarios.json and emits one denormalised JSON per
scenario under maintenance/schemas/narrative-ontology/precompiled/. Each
artefact carries the entries tagged with the scenario, partitioned by kind
(primary_terms / primary_quads / primary_pairs), with optional one-paragraph
encoding hints synthesised from the prose section.

Subcommands:
    emit-all                 -- write one JSON per scenario in scenarios.json
    emit --scenario <id>     -- write one JSON for a single scenario
    validate                 -- jsonschema-check every emitted JSON
    benchmark --query <id>   -- compare token cost vs. nav.py by-scenario+extract.py

Exit codes:
    0  success
    1  validation failure / benchmark gate failed
    2  bad CLI args / I/O failure
    3  ontology load failure
    4  unknown scenario id
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import OntologyError  # noqa: E402
from lib import ontology as ontology_lib  # noqa: E402

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("ERROR: jsonschema is required. Install with: pip install jsonschema",
          file=sys.stderr)
    sys.exit(2)


PROG = Path(__file__).name
SCHEMA_VERSION = "0.1"

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[1]
_NARRATIVE_DIR = _REPO_ROOT / "maintenance" / "schemas" / "narrative-ontology"
_ONTOLOGY_PATH = _NARRATIVE_DIR / "ontology.json"
_SCENARIOS_PATH = _NARRATIVE_DIR / "scenarios.json"
_SCHEMA_PATH = _NARRATIVE_DIR / "precompiled.schema.json"
_PRECOMPILED_DIR = _NARRATIVE_DIR / "precompiled"

# Quad and dynamic-pair are partitioned to their own arrays.
_TERM_KINDS: set[str] = {
    "class", "type", "variation", "element", "archetype",
    "character-dynamic", "plot-dynamic", "storypoint",
    "signpost-slot", "throughline", "concept",
}

_CONSUMER_HINT_TEMPLATE: dict[str, str] = {
    "novel-architect": (
        "Load this file when answering {scenario_id} queries; "
        "cite ontology entries by id, not label."
    ),
    "ncp-author": (
        "primary_terms[].ncp_appreciation maps each entry to its closest NCP "
        "enum (or null when absent — archetypes / quads / dynamic-pairs / "
        "concepts have no NCP target)."
    ),
}


# ---------------------------------------------------------------------------
# Encoding-hint synthesis
# ---------------------------------------------------------------------------

# Heading + metadata lines we strip before looking for prose.
_HEADING_RE = re.compile(r"^#{1,6}\s")
_METADATA_RE = re.compile(r"^\s*(\*Type:.*\*|\*\*[A-Za-z][^*]*\*\*\s*:.*|---|>\s)")
_NAV_YAML_RE = re.compile(r"<!-- nav-ontology[^>]*-->\n```yaml\n.+?\n```\n*", re.DOTALL)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _strip_yaml_block(prose: str) -> str:
    return _NAV_YAML_RE.sub("", prose)


def _collect_prose_paragraphs(prose: str) -> list[str]:
    """Return prose paragraphs (sequence of non-heading non-metadata lines)."""
    text = _strip_yaml_block(prose)
    lines = text.splitlines()
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        if _HEADING_RE.match(stripped):
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        if _METADATA_RE.match(stripped):
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        # Skip stray "syn." / synonym lines that do not start a new sentence.
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current).strip())
    return [p for p in paragraphs if p]


def synthesise_encoding_hint(prose: str | None, canonical_label: str) -> str | None:
    """Synthesise a <=2-sentence encoding hint from prose extract.

    Strategy: skip metadata, take the FIRST prose paragraph as the
    definition, then return up to 2 sentences from it (or from the next
    paragraph if the first is very short). Returns None if nothing usable.

    Bounded to 600 chars by the schema; we cap at 480 chars here to leave
    headroom.
    """
    if not prose:
        return None
    paragraphs = _collect_prose_paragraphs(prose)
    if not paragraphs:
        return None

    # Definition paragraph = first non-trivial paragraph.
    definition = paragraphs[0]
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(definition) if s.strip()]
    if not sentences:
        return None

    # Take up to 2 sentences from the definition.
    hint = " ".join(sentences[:2]).strip()

    # Drop trailing fragments past 480 chars on a sentence boundary if possible.
    if len(hint) > 480:
        truncated = hint[:480]
        # try cut on last sentence terminator
        for term in (".", "!", "?"):
            idx = truncated.rfind(term)
            if idx >= 200:
                truncated = truncated[: idx + 1]
                break
        hint = truncated.rstrip()

    if len(hint) < 12:  # too short to be useful
        return None

    return hint


# ---------------------------------------------------------------------------
# Prose loading (direct, no subprocess)
# ---------------------------------------------------------------------------

def _load_prose_for_entry(entry: dict) -> str | None:
    """Load and return the prose section for entry's term_file, if present."""
    tf = entry.get("term_file")
    if not tf or "#" not in tf:
        return None
    rel_path, anchor = tf.rsplit("#", 1)
    file_path = _REPO_ROOT / rel_path
    if not file_path.exists():
        return None

    # Reuse extract.py's section-finder via lib.frontmatter slugify + simple walk.
    try:
        from extract import find_heading_range  # type: ignore
    except ImportError:
        return None

    lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    start, end = find_heading_range(lines, anchor)
    if start == -1:
        return None
    section = "".join(lines[start:end])
    return _strip_yaml_block(section)


# ---------------------------------------------------------------------------
# Bundle synthesis
# ---------------------------------------------------------------------------

def _load_scenarios() -> list[dict]:
    try:
        data = json.loads(_SCENARIOS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise OntologyError(f"scenarios.json not found at {_SCENARIOS_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise OntologyError(f"scenarios.json malformed: {exc}") from exc
    return data.get("scenarios", [])


def _term_record(entry: dict, with_hint: bool) -> dict:
    rec: dict[str, Any] = {
        "id": entry["id"],
        "canonical_label": entry["canonical_label"],
        "kind": entry["kind"],
        "term_file": entry.get("term_file") or "",
    }
    # Optional fields (always emitted as keys so consumers don't branch).
    rec["dynamic_pair_id"] = entry.get("dynamic_pair_id")
    rec["quad_id"] = entry.get("quad_id")
    rec["ktad_position"] = entry.get("ktad_position")
    rec["ncp_appreciation"] = entry.get("ncp_appreciation")
    if with_hint:
        prose = _load_prose_for_entry(entry)
        rec["encoding_hint"] = synthesise_encoding_hint(prose, entry["canonical_label"])
    else:
        rec["encoding_hint"] = None
    return rec


def _quad_record(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "canonical_label": entry["canonical_label"],
        "term_file": entry.get("term_file"),
    }


def _pair_record(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "canonical_label": entry["canonical_label"],
        "pair_member_a": entry["pair_member_a"],
        "pair_member_b": entry["pair_member_b"],
        "term_file": entry.get("term_file"),
    }


def build_bundle(
    scenario: dict,
    idx: ontology_lib.OntologyIndex,
    *,
    generated_at: str,
    with_hints: bool = True,
) -> dict:
    """Synthesise the full precompiled bundle for one scenario."""
    sid = scenario["id"]
    entries = idx.by_scenario(sid)

    primary_terms: list[dict] = []
    primary_quads: list[dict] = []
    primary_pairs: list[dict] = []

    for e in sorted(entries, key=lambda x: x.get("id", "")):
        kind = e.get("kind")
        if kind in _TERM_KINDS:
            # term_file is required by schema but some derived entries lack it.
            # Skip without term_file (those are not consumable by extract anyway).
            if not e.get("term_file"):
                continue
            primary_terms.append(_term_record(e, with_hint=with_hints))
        elif kind == "quad":
            primary_quads.append(_quad_record(e))
        elif kind == "dynamic-pair":
            primary_pairs.append(_pair_record(e))

    consumer_hints = {
        k: v.format(scenario_id=sid)
        for k, v in _CONSUMER_HINT_TEMPLATE.items()
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "scenario_id": sid,
        "scenario_summary": scenario["summary"],
        "persona": scenario["persona"],
        "generated_from_ontology_version": idx.ontology_version,
        "generated_at": generated_at,
        "primary_terms": primary_terms,
        "primary_quads": primary_quads,
        "primary_pairs": primary_pairs,
        "consumer_hints": consumer_hints,
    }


# ---------------------------------------------------------------------------
# Emit / validate / benchmark
# ---------------------------------------------------------------------------

def _ensure_dir() -> None:
    _PRECOMPILED_DIR.mkdir(parents=True, exist_ok=True)


def _serialise_bundle(bundle: dict) -> str:
    """Stable serialisation — sort_keys for byte-identical idempotency."""
    return json.dumps(bundle, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _load_schema() -> dict:
    try:
        return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise OntologyError(f"schema not found at {_SCHEMA_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise OntologyError(f"schema malformed: {exc}") from exc


def emit_one(
    scenario: dict,
    idx: ontology_lib.OntologyIndex,
    *,
    generated_at: str,
) -> Path:
    bundle = build_bundle(scenario, idx, generated_at=generated_at)
    _ensure_dir()
    path = _PRECOMPILED_DIR / f"{scenario['id']}.json"
    path.write_text(_serialise_bundle(bundle), encoding="utf-8")
    return path


def cmd_emit_all(args: argparse.Namespace, idx: ontology_lib.OntologyIndex) -> int:
    scenarios = _load_scenarios()
    generated_at = args.generated_at or date.today().isoformat()
    written: list[str] = []
    for scenario in scenarios:
        path = emit_one(scenario, idx, generated_at=generated_at)
        written.append(path.name)
    print(f"{PROG}: emit-all wrote {len(written)} bundle(s) to "
          f"{_PRECOMPILED_DIR.relative_to(_REPO_ROOT)}/")
    for name in sorted(written):
        print(f"  {name}")
    return 0


def cmd_emit(args: argparse.Namespace, idx: ontology_lib.OntologyIndex) -> int:
    scenarios = _load_scenarios()
    target = next((s for s in scenarios if s["id"] == args.scenario), None)
    if target is None:
        print(f"{PROG}: emit: unknown scenario id {args.scenario!r}", file=sys.stderr)
        return 4
    generated_at = args.generated_at or date.today().isoformat()
    path = emit_one(target, idx, generated_at=generated_at)
    print(f"{PROG}: emit wrote {path.relative_to(_REPO_ROOT)}")
    return 0


def cmd_validate(args: argparse.Namespace, idx: ontology_lib.OntologyIndex) -> int:
    schema = _load_schema()
    validator = Draft202012Validator(schema)
    if not _PRECOMPILED_DIR.exists():
        print(f"{PROG}: validate: no precompiled directory at "
              f"{_PRECOMPILED_DIR.relative_to(_REPO_ROOT)}", file=sys.stderr)
        return 1

    files = sorted(_PRECOMPILED_DIR.glob("*.json"))
    if not files:
        print(f"{PROG}: validate: 0 files in precompiled/", file=sys.stderr)
        return 1

    failures = 0
    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  FAIL {fp.name}: malformed JSON: {exc}", file=sys.stderr)
            failures += 1
            continue
        errors = list(validator.iter_errors(data))
        if errors:
            failures += 1
            print(f"  FAIL {fp.name}: {len(errors)} schema error(s)", file=sys.stderr)
            for err in errors[:5]:
                print(f"    @ {list(err.absolute_path)}: {err.message}", file=sys.stderr)
        else:
            print(f"  OK   {fp.name}")
    if failures:
        print(f"{PROG}: validate: {failures}/{len(files)} files failed",
              file=sys.stderr)
        return 1
    print(f"{PROG}: validate: {len(files)}/{len(files)} files passed")
    return 0


# ---------------------------------------------------------------------------
# Benchmark — token-cost comparison
# ---------------------------------------------------------------------------

def _measure_prose_path(idx: ontology_lib.OntologyIndex, scenario_id: str) -> int:
    """Bytes a consumer would pay if calling nav.py by-scenario + extract.py.

    Approximates the agent workflow:
      1. nav.py by-scenario <id> --md   -- the listing
      2. for each term-kind entry with term_file, extract.py <id>  -- the prose

    Returns total bytes.
    """
    # 1. nav.py by-scenario <id> JSON output
    nav_payload = idx.by_scenario(scenario_id)
    nav_bytes = len(json.dumps(nav_payload, indent=2, ensure_ascii=False).encode("utf-8"))

    # 2. prose for each term-kind entry with term_file
    prose_bytes = 0
    for e in nav_payload:
        if e.get("kind") not in _TERM_KINDS:
            continue
        prose = _load_prose_for_entry(e)
        if prose:
            prose_bytes += len(prose.encode("utf-8"))
    return nav_bytes + prose_bytes


def _measure_precompiled_path(scenario_id: str) -> int:
    fp = _PRECOMPILED_DIR / f"{scenario_id}.json"
    if not fp.exists():
        return -1
    return len(fp.read_bytes())


def _benchmark_table(rows: list[tuple[str, int, int, float, str]]) -> str:
    header = (
        "| scenario-id | prose-path-bytes | precompiled-path-bytes "
        "| reduction-% | gate-status |"
    )
    sep = "| :--- | ---: | ---: | ---: | :--- |"
    lines = [header, sep]
    for sid, prose, pre, ratio_pct, gate in rows:
        lines.append(
            f"| {sid} | {prose} | {pre} | {ratio_pct:.1f}% | {gate} |"
        )
    return "\n".join(lines)


def benchmark_all(idx: ontology_lib.OntologyIndex) -> tuple[list[tuple[str, int, int, float, str]], float]:
    """Run benchmark across all 11 scenarios. Return (rows, average_ratio_pct)."""
    scenarios = _load_scenarios()
    rows: list[tuple[str, int, int, float, str]] = []
    ratios: list[float] = []
    for scenario in scenarios:
        sid = scenario["id"]
        prose_bytes = _measure_prose_path(idx, sid)
        pre_bytes = _measure_precompiled_path(sid)
        if pre_bytes == -1:
            rows.append((sid, prose_bytes, 0, 0.0, "MISSING"))
            continue
        ratio = (pre_bytes / prose_bytes * 100.0) if prose_bytes else 0.0
        ratios.append(ratio)
        gate = "PASS" if ratio <= 60.0 else "FAIL"
        rows.append((sid, prose_bytes, pre_bytes, ratio, gate))
    avg = sum(ratios) / len(ratios) if ratios else 0.0
    return rows, avg


def cmd_benchmark(args: argparse.Namespace, idx: ontology_lib.OntologyIndex) -> int:
    rows, avg = benchmark_all(idx)
    print(_benchmark_table(rows))
    avg_gate = "PASS" if avg <= 60.0 else "FAIL"
    print(f"\n**Average reduction:** {avg:.1f}% (gate <=60%) -> {avg_gate}")

    # If --query specified, also emit a single-scenario block at end.
    if args.query:
        target = next((r for r in rows if r[0] == args.query), None)
        if target is None:
            print(f"{PROG}: benchmark: unknown scenario {args.query!r}", file=sys.stderr)
            return 4
        sid, prose, pre, ratio, gate = target
        print(f"\nQuery: {sid}")
        print(f"  prose-path-bytes:       {prose}")
        print(f"  precompiled-path-bytes: {pre}")
        print(f"  reduction:              {ratio:.1f}% (gate {gate})")

    return 0 if avg <= 60.0 else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=PROG,
        description=(
            "Precompile persona-scenario JSON bundles from the narrative "
            "ontology + emit / validate / benchmark them."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="subcmd", required=True)

    sp = sub.add_parser("emit-all", help="Write one JSON per scenario in scenarios.json.")
    sp.add_argument(
        "--generated-at",
        default=None,
        help="ISO date stamp for generated_at (default: today).",
    )

    sp = sub.add_parser("emit", help="Write one JSON for a single scenario.")
    sp.add_argument("--scenario", required=True, help="Scenario id (e.g. novel.act-pivot).")
    sp.add_argument(
        "--generated-at",
        default=None,
        help="ISO date stamp for generated_at (default: today).",
    )

    sub.add_parser("validate", help="Validate emitted JSONs against precompiled.schema.json.")

    sp = sub.add_parser("benchmark", help="Token-cost benchmark vs. nav.py by-scenario.")
    sp.add_argument("--query", default=None, help="Scenario id to focus the report on.")

    return p


_HANDLERS = {
    "emit-all": cmd_emit_all,
    "emit": cmd_emit,
    "validate": cmd_validate,
    "benchmark": cmd_benchmark,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        idx = ontology_lib.load(_ONTOLOGY_PATH)
    except OntologyError as exc:
        print(f"{PROG}: ontology load failure: {exc}", file=sys.stderr)
        return 3

    handler = _HANDLERS.get(args.subcmd)
    if handler is None:  # pragma: no cover (argparse enforces required subcmd)
        print(f"{PROG}: unknown subcommand {args.subcmd!r}", file=sys.stderr)
        return 2
    return handler(args, idx)


if __name__ == "__main__":
    sys.exit(main())
