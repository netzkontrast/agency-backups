---
type: note
status: completed
slug: critique-pr63-fm-toolchain-suite-integration
summary: "Governance and code-quality critique of PR #63 (Task 017/019: complete flexible-frontmatter toolchain migration) by claude-code session claude/stoic-mendel-lONbq. Identifies two governance violations, one code-quality issue, three medium-grade findings, and one systemic process gap. Delivery quality is high; all 154 tests pass and governance check is green."
created: 2026-05-05
updated: 2026-05-05
---

# Critique — PR #63 (`Task 017/019: Complete flexible-frontmatter toolchain migration`)

**Reviewer:** `claude-code` session `claude/stoic-mendel-lONbq`  
**Date:** 2026-05-05  
**PR reviewed:** #63 — `claude/complete-frontmatter-toolchain-l5Q8E` → `main` (open, SHA `b73e615`)  
**Governing specs:** `AGENTS.md`, `TASK.md §3–§7`, `PROMPT.md §1–§4`, `FOLDERS.md`, `FRUSTRATED.md`  
**Original Task prompt:** [`tasks/019-fm-toolchain-suite-integration/task.md`](./task.md) + subtask index [`subtasks/readme.md`](./subtasks/readme.md)

---

## 1. Verdict

The delivery is substantively strong. All 154 tests pass (1 skipped), `tools/check-governance.sh` exits 0, and the new `tools/fm/` surface (validate, fix, graph, rename, section, new, edit, query, fm-wrapper) ships as a coherent whole. The friction log (`FL3`) is admirably candid about the parallel-agent infrastructure failures, and the falsification clauses in each subtask file are exemplary engineering practice worth preserving as a pattern.

That said, the PR introduces **two governance violations** against the canonical tri-partition model it is meant to reinforce, **one code-quality concern** in the `--baseline` implementation, and **three medium-grade issues** that weaken the audit trail for downstream tasks. One systemic process gap — the FL3 infrastructure failure — is documented but not yet actioned as a concrete Task.

The PR should not be blocked on these findings; the violations are well-understood deviations that can be resolved in Task 020 or a lightweight follow-up commit. They are recorded here so the audit trail is intact.

---

## 2. Governance Violations

### V1 — `status: active` on a Closed Task (High)

**Affected rule:** `TASK.md §3.2` — L1 `status` is one of `draft`, `active`, `blocked`, `completed`, `archived`.

`tasks/019-fm-toolchain-suite-integration/task.md` frontmatter reads:

```yaml
status: active
task_status: done
```

When `task_status` reaches `done`, the L1 `status` field MUST be updated to `completed`. Leaving `status: active` signals to future agents scanning the repository that this task is still in flight (per `AGENTS.md AG.1.1`, agents read `summary` and `status` before opening the body). A future maintenance-loop agent following the `archived`/`active` skipping heuristic in `AG.1.2` would correctly read this task when it should already be de-prioritised.

The validator does not currently emit an error for `status: active` + `task_status: done` co-occurrence. This is a missing F.T.3 rule — worth filing as a follow-up enhancement on `tools/fm/validate.py --type-check`.

**Fix:** In the same commit or the next cleanup commit, change `status: active` → `status: completed` in `task.md`.

---

### V2 — Subtask Prompts Stored as `type: note` Inside `/tasks/`, Not Under `/prompts/` (Medium-High)

**Affected rule:** `PROMPT.md §1` — "Every artifact whose primary purpose is to instruct an agent MUST be stored under `/prompts/<slug>/`."

The nine subtask files (`subtasks/01-fm-rename-cross-file-slug.md` through `subtasks/09-spec-amendments-q4-q5.md`) each carry an **Agent Prompt** section containing a self-contained, executable instruction set directed at a specific agent type. Their declared `type: note` understates their role. By `PROMPT.md §1`'s definition, these are prompt artifacts — they instruct agents to produce code and tests.

Consequences of the current placement:
- `task_uses_prompts: []` is misleadingly empty. Task 019 does use executable prompts; they are simply stored in the wrong canonical location.
- Future agents running the `repo-coherence-check` prompt (Step 2.5) that scan `/prompts/` for available instruction sets will not discover these subtask templates.
- The audit trail from Task → Prompt → Research breaks here: there is no forward link from Task 019's frontmatter to any prompt slug.

This deviation is pragmatically understandable: the subtasks were designed to be read inline by the orchestrating session, not executed as standalone prompts by a prompt-runner. The tri-partition model (`AGENTS.md §Task Type Routing`) was not designed with multi-agent fan-out subtask files in mind. This is a spec gap worth surfacing.

