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

- **All current repo content — including the 12 existing ADRs — is revoked.** Nothing in the live tree is binding any longer. The Gemini research briefs (`research/gemini-architectural-audit-2/` and friends) plus everything under `/migration/` are the only authoritative sources for the rebuild.
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

**If any precondition is unmet, the agent MUST NOT begin the archive.** Surface the unmet precondition to the user and ask for resolution. Do not proceed on the basis of "good enough" precondition coverage.

---

## 3. Exempt paths (DO NOT move)

The following top-level entries MUST remain in place; everything else in the repo root moves into `/archive/`:

| Path | Reason |
|---|---|
| `migration/` | The plan-of-record. Must remain live for the rebuild to consult. |
| `.claude/` | Plugin / session-state directory; carries the SuperClaude + Superpowers skill manifests and hook registrations. Removing it breaks the agent's runtime. |
| `.git/` | Git infrastructure. **Never** move. |
| `.githooks/` | Pre-commit hook directory; while governance is revoked the hook is a no-op via `--no-verify`, but the script itself MUST stay in place so the post-rebuild restoration of governance has something to point at. |
| `archive/` | Target folder; created by this task. If it already exists from a prior partial migration, abort and reconcile before proceeding (see §6 R.3). |
| `.gitignore` | Repository-level ignore patterns; needed for the rebuild to function predictably. Move into archive only if the rebuild explicitly redefines it. |

**Borderline cases requiring user adjudication before this task starts:**

- `.gitignore` — recommend keep in place; user MAY override.
- `LICENSE` / `LICENSE.md` (if present) — recommend keep in place to preserve repo licensing throughout the rebuild.
- `.editorconfig`, `.gitattributes`, similar dotfiles — recommend keep in place; user MAY override per-file.
- `install.sh` — currently at repo root; the bootstrap script. Recommend **move into archive** because the post-rebuild bootstrap will be reauthored from the migration plan. The user MAY override.

The next agent MUST surface these borderlines via `AskUserQuestion` before issuing any `git mv`.

---

## 4. Plan (Gherkin acceptance criteria)

```gherkin
Feature: Big-bang archive of pre-migration repo state

  Scenario: Every non-exempt entry moves to /archive/
    Given the preconditions in §2 all hold
    And the user has explicitly authorised execution
    When the archive task runs
    Then every top-level entry in the repo root except those listed in §3 is moved into /archive/<original-path>/
    And the move uses `git mv <source> <destination>` for each entry
    And `git status` shows all moves as `R` (rename), not as `D` (delete) + `A` (add)

  Scenario: Exempt paths survive unchanged
    Given the archive task has completed
    Then /migration/ is byte-for-byte identical to its pre-task state
    And /.claude/ is byte-for-byte identical to its pre-task state
    And /.git/, /.githooks/, /archive/ are intact

  Scenario: History is traversable across the move
    Given the archive task has completed
    When `git log --follow archive/<some-original-path>` runs
    Then the log shows the complete pre-archive history of that file
    And the rename event is visible at the top of the log

  Scenario: Live tree is empty except for migration and .claude
    Given the archive task has completed
    When `ls -A` runs in the repo root
    Then the output contains exactly: migration, .claude, .git, .githooks, archive, plus any §3-borderline paths the user opted to keep live

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

1. **Verify preconditions §2.1–§2.5.** If any fails, halt and report to user.
2. **Adjudicate §3 borderlines** via a single `AskUserQuestion` covering `install.sh`, `LICENSE`, `.editorconfig`, and any other dotfiles present at root.
3. **Snapshot the to-be-moved set** — `ls -A` filtered against §3. Confirm the list to the user before executing (one final go/no-go).
4. **Create `/archive/`** if not present: `mkdir archive`.
5. **For each entry in the to-be-moved set:** `git mv <entry> archive/<entry>`. Mirror the original path inside `/archive/`.
6. **Verify renames:** `git status | grep '^R'` count equals the to-be-moved set size.
7. **Commit:** `git commit --no-verify -m "archive: big-bang move of pre-migration repo state into /archive/"`. Body MUST cite `migration/waiver.md`, list the moved top-level entries, and include `Highest Frustration Level: FL[0-3]`.
8. **Push** to the migration branch.
9. **Update [`handover.md`](./handover.md)** with a "post-archive" section indicating the new state. Commit + push as a separate commit.
10. **Open a PR** (if not already open) or update the existing PR description to reflect the archive milestone.

---

## 6. Risks and mitigations

- **R.1 — Path collisions inside `/archive/`.** If a prior partial migration left `/archive/<some-path>/` in place, `git mv <path>/foo archive/<path>/foo` may fail or merge unexpectedly. **Mitigation:** §5 step 1 includes a check `git ls-tree HEAD archive/ | wc -l` to detect prior archive contents. Abort and reconcile with the user before proceeding.
- **R.2 — Submodules.** If any submodules exist, `git mv` on a submodule path may misbehave. **Mitigation:** `git submodule status` runs in §5 step 1; if submodules present, the agent halts and asks for guidance.
- **R.3 — Pre-existing `/archive/` from L11.43's original archive-first big-bang language.** The plan-recap (Roundtable 7) anticipated this; check whether prior commits already populated `/archive/`. **Mitigation:** as R.1.
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
