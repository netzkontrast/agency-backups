## 9. Brainstorm refinement — execution requirements (Phase 1 spec)

`/sc:brainstorm` output. Scope: requirements only — design (per-skill body structure, ADR-0011 acceptance criteria detail) deferred to a follow-up `/sc:design` call. The Phase 0 pilot from §5 is folded into Phase 1 because the user chose "dangling references first" (the pilot's anchor skill, `sc:createPR`, *is* one of the dangling references — they collapse to the same first batch).

### 9.1 User goals (clarified)

- **G1.** Resolve the dangling `/sc:*` references already cited in `CLAUDE.md §13` and `AGENTS.md` Closing Run Procedure. Today those references point to a remote SuperClaude repo URL; the Agency repo "promises" five skills it does not actually ship.
- **G2.** Each ported skill participates in Agency's existing surfaces (audit graph, tools/, root-spec citations) at a depth chosen *per skill*, not by a blanket rule.
- **G3.** First batch is self-contained: it lands ADR-0011, the five `/sc:*` skills, their critical agents, the necessary `tools/fm/validate.py` extension, and the root-spec citation rewrites — in one Task, atomically.

### 9.2 Phase 1 scope — 14 items, per-skill tier

| # | Item | Tier | Rationale |
|---|---|---|---|
| 1 | `sc:createPR` | **L4** | Already cited by `AGENTS.md` Closing Run Procedure (remote URL); replaces that URL with local path. Bundles `tools/check-governance.sh` (defense-in-depth on CR.3). |
| 2 | `sc:implement` | **L3** | Cited in `CLAUDE.md §13`. Bundles `tools/fm/edit.py` (frontmatter mutations during implementation). Graph-wires the architect family. |
| 3 | `sc:test` | **L3** | Cited in `CLAUDE.md §13`. Bundles `tools/tests/` (pytest entry point). May be cited from `PRE_COMMIT.md` as the canonical test-runner skill. |
| 4 | `sc:improve` | **L2** | Cited in `CLAUDE.md §13`. No natural tool bundle; graph-wired only to refactoring/quality/performance-engineer skills. |
| 5 | `sc:research` | **L4** | Cited in `CLAUDE.md §13`. Body MUST be MCP-adapted (Tavily optional, WebSearch/WebFetch primary). `RESEARCH.md` gains a §"Skill-driven research runs" citing this skill as canonical. |
| 6 | `sc-system-architect` | **L2** | Referenced by `sc:implement` and `sc:design`. |
| 7 | `sc-backend-architect` | **L1** | Verbatim cited mirror — leaf node, no graph edges to wire. |
| 8 | `sc-frontend-architect` | **L1** | Same. |
| 9 | `sc-security-engineer` | **L2** | Referenced by `sc:implement`. |
| 10 | `sc-quality-engineer` | **L2** | Referenced by `sc:test`, `sc:improve`. |
| 11 | `sc-refactoring-expert` | **L1** | Verbatim. |
| 12 | `sc-performance-engineer` | **L1** | Verbatim. |
| 13 | `sc-deep-research-agent` | **L2** | Referenced by `sc:research`. |
| 14 | `sc-pm-agent` | **L1** | Verbatim. **Not** hook-injected (would conflict with SS.1–SS.3); available for manual `/sc:pm` invocation. |

Five `/sc:*` skills + nine supporting agent-skills. Phase 2/3 from §5 unchanged.

### 9.3 Functional requirements

- **FR1.** Each of the 14 items MUST exist at `skills/sc-<slug>/SKILL.md` after Phase 1 completes.
- **FR2.** ADR-0011 (`decisions/0011-external-skill-corpora-import.md`) MUST be drafted and accepted **before** any skill file is written (governance ordering: architectural conventions land first, files second).
- **FR3.** `tools/fm/validate.py` MUST accept the new L2 frontmatter key `skill_source` (additive; no L1 change). This is a **T2 additive repair** per `MAINTENANCE.md §1`.
- **FR4.** `AGENTS.md` Closing Run Procedure prose paragraph MUST be rewritten to cite the local path `[skills/sc-createPR/SKILL.md](./skills/sc-createPR/SKILL.md)` in place of the remote `https://github.com/netzkontrast/SuperClaude_Framework/.../createPR.md` URL. The rewrite MUST land in the same commit as `skills/sc-createPR/SKILL.md` so AGENTS.md is never citing a non-existent local path.
- **FR5.** `RESEARCH.md` MUST gain a §"Skill-driven research runs" paragraph citing `skills/sc-research/SKILL.md` as the canonical implementation of the RESEARCH.md §6.5 deep-research integration flow.
- **FR6.** `sc:research` SKILL.md body MUST list WebSearch and WebFetch (built-in Claude Code tools) as the primary research surface; Tavily MCP MUST be marked OPTIONAL in `## Compatibility`. The upstream Tavily-required posture MUST NOT be ported verbatim.
- **FR7.** Each of the five `/sc:*` skills MUST populate `skill_references_skills` with its supporting agent-skills (per the §2.1 column "Activated agents"), so `tools/lint-linkage.py` enforces the audit graph.
- **FR8.** L3 items (`sc:implement`, `sc:test`) MUST declare `skill_bundles_tools` per ADR-0007's schema (each entry MUST resolve to an existing `tools/<slug>/` directory; no `..` segments).
- **FR9.** L4 items (`sc:createPR`, `sc:research`) MUST do FR7 + FR8 + carry citations into the relevant root spec(s).

### 9.4 Non-functional requirements

- **NFR1.** Every new SKILL.md MUST pass `tools/check-governance.sh` (ERROR-tier linters). Advisory WARN-tier diagnostics MAY be present at first commit but MUST be resolved before Phase 1 closes.
- **NFR2.** Every new SKILL.md body MUST be ≤ 5 KB per `SKILLS.md §7.3` (T2 ladder). The upstream `sc:implement` body is ~9 KB and `sc:research` is ~7 KB; both overflow → `references/`.
- **NFR3.** Every `## References` section MUST include a SHA-pinned citation to the upstream file per `AGENTS.md` Citation Reproducibility Protocol (`path/to/file.ext:Lstart-Lend@<sha>`).
- **NFR4.** No SessionStart hook MAY be added. The upstream SuperClaude `SessionStart` (pm-agent auto-restore via Serena) is silently dropped; `sc-pm-agent` is invocable but inert at session start.
- **NFR5.** The `tools/fm/validate.py` extension (FR3) MUST be backwards-compatible: skills without `skill_source` MUST continue to validate (the existing 22 native skills don't carry this key and MUST NOT be flagged).

### 9.5 User stories

- **US1.** *As an Agency operator running a Claude Code session,* when I reach the Closing Run Procedure step 4, I invoke `/sc:createPR` and the local `skills/sc-createPR/SKILL.md` fires — so I'm not externally dependent on the SuperClaude repo's availability.
- **US2.** *As an Agency operator implementing a Task,* when I invoke `/sc:implement`, the skill body knows to invoke `tools/fm/edit.py` for frontmatter changes (rather than freelancing sed/awk per CLAUDE.md §14.6) — so the implementation stays governance-compliant.
- **US3.** *As an Agency operator running tests,* when I invoke `/sc:test`, the skill body knows to invoke `tools/tests/` and report coverage against the existing pytest suite — so I don't need to remember the pytest invocation by hand.
- **US4.** *As an Agency operator doing research,* when I invoke `/sc:research`, the skill body knows the output deliverable lands under `/research/<slug>/output/SPEC.md` per RESEARCH.md (not a free-form scratchpad), and uses WebSearch/WebFetch by default (not a missing Tavily MCP).
- **US5.** *As a reader of `CLAUDE.md §13`,* every `/sc:*` reference resolves to a real local skill body — so the repo no longer "lies" about what it ships.

### 9.6 Acceptance criteria

```gherkin
Feature: Phase 1 closes the CLAUDE.md §13 dangling-reference gap

  # anchor: BR.9.1
  Scenario: All five dangling references resolve to local skill bodies
    Given the five skills cited in CLAUDE.md §13 (sc:implement, sc:test, sc:createPR, sc:improve, sc:research)
    When Phase 1 is complete
    Then for each cited skill there MUST exist skills/sc-<slug>/SKILL.md
    And each SKILL.md MUST carry skill_source: "superclaude@<sha>"
    And tools/check-governance.sh MUST exit 0 on the final commit

  # anchor: BR.9.2
  Scenario: AGENTS.md no longer cites the remote SuperClaude URL
    Given Phase 1 is complete
    When `grep -n "src/superclaude/commands/createPR.md" AGENTS.md` runs
    Then the command MUST return zero matches
    And `grep -n "skills/sc-createPR/SKILL.md" AGENTS.md` MUST return at least one match

  # anchor: BR.9.3
  Scenario: sc:research is MCP-adapted, not a Tavily-only mirror
    Given skills/sc-research/SKILL.md exists
    When a reader opens its "## How to use" and "## Compatibility" sections
    Then WebSearch and WebFetch MUST be listed as the primary research surface
    And Tavily MUST be marked OPTIONAL
    And the upstream "Tavily MCP required" posture MUST NOT appear in the SKILL.md body

  # anchor: BR.9.4
  Scenario: Audit graph picks up the new skills
    Given the 14 Phase-1 skills are committed
    When tools/lint-linkage.py runs
    Then every skill_references_skills entry MUST resolve to a sibling skill folder
    And no broken reference MUST be reported
    And reciprocity (the X-referenced-by-Y computed inverse) MUST be present in the manifest

  # anchor: BR.9.5
  Scenario: T2 size cap enforced; overflow lives in references/
    Given any imported SKILL.md whose upstream body exceeded 5 KB (e.g. sc:implement, sc:research)
    When tools/fm/validate.py --check-body runs
    Then the body MUST be ≤ 5 KB
    And the overflow MUST live under skills/sc-<slug>/references/
    And references/ MUST be cited from the body's "## References" section
```

### 9.7 Resolved decisions (was: Open questions)

All five questions resolved in the `/sc:brainstorm` follow-up turn. Decisions bake into the Phase-1 requirements above; rationale captured here for the next reader.

- **OQ1 — Task atomicity → Split into 2 (corpus + hookup).** Task A ships ADR-0011 + `tools/fm/validate.py` extension + 14 skill files. Task B ships AGENTS.md URL rewrite (FR4) + RESEARCH.md new § (FR5). Two PRs. The mid-state between Task A and Task B is functional: local skills exist and resolve via Claude Code's `Skill` tool; AGENTS.md still cites the remote URL but no longer needs to. Failure mode is bounded — if Task B never lands, the repo still gained a complete local skill corpus.
- **OQ2 — pm-agent posture → Port at L1 in Phase 1** (no AskUserQuestion; locked by `/sc:brainstorm` author recommendation, see §9.10). Body sits available for manual `/sc:pm`; no SessionStart hook injection. Future hook-driven workflows can opt in without re-porting.
- **OQ3 — sc:research adaptation → Rewrite body for Agency primitives.** `## How to use` MUST cite WebSearch + WebFetch as the primary surface. Tavily MCP appears only in `## Compatibility` as an optional optimization. The upstream Tavily-first body lands in `references/upstream-sc-research.md` as a verbatim mirror for re-sync auditability; the SKILL.md body itself is Agency-adapted.
- **OQ4 — ADR-0011 timing → ADR first, separate session.** ADR-0011 drafted, validated (`tools/adr/cli.py validate`), and flipped to `Accepted` in its own session before any skill files are written. Matches Agency precedent (ADR-0007 preceded Tasks 010/011). Synthesis pipeline (`tools/adr/cli.py synthesize`) will rewrite the `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` block in AGENTS.md automatically on acceptance.
- **OQ5 — `skill_source` format → Version tag only.** Frontmatter shape: `skill_source: "superclaude@v4.3.0"` and `skill_source: "superpowers@v4.0.3"`. Tag-rot risk acknowledged; mitigations are (a) upstream maintainers do not force-push release tags, (b) PyPI/marketplace immutable for SuperClaude/Superpowers respectively, (c) optional follow-up `tools/check-skill-source-pinning.py` advisory linter if drift is later observed.

### 9.8 Out of scope for Phase 1

- Phase 2 (workflow loops: TDD discipline, systematic debugging, writing-plans, reflect-into-friction-log) — sequenced next.
- Phase 3 (remaining must-haves + Superpowers corpus) — sequenced after that.
- Auto-sync from upstream — future ADR.
- MCP installer packaging — Agency does not ship installers.
- Modifying root specs other than AGENTS.md (CR.1.1 paragraph) and RESEARCH.md (new §) — any other root-spec change is a T3 structural edit and MUST be filed as its own Task per `MAINTENANCE.md §1`.
- Tag-pin drift monitoring (`tools/check-skill-source-pinning.py`) — deferred until empirical drift is observed.

### 9.9 Handoff

Next step per `/sc:brainstorm` boundaries: invoke **`/sc:design`** to convert this requirements spec into a per-skill body design (header structure, exact `references/` layout per skill, exact `skill_bundles_tools` entries for L3 items, exact root-spec citation diff for FR4/FR5). After `/sc:design`, the two Task files (Task A "corpus", Task B "hookup") can be written and execution begins — starting with the ADR-0011 drafting session per OQ4.

### 9.10 Decision-trail (resolved-in-this-session)

| # | Question | Decision | Author | Captured-in |
|---|---|---|---|---|
| OQ1 | Phase-1 atomicity | Split: Task A (corpus) + Task B (hookup) | user | §9.7 |
| OQ2 | pm-agent | L1 verbatim, no hook | author recommendation (no user dissent) | §9.7 |
| OQ3 | sc:research adaptation | Rewrite body; verbatim upstream → references/ | user | §9.7, §FR6, §BR.9.3 |
| OQ4 | ADR-0011 timing | Separate session, before skill files | user | §9.7, §FR2 |
| OQ5 | skill_source format | Version tag only (`superclaude@v4.3.0`) | user | §9.7, §FR3, §NFR3 |

All five resolved. Phase 1 requirements are now locked. Ready for `/sc:design`.

---

