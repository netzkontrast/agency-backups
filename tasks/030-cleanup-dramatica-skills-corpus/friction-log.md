---
type: friction-log
status: active
slug: task-030-friction-log
summary: "Execution-time friction log for Task 030. All four §Goal gates now PASS after a re-dispatch on a fresh quota cycle landed ST-7 (aliases), ST-8 (scenario coverage), and ST-9 (precompile). Task is task_status: done. Five execution-time friction events recorded for Task 029 to absorb."
created: 2026-05-06
updated: 2026-05-06
---

# Task 030 — Execution Friction Log

This file records friction encountered while EXECUTING Task 030. The planning-time friction is in `notes.md §3` (separate file, separate scope, per the FRUSTRATED.md convention).

## Run summary

**Branch:** `claude/cleanup-dramatica-skills-tTTDq`

**Commits landed (in order):**

| SHA | Subject |
|---|---|
| 6fe4592 | chore(dramatica): strip PDF artefacts from references (Task 030 ST-1) |
| c0cfbb3 | fix(dramatica): repair corrupted headings + mis-attributed YAML (Task 030 ST-2) |
| 9dc6b92 | fix(dramatica): resolve 8 anchor mismatches + partition 106 unmapped headings (Task 030 ST-3) |
| 4150b37 | fix(dramatica): resolve 5 empty redirect entries (Task 030 ST-4) |
| 6d5e2d2 | feat(dramatica-nav): cleanup.py — corpus cleanup linter (Task 030 ST-6) |
| eb61adb | feat(dramatica-nav): term.py for create/edit/move/deprecate (Task 030 ST-5) |
| d5e2cf6 | chore(task-030): update vocab block-count baseline + salvage ST-7 partial |
| 1e95a1f | docs(task-030): friction-log capturing partial run state (later superseded by this final state) |
| 14fbe8a | feat(dramatica-nav): aliases.py — bulk EN loader + DE starter set (Task 030 ST-7) |
| 652ff81 | chore(task-030): fix st7-partial/readme.md frontmatter |
| 3b16a88 | feat(dramatica-nav): scenario coverage iter 1/3 (Task 030 ST-8) |
| f169a26 | feat(dramatica-nav): scenario coverage iter 2/3 (Task 030 ST-8) |
| 489b5e8 | feat(dramatica-nav): scenario coverage iter 3/3 (Task 030 ST-8) |
| (ST-9)  | feat(dramatica-nav): precompile persona-scenario encoding hints (Task 030 ST-9) |

**Acceptance gate status (Task 030 §Goal) — all four PASS:**

- **Gate 1 — corpus is artefact-free.** PASS. `tools/dramatica-nav/cleanup.py --check` reports `0 diagnostics`. ST-1 stripped 37 copyright footers, 336 page-number lines, 8 double-apostrophe escapes, and 100 leading-`>` Contents-list bullets. ST-2 + ST-4 cleared the corrupted-heading and empty-redirect classes.
- **Gate 2 — anchors and frontmatter agree.** PASS for canonical kinds. `validate.py` reports `term_file-anchor-mismatch: 0`. The 17 partial-quad-membership warnings remain (deferred to Task 029 per A-2). The unmapped-heading count is 103, partitioned into Buckets A/B/C/D in `notes.md §5` (ST-3 deliverable).
- **Gate 3 — tooling is mechanical.** PASS. All four scripts shipped with smoke tests: `term.py` (ST-5, 9 tests), `cleanup.py` (ST-6, 18 tests, wired into `check-governance.sh`), `aliases.py` (ST-7, 11 tests, projects 395 EN aliases + 102 DE aliases), `precompile.py` (ST-9, 7 tests).
- **Gate 4 — consumer-side payloads exist.** PASS. 11 JSON files under `maintenance/schemas/narrative-ontology/precompiled/`. Token-cost benchmark: precompiled path consumes **41.1% of prose path on average** (gate ≤60%). Per-scenario range 34.4%–47.4%; novel.crucial-element-audit specifically lands at 37.2%.

**Net:** 9 of 9 subtasks landed plus housekeeping commits. Task is `task_status: done`.

**Validator state at run end:** `quad-membership-partial: 17 / term_file-anchor-mismatch: 0 / unmapped-heading: 103 / schema: 0 / alias-uniqueness: 0`. `pytest tools/dramatica-nav/tests/`: 87 passed. `tools/check-governance.sh`: PASS.

