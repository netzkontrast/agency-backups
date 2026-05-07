---
type: note
status: active
slug: core-architecture-review-2026-05-brief
summary: "Raw user request and context for the core-architecture-review-2026-05 prompt. Authored retrospectively after PR #86 review (D3) flagged the missing Actor layer."
created: 2026-05-07
updated: 2026-05-07
---

# Brief — Core Architecture Review (2026-05)

## Raw User Request

> Task for Agency: Create a new Task — adressing the following: Here's an honest assessment based on reading the specs, tooling, and actual repo state. […] What's Good […] What's Bad / Limitations […] What I Would Do Differently […]

The user provided a verbatim 10-finding architectural review of the Agency substrate as input. The Task that captured and dispatched it is `tasks/053-core-architecture-review-followups/`. This prompt is the *retrospective* Actor-layer artefact that documents the implicit instruction the audit followed — authored to close the audit-graph hole flagged as **D3 (advisory)** in the [PR #86 review](../../tasks/053-core-architecture-review-followups/review-pr86-claude-brave-darwin.md).

## Target Audience

Repository maintainer (`@netzkontrast`) and any agent re-running the audit on a future commit.

## Intended Model / Agent

Claude Code (orchestrator), single-agent execution. No subagent fan-out; the audit is small enough to run in one pass.

## Use-Case Context

Agency is a long-horizon agent-governance substrate. Periodically the substrate itself MUST be audited against its own rules to catch drift (R.19 self-violations, dual-toolchain debt, scope creep, silent failure modes). This prompt is the canonical shape such an audit takes; future repetitions SHOULD reuse it (with a fresh `core-architecture-review-YYYY-MM` slug).

## Authoring Note

This `prompt.md` was authored *after* the audit was already executed, as the disposition for D3 in [PR #86 review](../../tasks/053-core-architecture-review-followups/review-pr86-claude-brave-darwin.md). The instruction reconstructed here matches what the audit demonstrably followed — verifiable by inspecting `research/core-architecture-review-2026-05/output/REPORT.md` against the §S — Steps section.
