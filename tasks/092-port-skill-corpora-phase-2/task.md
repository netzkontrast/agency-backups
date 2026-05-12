---
type: task
status: active
slug: port-skill-corpora-phase-2
summary: "Epic: Complete the upstream skill-corpora port. Triage the Phase-2 candidates in tasks/091-…/references/upstream-snapshot/ (SuperClaude_Framework v4.3.0 + Superpowers v4.0.3), port the keep-list under skills/sc-*/ and skills/superpowers-*/ per ADR-0011, then retire the snapshot + waivers."
created: 2026-05-12
updated: 2026-05-12
task_id: "092"
task_status: done
task_owner: "claude"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - skills/sc-*/
  - skills/superpowers-*/
  - skills/readme.md
  - tasks/091-port-external-skill-corpora/references/upstream-snapshot/
  - tools/.frontmatter-waivers
  - tools/.script-allowlist
task_blocked_by:
  - 091
---

# Task 092 — Port Skill Corpora (Phase 2 / Epic)

## Note — Internal research only

**This Task MUST source its research from the local snapshot at [`tasks/091-port-external-skill-corpora/references/upstream-snapshot/`](../091-port-external-skill-corpora/references/upstream-snapshot/), NOT from external GitHub URLs.** The snapshot is byte-pinned at SuperClaude_Framework `22ad3f48` (v4.3.0) and Superpowers `b9e16498` (v4.0.3); external sources may drift.

When delegating research, use the local-only modes of the project's analysis skills:

- **[`/sc:research`](../../skills/sc-research/SKILL.md)** — Agency-adapted per ADR-0011 D.8 (WebSearch + WebFetch primary, Tavily OPTIONAL). For Phase 2 triage, override the primary surface: pass the snapshot path as the target (`/sc:research --target tasks/091-…/references/upstream-snapshot/`) so WebSearch / WebFetch are not invoked and the skill operates over the local mirror only. Output lands at `/research/<slug>/output/SPEC.md` per RESEARCH.md §6.5.
- **[`/sc:analyze`](../../skills/sc-implement/SKILL.md)** — point its `target` at a snapshot subtree (e.g. `tasks/091-…/references/upstream-snapshot/superpowers/skills/`). It will perform domain analysis (quality / security / performance / architecture) without network egress.

Whenever a subtask cites "research", read this as "local-snapshot research". External fetches are an anti-pattern for this Epic — they introduce SHA drift, network dependency, and unreproducible results.

## Goal

Complete the upstream skill-corpora port operationalised by [ADR-0011 — External Skill Corpora Import Policy](../../decisions/0011-external-skill-corpora-import.md). Phase 1 (closed by Task 091 ST-1) ported 14 specific skills resolving the dangling `/sc:*` references in `CLAUDE.md §13`. Phase 2 covers the **remaining** upstream content:

- **SuperClaude_Framework v4.3.0** — 26 unported commands + 11 unported agents + 5 unbundled modes + the upstream `confidence-check` skill.
- **Superpowers v4.0.3** — entire corpus (14 skills + 3 commands + 1 agent + supporting hooks/lib/docs/.claude-plugin), staged under a new `skills/superpowers-*/` namespace per ADR-0011 D.1.

The Epic is **done** when:

1. Every snapshot artefact under [`tasks/091-…/references/upstream-snapshot/`](../091-port-external-skill-corpora/references/upstream-snapshot/) has a recorded triage decision (port / adapt / skip).
2. Every "port" or "adapt" decision has produced a corresponding `skills/<vendor>-<slug>/` folder that passes governance.
3. The snapshot directory and its two waivers ([`tools/.frontmatter-waivers`](../../tools/.frontmatter-waivers) + [`tools/.script-allowlist`](../../tools/.script-allowlist)) are deleted in a final cleanup commit, before the snapshot's 2026-08-12 expiry.

## Context

