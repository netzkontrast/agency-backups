"""Supersession DAG construction and validation.

Spec anchors:
  - ADR.A.4.4 — DAG-aware conflict resolution.
  - ADR.A.4.5 — cycle detection (Kahn's algorithm).
  - ADR.A.4.6 — reciprocity between adr_supersedes / adr_superseded_by.
  - ADR.A.5.7 — orphan reference detection.
"""
from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
_FM = str(Path(__file__).resolve().parent.parent / "fm")
if _FM not in sys.path:
    sys.path.insert(0, _FM)
import _core  # type: ignore  # noqa: E402
from adr.corpus import AdrRecord  # type: ignore  # noqa: E402

Diagnostic = _core.Diagnostic


@dataclass(frozen=True)
class AdrGraph:
    nodes: dict[str, AdrRecord]
    edges_supersedes: dict[str, tuple[str, ...]]
    edges_superseded_by: dict[str, tuple[str, ...]]
    live_ids: frozenset[str]


def build_graph(corpus: list[AdrRecord]) -> AdrGraph:
    """Build an ``AdrGraph`` keyed by ``adr_id``.

    Records that lack a non-empty ``adr_id`` are dropped from the graph;
    they will surface as ADR.A.5.4 (missing required key) elsewhere.
    """
    nodes: dict[str, AdrRecord] = {}
    for rec in corpus:
        if rec.adr_id and rec.adr_id not in nodes:
            nodes[rec.adr_id] = rec
    edges_sup: dict[str, tuple[str, ...]] = {
        aid: rec.adr_supersedes for aid, rec in nodes.items()
    }
    edges_by: dict[str, tuple[str, ...]] = {
        aid: rec.adr_superseded_by for aid, rec in nodes.items()
    }
    live: set[str] = set()
    for aid, rec in nodes.items():
        if rec.adr_status == "Accepted" and not rec.adr_superseded_by:
            live.add(aid)
    return AdrGraph(
        nodes=nodes,
        edges_supersedes=edges_sup,
        edges_superseded_by=edges_by,
        live_ids=frozenset(live),
    )


def detect_cycles(g: AdrGraph) -> list[list[str]]:
    """Return each cycle in the supersession DAG as a list of ``adr_id``.

    Uses Kahn's algorithm to identify nodes that cannot be topologically
    ordered, then runs a DFS over the residual sub-graph to recover the
    cycles for diagnostic emission.
    """
    indegree: dict[str, int] = {aid: 0 for aid in g.nodes}
    adj: dict[str, list[str]] = {aid: [] for aid in g.nodes}
    for aid, targets in g.edges_supersedes.items():
        for t in targets:
            if t in g.nodes:
                adj[aid].append(t)
                indegree[t] = indegree.get(t, 0) + 1

    queue: deque[str] = deque(a for a, d in indegree.items() if d == 0)
    visited: set[str] = set()
    while queue:
        n = queue.popleft()
        visited.add(n)
        for t in adj[n]:
            indegree[t] -= 1
            if indegree[t] == 0:
                queue.append(t)

    residual = {n for n in g.nodes if n not in visited}
    cycles: list[list[str]] = []
    seen: set[str] = set()
    for start in sorted(residual):
        if start in seen:
            continue
        path: list[str] = []
        index: dict[str, int] = {}

        def dfs(node: str) -> bool:
            if node in index:
                cycle = path[index[node]:]
                cycles.append(cycle + [node])
                return True
            if node not in residual or node in seen:
                return False
            index[node] = len(path)
            path.append(node)
            for nxt in adj.get(node, []):
                if nxt in residual and dfs(nxt):
                    return True
            path.pop()
            del index[node]
            seen.add(node)
            return False

        dfs(start)
    return cycles


def check_cycles(g: AdrGraph) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    for cycle in detect_cycles(g):
        rel = g.nodes[cycle[0]].rel if cycle and cycle[0] in g.nodes else "<graph>"
        diags.append(Diagnostic(
            rel, None, "ERROR", "ADR.A.4.5",
            "cyclic supersession edge: " + " -> ".join(cycle),
        ))
    return diags


def check_reciprocity(g: AdrGraph) -> list[Diagnostic]:
    """Verify every ``adr_supersedes`` edge has its reciprocal ``adr_superseded_by``."""
    diags: list[Diagnostic] = []
    for aid, targets in g.edges_supersedes.items():
        for t in targets:
            if t not in g.nodes:
                continue
            back = g.edges_superseded_by.get(t, ())
            if aid not in back:
                rel = g.nodes[t].rel
                diags.append(Diagnostic(
                    rel, None, "ERROR", "ADR.A.4.6",
                    f"missing reciprocal: {aid} declares adr_supersedes "
                    f"contains {t} but {t}.adr_superseded_by does not name {aid}",
                ))
    for aid, sources in g.edges_superseded_by.items():
        for s in sources:
            if s not in g.nodes:
                continue
            fwd = g.edges_supersedes.get(s, ())
            if aid not in fwd:
                rel = g.nodes[s].rel
                diags.append(Diagnostic(
                    rel, None, "ERROR", "ADR.A.4.6",
                    f"missing reciprocal: {aid} declares adr_superseded_by "
                    f"contains {s} but {s}.adr_supersedes does not name {aid}",
                ))
    return diags


def check_orphans(g: AdrGraph) -> list[Diagnostic]:
    """Emit ADR.A.5.7 for every reference whose target file does not exist."""
    diags: list[Diagnostic] = []
    for aid, targets in g.edges_supersedes.items():
        rec = g.nodes[aid]
        for t in targets:
            if t not in g.nodes:
                diags.append(Diagnostic(
                    rec.rel, None, "ERROR", "ADR.A.5.7",
                    f"adr_supersedes references {t!r} but no such ADR exists in /decisions/",
                ))
    for aid, sources in g.edges_superseded_by.items():
        rec = g.nodes[aid]
        for s in sources:
            if s not in g.nodes:
                diags.append(Diagnostic(
                    rec.rel, None, "ERROR", "ADR.A.5.7",
                    f"adr_superseded_by references {s!r} but no such ADR exists in /decisions/",
                ))
    return diags
