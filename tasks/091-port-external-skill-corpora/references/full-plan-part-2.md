## 4. Porting policy (becomes ADR-0011)

The port introduces a new architectural concept: **external skill corpora imported under a vendor-prefixed namespace**. Per Agency's MADR 4.0.0 governance (`decisions/readme.md`), this MUST land as an ADR before any porting Task files.

### 4.1 Decision (proposed `decisions/0011-external-skill-corpora-import.md`)

```yaml
---
type: adr
status: proposed
slug: external-skill-corpora-import
summary: "Policy for importing external skill corpora (SuperClaude_Framework, Superpowers) into /skills/ under vendor-prefixed namespaces."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0011
adr_status: Proposed
adr_supersedes: []
adr_superseded_by: []
adr_relates_to: [ADR-0006, ADR-0007]
---
```

**Context** — `AGENTS.md` and `CLAUDE.md §13` already cite `/sc:createPR` and other `/sc:*` skills as canonical, but only 22 skills exist locally and none of them are the `/sc:*` set. The references dangle. Two upstream corpora (SuperClaude_Framework v4.3.0, Superpowers v4.0.3) ship the missing skills under their own naming conventions. We need a policy for how to mirror them.

**Decision** —

1. **Namespace prefixing.** External skills land at `skills/<vendor>-<bare-slug>/` (e.g. `skills/sc-implement/`, `skills/superpowers-test-driven-development/`). Bare slugs (no prefix) are reserved for Agency-native skills.
2. **Vendor pin.** A new L2 frontmatter key `skill_source` MUST be set on every imported SKILL.md: `skill_source: "superclaude@v4.3.0"` or `skill_source: "superpowers@v4.0.3"`. This is additive frontmatter; no L1 change.
3. **Attribution.** Every imported SKILL.md MUST include a `## References` line citing the upstream file URL pinned to the source SHA per `AGENTS.md "Citation Reproducibility Protocol"` (`path/to/file.ext:Lstart-Lend@<sha>`).
4. **Agent-as-skill normalization.** SuperClaude agents are `.md` files with their own frontmatter — port them as `skill_kind: domain` skills (single agent persona = single skill), or `skill_kind: orchestrator` when an agent coordinates other agents (`pm-agent`, `business-panel-experts`).
5. **Modes as references.** SuperClaude `MODE_*.md` files MUST be bundled inside the relevant skill's `references/` directory, not as standalone skills, because they are behavioral framing, not standalone capabilities (SKILLS.md §7.3 T3).
6. **T2 size cap.** Every imported SKILL.md body MUST be ≤ 5 KB per SKILLS.md §7.3. Excess prose moves into `references/`. The 22.5 KB `superpowers:writing-skills` SKILL.md MUST be split.
7. **No SessionStart hook injection.** External SessionStart hooks (SuperClaude's pm-agent restore, Superpowers' `using-superpowers` injection) MUST NOT be ported — they conflict with `AGENTS.md SS.1–SS.3` mandatory bootstrap contract.
8. **Sync cadence.** The first port is a snapshot. Subsequent re-syncs MUST file a new Task; an automated upstream-pull is explicitly out of scope and would be a future ADR.
9. **Don't port these.** SuperClaude `sc:help`/`sc:sc`/`sc:recommend`/`sc:select-tool`/`sc:load`/`sc:save`/`sc:git`/`sc:task`/`sc:index` and Superpowers `using-superpowers`/`brainstorming` MUST NOT be ported — they conflict with or duplicate existing Agency surfaces (see §2.1, §3.1 rationale).

**Consequences** —

- `CLAUDE.md §13` references resolve: `/sc:implement`, `/sc:test`, `/sc:createPR`, `/sc:improve`, `/sc:research` become real skill bodies under `skills/sc-*/`.
- `tools/fm/validate.py` MUST learn the new `skill_source` key — minor extension to `_check_skill_*` in `tools/fm/validate.py` (T2 additive).
- Skill count goes from 22 to ~42 (+20 imports). The skills manifest `skills/skills-skill-bootstrap/sync.sh` MUST regenerate.
- `skills/readme.md` index grows; expect 1–2 new sections "Imported from SuperClaude" / "Imported from Superpowers".

**Alternatives considered** —

