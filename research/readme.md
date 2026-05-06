---
type: index
status: active
slug: research-root
summary: "Root of /research/. Each subfolder is the workspace produced by executing a prompt of matching slug; /research/ does not house prompt drafts."
created: 2026-05-02
updated: 2026-05-05
---

# Research Root

**What is this folder?** The execution-only home for research workspaces. Each subfolder records what running a prompt produced (workspace, synthesis, reflection, output).

**Why is it here?** To separate evidence from instruction. Prompt-craft and follow-up question authoring MUST happen in [`/prompts/`](../prompts/), not here. Coordination across runs lives in [`/tasks/`](../tasks/).

## Governing Specification

All work here MUST conform to [`RESEARCH.md`](../RESEARCH.md). Frontmatter and cross-directory linkage rules live in [`TASK.md`](../TASK.md) §3. External research ingestion rules live in [`RESEARCH.md`](../RESEARCH.md) §6.

## Contents

### In-House Research Workspaces

- [`adr-assumption-audit/`](./adr-assumption-audit/) — Critical-thinking audit (M13, M07, M06+M08) of the Task 027 SPEC and Task 028 plan. Output: [`output/REPORT.md`](./adr-assumption-audit/output/REPORT.md) — 9 hidden assumptions, 11 implicit ADRs, 7 pending decisions (2 novel), 5 Recommended Actions. Closes [Task 029](../tasks/029-adr-assumption-audit/task.md).
- [`adr-spec-research-synthesis/`](./adr-spec-research-synthesis/) — Repo-native ADR Governance Specification (§0–§9): canonical `decisions/` storage path, `adr_*` L2 namespace, guarded-section AGENTS.md synthesis, and the `agency-adr` CLI shape under `tools/adr/`. Output: [`output/SPEC.md`](./adr-spec-research-synthesis/output/SPEC.md). Closes [Task 027](../tasks/027-adr-spec-research-synthesis/task.md).
- [`agent-prompt-specs-3-systems-sdd/`](./agent-prompt-specs-3-systems-sdd/) — Spec-A/B/C: agentic prompt specifications (3-systems SDD).
- [`agentic-eval-trust-improvement-spec/`](./agentic-eval-trust-improvement-spec/) — Spec-J/K/L: evaluation, trust, improvement loops.
- [`agentic-session-continuity-spec/`](./agentic-session-continuity-spec/) — Spec-G/H/I: session continuity across runs.
- [`flexible-frontmatter-toolchain/`](./flexible-frontmatter-toolchain/) — Synthesis run: distils prior research + Anthropic's `skill-creator` into a flexible (required-only) maintenance contract plus a stateless `fm-validate / fm-extract / fm-edit / fm-query` toolchain. Supersedes the persisted-index strategy from Task 010 (see `M07-contradiction-log.md §C1`).
- [`ncp-novel-co-authoring-spec/`](./ncp-novel-co-authoring-spec/) — Narrative Context Protocol / Dramatica integration.
- [`obsidian-frontmatter-agentic-spec/`](./obsidian-frontmatter-agentic-spec/) — The Layered Schema with Namespacing model that backs this repo's frontmatter ontology.
- [`skills-namespace-ontology/`](./skills-namespace-ontology/) — Ratified `skill_*` L2 namespace: five kind values, three tier values, 14-skill mapping, two-case reciprocity rule, migration plan. Unblocks Tasks 009 and 011.
- [`spec-driven-research-agentic-workflows/`](./spec-driven-research-agentic-workflows/) — Spec-driven research workflow patterns.
- [`governance-specs-update-research/`](./governance-specs-update-research/) — Execution workspace assessing the tooling and spec drift to create an update plan for Task 026.

### External Research Results (Third-Party Sources)

See [`RESEARCH.md`](../RESEARCH.md) §6 for ingestion rules.

- [`gemini/github-skillmd-novel-authoring-de-en/result.md`](./gemini/github-skillmd-novel-authoring-de-en/result.md) — Gemini analysis of GitHub repos with SKILL.md-conformant novel-authoring capabilities (DE/EN). Downstream analysis: [`tasks/003-analyze-skillmd-novel-authoring/`](../tasks/003-analyze-skillmd-novel-authoring/).
- [`gemini/agency-adr-governance-spec/`](./gemini/agency-adr-governance-spec/) — Gemini-authored ADR governance spec (§0–§9) — MDL compression + supersession DAG paradigm. Downstream analysis: [`tasks/027-adr-spec-research-synthesis/`](../tasks/027-adr-spec-research-synthesis/) → implemented in [`tasks/031-adr-tooling-impl/`](../tasks/031-adr-tooling-impl/).
- [`gemini/superclaude-agency-orchestration-spec/`](./gemini/superclaude-agency-orchestration-spec/) — Gemini-authored SuperClaude Orchestration & Meta-Governance spec (§0–§10) proposing workspace↔command↔MCP-server mapping and `SC.CMD.*` Gherkin anchors. Self-asserts binding status; binding decision pending. Downstream analysis: [`tasks/040-superclaude-spec-evaluation/`](../tasks/040-superclaude-spec-evaluation/).

## Workflow Assumptions

- Each in-house subfolder slug equals the slug of the prompt that triggered the run (see `research_executes_prompt` in each output's frontmatter).
- Workspaces are read-mostly once `research_phase: complete`. Follow-up questions are filed as new prompts in `/prompts/`, not appended here.
- External results under `/research/<provider>/` follow the ingestion workflow in `RESEARCH.md` §6 and always have a corresponding downstream Task in `/tasks/`.
