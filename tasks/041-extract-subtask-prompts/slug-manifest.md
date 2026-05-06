---
type: note
status: active
slug: task-041-slug-manifest
summary: "Phase 1 manifest — maps the 35 subtask files under tasks/03[2-9]*/subtasks/ to target prompt slugs under /prompts/. Each subtask gets its own prompt slug; consolidation rejected (see §Decision)."
created: 2026-05-06
updated: 2026-05-06
---

# Slug Manifest — Task 041 Phase 1

## Decision: 35 subtasks → 35 unique prompt slugs (no consolidation)

The Falsification clause in `task.md` permits consolidating the 8 spec-amendment subtasks (032 ST-5, 033 ST-5, 034 ST-4, 035 ST-5, 036 ST-3, 037 ST-4, 038 ST-3, 039 ST-6) into a single `task-spec-amendment-template` prompt **only iff** the resulting prompts would be near-byte-identical apart from a handful of substitutions.

Inspection of the 8 spec-amendment subtasks shows substantial unique content per subtask:

- Different host specs (AGENTS.md / TASK.md / PROMPT.md / RESEARCH.md / FOLDERS.md / PRE_COMMIT.md / FRUSTRATED.md / MAINTENANCE.md).
- Different inputs (each cites different research SPECs and different precursor linters).
- Different acceptance criteria (different §-anchors, different Gherkin-anchor namespaces, different counts of new scenarios).
- Different dependencies (each names different sibling subtasks as predecessors).

Estimated body-divergence is ~70-80% per pair, far above the 20% consolidation threshold. Consolidation rejected; each spec-amendment subtask gets its own prompt.

The same logic applies a fortiori to the research and tooling subtasks, which have higher inter-subtask divergence.

## Slug Allocation

The slug for each prompt = the subtask filename minus its leading `NN-` index. Verified collision-free against (a) the 35 subtask filenames among themselves and (b) the existing `/prompts/<slug>/` corpus.

Each prompt is `prompt_kind: task-spec` with `prompt_relates_to_task` pointing back to its parent task slug.

