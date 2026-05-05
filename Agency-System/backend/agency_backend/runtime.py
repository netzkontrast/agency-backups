"""Tail JSONL files for live agent + chat events."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, AsyncIterator


async def tail_jsonl(path: Path, *, from_start: bool = True
                     ) -> AsyncIterator[dict[str, Any]]:
    """Tail a JSONL file. Yields parsed objects as they're appended.

    Robust to the file being missing at startup — it polls for creation,
    then tracks the inode + offset and re-opens on truncation/rotation.
    """
    while not path.exists():
        await asyncio.sleep(1.0)

    f = path.open("r", encoding="utf-8")
    if not from_start:
        f.seek(0, 2)
    inode = path.stat().st_ino
    buf = ""

    try:
        while True:
            chunk = f.read()
            if chunk:
                buf += chunk
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
            else:
                await asyncio.sleep(0.4)
                # rotation / truncation check
                try:
                    st = path.stat()
                    if st.st_ino != inode or st.st_size < f.tell():
                        f.close()
                        f = path.open("r", encoding="utf-8")
                        inode = st.st_ino
                        buf = ""
                except FileNotFoundError:
                    await asyncio.sleep(1.0)
    finally:
        f.close()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
