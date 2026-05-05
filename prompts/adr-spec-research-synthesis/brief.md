---
type: brief
status: active
slug: adr-spec-research-synthesis-brief
summary: "User request to analyze root specs and tooling, brainstorm integration with the Gemini ADR governance draft, and execute a research run producing the repo-native ADR governance specification."
created: 2026-05-05
updated: 2026-05-05
---

# Brief — ADR Spec Research Synthesis

## Raw User Request

> Create a new Task, with the goal of /sc:analyze and /sc:brainstorm the current Root specs, and tooling - to Create and execute a Research Task… with the goal of integrating the current repos specs, and there Interaktion with the newly created adr spec (wich is the Overall goal… to Create that spec…) use superclaude skills and Command where possible - with the spec generated, the Task is Done

## Target Audience

Repository maintainer and any agent executing Task 027.

## Intended Model / Agent

Claude Code (primary); model-agnostic for the research execution phase.

## Use-Case Context

The Gemini-generated ADR governance spec (`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`) is a theoretically sound but repo-ungrounded document. This prompt drives the work that grounds it: analyze actual root specs and tooling, brainstorm the integration gaps, and synthesize a deployable §0–§9 spec that enforces correctly within the existing `netzkontrast/agency` governance conventions.
