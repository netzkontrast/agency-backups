---
type: index
status: active
slug: prompts-root
summary: "Root of /prompts/. Holds every executable instruction set: research proposals, follow-ups, tool instructions, task-specs."
created: 2026-05-02
updated: 2026-05-06
# (also lists: author-skills-root-spec, skills-frontmatter-index-suite, skills-frontmatter-schema-files, flexible-frontmatter-toolchain, build-flexible-frontmatter-toolchain, migrate-repo-to-flexible-toolchain)
---

# Prompts Root

**What is this folder?** The single home for every executable instruction set in this repository. Prompts are the *what the agent is told to do*; Tasks coordinate, Research records what running them produced.

**Why is it here?** To enforce separation of concerns. Prompt drafting MUST NOT happen inside `/research/` (which is execution-only) and MUST NOT be inlined inside `/tasks/<NNN>-<slug>/task.md` (which only links via `task_uses_prompts`).

## Governing Specification

All work in this folder MUST conform to [`PROMPT.md`](../PROMPT.md). Frontmatter and cross-directory linkage rules live in [`TASK.md`](../TASK.md) §3 and [`FOLDERS.md`](../FOLDERS.md).

## What Belongs Here (per `PROMPT.md` §1)

1. Research proposals (`prompt_kind: research-proposal`).
2. Follow-up prompts surfaced from prior research runs (`prompt_kind: follow-up`).
3. Tool instructions (`prompt_kind: tool-instruction`).
4. Task-specs referenced by `/tasks/<NNN>-<slug>/task.md` (`prompt_kind: task-spec`).

## Contents

- [`research-prompt-from-annotations/`](./research-prompt-from-annotations/) — A prompt that scans an existing research folder for open questions and generates new research prompts from those findings.
- [`author-skills-root-spec/`](./author-skills-root-spec/) — Task-spec prompt that authors `SKILLS.md` at the repository root, plus the supporting edits to AGENTS.md / FOLDERS.md / templates. Drives Task 009.
- [`skills-frontmatter-index-suite/`](./skills-frontmatter-index-suite/) — Research-proposal + build prompt for the token-efficient frontmatter index, query CLI, and skills manifest emitter. Drives Task 010.
- [`skills-frontmatter-schema-files/`](./skills-frontmatter-schema-files/) — Task-spec prompt that authors JSON Schemas for L1/L2 frontmatter and the header ontology. Drives Task 011.
- [`flexible-frontmatter-toolchain/`](./flexible-frontmatter-toolchain/) — Research-proposal prompt that synthesises prior research + Anthropic's `skill-creator` into a flexible (required-only) maintenance contract plus a stateless toolchain spec. Drives `/research/flexible-frontmatter-toolchain/`.
- [`build-flexible-frontmatter-toolchain/`](./build-flexible-frontmatter-toolchain/) — Task-spec prompt for Task 016 (build the four-tool CLI surface + header-ontology JSON).
- [`migrate-repo-to-flexible-toolchain/`](./migrate-repo-to-flexible-toolchain/) — Task-spec prompt for Task 017 (three-batch migration; retires legacy linters; scope-narrows Task 010).
- [`governance-specs-update-research/`](./governance-specs-update-research/) — Research proposal to assess and create an update plan for governance specs after Task 001.

### Task 041 — Subtask Task-Specs (Tasks 032–039)

