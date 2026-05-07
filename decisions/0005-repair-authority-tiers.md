---
type: adr
status: draft
slug: 0005-repair-authority-tiers
summary: "Every change is classified T1 (mechanical) / T2 (additive) / T3 (structural) / T4 (research-touching). T1/T2 land in-place via tools/fm/edit.py; T3 land via Tasks; T4 (closed research, Accepted ADRs) MUST NOT be mutated."
created: 2026-05-07
updated: 2026-05-07
adr_id: ADR-0005
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - maintenance
  - tier-classification
  - immutability
  - mutation-surface
---

# ADR-0005 — Repair Authority Tiers and Mutation Surface Boundaries

## Context and Problem Statement

Without a tier-classification rule, agents either over-modify (rewrite an entire Task to fix a typo, dragging in unrelated changes that cloud the diff) or under-modify (open a Task PR for a missing `updated:` date, exhausting reviewer attention on trivia). Closed research workspaces and root governance specs MUST resist accidental rewriting; agents working in good faith still need a fast path for trivial mechanical fixes.

The repo declares the four-tier classification at [`MAINTENANCE.md:24-32`](../MAINTENANCE.md) (tier table) with T4 immutability at line 33 and the root-spec ceiling at line 35. The canonical mutation surface is `tools/fm/edit.py`. This ADR formalises both the tiers and the mutator boundary.

## Decision Drivers

- **Cost-of-fix gradient.** Drift is cheap to fix at T1/T2 and expensive at T3+; the rule rewards fast, low-risk mechanical fixes and forces deliberation only when warranted.
- **Immutability of closed evidence.** A `/research/<slug>/` workspace whose `research_phase: complete` is the epistemic anchor for downstream Tasks; mutating it after closure invalidates citations.
- **Mutation-surface stability.** A canonical mutator that takes a file lock, preserves body bytes, and rejects T3/T4 by construction is the only sound way to enforce the tier rule mechanically.

## Considered Options

1. **Single "edit anything" rule.** Rejected: conflates T1 typo fixes with T3 structural rewrites; reviewer attention degrades; closed research silently mutates.
2. **Four-tier classification with a canonical mutator (chosen).** Tiers T1–T4 with explicit permitted actions and a canonical `tools/fm/edit.py` that rejects T3/T4 operations.
3. **Branch-protection-only enforcement.** Rejected: doesn't help in-session; agents still need a clear in-the-moment classification rule.

## Decision Outcome

Every change MUST be classified T1 (mechanical), T2 (additive), T3 (structural), or T4 (research-touching) before mutation; T1 and T2 changes MUST land in-place via `tools/fm/edit.py`; T3 changes MUST be written as Tasks under `/tasks/`; T4 surfaces (closed research workspaces, Accepted ADRs) MUST NOT be mutated at all — alterations land via successor records (a new research run, a superseding ADR).

## Consequences

- **Positive.** Agents self-classify in seconds; the canonical mutator rejects T3/T4 by construction; closed research is stable as an epistemic anchor. The tier rule is the lifecycle paradigm the ADR `Accepted` lifecycle inherits directly.
- **Negative.** The boundary between tiers is a judgement call at the margin (e.g. is a body-paragraph rewording T2 or T3?); ambiguity must be resolved by escalating to T3 conservatively.
- **Neutral.** Root governance specs (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`) are subject to T1/T2 only; structural changes to these files are always Tasks, which is the Task 027/028/029 pattern in lived practice.
