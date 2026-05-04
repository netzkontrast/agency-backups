# research-prompt-from-annotations

**What is this folder?** A Prompt Task that produces a self-contained prompt enabling any agent to scan a completed or in-progress research folder for unresolved annotations, open questions, [NOT-FOUND] gaps, and friction-log suggestions — then generate one or more follow-up research prompts in the `research-prompt-optimizer v2.1.0` format.

**Why is it here?** The existing `RESEARCH.md` workflow produces rich reflection artifacts (`friction-log.md`, `reflection/M*.md`, synthesis gaps) but provides no standardized path for converting those artifacts into new, actionable research prompts. This task fills that gap by producing a reusable prompt that treats completed research folders as structured input for the next research cycle.

## Contents

- [brief.md](./brief.md): The original user request that initiated this task.
- [prompt.md](./prompt.md): The deliverable — a self-contained prompt for the research-prompt-optimizer annotation-expansion capability.

## Workflow Assumptions

- The deliverable `prompt.md` is designed to be given verbatim to an agent together with a path to an existing `/research/<slug>/` folder.
- It does not require the `research-prompt-optimizer` skill to be installed; the prompt is fully self-contained.
- The output of executing `prompt.md` against a research folder is one or more new prompt files deposited into `/prompt/<new-slug>/prompt.md`.
- Analogy: `RESEARCH.md` governs how research is *executed*; this prompt governs how research *outputs* are recycled into new research tasks.
