---
type: index
status: active
slug: cleanup-dramatica-skills-corpus
summary: "Index for Task 030 — clean up corruption / empty entries / PDF artefacts in dramatica-theory + dramatica-vocabulary, extend the navigator tooling so create/edit/deprecate/alias-load/precompile are mechanical, and emit precompiled persona-scenario JSON payloads for novel-architect + ncp-author consumption."
created: 2026-05-05
updated: 2026-05-05
---

# Task 030 — Cleanup Dramatica Skills Corpus + Tooling Extension

## What and Why

Phase-0 maintenance task on the Dramatica skills landed by [Task 015](../015-integrate-dramatica-ncp-skills/). Task 015's friction log explicitly named three v0.2 follow-ups (multi-quad encoding / term_file anchor cleanup / DE-locale alias coverage) but did NOT cover the larger corpus-corruption surface a working session surfaced: PDF page-break footers, broken `## Sex)` headings, mis-attributed YAML, "See X" empty redirect entries, and a lack of authoring tooling for create / edit / deprecate / alias-load / precompile workflows.

This task converts those surfaces into mechanical scripts and clean-corpus invariants. Its second purpose: produce the precompiled persona-scenario JSON payloads (`novel.*`, `lyric.*`) that `novel-architect` and `ncp-author` need to STOP reconstructing structured data from prose every query.

## Linked Navigation

- [`task.md`](./task.md) — the four §Goal acceptance gates, the nine-subtask plan, the Anti-Patterns list.
- [`notes.md`](./notes.md) — assumption log + meta-frustration log written **at planning time** (per the user's explicit request); separate from the `friction-log.md` written at task close.
- [`subtasks/`](./subtasks/) — nine `/sc:agent`-dispatchable subtask files; format is PROVISIONAL pending [Task 029](../029-adr-assumption-audit/).
- [`friction-log.md`](./friction-log.md) — written at task close per [`FRUSTRATED.md`](../../FRUSTRATED.md). Until then this file does not exist.
- ADR-governance prompt (owned by main): [`/prompts/agency-adr-governance-spec/`](../../prompts/agency-adr-governance-spec/) — stub pointing at the externally executed Gemini run at [`research/gemini/agency-adr-governance-spec/`](../../research/gemini/agency-adr-governance-spec/). This task does NOT execute it; the canonical ADR-governance work is owned by main's [Task 027](../027-adr-spec-research-synthesis/), [Task 028](../028-adr-tooling-impl-plan/), and [Task 029](../029-adr-assumption-audit/).

## Workflow Assumptions

- Subtask files under [`subtasks/`](./subtasks/) follow the Task 019 layout (briefing + inputs + acceptance criteria + falsification clause + agent-prompt block) because that is the closest precedent in the repo. They are PROVISIONAL: if main's [Task 027](../027-adr-spec-research-synthesis/) ADR-governance spec invalidates the layout, this task's subtask files re-render under the new contract before Phase A dispatches.
- The `/sc:agent` invocation syntax is inferred from Task 019. Worktree isolation is used selectively (Phase B only); Phase A runs in main-tree because its subtasks touch overlapping markdown.
- `tools/dramatica-nav/` is the home for new tooling rather than `tools/fm/` because the new tools couple to the Narrative Ontology, not the Frontmatter Ontology — and rule [`AGENTS.md § NO.5`](../../AGENTS.md) prohibits cross-loading. New scripts ARE allowed to reuse the lightweight `tools/fm/_core.py` helpers (e.g., `iter_operational_files`) where they don't pull in the frontmatter-ontology JSON.
- **Verbosity is intentional in `notes.md`.** The user explicitly asked for a "verlose Frustration Log" of the planning session itself so a downstream reader (most likely main's [Task 029](../029-adr-assumption-audit/) assumption-audit subagent) can extract pattern requirements. Do not collapse it on the next coherence pass without their consent.
