---
type: task
status: active
slug: adr-tooling-impl
summary: "Successor to Task 028 (plan-only). Implements the agency-adr CLI suite (validate / synthesize), tests, GitHub Actions workflow, governance hook integration, and AGENTS.md guarded-section markers per the build contract in tasks/028-adr-tooling-impl-plan/implementation-plan.md."
created: 2026-05-06
updated: 2026-05-06
task_id: "031"
task_status: in_progress
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - adr-tooling-impl
task_spawns_research: []
task_spawns_prompts: []
task_supersedes: []
task_blocked_by:
  - "028"
task_affects_paths:
  - tools/adr/
  - tests/adr/
  - .github/workflows/adr-validate.yml
  - decisions/
  - AGENTS.md
  - PRE_COMMIT.md
  - FOLDERS.md
  - maintenance/schemas/header-ontology.json
  - maintenance/schemas/diagnostic-explanations.json
  - tools/check-governance.sh
  - prompts/adr-tooling-impl/
  - tasks/031-adr-tooling-impl/
---

# Task 031 — ADR Tooling Implementation

## Goal

Land the `agency-adr` CLI suite specified by [Task 028's implementation plan](../028-adr-tooling-impl-plan/implementation-plan.md), end-to-end: every module under `tools/adr/`, every test under `tests/adr/`, the `.github/workflows/adr-validate.yml` workflow, the `tools/check-governance.sh` step, the `PRE_COMMIT.md §7.C` documentation, the `AGENTS.md` guarded-section markers, and the `types.adr` registration in `header-ontology.json`. The Task is **done** when (a) `tools/check-governance.sh` and the full pytest suite both exit 0 against the implementation, (b) PR #67's review findings T.1–T.4 are applied, and (c) PR [#67](https://github.com/netzkontrast/agency/pull/67) merges to `main` with the `adr-validate` GitHub Actions job green.

## Plan

1. Audit the existing tooling surface (`tools/fm/_core.py`, `tools/check-governance.sh`, `header-ontology.json`) to confirm reuse boundaries per ADR.A.5.9.
2. Implement phase-1 modules: `__init__.py`, `schema.py`, `body.py`.
3. Implement phase-2 modules: `corpus.py`, `graph.py`, `ids.py`.
4. Implement phase-3 modules: `extract.py`, `compress.py`, `fidelity.py`.
5. Implement phase-4 modules: `synthesize.py`, `runlog.py`.
6. Implement phase-5: `cli.py`, `tools/adr/readme.md`.
7. Author every test file in `tests/adr/` per the §3 acceptance test map; ensure each scenario carries a `# anchor: ADR.A.<aspect>.<stmt>` comment.
8. Register `types.adr` in `maintenance/schemas/header-ontology.json` with the §7.4 JSON-Schema; add the `decisions/<NNNN>-*.md` path classification rule.
9. Add `/decisions/` to the §8 non-operational table in `FOLDERS.md`; seed `decisions/readme.md`.
10. Insert `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers in `AGENTS.md` (OD.6 — placed in a new `## Synthesised ADR Constraints` section).
11. Wire the validator into `tools/check-governance.sh` as numbered step `[5/5]`; renumber downstream steps.
12. Add `PRE_COMMIT.md §7.C` documenting the validator's diagnostic codes and remedies.
13. Author `.github/workflows/adr-validate.yml` per plan §4 (governance gate + dry-run synthesis + diff gate against committed `AGENTS.md`).
14. Apply PR #67 review findings T.1 (count_tokens BPE divergence note), T.2 (stdout/stderr split docs), T.3 (`decisions_root: Path | None = None`), T.4 (cycle-detection dedup).
15. Verify: `python3 -m pytest tests/` and `tools/check-governance.sh` both exit 0; commit and push.

## Todo

- [x] 1. Audit tooling primitives.
- [x] 2. Implement phase-1 modules.
- [x] 3. Implement phase-2 modules.
- [x] 4. Implement phase-3 modules.
- [x] 5. Implement phase-4 modules.
- [x] 6. Implement phase-5 modules.
- [x] 7. Author the `tests/adr/` suite (49 cases mapping to every Gherkin anchor).
- [x] 8. Register `types.adr` in `header-ontology.json`.
- [x] 9. Add `/decisions/` to `FOLDERS.md` + seed `decisions/readme.md`.
- [x] 10. Insert AGENTS.md markers.
- [x] 11. Wire `tools/check-governance.sh` step `[5/5]`.
- [x] 12. Document `PRE_COMMIT.md §7.C`.
- [x] 13. Author `.github/workflows/adr-validate.yml`.
- [x] 14. Apply PR #67 review T.1–T.4 fixes.
- [x] 15. Run pytest + governance gate; commit; push (commits `97719e7`, `1643110`, `01c8a96`, `6a30991`).
- [ ] 16. PR #67 `adr-validate` CI job exits 0 on the head commit.
- [ ] 17. PR #67 merges to `main`; flip `task_status: done` and finalise [`./friction-log.md`](./friction-log.md).

## Links

- [`./friction-log.md`](./friction-log.md) — closure friction log.
- [`../028-adr-tooling-impl-plan/implementation-plan.md`](../028-adr-tooling-impl-plan/implementation-plan.md) — build contract this Task executes.
- [`../028-adr-tooling-impl-plan/task.md`](../028-adr-tooling-impl-plan/task.md) — predecessor Task (plan only).
- [`../028-adr-tooling-impl-plan/pr67-review.md`](../028-adr-tooling-impl-plan/pr67-review.md) — review findings addressed in commit `6a30991`.
- [`../../prompts/adr-tooling-impl/prompt.md`](../../prompts/adr-tooling-impl/prompt.md) — task-spec prompt for this implementation.
- [`../../research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) — governance spec (Task 027 output).
- [`../../tools/adr/readme.md`](../../tools/adr/readme.md) — `agency-adr` package index.
