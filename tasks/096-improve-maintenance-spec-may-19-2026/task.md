---
type: task
status: active
slug: improve-maintenance-spec-may-19-2026
summary: "Distil six findings (F27–F32) from the 2026-05-19 Repo Coherence Check into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, tools/fm/, tools/hooks/, and maintenance/run-log.md. Companion to Tasks 025, 044, 064 (all open) carrying earlier maintenance-spec findings."
created: 2026-05-19
updated: 2026-05-19
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/fm/edit.py
  - tools/hooks/_user-prompt-submit.py
  - maintenance/run-log.md
---

# Task 096 — Improve Maintenance Spec from 2026-05-19 Coherence Run

## Goal

Each of the six findings F27–F32 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`tools/fm/edit.py`](../../tools/fm/edit.py), [`tools/hooks/_user-prompt-submit.py`](../../tools/hooks/_user-prompt-submit.py), or [`maintenance/run-log.md`](../../maintenance/run-log.md); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md), [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md), and [Task 064](../064-improve-maintenance-spec-may-08-2026/task.md) — all of which carry earlier findings and remain open. The accumulation of four open `improve-maintenance-spec-*` Tasks is itself a manifestation of Task 064's F21 (the forcing-function gap is not yet enforced); see Meta-finding §M below.

## Findings

### F27 — Index-bullet status drift is the dominant ERROR shape but has no auto-repair mutator

**Symptom.** The 2026-05-19 coherence run produced exactly one gating ERROR from [`tools/check-governance.sh`](../../tools/check-governance.sh): diagnostic `T.7.11` on [`tasks/readme.md`](../../tasks/readme.md), reporting that Task 093's bullet still rendered `Status: open` even though [`tasks/093-skill-subfolder-readme-audit-linter/task.md`](../093-skill-subfolder-readme-audit-linter/task.md) carries `task_status: done`. The repair was unambiguously T1 mechanical: replace `Status: \`open\`.` with `Status: \`done\`.` on a single line, then `tools/fm/edit.py --bump-updated tasks/readme.md`. Task 064 F22 already flagged the **in-session signal** gap; this finding adds the **mutator** gap.

Today the agent must hand-edit the index every time a PR merges a task closure without touching the index bullet. The pattern has fired at least twice (Tasks 064 and 096 both observed `T.7.11` as the sole or dominant ERROR). The [`tools/fm/index_diff.py`](../../tools/fm/index_diff.py) linter detects the drift but does not repair it.

**Concrete diff:**

- Ship `tools/fm/sync-index.py` (or extend `index_diff.py` with a `--repair` flag) that consumes `T.7.11` diagnostics and rewrites the offending bullet's `Status: \`<old>\`` → `Status: \`<new>\`` per the source `task_status` value. The script MUST be idempotent and MUST refuse to touch any bullet whose status field is non-canonical (i.e. not one of `open|in_progress|done|abandoned|updated`).
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 3 T1 checklist SHOULD add a bullet "If `T.7.11` fires, invoke `tools/fm/sync-index.py` rather than hand-editing." This converts the recurring T1 drudge into a one-line invocation.
- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) "Mutation surface stability" paragraph SHOULD list `tools/fm/sync-index.py` alongside `tools/fm/edit.py` as canonical T1 mutators.

### F28 — Per-PR delta segmentation + ADR-governed bulk-add trust is missing

**Symptom.** The 2026-05-19 baseline (`6e4859d`, 2026-05-12) is 7 days old. The delta covers **65 commits and 762 changed files**, of which ~520 are under [`skills/`](../../skills/) (the SuperClaude + Superpowers corpus port governed by [ADR-0011](../../decisions/0011-external-skill-corpora-import.md), executed by Tasks 091 + 092, and each PR independently passed `tools/check-governance.sh`). Re-triaging those files in a coherence run is wasted work: every file was already gated at merge time.

