---
type: note
status: draft
slug: task-026-st2-fix-corrupted-headings
summary: "Subtask ST-2: repair structurally corrupted headings — `## Sex)` lone-paren artefact, the `## Approach` heading carrying Growth's frontmatter, and any other heading-level corruption discovered during ST-1's diff review."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-2"
subtask_phase: "A"
subtask_recommended_agent: "technical-writer"
subtask_depends_on: []
subtask_falsification: "Wrong cut iff broken headings encode dictionary information that a re-extraction from canonical PDF could recover. Mitigated by forbidding source-prose quoting >1 line per repo's existing rule."
---

# ST-2: Fix Corrupted Headings & Mis-Attributed Frontmatter

## Goal

Three concrete fixes:

1. **`## Sex)` orphan.** In `skills/dramatica-vocabulary/references/character-dynamics.md` line 392, repair the broken heading. Inspection shows the body content following it discusses problem-solving styles. Two options:
   - **Option A (preferred).** If the body is a mis-cut from the canonical `## Mental Sex` entry (which exists in the same file at line 302 with proper frontmatter), DELETE this orphan heading and merge any non-redundant content into the canonical `## Mental Sex` body.
   - **Option B.** If the body is genuinely standalone, repair the heading text to match the body's actual content and DOCUMENT the fix in the commit body.

2. **`## Approach` carrying `character-dynamic.growth` frontmatter.** In `skills/dramatica-vocabulary/references/character-dynamics.md` lines 21–30, the `## Approach` heading has YAML frontmatter for `character-dynamic.growth` (canonical_label: Growth). This is wrong: the heading and the YAML disagree on which term is being defined. **Both entries already exist in `ontology.json`** (`character-dynamic.approach` AND `character-dynamic.growth`), and BOTH currently have `term_file` pointing at the same `character-dynamics.md#approach` anchor — that's why `validate.py` doesn't surface the wrong-YAML-on-Approach-heading as an error. The body following the heading mixes Approach + Growth content. Two-step fix:
   - Split the heading. Create a separate `## Growth` heading carrying the existing `character-dynamic.growth` frontmatter and the Growth-specific body lines.
   - Rewrite `## Approach`'s YAML block to reference the already-existing `character-dynamic.approach` ontology entry (which currently still points at the same anchor).
   - Coordinate with ST-3 via the commit body (one-line note: "ST-3 must update `character-dynamic.growth.term_file` to `character-dynamics.md#growth` so the ontology table tracks the new heading anchor").

