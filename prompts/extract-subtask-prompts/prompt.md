---
type: prompt
status: active
slug: extract-subtask-prompts
summary: "Drives Task 041 — extract 35 inlined subtask Execution Briefs to /prompts/<slug>/ folders, populate task_uses_prompts on Tasks 032–039, and verify the task↔prompt audit-graph edge via tools/check-governance.sh + tools/fm/validate.py --type-check."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: extract-subtask-prompts
---

# Extract Subtask Prompts — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; **Constraints** groups normative scope and failure rules per repo convention.

## R — Role

You are the **Maintenance Agent** dispatched to execute [Task 041](../../tasks/041-extract-subtask-prompts/task.md). Your remit is the bulk migration of 35 inlined subtask briefs into registered `/prompts/<slug>/` folders. You SHOULD lean on a deterministic Python driver for the mechanical work and reserve agent judgment for Phase 1 slug allocation and Phase 5 closure.

## I — Input

- [`tasks/041-extract-subtask-prompts/task.md`](../../tasks/041-extract-subtask-prompts/task.md) — the Task this prompt drives (Goal, Plan, Falsification, Estimated Effort, Links).
- [`tasks/041-extract-subtask-prompts/readme.md`](../../tasks/041-extract-subtask-prompts/readme.md) — folder index and Assumptions Log.
- All 35 subtask files under `tasks/03[2-9]*/subtasks/[0-9]*.md` (the migration sources).
- Each parent task `tasks/03[2-9]*/task.md` (the destination of `task_uses_prompts` updates).
- [`templates/prompt.md`](../../templates/prompt.md) — base template for new `prompt.md` files.
- [`templates/notes.md`](../../templates/notes.md) — base template for new `brief.md` / friction-log files.
- [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json) — type enum, required keys, required headings, reciprocity rules.
- [`AGENTS.md`](../../AGENTS.md), [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`FOLDERS.md`](../../FOLDERS.md) — governing specs (frontmatter ontology, prompt §3 schema, F.4.1.1 three-file scaffold).

## S — Steps

1. The agent MUST author `tasks/041-extract-subtask-prompts/slug-manifest.md` listing every source subtask file with its target prompt slug; the agent MUST evaluate the 8 spec-amendment subtasks for consolidation per Task 041 §Falsification (consolidate iff body-divergence <20% per pair) and document the decision.
2. The agent SHOULD ship a deterministic Python driver under `tasks/041-extract-subtask-prompts/scripts/extract.py` that consumes the slug manifest and performs Phases 2 and 3 mechanically; the agent MAY extend `tools/fm/new.py` instead if that path is cleaner.
3. The agent MUST scaffold every target `/prompts/<slug>/` with the F.4.1.1-mandatory three-file scaffold (`brief.md` carrying `type: note`, `prompt.md` carrying `type: prompt` + `prompt_kind: task-spec` + `prompt_relates_to_task: <parent-task-slug>`, `readme.md` carrying `type: index`); the agent MUST migrate the source subtask's Goal / Falsification / Inputs / Acceptance / Dependencies / Estimated Effort sections into `brief.md` and synthesise its Execution Brief content into `prompt.md`'s `## S — Steps` as RFC-2119-normative discrete deliverables (no verbatim wrapping that re-introduces opacity).
4. The agent MUST collapse every source subtask file body to a thin pointer carrying only L1 frontmatter, the H1 title, the Executor / Parallelism / Insertion-point metadata lines, and a one-line `**Prompt:**` cross-reference to the corresponding `/prompts/<slug>/prompt.md`.
5. The agent MUST append every new prompt slug to its parent task's `task_uses_prompts` list via a line-based frontmatter edit that preserves original quoting (avoid full YAML round-trips that drop quote characters from string-typed values like `task_id`).
6. The agent MUST run `tools/check-governance.sh --no-trust` and `tools/fm/validate.py --type-check`, both of which MUST exit 0 with reciprocity verified across `task_uses_prompts ↔ prompt_relates_to_task` for every parent-task / child-prompt pair.
7. The agent MUST update `tasks/readme.md` (Task 041 entry → status `done`) and `prompts/readme.md` (~35 new entries grouped by parent task), and SHOULD author `tasks/041-extract-subtask-prompts/friction-log.md` with an FL[0-3] declaration covering frictions encountered.
8. The agent MUST set `task_status: done` and `task_owner: <agent-identifier>` on `tasks/041-extract-subtask-prompts/task.md`, then commit with a descriptive message and push to the working branch; the agent MUST NOT push to `main` directly.

## E — Expectations

- 35 new `/prompts/<slug>/` folders, each carrying the F.4.1.1 three-file scaffold; every `brief.md` carries `type: note`; every `prompt.md` carries `type: prompt` + `prompt_kind: task-spec` + a non-empty `prompt_relates_to_task`.
- Every source subtask file under `tasks/03[2-9]*/subtasks/[0-9]*.md` is a thin pointer (no inlined Goal / Falsification / Inputs / Acceptance / Dependencies / Effort / Execution Brief sections).
- `tasks/03[2-9]*/task.md` carry non-empty `task_uses_prompts` lists naming every child prompt slug.
- `tools/check-governance.sh --no-trust` exits 0; `tools/fm/validate.py --type-check` reports `Checked <N> files; 0 diagnostic(s)` with N reflecting the +70 operational files added under `/prompts/`.
- `tasks/readme.md` + `prompts/readme.md` updated; `tasks/041-extract-subtask-prompts/{slug-manifest.md, friction-log.md, scripts/extract.py}` shipped; `task_status: done`.
- A pull request is open against `main` with the test plan checklist from this prompt's Expectations section.

## Constraints

- The agent MUST NOT inline any prompt content into a subtask or task file; the contract is `task → prompt → brief`, never `task → brief` directly.
- The agent MUST NOT bypass `path_classification` blind spots silently; if a generated artefact's `type` value is not enforced by the validator (e.g. `prompts/*/brief.md`), the agent MUST still pick a value from the closed enum (`note` for briefs).
- The agent MUST NOT propagate template defaults that violate spec semantics; OPTIONAL frontmatter fields (e.g. `prompt_spawned_from_research`) MUST be omitted when not applicable, never left as empty strings.
- The agent SHOULD NOT consolidate the 8 spec-amendment subtasks into a single template-prompt unless inspection confirms <20% body divergence per pair; if divergence is higher, each subtask MUST get its own slug.
- The agent SHOULD prefer line-based frontmatter edits over full YAML round-trips when mutating `task_uses_prompts`, to preserve original quoting.
