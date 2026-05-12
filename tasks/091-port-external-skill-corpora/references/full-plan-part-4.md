## 10. Design specifications (output of `/sc:design`)

This section is the executable design for Phase 1. It converts the locked requirements (§9) into per-artifact specs that `/sc:implement` (or any porting agent) can act on without further clarification. Five design artifacts: **ADR-0011** (§10.1), **validator extension** (§10.2), **per-skill SKILL.md design** (§10.3), **root-spec citation diffs** (§10.4), **Task A & Task B scaffolds** (§10.5). Plus a **build order DAG** (§10.6) and **verification recipe** (§10.7).

### 10.1 ADR-0011 detailed structure

File: `decisions/0011-external-skill-corpora-import.md`. Format: MADR 4.0.0 per `decisions/readme.md`. Validated by `python3 tools/adr/cli.py validate`. On `adr_status: Accepted`, the synthesis pipeline (`tools/adr/cli.py synthesize`) rewrites the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block in `AGENTS.md`.

**Frontmatter** (exact YAML to write — copy verbatim, adjust `created`):

```yaml
---
type: adr
status: active
slug: external-skill-corpora-import
summary: "Policy for importing external skill corpora (SuperClaude_Framework, Superpowers) into /skills/ under vendor-prefixed namespaces with skill_source pin."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0011
adr_status: Proposed
adr_supersedes: []
adr_superseded_by: []
adr_relates_to: [ADR-0003, ADR-0006, ADR-0007]
---
```

**Section structure** (MADR 4.0.0 mandatory sections + Agency-required Gherkin AC):

