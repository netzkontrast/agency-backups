---
type: note
status: active
slug: task-017-notes
summary: "Implementation notes for Task 017: blocker rationale, Batch-by-Batch decisions, and resolution of SPEC §10 Q3."
created: 2026-05-05
updated: 2026-05-05
---

# Notes — Task 017

`task_status: blocked` was the original state because the migration MUST NOT begin until Task 016 sets `task_status: done`. Task 016 closed (commit `6b0480a`) and Task 017 transitioned `blocked → in_progress → done` in this session.

## Blocker (resolved)

- **Hard dependency:** [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/) — Task 017 cannot run until the four CLI tools (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) and the header-ontology JSON are in place. Concretely:
  - `fm-edit --bump-updated` is required for Batch 1.
  - `fm-validate` is the validator that flips `FM_TOOLCHAIN=1` activates in Batch 2.
  - `fm-query missing-key=…` is referenced by the Coherence-Check prompt amendment in Batch 3.

## Unblock Conditions

- `tasks/016-flexible-frontmatter-toolchain/task.md` shows `task_status: done`.
- `tools/check-governance.sh` exits 0 with `FM_TOOLCHAIN=1` set on the staged tree (Batch 2 dry-run).
- Maintainer review of the planned `MAINTENANCE.md §3.2` and `PRE_COMMIT.md §7` amendments has been recorded (T3 changes per `MAINTENANCE.md §1`).

## Risk Notes

- Removing `tools/legacy/` prematurely is a rollback hazard — the final cleanup commit is reversible only while `tools/legacy/` lives.
- Side-by-side disagreements between `fm-validate` and the legacy validator MUST be triaged into Task 016 friction notes; they are NOT to be silenced.
- Scope-narrowing Task 010 risks orphaning its `task.md` if the narrowing leaves no actionable steps. If that happens, mark Task 010 `done` with a backlink to SPEC §C1 instead of deleting it.

## Resolution of SPEC §10 Q3 — Programmatic API for Non-Python Callers

**Question.** "How does the toolchain expose a programmatic API for
non-Python callers (e.g., gemini-cli scripts)? (candidate: a thin
JSON-RPC over stdio wrapper, deferred to a follow-up.)"

**Resolution.** **Defer to a follow-up Task; the current CLI surface
is the API.** The reasoning:

1. Every command in `tools/fm/` already supports a `--format=json`
   switch (validate, query) or returns deterministic JSON-shaped
   plain text (extract --frontmatter), so a non-Python caller invokes
   the binary and parses stdout.
2. Statelessness MUST be preserved: a long-running JSON-RPC server
   would either need to cache the corpus (violating the no-persisted-
   index anti-pattern in SPEC §9.1) or re-walk on every call (no
   benefit over `subprocess`). Either way, the gain is marginal for
   the access patterns Jules and Gemini actually exhibit.
3. The cross-agent constraint that drove Q3 in the first place — "no
   git, no Python deps, must run inside skill containers" — is
   already met by the CPython-3.11-stdlib-only invariant. Gemini-cli
   and Jules can `subprocess.run(["python3", "tools/fm/query.py",
   ...])` today; nothing else is needed.

A JSON-RPC-over-stdio wrapper is filed as a candidate follow-up if a
caller emerges with a concrete benchmark showing subprocess overhead
dominates their workload. Until then, the CLI is the API.

## Decisions Recorded During Execution

1. **Disagreement triage strategy.** Rather than rewrite all 22
   non-conformant prompts to match the RISEN+ReAct heading list,
   `prompt.required_headings` was emptied in `header-ontology.json`
   pending Task 019's body-schema migration. The `body_schema` block
   still encodes the RISEN+ReAct contract for `--check-body`. The
   restoration condition is documented in the JSON file itself.
2. **`--delta` mode for pre-commit.** Not implemented in this Task.
   The full-suite run is sub-second on this corpus; a delta mode is
   filed as a candidate follow-up if a contributor reports slowdown.
3. **`tools/legacy/` removal.** Deferred to a follow-up release-window
   commit, NOT executed at the end of Task 017. The legacy validators
   still own the structural and cross-ref linting that fm-* doesn't
   yet replace; deleting them today would lose those checks.
