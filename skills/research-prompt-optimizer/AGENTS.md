# Agent Instructions — research-prompt-optimizer

This file extends [../AGENTS.md](../AGENTS.md). Read that first.

This document captures rules and conventions specific to the
**research-prompt-optimizer** skill — a three-phase pipeline that
turns vague research intent into a fully-rendered Markdown research
prompt consumable by external research agents (Gemini Deep Research,
Perplexity, Claude Research, GPT Deep Research, custom pipelines).

---

## 1. The Three-Phase Contract

The skill is a strict pipeline. Each phase has a hard exit gate and a
typed YAML hand-off file. **No phase ever consumes prose context from
a previous phase — only YAML.**

| Phase | Input | Output | Approval gate |
|-------|-------|--------|---------------|
| 1 — Intent Capture | user's raw message | `intent_<slug>.yaml` | user `Approve` button |
| 2 — Planning | `intent_<slug>.yaml` | `meta-prompt_<slug>.yaml` | user `Approve` button |
| 3 — Render | `meta-prompt_<slug>.yaml` | `research-prompt_<slug>.md` | renderer exits clean |

**Hard rule:** never skip an approval gate. Approval is the file-write
trigger for Phase 1 and Phase 2. Phase 3 has no user-approval gate —
its gate is the renderer's own validation (zero unfilled
non-runtime slots, zero schema violations).

**Hard rule:** never modify an upstream YAML. Phase 2 reads
`intent.yaml` but only Phase 1 writes it. Same for `meta-prompt.yaml`
and Phase 2.

---

## 2. Schema Discipline

Three schemas govern this skill:

- **Schema 1** — `intent.yaml` shape. Defined in
  [meta-prompt-spec.md](./meta-prompt-spec.md).
- **Schema 2** — `meta-prompt.yaml` shape. Defined in same.
- **Schema 3** — assembled `research-prompt.md` section order.
  Implemented in [render/render.py](./render/render.py).

**Schema-change rules:**

| Change | Allowed without bump | Requires |
|--------|---------------------|----------|
| Add optional field to Schema 1 or 2 | Yes — patch bump | Update `meta-prompt-spec.md` + `examples/example-*.yaml` |
| Add required field to any schema | No | Major bump + migration note in `NEXT_STEPS.md` (or `CHANGELOG.md` if introduced) |
| Reorder sections in Schema 3 | No | Major bump; renderer test fixtures must be regenerated |
| Add new slot type beyond the four (`phase2_fill` / `phase2_fill_or_runtime` / `agent_runtime_fill` / `fill_from`) | No | Architectural decision; document rationale in `phases/phase3-render.md` |

---

## 3. Catalog & Module Discipline

`catalog.yaml` is the single source of truth for which modules exist
and how Phase 2 selects among them. **Every file in `modules/*/` MUST
be registered in `catalog.yaml`** — and conversely, every entry in
`catalog.yaml` MUST point at a real file on disk.

**Current module census** (verify with
`ls modules/*/*.md | wc -l`):

| Type | Count | Location |
|------|-------|----------|
| Methods (M01–M13) | 13 | [modules/methods/](./modules/methods/) |
| Frameworks | 7 | [modules/frameworks/](./modules/frameworks/) |
| Replication mechanisms | 5 | [modules/replication/](./modules/replication/) |
| Cross-pollinations | 6 | [modules/cross-pollination/](./modules/cross-pollination/) |
| Categories | 3 | [modules/categories/](./modules/categories/) |
| Partials | 5 | [modules/partials/](./modules/partials/) |
| Verification | 1 | [modules/verification/](./modules/verification/) |

**When adding a new module:**

1. Create the file in the correct subfolder of `modules/`.
2. Register it in `catalog.yaml` with `provides`/`requires` edges.
3. If it has a concept doc, create the corresponding file under
   `docs/<type>/<id>.md`.
4. If it is a method, framework, or replication mechanism, decide
   whether any category's `default_methods` / `default_framework_*`
   list should now include it.
5. Update [modules/readme.md](./modules/readme.md) and the type-
   subfolder readme.

**Naming conventions:**

- Methods: `m<NN>-<kebab-slug>.md`, where `NN` is a two-digit number
  matching the M01–M13 catalog ordering.
- Frameworks: `<lowercase-name>.md`.
- Cross-pollinations: `<source>-into-<target>.md` (e.g.
  `b-into-a.md`).
- Categories: `<letter>-<descriptor>.md` (e.g. `a-exploration.md`).

---

## 4. Self-Applied Hooks (Q6 Mechanism)

