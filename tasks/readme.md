---
type: index
status: active
slug: tasks-root
summary: "Root of /tasks/. Each subfolder is one orchestrated unit of work linking prompts, research, and code via frontmatter."
created: 2026-05-04
updated: 2026-05-05
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
- [`001-refactor-governance-from-specs/`](./001-refactor-governance-from-specs/) — Encode rules from Spec-A/B/C, Spec-G/H/I, and Spec-J/K/L into linters, hooks, and templates. Status: `updated` → superseded by [026](./026-update-governance-specs-from-research/).
- [`002-token-efficiency-tool-suite/`](./002-token-efficiency-tool-suite/) — Build token-efficiency tooling for agentic workflows. Status: `done`.
- [`003-analyze-skillmd-novel-authoring/`](./003-analyze-skillmd-novel-authoring/) — Analyze Gemini SKILL.md novel-authoring research (DE/EN) and extract actionable recommendations. Status: `done`.
- [`004-create-missing-prompts/`](./004-create-missing-prompts/) — Author missing prompts for Tasks 001 and 002. Status: `updated` → superseded by [020](./020-audit-prompt-fm-validate-conformance/).
- [`005-address-deferred-coherence-issues/`](./005-address-deferred-coherence-issues/) — Apply 148 deferred T1/T2 frontmatter stubs from coherence run 2026-05-04. Status: `updated` → superseded by [021](./021-apply-fm-edit-to-deferred-coherence/).
- [`006-skills-navigation-bootstrap/`](./006-skills-navigation-bootstrap/) — Research and design the internal skill navigation architecture, bootstrap process, and propose a root skill.md spec. Status: `done`. (Note: shares `task_id: "006"` with `006-surface-skills-architecture/` pending the renumber tracked by [Task 024](./024-renumber-duplicate-task-ids-v2/).)
- [`006-surface-skills-architecture/`](./006-surface-skills-architecture/) — Surface `skills-skill-architecture` research findings to root governance. Renumbered from `003` per TASK.md §8.1. Status: `open`.
- [`007-reconcile-closed-task-linkage/`](./007-reconcile-closed-task-linkage/) — Reconcile linkage drift in closed Tasks 002 and 003 (missing friction-logs, prompt/research field confusion, namespaced research path). Status: `open`.
- [`008-harden-coherence-baseline-protocol/`](./008-harden-coherence-baseline-protocol/) — Harden the coherence-check baseline + run-log protocol against squash-merges, malformed records, duplicate task_ids, and silent fallbacks. Status: `open`.
- [`009-author-skills-root-spec/`](./009-author-skills-root-spec/) — Author `SKILLS.md`, the missing root governance spec for `/skills/`, and wire skill-to-skill cross-references. Status: `open`.
- [`009-review-pr28-readme-spec/`](./009-review-pr28-readme-spec/) — Structured governance review of PR #28 (root README + self-update spec). Status: `in_progress`. (Note: shares `task_id: "009"` with `009-author-skills-root-spec/` pending the renumber tracked by [Task 024](./024-renumber-duplicate-task-ids-v2/).)
- [`010-skills-frontmatter-index-suite/`](./010-skills-frontmatter-index-suite/) — Build the token-efficient frontmatter index + skills tool suite that operationalizes `SKILLS.md §B.5` for cross-agent navigation. Status: `updated` → superseded by [022](./022-skills-query-cli-atop-fm-query/) per `research/flexible-frontmatter-toolchain/output/SPEC.md §C1`.
- [`011-skills-frontmatter-schema-files/`](./011-skills-frontmatter-schema-files/) — Author JSON Schemas for L1/L2 frontmatter and the canonical header ontology so tools and external agents share one machine-readable contract. Status: `updated` → superseded by [023](./023-header-ontology-and-schema-mirror/); the canonical contract now lives at `maintenance/schemas/header-ontology.json`.
- [`012-review-pr-29/`](./012-review-pr-29/) — Structured code review of PR #29 (skills governance, Tasks 009–011). Status: `in_progress`.
- [`013-renumber-duplicate-task-ids/`](./013-renumber-duplicate-task-ids/) — Resolve duplicate `task_id` collisions for ids 006 and 009 per TASK.md §8.1. Status: `updated` → superseded by [024](./024-renumber-duplicate-task-ids-v2/) (target slots 014/015 are no longer free).
- [`014-improve-maintenance-spec-from-session/`](./014-improve-maintenance-spec-from-session/) — Capture maintenance-spec improvements distilled from the 2026-05-05 coherence run. Status: `updated` → superseded by [025](./025-maintenance-spec-remaining-findings/) (F1/F5/F6 already absorbed; F2/F3/F4/F7 carried forward).
- [`015-integrate-dramatica-ncp-skills/`](./015-integrate-dramatica-ncp-skills/) — Spec-driven, scenario-keyed restructure of the dramatica skills with deep `ncp-author` + `novel-architect` integration via a shared Narrative Ontology, per-term frontmatter, and a token-efficient Python navigator suite. Status: `in_progress`. (Renumbered from 013 per TASK.md §8.1 — collided with main's Task 013.)
- [`016-flexible-frontmatter-toolchain/`](./016-flexible-frontmatter-toolchain/) — Implement the four-tool stateless toolchain (`fm-validate / fm-extract / fm-edit / fm-query`) and the per-type required-headings ontology specified in `research/flexible-frontmatter-toolchain/output/SPEC.md`. Status: `open`.
- [`017-migrate-repo-to-flexible-toolchain/`](./017-migrate-repo-to-flexible-toolchain/) — Migrate the repo onto the flexible toolchain shipped by Task 016 in three batches (mechanical, additive, structural); retire the legacy linters; scope-narrow Task 010 per SPEC §C1. Status: `blocked` (gated on Task 016).
- [`018-fm-section-editor/`](./018-fm-section-editor/) — Build the `fm-section` editor (replace/append/insert/delete/rename) per SPEC §13. Status: `open`.
- [`019-fm-toolchain-suite-integration/`](./019-fm-toolchain-suite-integration/) — Decompose the gap between the four-tool fm-* atomic surface and a complete authoring/refactoring/validation toolchain into nine parallelizable subtasks. Status: `open`.
- [`020-audit-prompt-fm-validate-conformance/`](./020-audit-prompt-fm-validate-conformance/) — Successor to [Task 004](./004-create-missing-prompts/). Bring every `/prompts/<slug>/prompt.md` into conformance with the prompt-type required-headings contract. Status: `open`.
- [`021-apply-fm-edit-to-deferred-coherence/`](./021-apply-fm-edit-to-deferred-coherence/) — Successor to [Task 005](./005-address-deferred-coherence-issues/). Apply deferred T1/T2 frontmatter stubs via `tools/fm/edit.py` after the Task 017 migration completes. Status: `open` (blocked by [017](./017-migrate-repo-to-flexible-toolchain/)).
- [`022-skills-query-cli-atop-fm-query/`](./022-skills-query-cli-atop-fm-query/) — Successor to [Task 010](./010-skills-frontmatter-index-suite/). Thin skills-query convenience wrapper atop the stateless `tools/fm/query.py`; no persistent index. Status: `open` (blocked by [019](./019-fm-toolchain-suite-integration/)).
- [`023-header-ontology-and-schema-mirror/`](./023-header-ontology-and-schema-mirror/) — Successor to [Task 011](./011-skills-frontmatter-schema-files/). Add the per-type JSON Schema *mirror* (generated from `header-ontology.json`) plus a divergence gate. Status: `open`.
- [`024-renumber-duplicate-task-ids-v2/`](./024-renumber-duplicate-task-ids-v2/) — Successor to [Task 013](./013-renumber-duplicate-task-ids/). Renumber the persistent 006/006 and 009/009 duplicates into the next free slots. Status: `open`.
- [`025-maintenance-spec-remaining-findings/`](./025-maintenance-spec-remaining-findings/) — Successor to [Task 014](./014-improve-maintenance-spec-from-session/). Carry forward only F2 / F3 / F4 / F7 (F1 / F5 / F6 absorbed by Tasks 008 + 016). Status: `open` (blocked by [019](./019-fm-toolchain-suite-integration/)).
- [`026-update-governance-specs-from-research/`](./026-update-governance-specs-from-research/) — Successor to [Task 001](./001-refactor-governance-from-specs/). Implement the governance specs update plan derived from research on the current tooling ecosystem. Status: `done`.
- [`027-adr-spec-research-synthesis/`](./027-adr-spec-research-synthesis/) — Analyze root specs + tooling via `/sc:analyze` and `/sc:brainstorm`, then execute a Research run producing the repo-native ADR governance specification (§0–§9) that integrates the Gemini draft with this repo's actual governance conventions. Status: `done`. Output: [`research/adr-spec-research-synthesis/output/SPEC.md`](../research/adr-spec-research-synthesis/output/SPEC.md). Unblocks Tasks 028 and 029.
- [`028-adr-tooling-impl-plan/`](./028-adr-tooling-impl-plan/) — From the spec produced by Task 027, design the concrete implementation plan for the `agency-adr` CLI tool suite (validate, synthesize/MDL, DAG cycle-detection, JSON-Schema linter, CI integration). Status: `done`. Output: [`implementation-plan.md`](./028-adr-tooling-impl-plan/implementation-plan.md) — §1–§7 build contract; ≈ 3–5 working weeks of implementation effort estimated.
- [`029-adr-assumption-audit/`](./029-adr-assumption-audit/) — Multi-subagent critical-thinking audit (M13, M07, M06+M08) that surfaces hidden assumptions in the ADR governance spec, catalogues implicit ADRs already in force in this repo, and enumerates pending decisions blocking the Task 028 implementation. Status: `done`. Output: [`research/adr-assumption-audit/output/REPORT.md`](../research/adr-assumption-audit/output/REPORT.md) — 9 ASMs (4 high-blast), 11 IADRs (5 P1), 7 PDs (2 novel: PD-006 review loop, PD-007 stale-Proposed lifecycle), 5 Recommended Actions. PD↔OD cross-reference appended as [Task 028 plan §B](./028-adr-tooling-impl-plan/implementation-plan.md).
- [`030-cleanup-dramatica-skills-corpus/`](./030-cleanup-dramatica-skills-corpus/) — Phase-0 follow-up to [Task 015](./015-integrate-dramatica-ncp-skills/). Strip PDF artefacts from the dramatica corpus, fix corrupted headings + anchor mismatches, ship `term.py` / `cleanup.py` / `aliases.py` / `precompile.py` under `tools/dramatica-nav/`, and emit pre-compiled persona-scenario JSONs. Nine subtasks dispatch via `/sc:agent`. The FE-1…FE-10 frustration items in its `notes.md §3` are candidate inputs for [Task 029](./029-adr-assumption-audit/)'s assumption audit. Status: `open`.

## Workflow Assumptions

- Tasks reference prompts via `task_uses_prompts`; prompts are NEVER inlined inside a `task.md`.
- Tasks may spawn research; spawned research slugs equal the executing prompt's slug and are listed in `task_spawns_research`.
- The sequence number is monotonically increasing across the lifetime of the repository.
