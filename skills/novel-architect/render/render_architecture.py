"""
render_architecture.py — Render architecture.yaml to status-view + NCP-skeleton hint

Phase 2 entry point. Reads `architecture.yaml`, generates a status-view that
displays storyform shape, throughlines (with names + class), 8-step worksheet
progress, dynamics, story points, crucial element, signposts/journeys,
ending type, gate-approval state, and NCP wiring.

Task 072 extended this renderer to surface the new architecture-template.yaml
schema blocks (throughline names, story_points, crucial_element, signposts,
journeys, ending_type, genre_mode, worksheet_audit). Backward-compatible with
v1.0.0 architecture.yaml files that lack the new blocks: missing blocks render
as `—` rows rather than tracebacks.

Usage:
    python3 render_architecture.py <project-slug>
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from io_helpers import (  # noqa: E402
    project_workspace,
    read_yaml,
    write_status_view,
)


def _fmt(val: Any) -> str:
    """Compact value formatter: dashes for empty, str-cast otherwise."""
    if val is None or val == "" or val == [] or val == {}:
        return "—"
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    if isinstance(val, dict):
        # one-line dict; keep short for status-view density.
        return ", ".join(f"{k}={v}" for k, v in val.items())
    return str(val)


def _render_narrative(narrative: dict[str, Any]) -> list[str]:
    """Render one narrative block. Pure function — returns body lines."""
    lines: list[str] = []
    nid = narrative.get("id", "?")
    lines.append(f"### Narrative `{nid}`")
    lines.append("")

    # Step 1 + 2: Throughlines (name + class)
    tl = narrative.get("throughlines", {})
    lines.append("**Throughlines (Steps 1 + 2):**")
    lines.append("")
    lines.append("| Slot | Name | Class | Type | Variation | Element |")
    lines.append("|------|------|-------|------|-----------|---------|")
    for k in ("os", "mc", "ic", "ss"):
        t = tl.get(k, {}) if isinstance(tl.get(k), dict) else {}
        lines.append(
            f"| `{k.upper()}` | {_fmt(t.get('name'))} | {_fmt(t.get('class'))} | "
            f"{_fmt(t.get('type'))} | {_fmt(t.get('variation'))} | {_fmt(t.get('element'))} |"
        )
    lines.append("")

    # Steps 3 + 4: Dynamics + auto-derived ending_type
    dyn = narrative.get("dynamics", {})
    lines.append("**Dynamics (Steps 3 + 4):**")
    lines.append("")
    for k in (
        "mc_resolve", "mc_growth", "mc_approach", "mc_mental_sex",
        "plot_driver", "plot_limit", "outcome", "judgment",
    ):
        lines.append(f"- `{k}`: {_fmt(dyn.get(k))}")
    lines.append(f"- `ending_type` (auto from Outcome×Judgment): "
                 f"**{_fmt(narrative.get('ending_type'))}**")
    lines.append("")

    # Step 5: Story Points
    sp = narrative.get("story_points", {})
    if sp:
        lines.append("**Story Points (Step 5):**")
        lines.append("")
        static = sp.get("static", {}) if isinstance(sp.get("static"), dict) else {}
        driver = sp.get("driver", {}) if isinstance(sp.get("driver"), dict) else {}
        thematic = sp.get("thematic", {}) if isinstance(sp.get("thematic"), dict) else {}
        for k in ("goal", "requirements", "consequences", "forewarnings"):
            lines.append(f"- static.`{k}`: {_fmt(static.get(k))}")
        for k in ("dividends", "costs", "prerequisites", "preconditions"):
            lines.append(f"- driver.`{k}`: {_fmt(driver.get(k))}")
        lines.append("- thematic (per throughline): "
                     + ", ".join(f"`{tl_id}`" for tl_id in thematic) if thematic else
                     "- thematic: —")
        lines.append("")

    # Step 6: Crucial Element
    ce = narrative.get("crucial_element", {})
    if ce:
        lines.append("**Crucial Element (Step 6):**")
        lines.append("")
        lines.append(f"- `element`: {_fmt(ce.get('element'))}")
        lines.append(f"- `dynamic_pair_partner`: {_fmt(ce.get('dynamic_pair_partner'))}")
        lines.append(f"- `role`: {_fmt(ce.get('role'))}")
        lines.append("")

    # Step 7: Signposts + Journeys
    sgnp = narrative.get("signposts", {})
    jnys = narrative.get("journeys", {})
    if sgnp or jnys:
        lines.append("**Signposts + Journeys (Step 7):**")
        lines.append("")
        lines.append("| Throughline | SP1 | J1→2 | SP2 | J2→3 | SP3 | J3→4 | SP4 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for k in ("os", "mc", "ic", "ss"):
            sps = sgnp.get(k, []) if isinstance(sgnp.get(k), list) else []
            js = jnys.get(k, []) if isinstance(jnys.get(k), list) else []
            # Pad to 4 sgnp + 3 jny so the row layout never breaks.
            sps = (sps + ["—"] * 4)[:4]
            js = (js + ["—"] * 3)[:3]
            lines.append(
                f"| `{k.upper()}` | {_fmt(sps[0])} | {_fmt(js[0])} | {_fmt(sps[1])} | "
                f"{_fmt(js[1])} | {_fmt(sps[2])} | {_fmt(js[2])} | {_fmt(sps[3])} |"
            )
        lines.append("")

    # Step 8: Genre Mode (optional)
    gm = narrative.get("genre_mode")
    if gm is not None and gm != "":
        lines.append(f"**Genre Mode (Step 8, optional):** {_fmt(gm)}")
        lines.append("")

    return lines


def render(slug: str) -> Path:
    """Render architecture-status-view.md from architecture.yaml."""
    ws = project_workspace(slug)
    arch_path = ws / "architecture.yaml"
    arch = read_yaml(arch_path)
    architecture = arch.get("architecture", {}) if arch else {}
    gates = arch.get("gates", {}) if arch else {}
    worksheet_audit = arch.get("worksheet_audit", {}) if arch else {}

    body_lines: list[str] = [
        "## Storyform Shape (Step 0 — from intent.yaml)",
        "",
        f"- **storyform_count:** {_fmt(architecture.get('storyform_count'))}",
        f"- **narratives count:** {len(architecture.get('narratives', []) or [])}",
        "",
        "## Narratives",
        "",
    ]
    for narrative in architecture.get("narratives", []) or []:
        body_lines.extend(_render_narrative(narrative))

    # Worksheet step audit
    body_lines.extend([
        "## Worksheet Step Audit",
        "",
        "Per-step completion flags (set by the loop as each step's slots commit).",
        "",
        "| Step | Flag | Set |",
        "|------|------|-----|",
    ])
    for step_key in (
        "step_0_intent_loaded",
        "step_1_throughlines_named",
        "step_2_classes_assigned",
        "step_3_character_dynamics_set",
        "step_4_plot_dynamics_set",
        "step_5_story_points_set",
        "step_6_crucial_element_set",
        "step_7_signposts_set",
        "step_8_genre_mode_set",
        "validation_pass",
    ):
        body_lines.append(
            f"| `{step_key}` | {'✓' if worksheet_audit.get(step_key) else '⏳'} | "
            f"{worksheet_audit.get(step_key, False)} |"
        )
    body_lines.append("")

    # Gates — read the canonical keys per architecture-template.yaml.
    body_lines.extend([
        "## Gates",
        "",
        "| Gate | Approved | Edits |",
        "|------|----------|-------|",
    ])
    # Canonical key names (Task 072 schema). Fall back to v1.0.0 legacy keys
    # for backward-compat with pre-Task-072 workspaces.
    canonical_keys = (
        "gate_1_storyform_shape",
        "gate_2_classes_dynamics_storypoints",
        "gate_3_final_architecture",
    )
    legacy_v100_keys = {
        "gate_2_classes_dynamics_storypoints": "gate_2_throughlines_classes_dynamics",
    }
    for g in canonical_keys:
        gdata = gates.get(g, {})
        if not gdata and g in legacy_v100_keys:
            gdata = gates.get(legacy_v100_keys[g], {})
        body_lines.append(
            f"| `{g}` | {gdata.get('approved', False)} | {gdata.get('edits', 0)} |"
        )

    ncp = arch.get("ncp", {}) if arch else {}
    body_lines.extend([
        "",
        "## NCP",
        "",
        f"- **skeleton_written:** {ncp.get('skeleton_written', False)}",
        f"- **ncp_file:** {ncp.get('ncp_file', '—')}",
        f"- **validation_status:** {ncp.get('validation_status', 'pending')}",
        "",
        f"- **architecture.approved:** {arch.get('approved', False) if arch else False}",
        f"- **revisions:** {len(arch.get('revisions', []) or []) if arch else 0}",
    ])

    body = "\n".join(body_lines)
    return write_status_view(slug, "phase2-architecture",
                              "Narrative Architecture — Status View", body)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_architecture.py <project-slug>", file=sys.stderr)
        sys.exit(1)
    out = render(sys.argv[1])
    print(f"Wrote: {out}")
