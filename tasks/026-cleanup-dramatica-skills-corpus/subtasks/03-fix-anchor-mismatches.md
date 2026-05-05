---
type: note
status: draft
slug: task-026-st3-fix-anchor-mismatches
summary: "Subtask ST-3: repair the 8 known term_file anchor mismatches and partition the 106 unmapped headings into ontology-adoptable vs. structural-prose categories. Mint the small set of canonical entries Task 015 explicitly missed (Ability, Change, Non-acceptance, Non-accurate, character-dynamic.approach)."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-3"
subtask_phase: "A"
subtask_recommended_agent: "refactoring-expert"
subtask_depends_on:
  - "ST-2"  # via commit body — ST-3 needs ST-2's coordination note for character-dynamic.approach
subtask_falsification: "Wrong cut iff the 106 unmapped headings turn out to need a fourth bucket (e.g., terms that ARE canonical but were missed in Task 015's bootstrap). Mitigated by surfacing any such terms as named friction items rather than silently bucketing them."
---

# ST-3: Fix Anchor Mismatches & Partition Unmapped Headings

## Goal

Two coupled deliverables:

1. **Fix the 8 known `term_file-anchor-mismatch` warnings from `validate.py`.**

   ```
   concept.archetype       → archetypes.md#contents          (anchor exists, but is a TOC, not a term)
   el.ability              → elements.md#ability             (heading missing — Ability is canonical, not in source)
   el.change               → elements.md#change              (heading missing)
   el.non-acceptance       → elements.md#non-acceptance      (heading missing)
   el.non-accurate         → elements.md#non-accurate        (heading missing)
   type.subconscious       → types.md#subconscious           (heading missing)
   var.self-interest       → variations.md#self-interest     (heading missing)
   var.work                → variations.md#work              (heading missing — Work appears in plot-dynamics.md)
   ```

   Per-case resolution:
   - **5 missing canonical entries** (Ability, Change, Non-acceptance, Non-accurate, Self-Interest): mint a `## <Term>` heading in the appropriate file (`elements.md` or `variations.md`), insert the `nav-ontology` YAML block, and write a one-paragraph structural description (NOT source prose). These ARE the same five terms Task 015 §Plan Step 4 documented as "5 missing canonical entities added to ontology" but the corresponding source headings were never created.
   - **`type.subconscious`**: per Task 015 §Plan Step 4, this is `Innermost Desires (a.k.a. Subconscious)` in source. Adopt `subconscious` as the slug per ontology, and either rename the heading or add `aliases_en: ["Innermost Desires"]` to the YAML block.
   - **`var.work`**: Work appears in `plot-dynamics.md` per source but is canonically a Variation per `element-quads.md`. The ontology has it as `var.work` with `term_file: variations.md#work`. Either move the heading from `plot-dynamics.md` to `variations.md`, OR change the ontology pointer to `plot-dynamics.md#work` (file-coordination question — pick the option that minimises moves).
   - **`concept.archetype`**: rename the ontology pointer from `archetypes.md#contents` to `archetypes.md#archetype` if a `## Archetype` heading exists, or to a fresh `## Archetype (concept)` heading minted at the head of `archetypes.md`.

2. **Partition the 106 `unmapped-heading` warnings into three buckets and emit the partition table.**

   - **Bucket A (≈25): anchor-format-mismatch** — terms that ARE canonical but the slug-from-heading mismatches the slug-in-ontology. Resolved during deliverable #1 above (the eight known cases plus any spillover discovered via the partition).
   - **Bucket B (≈30): kind-concept slot specialisations** — `## Female Mental Sex`, `## Impact Character Concern`, `## Dividend (Overall Story Throughline)`. These are NOT terms in their own right; they are throughline-specific instances of canonical terms. Either (a) delete the heading and add the spelling as `aliases_en` on the canonical (preferred for the historic pseudo-entries like Female Mental Sex — coordinate with ST-4) or (b) mint a `kind: concept` ontology entry pointing back at the canonical. Decision criterion: if the body has unique content, mint the concept; if the body is "See X", delete and alias.
   - **Bucket C (≈50): structural prose** — `## Why Quads matter for Encoding`, `## Phase 1 — Throughline Class assignments`, `## Worked Example 2 — Star Wars`. These are workflow-chapter sub-headings inside extension files. They are NOT ontology candidates; they remain unmapped legitimately. ST-3 documents them in the partition table with reason "structural prose; not a term".

3. **Mint `character-dynamic.approach` in `ontology.json`** per ST-2's coordination note. Frontmatter for the heading was authored by ST-2; ST-3 adds the matching ontology entry. Validate post-mint.

## Falsification

