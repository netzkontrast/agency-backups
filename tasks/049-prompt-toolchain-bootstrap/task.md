---
type: task
status: active
slug: prompt-toolchain-bootstrap
summary: "Port the prompt-optimizer skill primitives (intent classifier, 5-dim evaluator) into stateless tools/prompt/ CLIs and add an audit orchestrator that runs the Task 034 ST-2 + ST-3 linters together with RFC-2119 polarity. Mirrors the tools/fm/* pattern; foundation for a future prompts-author skill that pipelines /prompts/<slug>/ creation analogously to research-prompt-optimizer."
created: 2026-05-07
updated: 2026-05-07
task_id: "049"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/prompt/
  - tools/check-governance.sh
  - README.md
  - PROMPT.md
---

# Task 049 — Prompt Toolchain Bootstrap

## Goal

Ship a `tools/prompt/` toolchain that mirrors `tools/fm/` (stateless single-file CLIs, stdlib + minimal deps) and lifts the algorithmic ground truth from `skills/prompt-optimizer/scripts/` (intent classification + 5-dimension evaluation) so authoring and auditing a `/prompts/<slug>/prompt.md` becomes one orchestrated pipeline rather than three separate WARN-tier checks. The Task is `done` when **`python3 tools/prompt/audit.py prompts/<slug>/prompt.md`** produces a single Markdown report combining (a) the Task 034 ST-2 self-containedness diagnostic, (b) the Task 034 ST-3 framework-declaration diagnostic, (c) the RFC-2119-polarity advisory, and (d) the 5-dimension prompt-quality score from the ported `evaluate.py` — and the orchestrator is wired into `tools/check-governance.sh` as a single `[opt]` row replacing the two Task 034 rows.

## Context

Task 034 shipped two WARN-tier linters (ST-2 self-containedness, ST-3 framework declaration) plus the §4.3 framework-selection decision tree in PROMPT.md. The decision tree's algorithmic ground truth already exists at `skills/prompt-optimizer/scripts/intent_classifier.py` (27-framework catalog, 7-intent classifier) and `skills/prompt-optimizer/scripts/prompt_evaluator.py` (5-dimension rubric). Today these scripts run only inside the `prompt-optimizer` skill's mental model — there is no CLI an agent or pre-commit hook can call to enforce them mechanically.

`skills/research-prompt-optimizer/` provides the architectural template: a 5-phase pipeline with three approval gates, a YAML-driven render path (`render/render.py`), and a `catalog.yaml` of categories/methods/frameworks. That pattern is heavyweight; this Task's first cut adopts only the audit + select-framework slice and leaves the renderer + skill-side pipeline as stretch goals.

## Preconditions (satisfied at branch-time)

- **Task 034** (`prompt-spec-integration`, done) — ships ST-2 + ST-3 linters that this Task's `audit.py` orchestrator wraps.
- **Task 016/017** — flexible-frontmatter toolchain provides the `tools/fm/_core.py` import surface the new CLIs reuse.
- **`skills/prompt-optimizer/`** — the source of the intent classifier and 5-dimension evaluator that ST-2 and ST-3 lift.

## Build-On

- `skills/prompt-optimizer/scripts/intent_classifier.py` — 7-intent keyword classifier; lifts into `tools/prompt/select-framework.py`.
- `skills/prompt-optimizer/scripts/prompt_evaluator.py` — 5-dimension rubric; lifts into `tools/prompt/evaluate.py`.
- `tools/check-prompt-self-containedness.py` (Task 034 ST-2) — composed by the audit orchestrator.
- `tools/check-prompt-framework-declaration.py` (Task 034 ST-3) — composed by the audit orchestrator.
- `tools/check-rfc2119-polarity.py` (Task 032 ST-3) — composed by the audit orchestrator.
- `tools/fm/new.py` — already covers the scaffold step; this Task references but does not duplicate it.
- `templates/prompt.md` — canonical seed for the rendered prompt body.

## Plan

1. **Phase A (parallel) — Port the two scripts.**
   - **ST-1 (port-intent-classifier):** lift `skills/prompt-optimizer/scripts/intent_classifier.py` into `tools/prompt/select-framework.py`. CLI: `python3 tools/prompt/select-framework.py <brief.md|->`. Output: a single line `framework=<RISEN|RISE-DX|ReAct|RISEN+ReAct|CoT> rationale="<one sentence>"`. Tightens the 27-framework catalog to the canonical 5 from PROMPT.md §4.3 (no new tokens introduced — falsification clause caps at +0).
   - **ST-2 (port-evaluator):** lift `skills/prompt-optimizer/scripts/prompt_evaluator.py` into `tools/prompt/evaluate.py`. CLI: `python3 tools/prompt/evaluate.py <prompt.md>`. Output: a JSON-or-Markdown 5-dimension scorecard (Clarity/Specificity/Context/Completeness/Structure, 0–10 each) plus a `gaps` and `improvements` list per the source rubric.
