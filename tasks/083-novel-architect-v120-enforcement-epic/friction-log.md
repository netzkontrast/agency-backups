---
type: note
status: active
slug: novel-architect-v120-enforcement-epic-friction-log
summary: "Friction log for Task 083 — novel-architect@1.2.0 enforcement Mini-Epic. Tracks scaffold session (FL declaration appended end-of-session) and subsequent sub-task working sessions if they record Epic-level observations."
created: 2026-05-12
updated: 2026-05-12
---

# Friction Log — Task 083 (novel-architect@1.2.0 Enforcement Mini-Epic)

**Highest Frustration Level: FL1**

## Scaffold Session (2026-05-12)

### Context

Single-session scaffolding of the Mini-Epic shape per [Task 070 friction log §"Take-away"](../070-novel-architect-v110-epic/friction-log.md#take-away-for-future-sessions):

> When an Epic is created the same day as it is asked to close, the session agent should re-confirm scope before executing — the user may actually want "set up the scaffold, then iterate over weeks" rather than "implement everything now".

This session's contracted shape: **scaffold-only**. The Epic and 5 sub-task folders (084-088) are filed with full Goal/Context/Plan/Todo/Acceptance/Links bodies; the standalone gated Task 089 is filed separately; ADR-0010 is drafted at `adr_status: Proposed`. No implementation lands in this session — each sub-task is worked in its own session per the 070 lesson.

The execution plan was produced via a four-stage `/sc:*` decision chain (`brainstorm` → `design` → `workflow` → `implement`), each stage gated on explicit user confirmation:

- **brainstorm** locked: Mini-Epic shape, renderer in-scope, linters ship ERROR-tier day 1.
- **design** produced: 6 task folders + 1 ADR (16 new files + 1 modified `tasks/readme.md`), shared-lib pattern at `tools/novel-architect-checks/`, JSON-artefact renderer coupling, narrow-scope ADR.
- **workflow** produced: 10-phase execution plan (Phase 0 OQ resolution → Phase 9 commit+push+draft PR).
- **implement** (this session): executes phases 0-9 with `AskUserQuestion` gates at every substantive choice (per OQ-meta locked in Phase 0 batch 2).

### Observations during scaffold

- **OQ batch design absorbed material churn upfront.** Two `AskUserQuestion` batches in Phase 0 (4 + 3 questions) resolved 7 open decisions in two round-trips. Without this front-loading, each phase would have surfaced 2-4 ambiguities mid-write, with rollback cost on each redirect. Locking OQ-meta to "stop and ask for every ambiguity" added two further AskUserQuestion rounds (ADR substance + Epic content) before file writes — visible cost in turn count, real benefit in zero post-write redirects.
- **ADR number drift caught at Phase 1.** Design doc placeholdered "ADR-0008"; Phase 1 verification revealed ADR-0007/0008/0009 already filed, so the actual slot is **0010**. Catching this in Phase 1 before any file referenced "0008" avoided a multi-file cross-reference rewrite. Lesson: ADR-number verification belongs in Phase 1, not embedded as a literal in design docs.
- **Baseline governance gate passed with 8 pre-existing WARNs + 2 ERROR-tier FL declaration findings on Tasks 030 and 033.** The 2 ERRORs are advisory (linter is `[opt]` not gating); recorded here so post-scaffold Phase 7 can compare against the same baseline rather than treating pre-existing findings as new regressions.
- **Frontmatter `type: adr` confirmed via precedent** — CLAUDE.md §4's `type` enum lists `{task, prompt, research, spec, readme, note, index}` but does NOT include `adr`. Reading ADR-0009 confirmed `type: adr` is the in-use convention. The CLAUDE.md enum is non-exhaustive; the validator accepts `adr`. Worth flagging for a documentation update if anyone authors a successor ADR-NNNN cold from the CLAUDE.md text.

### Frustration sources (rated honestly)

- **FL1 — Phase 7 governance gate failed on first pass; 3 ERROR-tier fixes required.** The scaffold-only contract held overall (no scope creep, no rollback, no destructive operations), but the validation gate surfaced three real defects that required mid-flight edits before re-running:

  | # | Defect | Origin | Fix |
  |---|---|---|---|
  | 1 | `decisions/0010-*.md` summary 461 chars > 240 char `ADR.A.2.2` schema cap | I wrote a too-long summary embedding the full decision context; the validator caught it cleanly | `tools/fm/edit.py --set summary=<tighter>` |
  | 2 | `tasks/089-*/task.md` `task_supersedes: ["novel-architect-legacy"]` is a dangling reference (validator F.T.1) — `novel-architect-legacy` is a skill slug, not a task_id | Over-interpreted Task 070's body-prose suggestion as a literal frontmatter assignment | `tools/fm/edit.py --remove-from-list task_supersedes novel-architect-legacy`; preserved supersession intent in body prose + the new `notes.md` |
  | 3 | `tasks/089-*/notes.md` missing — TASK.md §8.4 + Spec-I.3.1 require `notes.md` on any `task_status: blocked` Task | Did not surface this constraint in `/sc:design` or `/sc:workflow` phases; the validator caught it | Authored `notes.md` with gating-criteria monitoring procedure + per-criterion evidence guidance (also a discoverability win — the notes file is more useful than the bare body section the validator wanted) |

- **FL1 (sub-source) — `/sc:workflow`'s Phase 7 budget under-estimated the rollback cost.** The plan assumed validation would pass first-pass with the precondition reads (Phase 1 precedent absorption). It didn't, because the 3 defects above were all from constraint *details* that the precedent reads did not surface: ADR summary length cap (only triggers on >240 chars), F.T.1 dangling-reference semantics (only triggers when the value is a non-task slug), and notes.md requirement on blocked Tasks (only triggers on task_status=blocked, which is uncommon enough that no precedent file used it).

  The first-pass-fail outcome is **defensible** — the alternative would have been to read TASK.md §8.4 + the ADR schema definitions + the F.T.1 validator source in Phase 1, which would have inflated Phase 1 from ~5 reads to ~10. The trade-off (smaller Phase 1, possible Phase 7 retry) was implicit in the workflow plan; making it explicit in future workflows is a cheap improvement.

- **FL0 (residual) — Everything else.** The 4-stage `/sc:*` chain ran without scope creep, the parallel-write batch (15 Writes in 2 messages) executed cleanly, the precedent-absorption Phase 1 read pass eliminated most body-shape ambiguity, and the OQ-meta "stop and ask for every ambiguity" policy held without descending into per-sentence interrupts. Net session is **FL1 (minor)**, not FL2 — no rollback, no broken state, just one fix-and-retry cycle on a hard gate.

### What worked

- **Phase 0 AskUserQuestion batches.** Two batches of 4+3 questions front-loaded all design-level decisions. Subsequent phases ran without further design-level user prompts (only content-level AskUserQuestion rounds for ADR substance and Epic content, which is a different kind of question).
- **Phase 1 repo-state verification with ADR-number capture as a discrete step.** Identified the off-by-two ADR-number drift before any file embedded the wrong literal.
- **Precedent reading before writing.** Phase 1.6 read ADR-0009, Tasks 070 + 072 task.md, the 070 readme.md and friction-log.md, plus `tasks/readme.md` in one parallel batch. The 6 files cost ~5K tokens but eliminated ~10 different "what does the convention say?" downstream questions.

### Take-away for future sessions

Mini-Epic scaffolding (no implementation) is the right cut when the parent Epic's friction log explicitly flagged scope-versus-session mismatch (070 §FL2). Each sub-task gets its own session, its own friction log, its own PR. The cost is more sessions; the benefit is each session lands cleanly within its scope-budget rather than producing the "lean but real" trade-off that 070 had to make under time pressure.

The 4-stage `/sc:*` chain (`brainstorm` → `design` → `workflow` → `implement`) is heavyweight for a 17-file scaffold (16 planned + 1 unplanned `notes.md` from the blocked-Task validator constraint) but absorbs material decision-churn upfront. For a same-day scope-and-implement Epic (which 070 was), skipping straight to `/sc:implement` is faster but produces FL1+ from the lack of explicit gating. This scaffold session traded turn-count for the FL1 outcome and the broader-than-expected file footprint — a defensible trade when the change touches governance contracts (ERROR-tier linter promotion, ADR precedent shift).

**Lessons captured for the next Mini-Epic scaffold session:**

1. **Phase 1 should explicitly read TASK.md §8.4 + the ADR frontmatter schema** when a `task_status: blocked` Task is in scope, OR when an ADR is being authored. Both surface validator constraints that Phase 7 will gate on but precedent-file reads alone won't show.
2. **`tools/fm/edit.py --remove-from-list KEY VALUE` is the syntax for list-valued frontmatter** (not `--set KEY=[]` as I tried first). Document this in future workflow plans where list-field cleanup is a possibility.
3. **A `notes.md` is a useful disposition artefact for any "blocked but discoverable" Task** even beyond the validator requirement — the per-criterion monitoring guidance produced for 089's notes.md is more useful than the bare body §"Gating Criteria" section the task.md already had.
4. **Summary fields under 240 chars require sustained compression discipline.** The ADR-0010 first-pass summary was 461 chars because I tried to embed the full decision context; the lesson is to summarize the *decision* + *narrowness* + *sunset* and let the body carry the context. The fix took 1 tool call once spotted.

## Sub-task summary

| Task | Status (at scaffold) | Primary deliverable | Sequel notes |
|------|---------------------|---------------------|--------------|
| 084 | open | Shared lib `tools/novel-architect-checks/` + `tools/check-hard-rules.py` ERROR-tier + worksheet_audit body-schema | Foundation: 085/086/087 block on this |
| 085 | open (blocked by 084) | `tools/check-worksheet-order.py` + `tools/check-scene-audit.py` ERROR-tier | Each linter needs ≥3 clean + ≥3 bad fixtures |
| 086 | open (blocked by 084) | `tools/check-canon-status.py` ERROR-tier | — |
| 087 | open (blocked by 084) | `render_architecture.py` reads `.architecture-validation.json` | Graceful fallback for stale/missing artefact |
| 088 | open | MIF L3 frontmatter backport on `references/learnings.md` | T4 entries get metadata-only edits per MAINTENANCE.md §1.0.1 |
| 089 | blocked (standalone, NOT a sub-task) | Legacy retirement gated on Task 070 criteria (a)/(b)/(c) | Filed in this scaffold for discoverability |

## Closing Procedure (AGENTS.md CR.1–CR.7)

- [x] Friction log written with FL declaration (this file — FL1)
- [x] tasks/readme.md index synced (in this commit set; 7 new entries Epic + sub-tasks 084-088 + standalone 089)
- [x] tools/check-governance.sh — exit 0 confirmed at Phase 7 re-run after the 3 mid-flight fixes
- [ ] Draft PR — opens via mcp__github__create_pull_request at Phase 9 (next step after this friction log is committed)
