---
type: index
status: active
slug: task-019-subtasks-index
summary: "Subtask index for Task 019. Each file is a self-contained /sc:agent prompt scoped to a single feature delivery; six run in parallel in Phase A, two sequentially in Phase B, one (Task 018 fm-section) is a peer."
created: 2026-05-05
updated: 2026-05-05
---

# Task 019 — Subtask Index

Each subtask file below contains:
- a self-contained briefing (context the agent will not have from this conversation),
- explicit inputs (file paths, references),
- explicit acceptance criteria (what "done" looks like),
- a falsification clause (what would prove the cut wrong),
- and the agent prompt copy-pastable into `/sc:agent`.

## Phase A — Parallel (no inter-dependencies)

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-fm-rename-cross-file-slug.md`](./01-fm-rename-cross-file-slug.md) | `python-expert` | M |
| ST-2 | [`02-fm-graph-dependency.md`](./02-fm-graph-dependency.md) | `python-expert` | M |
| ST-3 | [`03-fm-new-scaffolder.md`](./03-fm-new-scaffolder.md) | `python-expert` | S |
| ST-4 | [`04-fm-fix-auto-repair.md`](./04-fm-fix-auto-repair.md) | `python-expert` | M |
| ST-5 | [`05-validate-extensions.md`](./05-validate-extensions.md) | `python-expert` | M |
| ST-7 | [`07-fm-readme-cookbook.md`](./07-fm-readme-cookbook.md) | `technical-writer` | S |
| ST-9 | [`09-spec-amendments-q4-q5.md`](./09-spec-amendments-q4-q5.md) | `technical-writer` | S |

Peer (already filed as its own Task):

| ID | Reference | Recommended agent | Effort |
|---|---|---|---|
| Task 018 | [`/tasks/018-fm-section-editor/`](../../018-fm-section-editor/) | `python-expert` | L |

## Phase B — Sequential (after Phase A converges)

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-6 | [`06-legacy-linter-rewrite.md`](./06-legacy-linter-rewrite.md) | ST-5 (`--type-check`) | `refactoring-expert` | L |
| ST-8 | [`08-fm-cli-wrapper.md`](./08-fm-cli-wrapper.md) | All Phase A subtasks | `python-expert` | M |

## Parallel-spawn recipe

Open one driver session and dispatch Phase A in a single message containing seven `Agent` tool invocations (the framework runs them concurrently; see [`AGENTS.md`](../../../AGENTS.md) for the orchestrator pattern):

```
Agent(description="ST-1 fm-rename",        subagent_type="python-expert",
      prompt=<paste subtasks/01-fm-rename-cross-file-slug.md "Agent Prompt" section>)
Agent(description="ST-2 fm-graph",         subagent_type="python-expert",
      prompt=<paste subtasks/02-fm-graph-dependency.md>)
Agent(description="ST-3 fm-new",           subagent_type="python-expert",
      prompt=<paste subtasks/03-fm-new-scaffolder.md>)
Agent(description="ST-4 fm-fix",           subagent_type="python-expert",
      prompt=<paste subtasks/04-fm-fix-auto-repair.md>)
Agent(description="ST-5 validate ext.",    subagent_type="python-expert",
      prompt=<paste subtasks/05-validate-extensions.md>)
Agent(description="ST-7 docs cookbook",    subagent_type="technical-writer",
      prompt=<paste subtasks/07-fm-readme-cookbook.md>)
Agent(description="ST-9 SPEC amendments",  subagent_type="technical-writer",
      prompt=<paste subtasks/09-spec-amendments-q4-q5.md>)
```

Each agent runs in `isolation: "worktree"` so its branch is independent. After all seven return, the driver merges in the order Phase B → ST-6 → ST-8 (rebasing if needed) and runs the full test suite once over the converged tree.

## Why this decomposition

The cuts above optimise for three properties (research-prompt-optimizer pattern):

1. **Independence.** Phase A subtasks share no source files except the SPEC and the ontology JSON, and even those are amended by exactly one subtask (ST-9). Concurrent edits to the same Python module are eliminated by design.
2. **Falsifiable scope.** Each subtask names a single new file (or a tightly-scoped flag set on an existing file) and ships its own tests. "Done" is mechanical.
3. **Tier discipline.** No subtask is allowed to make T3/T4 changes. If a subtask discovers a structural change is needed, it MUST file a sibling Task per [MAINTENANCE.md §1](../../../MAINTENANCE.md).
