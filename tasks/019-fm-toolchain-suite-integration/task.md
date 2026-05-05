---
type: task
status: active
slug: fm-toolchain-suite-integration
summary: "Decompose the gap between the four-tool fm-* atomic surface and a complete authoring/refactoring/validation toolchain into nine parallelizable subtasks executable via /sc:agent. Sets the contract for fm-rename, fm-graph, fm-new, fm-fix, validate-extensions, legacy-linter rewrite, docs/cookbook, single-fm wrapper, and SPEC amendments."
created: 2026-05-05
updated: 2026-05-05
task_id: "019"
task_status: done
task_owner: "claude-code"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/
  - tools/legacy/
  - tasks/019-fm-toolchain-suite-integration/
  - research/flexible-frontmatter-toolchain/output/SPEC.md
  - maintenance/schemas/header-ontology.json
  - tests/fm/
  - PRE_COMMIT.md
  - TASK.md
  - MAINTENANCE.md
  - README.md
---

# Task 019 — fm Toolchain Suite Integration

## Goal

Close the gap between the **atomic** fm-* surface that Tasks 016 + 018 ship (validate / extract / edit / query / section) and the **complete** authoring + refactoring + validation toolchain the maintenance loop actually needs. Decompose the goal into nine parallelizable subtasks, each scoped to a single `/sc:agent` invocation, then merge their outputs into a single coherent v2 toolchain. By task close, the legacy linters are retired, `--check-body` is the default, and a single `fm` wrapper presents a discoverable subcommand surface.

## Plan

1. Spawn the seven Phase-A subtasks (ST-1, ST-2, ST-3, ST-4, ST-5, ST-7, ST-9) in parallel via `/sc:agent`, each in its own worktree, plus Task 018 (`fm-section`) as a peer.
2. Wait for all Phase-A agents to complete; review each subtask's commit on its worktree branch.
3. Merge Phase-A branches into the integration branch in any order (subtasks were designed to share no source files).
4. Spawn ST-6 (legacy linter rewrite) — sequential because it consumes ST-5's `--type-check`.
5. Spawn ST-8 (single `fm` wrapper) — sequential because it integrates every Phase-A deliverable.
6. Run the full test suite over the converged tree; rebase any subtask whose tests fail under integration.
7. Flip `FM_TOOLCHAIN=1` to default in `tools/check-governance.sh`; retire the legacy linters from CI in the same commit.
8. Close Task 019: bump `updated:`, set `task_status: done`, write friction log, append run-log entry.

## Decomposition diagram

```
Phase A (parallel, fan out):
  ST-1  fm-rename          — cross-file slug rename
  ST-2  fm-graph           — dependency graph + cycle/orphan detection
  ST-3  fm-new             — scaffold from template
  ST-4  fm-fix             — T1/T2 auto-repair driver
  ST-5  fm-validate ext.   — --explain, --baseline, --type-check
  ST-7  docs + cookbook    — tools/fm/readme.md + workflows
  ST-9  SPEC Q4/Q5 amends  — Levenshtein→OSA, skill keys
  Task 018 (peer)          — fm-section body editor

Phase B (sequential, merge):
  ST-6  legacy retirement  — depends on ST-5 (--type-check)
  ST-8  single `fm` wrapper — depends on every other ST stabilising
```

### Critical-thinking decomposition (research-prompt-optimizer pattern)

Each subtask carries its own falsification clause: *what observation would prove this subtask is the wrong cut?* Recorded in the subtask file and summarised here:

