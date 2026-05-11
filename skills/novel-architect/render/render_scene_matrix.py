"""
render_scene_matrix.py — Render scene-matrix.md from architecture + character files

Phase 5 entry point. Synthesizes scene-matrix.md from approved architecture and
character files, with placeholders for chapter/scene detail to be filled in
during Phase 5 sub-phases.

Usage:
    python3 render_scene_matrix.py <project-slug>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from io_helpers import (  # noqa: E402
    atomic_write,
    project_workspace,
    read_yaml,
)


def _act_for_chapter(ch: int, per_act: int, chapter_count: int) -> str:
    """Return roman-numeral act label for chapter number.

    Acts are computed from per_act size; the final act absorbs any remainder
    when chapter_count is not divisible by 4.
    """
    if ch <= per_act:
        return "I"
    if ch <= 2 * per_act:
        return "II"
    if ch <= 3 * per_act:
        return "III"
    return "IV"


def render(slug: str) -> Path:
    """Render scene-matrix.md initial skeleton (Phase 5.3 starting state)."""
    ws = project_workspace(slug)
    config = read_yaml(ws / "project-config.yaml")
    arch = read_yaml(ws / "architecture.yaml")
    chapter_count = config.get("narrative", {}).get("chapter_count_target", 40)
    storyform_count = arch.get("architecture", {}).get("storyform_count", "single")
    # Per phases/phase5-scene-matrix.md §5 and methods/conflict/dual-storyform.md
    # §3, a dual storyform seeds one storybeat in EACH narrative per chapter.
    narrative_suffixes = ("a", "b") if storyform_count == "dual" else ("a",)

    lines = [
        f"# Scene Matrix — `{slug}`",
        "",
        "> **Schema:** 4-Akt × N-Kapitel × M-Szenen Hierarchie",
        "> **Persistenz:** Struktur in NCP `storybeats[]` + `moments[]`",
        "> **Written by:** Phase 5",
        f"> **Storyform Count:** {storyform_count}",
        "",
        "## Akt-Übersicht",
        "",
        "| Akt | Kapitel-Range | Thema | Dramatica Sub-Concern |",
        "|-----|---------------|-------|----------------------|",
    ]

    # Compute act ranges
    per_act = max(1, chapter_count // 4)
    for i, label in enumerate(["I", "II", "III", "IV"]):
        start = i * per_act + 1
        end = (i + 1) * per_act if i < 3 else chapter_count
        lines.append(f"| {label}   | {start}–{end}          | <PLACEHOLDER> | <Storypoint> |")

    lines.extend([
        "",
        "## Kapitel-Detail",
        "",
    ])

    for ch in range(1, chapter_count + 1):
        chapter_lines = [
            f"### Kapitel {ch} — `<PLACEHOLDER Titel>`",
            "",
            f"- **Akt:** {_act_for_chapter(ch, per_act, chapter_count)}",
            "- **POV:** <PLACEHOLDER>",
            f"- **Storyform-Fokus:** {'Both' if storyform_count == 'dual' else 'Single'}",
            "- **Storypoint:** <PLACEHOLDER>",
            "- **Moments:**",
            "  1. <PLACEHOLDER>",
            "  2. <PLACEHOLDER>",
            "- **NCP-Referenzen:**",
        ]
        for suf in narrative_suffixes:
            chapter_lines.append(f"  - storybeat_id (narrative_{suf}): `beat_ch{ch:02d}_{suf}`")
            chapter_lines.append(
                f"  - moment_ids (narrative_{suf}): `[moment_ch{ch:02d}_{suf}_s01]`"
            )
        chapter_lines.extend(["", "---", ""])
        lines.extend(chapter_lines)

    lines.extend([
        "## Konsistenz-Checks",
        "",
        "- [ ] Jedes Kapitel referenziert mindestens einen Storybeat",
        "- [ ] Jedes Moment hat eine `moment.id` in NCP",
        "- [ ] Dramatica Storypoint pro Kapitel zugeordnet",
        "- [ ] Charakter-Auftritte konsistent mit character-architecture.yaml",
    ])

    if storyform_count == "dual":
        lines.append(
            "- [ ] Bei dual storyform: beide Narratives in 5D-Interferenz "
            "(parallel storybeats pro Kapitel, siehe `methods/conflict/dual-storyform.md` §3)"
        )

    content = "\n".join(lines) + "\n"
    out = ws / "scene-matrix.md"
    atomic_write(out, content)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_scene_matrix.py <project-slug>", file=sys.stderr)
        sys.exit(1)
    out = render(sys.argv[1])
    print(f"Wrote: {out}")
