---
type: prompt
status: active
slug: maintenance-todo-audit
summary: "Audit and ratify the /todo/ → /prompts/ correction in MAINTENANCE.md; scan for remaining /todo/ references."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
prompt_spawned_from_research: superclaude-integration-spec
---

# Maintenance /todo/ Audit Prompt

**Framework: RISEN**

## Role

You are an Agency governance auditor responsible for ensuring structural consistency between root specification files.

## Instructions

1. **Verify** that `MAINTENANCE.md §3` now correctly references `/prompts/` as the delegation target (not `/todo/`). If it still references `/todo/`, update it to use `/prompts/` per `FOLDERS.md §7`.

2. **Scan** the entire repository for any remaining references to `/todo/` path patterns: search all `.md` files for the string `/todo/` and identify which files contain such references.

3. **Amend** any found references in non-root-spec files directly. For root governance spec amendments, file a proposal prompt per `MAINTENANCE.md §1`.

4. **Document** all findings and changes in a commit message following Agency git conventions.

## Situation

During research run `superclaude-integration-spec` (2026-05-04), a contradiction was found: `MAINTENANCE.md §3` references `/todo/` while `FOLDERS.md §7` prohibits it. The research run updated `MAINTENANCE.md §3` to reference `/prompts/`, but no full audit was conducted.

## Expected Deliverable

- A commit confirming all `/todo/` references are resolved OR a set of proposal prompts in `/prompts/` for references requiring root-spec amendment.

## Exclusions

- MUST NOT create a `/todo/` directory.
- MUST NOT modify `AGENTS.md`, `FOLDERS.md`, `RESEARCH.md`, `PRE_COMMIT.md` directly; file proposals instead.

## Normative Language

Requirements use RFC 2119 keywords: MUST, SHOULD, MAY.
