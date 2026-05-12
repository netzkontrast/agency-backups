---
type: note
status: active
slug: pr-122-review-task-094-epic-spec
summary: "Peer review of PR #122 (Task 094 Epic spec): 0 blocking + 5 advisory items. Governance and frontmatter validated clean. Epic structure, D.7 compliance, and Gherkin AC anchoring all correct. Advisory items cover an ephemeral path reference, a prompt-layer audit-graph gap, an unverifiable Gherkin assertion, an executable ellipsis in grep paths, and a missing ADR for the new .claude/ topology."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #122 · Task 094 Epic Spec: Skill Integration & Agency Default Surface

**Reviewer:** @claude (claude-sonnet-4-6)  
**PR:** [#122](https://github.com/netzkontrast/agency/pull/122)  
**Branch:** `claude/task-094-epic-spec` → `main`  
**Commit reviewed:** `ddd9903c151530f1849f90ad65d6feb7c43b28e1`  
**Date:** 2026-05-12  
**cc:** @jules

---

## Verdict: APPROVED (0 blocking · 5 advisory)

The Epic spec is well-structured, governance-clean, and faithful to the Task 091/092 idiom. D.7 compliance is rigorously cited throughout all five spec files. Gherkin ACs are anchored. The source plan is archived. No structural or frontmatter errors were found. Five advisory items are documented below; none block merge.

---

## What was verified

| Check | Result |
|---|---|
| `tools/check-governance.sh` (full repo) | ✅ PASS (`=== PASS: all governance checks passed. ===`) |
| `python3 tools/fm/validate.py tasks/094-skill-integration-agency-default/` | ✅ 0 diagnostics (4 files) |
| L1 Vault Core keys (`type`, `status`, `slug`, `summary`, `created`, `updated`) | ✅ present in all 11 new files |
| L2 task keys (`task_id`, `task_status`, `task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`, `task_spawns_prompts`, `task_affects_paths`, `task_blocked_by`) | ✅ present in `task.md` |
| Gherkin AC anchors (BR.94.1–BR.94.5 Epic; T094.1.1–T094.4.4 per-subtask) | ✅ all anchored |
| D.7 re-asserted in Epic + all four subtask `## Out of scope` sections | ✅ confirmed |
| Friction-log initialized with `Highest Frustration Level: FL0` declaration | ✅ FR.B.4 satisfied |
| Source plan archived at `references/source-plan.md` | ✅ confirmed |
| `tasks/readme.md` index row for Task 094 | ✅ present with `Status: open` |
| `task_blocked_by: ["092"]` → Task 092 `task_status: done` (block satisfied at spec time) | ✅ confirmed |
| Three-file subtask scaffold: readme.md + 4 subtask files | ✅ confirmed |
| FOLDERS.md §8 carve-out for `.claude/` and `.claude-plugin/` flagged in ST-2 scope | ✅ addressed |
| No source-code, root-spec, `.claude/`, `tools/hooks/`, or `skills/` changes in this PR | ✅ zero implementation files changed |

---

## Advisory A1 — Ephemeral path reference leads the `task.md ## Note — Source plan` section

**Severity:** Advisory — does not break governance today, but will silently mislead future readers and agent sessions.

**What happened:**

The opening sentence of `task.md ## Note — Source plan` reads:

> "This Epic spec is the execution surface of the planning artifact at `/root/.claude/plans/now-please-look-at-greedy-cascade.md` (Claude-Code Plan-mode output from session `01WBrHNUZUEoew9PE9A7SguS`)."

`/root/.claude/plans/` is a per-session ephemeral harness directory. It does not exist after the session closes, is not in the repo, and cannot be resolved by any agent, reviewer, or CI job that opens this file in a subsequent session. `references/readme.md` correctly flags this (Assumptions Log: "The mirror in this folder is the **canonical record**; the original `/root/.claude/plans/` path is a per-session ephemeral location.") — but `task.md` itself leads with the unreachable path before mentioning the archived copy.

**Recommended repair (T1 — in-place):**

Replace the opening sentence with one that leads with the canonical archived path:

```
This Epic spec is the execution surface of the planning artifact archived at
[`references/source-plan.md`](./references/source-plan.md) (Claude-Code Plan-mode output,
session `01WBrHNUZUEoew9PE9A7SguS`, 2026-05-12). The original harness path
`/root/.claude/plans/now-please-look-at-greedy-cascade.md` is ephemeral and not tracked;
the archived copy is the durable record.
```

Can be applied in-place via `Edit` — no T3 Task required.

---

## Advisory A2 — `task_uses_prompts: []` bypasses the formal prompt layer; audit-graph gap

**Severity:** Advisory — architectural routing concern; policy decision required before ST-4 closes.

**What happened:**

Per CLAUDE.md §3 routing table:

> "Author an executable instruction set for an agent → `/prompts/<slug>/prompt.md` (+ `brief.md` + `readme.md`)."

This Epic was authored from a Claude Code Plan-mode artifact (`source-plan.md`) which served as the executable instruction set. No formal `type: prompt` file was filed under `/prompts/`. The `task_uses_prompts: []` annotation is accurate — no prompt exists — but it also means the audit graph has a traceable gap: there is no `prompt → research → output` chain for the origin of this Epic's design decisions.

This is the **first Epic in the Task 091/092/094 chain that was authored without a preceding prompt.** Tasks 091 and 092 were also authored directly (checking…) — this appears to be an established pattern for Plan-mode Epics. However, the pattern has never been ratified in a governance document.

**Recommended action (before ST-4 closes this Epic):**

One of:
1. **File a lightweight ADR** (or add a TASK.md §X note) recording "Plan-mode planning artifacts are an accepted substitute for the prompt layer when the artifact is archived under `references/source-plan.md` and `task_uses_prompts: []` is annotated explicitly." This closes the audit-graph gap at the policy layer.
2. **Retroactively file a `prompts/task-094-epic-spec/prompt.md`** that formally wraps the source-plan. Heavier but makes the graph complete.

Option 1 is lower friction. If the repo already has a precedent (Tasks 091/092 were similarly prompt-free), filing the ADR covers all three retroactively.

---

## Advisory A3 — Gherkin AC BR.94.2 contains an unverifiable "session log" assertion

**Severity:** Advisory — testability gap; affects ST-2 PR acceptance.

**What happened:**

Gherkin scenario `BR.94.2` (and its ST-2 mirror `T094.2.1`) includes:

```gherkin
And the session log MUST show 52 skill descriptions loaded into context
```

The Claude Code session log is an ephemeral, non-machine-readable artefact. There is no defined path, format, or tooling in this repo to observe "skill descriptions loaded into context" — unlike AC BR.94.4 (where `pytest tools/tests/test_hooks.py` provides a machine-testable oracle).

An ST-2 implementer reviewing the PR checklist cannot confirm this assertion via any command in the repo. It will inevitably be marked as "operator-verified" (i.e. informally checked by the PR author), which undermines the Gherkin precision standard.

**Recommended repair:**

Replace the unverifiable clause with a proxy that *can* be tested in the repo:

```gherkin
And `find .claude/skills -name "SKILL.md" | wc -l` MUST return 52
```

This proxy confirms the symlink resolves to the full corpus — which is the machine-checkable precondition for the loading claim. The actual loading behaviour can be noted as an operator-verified observation in the PR body, not a Gherkin MUST.

---

## Advisory A4 — Gherkin `grep` paths use Unicode ellipsis `…` (not resolvable by a shell executor)

**Severity:** Advisory — documentation convention, but may cause executor confusion.

**What happened:**

Multiple Gherkin `And` clauses use `…` (U+2026 HORIZONTAL ELLIPSIS) as a path placeholder:

```gherkin
And `grep "superclaude_framework@v4.3.0" tasks/092-…/references/triage-notes/` MUST return zero matches
```

The actual filesystem path is `tasks/092-port-skill-corpora-phase-2/references/triage-notes/`. An agent executing this Gherkin scenario verbatim would run a `grep` with a literal `…` in the path — which does not exist — and get a false-pass (no matches because no files were searched). The same pattern appears in AC BR.94.5, T094.1.3, and the `source-plan.md` mirror.

This is a documentation convention inherited from the plan, not an executable spec defect at the spec-planning stage. However, the repo's stated standard (CLAUDE.md §5) is "Gherkin scenarios MUST be self-contained and executable."

**Recommended repair (T1 — in-place):**

Replace all `…` ellipsis placeholders in Gherkin `And` clauses with the actual slug:

```
tasks/092-port-skill-corpora-phase-2/references/triage-notes/
```

Can be done with a targeted `Edit` on `task.md` and `references/source-plan.md`. Anchored occurrences to fix: `BR.94.5 (task.md:173)`, `T094.1.3 (subtasks/01-root-spec-hookup.md:75)`, `source-plan.md:196`.

---

## Advisory A5 — No ADR filed for the new `.claude/` + `.claude-plugin/` topology conventions

**Severity:** Advisory — CLAUDE.md §5 routing concern; ST-2 implementers should address before that PR merges.

**What happened:**

CLAUDE.md §5 routing table states:

> "Change a repo-architecture convention (paths, schemas, hooks, branching) → `decisions/<NNNN>-<slug>.md` (MADR 4.0.0)."

ST-2 introduces two new top-level directories (`.claude/` and `.claude-plugin/`) and establishes:
- The `.claude/skills/` symlink as the canonical skill-loading mechanism (Pattern A).
- The `.claude-plugin/plugin.json` as the plugin-manifest contract.
- The `.claude/agents/` thin-wrapper re-export idiom for persona skills.

These are **repo-architecture conventions** — they define where Agency's integration surface with Claude Code lives. The Epic "Out of scope" sections say "A new ADR is filed if Phase 3 surfaces new architecture decisions (e.g. ratifying the `.claude/skills/` symlink as the canonical loader path)." But the symlink *is* being ratified in this Epic (it's in the ST-2 AC at T094.2.1). Deferring the ADR to a hypothetical "Phase 3" leaves the architectural decision undocumented in the decisions ledger.

