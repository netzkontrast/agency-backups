"""Configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    repo_root: Path
    host: str
    port: int
    mcp_transport: str   # "stdio" | "sse"
    mcp_port: int
    agents_file: Path
    chat_file: Path

    @classmethod
    def load(cls) -> "Settings":
        repo_root = Path(os.environ.get("AGENCY_REPO_ROOT", "..")).resolve()
        runtime_dir = repo_root / "runtime"
        return cls(
            repo_root=repo_root,
            host=os.environ.get("AGENCY_HOST", "0.0.0.0"),
            port=int(os.environ.get("AGENCY_PORT", "8000")),
            mcp_transport=os.environ.get("AGENCY_MCP_TRANSPORT", "stdio"),
            mcp_port=int(os.environ.get("AGENCY_MCP_PORT", "8765")),
            agents_file=Path(os.environ.get(
                "AGENCY_AGENTS_FILE", str(runtime_dir / "agents.jsonl"))),
            chat_file=Path(os.environ.get(
                "AGENCY_CHAT_FILE", str(runtime_dir / "chat.jsonl"))),
        )


SETTINGS = Settings.load()
