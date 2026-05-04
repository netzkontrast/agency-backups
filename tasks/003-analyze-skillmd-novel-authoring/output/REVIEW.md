---
type: note
status: active
slug: task-003-review
summary: "Post-merge code review of Jules' Task 003 output. Documents MUST/SHOULD violations and positive findings."
created: 2026-05-04
updated: 2026-05-04
---

# Code Review — Task 003 (PR #23)

**Reviewer:** claude-code (claude/stoic-mendel-Kwncp)
**PR:** [#23 — task/003-analyze-skillmd-novel-authoring](https://github.com/netzkontrast/agency/pull/23)
**Head commit:** `6a8c86c`
**Governing specs consulted:** AGENTS.md, TASK.md §3–§7, PROMPT.md §2–§5, FOLDERS.md §2–§4, PRE_COMMIT.md §1–§7

---

## Summary

Jules produced a technically coherent analysis of the Gemini research and correctly derived the three unresolved open questions into follow-up prompts. The RECOMMENDATIONS.md content is well-structured and directionally accurate. However, the commit contains **four MUST violations** and **five SHOULD violations** that compromise audit-graph integrity and frontmatter consistency. None of them require rework of the analytical content — they are structural/metadata issues that can be fixed in a follow-up commit.

---

## Critical: MUST Violations

### V1 — `task_spawns_research` lists prompt slugs, not research workspaces

**File:** `tasks/003-analyze-skillmd-novel-authoring/task.md`

```yaml
task_spawns_research:
  - mega-context-limit-management
  - cross-skill-context-poisoning
  - subjective-quality-evaluation
```

Per TASK.md §3.3 and FOLDERS.md §6, `task_spawns_research` MUST contain slugs of research workspaces (`/research/<slug>/`) produced by the task. None of the three slugs above resolve to an existing `/research/` directory — they resolve to `/prompts/`. Jules created follow-up **prompts**, not research workspaces. The field MUST be `task_spawns_research: []` until an agent actually executes one of these prompts and produces a research run. Populating it prematurely with prompt slugs corrupts the frontmatter audit graph that tooling (e.g., a future `validate-graph.py`) would traverse.

**Fix:** Set `task_spawns_research: []` in task.md. No field in task frontmatter currently captures "prompts spawned by this task" — that direction flows through the prompts' own `prompt_relates_to_task` field, which Jules correctly populated.

---

### V2 — L1 `status: active` inconsistent with L2 `task_status: done`

**File:** `tasks/003-analyze-skillmd-novel-authoring/task.md`

```yaml
status: active       # L1 — should be "completed"
task_status: done    # L2 — correct
```

TASK.md §4 step 6 ("Close") requires updating frontmatter when closing. The L1 `status` field was not updated from `active` to `completed`. Per TASK.md §7.1 (Frontmatter Integrity pre-commit check), the task MUST carry consistent status signals across both layers. `status: active` signals to a scanning agent that this task is still open, directly contradicting `task_status: done`.

**Fix:** Change `status: active` → `status: completed`.

---

### V3 — `output/` subfolder created below the 4-file threshold

**File:** `tasks/003-analyze-skillmd-novel-authoring/output/` (2 files: RECOMMENDATIONS.md + readme.md)

FOLDERS.md §4 states: "Do not create a subfolder unless 4+ files of the exact same category accumulate." With only two files, the subfolder is premature. RECOMMENDATIONS.md and its readme belong at the task root (`tasks/003-analyze-skillmd-novel-authoring/`), not in a dedicated `output/` directory.

Note: The previous commit already created `output/` as a scaffold, so Jules inherited this pre-existing violation rather than introducing it. However, it was not corrected at closure time, and TASK.md §7.6 requires a readme audit before committing a closed task.

**Fix:** Move RECOMMENDATIONS.md to the task root; delete `output/`; update references in task.md's `## Links` section and in the task readme.

---

### V4 — RECOMMENDATIONS.md has no frontmatter

**File:** `tasks/003-analyze-skillmd-novel-authoring/output/RECOMMENDATIONS.md`

AGENTS.md §Frontmatter Ontology states: "Files inside operational directories (`/tasks/`, `/prompts/`, `/research/`) MUST carry frontmatter." RECOMMENDATIONS.md is the primary deliverable artifact of this task and carries no L1 frontmatter at all. The `tools/validate-frontmatter.py` did not flag this because the tool only validates files that already have frontmatter — it cannot detect absent frontmatter on files with no YAML block.

**Fix:** Prepend L1 frontmatter with `type: note`, `status: active`, `slug: task-003-recommendations`, appropriate `summary`, `created`, `updated`.

---

## Significant: SHOULD Violations

### S1 — `prompt_framework: CoT` incorrect for research-proposal follow-ups

**Files:** All three new `prompts/*/prompt.md`

All three follow-up prompts declare `prompt_framework: CoT`. Per PROMPT.md §4.3, `Chain-of-Thought` is designated for "open-ended reasoning, analysis, or evaluation." These prompts are **research proposals** (`prompt_kind: follow-up`) that, when executed, should spawn structured research workspaces requiring iteration, source triangulation, and reflection checkpoints. The correct framework would be `RISEN+ReAct` ("multi-step research and extraction tasks where the agent must iterate") or `RISE-DX` ("reflection-driven execution"). Using CoT tells the executing agent to apply a flat reasoning chain rather than a structured iterative research protocol, which is likely to produce lower-quality outputs for these specific questions.

---

### S2 — `prompt_target_agent: "Claude Code"` inappropriate for empirical research prompts

**Files:** All three new `prompts/*/prompt.md`

Claude Code is a software engineering CLI — it cannot "design and execute a benchmark", "investigate neural architectures", or conduct empirical DE/EN A/B tests without access to model internals or a test harness. The original research prompt (correctly) used `prompt_target_agent: external` (Gemini). These follow-up prompts should target `Gemini`, `external`, or `any`. Directing them at Claude Code will result in the prompt being unexecutable in the intended context.

---

### S3 — brief.md files contain only a single sentence; required fields missing

**Files:** `prompts/*/brief.md`

PROMPT.md §2 defines brief.md as: "Raw user request, target audience, intended model/agent, use-case context." Each brief.md here is a single sentence paraphrasing the research question. No target audience, no model/agent designation, and no use-case context are provided. While brief.md is an informal record rather than a normative artifact, the spec's intent is to preserve the original commissioning context so future agents understand *why* the prompt was written — a one-sentence paraphrase loses this.

---

### S4 — Prompt bodies do not declare their framework

**Files:** All three new `prompts/*/prompt.md`

PROMPT.md §5.2 (Framework Declaration): "Frontmatter `prompt_framework` and **a body header naming the framework**." The prompt bodies jump directly to `## 1. Context` with no framework declaration header. A future agent reading the body alone has no reminder of what protocol to apply.

---

### S5 — Prompts reference SKILL.md without defining it inline

**Files:** All three new `prompts/*/prompt.md`

PROMPT.md §5.1 (Self-Containedness): "Works without external context, prior conversation history, or out-of-band documentation. Every method, framework, constraint, and term MUST be defined inline." Each prompt assumes the executing agent knows what "SKILL.md specification" is without providing a definition or reference URL. An agent with no prior context on this repository would be unable to execute the prompt correctly.

---

## Positive Findings

- **Open-question extraction is complete and accurate.** All three unresolved vectors from `result.md §Open Questions and Unresolved Vectors` map 1:1 to the three new prompts. Coverage is 100%.
- **RECOMMENDATIONS.md content is analytically sound.** The three-tier structure (immediately actionable / requires further research / out of scope) cleanly maps to the task plan. The cross-referencing against the internal `ncp-novel-co-authoring-spec` SPEC.md (`§7.3`, 8-phase Skill Catalog) shows Jules read the in-house research.
- **Frontmatter on prompt.md files is mostly correct.** `prompt_kind`, `prompt_relates_to_task`, and `prompt_spawned_from_research` are all properly populated.
- **FL0 declaration in commit message.** PRE_COMMIT.md §3 allows inlining the FL0 declaration in the commit message rather than a separate file; Jules did this correctly.
- **Prompt readme files are well-structured.** All three include What/Why, linked navigation, and an assumptions log per FOLDERS.md §3.

---

## Required Follow-up Actions

| # | Severity | File | Action |
|---|---|---|---|
| 1 | MUST | task.md | Set `task_spawns_research: []` |
| 2 | MUST | task.md | Change `status: active` → `status: completed` |
| 3 | MUST | RECOMMENDATIONS.md | Add L1 frontmatter |
| 4 | MUST | output/ folder | Move RECOMMENDATIONS.md to task root; remove premature subfolder |
| 5 | SHOULD | All 3 prompt.md | Change `prompt_framework` from `CoT` to `RISEN+ReAct` |
| 6 | SHOULD | All 3 prompt.md | Change `prompt_target_agent` from `"Claude Code"` to `"Gemini"` or `"external"` |
| 7 | SHOULD | All 3 brief.md | Expand to include target audience, intended model, use-case context |
| 8 | SHOULD | All 3 prompt.md | Add framework declaration header in body |
| 9 | SHOULD | All 3 prompt.md | Add inline definition of "SKILL.md" term |
