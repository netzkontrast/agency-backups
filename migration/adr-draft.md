---
type: note
status: draft
slug: adr-draft-0013
summary: "Draft of ADR-0013 — Twelve-Type Ontology, Three-Mode Placement, Tasks-Only ULID, Auto-Generated Readmes. Status Proposed; Q1-Q7 in open-questions.md block promotion."
created: 2026-05-13
updated: 2026-05-13
---

# ADR-0013 (DRAFT) — Twelve-Type Ontology, Three-Mode Placement, Tasks-Only ULID, Auto-Generated Readmes

**This is the draft.** It is **not** in `decisions/` yet. It promotes there once [`open-questions.md`](./open-questions.md) Q1–Q7 are resolved and the corresponding sections below are filled in with user-confirmed answers. Promotion mints `adr_id: ADR-0013` and sets `adr_status: Proposed` (then `Accepted` when ratified).

When promoted, the frontmatter below replaces this draft preamble:

```yaml
---
type: adr
status: active
slug: 0013-twelve-type-ontology
summary: "12 first-class types, three placement modes, tasks-only ULID convention, auto-generated readmes; consolidates Roundtable 7+8 locks L11.32triple..L11.44."
created: 2026-05-13
updated: <promotion-date>
adr_id: ADR-0013
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - ontology
  - placement
  - identifier-convention
  - schema
  - cli
  - readme
  - locks
---
```

---

## Context and Problem Statement

Agency's artifact ontology, as ratified through Roundtables 1–6 (`.claude/plans/agency-refactor-plan.md`, `plan-rethink-overview.md`, `round-10-additions.md`, `synthesis-gemini-1-2.md`), pinned **7 first-class types** (`task`, `prompt`, `research`, `skill`, `adr`, `spec`, `readme`). Five additional concepts — `role`, `lock`, `gherkin`, `friction-log`, `hook` — were being authored, referenced, and audited in the wild as if first-class, but had **no graph edge type** in the audit linker. Cross-references degraded to body-Markdown links (which the linker ignores), and recurring confusion in roundtables 5–6 traced back to this ambiguity.

In parallel, Agency's identifier convention — `<NNN>-<slug>/` for tasks, bare `<slug>/` for prompts/research/skills, `<NNNN>-<slug>.md` for ADRs — produced two operational pains:

1. **Duplicate-NNN collisions** in `tasks/`. Tasks 013 and 024 share a slug; tasks 090 has two folders (`090-codex-pr-review` and `090-review-pr109-archive-spec`). Renaming-the-loser-to-the-next-number is repetitive friction with no graph benefit.
2. **Hand-written readmes drift** from their declared frontmatter. The "What and Why" prose, the link inventory, and the assumption log live in three different places; updates routinely synchronise only one.

Roundtables 7 and 8 closed both questions. This ADR consolidates the resulting **11 locks** (`L11.32‴` through `L11.44` plus Decision 4) into a single architectural commitment, citing the Gemini Deep Research brief (`research/gemini-architectural-audit-2/output/SPEC.md`) as evidence for each load-bearing decision.

## Decision Drivers

- **DD.1 Graph completeness.** Every artifact that participates in cross-references MUST be reachable via the linker. Body-Markdown links are for humans; the linker reads only frontmatter. Five promotion candidates currently degrade the graph.
- **DD.2 Migration safety.** ~30 in-flight tasks span multiple open PRs. Any naming-convention change MUST preserve existing paths so PR references, external citations, and git history remain navigable.
- **DD.3 Schema closedness.** Per Gemini D8, no `notes:` / `extra:` / `metadata:` escape hatches in any frontmatter schema. Forward compatibility lands via versioned schema additions through ADRs, not free-form blobs.
- **DD.4 Author ergonomics.** Folder names must remain readable when browsing the filesystem; references in prose must read as natural English; the audit graph must be queryable without memorising IDs.
- **DD.5 Reversibility.** First-class-type promotion is a T3 structural change. The ADR MUST be reversible — supersession via successor ADR, never edit-in-place.
- **DD.6 Tasks-only scope for ULID.** Adoption pain (~30 tasks needing archive + migration) is justified only where collision pain exists. Other types (prompts, research, skills, …) have bare-slug uniqueness without collision — no ULID benefit.
- **DD.7 Single source of truth for readmes.** Frontmatter is already authoritative for the audit graph. Extending it to carry narrative content (purpose, assumptions) lets the CLI render readmes deterministically — eliminating drift.
- **DD.8 Lock content-addressing.** Per Gemini D3, locks are checkpoints, not versioned packages. SHA-256 of body bytes is the identity; SemVer would imply mutable releases.