- Bare slugs (no `sc-` / `superpowers-` prefix): rejected per user choice (provenance loss, collision risk).
- One ADR per imported skill: rejected (40+ ADRs would drown the ledger; one umbrella ADR is sufficient for the policy).
- Auto-pull on every commit: rejected (snapshot-then-PR cadence aligns with Agency's deliberative governance; auto-pull would introduce upstream-drift risk).

---

## 5. Task scaffolds

Three sibling Tasks under `/tasks/` execute the port. Each gets its own folder with `task.md`, `readme.md`, and (per `PROMPT.md`) optional brief if a prompt is spawned. Task IDs continue from the highest existing number; assume next-free starts at `NNN`.

### 5.1 Task: `tasks/<NNN>-port-superclaude-must-have/`

```yaml
---
type: task
status: active
slug: port-superclaude-must-have
summary: "Port the 12 must-have SuperClaude commands and 11 must-have agents into skills/sc-*/."
created: 2026-05-12
updated: 2026-05-12
task_id: <NNN>
task_status: open
task_owner: claude
task_affects_paths:
  - skills/sc-analyze/
  - skills/sc-brainstorm/
  - skills/sc-business-panel/
  - skills/sc-createPR/
  - skills/sc-design/
  - skills/sc-implement/
  - skills/sc-improve/
  - skills/sc-reflect/
  - skills/sc-research/
  - skills/sc-spec-panel/
  - skills/sc-test/
  - skills/sc-troubleshoot/
  - skills/sc-business-panel-experts/
  - skills/sc-deep-research-agent/
  - skills/sc-performance-engineer/
  - skills/sc-pm-agent/
  - skills/sc-quality-engineer/
  - skills/sc-requirements-analyst/
  - skills/sc-root-cause-analyst/
  - skills/sc-security-engineer/
  - skills/sc-self-review/
  - skills/sc-socratic-mentor/
  - skills/sc-system-architect/
  - skills/readme.md
  - skills/skills-skill-bootstrap/sync.sh
task_uses_prompts: []
task_spawns_research: []
task_depends_on: [ADR-0011]
---
```

**Plan**:

1. Land ADR-0011 first (`decisions/0011-external-skill-corpora-import.md`, status Proposed → Accepted).
2. For each of the 23 must-have items (12 commands + 11 agents): copy upstream `.md` body, rewrite frontmatter to Agency's L1+L2 shape (use `templates/skill.md` as the starting skeleton), add the five required H2 sections (`## What`, `## When to use`, `## How to use`, `## References`, `## Compatibility`), pin upstream SHA in `## References`, ensure body ≤ 5 KB (overflow → `references/`).
3. Bundle modes: copy `MODE_Brainstorming.md` into `skills/sc-brainstorm/references/`, etc. (4 modes total — see §2.3).
4. Update `skills/readme.md` with a new "Imported from SuperClaude" section listing every entry.
5. Regenerate the skills manifest by running `skills/skills-skill-bootstrap/sync.sh` (or its successor) — `B.3` (SKILLS.md §7.1) requires the manifest to list every slug.
6. Run `tools/check-governance.sh` — all 23 new skills MUST pass `tools/fm/validate.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`. Fix any frontmatter or heading issues at this gate.
7. Commit and push to `claude/analyze-repo-architecture-KEvqh`. Open draft PR per `AGENTS.md` Closing Run Procedure step 4.

**Acceptance criteria (Gherkin)**:

```gherkin
Feature: Must-have SuperClaude skills ported to Agency

  # anchor: PORT.SC.1
  Scenario: Every must-have command has a skill body under skills/sc-*/
    Given the must-have command list from §2.1 (12 entries)
    When the task is complete
    Then for every entry "sc:X" there MUST exist skills/sc-X/SKILL.md
    And the SKILL.md MUST carry skill_source: "superclaude@<sha>"
    And the SKILL.md body MUST be ≤ 5 KB

  # anchor: PORT.SC.2
  Scenario: tools/check-governance.sh exits 0 on the final commit
    Given all 23 new skill folders are committed
    When tools/check-governance.sh runs
    Then it MUST exit 0
    And tools/lint-linkage.py MUST resolve every skill_references_skills entry
```

**Todo (extracted from plan steps)**:

- [ ] ADR-0011 drafted, validated, status set to Accepted
- [ ] 12 must-have commands ported (frontmatter, sections, references)
- [ ] 11 must-have agents ported (as `skill_kind: domain` or `orchestrator`)
- [ ] 4 modes bundled into respective skills' `references/`
- [ ] `skills/readme.md` updated with SuperClaude section
- [ ] Manifest regenerated, sync.sh verified
- [ ] `tools/check-governance.sh` green
- [ ] Friction log + PR

### 5.2 Task: `tasks/<NNN+1>-port-superpowers-must-have/`

```yaml
---
type: task
status: active
slug: port-superpowers-must-have
summary: "Port the 9 must-have Superpowers skills into skills/superpowers-*/."
created: 2026-05-12
updated: 2026-05-12
task_id: <NNN+1>
task_status: open
task_owner: claude
task_affects_paths:
  - skills/superpowers-writing-plans/
  - skills/superpowers-executing-plans/
  - skills/superpowers-test-driven-development/
  - skills/superpowers-systematic-debugging/
  - skills/superpowers-subagent-driven-development/
  - skills/superpowers-requesting-code-review/
  - skills/superpowers-receiving-code-review/
  - skills/superpowers-verification-before-completion/
  - skills/superpowers-writing-skills/
  - skills/readme.md
  - skills/skills-skill-bootstrap/sync.sh
task_uses_prompts: []
task_spawns_research: []
task_depends_on: [ADR-0011]
---
```

**Plan** (similar shape to §5.1):

1. For each of the 9 must-have skills: copy upstream `SKILL.md` + reference files (the supporting files are critical here — `superpowers:systematic-debugging` ships 6 ref files; `superpowers:writing-skills` ships 7), rewrite frontmatter to Agency's L1+L2 shape, ensure body ≤ 5 KB (the 22.5 KB `writing-skills` SKILL.md MUST be split).
2. Bundle the `code-reviewer` agent into `skills/superpowers-requesting-code-review/references/code-reviewer.md`.
3. Update `skills/readme.md` with a "Imported from Superpowers" section.
4. Regenerate manifest, run governance gate, commit, push, PR.

**Acceptance criteria (Gherkin)**:

```gherkin
Feature: Must-have Superpowers skills ported to Agency

  # anchor: PORT.SP.1
  Scenario: Every must-have skill has a SKILL.md under skills/superpowers-*/
    Given the must-have skill list from §3.1 (9 entries)
    When the task is complete
    Then for every entry "X" there MUST exist skills/superpowers-X/SKILL.md
    And the SKILL.md MUST carry skill_source: "superpowers@v4.0.3"

  # anchor: PORT.SP.2
  Scenario: writing-skills body split honours the T2 ladder
    Given skills/superpowers-writing-skills/SKILL.md exists
    When tools/fm/validate.py --check-body runs against it
    Then the body MUST be ≤ 5 KB
    And the overflow MUST live under skills/superpowers-writing-skills/references/
    And references/ MUST include anthropic-best-practices.md, persuasion-principles.md, testing-skills-with-subagents.md
```

**Todo**:

- [ ] 9 must-have skills ported
- [ ] `code-reviewer` agent bundled
- [ ] `writing-skills` body split (T2 ≤ 5 KB, references/ holds the rest)
- [ ] `skills/readme.md` updated with Superpowers section
- [ ] Manifest regenerated, governance green
- [ ] Friction log + PR

### 5.3 Task: `tasks/<NNN+2>-port-nice-to-have-corpora/`

Lower-priority follow-up — gates on the must-have Tasks landing first. Same shape, covers 11 SuperClaude nice-to-haves (`sc:agent`, `sc:build`, `sc:cleanup`, `sc:document`, `sc:estimate`, `sc:explain`, `sc:index-repo`, `sc:pm`, `sc:spawn`, `sc:workflow` + `MODE_Token_Efficiency`) + 8 SuperClaude agents (backend-architect, devops-architect, frontend-architect, learning-guide, python-expert, refactoring-expert, repo-index, technical-writer) + 3 Superpowers nice-to-haves (`using-git-worktrees`, `finishing-a-development-branch`, `dispatching-parallel-agents`).

Defer this Task to a later session; the must-have set is the priority.

---

## 6. Critical files to read/modify (porting agent's working set)

**Read first (governance):**
- `AGENTS.md` (entry-point, closing-run procedure)
- `SKILLS.md` (§3 frontmatter, §5 required sections, §7 bootstrap protocol, §7.3 T1/T2/T3 ladder)
- `decisions/0007-skill-bundles-tools-frontmatter.md` (precedent for adding L2 keys via ADR)
- `decisions/readme.md` (how to write ADR-0011)
- `templates/skill.md` (canonical skeleton — copy don't freelance)
- `PRE_COMMIT.md` (full gate matrix)
- `skills/readme.md` (existing skill index — where new sections land)

**Modify (porting Task 5.1, 5.2):**
- `decisions/0011-external-skill-corpora-import.md` (new ADR)
- `skills/sc-*/SKILL.md` (12 + 11 = 23 new files)
- `skills/sc-*/references/MODE_*.md` (4 modes bundled)
- `skills/superpowers-*/SKILL.md` (9 new files)
- `skills/superpowers-*/references/*.md` + `references/*.ts`, `references/*.sh` (~15 supporting files)
- `skills/superpowers-requesting-code-review/references/code-reviewer.md` (bundled agent)
- `skills/readme.md` (two new index sections)
- `skills/skills-skill-bootstrap/sync.sh` (verify it picks up new folders; may need extension if it filters by slug pattern)
- `tools/fm/validate.py` (T2 additive: register `skill_source` key in `_check_skill_*`)
- `tasks/<NNN>-port-superclaude-must-have/{task.md,readme.md}` (new Task)
- `tasks/<NNN+1>-port-superpowers-must-have/{task.md,readme.md}` (new Task)
- `tasks/readme.md` (index of all Tasks — `tools/fm/index_diff.py` enforces sync)

**Reuse without modification:**
- `tools/check-governance.sh` (the unified gate — already runs everything needed)
- `tools/adr/cli.py {validate,synthesize}` (ADR-0011 validated by `validate`, synthesised into `AGENTS.md` guarded block by `synthesize` after status flips to Accepted)
- `skills/skill-creator/SKILL.md` (mirror of Anthropic's authoring guide; consult for shape — but defer to `templates/skill.md` for Agency-specific shape)

---

## 7. Verification

End-to-end verification after each Task:

1. `./install.sh` — must exit 0 (Agency bootstrap)
2. `tools/check-governance.sh` — must exit 0 (full governance gate)
3. `python3 tools/adr/cli.py validate` — must pass on `decisions/0010-*`
4. `python3 tools/fm/validate.py --check-body skills/sc-*/SKILL.md skills/superpowers-*/SKILL.md` — must pass; specifically the T2 size constraint catches `writing-skills` overflow
5. `python3 tools/fm/query.py type=spec has-key=skill_source` — must return every newly imported skill, none of the pre-existing 22 native skills
6. `bash skills/skills-skill-bootstrap/verify.sh` — must confirm `.skills-manifest.json` lists all new slugs with their `skill_kind`
7. Manual smoke test in Claude Code: invoke `Skill` tool with `sc:createPR` — must surface the new ported body, not a "not found" error
8. PR opened (draft) with body citing closed Task slug + `Highest Frustration Level: FL0` per `FRUSTRATED.md`

A successful run leaves the repo with 22 → 42 skills, ADR-0011 Accepted, two new closed Tasks, and `CLAUDE.md §13`'s previously dangling `/sc:*` references now resolved against real skill bodies.

---

## 8. Out of scope (explicit)

- Porting MCP server installers (Agency is a governance repo, not a Claude Code installer)
- Porting SessionStart hooks (would conflict with AGENTS.md SS.1–SS.3 bootstrap contract)
- Auto-pull on upstream change (future ADR; this port is a snapshot)
- `sc:help`, `sc:sc`, `sc:recommend`, `sc:select-tool`, `sc:load`, `sc:save`, `sc:git`, `sc:task`, `sc:index`, `superpowers:using-superpowers`, `superpowers:brainstorming` (rationale in §2.1 / §3.1)
- ~~Modifying `AGENTS.md` Closing Run Procedure to reference the local `skills/sc-createPR/`~~ → **superseded by §9 below**: this is now IN scope for Phase 1.

---

