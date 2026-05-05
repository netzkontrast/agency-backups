"""HTTP integration tests — boot FastAPI against the fixture repo via httpx."""
from __future__ import annotations

import time
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from agency_backend import app as app_mod
from agency_backend.state import init_state


@pytest.fixture
async def client(fixture_repo: Path, monkeypatch):
    # Point the global state at the fixture; bypass the lifespan tail tasks
    # (we don't need live JSONL tailing to verify HTTP shape).
    state = init_state(fixture_repo)
    await state.reload_all()
    transport = ASGITransport(app=app_mod.app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_snapshot(client) -> None:
    r = await client.get("/api/snapshot")
    assert r.status_code == 200
    body = r.json()
    for key in ("tasks", "prompts", "research", "frictionLogs",
                "precommitRuns", "coherenceRuns", "agents",
                "channels", "messages"):
        assert key in body


async def test_tasks_filter(client) -> None:
    r = await client.get("/api/tasks", params={"status": "in_progress"})
    assert r.status_code == 200
    assert all(t["status"] == "in_progress" for t in r.json())


async def test_get_task(client) -> None:
    r = await client.get("/api/tasks/012")
    assert r.status_code == 200
    assert r.json()["slug"] == "frontend-prototype"


async def test_get_task_404(client) -> None:
    r = await client.get("/api/tasks/999")
    assert r.status_code == 404


async def test_post_message_round_trip(client) -> None:
    payload = {"text": "hello", "author": "you", "role": "human"}
    r = await client.post("/api/chat/general/messages", json=payload)
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r = await client.get("/api/chat/general/messages")
    assert r.status_code == 200
    assert any(m["text"] == "hello" for m in r.json())


async def test_graph_shape(client) -> None:
    r = await client.get("/api/graph")
    assert r.status_code == 200
    g = r.json()
    assert "nodes" in g and "edges" in g
    assert any(n["id"] == "task/012" for n in g["nodes"])