| Parent task | Subtask file | Target prompt slug | prompt_relates_to_task |
|---|---|---|---|
| 032-agents-spec-integration | 01-research-adr-corpus-extraction.md | research-adr-corpus-extraction | agents-spec-integration |
| 032-agents-spec-integration | 02-tooling-narrative-ontology-load-discipline.md | tooling-narrative-ontology-load-discipline | agents-spec-integration |
| 032-agents-spec-integration | 03-tooling-rfc2119-polarity-audit.md | tooling-rfc2119-polarity-audit | agents-spec-integration |
| 032-agents-spec-integration | 04-tooling-assumption-log-substance.md | tooling-assumption-log-substance | agents-spec-integration |
| 032-agents-spec-integration | 05-spec-amendment-agents-md.md | spec-amendment-agents-md | agents-spec-integration |
| 033-task-spec-integration | 01-research-friction-pattern-synthesis.md | research-friction-pattern-synthesis | task-spec-integration |
| 033-task-spec-integration | 02-research-spec-staleness-decision-formalization.md | research-spec-staleness-decision-formalization | task-spec-integration |
| 033-task-spec-integration | 03-tooling-duplicate-task-id-linter.md | tooling-duplicate-task-id-linter | task-spec-integration |
| 033-task-spec-integration | 04-tooling-lifecycle-classifier.md | tooling-lifecycle-classifier | task-spec-integration |
| 033-task-spec-integration | 05-spec-amendment-task-md.md | spec-amendment-task-md | task-spec-integration |
| 034-prompt-spec-integration | 01-research-prompt-engineering-principle-mechanizability.md | research-prompt-engineering-principle-mechanizability | prompt-spec-integration |
| 034-prompt-spec-integration | 02-tooling-self-containedness-checker.md | tooling-self-containedness-checker | prompt-spec-integration |
| 034-prompt-spec-integration | 03-tooling-framework-declaration-validator.md | tooling-framework-declaration-validator | prompt-spec-integration |
| 034-prompt-spec-integration | 04-spec-amendment-prompt-md.md | spec-amendment-prompt-md | prompt-spec-integration |
| 035-research-spec-integration | 01-research-session-continuity-protocol-instantiation.md | research-session-continuity-protocol-instantiation | research-spec-integration |
| 035-research-spec-integration | 02-tooling-workspace-cleanliness-linter.md | tooling-workspace-cleanliness-linter | research-spec-integration |
| 035-research-spec-integration | 03-tooling-external-result-downstream-task-linter.md | tooling-external-result-downstream-task-linter | research-spec-integration |
| 035-research-spec-integration | 04-tooling-trust-audit-gate.md | tooling-trust-audit-gate | research-spec-integration |
| 035-research-spec-integration | 05-spec-amendment-research-md.md | spec-amendment-research-md | research-spec-integration |
| 036-folders-spec-integration | 01-tooling-readme-frontmatter-validator.md | tooling-readme-frontmatter-validator | folders-spec-integration |
| 036-folders-spec-integration | 02-tooling-audit-graph-consistency-checker.md | tooling-audit-graph-consistency-checker | folders-spec-integration |
| 036-folders-spec-integration | 03-spec-amendment-folders-md.md | spec-amendment-folders-md | folders-spec-integration |
| 037-pre-commit-spec-integration | 01-research-pre-commit-readme-update-cadence.md | research-pre-commit-readme-update-cadence | pre-commit-spec-integration |
| 037-pre-commit-spec-integration | 02-tooling-clean-working-directory-linter.md | tooling-clean-working-directory-linter | pre-commit-spec-integration |
| 037-pre-commit-spec-integration | 03-tooling-per-rule-waiver-mechanism.md | tooling-per-rule-waiver-mechanism | pre-commit-spec-integration |
| 037-pre-commit-spec-integration | 04-spec-amendment-pre-commit-md.md | spec-amendment-pre-commit-md | pre-commit-spec-integration |
| 038-frustrated-spec-integration | 01-research-fl0-value-justification.md | research-fl0-value-justification | frustrated-spec-integration |
| 038-frustrated-spec-integration | 02-tooling-fl-declaration-linter.md | tooling-fl-declaration-linter | frustrated-spec-integration |
| 038-frustrated-spec-integration | 03-spec-amendment-frustrated-md.md | spec-amendment-frustrated-md | frustrated-spec-integration |
| 039-maintenance-spec-integration | 01-research-toolchain-flip-criteria.md | research-toolchain-flip-criteria | maintenance-spec-integration |
| 039-maintenance-spec-integration | 02-research-staleness-decision-formalization.md | research-staleness-decision-formalization | maintenance-spec-integration |
| 039-maintenance-spec-integration | 03-tooling-staleness-audit-script.md | tooling-staleness-audit-script | maintenance-spec-integration |
| 039-maintenance-spec-integration | 04-tooling-dynamic-readme-partition-linter.md | tooling-dynamic-readme-partition-linter | maintenance-spec-integration |
| 039-maintenance-spec-integration | 05-tooling-trust-audit-integration.md | tooling-trust-audit-integration | maintenance-spec-integration |
| 039-maintenance-spec-integration | 06-spec-amendment-maintenance-md.md | spec-amendment-maintenance-md | maintenance-spec-integration |

Total: 35 source rows → 35 unique target prompt slugs.

## Notes

- Note that `research-spec-staleness-decision-formalization` (033 ST-2) and `research-staleness-decision-formalization` (039 ST-2) are intentionally distinct slugs reflecting the distinct subtask filenames; they cover related but distinct research questions per their respective subtask bodies.
- `prompt_relates_to_task` is scalar per the ontology reciprocity rule (`task.task_uses_prompts ↔ prompt.prompt_relates_to_task`, scalar=true). Each prompt has exactly one parent task; the parent task's `task_uses_prompts` lists every child prompt.
