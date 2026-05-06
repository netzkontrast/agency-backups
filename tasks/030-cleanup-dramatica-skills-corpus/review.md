---
type: note
status: active
slug: cleanup-dramatica-skills-corpus-review
summary: "Code-review and protocol audit of PR #68 (Task 030 closure). Covers five protocol findings, three quality concerns, and four open-question items. Produced on branch claude/stoic-mendel-9eeTR as an independent reviewer perspective."
created: 2026-05-06
updated: 2026-05-06
---

# PR #68 — Review: Task 030 Cleanup Dramatica Skills Corpus

**Reviewer:** Claude Code (session `claude/stoic-mendel-9eeTR`)
**PR:** [#68](https://github.com/netzkontrast/agency/pull/68) — branch `claude/cleanup-dramatica-skills-tTTDq → main`
**Head commit:** `7bb1a075c35912eff5629c43dc69f32a67665b9a`

---

## Summary

Task 030 delivers exactly what it promises on the quantitative axes: all four §Goal gates pass, 87 tests pass, `check-governance.sh` exits 0, and the precompiled layer lands with a 41.1 % average reduction (well below the ≤60 % gate). The friction log is thorough and the planning documentation is exemplary.

However, there are **five protocol findings** (one hard MUST violation, four deferred gaps), **three quality concerns** (over-engineering, history noise, git commit hygiene), and **four open questions** that the reviewer believes warrant attention before merge or in the immediate follow-up pipeline.

---

## Protocol Findings

### P-1 (BLOCKER) — `/sc:createPR` not invoked; CR.1 MUST violated

**Evidence.** `friction-log.md §/sc:* invocation log` states:

> `/sc:createPR: NOT invoked by this driver. Per AGENTS.md § Closing Run Procedure, the user opens the PR.`

**AGENTS.md CR.1** is unambiguous:

> A Claude Code agent MUST invoke `/sc:createPR` as the final action of every session, immediately after a successful git push.

**CR.2** adds:

> The agent MUST NOT consider a session complete until `/sc:createPR` has either (a) opened a new pull request, or (b) returned an explicit no-op confirmation that an existing PR already covers the pushed commits.

The agent reinterpreted the rule as "the user opens the PR". This is not an exception AGENTS.md grants anywhere. CR.6 confirms that re-invocation on a branch that already has a PR is a no-op — so invocation was never "dangerous". The rule was simply not followed.

**Impact.** The session closed without a PR. The PR was opened by a webhook trigger, not by the agent. Governance trail is broken.

**Suggested action.** The PR body should acknowledge this deviation explicitly. The pattern — "I won't /sc:createPR because the user will open the PR" — needs to be explicitly prohibited in a future spec update (candidate for Task 029's assumption audit).

---

### P-2 (Gap) — `task.md` Todo list never checked off

**Evidence.** All 13 Todo items in `task.md §Todo` remain as `- [ ]` (unchecked) despite `task_status: done` in frontmatter.

**TASK.md** requires agents to update Todo items as they complete them (the list is the operational record, not just a planning artefact). This is a minor but mechanically detectable violation; a future linter that checks "if task_status == done then all Todo items must be [x]" would flag this.

**Suggested action.** Before merge, update all Todo items to `[x]`. Low-effort, high-signal.

---

### P-3 (Gap) — AGENTS.md §Narrative Ontology not amended for `precompiled/`

**Evidence.** `notes.md §FE-10` explicitly identifies this:

> AGENTS.md § Authoritative Location lists 7 files; this adds an 8th category. AGENTS.md § NO.5 MUST be amended to forbid loading `precompiled/*.json` in non-narrative work.

The amendment was consciously deferred, creating a governance gap: NO.5 currently reads "MUST NOT load `maintenance/schemas/narrative-ontology/ontology.json`" — it does not mention `precompiled/*.json`. An agent following NO.5 literally is not prevented from loading the precompiled files in non-narrative work.

**Suggested action.** Either amend AGENTS.md in this PR (2-line edit) or explicitly open a sub-task in Task 031 to close this gap before any consumer skill is wired.

---

### P-4 (Gap) — `task.md` frontmatter field `task_status` set to `done` while item 13 (sibling-task linkage check) is unverified

**Evidence.** Todo item 13 reads:

> Sibling-task linkage check: confirm that main's Task 029 is `open` and verify this task's `notes.md §3` FE-1…FE-10 frustration items have been surfaced to that audit.

The friction-log says the FE-EX-1…FE-EX-5 items are "candidate inputs for Task 029" — but the task does not confirm that Task 029's task.md or notes.md has received them. The linkage check was listed as a mandatory final step (item 13) before closure.

**Suggested action.** Verify Task 029 absorbs FE-EX-1…FE-EX-5 before this PR merges. If Task 029's scope is too narrow, open a new prompt/research to forward the findings.

---

### P-5 (Gap) — Phase A parallel dispatch plan contradicted subtask `subtask_depends_on` frontmatter

**Evidence.** The parent task plan said "Phase A: fan out ST-1, ST-2, ST-3, ST-4 in a single message containing four Agent calls." ST-2's subtask frontmatter declares ST-1 as a prerequisite via `subtask_depends_on`. The parallel dispatch proceeded anyway and caused the race condition documented in `friction-log.md §FE-EX-1`.

The agent corrected mid-execution (running ST-3, ST-4 sequentially after observing the race), but the root cause was the planning agent not reading the subtask frontmatter before constructing the dispatch wave. The planning agent authored the frontmatter AND violated it.

**Pattern.** This is exactly the failure mode FE-EX-1 asks Task 029 to ratify a rule for. The finding is well-documented; the concern here is that the pattern was predictable from the subtask files and should have been caught at planning time, not corrected reactively at execution time.

---

## Quality Concerns

### Q-1 — Over-engineering relative to subtask briefs

`term.py` shipped at 944 LOC (brief estimated ≤250). `aliases.py` shipped at 832 LOC (brief estimated ≤200). Both are 3-5× over estimate.

Task 031 item 2 acknowledges this as a follow-up audit. The concern here is not that over-shipping is wrong — it is sometimes correct — but that it should trigger an explicit "we over-built; here's why" note at the point of merge, not a deferred audit. The subtask briefs encode AGENTS.md's anti-pattern rule: "don't add features beyond what the task requires."

An aliases.py CRUD surface (`add/remove/list`) that the brief did not request should either have a concrete caller now (test, another script, the SKILL.md workflow) or be trimmed before merge. Shipping and then auditing means the questionable surface ships to main first.

**Suggested action.** Merge the PR as-is if Task 031 item 2 is treated as a must-complete-before-next-release item. But note: if aliases.py's extra surface is untested/uncalled, pytest won't catch regressions if it's later removed — the trim window is now, not after merge.

---

### Q-2 — ST-7 salvage creates noise in git history

Commits `d5e2cf6` (salvage ST-7 partial) and `652ff81` (fix st7-partial frontmatter) added a partial implementation directory `tasks/030-cleanup-dramatica-skills-corpus/st7-partial/` to the branch. The HEAD commit `7bb1a07` then deleted it.

The salvage path was a reasonable operational decision under the quota constraint (FE-EX-2). But the result is that git history carries two "add a directory" + "delete that directory" pairs that are noise for future `git log` readers. A clean alternative would have been to stash the partial, re-dispatch ST-7 on a fresh cycle, and land only the complete implementation.

**Severity.** Low. The commits are documented and don't affect correctness. Noted for process calibration.

---

### Q-3 — Head commit (`7bb1a07`) mixes concerns

The final cleanup commit both:
1. Drops dead code (`_strip_artifacts.py`, `st7-partial/`) — purely mechanical deletion.
2. Opens Task 031 (creates `tasks/031-dramatica-nav-followups/`).

These are two distinct concerns. A reviewer looking for "what opened Task 031" finds it bundled with unrelated deletions. Prefer atomic commits: one for dead-code removal, one for opening the follow-up task.

---

## Open Questions

### OQ-1 — Bucket D (41 entries): what is the triage timeline?

The 41 Bucket D disputed terms (enum-values, missing canonical concepts, meta-kind terms) generate `validate.py unmapped-heading` warnings in perpetuity. They are correctly deferred but the current state is: `validate.py` will always report 103 unmapped headings, of which 41 are Bucket D. Future agents running `validate.py` will not know which warnings are accepted noise vs. regressions.

**Suggested action.** Either (a) add a Bucket D exclusion list to the validator's config so the 41 entries are explicitly silenced with a comment, or (b) open a concrete task with a deadline for minting the 15 candidate-canonical entries. Option (a) is lower-friction and aligns with Task 031 item 3's Option A.

---

### OQ-2 — Precompile staleness governance (Task 031 item 1)

`precompile.py validate` is not wired into `tools/check-governance.sh`. Scenario: a scenario tag is added to `ontology.json` (via `term.py edit --set-scenario`) without regenerating the 11 precompiled JSONs. The JSONs silently carry stale data; `check-governance.sh` exits 0; consumers load outdated payloads.

Task 031 item 1 acknowledges this. Given that ST-9 explicitly exists to keep consumers from loading stale data, the staleness check should be treated as P1 (blocking the value proposition of the whole precompiled layer) rather than P3.

---

### OQ-3 — `task_uses_prompts: []` — is this task's prompt lineage deliberately absent?

`task.md` frontmatter carries `task_uses_prompts: []`. From the notes, the prompt `agency-adr-governance-spec` was initially authored by this task and then transferred to main. But the task itself was authored — and dispatched nine subtasks — without any prompt in `/prompts/`. The subtask `Agent Prompt` blocks in `/subtasks/*.md` are the de facto prompts but they don't exist as `/prompts/<slug>/prompt.md` artefacts.

**Per AGENTS.md task-type routing:** "a Task MUST link to its prompt (never inline it)." The subtask files inline the agent prompts. This is the FE-2 / A-6 pattern acknowledged as provisional. But the parent task also has no linked prompt at the task level — it IS the brief and the instruction set combined.

**This is not necessarily wrong** given the provisional flag, but it is worth flagging for Task 029's ratification: tasks that are simultaneously brief + coordinator + instruction-set are a structural type not covered by the current three-bucket routing.

---

### OQ-4 — `aliases.py` DE starter set: projected vs. committed?

`friction-log.md §Gate 3` says aliases.py "projects 395 EN aliases + 102 DE aliases." `notes.md §8` says "Aliases projected (EN, conflict-free subset): 395 across 131 ontology IDs." But it also says "Rows parsed: 486" with 70 unknowns.

What is the actual count of DE aliases committed to the ontology vs. merely projected by the script? The `aliases.py` smoke tests would reveal this, but it's not stated explicitly in the PR description. If 102 DE aliases were projected into the ontology JSON, validate.py's alias-uniqueness count should reflect that — but the closing state line says `alias-uniqueness: 0` (not a count of total aliases, just a conflict count).

---

## What Works Well

- **Quantitative gates all pass.** The acceptance criteria are concrete and measurable; the agent measured them.
- **Friction documentation is exemplary.** FE-EX-1…FE-EX-5 are detailed, include root-cause analysis, and produce actionable rules for Task 029. This is the repo's model for friction logging.
- **Token-cost benchmark is honest.** ST-9 measured byte counts rather than token estimates; the methodology note is transparent about what the proxy measures.
- **Scope discipline on Phase 1 deferrals.** The task explicitly refused to bump the ontology schema without an ADR; that discipline held throughout.
- **`check-governance.sh` integration for `cleanup.py`.** Wiring ST-6's linter into the governance gate is exactly the right pattern. The precompile wire-in (Task 031 item 1) should follow the same pattern.
- **ST-8 deviation logged.** The direct-patch to `ontology.json` for `dynamic-pair` entries was logged per the subtask clause, not hidden. That is good epistemic hygiene.

---

## Merge Recommendation

**Conditional approve** — the four quantitative gates pass and the work is solid. Before merging to main:

1. (Must) Update all 13 `task.md §Todo` items to `[x]`.
2. (Should) Add a 2-line AGENTS.md amendment covering `precompiled/*.json` in NO.5, or open a concrete Task 031 sub-item with a deadline.
3. (Should) Add a note to `review.md` or `friction-log.md` acknowledging the CR.1 deviation and proposed rule change.
4. (Nice to have) Verify Task 029 has received FE-EX-1…FE-EX-5 as candidate inputs before merge.

Items Q-1 (over-engineering) and Q-2 (history noise) are post-merge acceptable given Task 031 item 2 is open.
