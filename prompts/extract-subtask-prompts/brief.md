---
type: note
status: active
slug: extract-subtask-prompts-brief
summary: "Brief for prompt extract-subtask-prompts — drives Task 041's bulk extraction of 35 inlined subtask Execution Briefs to /prompts/<slug>/ folders, restoring the task→prompt audit-graph edge severed in PR #70 review C.3."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — Extract Subtask Prompts

## Raw User Request

> Close the audit-graph debt surfaced by [PR #70 review C.3](https://github.com/netzkontrast/agency/pull/70#issuecomment-4390879904) per Option B of the maintainer's reply: extract the inlined `## Execution Brief` blocks (and adjacent prompt content) from `tasks/03[2-9]*/subtasks/*.md` into proper `/prompts/<slug>/` folders carrying the F.4.1.1-mandatory three-file scaffold, then populate `task_uses_prompts` on Tasks 032–039 to restore the `task → prompt` reciprocity edge.

## Target Audience

The maintenance agent dispatched to execute [Task 041](../../tasks/041-extract-subtask-prompts/task.md). The task is a one-shot bulk migration; the prompt is registered retroactively to satisfy TASK.md §1 ("A Task MUST NOT inline a prompt; it MUST link to one") and to close the F-D finding from PR #72 review (`task_uses_prompts: []` on the policy-enforcement task itself).

## Intended Model / Agent

Claude Code. The actual execution leans on a deterministic Python driver at [`tasks/041-extract-subtask-prompts/scripts/extract.py`](../../tasks/041-extract-subtask-prompts/scripts/extract.py); the agent's role is to author the slug-allocation manifest, run the script, fix any governance diagnostics, and close the task.

## Use-Case Context

Task 041 is sequenced as the **first** task in the chain spanning Tasks 032–039: every downstream subtask MUST consume a registered `/prompts/<slug>/prompt.md` rather than an inlined Execution Brief. This prompt encodes the bulk migration that establishes that contract. It is registered after the fact (PR #72 originally closed Task 041 with `task_uses_prompts: []`); the registration here aligns Task 041 with the policy it enforces on Tasks 032–039.

## Scope (what the prompt drives)

- Phase 1 — author `slug-manifest.md` mapping the 35 source subtask files to target prompt slugs; decide on consolidation (default: 35 unique slugs unless body-divergence is <20% per pair).
- Phase 2 — bulk-scaffold 35 `/prompts/<slug>/{brief.md, prompt.md, readme.md}` triplets; migrate Goal / Falsification / Inputs / Acceptance / Dependencies / Estimated Effort / Execution Brief sections from each parent subtask file.
- Phase 3 — populate `task_uses_prompts` on Tasks 032–039; replace each subtask file body with a thin `**Prompt:**` cross-reference.
- Phase 4 — verify `tools/check-governance.sh --no-trust` exits 0; reciprocity holds across `task_uses_prompts ↔ prompt_relates_to_task`.
- Phase 5 — update indexes, author `friction-log.md`, set `task_status: done`.