| Section (H2) | Content design |
|---|---|
| `## Status` | Single line: `Proposed`. (Flipped to `Accepted` in the second commit of the ADR session after review.) |
| `## Context` | Three paragraphs: (a) the dangling-reference problem in CLAUDE.md §13 and AGENTS.md; (b) the two upstream corpora and their naming/distribution conventions; (c) why a single umbrella ADR (vs one ADR per imported skill) is the right granularity. Cites the §1 inventory in this plan and `research/skills-skill-architecture/output/SPEC.md` §6 R5 (trust-boundary invariants). |
| `## Decision` | Nine normative clauses **D.1–D.9** (RFC 2119 uppercase). Verbatim text below. |
| `## Consequences` | Three subsections: **Positive** (dangling references resolve; `tools/fm/validate.py` learns a generally-useful key; corpus grows from 22→36 in Phase 1), **Negative** (one new mutable-tag risk per OQ5; +14 skills' worth of governance overhead per commit; upstream re-syncs require manual Tasks), **Neutral** (sync.sh continues to work unmodified; no new MCP installer; SessionStart hooks remain Agency-controlled). |
| `## Alternatives` | Three rejected alternatives with one-paragraph rationale each: (a) bare slugs no prefix → rejected (provenance loss); (b) one ADR per imported skill → rejected (ledger drowning); (c) auto-pull-on-commit → rejected (drift risk; future ADR). |
| `## References` | SHA-pinned citations to: SKILLS.md §7.2 trust boundary, ADR-0007 (precedent for L2 additive frontmatter), AGENTS.md Closing Run Procedure (the dangling-reference site), upstream SuperClaude `pyproject.toml` v4.3.0, upstream Superpowers `.claude-plugin/plugin.json` v4.0.3. |
| `## Acceptance Criteria` | Three Gherkin scenarios verbatim below. |

**Verbatim D.1–D.9 normative clauses** (RFC 2119 uppercase; one keyword per sentence per `maintenance/language-spec.md` R1):

- **D.1 Namespace prefixing.** External skill folders MUST live at `skills/<vendor>-<bare-slug>/` where `<vendor>` ∈ `{sc, superpowers}`. Bare slugs (no vendor prefix) MUST be reserved for Agency-native skills.
- **D.2 Source pin.** Every imported `SKILL.md` MUST carry the L2 frontmatter key `skill_source` with value `<vendor>@v<semver>` (e.g. `superclaude@v4.3.0`). The key MUST NOT appear on Agency-native skills.
- **D.3 Citation.** Every imported `SKILL.md` `## References` section MUST include a SHA-pinned link to the upstream source file in the form `path/to/file.ext:Lstart-Lend@<sha>` per AGENTS.md "Citation Reproducibility Protocol".
- **D.4 Agent-as-skill.** Upstream agent files (SuperClaude `src/superclaude/agents/*.md`) MUST be ported as skills (`skill_kind: domain` for single-persona agents, `skill_kind: orchestrator` when the agent coordinates other agents). Agents MUST NOT be stored outside `/skills/`.
- **D.5 Modes as references.** Upstream `MODE_*.md` files MUST be bundled inside the relevant skill's `references/` directory. Modes MUST NOT be ported as standalone skills.
- **D.6 T2 size cap.** Every imported `SKILL.md` body MUST be ≤ 5 KB per SKILLS.md §7.3. Excess prose MUST move to the skill's `references/` directory and MUST be cited from the body's `## References` section.
- **D.7 No SessionStart injection.** Upstream SessionStart hooks (SuperClaude pm-agent restore, Superpowers `using-superpowers` injection) MUST NOT be ported. The Agency bootstrap contract in AGENTS.md SS.1–SS.3 remains canonical.
- **D.8 Body adaptation for MCP-free runtimes.** When an upstream body requires an MCP server Agency does not ship (Tavily, Morphllm, Magic, Serena, Chrome DevTools), the SKILL.md body MUST be rewritten so a built-in Claude Code primitive (WebSearch, WebFetch, Read/Write/Edit, Bash) is the primary path. The upstream MCP MUST appear only in `## Compatibility` as OPTIONAL. The verbatim upstream body MUST be archived at `skills/<vendor>-<slug>/references/upstream-<vendor>-<slug>.md`.
- **D.9 Sync cadence.** The first port is a one-shot snapshot. Subsequent re-syncs from upstream MUST file a new Task. Automated upstream-pull is OUT OF SCOPE for this ADR and MUST be addressed by a future ADR if needed.

**Verbatim Gherkin AC** (three scenarios; copy as-is):

```gherkin
Feature: External skill corpora import policy

  # anchor: ADR.11.1
  Scenario: Imported skill carries vendor prefix and source pin
    Given an external SKILL.md is being ported into /skills/
    When the porting agent writes the file
    Then the folder path MUST match skills/(sc|superpowers)-<bare-slug>/
    And the SKILL.md frontmatter MUST contain skill_source: "<vendor>@v<semver>"
    And the SKILL.md ## References section MUST include a SHA-pinned upstream citation

  # anchor: ADR.11.2
  Scenario: Validator accepts skill_source on imports, rejects on natives
    Given tools/fm/validate.py runs over /skills/
    When it encounters a SKILL.md with skill_source set
    Then it MUST accept the key if the folder path matches the vendor-prefix rule (D.1)
    And it MUST reject the key with diagnostic F.B.7 if the folder is a bare slug (Agency native)

  # anchor: ADR.11.3
  Scenario: T2 body cap enforced on every import
    Given any imported SKILL.md
    When tools/fm/validate.py --check-body runs against it
    Then the body MUST be ≤ 5 KB
    And the overflow MUST live under skills/<vendor>-<slug>/references/
    And references/ MUST be cited from the body's ## References section
```

### 10.2 `tools/fm/validate.py` extension design

**Goal**: register `skill_source` as a valid L2 frontmatter key for files under `skills/<vendor>-<bare-slug>/SKILL.md` (D.2). Reject it on bare-slug (Agency-native) skills.

**Change shape** (T2 additive per MAINTENANCE.md §1):

- New constant near the top of `tools/fm/validate.py`:
  ```python
  VENDOR_PREFIXES = ("sc-", "superpowers-")
  SKILL_SOURCE_RE = re.compile(r"^(superclaude|superpowers)@v\d+\.\d+\.\d+$")
  ```
- New check method (or extension of `_check_skill_*` if such exists):
  ```python
  def _check_skill_source(self, fm: dict, relpath: str) -> list[Diagnostic]:
      diagnostics = []
      if "skill_source" not in fm:
          return diagnostics  # absence is fine for native skills
      folder = relpath.split("/")[1]  # skills/<folder>/SKILL.md
      is_vendor_prefixed = folder.startswith(VENDOR_PREFIXES)
      if not is_vendor_prefixed:
          diagnostics.append(Diagnostic(
              relpath, "ERROR", "F.B.7",
              "skill_source is reserved for vendor-prefixed imports per ADR-0011 D.1"))
      value = fm.get("skill_source")
      if not isinstance(value, str) or not SKILL_SOURCE_RE.match(value):
          diagnostics.append(Diagnostic(
              relpath, "ERROR", "F.B.8",
              f"skill_source value '{value}' does not match '<vendor>@v<semver>' per ADR-0011 D.2"))
      return diagnostics
  ```
- Hook into the existing validator entry point (where `_check_skill_bundles` is invoked).

**New diagnostic codes** (register in the diagnostic catalog if `tools/fm/validate.py` maintains one):

| Code | Tier | Trigger |
|---|---|---|
| `F.B.7` | ERROR | `skill_source` present on a bare-slug (native) skill |
| `F.B.8` | ERROR | `skill_source` value does not match `^(superclaude\|superpowers)@v\d+\.\d+\.\d+$` |

**Test additions** (under `tools/tests/`):

- `test_skill_source_accepted_on_vendor_prefix` — vendor-prefixed folder + valid value → no diagnostic
- `test_skill_source_rejected_on_bare_slug` — bare-slug folder + value → F.B.7
- `test_skill_source_malformed_value` — vendor-prefixed folder + `superclaude@latest` → F.B.8
- `test_skill_source_absent_is_fine_for_natives` — bare-slug folder + no key → no diagnostic
- `test_existing_native_skills_still_validate` — regression test running validator over all 22 existing skill folders → no diagnostics

Diff size estimate: ~30 lines validate.py + ~50 lines test file. Single-commit T2 additive.

### 10.3 Per-skill SKILL.md design (14 items)

**Canonical SKILL.md shape** (every imported file follows this skeleton — derived from `templates/skill.md`):

```markdown
---
type: spec
status: active
slug: sc-<bare-slug>                  # or superpowers-<bare-slug>
summary: "<one-line, ≤120 chars>"
created: 2026-05-12
updated: 2026-05-12
skill_kind: <domain|tool|orchestrator|meta>
skill_target_agents: [claude-code]    # add claude-ai if container-portable
skill_references_skills: []            # populate per the table below
skill_references_research: []          # populate per the table below
skill_references_prompts: []
skill_bootstrap_required: false        # true only if the skill self-loads from origin/main
skill_source: "superclaude@v4.3.0"     # or superpowers@v4.0.3
# skill_bundles_tools:                 # OPTIONAL, only when listed in §10.3 per-skill table
#   - tools/<subdir>
---

# <Human-Readable Title>

## What
<2-3 sentences. Purpose and scope. T2 ≤ 5 KB body cap applies.>

## When to use
<Trigger conditions, third-person, "Use when ..." opener per Superpowers CSO convention.>

## How to use
<Actionable steps. For L3+ skills, MUST cite tools/ paths the skill expects. For L4 skills, MUST cite the root spec section that anchors the skill.>

## References
<Required bullets:
- Upstream pin: src/superclaude/<commands|agents>/<slug>.md:L1-L<N>@<sha> per ADR-0011 D.3
- Agency anchor: link to relevant /research/ workspace or root spec §
- references/ overflow: link to references/upstream-<vendor>-<slug>.md if §10.3 overflow column says "yes">

## Compatibility
<MCP servers used (if any) — mark Tavily/Magic/Morphllm/Serena/Chrome-DevTools as OPTIONAL per D.8.
Agent portability — usually [claude-code] for Phase 1.
Known limitations — copied from upstream where applicable.>
```

**Per-skill design table** — exact frontmatter fields and references/ layout for all 14 items:

| Slug | `skill_kind` | `skill_references_skills` | `skill_references_research` | `skill_bundles_tools` | `references/` files | Tier | Notes |
|---|---|---|---|---|---|---|---|
| `sc-createPR` | `tool` | `[skills-skill-bootstrap]` | `[skills-skill-architecture]` | — | `references/upstream-sc-createPR.md` | **L4** | Body cites AGENTS.md CR.1–CR.7 lifecycle. Body MUST instruct invoking `tools/check-governance.sh` before the PR call. Body MUST reference the `mcp__github__create_pull_request` primitive. |
| `sc-implement` | `orchestrator` | `[sc-system-architect, sc-backend-architect, sc-frontend-architect, sc-security-engineer, sc-quality-engineer]` | `[]` | `[tools/fm]` | `references/upstream-sc-implement.md`, `references/MODE_Orchestration.md` (if `sc-spawn` not in Phase 1, bundle the mode here) | **L3** | Body mentions `tools/fm/edit.py` for frontmatter mutations per CLAUDE.md §14.6 (never sed/awk). |
| `sc-test` | `tool` | `[sc-quality-engineer]` | `[]` | `[tools/tests]` | `references/upstream-sc-test.md` | **L3** | Body invokes pytest via `tools/tests/`; reports coverage. PRE_COMMIT.md may eventually cite this skill (deferred to Task B follow-up if appetite). |
| `sc-improve` | `orchestrator` | `[sc-quality-engineer, sc-refactoring-expert, sc-performance-engineer]` | `[]` | — | `references/upstream-sc-improve.md` | **L2** | No tool-bundle; graph-wired only. |
| `sc-research` | `orchestrator` | `[sc-deep-research-agent, prompt-optimizer, research-prompt-optimizer]` | `[]` | — | `references/upstream-sc-research.md` (verbatim Tavily-first body archived per D.8), `references/MODE_DeepResearch.md` | **L4** | Body MATERIALLY rewritten per OQ3: WebSearch + WebFetch primary; Tavily OPTIONAL. Output deliverable MUST land at `/research/<slug>/output/SPEC.md` per RESEARCH.md. Citation back from RESEARCH.md (FR5). |
| `sc-system-architect` | `domain` | `[]` | `[]` | — | `references/upstream-sc-system-architect.md` | **L2** | Body lists triggers per upstream agent shape. Referenced by `sc-implement` + `sc-design` (future). |
| `sc-backend-architect` | `domain` | `[]` | `[]` | — | `references/upstream-sc-backend-architect.md` | **L1** | Verbatim cited mirror. |
| `sc-frontend-architect` | `domain` | `[]` | `[]` | — | `references/upstream-sc-frontend-architect.md` | **L1** | Verbatim cited mirror. |
| `sc-security-engineer` | `domain` | `[]` | `[]` | — | `references/upstream-sc-security-engineer.md` | **L2** | Referenced by `sc-implement`. |
| `sc-quality-engineer` | `domain` | `[]` | `[]` | — | `references/upstream-sc-quality-engineer.md` | **L2** | Referenced by `sc-test`, `sc-improve`. |
| `sc-refactoring-expert` | `domain` | `[]` | `[]` | — | `references/upstream-sc-refactoring-expert.md` | **L1** | Verbatim cited mirror. |
| `sc-performance-engineer` | `domain` | `[]` | `[]` | — | `references/upstream-sc-performance-engineer.md` | **L1** | Verbatim cited mirror. |
| `sc-deep-research-agent` | `domain` | `[]` | `[]` | — | `references/upstream-sc-deep-research-agent.md` | **L2** | Referenced by `sc-research`. Body adapted per D.8 (Tavily OPTIONAL). |
| `sc-pm-agent` | `meta` | `[]` | `[]` | — | `references/upstream-sc-pm-agent.md` | **L1** | Inert at session start; manual `/sc:pm` only. |

**`skill_bundles_tools` rationale**: only `sc-implement` and `sc-test` declare bundles, and both bundle directories (`tools/fm`, `tools/tests`) not files — per ADR-0007's directory-only constraint. The other "L3-feeling" skills (`sc-createPR`, `sc-research`) reference Agency tools in their body prose but do not bundle, because the user's working tree already has `tools/` available — bundling is only needed if the skill must run in an isolated container without `/tools/` access (claude.ai web surface).

**Cross-skill reciprocity** (computed by `tools/lint-linkage.py`, not authored): after Phase 1 lands, the manifest will compute that `sc-system-architect` is `referenced_by: [sc-implement]`, `sc-quality-engineer` is `referenced_by: [sc-test, sc-improve]`, etc. Authors MUST NOT manually write `skill_referenced_by` (SKILLS.md X.3.1).

### 10.4 Root-spec citation diffs (FR4, FR5) — Task B content

**FR4 — `AGENTS.md` Closing Run Procedure rewrite.**

Locate the prose paragraph under `### Platform Implementation Notes` → `#### Claude Code`. The current text reads (verbatim from §AGENTS.md captured earlier):

> Step 4 is satisfied by invoking the `/sc:createPR` slash-command immediately after a successful `git push`. The command is provided by the **SuperClaude Framework** at [`src/superclaude/commands/createPR.md`](https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md); it is installed automatically alongside the rest of the `/sc:*` command set. The skill re-runs `tools/check-governance.sh` before opening the PR (defence-in-depth on CR.3) and assembles the citation block CR.5 requires.

Replace with:

> Step 4 is satisfied by invoking the `/sc:createPR` slash-command immediately after a successful `git push`. The command is provided locally at [`skills/sc-createPR/SKILL.md`](./skills/sc-createPR/SKILL.md) under the import policy ratified by [ADR-0011](./decisions/0011-external-skill-corpora-import.md); it is materialised under `~/.claude/skills/sc-createPR/` by [`skills/skills-skill-bootstrap/sync.sh`](./skills/skills-skill-bootstrap/sync.sh). The skill re-runs `tools/check-governance.sh` before opening the PR (defence-in-depth on CR.3) and assembles the citation block CR.5 requires.

The remote-URL paragraph that follows (the `gh` CLI fallback note) MAY remain verbatim or MAY be similarly relocalised — at the porting agent's discretion. Verification (BR.9.2) only requires the `src/superclaude/commands/createPR.md` URL to be removed.

**FR5 — `RESEARCH.md` new § "Skill-driven research runs".**

Append a new H2 section to `RESEARCH.md` (location: after the existing §6 deep-research integration flow, before any final acceptance-criteria section). Verbatim section:

```markdown
## 7. Skill-driven research runs

A research run MAY be initiated via the `/sc:research` skill at [`skills/sc-research/SKILL.md`](./skills/sc-research/SKILL.md), imported under the policy ratified by [ADR-0011](./decisions/0011-external-skill-corpora-import.md). The skill is Agency-adapted: WebSearch + WebFetch are the primary research surface; the upstream Tavily MCP appears only as an OPTIONAL optimization per ADR-0011 D.8.

When invoked, the skill MUST land its deliverables in `/research/<slug>/output/SPEC.md` per §6.5 above. Workspace cleanliness is enforced by [`tools/check-workspace-cleanliness.py`](./tools/check-workspace-cleanliness.py); follow-up downstream-Task linkage is enforced by [`tools/check-external-result-downstream-task.py`](./tools/check-external-result-downstream-task.py). Neither linter is modified by ADR-0011 — the skill operates inside the existing R.4.4 / R.6.5 envelopes.
```

This new section MUST also be added to `RESEARCH.md`'s table of contents if the file maintains one. The `updated:` frontmatter field of `RESEARCH.md` MUST bump to the commit date.

### 10.5 Task A and Task B detailed scaffolds

Two Tasks (per OQ1). Task A is the corpus; Task B is the hookup. Task A depends on ADR-0011 being Accepted; Task B depends on Task A being Done.

**Task A — `tasks/<NNN>-port-superclaude-phase-1-corpus/`**

Frontmatter (copy verbatim, fill `<NNN>` with the next free task ID per TASK.md §8.1):

```yaml
---
type: task
status: active
slug: port-superclaude-phase-1-corpus
summary: "Port the 5 dangling-reference sc:* skills (createPR, implement, test, improve, research) plus 9 supporting agents into skills/sc-*/."
created: 2026-05-12
updated: 2026-05-12
task_id: <NNN>
task_status: open
task_owner: claude
task_affects_paths:
  - tools/fm/validate.py
  - tools/tests/test_validate_skill_source.py
  - skills/sc-createPR/
  - skills/sc-implement/
  - skills/sc-test/
  - skills/sc-improve/
  - skills/sc-research/
  - skills/sc-system-architect/
  - skills/sc-backend-architect/
  - skills/sc-frontend-architect/
  - skills/sc-security-engineer/
  - skills/sc-quality-engineer/
  - skills/sc-refactoring-expert/
  - skills/sc-performance-engineer/
  - skills/sc-deep-research-agent/
  - skills/sc-pm-agent/
  - skills/readme.md
task_uses_prompts: []
task_spawns_research: []
task_depends_on: [ADR-0011]
---
```

**Plan (numbered steps)**:

1. Verify ADR-0011 is `Accepted` (`python3 tools/adr/cli.py validate decisions/0010-*` exits 0).
2. Extend `tools/fm/validate.py` per §10.2 (new constants, new `_check_skill_source` method, hook into entry point). Add tests under `tools/tests/test_validate_skill_source.py`.
3. Run validator regression: `python3 tools/fm/validate.py skills/` MUST exit 0 (no new diagnostics on the 22 existing skills).
4. For each of the 14 skills in §10.3 (in the order listed there): create `skills/sc-<slug>/` folder, copy upstream body into `references/upstream-sc-<slug>.md`, author `SKILL.md` per the canonical shape in §10.3 with the row's specific frontmatter values.
5. For `sc-implement`: also bundle `references/MODE_Orchestration.md` (copy from upstream `src/superclaude/modes/MODE_Orchestration.md`).
6. For `sc-research`: write the Agency-adapted body (WebSearch/WebFetch primary), and also bundle `references/MODE_DeepResearch.md`.
7. Update `skills/readme.md` — add a new "Imported from SuperClaude (v4.3.0)" section listing all 14 entries with one-line summaries.
8. Regenerate the manifest via `bash skills/skills-skill-bootstrap/sync.sh --emit-manifest` (or its equivalent — verify exact invocation against `sync.sh` source).
9. Run `tools/check-governance.sh` — MUST exit 0.
10. Run BR.9.5 size check: `python3 tools/fm/validate.py --check-body skills/sc-*/SKILL.md` — every body MUST be ≤ 5 KB.
11. Commit, push, open draft PR per AGENTS.md Closing Run Procedure step 4. PR body cites this Task slug and `Highest Frustration Level: FL[0-3]`.

**Todo (mirror of plan steps)**:

- [ ] ADR-0011 validated as Accepted
- [ ] `tools/fm/validate.py` extended; 5 new test cases passing
- [ ] Validator regression: 22 existing skills still pass
- [ ] 14 skill folders created with SKILL.md per §10.3
- [ ] `references/MODE_Orchestration.md` bundled into `sc-implement`
- [ ] `references/MODE_DeepResearch.md` bundled into `sc-research`
- [ ] `skills/sc-research/SKILL.md` body Agency-adapted (WebSearch/WebFetch primary, Tavily OPTIONAL)
- [ ] `skills/readme.md` updated with new section
- [ ] Manifest regenerated
- [ ] `tools/check-governance.sh` exits 0
- [ ] T2 size cap verified on every imported SKILL.md
- [ ] Friction log + PR

**Acceptance criteria (Gherkin)**:

```gherkin
Feature: Task A — Phase 1 corpus ported with governance green

  # anchor: TA.1.1
  Scenario: All 14 skill folders exist with valid SKILL.md
    Given Task A is complete
    When the porting agent runs `python3 tools/fm/validate.py skills/sc-*/`
    Then the validator MUST exit 0
    And each SKILL.md MUST carry skill_source: "superclaude@v4.3.0"

  # anchor: TA.1.2
  Scenario: Validator extension does not regress existing skills
    Given the validator extension is committed
    When `python3 tools/fm/validate.py skills/` runs
    Then it MUST emit zero ERROR diagnostics against the 22 pre-existing skill folders

  # anchor: TA.1.3
  Scenario: sc-research is Agency-adapted, not Tavily-mandatory
    Given skills/sc-research/SKILL.md exists
    When a reader greps the body for "Tavily" and "WebSearch"
    Then "WebSearch" MUST appear in the "## How to use" section
    And "Tavily" MUST appear only in the "## Compatibility" section marked OPTIONAL
    And the verbatim upstream body MUST exist at skills/sc-research/references/upstream-sc-research.md

  # anchor: TA.1.4
  Scenario: Audit graph reciprocity computed
    Given the 14 skill folders are committed
    When the manifest is regenerated
    Then the manifest entry for sc-system-architect MUST list referenced_by: [sc-implement]
    And the manifest entry for sc-quality-engineer MUST list referenced_by: [sc-test, sc-improve]
```

**Task B — `tasks/<NNN+1>-port-superclaude-phase-1-hookup/`**

Frontmatter:

```yaml
---
type: task
status: active
slug: port-superclaude-phase-1-hookup
summary: "Rewrite AGENTS.md to cite local skills/sc-createPR/ and add RESEARCH.md §7 citing skills/sc-research/, completing the Phase 1 dangling-reference fix."
created: 2026-05-12
updated: 2026-05-12
task_id: <NNN+1>
task_status: open
task_owner: claude
task_affects_paths:
  - AGENTS.md
  - RESEARCH.md
task_uses_prompts: []
task_spawns_research: []
task_depends_on: [<task_id of Task A>]
---
```

**Plan**:

1. Verify Task A is `task_status: done` and `tools/check-governance.sh` exits 0 on `main`.
2. Edit `AGENTS.md` per §10.4 FR4 verbatim diff. Bump `updated:` to today.
3. Edit `RESEARCH.md` per §10.4 FR5 verbatim diff. Bump `updated:` to today.
4. Run `tools/check-rfc2119-polarity.py AGENTS.md RESEARCH.md` — MUST NOT introduce any polarity inversions (the FR4 rewrite is in a prose paragraph, not a MUST clause, so polarity should be preserved).
5. Run `tools/check-governance.sh` — MUST exit 0.
6. Verify BR.9.2: `grep -n "src/superclaude/commands/createPR.md" AGENTS.md` MUST return zero matches.
7. Commit, push, draft PR.

**Acceptance criteria (Gherkin)**:

```gherkin
Feature: Task B — root-spec hookup completes the dangling-reference fix

  # anchor: TB.1.1
  Scenario: AGENTS.md cites the local sc-createPR skill
    Given Task B is complete
    When `grep -n "src/superclaude/commands/createPR.md" AGENTS.md` runs
    Then the command MUST return zero matches
    And `grep -n "skills/sc-createPR/SKILL.md" AGENTS.md` MUST return at least one match

  # anchor: TB.1.2
  Scenario: RESEARCH.md has a new §7 citing sc-research
    Given Task B is complete
    When a reader opens RESEARCH.md
    Then a level-2 heading "## 7. Skill-driven research runs" MUST exist
    And the section MUST contain a Markdown link to ./skills/sc-research/SKILL.md
    And the section MUST contain a Markdown link to ./decisions/0011-external-skill-corpora-import.md

  # anchor: TB.1.3
  Scenario: No polarity inversions introduced
    Given Task B's edits are staged
    When tools/check-rfc2119-polarity.py runs against AGENTS.md and RESEARCH.md
    Then it MUST emit zero new WARN diagnostics over and above the pre-Task-B baseline
```

### 10.6 Build-order DAG

Visual sequencing of the entire Phase 1 design — what must precede what.

```
ADR session (separate, per OQ4)
  └─► decisions/0011-external-skill-corpora-import.md (Proposed)
        │
        │  (review, flip to Accepted)
        │
        ├─► tools/adr/cli.py synthesize  (auto-updates AGENTS.md guarded block)
        └─► [ready for Task A]

Task A session
  ├─► (1)  tools/fm/validate.py extension + tests
  ├─► (2)  14 skills/sc-*/SKILL.md (in §10.3 table order)
  │         │
  │         ├─► sc-pm-agent     (no deps; safest first)
  │         ├─► sc-{backend,frontend,refactoring,performance}-architect/expert  (L1 leaves)
  │         ├─► sc-system-architect  (referenced by sc-implement)
  │         ├─► sc-{security,quality}-engineer  (referenced by sc-implement/test/improve)
  │         ├─► sc-deep-research-agent  (referenced by sc-research)
  │         ├─► sc-createPR  (L4, lifecycle-anchored)
  │         ├─► sc-test  (L3, depends on sc-quality-engineer)
  │         ├─► sc-improve  (L2, depends on quality/refactor/perf)
  │         ├─► sc-implement  (L3, depends on architects + engineers)
  │         └─► sc-research  (L4, depends on deep-research-agent + prompt-optimizer + research-prompt-optimizer)
  ├─► (3)  references/MODE_*.md bundled into sc-implement, sc-research
  ├─► (4)  skills/readme.md index updated
  ├─► (5)  manifest regenerated
  └─► [PR opened; merge to main]

Task B session (sequential — only after Task A merged)
  ├─► AGENTS.md citation rewrite (FR4)
  ├─► RESEARCH.md §7 addition (FR5)
  └─► [PR opened; merge to main; Phase 1 complete]
```

**Critical-path observation**: 13 of the 14 skills can be authored in parallel inside Task A (no inter-skill writes block each other once the validator is extended). Only the `skill_references_skills` validation requires sibling folders to exist — and `tools/lint-linkage.py` runs at the commit boundary, not per-file, so authors can write all 14 SKILL.md files before running the linker. Suggested batching: 1 commit for validator extension + tests, 1 commit per skill group (L1 leaves, L2 mid, L3/L4 top), 1 commit for readme + manifest. Total ≈ 4–5 commits per Task A; 1 commit per Task B.

### 10.7 Verification recipe (end-to-end)

After both Tasks merge, the operator MUST be able to run the following and have every check pass:

```bash
# 1. Bootstrap
./install.sh
tools/check-governance.sh

# 2. ADR validation
python3 tools/adr/cli.py validate decisions/0011-external-skill-corpora-import.md

# 3. Validator regression + new key
python3 tools/fm/validate.py skills/
python3 tools/fm/query.py type=spec has-key=skill_source
# expected output: 14 paths under skills/sc-*/SKILL.md; none under bare-slug folders

# 4. Body cap
python3 tools/fm/validate.py --check-body skills/sc-*/SKILL.md

# 5. Audit graph
python3 tools/lint-linkage.py skills/sc-*/
# expected: every skill_references_skills entry resolves; reciprocity computed

# 6. Manifest
bash skills/skills-skill-bootstrap/verify.sh
# expected: 14 new entries in .skills-manifest.json, each with skill_kind populated

# 7. Root-spec hookup
grep -n "src/superclaude/commands/createPR.md" AGENTS.md   # expected: zero matches
grep -n "skills/sc-createPR/SKILL.md" AGENTS.md            # expected: ≥1 match
grep -n "## 7. Skill-driven research runs" RESEARCH.md     # expected: 1 match

# 8. Polarity
python3 tools/check-rfc2119-polarity.py AGENTS.md RESEARCH.md
# expected: zero new diagnostics vs pre-Phase-1 baseline

# 9. Smoke test (manual, in Claude Code)
# Invoke the Skill tool with skill="sc:createPR" — expected: the local body fires
# Invoke the Skill tool with skill="sc:research" — expected: WebSearch path runs without Tavily
```

If every step passes, Phase 1 is **done** and CLAUDE.md §13's five-skill promise is fully resolved. The repo now has 22 → 36 skills (+14), one new accepted ADR (0010), a validator extension, and two updated root specs.

### 10.8 Handoff to `/sc:implement`

Per `/sc:design` boundaries: this section is design only, no implementation code or SKILL.md bodies are written here. The implementer should now invoke `/sc:implement` with this section as input, and execute in this order:

1. **Session 1 (ADR)** — draft `decisions/0011-external-skill-corpora-import.md` from §10.1 verbatim. Validate, flip to Accepted, run `tools/adr/cli.py synthesize`, commit, open PR. Merge before Session 2.
2. **Session 2 (Task A)** — file `tasks/<NNN>-port-superclaude-phase-1-corpus/` per §10.5 Task A; execute the 11-step plan; open PR. Merge before Session 3.
3. **Session 3 (Task B)** — file `tasks/<NNN+1>-port-superclaude-phase-1-hookup/` per §10.5 Task B; execute the 7-step plan; open PR. Merge to complete Phase 1.

After Phase 1 merges, the next brainstorm/design cycle picks up Phase 2 (workflow loops: TDD discipline, systematic debugging, writing-plans, reflect-into-friction-log).

### 9.8 Out of scope for Phase 1

- Phase 2 (workflow loops: TDD discipline, systematic debugging, writing-plans, reflect-into-friction-log) — sequenced next.
- Phase 3 (remaining must-haves + Superpowers corpus) — sequenced after that.
- Auto-sync from upstream — future ADR.
- MCP installer packaging — Agency does not ship installers.
- Modifying root specs other than AGENTS.md (CR.1.1 paragraph) and RESEARCH.md (new §) — any other root-spec change is a T3 structural edit and MUST be filed as its own Task per `MAINTENANCE.md §1`.

### 9.9 Handoff

Next step per `/sc:brainstorm` boundaries: when the open questions (§9.7) are resolved, invoke **`/sc:design`** to convert this requirements spec into a per-skill body design (header structure, references/ layout, exact tool-bundle entries, exact root-spec citation diff). After `/sc:design`, the Phase-1 Task file from §5.1 (re-scoped to the 14-item batch) can be written and execution begins.