The 35 prompts below were extracted from the 35 subtask files under `tasks/03[2-9]*/subtasks/` per [Task 041](../tasks/041-extract-subtask-prompts/task.md) (PR #70 review C.3 audit-graph repair). Each prompt is `prompt_kind: task-spec`; each binds to its parent task via `prompt_relates_to_task`. They are listed grouped by parent task for navigability.

**Task 032 — `agents-spec-integration`:**

- [`research-adr-corpus-extraction/`](./research-adr-corpus-extraction/) — ST-1 research head: extract ≥15 implicit ADRs from the 8 root governance specs as the bootstrap ADR-0001..N corpus.
- [`tooling-narrative-ontology-load-discipline/`](./tooling-narrative-ontology-load-discipline/) — ST-2 tooling: ship the linter that closes AGENTS.md NO.5 (narrative-ontology load discipline).
- [`tooling-rfc2119-polarity-audit/`](./tooling-rfc2119-polarity-audit/) — ST-3 tooling: scan AGENTS.md for RFC-2119 polarity inversions per ASM-001.
- [`tooling-assumption-log-substance/`](./tooling-assumption-log-substance/) — ST-4 tooling: enforce assumption-log substance (§60-65 enforcement gap).
- [`spec-amendment-agents-md/`](./spec-amendment-agents-md/) — ST-5 Phase B: apply the AGENTS.md edits per Task 032 (a)-(f).

**Task 033 — `task-spec-integration`:**

- [`research-friction-pattern-synthesis/`](./research-friction-pattern-synthesis/) — ST-1 research: synthesise repo-wide friction-log patterns to ground TASK.md updates.
- [`research-spec-staleness-decision-formalization/`](./research-spec-staleness-decision-formalization/) — ST-2 research: formalise the §4.7 updated/abandoned decision boundary.
- [`tooling-duplicate-task-id-linter/`](./tooling-duplicate-task-id-linter/) — ST-3 tooling: mechanically detect duplicate `task_id` collisions at pre-commit time.
- [`tooling-lifecycle-classifier/`](./tooling-lifecycle-classifier/) — ST-4 tooling: deterministic helper for §4.7 updated-vs-abandoned classification.
- [`spec-amendment-task-md/`](./spec-amendment-task-md/) — ST-5 Phase B: apply the TASK.md edits per Task 033 (a)-(f).

**Task 034 — `prompt-spec-integration`:**

- [`research-prompt-engineering-principle-mechanizability/`](./research-prompt-engineering-principle-mechanizability/) — ST-1 research: assess which of the 7 engineering principles (P.5.1–P.5.7) are mechanically expressible.
- [`tooling-self-containedness-checker/`](./tooling-self-containedness-checker/) — ST-2 tooling: enforce prompt self-containedness per PROMPT.md §1.
- [`tooling-framework-declaration-validator/`](./tooling-framework-declaration-validator/) — ST-3 tooling: validate every prompt declares a recognised RISEN/RISE-DX/ReAct/RISEN+ReAct/CoT framework.
- [`spec-amendment-prompt-md/`](./spec-amendment-prompt-md/) — ST-4 Phase B: apply PROMPT.md edits per Task 034 (a)-(d).

**Task 035 — `research-spec-integration`:**

- [`research-session-continuity-protocol-instantiation/`](./research-session-continuity-protocol-instantiation/) — ST-1 research: instantiate the session-continuity protocol from `agentic-session-continuity-spec`.
- [`tooling-workspace-cleanliness-linter/`](./tooling-workspace-cleanliness-linter/) — ST-2 tooling: mechanically enforce R.4.4 (workspace cleanup at `research_phase: complete`).
- [`tooling-external-result-downstream-task-linter/`](./tooling-external-result-downstream-task-linter/) — ST-3 tooling: mechanically enforce R.6.5 (external-result downstream-task creation).
- [`tooling-trust-audit-gate/`](./tooling-trust-audit-gate/) — ST-4 tooling: per-workspace trust-audit GATE invoked at `research_phase: complete`.
- [`spec-amendment-research-md/`](./spec-amendment-research-md/) — ST-5 Phase B: apply RESEARCH.md edits per Task 035 (a)-(g).

**Task 036 — `folders-spec-integration`:**

- [`tooling-readme-frontmatter-validator/`](./tooling-readme-frontmatter-validator/) — ST-1 tooling: enforce F.5 readme.md L1 frontmatter (SHOULD → MUST).
- [`tooling-audit-graph-consistency-checker/`](./tooling-audit-graph-consistency-checker/) — ST-2 tooling: F.6 frontmatter↔body audit-graph consistency check.
- [`spec-amendment-folders-md/`](./spec-amendment-folders-md/) — ST-3 Phase B: apply FOLDERS.md edits per Task 036 (a)-(d).

**Task 037 — `pre-commit-spec-integration`:**

- [`research-pre-commit-readme-update-cadence/`](./research-pre-commit-readme-update-cadence/) — ST-1 research: canonical wording reconciling PRE_COMMIT.md §2 with FRUSTRATED.md §28.
- [`tooling-clean-working-directory-linter/`](./tooling-clean-working-directory-linter/) — ST-2 tooling: mechanise PC.1.1 clean-working-directory checks.
- [`tooling-per-rule-waiver-mechanism/`](./tooling-per-rule-waiver-mechanism/) — ST-3 tooling: refactor PC.7.B waivers from per-file to per-rule scope.
- [`spec-amendment-pre-commit-md/`](./spec-amendment-pre-commit-md/) — ST-4 Phase B (joint with Task 038 ST-3): apply PRE_COMMIT.md edits per Task 037 (a)-(e).

**Task 038 — `frustrated-spec-integration`:**

- [`research-fl0-value-justification/`](./research-fl0-value-justification/) — ST-1 research: justify the FL0-mandatory rule with research-backed evidence.
- [`tooling-fl-declaration-linter/`](./tooling-fl-declaration-linter/) — ST-2 tooling: gate the FL declaration at commit time.
- [`spec-amendment-frustrated-md/`](./spec-amendment-frustrated-md/) — ST-3 Phase B (joint with Task 037 ST-4): apply FRUSTRATED.md edits per Task 038.

**Task 039 — `maintenance-spec-integration`:**

- [`research-toolchain-flip-criteria/`](./research-toolchain-flip-criteria/) — ST-1 research: §1.1.2 toolchain-flip-criteria for the Legacy/Flexible/ADR three-way.
- [`research-staleness-decision-formalization/`](./research-staleness-decision-formalization/) — ST-2 research: §3.4 staleness algorithm.
- [`tooling-staleness-audit-script/`](./tooling-staleness-audit-script/) — ST-3 tooling: ship `tools/maintenance/staleness-audit.py`.
- [`tooling-dynamic-readme-partition-linter/`](./tooling-dynamic-readme-partition-linter/) — ST-4 tooling: lint dynamic-vs-static partitions in repo readmes.
- [`tooling-trust-audit-integration/`](./tooling-trust-audit-integration/) — ST-5 tooling: cross-workspace trust-audit aggregator (vs Task 035 ST-4's per-workspace gate).
- [`spec-amendment-maintenance-md/`](./spec-amendment-maintenance-md/) — ST-6 Phase B: apply MAINTENANCE.md edits per Task 039.

## Workflow Assumptions

- Each subfolder corresponds to exactly one Prompt Task, identified by a kebab-case slug.
- The slug is derived from the prompt's core intent, not from a date or ticket number.
- `brief.md` is immutable once written; it records what was originally requested.
- `prompt.md` carries L1 + `prompt_*` frontmatter and MUST be executable in isolation.
- This folder was renamed from `/prompt/` (singular) to `/prompts/` (plural) on 2026-05-04 as part of the orchestration refactor that introduced `/tasks/`.
