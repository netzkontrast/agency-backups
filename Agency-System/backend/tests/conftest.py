"""Pytest fixtures — build a synthetic repo in a tmp dir and point RepoState at it."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def fixture_repo(tmp_path: Path) -> Path:
    """Materialise a minimal repo that the parsers should successfully ingest."""
    repo = tmp_path / "repo"
    (repo / "tasks" / "012-frontend-prototype").mkdir(parents=True)
    (repo / "tasks" / "012-frontend-prototype" / "TASK.md").write_text(
        "---\n"
        "id: \"012\"\n"
        "slug: frontend-prototype\n"
        "status: in_progress\n"
        "priority: P1\n"
        "owner: claude-code\n"
        "summary: Build the static prototype frontend.\n"
        "uses_prompts: [frontend-prototype-spec]\n"
        "spawns_research: [layout-density]\n"
        "---\n"
        "Body of the task.\n"
    )

    (repo / "prompts").mkdir(parents=True)
    (repo / "prompts" / "frontend-prototype-spec.md").write_text(
        "---\n"
        "slug: frontend-prototype-spec\n"
        "kind: task-spec\n"
        "relates_to_task: \"012\"\n"
        "summary: Spec for the prototype.\n"
        "---\n"
        "Prompt body.\n"
    )

    (repo / "research" / "layout-density").mkdir(parents=True)
    (repo / "research" / "layout-density" / "RESEARCH.md").write_text(
        "---\n"
        "slug: layout-density\n"
        "phase: in_progress\n"
        "executes_prompt: frontend-prototype-spec\n"
        "summary: Trying density variants.\n"
        "---\n"
        "Notes.\n"
    )

    (repo / "friction-logs" / "012").mkdir(parents=True)
    (repo / "friction-logs" / "012" / "2026-05-05T0814.md").write_text(
        "---\n"
        "task: \"012\"\n"
        "level: FL2\n"
        "session: 2026-05-05T0814\n"
        "agent: claude-code\n"
        "duration: 14m\n"
        "tokens: 38211\n"
        "---\n"
        "ESLint resolver kept thrashing during refactor.\n"
    )

    (repo / "precommit" / "runs").mkdir(parents=True)
    (repo / "precommit" / "runs" / "2026-05-05T0901.json").write_text(json.dumps({
        "id": "2026-05-05T0901",
        "task": "012",
        "status": "pass",
        "duration": "11s",
        "checks": {"types": "pass", "lint": "pass", "fmt": "pass", "tests": "pass"},
    }))

    (repo / "coherence" / "runs").mkdir(parents=True)
    (repo / "coherence" / "runs" / "2026-05-05.md").write_text(
        "---\n"
        "date: 2026-05-05\n"
        "status: partial\n"
        "issues: 7\n"
        "deferred: 12\n"
        "---\n"
        "Coherence ran clean except for 7 broken cross-refs.\n"
    )

    (repo / "runtime").mkdir(parents=True)
    (repo / "runtime" / "agents.jsonl").write_text(
        json.dumps({"id": "a1", "handle": "claude-code", "status": "running",
                    "model": "claude-sonnet-4.5", "tokensUsed": 100,
                    "tokenBudget": 240000, "currentTask": "012"}) + "\n"
    )
    (repo / "runtime" / "chat.jsonl").write_text(
        json.dumps({"channel": "general", "id": "m1", "ts": "08:14",
                    "author": "you", "role": "human",
                    "text": "Hello from fixture."}) + "\n"
    )

    return repo
