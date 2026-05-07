---
type: index
status: active
slug: task-050-folder
summary: "Folder index for Task 050 — prompt-toolchain bootstrap. Ports the prompt-optimizer skill primitives into stateless tools/prompt/ CLIs and adds an audit orchestrator combining the Task 034 ST-2 + ST-3 linters with RFC-2119 polarity and a 5-dimension quality score."
created: 2026-05-07
updated: 2026-05-07
---

# Task 050 Folder

## What

Operational folder for Task 050, which establishes a `tools/prompt/` toolchain mirroring `tools/fm/`. The first cut lifts two scripts from `skills/prompt-optimizer/scripts/` (`intent_classifier.py` → `select-framework.py`, `prompt_evaluator.py` → `evaluate.py`) and adds an `audit.py` orchestrator that composes the existing Task 034 ST-2 / ST-3 linters with the Task 032 RFC-2119 polarity advisory and the new evaluator. Renderer + query wrapper + companion skill are explicitly deferred to a successor task.

## Files

- [`task.md`](./task.md) — Goal, Plan, Falsification, Stretch, Todo.

## Assumptions Log

- The 27-framework catalog inside `skills/prompt-optimizer/` is treated as a superset reference; only the 5 canonical PROMPT.md §4.3 values (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`) ship in `tools/prompt/select-framework.py`. Extending beyond this set MUST go through an ADR amending PROMPT.md §4.3.
- `skills/prompt-optimizer/scripts/intent_classifier.py` and `prompt_evaluator.py` are the canonical algorithmic ground truth and are copy-portable; this Task does NOT re-derive their logic.
- `tools/check-prompt-self-containedness.py` and `tools/check-prompt-framework-declaration.py` (shipped by Task 034) keep their independent CLI surfaces; the `audit.py` orchestrator composes them via subprocess, not via in-process import, so each linter remains independently runnable from a pre-commit hook.
- The `tools/check-governance.sh` advisory rows for the two Task 034 linters are replaced by a single advisory row pointing at `audit.py`; the gate's behaviour at the WARN-tier MUST remain unchanged (no new ERRORs, no removed checks).
