---
type: note
status: draft
slug: task-019-st2-fm-graph
summary: "Subtask ST-2: ship tools/fm/graph.py — a stateless dependency-graph builder that walks the operational tree and emits cycles, orphans, and dangling references in machine-readable form."
created: 2026-05-05
updated: 2026-05-05
---

# ST-2: `fm-graph` — Dependency Graph + Diagnostics

## Goal

Ship `tools/fm/graph.py` that builds the task → prompt → research → task dependency graph from frontmatter cross-references and emits structural diagnostics (cycles, orphans, dangling references) plus a Graphviz `dot` rendering on demand. The named consumer is the repo-coherence-check prompt, which today cannot detect dangling slugs without re-implementing graph traversal.

## Falsification

Wrong cut **iff** the resulting graph has trivially few edges and no real consumer signs up. Mitigation: the [`/prompts/repo-coherence-check/prompt.md`](../../../prompts/repo-coherence-check/prompt.md) Step 2.5 already calls out a "dangling reference" check that this tool implements; if that prompt does not adopt fm-graph after this subtask lands, the subtask is wrong and should be deleted.

## Inputs

- [`/tools/fm/_core.py`](../../../tools/fm/_core.py), [`/tools/fm/query.py`](../../../tools/fm/query.py) — iteration helpers + `_build_referenced_index` reference impl.
- [`/maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — list-valued L2 keys define the edges.
- [`/tools/lint-linkage.py`](../../../tools/lint-linkage.py) — current ad-hoc graph implementation; this tool supersedes it (formal retirement is ST-6).

## Acceptance Criteria

1. **Surface.** `tools/fm/graph.py [--scope=…] [--format=text|json|dot] [--detect=cycles|orphans|dangling|all]`. Default: `--detect=all --format=text`.
2. **Edges.** Emit one edge per (file_slug, list_key, target_slug) tuple where `target_slug` resolves to an existing operational file. Tag edges by type (`uses_prompt`, `spawns_research`, `affects_path`, `relates_to_task`, `executes_prompt`).
3. **Diagnostics.** Cycles (any non-trivial SCC), orphans (operational files with no inbound edge AND no outbound edge OR not transitively reachable from any open Task), dangling (slug referenced but file missing).
4. **Statelessness.** No cache files, no `.agent_cache/` reads. The graph is rebuilt per invocation.
5. **Tests.** New file `tests/fm/test_graph.py`. Cover: a clean graph, an injected cycle, a dangling reference, an orphan prompt, the dot output round-tripping through `dot -Tsvg` (skip-if-not-installed).
6. **Output cap.** Default `--format=text` ≤ 4 KB. `--format=json` and `--format=dot` are uncapped (caller controls).

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~200 LOC + 120 LOC tests).

## Agent Prompt

```text
You are implementing tools/fm/graph.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe. Read the context files first.

Repo root: /home/user/agency

Context files (read first):
  - tools/fm/_core.py
  - tools/fm/query.py        (use _build_referenced_index as a starting point)
  - tools/lint-linkage.py    (the legacy implementation; you supersede it)
  - maintenance/schemas/header-ontology.json
  - prompts/repo-coherence-check/prompt.md  (Step 2.5 — your named consumer)

Acceptance criteria:
  1. tools/fm/graph.py [--scope=…] [--format=text|json|dot] [--detect=cycles|orphans|dangling|all]
  2. Edge tuples: (source_slug, edge_kind, target_slug). Edge kinds derived
     from the ontology's list-valued L2 keys.
  3. Cycle detection via Tarjan's algorithm or equivalent. SCCs of size > 1
     are cycles.
  4. Orphan = operational file whose slug appears as neither source nor
     target of any edge AND whose file is not a root governance spec.
  5. Dangling = a slug appearing as an edge target with no matching file.
  6. Stateless. No caches, no writes (other than the explicit --output path
     if you choose to add one — not required for v1).
  7. Tests in tests/fm/test_graph.py covering each diagnostic class.
  8. All existing tests still pass.

Constraints:
  - Python 3.11 stdlib only.
  - Do NOT modify _core.py except to add small helpers if necessary
    (graph-building belongs in graph.py, not _core).
  - Do NOT touch other tools/fm/*.py modules.

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - python3 tools/validate-frontmatter.py
  Both must succeed. Commit "feat(fm/graph): dependency graph + cycle/orphan/dangling
  detection (Task 019 ST-2)". Do NOT push.
```
