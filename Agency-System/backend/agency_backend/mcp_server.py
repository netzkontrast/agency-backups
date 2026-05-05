"""MCP server (FastMCP) — exposes the same RepoState as LLM-callable tools.

Run as stdio (default) or SSE:

    python -m agency_backend.mcp_server                  # stdio
    AGENCY_MCP_TRANSPORT=sse python -m agency_backend.mcp_server   # SSE on :8765

The server runs its own RepoState + watcher, so it can be spawned
independently of the FastAPI HTTP server.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from fastmcp import FastMCP

from .config import SETTINGS
from .runtime import read_jsonl
from .state import init_state, get_state
from .watcher import RepoWatcher

log = logging.getLogger("agency_mcp")
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("agency")


# ── tools ────────────────────────────────────────────────────────────────

@mcp.tool()
def list_tasks(status: str | None = None,
               priority: str | None = None) -> list[dict[str, Any]]:
    """List repo tasks. Optional filters: status, priority."""
    out = get_state().tasks
    if status:   out = [t for t in out if t["status"] == status]
    if priority: out = [t for t in out if t["priority"] == priority]
    return out

@mcp.tool()
def get_task(task_id: str) -> dict[str, Any]:
    """Fetch one task by id (e.g. '012')."""
    for t in get_state().tasks:
        if t["id"] == task_id:
            return t
    raise ValueError(f"task {task_id} not found")

@mcp.tool()
def list_prompts(kind: str | None = None) -> list[dict[str, Any]]:
    """List prompts. Optional filter: kind (task-spec, research-proposal, …)."""
    out = get_state().prompts
    if kind: out = [p for p in out if p["kind"] == kind]
    return out

@mcp.tool()
def list_research(phase: str | None = None) -> list[dict[str, Any]]:
    """List research entries. Optional filter: phase."""
    out = get_state().research
    if phase: out = [r for r in out if r["phase"] == phase]
    return out

@mcp.tool()
def list_agents(status: str | None = None) -> list[dict[str, Any]]:
    """List currently-known agents and their runtime status."""
    out = get_state().agents
    if status: out = [a for a in out if a["status"] == status]
    return out

@mcp.tool()
def tail_chat(channel: str, limit: int = 50) -> list[dict[str, Any]]:
    """Return the last `limit` messages in a channel (most-recent last)."""
    msgs = get_state().messages.get(channel, [])
    return msgs[-limit:]

@mcp.tool()
async def post_chat(channel: str, text: str,
                    author: str = "mcp-agent") -> dict[str, Any]:
    """Post a message into a channel. Returns the persisted message."""
    obj = {
        "id": f"m{int(time.time()*1000)}",
        "ts": time.strftime("%H:%M"),
        "author": author,
        "role": "agent",
        "text": text,
    }
    await get_state().append_message(channel, obj)
    return obj

@mcp.tool()
def find(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Fuzzy substring search across tasks, prompts, research."""
    q = query.lower()
    hits: list[dict[str, Any]] = []
    state = get_state()
    for t in state.tasks:
        if q in t["slug"].lower() or q in (t.get("summary") or "").lower():
            hits.append({"kind": "task", "id": t["id"], "label": t["slug"],
                         "summary": t.get("summary", "")})
    for p in state.prompts:
        if q in p["slug"].lower() or q in (p.get("summary") or "").lower():
            hits.append({"kind": "prompt", "id": p["slug"], "label": p["slug"],
                         "summary": p.get("summary", "")})
    for r in state.research:
        if q in r["slug"].lower() or q in (r.get("summary") or "").lower():
            hits.append({"kind": "research", "id": r["slug"], "label": r["slug"],
                         "summary": r.get("summary", "")})
    return hits[:limit]

@mcp.tool()
def repo_graph() -> dict[str, Any]:
    """Return the full task↔prompt↔research graph (nodes + edges)."""
    return get_state().graph()

@mcp.tool()
def repo_summary() -> dict[str, Any]:
    """One-shot counts + recent-activity summary for the repo."""
    s = get_state()
    return {
        "tasks":          len(s.tasks),
        "open":           sum(1 for t in s.tasks if t["status"] == "open"),
        "in_progress":    sum(1 for t in s.tasks if t["status"] == "in_progress"),
        "blocked":        sum(1 for t in s.tasks if t["status"] == "blocked"),
        "done":           sum(1 for t in s.tasks if t["status"] == "done"),
        "prompts":        len(s.prompts),
        "research":       len(s.research),
        "friction_logs":  len(s.friction_logs),
        "precommit_runs": len(s.precommit_runs),
        "agents":         len(s.agents),
        "active_agents":  sum(1 for a in s.agents
                              if a["status"] in ("running", "thinking")),
    }


# ── bootstrap ────────────────────────────────────────────────────────────

async def _bootstrap() -> None:
    state = init_state(SETTINGS.repo_root)
    await state.reload_all()
    # Hydrate runtime from JSONL (best-effort)
    for obj in read_jsonl(SETTINGS.agents_file):
        await state.upsert_agent(obj)
    for obj in read_jsonl(SETTINGS.chat_file):
        ch = obj.pop("channel", "general")
        await state.append_message(ch, obj)
    RepoWatcher(state).start(asyncio.get_running_loop())


def main() -> None:
    asyncio.get_event_loop().run_until_complete(_bootstrap())
    transport = SETTINGS.mcp_transport
    if transport == "sse":
        mcp.run(transport="sse", host="0.0.0.0", port=SETTINGS.mcp_port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