**Fix (spec-compliant):** Move each subtask file to `/prompts/<slug>/prompt.md`, add `prompt_kind: task-spec`, and update `task_uses_prompts` in `task.md`. This is a significant migration; a lighter alternative is to file a schema extension request (adding `type: subtask` or `type: agent-prompt` to the closed set) and reclassify in place.

**Recommended action:** File a follow-up Task to resolve the tri-partition gap for multi-agent subtask files, rather than silently leaving the current state as a permanent deviation.

---

## 3. Code-Quality Issue

### C1 — `--baseline` Writes Temp Files to `repo_root` (Low-Medium)

**Affected code:** `tools/fm/validate.py:_diags_for_baseline()`, lines ~413–426.

```python
with tempfile.NamedTemporaryFile(
        "w", suffix=".md", dir=repo_root, delete=False, encoding="utf-8") as tf:
    tf.write(result.stdout)
    tmp_path = Path(tf.name)
try:
    ...
finally:
    tmp_path.unlink(missing_ok=True)
```

Using `dir=repo_root` places the temp file inside the working tree, not in the OS temp directory. If the process is interrupted (SIGKILL, OOM, test runner abort), the `finally` block is skipped and orphan `.md` temp files accumulate in the repository root, appearing in `git status` and potentially triggering the governance linter on the next run.

The `dir=repo_root` argument is not needed for correctness: `classify_path(path, repo_root, ontology)` uses the original `path` for classification (the result is passed as `cls=` to `check_file`), so the temp file's location on disk does not affect the classification logic. Moving the temp file to `tempfile.gettempdir()` is safe and avoids the working-tree noise.

**Fix:**

```python
import tempfile, os
with tempfile.NamedTemporaryFile(
        "w", suffix=".md", dir=None, delete=False, encoding="utf-8") as tf:
```

(`dir=None` uses the OS temp directory, which is the default behaviour and the correct choice here.)

---

## 4. Medium-Grade Issues

### M1 — PR Body Overstates Legacy Retirement Scope (Medium)

The PR summary states: "Legacy shims: `tools/lint-linkage.py`, `tools/lint-structure.py`, `tools/validate-frontmatter.py` now forward to fm-validate with deprecation notices."

