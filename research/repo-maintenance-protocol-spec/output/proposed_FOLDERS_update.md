# Proposed Update to FOLDERS.md

The following section should be appended or used to update `FOLDERS.md` to support the new Dynamic Readme schema and `/todo/` pipeline.

```markdown
<<<<<<< SEARCH
## Mandatory `readme.md` Rule (Decentralized Documentation)
- **Rule:** EVERY folder in the repository MUST contain a `readme.md` file.
- **Purpose (Human-Centric):** These readmes serve as human-readable, decentralized user documentation. Keeping documentation adjacent to the operational files prevents "doc drift," ensures the user can trust the repository state, and prevents agents from having to fix decoupled `/docs` folders blindly.
- **Update Trigger (Pre-Commit Batching):** To avoid administrative bloat and save agent context tokens, agents DO NOT need to update the `readme.md` on every single file change. Instead, updating the `readme.md` files for all touched directories is a **mandatory pre-commit step**.
- **Content Requirements:**
  1. **What and Why:** Explain exactly *what* the file/folder is and *why* it exists in this specific location.
  2. **Linked Navigation:** Every file or subfolder listed MUST use a relative Markdown link (e.g., `[output/](./output)` or `[SPEC.md](./SPEC.md)`).
  3. **Assumptions Log:** If the agent made any implicit assumptions about how a folder should be used that are not explicitly codified here, document them in the `readme.md` to prevent future workflow drift.
=======
## Mandatory `readme.md` Rule (Dynamic Documentation State)
- **Rule:** EVERY folder in the repository MUST contain a `readme.md` file partitioned into a Static Section and a Dynamic Section.
- **Purpose (Agentic Context & Human Trust):** These readmes serve as executable state machines for agents to establish local context, while providing decentralized documentation for humans.
- **Update Trigger (Pre-Commit Batching):** Updating the `readme.md` files for all touched directories is a **mandatory pre-commit step**. Agents MUST update the dynamic sections to reflect their recent actions.
- **Content Requirements:**
  - **Static Section (Preserve):**
    1. **Purpose:** Explain exactly *what* the file/folder is and *why* it exists.
    2. **Linked Navigation:** Relative Markdown links to all files/subfolders.
  - **Dynamic Section (Update):**
    3. **Current State:** Active status of the folder (e.g., "Active Task", "Completed").
    4. **Latest Synthesized Learnings:** Key insights pulled from child synthesis logs.
    5. **Open Blockers:** Current friction or required tasks.
    6. **Assumptions Log:** Implicit assumptions the agent made about folder usage.
>>>>>>> REPLACE

<<<<<<< SEARCH
## Subfolder Creation Heuristics
=======
## The /todo/ Pipeline Delegation
- **Rule:** Complex issues, unresolved contradictions, and high-friction (`FL1-FL3`) observations MUST NOT cause active tasks to derail.
- **Process:** These issues MUST be extracted by maintenance agents (or the active agent, if capable) and synthesized into a self-contained `prompt.md` placed in a unique `/todo/<issue-slug>/` directory.

## Subfolder Creation Heuristics
>>>>>>> REPLACE
```
