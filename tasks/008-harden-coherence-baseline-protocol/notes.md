---
type: note
status: active
slug: harden-coherence-baseline-protocol
summary: "Post-merge review of PR #26 (claude/funny-curie-zVZBH → main) by claude-code session claude/stoic-mendel-4pxCa. Documents conformance findings, constraint collisions, and recommendations for the agent picking up Task 008."
created: 2026-05-04
updated: 2026-05-04
---

# Review Notes — PR #26 (task(008): harden coherence-check baseline protocol)

**Reviewer:** `claude-code` session `claude/stoic-mendel-4pxCa`
**Date:** 2026-05-04
**Branch reviewed:** `claude/funny-curie-zVZBH` → `main` (merged)
**Commits:** `2ac93bd` (chore(coherence)) + `6f41a1b` (task(008))
**Governing prompt:** `prompts/repo-coherence-check/prompt.md`
**Governing spec:** `TASK.md`, `MAINTENANCE.md`, `PROMPT.md`, `FOLDERS.md`

---

## 1. Summary Verdict

The PR delivers correct T1/T2 repairs and two well-structured T3 Tasks. The Background section of Task 008 is a high-quality root-cause analysis. However, the PR carries **four conformance issues** that the agent executing Task 008 MUST be aware of, and **one hard constraint collision** that is worth feeding back into the prompt itself.

---

## 2. Positive Findings

### 2.1 T1 Fixes Are Precise and Correct

Both `prompt_relates_to_task` slug corrections (`002-token-efficiency-tool-suite` → `token-efficiency-tool-suite`) are exactly the kind of mechanical, unambiguous repair T1 permits. The awk-like distinction between folder-name format and slug format was correctly identified and fixed.

### 2.2 TASK.md §8.1 Compliance on Duplicate Task ID

Renaming `tasks/003-surface-skills-architecture/` → `tasks/006-surface-skills-architecture/` and updating only `task_id` (not the slug) is textbook-correct per TASK.md §8.1. The slug stability is exactly what the spec requires.

### 2.3 Task 007 — Reconciliation Strategy Design

Task 007's Background section correctly decomposes the 13 lint errors and 2 trust errors into four independent root-cause categories (friction-logs, `task_spawns_research` semantic confusion, reciprocity gaps, provider-namespaced paths). The four-option reconciliation menu (A/B/C/D) gives the next agent clear decision branches without prescribing a single path — appropriate for a task with schema implications.

### 2.4 Task 008 Background — Six Failure Modes

The six failure modes in Task 008's Background are diagnostically precise:

1. Squash-merge erases the recorded hash — factually accurate (hash `4c5e7e4` is unreachable from any ref post-merge).
2. Malformed `end_commit` field silently yields the wrong baseline — the two-hash issue in the bootstrap record is real and directly observable in `maintenance/run-log.md` line 32.
3. Pre-commit hook not installed by default — confirmed by the fact that `check-governance.sh` exits non-zero after the PR landed.
4. Self-injected duplicate `task_id` — diagnosed correctly; the maintenance prompt's T3 Task creation step does not include a pre-creation `ls tasks/ | sort` check.
5. L2 schema gap for spawned prompts — the `task_spawns_prompts` gap is a real schema deficiency causing Task 003's misuse of `task_spawns_research`.
6. Provider-namespaced research paths invisible to the linter — confirmed; `research/gemini/github-skillmd-novel-authoring-de-en/` is invisible to `tools/lint-linkage.py`.

### 2.5 Run-Log Transparency

The run-log entry is unusually candid: it names the exact failure mode (squash-merge hash loss), documents the malformed bootstrap record, and records the linter-driven strategy rather than trying to paper over the 7-day fallback.

---

## 3. Critical Findings

### 3.1 `check-governance.sh` Still Exits Non-Zero After Merge

**Severity:** High — this directly contradicts the Expectations table in `prompts/repo-coherence-check/prompt.md § E`:

> No regressions — The repo MUST pass any existing lint or pre-commit checks after the repair commit.

After PR #26 was merged into `main`, running `tools/check-governance.sh` produces:

```
lint-linkage: 13 error(s).
check-trust: 2 error(s).
=== FAIL: one or more checks failed. ===
```

The PR description claims to "reconcile coherence-check findings" and "fix linkage," but the 13 errors and 2 trust errors listed in Task 007 were **deferred, not fixed**. The "no regressions" clause in the prompt's Expectations table was not satisfied.

**Mitigation acknowledged by this PR:** The errors predate this PR (they existed on `main` before the run). The agent correctly created Task 007 for them. However, the PR description's phrasing ("fix linkage") is misleading — the errors were *documented*, not fixed.

**Recommendation for the agent picking up Task 008:** When Plan item 3 (maintenance-bypass pre-commit policy) is implemented, it MUST also handle this case: pre-existing errors with an open covering Task should not block new commits. Otherwise the policy definition is circular — the very act of implementing Task 008 will be blocked by the errors Task 007 is supposed to fix.

### 3.2 Two-Commit Structure Violates Atomicity Mandate

**Severity:** Medium

The coherence prompt Step 5 mandates:

> All T1 and T2 repairs, any new Tasks, and the run-log entry (Step 6) MUST be committed together in a single atomic commit.

PR #26 has two commits:

- `2ac93bd` — chore(coherence): 2026-05-04 check — 3 repairs, 1 task (T1/T2 fixes + Task 007 + run-log)
- `6f41a1b` — task(008): harden coherence-check baseline protocol (Task 008 + run-log patch)

Task 008 was committed separately, after the run-log entry had already been written with `end_commit: 2ac93bd`. This means:

