---
type: note
status: draft
slug: task-034-st1-research-session-continuity-protocol-instantiation
summary: "Subtask ST-1 (research head): translate the orphaned agentic-session-continuity-spec Spec-I (cross-session protocol) into a concrete checkpoint/restore protocol implementable as a state.md file under /research/<slug>/workspace/, with epistemic-delta encoding and session-ID conventions."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — Session-Continuity Protocol Instantiation

## Goal

Produce `research/session-continuity-protocol-instantiation/output/SPEC.md` containing a concrete, file-format-spec'd instantiation of the abstract Spec-I from `agentic-session-continuity-spec/output/SPEC.md`. Output: (a) `state.md` schema (frontmatter + sections), (b) checkpoint emission cadence (every N synthesis steps), (c) epistemic-delta encoding format, (d) restore procedure for a fresh-context successor agent, (e) integration points with RESEARCH.md §4.

## Falsification

Wrong cut **iff** the checkpoint cadence cannot fit in <10% additional token cost vs. uninstrumented runs. Mitigation: synthesis-step boundaries are natural checkpoint points; the cost is one file write per boundary.

## Phase 1 Intent

```yaml
research_question: >-
  How should the abstract Spec-I cross-session protocol from
  agentic-session-continuity-spec be concretized as a file-format
  contract that fits inside /research/<slug>/workspace/state.md and
  is parseable by both the originating agent and a fresh-context
  successor?
research_question_unpacked: >-
  This is NOT "should we have continuity" (policy already in
  agentic-session-continuity-spec). It is "what is the file format,
  cadence, and restore procedure that operationalizes it."
audience: research-run agent (Claude Code, Gemini, Jules) executing a multi-session research workflow under RESEARCH.md
output_format: structured Markdown SPEC.md with §1 state.md schema, §2 checkpoint cadence rules, §3 epistemic-delta encoding, §4 restore procedure, §5 RESEARCH.md amendment recommendation
temporal_scope: unbounded
language: en
depth: standard
success_criterion: >-
  state.md schema validates against fm-validate; restore procedure
  succeeds in a worked example (Task 027's research workspace as
  test bed); token overhead <10% on a synthesis run.
known_priors: >-
  agentic-session-continuity-spec/output/SPEC.md proposes Spec-G
  (context pruning), Spec-H (memory state machine), Spec-I (cross-
  session protocol). Spec-I is the target for instantiation.
  RESEARCH.md §4 already mandates a workspace folder.
known_constraints: >-
  Schema must use L1 Vault Core frontmatter. Must work with stdlib
  Python (fm-validate). Must NOT introduce a new top-level
  directory. Must integrate with existing reflection/friction-log.md.
domain_context: >-
  Research workspaces are read-mostly once research_phase: complete.
  Agents may resume after long gaps (cross-session = days/weeks).
category_signal: A  # architectural design with explicit constraints
```

## Phase 2 Plan Hints

- **Methods:** M03 (pre-mortem on resume failures), M11 (formal protocol decomposition), M01 (falsifiability of the cadence claim)
- **Frameworks:** state-machine + filesystem-as-IPC; protocol-spec template
- **Seed queries:** "session.log", "checkpoint", "memory snapshot", "epistemic delta", "agent handoff"

## Inputs

- [`research/agentic-session-continuity-spec/output/SPEC.md`](../../../research/agentic-session-continuity-spec/output/SPEC.md) (Spec-G/H/I).
- [`RESEARCH.md`](../../../RESEARCH.md) §4 (workspace structure).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) — example multi-session workspace.
- [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — frontmatter schema constraint.

## Acceptance Criteria

1. SPEC.md at `/research/session-continuity-protocol-instantiation/output/SPEC.md`.
2. §1 includes a complete `state.md` example for a real research workspace (Task 027 as worked example).
3. §2 cadence rule cites empirical token cost on the worked example.
4. §3 delta-encoding format is JSON-Schema-validated.
5. §4 restore-procedure pseudocode runs against the worked example without error.
6. §5 contains a verbatim RESEARCH.md §4 amendment ready for Task 034 ST-5 to lift.
7. `research_phase: complete`; reflection friction-log.

## Dependencies

None. Phase A.

## Estimated Effort

Large (~5 hours; protocol design + worked example + token measurement).

## Agent Prompt

```text
Run research-prompt-optimizer Phase 1–3. Repo root: /home/user/agency.
Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser; intent canonical.
Render to /research/session-continuity-protocol-instantiation/research-prompt.md.
Execute and produce /research/session-continuity-protocol-instantiation/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(session-continuity): file-format instantiation of Spec-I (Task 034 ST-1)".
Do NOT push.
```
