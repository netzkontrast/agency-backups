---
type: note
status: draft
slug: task-033-st2-research-spec-staleness-decision-formalization
summary: "Subtask ST-2 (research, shared with Task 039): formalize MAINTENANCE.md §3.4 staleness decision algorithm — produce a deterministic decision tree mapping observable signals to {still accurate / drifted / completed-by-drift / no-longer-desirable}."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: Research — Staleness Decision Formalization

## Goal

Produce `research/spec-staleness-decision-formalization/output/SPEC.md` containing a decision tree that converts observable git-history + repo-state signals into one of four staleness buckets without subjective judgment, plus the `MAINT_STALE_DAYS` declaration mechanism.

## Falsification

Wrong cut **iff** the decision tree requires more than 5 levels or more than 12 leaf rules. Mitigation: TASK.md §4.7 already enumerates 4 buckets; the algorithm need only deterministically map signals → buckets.

## Phase 1 Intent

```yaml
research_question: >-
  Given a Task with task_status=open whose `created` date precedes the
  most recent task_status=done by ≥ MAINT_STALE_DAYS, what observable
  signals deterministically map it to one of {still-accurate, drifted,
  completed-by-drift, no-longer-desirable}?
research_question_unpacked: >-
  This is NOT "should staleness use 7 days vs 14 days" (parameter
  choice). It is "what is the algorithm that, given the signals,
  always yields the same bucket regardless of which agent runs it."
audience: maintenance-run agent (Claude Code) executing MAINTENANCE.md §3.4
output_format: structured Markdown SPEC.md with §1 decision tree (graphviz + prose), §2 signal taxonomy (each signal extractable via git/grep), §3 example walk-throughs (≥4), §4 MAINT_STALE_DAYS declaration mechanism
temporal_scope: unbounded  # rule, not data
language: en
depth: exhaustive
success_criterion: >-
  Two agents running the algorithm against the same Task at the same
  commit MUST produce the same bucket assignment. The algorithm cites
  ≤5 signals; signals are mechanically extractable.
known_priors: >-
  TASK.md §4.7 enumerates 4 buckets. MAINTENANCE.md §3.4 defines the
  staleness window (default 7 days). MAINTENANCE.md §1 partitions
  T1/T2/T3 tiers. Task 014 + Task 025 surfaced F2-F4-F7 findings
  about staleness rules.
known_constraints: >-
  Algorithm MUST NOT require LLM-call judgment ("Goal is still
  desirable?"). It MUST work on stdlib + git. It MUST be re-runnable.
domain_context: >-
  Coherence runs are git-delta-aware. Tasks may depend on other Tasks.
  Supersession changes the staleness semantics.
category_signal: B  # algorithmic formalization
```

## Phase 2 Plan Hints

- **Methods:** M01 (falsification of each rule), M11 (formal logic decomposition), M04 (operationalize subjective predicates into observable signals)
- **Frameworks:** decision tree + signal-extractor catalog
- **Seed queries:** "git log --before", "task_blocked_by satisfied", "task_affects_paths still exists"

## Inputs

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.4 (current prose algorithm).
- [`TASK.md`](../../../TASK.md) §4.7 (lifecycle states).
- [`tasks/014-improve-maintenance-spec-from-session/`](../../014-improve-maintenance-spec-from-session/) (F2/F3/F4/F7 findings).
- [`tasks/025-maintenance-spec-remaining-findings/`](../../025-maintenance-spec-remaining-findings/) (carry-forward findings).
- All currently-open tasks (~7) as test cases for the algorithm.

## Acceptance Criteria

1. SPEC.md at `/research/spec-staleness-decision-formalization/output/SPEC.md`.
2. §1 contains a decision tree expressible in <30 lines of pseudocode.
3. §2 lists ≤5 signals; each has a one-line extraction recipe.
4. §3 walks through ≥4 currently-open tasks (e.g., 022, 023, 024, 025) and assigns each a bucket per the algorithm.
5. §4 declares the configuration mechanism (env var, repo file, or TASK.md frontmatter).
6. Two test runs by independent agents agree on bucket assignment for the §3 walkthroughs.

## Dependencies

None. Phase A. NOTE: Task 039 ST-2 is the *same* research subtask (cross-Task shared input). Whichever lands first authors the SPEC; the second references it.

## Estimated Effort

Medium (~3 hours).

## Execution Brief (for the main agent — do NOT dispatch via /sc:agent)

```text
Run research-prompt-optimizer Phase 1–3 against the intent above. Repo root:
/home/user/agency. Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser; intent is canonical.
Render the research prompt to /research/spec-staleness-decision-formalization/research-prompt.md.
Execute and produce /research/spec-staleness-decision-formalization/output/SPEC.md per acceptance.
Run tools/check-governance.sh.
Commit "research(staleness-formalization): deterministic algorithm (Task 033 ST-2 / Task 039 ST-2)".
Do NOT push.
```
