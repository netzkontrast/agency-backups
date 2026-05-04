---
type: prompt
status: completed
slug: github-skillmd-novel-authoring-de-en
summary: "Research proposal stub: extract GitHub repos featuring SKILL.md-conformant novel-authoring capabilities, bilingual DE/EN. Executed externally by Google Gemini."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN
prompt_target_agent: external
prompt_relates_to_task: analyze-skillmd-novel-authoring
prompt_spawned_from_research: ""
---

# GitHub SKILL.md Novel-Authoring Repositories (DE/EN) — Stub Prompt

> **Execution:** Executed externally by Google Gemini.
> **Result:** [`research/gemini/github-skillmd-novel-authoring-de-en/result.md`](../../research/gemini/github-skillmd-novel-authoring-de-en/result.md)
> **Analysis task:** [`tasks/003-analyze-skillmd-novel-authoring/`](../../tasks/003-analyze-skillmd-novel-authoring/)

This stub exists to preserve the `Prompt → Research` audit graph per `RESEARCH.md` §6.3. The research was executed outside the repository by Google Gemini; the result was ingested per the External Research Ingestion workflow.

## Original Research Intent

Extract and evaluate GitHub repositories implementing the SKILL.md open standard for novel-authoring and fiction writing, with strict filtering for bilingual applicability in English and German.

Classify repositories as:
- **Klasse A** (Weight 1.0): Dedicated novel-writing repos with normative workflows, YAML frontmatter, and SKILL.md conformance.
- **Klasse B** (Weight 0.5): Generic skill collections containing at least one conforming writing/authoring skill.

Apply the Quality Signal Rubric (GitHub stars, last commit recency, README quality, license, CI/tests) and document key architectural patterns: multi-agent orchestration, progressive disclosure, externalized state management, bilingual processing nuances, and anti-slop linting.
