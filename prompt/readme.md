# Prompt Root

**What is this folder?** The root directory for all Prompt Tasks executed by agents in this repository. A Prompt Task is any task whose primary deliverable is a crafted, self-contained prompt intended for use by an AI agent or model.

**Why is it here?** To keep prompt engineering work cleanly separated from research (`/research`) and from root-level specification files. Prompts are operational artifacts — they get executed, refined, and versioned — and they deserve their own traceable task structure.

## Governing Specification

All work in this folder MUST conform to [PROMPT.md](../PROMPT.md) at the repository root.

## Contents

- [research-prompt-from-annotations/](./research-prompt-from-annotations/): A prompt that enables an agent to scan an existing research folder for open questions, annotations, and gaps, and generate new research prompts from those findings.

## Workflow Assumptions

- Each subfolder corresponds to exactly one Prompt Task, identified by a kebab-case slug.
- The slug is derived from the task's core intent, not from the date or a ticket number.
- `brief.md` in each task folder is immutable after creation — it records what was originally requested.
- `prompt.md` is the sole deliverable artifact; it MUST be executable in isolation.
