# Repository Maintenance Protocol

Welcome, maintenance agent. This document governs the automated "Nightly Maintenance Run" designed to manage technical debt, update dynamic documentation, and delegate future tasks.

**If you are an agent executing a scheduled maintenance run, you MUST strictly adhere to the operational rules below.**

> **SC Tooling:** Maintenance agents SHOULD use `/sc:index-repo` and `/sc:analyze` at the start of each run, and MUST execute the SuperClaude Integration Scan defined in §5. See [SuperClaude Integration Spec §3.7](./research/superclaude-integration-spec/output/SPEC.md).

## 1. Scope of the Maintenance Agent
- **DO:** Update the dynamic sections of `readme.md` files (State, Learnings, Blockers) across the repository.
- **DO:** Aggregate unstructured insights (like `friction-log.md` files) into formal delegation prompts in the `/prompts/` directory.
- **DON'T:** Modify root governance specifications directly (`AGENTS.md`, `FOLDERS.md`, `RESEARCH.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`). If you discover a required change for these files, you MUST write a proposal prompt to the `/prompts/` directory per `PROMPT.md`.
- **DON'T:** Attempt to execute complex research or code refactors yourself during the maintenance loop.

## 2. Dynamic Readme Updates
You MUST ensure that `readme.md` files act as executable state machines, not just static indices. When updating a directory's `readme.md`, enforce the following partition:

### 2.1 Static Section (Preserve)
- **Purpose:** What this folder is and why it exists.
- **Linked Navigation:** Clickable relative links to all files and subfolders.
- *Rule:* Do not modify this section unless files have been moved, renamed, or deleted.

### 2.2 Dynamic Section (Update)
- **Current State:** The operational status of the folder (e.g., "Active Task", "Completed Research").
- **Latest Synthesized Learnings:** Bullet points extracting the core findings from nested `/synthesis` or `/reflection` folders.
- **Open Blockers:** Any outstanding issues preventing further progress in this directory.
- *Rule:* You MUST actively rewrite this section to reflect the most current logs and task statuses.

## 3. The Task Delegation Pipeline (`/prompts/`)
The repository self-improves by converting friction into isolated tasks.

### 3.1 Extracting Friction
- Scan all `/reflection/friction-log.md` files across the repository.
- Identify issues marked `FL1`, `FL2`, or `FL3`, as well as any unresolved contradictions logged during research tasks.

### 3.2 Packaging Prompts
- You MUST NOT fix the complex issues directly.
- Instead, you MUST synthesize the context and the problem into a self-contained `prompt.md` file per `PROMPT.md`.
- Place this generated prompt into a dedicated subfolder within `/prompts/` (e.g., `/prompts/fix-api-rate-limits/prompt.md`).
- The `prompt.md` MUST contain clear instructions for a future agent to execute.

## 4. Finalizing the Run
Before completing your maintenance session, verify that:
- All touched `readme.md` files comply with the static/dynamic partitioning schema.
- All extracted friction logs have corresponding `prompt.md` files in `/prompts/`.
- No Root Specs were directly edited.
- The SuperClaude Integration Scan (§5) has been completed and all gaps have been filed.

## 5. SuperClaude Integration Scan

> **Governed by:** [SuperClaude Integration Spec](./research/superclaude-integration-spec/output/SPEC.md)

This section governs a recurring check during every Maintenance Run. Its purpose is to detect new Agency artifacts (research runs, tasks, prompts, root spec amendments) that would benefit from SuperClaude integration, and to file delegation prompts when such opportunities are found.

### 5.1 Required SC Tooling at Run Start

At the beginning of every Maintenance Run, the maintenance agent MUST execute:

```
/sc:index-repo
```

This produces a token-efficient repository index (94% token reduction). The agent SHOULD use this index as its primary navigation map for the remainder of the run, rather than traversing the directory tree manually.

### 5.2 Drift Detection

The maintenance agent MUST scan the following for SuperClaude integration gaps:

1. **New research runs** (`/research/*/output/SPEC.md`): Check if `SPEC.md` contains a `## SC Integration` block per [Integration Spec §4](./research/superclaude-integration-spec/output/SPEC.md). If missing, log as FL1 and file a delegation prompt.

2. **New tasks** (`/tasks/*/task.md`): Check if the task plan references appropriate `/sc:*` commands for its domain. If a task spanning 3+ domains has no `/sc:spawn` reference in its Plan, log as FL1 and file a prompt.

3. **New prompts** (`/prompts/*/prompt.md`): Check if research-proposal prompts include `/sc:research` in their execution instructions. If missing and the prompt governs multi-hop research, log as FL1.

4. **Root spec amendments**: Check if any root spec modified since the last maintenance run is missing the SC Integration cross-link recommended in [Integration Spec §5](./research/superclaude-integration-spec/output/SPEC.md). If missing, log as FL1.

### 5.3 Structural Drift Analysis

After indexing, the maintenance agent SHOULD run:

```
/sc:analyze --focus architecture
```

This detects structural drift in repository topology (FOLDERS.md compliance, orphaned research runs, missing `readme.md` files). The analysis output SHOULD inform which `readme.md` files need updates per §2.

### 5.4 Packaging Integration Gaps

For each integration gap identified in §5.2, the maintenance agent MUST:

1. Create a new prompt under `/prompts/<gap-slug>/` following `PROMPT.md`.
2. Set `prompt_kind: follow-up` and `prompt_spawned_from_research: superclaude-integration-spec`.
3. Include in the prompt body: the specific artifact path, the missing integration element, and a reference to [Integration Spec §4](./research/superclaude-integration-spec/output/SPEC.md).

### 5.5 SuperClaude Framework Version Check

The maintenance agent SHOULD check if a newer version of the SuperClaude Framework has been installed since the last run:

```bash
superclaude --version
```

If the version has changed, the agent MUST file a new research prompt under `/prompts/superclaude-update-<version>/` to re-execute the integration scan with the updated framework capabilities.

### 5.6 SC Scan Completion Checklist

The SC Integration Scan is complete when:
- `/sc:index-repo` has been run and its index reviewed.
- All new research/task/prompt artifacts have been checked for SC Integration blocks.
- All identified gaps have corresponding delegation prompts in `/prompts/`.
- The SuperClaude Framework version has been checked.
- Any version change has a corresponding re-scan prompt filed.
