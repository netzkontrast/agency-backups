---
type: index
status: active
slug: dramatica-scenarios-foundation
summary: "Directory index for the foundational research prompt that drives the dramatica-scenarios Epic. Three-file scaffold per FOLDERS.md §4.1."
created: 2026-05-11
updated: 2026-05-11
---

# `dramatica-scenarios-foundation` — Prompt Directory Index

**What:** A `prompt_kind: research-proposal` prompt that, when executed by an
external research agent (Gemini Deep Research / Claude Research / Perplexity),
produces a foundational SPEC.md spec for the dramatica-scenarios Epic.

**Why here:** Per `FOLDERS.md` §1: the prompt belongs in `/prompts/`; the
research workspace it produces will live at `/research/dramatica-scenarios-
foundation/` (slug-equality rule). The Task that uses this prompt
(forthcoming Epic — Task 078 candidate) will reference it via
`task_uses_prompts: [dramatica-scenarios-foundation]`.

## Files

| File | Role |
|---|---|
| [`brief.md`](./brief.md) | Phase-1 intent capture: raw user request + 14 askuser answers + framework selection + acceptance criteria. Immutable record of what was asked. |
| [`prompt.md`](./prompt.md) | The deliverable: self-contained RISEN+ReAct research prompt with R / I / S / E / N sections, 4 explicit investigative steps (content-template + line-indexing + gap-analysis + Epic decomposition), and the SPEC.md output skeleton. |

## Audit graph

```text
prompts/dramatica-scenarios-foundation/prompt.md
        │ task_uses_prompts (forthcoming Epic) ──► tasks/<NNN>-dramatica-scenarios/task.md
        │ executed by agent ──────────────────────► research/dramatica-scenarios-foundation/output/SPEC.md
                                                            │ output drives ──► tasks/<NNN+1..NNN+M>-dramatica-scenarios-*/task.md (child Tasks)
```

## Execution status

- **Composed:** 2026-05-11.
- **Reader-test (Phase 4):** to be run before the Epic Task is created;
  findings fold back into `prompt.md` with inline `[reader-test:<id>]` tags.
- **Executed:** not yet — awaiting the Epic Task to reference + dispatch.

## Assumptions Log

- The user explicitly chose: novel.* scenarios only (lyric.* deferred to
  suno-lyric-writer's domain), EN-throughout bilingual contract, build-time
  line-index in `ontology.json`, new `nav.py instruct` subcommand
  (additive — does not modify the existing `by-id` contract), Phase-4
  reader-test ENABLED.
- The Epic decomposition target is the Task 070 pattern (umbrella + many
  child Tasks) per the user's Round-2 answer.
- The research executor is assumed to have file-read access to
  `/home/user/agency/`. If executed in an isolated context, the paths
  must be substituted with corresponding URLs to the public mirror.
