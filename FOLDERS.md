# Folder Interaction Specification

To ensure navigation and traceability across the repository, agents MUST abide by the following directory management rules.

## Basic Hierarchy
All operational work must be siloed by task type and a unique task slug. The top-level directory structure follows:
`/<tasktype>/<task-slugname>/`

## Mandatory `readme.md` Rule (Decentralized Documentation)
- **Rule:** EVERY folder in the repository MUST contain a `readme.md` file.
- **Purpose (Human-Centric):** These readmes serve as human-readable, decentralized user documentation. Keeping documentation adjacent to the operational files prevents "doc drift," ensures the user can trust the repository state, and prevents agents from having to fix decoupled `/docs` folders blindly.
- **Update Trigger (Pre-Commit Batching):** To avoid administrative bloat and save agent context tokens, agents DO NOT need to update the `readme.md` on every single file change. Instead, updating the `readme.md` files for all touched directories is a **mandatory pre-commit step**.
- **Content Requirements:**
  1. **What and Why:** Explain exactly *what* the file/folder is and *why* it exists in this specific location.
  2. **Linked Navigation:** Every file or subfolder listed MUST use a relative Markdown link (e.g., `[output/](./output)` or `[SPEC.md](./SPEC.md)`).
  3. **Assumptions Log:** If the agent made any implicit assumptions about how a folder should be used that are not explicitly codified here, document them in the `readme.md` to prevent future workflow drift.

## Subfolder Creation Heuristics
1. **Prefer Flat Structures:** Do not create a subfolder unless there are 4 or more distinct files of the exact same category.
2. **Consolidation First:** Consolidate files in the parent folder before reaching for sub-directories, ensuring that folder traversal remains efficient.
