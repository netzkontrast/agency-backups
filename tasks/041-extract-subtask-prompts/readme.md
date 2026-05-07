---
type: index
status: active
slug: task-041-extract-subtask-prompts
summary: "Folder index for Task 041 — extract 35 inlined `## Execution Brief` blocks from tasks 032-039 subtasks to proper /prompts/<slug>/prompt.md files; populate task_uses_prompts on Tasks 032-040 to close the audit-graph debt surfaced by PR #70 review C.3."
created: 2026-05-06
updated: 2026-05-06
---

# Task 041 Folder

## What

Operational folder for Task 041 — the audit-graph repair Task that closes [PR #70 review finding C.3](https://github.com/netzkontrast/agency/pull/70#issuecomment-4390879904). Filed per Option B of the maintainer's reply: "keep this PR focused on chain design; close the audit-graph debt as its own auditable unit of work."

## Files

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- (mid-execution) `slug-manifest.md` — Phase 1 output mapping the 35 source subtask Execution Briefs to their target prompt slugs (some may consolidate).

## Sequencing

**Task 041 MUST land before any subtask in Tasks 032–040 is dispatched.** Otherwise a dispatching agent would read the inlined Execution Brief and bypass the audit graph entirely. This ordering is informational rather than via `task_blocked_by` — Task 041 itself has no blockers and can start immediately.

## Assumptions Log

- Phase 1's slug-allocation policy decides whether the 6 spec-amendment subtasks (one per host spec) consolidate to a single `task-spec-amendment-template` prompt parametrized by host + acceptance anchors, or remain 8 distinct prompts. The Falsification clause in `task.md` constrains this: if shape divergence <20%, consolidate.
- The mechanical Phase 2 + Phase 3 work is amenable to a Python script driven by the Phase 1 manifest. The Task ships that script under `tasks/041-extract-subtask-prompts/scripts/extract.py` if useful, otherwise inline in the prompt body.
- Task 020 (`audit-prompt-fm-validate-conformance`) and this Task share scope on `/prompts/` health. Task 020 audits *existing* prompts; Task 041 *creates* new prompts that conform to the same contract. The two tasks complement; no merge is needed.
