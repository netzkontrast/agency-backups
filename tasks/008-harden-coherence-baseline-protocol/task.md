---
type: task
status: active
slug: harden-coherence-baseline-protocol
summary: "Harden the coherence-check baseline + run-log protocol so it survives squash-merges, malformed records, and pre-existing T3 backlog without silent fallbacks."
created: 2026-05-04
updated: 2026-05-04
task_id: "008"
task_status: done
task_owner: "claude-code"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - maintenance/run-log.md
  - .githooks/pre-commit
  - tools/check-governance.sh
---

# Task 008 — Harden the Coherence-Check Baseline Protocol

## Goal

After two consecutive coherence runs (Jules's on 2026-05-04 and the second `claude-code` run later the same day), the baseline-recovery path was triggered both times. The current protocol degrades silently to a 7-day window whenever the recorded `end_commit` is lost, which masks the underlying squash-merge problem. Make the baseline contract robust enough that a coherence run either resolves a real baseline or fails loudly and proposes a reseed — never silently re-scans 600+ files.

## Background — Friction Found by the 2026-05-04 (second) Run

The second run of the day surfaced concrete failure modes in the existing spec:

1. **Squash-merge erases the baseline.** Jules's run recorded `end_commit: 4c5e7e4`. The PR was squash-merged, which rewrote history; `4c5e7e4` is no longer reachable from any ref. The run-log baseline cannot survive squash-merges. The next agent fell back to the 7-day window (per gate R1) — but that window scans 624 files and dilutes the delta-only mandate of the Coherence Check.

2. **Malformed `end_commit` line went undetected.** Jules's run-log entry contained `end_commit: 4c5e7e4 f620b6d` (two whitespace-separated hashes). The awk one-liner in `prompts/repo-coherence-check/prompt.md` Step 1 (`awk '{print $2}'`) silently picks the first hash; if a record had switched their order, the routine would have used the *baseline* as its own baseline, going in circles. There is no schema check on the run-log record format.

3. **Pre-commit hook is not installed by default.** `tools/check-governance.sh` reports 13 lint errors and 2 trust errors that pre-existed both runs. The pre-commit hook in `.githooks/pre-commit` is not wired into `.git/hooks/`, so commits succeed even though the protocol's "no regressions" expectation is technically violated. The previous run committed under the same gap. A maintenance-mode bypass policy is needed: pre-existing errors with an open Task SHOULD be allowed; new errors MUST block.

4. **Self-injected duplicate `task_id`.** The previous coherence run created `tasks/003-surface-skills-architecture/` while `tasks/003-analyze-skillmd-novel-authoring/` already existed. TASK.md §8.1 mandates renumbering before commit, but the maintenance prompt does not include this check in its T3-task-creation step. The duplicate landed and only this run's renumber-on-detect repaired it.

5. **L2 schema gap for "spawned prompts".** Three prompts (`cross-skill-context-poisoning`, `mega-context-limit-management`, `subjective-quality-evaluation`) are *follow-up* prompts spawned by Task 003. The current frontmatter schema only has `task_uses_prompts` (input) and `task_spawns_research` (output). Spawned-but-not-yet-executed prompts have nowhere to go that doesn't violate either reciprocity (FOLDERS.md §6) or `task_spawns_research` resolution (TASK.md §7.3). Task 003's author worked around this by listing prompt slugs in `task_spawns_research` — which then fail to resolve.

6. **Path-namespaced research workspaces are invisible to the linter.** `research/gemini/github-skillmd-novel-authoring-de-en/` exists but `tools/lint-linkage.py` only resolves top-level `research/<slug>/`. The `gemini/` provider sub-namespace introduced for external research ingestion (per `RESEARCH.md §6`) was not propagated to the validator.

## Plan

1. **Squash-merge resilience.** Update `MAINTENANCE.md §2.3` and the prompt's Step 1 so the baseline is recorded as a *content-hash of the run-log entry* in addition to the commit hash, and the baseline lookup falls forward by reading the most recent reachable `end_commit` rather than only the last record. If no recent `end_commit` is reachable, the agent MUST fail loudly and require a human-confirmed reseed (a tagged "coherence-reseed" annotation in `maintenance/run-log.md`).
2. **Run-log record validator.** Add a small linter (e.g. `tools/lint-runlog.py`) that parses `maintenance/run-log.md`, validates each record's fields (single hash per `end_commit`, ISO date, required keys), and is called from `tools/check-governance.sh`.
3. **Pre-commit policy for maintenance mode.** Define a `maintenance-bypass` mode in `.githooks/pre-commit` that allows commits if every error has a corresponding open Task whose `task_affects_paths` covers the offending file — and blocks otherwise. Document the policy in `MAINTENANCE.md §4`.
4. **Duplicate-`task_id` guard in the prompt.** Add an explicit Step 4 sub-check to `prompts/repo-coherence-check/prompt.md`: before creating a new Task, run `ls tasks/ | sort` and ensure the next free `<NNN>` is used. This mirrors TASK.md §8.1 but moves it earlier (creation-time) instead of relying on commit-time renumbering.
5. **Schema extension for spawned prompts.** Add `task_spawns_prompts` (list, scalar slugs) to the Task L2 namespace in `TASK.md §3.3`, `maintenance/language-spec.md §4`, and `tools/validate-frontmatter.py`. Update `tools/lint-linkage.py` reciprocity to honor it.
6. **Provider-namespaced research path resolution.** Extend `tools/lint-linkage.py` to accept `research/<provider>/<slug>/` as a valid resolution for `prompt_spawned_from_research` and `task_spawns_research`. Document the convention in `RESEARCH.md §6`.
7. **Smoke-test the new flow.** Run a third coherence check after the changes land and confirm `check-governance.sh` exits zero and the run-log is parsed without fallback.

## Todo

- [x] Specify the squash-merge-resilient baseline contract in `MAINTENANCE.md` and the prompt.
- [x] Implement `tools/lint-runlog.py` and wire it into `tools/check-governance.sh`.
- [x] Define and implement the maintenance-bypass commit policy in `.githooks/pre-commit`.
- [x] Add the duplicate-`task_id` pre-creation check to `prompts/repo-coherence-check/prompt.md` Step 4.
- [x] Extend the L2 schema with `task_spawns_prompts` (TASK.md, language-spec, validators).
- [x] Extend `tools/lint-linkage.py` to resolve `research/<provider>/<slug>/`.
- [x] Run the next coherence check and confirm zero pre-commit errors and a clean run-log entry.

## Links

- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-04 (second).
- Sibling Task that addresses the lint backlog uncovered by the same run: [`../007-reconcile-closed-task-linkage/task.md`](../007-reconcile-closed-task-linkage/task.md).
- Governing specs: [MAINTENANCE.md](../../MAINTENANCE.md) §1, §2, §4; [TASK.md](../../TASK.md) §3.3, §7, §8.1; [PROMPT.md](../../PROMPT.md) §6.5, §6.6; [FOLDERS.md](../../FOLDERS.md) §6; [RESEARCH.md](../../RESEARCH.md) §6.
- Coherence prompt to update: [`../../prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md).