The current protocol ([`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 1) treats the whole delta as a uniform inspection set. There is no notion of "this file was governed by a per-PR gate and does not need re-triage" — nor is there a notion of "this PR is an ADR-ratified bulk import" beyond reading the commit graph.

**Concrete diff:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 1c (new) SHOULD instruct the agent to detect `Merge pull request #NNN` commits in `git log <baseline>..HEAD --merges` and treat each PR's file set as a segmented unit. Files governed by an ADR (i.e. their path matches a glob declared in any `decisions/<NNNN>-<slug>.md` body or `adr_affects_paths` if such a key is added) MAY be skipped from manual triage on the trust that the PR's own gate handled them.
- [`MAINTENANCE.md §2.2`](../../MAINTENANCE.md) "What it Does" SHOULD note that the Coherence Check scope is **drift since last gate**, not **all files in delta**. Files that crossed a green gate at merge time are conformant by definition; the Coherence Check's job is to find drift introduced **between** gates.
- (Won't-fix candidate) If the team prefers a single-gate model (treat every coherence run as a fresh whole-delta inspection), record that disposition. The cost is the 762-file blast radius observed this session.

### F29 — Step 2 manual-triage table breaks down at >100 file deltas

**Symptom.** [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 2 instructs the agent to "build a triage table" with one row per file, classifying each as Governance spec / Operational / Research (complete) / Maintenance / Non-markdown / Deleted. The prompt notes "or in a workspace scratch note if the delta exceeds 20 files" — but it does not say what happens at 200, 700, 7000 files. This session's 762-file delta exceeds the workspace-scratch threshold by 38×.

Task 064 F24 ("linter-first as the canonical path on large deltas") proposed inverting the order — run Step 2.5 Linter-First Triage **first**, and use its diagnostics as the triage table. F29 here is the **quantification refinement** of F24: F24 establishes *which* path is canonical at scale, F29 specifies the *threshold* at which that path becomes mandatory rather than recommended. The two findings MUST be considered together — landing F24's inversion without F29's hard cap leaves agents free to attempt manual triage on arbitrarily large deltas; landing F29's cap without F24's inversion leaves no canonical alternative when the cap fires. F29 is narrower than F24 in another dimension too: even with linter-first, the manual file-by-file checklist at Step 3 (T1: stale `updated:`, broken links, missing readme) does not scale.

**Concrete diff:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 2 SHOULD declare a hard scale cap: when `git diff --name-only ${BASELINE} HEAD | wc -l > 100`, the agent MUST skip the manual Step 2 table and defer the entire triage to Step 2.5 linter output. The manual Step 3 T1/T2 checklist remains applicable only to files the linter flagged.
- Step 3 SHOULD add a one-line bypass: "If the delta exceeds 100 files, the T1 checklist is satisfied by `tools/fm/validate.py` exit 0 — manual per-file inspection is not required."
- [`MAINTENANCE.md`](../../MAINTENANCE.md) §2.2 SHOULD note the scale-cap rule.

### F30 — Closed-Task friction-log repair tier is unspecified

**Symptom.** [`tasks/030-cleanup-dramatica-skills-corpus/friction-log.md`](../030-cleanup-dramatica-skills-corpus/friction-log.md) and [`tasks/033-task-spec-integration/friction-log.md`](../033-task-spec-integration/friction-log.md) trip the FL declaration linter's `FR.B.4` ERROR on every coherence run (and have done so since at least 2026-05-08, per Task 064). The owning Tasks are `task_status: done`. The friction-logs are inside closed-Task folders but are NOT research workspaces, so [§1 T4](../../MAINTENANCE.md) does not strictly apply; conversely, the §1.0.1 closed-research T1/T2 allowance is research-workspace-specific.

The result is repair-tier ambiguity: an agent observing the recurring `FR.B.4` ERROR has no spec-clear answer to "may I add a `Highest Frustration Level: FL1` declaration line to a closed Task's friction-log without re-opening the Task?" Today the diagnostics are silently ignored, contradicting `FRUSTRATED.md §FL.Log` which requires a parseable declaration.

**Concrete diff:**

- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) repair-tier table SHOULD add a row (or §1.0.2 sibling subsection) for "Closed-Task friction-log metadata repair": permitted as T1 when the repair is a declaration-line addition or canonical-form normalisation; forbidden as T2/T3 (no new findings, no narrative rewrites). The owning Task's `task_status` MUST NOT mutate; the friction-log's `updated:` (if frontmatter is present) MAY be bumped.
- (Once the spec lands the rule) Apply the T1 fix to `tasks/030-…/friction-log.md` and `tasks/033-…/friction-log.md` in a follow-up commit so the recurring `FR.B.4` ERROR clears.
- (Won't-fix candidate) Promote `FR.B.4` from `[opt]` ERROR-tier to WARN-tier in [`tools/check-governance.sh`](../../tools/check-governance.sh) — but this masks the underlying ambiguity rather than resolving it.

### F31 — `/sc:*` skill mentions in user prompts are not surfaced by the hook routing

**Symptom.** The 2026-05-19 operator instruction included an explicit `/sc:analyze → /sc:reflect → /sc:improve → /sc:Review → /sc:createPR` sequence. The [`tools/hooks/_user-prompt-submit.py`](../../tools/hooks/_user-prompt-submit.py) hook (shipped by Task 094 ST-3) implements the `superpowers-using-superpowers` discipline-gate selector via verb-family heuristics (`bug`, `done`, `test`, `review`). It does NOT recognise `/sc:` skill references in the user prompt as deferred invocations the agent SHOULD honour, so its `additionalContext` payload misses the operator-requested skill set entirely.

This is the second time a coherence run has surfaced an operator instruction that the hook routing did not encode (F18 in Task 044 was the parallel finding for the operator-instructed post-run commits). F31 is narrower: the hook should DETECT explicit `/sc:` mentions and pass them through as an actionable suggestion.

**Concrete diff:**

- [`tools/hooks/_user-prompt-submit.py`](../../tools/hooks/_user-prompt-submit.py) SHOULD add a regex pass for `r'/sc:[a-z][a-z-]*'` against the submitted prompt. When matches are found, the hook MUST emit `hookSpecificOutput.additionalContext` enumerating the matched skill slugs and routing them through [`skills/sc-pm-agent/`](../../skills/sc-pm-agent/) (the orchestrator that coordinates `/sc:*` workflows).
- Add a pytest case under [`tools/tests/test_hooks.py`](../../tools/tests/test_hooks.py) exercising the new regex against a fixture prompt containing `/sc:analyze` + `/sc:reflect` + `/sc:createPR`.
- [`CLAUDE.md §14`](../../CLAUDE.md) `UserPromptSubmit` paragraph SHOULD mention the new detector alongside the existing verb-family heuristics.

### F32 — `pending` sentinel in run-log baseline lookup is undocumented

**Symptom.** The [`maintenance/run-log.md`](../../maintenance/run-log.md) file contains entries with literal `end_commit: pending` (recorded mid-session by agents who never returned to finalise the value). The Step 1a awk fall-forward in [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) handles this correctly via `git cat-file -e $i` (which fails on `pending`), but the `pending` sentinel is not documented anywhere — neither in [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) Record Types nor in the run-log's own header.

A future agent reading the run-log directly (rather than invoking the awk recipe) might be confused or attempt to git-checkout `pending`. The sentinel is operationally meaningful (it marks an unfinalised record), but the spec does not name it.

**Concrete diff:**

- [`maintenance/run-log.md`](../../maintenance/run-log.md) header (the "How to Read This File" section, plus the Record Format block) SHOULD document the `pending` sentinel: "If `end_commit:` cannot be computed before commit time, the agent MAY record `pending`; subsequent reads use the awk fall-forward to skip pending records and recover the most recent valid `end_commit`."
- [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) "Run-log baseline recovery" paragraph SHOULD reference the sentinel.
- (Optional) Ship a `tools/fm/finalise-runlog.py` mutator that rewrites a `pending` value to a concrete SHA when invoked post-commit (low priority — the awk handles it).

## Meta — Task accumulation observation (also Task 064 F21)

Filing Task 096 while Tasks 025, 044, and 064 remain open is itself a manifestation of Task 064 F21 ("`improve-maintenance-spec-*` Task accumulation lacks an enforcing function"). The operator's standing instruction is to file a new Task per coherence session; Task 064's proposed forcing function ("at most ONE open `improve-maintenance-spec-*` Task at a time") has not landed. This Task does NOT re-file F21; it cross-references the unresolved tension and treats it as a meta-observation rather than a new finding. The resolution belongs to Task 064 (land the diff or record won't-fix).

## Plan

1. Review F27–F32 against the four open companion Tasks (025 / 044 / 064 / this one); confirm none of the findings duplicates an open finding verbatim (preliminary check done at file time; the executing agent SHOULD re-verify before drafting diffs).
2. For each finding, draft the proposed diff (or won't-fix rationale) in a sibling `notes.md` or as a comment in the affected file's PR.
3. Land diffs incrementally; the Task closes when every F27–F32 has a landed diff or a documented disposition.
4. Update this Task's `task_status: done` and append a friction-log capturing what was hard.

## Todo

- [ ] 1. F27 — Ship `tools/fm/sync-index.py` (or `index_diff.py --repair`) auto-repair for `T.7.11`; wire into prompt Step 3 T1 checklist; mention in MAINTENANCE.md §1 mutation surface stability paragraph.
- [ ] 2. F28 — Add Step 1c per-PR delta segmentation to the coherence prompt; update MAINTENANCE.md §2.2 to scope the routine as drift-since-last-gate.
- [ ] 3. F29 — Document the 100-file scale cap in the prompt Steps 2/3 and in MAINTENANCE.md §2.2.
- [ ] 4. F30 — Add a closed-Task friction-log T1 allowance row to MAINTENANCE.md §1 (or as §1.0.2); apply the T1 fix to Tasks 030 + 033 friction-logs in a follow-up commit.
- [ ] 5. F31 — Extend `tools/hooks/_user-prompt-submit.py` with a `/sc:*` detector + emit additionalContext routing through `skills/sc-pm-agent/`; add pytest fixture + case; mention in CLAUDE.md §14.
- [ ] 6. F32 — Document the `pending` sentinel in `maintenance/run-log.md` header + MAINTENANCE.md §2.3.
- [ ] 7. Close the Task with `task_status: done`, sync the bullet in [`tasks/readme.md`](../readme.md), and write a friction-log summarising the work + FL declaration.

## Links

- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-19.
- Companion (open) Tasks: [025](../025-maintenance-spec-remaining-findings/task.md), [044](../044-improve-maintenance-spec-may-07-2026/task.md), [064](../064-improve-maintenance-spec-may-08-2026/task.md).
- Governing specs: [MAINTENANCE.md](../../MAINTENANCE.md), [TASK.md](../../TASK.md), [PROMPT.md](../../PROMPT.md), [FRUSTRATED.md](../../FRUSTRATED.md).
- Related skills: [`sc-pm-agent`](../../skills/sc-pm-agent/SKILL.md) (F31 routing target), [`sc-analyze`](../../skills/sc-analyze/SKILL.md) + [`sc-reflect`](../../skills/sc-reflect/SKILL.md) + [`sc-createPR`](../../skills/sc-createPR/SKILL.md) (operator-requested closing sequence).
