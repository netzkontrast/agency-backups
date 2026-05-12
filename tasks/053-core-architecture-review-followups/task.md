---
type: task
status: archived
slug: core-architecture-review-followups
summary: "Triage an architectural review of the Agency spec corpus + fm-toolchain against the live Task graph; dispatch follow-up Tasks for the seven gaps not already owned by 017/019/043/044/045/046."
created: 2026-05-07
updated: 2026-05-12
task_id: "053"
task_status: open
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - core-architecture-review-2026-05
task_spawns_research:
  - core-architecture-review-2026-05
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tasks/053-core-architecture-review-followups/
  - tasks/readme.md
  - prompts/core-architecture-review-2026-05/
  - research/core-architecture-review-2026-05/
---

# Task 053 — Core Architecture Review Follow-ups

## Goal

Land the architectural review of the Machine/Actor/Space substrate (root specs + `tools/fm/` toolchain + governance pipeline) as a first-class repo artefact, **and** convert each of its actionable "What's Bad" / "What I Would Do Differently" findings into either (a) a citation against an already-open Task, or (b) a freshly filed successor Task at the next free `<NNN>` slot. The single falsifiable outcome is: every one of the ten review findings is mapped to exactly one owning Task (existing or newly opened by this Task) before this Task closes as `done`.

This Task does **not** itself implement the fixes. Per [`MAINTENANCE.md §3`](../../MAINTENANCE.md), complex issues surfaced by an audit MUST be packaged as Tasks for a future agent rather than fixed inline by the auditor. This is the packaging Task.

## Plan

