"""Single source of truth — in-memory snapshot + thread-safe mutations.

`RepoState` aggregates everything served by both the FastAPI and MCP
surfaces: parsed entities from disk + tailed runtime events. It also
fans out updates to subscribers via an async pub/sub.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator

from . import parsers, runtime

log = logging.getLogger(__name__)


@dataclass
class RepoState:
    repo: Path
    tasks: list[dict[str, Any]] = field(default_factory=list)
    prompts: list[dict[str, Any]] = field(default_factory=list)
    research: list[dict[str, Any]] = field(default_factory=list)
    friction_logs: list[dict[str, Any]] = field(default_factory=list)
    precommit_runs: list[dict[str, Any]] = field(default_factory=list)
    coherence_runs: list[dict[str, Any]] = field(default_factory=list)
    agents: list[dict[str, Any]] = field(default_factory=list)
    channels: list[dict[str, Any]] = field(default_factory=list)
    messages: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    _subscribers: set[asyncio.Queue] = field(default_factory=set)

    # ── full reload ────────────────────────────────────────────────
    async def reload_all(self) -> None:
        async with self._lock:
            self.tasks          = parsers.parse_tasks(self.repo)
            self.prompts        = parsers.parse_prompts(self.repo)
            self.research       = parsers.parse_research(self.repo)
            self.friction_logs  = parsers.parse_friction_logs(self.repo)
            self.precommit_runs = parsers.parse_precommit_runs(self.repo)
            self.coherence_runs = parsers.parse_coherence_runs(self.repo)
        await self._publish("snapshot", self.snapshot())

    async def reload_path(self, path: Path) -> None:
        """Targeted reload — only re-parses the directory the change hit."""
        rel = str(path.relative_to(self.repo)) if path.is_relative_to(self.repo) else str(path)
        async with self._lock:
            if rel.startswith("tasks"):
                self.tasks = parsers.parse_tasks(self.repo)
                evt = "tasks.update"
            elif rel.startswith("prompts"):
                self.prompts = parsers.parse_prompts(self.repo)
                evt = "prompts.update"
            elif rel.startswith("research"):
                self.research = parsers.parse_research(self.repo)
                evt = "research.update"
            elif rel.startswith("friction-logs"):
                self.friction_logs = parsers.parse_friction_logs(self.repo)
                evt = "friction.update"
            elif rel.startswith("precommit"):
                self.precommit_runs = parsers.parse_precommit_runs(self.repo)
                evt = "precommit.update"
            elif rel.startswith("coherence"):
                self.coherence_runs = parsers.parse_coherence_runs(self.repo)
                evt = "coherence.update"
            else:
                return
        await self._publish(evt, {"path": rel})

    # ── runtime updates ───────────────────────────────────────────
    async def upsert_agent(self, agent: dict[str, Any]) -> None:
        async with self._lock:
            for i, a in enumerate(self.agents):
                if a["id"] == agent["id"]:
                    self.agents[i] = {**a, **agent}
                    break
            else:
                self.agents.append(agent)
        await self._publish("agent.update", agent)

    async def append_message(self, channel: str, msg: dict[str, Any]) -> None:
        async with self._lock:
            self.messages.setdefault(channel, []).append(msg)
        await self._publish("chat.message", {"channel": channel, "message": msg})

    async def set_channels(self, channels: list[dict[str, Any]]) -> None:
        async with self._lock:
            self.channels = channels
        await self._publish("channels.update", channels)

    # ── view ───────────────────────────────────────────────────────
    def snapshot(self) -> dict[str, Any]:
        return {
            "tasks":          self.tasks,
            "prompts":        self.prompts,
            "research":       self.research,
            "frictionLogs":   self.friction_logs,
            "precommitRuns":  self.precommit_runs,
            "coherenceRuns":  self.coherence_runs,
            "agents":         self.agents,
            "channels":       self.channels,
            "messages":       self.messages,
        }

    def graph(self) -> dict[str, Any]:
        return parsers.build_graph(self.tasks, self.prompts, self.research)

    # ── pub/sub ────────────────────────────────────────────────────
    async def subscribe(self) -> AsyncIterator[tuple[str, Any]]:
        q: asyncio.Queue = asyncio.Queue(maxsize=512)
        self._subscribers.add(q)
        try:
            # Send snapshot on connect
            yield ("snapshot", self.snapshot())
            while True:
                evt = await q.get()
                yield evt
        finally:
            self._subscribers.discard(q)

    async def _publish(self, event: str, data: Any) -> None:
        dead: list[asyncio.Queue] = []
        for q in self._subscribers:
            try:
                q.put_nowait((event, data))
            except asyncio.QueueFull:
                dead.append(q)
        for q in dead:
            self._subscribers.discard(q)


STATE: RepoState | None = None


def get_state() -> RepoState:
    assert STATE is not None, "RepoState not initialised — call init_state() first"
    return STATE


def init_state(repo: Path) -> RepoState:
    global STATE
    STATE = RepoState(repo=repo)
    return STATE
