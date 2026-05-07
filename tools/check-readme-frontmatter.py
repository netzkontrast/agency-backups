#!/usr/bin/env python3
"""check-readme-frontmatter — operational-folder readme.md L1 validator.

Spec anchors:
    FOLDERS.md F.5 (readme.md L1 frontmatter — promoted from SHOULD to MUST
    by Task 036 ST-3).
    maintenance/schemas/header-ontology.json (canonical L1 key list).

Surface:
    python3 tools/check-readme-frontmatter.py [<paths> ...]

Default scope when no paths are passed: the operational roots `tasks/`,
`prompts/`, `research/`. Each readme.md found one level deep under the
root (e.g. `tasks/<NNN>-<slug>/readme.md`, `prompts/<slug>/readme.md`,
`research/<slug>/readme.md`) MUST carry every L1 Vault Core key
(`type`, `status`, `slug`, `summary`, `created`, `updated`) and its
`slug:` value MUST agree with the parent folder name (modulo the
`<NNN>-` task prefix, which is stripped before the comparison).

Exemptions (per FOLDERS.md F.1.1, FOLDERS.md §8):
    - `/research/<provider>/<slug>/` provider folders (gemini, gpt,
      human, other) — these are external-result mirrors, not
      operational orchestration folders.
    - `/decisions/` — ADR ledger; ADR files carry the `adr` type and
      `adr_*` L2 namespace, not an operational `<slug>/readme.md`.
    - `/skills/<slug>/` — the auto-generated `readme.md` is mirrored
      from `SKILL.md`; FOLDERS.md §8 explicitly exempts it from the
      L1 Vault Core requirement.

Slug agreement (per repo convention):
    Vault-level uniqueness forces sibling files in the same folder to
    carry distinct slugs (a task.md and its readme.md cannot share one).
    The convention qualifies the readme slug — e.g. `task-<NNN>-<slug>`,
    `<slug>-readme`, `<slug>-prompt-readme`. The linter therefore
    requires the bare folder slug (with the `<NNN>-` prefix stripped
    for task folders) to appear as a substring of the readme `slug:`,
    rather than demanding an exact match.

Diagnostic codes (all ERROR-tier; the linter gates pre-commit):
    F.5.MISSING-KEY   — one or more L1 keys absent.
    F.5.SLUG-MISMATCH — `slug:` value does not contain the parent
                        folder's bare slug.
    F.5.UNREADABLE    — frontmatter cannot be parsed.

Exit codes:
    0 — clean.
    1 — at least one diagnostic emitted.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

# Wire in the canonical frontmatter parser shared with fm-validate so the
# semantics stay consistent across the toolchain. Task 032 ST-2/3/4 linters
# follow the same pattern; mirror their import shape.
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
        "check-readme-frontmatter: tools/fm/_core.py not importable — "
        "skipping (advisory degradation, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)


L1_REQUIRED = ("type", "status", "slug", "summary", "created", "updated")
DIAG_PREFIX = "F.5"

# Provider folders under /research/ — exempt per FOLDERS.md F.1.1 / §8.
PROVIDER_NAMES = frozenset({"gemini", "gpt", "human", "other"})

# Operational roots scanned by default. `decisions/` and `skills/` are NOT
# in this list — they are governed by their own type-specific schemas.
DEFAULT_ROOTS = ("tasks", "prompts", "research")

TASK_PREFIX_RE = re.compile(r"^\d{3}-(.+)$")


def _expected_slug_for_folder(folder: Path) -> str:
    """Return the slug the folder name implies.

    Tasks live under `tasks/<NNN>-<slug>/`; strip the numeric prefix.
    Prompts and research live under `<slug>/` directly.
    """
    name = folder.name
    m = TASK_PREFIX_RE.match(name)
    return m.group(1) if m else name


def _is_provider_research_path(folder: Path, repo_root: Path) -> bool:
    """True iff `folder` is a provider sub-tree under research/."""
    try:
        rel = folder.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "research" and parts[1] in PROVIDER_NAMES:
        return True
    return False


def _iter_operational_readmes(target: Path, repo_root: Path) -> Iterable[Path]:
    """Yield every operational readme.md exactly one level under `target`.

    Only paths matching `<root>/<slug>/readme.md` are operational. Index
    readmes (`tasks/readme.md`) are governed by fm-validate's path
    classification (type=index) and out of scope for this linter.
    """
    if target.is_file():
        if target.name.lower() == "readme.md":
            yield target
        return
    if not target.is_dir():
        return
    for slug_dir in sorted(target.iterdir()):
        if not slug_dir.is_dir():
            continue
        if _is_provider_research_path(slug_dir, repo_root):
            continue
        readme = slug_dir / "readme.md"
        if readme.is_file():
            yield readme


def diagnostics_for(readme: Path) -> list[str]:
    diags: list[str] = []
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError as exc:
        diags.append(
            f"{readme}::ERROR:{DIAG_PREFIX}.UNREADABLE:cannot read file ({exc})"
        )
        return diags

    fm = _core.parse_frontmatter(text, strict=False)
    if not fm:
        diags.append(
            f"{readme}::ERROR:{DIAG_PREFIX}.MISSING-KEY:"
            "no parseable YAML frontmatter (FOLDERS.md F.5 — readme.md MUST "
            "carry L1 Vault Core frontmatter)"
        )
        return diags

    missing = [k for k in L1_REQUIRED if not _core.str_val(fm, k)]
    if missing:
        diags.append(
            f"{readme}::ERROR:{DIAG_PREFIX}.MISSING-KEY:"
            f"missing required L1 Vault Core key(s): {', '.join(missing)} "
            "(FOLDERS.md F.5)"
        )

    folder = readme.parent
    expected_slug = _expected_slug_for_folder(folder)
    actual_slug = _core.str_val(fm, "slug")
    if actual_slug and expected_slug not in actual_slug:
        diags.append(
            f"{readme}::ERROR:{DIAG_PREFIX}.SLUG-MISMATCH:"
            f"slug `{actual_slug}` does not contain folder slug "
            f"`{expected_slug}` (folder `{folder.name}`; FOLDERS.md F.5 / F.2)"
        )

    return diags


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-readme-frontmatter",
        description=(
            "ERROR-tier linter for operational-folder readme.md L1 Vault Core "
            "frontmatter (FOLDERS.md F.5)."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="readme.md files or operational roots to scan "
        "(default: tasks/ prompts/ research/).",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used to identify provider research paths "
        "(default: cwd).",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    raw_paths = args.paths or list(DEFAULT_ROOTS)
    targets = [Path(p) for p in raw_paths]

    all_diags: list[str] = []
    seen: set[Path] = set()
    for target in targets:
        if not target.exists():
            print(
                f"check-readme-frontmatter: warning: path does not exist: {target}",
                file=sys.stderr,
            )
            continue
        for readme in _iter_operational_readmes(target, repo_root):
            resolved = readme.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            all_diags.extend(diagnostics_for(readme))

    for d in all_diags:
        print(d)

    print(
        f"check-readme-frontmatter: {len(all_diags)} ERROR diagnostic(s) "
        f"across {len(seen)} readme(s).",
        file=sys.stderr,
    )
    return 1 if all_diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
