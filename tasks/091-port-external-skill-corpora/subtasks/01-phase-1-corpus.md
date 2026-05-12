---
type: note
status: active
slug: task-091-st1-phase-1-corpus
summary: "ST-1 (Task 091 Epic): extend tools/fm/validate.py for skill_source key + create 14 skill folders under skills/sc-*/ per ADR-0011 Phase 1. Corpus only; root-spec hookup deferred to ST-2."
created: 2026-05-12
updated: 2026-05-12
---

# ST-1 — Phase 1 Corpus (was "Task A" in §10.5)

**Executor:** main-agent (Claude Code with `/sc:implement`).

**Parallelism:** Sequential — ST-1 MUST complete and merge before ST-2 starts (per `../references/full-plan-part-3.md` §9.7 OQ1 resolution: split-into-2 Task shape).

**Depends on:** [ADR-0011](../../../decisions/0011-external-skill-corpora-import.md) at `adr_status: Accepted` (landed in commit `91d3949` on this branch).

**Spec:** [`../references/full-plan-part-4.md` §10.5 "Task A"](../references/full-plan-part-4.md) — the canonical 11-step plan, 4 Gherkin AC (`TA.1.1`–`TA.1.4`), per-skill design table (§10.3), validator extension details (§10.2), and build-order DAG (§10.6).

## Scope

- **Validator extension.** Extend [`tools/fm/validate.py`](../../../tools/fm/validate.py) per `../references/full-plan-part-4.md` §10.2:
  - Add constants `VENDOR_PREFIXES = ("sc-", "superpowers-")` and `SKILL_SOURCE_RE = re.compile(r"^(superclaude|superpowers)@v\d+\.\d+\.\d+$")`.
  - Add method `_check_skill_source(fm, relpath)` returning two new diagnostic codes:
    - `F.B.7` — ERROR — `skill_source` present on a bare-slug (native) skill (ADR-0011 D.1 violation).
    - `F.B.8` — ERROR — `skill_source` value does not match the regex (ADR-0011 D.2 violation).
  - Hook into the existing validator entry point alongside `_check_skill_bundles`.
  - Author 5 new tests under `tools/tests/test_validate_skill_source.py`:
    1. `test_skill_source_accepted_on_vendor_prefix` (vendor + valid value → 0 diagnostics)
    2. `test_skill_source_rejected_on_bare_slug` (bare slug + value → F.B.7)
    3. `test_skill_source_malformed_value` (vendor + `superclaude@latest` → F.B.8)
    4. `test_skill_source_absent_is_fine_for_natives` (bare slug + no key → 0 diagnostics)
    5. `test_existing_native_skills_still_validate` (regression over 22 existing skill folders → 0 diagnostics)
- **14 skill folders.** Create `skills/sc-<bare-slug>/` for each item in `../references/full-plan-part-4.md` §10.3 per-skill design table. Recommended landing order (L1 leaves first, then L2, then L3/L4):
  1. `sc-pm-agent`, `sc-backend-architect`, `sc-frontend-architect`, `sc-refactoring-expert`, `sc-performance-engineer` (L1 leaves)
  2. `sc-system-architect`, `sc-security-engineer`, `sc-quality-engineer`, `sc-deep-research-agent` (L2)
  3. `sc-createPR` (L4), `sc-test` (L3), `sc-improve` (L2), `sc-implement` (L3), `sc-research` (L4)
- **Modes as references.** Bundle `references/MODE_Orchestration.md` into `skills/sc-implement/` and `references/MODE_DeepResearch.md` into `skills/sc-research/` (ADR-0011 D.5).
- **MCP-free adaptation.** Rewrite `skills/sc-research/SKILL.md` body so WebSearch + WebFetch are the primary surface; Tavily appears only in `## Compatibility` marked OPTIONAL (ADR-0011 D.8). Archive verbatim upstream body to `skills/sc-research/references/upstream-sc-research.md`.
- **Skills index + manifest.** Update [`skills/readme.md`](../../../skills/readme.md) with a new "Imported from SuperClaude (v4.3.0)" section. Regenerate `.skills-manifest.json` via `bash skills/skills-skill-bootstrap/sync.sh --emit-manifest` (verify the exact invocation against `sync.sh`).

## Out of scope

- AGENTS.md citation rewrite — ST-2.
- RESEARCH.md §7 addition — ST-2.
- Superpowers corpus — Phase 2 (sequenced post-this-Epic).
- `sc:agent`, `sc:design`, `sc:analyze`, etc. — Phase 1 covers only the 5 dangling-reference skills + their 9 supporting agents (full rationale in `../references/full-plan-part-1.md` §2.1).
- MCP installer packaging — never in scope per Agency's "governance repo, not installer" position.

## Acceptance Criteria

Verbatim from `../references/full-plan-part-4.md` §10.5 Task A — anchors `TA.1.1`–`TA.1.4`:

- **TA.1.1** — All 14 skill folders exist with valid SKILL.md; `python3 tools/fm/validate.py skills/sc-*/` exits 0; each SKILL.md carries `skill_source: "superclaude@v4.3.0"`.
- **TA.1.2** — Validator extension does not regress existing skills: `python3 tools/fm/validate.py skills/` emits 0 ERROR diagnostics against the 22 pre-existing skill folders.
- **TA.1.3** — `sc-research` is Agency-adapted: `WebSearch` appears in `## How to use`; `Tavily` appears only in `## Compatibility` marked OPTIONAL; verbatim upstream body exists at `skills/sc-research/references/upstream-sc-research.md`.
- **TA.1.4** — Audit-graph reciprocity computed: manifest entry for `sc-system-architect` lists `referenced_by: [sc-implement]`; manifest entry for `sc-quality-engineer` lists `referenced_by: [sc-test, sc-improve]`.
  > **Status (ST-1 closure):** forward references are correctly declared in YAML (`skill_references_skills` on `sc-implement`, `sc-test`, `sc-improve`) and reciprocity is derivable via `grep -l <slug> skills/sc-*/SKILL.md`. The materialised manifest the AC asserts against (`.skills-manifest.json` or equivalent) **does not exist in the toolchain today** — `skills/skills-skill-bootstrap/sync.sh` has no `--emit-manifest` flag and `tools/fm/graph.py` does not crawl `skill_references_skills`. Manifest verification is deferred to a follow-up Task per the two closure paths documented in [`../friction-log.md` FL1.2](../friction-log.md). PR #115 ships ST-1 with forward refs in place; reciprocity-materialisation is a Phase-2 ADR-level scope.

## Branch + PR shape

Author on a **fresh branch** derived from `main` post-merge of this Epic-scaffold PR (#107). Do NOT continue on `claude/analyze-repo-architecture-KEvqh` — that branch is the ADR + Epic-scaffold, not the corpus implementation. PR title MUST cite this subtask, e.g. `Task 091 ST-1: Phase 1 corpus (14 sc-* skills + validator)`. PR body MUST include:

- The BR.9.5 size-cap verification command output (`python3 tools/fm/validate.py --check-body skills/sc-*/SKILL.md` exit 0).
- The TA.1.4 reciprocity verification output from the regenerated manifest.
- Friction-log declaration (FL0-FL3) per `FRUSTRATED.md`.
