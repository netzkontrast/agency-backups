---
type: research
status: completed
slug: governance-specs-update-research
summary: "Detailed update plan for governance specifications based on tooling state after Task 001."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: governance-specs-update-research
research_friction_level: FL0
---

# Governance Specs Update Plan

## 1. Overview
The implementation of Task 001 introduced linters (`check-governance.sh`, `lint-structure.py`, `lint-linkage.py`, `validate-frontmatter.py`) and pre-commit hooks that strictly enforce governance rules. Subsequent runs in `MAINTENANCE.md` and friction logs revealed areas where the written specifications (`MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, `TASK.md`) are either ambiguous, misaligned with the linters, or lacking explicit documentation of newly introduced mechanisms (e.g. flexible toolchain vs legacy).

This document outlines the required updates to bring the specifications in line with the enforced reality.

## 2. Updates to `MAINTENANCE.md`
- **Toolchain Migration Context:** `MAINTENANCE.md` MUST explicitly document the parallel existence of the legacy toolchain and the new flexible toolchain (`FM_TOOLCHAIN=1`) introduced in Task 016, and clarify how maintenance bypass interactions work under the new regime.
- **Duplicate Task ID Governance:** The maintenance run-log revealed collisions (006, 009). The spec MUST clarify that resolving duplicate `task_id` collisions is a T3 (or explicit manual) task and should detail the renumbering procedure more rigorously than the current brief mention.
- **Staleness/Drift Checks:** Update the drift-check algorithm documentation to differentiate between spec-bearing and review-bearing research, to prevent false positives when checking `task_status`.

## 3. Updates to `PRE_COMMIT.md`
- **Linter Documentation:** Update Section 7 ("Mechanical Governance Checks") to clarify the transition plan from legacy tools (`tools/validate-frontmatter.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`) to the new `FM_TOOLCHAIN=1` based system (Task 016). Make it clear when to use which.
- **Waivers:** Explicitly document the `tools/.frontmatter-waivers` burn protocol and state that *new* research files MUST NOT be added to the waivers list, addressing the FL1 feedback from Task 001.

## 4. Updates to `FOLDERS.md`
- **Subfolder Heuristics:** Ensure the rules surrounding the creation of `brief.md` and `readme.md` alongside `prompt.md` in the `/prompts/` directory are explicitly stated as mandatory scaffold requirements, rather than relying solely on templates, to prevent omissions noted in Task 001's friction log.

## 5. Updates to `TASK.md`
- **Linkage Rules (Section 7):** Clarify that the `task_spawns_research` resolution check is enforced by `lint-linkage.py` **only** upon task closure (`done` or `abandoned`), not while the task is `open` or `in_progress`. This addresses the aggressive linting false positive logged in Task 001.
- **Duplicate IDs (Section 8.1):** State explicitly that while duplicate `task_id` prevention is a spec-bearing rule, it is not currently linter-enforced, putting the onus on the agent to run `ls tasks/ | sort` before creating a new task folder.
