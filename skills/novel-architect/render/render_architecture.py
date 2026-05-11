"""
render_architecture.py — Render architecture.yaml to status-view + NCP-skeleton hint

Phase 2 entry point. Reads `architecture.yaml`, generates a status-view that
displays storyform shape, throughlines, classes, dynamics, gate-approval state.

Usage:
    python3 render_architecture.py <project-slug>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from io_helpers import (  # noqa: E402
    project_workspace,
    read_yaml,
    write_status_view,
)


def render(slug: str) -> Path:
    """Render architecture-status-view.md from architecture.yaml."""
    ws = project_workspace(slug)
    arch_path = ws / "architecture.yaml"
    arch = read_yaml(arch_path)
    architecture = arch.get("architecture", {}) if arch else {}
    gates = arch.get("gates", {}) if arch else {}

    body_lines = [
        "## Storyform Shape",
        "",
        f"- **storyform_count:** {architecture.get('storyform_count', '—')}",
        f"- **narratives count:** {len(architecture.get('narratives', []))}",
        "",
        "## Narratives",
        "",
    ]

    for narrative in architecture.get("narratives", []) or []:
        nid = narrative.get("id", "?")
        body_lines.append(f"### {nid}")
        body_lines.append("")
        tl = narrative.get("throughlines", {})
        body_lines.append("**Throughlines:**")
        for k in ("os", "mc", "ic", "ss"):
            t = tl.get(k, {})
            cls = t.get("class", "—") if isinstance(t, dict) else "—"
            body_lines.append(f"- `{k.upper()}`: class={cls}")
        body_lines.append("")
        body_lines.append("**Dynamics:**")
        dyn = narrative.get("dynamics", {})
        for k, v in dyn.items():
            body_lines.append(f"- `{k}`: {v}")
        body_lines.append("")

    body_lines.extend([
        "## Gates",
        "",
        "| Gate | Approved | Edits |",
        "|------|----------|-------|",
    ])
    for g in ("gate_1_storyform_shape", "gate_2_throughlines_classes_dynamics",
              "gate_3_final_architecture"):
        gdata = gates.get(g, {})
        body_lines.append(
            f"| {g} | {gdata.get('approved', False)} | {gdata.get('edits', 0)} |"
        )

    ncp = arch.get("ncp", {}) if arch else {}
    body_lines.extend([
        "",
        "## NCP",
        "",
        f"- **skeleton_written:** {ncp.get('skeleton_written', False)}",
        f"- **ncp_file:** {ncp.get('ncp_file', '—')}",
        f"- **validation_status:** {ncp.get('validation_status', 'pending')}",
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