Phase 2 applies seven of its own catalog methods to its own planning
work — see [SKILL.md](./SKILL.md) "Self-Applied Hooks Map" and
`catalog.yaml`'s top-level `self_applied_phase2_index`.

**Rule:** if you add or modify a method in `catalog.yaml`, check
whether it is referenced in the `self_applied_phase2_index`. If yes,
update both. If not, decide whether the new/changed method *should*
become a Phase-2 self-applied hook and document the decision in
[modules/methods/readme.md](./modules/methods/readme.md).

**Depth gating:**

| `intent.depth` | Self-applied hooks active |
|----------------|---------------------------|
| `surface` | Only M4 6-item integrity check; `hooks_skipped_reason` populated for the rest |
| `standard` | All 7 hooks active; M03 produces 3 pre-mortem items |
| `exhaustive` | All 7 hooks active; M03 produces 5 pre-mortem items |

---

## 5. The 500-Line Pressure Tracker

`SKILL.md` is the eagerly-loaded router. It must stay ≤ 500 lines.

**Cadence:** at the end of every session that touched `SKILL.md`,
log `wc -l SKILL.md` against this watermark:

```
historical: 441 (v3.0-phase2) → 497 (v3.1.0 pre-cleanup)
            → 489 (v3.1.0 post-consistency-pass)
            → 687 (v3.2.0 mid-kaizen, 4-phase + provenance)
            → 497 (v3.2.0 post-compression)
            → 508 (v3.2.0 post-skill-creator-review,
                   description expanded for triggering;
                   body still 470 lines, frontmatter 38)
            → 572 (v3.3.0 opt-in audit + Phase 5 finalize;
                   body 572, frontmatter 28; 14% over budget)
budget:     500 hard for body; frontmatter excluded
                   ⚠ v3.3.0 breaches budget. Compression candidates:
                   Phase 5 algorithm block (could move detail to
                   phases/phase5-finalize.md); Anti-Patterns table
                   (4 new rows could collapse into 2). Defer until
                   next routine review pass.
```

**When the file approaches 500:**

1. Look first at sections that duplicate `phases/*.md` or
   `meta-prompt-spec.md`. The reference-file pattern means the
   detail belongs there, not here.
2. Look at status tables and version annotations — these accumulate
   cruft fastest.
3. Only as last resort: move a whole sub-section into a new
   `phases/*.md` reference file.

**Never** compress by removing the askuser-loop algorithm, the
hard-rules block, or the anti-patterns table. Those are
behavior-shaping, not documentation.

---

## 6. The `_archive/` Convention

When a major version is superseded:

- Move the old SKILL.md, modules, etc. to `_archive/v<old>/`
- The `_archive/` tree is exempt from rules in §3 (no catalog
  registration, no readme touching) — it is frozen historical record
- A "diff harness" run comparing old vs new should be logged in
  `NEXT_STEPS.md` or a `CHANGELOG.md`

**Currently no `_archive/` exists** — v3.1.0 and v3.2.0 were in-place
evolutions of v3.0. The next major (v4.0) will trigger archival.

---

## 7. Project-Specific Pre-Commit Additions

Beyond the generic [../AGENTS.md §5](../AGENTS.md#5-pre-commit-checklist-mandatory)
checklist, this skill adds:

### 7.1 End-to-end render smoke test

Before any commit that touches `render/`, `catalog.yaml`, or any file
in `modules/`:

```bash
cd /path/to/research-prompt-optimizer
python3 render/render.py examples/example-meta-prompt.yaml \
    --skill-root . \
    --output-dir /tmp/render-smoke
```

Must exit 0. Stderr warnings are tolerable only if they reference
`agent_runtime_fill` slots (those are intentional). Any
`phase2_fill` slot showing as unfilled is a hard fail.

### 7.2 Schema-version reconciliation

If you bumped any schema version, grep for the old version string
across `meta-prompt-spec.md`, `SKILL.md`, `catalog.yaml`,
`render/render.py`, and `examples/*.yaml`. Zero remaining matches.

### 7.3 `created_by_skill` fixture sync

If `metadata.version` in [SKILL.md](./SKILL.md) frontmatter changed,
the `created_by_skill` field in:

- The YAML output template inside `SKILL.md` (Phase 1 output block)
- `examples/example-intent.yaml`
- `examples/example-meta-prompt.yaml`

must all match the new version.

---

## 8. Override Rationale (vs. Generic AGENTS.md)

This file does not currently override any rule from
[../AGENTS.md](../AGENTS.md) — it only adds. If a future override
becomes necessary, document it here with:

1. Which rule is overridden
2. Why (concrete failure mode the override prevents)
3. Whether the override should generalize back to `../AGENTS.md`
