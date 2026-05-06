---
type: note
status: active
slug: improve-maintenance-spec-2026-05-06-notes
summary: "PR #66 review notes: spec conformance audit of the Task 032 filing commit (8cc2fd2). Five findings, two critical."
created: 2026-05-06
updated: 2026-05-06
---

# Task 032 — Running Notes

## PR #66 Spec-Conformance Audit (2026-05-06)

Reviewer: Claude Code (session `claude/stoic-mendel-9NrgD`)
Commit under review: `8cc2fd235128d742365a34e0d9d1568f351981eb`
PR: [#66 — feat(task-032): file maintenance-spec improvement Task from 2026-05-06 session](https://github.com/netzkontrast/agency/pull/66)

---

### Summary

The commit is well-intentioned and structurally sound in the majority of its surface. The six findings (F8–F13) are concrete, rooted in observed symptoms, and each carries actionable diff options. The plan maps 1:1 to findings with no ambiguity in steps 1, 2, 4, 5, 6, or 7. The `task.md` frontmatter is complete at L1 and L2 layers; the `readme.md` satisfies the TASK.md §7.7 stub requirement; and `tasks/readme.md` was updated atomically in the same commit per TASK.md §4.8.

Five conformance issues were identified, ranked below by severity.

---

### Finding A — CRITICAL: `slug` Exceeds the Max-5-Token Constraint (TASK.md §2)

**Clause:** TASK.md §2 — "The folder name MUST be `<NNN>-<slug>` where … `<slug>` is kebab-case (max 5 tokens)."

**Observed:** `slug: improve-maintenance-spec-2026-05-06`

Token count (splitting on hyphens): `improve` · `maintenance` · `spec` · `2026` · `05` · `06` = **6 tokens**.

The date component alone adds three tokens. For comparison, Task 014 — the predecessor — uses `improve-maintenance-spec-from-session` (5 tokens, exactly at the limit).

**Impact:** The `tools/fm/validate.py` slug-format check (`F.3.3`) enforces kebab-case but does not yet enforce token count (that would be a new `F.3.5` check). The violation is silent today but sets a precedent that erodes the max-5-token rule systematically. Each coherence-run-dated task slug will violate it.

**Recommended fix:** Shorten to `improve-maintenance-spec-may-2026` (5 tokens) or `maintenance-spec-repair-2` (4 tokens, distinguishing from Task 014's `-1` or `-from-session` variants). If date disambiguation is operationally important, the convention SHOULD be encoded as a repo-level exception in TASK.md §2 with a rationale comment — not silently committed.

---

### Finding B — CRITICAL: `tasks/readme.md` Entry Missing from `task_affects_paths`

**Clause:** TASK.md §4.8 — "Every change that affects the membership or `task_status` of any Task MUST be accompanied **in the same commit** by an update to `tasks/readme.md`." TASK.md §3.3 — `task_affects_paths`: "Relative paths the Task is allowed to modify."

**Observed:** The commit updates `tasks/readme.md` (as required by §4.8), yet `task_affects_paths` in `task.md` does not include `tasks/readme.md`:

```yaml
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - install.sh
  - TASK.md
  - tools/check-governance.sh
  - tools/dramatica-nav/validate.py
```

`tasks/readme.md` is absent.

**Impact:** `task_affects_paths` serves as the access-control declaration for the Task — it lists what the agent is permitted to modify. Any agent picking up Task 032 from a cold-start reads this list and may infer they MUST NOT touch `tasks/readme.md`. This is wrong; the §4.8 index-update obligation applies to every Task transition, so `tasks/readme.md` should always appear here when a task folder is created.

**Recommended fix:** Add `tasks/readme.md` to `task_affects_paths`.

---

### Finding C — MODERATE: `task_uses_prompts` Semantic Mismatch

**Clause:** TASK.md §3.3 — `task_uses_prompts`: "Slugs of prompts this Task *executes*."

**Observed:** `task_uses_prompts: [repo-coherence-check]`

Task 032's goal is to **improve** `prompts/repo-coherence-check/prompt.md` and related governance files — not to *execute* the coherence check. The `task_uses_prompts` field documents the instruction sets an agent will run as part of the Task's execution; it is not a "discovered-by" or "relates-to" pointer.

The correct field for "this task was found by coherence run" is the `## Links` prose section, which the commit uses correctly (`Found by: coherence-check run 2026-05-06`). Task 025, the sibling, has the same `task_uses_prompts: [repo-coherence-check]` pattern, suggesting this is a recurring convention error rather than a one-off.

**Impact:** `lint-linkage.py` §7.3 will verify the slug resolves to a file (it does), but the semantic intent is misleading. An agent picking up Task 032 might interpret `task_uses_prompts` as an instruction to run the coherence check before starting — which is actually correct per AGENTS.md §SS but is not what the field is meant to record. The conflation is low-harm today but will confuse automated tooling once Task 031's `tasks-index-diff` check starts consuming this field.

**Recommended fix:** Either (a) clear `task_uses_prompts: []` and keep the `## Links` prose, or (b) add a `task_references_prompts` L2 field for "prompt modified but not executed" relationships. The latter is a T3 finding itself (schema extension), so option (a) is preferred for this commit.

---

### Finding D — MODERATE: F10 Coordination is Under-Specified

**Clause:** TASK.md §5 — "Every `task.md` MUST contain … `## Plan` — Numbered steps. Each step SHOULD reference the artifact it produces."

**Observed:** Plan step 3 reads: "Land F10 in coordination with Task 025, OR record `delegated to Task 025` disposition."

This is a binary decision left to the executing agent. Per the spec's own anti-pattern catalogue (PROMPT.md §5.5 "Anti-Ambiguity"), ambiguity that has two valid readings MUST be resolved inline. Here the ambiguity is:

- Does the agent implement F10 or defer? There is no criterion to decide.
- If deferring, does the agent update Task 025's `task.md` to formally absorb F10? Or just log in `friction-log.md`?

Additionally, Task 025 still has `task_blocked_by: ["019"]` in its frontmatter even though Task 019 is `done`. Task 032's F10 text correctly notes this ("Task 025 is unblockable") but doesn't account for the fact that Task 025's stale `task_blocked_by` entry might cause a future linter ERROR — this is exactly the stale-status-drift Problem that Task 031 is meant to solve.

**Recommended fix:** Resolve the F10 ownership question now (not in the executing agent's discretion). Recommended: "Record `delegated to Task 025`; in the same commit, remove `task_blocked_by: ["019"]` from Task 025's frontmatter and update `tasks/readme.md` to reflect Task 025 is no longer blocked." This turns a soft coordination into a concrete, auditable diff.

---

### Finding E — MINOR: `readme.md` `summary` Describes Task 032 as "Successor to Task 025"

**Clause:** TASK.md §4 — "A Task is set to `task_status: updated` when … A successor Task has been created." The `task.md` correctly uses "Companion (NOT successor)" and the `task_supersedes: []` field is empty.

**Observed:** `tasks/032-improve-maintenance-spec-2026-05-06/readme.md` frontmatter:

```yaml
summary: "Index for Task 032: Successor to Task 025. …"
```

The word "Successor" in the `readme.md` summary contradicts the explicit "Companion (NOT successor)" declaration in `task.md` and the empty `task_supersedes` field. The distinction is load-bearing: the `updated` lifecycle in TASK.md §4.7 requires explicit `task_supersedes`/`task_superseded_by` reciprocity — calling this a successor without the reciprocal frontmatter entry creates an audit-graph inconsistency visible to any agent that reads the `readme.md` summary before the `task.md` body (per AGENTS.md AG.1.1 "Agent MUST read summary field first").

**Recommended fix:** Change `readme.md` summary to "Index for Task 032: Companion (not successor) to Task 025. …"

---

### Overall Verdict

The commit is **approvable with minor fixes**. Findings A and B SHOULD be addressed before the task is executed against (an agent cold-starting from `task_affects_paths` will be misinformed, and the slug violation silently erodes a spec constraint). Findings C–E are low-risk today but accumulate technical debt.

The quality of the findings themselves (F8–F13) is high: each identifies a concrete symptom, a root cause, and a discrete set of diff options. The "companion vs successor" distinction is correctly observed in the `task.md` body even if contradicted in the `readme.md` summary. The Plan-to-Todo 1:1 mapping is exemplary.
