# Friction Log — Task 001 (refactor-governance-from-specs)

**Highest Frustration Level: FL1**

**Date:** 2026-05-04
**Agent:** claude-code

---

## FL1 — Minor Annoyances Encountered

### 1. Waiver List Required Mid-Stream Backfilling

The `.frontmatter-waivers` file listed 11 pre-existing research files grandfathered before the governance architecture existed. Retrofitting frontmatter on 14 files (11 waived + 3 newly failing) required a parallel sub-task to read each file, derive a summary, and prepend frontmatter. This was mechanical but time-consuming.

**Recommendation:** Future research runs MUST add frontmatter at creation time, not after the fact. The `templates/research-readme.md` template enforces this for new runs.

### 2. task_spawns_research Check Was Too Aggressive

The initial `lint-linkage.py` errored on `tasks/002-token-efficiency-tool-suite/task.md` because `task_spawns_research` listed a future research folder that doesn't exist yet (the task is still `open`). Per `TASK.md §7`, the linkage check applies only when *closing* a task, not for open/in-progress ones.

**Resolution:** Updated `lint-linkage.py` to only check `task_spawns_research` resolution when `task_status` is `done` or `abandoned`.

**Recommendation:** The spec wording in TASK.md §7 should be clarified to explicitly state "applicable only on closure" to prevent future agent confusion.

### 3. prompts/ Folder Missing Structural Files

`prompts/github-skillmd-novel-authoring-de-en/` was missing `brief.md` and `readme.md` — it was created as a stub without these files. The structure linter caught this immediately.

**Resolution:** Created both files.

**Recommendation:** The `templates/prompt.md` exists but there is no automation to scaffold the full folder (brief.md + readme.md + prompt.md) from a template. A `tools/scaffold-prompt.sh` would prevent these omissions.

---

## What Went Well (FL0 Components)

- The `validate-frontmatter.py` script pre-existed and was complete — no changes needed.
- The templates (`task.md`, `prompt.md`, `research-readme.md`) pre-existed — only `notes.md` needed to be added.
- The three research specs (A/B/C, G/H/I, J/K/L) were well-structured and the mechanically-checkable clauses were easy to identify.
- All four linters (validate-frontmatter, lint-structure, lint-linkage, check-trust) pass cleanly on the current repo state.

---

## Governance Note (FL1 → routed to prompt improvement, not governance block update)

The FL1 issues above are prompt-level improvements (clearer waiver burn protocol, spec wording clarification). No FL2+ governance block update is required.

## Supersession Rationale

The original goal of encoding theoretical rules from Spec-A/B/C, G/H/I, and J/K/L into enforced repository linters was achieved. However, the subsequent coherence runs and new tooling updates (like the flexible frontmatter toolchain in Task 016) mean the documentation in `MAINTENANCE.md`, `PRE_COMMIT.md`, `FOLDERS.md`, and `TASK.md` needs to be brought into sync with these new systems. The remaining documentation syncing effort has been superseded by Task 026 (`026-update-governance-specs-from-research`), shifting the status to `updated`.