1. **Land the review report.** ~~Commit `review-report.md` verbatim into this Task folder.~~ **Superseded by [PR #86 review](./review-pr86-claude-brave-darwin.md) D1 disposition (a):** the verbatim review now lives at [`research/core-architecture-review-2026-05/output/REPORT.md`](../../research/core-architecture-review-2026-05/output/REPORT.md), Actor layer at [`prompts/core-architecture-review-2026-05/`](../../prompts/core-architecture-review-2026-05/). The report is the artefact (Space); the Plan steps below dispatch its findings (Machine).
2. **Triage the ten findings against the live Task index.** For each "What's Bad" item B.1–B.10 in the report, append a row to [`triage.md`](./triage.md) (created in step 4) citing the owning Task, the gap, and the dispatch decision (`existing` / `open-new` / `wontfix-rationale`). Cross-references against [`tasks/readme.md`](../readme.md) state at branch-time:
   - **B.1 Dual-toolchain transition debt** → already addressed by [Task 017](../017-migrate-repo-to-flexible-toolchain/) (`done`) and [Task 019](../019-fm-toolchain-suite-integration/) (`done`); **residual gap**: [`tools/check-governance.sh:33`](../../tools/check-governance.sh) still gates on `FM_TOOLCHAIN=1` rather than defaulting to fm-as-primary. Open a thin successor Task to flip the default and retire the legacy branch.
   - **B.2 `LOOP_LOG` in `AGENTS.md`** → no existing Task; runtime session state living in a governance spec violates [`README.md §11.6 R.19`](../../README.md). Open a new Task to relocate `AGENTS.md` lines 340–403 into `maintenance/session-logs/` (or the friction-log of the originating Task) and add a `tools/check-spec-runtime-state.py` linter that flags any runtime-state section pattern in root specs.
   - **B.3 Duplicate task IDs (006/006, 009/009, 031/031, 032/032)** → owned by [Task 043](../043-renumber-duplicate-task-ids-v3/) (`open`). The duplicate-ID *prevention* linter is owned by [Task 033](../033-task-spec-integration/) ST-3 (advisory by default; gated under `FM_DUPLICATE_TASK_ID_STRICT=1` per [`TASK.md §8.1`](../../TASK.md)). No new Task; cite both.
   - **B.4 No CI/CD** → owned by [Task 046](../046-github-workflow-research/) (`open`). No new Task; verify Task 046's scope covers the governance suite + ADR validation.
   - **B.5 Narrative ontology scope creep** → no existing Task. The repo's `NO.5` rule warns agents *not to load* the narrative ontology for non-narrative work, which is a workaround, not a fix. Open a new Task to evaluate extracting `skills/novel-architect/`, `skills/the-agency-system-architect/`, `skills/suno-lyric-writer/`, and the Dramatica corpus into a sibling repo (or at minimum a clearly governance-isolated `skills/narrative/` namespace with its own root spec). Decision-class Task — produce an ADR, not an immediate move.
   - **B.6 Spec proliferation (9+ root specs)** → owned in part by [Task 044](../044-improve-maintenance-spec-may-07-2026/) (`open`) and [Task 045](../045-readme-coherence-refresh/) (`open`); neither targets *consolidation*. Open a new Task to evaluate merging `PRE_COMMIT.md` into `AGENTS.md §Mandatory Pre-Commit` and `FRUSTRATED.md` into `MAINTENANCE.md §Friction Logging` against the load-cost / coupling tradeoff. Decision-class Task — produce an ADR before acting.
   - **B.7 `read_fm()` silent `{}` on parse error** → no existing Task. [`tools/fm/_core.py:145`](../../tools/fm/_core.py) returns `{}` for a non-empty file with malformed frontmatter, causing downstream linters to emit "missing key" rather than "parse error". Open a new Task to either (a) emit a `WARN`-tier `Diag` from `read_fm` when `strict=False` parsing of a non-empty file produces an empty dict, or (b) thread an out-parameter so callers can disambiguate `no-frontmatter` from `malformed-frontmatter`.
   - **B.8 Research immutability is absolute** → no existing Task. [`MAINTENANCE.md §1`](../../MAINTENANCE.md) `T4` blocks every modification to a `research_phase: complete` workspace, including T1 (frontmatter date bumps) and T2 (broken-link repair). Open a new Task to amend MAINTENANCE.md to permit T1/T2 repairs on closed research while preserving T3/T4 content immutability — and ratify the change via the §4.7 `updated` lifecycle on any affected closed Task.
   - **B.9 Closing procedure is `/sc:createPR`-specific** → no existing Task. [`AGENTS.md §Skill Provenance`](../../AGENTS.md) makes the SuperClaude `sc:createPR` command authoritative; Jules / Gemini get vague guidance. Open a new Task to define a platform-agnostic closing-run procedure ("open a PR via your platform's mechanism, attach the friction-log, ensure index sync") and demote `/sc:createPR` to one implementation.
   - **B.10 No end-to-end integration tests** → no existing Task. The `tests/fm/` suite covers atomic tools well; nothing simulates `Task → Prompt → Research → check-governance.sh` end-to-end. Open a new Task to scaffold a tmpdir-based integration test that creates a minimal triptych and verifies `tools/check-governance.sh` exits zero, then mutates each tier to verify each linter row in [`TASK.md §7.0`](../../TASK.md) emits the documented diagnostic.
3. **Open the seven new follow-up Tasks.** For each B.1, B.2, B.5, B.6, B.7, B.8, B.9, B.10 row above whose dispatch decision is `open-new`, create a sibling `tasks/<NNN>-<slug>/` folder per [`TASK.md §8.1`](../../TASK.md) (next free `<NNN>` discovered at commit-time, not pre-allocated here — slot races are resolved per §8.1 step 1–3). Each successor Task MUST carry `task_blocked_by: []` (none of these block on this Task; this Task is the dispatch, not the precondition). Each successor Task's `task.md` MUST cite this Task by relative path under `## Links`.
4. **Cross-link the dispatch.** Add [`triage.md`](./triage.md) recording the ten-row map above with one row per finding: `finding_id | owning_task | gap_residual | dispatch_decision | new_task_slot`. Update this Task's `task_spawns_prompts` (none) and the new Tasks' `task.md` files; do **not** populate `task_spawns_research` because none of the gaps require a fresh research run distinct from those listed in the new Tasks' own plans.
5. **Sync the tasks index.** Per [`TASK.md §4.8 / §7.11`](../../TASK.md), update [`tasks/readme.md`](../readme.md) **in the same commit** as each new folder creation: one bullet per new folder, citing its `task_status: open`, with this Task as a `(see Task 053)` annotation on each. The index `updated:` field is bumped on every such commit.
6. **Close.** When all eight successor Tasks are filed and the triage matrix is complete, set `task_status: archived`, write [`friction-log.md`](./friction-log.md) with an FL[0–3] declaration (FL0 acceptable if dispatch executed cleanly), and re-sync the index per §4.8.

## Todo

- [x] Land `task.md` (this file) + `readme.md` + `review-report.md` + `tasks/readme.md` membership entry on branch `claude/review-core-architecture-bMU9X`.
- [x] Author `triage.md` with one row per B.1–B.10 finding (Plan step 2). → [`./triage.md`](./triage.md).
- [x] Disposition for [PR #86 review](./review-pr86-claude-brave-darwin.md) D1 (option a): move `review-report.md` to [`research/core-architecture-review-2026-05/output/REPORT.md`](../../research/core-architecture-review-2026-05/output/REPORT.md); add the Actor layer at [`prompts/core-architecture-review-2026-05/`](../../prompts/core-architecture-review-2026-05/); update Task 053 frontmatter (`task_uses_prompts`, `task_spawns_research`).
- [x] Open new Task for B.1 residual: flip `FM_TOOLCHAIN` default + retire `tools/check-governance.sh:33` legacy branch. → [Task 054](../054-flip-fm-toolchain-default/).
- [x] Open new Task for B.2: relocate `AGENTS.md` `LOOP_LOG` runtime state + ship `tools/check-spec-runtime-state.py` WARN-tier linter. → [Task 055](../055-relocate-agents-loop-log/).
- [x] Open new Task for B.5: ADR-class evaluation of narrative-skills extraction (`skills/novel-architect/`, `skills/the-agency-system-architect/`, `skills/suno-lyric-writer/`, Dramatica corpus). → [Task 056](../056-narrative-skills-extraction-adr/).
- [x] Open new Task for B.6: ADR-class evaluation of root-spec consolidation (`PRE_COMMIT.md` → `AGENTS.md`; `FRUSTRATED.md` → `MAINTENANCE.md`). → [Task 057](../057-root-spec-consolidation-adr/).
- [x] Open new Task for B.7: emit WARN `Diag` from `tools/fm/_core.py read_fm` when `strict=False` parse of non-empty file yields `{}`. → [Task 058](../058-read-fm-warn-diagnostic/).
- [x] Open new Task for B.8: amend `MAINTENANCE.md` T4 rule to permit T1/T2 repairs on closed research while preserving T3/T4 content immutability. → [Task 059](../059-closed-research-repair-allowance/).
- [x] Open new Task for B.9: platform-agnostic closing-run procedure in `AGENTS.md`; `/sc:createPR` becomes one implementation. → [Task 060](../060-platform-agnostic-closing-procedure/).
- [x] Open new Task for B.10: scaffold `tests/integration/test_governance_e2e.py` covering Task → Prompt → Research → check-governance.sh. → [Task 061](../061-governance-integration-test-scaffold/).
- [x] Cite Tasks 017, 019, 033, 043, 046 in `triage.md` for findings B.1, B.3, B.4 respectively (no new Tasks for those rows). → [`./triage.md`](./triage.md) Matrix rows B.1, B.3, B.4.
- [x] Re-sync `tasks/readme.md` (membership + statuses + lineage) on each new-Task commit per §4.8 / §7.11.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure (mandatory per FRUSTRATED.md, FL0 acceptable).

## Links

- [`../../prompts/core-architecture-review-2026-05/`](../../prompts/core-architecture-review-2026-05/) — Actor layer: the executable RISEN+ReAct prompt this Task ran. Authored retrospectively per [PR #86 review](./review-pr86-claude-brave-darwin.md) D3.
- [`../../research/core-architecture-review-2026-05/output/REPORT.md`](../../research/core-architecture-review-2026-05/output/REPORT.md) — Space layer: the verbatim architectural review (citations into `README.md`, `AGENTS.md`, `MAINTENANCE.md`, `tools/fm/_core.py`, `tools/lint-linkage.py`, `tools/check-governance.sh`, `tests/fm/test_falsification_attacks.py`). Lifted from `tasks/053-…/review-report.md` per [PR #86 review](./review-pr86-claude-brave-darwin.md) D1 disposition (a).
- [`./triage.md`](./triage.md) — 10-row matrix mapping each B-finding to its owning Task.
- [`./review-pr86-claude-brave-darwin.md`](./review-pr86-claude-brave-darwin.md) — Reviewer findings that triggered the D1+D2+D3 disposition.
- [`./readme.md`](./readme.md) — folder index per [`FOLDERS.md`](../../FOLDERS.md).
- [`../../TASK.md`](../../TASK.md) — Task lifecycle, frontmatter ontology, blocker semantics.
- [`../../MAINTENANCE.md`](../../MAINTENANCE.md) — friction-to-Task conversion rule (§3) and T1–T4 mutation classes (§1) cited above.
- Existing Tasks cited by triage rows: [017](../017-migrate-repo-to-flexible-toolchain/), [019](../019-fm-toolchain-suite-integration/), [033](../033-task-spec-integration/), [043](../043-renumber-duplicate-task-ids-v3/), [044](../044-improve-maintenance-spec-may-07-2026/), [045](../045-readme-coherence-refresh/), [046](../046-github-workflow-research/).