- **ST-1** wrong if cross-file rename turns out to be an ambiguity-explosion (multiple meanings of "rename"). Mitigation: scope to *slug* renames only; folder renames stay manual.
- **ST-2** wrong if the dependency graph has trivially few edges and no real consumer. Mitigation: the coherence-check prompt (Step 2.5) is the named consumer.
- **ST-3** wrong if templates are too few to justify a tool. Mitigation: even three templates today (task / prompt / research) save ~50 lines of frontmatter typing per scaffold.
- **ST-4** wrong if T1/T2 repairs cluster too tightly with structural T3 changes that no auto-repair can safely apply. Mitigation: tier-tagged dispatch — `fm-fix` only applies T1/T2, refuses T3.
- **ST-5** wrong if `--explain` becomes a documentation maintenance burden. Mitigation: explanations live in JSON adjacent to the diagnostic-code declarations.
- **ST-6** wrong if rewriting the legacy linters as `fm-*` wrappers exposes a constraint the new tools can't satisfy. Mitigation: ST-6 is gated behind ST-5 specifically because `--type-check` is the highest-risk new capability — landing it first lets ST-6 fail fast.
- **ST-7** wrong if docs duplicate existing SPEC content. Mitigation: cookbook is *example-driven*; SPEC remains normative.
- **ST-8** wrong if the unified wrapper introduces import latency that breaks the per-invocation budget. Mitigation: lazy subcommand dispatch (only import the subcommand module that's invoked).
- **ST-9** is purely textual; no falsification risk beyond consensus on the wording.

## Todo

- [x] 1. Spawn ST-1 fm-rename via `/sc:agent` using [`subtasks/01-fm-rename-cross-file-slug.md`](./subtasks/01-fm-rename-cross-file-slug.md).
- [x] 2. Spawn ST-2 fm-graph via `/sc:agent` using [`subtasks/02-fm-graph-dependency.md`](./subtasks/02-fm-graph-dependency.md).
- [x] 3. Spawn ST-3 fm-new via `/sc:agent` using [`subtasks/03-fm-new-scaffolder.md`](./subtasks/03-fm-new-scaffolder.md).
- [x] 4. Spawn ST-4 fm-fix via `/sc:agent` using [`subtasks/04-fm-fix-auto-repair.md`](./subtasks/04-fm-fix-auto-repair.md).
- [x] 5. Spawn ST-5 validate extensions via `/sc:agent` using [`subtasks/05-validate-extensions.md`](./subtasks/05-validate-extensions.md).
- [x] 6. Spawn ST-7 docs + cookbook via `/sc:agent` using [`subtasks/07-fm-readme-cookbook.md`](./subtasks/07-fm-readme-cookbook.md).
- [x] 7. Spawn ST-9 SPEC amendments via `/sc:agent` using [`subtasks/09-spec-amendments-q4-q5.md`](./subtasks/09-spec-amendments-q4-q5.md).
- [x] 8. Merge Phase A outputs (verify no API conflicts; rebase if needed).
- [x] 9. Spawn ST-6 legacy retirement via `/sc:agent` using [`subtasks/06-legacy-linter-rewrite.md`](./subtasks/06-legacy-linter-rewrite.md).
- [x] 10. Spawn ST-8 single-fm wrapper via `/sc:agent` using [`subtasks/08-fm-cli-wrapper.md`](./subtasks/08-fm-cli-wrapper.md).
- [x] 11. Flip `FM_TOOLCHAIN=1` to default + retire legacy linkage from CI. *(FM_TOOLCHAIN=1 was already default after Task 017; this task added `--type-check` to the gate and reduced lint-linkage step to a documentation note. Flipping `--check-body` default-on is explicit Task 020 territory per SPEC §12.6 — the corpus has 71 pre-existing F.B.* drifts that need a migration pass first.)*
- [x] 12. Set `task_status: done`; write `friction-log.md`; append `maintenance/run-log.md`.

## Links

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) (§3, §4, §5, §12, §13, §14).
- Predecessor: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/) — atomic toolchain.
- Peer (parallel): [`/tasks/018-fm-section-editor/`](../018-fm-section-editor/) — body-side editor.
- Migration peer: [`/tasks/017-migrate-repo-to-flexible-toolchain/`](../017-migrate-repo-to-flexible-toolchain/).
- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md).
- Parallel-spawn instructions: [`subtasks/readme.md#parallel-spawn-recipe`](./subtasks/readme.md).
