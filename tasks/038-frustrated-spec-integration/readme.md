---
type: index
status: active
slug: task-038-folder
summary: "Folder index for Task 038 — FRUSTRATED.md spec integration. Justifies the FL0-mandatory rule with research-backed evidence, mechanically gates the FL declaration on commit, and adds Gherkin acceptance criteria."
created: 2026-05-06
updated: 2026-05-07
---

# Task 038 Folder

## What

Operational folder for Task 038. Closed `task_status: done`; the §28-vs-PRE_COMMIT.md-§2 reconciliation is delegated to Task 037 ST-4 per the joint-commit clause (see [`friction-log.md`](./friction-log.md) §1).

## Files

- [`task.md`](./task.md) — closure spec; all 8 Todo items checked off.
- [`friction-log.md`](./friction-log.md) — FL1; documents the §28 deferral, the `set -e` unblock fix, and the two historical malformed logs.
- [`subtasks/`](./subtasks/) — 1 research, 1 tooling, 1 spec amendment (subtask pointers; deliverables landed under `/research/`, `/tools/`, and `/FRUSTRATED.md`).

## Deliverables Landed

- [`research/fl0-value-justification/output/SPEC.md`](../../research/fl0-value-justification/output/SPEC.md) — 60-log empirical study; 38% FL0 / 50% FL1 / 10% FL2 / 2% FL3; verdict MANDATE-FL0; drop-in §FL.0 paragraph.
- [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) + [`tools/tests/test_fl_declaration.py`](../../tools/tests/test_fl_declaration.py) — 28 tests; 14 variant forms accepted; advisory-tier in `tools/check-governance.sh`; promote with `FM_FL_DECLARATION_STRICT=1`.
- [`FRUSTRATED.md`](../../FRUSTRATED.md) — §"Why FL0 is mandatory", §"Mechanical Enforcement", 4 Gherkin scenarios anchored FR.B.1–FR.B.4, plus an example §"Frustration Log" so the spec self-tests.

## Assumptions Log

- The FL0 justification subtask analyses *every* `friction-log.md` in the repo (40 task closures + 20 research-reflection runs = 60) — no sampling. Empirical signal: 23 FL0 / 30 FL1 / 6 FL2 / 1 FL3.
- The FL declaration linter parses BOTH `/research/<slug>/reflection/friction-log.md` AND task-folder `friction-log.md`, with PR-description `## Frustration Log` section as a fallback per FRUSTRATED.md §FL.Log.1 / §FL.Log.2.
- The §28-vs-PRE_COMMIT.md-§2 byte-identicality clause is owned by Task 037 ST-4. No §28 edit was made in this Task; Task 037 will lift the existing prose verbatim.
- The two historical malformed logs (tasks 030, 033) are intentionally NOT remediated in this PR — that work will accompany the eventual `FM_FL_DECLARATION_STRICT=1` flip.
- The Task 040 §A row §7 "Reflexion pattern" merge is not lifted — the cited source (`research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md`) is not present in this branch; lifting a non-existent source would invent content.
