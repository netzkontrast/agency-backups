# research-prompt-optimizer

A four-phase pipeline that turns vague research intent into a
self-contained Markdown research prompt consumable by external
research agents — Gemini Deep Research, Perplexity, GPT Deep
Research, Claude Research, or any custom agentic pipeline.

**Current version:** 3.2.2 (stable). Four-phase pipeline.

---

## What it does

You ask a research question. The skill:

1. **Phase 1 — Intent Capture.** Loops with you (file-first status
   views, askuser for ambiguities) until every required slot of the
   research brief is filled and explicitly approved. Outputs
   `intent_<slug>.yaml`.
2. **Phase 2 — Planning.** Selects critical-thinking methods,
   prompt-engineering frameworks, replication mechanisms, and
   cross-pollination blocks from the catalog. Authors constraint
   blocks and seed queries. Walks you through three mini-gates
   (routing → modules+CB → final plan). Outputs
   `meta-prompt_<slug>.yaml`.
3. **Phase 3 — Render.** Composes the final
   `research-prompt_<slug>.md` from the approved plan and writes it
   to `/mnt/user-data/outputs/` with v3.2 provenance frontmatter
   (versioned `_vN.md` if a previous render exists).
4. **Phase 4 — Reader Test.** Audits the rendered prompt with a
   fresh-frame pass: 5 reader questions + ambiguity / assumption /
   contradiction sweeps. Outputs `research-prompt-audit_<slug>.md`.
   You accept or loop back to fix.

The rendered prompt is self-contained: the external research agent
sees no skill internals, no conversation history, no implicit
context — only the Markdown file.

---

## Where things live

| File / folder | What |
|---------------|------|
| [SKILL.md](./SKILL.md) | The router. Phase 1 + Phase 2 algorithms inline; Phase 3 invoked via `render/render.py` |
| [AGENTS.md](./AGENTS.md) | Project-specific rules for agents working on this skill (extends [`../AGENTS.md`](../AGENTS.md)) |
| [CHANGELOG.md](./CHANGELOG.md) | Version history (3.0.0-phase1 → 3.2.2) |
| [catalog.yaml](./catalog.yaml) | Machine-readable index of all 34 modules + 5 partials + 1 verification + 7 self-applied hooks |
| [meta-prompt-spec.md](./meta-prompt-spec.md) | Schema 1 (intent.yaml) + Schema 2 (meta-prompt.yaml) + Schema 3 (rendered .md) |
| [render/](./render/) | Phase 3 implementation — single-file Python renderer |
| [phases/](./phases/) | Detail-level specs for each phase, lazy-loaded from `SKILL.md` |
| [modules/](./modules/) | All building-block module files consumed by Phase 2 + 3 |
| [docs/](./docs/) | Per-module concept docs (design rationale, slot provenance, extension points) |
| [examples/](./examples/) | Worked YAML outputs used as renderer smoke-test fixtures |
| [phase2-design-plan.md](./phase2-design-plan.md) | Frozen v1.2 spec the planning algorithm was built against (historical reference) |

Every folder has its own `readme.md` with linked navigation —
follow them down for details.

---

## Quick start

The skill auto-triggers on phrases like *"deep research prompt"*,
*"investigate"*, *"competitive analysis"*, *"systematic review"*,
*"Marktanalyse"*, *"Due Diligence"*. Just describe what you want to
research; the skill takes over.

If you want to invoke Phase 3 manually after Phase 2 has produced a
`meta-prompt_<slug>.yaml`:

```bash
python3 render/render.py meta-prompt_<slug>.yaml \
    --skill-root . \
    --output-dir /mnt/user-data/outputs
```

---

## Design principles

- **Strict four-phase pipeline.** Each phase has a hard exit gate.
  Hand-off between phases is structured YAML, never prose context.
- **Approval gates.** Phase 1 and Phase 2 write their YAML files only
  after you explicitly approve. No silent state advancement.
- **4-type slot system.** Every placeholder in every module is one of
  `phase2_fill` / `phase2_fill_or_runtime` / `agent_runtime_fill` /
  `fill_from`. Phase 2 prompts you only for slots that actually need
  human input; everything else is computed or deferred.
- **Self-applied critical thinking.** Phase 2 applies seven of its
  own catalog methods (M01, M03, M05, M07, M0, M4, M13) to its own
  planning work, depth-scaled.
- **ReAct-loop-anchored synthesis table.** The KEY INNOVATION
  ([modules/partials/react-loop-anchored.md](./modules/partials/react-loop-anchored.md)) —
  inline active-methods table inside the ReAct loop, anti-drift
  mechanism for long agent runs.
- **Progressive disclosure.** `SKILL.md` ≤ 500 lines, eager-loaded.
  Everything else is lazy-loaded on demand via the reference-files
  table in `SKILL.md`.

---

## For contributors / agents

If you are an agent or human working on this skill, read
[AGENTS.md](./AGENTS.md) first. It defines the schema-change rules,
catalog/module discipline, the 500-line pressure tracker, and the
project-specific pre-commit additions.

For session-end frustration logging conventions and the generic
skill-development rules: see [`../AGENTS.md`](../AGENTS.md).
