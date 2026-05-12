---
type: note
status: active
slug: task-092-st4-pr121-review
summary: "Peer review of PR #121 (Task 092 ST-4): snapshot retirement + waiver cleanup + Epic closure. Verdict: APPROVED with 1 blocking + 2 advisory items — unchecked Todo boxes while task_status:done (blocking), subtask note statuses not updated (advisory), stale snapshot path in tasks/readme.md (advisory)."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #121 · Task 092 ST-4: retire upstream snapshot + waivers; flip Epic to done

**Reviewer:** claude-sonnet-4-6  
**PR:** [#121](https://github.com/netzkontrast/agency/pull/121)  
**Branch:** `claude/task-92-st4-snapshot-cleanup` → `main`  
**Commit:** `d1995f9`  
**Date:** 2026-05-12

---

## Verdict: APPROVED WITH 1 BLOCKING + 2 ADVISORY ITEMS

The core ST-4 mechanics are sound — all four Gherkin acceptance criteria
(T092.4.1–T092.4.4) are satisfied and verifiable. The snapshot is gone,
waivers are stripped, governance exits 0, and the audit trail is complete.
One blocking defect prevents clean merge: the `task.md` Todo section is entirely
unchecked despite every item being verifiably complete. Two advisory gaps
should be addressed or explicitly waived before this becomes a maintenance
hazard.

---

## What works

### T092.4.1 — Snapshot directory deleted ✓

`tasks/091-port-external-skill-corpora/references/upstream-snapshot/` no longer
exists. Commit removes 516 files (~4.7 MB) — the verbatim SuperClaude_Framework
v4.3.0 + Superpowers v4.0.3 corpora. The snapshot's governance purpose is
exhausted; its deletion is correct and timely (3 months ahead of the 2026-08-12
waiver expiry).

The permanent audit trail (triage matrix + 21 triage notes + 5 review files)
remains intact under `tasks/092-port-skill-corpora-phase-2/references/`.

### T092.4.2 — Waivers stripped ✓

Both governance carve-outs are cleanly removed:

- `tools/.frontmatter-waivers`: the `tasks/091-…/references/upstream-snapshot/*`
  row (the only time-bound waiver in the ledger) is gone.
- `tools/.script-allowlist`: the upstream-snapshot glob and its preceding
  comment block are gone.

`grep upstream-snapshot tools/.frontmatter-waivers tools/.script-allowlist`
returns exit code 1 (zero matches). Spec-language: MUST satisfied.

### T092.4.3 — No expired waivers ✓

The removed row was the only row with a non-`-` expiry date. The post-ST-4
ledger is empty of rows, meaning no future expiry-check can fire.

### T092.4.4 — Governance green ✓

Independently confirmed: `tools/check-governance.sh` exits 0 on the
post-cleanup tree (also verified at session start above). The validator runs
cleanly across 75 `SKILL.md` files (`python3 tools/fm/validate.py skills/`
emits 0 ERROR diagnostics). `PC.1.1` clean-working-directory check passes.

### Friction log + Epic closure ✓

`friction-log.md` carries `Highest Frustration Level: FL1` on the opening
line (FR.B.4 compliant). The Epic-level summary table is complete. The
recommended follow-up Tasks are clearly called out:

- T3 — ratify expanded `skill_kind` enumeration in SKILLS.md §3
- T1 — fix `superclaude_framework@v4.3.0` → `superclaude@v4.3.0` typos in
  triage notes

### ADR-0012 — Accepted ✓

`decisions/0012-skill-source-validator-diagnostic-codes.md` carries
`adr_status: Accepted`. Todo item #2 ("ADR amendment Accepted on `main`") is
satisfied. The blocker from Task 091 FL1.1 is resolved.

### Epic output verified ✓

The 75 `skills/` folders span the full Epic:

| PR | Subtask | Deliverable |
|----|---------|-------------|
| #116 | ST-1 | 81-row triage matrix + 21 notes |
| #117 | ST-2 A | 10 `sc-*` pure-port skills |
| #118 | ST-2 B | 15 `sc-*` adapt skills + 2 mode bundles |
| #119 | ST-3 A | 6 `superpowers-*` discipline-gate skills |
| #120 | ST-3 B | 9 `superpowers-*` adapt/agent skills |
| #121 | ST-4 | snapshot retired + waivers stripped |

`python3 tools/fm/validate.py skills/` exits 0 across all 75 SKILL.md files. ✓

---

## Blocking B1 — Todo checkboxes all `- [ ]` while `task_status: done`

**Severity: BLOCKING** — factual inconsistency; a `task_status: done` Epic whose
own Todo section reports zero completed items misleads future readers and any
tooling that parses Todo state.

**What happened:**

`tasks/092-port-skill-corpora-phase-2/task.md` lines 71–78 still read:

```markdown
- [ ] 1. ST-1 triage matrix authored, reviewed, and closed `done`
- [ ] 2. ADR amendment (0012-skill-source-validator-diagnostic-codes) Accepted on `main`
- [ ] 3. ST-2 SuperClaude Phase 2 batch ported and PR'd
- [ ] 4. ST-3 Superpowers corpus ported and PR'd
- [ ] 5. ST-4 snapshot deleted; waivers removed; `skills/readme.md` updated
- [ ] 6. End-to-end governance: `tools/check-governance.sh` exits 0; no expired waivers
- [ ] 7. `tasks/readme.md` index entry flipped `Status: open` → `done`
- [ ] 8. Friction log authored (`friction-log.md` with `Highest Frustration Level: FL[0-3]`)
```

All eight items are verifiably complete by this commit:
- Items 1, 3, 4 — evidence: PRs #116, #118, #120.
- Item 2 — `decisions/0012-skill-source-validator-diagnostic-codes.md` shows
  `adr_status: Accepted`.
- Item 5 — `find tasks/091-…/references/upstream-snapshot/ -type f` → 0;
  `skills/readme.md` updated: 2026-05-12.
- Item 6 — `tools/check-governance.sh` exits 0 (T092.4.4 above).
- Item 7 — `tasks/readme.md` entry now reads `Status: done`.
- Item 8 — `friction-log.md` opens with `Highest Frustration Level: FL1`.

**Required fix (T1 mechanical — in-place):**

Change all eight `- [ ]` to `- [x]` in `task.md` before merge. This is a
cosmetic-but-normative correction; the `task_status: done` frontmatter already
reflects truth, but the body must not contradict it.

```bash
# Manual edit via Edit tool — sed-style substitution not recommended per CLAUDE.md §4
# Open tasks/092-port-skill-corpora-phase-2/task.md, lines 71-78
# Replace every `- [ ]` with `- [x]`
```

---

## Advisory A1 — Subtask note files retain `status: active`

**Severity: Advisory** — spec-vocabulary gap; no validator enforcement today.

All four subtask files (`01-triage.md`, `02-superclaude-phase-2.md`,
`03-superpowers-port.md`, `04-cleanup.md`) carry `status: active` in
frontmatter even though all subtasks are closed. These are `type: note` files,
not `type: task`, and CLAUDE.md §4 does not define a terminal status for `note`
artefacts. However, `active` connotes "work in progress" to readers; at minimum
`04-cleanup.md` should be updated to a terminal value (e.g. `status: done`) to
signal that this subtask's scope is exhausted.

The repair tier is T1 (mechanical — derivable state, no structural change).

**Recommended fix:**

```bash
python3 tools/fm/edit.py tasks/092-port-skill-corpora-phase-2/subtasks/04-cleanup.md \
  --set status done
# Optionally update 01-, 02-, 03- as well for consistency
```

If the CLAUDE.md §4 `status` vocabulary for `type: note` is intentionally
undefined (i.e. `active` is permanently the only valid value for notes), this
advisory can be waived with a one-line comment in the friction log.

---

## Advisory A2 — `tasks/readme.md` entry references a now-deleted path

**Severity: Advisory** — stale relative link; any Markdown renderer (GitHub
included) will show a 404 for the snapshot path.

**What happened:**

The `tasks/readme.md` index entry for Task 092 retains the description phrase:

> "…staged at [`tasks/091-…/references/upstream-snapshot/`](./091-port-external-skill-corpora/references/upstream-snapshot/)…"

This is a Markdown relative link to a directory that was deleted in this very
commit. The commit message and friction log note that "historical references
to the deleted snapshot path are intentional" — and the prose context is
indeed correct (the snapshot *was* there). The issue is that the text wraps the
path in a clickable Markdown link, which now resolves to a 404.

**Recommended fix (T1 mechanical):**

Remove the link markup (`[…](./…)`) but keep the descriptive prose as
plain text, e.g.:

```markdown
…staged at `tasks/091-…/references/upstream-snapshot/` (now retired)…
```

This preserves the historical context the commit message justifies while
stopping the renderer from presenting a broken anchor.

---

## Summary table

| ID | Severity | Issue | Action |
|----|----------|-------|--------|
| B1 | **Blocking** | All 8 Todo items unchecked while `task_status: done` | Fix `- [ ]` → `- [x]` in task.md lines 71–78 before merge |
| A1 | Advisory | Subtask note files still `status: active` | T1 repair via `tools/fm/edit.py` (or waive with note) |
| A2 | Advisory | tasks/readme.md Markdown link to deleted snapshot path | Strip link markup; keep prose as plain text |

**Merge gate:** resolve B1 in a follow-up commit on this branch before
merge. A1 and A2 MAY be addressed in the same commit or filed as T1
maintenance Tasks for the Nightly Run.
