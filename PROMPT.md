# Prompt Task Specification

When handling a Prompt Task, the agent MUST enforce the following directory structure and workflow. This ensures every crafted prompt is traceable, self-contained, and improvable. No required file may remain completely empty.

## Directory Structure

For every new prompt task, create a dedicated subfolder within the root `/prompt` directory. The folder name is the `slugname` of the task. All folders must adhere to the rules in `FOLDERS.md`.

```text
/prompt
└── /<slugname>
    ├── readme.md     # Directory index with relative links and assumption logs.
    ├── brief.md      # The raw user request, target audience, intended model/agent, use-case context.
    └── prompt.md     # The deliverable: the final, self-contained crafted prompt.
```

Keep the structure flat per `FOLDERS.md`. Only create subfolders when 4 or more files of the exact same category accumulate (e.g., 4+ iteration drafts).

## Workflow Requirements

1. **Initialize Directory:** Create `/<slugname>/` immediately. Derive the slug from the brief's core intent (kebab-case, max 5 tokens).
2. **Store Brief:** Save the unedited user request and any contextual metadata into `brief.md`. This is the immutable record of what was asked.
3. **Select Framework:** Choose a prompt engineering framework based on the task type:
   - `RISEN + ReAct` — for multi-step research and extraction tasks where the agent must iterate.
   - `RISEN` — for structured one-shot output tasks (spec generation, code scaffolding).
   - `Chain-of-Thought` — for open-ended reasoning, analysis, or evaluation tasks.
   Declare the chosen framework explicitly at the top of `prompt.md`.
4. **Draft the Prompt:** Write `prompt.md` according to the Prompt Engineering Principles below.
5. **Pre-Commit:** Run through all Mandatory Pre-Commit Checks.

## Prompt Engineering Principles

Every prompt produced by a Prompt Task MUST satisfy the following:

1. **Self-Containedness:** The prompt MUST work without external context, prior conversation history, or out-of-band documentation. Every method, framework, constraint, and term MUST be defined inline.
2. **Framework Declaration:** State the structural framework (RISEN, ReAct, CoT) at the top. The executing agent must be able to identify the framework without guessing.
3. **RFC 2119 Normativity:** Use `MUST`, `SHOULD`, and `MAY` (as defined by RFC 2119) for normative requirements. Never use "please", "try to", or ambiguous hedging in mandatory clauses.
4. **Deliverable Lock:** Specify the output format precisely — including file names, section headings, data types, and encoding. Never leave the output format open to interpretation.
5. **Anti-Ambiguity:** If a term can mean two things in context, define it explicitly. Do not assume the executing agent shares your mental model.
6. **Constraint Isolation:** Group all exclusions, scope limits, and hard constraints into a dedicated `Narrowing` or `Constraints` section. Do not scatter them throughout the body.
7. **Failure Handling:** Specify what the agent MUST do when a step fails, a source is unavailable, or a required piece of information is not found. Never leave failure modes implicit.

## Mandatory Pre-Commit Checks for Prompt Tasks

Before committing the final deliverables of any Prompt Task, the agent MUST verify:

1. **Brief Integrity:** `brief.md` exists and contains the exact, unedited user request.
2. **Prompt Non-Empty:** `prompt.md` exists, is non-empty, and constitutes a complete, executable prompt.
3. **Self-Containedness Test:** Read `prompt.md` in isolation. Confirm no section requires external context to be actionable.
4. **Readme Audit:** Every folder touched during this task has a `readme.md` that explains the "what" and "why", uses relative Markdown links, and documents workflow assumptions.
5. **Frustration Log:** A feedback entry conforming to `FRUSTRATED.md` MUST be written. For prompt tasks that are part of a larger session, include it in the PR description as `## Frustration Log`. For standalone prompt-only sessions, add a `friction-log.md` adjacent to the task folder's `readme.md`.

Follow these rules for every prompt-oriented task without deviation.
