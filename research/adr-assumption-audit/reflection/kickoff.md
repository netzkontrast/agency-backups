---
type: note
status: active
slug: adr-assumption-audit-kickoff
summary: "CB0 kickoff reflection: five answers before launching any subagent."
created: 2026-05-05
updated: 2026-05-05
---

# Kickoff Reflection (CB0)

## Q1. What do I actually believe right now about the quality of the ADR governance spec, and how confident?

I believe the Task 027 SPEC is structurally sound and repo-grounded — the §0–§9 schema is honoured, every MUST has a Gherkin anchor, the `decisions/` storage path resolves the Gemini draft's `docs/` mismatch, and the guarded-section synthesis design avoids the destructive-overwrite trap. **Confidence: 0.80.** The 20% I am not confident about: (a) the fidelity-mode default `bcp14-keyword` is provisional and untested; (b) the spec assumes ADRs *will* be authored, but the repo has no precedent for proactive ADR authoring and the agent culture skews toward Tasks-as-decisions; (c) the supersession DAG semantics inherit cleanly from `task_supersedes` but the *blast radius* of a missed reciprocal edge is larger for ADRs (silent rule disappearance) than for Tasks (orphaned breadcrumb).

## Q2. What is the strongest evidence that the spec may be wrong in a consequential way?

Two pieces of evidence:

1. **No actual ADR exists in the repo yet.** The spec was authored against an empty corpus. The first time `agency-adr synthesize` runs against a real ADR, it will reveal whichever section parsing assumption is wrong (heading variants, language drift, embedded code blocks confusing the body extractor). That is an empirical fact the spec has not been calibrated against.
2. **The 22:1 compression-ratio claim** (45K input → 2K output) is inherited verbatim from the Gemini draft and never re-derived against this repo's `AGENTS.md` size. My own analysis (`research/adr-spec-research-synthesis/reflection/M13-query-expansion.md` Axis 4) put `AGENTS.md` at ≈ 4,800 tokens *before* synthesis adds anything; if the synthesised section actually weighs in at 2K, the *post-synthesis* file is ≈ 6,800 tokens, which the spec frames as fine but the empirical attention-recession threshold for Claude is unverified at that scale.

## Q3. Where am I most likely to find a hidden assumption that would break the implementation?

Three high-yield veins:

1. **Authorship assumptions.** The spec describes ADR authoring in third-person ("the author MUST verify…") without specifying who *the author* is. In an agentic repo, the author is typically an agent operating on behalf of a maintainer. If the spec assumes human authorship, every ADR.A.1.x and ADR.A.2.x normative becomes ambiguous. (Subagent A target.)
2. **Implicit tooling decisions.** The repo has 14 implicit decisions catalogued in the Task 027 analysis, but the analysis only looked at *root specs*. The tooling files (`tools/fm/_core.py`, `tools/check-governance.sh`) likely encode a dozen more — Python version, depth-1 YAML enforcement strategy, hand-rolled vs PyYAML parsing — that have never been ADR-formalised. (Subagent B target.)
3. **Pending-decision decay.** SPEC §8 lists 7 OQs, plan §6 lists 10 ODs. The two lists overlap but were authored independently. The audit needs to triangulate them and surface which ones are duplicates, which are independent, and which are missing from both. (Subagent C target.)

## Q4. If I were starting this audit from scratch, what would I read first?

I would read [`tools/fm/_core.py`](../../../tools/fm/_core.py) end-to-end, because it is the load-bearing primitive for both the Task 027 SPEC and the Task 028 plan. Every ADR validation diagnostic, every frontmatter parse, every section walk depends on it. If `_core.py` carries assumptions that break under ADR shapes (multi-paragraph "Decision Outcome", code-fenced "Consequences", Y-Statement single-line decisions), the entire validate→synthesize pipeline collapses silently. Reading the SPEC first is correct for *understanding the design*; reading `_core.py` first would be correct for *finding what breaks the design*.

## Q5. What is the single highest-value subagent assignment for this run?

Subagent B (M07 implicit-ADR inventory). The other two subagents produce *recommendations*; Subagent B produces *facts about what is already true in the repo*. Those facts are the seed corpus for Task 030 (first-batch ADR authoring) and they cannot be deferred — every day the repo accretes new behaviour, the implicit-ADR list grows. The audit value of catching today's implicit decisions is structurally higher than the audit value of catching tomorrow's hypothetical hidden assumption.

## Pre-Commitments

Before running the subagents I commit to:

1. **Falsifiability discipline.** Every assumption (ASM-NNN), every implicit ADR (IADR-NNN), every pending decision (PD-NNN) MUST cite a specific `file:line` or `file §section` evidence anchor. "The spec assumes X" without a citation is rejected.
2. **Boundary respect.** I will NOT modify `research/adr-spec-research-synthesis/output/SPEC.md`. Per `MAINTENANCE.md §1` it is T4-immutable. If the audit recommends a change, the change goes into REPORT.md §4 as a recommendation, never as an in-place edit.
3. **PD ↔ OD reciprocity.** If a PD found by Subagent C maps to an existing OD in `tasks/028-adr-tooling-impl-plan/implementation-plan.md §6`, I will note both IDs in REPORT.md and add a one-line cross-reference to the plan (the only permissible edit to the closed Task 028).

## Highest-Value Single Action

Author Subagent B's output first if a constraint forces serial execution. The implicit-ADR inventory is the only artefact that produces forward leverage (seeds Task 030); the M13 and M06+M08 outputs produce upstream leverage (refine SPEC §8 / plan §6) but do not unblock new work.
