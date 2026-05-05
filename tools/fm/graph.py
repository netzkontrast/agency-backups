#!/usr/bin/env python3
"""fm-graph — stateless dependency-graph builder + structural diagnostics.

Spec anchor: F.5.x (Task 019 ST-2). Supersedes the legacy
``tools/legacy/lint-linkage.py`` graph traversal.

Usage::

    python3 tools/fm/graph.py [--scope=…] \\
            [--format=text|json|dot] \\
            [--detect=cycles|orphans|dangling|all]

The graph is built fresh on every invocation by walking the operational
roots, parsing frontmatter via :mod:`tools.fm._core`, and turning each
slug-valued L2 cross-reference into an edge tuple
``(source_slug, edge_kind, target_slug)``.

Diagnostics
-----------

cycles
    Strongly-connected components of size > 1, found via Tarjan's
    iterative SCC algorithm. A self-loop counts as a cycle when it is
    not a benign reciprocal supersession (``task_supersedes`` ↔
    ``task_superseded_by``); for v1 we surface every non-trivial SCC.

orphans
    Operational files whose slug appears as **neither** the source nor
    the target of any edge AND whose path is not a root governance spec
    (root specs are the AGENTS.md / TASK.md / ... files at the repo
    top level; they are deliberately not part of the slug graph).

dangling
    A target slug referenced by some edge for which no operational
    file with that slug exists on disk. The dangling target is the
    canonical signal the repo-coherence-check prompt (Step 2.5) uses.

Statelessness
-------------

The tool MUST NOT read or write any cache file. The graph is rebuilt
in-memory per invocation. The only output is to stdout (and stderr for
warnings); there is no ``--output`` flag in v1.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

# Allow running as ``python3 tools/fm/graph.py`` (script mode).
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore


# ---- Edge-kind vocabulary ----------------------------------------------------
#
# Derived from the ontology's list-valued L2 keys (per Task 019 ST-2 brief).
# We pin the set explicitly because some L2 list keys carry *paths* rather
# than slugs (notably ``task_affects_paths``) and would generate spurious
# edges and dangling diagnostics if mixed in.
#
# A "slug-list" key holds a list of target slugs. A "slug-scalar" key holds a
# single target slug as a plain string (the prompt/research scalars).

SLUG_LIST_KEYS: frozenset[str] = frozenset({
    "task_uses_prompts",
    "task_spawns_research",
    "task_spawns_prompts",
    "task_blocked_by",
    "task_supersedes",
    "task_superseded_by",
})

SLUG_SCALAR_KEYS: frozenset[str] = frozenset({
    "prompt_relates_to_task",
    "prompt_spawned_from_research",
    "research_executes_prompt",
})

ALL_EDGE_KINDS: frozenset[str] = SLUG_LIST_KEYS | SLUG_SCALAR_KEYS

# Edge kinds whose targets are interpreted as task ids OR slugs (TASK.md §7.10
# allows either form on the supersession axis). When a token looks like a
# zero-padded task id, we resolve it through the task-id index before falling
# back to slug-lookup.
TASK_ID_OR_SLUG_KEYS: frozenset[str] = frozenset({
    "task_blocked_by",
    "task_supersedes",
    "task_superseded_by",
})

DEFAULT_TEXT_CAP_BYTES = 4096


# ---- Data shapes -------------------------------------------------------------


@dataclass(frozen=True)
class Edge:
    source: str        # source file slug
    kind: str          # ontology key name, e.g. "task_uses_prompts"
    target: str        # target slug (or task id, for TASK_ID_OR_SLUG_KEYS)

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.source, self.kind, self.target)


@dataclass
class GraphIndex:
    """Raw, unresolved slug graph + auxiliary indices.

    Attributes
    ----------
    slug_to_path:
        ``{slug: relative_path}`` for every operational file whose
        frontmatter declares a non-empty ``slug:``. When two files
        declare the same slug, the lexicographically first relative
        path wins (deterministic across runs); the duplicate is
        recorded in :attr:`duplicate_slugs` for downstream warning.
    task_id_to_slug:
        ``{task_id: slug}`` for files with type=task and a populated
        ``task_id:``. Used to resolve task_id-shaped references on the
        supersession / blocked-by axis.
    edges:
        Every (source, kind, target) tuple, in document discovery
        order. Targets are stored *unresolved* — task ids and slugs
        live side-by-side here.
    duplicate_slugs:
        ``{slug: [paths…]}`` for any slug that appeared in more than
        one file. Reported as a stderr warning by ``main()``.
    """
    slug_to_path: dict[str, str] = field(default_factory=dict)
    task_id_to_slug: dict[str, str] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    duplicate_slugs: dict[str, list[str]] = field(default_factory=dict)


# ---- Graph construction ------------------------------------------------------


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _iter_slug_targets(key: str, fm: dict[str, Any]) -> Iterable[str]:
    """Yield each target token attached to ``key`` in the frontmatter.

    For list-valued keys we yield each non-empty string element. For
    scalar slug keys we yield the trimmed string when non-empty. The
    parser stores list values as ``list`` and scalar values as ``str``;
    we tolerate either shape because retrofitted files occasionally
    carry the "wrong" YAML shape.
    """
    val = fm.get(key)
    if isinstance(val, list):
        for item in val:
            if isinstance(item, str):
                tok = item.strip()
                if tok:
                    yield tok
    elif isinstance(val, str):
        tok = val.strip()
        if tok:
            yield tok


def build_index(
    repo_root: Path,
    *,
    scope: list[str] | None = None,
) -> GraphIndex:
    """Walk the operational tree and build an unresolved :class:`GraphIndex`.

    The walk is deterministic: files are visited in the order returned
    by :func:`_core.iter_operational_files`, which itself uses
    ``Path.rglob`` (sorted is not guaranteed; we sort here to make
    duplicate-slug arbitration deterministic).
    """
    idx = GraphIndex()

    files = sorted(
        _core.iter_operational_files(repo_root, scope=scope),
        key=lambda p: _rel(p, repo_root),
    )

    # First pass: populate slug + task_id indices. The task_id index is
    # populated independently of the slug index because two files may
    # legitimately share a slug (e.g., a Task and its sibling prompt
    # named for the Task) while only one declares ``task_id``.
    fm_cache: dict[str, dict[str, Any]] = {}
    for path in files:
        fm = _core.read_fm(path, strict=False)
        rel = _rel(path, repo_root)
        fm_cache[rel] = fm
        if _core.str_val(fm, "type") == "task":
            tid = _core.str_val(fm, "task_id").strip()
            tslug = _core.str_val(fm, "slug").strip()
            if tid and tslug:
                idx.task_id_to_slug.setdefault(tid, tslug)
        slug = _core.str_val(fm, "slug")
        if not slug:
            continue
        if slug in idx.slug_to_path:
            idx.duplicate_slugs.setdefault(
                slug, [idx.slug_to_path[slug]],
            ).append(rel)
            continue
        idx.slug_to_path[slug] = rel

    # Second pass: emit edges.
    for path in files:
        rel = _rel(path, repo_root)
        fm = fm_cache[rel]
        slug = _core.str_val(fm, "slug")
        if not slug:
            continue
        for kind in sorted(ALL_EDGE_KINDS):
            for target in _iter_slug_targets(kind, fm):
                idx.edges.append(Edge(slug, kind, target))

    return idx


def _resolve_target(idx: GraphIndex, kind: str, target: str) -> str | None:
    """Resolve a target token to a known slug, or return None if dangling.

    For ``TASK_ID_OR_SLUG_KEYS`` the token may be either a zero-padded
    task id (``"010"``) or a slug. We try task_id first, then fall
    back to direct slug lookup. For all other kinds the token must be
    a slug present in :attr:`GraphIndex.slug_to_path`.
    """
    if kind in TASK_ID_OR_SLUG_KEYS:
        if target in idx.task_id_to_slug:
            return idx.task_id_to_slug[target]
    if target in idx.slug_to_path:
        return target
    return None


# ---- Diagnostics -------------------------------------------------------------


def find_cycles(idx: GraphIndex) -> list[list[str]]:
    """Return a list of slug-cycles (each cycle is a list of slugs).

    Implementation: Tarjan's SCC algorithm, iterative to avoid stack
    overflow on a deeply linked corpus. A non-trivial SCC is one of
    size ≥ 2, OR a singleton with a self-edge. Within each SCC we
    return slugs in their discovery order so output is deterministic
    given a deterministic input ordering.
    """
    # Build a resolved adjacency: only edges that point at known slugs
    # contribute to cycle detection. Dangling edges cannot participate
    # in a cycle.
    adj: dict[str, list[str]] = {s: [] for s in idx.slug_to_path}
    has_self_loop: set[str] = set()
    for edge in idx.edges:
        resolved = _resolve_target(idx, edge.kind, edge.target)
        if resolved is None:
            continue
        if edge.source not in adj:
            # Source has no slug entry (e.g., file without slug FM); skip.
            continue
        adj[edge.source].append(resolved)
        if edge.source == resolved:
            has_self_loop.add(edge.source)

    # Iterative Tarjan.
    index_of: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    sccs: list[list[str]] = []
    counter = 0

    # `work` is a stack of (node, neighbour_iterator) frames.
    nodes_in_order = sorted(adj.keys())
    for start in nodes_in_order:
        if start in index_of:
            continue
        work: list[tuple[str, list[str], int]] = []
        # Initial push.
        index_of[start] = counter
        lowlink[start] = counter
        counter += 1
        stack.append(start)
        on_stack.add(start)
        work.append((start, adj[start], 0))

        while work:
            v, neighbours, i = work[-1]
            if i < len(neighbours):
                w = neighbours[i]
                work[-1] = (v, neighbours, i + 1)
                if w not in index_of:
                    index_of[w] = counter
                    lowlink[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, adj[w], 0))
                elif w in on_stack:
                    lowlink[v] = min(lowlink[v], index_of[w])
            else:
                # Post-order: settle SCC root if applicable.
                work.pop()
                if lowlink[v] == index_of[v]:
                    component: list[str] = []
                    while True:
                        x = stack.pop()
                        on_stack.discard(x)
                        component.append(x)
                        if x == v:
                            break
                    if len(component) > 1 or v in has_self_loop:
                        # Reverse so the SCC reads in discovery order.
                        sccs.append(list(reversed(component)))
                # Propagate lowlink up to the parent frame.
                if work:
                    parent = work[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[v])

    return sccs


def find_dangling(idx: GraphIndex) -> list[Edge]:
    """Return every edge whose target does not resolve to a known file."""
    out: list[Edge] = []
    for edge in idx.edges:
        if _resolve_target(idx, edge.kind, edge.target) is None:
            out.append(edge)
    # Stable order: sort by (source, kind, target) for reproducible output.
    out.sort(key=lambda e: (e.source, e.kind, e.target))
    return out


def find_orphans(idx: GraphIndex, repo_root: Path) -> list[str]:
    """Return slugs whose file participates in no edge.

    Orphan = an operational file whose slug is neither the source nor
    the (resolved) target of any edge AND whose file is not a root
    governance spec. Root governance specs sit at the repo top level
    (``AGENTS.md``, ``TASK.md``, ``MAINTENANCE.md`` …); they are
    deliberately outside the slug graph.

    The order of the returned list is the slug's lexicographic order
    so callers can diff successive runs cleanly.
    """
    sources: set[str] = {e.source for e in idx.edges}
    targets: set[str] = set()
    for edge in idx.edges:
        resolved = _resolve_target(idx, edge.kind, edge.target)
        if resolved is not None:
            targets.add(resolved)

    orphans: list[str] = []
    for slug, rel in idx.slug_to_path.items():
        if slug in sources or slug in targets:
            continue
        if _is_root_governance_spec(rel):
            continue
        orphans.append(slug)
    orphans.sort()
    return orphans


def _is_root_governance_spec(rel_path: str) -> bool:
    """A root governance spec lives at the repo top level (no ``/`` in path).

    We do not enumerate them by name because new ones (e.g. ``PRE_COMMIT.md``)
    have appeared since the project began. The path-shape rule (top-level
    ``.md``) is the durable predicate.
    """
    return "/" not in rel_path and rel_path.endswith(".md")


# ---- Output formatting -------------------------------------------------------


def _format_text(
    idx: GraphIndex,
    *,
    detect: set[str],
    cycles: list[list[str]],
    dangling: list[Edge],
    orphans: list[str],
) -> str:
    lines: list[str] = []
    lines.append(
        f"# fm-graph — {len(idx.slug_to_path)} slugs, "
        f"{len(idx.edges)} edges"
    )
    if "cycles" in detect:
        lines.append(f"\n## Cycles ({len(cycles)})")
        if not cycles:
            lines.append("(none)")
        for i, cyc in enumerate(cycles, start=1):
            lines.append(f"  {i}. " + " -> ".join(cyc) + f" -> {cyc[0]}")
    if "dangling" in detect:
        lines.append(f"\n## Dangling ({len(dangling)})")
        if not dangling:
            lines.append("(none)")
        for e in dangling:
            lines.append(f"  - {e.source} --[{e.kind}]--> {e.target}  (target missing)")
    if "orphans" in detect:
        lines.append(f"\n## Orphans ({len(orphans)})")
        if not orphans:
            lines.append("(none)")
        for s in orphans:
            lines.append(f"  - {s}  ({idx.slug_to_path[s]})")
    return "\n".join(lines) + "\n"


def _format_json(
    idx: GraphIndex,
    *,
    detect: set[str],
    cycles: list[list[str]],
    dangling: list[Edge],
    orphans: list[str],
) -> str:
    payload: dict[str, Any] = {
        "slugs": sorted(idx.slug_to_path.keys()),
        "edges": [list(e.as_tuple()) for e in idx.edges],
    }
    if "cycles" in detect:
        payload["cycles"] = cycles
    if "dangling" in detect:
        payload["dangling"] = [list(e.as_tuple()) for e in dangling]
    if "orphans" in detect:
        payload["orphans"] = orphans
    return json.dumps(payload, indent=2) + "\n"


def _dot_id(slug: str) -> str:
    """Quote a slug for safe use as a Graphviz node id."""
    return '"' + slug.replace('"', '\\"') + '"'


def _format_dot(idx: GraphIndex) -> str:
    lines: list[str] = ['digraph fm_graph {', '  rankdir=LR;']
    for slug in sorted(idx.slug_to_path):
        lines.append(f"  {_dot_id(slug)};")
    for edge in idx.edges:
        resolved = _resolve_target(idx, edge.kind, edge.target)
        if resolved is None:
            # Materialise dangling targets as styled placeholder nodes so
            # operators can see the break in the rendered SVG.
            lines.append(
                f'  {_dot_id(edge.target)} [style=dashed,color=red];'
            )
            tgt_node = _dot_id(edge.target)
        else:
            tgt_node = _dot_id(resolved)
        lines.append(
            f'  {_dot_id(edge.source)} -> {tgt_node} [label="{edge.kind}"];'
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


# ---- CLI ---------------------------------------------------------------------


def _parse_detect(spec: str) -> set[str]:
    raw = [s.strip() for s in spec.split(",") if s.strip()]
    if not raw:
        raise SystemExit("fm-graph: --detect requires at least one value")
    valid = {"cycles", "orphans", "dangling", "all"}
    out: set[str] = set()
    for item in raw:
        if item not in valid:
            raise SystemExit(
                f"fm-graph: --detect={item!r} is not one of "
                f"cycles|orphans|dangling|all"
            )
        if item == "all":
            return {"cycles", "orphans", "dangling"}
        out.add(item)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-graph", add_help=True)
    p.add_argument("--scope", default=None,
                   help="comma-separated subset of operational roots")
    p.add_argument("--format", choices=("text", "json", "dot"), default="text")
    p.add_argument("--detect", default="all",
                   help="comma-separated subset of cycles|orphans|dangling|all")
    args = p.parse_args(argv)

    repo_root = _core.repo_root_from_cwd()
    scope: list[str] | None = (
        [s.strip() for s in args.scope.split(",") if s.strip()]
        if args.scope else None
    )
    detect = _parse_detect(args.detect)

    idx = build_index(repo_root, scope=scope)

    if idx.duplicate_slugs:
        for slug, paths in sorted(idx.duplicate_slugs.items()):
            sys.stderr.write(
                f"fm-graph: WARN duplicate slug {slug!r} declared in "
                f"{len(paths)} files: {', '.join(paths)}\n"
            )

    cycles = find_cycles(idx) if "cycles" in detect else []
    dangling = find_dangling(idx) if "dangling" in detect else []
    orphans = find_orphans(idx, repo_root) if "orphans" in detect else []

    if args.format == "json":
        out = _format_json(idx, detect=detect, cycles=cycles,
                           dangling=dangling, orphans=orphans)
    elif args.format == "dot":
        out = _format_dot(idx)
    else:
        out = _format_text(idx, detect=detect, cycles=cycles,
                           dangling=dangling, orphans=orphans)

    if args.format == "text":
        raw = out.encode("utf-8")
        if len(raw) > DEFAULT_TEXT_CAP_BYTES:
            truncated = raw[:DEFAULT_TEXT_CAP_BYTES].decode("utf-8", errors="ignore")
            if "\n" in truncated:
                truncated = truncated[: truncated.rfind("\n") + 1]
            sys.stdout.write(truncated)
            sys.stdout.write(
                f"… [truncated; cycles={len(cycles)} dangling={len(dangling)} "
                f"orphans={len(orphans)}]\n"
            )
        else:
            sys.stdout.write(out)
    else:
        sys.stdout.write(out)

    # Exit 0 by default; any diagnostic detected returns 1 so the tool
    # is usable inside pre-commit hooks. ``--format=dot`` always returns
    # 0 because dot is a rendering mode, not a check.
    if args.format == "dot":
        return 0
    if cycles or dangling or orphans:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