## Considered Options

### Option A — Keep 7-type ontology + body-Markdown for the 5 candidates

Status quo. `role`, `lock`, `gherkin`, `friction-log`, `hook` continue as body sections or sidecar files without first-class edge types.

- **Positives.** Zero migration cost. No schema delta.
- **Negatives.** Graph incompleteness perpetuates. Each roundtable re-litigates "is this a first-class concept?". Linker can't audit cross-references to these concepts; reviewers manually grep instead. Cost: ongoing high-cognitive-overhead.

### Option B — 12-type ontology + STANDALONE-only

Promote all 5 candidates to first-class with their own folders. No SUBFILE or SUBDOC mode. Every artifact lives in its own folder.

- **Positives.** Maximal graph clarity. Simple to lint.
- **Negatives.** Forces over-fragmentation. A prompt body that defines its required role inline (current pattern) must extract the role to a separate folder — adds 2-3 files per prompt. Edges multiply without semantic gain. Cost: high one-time migration + ongoing authoring friction.

### Option C — 12-type ontology + three-mode placement (CHOSEN)

Promote all 5 to first-class. Each type declares which of STANDALONE / SUBFILE / SUBDOC it permits via `templates/<type>/manifest.yml`. SUBDOC syntax = Pandoc fenced divs.

- **Positives.** Author keeps the natural form (role embedded in prompt; gherkin embedded in spec); audit linker still sees a first-class artifact. Migration via `agency promote` is non-destructive. Graph edges are mode-blind — no special-casing.
- **Negatives.** Per-type mode matrix introduces decision surface (resolved as **Q1**). SUBDOC byte offsets need a regenerable cache (`subdocument_locations`). Cost: medium one-time tooling + per-type matrix decision.

### Option D — 12-type ontology + dynamic placement (mode mutable post-creation without `agency promote`)

Same as Option C but `placement_mode` is a free-edit frontmatter field; any tool can transition artifacts between modes at any time.

- **Positives.** Maximum flexibility.
- **Negatives.** Edge integrity becomes a runtime-verification problem. Two parallel agents could mutate mode + edges into inconsistent states. Loss of `agency promote` as a single point of audit. Cost: high; fragile.

## Decision Outcome

**Chosen: Option C** — 12-type ontology + three-mode placement, with the following ratified locks. See [`migration/locks-ratified.md`](../migration/locks-ratified.md) for the canonical text of each lock.

