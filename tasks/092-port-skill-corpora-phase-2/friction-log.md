---
type: note
status: active
slug: task-092-friction-log
summary: "Task 092 Epic friction log. Final declaration: FL1 (ST-2 triage-note typo + Write tool noise). ST-1, ST-3, ST-4 closed FL0."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — Friction Log

Highest Frustration Level: FL1

## ST-1 — Phase 2 triage matrix (FL0)

- Inventory + parallel subagent triage + matrix authoring completed without governance-tool friction.
- `tools/check-governance.sh` exited 0 on the first attempt after authoring `references/triage-matrix.md`, `references/triage-notes/*.md`, and `references/readme.md`.
- Three parallel `Explore` subagents (SC commands, SC agents+modes+skills, Superpowers full corpus) returned consistent JSON-style outputs that synthesised cleanly into the 81-row matrix. Subagent context isolation kept the main-agent context budget healthy.
- AC T092.1.3 (zero `https://github.com` citations in matrix or notes) caught one self-reference during initial drafting — fixed in two `Edit` calls by rewording the audit-trail line; no rework of substantive content.
- AC T092.1.4 (≥ 75 rows) met with 81 rows by including all four `confidence-check` snapshot copies as distinct rows.

No FL1+ items from ST-1. Nightly maintenance does not need a follow-up Task from this subtask.

## ST-2 — SuperClaude Phase 2 batch (FL1)

Highest Frustration Level: FL1

- **Scale:** 25 new `skills/sc-*/` folders created in one session (4 port commands + 13 adapt commands + 6 port agents + 1 adapt agent + 1 adapt skill), plus 2 MODE bundles (`MODE_Introspection` → `sc-reflect/references/`, `MODE_Task_Management` → `sc-task/references/`). Total new files: ~80 (25 SKILL.md + 25 readme.md + 25 verbatim mirrors + 2 mode bundles + ~10 D.6 reference extracts under `sc-spec-panel/references/experts/`, `sc-socratic-mentor/references/`, `sc-business-panel/references/`).
- **Parallelism (FL0):** Five parallel subagents executed disjoint slug batches (pure-port cluster, light-MCP-adapt cluster, Serena trio + MODE_Introspection bundle, heavy-adapt cluster A with `sc-task`/`sc-workflow`/`sc-brainstorm`/`sc-business-panel`, heavy-adapt cluster B with `sc-spec-panel`/`sc-socratic-mentor`/`sc-confidence-check`). No file-write collisions; main-agent context budget stayed healthy. Phase 1 ST-1's Python-script pattern was matched at a higher level (subagent → many files) rather than literal script-driven generation.
- **FL1.1 — Triage-note `skill_source` typo:** the triage notes (`references/triage-notes/sc-*.md` rows authored in ST-1) cite `skill_source: "superclaude_framework@v4.3.0"`, but the validator regex (tools/fm/validate.py `SKILL_SOURCE_RE`) and Phase 1 precedent require the short form `superclaude@v4.3.0`. Caught pre-write by reading `tools/fm/validate.py`; all 25 SKILL.md files used the correct form. The triage notes themselves SHOULD be re-aligned in a follow-up `T1` Edit pass; not blocking. Filed mental note for a maintenance fix.
- **FL1.2 — `Write` tool spurious "File has not been read yet" errors:** two of the five subagents reported intermittent `Write` errors that were false negatives (files were created on disk; verified by `wc -c`). Treated as harness noise; no rework. Recommend a Task to investigate the Write-tool state-tracking interaction with parallel subagents.
- **Body-cap discipline (D.6):** Three SKILL.md bodies landed within ~120 bytes of the 5 KB cap (`sc-business-panel`: 5001 B; `sc-spec-panel`: 5023 B; `sc-confidence-check`: 5009 B; `sc-task`: 4838 B; `sc-workflow`: 4629 B; `sc-brainstorm`: 4956 B). D.6 reference extraction worked cleanly for `sc-spec-panel` (10 expert profiles under `references/experts/`), `sc-socratic-mentor` (`references/teaching-corpus.md`), and `sc-business-panel` (`references/expert-profiles.md` + `references/sub-modes.md`).
- **D.7 enforcement (`sc-confidence-check`):** the canonical upstream skill body was audited for SessionStart-injection clauses across all four upstream copies (canonical `src/`, `.claude/skills/`, `plugins/`, root `skills/`). None found. Documented the negative result in `skills/sc-confidence-check/SKILL.md` `## Adaptations from upstream` and `readme.md` `## Assumptions Log` so the audit trail is traceable.
- **Governance gate:** `tools/check-governance.sh` exited 0 on first attempt after the readme update.

Outcome: ST-2 closes at FL1. The two FL1 items are tooling / spec-text fixes filed as follow-ups; neither is blocking for ST-3.

## ST-3 — Superpowers full corpus (FL0)

Highest Frustration Level: FL0

