---
type: task
status: active
slug: skills-navigation-bootstrap
summary: "Research and design the internal skill navigation architecture, bootstrap process, and propose a root skill.md spec."
created: 2026-05-04
updated: 2026-05-04
task_id: "006"
task_status: open
task_owner: "jules"
task_priority: P1
task_uses_prompts:
  - skills-navigation-bootstrap
task_spawns_research: []
task_affects_paths:
  - prompts/skills-navigation-bootstrap/
  - research/skills-navigation-bootstrap/
  - tasks/006-skills-navigation-bootstrap/
---

# Task 006 — Skills Navigation and Bootstrap

## Goal
The goal of this task is to execute the `skills-navigation-bootstrap` prompt. This will produce a research workspace that investigates how skills should inter-reference, defines the skills bootstrap checkout process, proposes markdown indexing tools/schemas for token efficiency, and drafts a normative `skill.md` root specification. The task is complete when the research output is finalized and any unresolved architecture questions are filed as follow-up prompts.

## Plan
1.  **Initialize Research Workspace:** Create `/research/skills-navigation-bootstrap/` and snapshot the prompt.
2.  **Execute Research:** Follow the steps in the prompt to analyze the current `/skills/` structure, design the inter-referencing tools, and define the bootstrap process.
3.  **Synthesize Findings:** Document the proposed architecture, including the markdown indexing tool suite and schemas for header extraction.
4.  **Draft Deliverables:** Write the draft `skill.md` root specification within the research output directory.
5.  **Identify Follow-ups:** File any open questions or skipped components as new research-proposal or follow-up prompts.
6.  **Finalize:** Run all pre-commit checks on the research folder and close this task.

## Todo
- [ ] 1. Initialize `/research/skills-navigation-bootstrap/` workspace.
- [ ] 2. Execute research into skill navigation, bootstrapping, and markdown indexing.
- [ ] 3. Synthesize findings into `synthesis/` artifacts.
- [ ] 4. Draft the `skill.md` root spec in `output/SPEC.md`.
- [ ] 5. File open questions as follow-up prompts under `/prompts/`.
- [ ] 6. Ensure `task_spawns_research` is updated and all checks pass.

## Links
- Executing prompt: [`/prompts/skills-navigation-bootstrap/prompt.md`](../../prompts/skills-navigation-bootstrap/prompt.md)
