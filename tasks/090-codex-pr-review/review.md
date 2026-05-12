---
type: note
status: active
slug: codex-pr-review-review
summary: "Governance review of PR #112 (codex/init-repo-for-codex-with-root-specs-4e44z1 → main): critical defects, significant gaps, and minor findings against AGENTS.md, TASK.md, FRUSTRATED.md, and ADR conventions."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #112: Add Codex platform support

**Branch:** `codex/init-repo-for-codex-with-root-specs-4e44z1` → `main`
**Reviewer:** Claude (claude/brave-darwin-Z3tXz session)
**Reviewed against:** AGENTS.md, TASK.md, FRUSTRATED.md, PRE_COMMIT.md, CLAUDE.md, decisions/ ADR conventions
**Governance gate result:** `FAIL` (see C1–C3 below)

---

## Summary

PR #112 introduces Codex platform onboarding via `CODEX.md`, a platform implementation note in `AGENTS.md`, ADR-0011, and Task 090. The intent is correct and necessary. However, the PR contains **four critical defects** that violate `MUST`-level rules from the very governance it claims to establish, plus a set of significant and minor gaps detailed below. The PR MUST NOT be merged until C1–C4 are resolved.

---

## Critical Defects — MUST be resolved before merge

### C1 — Missing `friction-log.md` (TASK.md §2, Spec-J.7.1, Spec-L.3.1)

Task 090 carries `task_status: done` but no `friction-log.md` exists in `tasks/090-codex-pr-review/`. TASK.md §2 lists `friction-log.md` as **MANDATORY when `task_status` reaches `done` or `abandoned`**. The `## Frustration Log` section inside `task.md` is not a substitute — it is a different artefact slot.

`tools/check-trust.py` catches this and surfaces it as an ERROR:

```
ERROR tasks/090-codex-pr-review: done task has no friction-log.md
       (Spec-J.7.1 / Spec-L.3.1)
```

This is a hard-error in `tools/check-governance.sh`.

### C2 — `tools/check-governance.sh` exits non-zero; PR MUST NOT have been opened (CR.3)

AGENTS.md CR.3: "A failing working tree MUST NOT be promoted to a pull request." This PR was opened with the governance gate in a `FAIL` state (caused by C1 above). The pre-commit hook (`tools/check-trust.py`) produces an error that `tools/check-governance.sh` correctly surfaces as `=== FAIL ===`. Opening a PR on top of a failing gate violates the CR.3 invariant the PR itself is trying to encode.

### C3 — PR body does not satisfy CR.5 (AGENTS.md CR.5)

AGENTS.md CR.5 requires the PR body to reference: "(a) the closed Task slug(s) under `/tasks/` if any, and **(b) the FL declaration from the friction log**." The PR body does not contain an FL declaration (`Highest Frustration Level: FL[n]`). The Task slug (`090-codex-pr-review`) is not cited either — the PR body is free-form narrative without the mandatory citation block.

### C4 — PR opened as non-draft (AGENTS.md Closing Run Procedure step 4)

AGENTS.md Closing Run Procedure step 4: "The agent MUST open a **draft** pull request." PR #112 was opened with `draft: false`. This deviates from the explicit requirement in the same spec the PR is adding Codex support for.

---

## Significant Gaps — SHOULD be addressed before merge

### S1 — ADR-0011 `adr_status: Proposed` while decision is already implemented

ADR-0011 documents an architectural decision (`CODEX.md` as root entry-point, Codex platform note in `AGENTS.md`) that is already implemented in the same PR. By MADR convention, an ADR transitions to `Accepted` when its implementation lands. Leaving it as `Proposed` implies the decision is still under deliberation, which is misleading for future agents and reviewers reading the ledger.

`decisions/readme.md` should list `adr_status: Accepted` for ADR-0011 as well.

### S2 — ADR-0010 numbering gap in the append-only ledger

The decisions ledger jumps from ADR-0009 to ADR-0011. No ADR-0010 exists. The append-only ADR ledger SHOULD maintain sequential numbering per the ADR governance spec (`tools/adr/cli.py validate`). Either ADR-0010 was erroneously skipped, or it was previously created and deleted (which would violate the `Accepted` ADR T4-immutability rule). The gap requires explanation in an Assumptions Log entry or a new ADR-0010 must be created or the numbering rationalized.

### S3 — CODEX.md §1 omits `tools/install-hooks.sh` hook installation

CLAUDE.md §2 mandates: "Install the pre-commit hook once per clone: `tools/install-hooks.sh`." CODEX.md §1 (Mandatory bootstrap) only lists `./install.sh` and `tools/check-governance.sh`. A Codex agent bootstrapping from CODEX.md would operate without the pre-commit hook installed, silently bypassing the gate on every commit. The hook install step MUST be added to CODEX.md §1.

### S4 — CODEX.md missing `tools/fm/edit.py` frontmatter mutation requirement

CLAUDE.md §14 rule 6: "Mutate frontmatter via `tools/fm/edit.py`, not `sed`/`awk`." CODEX.md §3 (Frontmatter, readmes, and structure) does not mention this requirement. A Codex agent following CODEX.md could mutate frontmatter with shell tools, producing subtly malformed YAML that `tools/fm/validate.py` would then flag. This is a functional gap, not a stylistic one.

