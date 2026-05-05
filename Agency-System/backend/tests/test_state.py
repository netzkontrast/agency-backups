"""End-to-end RepoState tests — exercise reload, upsert, snapshot, pub/sub."""
from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from agency_backend.state import RepoState


async def test_reload_all_populates_snapshot(fixture_repo: Path) -> None:
    state = RepoState(repo=fixture_repo)
    await state.reload_all()
    snap = state.snapshot()
    assert len(snap["tasks"]) == 1
    assert len(snap["prompts"]) == 1
    assert len(snap["research"]) == 1
    assert len(snap["frictionLogs"]) == 1
    assert len(snap["precommitRuns"]) == 1
    assert len(snap["coherenceRuns"]) == 1


async def test_upsert_agent_patches_existing(fixture_repo: Path) -> None:
    state = RepoState(repo=fixture_repo)
    await state.upsert_agent({"id": "a1", "handle": "claude-code",
                              "status": "running", "tokensUsed": 100})
    await state.upsert_agent({"id": "a1", "status": "idle"})
    assert len(state.agents) == 1
    assert state.agents[0]["status"] == "idle"
    assert state.agents[0]["tokensUsed"] == 100  # preserved


async def test_append_message_groups_by_channel(fixture_repo: Path) -> None:
    state = RepoState(repo=fixture_repo)
    await state.append_message("general", {"id": "m1", "text": "hi"})
    await state.append_message("tasks",   {"id": "t1", "text": "task"})
    assert [m["id"] for m in state.messages["general"]] == ["m1"]
    assert [m["id"] for m in state.messages["tasks"]]   == ["t1"]


async def test_subscribe_receives_initial_snapshot(fixture_repo: Path) -> None:
    state = RepoState(repo=fixture_repo)
    await state.reload_all()
    sub = state.subscribe()
    evt, data = await asyncio.wait_for(sub.__anext__(), timeout=1)
    assert evt == "snapshot"
    assert "tasks" in data
    await sub.aclose()


async def test_subscribe_receives_agent_update(fixture_repo: Path) -> None:
    state = RepoState(repo=fixture_repo)
    sub = state.subscribe()
    # consume initial snapshot
    await asyncio.wait_for(sub.__anext__(), timeout=1)
    await state.upsert_agent({"id": "a1", "status": "running"})
    evt, data = await asyncio.wait_for(sub.__anext__(), timeout=1)
    assert evt == "agent.update"
    assert data["id"] == "a1"
    await sub.aclose()
