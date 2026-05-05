---
type: note
status: draft
slug: task-030-st4-resolve-empty-redirects
summary: "Subtask ST-4: resolve the five 'See X' empty redirect entries (Female Mental Sex, Male Mental Sex, Sex), Direction (OS Throughline), Focus). Per case: delete + alias on canonical, OR reify with substantive prose."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-4"
subtask_phase: "A"
subtask_recommended_agent: "technical-writer"
subtask_depends_on: []
subtask_falsification: "Wrong cut iff a redirect entry is load-bearing for an agent that searches by the historic vocabulary. Mitigated by reifying as deprecated_aliases_en on the canonical instead of pure deletion."
---

# ST-4: Resolve Empty Redirect Entries

## Goal

Five "See X" pseudo-entries currently produce useless navigator hits. Resolve each per the case-by-case decisions below:

1. **`## Female Mental Sex` → "See Intuitive Problem Solving Style"** (`character-dynamics.md:141`).
   - DELETE the heading + body.
   - ADD `Female Mental Sex` to `deprecated_aliases_en` on `character-dynamic.problem-solving-style` (canonical entry).
   - Rationale: per the canonical's deprecated label note ([Task 015 §C4](../../015-integrate-dramatica-ncp-skills/task.md)), the modern term is "Problem-solving Style"; the old gendered label is preserved as a deprecated alias.

2. **`## Male Mental Sex` → "See Logical Problem Solving Style"** (`character-dynamics.md:291`).
   - Same treatment as #1; add `Male Mental Sex` to `deprecated_aliases_en` on `character-dynamic.problem-solving-style`.

3. **`## Sex)` orphan** (`character-dynamics.md:392`).
   - Already covered by ST-2 deliverable #1. ST-4 verifies the heading is gone post-ST-2; if not, escalates as a friction event.

4. **TOC bullet `- [Direction (Overall Story Throughline)](#direction-overall-story-throughline) — See`** (`elements.md:22`).
   - The TOC bullet is malformed — its description is "See" with no target. The body's `## Direction (Overall Story Throughline)` section exists and has substantive content. Repair the bullet description to a one-line summary derived from the body's first paragraph (≤1 line of source prose).

5. **TOC bullet `- [Focus](#focus) — See Symptom`** (`elements.md:31`).
   - Per the canonical structure, Focus IS a redirect to Symptom. The body section `## Focus` (line 1135) exists and uses content for Symptom. Two options:
   - **Option A (preferred).** Add `Focus` to `aliases_en` on `concept.symptom-element` (the canonical Symptom Element entry). Delete the `## Focus` body entirely. Update the TOC bullet to remove the entry.
   - **Option B.** Keep both `## Symptom Element` and `## Focus` as kind:concept entries that mutually reference. Less clean; only choose if Option A breaks something downstream.

## Falsification

Wrong cut **iff** a redirect entry is load-bearing for an agent that searches by the historic vocabulary (e.g., a German-speaking author who learned Dramatica before "Mental Sex" was renamed to "Problem-solving Style"). Mitigation: ST-4 PRESERVES the historic terms as `deprecated_aliases_en` rather than pure deletion. This is the same pattern Task 015 used for "Male/Female problem-solving" → already on the canonical.

## Inputs

- `skills/dramatica-vocabulary/references/character-dynamics.md` (cases #1, #2, #3).
- `skills/dramatica-vocabulary/references/elements.md` (cases #4, #5).
- `maintenance/schemas/narrative-ontology/ontology.json` — write surface for the alias additions.
- ST-2's commit body (verify the `## Sex)` removal landed before ST-4 runs).

## Acceptance Criteria

1. **No "See X" empty bodies.** `grep -nE "^See [A-Z]" skills/dramatica-vocabulary/references/character-dynamics.md` returns 0 lines (currently returns 2 — the two Mental Sex redirects).
2. **Aliases land in ontology.** `python3 tools/dramatica-nav/nav.py by-alias 'Female Mental Sex'` returns the canonical `character-dynamic.problem-solving-style` entry. Likewise for `'Male Mental Sex'` and `'Focus'` (the latter resolving to `concept.symptom-element`).
3. **TOC bullets repaired.** `elements.md` has no bullet whose description is just "See" — every TOC entry has a one-line meaningful description.
4. **Validator clean.** `validate.py` reports no NEW `unmapped-heading` warnings beyond what existed pre-ST-4. The two deletions REDUCE the count; ST-3 partition table absorbs the reduction.
5. **No new ontology kinds.** Schema is unchanged. If a case needs a new kind, file as Bucket D + Task 027 issue.
6. **Single commit.** Title: `fix(dramatica): resolve 5 empty redirect entries (Task 030 ST-4)`.

## Dependencies

ST-2 must land before ST-4 (case #3 verification).

## Estimated Effort

Small (~1.5 hours).

## Agent Prompt

```text
You are implementing ST-4 of Task 030 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/030-cleanup-dramatica-skills-corpus/task.md
  - tasks/030-cleanup-dramatica-skills-corpus/subtasks/04-resolve-empty-redirects.md (this file)
  - tasks/030-cleanup-dramatica-skills-corpus/notes.md §2.5 (the 5 redirect cases)
  - skills/dramatica-vocabulary/references/character-dynamics.md
  - skills/dramatica-vocabulary/references/elements.md
  - tasks/015-integrate-dramatica-ncp-skills/task.md §Contradiction Log §C4 (the canonical-naming history)

Goal:
  Resolve the five "See X" empty redirect entries per the case-by-case
  treatment in §Goal of this subtask file. Three deletes + two TOC bullet
  repairs. Two alias additions to ontology.json (one to concept.symptom-element,
  two to character-dynamic.problem-solving-style).

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All six must be true.

Implementation approach:
  1. Verify ST-2 landed (## Sex) heading is gone). If not, halt with
     a friction note.
  2. Apply cases #1 and #2 — delete two ## Female / Male Mental Sex
     headings + bodies; add deprecated_aliases_en entries on the canonical.
  3. Apply case #4 — repair the malformed TOC bullet description.
  4. Apply case #5 — pick Option A; delete ## Focus body, alias on
     concept.symptom-element, remove the TOC bullet.
  5. Run validate.py; expect unmapped-heading count to DROP by 2 or 3
     (ST-3 partition absorbs the rest).
  6. Run nav.py by-alias smoke tests for all three aliases.
  7. Commit one focused commit; do NOT push.

Constraints:
  - DO NOT quote more than 1 line of Phillips/Huntley source prose into
    repaired TOC bullet descriptions.
  - DO NOT add aliases beyond the three named (Female Mental Sex, Male
    Mental Sex, Focus). Bulk alias loading is ST-7's job.
  - DO NOT touch the canonical ## Mental Sex heading (the modern
    Problem-solving Style entry); only the historic redirects.

When done:
  - python3 tools/dramatica-nav/validate.py
  - python3 tools/dramatica-nav/nav.py by-alias "Female Mental Sex"
    (must return character-dynamic.problem-solving-style)
  - python3 tools/dramatica-nav/nav.py by-alias "Focus"
    (must return concept.symptom-element)
  - grep -nE "^See [A-Z]" skills/dramatica-vocabulary/references/character-dynamics.md
    (must return zero lines)
  - Commit "fix(dramatica): resolve 5 empty redirect entries (Task 030 ST-4)"
  - Do NOT push.
```
