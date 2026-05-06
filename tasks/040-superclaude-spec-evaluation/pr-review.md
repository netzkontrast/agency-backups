---
type: note
status: active
slug: pr70-review
summary: "Governance review of PR #70 (Tasks 032–040 spec-integration chain). Identifies 3 critical spec-compliance issues, 2 major portability gaps, and 2 minor discrepancies, alongside substantive strengths."
created: 2026-05-06
updated: 2026-05-06
---

# PR #70 Review — Tasks 032–040 Spec-Integration Chain

**Reviewer:** claude-code (session `claude/stoic-mendel-CjI39`)  
**PR:** https://github.com/netzkontrast/agency/pull/70  
**Branch:** `claude/integrate-repo-specs-cIWtI → main`  
**Scope:** AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md governance compliance; Task 040 synthesis quality; subtask file conventions; tasks/readme.md index integrity.

---

## Executive Summary

The 9-task chain (032–040) is architecturally sound, well-reconnoitered (three parallel Explore agents before any spec was written), and the Gemini SuperClaude spec evaluation (Task 040) is the most rigorous external-research triage this repo has seen: 0 ACCEPT-AS-IS, 8 AMEND, 4 MERGE-INTO, 1 REJECT is the correct disposition. The frontend-architect's `sc-document` conflation catch (§F.note) alone justifies the dual-lens approach.

Three critical spec-compliance issues MUST be fixed before or immediately after merge. Two major portability gaps SHOULD be addressed before the first subtask is dispatched. Two minor discrepancies MAY be fixed inline.

---

## CRITICAL

### C.1 — `tasks/readme.md` `updated` frontmatter is stale

**Spec:** TASK.md §4.8 rule 4: "`tasks/readme.md`'s own `updated:` field MUST be bumped to today's ISO date on every such change." §7.11: linter emits ERROR if the condition fails.

**Finding:** `tasks/readme.md` frontmatter reads `updated: 2026-05-05`. Tasks 032–040 were created 2026-05-06 and ARE listed in the index. The membership is correct; the timestamp is not. This is the most mechanical compliance failure in the PR — `tools/check-governance.sh` should have caught it; that it did not suggests §7.11 is not yet mechanically enforced (consistent with §7.0 row §7.11 being labelled "Task 019 — not yet active"). Until Task 019 ships, the agent carries the obligation manually.

**Fix:** Change `updated: 2026-05-05` → `updated: 2026-05-06` in `tasks/readme.md` frontmatter.

---

### C.2 — Task 040 todo list does not reflect completed phases

**Spec:** TASK.md §4 Step 4 ("Execute — Set `task_status: in_progress`"); TASK.md §5 ("Todo — The Task is `done` only when every box is checked"); general principle that `task.md` is an agent's primary signal of prior work.

**Finding:** `tasks/040-superclaude-spec-evaluation/task.md` has `task_status: open` with all 9 todo items as `- [ ]`. But:

- `evaluation-notes.md` — Phase 1 backend-architect lens (complete, 5-section filing)
- `evaluation-notes-frontend.md` — Phase 1 frontend-architect lens (complete, 7-section filing)
- `synthesis.md` — Phases 2, 3, 4 (§A classification, §B anchor reconciliation, §C MCP reality-check — all complete)

At minimum, todo items 1–4 are done. A dispatching agent landing on this task after merge would re-execute the already-completed phases, consuming tokens and potentially overwriting the filed synthesis.

**Fix (two-part):**
1. Set `task_status: in_progress` in frontmatter (work has started).
2. Mark todo items 1–4 as `- [x]` to reflect the filed phases:
   - `[x] 1. Phase 1 — read backend-architect + frontend-architect findings`
   - `[x] 2. Phase 2 — produce §A classification matrix`
   - `[x] 3. Phase 3 — produce §B anchor-scheme reconciliation decision`
   - `[x] 4. Phase 4 — produce §C MCP-server reality-check matrix`

---

### C.3 — Subtask execution briefs are inlined prompts — TASK.md §1 / §4.3 violation

**Spec:** TASK.md §1: "A Task MUST NOT inline a prompt; it MUST link to one." TASK.md §4.3: "If the Task requires an instruction set, ensure a prompt exists under `/prompts/<slug>/` and reference its slug in `task_uses_prompts`. If no suitable prompt exists, the agent MUST first create one as a Prompt Task per `PROMPT.md`."

**Finding:** Every subtask file (e.g., `tasks/032-agents-spec-integration/subtasks/01-research-adr-corpus-extraction.md`) contains a multi-section `## Execution Brief (for the main agent…)` block that is — functionally — a self-contained, executable prompt: it declares `research_question`, `output_format`, `process_gates`, `Acceptance Criteria`, `Phase 2 Plan Hints`, and explicit step-by-step agent instructions. These artifacts are filed as `type: note` under `/tasks/<NNN>/subtasks/`, not as `type: prompt` under `/prompts/<slug>/`.

The `type: note` designation does not launder the anti-pattern. TASK.md §1 prohibits inlining regardless of the file's declared type. The relevant question is whether the artifact is *functioning as a prompt* — and 35 subtask files with verbatim agent instruction blocks plainly are.

**Implication:** All 9 tasks have `task_uses_prompts: []` while their execution briefs constitute 35 instruction sets distributed across subtask files. This decouples the audit graph: no `task → prompt` edge exists; `tools/lint-linkage.py` has nothing to traverse; the Frontmatter Ontology is silent about these instruction sets.

**Recommended fix:** For each subtask that contains an `## Execution Brief`, create a corresponding `/prompts/<chain-slug>/<st-slug>/prompt.md` with proper `type: prompt` frontmatter and `prompt_kind: task-spec`, and update the parent task's `task_uses_prompts` to list it. This would produce ~35 proper prompts, which is the correct shape for this chain's scale.

