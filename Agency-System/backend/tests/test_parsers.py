"""Pure-function parser tests — no asyncio, no network."""
from __future__ import annotations

from pathlib import Path

from agency_backend import parsers


def test_parse_tasks(fixture_repo: Path) -> None:
    tasks = parsers.parse_tasks(fixture_repo)
    assert len(tasks) == 1
    t = tasks[0]
    assert t["id"] == "012"
    assert t["slug"] == "frontend-prototype"
    assert t["status"] == "in_progress"
    assert t["priority"] == "P1"
    assert t["uses_prompts"] == ["frontend-prototype-spec"]
    assert t["spawns_research"] == ["layout-density"]


def test_parse_prompts(fixture_repo: Path) -> None:
    prompts = parsers.parse_prompts(fixture_repo)
    assert any(p["slug"] == "frontend-prototype-spec" for p in prompts)
    p = next(p for p in prompts if p["slug"] == "frontend-prototype-spec")
    assert p["kind"] == "task-spec"
    assert p["relates_to_task"] == "012"


def test_parse_research(fixture_repo: Path) -> None:
    research = parsers.parse_research(fixture_repo)
    assert any(r["slug"] == "layout-density" for r in research)
    r = next(r for r in research if r["slug"] == "layout-density")
    assert r["phase"] == "in_progress"
    assert r["executes_prompt"] == "frontend-prototype-spec"


def test_parse_friction_logs(fixture_repo: Path) -> None:
    logs = parsers.parse_friction_logs(fixture_repo)
    assert len(logs) == 1
    assert logs[0]["level"] == "FL2"
    assert logs[0]["task"] == "012"
    assert logs[0]["tokens"] == 38211


def test_parse_precommit(fixture_repo: Path) -> None:
    runs = parsers.parse_precommit_runs(fixture_repo)
    assert len(runs) == 1
    assert runs[0]["status"] == "pass"
    assert runs[0]["checks"]["types"] == "pass"


def test_parse_coherence(fixture_repo: Path) -> None:
    runs = parsers.parse_coherence_runs(fixture_repo)
    assert len(runs) == 1
    assert runs[0]["status"] == "partial"
    assert runs[0]["issues"] == 7
    assert runs[0]["deferred"] == 12


def test_build_graph(fixture_repo: Path) -> None:
    tasks    = parsers.parse_tasks(fixture_repo)
    prompts  = parsers.parse_prompts(fixture_repo)
    research = parsers.parse_research(fixture_repo)
    g = parsers.build_graph(tasks, prompts, research)

    ids = {n["id"] for n in g["nodes"]}
    assert "task/012" in ids
    assert "prompt/frontend-prototype-spec" in ids
    assert "research/layout-density" in ids

    rels = {(e["from"], e["to"], e["rel"]) for e in g["edges"]}
    assert ("task/012", "prompt/frontend-prototype-spec", "uses_prompt") in rels
    assert ("task/012", "research/layout-density", "spawns_research") in rels
    assert ("research/layout-density", "prompt/frontend-prototype-spec",
            "executes_prompt") in rels
