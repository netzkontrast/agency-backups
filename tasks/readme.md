---
type: index
status: active
slug: tasks-root
summary: "Root of /tasks/. Each subfolder is one orchestrated unit of work linking prompts, research, and code via frontmatter."
created: 2026-05-04
updated: 2026-05-04
---

# Tasks Root

**What is this folder?** The orchestration layer of the repository. A Task assigns a goal, plans steps, and links — via frontmatter only — to the prompts it executes and the artifacts it touches.

**Why is it here?** To stop burying coordination work inside `/research/` or scattering it across PR descriptions. Tasks make the audit graph (Task → Prompt → Research) queryable.

## Governing Specification

All work here MUST conform to [`TASK.md`](../TASK.md). Cross-directory linkage rules and the Frontmatter Ontology live there.

## Naming

Subfolders follow `<NNN>-<slug>/` where `<NNN>` is a zero-padded sequence number and `<slug>` is kebab-case (max 5 tokens).

## Contents

- [`000-decouple-architecture/`](./000-decouple-architecture/) — Bootstrap meta-task that introduced this folder, the Frontmatter Ontology, `TASK.md`, templates, and the validator. Status: `done`.
- [`001-refactor-governance-from-specs/`](./001-refactor-governance-from-specs/) — Encode rules from Spec-A/B/C, Spec-G/H/I, and Spec-J/K/L into linters, hooks, and templates. Status: `open`.
- [`002-token-efficiency-tool-suite/`](./002-token-efficiency-tool-suite/) — Build token-efficiency tooling for agentic workflows. Status: `open`.
- [`003-analyze-skillmd-novel-authoring/`](./003-analyze-skillmd-novel-authoring/) — Analyze Gemini SKILL.md novel-authoring research (DE/EN) and extract actionable recommendations. Status: `open`.

## Workflow Assumptions

- Tasks reference prompts via `task_uses_prompts`; prompts are NEVER inlined inside a `task.md`.
- Tasks may spawn research; spawned research slugs equal the executing prompt's slug and are listed in `task_spawns_research`.
- The sequence number is monotonically increasing across the lifetime of the repository.
