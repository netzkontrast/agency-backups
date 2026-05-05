---
type: note
status: draft
slug: task-019-st1-fm-rename
summary: "Subtask ST-1: ship tools/fm/rename.py — a stateless cross-file slug-rename CLI that updates every reference to a renamed slug across the operational tree atomically. Independent of all other Task 019 subtasks."
created: 2026-05-05
updated: 2026-05-05
---

# ST-1: `fm-rename` — Cross-File Slug Rename

## Goal

Ship `tools/fm/rename.py` that renames a slug everywhere it appears: the file's own `slug:` field, every list-valued frontmatter field that references it across the operational tree, and (optionally, with `--rename-folder`) the enclosing folder name. The tool is the missing T2-tier mutation surface for renames; every call SHOULD be reversible by running the tool again with the old/new arguments swapped.

## Falsification

This subtask is the wrong cut **iff** "rename" turns out to be ambiguous (multiple meanings — slug rename vs folder rename vs file rename) AND those ambiguities can't be parameterised cleanly with flags. Mitigation already in plan: `--rename-folder` is opt-in; default scope is *only the slug field and its list references*.

## Inputs

Read these files before writing code:

- [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §5.3 (`fm-edit` invariants), §7.2 (T1/T2 tier ladder).
- [`/tools/fm/_core.py`](../../../tools/fm/_core.py) — reuse `parse_frontmatter`, `iter_operational_files`, `FileLock`.
- [`/tools/fm/edit.py`](../../../tools/fm/edit.py) — model the read-modify-write loop on this file's `apply_edit` pattern. Body bytes outside the edited frontmatter MUST be byte-identical pre/post.
- [`/tools/fm/query.py`](../../../tools/fm/query.py) — model the iteration pattern; do NOT couple to query's main(); reuse helpers.
- [`/maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — list-valued L2 keys to scan: `task_uses_prompts`, `task_spawns_research`, `task_spawns_prompts`, `task_affects_paths`, plus prompt L2 string fields (`prompt_relates_to_task`, `prompt_spawned_from_research`).

## Acceptance Criteria

1. **Surface.** `tools/fm/rename.py <old-slug> <new-slug> [--scope=…] [--rename-folder] [--dry-run]`. Exit 0 on success; exit 1 on any partial failure (rollback via no writes); exit 2 on usage error.
2. **Idempotency.** Running the tool twice with the same arguments is a no-op the second time.
3. **Atomicity.** Either every reference is updated or none are. Take a `FileLock` per file in iteration order; on any error, abort before writing the first byte.
4. **Body invariant.** Bytes outside the frontmatter block of every touched file MUST be byte-identical pre/post (mirror `fm-edit`).
5. **Tests.** New file `tests/fm/test_rename.py`. Cover: scalar field rename (`prompt_relates_to_task`), list field rename (`task_uses_prompts`), no-match case (exit 0, no writes), idempotency, atomicity (mock a write failure mid-run; verify no partial state), `--dry-run` (no writes).
6. **Docs.** Add a one-paragraph entry in [`/tools/fm/__init__.py`](../../../tools/fm/__init__.py) docstring listing the new tool.
7. **Tier discipline.** The tool MUST refuse to rename a slug that's referenced from a `done` Task's `task_affects_paths` (those references are historical record). Refuse with exit 4 (T3 territory — file a Task).

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~150 LOC + 100 LOC tests).

## Agent Prompt

```text
You are implementing tools/fm/rename.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe (already checked out). Read the four
context files listed below before writing code, then implement the tool to
the acceptance criteria.

Repo root: /home/user/agency

Context files (read first):
  - research/flexible-frontmatter-toolchain/output/SPEC.md  (§5.3, §7.2)
  - tools/fm/_core.py
  - tools/fm/edit.py
  - tools/fm/query.py
  - maintenance/schemas/header-ontology.json

Acceptance criteria (verify each before completing):
  1. tools/fm/rename.py <old-slug> <new-slug> [--scope=…] [--rename-folder] [--dry-run]
  2. Idempotent: running twice with same args is a no-op the second time.
  3. Atomic: pre-scan to collect every change; abort if any check fails;
     only then write. FileLock per file. Body bytes byte-identical outside
     the frontmatter of every touched file.
  4. Refuses to rename a slug referenced from a done-Task task_affects_paths
     entry. Exits 4 in that case.
  5. Tests in tests/fm/test_rename.py covering: scalar rename, list rename,
     no-match, idempotency, atomicity (mock write failure), --dry-run.
  6. All existing tests still pass. Run: python3 -m unittest discover -s tests/fm -t .
  7. Legacy linter clean: python3 tools/validate-frontmatter.py exits 0.

Constraints:
  - Python 3.11 stdlib only. No new runtime dependencies.
  - Do NOT modify _core.py beyond adding small helpers if absolutely needed.
  - Do NOT change SPEC.md or the ontology JSON.
  - Do NOT touch other tools/fm/*.py files.

Deliverables:
  - tools/fm/rename.py (new)
  - tests/fm/test_rename.py (new)
  - one paragraph appended to tools/fm/__init__.py docstring (existing)

When done, run: python3 -m unittest discover -s tests/fm -t . && \
  python3 tools/validate-frontmatter.py
Both must succeed. Then commit with a message in the form
"feat(fm/rename): cross-file slug rename per SPEC §7.2 (Task 019 ST-1)".
Do NOT push; the driver session merges all Phase A branches.
```
