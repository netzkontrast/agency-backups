---
type: note
status: active
slug: task-092-st3-pr120-review
summary: "Peer review of PR #120 (Task 092 ST-3 batch B): 9 Superpowers adapt skills. Verdict: APPROVED with 3 advisory items — novel skill_kind vocabulary, incomplete skill_references_skills graph edge, AC anchors not cited by name."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #120 · Task 092 ST-3 batch B: port 8 Superpowers adapt skills + code-reviewer agent

**Reviewer:** claude-sonnet-4-6  
**PR:** [#120](https://github.com/netzkontrast/agency/pull/120)  
**Branch:** `claude/task-92-st3-batch-b` → `main`  
**Commit:** `083c728`  
**Date:** 2026-05-12

---

## Verdict: APPROVED (3 advisory items)

The adapt-port mechanics are correct — all 9 triage-matrix rows 59–67 landed, validator exits 0 across 27 new files, the D.7 strip on `using-superpowers` is well-documented, and no body crosses the 5 KB D.6 cap. Three advisory issues should be addressed in a follow-up commit or filed as maintenance Tasks before ST-4.

---

## What works

### Completeness — T092.3.1 satisfied

All nine `Vendor=superpowers / Decision=adapt` rows (59–67) are present:

| Matrix # | Slug | SKILL.md bytes |
|---|---|---|
| 59 | `superpowers-brainstorming` | 2764 |
| 60 | `superpowers-dispatching-parallel-agents` | 2906 |
| 61 | `superpowers-executing-plans` | 2412 |
| 62 | `superpowers-subagent-driven-development` | 2690 |
| 63 | `superpowers-requesting-code-review` | 2788 |
| 64 | `superpowers-writing-plans` | 2769 |
| 65 | `superpowers-using-superpowers` | 3622 |
| 66 | `superpowers-writing-skills` | 3120 |
| 67 | `superpowers-code-reviewer` | 3248 |

`python3 tools/fm/validate.py` exits 0 across all 27 new files. Every `SKILL.md` carries `skill_source: "superpowers@v4.0.3"`. ✓

### D.7 enforcement — T092.3.2 satisfied

`superpowers-using-superpowers/SKILL.md` carries a canonical `## Adaptations from upstream` section explicitly calling out the SessionStart strip and the Skill-tool replacement. The upstream hook files (rows 71–73) remain `skip`. No `SKILL.md` in this batch instructs a SessionStart-style injection. `grep -r "SessionStart" skills/superpowers-*/SKILL.md` returns only the `using-superpowers` explanatory references — no live injection patterns. ✓

### Body cap — T092.3.3 satisfied

All nine bodies land between 2412 B and 3622 B, well under the ADR-0011 D.6 5 KB cap. The 22 KB `writing-skills` upstream body is correctly extracted to `references/upstream-superpowers-writing-skills.md`; the `SKILL.md` body itself is 3120 B. ✓

### Upstream attribution headers

All nine `references/upstream-superpowers-<slug>.md` files open with the SHA-pinned attribution header pinned at `b9e16498` (Superpowers v4.0.3). ADR-0011 D.3 satisfied. ✓

### Deconfliction notes

- Row 59 (`brainstorming`): "Pairs with `sc-brainstorm` (SuperClaude Socratic discovery)… brainstorming is the upstream step that feeds both." Deconfliction present. ✓
- Row 64 (`writing-plans`): "`sc-workflow` — translates a PRD… `superpowers-writing-plans` lives one layer deeper (structure → granular tasks)." Deconfliction present. ✓

### Cross-batch fixup

`superpowers-receiving-code-review/SKILL.md` now carries `skill_references_skills: [sc-self-review, superpowers-requesting-code-review]` with the restored edge that had been left dangling in PR #119 (commit `37e36aa`). The redundant forward-reference body note is correctly removed. ✓

### ST-3 scope closure

Triage matrix rows 53–67 (port: rows 53–58, adapt: rows 59–67) are all present in `skills/superpowers-*/`. Combined with PR #119's batch A port rows, ST-3 is complete. Rows 68–81 are correctly `skip`. The claim "Closes ST-3 port scope" is accurate. ✓

---

## Advisory A1 — novel `skill_kind: agent-template` not in SKILLS.md spec enumeration

**Severity:** Advisory — spec-vocabulary drift; no validator enforcement gap today, but accumulating silently.

**What happened:**

`superpowers-code-reviewer/SKILL.md` introduces `skill_kind: agent-template`. SKILLS.md §3 defines the closed set as:

> One of: `domain`, `tool`, `orchestrator`, `meta`

Neither `agent-template` nor `discipline` (introduced in PR #119 batch A, e.g. `superpowers-finishing-a-branch`) nor `workflow` (also PR #119) appears in this enumeration. `tools/fm/validate.py` does not enforce the enum — it accepts any string — so governance exits 0, but the spec says one thing and the machine checks another.

**Current landscape of novel values:**

| `skill_kind` | Introduced by | PR |
|---|---|---|
| `analysis` | SC skills (Task 091/092 ST-2) | #117/#118 |
| `persona` | SC skills | #117/#118 |
| `discipline` | Superpowers batch A | #119 |
| `workflow` | Superpowers batch A | #119 |
| `agent-template` | **This PR** | #120 |

**Recommended fix:**

File a T3 structural Task to:
1. Update SKILLS.md §3's `skill_kind` enumeration to ratify all observed values.
2. Add an enum check to `tools/fm/validate.py` so the gap between spec and machine closes.

This should be done before ST-4 or any further skill imports to stop the vocabulary from drifting further.

---

## Advisory A2 — `superpowers-using-superpowers` `skill_references_skills` is incomplete

**Severity:** Advisory — frontmatter graph edge missing; affects linker reciprocity computation.

**What happened:**

`superpowers-using-superpowers/SKILL.md` frontmatter declares:

```yaml
skill_references_skills: [superpowers-tdd, superpowers-systematic-debugging, superpowers-verification-before-completion]
```

But the `## How to use` dispatch table lists **eight** skills as things to "fire":

| Table row | In `skill_references_skills`? |
|---|---|
| `superpowers-tdd` | ✓ |
| `superpowers-systematic-debugging` | ✓ |
| `superpowers-verification-before-completion` | ✓ |
| `superpowers-receiving-code-review` | ✗ MISSING |
| `superpowers-finishing-a-branch` | ✗ MISSING |
| `superpowers-executing-plans` | ✗ MISSING |
| `superpowers-writing-plans` | ✗ MISSING |
| `superpowers-dispatching-parallel-agents` | ✗ MISSING |

Five invocation edges are absent from the frontmatter. Per SKILLS.md §4.X: "Reciprocity is computed by the linter." These missing edges mean any graph traversal starting from the five target skills will not find `superpowers-using-superpowers` as an inbound reference.

**Recommended fix (T2 additive repair — can be done in-place via `tools/fm/edit.py`):**

```bash
python3 tools/fm/edit.py skills/superpowers-using-superpowers/SKILL.md \
  --append-list skill_references_skills superpowers-receiving-code-review \
  --append-list skill_references_skills superpowers-finishing-a-branch \
  --append-list skill_references_skills superpowers-executing-plans \
  --append-list skill_references_skills superpowers-writing-plans \
  --append-list skill_references_skills superpowers-dispatching-parallel-agents
```

---

## Advisory A3 — PR body does not cite T092.3.x Gherkin anchors

**Severity:** Advisory — auditability gap; the substance is correct, the traceability is not.

**What happened:**

The subtask spec `subtasks/03-superpowers-port.md` defines three Gherkin acceptance anchors:
- `# anchor: T092.3.1` — vendor prefix + validator pass
- `# anchor: T092.3.2` — D.7 SessionStart enforcement
- `# anchor: T092.3.3` — body cap holds

The PR body's "Acceptance criteria" section lists the items as informal bullets without citing these anchors. The mapping is inferrable but not explicit. This was flagged as a blocking issue in the PR #117 review (where the substance was also wrong); here the substance is correct, so it's advisory. Citing anchors by name makes downstream batch-tracking and future Epic audits unambiguous.

**Recommended practice for ST-4 and future PRs:**

> - **T092.3.1** — every `Vendor=superpowers / Decision=adapt` row has a SKILL.md + `skill_source: "superpowers@v4.0.3"`. ✅  
> - **T092.3.2** — no SessionStart injection in any SKILL.md; row 65 D.7 strip documented. ✅  
> - **T092.3.3** — `python3 tools/fm/validate.py --check-body skills/superpowers-*/` exits 0. ✅

---

## Summary table

| Issue | Severity | Action |
|---|---|---|
| `skill_kind: agent-template` outside spec enumeration | Advisory A1 | File T3 Task: ratify enum + add validator check |
| 5 missing `skill_references_skills` edges in `superpowers-using-superpowers` | Advisory A2 | T2 in-place repair via `tools/fm/edit.py` |
| AC anchors T092.3.x not cited in PR body | Advisory A3 | Pattern fix for ST-4 PR body |

No blocking issues. ST-3 is complete; ST-4 (snapshot cleanup, deadline 2026-08-12) may proceed.