## Friction events

### FE-EX-1 (FL2, Significant) — Parallel main-tree dispatch races on shared markdown.

**What happened.** The task plan called for Phase A's four subtasks (ST-1..ST-4) to be dispatched as four parallel `Agent` calls in main-tree (no worktree). Both ST-1 (refactoring-expert, regex-driven deletions across all references) and ST-2 (technical-writer, heading repairs in character-dynamics.md) wrote to the same file. The first attempt produced two race conditions (per ST-2's report):

1. ST-2's structural edits to `character-dynamics.md` were silently reverted twice. ST-1 rewrote the entire file via `_strip_artifacts.py` between ST-2's Edit and `git add` calls. ST-2 had to roll back a botched `41a6901` commit that captured ST-1's deletions only and re-apply.
2. `git add <single-file>` auto-staged 22 unrelated files, presumably from a parallel `git add -A` by ST-1's process.

ST-1 reported the same observation from its side: a pre-existing uncommitted ST-2 modification was found at session start. ST-1 worked around by restoring HEAD before applying its work, then re-laying ST-2's change as an uncommitted working-tree change.

**Outcome.** Both subagents recovered and produced clean commits, but the race burned ~1 round-trip of agent budget on ST-2's side.

**Mitigation taken in this run.** After ST-1 + ST-2 landed, ST-3 and ST-4 (which both depended on ST-2 and would have collided on `ontology.json` and `elements.md`) were dispatched **sequentially**, not in parallel. This contradicted the task plan but matched the subtasks' explicit `subtask_depends_on` frontmatter (ST-3 and ST-4 declare ST-2 as prerequisite). Both ran cleanly.

**Pattern this exposes.** The task plan's "main-tree, dispatch in parallel" recipe is unsafe whenever agents touch overlapping files, and the dispatcher cannot tell statically when files will overlap. The frontmatter `subtask_depends_on` field IS the canonical signal — and when it lists prerequisites, parallel dispatch is wrong by definition.

**Suggested rule for Task 029 to ratify.** A driver implementing `/sc:agent` parallel dispatch MUST honour `subtask_depends_on` as a serialisation barrier: if any subtask in the wave declares another subtask in the same wave as its prerequisite, the wave MUST be split.

### FE-EX-2 (FL3, Blocking) — Org monthly usage limit hit mid-Phase-B.

**What happened.** ST-7 was dispatched in parallel with ST-5 and ST-6 in worktree isolation. ST-5 and ST-6 completed cleanly. ST-7 returned `You've hit your org's monthly usage limit` after producing `tools/dramatica-nav/aliases.py` (~826 LOC) but before authoring tests, the DE starter JSON, the conflict report, the `notes.md §8` update, or any commit.

**Immediate impact.** Phase C (ST-8, ST-9) was not dispatched because subsequent agent calls would have hit the same limit. The driver continued in the main session: cherry-picked ST-5 and ST-6 commits onto the parent branch, salvaged ST-7's partial under `tasks/030-cleanup-dramatica-skills-corpus/st7-partial/`, fixed a stale test assertion (vocab block count 187 → 194 to match the new Phase A baseline), and committed.

**Outcome.** Task 030 reaches a stable open state with §Goal gates 1, 2, and partial-3 satisfied. Gates partial-3 (aliases.py + precompile.py) and gate 4 (precompiled JSONs) require a re-dispatch on a fresh quota cycle.

**Pattern this exposes.** A long-running multi-subtask task can be partially blocked by a quota event that affects only some subtasks. The task graph survives — the work that landed is consistent and tested — but the §Goal definition's all-or-nothing acceptance ("all four §Goal items hold simultaneously") is incompatible with partial completion. Either the task needs partial-completion semantics, or the §Goal needs to be split into per-phase milestones each of which can close independently.

**Suggested rule for Task 029 to ratify.** Multi-phase tasks SHOULD declare per-phase milestones rather than a single all-or-nothing §Goal block. Each phase's milestone is `done` independently; the task is `done` iff all phases are. This matches how ADR-style governance handles incremental ratification.

### FE-EX-3 (FL1, Minor) — Pre-existing test assertion stale post-Phase-A.

