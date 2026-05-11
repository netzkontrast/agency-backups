"""
render_intent.py — Render intent.yaml to status-view markdown

Phase 1 entry point. Reads `intent.yaml`, generates a human-readable
status-view that displays slot fill state, contradictions, and pending asks.

Usage:
    python3 render_intent.py <project-slug>
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Allow running as script
sys.path.insert(0, str(Path(__file__).parent))

from io_helpers import (  # noqa: E402
    load_project_config,
    project_workspace,
    read_yaml,
    write_status_view,
)


def slot_state(value: Any) -> str:
    """Classify slot state for the status view."""
    if value is None or value == "" or value == "<PLACEHOLDER>":
        return "⏳ empty"
    if isinstance(value, str) and "<PLACEHOLDER>" in value:
        return "⏳ partial"
    if isinstance(value, list) and len(value) == 0:
        return "⏳ empty"
    return "✓ filled"


REQUIRED_SLOTS = [
    "genre",
    "subgenre_modifiers",
    "audience",
    "core_conflict_question",
    "core_conflict_unpacked",
    "length_target",
    "language",
    "chapter_count_target",
    "methods_preference",
    "dramatica_storyform_count",
    "success_criterion",
]

OPTIONAL_SLOTS = [
    "philosophy_integration_level",
    "science_integration_level",
    "known_priors",
]


def render(slug: str) -> Path:
    """Render intent-status-view.md from intent.yaml."""
    ws = project_workspace(slug)
    intent_path = ws / "intent.yaml"
    intent = read_yaml(intent_path)
    intent_data = intent.get("intent", {}) if intent else {}

    body_lines = [
        "## Required Slots",
        "",
        "| Slot | State | Value (kurz) |",
        "|------|-------|--------------|",
    ]
    for slot in REQUIRED_SLOTS:
        val = intent_data.get(slot)
        state = slot_state(val)
        short = str(val)[:60] if val else "—"
        body_lines.append(f"| `{slot}` | {state} | {short} |")

    body_lines.extend(["", "## Optional Slots", "",
                        "| Slot | State | Value (kurz) |",
                        "|------|-------|--------------|"])
    for slot in OPTIONAL_SLOTS:
        val = intent_data.get(slot)
        state = slot_state(val)
        short = str(val)[:60] if val else "—"
        body_lines.append(f"| `{slot}` | {state} | {short} |")

    approval = intent.get("approved", False) if intent else False
    body_lines.extend([
        "",
        "## Approval",
        "",
        f"- **approved:** {approval}",
        f"- **revisions:** {len(intent.get('revisions', [])) if intent else 0}",
    ])

    body = "\n".join(body_lines)
    return write_status_view(slug, "phase1-intent", "Intent Capture — Status View", body)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_intent.py <project-slug>", file=sys.stderr)
        sys.exit(1)
    out = render(sys.argv[1])
    print(f"Wrote: {out}")