### S5 — `task_uses_prompts: []` breaks the Task→Prompt audit chain

TASK.md §1: "A Task is the orchestration layer that links *what should be done* (Task) to *the instruction set* (Prompt) […] A Task MUST NOT inline a prompt; it MUST link to one." Task 090 has no linked prompt. The Codex task URL in the PR body (`chatgpt.com/codex/cloud/tasks/…`) is external and non-addressable within the repo audit graph. The frontmatter cross-reference (`task_uses_prompts`) is deliberately the *only* sanctioned linkage mechanism per CLAUDE.md §4: "Cross-directory linkage flows through frontmatter only."

If this work genuinely required no prompt (pure governance repair), the readme Assumptions Log entry that says as much should cite MAINTENANCE.md §1 T1/T2 tier as the authority, and the maintenance bypass mechanism (`tools/check-maintenance-bypass.py`) should be invoked. Otherwise a minimal prompt under `/prompts/codex-pr-review/` should be created to close the audit chain.

### S6 — ADR-0011 contains no Gherkin acceptance criteria

AGENTS.md §Spec Language Reference and CLAUDE.md §5 require: "Every acceptance criterion is a **Gherkin scenario**." ADR-0011 has only prose "Consequences" bullets — no `Feature:` / `Scenario:` blocks, no stable `# anchor: <id>` anchors. This is a spec-language violation for every normative consequence stated in the ADR.

### S7 — Codex platform note in AGENTS.md has no Gherkin scenario

The existing `CR.1.1` (Claude Code) has a Gherkin scenario at anchor `CR.1.1`; Jules has `CR.1.2`; Gemini `CR.1.3`. The new Codex platform note does not add a `CR.1.N` scenario block. Parity with the existing platforms requires a scenario of the form:

```gherkin
# anchor: CR.1.5
Scenario: Codex session closes with make_pr
  Given a Codex session has finished its work
  And tools/check-governance.sh exited 0 on the final commit
  And the friction-log.md carries a "Highest Frustration Level: FL[0-3]" line
  When the agent reaches the end of the session
  Then the agent MUST invoke make_pr before declaring the session complete
  And the resulting pull request MUST be a draft
  And the resulting pull request body MUST cite the closed Task slug(s) and the FL declaration
```

---

## Minor Observations

### M1 — `tasks/090-codex-pr-review/readme.md` Linked Navigation is incomplete

The readme only links to `task.md`. `task_affects_paths` in `task.md` lists `CODEX.md`, `AGENTS.md`, `decisions/`, and `tasks/readme.md`. Per FOLDERS.md §3 and the readme rule (CLAUDE.md §7), every file and subfolder in the operational scope SHOULD be navigable from the folder's `readme.md`. Add links to at least `CODEX.md`, `AGENTS.md`, and `decisions/0011-codex-entrypoint-and-platform-note.md`.

### M2 — CODEX.md `type: spec` is novel; `type` enum does not yet include platform entry-points

`type ∈ {task, prompt, research, spec, readme, note, index}` — `spec` is defensible for CODEX.md but the platform entry-points are a new structural category. If more platforms follow (DEVIN.md, JULES.md, etc.), the type vocabulary may need an explicit `platform-spec` or `entrypoint` value. This is a forward-looking concern, not a blocker, but worth logging as an assumption.

### M3 — `decisions/readme.md` entry for ADR-0011 should list `adr_status: Accepted` (mirrors S1)

The entry added in `decisions/readme.md` ends with "`adr_status: Proposed`." Consistent with S1 above, this should read `adr_status: Accepted` once the PR merges.

---

## Required actions before merge

| # | Action | Owner |
|---|--------|-------|
| C1 | Create `tasks/090-codex-pr-review/friction-log.md` with `Highest Frustration Level: FL[n]` line | Codex / @jules |
| C2 | Verify `tools/check-governance.sh` exits 0 before any further push | Codex / @jules |
| C3 | Add FL declaration and Task slug citation to PR body | Codex / @jules |
| C4 | Convert PR to draft (GitHub API or UI) | Codex / @jules |
| S1 | Change ADR-0011 `adr_status` from `Proposed` to `Accepted` | Codex / @jules |
| S2 | Investigate and resolve ADR-0010 gap or document the gap in Assumptions Log | Codex / @jules |
| S3 | Add `tools/install-hooks.sh` step to CODEX.md §1 bootstrap | Codex / @jules |
| S4 | Add `tools/fm/edit.py` requirement to CODEX.md §3 | Codex / @jules |
| S5 | Link prompt or file maintenance bypass for `task_uses_prompts: []` | Codex / @jules |
| S6 | Add Gherkin scenarios to ADR-0011 | Codex / @jules |
| S7 | Add `CR.1.5` (or next index) Gherkin scenario for Codex platform note in AGENTS.md | Codex / @jules |

---

*Review authored by Claude (session claude/brave-darwin-Z3tXz, 2026-05-12). Full findings file: [`tasks/090-codex-pr-review/review.md`](./review.md).*