- **Scope:** 15 new `skills/superpowers-*/` folders across two PRs (PR #119 batch A: 6 pure-port discipline gates; PR #120 batch B: 8 adapt skills + 1 agent template). Total new files: 45 (15 SKILL.md + 15 readme.md + 15 verbatim mirrors).
- **D.7 enforcement (`superpowers-using-superpowers`):** the upstream meta-skill ships with a SessionStart-injection hook (`hooks/session-start.sh`). ADR-0011 D.7 forbids that pattern. Adaptation stripped the SessionStart framing and re-bound to the Agency Skill tool semantics. Three additional D.7-prohibited hook files (`hooks.json`, `session-start.sh`, `run-hook.cmd`) were classified `skip` per [`triage-notes/superpowers-hooks-skip.md`](./references/triage-notes/superpowers-hooks-skip.md).
- **Body-cap discipline (D.6):** All 15 Agency SKILL.md bodies landed ≤ 3.7 KB — comfortably under D.6 5 KB cap. Two upstream bodies exceeded 5 KB (`writing-skills` at 22 KB, `systematic-debugging` at 9.9 KB, `test-driven-development` at 9.9 KB, `subagent-driven-development` at 9.8 KB, `receiving-code-review` at 6.3 KB, `dispatching-parallel-agents` at 6.1 KB, `using-git-worktrees` at 5.6 KB). These live in `references/upstream-*.md` only; the Agency SKILL.md body is a concise rewrite per ADR-0011 D.3+D.6.
- **Cross-batch fixup (batch B):** PR #119 (batch A) intentionally left a forward-reference in body prose pointing at `superpowers-requesting-code-review` (not yet ported) instead of breaking the audit graph with a dangling `skill_references_skills` edge. Batch B (PR #120) restored the edge and removed the body note in a single commit.
- **Review feedback addressed in one round each:** PR #119 received 1 BLOCKING + 3 ADVISORY items; fixed in commit `37e36aa` (PR body D.7 callouts + dangling edge + display-text fix). PR #120 received 3 ADVISORY items; A2 fixed in commit `1fb6f28` (added 5 missing `skill_references_skills` edges in `superpowers-using-superpowers`).

Outcome: ST-3 closes at FL0. The two review-fix rounds were procedural (PR body completeness, graph reciprocity) and resolved cleanly via the standard `Edit` + push flow.

## ST-4 — Snapshot cleanup (FL0)

Highest Frustration Level: FL0

- **Scope:** deleted `tasks/091-port-external-skill-corpora/references/upstream-snapshot/` (516 files; ~4.7 MB) in a single `rm -rf`. Stripped the two governance carve-outs (`tools/.frontmatter-waivers` row + `tools/.script-allowlist` row + preceding comment block).
- **AC verification:**
  - T092.4.1 — `find tasks/091-…/references/upstream-snapshot/ -type f` returns 0 (directory does not exist).
  - T092.4.2 — `grep upstream-snapshot tools/.frontmatter-waivers tools/.script-allowlist` returns exit 1 (zero matches).
  - T092.4.3 — only waiver row was the 2026-08-12 upstream-snapshot row; now removed. No expired waivers remain.
  - T092.4.4 — `tools/check-governance.sh` exits 0 on the post-cleanup tree.
- **Audit-trail preserved:** the triage matrix + 21 triage notes + 5 review files remain in `tasks/092-port-skill-corpora-phase-2/` as the permanent record of "what was ported, what was skipped, and why". Historical references to the deleted snapshot path are intentional — they describe what the Epic did.
- No deadline pressure (cleanup landed 3 months before the 2026-08-12 expiry).

## Epic-level summary

**Highest Frustration Level (Epic): FL1** — driven entirely by the ST-2 batch (triage-note slug-form typo + Write-tool harness noise). All other subtasks closed FL0.

**Cumulative output (41 skill folders + 21 triage notes + 5 review files):**

| Subtask | PR | Skills shipped |
|---|---|---|
| ST-1 (triage) | #116 | 81-row matrix + 21 notes |
| ST-2 batch A (SC pure ports) | #117 | 10 `sc-*` skills |
| ST-2 batch B (SC adapts) | #118 | 15 `sc-*` skills + 2 mode bundles |
| ST-3 batch A (SP discipline gates) | #119 | 6 `superpowers-*` skills |
| ST-3 batch B (SP adapts + agent) | #120 | 9 `superpowers-*` skills |
| ST-4 (cleanup) | this PR | snapshot retired + waivers stripped |

**Recommended follow-up Tasks** (carried forward from PR #120 review A1):

- T3 — ratify the expanded `skill_kind` enumeration in SKILLS.md §3 to include `discipline | workflow | persona | analysis | meta | agent-template | orchestrator`, and add an enum check to `tools/fm/validate.py`. The Phase 2 corpus introduced `discipline`, `workflow`, `agent-template`, `meta`, `persona`, and `analysis` ad hoc; the spec needs to catch up.
- T1 — fix the `superclaude_framework@v4.3.0` → `superclaude@v4.3.0` typos in the triage notes (ST-1 FL1.1 carry-over).

At PR merge, Task 092 flips `task_status: done`. Epic closed.
