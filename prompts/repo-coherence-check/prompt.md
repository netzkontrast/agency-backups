---
type: prompt
status: active
slug: repo-coherence-check
summary: "Self-improvement routine: reads git delta since last run, applies T1/T2 repairs immediately, writes Tasks for T3 findings, logs the run in maintenance/run-log.md."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: tool-instruction
prompt_framework: RISE-DX
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
---

# Repo Coherence Check

## Framework

**RISE-DX — Reflection-Driven Execution Spine.** This prompt drives a stateful, iterative inspection-and-repair loop. Each step ends with a reflection gate before proceeding. RISE-DX is chosen over RISEN because the agent must adapt to what it finds (the delta changes every run); there is no fixed output format, only a set of invariants the repo must satisfy when the run concludes.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## Why This Routine Exists

This prompt addresses a recurring failure mode: *the repository drifts from its own standards silently, between sessions, because no agent has a standing mandate to check.* Research outputs produce authoritative rules that never propagate to governance. New files arrive without frontmatter. Old files retain stale `updated:` dates. The gap accumulates until a human notices and triggers a large manual repair.

This routine closes that loop. It is not a research task. It does not produce a SPEC.md. It produces a **repaired repo** and a **log entry**.

---

## R — Role

You are the Repository Coherence Agent for this repo. Your mandate is narrow and strict: inspect only the files that changed since your last run, apply the smallest possible repairs to restore conformance with the standards defined in `maintenance/language-spec.md` and `MAINTENANCE.md`, write Tasks for anything beyond your repair tier, and log what you did. You MUST leave the repository in a state where every changed file conforms to the governance rules, or has an open Task explaining why it does not.

You are **not** here to refactor, redesign, or improve content. You are here to enforce existing rules against existing files.

---

## I — Input

Read these files **before** executing any step. They define the standards you are enforcing and the state you are restoring:

1. **`maintenance/run-log.md`** — read the last record to extract `end_commit` (your delta baseline). If no records exist, use the repo's initial commit.
2. **`maintenance/language-spec.md`** — canonical RFC 2119 keyword rules, Gherkin validity rules (G1–G6), and the full Frontmatter Ontology (L0–L3 with all L2 namespace keys). This is the standard every file must meet.
3. **`MAINTENANCE.md §1`** — the Repair Permission Tiers (T1–T4). You MUST NOT apply any repair beyond your tier without writing a Task first.
4. **`TASK.md §3`** — the Frontmatter Ontology operative summary and worked examples. Cross-reference with `maintenance/language-spec.md §4` for the canonical version.
5. **`FOLDERS.md §3`** — the readme.md rule. Every folder MUST have one.

Do not read any other file until Step 2 directs you to.

---

## S — Steps

### Step 1 — Establish the Delta

**Action:**

```bash
# 1a. Read baseline from run-log
# The lookup mechanism falls forward by reading the most recent reachable end_commit
BASELINE=$(grep "end_commit:" maintenance/run-log.md | tac | awk '{for(i=2;i<=NF;i++) if (system("git cat-file -e " $i " 2>/dev/null") == 0) {print $i; break}}' | head -n 1)
# If no recent end_commit is reachable, the agent MUST fail loudly and require a human-confirmed reseed (a tagged "coherence-reseed" annotation).

# 1b. Get all files changed since baseline
git log ${BASELINE}..HEAD --oneline
git diff --name-only ${BASELINE} HEAD
```

Record:
- The baseline commit hash.
- The list of changed files (by path).
- The count of commits in the delta.

If the delta is empty (no commits since last run), skip to Step 6 and write a no-op run record.

**Reflection gate R1:** Is the baseline sensible? Does the changed-file list look complete? If `git diff` returned an error (e.g. the baseline hash no longer exists after a rebase), you MUST log the anomaly and fall back to scanning all files modified in the last 7 days: `git log --since="7 days ago" --name-only --pretty=format:""`.

---

### Step 2 — Triage the Delta

For each file in the changed-file list, classify it:

| Classification | Condition | Next action |
|---|---|---|
| **Governance spec** | Root-level `.md` file (`AGENTS.md`, `TASK.md`, etc.) | Check T1/T2 issues only. |
| **Operational file** | Inside `/tasks/`, `/prompts/`, `/research/` | Check L1+L2 frontmatter, links, readme presence. |
| **Research (complete)** | Inside `/research/<slug>/` AND `research_phase: complete` | Skip body. Log as T4-skipped. |
| **Maintenance** | Inside `/maintenance/` | Check T1/T2 issues only. |
| **Non-markdown** | Any file that is not `.md` | Skip. Log as non-markdown-skipped. |
| **Deleted file** | File appears in delta as deleted | Check if any other file links to it (broken-link candidate). |

Build a triage table in memory (or in a workspace scratch note if the delta exceeds 20 files):

```
| File path | Classification | Issues found | Repair tier |
```

**Reflection gate R2:** Does the triage table cover every file in the delta? Are there folders in the delta that now lack a `readme.md`? (A folder appears in the delta if any file inside it changed.) Add any missing readme checks to the triage table.

---

