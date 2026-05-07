---
type: index
status: active
slug: tooling-adr-mirror-roundtrip-check-prompt-readme
summary: "Index for prompt tooling-adr-mirror-roundtrip-check — ships a linter that asserts every IADR row in research/adr-corpus-extraction-from-governance-specs/output/SPEC.md has a corresponding `decisions/<NNNN>-<slug>.md` body whose adr_id and source citation match the SPEC mirror."
created: 2026-05-07
updated: 2026-05-07
---

# Prompt — tooling-adr-mirror-roundtrip-check

- [`brief.md`](./brief.md) — Subtask orientation: Goal, Falsification, Inputs, Acceptance, Dependencies, Effort.
- [`prompt.md`](./prompt.md) — The executable RISEN+ReAct task-spec prompt.

## Origin

Filed in response to PR #79 review finding **R-5** (`maintenance/pr-79-review.md` §"Minor Finding"): the SPEC.md mirror ↔ `decisions/<NNNN>-<slug>.md` round-trip has no mechanical check today, surfaced as FL1 in [Task 032's friction log](../../tasks/032-agents-spec-integration/friction-log.md). PROMPT.md §1 item 2 requires follow-up questions to land as new prompts, not loose friction-log entries.

## Usage

Execute when a successor Task adopts this prompt via its `task_uses_prompts` list. The prompt is currently **unbound** — `prompt_relates_to_task` is empty until a successor task claims it.
