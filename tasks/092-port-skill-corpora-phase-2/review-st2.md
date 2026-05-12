---
type: note
status: active
slug: task-092-st2-review
summary: "Peer review of PR #118 (Task 092 ST-2): SuperClaude Phase 2 batch — 25 sc-* skills. Verdict: APPROVED. Governance clean; ADR-0011 D.1–D.8 enforced correctly. Three non-blocking follow-up items (FL1.1 Task, FL1.2 Task, sc-spec-panel body-cap watch)."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #118 · Task 092 ST-2: SuperClaude Phase 2 batch (25 skills)

**Reviewer:** claude-sonnet-4-6  
**PR:** [#118](https://github.com/netzkontrast/agency/pull/118)  
**Branch:** `claude/task-92-st2-superclaude-FBXJI` → `main`  
**Commit:** `69dafbe`  
**Date:** 2026-05-12

---

## Verdict: APPROVED

No blocking issues. All 25 `skills/sc-*/` folders are structurally correct, governance
exits 0, and ADR-0011 enforcement is thorough across all eight clauses (D.1–D.8).
Three non-blocking observations are filed below as recommended follow-up Tasks.

---

## What works

### Governance and validator

`tools/check-governance.sh` exits 0.  
`python3 tools/fm/validate.py --check-body skills/` — 60 files, 0 diagnostic(s).

Both numbers include the 25 new folders without regression to the 35 Phase 1 + native
skills. This is the cleanest possible gate result.

### ADR-0011 clause-by-clause verification

**D.1 — vendor prefix `sc-`**  
All 25 slugs carry the `sc-` prefix. ✓

**D.2 — `skill_source` pin**  
Every `SKILL.md` carries `skill_source: "superclaude@v4.3.0"`. Checked via
`python3 tools/fm/validate.py skills/` (codes F.B.8 / F.B.9 per ADR-0012). ✓

**D.3 — SHA-pinned verbatim mirrors**  
Random-checked `skills/sc-analyze/references/upstream-sc-analyze.md` and
`skills/sc-socratic-mentor/references/upstream-sc-socratic-mentor.md`. Both open with
the canonical attribution header:

```
<!-- Mirror of SuperClaude-Org/SuperClaude_Framework/…/analyze.md @ 22ad3f483a6fe6c…
     Verbatim per ADR-0011 D.3. DO NOT EDIT — re-sync via a new Task. -->
```

Attribution format is consistent and correct. ✓

**D.5 — MODE bundles as `references/` content**  
`sc-reflect/references/mode-introspection.md` and
`sc-task/references/mode-task-management.md` both carry the D.3/D.5 dual attribution
header. The three remaining MODE files (rows 40–42 in the ST-1 triage matrix) are
correctly skip-classified with rationale ("behavioural duplicate", "MCP-heavy duplicate",
"already represented"). ✓

**D.6 — ≤ 5 120 B body cap**  
All 25 SKILL.md bodies are within cap. Largest is `sc-spec-panel` at 5 023 B (97 B
headroom). The three bodies that needed extraction handled it cleanly:

- `sc-spec-panel` → 10 expert profiles under `references/experts/*.md`
- `sc-socratic-mentor` → `references/teaching-corpus.md`
- `sc-business-panel` → `references/expert-profiles.md` + `references/sub-modes.md`

The `SKILL.md` body in each case retains only the structural discipline; the extracted
reference file holds the corpus. This is the correct D.6 pattern. ✓

**D.7 — SessionStart-injection strip**  
The `sc-confidence-check` audit is exemplary: all four upstream copies (canonical `src/`,
`.claude/skills/`, `plugins/`, root `skills/`) were checked for `SessionStart` /
`session-start` / `session_start` / `hook` patterns. Negative result documented in both
`SKILL.md §Adaptations from upstream` and `readme.md §Assumptions Log`. This traceability
pattern SHOULD become the standard for any future D.7 audit. ✓

**D.8 — Non-Agency MCP demoted to OPTIONAL**  
Spot-checked four "adapt" rows across the MCP spectrum:

| Skill | MCPs stripped | `## How to use` uses | OPTIONAL in `## Compatibility` |
|---|---|---|---|
| `sc-build` | playwright | Bash | ✓ |
| `sc-load` | serena | Read, tools/fm/edit.py | ✓ |
| `sc-task` | sequential, context7, magic, playwright, morphllm, serena | Read/Edit/Bash/TodoWrite | ✓ |
| `sc-confidence-check` | context7, tavily | WebFetch, WebSearch | ✓ |

In each case, `## How to use` cites only Agency-native or built-in Claude Code primitives;
non-Agency MCPs appear nowhere in the action body. ✓

### Structural completeness

All 25 folders carry the three required files (`SKILL.md`, `readme.md`,
`references/upstream-sc-<slug>.md`). D.6-extracted folders carry additional
`references/` subdirs as needed. No folder violates the CLAUDE.md §7 readme rule. ✓

`skills/readme.md` Phase 2 section lists all 25 slugs with MCP footnotes, cites
ADR-0011 + Task 092 as authority, and updates the "Current State" tally to 39 sc-*
skills (14 Phase 1 + 25 Phase 2). ✓

### Parallelism execution

5 parallel subagents with disjoint slug batches, no write collisions, main-agent context
budget preserved. The Phase 1 subagent pattern scales correctly to the larger batch.
FL1.2 false-negative Write errors did not corrupt any file (verified by `wc -c`).

### ADR-0012 prerequisite

`decisions/0012-skill-source-validator-diagnostic-codes.md` is `adr_status: Accepted`.
The ST-2 spec dependency ("Depends on ADR-0011 amendment (FL1.1 carry-over, 0012-…)
Accepted") is met. ✓

---

## Observation 1 (P2): FL1.1 triage-note `skill_source` typo — no Task filed

**Severity:** Non-blocking / recommended follow-up.

The 5 triage notes under
`tasks/092-port-skill-corpora-phase-2/references/triage-notes/` contain:

```yaml
- `skill_source: "superclaude_framework@v4.3.0"`
```

The validator regex (ADR-0012 / `tools/fm/validate.py SKILL_SOURCE_RE`) requires the
short form `superclaude@v4.3.0`. The friction log correctly notes this was caught
pre-write and says "filed mental note for a maintenance fix" — but no Task artefact
was created.

Per MAINTENANCE.md §1 and FRUSTRATED.md, FL1+ items SHOULD convert to Tasks via the
maintenance pipeline. A T1 in-place `Edit` pass on the triage notes is appropriate.
The triage-note files are `type: note` in operational research — they are not
`research_phase: complete` workspaces — so T4 immutability does not apply.

**Recommended action:** File a T1 maintenance Task before or shortly after ST-3 begins.
The fix is trivial (global replace in ~21 values) but the untracked state creates
validator drift risk for future readers of the matrix.

---

## Observation 2 (P3): FL1.2 Write-tool parallel-subagent issue — no Task filed

**Severity:** Advisory.

The friction log says: "Recommend a Task to investigate Write-tool state-tracking
under parallel subagents." That Task was not filed. Two subagents saw false-negative
`Write` errors (files confirmed created on disk via `wc -c`); the mechanism is
unexplained.

If this pattern recurs in ST-3 (Superpowers corpus, ~19 skills) or ST-4, silent
harness noise could mask a genuine write failure. A P3 Task scoped to reproducing the
issue under controlled parallelism is the appropriate response.

**Recommended action:** File a P3 tooling Task citing the FL1.2 evidence from this
friction log before ST-3.

---

## Observation 3 (Advisory): `sc-spec-panel` at 5 023 B — 97 B headroom

`sc-spec-panel` is the largest SKILL.md at 5 023 B of the 5 120 B D.6 cap.
Any future T1 repair that adds a `skill_references_skills:` entry or bumps an `updated:`
date in the YAML frontmatter could push the body over the cap and trigger F.B.8/F.B.9
errors.

The 10-expert extraction is already well-executed. No action required now. This is a
watch item for whoever authors T1 repairs on `sc-spec-panel` in future sessions.

---

## Checklist against T092.2.1–T092.2.4 and BR.92.*

| Criterion | Status | Notes |
|---|---|---|
| **T092.2.1** — every keep-list row has `skills/sc-*/SKILL.md` + `skill_source` pin | ✅ | 25/25 folders; `validate.py` 0 diagnostics |
| **T092.2.2** — D.8 adaptation enforced for "adapt" rows | ✅ | MCPs in `## Compatibility` OPTIONAL; Agency primitives in `## How to use` |
| **T092.2.3** — D.6 body cap ≤ 5 120 B | ✅ | Max 5 023 B (`sc-spec-panel`); 0 `--check-body` errors |
| **T092.2.4** — `skills/readme.md` lists all new entries | ✅ | Phase 2 batch section present and comprehensive |
| **BR.92.1** — triage matrix covers every snapshot artefact | ✅ | 81 rows authored in ST-1 (not modified here) |
| **BR.92.2** — keep-list items validate clean | ✅ | 60 files, 0 diagnostics |
| **BR.92.3** — snapshot retired | 🔲 | ST-4 scope — not expected in this PR |
| **BR.92.4** — no external GitHub fetch in triage | ✅ | ST-1 confirmed; this PR adds no new triage fetches |

---

## Summary

| # | Severity | Action | Owner |
|---|---|---|---|
| O1 | **P2 / recommended** | File T1 Task for triage-note `skill_source` typo | pre-ST-3 |
| O2 | **P3 / advisory** | File P3 Task for Write-tool parallel-subagent investigation | pre-ST-3 |
| O3 | **Watch item** | `sc-spec-panel` body cap headroom (97 B) | T1 repair authors |

No blocking issues. This PR is ready to merge.
