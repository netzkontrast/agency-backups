---
type: task
status: active
slug: cleanup-dramatica-skills-corpus
summary: "Clean up corrupted, empty, and PDF-artifact-bearing entries in dramatica-theory + dramatica-vocabulary; extend the navigator tooling so creating, editing, deprecating, alias-loading, and scenario-tagging are mechanical; pre-compile encoding hints so novel-architect and ncp-author consume structured payloads instead of prose. Subtasks dispatch to specialised subagents via /sc:agent. The subtask-format / sub-prompt-format / subagent-dispatch / /sc:* conventions used here are PROVISIONAL and tracked for ratification by Task 029."
created: 2026-05-05
updated: 2026-05-05
task_id: "030"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes: []
task_superseded_by: []
task_blocked_by: []
task_affects_paths:
  - skills/dramatica-theory/
  - skills/dramatica-vocabulary/
  - tools/dramatica-nav/
  - maintenance/schemas/narrative-ontology/
  - tasks/030-cleanup-dramatica-skills-corpus/
---

# Task 030 — Cleanup Dramatica Skills Corpus + Tooling Extension

## Goal

The dramatica corpus is operational but degraded. **Phase 0 (now)** of this task delivers four observable outcomes; the Task is `done` when ALL four hold simultaneously:

1. **Corpus is artefact-free.** `tools/dramatica-nav/cleanup.py --check` (delivered by ST-3) reports zero PDF page-break footers, zero stray page-number lines, zero double-apostrophe escapes, zero broken-parenthesis headings, zero "See X" empty redirect entries across `skills/dramatica-theory/references/*.md` and `skills/dramatica-vocabulary/references/*.md`. Concrete starting baseline: ≥38 copyright footers in vocabulary, ≥324 page-number artefacts in theory chunks, 1 broken `## Sex)` heading, 2 empty "See Intuitive / See Logical" redirects, 8 known `term_file` anchor mismatches.
2. **Anchors and frontmatter agree.** `tools/dramatica-nav/validate.py` reports zero `term_file-anchor-mismatch` warnings AND zero `unmapped-heading` warnings for canonical kinds (`element`, `variation`, `type`, `archetype`, `class`, `throughline`, `character-dynamic`, `plot-dynamic`, `concept`). The 17 partial-quad-membership warnings remain (they require an OQ-X schema decision deferred to Task 029) and are acknowledged as accepted v0.1 limitations.
3. **Tooling is mechanical.** Four new scripts under `tools/dramatica-nav/` (`term.py`, `aliases.py`, `cleanup.py`, `precompile.py`) cover the create / edit / deprecate / alias-load / scenario-tag / encoding-hint-precompile workflows. Deprecation is a subcommand on `term.py` (`term.py deprecate …`), not a standalone script — see ST-5's CLI surface. Each ships with smoke tests under `tools/dramatica-nav/tests/`. The hand-edit path remains supported but is no longer required for any of those workflows.
4. **Consumer-side payloads exist.** `maintenance/schemas/narrative-ontology/precompiled/` contains one JSON file per persona scenario (`novel.crucial-element-audit.json`, `lyric.verse-chorus-pair.json`, …) holding the pre-compiled element/variation payload `novel-architect` and `ncp-author` need. Each file passes a new `precompiled.schema.json` and is regenerated idempotently from the ontology. **Bytes loaded** for a typical `novel.crucial-element-audit` query drop from "load the navigator + the prose section" (≈3–5 KB) to "load one precompiled JSON" (≈1 KB target). The acceptance gate `CL.1.5` measures bytes (not tokens) — for plain-ASCII JSON+prose the two are within 5%, but the byte measurement is unambiguous and the only thing the smoke tooling can assert directly.

**Phase 1 deferrals (out of scope here, captured for Task 029 to ratify):** schema bumps for term-level deprecation lifecycle, multi-quad encoding (`quad_ids: array`), structured `encoding_hints` field on the term schema. These are ontology-extension decisions that the ADR-governance research must surface BEFORE we cement them.

