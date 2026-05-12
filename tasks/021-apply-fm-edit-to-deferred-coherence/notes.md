---
type: note
status: active
slug: task-021-notes
summary: "Residual capture for Task 021. Post-Task-017 baseline: zero F.3.1/F.3.2 (missing-key) diagnostics across the corpus. The plan's batch-mutator step has no inputs to consume; the Task closes administratively."
created: 2026-05-05
updated: 2026-05-05
---

# Task 021 — Residual Capture

## Method

Per `task.md` Plan step 2, capture the residual missing-key set on top of Task 017's migrated tree:

```
$ python3 tools/fm/validate.py 2>&1 | grep -E "F\.3\.[12]"
(no output)

$ python3 tools/fm/validate.py
Checked 252 files; 0 diagnostic(s).
```

## Result

**Empty.** Task 017 (`migrate-repo-to-flexible-toolchain`, end_commit `b73e615`) and Task 019 (toolchain integration) already drove every operational file under `/research/`, `/skills/`, `/tasks/`, `/maintenance/`, `/prompts/`, and `/specs/` to F.3-clean. Task 020 (prompt RISEN+ReAct conformance) closed the F.4.x heading drift on top.

Baseline used: HEAD = `0669322` (Task 020 closure merge).

## Out of Scope

`fm-validate --check-body` still reports F.B.1 / F.B.7 diagnostics across `/tasks/`. Those are body-shape (paragraph/ordered_list/link_list) mismatches, not missing-key (F.3.1/F.3.2). They are explicitly the remit of SPEC §12.6 Phase 3 and Task 020's friction-log FL2 follow-up, **not** Task 021's mission per `task.md` Goal: "zero `F.3.1` / `F.3.2` (missing-key) diagnostics."

## Decision

The Task closes with `task_status: done`. No `tools/fm/edit.py` invocations were needed — the goal predicate evaluated true at the moment Task 017 merged. The Task's value is the residual-confirmation gate itself: had Task 017's migration left stragglers, this Task would have absorbed them with `fm-edit`. It did not.

## Pointers

- Predecessor (superseded): [`../005-address-deferred-coherence-issues/task.md`](../005-address-deferred-coherence-issues/task.md)
- Blocker (now `done`): [`../017-migrate-repo-to-flexible-toolchain/task.md`](../017-migrate-repo-to-flexible-toolchain/task.md)
- Co-clearing peers: Task 019, Task 020 (Task 020 reduced fm-validate to 0 across 252 files).
- Phase 3 follow-up holder: [`../020-audit-prompt-fm-validate-conformance/friction-log.md`](../020-audit-prompt-fm-validate-conformance/friction-log.md) §FL2.