1. **L11.32‴** — 12 first-class artifact types: 7 base (`task`, `prompt`, `research`, `skill`, `adr`, `spec`, `readme`) + 5 promoted (`role`, `lock`, `gherkin`, `friction-log`, `hook`).
2. **L11.36′** — Three placement modes: STANDALONE / SUBFILE / SUBDOC. Per-type matrix declared in `templates/<type>/manifest.yml`.
3. **L11.37′** — Single SQLite graph DB at `tools/graph/agency.db`. Edges are mode-blind. `subdocument_locations` is a regenerable cache, never source of truth (per Gemini D6).
4. **L11.38′** — SUBDOC syntax = Pandoc fenced divs with YAML inside (per Gemini D4).
5. **L11.39′** — Mode-aware `agency` CLI surface: `new`, `extract`, `edit`, `promote`, `archive`, `readme`.
6. **L11.40′** — Locks are STANDALONE-only under `decisions/locks/<lock-id>-<slug>.md`. Content-addressed via `lock_sha` = SHA-256 of body bytes below the frontmatter (per Gemini D3). No SemVer.
7. **L11.41′** — Hooks are STANDALONE-only under `tools/hooks/<event>/<slug>/`. Each folder has `hook.md` + `<event>.sh` + `_<event>.py`. Registration in `.claude/settings.json` continues per ADR-0011 §D.7.
8. **L11.42** — Closed schemas everywhere. No `notes:` / `extra:` / `metadata:` escape hatches (per Gemini D8).
9. **L11.43 (revised)** — **Tasks-only ULID convention.** Folder shape `tasks/<slug>/` bare slug. ULID lives in frontmatter `id:` field. Slug uniqueness enforced at `agency new` time. Prose references use slug alone with auto-disambiguation (short ULID prefix) only on collision. Migration is archive-first: current `tasks/<NNN>-<slug>/` move to `archive/tasks/<NNN>-<slug>/` preserving original NNN-slug names; live `tasks/` starts empty. **No retroactive ULID minting** for archived tasks.
10. **L11.44 (v2)** — **`agency readme` CLI auto-generates every operational readme.** Frontmatter is the sole source of truth. Schemas expand to carry the narrative content (`purpose`, `assumptions`) that previously lived in readme bodies. Pre-commit auto-regenerates touched readmes. Bidirectional edge rendering; `(none)` for zero-edge relations. Primary artifact files (`task.md`, `prompt.md`, `research.md`, `role.md`, etc.) remain hand-written; only the sibling `readme.md` is machine-rendered.
11. **Decision 4** — Per-type natural-fit ID convention for the 5 promoted types:
    - `role` → `roles/<slug>/role.md` — **new top-level operational folder**.
    - `lock` → preserves user-facing `L<round>.<sub>` notation in filename; slug field uses kebab-case for L1 conformance.
    - `gherkin` / `friction-log` / `hook` → defer detail to **Q6** in [`open-questions.md`](./open-questions.md).

## Consequences

### Positive

- **Graph completeness.** The 5 promoted types acquire explicit edges. Cross-references no longer degrade to body-Markdown.
- **Author ergonomics preserved.** Three-mode placement lets authors keep natural inlining; SUBDOC is a real audit-visible mode.
- **Tasks-only ULID minimises pain.** Only the surface with collision history pays the migration cost. 11 other types are unaffected.
- **Archive-first migration is reversible.** Worst case: revert the archive move, locks revert to draft, no in-flight Task disruption.
- **Auto-generated readmes eliminate drift.** Frontmatter is the source; readmes are derived.
- **Closed schemas anchor evolvability.** Versioned additions land via ADRs; no escape hatches.

### Negative

- **Schema-delta surface.** L1 type enum gains 5 values; L1 gains `purpose` + `assumptions`; new L2 schemas for `lock`, `role`, `gherkin`, `friction-log`, `hook`; `l2-readme.schema.json` (new) for auto-generation contract. Detailed in [`schemas-delta.md`](./schemas-delta.md).
- **Migration tooling gap.** `agency new`, `agency archive`, `agency promote`, `agency readme` do not exist. Each is a Task-scale piece of work.
- **Root-spec cascade.** TASK.md, PROMPT.md, RESEARCH.md, SKILLS.md, FOLDERS.md, PRE_COMMIT.md, AGENTS.md, CLAUDE.md all need updates to reflect 12 types + three modes + tasks-only ULID + auto-readmes. ~8 files; medium-sized PR.
- **`/migration/` workspace overhead.** A non-operational top-level folder lives in the repo until the migration executes.
- **Lock filename ↔ slug divergence.** Lock files use `L11.43-…md` filenames but kebab-case slugs. Either the L1 slug pattern relaxes for `type: lock`, or a per-type exception is encoded.

### Falsifier triggers

These convert ADR-0013 from `Accepted` back to `Proposed` (or trigger a successor ADR):

- **F.1** Any single open Question (Q1–Q7) blocks ratification for more than 2 weeks → re-open a roundtable; ontology may be wrong.
- **F.2** Migration cost (LOC + agent-time) exceeds 5× initial estimate → switch to incremental per-type migration.
- **F.3** Auto-generated readmes prove brittle (renderer produces unparseable output, frontmatter expansion balloons beyond ~3KB per artifact) → revert L11.44 to v1 (hand-written body + auto-managed nav block).
- **F.4** `subdocument_locations` cache invalidation produces real-world bugs (stale offsets crash agents) → reconsider SUBDOC mode entirely.
- **F.5** A 13th first-class type (e.g. `assumption-entry`) becomes load-bearing within 6 months → the 12-type ceiling was wrong; re-roundtable.