3. **Truncated content blocks.** Search for body content that ends mid-word (e.g., line 160: `preferential method of approaching proble` followed by `### Type` heading). For each truncation:
   - If the missing tail is reconstructable from canonical Phillips/Huntley source AND the reconstruction is ≤1 line of prose, fix it (per repo's [Task 015 §Anti-Patterns](../../015-integrate-dramatica-ncp-skills/task.md) MUST-NOT-quote-more-than-1-line rule).
   - If the missing tail exceeds 1 line, mark the body explicitly with an HTML comment: `<!-- truncated extract; consult original source -->` and leave the truncation visible.
   - Catalog every truncation in the commit body so a future re-extraction pass knows where to focus.

## Falsification

Wrong cut **iff** the broken `## Sex)` body actually encodes dictionary information that a re-extraction from canonical PDF could recover. Mitigation: ST-2 explicitly forbids quoting >1 line of source prose in repairs (per Task 015's [`task.md §Anti-Patterns`](../../015-integrate-dramatica-ncp-skills/task.md) line 450). When in doubt, ST-2 deletes the corrupted body and emits a friction-log entry pointing at the source PDF coordinate (page-number range from `dramatica-theory/references/`'s extracted chunks).

## Inputs

- `skills/dramatica-vocabulary/references/character-dynamics.md` — the worst-case file, three known issues.
- `skills/dramatica-vocabulary/references/elements.md` — spot-check for similar patterns (one known: `## Hinder` body says `>Help` instead of Hinder content).
- `maintenance/schemas/narrative-ontology/ontology.json` — read-only consultation for canonical labels and IDs.
- `maintenance/schemas/narrative-ontology/term-frontmatter.schema.json` — the schema any new YAML block must satisfy.
- `tasks/026-cleanup-dramatica-skills-corpus/notes.md §2.4 + §2.6` — exact line numbers + context for the known cases.

## Acceptance Criteria

1. **No `## Sex)` heading remains.** `grep -E "^## .*\)$" skills/dramatica-vocabulary/references/*.md` returns 0 hits.
2. **Approach/Growth frontmatter agrees with heading.** The `## Approach` heading carries a YAML block whose `canonical_label: Approach`. A new `## Growth` heading exists with `canonical_label: Growth`. `validate.py` reports both as `term_file-anchor-match`.
3. **Schema valid.** Both NEW frontmatter blocks pass `term-frontmatter.schema.json` validation (run `validate.py`).
4. **No quoted source prose >1 line.** `git diff -- skills/dramatica-vocabulary/references/character-dynamics.md | grep '^+' | grep -v '^+++' | wc -l` should be small (<30 lines for content additions); any larger means prose was added.
5. **Truncation catalog emitted.** Commit body MUST include a markdown table listing every truncation found, with file:line and canonical-source pointer (page range in `dramatica-theory/references/0X-foo.md` if reconstructable).
6. **Coordination note for ST-3.** Commit body MUST include a single-line item: `ST-3 must mint character-dynamic.approach in ontology.json` (or similar) so ST-3's brief is unambiguous.
7. **Single commit.** Title: `fix(dramatica): repair corrupted headings + mis-attributed YAML (Task 026 ST-2)`.

## Dependencies

None at execution time. ST-3 will consume ST-2's coordination note (via the commit body).

## Estimated Effort

Medium (~3 hours of careful prose decisions + frontmatter authoring).

## Agent Prompt

```text
You are implementing ST-2 of Task 026 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/026-cleanup-dramatica-skills-corpus/task.md
  - tasks/026-cleanup-dramatica-skills-corpus/subtasks/02-fix-corrupted-headings.md (this file)
  - tasks/026-cleanup-dramatica-skills-corpus/notes.md (specifically §2.4 and §2.6)
  - tasks/015-integrate-dramatica-ncp-skills/task.md §Anti-Patterns
    (MUST-NOT-quote-source-prose-over-1-line rule)
  - skills/dramatica-vocabulary/references/character-dynamics.md
    (the file with all three known issues)
  - maintenance/schemas/narrative-ontology/term-frontmatter.schema.json
    (any new YAML block must satisfy this)

Three concrete fixes (verbatim from this subtask file's Goal section):
  1. The `## Sex)` orphan at character-dynamics.md:392.
  2. The `## Approach` heading carrying character-dynamic.growth frontmatter
     at character-dynamics.md:21–30.
  3. Any other truncated-mid-word content blocks discovered in the file.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Read character-dynamics.md end-to-end; sketch the structural map of
     headings before vs. after.
  2. Apply fix #1 (delete or rename), fix #2 (split into ## Approach + ##
     Growth with corrected YAML), fix #3 (catalog truncations).
  3. For fix #2, BOTH character-dynamic.approach AND character-dynamic.growth
     already exist in ontology.json — both currently have term_file pointing
     at character-dynamics.md#approach. Your task here: write the correct
     character-dynamic.approach YAML under ## Approach, AND write the
     character-dynamic.growth YAML under a NEW ## Growth heading. ST-3
     updates the ontology table's term_file pointer for character-dynamic.growth
     to ...#growth (your commit body coordinates this).
  4. Run validate.py; expect the term_file-anchor-mismatch count to stay
     stable (the broken pointer for character-dynamic.growth is what ST-3
     fixes) — no new warnings introduced.
  5. Commit one focused commit; do NOT push.

Constraints:
  - DO NOT quote more than 1 line of Phillips/Huntley source prose into
    repaired body content.
  - DO NOT touch any file outside skills/dramatica-vocabulary/references/.
  - DO NOT mint new ontology IDs in ontology.json — that is ST-3's job.
  - The truncation catalog in your commit body is mandatory; an empty
    catalog means truncations were missed.

When done:
  - python3 tools/dramatica-nav/validate.py
    (one new warning expected — character-dynamic.approach not in ontology
    until ST-3 lands; that's the only new warning)
  - grep -E "^## .*\)$" skills/dramatica-vocabulary/references/*.md
    (must return zero lines)
  - Commit "fix(dramatica): repair corrupted headings + mis-attributed YAML
    (Task 026 ST-2)" with the truncation catalog table in the body.
  - Do NOT push.
```
