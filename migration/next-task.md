---
type: note
status: pending
slug: archive-pre-migration-tree
summary: "Mandatory next task: archive every file in the repo (except /migration/ and /.claude/) into /archive/ via git mv, then rebuild from the migration plan. Triggers only when refactoring plan is ratified and user explicitly authorises execution."
created: 2026-05-13
updated: 2026-05-13
---

# Next Task — big-bang archive of pre-migration repo state

> **Status:** `pending`. This task is **MANDATORY** but **NOT yet executable**. It triggers only when the refactoring plan in `/migration/` is ratified (open questions Q1–Q7 closed; turn-11 provisional answers re-confirmed; ADR-0013 finalised in `/migration/adr-draft.md`) AND the user explicitly authorises execution via direct instruction.

---

## 1. User directive

Quoted verbatim from the session that produced this file:

> *"All Content of the repo - including the Adrs Are revoked until further notice… Based on the Gemini Research… and all Migration artefacts - we rebziöd this repo completly - starting with archiving (git mv) of every file execept the Migration folder - and the .claude folder - into Archive (Save this as mandatory Next Task - that Starts when the refactoring plan is Ready)"*

Parsed:

- **All current repo content — including the 12 existing ADRs — is revoked.** Nothing in the live tree is binding any longer. The authoritative sources for the rebuild are: (a) the Gemini Deep Research briefs at [`.claude/research-results/gemini-1-architecture-audit.md`](../.claude/research-results/gemini-1-architecture-audit.md) (primary, 75 KB) + [`.claude/research-results/gemini-2-bootstrap-context-engineering.md`](../.claude/research-results/gemini-2-bootstrap-context-engineering.md) (companion, 54 KB) — both of which survive the archive intact because `.claude/` is exempt; and (b) everything under `/migration/`. (Earlier drafts of this preface cited `research/gemini-architectural-audit-2/` — that path is not present in the repo; corrected via PR #129 review.)
- **The rebuild is a "complete and extreme refactoring".** Not incremental, not per-folder, not opt-in.
- **First operational step:** archive everything except `/migration/` and `/.claude/`. Use `git mv` (preserves history; renames track via `git log --follow`).
- **Trigger:** "when the refactoring plan is Ready" — interpret as **user explicitly authorises execution**. The plan being ready is necessary but not sufficient; the user's go-ahead is required.

---

## 2. Preconditions (all must hold before the task starts)

The next agent MUST verify each before issuing any `git mv` command.

- **P.1** Every open question in [`open-questions.md`](./open-questions.md) Q1–Q7 has a user-confirmed answer captured in [`locks-ratified.md`](./locks-ratified.md) (either in the main body or appended in `§Revision history`).
- **P.2** The three provisional answers (R1 / R2 / R3) in [`locks-ratified.md §Revision history`](./locks-ratified.md#revision-history--answers-given-mid-session-after-waiver-request) are re-confirmed by the user (single AskUserQuestion at session start per [`next-agent-report.md §6`](./next-agent-report.md#6-recommended-next-session-arc)).
- **P.3** The ADR draft in [`adr-draft.md`](./adr-draft.md) has been revised to reflect (a) L11.43 v3 scope (6 types, not tasks-only) and (b) the per-type natural-fit reversal. The user has reviewed the revised draft.
- **P.4** [`schemas-delta.md`](./schemas-delta.md) has been updated to reflect the Decision 4 reversal (uniform L2 `id:` field across the 5 promoted types).
- **P.5** The user issues an **explicit, unambiguous instruction** to execute this task. The instruction MUST name "archive" or "git mv" or this task's slug. Implicit cues (e.g. "let's start") are **not** sufficient.
- **P.6 — No staged/unstaged tracked changes outside `/migration/`.** `git status --porcelain | grep -v '^?? ' | grep -v '^.. migration/'` MUST produce empty output. Untracked root-level entries (status `??`) are permitted at this precondition — they are adjudicated explicitly in §5 step 4's untracked-leftovers branch. Staged or unstaged changes (`M`, `A`, `D`, `R`, etc.) on tracked paths outside `/migration/` are NOT permitted — they would silently corrupt the move-set built in step 4 (where `git ls-files` reflects the index, including staged changes the operator may not have intended to archive). If P.6 fails, surface the dirty paths to the user and ask them to commit, stash, or discard before re-running.

**If any precondition is unmet, the agent MUST NOT begin the archive.** Surface the unmet precondition to the user and ask for resolution. Do not proceed on the basis of "good enough" precondition coverage.

---

## 3. Exempt paths (DO NOT move)

Turn-14 user directive (verbatim, in [`original-prompt.md`](./original-prompt.md)): *"archiving (git mv) of every file except the Migration folder - and the .claude folder."*

Therefore **only two paths are unconditionally exempt** by user directive:

| Path | Reason |
|---|---|
| `migration/` | Named by user. The plan-of-record; must remain live for the rebuild to consult. |
| `.claude/` | Named by user. Plugin / session-state directory; carries the SuperClaude + Superpowers skill manifests, hook registrations, and (critically) the authoritative Gemini Deep Research briefs at `.claude/research-results/gemini-{1,2}-*.md` that anchor the D1–D8 evidence chain in [`gemini-evidence.md`](./gemini-evidence.md). |

**Technical-necessity exceptions** (not files; not user-adjudicable):

| Path | Reason |
|---|---|
| `.git/` | Git infrastructure. Moving it would break the repo entirely. Not a "file" in the directive's sense. |
| `archive/` | Target folder being created by this task. Cannot move a folder into itself. Created fresh; if it already exists from a prior partial run, abort and reconcile (§6 R.3). |

**Borderline cases — every entry below MUST be adjudicated by the user via a single `AskUserQuestion` before any `git mv` runs.** None are unconditionally exempt; the user explicitly chooses keep-live vs. archive for each:

| Path | Default recommendation | Rationale |
|---|---|---|
| `.githooks/` | **keep live** (recommended) | Pre-commit hook directory. While governance is revoked the hook is a no-op via `--no-verify`, but the script MUST exist post-rebuild for governance restoration. User MAY override. |
| `.gitignore` | **keep live** (recommended) | Repo-level ignore patterns. Move only if the rebuild explicitly redefines them. User MAY override. |
| `LICENSE` / `LICENSE.md` (if present) | **keep live** (recommended) | Preserves repo licensing throughout the rebuild. User MAY override. |
| `.editorconfig`, `.gitattributes`, other dotfiles | **keep live** (recommended) | Editor / git-attribute config. User MAY override per-file. |
| `install.sh` (if present at root) | **archive** (recommended) | Post-rebuild bootstrap will be reauthored from the migration plan. User MAY override. |

**Authority-chain note.** The Gemini briefs at `.claude/research-results/` (anchoring D1–D8) survive the archive intact because `.claude/` is unconditionally exempt. Any *other* `research/` workspaces (e.g. `research/adr-assumption-audit/`, `research/gemini/`) move into `archive/research/` and become **non-binding** historical context per §4 Scenario "Rebuild proceeds from /migration/". If a rebuild task needs an archived research workspace as a binding input, it MUST first promote that workspace's relevant artefacts into `/migration/` (or a fresh live folder) via a documented amendment to this task spec — not by silently consulting `archive/`.

---

## 4. Plan (Gherkin acceptance criteria)

```gherkin
Feature: Big-bang archive of pre-migration repo state

  Scenario: Every non-exempt entry moves to /archive/
    Given the preconditions in §2 all hold
    And the user has explicitly authorised execution
    And the §3 borderlines have been adjudicated
    When the archive task runs
    Then every top-level entry in the repo root except those listed in §3 (unconditional exempts + technical exceptions + user-kept borderlines) is moved into /archive/<original-path>/
    And the move uses `git mv <source> <destination>` for each entry (or recursively for directories)
    And `git status --porcelain` shows every moved file with status code `R` (rename), not as `D` (delete) + `A` (add)
    And the count of `R` lines in `git status --porcelain` equals the total file count (recursive) of the to-be-moved set

  Scenario: Exempt paths survive unchanged at the archive-commit boundary
    Given the archive commit (§5 step 8) has just been authored
    Then /migration/ is byte-for-byte identical to its pre-task state at that commit
    And /.claude/ is byte-for-byte identical to its pre-task state at that commit
    And the Gemini briefs at .claude/research-results/gemini-1-architecture-audit.md and .claude/research-results/gemini-2-bootstrap-context-engineering.md are unmoved at that commit
    And /.git/ and /archive/ are intact at that commit
    And every user-elected keep-live borderline path (§3) is unmoved at that commit
    # Post-archive followup commits (§5 step 10) explicitly add post-archive prose to /migration/handover.md;
    # those changes land AFTER the archive commit and are out of scope for this Scenario's byte-identity test.

  Scenario: History is traversable across the move
    Given the archive task has completed
    When `git log --follow archive/tasks/039-maintenance-spec-integration/task.md` runs (one concrete file path as the example; `--follow` works only for individual files, not directories)
    Then the log shows the complete pre-archive history of that file
    And the rename event is visible at the top of the log
    And the same property holds for any other individually-named archived file path

  Scenario: Live tree is empty except for migration and .claude
    Given the archive task has completed
    When `ls -A` runs in the repo root
    Then the output contains exactly: migration, .claude, .git, archive, plus every §3-borderline path the user opted to keep live
    And no other entries exist at the repo root

  Scenario: Rebuild proceeds from /migration/
    Given the archive task has completed
    When the rebuild task starts
    Then it consults /migration/handover.md as the canonical plan-of-record
    And it does not consult any file in /archive/ as a binding rule
    And it may consult /archive/ for historical context only (read-only)

  Scenario: Governance remains revoked throughout
    Given the archive task is in progress
    Then tools/check-governance.sh exit code is ignored (see migration/waiver.md)
    And every commit uses git commit --no-verify with the waiver cited
    And the agent does not stop on any pre-existing baseline failure
```

---

## 5. Step-by-step execution sequence

When the task triggers, the agent executes:

1. **Verify preconditions §2.1–§2.6.** If any fails, halt and report to user.
2. **Filesystem + git state preflight (mitigates R.1, R.2, R.3, R.3a).** Run each check, halt on any check that fails:
    - **`archive/` must NOT exist.** Test: `! test -e archive`. The shell-portable form is an explicit `if [ -e archive ]; then echo 'HALT: archive/ exists; reconcile before run'; exit 1; fi`. If `archive/` exists at all (whether populated, empty, tracked, untracked, or partial from a prior interrupted run), halt and reconcile with the user. **Do not** rely on `git ls-tree HEAD archive/ | wc -l` — that only inspects the committed tree and misses working-tree-only content. Existence-based filesystem check is the correct semantic.
    - **Submodules must be absent.** Test: `[ -z "$(git submodule status)" ]`. The shell-portable form is `if [ -n "$(git submodule status)" ]; then echo 'HALT: submodules present; per-submodule guidance required'; exit 1; fi`. `git mv` on a submodule path may misbehave; the user MUST guide the per-submodule strategy before proceeding.
    - **No staged/unstaged tracked changes outside `/migration/`.** Test: `[ -z "$(git status --porcelain | grep -v '^?? ' | grep -v '^.. migration/')" ]`. The shell-portable form is `dirty="$(git status --porcelain | grep -v '^?? ' | grep -v '^.. migration/')"; if [ -n "$dirty" ]; then echo "HALT: dirty tree outside /migration/:\n$dirty"; exit 1; fi`. (This enforces P.6 operationally.) Untracked entries (`??`) are explicitly permitted here — they're adjudicated in step 4.
3. **Adjudicate §3 borderlines** via a single `AskUserQuestion` covering `install.sh`, `LICENSE`, `.editorconfig`, `.githooks/`, `.gitignore`, and any other dotfiles present at root.
4. **Snapshot the to-be-moved set — only Git-controlled root entries from the index, not just HEAD:**
    - `git ls-files -- ':(top)*' | awk -F/ '{print $1}' | sort -u` gives the canonical list of top-level entries tracked in the **index** (includes staged-but-not-committed paths; `git ls-tree HEAD` alone would miss those). Filter against §3 to get the move-set; this is the input to step 6.
    - Separately, `(ls -A ; git ls-files -- ':(top)*' | awk -F/ '{print $1}' | sort -u) | sort | uniq -u | grep -vFf <(printf '%s\n' "${EXEMPTS[@]}")` yields the **untracked-leftovers** set (entries in `ls -A` that aren't in the index and aren't §3-exempt). `git mv` cannot move untracked entries (it requires tracked sources), so untracked files must be handled explicitly. **Leave-in-place is NOT a permitted option** at this step — it would violate the §4 acceptance criterion "Live tree is empty except for migration and .claude". Any untracked file the user wants to keep live MUST first be added to the §3 borderline-keep-live list and re-adjudicated there; only then does it become exempt and skip this step.
    - For each non-exempt untracked entry, the user picks one of three options:
      - **`git add` then archive** (default; preserves the artefact in history). Use `git add -f <entry>` for entries matched by `.gitignore` — plain `git add` refuses ignored paths and would halt the run.
      - **`mv` aside** — filesystem-move to a temporary location outside the repo. Use when the artefact should not enter git history at all.
      - **`rm`** — delete. Use when the artefact is generated junk.
    - Surface both lists to the user before executing (one final go/no-go for the tracked-move-set + per-file adjudication for any untracked-leftovers).
5. **Create `/archive/`** if not present: `mkdir archive`. (Step 2 already verified it was absent or only-empty.)
6. **For each entry in the tracked move-set:** `git mv <entry> archive/<entry>`. Mirror the original path inside `/archive/`. For untracked-leftover entries adjudicated as "archive" in step 4, run `git add <entry>` (or `git add -f <entry>` for ignored entries) first, then `git mv <entry> archive/<entry>`.
7. **Verify renames:** the file-level rename count from `git status --porcelain | grep -c '^R'` equals the recursive file count of the to-be-moved set (computed via e.g. `git diff --cached --name-status --find-renames | grep -c '^R'` for staged moves, or `find <moved-path> -type f | wc -l` on the source set before the move). **Do not** use `git status` without `--porcelain` — the long human-readable format prints `renamed:` lines, not `R` codes, so `grep '^R'` returns zero matches even on successful moves. **Do not** compare against the count of top-level entries — `git mv tasks/` expands to one rename per file inside `tasks/`, not one rename total.
8. **Commit:** the body MUST cite `migration/waiver.md`, list the moved top-level entries, and include `Highest Frustration Level: FL[0-3]`. A single `-m` produces a subject-only commit and silently drops these mandatory fields, so use a HEREDOC pattern (or multiple `-m` flags) to deliver subject + body in one invocation:

    ```bash
    git commit --no-verify -m "$(cat <<'EOF'
    archive: big-bang move of pre-migration repo state into /archive/

    Moved top-level entries (verbatim list from §5 step 4 tracked move-set):
    - tasks/
    - prompts/
    - research/
    - skills/
    - decisions/
    - tools/
    - maintenance/
    - templates/
    - Agency-System/
    - AGENTS.md, CLAUDE.md, TASK.md, PROMPT.md, RESEARCH.md, SKILLS.md,
      FOLDERS.md, PRE_COMMIT.md, FRUSTRATED.md, MAINTENANCE.md
    - README.md
    - <plus any borderline paths the user adjudicated as "archive">

    Untracked-leftover handling: <enumerate per-file decisions from §5
    step 4 untracked branch, e.g. "added .env-example via git add -f
    then archived; rm'd .DS_Store; mv'd /tmp/scratch.txt out of repo">

    Waiver: migration/waiver.md (governance suspended during refactor —
    turn 13). Authority chain: .claude/research-results/gemini-{1,2}-*.md
    survive the archive (.claude/ exempt) so D1–D8 evidence remains
    reachable for the rebuild.

    Highest Frustration Level: FL[0-3]
    EOF
    )"
    ```

    Verify the commit body landed before pushing: `git log -1 --format=%B | head -30` should show subject + body + waiver citation + FL line.
9. **Push** to the migration branch.
10. **Post-archive followup (separate commit; explicitly OUTSIDE the §4 exempt-paths-survive Scenario which applies only at step 8's commit boundary):** edit `migration/handover.md` to add a "post-archive" section indicating the new state. Commit + push as a separate followup commit. This step intentionally violates the byte-identity property of `/migration/`; that property is point-in-time at the archive commit (step 8) only.
11. **Open a PR** (if not already open) or update the existing PR description to reflect the archive milestone.

---

## 6. Risks and mitigations

- **R.1 — Path collisions inside `/archive/`.** If a prior partial migration left `/archive/<some-path>/` in place (committed, staged, or only in the working tree), `git mv <path>/foo archive/<path>/foo` may fail or merge unexpectedly. **Mitigation:** §5 **step 2** runs a filesystem-level `test -e archive` plus a non-empty content check — NOT just `git ls-tree HEAD archive/`, which would miss working-tree-only `archive/` content from an interrupted prior run.
- **R.2 — Submodules.** If any submodules exist, `git mv` on a submodule path may misbehave. **Mitigation:** §5 **step 2** runs `git submodule status`; if non-empty, the agent halts and surfaces the list for per-submodule user guidance.
- **R.3 — Pre-existing `/archive/` from L11.43's original archive-first big-bang language.** The plan-recap (Roundtable 7) anticipated this; check whether prior commits already populated `/archive/`. **Mitigation:** as R.1 — same step-2 filesystem check covers it.
- **R.3a — Staged-but-not-committed root entries silently excluded.** If the operator starts the archive run with staged tracked root entries that aren't in `HEAD`, naïve `git ls-tree HEAD --name-only` would miss them and they'd remain live at root, violating §4 acceptance. **Mitigation:** P.6 + §5 **step 2** require a clean working tree before run; §5 **step 4** uses `git ls-files` (which reflects the index) instead of `git ls-tree HEAD`.
- **R.4 — `.claude/` may legitimately need updating during the rebuild** (e.g. hook registrations point at archived `tools/hooks/` paths). **Mitigation:** rebuild task (not this one) handles `.claude/` updates. This task leaves `.claude/` strictly untouched.
- **R.5 — Governance scripts (`tools/check-governance.sh`, `tools/fm/`) move to `/archive/`, breaking any agent that tries to run them post-archive.** **Mitigation:** governance is revoked per the waiver; no agent should run those scripts during the refactor window. The next agent's banner-mandated workflow does not require them.
- **R.6 — Branch hygiene.** This task ideally lands on the migration branch (`claude/repo-refactoring-plan-CfLY5` or a successor) and ships as one or more commits in PR #129 (or its successor). Do NOT execute the archive on a feature branch that has already been merged or that diverges from the migration plan.
- **R.7 — User's "Save this as mandatory Next Task" instruction is captured here, NOT in `/tasks/<NNN>-archive-pre-migration-tree/task.md`.** Reason: `/tasks/` is part of the to-be-archived set; placing the task spec there means it gets archived before it can execute. The task spec lives in `/migration/` and survives the archive operation.

---

## 7. Post-archive state

After the task completes, the repo's live tree contains:

```
agency/
├── migration/              # plan-of-record; unchanged
├── .claude/                # plugin / session state; unchanged
├── .git/                   # never touched
├── .githooks/              # pre-commit hook; gate is no-op until governance restored
├── .gitignore              # if kept per §3
├── LICENSE / similar       # if kept per §3
└── archive/
    ├── tasks/              # all 95+ pre-migration tasks
    ├── prompts/            # all pre-migration prompts
    ├── research/           # all pre-migration research workspaces
    ├── skills/             # all 54 SuperClaude + Superpowers skills
    ├── decisions/          # all 12 pre-migration ADRs + locks/ if present
    ├── tools/              # all linters, agency CLI, hooks, dramatica-nav, etc.
    ├── maintenance/        # schemas, run-log, narrative-ontology
    ├── templates/          # task / prompt / research / readme / skill skeletons
    ├── Agency-System/      # frontend prototype
    ├── AGENTS.md, CLAUDE.md, TASK.md, PROMPT.md, …  # root specs
    ├── README.md           # repo readme
    └── install.sh          # if user opts to archive per §3 adjudication
```

The next phase ("rebuild") starts from `/migration/handover.md` and writes net-new artifacts directly into the live tree — `tasks/`, `prompts/`, `decisions/`, etc. get re-created from scratch under the post-refactor conventions (12-type ontology, 6-type ULID, auto-generated readmes, three placement modes).

---

## 8. Out of scope (separate tasks, NOT this one)

- **Rebuild itself.** This task only moves things. The rebuild is a successor task or sequence of tasks, driven by `/migration/handover.md` + the ratified `/migration/adr-draft.md`.
- **Restoring governance.** The waiver remains in force until the user explicitly retracts it (see [`waiver.md §5`](./waiver.md)).
- **Updating banners after archive.** The CLAUDE.md and AGENTS.md banners themselves move into `/archive/`. Whether the rebuild reauthors them or restores them from archive is a rebuild-phase decision, not this task's.
- **Deleting `/archive/` at any future point.** Archive is permanent unless the user explicitly authorises pruning.

---

## 9. Cross-references

- **Predecessor reading (mandatory before executing this task):**
  - [`handover.md`](./handover.md) — operational summary.
  - [`next-agent-report.md`](./next-agent-report.md) — deep reflection on revision patterns and inherited risks.
  - [`locks-ratified.md`](./locks-ratified.md) **including §Revision history** — the 11 binding decisions.
  - [`open-questions.md`](./open-questions.md) — what's blocking ratification.
- **Authorisation chain:**
  - [`waiver.md`](./waiver.md) — governance revoked for the refactor window.
  - [`original-prompt.md`](./original-prompt.md) — verbatim user instructions; turn 13 + this task's source.
- **Successor tasks (post-archive):**
  - Rebuild Task #1 — scaffold the new operational tree from migration plan.
  - Rebuild Task #2 — author ADR-0013 in the live `/decisions/` and synthesise to AGENTS.md.
  - Rebuild Task #3 — port research artefacts that the new design retains.
  - Rebuild Task #N — restore governance (retract waiver; re-enable `tools/check-governance.sh` gate).

## Assumptions Log

- **Assumption NT1.** "All content of the repo - including the ADRs - are revoked" means the existing 12 ADRs in `decisions/` are no longer binding, NOT that they cease to exist as artifacts. They move into `/archive/decisions/` and remain queryable for historical / evidence purposes. *Status: implied by "archive" framing; not explicitly user-confirmed.*
- **Assumption NT2.** The user's "save this as mandatory Next Task" instruction does not require this task to be authored in the legacy `/tasks/<NNN>-<slug>/` shape. The pre-migration task convention is itself revoked; the migration workspace is the right home. *Status: implied; consistent with §6 R.7.*
- **Assumption NT3.** Submodules are absent from the repo. *Status: unverified; the agent MUST run `git submodule status` at §5 step 1 before relying on this.*
- **Assumption NT4.** `.gitignore` survives the archive. The current `.gitignore` may reference paths that move into `/archive/`; those references become broken but harmless. The rebuild reauthors `.gitignore` if needed. *Status: §3 default; user MAY override.*
- **Assumption NT5.** The branch landing this task is `claude/repo-refactoring-plan-CfLY5` or a successor designated by the user. Executing on `main` is forbidden. *Status: implicit in CLAUDE.md §11 / AGENTS.md branch discipline; not separately ratified for this task.*
