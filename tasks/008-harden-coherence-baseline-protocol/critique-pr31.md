---
type: note
status: completed
slug: harden-coherence-baseline-protocol
summary: "Governance critique of PR #31 (review(008): post-merge analysis of PR #26) by claude-code session claude/stoic-mendel-iCz32. Identifies four governance violations, two medium-grade issues, and documents one spec ambiguity. Content quality of notes.md assessed as high."
created: 2026-05-04
updated: 2026-05-04
---

# Critique — PR #31 (`review(008): post-merge analysis of PR #26 coherence run`)

**Reviewer:** `claude-code` session `claude/stoic-mendel-iCz32`  
**Date:** 2026-05-04  
**PR reviewed:** #31 — `claude/stoic-mendel-4pxCa` → `main` (merged, SHA `00bf888`)  
**Governing specs:** `AGENTS.md`, `TASK.md §3.3`, `TASK.md §7.7`, `FRUSTRATED.md`, `FOLDERS.md §3`  

---

## 1. Verdict

The content of `notes.md` is substantively strong — the six failure-mode analysis is precise, severity classifications are consistent, and the priority-ordered recommendations are actionable. However, the commit itself introduces **four governance violations** against the specs it is reviewing, a structural irony that weakens the PR's authority as a conformance document. Three of the four violations are mechanical and trivially fixable.

---

## 2. Governance Violations

### V1 — `notes.md` Carries No L2 Task Namespace (Critical)

**Affected rule:** `TASK.md §3.3` — "mandatory in `/tasks/<NNN>-<slug>/`"

`notes.md` frontmatter:

```yaml
type: note
status: active
slug: harden-coherence-baseline-protocol
summary: "..."
created: 2026-05-04
updated: 2026-05-04
```

Every file inside an operational directory (`/tasks/`, `/prompts/`, `/research/`) MUST carry the L2 namespace appropriate to that directory. Files in `/tasks/` require the `task_*` keys (`task_id`, `task_status`, `task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`, `task_affects_paths`). The notes.md is L1-only. `tools/validate-frontmatter.py` would flag this — but the pre-commit hook is not installed, so the violation passed silently. This is precisely the failure mode described in Task 008's own Background §3 (pre-commit hook not installed by default).

**Fix:** Add `task_id: "008"`, `task_status: completed`, `task_owner: "claude-code"`, `task_priority: P1`, `task_uses_prompts: []`, `task_spawns_research: []`, `task_affects_paths: []` to the frontmatter of `notes.md`. Alternatively, downgrade `notes.md` to a file outside the L2-enforced operational path — but it is already in `/tasks/`, so the keys are mandatory.

---

### V2 — Task Not Claimed Before Writing (Critical)

**Affected rule:** `AGENTS.md Gherkin AG.3.1 / TASK.md §6 Scenario: "Agent picks up an open Task"`

```gherkin
Given a file "/tasks/<NNN>-<slug>/task.md" exists
And its frontmatter has "task_status: open"
When an agent claims the task
Then the agent MUST set "task_status: in_progress" before any other write
And the agent MUST set "task_owner" to its identifier
```

After merging PR #31, `tasks/008-harden-coherence-baseline-protocol/task.md` still reads:

```yaml
task_status: open
task_owner: "unassigned"
```

The session that created `notes.md` wrote extensively about Task 008 without ever claiming it. Per the Gherkin scenario, claiming the task (setting `task_status: in_progress` and `task_owner`) MUST precede any other write to the task folder. This is not a SHOULD — it is a MUST. The notes.md was written under an unclaimed, unowned task.

**Fix:** The agent picking up Task 008 must update `task.md` frontmatter in the same commit that begins execution. This commit should have done so.

---

### V3 — Missing `friction-log.md` for FL1 Declaration (High)

**Affected rule:** `TASK.md §7.7`, `FRUSTRATED.md §When and How to Log`

Section 6 of `notes.md` declares:

> FL1 — Minor friction. The two-commit atomicity violation was forced by a genuine spec ambiguity…

`TASK.md §7.7` states: "`friction-log.md` exists if `FL > FL0`; an FL0 declaration MAY be inlined in the closing commit message instead." FL1 is greater than FL0, therefore a dedicated `friction-log.md` is REQUIRED — not optional. An inline declaration inside `notes.md §6` does not satisfy this requirement. `tools/lint-linkage.py` + `tools/check-trust.py` would catch this (per the §7.0 mechanical enforcement table).

**Fix:** Create `tasks/008-harden-coherence-baseline-protocol/friction-log.md` with the FL1 declaration extracted from `notes.md §6`, and link it from `readme.md`.

---

### V4 — PR Body Omits FL Declaration (Medium-High)

