---
type: note
status: draft
slug: task-034-st1-research-prompt-engineering-principle-mechanizability
summary: "Subtask ST-1 (research head): per-principle assessment of PROMPT.md §5.1–§5.7 mechanical enforceability; identify which principles can be linter-checked, the false-positive rate on the existing prompt corpus, and the tooling each requires."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — Prompt-Engineering Principle Mechanizability

**Executor:** main-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3. No inter-dependencies.

## Goal

Produce `research/prompt-engineering-principle-mechanizability/output/SPEC.md` containing a per-principle assessment for PROMPT.md §5.1 (self-containedness), §5.2 (framework declaration), §5.3 (RFC 2119), §5.4 (deliverable lock), §5.5 (anti-ambiguity), §5.6 (constraint isolation), §5.7 (failure handling). For each: (a) is it mechanically expressible? (b) what tool/heuristic? (c) false-positive rate against existing `/prompts/<slug>/prompt.md` corpus, (d) recommended ERROR vs WARN vs human-only verdict.

## Falsification

Wrong cut **iff** none of P.5.1–P.5.7 (other than P.5.3 which is already linted) admits a mechanical check below 20% false-positive rate. Mitigation: P.5.1 (self-containedness) is testable via "render the prompt to a fresh-context agent and ask for fidelity" — research-prompt-optimizer Phase 4 prior art proves the pattern.

## Phase 1 Intent

```yaml
research_question: >-
  For each of the seven prompt-engineering principles (P.5.1–P.5.7) in
  PROMPT.md, what is the cheapest mechanical enforcement mechanism with
  acceptable false-positive rate (<20%) against the existing prompt
  corpus, and which principles must remain human-review?
research_question_unpacked: >-
  This is NOT "should we enforce all principles" (policy). It is "which
  ones admit cheap mechanical enforcement, and what is the empirical
  false-positive rate on real prompts in this repo".
audience: maintainer authoring PROMPT.md amendments and the new linters in Task 034
output_format: structured Markdown SPEC.md with §1 per-principle assessment table, §2 false-positive measurement methodology, §3 recommended tooling spec for each enforceable principle, §4 the principles that stay human-review with rationale
temporal_scope: {from: "2026-05-04", to: "2026-05-06"}
language: en
depth: standard
success_criterion: >-
  All 7 principles assessed; ≥3 ranked enforceable with <20% FPR;
  ≥1 ranked unenforceable with rationale; ≥30 prompts in the corpus
  scanned as test data.
process_gates:
  - "research_phase: complete on the produced workspace"
  - "reflection/friction-log.md present with FL[0-3] declaration"
  - "/research/readme.md updated to list the new entry per RESEARCH.md §4 Step 5"
  - "tools/check-governance.sh exits 0 against the produced workspace"
known_priors: >-
  P.5.3 (RFC 2119) is already enforced via tools/validate-frontmatter.py
  keyword count. The research-prompt-optimizer skill embeds a Phase 4
  reader-test that mechanizes P.5.1 (self-containedness).
known_constraints: >-
  No LLM-call enforcement (would create cost). Static-analysis only.
  False-positive rate ≤ 20% on pass criteria.
domain_context: >-
  /prompts/ has ~33 active slugs; brief.md + prompt.md per slug.
category_signal: B  # bounded empirical evaluation
```

## Phase 2 Plan Hints

- **Methods:** M02 (steel-man each principle vs. mechanizability), M12 (base-rate measurement on existing corpus), M01 (falsification: which principles fail to lint)
- **Frameworks:** static-analysis pattern (regex / AST / structural checks)
- **Seed queries:** "framework_declaration", "{deliverable", "constraint block heading"

## Inputs

- [`PROMPT.md`](../../../PROMPT.md) §5 (the seven principles).
- All `/prompts/<slug>/prompt.md` files (~33 active).
- [`skills/research-prompt-optimizer/SKILL.md`](../../../skills/research-prompt-optimizer/SKILL.md) (Phase 4 reader-test prior art).
- [`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`](../../../research/agent-prompt-specs-3-systems-sdd/output/SPEC.md) §A.2 (RFC-2119 + Gherkin contract).

## Acceptance Criteria

1. SPEC.md at `/research/prompt-engineering-principle-mechanizability/output/SPEC.md`.
2. §1 table: 7 rows × 5 columns (principle, mechanical recipe, FPR, ERROR/WARN/human, sample-size).
3. §2 documents the FPR-measurement methodology reproducibly.
4. §3 specifies tooling for each enforceable principle (the spec for ST-2 + ST-3 to consume).
5. §4 names the principles that stay human-review.
6. `research_phase: complete`; reflection friction-log.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~3 hours; corpus-scan + statistical FPR calc).

## Execution Brief

```text
Run research-prompt-optimizer Phase 1–3 against the intent. Repo root:
/home/user/agency. Branch: claude/integrate-repo-specs-cIWtI.

Skip Phase 1 askuser. Render to /research/prompt-engineering-principle-mechanizability/research-prompt.md.
Execute and produce /research/prompt-engineering-principle-mechanizability/output/SPEC.md.
Scan all /prompts/<slug>/prompt.md files; report exact corpus size.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(prompt-principle-mechanizability): per-principle FPR assessment (Task 034 ST-1)".
Do NOT push.
```