## Open Issues

Q1–Q7 in [`open-questions.md`](./open-questions.md). Each must close before this ADR promotes to `Accepted`. Listed here for ADR-internal cross-reference; canonical text + recommendations live in that file.

- **Q1** — Mode matrix per type
- **Q2** — `agency promote` edge-rewrite semantics
- **Q3** — Parallel-edit locking
- **Q4** — Slug-collision disambiguation tooling
- **Q5** — `assumption-entry` as the 13th type
- **Q6** — Natural-fit detail for `gherkin` / `friction-log` / `hook`
- **Q7** — Sequencing — ADR / cascade / tooling / close order

## Implementation cascade

When this ADR ratifies, the following land in dependency order:

1. **Schema deltas** ([`schemas-delta.md`](./schemas-delta.md)) — L1 type enum +5; L1 `purpose` + `assumptions`; new L2 schemas; regenerate mirrors via `tools/fm/gen_schema_mirror.py`.
2. **Lock files in `decisions/locks/`** — 11 lock files move from `/migration/locks-ratified.md` (consolidated) to per-lock standalone files. `decisions/locks/readme.md` created.
3. **`agency` CLI scaffolding** — `tools/cli/agency.py` with `new`, `archive`, `promote`, `readme` subcommands; `tools/cli/ulid.py` for ULID mint + short-prefix resolver.
4. **Migration runner** — `tools/graph/migrate-to-ulid.py`: one-shot script that moves `tasks/<NNN>-<slug>/` to `archive/tasks/<NNN>-<slug>/`, leaves the live `tasks/` empty, mints initial ULIDs for any task created post-migration.
5. **Root-spec cascade** — `AGENTS.md`, `CLAUDE.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `SKILLS.md`, `FOLDERS.md`, `PRE_COMMIT.md` updated to reference 12 types + three modes + tasks-only ULID + auto-readmes.
6. **Linter updates** — `tools/fm/validate.py` recognises new types; `tools/lint-structure.py` registers `roles/` + `decisions/locks/` + `tools/hooks/<event>/<slug>/` as operational; `tools/check-governance.sh` adds `agency readme --check` step.
7. **Cleanup** — `/migration/` deleted; banners removed from `CLAUDE.md` and `AGENTS.md`; this ADR's `adr_status` flips `Proposed → Accepted` after `python3 tools/adr/cli.py synthesize` runs.

## Evidence

Gemini Deep Research brief #2 (`research/gemini-architectural-audit-2/output/SPEC.md`) supplied 8 load-bearing decisions, each cited by ID in [`gemini-evidence.md`](./gemini-evidence.md):

- **D1** — Promoting `role` / `lock` / `gherkin` / `friction-log` / `hook` to first-class is correct (anchors L11.32‴).
- **D2** — Three-mode placement is the right factoring (anchors L11.36′).
- **D3** — Locks are content-addressed checkpoints, not versioned packages (anchors L11.40′).
- **D4** — Pandoc fenced divs are the right SUBDOC syntax (anchors L11.38′).
- **D5** — SQLite is sufficient; no graph DB (anchors L11.37′).
- **D6** — `subdocument_locations` MUST be regenerable, never source of truth (anchors L11.37′).
- **D7** — `agency promote` is a first-class CLI verb, not generic `agency move` (anchors L11.39′).
- **D8** — Closed schemas everywhere (anchors L11.42).

## Supersedes

- L11.43 *original* (Roundtable 7) — superseded by L11.43 *revised* (Roundtable 8) within this same ADR.
- L11.32′ + L11.32″ — superseded by L11.32‴ within this same ADR.

(These supersessions are intra-ADR consolidations of in-flight lock revisions, not supersessions of prior Accepted ADRs.)

## Assumptions Log

(none — assumptions belong to the locks themselves; see [`locks-ratified.md`](./locks-ratified.md) Assumption Log entries.)
