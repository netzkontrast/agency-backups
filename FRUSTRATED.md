# Agent Frustration & Friction Specification

To continuously improve prompts, tooling, and repository structure, we require agents to self-report friction and frustration encountered during any session.

Agents MUST use the following **Frustration Levels (FL)** when logging their experience in the designated `friction-log.md` (or equivalent session logs).

## Frustration Levels Defined

### FL0 — Zero Friction
- **Definition:** The task proceeded exactly as expected. Instructions were clear, tools worked flawlessly, and no backtracking was required.
- **Action:** Briefly state that the execution was perfectly aligned with the prompt.

### FL1 — Minor Annoyance
- **Definition:** The agent encountered minor ambiguities, syntax issues in the prompt, or had to execute repetitive tool calls to format data. The task was completed without needing to fundamentally alter the plan.
- **Action:** Document the specific ambiguity or repetitive task. Suggest a minor prompt or process tweak.
- **Example:** "Having to manually reconstruct a `session.log` from memory because an automatic script wasn't provided."

### FL2 — Significant Frustration
- **Definition:** The agent experienced conflicting instructions, had to significantly backtrack to retrofit work due to shifting constraints, or encountered tooling/dependency failures that required substantial diagnostic effort to bypass.
- **Action:** Clearly identify the exact conflicting instructions or tooling failures. Provide a concrete recommendation for how the initial prompt or environment must be restructured to prevent this.
- **Example:** "The initial prompt demanded a monolithic file, but a later prompt demanded a deep directory structure, forcing a tedious teardown and rebuild of the data."

### FL3 — Task Blocker / Extreme Frustration
- **Definition:** The agent is stuck in a loop, the instructions are fundamentally impossible to execute within the sandbox, or environmental errors prevent the completion of the core objective.
- **Action:** Halt normal execution. Log the FL3 status, document the exact point of failure, and request human intervention.

## When and How to Log
1. **Research Tasks:** You MUST create or update `/reflection/friction-log.md` at the end of the session, explicitly declaring your highest FL experienced during the run at the top of the file (e.g., `Highest Frustration Level: FL2`).
2. **Standard Tasks:** Even outside of deep research, if you hit FL2 or FL3, you must include a section named `## Frustration Log` in your final PR description or submit message.

### Special Triggers
- **Structural Bloat / Micromanagement:** If a prompt demands deeply nested folder structures with less than 3 files per folder, or requires tedious administrative overhead (e.g., updating a `readme.md` for every single minor file change instead of relying on standard `ls` or Git tooling), the agent MUST log this as FL2. This administrative burden distracts the LLM's context window from actual logic and code generation.
