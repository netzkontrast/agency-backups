---
type: prompt
status: active
slug: fixture-prompt
summary: "Run-start snapshot of the fixture prompt."
created: 2026-05-13
updated: 2026-05-13
prompt_kind: research-proposal
prompt_framework: RISEN
prompt_target_agent: "any"
prompt_relates_to_task: "fixture-task"
---

# Fixture Prompt (snapshot)

## Framework

RISEN.

## R — Role

Fixture executor.

## I — Input

- [`../../prompts/fixture-prompt/brief.md`](../../prompts/fixture-prompt/brief.md)

## S — Steps

1. Read the brief and source spec.
2. Produce a stub SPEC.md in `output/`.
3. Declare FL0 in `reflection/friction-log.md`.

## E — Expectations

- `output/SPEC.md` non-empty.

## Constraints

- Self-contained.
