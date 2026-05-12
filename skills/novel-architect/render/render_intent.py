"""
render_intent.py — Render intent.yaml to status-view markdown

Phase 1 entry point. Reads `intent.yaml`, generates a human-readable
status-view that displays slot fill state, contradictions, and pending asks.

The Phase 1 slot set is loaded from `assets/intent-template.yaml` at runtime
(`_meta._required` / `_meta._optional`) — that file is the single source of
truth. Task 072 (PR #101 review §2.5) consolidated three previously-drifting
copies (this module, the template YAML, and the Markdown table in
`phases/phase1-intent-capture.md`) into one.

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
    project_workspace,
    read_yaml,
    write_status_view,
)


# ─── Slot-state classification ──────────────────────────────────────────────


_PLACEHOLDER = "<PLACEHOLDER>"


def slot_state(value: Any) -> str:
    """Classify slot state for the status view.

    Returns one of: `"⏳ empty"`, `"⏳ partial"`, `"✓ filled"`.

    Empty: ``None``, ``""``, ``"<PLACEHOLDER>"``, or an empty list.
    Partial: a non-placeholder string that still embeds ``"<PLACEHOLDER>"``
    (e.g. ``"Hard-SF (subgenre: <PLACEHOLDER>)"``).
    Filled: anything else.

    Task 072 (PR #101 review §2.7) collapsed the earlier redundant
    ``value == "<PLACEHOLDER>"`` then ``"<PLACEHOLDER>" in value`` ordering:
    a bare-placeholder string falls through the ``in`` test on the same
    branch.
    """
    if value is None or value == "":
        return "⏳ empty"
    if isinstance(value, list) and len(value) == 0:
        return "⏳ empty"
    if isinstance(value, str) and _PLACEHOLDER in value:
        # Bare placeholder → empty; otherwise partially-filled.
        return "⏳ empty" if value == _PLACEHOLDER else "⏳ partial"
    return "✓ filled"


# ─── Slot-list loader (SSoT: assets/intent-template.yaml) ───────────────────


# Hardcoded fallback — used only if the template is missing / unparseable.
# Kept in sync with `assets/intent-template.yaml` by convention; the template
# is the authority. Drift here is non-fatal (warning) but a regression.
_FALLBACK_REQUIRED = [
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
_FALLBACK_OPTIONAL = [
    "philosophy_integration_level",
    "science_integration_level",
    "known_priors",
]


def _template_path() -> Path:
    """Resolve the canonical intent-template.yaml location."""
    return Path(__file__).resolve().parent.parent / "assets" / "intent-template.yaml"


def load_slot_lists(
    template_path: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Return ``(required, optional)`` slot names from the template YAML.

    Reads ``_meta._required`` and ``_meta._optional`` from
    ``assets/intent-template.yaml``. Falls back to the embedded constants
    (warning to stderr) if the file is missing, unparseable, or lacks the
    `_meta` block — never raises, so a partial-install repo still renders.

    ``template_path`` is overridable for tests; production code should pass
    nothing and let the function resolve the canonical path.
    """
    path = template_path or _template_path()
    try:
        data = read_yaml(path)
    except Exception as exc:  # broad: yaml.YAMLError, OSError, …
        print(
            f"render_intent: failed to load slot lists from {path}: {exc}; "
            "using embedded fallback",
            file=sys.stderr,
        )
        return list(_FALLBACK_REQUIRED), list(_FALLBACK_OPTIONAL)

    meta = data.get("_meta") if isinstance(data, dict) else None
    if not isinstance(meta, dict):
        print(
            f"render_intent: {path} missing `_meta` block; using embedded fallback",
            file=sys.stderr,
        )
        return list(_FALLBACK_REQUIRED), list(_FALLBACK_OPTIONAL)

    required = meta.get("_required")
    optional = meta.get("_optional")
    if not isinstance(required, list) or not all(isinstance(s, str) for s in required):
        print(
            f"render_intent: {path} `_meta._required` malformed; using embedded fallback",
            file=sys.stderr,
        )
        required = list(_FALLBACK_REQUIRED)
    if not isinstance(optional, list) or not all(isinstance(s, str) for s in optional):
        print(
            f"render_intent: {path} `_meta._optional` malformed; using embedded fallback",
            file=sys.stderr,
        )
        optional = list(_FALLBACK_OPTIONAL)
    return list(required), list(optional)


REQUIRED_SLOTS, OPTIONAL_SLOTS = load_slot_lists()


# ─── Render ─────────────────────────────────────────────────────────────────


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
