"""FastAPI app — REST + SSE surface for the frontend."""
from __future__ import annotations

import asyncio
import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from .config import SETTINGS
from .runtime import tail_jsonl, read_jsonl
from .state import init_state, get_state
from .watcher import RepoWatcher

log = logging.getLogger("agency_backend")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")


# ── runtime tasks ────────────────────────────────────────────────────────

async def _tail_agents() -> None:
    state = get_state()
    # Hydrate from existing file
    for obj in read_jsonl(SETTINGS.agents_file):
        await state.upsert_agent(obj)
    # Then stream tail
    async for obj in tail_jsonl(SETTINGS.agents_file, from_start=False):
        await state.upsert_agent(obj)


async def _tail_chat() -> None:
    state = get_state()
    for obj in read_jsonl(SETTINGS.chat_file):
        ch = obj.pop("channel", "general")
        await state.append_message(ch, obj)
    async for obj in tail_jsonl(SETTINGS.chat_file, from_start=False):
        ch = obj.pop("channel", "general")
        await state.append_message(ch, obj)


# ── lifespan ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    state = init_state(SETTINGS.repo_root)
    log.info("Watching repo at %s", SETTINGS.repo_root)
    await state.reload_all()
    watcher = RepoWatcher(state)
    watcher.start(asyncio.get_running_loop())
    tasks = [
        asyncio.create_task(_tail_agents(), name="tail-agents"),
        asyncio.create_task(_tail_chat(),   name="tail-chat"),
    ]
    try:
        yield
    finally:
        watcher.stop()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


app = FastAPI(title="Agency Backend", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


# ── REST endpoints ───────────────────────────────────────────────────────

@app.get("/api/snapshot")
def snapshot() -> dict[str, Any]:
    return get_state().snapshot()

@app.get("/api/tasks")
def list_tasks(status: str | None = None, priority: str | None = None) -> list[dict[str, Any]]:
    out = get_state().tasks
    if status:   out = [t for t in out if t["status"] == status]
    if priority: out = [t for t in out if t["priority"] == priority]
    return out

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str) -> dict[str, Any]:
    for t in get_state().tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(404, f"task {task_id} not found")

@app.get("/api/prompts")
def list_prompts(kind: str | None = None) -> list[dict[str, Any]]:
    out = get_state().prompts
    if kind: out = [p for p in out if p["kind"] == kind]
    return out

@app.get("/api/prompts/{slug}")
def get_prompt(slug: str) -> dict[str, Any]:
    for p in get_state().prompts:
        if p["slug"] == slug: return p
    raise HTTPException(404, f"prompt {slug} not found")

@app.get("/api/research")
def list_research(phase: str | None = None) -> list[dict[str, Any]]:
    out = get_state().research
    if phase: out = [r for r in out if r["phase"] == phase]
    return out

@app.get("/api/research/{slug}")
def get_research(slug: str) -> dict[str, Any]:
    for r in get_state().research:
        if r["slug"] == slug: return r
    raise HTTPException(404, f"research {slug} not found")

@app.get("/api/friction-logs")
def list_friction() -> list[dict[str, Any]]:
    return get_state().friction_logs

@app.get("/api/precommit/runs")
def list_precommit() -> list[dict[str, Any]]:
    return get_state().precommit_runs

@app.get("/api/coherence/runs")
def list_coherence() -> list[dict[str, Any]]:
    return get_state().coherence_runs

@app.get("/api/agents")
def list_agents(status: str | None = None) -> list[dict[str, Any]]:
    out = get_state().agents
    if status: out = [a for a in out if a["status"] == status]
    return out

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str) -> dict[str, Any]:
    for a in get_state().agents:
        if a["id"] == agent_id: return a
    raise HTTPException(404, f"agent {agent_id} not found")


class AgentAction(BaseModel):
    reason: str | None = None

@app.post("/api/agents/{agent_id}/release")
async def release_agent(agent_id: str, _action: AgentAction | None = None) -> dict[str, Any]:
    state = get_state()
    for a in state.agents:
        if a["id"] == agent_id:
            await state.upsert_agent({**a, "status": "idle", "currentTask": None,
                                      "currentAction": "context released"})
            return {"ok": True, "agent": agent_id}
    raise HTTPException(404, f"agent {agent_id} not found")

@app.get("/api/chat/channels")
def list_channels() -> list[dict[str, Any]]:
    return get_state().channels

@app.get("/api/chat/{channel}/messages")
def list_messages(channel: str, limit: int = 200) -> list[dict[str, Any]]:
    msgs = get_state().messages.get(channel, [])
    return msgs[-limit:]


class ChatMessage(BaseModel):
    text: str
    author: str = "you"
    role: str = "human"

@app.post("/api/chat/{channel}/messages")
async def post_message(channel: str, msg: ChatMessage) -> dict[str, Any]:
    state = get_state()
    obj = {
        "id": f"u{int(time.time()*1000)}",
        "ts": time.strftime("%H:%M"),
        "author": msg.author,
        "role": msg.role,
        "text": msg.text,
    }
    await state.append_message(channel, obj)
    return {"ok": True, "message": obj}

@app.get("/api/graph")
def graph() -> dict[str, Any]:
    return get_state().graph()


# ── SSE stream ───────────────────────────────────────────────────────────

@app.get("/api/events")
async def events(request: Request) -> EventSourceResponse:
    state = get_state()

    async def gen():
        async for evt, data in state.subscribe():
            if await request.is_disconnected():
                break
            yield {"event": evt, "data": json.dumps(data, default=str)}

    return EventSourceResponse(gen())


# ── Entrypoint ───────────────────────────────────────────────────────────

def main() -> None:
    import uvicorn
    uvicorn.run("agency_backend.app:app",
                host=SETTINGS.host, port=SETTINGS.port, reload=False)


if __name__ == "__main__":
    main()