1. Task 008's files (`tasks/008-harden-coherence-baseline-protocol/`) are **not included in the run-log's `t3_tasks_created` count** (the log says `t3_tasks_created: 1`, counting only Task 007).
2. The second commit patched `end_commit` in the run-log, turning the bootstrap record into `end_commit: 4c5e7e4 f620b6d` — but the format waiver was applied to the new run's record, not the bootstrap. This part is actually fine.
3. The next run's baseline will be `2ac93bd`, which will include `6f41a1b` in its delta. Task 008's files will therefore be re-scanned by the next coherence run. This is a minor inefficiency but not a data-loss risk.

**Root constraint collision:** The prompt says "do not amend previous commits" AND "commit everything in one atomic commit." If the agent discovers a T3 finding *after* having already written the run-log entry, the only compliant path is a second commit — which violates atomicity. This is a genuine spec ambiguity. **Task 008's Plan item 4 should add a pre-write check for this: enumerate all T3 findings before writing the run-log entry.**

### 3.3 Task 008 Has `task_uses_prompts: []` Despite Modifying a Prompt

**Severity:** Low-Medium

Task 008's Plan item 4 states:

> Add an explicit Step 4 sub-check to `prompts/repo-coherence-check/prompt.md` before creating a new Task

And `task_affects_paths` lists `prompts/repo-coherence-check/prompt.md`. Yet `task_uses_prompts: []`.

Per TASK.md §3.3, `task_uses_prompts` holds "Slugs of prompts this Task executes." Modifying a prompt is not the same as executing it, so the empty list is technically correct. But the `task_affects_paths` entry creates an expectation of reciprocity that FOLDERS.md §6 requires: if this prompt's `prompt_relates_to_task` were updated to reference Task 008, the linkage linter would fire a reciprocity error unless `task_uses_prompts` lists the slug.

**Recommendation:** Either (a) leave `task_uses_prompts: []` and do not set `prompt_relates_to_task` on the coherence prompt when executing Task 008, or (b) if the schema extension lands (`task_spawns_prompts`), use that field instead. Document the decision in this notes.md.

### 3.4 Bootstrap Run-Log Record Remains Malformed

**Severity:** Low

The first record in `maintenance/run-log.md` (the bootstrap entry from session `claude/improve-agents-documentation-DyXZf`) still contains:

```
end_commit: 4c5e7e4 f620b6d
```

Task 008 correctly identifies this as a T1/T2-eligible repair (malformed field with unambiguous correct value), but neither the chore commit nor the task(008) commit fixed it in place. The second run's note says the awk one-liner "silently picks the first hash" — which means subsequent runs will keep extracting `4c5e7e4` (an unreachable hash) as the bootstrap baseline. The 7-day fallback will continue to fire until the bootstrap record is corrected.

**Fix:** The agent implementing `tools/lint-runlog.py` (Plan item 2) should simultaneously correct the bootstrap record to a single valid hash (or mark it `none` if the original commit is no longer reachable).

---

## 4. Minor Observations

### 4.1 PR Description Conflates Tasks 007 and 008

The PR description bundles two independent T3 Tasks (007: linkage reconciliation; 008: protocol hardening) under a single "reconcile coherence-check findings" heading. The commit history is clean (each task is its own commit), but the PR title blurs the boundary. Future searches for "baseline hardening" may not surface this PR. A dedicated PR per T3 Task group would have improved traceability.

### 4.2 `tasks/readme.md` Link Count vs. Actual Tasks

The task index (`tasks/readme.md`) now lists Tasks 001–008. Verify that the table entry for Task 006 points to the renamed folder (`006-surface-skills-architecture/`) not the old `003-` path. (The rename was done correctly in the commit, but cross-reference readers may still be confused if any external link cache is stale.)

### 4.3 `prompts/repo-coherence-check/prompt.md` Has No Forward Link

After Task 008 is executed and the prompt is updated per Plan item 4, the prompt's `prompt_relates_to_task` SHOULD be updated to reference `harden-coherence-baseline-protocol` so FOLDERS.md §6 reciprocity is satisfied. This was not done in this PR (correctly — the task is still open). Whoever closes Task 008 MUST add this link.

---

## 5. Recommendations for the Agent Executing Task 008

In priority order:

1. **Before starting:** Run `tools/check-governance.sh`. Confirm the 13 + 2 errors are still present and covered by Task 007 (open). Document the pre-existing-error decision in this notes file. Do not block Task 008 on Task 007.
2. **Plan item 3 first:** Implement the maintenance-bypass pre-commit policy *before* attempting any other plan items. Without it, every commit during Task 008's execution will fail the pre-commit hook (once the hook is installed per Plan item 3 as well). The ordering is: install hook → define bypass policy → then iterate on the other items.
3. **Plan item 4 early:** Add the `ls tasks/ | sort` guard to the coherence prompt before running another coherence check. The duplicate-`task_id` bug will recur until this guard is in place.
4. **Spec-ambiguity note on atomicity:** When updating `prompts/repo-coherence-check/prompt.md` Step 5, explicitly resolve the T3-after-run-log scenario: the prompt MUST instruct the agent to enumerate all T3 findings (including structural) BEFORE writing the run-log entry, so both the Tasks and the log are included in one atomic commit.
5. **Bootstrap record fix:** When implementing `tools/lint-runlog.py`, fix the bootstrap record's `end_commit` field as part of the same commit that introduces the linter. Running the linter immediately after would otherwise report its own bootstrap as an error.

---

## 6. Friction Level

FL1 — Minor friction. The two-commit atomicity violation was forced by a genuine spec ambiguity (no-amend + atomic-commit). The constraint collision is real and worth fixing in the prompt. Everything else is within normal operating range for a coherence run that finds pre-existing debt.
