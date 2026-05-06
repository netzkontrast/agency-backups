---
type: research
status: completed
slug: pr71-meta-review
summary: "Meta-review of PR #71: governance critique of PR #70. Finds 3 critical and 3 major meta-compliance violations in the review artifact itself, plus 3 content-quality gaps."
created: 2026-05-06
updated: 2026-05-06
research_phase: complete
research_executes_prompt: pr71-meta-review
research_friction_level: FL1
---

# Meta-Review — PR #71

**PR under review:** #71 (`claude/stoic-mendel-CjI39 → main`, SHA `ec9109a`)  
**Review artifact:** `tasks/040-superclaude-spec-evaluation/pr-review.md`  
**Meta-reviewer:** claude-code (claude-sonnet-4-6), session `claude/stoic-mendel-1VEa6`  
**Date:** 2026-05-06  
**Verdict:** ⚠️ **APPROVE WITH MANDATORY PRE-MERGE FIXES** — the content is substantively
correct and valuable, but the session that produced it violated the same conventions it
enforces in the reviewed PR, with the ironic exception of C.3.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in
BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## Executive Summary

The `pr-review.md` delivers seven well-cited governance findings against PR #70. The
severity calibration is accurate, the spec citations are correct, and the substantive
strengths section is appropriately balanced. It is the most complete review in the
recent PR history.

However, the review artifact is itself non-compliant with the repo conventions it cites.
Three critical structural violations exist — all traceable to the same root cause: the
reviewing session produced no formal prompt in `/prompts/` and no research workspace in
`/research/`, depositing the output directly into a task subfolder instead. This mirrors
the C.3 pattern it criticises in PR #70 (inlined prompts in task subfolders), and the
parallel is exact enough to require explicit acknowledgement.

Additionally, C.3's "Acceptable minimal fix" is not actually acceptable under the
normative language of TASK.md §1.

---

## A — Meta-Compliance Issues (the artifact's own spec violations)

### MC.1 — Review artifact placed in the wrong directory (CRITICAL)

**Finding:** `pr-review.md` lives at
`tasks/040-superclaude-spec-evaluation/pr-review.md`. The canonical location for a
PR review output is `research/<slug>/output/REVIEW.md`.

**Precedent:** `research/pr27-governance-review/output/REVIEW.md` is the established
pattern for all prior PR reviews in this repo. Every element of FOLDERS.md §1's hard
flow rule applies here:

```
/tasks/<NNN>-<slug>/task.md
        │ task_uses_prompts ──► /prompts/<slug>/prompt.md
                                        │ executed ──► /research/<slug>/output/REVIEW.md
```

The review is a *research output* (evidence produced by executing an instruction set),
not a *task coordination artifact*. Depositing it under `/tasks/` collapses the
separation of concerns that FOLDERS.md §1 and RESEARCH.md §1 exist to enforce.

