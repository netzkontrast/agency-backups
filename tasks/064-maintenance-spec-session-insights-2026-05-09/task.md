---
type: task
status: active
slug: maintenance-spec-session-insights-2026-05-09
summary: "Roll five gaps surfaced during the 2026-05-09 maintenance-run session into MAINTENANCE.md as concrete amendments: (a) delta-only vs. corpus-wide aggregator scope reconciliation, (b) advisory-tier WARN deduplication policy when filing Tasks, (c) MAINT_STALE_DAYS gate-skipped signal, (d) /sc:* skill bindings for the nightly routines, (e) root-spec frontmatter exemption for README.md."
created: 2026-05-09
updated: 2026-05-09
task_id: "064"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - maintenance-spec-session-insights-2026-05-09
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/maintenance/staleness-audit.py
  - tools/maintenance/trust-audit.py
---

# Task 064 — Roll 2026-05-09 maintenance-run session insights into MAINTENANCE.md

## Goal

Amend `MAINTENANCE.md` so the next agent that executes both the Coherence Check (§2) and the Nightly Maintenance Run (§3) in a single session does not hit the five ambiguities recorded by the 2026-05-09 run. The Task is `done` when the spec answers each of the five questions in §Plan below with a single, mechanically verifiable rule, and `tools/check-governance.sh` exits 0 against the amended state.

## Plan

1. **Delta-vs-aggregator scope reconciliation.** The Coherence Check is delta-only (§2.2), but `tools/maintenance/trust-audit.py` (Task 039 ST-5) ALWAYS scans every `research/<slug>/`. Add a §2.4 paragraph that states which aggregator linters are exempt from the delta-only constraint and why, and how the agent reports their findings without double-filing Tasks for issues outside the delta.
2. **WARN-tier dedup policy.** During the 2026-05-09 run the trust-audit aggregator emitted 13 `recommend-task` lines for pre-existing FL≥1 workspaces that were already covered by open Tasks elsewhere (or were known WARN-tier corpus issues). Add a §3.3 sub-rule: before filing a Task for a WARN-tier finding, the agent MUST grep `tasks/*/task.md` for the offending slug AND check `task_affects_paths`; if either covers it, log in run-log notes and skip.
3. **MAINT_STALE_DAYS gate-skipped reporting.** `tools/maintenance/staleness-audit.py` exits 0 when every active Task is younger than the window (the 2026-05-09 run: 27 of 27 Tasks gate-skipped). Amend §3.4 so the maintenance agent records the gate-skipped count in the run-log explicitly (currently it just shows up as `0 flagged`, which conflates "no drift" with "audit-window-skip").
4. **`/sc:*` skill bindings.** The 2026-05-09 run combined the maintenance routines with `/sc:analyze`, `/sc:reflect`, `/sc:improve`, `/sc:review`, and `/sc:createPR`. None of these skills are referenced from MAINTENANCE.md or `prompts/repo-coherence-check/prompt.md`. Add a "Wiring as a Claude Code Routine" subsection that names the two or three skills that ARE useful to combine with the routines (and explicitly disclaims the rest as out-of-scope for maintenance).
5. **Root-spec frontmatter exemption.** `README.md` has no L1 frontmatter; the governance gate accepts this silently. Either add `README.md` (and any other exempt root files) to a §1 explicit-exemption list, or extend `tools/fm/validate.py` so it emits a diagnostic on root files lacking L1 keys. The Plan MUST decide which path to take and amend whichever spec/tool reflects that decision.

## Todo

- [ ] 1. Read `MAINTENANCE.md` §2.2, §2.3, §3.3, §3.4, §4.1 in full and identify the smallest viable insertion point for each amendment.
- [ ] 2. Draft the §2.4 paragraph (Plan-1) with a short table listing aggregator linters and their delta-exemption rationale.
- [ ] 3. Draft the §3.3 dedup sub-rule (Plan-2) with a worked grep recipe (`grep -lE "task_affects_paths:" tasks/*/task.md | xargs grep -l "<offending-path>"`).
- [ ] 4. Patch `tools/maintenance/staleness-audit.py` (Plan-3) so the gate-skipped count is emitted on stderr in the canonical `<path>::<level>:<code>:<msg>` format and folded into the run-log notes section.
- [ ] 5. Author the `/sc:*` skill bindings subsection (Plan-4) — list `/sc:analyze`, `/sc:reflect`, `/sc:improve`, `/sc:review`, `/sc:createPR` with one-line rationale each.
- [ ] 6. Decide and implement the README.md exemption (Plan-5).
- [ ] 7. Add a paired Gherkin scenario for each amendment under the next free `M.B.<n>` anchor in §6 (Acceptance Criteria).
- [ ] 8. Run `tools/check-governance.sh` against the amended state and confirm exit 0.

## Links

- Executing prompt(s): [`/prompts/maintenance-spec-session-insights-2026-05-09/prompt.md`](../../prompts/maintenance-spec-session-insights-2026-05-09/prompt.md)
- Source spec(s): [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
- Found by: 2026-05-09 maintenance-run session (Coherence Check + Nightly Maintenance combined run); see `maintenance/run-log.md` entry dated 2026-05-09.