- Phase 1 (Task 091 ST-1, [PR #115](https://github.com/netzkontrast/agency/pull/115)) extended `tools/fm/validate.py` for the `skill_source` L2 key (diagnostics `F.B.8` / `F.B.9`) and shipped 14 `skills/sc-*/` folders. The validator extension is forward-compatible with `superpowers-` prefix (test `test_superpowers_vendor_prefix_accepted` is green).
- Phase 1 ST-2 (`AGENTS.md` + `RESEARCH.md` hookup) is a sibling Task to file when Phase 1 ST-1 merges; it is NOT blocking this Epic.
- The full upstream working trees are staged at [`tasks/091-…/references/upstream-snapshot/`](../091-port-external-skill-corpora/references/upstream-snapshot/) — 515 files, ~4.7 MB, with governance carve-outs that expire **2026-08-12**. The expiry is the natural hard deadline for this Epic.
- ADR-0011 D.8 (MCP-free adaptation) and D.6 (≤ 5 KB body cap) apply to every Phase 2 port. Per ADR-0011 D.9, re-syncs from a newer upstream release are out of scope and require a new Task.
- A blocker resolution is open per [Task 091 friction-log FL1.1](../091-port-external-skill-corpora/friction-log.md) — ST-2 reviewer to file `decisions/0012-skill-source-validator-diagnostic-codes.md` reconciling the `F.B.7` → `F.B.8`/`F.B.9` renumber. **This Epic SHOULD wait for that ADR to be Accepted** before mass-porting, otherwise every new SKILL.md citation propagates the F.B.7 ambiguity.

## Plan (four sequential subtasks)

1. **[ST-1 — Triage](./subtasks/01-triage.md):** read every snapshot artefact via `/sc:research` and `/sc:analyze` *(local-only — see Note above)*; produce a decision matrix (port / adapt / skip with rationale) at `references/triage-matrix.md`. Output is read-only; no `/skills/` writes.
2. **[ST-2 — SuperClaude Phase 2 batch](./subtasks/02-superclaude-phase-2.md):** port every `superclaude` keep-list item from the ST-1 matrix into `skills/sc-<slug>/`. Bundles the 5 remaining MODE files into the relevant skills' `references/`. Body adaptation (D.8) for any skill that binds to a non-Agency MCP.
3. **[ST-3 — Superpowers full corpus](./subtasks/03-superpowers-port.md):** port every `superpowers` keep-list item into `skills/superpowers-<slug>/`. Bundles upstream hooks/lib only when their behaviour passes the SS.1–SS.3 SessionStart-no-injection rule (ADR-0011 D.7).
4. **[ST-4 — Snapshot cleanup](./subtasks/04-cleanup.md):** delete the snapshot directory, remove the two waivers, update `skills/readme.md`. Final governance run.

ST-1 → ST-2 → ST-3 → ST-4 is strictly sequential: each subtask depends on its predecessor being closed `done`. ST-2 and ST-3 MAY proceed in parallel only if the triage matrix explicitly partitions their work non-overlappingly.

## Todo

- [ ] 1. ST-1 triage matrix authored, reviewed, and closed `done`
- [ ] 2. ADR amendment (0012-skill-source-validator-diagnostic-codes) Accepted on `main` (carry-over from Task 091 FL1.1)
- [ ] 3. ST-2 SuperClaude Phase 2 batch ported and PR'd
- [ ] 4. ST-3 Superpowers corpus ported and PR'd
- [ ] 5. ST-4 snapshot deleted; waivers removed; `skills/readme.md` updated
- [ ] 6. End-to-end governance: `tools/check-governance.sh` exits 0; no expired waivers
- [ ] 7. `tasks/readme.md` index entry flipped `Status: open` → `done`
- [ ] 8. Friction log authored (`friction-log.md` with `Highest Frustration Level: FL[0-3]`)

## Acceptance Criteria

Gherkin scenarios (anchored for downstream tooling). Per-subtask AC live inside each subtask file.

```gherkin
Feature: Phase 2 skill-corpora port closes the snapshot

  # anchor: BR.92.1
  Scenario: Triage matrix covers every snapshot artefact
    Given Task 092 ST-1 is complete
    When a reader greps the triage matrix for upstream filenames
    Then every *.md file under tasks/091-…/references/upstream-snapshot/ MUST have a row
    And each row MUST carry one of decisions ∈ {port, adapt, skip}
    And each "adapt" row MUST cite the ADR-0011 D.* clause that justifies the adaptation

  # anchor: BR.92.2
  Scenario: Keep-list items are ported and validate clean
    Given ST-2 and ST-3 are complete
    When `python3 tools/fm/validate.py skills/` runs
    Then exit code MUST be 0
    And every skills/sc-*/SKILL.md and skills/superpowers-*/SKILL.md MUST carry
        skill_source: "<vendor>@v<semver>"
    And every imported SKILL.md body MUST be ≤ 5 KB (ADR-0011 D.6)

  # anchor: BR.92.3
  Scenario: Snapshot is retired
    Given ST-4 is complete
    When a reader runs `find tasks/091-…/references/upstream-snapshot/ -type f`
    Then the result MUST be empty (directory deleted)
    And tools/.frontmatter-waivers MUST NOT contain the upstream-snapshot glob
    And tools/.script-allowlist MUST NOT contain the upstream-snapshot glob

  # anchor: BR.92.4
  Scenario: No external GitHub fetch occurred during triage
    Given Task 092 ST-1 produced the triage matrix
    When a reader inspects the matrix's source-citations
    Then every citation MUST resolve to a file path under
        tasks/091-…/references/upstream-snapshot/
    And NO citation MAY resolve to a `https://github.com/.../blob/` URL
```

## Out of scope

- Auto-pull / re-sync from a newer upstream release — explicitly future-ADR territory per ADR-0011 D.9.
- Phase 1 ST-2 (`AGENTS.md` + `RESEARCH.md` hookup) — sibling Task; this Epic depends on Phase 1 ST-1 but not on ST-2.
- MCP installer packaging — Agency does not ship installers (per ADR-0011 §10.8 out-of-scope clause).
- Porting `confidence-check` (the upstream-bundled skill at `src/superclaude/skills/confidence-check/`) is **explicitly in-scope for ST-2** but flagged as a careful case: ADR-0011 D.7 prohibits SessionStart injection, and this skill's upstream packaging may include a SessionStart hook. Triage MUST classify it as `adapt` rather than verbatim `port`.

## Links

- Parent Epic: [Task 091 — Port External Skill Corpora (Phase 1)](../091-port-external-skill-corpora/task.md) — `task_status: open` (ST-1 in PR review)
- Source ADR: [ADR-0011](../../decisions/0011-external-skill-corpora-import.md) (`adr_status: Accepted` 2026-05-12)
- Blocker remediation: [Task 091 friction-log FL1.1](../091-port-external-skill-corpora/friction-log.md) — pending new ADR `0012-skill-source-validator-diagnostic-codes.md`
- Snapshot: [`tasks/091-…/references/upstream-snapshot/readme.md`](../091-port-external-skill-corpora/references/upstream-snapshot/readme.md)
- Sibling ADRs cited: [ADR-0003](../../decisions/0003-frontmatter-source-of-truth.md), [ADR-0006](../../decisions/0006-agency-system-prototype-exemption.md), [ADR-0007](../../decisions/0007-skill-bundles-tools-frontmatter.md)
- Governing root specs: [TASK.md](../../TASK.md), [SKILLS.md](../../SKILLS.md), [RESEARCH.md](../../RESEARCH.md), [AGENTS.md](../../AGENTS.md)
