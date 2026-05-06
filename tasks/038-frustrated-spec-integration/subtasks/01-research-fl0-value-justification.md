---
type: note
status: draft
slug: task-038-st1-research-fl0-value-justification
summary: "Subtask ST-1 (research head): empirically justify the FL0-mandatory rule by analyzing every closed-task friction-log.md for the upstream value of FL0 entries (do they feed maintenance, or are they pure overhead?), and producing a defensible §FL.0 rationale for FRUSTRATED.md."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — FL0 Value Justification

**Executor:** main-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

## Goal

Produce `research/fl0-value-justification/output/SPEC.md` answering the question "what does an FL0 entry contribute upstream that an absent log does not". Inputs: every closed-task friction log. Outputs: (a) FL0-frequency stats, (b) qualitative analysis of FL0 entry content, (c) the upstream consumers that depend on FL0 presence (e.g., MAINTENANCE.md §3.2 friction aggregation), (d) verbatim §FL.0 rationale paragraph for FRUSTRATED.md.

## Falsification

Wrong cut **iff** FL0 entries provide no measurable upstream signal — in that case, the recommendation should be to make FL0 *optional* (a finding that itself justifies a spec amendment).

## Phase 1 Intent

```yaml
research_question: >-
  Empirically, what value do FL0 entries contribute to upstream
  governance processes (MAINTENANCE.md aggregation, Repo Coherence
  Check, Task delegation pipeline), and is the value sufficient to
  justify mandating them?
research_question_unpacked: >-
  This is NOT "are agents annoyed by FL0" (subjective). It is
  "what concrete signal do existing FL0 entries carry that an absent
  log would not, and how does upstream tooling depend on that signal."
audience: maintainer authoring FRUSTRATED.md §FL.0 amendment in Task 038
output_format: structured Markdown SPEC.md with §1 frequency stats, §2 content analysis (sample 10 FL0 entries verbatim), §3 upstream-consumer audit, §4 verdict (mandate / make-optional / clarify), §5 verbatim §FL.0 rationale paragraph
temporal_scope: {from: "2026-05-04", to: "2026-05-06"}
language: en
depth: standard
success_criterion: >-
  Verdict supported by ≥3 distinct lines of evidence; §5 paragraph
  fits within existing §FL.0 line budget; recommendation is
  internally consistent with MAINTENANCE.md §3.2 aggregation.
process_gates:
  - "research_phase: complete on the produced workspace"
  - "reflection/friction-log.md present with FL[0-3] declaration"
  - "/research/readme.md updated to list the new entry per RESEARCH.md §4 Step 5"
  - "tools/check-governance.sh exits 0 against the produced workspace"
known_priors: >-
  TASK.md §306 reinforces FL0 mandate. MAINTENANCE.md §3.2 aggregates
  friction from logs. Task 029 closed at FL1; many other tasks at
  FL0/FL1.
known_constraints: >-
  Read-only against logs. Anonymise where helpful. Do not propose
  changes to other specs.
domain_context: >-
  Friction logs live in two surfaces: /research/<slug>/reflection/
  and PR descriptions. The mandate covers both.
category_signal: B  # bounded empirical question
```

## Phase 2 Plan Hints

- **Methods:** M12 (base-rate analysis), M02 (steel-man the FL0 mandate), M01 (falsifiability — what would make us drop it?)
- **Frameworks:** content analysis with quote sampling
- **Seed queries:** "Highest Frustration Level: FL0", "FL0", upstream consumer references

## Inputs

- All closed-task `friction-log.md` files (~16 closed tasks).
- All `research/<slug>/reflection/friction-log.md`.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2 (upstream consumer).
- [`TASK.md`](../../../TASK.md) §306 (mandate restatement).

## Acceptance Criteria

1. SPEC.md at `/research/fl0-value-justification/output/SPEC.md`.
2. §1 covers ≥15 closed tasks.
3. §2 quotes ≥10 distinct FL0 entries verbatim.
4. §3 names ≥1 concrete upstream consumer that depends on FL0 presence.
5. §4 verdict is one of {mandate / make-optional / clarify} with rationale.
6. §5 contains a drop-in §FL.0 paragraph for FRUSTRATED.md.
7. `research_phase: complete`; reflection friction-log.

## Dependencies

None. Phase A. NOTE: Task 033 ST-1 (friction-pattern-synthesis) is a sibling — they share the same corpus but ask orthogonal questions (patterns vs FL0 specifically). They can run in parallel; the FL0 study cites the pattern-synthesis if it lands first.

## Estimated Effort

Medium (~2.5 hours).

## Execution Brief

```text
Run research-prompt-optimizer Phase 1–3. Repo root: /home/user/agency.
Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser; intent canonical.
Render to /research/fl0-value-justification/research-prompt.md.
Execute and produce /research/fl0-value-justification/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(fl0-justification): empirical value of FL0 entries (Task 038 ST-1)".
Do NOT push.
```
