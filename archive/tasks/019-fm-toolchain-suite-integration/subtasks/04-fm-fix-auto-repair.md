---
type: note
status: draft
slug: task-019-st4-fm-fix
summary: "Subtask ST-4: ship tools/fm/fix.py — a tier-tagged auto-repair driver that converts fm-validate diagnostics into safe T1/T2 mutations applied via fm-edit, refusing T3/T4 and writing a Task stub instead."
created: 2026-05-05
updated: 2026-05-05
---

# ST-4: `fm-fix` — T1/T2 Auto-Repair Driver

## Goal

Ship `tools/fm/fix.py` that consumes `fm-validate` diagnostics and, for each one, emits a fix proposal: T1/T2 fixes are applied via `fm-edit` automatically; T3/T4 findings are written to a draft `tasks/<NNN>-fix-<slug>/task.md` stub and reported to the operator. Closes the loop between "validator says it's broken" and "tool fixes it" — without ever crossing the tier ladder.

## Falsification

Wrong cut **iff** T1/T2 repairs cluster too tightly with T3 changes that no auto-repair can safely apply (i.e., the safe set is empty or trivially small). Mitigation: scope to a closed set of repair recipes (one per F.* code), and refuse anything outside the set with an explicit "T3 — file a Task" message.

## Inputs

- [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §5.1 (diagnostic codes), §7.2 (tier ladder), §12.4 (F.B.* codes).
- [`/MAINTENANCE.md`](../../../MAINTENANCE.md) §1 (T1/T2/T3/T4 definitions; check the updated mutation-surface column).
- [`/tools/fm/validate.py`](../../../tools/fm/validate.py) — the diagnostic source.
- [`/tools/fm/edit.py`](../../../tools/fm/edit.py) — the mutation surface.

## Acceptance Criteria

1. **Surface.** `tools/fm/fix.py [PATH ...] [--dry-run] [--apply] [--code F.X.Y[,F.A.B...]]`. `--dry-run` is default; `--apply` actually writes.
2. **Repair recipes (closed set, T1/T2 only).** At minimum:
   - `F.3.1 missing L1 key 'updated'` → `fm-edit --bump-updated` (T1)
   - `F.3.1 missing L1 key 'created'` → `fm-edit --set created=<today-utc>` (T1)
   - `F.3.2 missing L2 list key` → `fm-edit --append-list <key>` with empty value (T2; produces `key: []`)
   - `F.3.3 type 'X' disagrees with path-expected type` → emit Task stub (T3)
   - `F.3.4 unknown key 'tpye' — did you mean 'type'?` → emit Task stub (T3, requires content review)
   - `F.4.2 missing required heading '## Foo'` → emit Task stub (T3, body authoring)
3. **T3 stub generation.** When a finding is T3, write `tasks/<NNN>-fix-<slug>/task.md` with `task_status: draft`, `task_priority: P3`, the diagnostic embedded, and a one-line plan. Use the next-free task id (mirror the `fm-new` allocation if available; otherwise scan tasks/ inline).
4. **Tests.** New file `tests/fm/test_fix.py`. Cover: each recipe, the T3 stub path, `--dry-run` (no writes), `--apply` (writes), and the closed-set refusal (an unknown F.* code → exit 4).
5. **Output.** Default summary line: `Fixed N (T1=A, T2=B); deferred to Tasks: M; refused: K.`

## Dependencies

None. Phase A. (If ST-3 lands first, you MAY reuse its next-id allocator; otherwise inline.)

## Estimated Effort

Medium (~180 LOC + 150 LOC tests).

## Agent Prompt

```text
You are implementing tools/fm/fix.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe.

Repo root: /home/user/agency

Context files (read first):
  - research/flexible-frontmatter-toolchain/output/SPEC.md  (§5.1, §7.2, §12.4)
  - MAINTENANCE.md                                          (§1 tier ladder + canonical mutators)
  - tools/fm/validate.py                                    (diagnostic source)
  - tools/fm/edit.py                                        (mutation surface)
  - tools/fm/_core.py

Acceptance criteria:
  1. tools/fm/fix.py [PATH ...] [--dry-run | --apply] [--code F.X.Y[,…]]
     Default --dry-run.
  2. Closed-set recipe table covering at minimum the codes listed in the
     subtask file (F.3.1/2/3/4, F.4.2). Anything outside the set → T3 stub.
  3. T3 stub: tasks/<NNN>-fix-<slug>/task.md with task_status: draft,
     task_priority: P3, the diagnostic line, a one-step plan, and a Goal.
     The stub MUST itself pass fm-validate.
  4. Atomic per-file: gather all repairs for a given path, take the FileLock
     once, apply via subprocess to fm-edit (or by importing edit.apply_edit),
     release. No partial application.
  5. Tests in tests/fm/test_fix.py — every recipe + T3 path + dry-run/apply
     contrast + unknown-code refusal.
  6. Final summary line printed to stdout: "Fixed N (T1=A, T2=B); deferred
     to Tasks: M; refused: K."

Constraints:
  - Python 3.11 stdlib only.
  - Reuse fm-edit's apply_edit by importing, NOT by shelling out (faster, lockable).
  - Do NOT modify other tools/fm/*.py modules' public surfaces.

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - python3 tools/validate-frontmatter.py
  Commit "feat(fm/fix): T1/T2 auto-repair driver with T3 stub generation (Task 019 ST-4)".
  Do NOT push.
```
