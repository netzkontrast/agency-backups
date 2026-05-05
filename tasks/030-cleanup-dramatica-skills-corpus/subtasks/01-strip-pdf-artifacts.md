---
type: note
status: draft
slug: task-030-st1-strip-pdf-artifacts
summary: "Subtask ST-1: strip PDF page-break footers, page-number-only lines, double-apostrophe escapes, and stray > prefix artefacts from skills/dramatica-{theory,vocabulary}/references/*.md. Pure deletion, no semantic edits."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-1"
subtask_phase: "A"
subtask_recommended_agent: "refactoring-expert"
subtask_depends_on: []
subtask_falsification: "Wrong cut iff a deleted artefact turns out to be load-bearing for an agent (e.g., a copyright footer used as a section terminator). Mitigated by --dry-run first and human-reviewed diff."
---

# ST-1: Strip PDF Artefacts

## Goal

Remove four classes of PDF-extract residue from the dramatica corpus, in pure-deletion mode (no semantic edits, no rewriting prose):

1. **Copyright footers.** Every line matching `^Copyright \(c\) 2001 Screenplay Systems Inc\..*` plus the immediately-preceding blank line and the immediately-following page-number-only line. Baseline: 38 occurrences in `skills/dramatica-vocabulary/references/*.md`. Theory chunks already had these stripped upstream — confirm 0 hits there.

2. **Page-number-only lines.** Every line matching `^[0-9]+\.\s*$` AND surrounded by blank lines on both sides AND not followed by a `## ` or `### ` heading (i.e., not a numbered list item). Baseline: 324 occurrences in `skills/dramatica-theory/references/*.md` (most-affected: `02-characters.md` 51, `06-storyforming.md` 45, `09-reference.md` 78). Plus the 38 occurrences interleaved with §1's footers in vocabulary.

3. **Double-apostrophe escapes.** Replace `''` (literal two single-quotes) with `'`. Baseline: 8 occurrences across `domains.md` (1), `character-dynamics.md` (1), `plot-dynamics.md` (1), `types.md` (2), `elements.md` (2), `variations.md` (1).

4. **Leading-`>` bullet artefacts.** In Contents-list bullet items only (lines matching `^- \[.*\] — `), strip a leading `>` from the description portion if present. Example: `- [Trust](#trust) — >Trust` becomes `- [Trust](#trust) — Trust`. Do NOT touch `>` characters inside body prose (they are markdown blockquotes there). Baseline: numerous occurrences in `elements.md`, `variations.md`, `types.md` Contents lists.

## Falsification

Wrong cut **iff** a deleted artefact turns out to be load-bearing for an agent. Mitigation: ST-1 first runs in `--dry-run` mode that emits a unified diff to stdout. The driver reviews the diff. ONLY after the driver confirms the diff is clean does ST-1 apply changes. Lock the regex set to the four classes above; do NOT add new regexes during this subtask.

## Inputs

- All `*.md` files under `skills/dramatica-vocabulary/references/`.
- All `*.md` files under `skills/dramatica-theory/references/`.
- DO NOT touch the SKILL.md files in either skill (they are the entry points; their YAML and prose are intentional).
- DO NOT touch `_synonym-lookup.md` or `dynamic-pairs-index.md` (different structure; ST-7's domain).

## Acceptance Criteria

1. **Mechanical.** After ST-1's commit, the following greps return 0 lines:
   - `grep -rE "^Copyright \(c\) 2001" skills/dramatica-{theory,vocabulary}/references/`
   - `grep -rE "^[0-9]+\.\s*$" skills/dramatica-{theory,vocabulary}/references/` (excluding numbered list items per §1.2 above — these have non-blank context lines)
   - `grep -rl "''" skills/dramatica-{theory,vocabulary}/references/` returns no files
2. **Heading preservation.** All `## ` and `### ` headings present BEFORE ST-1 are still present AFTER. Verify via diff of `grep -c '^## '` per file (counts unchanged).
3. **Validator clean.** `python3 tools/dramatica-nav/validate.py` exits 0 with the same warning count as before (modulo the `unmapped-heading` count for any heading whose anchor changed because of `''` → `'` slug normalization — flag these for ST-3).
4. **Diff is pure deletion.** `git diff --stat` shows insertion count ≤ 5 (for §1.4 Contents-list rewrites). Anything more means non-deletion edits crept in; revert.
5. **Single commit.** Title: `chore(dramatica): strip PDF artefacts from references (Task 030 ST-1)`. Body lists the four artefact classes and per-class deletion counts.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~80 LOC of regex-driven Python helper script + manual review of dry-run diff).

## Agent Prompt

```text
You are implementing ST-1 of Task 030 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first; do not load other ontology files):
  - tasks/030-cleanup-dramatica-skills-corpus/task.md (the parent task)
  - tasks/030-cleanup-dramatica-skills-corpus/subtasks/01-strip-pdf-artifacts.md (this file)
  - skills/dramatica-vocabulary/references/character-dynamics.md (worst-case sample)
  - skills/dramatica-theory/references/02-characters.md (worst-case sample)

Goal:
  Strip four classes of PDF-extract residue from the dramatica corpus, in
  pure-deletion mode (no semantic edits). Class definitions are in this
  subtask's "Goal" section above; reproduce them exactly.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). Mechanical pass requires all four be true.

Implementation approach:
  1. Author a one-shot Python helper at tools/dramatica-nav/_strip_artifacts.py
     (note the leading underscore — this is internal, not a stable API).
  2. Helper supports --dry-run (prints unified diff) and --apply (writes files).
  3. Run --dry-run; print the diff stats per artefact class.
  4. Apply.
  5. Verify all four acceptance criteria mechanically.
  6. Commit one focused commit; do NOT push.

Constraints:
  - Python 3.11 stdlib only.
  - No new dependencies, no third-party regex libs.
  - The four regex classes are LOCKED. Do not invent new artefact classes.
    If you find suspicious content that doesn't match the four classes,
    surface it as a friction event in the commit body but do NOT delete it.
  - Do NOT modify SKILL.md, _synonym-lookup.md, or dynamic-pairs-index.md.
  - Do NOT edit any heading text (## or ###).
  - The helper script SHOULD be deletable after ST-1 closes; it is one-shot.

When done:
  - python3 tools/dramatica-nav/validate.py        (must exit 0)
  - git diff --stat                                (deletions ≫ insertions)
  - git diff -- skills/                            (visually confirm only artefacts removed)
  - Commit "chore(dramatica): strip PDF artefacts from references (Task 030 ST-1)"
  - Do NOT push.
```
