---
type: note
status: active
slug: recommendations
summary: "Actionable recommendations extracted from the SKILL.md novel-authoring research."
created: 2026-05-04
updated: 2026-05-04
---

# Analysis & Recommendations: SKILL.md Novel-Authoring (DE/EN)

**Goal:** Extract concrete, scoped recommendations for the agency repository and SKILL.md-based writing workflows based on the Gemini extraction of external repositories (`research/gemini/github-skillmd-novel-authoring-de-en/result.md`) and internal specifications (`research/ncp-novel-co-authoring-spec/output/SPEC.md`).

---

## 1. Actionable Recommendations (Immediately Applicable)

**Multi-Agent Orchestration & Strict Separation of Concerns**
- External repositories rely on a multi-phase, multi-agent pipeline rather than zero-shot single-prompt generation.
- *Recommendation:* Implement discrete, highly specialized agents for distinct phases of the narrative workflow (e.g., developmental editor, continuity tracker, structural critic). This perfectly aligns with our internal `SPEC.md` "Autonomous hand-off via NCP-state" recommendation (§7.3) and the 8-phase Skill Catalog.

**Progressive Disclosure via Externalized Markdown Registries**
- To combat context-window exhaustion, top repositories use progressive disclosure to load metadata dynamically.
- *Recommendation:* Extend the NCP specification and agency prompts to strictly use externalized flat-file Markdown registries for lore, worldbuilding, and character bibles (akin to `danjdewhurst/story-skills`). Agents should query derived computational cache files instead of ingesting full documents on every turn.

**Integration with Dramatica-in-NCP**
- Our internal `SPEC.md` opts for Option B (Dramatica-In-NCP).
- *Recommendation:* Ensure that the progressive disclosure architecture allows for selective retrieval of `subtext.storypoints` and `subtext.dynamics` when passing context to specialized sub-agents.

**Anti-Slop and Quality Assurance Linting**
- External analysis revealed a critical need for adversarial linting (e.g., removing hedging stacks, tricolons, sycophantic openers).
- *Recommendation:* Integrate a dedicated adversarial QA linter into Phase 7 (Revision) or Phase 8 (Editing) of the workflow defined in `SPEC.md`. Raw generative output must be programmatically audited before human presentation.

---

## 2. Requires Further Research (Bilingual Processing & Empirical Resolution)

**German DE/EN Localization Accommodations**
- *Observation:* German string translations and compound lexical structures create higher token overhead and syntactic density. This can degrade model character voice capabilities.
- *Recommendation:* For bilingual (DE/EN) execution, implement an explicit localization-lead persona (similar to `Claude-Code-Game-Studios`) to verify that UI bounds or dialogue strings possess a mandatory **30% character expansion headroom**.
- *Follow-up:* Initiate quantitative testing on character voice degradation in German vs. English when executing identical SKILL.md persona constraints.

**Context Economics and Truncation Mitigation**
- *Observation:* The translation overhead implies that orchestrating agents must trigger memory pruning or compaction protocols earlier when operating in German.
- *Follow-up:* Test localized context limits. Create follow-up prompts to address unresolved vectors such as "Mega-Context Limit Management", "Cross-Skill Context Poisoning", and "Subjective Quality Evaluation" directly.

---

## 3. Out of Scope for this Repo

**TDD for Prompt Authoring**
- *Observation:* `obra/superpowers` uses a strict RED-GREEN-REFACTOR loop for testing LLM failure modes.
- *Assessment:* While conceptually fascinating, implementing full TDD syntax for individual LLM prompts falls outside the current scope of our novel-authoring framework and protocol standardisation.

**Generic Auto-Publishing Pipelines**
- *Observation:* Some repositories manage complete epub-to-store logic.
- *Assessment:* As per `SPEC.md` (§3.2 Non-goals), proprietary publishing export logic remains out of scope for the Narrative Context Protocol.
