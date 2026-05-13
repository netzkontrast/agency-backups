---
type: prompt
status: active
slug: fixture-prompt
summary: "Minimal valid prompt referenced by Task 099 in the integration-test fixture."
created: 2026-05-13
updated: 2026-05-13
prompt_kind: research-proposal
prompt_framework: RISEN
prompt_target_agent: "any"
prompt_relates_to_task: "fixture-task"
---

# Fixture Prompt

## Framework

RISEN — the prompt is a single-shot research proposal, no ReAct loop needed.

## R — Role

You are a fixture executor; you exist to be linted, not executed.

## I — Input

- [`brief.md`](./brief.md) — the source question

## S — Steps

1. Read [`brief.md`](./brief.md) and the linked spec context.
2. Produce a one-paragraph `SPEC.md` in `/research/fixture-research/output/`.
3. Write a brief `friction-log.md` declaring FL0.

## E — Expectations

- `output/SPEC.md` MUST exist and MUST be non-empty.

## Constraints

- The fixture MUST remain self-contained; no external network reads.
