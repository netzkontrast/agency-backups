---
type: note
status: active
slug: adr-tooling-impl-brief
summary: "User request — capture the implementation work that landed in PR #67 as a proper follow-up Task with a registered task-spec prompt, addressing PR #67 review findings G.1 (Task entry) and G.2 (prompt boundary violation)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ADR Tooling Implementation

## Raw User Request

> Follow up Task

(Reply to the PR #67 review triage triage, which proposed creating `tasks/031-adr-tooling-impl/` plus a registered prompt artefact under `prompts/adr-tooling-impl/`.)

## Target Audience

Repository maintainer; any agent that needs to re-run or audit the `agency-adr` implementation; reviewers of PR [#67](https://github.com/netzkontrast/agency/pull/67).

## Intended Model / Agent

Claude Code.

## Use-Case Context

[Task 028](../../tasks/028-adr-tooling-impl-plan/) produced a build contract for the `agency-adr` CLI ([`implementation-plan.md`](../../tasks/028-adr-tooling-impl-plan/implementation-plan.md)) but explicitly forbade writing any code. The implementation work that followed (PR [#67](https://github.com/netzkontrast/agency/pull/67)) crossed that boundary by design — it is the successor unit of work — but no prompt artefact was registered for it. The PR #67 review at [`../../tasks/028-adr-tooling-impl-plan/pr67-review.md`](../../tasks/028-adr-tooling-impl-plan/pr67-review.md) flagged this as governance violation G.2.

This prompt closes that gap. It is the executable instruction set for Task 031; reading it alongside the implementation plan and the ADR governance spec is sufficient context to reproduce the implementation from scratch.
