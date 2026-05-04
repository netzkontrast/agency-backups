#!/usr/bin/env python3
"""
state_manager.py — Album-State-Manager für The Agency System.

Nutzung:
    python3 state_manager.py read  <pfad-zur-state-datei>
    python3 state_manager.py init  <pfad-zur-state-datei> <album>
    python3 state_manager.py update <pfad-zur-state-datei> <track-json>

Der State hält:
    - aktuelles Album (1 | 2 | 3)
    - Tracklist mit Phase×Cluster-Zuordnung
    - Status pro Track (draft | prompted | validated | completed)
    - letzter Auditor-Verdict

Verwendet nur Standard-Library. Idempotent.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime, timezone


EMPTY_STATE = {
    "album": None,
    "album_title": None,
    "tracks": [],
    "last_updated": None,
    "last_verdict": None,
}


def init_state(path: Path, album: str) -> dict:
    titles = {
        "1": "Together We Confide",
        "2": "Moment der Klarheit",
        "3": "Gegenüber",
    }
    if album not in titles:
        raise SystemExit(f"Album muss 1, 2 oder 3 sein. Bekam: {album}")
    state = {
        **EMPTY_STATE,
        "album": int(album),
        "album_title": titles[album],
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return state


def read_state(path: Path) -> dict:
    if not path.exists():
        return EMPTY_STATE
    return json.loads(path.read_text(encoding="utf-8"))


def update_state(path: Path, track_data: dict) -> dict:
    state = read_state(path)
    tracks = state.get("tracks", [])
    track_id = track_data.get("id")
    if track_id is None:
        track_data["id"] = len(tracks) + 1
        tracks.append(track_data)
    else:
        # Update existing
        for i, t in enumerate(tracks):
            if t.get("id") == track_id:
                tracks[i] = {**t, **track_data}
                break
        else:
            tracks.append(track_data)
    state["tracks"] = tracks
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    state["last_verdict"] = track_data.get("verdict")
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return state


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    path = Path(sys.argv[2])

    if cmd == "read":
        state = read_state(path)
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0

    if cmd == "init":
        if len(sys.argv) < 4:
            print("init braucht Album-Nummer (1|2|3).", file=sys.stderr)
            return 2
        state = init_state(path, sys.argv[3])
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0

    if cmd == "update":
        if len(sys.argv) < 4:
            print("update braucht Track-JSON-String.", file=sys.stderr)
            return 2
        track = json.loads(sys.argv[3])
        state = update_state(path, track)
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0

    print(f"Unbekanntes Kommando: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
