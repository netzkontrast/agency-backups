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
- [`002-token-efficiency-tool-suite/`](./002-token-efficiency-tool-suite/) — Build token-efficiency tooling for agentic workflows. Status: `done`.
- [`003-analyze-skillmd-novel-authoring/`](./003-analyze-skillmd-novel-authoring/) — Analyze Gemini SKILL.md novel-authoring research (DE/EN) and extract actionable recommendations. Status: `done`.
- [`004-create-missing-prompts/`](./004-create-missing-prompts/) — Author missing prompts for Tasks 001 and 002. Status: `open`.
- [`005-address-deferred-coherence-issues/`](./005-address-deferred-coherence-issues/) — Apply 148 deferred T1/T2 frontmatter stubs from coherence run 2026-05-04. Status: `open`.
- [`006-surface-skills-architecture/`](./006-surface-skills-architecture/) — Surface `skills-skill-architecture` research findings to root governance. Renumbered from `003` per TASK.md §8.1. Status: `open`.
- [`007-reconcile-closed-task-linkage/`](./007-reconcile-closed-task-linkage/) — Reconcile linkage drift in closed Tasks 002 and 003 (missing friction-logs, prompt/research field confusion, namespaced research path). Status: `open`.
- [`008-harden-coherence-baseline-protocol/`](./008-harden-coherence-baseline-protocol/) — Harden the coherence-check baseline + run-log protocol against squash-merges, malformed records, duplicate task_ids, and silent fallbacks. Status: `open`.
- [`009-author-skills-root-spec/`](./009-author-skills-root-spec/) — Author `SKILLS.md`, the missing root governance spec for `/skills/`, and wire skill-to-skill cross-references. Status: `open`.
- [`010-skills-frontmatter-index-suite/`](./010-skills-frontmatter-index-suite/) — Build the token-efficient frontmatter index + skills tool suite that operationalizes `SKILLS.md §B.5` for cross-agent navigation. Status: `open`.
- [`011-skills-frontmatter-schema-files/`](./011-skills-frontmatter-schema-files/) — Author JSON Schemas for L1/L2 frontmatter and the canonical header ontology so tools and external agents share one machine-readable contract. Status: `open`.
- [`015-integrate-dramatica-ncp-skills/`](./015-integrate-dramatica-ncp-skills/) — Spec-driven, scenario-keyed restructure of the dramatica skills with deep `ncp-author` + `novel-architect` integration via a shared Narrative Ontology, per-term frontmatter, and a token-efficient Python navigator suite. Status: `in_progress`.

## Workflow Assumptions

- Tasks reference prompts via `task_uses_prompts`; prompts are NEVER inlined inside a `task.md`.
- Tasks may spawn research; spawned research slugs equal the executing prompt's slug and are listed in `task_spawns_research`.
- The sequence number is monotonically increasing across the lifetime of the repository.
