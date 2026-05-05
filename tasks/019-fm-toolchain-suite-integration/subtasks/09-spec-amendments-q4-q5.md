---
type: note
status: draft
slug: task-019-st9-spec-amendments
summary: "Subtask ST-9: amend SPEC.md to resolve Q4 (Levenshtein → Optimal String Alignment distance) and Q5 (skill required-keys disagreement between §3.2 and §6.1). Pure documentation work; independent of all other Task 019 subtasks."
created: 2026-05-05
updated: 2026-05-05
---

# ST-9: SPEC Amendments — Q4 (OSA) + Q5 (Skill Keys)

## Goal

Amend the SPEC to close two ambiguities Task 016 surfaced and pinned in §10:

- **Q4** §3.4 says "Levenshtein-distance 1" but the §6.1 example (`tpye` → `type`) is *Optimal String Alignment* (Damerau-restricted) distance 1, not standard Levenshtein 1. The implementation uses OSA. Amend §3.4 to read OSA-1.
- **Q5** §3.2 says `type=skill` requires `skill_kind, skill_target_agents`. §6.1 example treats `name` as required. The implementation requires `name` and `description`. Amend §3.2 to match the implementation: `name` and `description` REQUIRED; `skill_kind, skill_target_agents` RECOMMENDED.

## Falsification

Pure documentation alignment. Falsifiable only if a future review concludes the *prose* was correct and the *implementation* should change instead. Mitigation: this subtask explicitly cites the live SKILL.md format (Anthropic's), which dictates `name`/`description`; the prose loses on contact with reality.

## Inputs

- [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md) §3.2, §3.4, §6.1, §10.
- [`/maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — already encodes the implementation's view; SPEC must match.
- [`/skills/`](../../../skills/) — every live SKILL.md uses Anthropic's `name`+`description` format.

## Acceptance Criteria

1. **§3.4 amended.** "Levenshtein-distance 1" → "Optimal String Alignment distance 1 (Damerau-restricted edit distance: insertion, deletion, substitution, OR adjacent-character transposition each cost 1)". Add a one-sentence rationale citing the `tpye` → `type` example.
2. **§3.2 amended.** `skill` row reads:
   ```
   type: skill   →  name, description (REQUIRED — Anthropic SKILL.md format)
                    skill_kind, skill_target_agents (RECOMMENDED, not required)
   ```
3. **§6.1 row left intact.** The `| skills/abc/SKILL.md | skill | name |` example now agrees with §3.2.
4. **§10 closed.** Q4 and Q5 marked "Resolved by Task 019 ST-9 (PR #N)".
5. **Frontmatter `updated:`** bumped on the SPEC.
6. **No tooling change.** This subtask is purely documentation. The implementation already matches the amended SPEC; no Python file gets touched.
7. **Smoke.** `python3 tools/fm/validate.py research/flexible-frontmatter-toolchain/output/SPEC.md` exits 0.

## Dependencies

None. Phase A.

## Estimated Effort

Small (≤ 50 lines of edits in SPEC.md).

## Agent Prompt

```text
You are amending research/flexible-frontmatter-toolchain/output/SPEC.md
in the netzkontrast/agency repo on branch claude/execute-task-16-ZrBJe.
Pure documentation; no code changes.

Repo root: /home/user/agency

Context files (read first):
  - research/flexible-frontmatter-toolchain/output/SPEC.md  (§3.2, §3.4, §6.1, §10)
  - maintenance/schemas/header-ontology.json
  - tools/fm/_core.py      (the levenshtein() function comment confirms OSA)
  - tasks/016-flexible-frontmatter-toolchain/notes.md  (the implementation
                                                       deviations are listed there)
  - skills/skill-creator/SKILL.md   (live Anthropic format reference)

Acceptance criteria:
  1. §3.4 anchor F.3.4 prose updated: "Levenshtein-distance 1" →
     "Optimal String Alignment distance 1 (Damerau-restricted edit
     distance — insertion, deletion, substitution, OR adjacent-character
     transposition each cost 1)". Append a one-sentence rationale citing
     the `tpye` → `type` example.
  2. §3.2 anchor F.3.2 prose updated for `type: skill`:
       skill → name, description (REQUIRED, Anthropic SKILL.md format)
               skill_kind, skill_target_agents (RECOMMENDED)
  3. §10 entries Q4 and Q5 marked "Resolved by Task 019 ST-9".
  4. Frontmatter `updated:` bumped to today's UTC date.
  5. python3 tools/fm/validate.py research/flexible-frontmatter-toolchain/output/SPEC.md
     exits 0.
  6. python3 tools/validate-frontmatter.py exits 0.
  7. No code files modified.

Constraints:
  - Markdown only.
  - Preserve all existing anchor IDs.
  - Do NOT modify the JSON ontology — it already matches your amended prose.

When done:
  - python3 tools/fm/validate.py research/flexible-frontmatter-toolchain/output/SPEC.md
  - python3 tools/validate-frontmatter.py
  Commit "docs(spec): close Q4 (OSA) and Q5 (skill keys) (Task 019 ST-9)".
  Do NOT push.
```
