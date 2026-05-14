---
type: task
status: active
slug: maintenance-spec-friction-log-declaration-hardening
summary: "Filed by the 2026-05-14 coherence run after fixing three T1 ERRORs surfaced by MAINTENANCE.md's routines. Captures four MAINTENANCE.md improvement opportunities: (a) closed-Task friction-log T1/T2 repair allowance parallel to §1.0.1 closed-research clause; (b) fm/edit.py --bump-updated batch semantics; (c) FR.B.4 auto-derivation of canonical declaration line from inline FL tokens; (d) /sc:* command routing inside the maintenance routine."
created: 2026-05-14
updated: 2026-05-14
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - MAINTENANCE.md
  - tools/fm/edit.py
  - tools/check-fl-declaration.py
  - tools/tests/test_fm_edit_bump_batch.py
  - research/fl0-value-justification/output/SPEC.md
---

# Task 096 — MAINTENANCE.md hardening: friction-log declaration + closed-Task repair allowance

## Goal

MAINTENANCE.md §1 and §3 are extended so a coherence-run agent can mechanically
resolve the four classes of friction surfaced during the 2026-05-14 coherence run
(see [`maintenance/run-log.md`](../../maintenance/run-log.md) — Run 2026-05-14 —
coherence-check) without re-deriving the rules from prose. Task is `done` iff
the four §Plan items below land in one PR, `tools/check-governance.sh` exits 0
on the closing commit, and one new Gherkin scenario per item is added to
MAINTENANCE.md §6 under anchors `M.B.9` through `M.B.12`.

## Plan

1. **Closed-Task friction-log T1/T2 repair allowance (§1.0.2 — parallel to §1.0.1).**
   Extend MAINTENANCE.md §1.0 with a new subsection that mirrors the closed-research
   T1/T2 allowance for friction-log declaration-line repairs on `task_status: done`
   Tasks. Today's prose treats the entire `tasks/<NNN>-<slug>/` folder as
   semantically frozen once `done`, which is over-broad — a malformed
   `Highest Frustration Level:` line is recoverable mechanically and SHOULD NOT
   require a successor Task. Acceptance contract: anchor `M.B.9`.

2. **`tools/fm/edit.py --bump-updated` batch semantics.** The current CLI
   accepts exactly one path; a coherence sweep typically touches 3–10 files in
   one wave (this run touched 4). Extend the arg parser to accept N paths and
   bump each atomically (the file lock per-path is already correct; only the
   argparse declaration needs to change). Add a smoke test in
   `tools/tests/test_fm_edit_bump_batch.py` covering the multi-path success
   path + the "one path fails, others succeed" partial-failure semantics.
   Acceptance contract: anchor `M.B.10`.

3. **FR.B.4 declaration-line auto-derivation (advisory, NOT mutator).** When
   `tools/check-fl-declaration.py` emits ERROR:FR.B.4:malformed on a
   friction-log, the message MUST include the *suggested* canonical line the
   agent can paste, derived from the file's frontmatter `summary:` (if it
   contains `FL[0-3]`) and from the highest inline `(FL[0-3], …)` token in the
   body. The linter remains a verifier — the auto-derivation is suggestion-only,
   surfaced in the diagnostic message. Acceptance contract: anchor `M.B.11`.

4. **`/sc:*` routing from the maintenance routine (§4.2 — new subsection).**
   Document the canonical `/sc:*` command flow for a coherence-run agent so the
   user instruction "Execute Maintenance.md, use /sc: skills" has a deterministic
   spec answer. The empirically-confirmed flow (this 2026-05-14 run) is:
   `/sc:analyze` on the changed-files delta and the T1/T2/T3 bucket classification →
   `/sc:reflect` on adherence to CR.1–CR.7 + MAINTENANCE.md §§1–4 →
   `/sc:improve` for advisory quality lifts to artefacts authored in the session
   (NOT to T1 repairs themselves, which are already mechanically minimal) →
   `/sc:Review` (self-review) on the staged diff before commit →
   `/sc:createPR` for the closing draft pull request.
   Acceptance contract: anchor `M.B.12`.

## Todo

- [ ] 1. Draft MAINTENANCE.md §1.0.2 (closed-Task T1/T2 allowance) + M.B.9 Gherkin.
- [ ] 2. Extend `tools/fm/edit.py` argparse for multi-path `--bump-updated`; add `tools/tests/test_fm_edit_bump_batch.py` (5 cases).
- [ ] 3. Extend `tools/check-fl-declaration.py` ERROR:FR.B.4 diagnostic message to embed the derived canonical line; add three new linter test fixtures (frontmatter-only, body-only, both-missing).
- [ ] 4. Draft MAINTENANCE.md §4.2 (`/sc:*` routing) + M.B.12 Gherkin.
- [ ] 5. `tools/check-governance.sh` exits 0 on the closing commit.
- [ ] 6. Friction-log written; PR opened citing this Task slug + FL declaration.
- [ ] 7. `tasks/readme.md` bullet added for Task 096 (TASK.md §4.8 / §7.11).

## Links

- Source observations: [`maintenance/run-log.md` — Run 2026-05-14 — coherence-check](../../maintenance/run-log.md)
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`FRUSTRATED.md`](../../FRUSTRATED.md)
- FR.B.4 SPEC: [`research/fl0-value-justification/output/SPEC.md`](../../research/fl0-value-justification/output/SPEC.md)
- §1.0.1 precedent (closed-research T1/T2 allowance): [`MAINTENANCE.md` §1.0.1](../../MAINTENANCE.md)