**Affected rule:** `AGENTS.md CR.5`

> The PR body created by `/sc:createPR` MUST reference (a) the closed Task slug(s) under `/tasks/` if any, and (b) the FL declaration from the friction log per `FRUSTRATED.md`.

The PR #31 body contains no FL declaration. The phrase "FL1" appears nowhere in the PR description. The requirement is explicit: the PR body MUST carry the FL declaration. Whether `/sc:createPR` was actually invoked cannot be verified from the commit, but the output (the PR body) does not comply with CR.5 regardless.

**Fix:** PR body should include, at minimum: `FL: FL1 — constraint collision between no-amend and atomic-commit mandates`.

---

## 3. Medium-Grade Issues

### M1 — `status: active` on a Completed Review Document

`notes.md` frontmatter sets `status: active`. The valid statuses per `TASK.md §3.2` are: `draft`, `active`, `blocked`, `completed`, `archived`. This file is a completed review — written once, not ongoing. `status: completed` is the semantically correct value. `active` implies the document is still being edited, which would be misleading to future agents reading the summary before the body (per `AGENTS.md AG.1.1`).

---

### M2 — `review(008)` Is a Non-Standard Conventional Commit Type

The commit message prefix `review(008):` does not exist in the Conventional Commits specification (which defines: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`, `revert`). Reviewing existing repository commit history, the project uses `chore`, `task`, `feat`, `fix`, and `refactor` as type identifiers. `review` is an invention of this session. The closest valid type would be `docs(008):` or `chore(008):`.

This is a minor issue in isolation, but in a repository explicitly designed for agent-readable audit trails, non-standard commit types degrade machine-parseable git history. The coherence prompt's `git log` step reads commit messages as structured data.

---

### M3 — PR Merged Without Review Window

PR #31 was created at `2026-05-04T15:12:04Z` and merged at `2026-05-04T15:12:14Z` — a 10-second window. No human review was possible. While the repository does not mandate a mandatory human review delay, a conformance-review PR that is itself non-conformant (V1–V4 above) arriving and merging before any reviewer can intervene is a process gap worth flagging. Branch protection rules or a minimum review window should be considered for `main`.

---

## 4. Content Assessment (Positive)

Despite the governance violations, the analytical quality of `notes.md` is high:

- **Finding 3.1** (check-governance.sh still failing) is the most important finding in the PR. The acknowledgment that the errors *pre-date* the PR while flagging that "fix linkage" in the PR description is misleading is both honest and precise.
- **Finding 3.2** (two-commit atomicity collision) correctly identifies a genuine spec ambiguity — the `no-amend` + `atomic-commit` combination creates a provably impossible constraint when T3 findings emerge after the run-log entry is already written. The recommendation (enumerate all T3 findings before writing the run-log) is the correct fix.
- **Finding 3.3** (`task_uses_prompts: []` gap) raises a real schema question about the difference between "executing" and "modifying" a prompt.
- **Finding 3.4** (bootstrap run-log malformed) correctly ties to the 7-day silent fallback problem and gives a concrete fix.
- **Section 5** (recommendations in priority order) is the most immediately useful part for whoever picks up Task 008. The ordering — install hook → define bypass policy → then iterate — is operationally sound.

---

## 5. Spec Ambiguity Surfaced

**The `type: note` vs. review artifact distinction.** `AGENTS.md §Frontmatter Ontology` lists valid `type` values as: `task`, `prompt`, `research`, `spec`, `readme`, `note`, `index`. None of these maps cleanly to a "post-merge conformance review." The notes.md uses `type: note` which is the closest available value, but this loses semantic precision. A future `type: review` or `type: analysis` may be warranted in the ontology. This should be filed as a schema extension request (parallel to the `task_spawns_prompts` extension in Task 008 Plan item 5).

---

## 6. Summary Table

| ID | Severity | Rule | Status |
|----|----------|------|--------|
| V1 | Critical | TASK.md §3.3 — L2 task namespace missing in notes.md | Open |
| V2 | Critical | TASK.md §6 / AGENTS.md — task not claimed before write | Open |
| V3 | High | TASK.md §7.7 — friction-log.md required for FL1 | Open |
| V4 | Medium-High | AGENTS.md CR.5 — PR body missing FL declaration | Cannot reopen (merged) |
| M1 | Medium | TASK.md §3.2 — `status: active` should be `completed` | Open |
| M2 | Low | Conventional Commits — `review` is non-standard type | Cannot reopen (merged) |
| M3 | Low | Process — 10s merge window, no human review | Process recommendation |

---

## 7. Friction Level

FL0 — This critique was produced with no tooling friction. All relevant information was accessible from the PR diff, the task files, and the governance specs without any fallbacks or re-reads.
