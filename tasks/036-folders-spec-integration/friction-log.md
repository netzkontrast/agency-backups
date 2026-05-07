---
type: note
status: completed
slug: task-036-friction-log
summary: "FL1 — Task 036 closure friction log. Three subtasks landed cleanly; the only friction was an 18-readme T1 slug-repair burst surfaced when the new ERROR-tier F.5 linter first scanned the corpus."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log — Task 036 FOLDERS.md Spec Integration

Highest Frustration Level: FL1

## What was done in one session

- ST-1 `tools/check-readme-frontmatter.py` (~190 LOC) + 12 unit tests — promotes FOLDERS.md F.5 from SHOULD to mechanically-enforced MUST. ERROR-tier `[2b/6]` of `tools/check-governance.sh`. Honours provider research and `/decisions/` exemptions per F.1.1 / §8.
- ST-2 `tools/check-audit-graph-consistency.py` (~210 LOC) + 8 unit tests — closes the F.6 dual-surface drift gap. WARN-tier `[opt]` (343 historical drift findings surfaced for a follow-up triage Task; never gating); strict gate available via `FM_AUDIT_GRAPH_STRICT=1`.
- ST-3 FOLDERS.md amendments: §F.1.1 exemption clause enumerating both `/research/<provider>/<slug>/` and `/decisions/`; §F.5 promoted to MUST with the slug-containment convention documented and linter-cited; §F.6 dual-surface drift clause with WARN-tier behaviour spelled out; new §6.1 carries five Gherkin scenarios anchored F.B.1–F.B.5 (readme presence, slug naming, prompt scaffold, audit-graph dual-surface, ADR exemption).
- 18 task-folder readmes had non-conforming slugs (`task-NNN-folder` / `task-NNN-readme`). Repaired in-place via `tools/fm/edit.py --set` per MAINTENANCE.md §1 T1 ("derivable slug" mechanical repair).
- Linter table refreshed in `README.md §6` with rows for both new linters.

## Why FL1 (not FL0, not FL2)

- **Why not FL0**: the 18-readme slug-repair burst was unplanned. The first scan with the new ERROR-tier linter surfaced 100 SLUG-MISMATCH diagnostics; investigation showed the actual repo convention (vault-uniqueness via `task-<NNN>-<slug>` qualification) was stricter than my initial exact-match implementation, so I relaxed to substring-containment AND repaired 18 outliers that used `task-NNN-folder` / `task-NNN-readme`. Both moves were correct but each forced a small detour.
- **Why not FL2**: the plan from `task.md` Phase 1/2 survived intact. No subtasks were merged or split. No falsification clauses fired. The slug-mismatch burst resolved in two iterations: relax linter to actual convention, repair the eighteen outliers.

## Drift findings booked for follow-up

- **F.6 audit-graph drift backlog** (343 WARN). The new advisory linter surfaces every body-link-without-frontmatter pair across the corpus. Resolving these is body-of-work for a future triage Task; the WARN-tier integration ensures the count cannot grow silently without a future maintainer noticing.
- **`pip install` SuperClaude noise**: `./install.sh` pulled in `SuperClaude-4.3.0` plugins via the system `pytest` configuration that print test-collection banners. Cosmetic only; not a Task 036 concern.

## Outputs

- `tools/check-readme-frontmatter.py` (ERROR-tier; promoted F.5 to MUST).
- `tools/check-audit-graph-consistency.py` (WARN-tier; F.6 drift detector).
- `tools/tests/test_readme_frontmatter.py` (12 tests).
- `tools/tests/test_audit_graph_consistency.py` (8 tests).
- `FOLDERS.md` updated (§F.1.1, §F.5, §F.6 + new §6.1 Gherkin block).
- `tools/check-governance.sh` extended with steps `[2b/6]` ERROR + `[opt]` WARN.
- `README.md` §6 linter table extended (two rows).
- `tasks/036-folders-spec-integration/readme.md` slug repaired as part of the 18-readme T1 fix.

## Links

- Parent task: [`task.md`](./task.md)
- Subtasks: [`subtasks/readme.md`](./subtasks/readme.md)
- Spec amended: [`FOLDERS.md`](../../FOLDERS.md)
- Governing specs: [`MAINTENANCE.md` §1](../../MAINTENANCE.md), [`FRUSTRATED.md`](../../FRUSTRATED.md)
