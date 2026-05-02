# Folder Interaction Specification

To ensure navigation and traceability across the repository, agents MUST abide by the following directory management rules.

## Basic Hierarchy
All operational work must be siloed by task type and a unique task slug. The top-level directory structure follows:
`/<tasktype>/<task-slugname>/`

For example:
- `/research/ncp-novel-co-authoring-spec/`
- `/feature/auth-provider-v2/`

## Mandatory `readme.md` Rule
- **Rule:** EVERY folder in the repository MUST contain a `readme.md` file.
- **Update Trigger:** Whenever a file or subfolder is added, modified, or deleted within a folder, the agent MUST immediately update that folder's `readme.md` to reflect the current state of its contents.
- **Content:** The `readme.md` must contain a brief summary of the folder's purpose and a bulleted catalog of its current contents.

## Subfolder Creation Heuristics
To prevent structural bloat and extreme "agent agony" from managing deeply nested index files:
1. **Prefer Flat Structures:** Do not create a subfolder unless there are 4 or more distinct files of the exact same category.
2. **Consolidation First:** If you have `aspect-1.md` and `aspect-2.md`, keep them in the parent folder. Only if you generate `aspect-5.md` should you refactor them into an `/aspects/` subfolder.
