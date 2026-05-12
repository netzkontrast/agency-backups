---
type: note
status: active
slug: task-092-st2-pr117-review
summary: "Peer review of PR #117 (Task 092 ST-2 batch A): 10 pure-port SC skills. Two blocking issues: false ✅ on T092.2.1 and a dangling forward reference in sc-troubleshoot. Two advisory items."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #117 · Task 092 ST-2 batch A: Pure-port 10 SuperClaude skills

**Reviewer:** claude-sonnet-4-6  
**PR:** [#117](https://github.com/netzkontrast/agency/pull/117)  
**Branch:** `claude/task-92-st2-pure-ports` → `main`  
**Commit:** `d24e6e6`  
**Date:** 2026-05-12

---

## Verdict: CHANGES REQUESTED

The pure-port mechanics are correct — 30 files, valid frontmatter, bodies well under the 5 KB D.6 cap, governance exits 0. Two issues require resolution before merge: a false acceptance-criteria tick that will mislead downstream batch implementers, and a dangling forward reference that creates a broken escalation path for users of `/sc:troubleshoot` today.

---

## What works

### Structure and frontmatter — all 30 files

All 10 folders follow the 3-file pattern established by Task 091 ST-1: `SKILL.md`, `readme.md`, `references/upstream-sc-<slug>.md`. Every `SKILL.md` carries:

- `skill_source: "superclaude@v4.3.0"` (ADR-0011 D.2 ✓)
- `skill_kind`, `skill_target_agents`, `skill_references_skills` (L2 namespace ✓)
- `skill_bootstrap_required: false` — correct for stateless command ports
- `name`+`description` per ontology-required keys ✓

### Body sizes — well under cap

All 10 bodies fall between 1845 B (`sc-design`) and 2169 B (`sc-root-cause-analyst`). The D.6 5 KB cap is not even approached; no overflow extraction to `references/` was required. This matches the triage matrix tier (L1/L2) classification.

### Upstream attribution headers

Every `references/upstream-sc-<slug>.md` opens with the canonical SHA-pinned header:

```
<!-- Mirror of src/superclaude/…/<slug>.md @ 22ad3f48 (v4.3.0). DO NOT EDIT — re-sync via a new Task. -->
```

ADR-0011 D.3 satisfied. ✓

### readme.md scaffold

Each folder's `readme.md` carries `type: index` frontmatter, a "What / Why here" paragraph linking to ADR-0011 and Task 092, a Contents table, and an Assumptions Log with a substantive entry recording the pure-port triage decision. This addresses the blocking Issue 1 from the Phase 1 review (PR #115). ✓

### `skills/readme.md` extension

The new "Imported in Phase 2 batch A" subsection correctly cites ADR-0011 + Task 092 and lists all 10 new skill slugs with one-line descriptions. T092.2.4 satisfied. ✓

### Governance gate

`tools/check-governance.sh` exits 0 across the full repo. `python3 tools/fm/validate.py skills/sc-*/` produces 0 diagnostics across all 24 skill folders (14 Phase 1 + 10 Phase 2 batch A). ✓

### Friction log

`Highest Frustration Level: FL0` — a correct and honest assessment for a mechanical port batch. No self-improvement items requiring Task creation.

---

## Issue 1 (BLOCKING): T092.2.1 incorrectly marked ✅

**Severity:** Blocking — misleads downstream implementers about batch-completion state.

**What the PR body says:**

> - **T092.2.1** — every row with `Vendor=superclaude` AND `Decision=port` AND no MCP has a corresponding `skills/sc-<slug>/SKILL.md`. ✅

**Why this is wrong:**

AC T092.2.1 in `subtasks/02-superclaude-phase-2.md` (anchor `T092.2.1`) reads:

```gherkin
Scenario: Every keep-list row produces a /skills/sc-*/ folder
  Given ST-2 is complete
  When a reader cross-references the triage matrix
  Then every row with Vendor=superclaude AND Decision ∈ {port, adapt}
      MUST have a corresponding skills/sc-<slug>/SKILL.md on the branch
  And every such SKILL.md MUST carry skill_source: "superclaude@v4.3.0"
```

The `Then` clause covers `Decision ∈ {port, **adapt**}` — not just pure-port rows. The triage matrix records **22 adapt rows** still unported (sc-brainstorm, sc-business-panel, sc-build, sc-cleanup, sc-estimate, sc-explain, sc-index, sc-load, sc-reflect, sc-save, sc-spec-panel, sc-task, sc-workflow, sc-socratic-mentor, and the MODE bundles in rows 38–39). Checking this AC off now is factually incorrect and will mislead any agent that reads the PR to determine ST-2's completion state.

Additionally, the PR description silently re-narrows the criterion: it quotes `Decision=port AND no MCP` (a subset), not the spec's `Decision ∈ {port, adapt}`. This looks like an attempt to pass the criterion against a weaker version of it.

**Required repair:**

Replace the ✅ with the accurate partial state:

```markdown
- **T092.2.1** — *partial* — 10 of ~32 keep-list rows ported (pure-port cluster only).
  Adapt rows (22) and MODE-bundle ports (rows 38–39) deferred to batch B per
  ADR-0012 SHOULD-gate. Full criterion not satisfiable until ST-2 batch B lands.
```

---

## Issue 2 (BLOCKING): `sc-troubleshoot` contains a dangling forward reference

**Severity:** Blocking — creates a broken escalation path visible to every user who invokes `/sc:troubleshoot` today.

**Evidence:**

`skills/sc-troubleshoot/SKILL.md` — `## When to use` (line ~22):

```markdown
For deeper root-cause investigation when triage cannot identify the failure in one pass,
escalate to `sc-root-cause-analyst` or to the `superpowers-systematic-debugging`
4-phase methodology (per Task 092 ST-3).
```

`skills/sc-troubleshoot/SKILL.md` — `## How to use` step 4:

```markdown
4. If triage is inconclusive, escalate to `sc-root-cause-analyst` or
   `superpowers-systematic-debugging`.
```

`superpowers-systematic-debugging` does **not exist** — it is a Superpowers corpus row (ST-3 scope, not yet ported). The `skill_references_skills` frontmatter also does **not** list it, so the validator cannot catch this. A user following the escalation path today finds nothing.

**Required repair (two options, pick one):**

Option A — Remove the forward reference entirely until ST-3 lands:

```markdown
## When to use
…escalate to `sc-root-cause-analyst` for evidence-based systematic investigation.

## How to use
4. If triage is inconclusive, escalate to `sc-root-cause-analyst`.
```

Option B — Retain the forward reference but mark it explicitly deferred:

```markdown
## When to use
…escalate to `sc-root-cause-analyst` or, once Task 092 ST-3 lands, to
`superpowers-systematic-debugging` for the 4-phase root-cause methodology.

## How to use
4. If triage is inconclusive, escalate to `sc-root-cause-analyst`
   (or `superpowers-systematic-debugging` after Task 092 ST-3 merges).
```

Option A is recommended: the SKILL.md body should describe current capabilities; forward references to non-existent skills should live in the friction log or task notes, not in a user-facing "How to use" section.

---

## Issue 3 (Advisory): Two MODE `port` rows (38, 39) deferred but not acknowledged

**Severity:** Advisory — no merge blocker, but creates a misleading read of the batch's completeness against the triage matrix.

The triage matrix lists rows 38 and 39 as `port` decisions:

| # | Upstream path | Target | Decision |
|---|---|---|---|
| 38 | `modes/MODE_Introspection.md` | bundle in `sc-reflect` `references/` | port |
| 39 | `modes/MODE_Task_Management.md` | bundle in `sc-task` `references/` | port |

These rows are correctly deferred because their bundle targets (`sc-reflect`, `sc-task`) are `adapt` rows pending the ADR-0012 SHOULD-gate. However the PR body says only "all adapt rows deferred" — a reader who checks the matrix will find two `port` rows not in the batch and incorrectly conclude the triage matrix is wrong.

**Recommended repair:** Add one sentence to the "Out of scope" section:

```markdown
- **MODE port rows (matrix #38, #39)** — MODE_Introspection and MODE_Task_Management are
  `port` decisions that bundle into `sc-reflect` and `sc-task` respectively; since both
  bundle targets are `adapt` rows, they cannot land until batch B.
```

---

## Issue 4 (Advisory, carry-over from PR #115): L1 Vault Core keys absent from SKILL.md files

**Severity:** Advisory — pre-existing gap from Phase 1; not introduced by this PR.

SKILLS.md §3.2 states:

> Every `SKILL.md` MUST carry these six L1 keys: `type`, `status`, `slug`, `summary`, `created`, `updated`.

None of the `sc-*/SKILL.md` files (Phase 1 or Phase 2) carry these keys. The validator passes because the ontology's `skill` type only requires `name` and `description` — creating a discrepancy between the normative spec and the enforcement tooling.

This was noted in the Phase 1 review (PR #115, Observation 1 analogue) and is not regrressed here. It should be resolved in a follow-up T3 Task that either:

- Updates the ontology `skill.required_keys` to include the six L1 keys and adds them to all existing SKILL.md files, **or**
- Updates SKILLS.md §3.2 to explicitly exempt `SKILL.md` from L1 key requirements (with rationale).

A T3 structural change — MUST NOT be resolved in this PR.

---

## Checklist against T092.2.1–T092.2.4 and BR.92.*

| Criterion | Status | Notes |
|---|---|---|
| **T092.2.1** — every keep-list row has `skills/sc-<slug>/SKILL.md` | ⚠️ PARTIAL | 10/32 rows. AC not satisfiable until batch B lands. See Issue 1. |
| **T092.2.2** — D.8 adaptation enforced where flagged | N/A | No adapt rows in this batch. |
| **T092.2.3** — body cap ≤ 5 KB | ✅ | Max 2169 B (`sc-root-cause-analyst`). |
| **T092.2.4** — `skills/readme.md` updated | ✅ | Phase 2 batch A subsection present, citing ADR-0011 + Task 092. |
| **BR.92.1** — triage matrix covers every snapshot artefact | ✅ | ST-1 closed; 81 rows, 0 uncovered. |
| **BR.92.2** — keep-list items validate clean | ✅ | `python3 tools/fm/validate.py skills/sc-*/` → 0 diagnostics. |
| **BR.92.3** — snapshot retired | 🔲 | ST-4 scope. |
| **BR.92.4** — no external GitHub fetch during triage | ✅ | All source citations resolve to local snapshot paths. |

---

## Summary of required actions before merging

| # | Severity | Action | File(s) |
|---|---|---|---|
| 1 | **Blocking** | Fix T092.2.1 ✅ → partial state with accurate row counts | `PR description` (edit) |
| 2 | **Blocking** | Remove or clearly mark deferred the `superpowers-systematic-debugging` forward reference | `skills/sc-troubleshoot/SKILL.md` |
| 3 | Advisory | Add MODE rows 38–39 to PR "Out of scope" explanation | `PR description` (edit) |
| 4 | Advisory | File T3 Task to reconcile L1 key gap between SKILLS.md §3.2 and validator ontology | `tasks/readme.md` + new task |
