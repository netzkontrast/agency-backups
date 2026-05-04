# Repository Maintenance Protocol

Welcome, maintenance agent. This document governs the automated "Nightly Maintenance Run" designed to manage technical debt, update dynamic documentation, and delegate future tasks.

**If you are an agent executing a scheduled maintenance run, you MUST strictly adhere to the operational rules below.**

## 1. Scope of the Maintenance Agent
- **DO:** Update the dynamic sections of `readme.md` files (State, Learnings, Blockers) across the repository.
- **DO:** Aggregate unstructured insights (like `friction-log.md` files) into formal delegation tasks in the `/todo/` pipeline.
- **DON'T:** Modify root governance specifications directly (`AGENTS.md`, `FOLDERS.md`, `RESEARCH.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`). If you discover a required change for these files, you MUST write a proposal prompt to the `/todo/` pipeline.
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

## 3. The Task Delegation Pipeline (`/todo/`)
The repository self-improves by converting friction into isolated tasks.

### 3.1 Extracting Friction
- Scan all `/reflection/friction-log.md` files across the repository.
- Identify issues marked `FL1`, `FL2`, or `FL3`, as well as any unresolved contradictions logged during research tasks.

### 3.2 Packaging Prompts
- You MUST NOT fix the complex issues directly.
- Instead, you MUST synthesize the context and the problem into a self-contained `prompt.md` file.
- Place this generated prompt into a dedicated subfolder within the root `/todo/` directory (e.g., `/todo/fix-api-rate-limits/prompt.md`).
- The `prompt.md` MUST contain clear instructions for a future agent to execute.

## 4. Finalizing the Run
Before completing your maintenance session, verify that:
- All touched `readme.md` files comply with the static/dynamic partitioning schema.
- All extracted friction logs have corresponding `prompt.md` files in the `/todo/` directory.
- No Root Specs were directly edited.
