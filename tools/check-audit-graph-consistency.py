#!/usr/bin/env python3
"""check-audit-graph-consistency — F.6 dual-surface drift linter.

Spec anchor: FOLDERS.md F.6 (frontmatter-vs-body-link audit-graph
consistency rule, added by Task 036 ST-3).

FOLDERS.md §6 declares frontmatter linkage keys (`task_uses_prompts`,
`task_spawns_research`, `prompt_relates_to_task`,
`prompt_spawned_from_research`, `research_executes_prompt`) the
**source of truth**. Body-level Markdown links are encouraged for
human navigation but the linter cannot detect when they drift —
e.g. `task.md` body cites a sibling prompt, but the prompt is missing
from `task_uses_prompts`. This linter walks every `task.md`, `prompt.md`,
`readme.md` in an operational folder and emits a WARN diagnostic when
a body link references an operational folder without a corresponding
frontmatter linkage.

Surface:
    python3 tools/check-audit-graph-consistency.py [<paths> ...]

Default scope: tasks/ prompts/ research/ (operational roots).

Heuristic:
    For each operational source file, find every Markdown link
    `[label](relative-path)` whose resolved target sits inside an
    operational folder. Map the target's containing folder to a slug
    (stripping the `<NNN>-` prefix for tasks). Look up the source
    file's frontmatter for the appropriate linkage key (per the
    source/target type pair) and warn if the slug is absent.

Diagnostic format:
    <relpath>::WARN:F.6:body-link-without-frontmatter:<target-slug>

The diagnostic is WARN-tier; this linter is advisory only. FOLDERS.md
§6 explicitly encourages body links — this rule catches the asymmetric
case where a body link is present but the frontmatter is silent. The
inverse (frontmatter present, body silent) is **not** flagged: body
links are encouraged, not required.

Exit codes:
    0 — clean.
    2 — at least one WARN diagnostic emitted (advisory).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
_FM = _TOOLS / "fm"
if str(_FM) not in sys.path:
    sys.path.insert(0, str(_FM))

try:
    import _core  # type: ignore  # noqa: E402
except ImportError:
    print(
        "check-audit-graph-consistency: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)


DIAG_CODE = "F.6"
EXIT_OK = 0
EXIT_WARN = 2

# Markdown inline link `[label](target)` — match conservatively. Skip
# images (`![...]`) and reference-style links; those are rare in this
# corpus and easily covered by a future iteration if needed.
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Operational folder shapes:
TASKS_DIR_RE = re.compile(r"^tasks/(\d{3}-[a-z0-9-]+)(?:/|$)")
PROMPTS_DIR_RE = re.compile(r"^prompts/([a-z0-9-]+)(?:/|$)")
RESEARCH_DIR_RE = re.compile(r"^research/([a-z0-9-]+)(?:/|$)")
PROVIDER_NAMES = frozenset({"gemini", "gpt", "human", "other"})

# Source-file → target-type → frontmatter key.
# Keys per FOLDERS.md §6 + TASK.md §3 / PROMPT.md §3 / RESEARCH.md §3.
LINKAGE_KEYS: dict[str, dict[str, tuple[str, ...]]] = {
    "task": {
        "prompt": ("task_uses_prompts",),
        "research": ("task_spawns_research",),
        "task": ("task_supersedes", "task_superseded_by", "task_blocked_by"),
    },
    "prompt": {
        "task": ("prompt_relates_to_task",),
        "research": ("prompt_spawned_from_research",),
    },
    "research": {
        "prompt": ("research_executes_prompt",),
    },
}

# Sources walked by this linter. Each tuple is (path-glob, source-type).
SOURCE_GLOBS = (
    ("tasks/*/task.md", "task"),
    ("tasks/*/readme.md", "task"),
    ("prompts/*/prompt.md", "prompt"),
    ("prompts/*/readme.md", "prompt"),
    ("research/*/readme.md", "research"),
)


def _strip_task_prefix(slug: str) -> str:
    m = re.match(r"^(\d{3})-(.+)$", slug)
    return m.group(2) if m else slug


def _classify_target(rel: str) -> tuple[str, str] | None:
    """Return (target-type, target-slug) or None if not an operational target.

    `rel` is a forward-slash, repo-relative path with leading `./` and
    `../` already collapsed by the caller. Provider research subtrees
    (`research/gemini/...`) are excluded — they are external mirrors,
    not audit-graph nodes.
    """
    rel = rel.lstrip("/")
    m = TASKS_DIR_RE.match(rel)
    if m:
        return ("task", _strip_task_prefix(m.group(1)))
    m = PROMPTS_DIR_RE.match(rel)
    if m:
        return ("prompt", m.group(1))
    m = RESEARCH_DIR_RE.match(rel)
    if m:
        # Provider tree — not in the audit graph.
        if m.group(1) in PROVIDER_NAMES:
            return None
        return ("research", m.group(1))
    return None


def _resolve_link(source: Path, link: str, repo_root: Path) -> Path | None:
    """Resolve a Markdown link target to a repo-relative path.

    Strips fragment + query; rejects external (http/https/mailto) links
    and pure anchor (`#foo`) targets.
    """
    if not link or link.startswith("#"):
        return None
    if "://" in link or link.startswith("mailto:"):
        return None
    # Drop fragment + query.
    target = link.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    # Resolve relative to the source file's directory.
    base = source.parent
    try:
        resolved = (base / target).resolve()
        relative = resolved.relative_to(repo_root.resolve())
    except (ValueError, OSError):
        return None
    return Path(*relative.parts)


def _strip_frontmatter(text: str) -> str:
    """Return the body of `text` with the YAML frontmatter block removed.

    Operates on the textual surface so body-link extraction never sees
    quoted-string slug references inside frontmatter.
    """
    m = _core.FRONTMATTER_RE.match(text)
    if not m:
        return text
    return text[m.end():]


def _collect_links(text: str) -> list[str]:
    body = _strip_frontmatter(text)
    return LINK_RE.findall(body)


def _slug_present_in_linkage(
    fm: dict, keys: Iterable[str], slug: str
) -> bool:
    """True iff `slug` appears in any of the given frontmatter keys.

    Each key may be a scalar or a list (`prompt_relates_to_task` is a
    scalar; `task_uses_prompts` is a list). The slug also matches when
    the linkage value is a task_id ("032") whose target folder slug is
    `slug` — TASK.md §3 allows either form for `task_blocked_by` /
    `task_supersedes`. We don't reverse-resolve task_ids here; we
    accept the literal slug (the most common case in this corpus).
    """
    for key in keys:
        values = _core.str_list(fm, key)
        if not values:
            scalar = _core.str_val(fm, key)
            if scalar:
                values = [scalar]
        for v in values:
            v = v.strip().strip('"').strip("'")
            if v == slug:
                return True
            # Allow `<NNN>-<slug>` form for task references.
            if v.endswith(f"-{slug}") and re.match(r"^\d{3}-", v):
                return True
    return False


def diagnostics_for(source: Path, source_type: str, repo_root: Path) -> list[str]:
    diags: list[str] = []
    try:
        text = source.read_text(encoding="utf-8")
    except OSError:
        return diags

    fm = _core.parse_frontmatter(text, strict=False)
    self_slug = _core.str_val(fm, "slug")
    self_dir = source.parent.name
    self_dir_slug = _strip_task_prefix(self_dir) if source_type == "task" else self_dir

    seen: set[tuple[str, str]] = set()  # (target-type, target-slug)
    for link in _collect_links(text):
        rel = _resolve_link(source, link, repo_root)
        if rel is None:
            continue
        rel_str = rel.as_posix()
        classified = _classify_target(rel_str)
        if classified is None:
            continue
        target_type, target_slug = classified

        # Skip self-references — the source's own folder isn't an
        # audit-graph edge, just a structural relative link
        # (e.g. `[./subtasks/](./subtasks/)`).
        if target_type == source_type and target_slug == self_dir_slug:
            continue
        # Skip self-slug match — sometimes a readme links to its own
        # task.md or vice versa within the same folder.
        if target_type == source_type and self_slug and target_slug == self_slug:
            continue

        if (target_type, target_slug) in seen:
            continue
        seen.add((target_type, target_slug))

        # Look up the relevant frontmatter linkage keys.
        per_target = LINKAGE_KEYS.get(source_type, {}).get(target_type)
        if not per_target:
            # No linkage edge defined for this source/target pair.
            # E.g. research → task is not in the audit graph; skip.
            continue

        if _slug_present_in_linkage(fm, per_target, target_slug):
            continue

        diags.append(
            f"{source.as_posix()}::WARN:{DIAG_CODE}:body-link-without-frontmatter:"
            f"{target_slug} (target={target_type}; expected one of "
            f"{', '.join(per_target)})"
        )

    return diags


def _iter_sources(roots: list[Path], repo_root: Path) -> Iterable[tuple[Path, str]]:
    # Globs are repo-relative (e.g. `tasks/*/task.md`) and resolved against
    # repo_root, so each glob runs once across the whole repo. Per-root
    # scoping is applied as a post-filter via _is_under.
    seen: set[Path] = set()
    for glob, src_type in SOURCE_GLOBS:
        for path in repo_root.glob(glob):
            if not path.is_file():
                continue
            try:
                rel = path.resolve().relative_to(repo_root.resolve())
            except ValueError:
                continue
            parts = rel.parts
            if len(parts) >= 2 and parts[0] == "research" and parts[1] in PROVIDER_NAMES:
                continue
            if not any(_is_under(path, r) for r in roots):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield path, src_type


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-audit-graph-consistency",
        description=(
            "WARN-tier linter for FOLDERS.md F.6 audit-graph dual-surface "
            "drift (body link present, frontmatter linkage missing)."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Operational roots to walk (default: tasks/ prompts/ research/).",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used for path resolution (default: cwd).",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    raw_paths = args.paths or ["tasks", "prompts", "research"]
    roots = [(repo_root / p).resolve() for p in raw_paths]

    all_diags: list[str] = []
    for src, src_type in _iter_sources(roots, repo_root):
        all_diags.extend(diagnostics_for(src, src_type, repo_root))

    for d in all_diags:
        print(d)

    print(
        f"check-audit-graph-consistency: {len(all_diags)} WARN diagnostic(s).",
        file=sys.stderr,
    )
    return EXIT_WARN if all_diags else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