**What happened.** `tools/dramatica-nav/tests/test_lib_frontmatter.py::test_walk_vocab_blocks_count` asserted `len(blocks) == 187` (the Task 015 baseline). After Phase A landed, the count rose to 194 (ST-2 split Approach into Approach + Growth + Intuitive; ST-3 minted Ability + Change + Non-acceptance + Non-accurate + Self-Interest). Both ST-5 and ST-6 reported the failure; both correctly noted it was pre-existing, not their regression.

**Outcome.** Driver updated the assertion to 194 with a comment naming the Task 030 deltas; full pytest suite returns 69 passed.

**Pattern this exposes.** Hard-coded baseline counts in test assertions create silent failure modes whenever a downstream task changes the corpus. They should either be data-driven (count blocks, write to fixture, regenerate fixture under change) or named-guard (test that the *delta* matches an expectation, not the absolute count).

**Suggested rule for Task 029 to ratify.** Test assertions over corpus-wide counts MUST either be regenerated automatically (fixture-from-corpus pattern) or carry an explicit "update when this changes" comment naming the source of truth.

### FE-EX-4 (FL1, Minor) — `agency-adr` CLI not on PATH despite Task 028 being `task_status: done`.

**What happened.** ST-5 and ST-6's pre-dispatch gate (per parent task §Background) required Task 028 to be `task_status: done` before opening their worktrees. Task 028's frontmatter is `done`. But the actual `agency-adr` CLI is not installed on PATH in this environment. ST-5's `term.py deprecate` and ST-6's `cleanup.py --explain` both correctly fell through to the documented `# TODO(after-028)` stderr fallback path; neither subtask was blocked.

**Outcome.** No execution-time block, but the gate's signal-to-noise is worse than ideal — the `task_status: done` field claims a deliverable that is not yet on PATH.

**Pattern this exposes.** Frontmatter `task_status: done` is a coarse signal; it doesn't distinguish "specification ratified" from "tooling shipped and installed". For tasks whose deliverable is a runnable CLI, the dispatch gate should check `command -v <cli>` rather than (or in addition to) the upstream task's frontmatter.

**Suggested rule for Task 029 to ratify.** A pre-dispatch gate for "CLI X must exist" should be a runtime probe (`command -v X`), not a metadata read of an upstream task's `task_status`. The metadata gate stays as a coarse readiness hint; the runtime probe is the authoritative check.

### FE-EX-5 (FL1, Minor) — Worktree-side artefact leaked into main checkout.

**What happened.** ST-9 ran in a worktree (`agent-a93f60e99cd01431c`). During its run the main checkout developed an untracked `maintenance/schemas/narrative-ontology/precompiled.schema.json` file. Likely cause: the worktree shares `.git` with the main checkout but not the working tree, so file system events are isolated; the leak is more likely from the agent's smoke-test invocations probing relative paths and brushing the parent repo. The file was removed before cherry-picking the ST-9 commit.

**Outcome.** No data loss; ST-9's commit applied cleanly after the stray file was removed.

**Pattern this exposes.** Worktree isolation is git-tree-only, not filesystem-only. Agents that resolve repo paths via `Path.cwd()` or `os.getcwd()` can land artefacts outside their worktree if they accidentally walk up to the parent checkout.

**Suggested rule for Task 029 to ratify.** Worktree-mode agent prompts should explicitly fence the agent to its worktree path; the harness could enforce this with a `--require-cwd-prefix` flag.

## /sc:* invocation log (final)

| When | Command | Notes |
|---|---|---|
| Phase A wave 1 | `/sc:agent` × 2 (ST-1, ST-2) | Parallel main-tree dispatch via two harness `Agent` calls in one message. Race documented in FE-EX-1. |
| Phase A wave 2 | `/sc:agent` × 1 (ST-3) | Sequential, after ST-2 landed (depends_on contract). |
| Phase A wave 3 | `/sc:agent` × 1 (ST-4) | Sequential, after ST-3 landed (overlap on ontology.json + elements.md). |
| Phase B | `/sc:agent` × 3 (ST-5, ST-6, ST-7) | Parallel worktree dispatch in one message. ST-7 hit usage limit (FE-EX-2). |
| Phase B retry | `/sc:agent` × 1 (ST-7 restart) | Re-dispatched on a fresh quota cycle with the salvaged partial as a starting hint. Landed cleanly. |
| Phase C-1 | `/sc:agent` × 1 (ST-8) | Main-tree, sequential. Three commits, one per iteration; M01 gate held throughout (median 3.0, max 4). |
| Phase C-2 | `/sc:agent` × 1 (ST-9) | Worktree, sequential. Single commit; benchmark 41.1% avg (gate ≤60% PASS). |

