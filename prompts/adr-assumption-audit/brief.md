---
type: brief
status: active
slug: adr-assumption-audit-brief
summary: "User request to create a task using subagents and critical thinking from the Research Prompt Optimizer to surface hidden assumptions, identify active ADRs, and enumerate pending decisions."
created: 2026-05-05
updated: 2026-05-05
---

# Brief — ADR Assumption Audit

## Raw User Request

> another Task, that uses subagents to extract and think through (use critical thinking from the Research prompt optimizer skill) what hidden assumptions where made.. what Adrs are in effect, and what descissions have to be made

## Target Audience

Repository maintainer and any agent executing Task 028.

## Intended Model / Agent

Claude Code (orchestrator); three parallel subagents for M13, M07, M06+M08 method execution.

## Use-Case Context

The ADR governance spec was generated without full repo access, meaning hidden assumptions were baked in. This prompt drives an adversarial audit using the critical-thinking methods from the Research Prompt Optimizer verbatim (M06, M07, M08, M13) to find what the spec assumed without evidence, what architectural decisions the repo has already implicitly made, and what open questions must be resolved before implementation begins.
