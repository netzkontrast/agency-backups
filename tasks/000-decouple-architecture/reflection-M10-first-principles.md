# M10 — First-Principles Decomposition

**Method:** Strip each concept to its irreducible essence, name the *information* it carries, then design the data-structure around that information rather than around legacy folder names.

## Atomic Definitions

| Concept | Irreducible Essence | What It Carries |
|---|---|---|
| **Task** | A reified intention with a falsifiable outcome. | Goal, Plan, Todo, links to instruction set, links to evidence. |
| **Prompt** | A reified instruction set, executable in isolation. | Role, Input, Steps, Expectations, Constraints. |
| **Research** | A reified attempt at execution; evidence captured. | Workspace, Synthesis, Reflection, Output. |

## Why the Decoupling

Three concepts → three irreducible information shapes → three directories. Conflating them (the pre-refactor state, where prompts and research lived in the same `/research/<slug>/`) collapsed three different lifecycles into one. Specifically:

1. **Task lifecycle** is *coordination-bound*: open → in_progress → done/abandoned/blocked. Owned by an orchestrator.
2. **Prompt lifecycle** is *authorship-bound*: draft → active → archived. Owned by a prompt engineer.
3. **Research lifecycle** is *execution-bound*: kickoff → synthesis → reflection → complete. Owned by an executor.

Forcing these into one directory meant friction-logs had to be re-purposed for prompt critique, follow-up questions had to be jammed into research outputs, and there was no place to record cross-run coordination work.

## Why the Frontmatter Ontology Is Flat

LLMs hallucinate on nested YAML (per the obsidian-frontmatter spec). A graph is also flat: nodes have attributes, edges are foreign keys. Therefore the ontology is intentionally a *node table* (L1 + L2 namespaces) plus *edge keys* (`task_uses_prompts`, `research_executes_prompt`, etc.). Future tooling can build a graph in O(N) by reading the table.

## Why L3 Is Sidecar

Vector embeddings, graph scores, and token matrices are *agent-only* metadata. They serve no human reader and they explode the YAML beyond the Obsidian Properties UI's tolerance. Per the source ontology, L3 belongs in `.agent_cache/<file>.meta.json`. This Task does not yet need L3, but the spec reserves the convention so future tooling does not collide with L1/L2.

## What Could Have Been Different

A first-principles re-derivation might have collapsed `/prompts/` into `/tasks/` if every prompt always belonged to exactly one Task. It does not: tool-instruction prompts are reusable across tasks; follow-up prompts surface from research without yet having a coordinating task. Therefore prompts are independent first-class artifacts. The decoupling is justified.
