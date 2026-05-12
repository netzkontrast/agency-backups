---
type: index
status: active
slug: flexible-frontmatter-toolchain-synthesis
summary: "Structured synthesis artefacts for the flexible-frontmatter-toolchain run."
created: 2026-05-05
updated: 2026-05-05
---

# Synthesis

Flat layout per `FOLDERS.md`. The hard result of the run is collapsed into the bullets below; the deliverable lives at [`../output/SPEC.md`](../output/SPEC.md).

## Hard Results

1. **Required-only is enforceable today** — `tools/_frontmatter.py` already returns the parsed map; `validate-frontmatter.py` applies set-difference against `L1_REQUIRED`. Adding a per-`type:` `REQUIRED_HEADINGS` map and an AST-style header walk reuses the same pattern dramatica-nav uses.
2. **Stateless beats stored** — task 010's index covers ten queries; nine of them are O(N) over ~250 markdown files (< 600 KB total payload). A live scan + frontmatter parse is < 200 ms on the staged tree, well under the agent's per-query budget.
3. **Section extraction generalises** — dramatica-nav's `extract.py` is heading-anchor-aware. Rebinding it to "any operational markdown file × any `## heading`" gives token-efficient access without an index.
4. **Skill-creator's loop maps cleanly** — `quick_validate` ↔ `fm-validate`, `package_skill` ↔ `fm-extract --whole-file`, `improve_description` ↔ `fm-edit --set summary=…`. The grader/feedback layer maps to `friction-log.md` + run-log.

## Linked Navigation

- [`methodology.md`](./methodology.md) — methods applied (M01, M06, M07, M13).
- [`tracks.md`](./tracks.md) — per-track work breakdown.
- [`state.md`](./state.md) — synthesis-step checklist.
- [`post-synthesis-log.md`](./post-synthesis-log.md) — chronological merge log.