## Background — Why This Task Exists

[Task 015](../015-integrate-dramatica-ncp-skills/task.md) integrated the dramatica skills with NCP and novel-architect via a Narrative Ontology, per-term frontmatter, and a Python navigator suite. Its [friction-log §Action items](../015-integrate-dramatica-ncp-skills/friction-log.md) surfaced three v0.2 follow-ups (OQ-X multi-quad / OQ-Y term_file anchor cleanup / OQ-Z DE-locale alias coverage) that were marked "can be standalone follow-up tasks; none are blockers for closing v0.1". This task absorbs all three.

The "Phase 1" schema-decision questions (deprecation lifecycle, multi-quad encoding, structured `encoding_hints` field) are deferred to main's ADR-governance pipeline — [Task 027](../027-adr-spec-research-synthesis/) (canonical ADR spec from the executed Gemini draft), [Task 028](../028-adr-tooling-impl-plan/) (ADR tooling impl plan), and [Task 029](../029-adr-assumption-audit/) (assumption audit). The FE-1…FE-10 items in this task's `notes.md §3` are intended inputs to Task 029.

**Per-subtask dependency on Task 028 (NOT task-level).** ST-5 and ST-6 — and only those two — depend on the `agency-adr` CLI tool suite that [Task 028](../028-adr-tooling-impl-plan/) ships (validate / synthesize / DAG / JSON-Schema linter / GHA integration). Concretely: ST-6's `cleanup.py` lint catalogue and ST-5's `term.py` deprecation lifecycle are natural callers of `agency-adr validate` and the JSON-Schema linter; the schema-bump procedure ST-5 surfaces (term-level `status: deprecated`) is precisely the kind of decision the `agency-adr` synthesise pipeline records as an ADR. The dependency is recorded in ST-5 and ST-6's `## Dependencies` sections as a **Pre-dispatch Gate** rather than as a task-level `task_blocked_by` so Phase A (ST-1…ST-4) and ST-7 / ST-8 / ST-9 can proceed without waiting for `agency-adr`. Per [PR #55 review C1](https://github.com/netzkontrast/agency/pull/55) and Assumption A-11.

This task adds:

- **PDF-artefact stripping** (not flagged in Task 015's friction log; only surfaced here when the user explicitly asked for a cleanup pass).
- **Empty redirect resolution** (`Female Mental Sex → See Intuitive`-style placeholder entries that produce useless navigator hits).
- **Tooling for the create/edit/deprecate workflows** (Task 015 shipped `nav.py`/`extract.py`/`validate.py`/`ontology-build.py` — all read-only; authoring still requires hand-editing 22 source files).
- **Precompiled persona-scenario payloads** (the SKILL.md describes "encoding suggestions" but they live in prose; novel-architect and ncp-author have to reconstruct them from scattered `## <Term>` sections every query).

The user's explicit framing: *"the Data in the skill is not that useful, because it lacks precompiled and extended relevance for the use within the novel-architect and ncp skill"*. Phase 0 closes the **mechanical** gap (corruption, anchors, tooling); Phase 1 (Task 027) closes the **schema** gap (deprecation lifecycle, multi-quad, encoding-hints).

## Personas and Working Scenarios (carried over from Task 015)

This task does NOT mint new persona scenarios. The eleven v0.1 scenarios in [`maintenance/schemas/narrative-ontology/scenarios.json`](../../maintenance/schemas/narrative-ontology/scenarios.json) remain canonical:

- Novel Author Anna: `novel.storyform-slot-fill`, `novel.act-pivot`, `novel.crucial-element-audit`, `novel.character-arc`, `novel.diagnose-flat-draft`, `novel.dual-storyform`.
- Organist Otto: `lyric.verse-chorus-pair`, `lyric.bridge-pivot`, `lyric.album-arc-mapping`, `lyric.archetype-as-system-part`, `lyric.refrain-as-restatement`.

What CHANGES in this task: each scenario gains a precompiled JSON payload (ST-9 deliverable) so an agent answering *"which Element-Pair drives Verse↔Chorus tension on this track?"* gets one structured response instead of having to walk five reference files.

## Plan

The plan is decomposed into **nine subtasks** dispatched via `/sc:agent` in three phases. Each subtask file under [`subtasks/`](./subtasks/) is self-contained per the Task 019 subtask convention (briefing + inputs + acceptance criteria + falsification clause + agent-prompt block).

```
Phase A — Mechanical Cleanup (parallel, low-risk):
  ST-1  strip-pdf-artifacts          — strip 38 copyright footers + 324 page-number lines + double-apostrophe escapes
  ST-2  fix-corrupted-headings       — fix `## Sex)`, mis-attributed YAML on Approach/Growth, truncated content blocks
  ST-3  fix-anchor-mismatches        — repair the 8 term_file mismatches from validate.py + reconcile 106 unmapped headings (split into ontology-adoptable vs. structural prose)
  ST-4  resolve-empty-redirects      — Female/Male Mental Sex pseudo-entries: delete or reify with proper data

Phase B — Tooling Extensions (parallel, depends on Phase A merging):
  ST-5  build-term-editor            — tools/dramatica-nav/term.py create/edit/move/deprecate with frontmatter+body coordination
  ST-6  build-cleanup-linter         — tools/dramatica-nav/cleanup.py --check / --apply for ongoing artefact prevention
  ST-7  bulk-alias-loader            — tools/dramatica-nav/aliases.py: parse _synonym-lookup.md → aliases_en; DE starter set hand-curated

Phase C — Content Coverage (sequential, depends on Phase B):
  ST-8  scenario-tag-coverage        — bring scenario coverage from 85 → ~250 entries (median ≤5 invariant from Task 015 holds)
  ST-9  precompile-encoding-hints    — emit one JSON per persona scenario; consumers (novel-architect, ncp-author) load these instead of prose
```

**Phase ordering rationale:** Phase A is read-only-on-the-ontology + write-only-on-source-files; A's outputs do not change the schema or any tool API. Phase B builds the tools whose first user IS Phase C. Phase C consumes both Phase A's clean corpus and Phase B's tools.

**Why /sc:agent specifically:** subtasks fan out to specialised subagent types (python-expert for code-heavy ST-5/ST-6/ST-7, refactoring-expert for ST-3 anchor reconciliation, technical-writer for ST-2's prose decisions, quality-engineer for ST-9 schema compliance). The `isolation: "worktree"` mode is appropriate for ST-5/ST-6/ST-7 (independent code surfaces) but NOT for ST-1/ST-2/ST-3/ST-4 (they touch overlapping markdown files and merge sequentially in the driver's main context).

### Critical-thinking decomposition (research-prompt-optimizer pattern)

Each subtask carries its own falsification clause: *what observation would prove this cut wrong?* Recorded in the subtask file and summarised here:

- **ST-1** wrong if "PDF artefacts" turn out to be load-bearing (e.g., a copyright footer that an agent expects to find as a section terminator). Mitigation: ST-1 first runs in `--dry-run` and the diff is human-reviewed; the regex set is locked in the subtask file.
- **ST-2** wrong if the broken headings encode dictionary information that a re-extraction from canonical PDF could recover. Mitigation: ST-2's brief explicitly forbids quoting >1 line of source prose; corrupted entries are either DELETED (with deprecation note) or repaired structurally only.
- **ST-3** wrong if the 106 unmapped headings are mostly intentional prose-only sections (essential-questions phases, encoding examples). Mitigation: ST-3 partitions the 106 into "ontology-adoptable" (must mint an ID + frontmatter) vs. "structural prose" (no ontology entry; document why). The subtask deliverable is the partition table, not a 106-row index.
- **ST-4** wrong if the Female/Male Mental Sex redirects are load-bearing for German-speaking authors who searched the historic vocabulary. Mitigation: ST-4 reifies them as `deprecated_aliases_en: ["Female Mental Sex", "Male Mental Sex"]` on the canonical `character-dynamic.problem-solving-style` entry instead of deleting outright.
- **ST-5** wrong if the term-editor surface conflicts with the existing `tools/fm/edit.py` ergonomics. Mitigation: ST-5's brief calls out the `tools/fm/` API contract and asks the subagent to prefer `tools/fm/edit.py` for frontmatter-only operations, only adding new behaviour for term-spanning operations.
- **ST-6** wrong if `cleanup.py` becomes a bottomless pit of ad-hoc regex bandaids. Mitigation: ST-6 ships a fixed v0.1 lint catalogue (the four rules listed in Goal §1) and refuses to grow without a Task 027 ADR.
- **ST-7** wrong if the synonym lookup contains alias entries that conflict with already-distinct ontology IDs. Mitigation: ST-7 first emits a conflict report; only conflict-free aliases are committed.
- **ST-8** wrong if scenario tagging at scale dilutes the median below the 5-tag M01 invariant from Task 015. Mitigation: ST-8 caps per-term tags at 8 (schema-enforced) AND at 4 (subtask-enforced) to leave headroom.
- **ST-9** wrong if the precompiled payloads turn out to be redundant with calling `nav.py by-scenario <id>` directly. Mitigation: ST-9 measures token cost of the two paths on the same set of queries; if the precompiled path doesn't beat `nav.py` by ≥40% on average, the precompiled artefacts are deleted and the task closes without §Goal item 4.

### Heavy /sc:* command usage

This task explicitly demands the following SuperClaude command surface:

- **`/sc:agent`** — primary subtask dispatcher. One call per subtask; Phase A subtasks fanned out as a single message containing four `Agent` tool invocations.
- **`/sc:research`** — invoked by ST-3's anchor-reconciliation pass when the 106 unmapped headings need cross-referenced against `dramatica-vocabulary/SKILL.md`'s Lookup-Disziplin discipline AND the original Phillips/Huntley canonical-list chapter (`references/09-reference.md`). One-shot per subtask, not iterative.
- **`/sc:improve --loop --iterations 3`** — used by ST-8 in the same shape Task 015 §Plan step 7 used it: bring scenario coverage up incrementally with an M01 median-tag-count gate after each iteration. Cap at 3 iterations per Task 015's empirical sweet spot.
- **`/sc:test`** — runs `pytest tools/dramatica-nav/tests/` after every subtask merges into the integration branch. Pre-commit gate for §Goal item 3.
- **`/sc:cleanup`** — invoked manually (not as part of any subtask) before commit on Phase A branches; lets the human reviewer see what `/sc:cleanup` would change vs. what ST-1/ST-2 changed deliberately.
- **`/sc:createPR`** — final action of the session per [`AGENTS.md § Closing Run Procedure`](../../AGENTS.md). MUST NOT fire unless `tools/check-governance.sh` exits 0.

**Provisional convention warning:** the precise dispatch syntax for `/sc:agent` (worktree vs. inline, max parallel count, output capture format) is currently inferred from Task 019's pattern. Task 029's audit output is expected to formalise it.

## Todo

- [ ] 1. Author this `task.md` (current step) — set `task_status: open`.
- [ ] 2. Author the nine subtask files under [`subtasks/`](./subtasks/) — one per ST. Each MUST include the four critical-thinking sections (briefing / inputs / acceptance / falsification) per the Task 019 convention and the agent-prompt block formatted for `/sc:agent` consumption.
- [ ] 3. Author the assumption log + frustration log in [`notes.md`](./notes.md) BEFORE any subtask dispatches. Per [`FRUSTRATED.md`](../../FRUSTRATED.md), the user explicitly asked for a verbose meta-frustration log of the planning session.
- [ ] 4. Spawn ST-1 / ST-2 / ST-3 / ST-4 (Phase A) via four parallel `/sc:agent` calls. Each subagent runs in main-tree (NOT worktree — they touch overlapping markdown files).
- [ ] 5. Wait for Phase A; review each subagent's commit; merge sequentially with conflict resolution. Run `tools/dramatica-nav/validate.py` after each merge.
- [ ] 6. Spawn ST-5 / ST-6 / ST-7 (Phase B) via three parallel `/sc:agent` calls, each in `isolation: "worktree"` (independent code surfaces, no markdown overlap).
- [ ] 7. Wait for Phase B; merge worktrees in order ST-6 → ST-5 → ST-7 (validation tooling first, then editor, then alias loader). Run `pytest tools/dramatica-nav/tests/` after each merge.
- [ ] 8. Spawn ST-8 (Phase C). Sequential `/sc:agent` call, NOT worktree (large markdown surface area touched).
- [ ] 9. Spawn ST-9 (Phase C). Sequential `/sc:agent` call in `isolation: "worktree"` (new artefact surface under `maintenance/schemas/narrative-ontology/precompiled/`).
- [ ] 10. Run the §Goal acceptance gate end-to-end: `tools/dramatica-nav/cleanup.py --check`, `tools/dramatica-nav/validate.py`, `pytest tools/dramatica-nav/tests/`, plus the ST-9 token-cost benchmark. Each MUST pass.
- [ ] 11. Append [`friction-log.md`](./friction-log.md) with the FL declaration per [`FRUSTRATED.md`](../../FRUSTRATED.md) — note this is a SEPARATE file from `notes.md`'s in-session meta-frustration log.
- [ ] 12. Set `task_status: done`. Run `tools/check-governance.sh`. If exit 0, invoke `/sc:createPR` per [`AGENTS.md § Closing Run Procedure`](../../AGENTS.md).
- [ ] 13. **Sibling-task linkage check:** confirm that main's [Task 029](../029-adr-assumption-audit/task.md) is `open` and verify this task's `notes.md §3` FE-1…FE-10 frustration items have been surfaced to that audit (either by direct reference in 029's task body or by an explicit comment in 029's research workspace).

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Cleaned-up dramatica corpus passes the four §Goal gates

  Background:
    Given skills/dramatica-theory/references/ and skills/dramatica-vocabulary/references/ exist
    And tools/dramatica-nav/ contains nav.py, extract.py, validate.py, ontology-build.py from Task 015
    And maintenance/schemas/narrative-ontology/ontology.json carries 304 entries

  # anchor: CL.1.1
  Scenario: PDF page-break artefacts are gone
    Given the corpus had 38 copyright footers and 324 page-number lines before this task
    When tools/dramatica-nav/cleanup.py --check runs
    Then the script MUST exit 0
    And the report MUST list 0 copyright-footer hits and 0 page-number-line hits

  # anchor: CL.1.2
  Scenario: All canonical-kind anchors resolve
    Given tools/dramatica-nav/validate.py runs after Phase A merges
    When the script completes
    Then the term_file-anchor-mismatch count for kinds {element,variation,type,archetype,class,throughline,character-dynamic,plot-dynamic} MUST be 0
    And the partial-quad-membership warning count MAY remain at 17 (deferred to Task 029)

  # anchor: CL.1.3
  Scenario: Empty redirect entries are reified or deleted
    Given character-dynamics.md previously carried "## Female Mental Sex" with body "See Intuitive Problem Solving Style"
    When ST-4 completes
    Then either the heading is deleted AND the alias "Female Mental Sex" appears in deprecated_aliases_en on character-dynamic.problem-solving-style
    Or the heading is reified with substantive prose conforming to the source's intent
    And tools/dramatica-nav/validate.py MUST report no unmapped-heading for that anchor

  # anchor: CL.1.4
  Scenario: Tooling covers the create/edit/deprecate/alias-load/precompile workflows
    Given tools/dramatica-nav/term.py (with `deprecate` subcommand), aliases.py, cleanup.py, precompile.py exist
    When pytest tools/dramatica-nav/tests/ runs
    Then every script MUST have ≥3 smoke tests (happy path + edge case + failure)
    And the test suite MUST pass with 0 failures

  # anchor: CL.1.5
  Scenario: Precompiled persona payloads beat prose loading on token cost
    Given maintenance/schemas/narrative-ontology/precompiled/novel.crucial-element-audit.json exists
    When an agent answers a typical novel.crucial-element-audit query via the precompiled path vs. the prose-only path
    Then the precompiled path MUST consume ≤60% of the bytes the prose-only path consumes
    And the same constraint MUST hold averaged across all 11 persona scenarios

  # anchor: CL.1.6
  Scenario: Heavy /sc:* usage is documented post-hoc
    Given Task 030 has dispatched 9 subtasks
    When friction-log.md is written
    Then the log MUST cite the exact /sc:agent / /sc:improve / /sc:test / /sc:createPR invocations made
    And ANY deviation from the conventions in §Plan MUST be logged as a friction event
```

## Anti-Patterns to Avoid

- **MUST NOT** quote >1 line of source Dramatica prose into ontology entries (preserves the © Screenplay Systems copyright-respect rule from Task 015 §Anti-Patterns).
- **MUST NOT** mint new ontology IDs for prose-only sections in `essential-questions.md`, `storyform-mechanics.md`, `encoding-patterns.md`, `element-quads.md` — they are workflow chapters, not term entries. ST-3 partitions them into "structural prose" explicitly.
- **MUST NOT** load `maintenance/schemas/narrative-ontology/precompiled/*.json` in non-narrative work (per [`AGENTS.md § Narrative Ontology` rule NO.5](../../AGENTS.md)). The precompiled layer extends the ontology; the loading rule extends with it.
- **MUST NOT** introduce a new `kind:` enum value without amending `maintenance/schemas/narrative-ontology/term-frontmatter.schema.json` AND `ontology.schema.json` AND filing a Task 027 follow-up. The schema bump procedure is OUT OF SCOPE for this task.
- **MUST NOT** treat the subtask format / sub-prompt format / `/sc:*` usage in this task as a precedent. They are PROVISIONAL pending [Task 029's audit output](../029-adr-assumption-audit/task.md). Conventions discovered as broken during this run go into the friction log for Task 029 to absorb.
- **SHOULD NOT** expand the precompiled JSON layer past the 11 v0.1 persona scenarios. New scenarios go through Task 015's frozen-at-v0.1 ID-mint procedure first.

## Links

- Predecessor (non-blocking): [`/tasks/015-integrate-dramatica-ncp-skills/`](../015-integrate-dramatica-ncp-skills/) — set up the Narrative Ontology + navigator that this task extends.
- Successor (research-spec request): [`/tasks/027-adr-spec-research-synthesis/`](../027-adr-spec-research-synthesis/) (Gemini-draft synthesis) and [`/tasks/029-adr-assumption-audit/`](../029-adr-assumption-audit/) (assumption audit consuming this task's FE-1…FE-10 frustration items) — produces the ADR-governance spec that ratifies the conventions used here.
- ADR-governance prompt (already executed externally on Gemini, owned by main): [`/prompts/agency-adr-governance-spec/`](../../prompts/agency-adr-governance-spec/) is a stub pointing at [`research/gemini/agency-adr-governance-spec/`](../../research/gemini/agency-adr-governance-spec/). This task does NOT spawn or execute that prompt; main's Task 027 synthesises the Gemini draft into the canonical ADR spec, and main's Task 029 absorbs assumption-audit material — both are upstream of any future ratification of the conventions used in this task.
- Sibling pattern reference: [`/tasks/019-fm-toolchain-suite-integration/`](../019-fm-toolchain-suite-integration/) — the `/sc:agent` subtask-decomposition pattern this task follows.
- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md).
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`FRUSTRATED.md`](../../FRUSTRATED.md).
- Skills touched: [`dramatica-theory`](../../skills/dramatica-theory/), [`dramatica-vocabulary`](../../skills/dramatica-vocabulary/), and consumer-side [`novel-architect`](../../skills/novel-architect/) + [`ncp-author`](../../skills/ncp-author/).
- Critical-thinking source: [`research-prompt-optimizer`](../../skills/research-prompt-optimizer/) — methods M01, M03, M04, M05, M07, M13, M0 applied above.
