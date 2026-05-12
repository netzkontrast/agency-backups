---
type: note
status: active
slug: pr-119-review-st3-batch-a
summary: "Peer review of PR #119 (Task 092 ST-3 batch A): 1 blocking + 3 advisory issues identified. D.7 compliance verified; governance exits 0; body cap holds."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #119: Task 092 ST-3 batch A (6 Superpowers discipline-gate skills)

Reviewed by: @claude (claude-sonnet-4-6), 2026-05-12.
PR branch: `claude/task-92-st3-superpowers-batch-a` → `main`.
Commit reviewed: `88079f560ac69816349aed94d8b3cd36d53559e0`.

---

## Verdict

**BLOCKING: 1 item.** Advisory: 3 items. The port quality is high and governance is clean. One required PR-body clause (D.7 special-case traceability) is absent; see below.

---

## What was verified

| Check | Result |
|---|---|
| `tools/fm/validate.py skills/superpowers-*/SKILL.md` | ✅ 0 diagnostics (6 files) |
| `tools/fm/validate.py --check-body skills/superpowers-*/SKILL.md` | ✅ 0 diagnostics |
| `tools/check-governance.sh` (full repo) | ✅ PASS |
| SKILL.md body sizes (D.6 ≤ 5 KB) | ✅ max 2556 B — well under cap |
| D.7: no SessionStart injection in any SKILL.md | ✅ confirmed |
| SHA-pinned attribution headers in all `references/upstream-*.md` | ✅ confirmed |
| Three-file structure per skill (SKILL.md + readme.md + references/) | ✅ confirmed |
| `skills/readme.md` updated with new Superpowers section | ✅ confirmed |
| `skill_source: "superpowers@v4.0.3"` present in all SKILL.md | ✅ confirmed |

---

## BLOCKING — B1: PR body omits required D.7 special-case triage callouts

**Spec reference:** [`tasks/092-port-skill-corpora-phase-2/subtasks/03-superpowers-port.md`](./03-superpowers-port.md) (closing sentence):

> "PR body MUST cite the special-case triage outcomes (using-superpowers, session-start.sh, pre-tool-use.sh) so the reviewer can verify D.7 enforcement."

The PR body says "No MCP bindings, no SessionStart-injection. Mechanical ports." — correct as a summary, but it does **not** list the three flagged artifacts and their triage dispositions by name. A reviewer auditing D.7 compliance cannot confirm the outcomes without cross-referencing the full triage matrix.

**Required addition to PR body** (example):

```
### D.7 special-case triage outcomes

| Artifact | Triage decision | Rationale |
|---|---|---|
| `superpowers/skills/using-superpowers/SKILL.md` | adapt (batch B) | Row 65 — meta-skill; upstream SessionStart injection removed; ported without injection |
| `superpowers/hooks/session-start.sh` | skip | Row 72 — D.7 prohibits |
| `superpowers/hooks/hooks.json` | skip | Row 71 — D.7 prohibits |
| `superpowers/hooks/run-hook.cmd` | skip | Row 73 — mooted by D.7 |
| `superpowers/hooks/pre-tool-use.sh` | skip | Row 71 note — classified as global gate; D.7 scope |
```

This information exists in the triage matrix (rows 65, 71–73) but must appear in the PR body per the subtask spec so the CI reviewer — or future repo archaeologist — can confirm D.7 compliance at the PR layer without loading the matrix.

---

## Advisory — A1: Dangling `skill_references_skills` cross-reference

`skills/superpowers-receiving-code-review/SKILL.md` carries:

```yaml
skill_references_skills: [superpowers-requesting-code-review, sc-self-review]
```

`superpowers-requesting-code-review` is an `adapt` row (triage matrix row 63, batch B) and **does not yet exist** under `skills/`. The current validator (`tools/fm/validate.py`) does not resolve cross-references, so this passes governance, but the reference is semantically broken until batch B ships.

**Recommendation:** Either remove `superpowers-requesting-code-review` from `skill_references_skills` for now (add it back when batch B lands), or add an inline comment in the body noting the forward reference. The triage-notes document already records the audit-graph edge, so the information is not lost.

---

## Advisory — A2: Triage adaptation plan not executed for large-body skills

The triage-notes file ([`references/triage-notes/superpowers-discipline-cluster.md`](./triage-notes/superpowers-discipline-cluster.md)) specifies structured phase extractions for three skills that exceed 6 KB upstream:

| Skill | Upstream KB | Planned extraction |
|---|---|---|
| `superpowers-systematic-debugging` | 9.9 | phases 1–4 → `references/phase-{1..4}.md` |
| `superpowers-tdd` | 9.9 | RED/GREEN/REFACTOR → `references/{red,green,refactor}.md` |
| `superpowers-receiving-code-review` | 6.3 | heuristics → `references/heuristics.md` |

What shipped: single verbatim upstream files (`references/upstream-superpowers-*.md`) for all three. The D.6 cap is satisfied (SKILL.md bodies ≤ 2.6 KB), so this does not block merging. But the planned structured navigation (per-phase reference files) is absent, making the large upstream mirrors less approachable. The triage plan should either be retroactively updated or the phase files added in batch B follow-up.

---

## Advisory — A3: Display-text inconsistency in triage-notes links

Two SKILL.md files (`superpowers-systematic-debugging`, `superpowers-tdd`) have a display-text mismatch in their triage-notes links:

```markdown
<!-- incorrect display text (missing references/) -->
[`tasks/092-…/triage-notes/superpowers-discipline-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-discipline-cluster.md)
```

The link target is correct; only the display text is wrong (omits `references/`). `superpowers-verification-before-completion` has the correct form. T1 mechanical repair — can be done post-merge without blocking.

---

## Summary table

| ID | Severity | Item | Actionable now? |
|---|---|---|---|
| B1 | **Blocking** | PR body missing D.7 special-case triage callouts (subtask spec MUST) | Add to PR body before merge |
| A1 | Advisory | Dangling `skill_references_skills: [superpowers-requesting-code-review]` | Remove for now or annotate; fix at batch B |
| A2 | Advisory | Triage plan phase-extraction not executed; verbatim upstream used | File as batch B follow-up note |
| A3 | Advisory | Display-text inconsistency in triage-notes Markdown links | T1 repair post-merge |

@jules — bitte sieh dir insbesondere **B1** an: der Subtask-Spec schreibt ein `MUST` vor, das die PR-Beschreibung die drei D.7-Sonderfälle namentlich nennt. Das fehlt aktuell. Die übrigen Punkte sind advisory und blockieren den Merge nicht.