**Spec:** FOLDERS.md §1 (hard flow rule), RESEARCH.md §1 ("Research IS the workspace
where a prompt is executed … IS NOT a place to coordinate work across runs").

**Fix:** Move to `research/pr70-governance-review/output/REVIEW.md` (matching the
`pr27-governance-review` precedent). The Task 040 folder MAY keep a pointer note, but
MUST NOT host the deliverable.

---

### MC.2 — No formal prompt authored for this review session (CRITICAL)

**Finding:** No prompt exists at `/prompts/pr70-governance-review/` (or any slug).
`tasks/040-superclaude-spec-evaluation/task.md` has `task_uses_prompts: []`; the
review session is invisible to the audit graph.

**Spec:** PROMPT.md §1: "Every artifact whose primary purpose is to instruct an agent
MUST be stored under `/prompts/<slug>/`." FOLDERS.md §1: the `task_uses_prompts` edge
is the single source of truth linking task-scope to instruction sets. RESEARCH.md §4
rule 1: "Confirm `/prompts/<slug>/prompt.md` exists. If it does not, the agent MUST
stop and create one per `PROMPT.md`. Research MUST NOT fabricate its own instruction set."

The reviewing agent executed an implicit instruction set (the mental model of "how to
review a PR in this repo") without externalising it as a prompt. This makes the review
non-reproducible and non-auditable.

**Fix:** Create `/prompts/pr70-governance-review/` with `brief.md`, `prompt.md`,
`readme.md`. Update Task 040's `task_uses_prompts` to reference it.

> Note: This meta-review retroactively creates `/prompts/pr71-meta-review/` to
> demonstrate the correct pattern. The same fix MUST be applied to the reviewed session.

---

### MC.3 — No research workspace scaffolded (CRITICAL)

**Finding:** RESEARCH.md §2 requires the directory structure:
```
/research/<slug>/
    readme.md
    prompt.md          # immutable snapshot at run-start
    /workspace/
    /synthesis/
    /reflection/
    /output/
        REVIEW.md
```
None of these folders or files were created. The output was deposited as a flat note.

**Spec:** RESEARCH.md §2 (directory structure), FOLDERS.md §3 (`readme.md` rule):
"EVERY folder MUST contain a `readme.md`." The `tools/lint-structure.py` linter would
emit an ERROR for a research slug missing a `readme.md`.

**Fix:** Scaffold `research/pr70-governance-review/` with the canonical structure.
Minimal compliant form: `readme.md` + `output/REVIEW.md` (workspace, synthesis,
reflection subfolders are OPTIONAL per RESEARCH.md §2, but `readme.md` and `output/`
are mandatory).

---

### MC.4 — `type: note` conceals a functional research output (MAJOR)

**Finding:** The review file declares `type: note` and `status: active`. A PR review
output is `type: research` per the L1 ontology. The missing L2 research namespace keys
(`research_phase`, `research_executes_prompt`, `research_friction_level`) make the file
invisible to tooling that queries research metadata.

**Spec:** TASK.md §3.3 (Research namespace — mandatory inside `/research/<slug>/`).
AGENTS.md Frontmatter Ontology: "files in operational directories MUST carry frontmatter."

**Fix:** After moving to the correct folder, change frontmatter to:
```yaml
type: research
status: completed
research_phase: complete
research_executes_prompt: pr70-governance-review
research_friction_level: FL0   # or FL1 if the review took iteration
```

---

### MC.5 — Task 040 `task_status: open` not updated before review work (MAJOR)

**Finding:** The review session wrote `pr-review.md` without first setting
`task_status: in_progress` in `task.md`. This violates the lifecycle precondition in
TASK.md §4 Step 4: "Set `task_status: in_progress`. Precondition: every entry in
`task_blocked_by` MUST already have `task_status: done`."

The review correctly identifies this issue as C.2 in the reviewed PR — and then
exhibits the same behaviour in the very session that wrote the critique.

**Spec:** TASK.md §4 Step 4, TASK.md §6 Gherkin Scenario "Agent picks up an open Task".

**Fix:** Set `task_status: in_progress` in Task 040's `task.md` and mark at minimum
the review step as `[x]` in the Todo.

---

### MC.6 — No friction-log.md for this review session (MAJOR)

**Finding:** FRUSTRATED.md mandates an FL[0-3] declaration for every session, including
FL0 runs. No `friction-log.md` was committed alongside `pr-review.md`, and the commit
message contains no inline declaration.

**Spec:** AGENTS.md: "You MUST consult FRUSTRATED.md to accurately log the Frustration
Level (FL) associated with your task. This is a mandatory step for every session, even
if everything went perfectly (FL0)." TASK.md §4 Step 6 / §7.8.

**Fix:** Add `tasks/040-superclaude-spec-evaluation/friction-log.md` (or include the
FL declaration in the commit message as per PROMPT.md §6.8's allowance for standalone
runs). The declaration MUST appear before or alongside the commit.

---

## B — Content Quality Assessment

### CQ.1 — C.3 "Acceptable minimal fix" is not acceptable (MAJOR)

**Finding:** C.3 proposes a two-tier fix hierarchy:

> "Recommended fix: Extract to `/prompts/<chain-slug>/<st-slug>/prompt.md`."  
> "Acceptable minimal fix: Explicitly note in each `task.md` that subtask files serve
> as de-facto prompt substitutes, pending formal extraction."

The "acceptable minimal fix" is not acceptable under TASK.md §1, which states:
"A Task **MUST NOT** inline a prompt; it MUST link to one." MUST NOT in RFC 2119
is an **absolute prohibition** — no documented exception exists, and no annotation
or footnote can launder the anti-pattern.

The only compliant fix is the recommended one: extraction to `/prompts/`. Filing a
debt-task (e.g. "Task 041 — extract subtask execution briefs to prompts") is a
legitimate sequencing strategy, but the debt-task does not make the current state
compliant — it merely schedules the repair.

**Spec:** TASK.md §1, TASK.md §9 Anti-Patterns ("MUST NOT inline an executable prompt
body inside `task.md`"). RFC 2119 keyword semantics (MUST NOT = absolute prohibition,
no deviation under any circumstances).

**Impact:** Maintainers reading the "acceptable minimal fix" might implement it and
consider the issue resolved. The review SHOULD have been unambiguous: the only path
to compliance is extraction.

---

### CQ.2 — Missing finding: `subtasks/` subfolder creation heuristic (MINOR)

**Finding:** FOLDERS.md §4.1 states: "Do not create a subfolder unless 4+ files of
the exact same category accumulate." Tasks 032–039 each have a `subtasks/` subfolder.
The review does not verify that each subtask folder reached the 4-file threshold before
the subfolder was created.

A spot-check of Task 037 (`pre-commit-spec-integration`) shows 3 subtask files —
`subtasks/01-*, 02-*, 03-*`. This is below the 4-file threshold and should have been
flagged as a MINOR violation.

**Spec:** FOLDERS.md §4 ("Prefer Flat Structures — do not create a subfolder unless
4+ files of the exact same category accumulate").

---

### CQ.3 — M.2 patch-count discrepancy is under-resolved (MINOR)

**Finding:** M.2 correctly identifies the discrepancy (PR body says 3 patches,
`synthesis.md §E` says 2). However, the fix recommendation ("bring into agreement with
the actual diff") does not specify which claim is correct, making it unactionable
without additional diff inspection.

**Improvement:** The review SHOULD have checked the actual git diff for commits to
`tasks/033-task-spec-integration/task.md`, `tasks/038-frustrated-spec-integration/task.md`,
and `tasks/039-maintenance-spec-integration/task.md`, and stated definitively which
count is accurate.

---

## C — Missed Findings

| ID | Severity | Finding |
|---|---|---|
| MF.1 | CRITICAL | Review artifact itself not in `/research/` workspace (see MC.1-MC.3) |
| MF.2 | MAJOR | C.3 "acceptable minimal fix" is not MUST-NOT compliant (see CQ.1) |
| MF.3 | MINOR | `subtasks/` created below 4-file threshold in ≥1 task (see CQ.2) |

---

## D — Strengths (Preserved)

The following observations from the review MUST be preserved in any follow-up:

1. **Accurate severity calibration.** C.1, C.2, C.3 are genuine CRITICAL issues. The
   MAJOR/MINOR tier is correctly populated.

2. **Correct spec citations.** Every cited clause (TASK.md §4.8 rule 4, TASK.md §1,
   TASK.md §4.3) is accurate and verifiable.

3. **M.1 portability finding is actionable.** The hardcoded `/home/user/agency` path
   is a real operational hazard; the fix is precise.

4. **Substantive strengths section is balanced and accurate.** The dual-lens evaluation
   approach, the `sc-document` conflation catch, and the chain falsification criteria
   are correctly identified as model practices.

5. **C.3 identification is the highest-value finding.** Noting that 35 inlined execution
   briefs constitute an audit-graph gap is architecturally important for the chain's
   long-term maintainability.

---

## Summary Table

| ID | Severity | Dimension | Finding | Fix |
|---|---|---|---|---|
| MC.1 | CRITICAL | Placement | Review output in `/tasks/` not `/research/` | Move to `research/pr70-governance-review/output/REVIEW.md` |
| MC.2 | CRITICAL | Audit graph | No `/prompts/pr70-governance-review/` exists | Create prompt; update `task_uses_prompts` |
| MC.3 | CRITICAL | Workspace | No research workspace scaffolded | Scaffold `research/pr70-governance-review/` |
| MC.4 | MAJOR | Frontmatter | `type: note` on a research output; missing L2 keys | Change to `type: research`; add `research_*` keys |
| MC.5 | MAJOR | Lifecycle | `task_status: open` not updated before writing | Set `in_progress`; mark completed todos |
| MC.6 | MAJOR | Friction | No `friction-log.md` for review session | Add `friction-log.md` with FL[0-3] |
| CQ.1 | MAJOR | Content | C.3 "acceptable minimal fix" violates MUST NOT | Revise: only extraction is compliant |
| CQ.2 | MINOR | Content | `subtasks/` below 4-file threshold not flagged | Add finding for FOLDERS.md §4 violation |
| CQ.3 | MINOR | Content | M.2 unactionable without diff verification | State which patch count is correct |

---

## Verdict

The `pr-review.md` content is substantively valuable and SHOULD be merged after structural
remediation. The three critical issues (MC.1–MC.3) MUST be addressed before the artifact
can be considered repo-compliant. The most efficient remediation path:

1. Move `pr-review.md` to `research/pr70-governance-review/output/REVIEW.md`.
2. Create the minimal prompt at `/prompts/pr70-governance-review/` (brief.md, prompt.md,
   readme.md).
3. Scaffold `research/pr70-governance-review/readme.md`.
4. Update Task 040 `task.md`: set `task_status: in_progress`, mark todos 1–4 as `[x]`,
   add `task_uses_prompts: [pr70-governance-review]`.
5. Add `friction-log.md` to `tasks/040-superclaude-spec-evaluation/`.
6. Revise C.3 to remove the "acceptable minimal fix" (it is not acceptable).

The irony is not lost: the session reviewing C.3 (inlined prompts in task subfolders)
committed the same structural violation by placing its own output directly in a task
subfolder without a corresponding prompt or research workspace.
