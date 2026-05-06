---
type: note
status: draft
slug: task-033-st1-research-friction-pattern-synthesis
summary: "Subtask ST-1 (research head): aggregate every closed-task friction-log.md across the repo, classify FL0–FL3 patterns by recurring root cause, and produce a synthesis report feeding TASK.md §4.6 closure-rule clarifications and FRUSTRATED.md FL0 justification."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — Friction Pattern Synthesis

**Executor:** main-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies. Sibling research subtask Task 038 ST-1 (FL0 justification) reads same corpus and may run in parallel for token-cost amortization.

## Goal

Produce `research/friction-pattern-synthesis/output/SPEC.md` aggregating every `friction-log.md` in `/tasks/<NNN>-<slug>/` and `/research/<slug>/reflection/` into a structured synthesis: (a) FL distribution histogram, (b) recurring root-cause taxonomy (≥6 categories), (c) per-spec friction-attribution (which root spec generated which friction), (d) recommended TASK.md / FRUSTRATED.md amendments grounded in evidence.

## Falsification

Wrong cut **iff** fewer than 15 closed tasks have a non-empty friction-log.md. Mitigation: 16 closed tasks (per Task 029 closure note) already exist; this is a sufficient corpus.

## Phase 1 Intent

```yaml
research_question: >-
  What recurring patterns of friction (FL1+) appear across closed agency
  tasks, which root specs generate them, and what amendments to TASK.md
  §4.6 closure rules and FRUSTRATED.md FL0 wording would reduce future
  friction?
research_question_unpacked: >-
  This is NOT "are agents complaining" (subjective). It is a behavioural-
  evidence audit: aggregate logs, classify root causes, propose
  spec-text amendments backed by frequency.
audience: maintainer authoring TASK.md §4.6 and FRUSTRATED.md amendments (Tasks 032 + 037)
output_format: structured Markdown SPEC.md with §1 histogram, §2 root-cause taxonomy, §3 per-spec attribution table, §4 recommended amendments
temporal_scope: {from: "2026-05-04", to: "2026-05-06"}
language: en
depth: standard
success_criterion: >-
  ≥6 distinct root-cause categories identified; ≥3 spec-text amendments
  proposed with verbatim before/after wording; 100% of FL2/FL3 entries
  attributed to at least one root cause.
process_gates:
  - "research_phase: complete on the produced workspace"
  - "reflection/friction-log.md present with FL[0-3] declaration"
  - "/research/readme.md updated to list the new entry per RESEARCH.md §4 Step 5"
  - "tools/check-governance.sh exits 0 against the produced workspace"
known_priors: >-
  Tasks 014 and 025 distill 7 maintenance-spec findings (F1-F7).
  Task 030 notes.md §3 lists FE-1..FE-10. These are pre-classified
  friction items that the synthesis MUST cite.
known_constraints: >-
  Read-only against logs. Anonymise agent names if needed (don't blame
  individual agents). Don't propose tooling-only changes — focus on
  spec amendments.
domain_context: >-
  FRUSTRATED.md defines FL0–FL3. TASK.md §4.6 mandates a friction-log
  for closure. MAINTENANCE.md §3.2 aggregates friction into Tasks.
category_signal: B  # bounded extraction across a known corpus
```

## Phase 2 Plan Hints

- **Methods:** M07 (contradiction log across friction entries), M12 (base-rate anchoring on FL distribution), M02 (steel-manning each FL2/FL3 root cause)
- **Frameworks:** thematic-coding (Boyatzis pattern); RCA fishbone for cause categories
- **Seed queries:** "FL2", "FL3", "tooling failure", "spec ambiguity", "readme bloat"

## Inputs

- All `tasks/<NNN>-<slug>/friction-log.md` (~20 files; closed tasks only).
- All `research/<slug>/reflection/friction-log.md`.
- [`tasks/030-cleanup-dramatica-skills-corpus/notes.md`](../../030-cleanup-dramatica-skills-corpus/notes.md) §3 (FE-1..FE-10 already classified).
- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (high-blast assumptions).

## Acceptance Criteria

1. SPEC.md at `/research/friction-pattern-synthesis/output/SPEC.md`.
2. §1 histogram counts FL0/FL1/FL2/FL3 across both surfaces (PR descriptions + reflection files); covers ≥15 closed tasks.
3. §2 root-cause taxonomy has ≥6 categories with frequency counts.
4. §3 per-spec attribution: which root spec each FL2+ entry implicates.
5. §4 amendments: ≥3 verbatim spec-text proposals with file:line targets.
6. `research_phase: complete`; friction-log.md present.

## Dependencies

None. Phase A.

## Estimated Effort

Large (~5 hours; corpus aggregation + thematic coding).

## Execution Brief

```text
Run the research-prompt-optimizer pipeline (Phase 1–3) against the intent
block above.

Phase 1 intent is canonical (above) — skip the askuser loop.
Phase 2: select M07 / M12 / M02 modules; author CBs from constraints.
Phase 3: render to /research/friction-pattern-synthesis/research-prompt.md.
Then EXECUTE: produce /research/friction-pattern-synthesis/output/SPEC.md
meeting the acceptance criteria; author the reflection friction-log.md;
update /research/readme.md.

Run tools/check-governance.sh and fix every ERROR.
Commit "research(friction-pattern-synthesis): cross-task friction taxonomy (Task 033 ST-1)".
Do NOT push.
```
