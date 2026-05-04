# Phase 3 — Render

> **Status: ✅ Implemented since v3.1.0** — extended in v3.2.0 with
> append-only versioning (`_v2.md`, `_v3.md` ...) and v3.2 provenance
> frontmatter (see `meta-prompt-spec.md` §3.1).
>
> Phase 3 is the deterministic render layer that turns an approved
> `meta-prompt.yaml` (Phase 2 output) into the final
> `research-prompt_<slug>.md` file the user hands to an external
> research agent.

## Implementation

**File:** `render/render.py` (single-file Python module)
**Stack:** Python 3.10+, `pyyaml`, stdlib only — no Jinja, no external
templating engine.

## Inputs

- `meta-prompt_<slug>.yaml` — Phase 2 output, schema_version `2.0`,
  `approved: true`
- `catalog.yaml` — master module index
- `modules/**/*.md` — frontmatter + body templates
- `--skill-root` (defaults to cwd)
- `--output-dir` (defaults to `/mnt/user-data/outputs`)

## Outputs

- `research-prompt_<slug>.md` — final 800–1200 line Markdown prompt
- stderr warnings if non-fatal issues encountered (unfilled
  `phase2_fill` slots, divergent cross-module slot values, etc.)

## Behaviour — 7 Pipeline Stages

1. **LOAD** — parse YAML, resolve catalog → file paths
2. **VALIDATE** — schema_version match, `approved == true`,
   mandatories present, cross-pollination count == 2
3. **LOAD MODULES** — walk active module ID list, parse frontmatter,
   extract render template from fenced block
4. **AUTO-FILL BRIDGE** — if `slot_fills.m3-batch` is missing but
   `batches[]` declares a domain batch, derive m3-batch slots from it
5. **SLOT RESOLUTION** — three layers, in order:
   (a) global slots (topic, slug, language, etc.)
   (b) cross-module phase2_fill flatten (so e.g. `M13.orthogonal_lens`
       is visible inside `final-checklist`)
   (c) `fill_from` handler invocation
   Per-module phase2_fill values override globals.
6. **ASSEMBLE** in Schema-3 ordering (see "Schema 3 Section
   Ordering" below)
7. **POST-RENDER CHECK** — find any unfilled `{{slot}}` that ISN'T
   tagged `agent_runtime_fill` in module frontmatter; warn (non-fatal)

## The Four Slot Types — How Each Resolves

| Type | Resolution |
|------|-----------|
| `phase2_fill` | Looked up in `meta-prompt.slot_fills.<module_id>.<slot>`. Required-but-unfilled emits a stderr warning. Cross-module flatten makes values visible to OTHER modules' templates too. |
| `phase2_fill_or_runtime` | Same as `phase2_fill` if value present; otherwise the placeholder is preserved as `{{slot}}` for the executing agent. |
| `agent_runtime_fill` | NEVER substituted. Always preserved as `{{slot}}` in the output for the executing agent to fill. |
| `fill_from` | Computed by a deterministic Python handler in `FILL_FROM_HANDLERS` registry. |

## fill_from Handler Registry

The handlers are stateless functions taking `RenderContext` and
returning a string. Adding a new handler:

1. Define `def fillfrom_<slot_name>(ctx: RenderContext) -> str: ...`
2. Register in `FILL_FROM_HANDLERS` dict
3. Use `{{<slot_name>}}` in any module body

Current handlers (as of v3.2.0) cover: active method anchors, CB
restatement blocks, method restatement blocks, bespoke synthesis
component rendering, frontmatter list rendering (methods, CBs,
cross-pollinations), bespoke provenance, category-specific synthesis
sub-templates, conditional world-change-log, and m3-batch render
blocks (items, iteration steps, output schema).

## Schema 3 Section Ordering

Implemented in `assemble_final_document`:

1. YAML frontmatter (from `frontmatter-template` partial)
2. Title + executing-AI callout (inside meta-header)
3. Meta-header — composes 4 sub-blocks: language-warning
   (conditional) + category block + react block + structural framework
4. Constraint Blocks — CB-0 from `m0-reflection` module body, CB-1..N
   from authored content in `meta-prompt.constraint_blocks`
5. Critical-Thinking Methods — each method module's render template
6. Steps & Replication Mechanisms — M2 restatement template + M3
   batch (if active) + cross-pollination blocks
7. Pre-Synthesis Integrity Check — M4 module body
8. Synthesis schema — synthesis-schema partial body
9. Self-Verification Checklist — final-checklist module body
10. End marker

## Template Extraction Strategy

Module bodies have documentation wrappers AND fenced render templates.
The renderer extracts the first fenced markdown (or yaml) block
AFTER a `## Rendered ...` H2 heading. Falls back to the first fenced
block in the body if no heading match. Falls back to body-as-is if no
fenced block exists (e.g. some pure-template partials).

This makes modules self-documenting (read for a human) AND
machine-renderable (extract the fenced block).

## What Phase 3 Does NOT Modify

Phase 3 is a strict read+compose layer. It does not:
- Change `meta-prompt.yaml`
- Modify any module file
- Add to the catalog
- Adjudicate Phase-2 self-applied hook results (those are baked into
  the meta-prompt and rendered as-is into the plan-view; Phase 3
  doesn't see them in the final output because they live in
  `meta-prompt.self_reflection`, not in `slot_fills`)

The only side effect outside `output_dir` is stderr warnings.

## CLI

```bash
# Direct invocation
python3 render/render.py examples/example-meta-prompt.yaml \
    --skill-root . \
    --output-dir /mnt/user-data/outputs

# Programmatic
from render.render import render_meta_prompt
out_path = render_meta_prompt(
    meta_prompt_yaml=Path("plan.yaml"),
    skill_root=Path("."),
    output_dir=Path("/tmp/out"),
)
```

## Tested Against

- `examples/example-meta-prompt.yaml` (EU-AI-Act SaaS, Cat-B,
  RISEN, 6 methods, 2 cross-pollinations, 4 batches)
- Output: 900 lines, 13 sections, all agent_runtime slots preserved,
  0 unfilled non-runtime slots, 0 Jinja remnants

## Known Limitations / Future Polish

1. **Bespoke synthesis** not yet end-to-end-tested with a `bespoke`
   framework_structural choice. The handlers exist but no example
   meta-prompt drives them yet.
2. **Cat-A and Cat-C examples** not yet rendered. Cat-B is the
   default test; Cat-A would verify the `hypothesis_tree` synthesis
   sub-template; Cat-C would verify `world_change_log_section_or_empty`
   emission + `periodic_brief` sub-template.
3. **Rich slot types in m3-batch** — when `iteration_steps` comes
   from Phase 2 as actual prose (not just method-default stubs), the
   render-block handler should preserve the prose; currently joins
   list items with newline+numbering.
4. **Slot-name collisions** across modules currently warn on
   divergent values (first-write-wins). Could promote to error or
   namespace slots per-module if collisions become common.
5. **No incremental render** — every run re-reads all modules.
   Acceptable for current sizes but worth caching when catalog grows.

## Why Pure Python (no Jinja)

The skill ships into a constrained execution environment. Pure
stdlib + pyyaml means zero install friction. The slot system is
simple enough (4 types, regex substitution, deterministic handlers)
that a templating engine would add 5× the code surface for no gain.
Audit-friendliness > clever templating.
