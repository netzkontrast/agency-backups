"""Watchdog → asyncio bridge. Watches the repo and triggers targeted reloads."""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .state import RepoState

log = logging.getLogger(__name__)

WATCHED_PREFIXES = ("tasks", "prompts", "research", "friction-logs",
                    "precommit", "coherence")


class _Handler(FileSystemEventHandler):
    def __init__(self, state: RepoState, loop: asyncio.AbstractEventLoop) -> None:
        self.state = state
        self.loop = loop

    def _dispatch(self, raw_path: str) -> None:
        try:
            path = Path(raw_path)
            rel = path.relative_to(self.state.repo)
        except (ValueError, OSError):
            return
        first = rel.parts[0] if rel.parts else ""
        if first not in WATCHED_PREFIXES:
            return
        asyncio.run_coroutine_threadsafe(
            self.state.reload_path(path), self.loop)

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._dispatch(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._dispatch(event.src_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        self._dispatch(event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        self._dispatch(event.dest_path)


class RepoWatcher:
    def __init__(self, state: RepoState) -> None:
        self.state = state
        self.observer: Observer | None = None

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        if self.observer:
            return
        self.observer = Observer()
        self.observer.schedule(_Handler(self.state, loop),
                               str(self.state.repo), recursive=True)
        self.observer.start()
        log.info("RepoWatcher started on %s", self.state.repo)

    def stop(self) -> None:
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2)
            self.observer = None
