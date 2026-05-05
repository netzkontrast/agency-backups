# Brief — ADR-Governance Spec for the Agency Repo

## Raw user request

The prompt was rendered upstream by `research-prompt-optimizer v3.2.0` (intent slug `agency-adr-governance-spec`) and pasted into the same conversation that produced [Task 026 — cleanup-dramatica-skills-corpus](../../tasks/026-cleanup-dramatica-skills-corpus/). The user's literal instruction was:

> "Save the corresponding prompt als in that folder: …"

— meaning: save the rendered Category-B research prompt verbatim under `/prompts/agency-adr-governance-spec/` so a downstream agent can execute it when Task 027 transitions from `open` to `in_progress`.

## Target audience

The agent (Claude Code primary; any model-agnostic agent capable of repo-first reading + ADR-canon retrieval) that picks up [Task 027 — spec-subagent-subtask-prompt-format](../../tasks/027-spec-subagent-subtask-prompt-format/). The downstream beneficiary is the maintenance loop that needs a **single normative ADR-governance spec** covering: ADR lifecycle (proposed → accepted → superseded), token-efficient rule synthesis (compression ratio + semantic-fidelity bounds), and tooling acceptance criteria (Gherkin + JSON-Schema sketches + CLI shape — no reference implementation source code).

## Intended model / agent

Model-agnostic per the renderer's frontmatter (`target_agent: model-agnostic`). In practice the executing agent will be Claude Code or Jules — the prompt is fully self-contained and does not depend on Anthropic-specific tool surfaces.

## Use-case context

The agency repo currently has:

- a Frontmatter Ontology (Tasks 011 → 016 → 023) that governs file headers,
- a Narrative Ontology (Task 015) that governs Dramatica × NCP × Novel-Architect,
- per-spec normative-statement conventions sprinkled through TASK.md, PROMPT.md, RESEARCH.md, MAINTENANCE.md, AGENTS.md.

What it does **not** have is a unified ADR-governance contract that would let agents:

1. file an architectural decision (subtask format, sub-prompt format, subagent-dispatch convention, /sc:* command lifecycle, frustration-log format, …) as a versioned, auditable record;
2. supersede an ADR cleanly when a newer decision overrides an older one (the same `task_supersedes` / `task_superseded_by` pattern that already exists at the Task layer, lifted to spec-level decisions);
3. synthesise the ADR corpus into a token-efficient rules-file that AI coding agents load instead of the full ADR set (compression ratio + fidelity bounds = measurable, not vibes-based).

This prompt drives the research that produces that spec. Task 026 (the dramatica cleanup) is its first concrete use case: every subtask file under `tasks/026-cleanup-dramatica-skills-corpus/subtasks/` is **provisional** because the subtask format itself has no canonical contract yet — Task 027's research output (the ADR-governance spec) is intended to ratify or amend it.

## Constraints carried forward

- **CB1 (Repo-First).** The repo's root files (`README.md`, `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `MAINTENANCE.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`) are the first sources the executing agent reads. The produced spec MUST cite them in §0 and §2.
- **CB2 (Temporal Scope).** ADR fundamentals from 2011-01-01 (Nygard's post). Tooling / AI-agent-rule-file patterns / token-efficient synthesis from 2022-01-01 onward only.
- **CB3 (Output Exclusions).** No generic ADR-template recommendations divorced from the agency repo's actual structure. No concrete ADR records (the spec governs HOW ADRs are made, not their content). No reference implementation source code — interface contracts only (JSON-Schema sketches, CLI shape, Gherkin scenarios).
- **CB4 (Privacy).** Public OSS context. The repo is public.

## Why this prompt is filed even though Task 027 is `open`

Per [PROMPT.md §4](../../PROMPT.md), prompts MUST live in `/prompts/<slug>/` and MUST NOT be inlined inside `task.md`. Task 027 lists this prompt in its `task_uses_prompts` field so the audit graph (Task ↔ Prompt ↔ Research) is intact even before the prompt executes. When Task 027 transitions to `in_progress`, the executing agent reads `prompt.md` from this folder; the body's `prompt_relates_to_task: spec-subagent-subtask-prompt-format` field reciprocates the linkage.