Wrong cut **iff** the 106 unmapped headings turn out to need a fourth bucket (i.e., terms that ARE canonical Dramatica entries but were missed in Task 015's bootstrap, similar to the five-missing-canonical-entities fix). Mitigation: ST-3's deliverable IS the partition table; any heading that doesn't fit Bucket A/B/C is surfaced as a named "Bucket D — disputed" entry in the table, and the commit body asks Task 027 (or a follow-up Task) to resolve. No silent reassignment.

## Inputs

- `tools/dramatica-nav/validate.py` — run with current ontology to enumerate the 8 anchor-mismatches + 106 unmapped-headings.
- `maintenance/schemas/narrative-ontology/ontology.json` — read-only-then-write for the additions.
- `maintenance/schemas/narrative-ontology/ontology.schema.json` — the schema additions must satisfy.
- `skills/dramatica-vocabulary/references/elements.md`, `variations.md`, `types.md`, `archetypes.md`, `plot-dynamics.md` — likely write surfaces.
- ST-2's commit body — coordination note for `character-dynamic.approach`.
- `tasks/015-integrate-dramatica-ncp-skills/notes.md §Plan Step 4 + §Plan Step 5` — historic context on the 8 anchor mismatches and the 5 missing canonical entries.

## Acceptance Criteria

1. **0 anchor mismatches.** `python3 tools/dramatica-nav/validate.py` reports `term_file-anchor-mismatch: 0`.
2. **Partition table emitted.** A new section `## Unmapped-heading partition` appears in [`tasks/026-cleanup-dramatica-skills-corpus/notes.md §5`](../notes.md). Each row: `file | heading | bucket (A/B/C/D) | resolution`. Sum of A+B+C+D = 106 (or whatever validate.py's current count is at ST-3's runtime).
3. **`character-dynamic.approach` minted.** `nav.py by-id character-dynamic.approach` returns a valid entry. The ontology entry's `term_file` resolves to a heading in `character-dynamics.md` (created by ST-2).
4. **`var.work` resolved.** Either the heading moves to `variations.md` OR the ontology pointer moves to `plot-dynamics.md`. Whichever is chosen, `validate.py` reports clean.
5. **5 missing canonical entries added.** `elements.md` carries `## Ability`, `## Change`, `## Non-acceptance`, `## Non-accurate`. `variations.md` carries `## Self-Interest`. Each has `<!-- nav-ontology -->` block + structural description ≤1 line of source-prose.
6. **No new ontology kinds.** Schema is unchanged. If a Bucket B entry needs a kind that's not in the existing enum, file as a Bucket D + Task 027 issue; do NOT bump the schema here.
7. **Single commit.** Title: `fix(dramatica): resolve 8 anchor mismatches + partition 106 unmapped headings (Task 026 ST-3)`.

## Dependencies

ST-2 (via coordination note in ST-2's commit body).

## Estimated Effort

Medium-Large (~5 hours: partition is 106 rows, each needs a one-line decision + cross-reference).

## Agent Prompt

```text
You are implementing ST-3 of Task 026 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/026-cleanup-dramatica-skills-corpus/task.md
  - tasks/026-cleanup-dramatica-skills-corpus/subtasks/03-fix-anchor-mismatches.md (this file)
  - tasks/026-cleanup-dramatica-skills-corpus/notes.md §2.7 (the 8 mismatches) and §2.8 (the 106)
  - tasks/015-integrate-dramatica-ncp-skills/notes.md §Plan Step 4 (historical context on the 5 missing canonical entries)
  - tasks/015-integrate-dramatica-ncp-skills/notes.md §Plan Step 5 (historical context on the 106 unmapped headings)
  - maintenance/schemas/narrative-ontology/ontology.schema.json
  - maintenance/schemas/narrative-ontology/ontology.json

Two coupled deliverables:
  1. Fix all 8 term_file-anchor-mismatch warnings from validate.py.
  2. Partition the 106 unmapped-heading warnings into Buckets A/B/C/D and
     emit the partition table to tasks/026-cleanup-dramatica-skills-corpus/notes.md §5.

Plus mint character-dynamic.approach (per ST-2's coordination note) in
ontology.json.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Run validate.py; capture the current 8 mismatches + 106 unmapped + any
     drift from ST-2 (one expected new warning: character-dynamic.approach
     missing-from-ontology).
  2. For each of the 8 mismatches, apply the per-case resolution from §Goal
     deliverable #1.
  3. Walk the 106 unmapped headings; for each, decide bucket A/B/C/D and
     write one row in the partition table.
  4. For Bucket B entries decided as "alias on canonical", coordinate with
     ST-4 (alias additions overlap). DO NOT add aliases that ST-4 owns;
     leave a coordination note in the commit body.
  5. Mint character-dynamic.approach with appropriate frontmatter.
  6. Run validate.py end-to-end. term_file-anchor-mismatch must drop to 0.
  7. Commit one focused commit; do NOT push.

Constraints:
  - Do NOT quote more than 1 line of Phillips/Huntley source prose into
    new term descriptions.
  - Do NOT bump the ontology schema. New kinds are forbidden here.
  - Do NOT add aliases unless they are necessary to resolve the 8 mismatches.
    Bulk alias loading is ST-7's job.
  - The Bucket D list (disputed terms needing future ratification) MUST be
    visible in the commit body.

When done:
  - python3 tools/dramatica-nav/validate.py
    (term_file-anchor-mismatch: 0; unmapped-heading count drops by ≈25 anchor-format fixes)
  - python3 tools/dramatica-nav/nav.py by-id character-dramatic.approach
    (returns a valid entry)
  - cat tasks/026-cleanup-dramatica-skills-corpus/notes.md | grep -A1 "Unmapped-heading partition"
    (the partition table is present)
  - Commit "fix(dramatica): resolve 8 anchor mismatches + partition 106 unmapped headings (Task 026 ST-3)"
  - Do NOT push.
```