**Recommended action:**

Author `decisions/0013-claude-dir-integration-and-plugin-manifest.md` (MADR 4.0.0) as part of ST-2, before or alongside the `.claude/` directory creation. Key decisions to record:

1. `.claude/skills/` symlink (not copy) as the primary skill-loading path, with copy-fallback script as the Windows escape hatch.
2. `.claude-plugin/plugin.json` as the canonical plugin manifest (plugin root = repo root).
3. `.claude/agents/` thin-wrapper re-export idiom for persona-kind skills.
4. Rationale for NOT using SessionStart hooks for skill loading (D.7 constraint; `.claude/skills/` provides the same discoverability without hooking).

Without an ADR, future maintainers have no decisions-ledger entry explaining why the repo is structured this way, and the `check-governance.sh` trust audit cannot trace the architectural provenance.

---

## Summary table

| Issue | Severity | Recommended action |
|---|---|---|
| A1 — Ephemeral `/root/.claude/plans/` path leads `task.md ## Note` | Advisory | T1 in-place `Edit`; move canonical archived path to lead sentence |
| A2 — `task_uses_prompts: []` with no prompt-layer rationale | Advisory | File ADR or TASK.md policy note before ST-4; or retroactively file `prompts/` entry |
| A3 — BR.94.2 `session log MUST show 52 descriptions` is unverifiable | Advisory | Replace with proxy: `find .claude/skills -name "SKILL.md" \| wc -l` MUST return 52 |
| A4 — Gherkin grep paths use Unicode `…` (not executable) | Advisory | T1 in-place `Edit`; replace `…` with actual slug in all Gherkin code blocks |
| A5 — No ADR for new `.claude/` + `.claude-plugin/` topology | Advisory | Author `decisions/0013-*` as part of ST-2, before that PR merges |

No blocking issues. Epic spec may merge; advisory items should be addressed in ST-1 (A1, A3, A4) and ST-2 (A5) PRs, with A2 resolved no later than ST-4.

---

## Notes for @jules

@jules — if you pick up any of the ST-1 through ST-4 subtasks, the five items above are the key pre-flight checks beyond the per-subtask acceptance criteria:

- **ST-1 implementer:** Fix A1 (ephemeral path reference), A3 (unverifiable Gherkin clause), A4 (ellipsis in grep paths) as in-place `Edit` repairs in the same PR — they are all T1/T2 operations and add no T3 scope risk.
- **ST-2 implementer:** File ADR-0013 (A5) before or alongside the `.claude/` directory creation. This is MADR 4.0.0 scope; consult `decisions/0011-external-skill-corpora-import.md` as structural precedent.
- **ST-4 closer:** Confirm A2 (prompt-layer gap) has been addressed by a policy note or ADR before flipping `task_status: done`; the trust audit will flag a `task_owner: "unassigned"` — set it to `claude` via `tools/fm/edit.py --set` per ST-4 spec.