However, the friction log (Friction #5) correctly acknowledges:

> `lint-structure.py` / `check-trust.py` have no fm-* successor yet. Both still gate via the legacy code paths.

`tools/lint-structure.py` (the shim now at the original path) still delegates to the legacy implementation for structural-presence checks (does a slug folder have `task.md` / `readme.md`?). `tools/check-trust.py` still uses its own legacy detection for the friction-log FL[0-3] audit. These are not shims over `fm-validate`; they remain live legacy code.

The discrepancy between the PR body and the friction log creates a trust gap: a future agent reading only the PR body would believe the structural-presence and friction-log checks are fully migrated, when they are not.

**Fix:** The PR body SHOULD be amended to accurately state: "lint-linkage.py is a shim over fm-validate --type-check; lint-structure.py and check-trust.py remain legacy pending fm-* successors."

---

### M2 — Magic-String Sentinel `"REPLACE"` Not Documented in Ontology (Low-Medium)

**Affected code:** `tools/fm/validate.py:type_check()`, lines ~307–308 and ~320.

```python
if not ref or ref.startswith("REPLACE"):
    continue
```

The sentinel `"REPLACE"` is a hardcoded string that skips placeholder values in cross-reference fields. It is not declared in `maintenance/schemas/header-ontology.json`, not mentioned in the SPEC, and not visible to future agents generating frontmatter from templates. An agent that generates a different placeholder style (e.g., `"<slug>"`, `"TBD"`, `"TODO"`) would produce false-positive F.T.1 errors — and would have no way to discover the sentinel convention without reading the validator source.

**Fix:** Add a `"placeholder_sentinel"` key to the ontology (e.g., `"placeholder_prefix": "REPLACE"`) and drive the sentinel check from there. Alternatively, document the convention in `tools/fm/readme.md` and `templates/task.md`.

---

### M3 — `fm graph` Cycle Reports Include Benign Supersession Pairs (Low)

The governance check output (`tools/check-governance.sh` step 3) delegates to `fm-validate --type-check`, which does not surface `fm-graph` cycle results. But the friction log notes that "fm-graph cycles in the live tree (ST-2 surfaced 22): mostly legitimate supersession-chain reciprocity." This means `python3 tools/fm/graph.py --detect=cycles` currently produces ~22 reports that are not actionable, because `task_supersedes ↔ task_superseded_by` are two-element reciprocal pairs by design (per `TASK.md §4.7`).

A future operator running `fm graph --detect=cycles` would need to manually filter these out before finding any true cycle. The graph tool should distinguish "benign reciprocal pair" from "true cycle" using the ontology's `reciprocity.rules` to identify edge types that are definitionally bidirectional.

This is documented in the friction log's Suggested Follow-Ups section but not filed as a Task.

---

## 5. Systemic Process Gap

### P1 — FL3 Infrastructure Failure Not Filed as a Concrete Task

The friction log documents a significant infrastructure failure: the `Agent` tool's `isolation: "worktree"` placed agents on three different commit bases, causing four of nine planned subtask agents to fail or not deliver. The real cost was that the driver session absorbed ST-3, ST-5, ST-6, and ST-8 directly — making the actual execution mostly serial rather than the intended parallel fan-out.

This is documented under "Suggested Follow-Ups":

> **Worktree-base infrastructure hardening**: future multi-agent fan-out should specify the start commit explicitly, OR the driver should pre-flight check `git rev-parse HEAD` in each worktree and reject ones on the wrong base before issuing prompts.

A "Suggested Follow-Up" bullet is not a tracked, actionable item. Given that this pattern (multi-agent fan-out with `isolation: "worktree"`) is the only mechanism in the repository for parallel task decomposition, and given that the failure mode is deterministic and reproducible (not a one-time environment glitch), this warrants a concrete Task filed in `/tasks/`.

**Recommended action:** File `tasks/031-worktree-base-preflight-check/` (or the next available sequence number) with a goal of either (a) adding a pre-flight worktree-base check to the orchestration pattern documented in `subtasks/readme.md`, or (b) producing a hardened `fm-spawn` utility that pins the worktree to the current HEAD before dispatching an agent prompt.

---

## 6. Positive Findings

Despite the issues above, several implementation decisions merit explicit recognition:

1. **Falsification clauses per subtask.** Every subtask file carries a "Falsification" section asking "what observation would prove this subtask is the wrong cut?" This is a disciplined engineering practice that prevents scope creep and surface-area explosion. It should be canonised as a requirement in the subtask template.

2. **Lazy dispatch in `fm.py`.** The `_import_subcommand` function imports only the invoked submodule, keeping per-invocation startup cost proportional to the work done. This directly mitigates the ST-8 falsification risk and is the correct design for a multi-tool dispatcher.

3. **`diagnostic-explanations.json` architecture.** Linking diagnostic codes to structured `{what, why, fix}` rationale in a side JSON file — rather than embedding the rationale in the Python source or the SPEC — means the explanations can be updated without touching the validator logic. The CI guard (a test that verifies every emitted code has a matching explanation entry) prevents silent coverage drift.

4. **FL3 transparency.** The friction log is specific, factual, and complete. It names the exact commits that succeeded and failed, explains the root cause of each failure, and distinguishes "infrastructure fault" from "user error." This level of candour is operationally valuable and sets the right standard for future FL3 declarations.

5. **`--type-check` reciprocity edge case.** The decision to treat `prompt_relates_to_task: ""` as "shared / general" (skipping reciprocity assertion) rather than as a missing back-edge is precisely documented in the friction log and reflected in the test suite. This is the correct pragmatic resolution for prompts that serve multiple tasks.

---

## 7. Summary Table

| ID | Severity | Rule | Status |
|----|----------|------|--------|
| V1 | High | TASK.md §3.2 — `status: active` should be `completed` on closed task | Open — trivial fix |
| V2 | Medium-High | PROMPT.md §1 — subtask prompt files stored in wrong canonical location | Open — requires spec discussion or migration |
| C1 | Low-Medium | `_diags_for_baseline()` writes temp files into `repo_root` | Open — one-line fix |
| M1 | Medium | PR body overstates legacy retirement scope vs. friction-log truth | Open — PR body amendment |
| M2 | Low-Medium | `"REPLACE"` sentinel undocumented in ontology | Open — ontology amendment |
| M3 | Low | `fm graph --detect=cycles` conflates reciprocal pairs with true cycles | Open — follow-up Task |
| P1 | Process | FL3 worktree-base failure not filed as concrete Task | Open — file Task 031 |

---

## 8. Reviewer Friction Level

FL1 — Minor friction. The `--baseline` temp-file issue required reading the implementation in detail to rule out a set-difference correctness bug (the logic is correct; the directory choice is the only concern). All other findings emerged from first-pass reading of the PR body, friction log, and governance spec cross-references.