2. **Phase B (sequential, depends on Phase A) — Audit orchestrator.**
   - **ST-3 (audit-orchestrator):** ship `tools/prompt/audit.py` that runs ST-2 (Task 034) + ST-3 (Task 034) + `check-rfc2119-polarity.py` + the new `evaluate.py` in sequence and emits a single `prompts/<slug>/audit.md` report. Exit codes mirror the WARN-tier convention (0 pass, 2 WARN). Wire into `tools/check-governance.sh` as one `[opt]` row replacing the two Task-034 rows (no behaviour change at the gate; one less line of script).
3. **Phase C (sequential, depends on B) — Spec sync.**
   - Update **README.md §6** linter table: remove the two Task-034 rows, add one row for `tools/prompt/audit.py`.
   - Update **PROMPT.md §6.0** mapping table the same way.
   - Add a **`tools/prompt/readme.md`** describing the four CLIs (select-framework, evaluate, audit, future render) — mirror `tools/fm/readme.md`'s shape.
4. **Phase D (sequential, depends on C) — Tests + close.**
   - `tests/test_select_framework.py` — covers each of the 5 canonical frameworks plus an "ambiguous brief" path.
   - `tests/test_prompt_evaluate.py` — covers each of the 5 dimensions and a synthetic high-quality vs. low-quality prompt.
   - `tests/test_prompt_audit.py` — end-to-end on a fixture prompt; asserts the four sub-reports appear.
   - Run `tools/check-governance.sh`; close per TASK.md §7.7 (friction-log).

## Falsification

Wrong cut **iff** any of:

1. The ported `select-framework.py` recommends a framework outside the canonical 5-set defined in PROMPT.md §4.3 on >5% of a synthetic 100-brief test corpus. (The classifier MUST honour the closed set; the upstream skill catalogues 27 frameworks but only 5 ship as canonical here.)
2. The audit orchestrator's runtime exceeds 2× the sum of the four sub-linters run in series. (Composition MUST NOT introduce material overhead.)
3. The audit orchestrator's WARN output cannot be deterministically diffed across two runs against the same prompt. (Non-determinism breaks pre-commit reproducibility.)

## Stretch — Deferred to a Successor Task

The following are intentionally OUT OF SCOPE for the first cut and SHOULD spawn a successor task once the audit orchestrator has a few months of corpus exposure:

- **`tools/prompt/render.py`** — YAML-driven renderer mirroring `skills/research-prompt-optimizer/render/render.py`. Doubles the schema surface; deferred until reauthoring volume justifies it.
- **`tools/prompt/query.py`** — convenience wrapper around `tools/fm/query.py` for prompt-specific selectors (`framework=`, `kind=`, `relates-to-task=`). Skills-query (Task 022) is the precedent.
- **`skills/prompts-author/`** — full 5-phase + 3-gate skill that pipelines intent capture → framework selection → render → audit → finalize. Builds atop the CLIs landed by this Task.

## Todo

- [ ] 1. Phase A — dispatch ST-1 (port-intent-classifier) and ST-2 (port-evaluator) in parallel.
- [ ] 2. Phase B — dispatch ST-3 (audit-orchestrator) once Phase A lands.
- [ ] 3. Phase C — sync README.md §6 + PROMPT.md §6.0 + author `tools/prompt/readme.md`.
- [ ] 4. Phase D — author tests, run `tools/check-governance.sh`, friction-log, close.
- [ ] 5. Update `tasks/readme.md` Task 049 entry to `done` with shipped artefact summary.

## Links

- Predecessor (closes the corpus inconsistency that motivates the orchestrator): [Task 034 — prompt-spec-integration](../034-prompt-spec-integration/task.md).
- Source skill (algorithmic ground truth): [`skills/prompt-optimizer/SKILL.md`](../../skills/prompt-optimizer/SKILL.md).
- Architectural template (5-phase pipeline shape): [`skills/research-prompt-optimizer/SKILL.md`](../../skills/research-prompt-optimizer/SKILL.md).
- Spec discipline reference: [`skills/spec-skill/SKILL.md`](../../skills/spec-skill/SKILL.md).
- Sibling toolchain (the pattern this Task mirrors): [`tools/fm/`](../../tools/fm/).
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`FOLDERS.md`](../../FOLDERS.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md).
