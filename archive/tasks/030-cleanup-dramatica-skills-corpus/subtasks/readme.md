---
type: index
status: active
slug: task-030-subtasks-index
summary: "Subtask index for Task 030. Each file is a self-contained /sc:agent prompt scoped to one cleanup or tooling deliverable; four run in parallel in Phase A (markdown cleanup, main-tree), three run in parallel in Phase B (tooling, worktree-isolated), two run sequentially in Phase C (content coverage). Format is PROVISIONAL pending Task 029's ADR-governance ratification."
created: 2026-05-05
updated: 2026-05-05
---

# Task 030 — Subtask Index

> **Provisional status notice.** The structure of every file in this folder follows the [Task 019 subtask convention](../../019-fm-toolchain-suite-integration/subtasks/) — frontmatter + Goal + Falsification + Inputs + Acceptance + Dependencies + Estimated Effort + Agent Prompt. That convention has not been spec-ratified. [Task 029](../../029-adr-assumption-audit/) is expected to ratify or amend it. Do not propagate this layout to other tasks until 027 closes.

Each subtask file below contains:
- a self-contained briefing (context the agent will not have from this conversation),
- explicit inputs (file paths, line numbers, ontology IDs),
- explicit acceptance criteria (what "done" looks like, mechanically),
- a falsification clause (what observation would prove the cut wrong),
- and the agent prompt copy-pastable into `/sc:agent`.

## Phase A — Mechanical Cleanup (parallel, main-tree, 4 subtasks)

These subtasks touch overlapping markdown files; running them in worktree isolation would produce constant merge conflicts. Dispatch them as four parallel `Agent` calls in a single message but with `isolation` UNSET (main tree). Each subagent writes a small, focused commit that the driver merges sequentially in arbitrary order with conflict resolution.

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-strip-pdf-artifacts.md`](./01-strip-pdf-artifacts.md) | `refactoring-expert` | S |
| ST-2 | [`02-fix-corrupted-headings.md`](./02-fix-corrupted-headings.md) | `technical-writer` | M |
| ST-3 | [`03-fix-anchor-mismatches.md`](./03-fix-anchor-mismatches.md) | `refactoring-expert` | M |
| ST-4 | [`04-resolve-empty-redirects.md`](./04-resolve-empty-redirects.md) | `technical-writer` | S |

## Phase B — Tooling Extensions (parallel, worktree, 3 subtasks)

Independent code surfaces under `tools/dramatica-nav/`. Dispatch as three parallel `Agent` calls with `isolation: "worktree"`. Each delivers one new script + tests; merges in any order.

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-5 | [`05-build-term-editor.md`](./05-build-term-editor.md) | `python-expert` | M |
| ST-6 | [`06-build-cleanup-linter.md`](./06-build-cleanup-linter.md) | `python-expert` | S |
| ST-7 | [`07-bulk-alias-loader.md`](./07-bulk-alias-loader.md) | `python-expert` | M |

## Phase C — Content Coverage (sequential, 2 subtasks)

Phase C runs sequentially because ST-9 consumes ST-8's output. Both have large surface areas (markdown corpus or fresh JSON artefact directory).

| ID | File | Recommended agent | Effort | Isolation |
|---|---|---|---|---|
| ST-8 | [`08-scenario-tag-coverage.md`](./08-scenario-tag-coverage.md) | `quality-engineer` | M | main-tree |
| ST-9 | [`09-precompile-encoding-hints.md`](./09-precompile-encoding-hints.md) | `python-expert` | M | worktree |

## Parallel-spawn recipe

Phase A — open one driver session and dispatch in a single message containing four `Agent` tool invocations:

```
Agent(description="ST-1 strip PDF artefacts",     subagent_type="refactoring-expert",
      prompt=<paste subtasks/01-strip-pdf-artifacts.md "Agent Prompt" section>)
Agent(description="ST-2 fix corrupted headings",  subagent_type="technical-writer",
      prompt=<paste subtasks/02-fix-corrupted-headings.md>)
Agent(description="ST-3 fix anchor mismatches",   subagent_type="refactoring-expert",
      prompt=<paste subtasks/03-fix-anchor-mismatches.md>)
Agent(description="ST-4 resolve empty redirects", subagent_type="technical-writer",
      prompt=<paste subtasks/04-resolve-empty-redirects.md>)
```

Phase B — dispatch in a single message containing three `Agent` tool invocations, each with `isolation: "worktree"`:

```
Agent(description="ST-5 term editor",     subagent_type="python-expert", isolation="worktree",
      prompt=<paste subtasks/05-build-term-editor.md>)
Agent(description="ST-6 cleanup linter",  subagent_type="python-expert", isolation="worktree",
      prompt=<paste subtasks/06-build-cleanup-linter.md>)
Agent(description="ST-7 alias loader",    subagent_type="python-expert", isolation="worktree",
      prompt=<paste subtasks/07-bulk-alias-loader.md>)
```

Phase C — dispatch sequentially, one per message:

```
Agent(description="ST-8 scenario coverage", subagent_type="quality-engineer",
      prompt=<paste subtasks/08-scenario-tag-coverage.md>)

# wait for ST-8 to merge, then:
Agent(description="ST-9 precompile encoding hints", subagent_type="python-expert", isolation="worktree",
      prompt=<paste subtasks/09-precompile-encoding-hints.md>)
```

## Why this decomposition

The cuts above optimise for three properties (research-prompt-optimizer pattern):

1. **Independence at execution time.** Phase A subtasks share files; merge conflicts are localised. Phase B subtasks share NO source files — each ships a single new script. Phase C subtasks share input (the cleaned-up corpus) but produce different output surfaces.
2. **Falsifiable scope.** Each subtask file's "Falsification" section names the single observation that would prove the cut wrong. "Done" is mechanical.
3. **Tier discipline.** No subtask is allowed to make T3/T4 changes. Schema bumps (term-frontmatter.schema.json, ontology.schema.json), new ontology kinds, or amendments to AGENTS.md § Narrative Ontology are FORBIDDEN here and must be filed against [Task 029](../../029-adr-assumption-audit/).

## Convention-Provisional Notice

The Agent Prompt block format in each subtask is a literal copy-paste payload for `/sc:agent`. It assumes:

- the executing subagent reads the entire prompt as its system context,
- it has access to the agency repo at `/home/user/agency`,
- it MAY commit on its branch but MUST NOT push (per Task 019 precedent),
- it MUST run the smoke tests / validators named in the subtask's Acceptance Criteria before declaring done.

Task 027's ADR-governance spec is expected to formalise these assumptions. Until then, treat them as the working contract.