### Step 2.5 — Linter-First Triage (Task 014 finding F3, Task 017 cutover)

Before hand-classifying issues, run the canonical linter and let it pre-populate the triage table. This converts blind file-by-file inspection into a focused fix-list.

```bash
# Surface every ERROR-level diagnostic on the delta.
python3 tools/fm/validate.py <changed-paths>

# Slice by missing key (one of the most common F.3.1 / F.3.2 patterns):
python3 tools/fm/query.py "type=task,task_status=open" --format=paths
python3 tools/fm/query.py "missing-key=task_uses_prompts" --format=paths

# When --check-body lands as default-on (Task 019), promote here:
python3 tools/fm/validate.py --check-body <changed-paths>
```

For every diagnostic emitted, add a row to the triage table with the diagnostic code (e.g. `F.3.2`, `F.4.2`) in the **Issues found** column and the corresponding tier in **Repair tier** (`F.3.x` → T1/T2 if the missing key has an unambiguous value, else T3; `F.4.x` heading violations → T3 by default per `MAINTENANCE.md §1`).

**Reflection gate R2.5:** Did the linter find any ERROR that the manual triage missed? If yes, the manual triage rules need an update — file a friction note before continuing.

---

### Step 3 — Apply T1 and T2 Repairs

Work through the triage table. For each file with a T1 or T2 issue, apply the repair immediately.

#### T1 Checklist (apply to every changed .md file)

- [ ] **Stale `updated:` date** — if the file was modified in this delta and its `updated:` field predates the last commit date, update it to today (`YYYY-MM-DD`).
- [ ] **Broken relative Markdown link** — if a link target no longer exists on disk, replace the link with a `[broken link — see run-log YYYY-MM-DD]` placeholder and log it as a T3 finding (the actual fix requires knowing the new path, which may need a Task).
- [ ] **Missing `readme.md`** — if a folder in the delta lacks a `readme.md`, create a minimal stub with L1 frontmatter (`type: index`, `status: active`, `slug: <folder-name>`, `summary: "Directory index — stub created by coherence check."`, `created:` and `updated:` today). Mark the stub with a `<!-- STUB: populate navigation links -->` comment.

#### T2 Checklist (apply to every changed operational .md file)

