---
type: task
status: active
slug: analyze-skillmd-novel-authoring
summary: "Analyze Gemini extraction of SKILL.md-conformant novel-authoring repos (DE/EN); extract actionable recommendations for agency repo and SKILL.md writing workflows."
created: 2026-05-04
updated: 2026-05-04
task_id: "003"
task_status: open
task_owner: "claude-code"
task_priority: P1
task_uses_prompts:
  - github-skillmd-novel-authoring-de-en
task_spawns_research: []
task_affects_paths:
  - research/gemini/github-skillmd-novel-authoring-de-en/result.md
  - research/ncp-novel-co-authoring-spec/
  - tasks/003-analyze-skillmd-novel-authoring/
---

# Task 003 — Analyze SKILL.md Novel-Authoring GitHub Research (DE/EN)

## Goal

Analyze the external Gemini research result in `research/gemini/github-skillmd-novel-authoring-de-en/result.md`, cross-reference its findings with in-house research (particularly `research/ncp-novel-co-authoring-spec/`), and extract concrete, scoped recommendations applicable to this repository and any SKILL.md-based writing workflows. Done when all recommendations are documented in `output/RECOMMENDATIONS.md` and follow-up prompts for unresolved vectors are filed in `/prompts/`.

## Plan

1. Read `research/gemini/github-skillmd-novel-authoring-de-en/result.md` in full; annotate all key findings, contradictions, and open questions.
2. Cross-reference findings against `research/ncp-novel-co-authoring-spec/` and any other relevant in-house `/research/` workspaces.
3. Categorize findings: (a) immediately actionable, (b) requires further research, (c) out of scope for this repo.
4. Draft `output/RECOMMENDATIONS.md` covering:
   - Architecture patterns worth adopting (multi-agent orchestration, progressive disclosure, Markdown registries).
   - German DE/EN bilingual processing accommodations.
   - Anti-slop / quality-assurance linting approaches.
   - Unresolved contradictions requiring empirical resolution.
5. File follow-up prompts in `/prompts/` for each open question from the source document's "Open Questions and Unresolved Vectors" section.
6. Update frontmatter (`task_spawns_research`, `updated`) and close task.

## Todo

- [ ] 1. Read and annotate `result.md` key findings.
- [ ] 2. Cross-reference with in-house research workspaces.
- [ ] 3. Categorize findings (actionable / needs-research / out-of-scope).
- [ ] 4. Draft `output/RECOMMENDATIONS.md`.
- [ ] 5. File follow-up prompts for unresolved open questions.
- [ ] 6. Update frontmatter and close task.

## Links

- External result: [`research/gemini/github-skillmd-novel-authoring-de-en/result.md`](../../research/gemini/github-skillmd-novel-authoring-de-en/result.md)
- Stub prompt: [`prompts/github-skillmd-novel-authoring-de-en/prompt.md`](../../prompts/github-skillmd-novel-authoring-de-en/prompt.md)
- Related in-house research: [`research/ncp-novel-co-authoring-spec/`](../../research/ncp-novel-co-authoring-spec/)
- Governing ingestion spec: [`RESEARCH.md §6`](../../RESEARCH.md)