`/sc:improve --loop --iterations 3` (planned for ST-8): the spirit was honoured — three iterations with per-iteration M01 gate — but the dispatcher used the harness `Agent` tool with a single brief that internally drove the three iterations, rather than three discrete `/sc:improve` invocations. Equivalent shape, fewer dispatch round-trips.
`/sc:test`: invoked manually as `pytest tools/dramatica-nav/tests/` after each merge.
`/sc:cleanup`: not invoked (planning-stage convention; not load-bearing).
`/sc:createPR`: NOT invoked by this driver. Per AGENTS.md § Closing Run Procedure, the user opens the PR. The task is `task_status: done`, governance passes, and the branch is pushed; the PR is the user's call.

## Closing state

- Branch `claude/cleanup-dramatica-skills-tTTDq` carries 14 task-related commits ahead of `origin/main`.
- All four §Goal gates PASS (see Run summary table above).
- `tools/check-governance.sh`: PASS.
- `pytest tools/dramatica-nav/tests/`: 87 passed.
- `task.md` frontmatter: `task_status: done`.

## Pattern routing (post-mortem correction)

An earlier draft of this section claimed Task 029 absorbs FE-EX-1..5 as candidate inputs. **That was wrong.** Task 029 (`adr-assumption-audit`) was scoped specifically to the ADR-governance-spec audit and shipped its REPORT.md (9 ASMs / 11 IADRs / 7 PDs) before Task 030's friction patterns existed. Task 029 is `task_status: done`; it cannot retroactively absorb anything.

The patterns DO have homes — on main's open spec-integration chain (Tasks 032–040). The actual routing:

| Pattern | Natural home (open task on main) | Why |
|---|---|---|
| FE-1 — no canonical subtask file template | 033 task-spec-integration | T.4.* subtask format ratification. Partly resolved by 041 `prompt_kind: task-spec`. |
| FE-2 — `/sc:agent` contract undocumented | 040 superclaude-spec-evaluation | the `/sc:*` command surface is exactly its scope. |
| FE-3 — `task_status` drift readme vs frontmatter | 039 maintenance-spec-integration | drift-detection / repair tier. |
| FE-4 — renderer-emitted depth-2 YAML breaks rule | 034 prompt-spec-integration | prompt structure + frontmatter contract. |
| FE-5 — task spawns prompt that another task uses | 033 task-spec-integration | task↔prompt edge cardinality. Partly resolved by 041. |
| FE-6 — no `/sc:` command lifecycle spec | 040 superclaude-spec-evaluation | command-set documentation is in scope. |
| FE-7 — verbose-by-design vs anti-bloat tension | 038 frustrated-spec-integration | FRUSTRATED.md §28 + special-triggers home. |
| FE-8 — provisional-conventions pattern | 033 task-spec-integration | declaration mechanism for not-yet-ratified rules. |
| FE-9 — `task_spawns_prompts` cardinality unclear | 033 task-spec-integration | TASK.md §3.3 definition. |
| FE-10 — preview lifecycle for ontology artefacts | 032 agents-spec-integration | AGENTS.md §NO.5 amendment is its work surface. |
| FE-EX-1 — parallel-dispatch race | 040 superclaude-spec-evaluation | `/sc:agent` + `subtask_depends_on` interaction. |
| FE-EX-2 — org quota partial-completion | 040 superclaude-spec-evaluation | per-phase milestones for multi-phase tasks. |
| FE-EX-3 — hardcoded test-count drift | (none — Task 042 Item 10) | local fix; no downstream rule needed. |
| FE-EX-4 — `agency-adr` metadata-vs-runtime gap | 040 superclaude-spec-evaluation | pre-dispatch gate semantics. |
| FE-EX-5 — worktree filesystem leak | 040 superclaude-spec-evaluation | worktree contract for `/sc:agent`. |

This is documentation only. Filing each pattern as an explicit input on the destination task is **not** done from this branch — the destination tasks live on main, and editing them from a feature branch would be invasive. A future driver picking up Task 040 (or any of 032/033/034/037/038/039) is expected to discover this routing table when it audits Task 030's friction-log per the FRUSTRATED.md cross-referencing convention.
