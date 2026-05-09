---
type: prompt
status: active
slug: maintenance-spec-session-insights-2026-05-09
summary: "Amend MAINTENANCE.md so the next combined Coherence + Nightly run does not hit the five ambiguities recorded on 2026-05-09: delta-vs-aggregator scope, WARN dedup policy, MAINT_STALE_DAYS gate-skipped reporting, /sc:* skill bindings, root-spec frontmatter exemption."
created: 2026-05-09
updated: 2026-05-09
prompt_kind: tool-instruction
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-session-insights-2026-05-09
---

# Roll 2026-05-09 maintenance-run session insights into MAINTENANCE.md

## Framework

**RISEN — Role / Input / Steps / Expectations / Constraints.** The amendments are mechanical edits to a single root spec plus one tool patch and a paired Gherkin anchor block; there is no exploratory phase, so the linear RISEN spine is the right shape.

## R — Role

You are a governance-spec amendment agent. Your mandate is to lift the five gaps recorded by the 2026-05-09 maintenance-run session into `MAINTENANCE.md` as binding rules and to add one paired Gherkin acceptance scenario per amendment so the next coherence run can mechanically verify the changes.

## I — Input

Read these files in full before mutating anything:

- `tasks/064-maintenance-spec-session-insights-2026-05-09/task.md` — the Plan/Todo you MUST satisfy.
- `MAINTENANCE.md` §2.2, §2.3, §3.3, §3.4, §4.1, §6 — the target sections for each amendment.
- `prompts/repo-coherence-check/prompt.md` — the executing routine that exposed gap-1 (delta-vs-aggregator scope).
- `tools/maintenance/staleness-audit.py` — the tool patched in Plan-3 (gate-skipped count emission).
- `tools/maintenance/trust-audit.py` — the aggregator that motivates Plan-1 and Plan-2.
- `maintenance/run-log.md` (last entry, dated 2026-05-09) — the canonical record of the session that found the gaps.

## S — Steps

1. Read the Task body once and confirm the five Plan items are mutually independent. The agent MUST treat each as a separate atomic edit; bundling is permitted only when two edits share an insertion point.
2. Draft the §2.4 paragraph for Plan-1 (delta-vs-aggregator scope). The paragraph MUST list every aggregator linter by name and state whether each is delta-only or corpus-wide, with a one-line rationale per row.
3. Draft the §3.3 dedup sub-rule for Plan-2. The rule MUST cite a deterministic grep recipe the agent runs before filing a Task; if the recipe matches an existing open Task, the agent MUST skip and log in run-log notes.
4. Patch `tools/maintenance/staleness-audit.py` for Plan-3. The script MUST emit one diagnostic line in the form `<path>::<level>:<code>:<msg>` summarising the gate-skipped count, AND fold the count into the script's stdout summary. Existing tests under `tools/tests/maintenance/test_staleness_audit.py` MUST continue to pass; add a new test for the gate-skipped diagnostic.
5. Add the `/sc:*` skill-bindings subsection under §3 or §4. The subsection MUST list `/sc:analyze`, `/sc:reflect`, `/sc:improve`, `/sc:review`, `/sc:createPR` with one-line rationale per skill, AND it MUST disclaim the rest of the `/sc:*` corpus as out-of-scope for the maintenance routines.
6. Decide the README.md exemption for Plan-5: either (a) add `README.md` to a §1 explicit-exemption list, OR (b) extend `tools/fm/validate.py` to emit a diagnostic on root files lacking L1 keys. The agent MUST pick exactly one and SHOULD prefer (a) because (b) regresses every existing root-spec author who SHOULD already carry frontmatter.
7. Add one paired Gherkin scenario per amendment under the next free `M.B.<n>` anchor in `MAINTENANCE.md §6`. Each scenario MUST be self-contained, MUST cite the linter or grep recipe that mechanically verifies it, and MUST be addressable by its anchor.
8. Run `tools/check-governance.sh` against the amended state. Exit 0 is required before commit.
9. Commit and update `tasks/064-maintenance-spec-session-insights-2026-05-09/task.md` to `task_status: done` with a `friction-log.md` declaring the run's FL.

## E — Expectations

| Deliverable | Path |
|---|---|
| Amended root spec | `MAINTENANCE.md` |
| Tool patch + new test | `tools/maintenance/staleness-audit.py`, `tools/tests/maintenance/test_staleness_audit.py` |
| Paired Gherkin scenarios | `MAINTENANCE.md §6` (M.B.8 through M.B.12) |
| Closing FL declaration | `tasks/064-.../friction-log.md` |
| Closing run-log entry | `maintenance/run-log.md` (`routine_type: task-implementation`) |

## Constraints

- The agent MUST NOT mutate any file under `decisions/<NNNN>-<slug>.md` whose `adr_status:` is `Accepted` (T4-immutable per MAINTENANCE.md §1).
- The agent MUST NOT use `sed` or `awk` to mutate frontmatter; canonical mutator is `tools/fm/edit.py`.
- The agent MUST NOT bundle the five amendments into a single edit if it forces non-independent changes; preserve atomicity per Step 1.
- The agent MUST NOT introduce new aggregator linters as part of this Task — the scope is documenting what already exists, not extending the toolchain.
- Exactly one RFC 2119 keyword per sentence in any normative prose the agent writes (per `maintenance/language-spec.md §2.2 U1`).
