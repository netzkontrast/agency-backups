---
type: note
status: active
slug: 053-triage
summary: "Triage matrix mapping each B.1-B.10 finding from research/core-architecture-review-2026-05/output/REPORT.md to its owning Task (existing or newly opened). One row per finding; dispatch decisions are final."
created: 2026-05-07
updated: 2026-05-07
---

# Task 053 — Triage Matrix

This file closes Plan step 2 / 4 of [`task.md`](./task.md). One row per "What's Bad" finding from [`research/core-architecture-review-2026-05/output/REPORT.md`](../../research/core-architecture-review-2026-05/output/REPORT.md), dispatched against the live `tasks/readme.md` index at branch-time.

## Matrix

| Finding | Subject | Owning Task (existing) | Residual Gap | Dispatch Decision | New Task Slot |
|---|---|---|---|---|---|
| **B.1** | Dual-toolchain transition debt | [017](../017-migrate-repo-to-flexible-toolchain/) `done`, [019](../019-fm-toolchain-suite-integration/) `done` | `tools/check-governance.sh:33` still defaults to legacy-as-gate; `FM_TOOLCHAIN` env var still present | `open-new` (residual cleanup) | [054-flip-fm-toolchain-default](../054-flip-fm-toolchain-default/) |
| **B.2** | `LOOP_LOG` runtime state in `AGENTS.md` (R.19 violation) | — | None — fully unowned | `open-new` | [055-relocate-agents-loop-log](../055-relocate-agents-loop-log/) |
| **B.3** | Duplicate `task_id`s (006/006, 009/009, 031/031, 032/032) | [043](../043-renumber-duplicate-task-ids-v3/) `open` (renumber); [033](../033-task-spec-integration/) `done` ST-3 (advisory linter) | None — both renumber and prevention are owned | `existing` | — |
| **B.4** | No CI/CD (deleted `adr-validate.yml`, no replacement) | [046](../046-github-workflow-research/) `open` | None — research+decision+ship all in 046 scope | `existing` | — |
| **B.5** | Narrative ontology scope creep | — | `NO.5` is a load-discipline workaround, not a structural fix | `open-new` (ADR-class) | [056-narrative-skills-extraction-adr](../056-narrative-skills-extraction-adr/) |
| **B.6** | Spec proliferation (9+ root specs at session boot) | [044](../044-improve-maintenance-spec-may-07-2026/) `open`, [045](../045-readme-coherence-refresh/) `open` (neither targets consolidation) | Consolidation evaluation unowned | `open-new` (ADR-class) | [057-root-spec-consolidation-adr](../057-root-spec-consolidation-adr/) |
| **B.7** | `read_fm()` silent `{}` on parse error | — | None — fully unowned | `open-new` | [058-read-fm-warn-diagnostic](../058-read-fm-warn-diagnostic/) |
| **B.8** | Research immutability is absolute (no T1/T2 repair on closed research) | — | None — fully unowned | `open-new` | [059-closed-research-repair-allowance](../059-closed-research-repair-allowance/) |
| **B.9** | Closing procedure is `/sc:createPR`-specific | — | Asymmetry penalises Jules + Gemini | `open-new` | [060-platform-agnostic-closing-procedure](../060-platform-agnostic-closing-procedure/) |
| **B.10** | No end-to-end integration test | — | `tests/fm/` covers atomic tools only | `open-new` | [061-governance-integration-test-scaffold](../061-governance-integration-test-scaffold/) |

## Dispatch Summary

- **8 new Tasks opened:** 054, 055, 056, 057, 058, 059, 060, 061 (one per `open-new` row, slots discovered at commit-time per [TASK.md §8.1](../../TASK.md)).
- **5 existing Tasks cited:** 017, 019, 033, 043, 046.
- **0 findings dropped or merged.** Every B-row has a single owner.

## Reciprocity Audit

Each new Task's `task.md` cites Task 053 by relative path under `## Links`. Task 053's frontmatter references the prompt and research workspace via `task_uses_prompts: [core-architecture-review-2026-05]` and `task_spawns_research: [core-architecture-review-2026-05]` — closing the audit chain Task → Prompt → Research that PR #86 review **D1** flagged as broken in the original commit set.
