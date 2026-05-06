---
type: note
status: draft
slug: task-037-st1-research-pre-commit-readme-update-cadence
summary: "Subtask ST-1 (research head, shared interest with Task 038): produce the canonical readme-update cadence rule that reconciles FRUSTRATED.md §28 (batch at pre-commit, FL2 if per-file) with PRE_COMMIT.md §2 ('update every touched folder NOW'); back the recommendation with token-cost evidence on the existing corpus."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — Pre-Commit Readme-Update Cadence

## Goal

Produce `research/pre-commit-readme-update-cadence/output/SPEC.md` that resolves the contradiction surfaced by the spec audit. Output: (a) a single normative rule on when readme.md is updated (immediate / batched-at-pre-commit / hybrid), (b) token-cost data backing the choice, (c) verbatim before/after wording for FRUSTRATED.md §28 and PRE_COMMIT.md §2.

## Falsification

Wrong cut **iff** any choice yields >2× token cost vs. status quo. Mitigation: existing closed tasks already have an emergent practice; the research can codify the cheapest one.

## Phase 1 Intent

```yaml
research_question: >-
  When during a session MUST a touched folder's readme.md be updated:
  immediately on each touch, batched at pre-commit, or a hybrid? What
  wording reconciles FRUSTRATED.md §28 (FL2 trigger for per-file
  updates) with PRE_COMMIT.md §2 (every touched folder MUST be
  updated NOW)?
research_question_unpacked: >-
  This is NOT a tooling question (no linter changes either rule). It
  is a wording-reconciliation question backed by token-cost evidence
  from real sessions.
audience: maintainers authoring Task 037 + Task 038 spec amendments
output_format: structured Markdown SPEC.md with §1 cadence options + token-cost table, §2 normative recommendation, §3 verbatim before/after wording for both specs, §4 example walkthrough on a recent session
temporal_scope: {from: "2026-05-04", to: "2026-05-06"}
language: en
depth: standard
success_criterion: >-
  One cadence chosen with quantitative justification; before/after
  wording fits within existing §28 / §2 line budgets without
  restructuring; recommendation is internally consistent.
known_priors: >-
  Task 030 readme.md notes FE-3 "readme update fatigue".
  research/repo-maintenance-protocol-spec/output/SPEC.md §3.1 has
  a static/dynamic partition that may inform the choice.
known_constraints: >-
  Recommendation must be expressible in <10 lines per spec. Must not
  contradict MAINTENANCE.md §3.2 dynamic-readme partition.
domain_context: >-
  Both FRUSTRATED.md and PRE_COMMIT.md are root specs subject to
  T1/T2 repairs only per MAINTENANCE.md §1.1 — wording fixes are
  T2 Additive, allowed.
category_signal: B  # bounded empirical question
```

## Phase 2 Plan Hints

- **Methods:** M07 (contradiction log on §28 vs §2), M12 (base-rate token-cost measurement), M02 (steel-man each cadence)
- **Frameworks:** decision-matrix (cadence × token cost × consistency)
- **Seed queries:** "readme update", "pre-commit", "batched", "Global Readme Audit"

## Inputs

- [`FRUSTRATED.md`](../../../FRUSTRATED.md) §28.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §2.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2.
- [`research/repo-maintenance-protocol-spec/output/SPEC.md`](../../../research/repo-maintenance-protocol-spec/output/SPEC.md) §3.1 (static/dynamic partition).
- ≥3 recent merged PRs as token-cost evidence (one with many readme updates, one with few).

## Acceptance Criteria

1. SPEC.md at `/research/pre-commit-readme-update-cadence/output/SPEC.md`.
2. §1 token-cost comparison covers ≥3 cadence choices.
3. §2 normative rule is unambiguous and consistent with MAINTENANCE.md §3.2.
4. §3 contains drop-in wording for FRUSTRATED.md §28 AND PRE_COMMIT.md §2.
5. §4 walkthrough on a recent session shows the rule yields the expected behaviour.
6. `research_phase: complete`; reflection friction-log.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~3 hours).

## Execution Brief (for the main agent — do NOT dispatch via /sc:agent)

```text
Run research-prompt-optimizer Phase 1–3. Repo root: /home/user/agency.
Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser; intent canonical.
Render to /research/pre-commit-readme-update-cadence/research-prompt.md.
Execute and produce /research/pre-commit-readme-update-cadence/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(readme-cadence): reconcile FRUSTRATED.md §28 with PRE_COMMIT.md §2 (Task 037 ST-1)".
Do NOT push.
```