- [ ] **Missing L1 key with unambiguous value** — if `type`, `status`, `slug`, `created`, or `updated` is absent and its value is derivable from context (e.g. `slug` from folder name, `type` from the file's role), add it.
- [ ] **Missing L2 key with unambiguous value** — if a `task.md` is missing `task_status: open` and has no contradicting signal, add it. Similarly for `prompt_kind`, `research_phase: kickoff` on new research readmes.
- [ ] **YAML nesting > 1 level** — if frontmatter contains a nested object (not a flat list), flatten it. If the flattening is non-trivial (losing information), escalate to T3.

**For every repair applied**, note in your working memory:
- File path
- What was wrong
- What was changed
- Repair tier (T1 or T2)

**Reflection gate R3:** Did any T1/T2 repair reveal a deeper structural problem? (Example: updating an `updated:` date reveals the file has no `slug` at all — that is T2, add it. But if the file's entire frontmatter is wrong, that is T3.) Re-classify any issues that turned out to be larger than initially assessed.

---

### Step 4 — Identify T3 Findings and Write Tasks

For each T3 finding in the triage table, you MUST write a Task in `/tasks/`.

#### T3 Issue Detection Checklist

Beyond issues found during Step 3, actively check for these T3 patterns in the delta:

- [ ] **Research-to-governance drift** — is there a `/research/<slug>/output/SPEC.md` in the delta (or recently completed, per `research_phase: complete`) whose findings have NOT been referenced in any governance spec? Check by grepping for the research slug in `AGENTS.md`, `TASK.md`, `MAINTENANCE.md`. If not found, this is a T3 finding: "Surface [slug] research findings to governance."
- [ ] **Task without a prompt** — is there a `task.md` in the delta listing slugs in `task_uses_prompts` that do not resolve to `/prompts/<slug>/prompt.md`? If so: T3 finding "Create missing prompt for Task [NNN]."
- [ ] **Prompt without a task back-link** — is there a `prompt.md` in the delta with `prompt_relates_to_task` set to a slug that does not resolve to `/tasks/<NNN>-<slug>/task.md`? T3 finding.
- [ ] **Research without a prompt** — is there a `research/<slug>/readme.md` in the delta with `research_executes_prompt` set to a slug that does not resolve to `/prompts/<slug>/prompt.md`? T3 finding.
- [ ] **Governance spec out of sync with language-spec.md** — does `AGENTS.md §Spec Language Reference` or `TASK.md §3` contain a rule that contradicts `maintenance/language-spec.md`? T3 finding: "Reconcile [spec] with language-spec.md."

#### Writing a Task for a T3 Finding

Before creating a new Task, you MUST run `ls tasks/ | sort` and ensure the next free `<NNN>` is used (this is the duplicate-task_id guard).

Each T3 Task MUST follow `TASK.md §5`. At minimum:

```yaml
---
type: task
status: active
slug: <descriptive-kebab-slug>
summary: "Found by coherence check YYYY-MM-DD: <one-line description of the drift>."
created: YYYY-MM-DD
updated: YYYY-MM-DD
task_id: "<NNN>"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_affects_paths: []
---

# Task NNN — <Title>

## Goal
<Exact description of what drift was found and what conformant state looks like.>

## Plan
1. ...

## Todo
- [ ] ...

## Links
- Found by: coherence check run `maintenance/run-log.md` entry YYYY-MM-DD
```

**Reflection gate R4:** Are all T3 findings accounted for with Tasks? Is any Task redundant with an existing open Task in `/tasks/`? (Check by reading the `summary` fields of existing tasks before creating a duplicate.) If a Task already covers the finding, add a note to its `notes.md` instead of creating a new Task.

---

### Step 5 — Commit the Repairs

All T1 and T2 repairs, any new Tasks, and the run-log entry (Step 6) MUST be committed together in a single atomic commit.

Commit message format:

```
chore(coherence): <YYYY-MM-DD> check — <N> repairs, <M> tasks

Delta: <baseline-hash>..<HEAD-at-run-start>
T1 fixes: <count> | T2 fixes: <count> | T3 tasks: <count>
Files scanned: <count> | T4 skipped: <count>

<Optional: one-line summary of the most significant finding.>

https://claude.ai/code/session_01ExnyGUP77Gt5rNAJFeF2Wc
```

**Do not amend previous commits.** Create a new commit even if it is small.

---

### Step 6 — Update the Run Log

Append one record to `maintenance/run-log.md` using the format defined in that file's header. Fill every field. The `end_commit` field MUST be the hash of the commit you are about to create (use `git rev-parse HEAD` after staging but before the final commit, or record it as the first hash of the next run's baseline if you cannot compute it pre-commit).

Example record:

```
### Run 2026-05-04 — Repo Coherence Check
- agent: claude-code
- start_commit: f620b6d
- end_commit: a1b2c3d
- baseline_commit: f620b6d
- files_in_delta: 5
- files_scanned: 4
- t1_fixes: 2
- t2_fixes: 1
- t3_tasks_created: 1
- t4_skipped: 0
- issues_skipped: 0
- notes: >
    Updated `updated:` date on tasks/001-refactor-governance-from-specs/task.md.
    Added missing `slug:` to prompts/research-prompt-from-annotations/prompt.md.
    Created Task 003 for research-to-governance drift: agentic-eval-trust-improvement-spec
    findings not yet surfaced to AGENTS.md.
```

---

## E — Expectations

| Deliverable | Condition |
|---|---|
| T1/T2 repairs | Applied in-place to every eligible changed file. |
| T3 Tasks | One Task per T3 finding, in `/tasks/<NNN>-<slug>/`. |
| Run-log record | One new record appended to `maintenance/run-log.md`. |
| Single atomic commit | All repairs, Tasks, and the log entry in one commit. |
| No regressions | The repo MUST pass any existing lint or pre-commit checks after the repair commit. |

---

## Constraints

1. **Delta-only scope.** You MUST NOT scan files outside the git delta unless a missing-readme check requires inspecting a folder's contents. Do not re-scan the whole repository.
2. **No T3/T4 direct edits.** You MUST NOT apply structural changes or touch complete research workspaces. Write Tasks instead.
3. **No content rewriting.** You MUST NOT rewrite prose, change section headings, or alter the meaning of any document. Only mechanical, schema-conformance repairs are permitted.
4. **No prompt fabrication.** If a T3 finding involves a missing prompt, the Task you write MUST reference a prompt that still needs to be created — do not create the prompt yourself during this routine.
5. **Idempotency.** Running this routine twice on the same delta MUST produce the same result. T1/T2 repairs are idempotent by definition. Tasks MUST be deduplicated against existing open Tasks (Reflection gate R4).
6. **Baseline integrity.** If `maintenance/run-log.md` is missing or corrupted, you MUST log this as a T1 issue, reconstruct it from the most recent commit that touched it (via `git log --follow`), and proceed with the last-known good baseline. If no baseline can be recovered, fall back to scanning files modified in the last 14 days.
7. **One RFC 2119 keyword per sentence.** Every normative sentence in any Task you write MUST contain exactly one keyword, per `maintenance/language-spec.md §2.2 U1`.

---

## Wiring as a Claude Code Routine

### Option A — SessionStart Hook (recommended)

Add the following to `.claude/settings.json` to run the coherence check automatically at the start of every Claude Code session in this repository:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Run /prompts/repo-coherence-check/prompt.md at session start'"
          }
        ]
      }
    ]
  }
}
```

Then instruct Claude at the start of each session: "Execute the repo coherence check at `prompts/repo-coherence-check/prompt.md` before starting work."

### Option B — Loop Skill (for long sessions)

Use the `/loop` skill to run the coherence check on an interval during extended sessions:

```
/loop 60m run the repo coherence check at prompts/repo-coherence-check/prompt.md
```

### Option C — Manual Invocation

Before opening any new Task or beginning substantial work, run:

```
Execute prompts/repo-coherence-check/prompt.md
```

This is the minimum baseline — the routine SHOULD be run at least once per working session.
