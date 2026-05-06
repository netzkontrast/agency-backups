---
type: note
status: draft
slug: task-039-st1-research-toolchain-flip-criteria
summary: "Subtask ST-1 (research head): formalize the criteria under which MAINTENANCE.md §1.1.2 dual legacy/flexible toolchain transitions to flexible-as-default; produce a flip checklist and a post-flip cleanup list."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — Toolchain Flip Criteria

**Executor:** maintenance-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4, ST-5. No inter-dependencies.

## Goal

Produce `research/toolchain-flip-criteria/output/SPEC.md` containing the deterministic flip criteria + post-flip cleanup checklist for the MAINTENANCE.md §1.1.2 dual-toolchain transition. Includes: (a) quantifiable criteria (zero outstanding waivers, X% test coverage, all required Tasks done), (b) flip-day procedure (atomic commit shape), (c) post-flip cleanup (which legacy linters retire, which warning-mode rules graduate to ERROR), (d) rollback plan if the flip breaks production.

## Falsification

Wrong cut **iff** the criteria cannot be evaluated mechanically (e.g., requires LLM judgment). Mitigation: the criteria are git/grep-extractable (waiver count, task_status, lint exit codes).

## Phase 1 Intent

```yaml
research_question: >-
  What quantifiable, mechanically-verifiable criteria MUST be true
  before the flexible toolchain (FM_TOOLCHAIN=1) becomes the default
  in tools/check-governance.sh, and what cleanup steps follow the
  flip?
research_question_unpacked: >-
  This is NOT "should we flip" (decision belongs to maintainer). It
  is "what is the checklist so a maintenance agent can evaluate
  flip-readiness without LLM judgment."
audience: maintenance-run agent + human maintainer
output_format: structured Markdown SPEC.md with §1 flip criteria checklist, §2 atomic flip procedure, §3 post-flip cleanup, §4 rollback plan
temporal_scope: unbounded
language: en
depth: standard
success_criterion: >-
  Criteria evaluable by `tools/check-governance.sh` extension or simple
  git grep; checklist has ≤7 items; flip procedure is atomic (single
  commit); rollback is one git revert.
process_gates:
  - "research_phase: complete on the produced workspace"
  - "reflection/friction-log.md present with FL[0-3] declaration"
  - "/research/readme.md updated to list the new entry per RESEARCH.md §4 Step 5"
  - "tools/check-governance.sh exits 0 against the produced workspace"
known_priors: >-
  MAINTENANCE.md §1.1.2 declares parallel operation. Tasks 016-019
  shipped the flexible toolchain. governance-specs-update-research/
  output/SPEC.md §2 has amendment text awaiting back-port.
known_constraints: >-
  No LLM-call evaluation. Must work with Python stdlib + git.
  Must keep tools/.frontmatter-waivers under 50 entries by flip day
  (governance-specs-update-research §2 burn-down rule).
domain_context: >-
  Tasks 016, 017, 018, 019 are done. Tasks 022, 025 are unblock-
  eligible. Task 010 was superseded by Task 022.
category_signal: A  # operational checklist with explicit constraints
```

## Phase 2 Plan Hints

- **Methods:** M01 (falsification of each criterion), M03 (pre-mortem on the flip — what breaks?), M11 (formal procedural decomposition)
- **Frameworks:** checklist-driven release (NASA-style flight-readiness review)
- **Seed queries:** "FM_TOOLCHAIN", "default", "burn down", "waiver count"

## Inputs

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1.2.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.A and §7.B.
- [`research/governance-specs-update-research/output/SPEC.md`](../../../research/governance-specs-update-research/output/SPEC.md) §2.
- [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md).
- `tools/check-governance.sh`, `tools/.frontmatter-waivers`.
- Closed Tasks 016, 017, 018, 019.

## Acceptance Criteria

1. SPEC.md at `/research/toolchain-flip-criteria/output/SPEC.md`.
2. §1 checklist has ≤7 mechanically-verifiable items.
3. §2 flip procedure is a single git commit shape (file changes enumerated).
4. §3 post-flip cleanup names every linter to retire and every WARN-to-ERROR promotion.
5. §4 rollback procedure tested mentally against §2.
6. `research_phase: complete`; reflection friction-log.

## Dependencies

None. Phase A. Sibling subtask ST-2 (staleness formalization) runs in parallel.

## Estimated Effort

Medium (~3 hours).

## Execution Brief

```text
Run research-prompt-optimizer Phase 1–3. Repo root: /home/user/agency.
Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser; intent canonical.
Render to /research/toolchain-flip-criteria/research-prompt.md.
Execute and produce /research/toolchain-flip-criteria/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(toolchain-flip-criteria): mechanical flip checklist (Task 039 ST-1)".
Do NOT push.
```