**Acceptable minimal fix (if the above is deferred):** Explicitly note in each `task.md` that the subtask `.md` files serve as de-facto prompt substitutes pending formal `/prompts/` extraction, and file a follow-up Task (e.g. Task 041 "extract-subtask-execution-briefs-to-prompts") to close the debt. This at minimum acknowledges the violation rather than treating it as compliant.

---

## MAJOR

### M.1 — Absolute path and branch name hardcoded in execution briefs

**Finding:** Subtask execution briefs contain environment-specific literals:
- `Repo root: /home/user/agency` (appears in ≥10 subtask files)
- `Branch: claude/integrate-repo-specs-cIWtI` (the development branch, now being merged)

After merge, a dispatching agent on `main` (or any other branch) will follow a stale branch reference. The `/home/user/agency` root will silently break in any environment where the clone is not at that exact path.

**Fix:** Replace `Repo root: /home/user/agency` with `Repo root: $(git rev-parse --show-toplevel)` or simply `Repo root: <determine at runtime>`. Replace `Branch: claude/integrate-repo-specs-cIWtI` with `Branch: <create a new branch per AGENTS.md>` or omit — the dispatching agent creates its own branch.

---

### M.2 — PR body and synthesis.md disagree on the MERGE patch count

**Finding:**
- PR body (§ Process highlights, item 5): "3 highest-leverage MERGE patches already applied to host tasks 033, 038, 039."
- `synthesis.md §E`: "two highest-leverage MERGE patches applied in this commit … Remaining MERGE rows for Tasks 034, 037, 039 are queued for the maintainer."

The PR body claims 3 applied patches targeting {033, 038, 039}; synthesis.md says 2 applied, with {034, 037, 039} still queued. Both cannot be simultaneously correct. If 3 patches landed, synthesis.md §E is under-reporting; if 2 landed, the PR body is overcounting. This discrepancy is an audit-trail ambiguity: maintainers diffing `tasks/033-task-spec-integration/task.md`, `tasks/038-frustrated-spec-integration/task.md`, and `tasks/039-maintenance-spec-integration/task.md` should verify which patches are actually present in the diff.

**Fix:** Bring synthesis.md §E and the PR body into agreement with the actual diff contents.

---

## MINOR

### m.1 — research/readme.md updated-date should be checked

Same pattern as C.1: the research/readme.md may need its `updated` field bumped if any `research/` entry was added or modified in this branch (e.g. `research/gemini/superclaude-agency-orchestration-spec/` was scaffolded). Verify and fix if stale.

---

### m.2 — Task 040 `task_affects_paths` omits the evaluation note artifacts

`task_affects_paths` lists the 032–039 task folders and the Gemini research folder, but the task itself produced `evaluation-notes.md`, `evaluation-notes-frontend.md`, and `synthesis.md` inside `tasks/040-superclaude-spec-evaluation/`. These are within the 040 folder, which is technically not listed in `task_affects_paths`. Low blast radius (the files ARE within the task's own directory), but a pedantically correct fix would add `tasks/040-superclaude-spec-evaluation/` to the list.

---

## Substantive Strengths

These are notable positives worth preserving in any follow-up merge or review cycle:

1. **Gemini spec triage discipline.** The dual-lens approach (backend-architect + frontend-architect in parallel) produced converging, independent verdicts. 0 ACCEPT-AS-IS is the right call for a doc that self-asserts "binding/IN-FORCE" while citing 8 unintegrated MCP servers. The §D process notes for Phase 5 maintainers are unusually thorough.

2. **`sc-document` conflation catch (frontend §F.note).** The spec uses three distinct forms (`sc-document`, `(sc-document)`, `/sc:document`) for what it claims are two different commands. Catching this before it entered the normative chain prevented a high-confusion onboarding trap. The §J framing ("three highest-leverage UX adoptions") is exactly the right editorial move — lift the *pattern*, not the broken name.

3. **Chain falsification criteria (`tasks/readme.md` §Chain-Level Falsification).** Four operationalizable falsifiers with rollback pointers is a model of how to scope a multi-task chain. Most task chains lack any falsification gate; this one has four.

4. **ADR-guardedness.** The explicit "edits MUST land outside the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers" constraint in Task 032's Goal is the right way to respect an actively-rewritten guarded section. It prevents the most common post-Task-031 corruption mode.

5. **Anchor-scheme reconciliation decision (§B, option ii).** Folding `SC.CMD.*` into host-spec namespaces rather than adding a 10th top-level namespace is correct. The per-anchor remapping table in synthesis.md makes the decision auditable and reversible.

---

## Summary Table

| ID | Severity | File | Rule | Fix |
|---|---|---|---|---|
| C.1 | CRITICAL | `tasks/readme.md` | TASK.md §4.8 rule 4 | Bump `updated` to `2026-05-06` |
| C.2 | CRITICAL | `tasks/040-.../task.md` | TASK.md §4/§5 | Set `in_progress`; check off items 1–4 |
| C.3 | CRITICAL | 35 subtask files | TASK.md §1, §4.3 | Extract execution briefs to `/prompts/` or file debt-task |
| M.1 | MAJOR | 35 subtask files | Portability | Replace hardcoded path + branch |
| M.2 | MAJOR | `synthesis.md` / PR body | Audit-trail integrity | Reconcile patch count (2 vs 3) |
| m.1 | MINOR | `research/readme.md` | TASK.md §4.8 analogy | Verify + bump `updated` |
| m.2 | MINOR | `tasks/040-.../task.md` | TASK.md §3.3 | Add own folder to `task_affects_paths` |
