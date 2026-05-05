---
type: index
status: active
slug: research-root
summary: "Root of /research/. Each subfolder is the workspace produced by executing a prompt of matching slug; /research/ does not house prompt drafts."
created: 2026-05-02
updated: 2026-05-04
---

# Research Root

**What is this folder?** The execution-only home for research workspaces. Each subfolder records what running a prompt produced (workspace, synthesis, reflection, output).

**Why is it here?** To separate evidence from instruction. Prompt-craft and follow-up question authoring MUST happen in [`/prompts/`](../prompts/), not here. Coordination across runs lives in [`/tasks/`](../tasks/).

## Governing Specification

All work here MUST conform to [`RESEARCH.md`](../RESEARCH.md). Frontmatter and cross-directory linkage rules live in [`TASK.md`](../TASK.md) §3. External research ingestion rules live in [`RESEARCH.md`](../RESEARCH.md) §6.

## Contents

### In-House Research Workspaces

- [`agent-prompt-specs-3-systems-sdd/`](./agent-prompt-specs-3-systems-sdd/) — Spec-A/B/C: agentic prompt specifications (3-systems SDD).
- [`agentic-eval-trust-improvement-spec/`](./agentic-eval-trust-improvement-spec/) — Spec-J/K/L: evaluation, trust, improvement loops.
- [`agentic-session-continuity-spec/`](./agentic-session-continuity-spec/) — Spec-G/H/I: session continuity across runs.
- [`ncp-novel-co-authoring-spec/`](./ncp-novel-co-authoring-spec/) — Narrative Context Protocol / Dramatica integration.
- [`obsidian-frontmatter-agentic-spec/`](./obsidian-frontmatter-agentic-spec/) — The Layered Schema with Namespacing model that backs this repo's frontmatter ontology.
- [`skills-namespace-ontology/`](./skills-namespace-ontology/) — Ratified `skill_*` L2 namespace: five kind values, three tier values, 14-skill mapping, two-case reciprocity rule, migration plan. Unblocks Tasks 009 and 011.
- [`spec-driven-research-agentic-workflows/`](./spec-driven-research-agentic-workflows/) — Spec-driven research workflow patterns.

### External Research Results (Third-Party Sources)

See [`RESEARCH.md`](../RESEARCH.md) §6 for ingestion rules.

- [`gemini/github-skillmd-novel-authoring-de-en/result.md`](./gemini/github-skillmd-novel-authoring-de-en/result.md) — Gemini analysis of GitHub repos with SKILL.md-conformant novel-authoring capabilities (DE/EN). Downstream analysis: [`tasks/003-analyze-skillmd-novel-authoring/`](../tasks/003-analyze-skillmd-novel-authoring/).

## Workflow Assumptions

- Each in-house subfolder slug equals the slug of the prompt that triggered the run (see `research_executes_prompt` in each output's frontmatter).
- Workspaces are read-mostly once `research_phase: complete`. Follow-up questions are filed as new prompts in `/prompts/`, not appended here.
- External results under `/research/<provider>/` follow the ingestion workflow in `RESEARCH.md` §6 and always have a corresponding downstream Task in `/tasks/`.
