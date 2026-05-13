---
type: note
status: archived
slug: roundtable-7-ontology-locks-recap
summary: >
  Historical recap of Roundtable 7. Superseded by /migration/ in Roundtable 8.
  L11.43 captured below is the ORIGINAL form (12 types except ADR,
  <slug>-<ulid>/ folder shape) — revised same-session-sequence to tasks-only
  with bare-slug + frontmatter ULID. See /migration/handover.md.
created: 2026-05-13
updated: 2026-05-13
session_branch: claude/repo-refactoring-plan-CfLY5
session_phase: superseded
---

> **SUPERSEDED — see [`/migration/`](../../migration/)**
>
> Roundtable 8 revised L11.43 to tasks-only with bare-slug folders + frontmatter
> ULID, and introduced L11.44 (auto-generated readmes). This document captures the
> Roundtable 7 state only and is retained as a historical snapshot. The current
> plan-of-record is [`/migration/handover.md`](../../migration/handover.md). Do not
> edit this file further; supersede via the migration workspace.

# Roundtable 7 — Ontology Locks & Open Questions

This document is the **historical recap** of Roundtable 7. As of Roundtable 8 (2026-05-13), the plan-of-record is [`/migration/`](../../migration/); content below is preserved for audit only.

File is `type: note` and lives in `.claude/plans/` — outside the 12-type governance scope, so it carries a bare-slug filename matching its sibling plan files (`agency-refactor-plan.md`, `round-10-additions.md`, etc.). The ULID convention pinned in L11.43 applies to operational artifacts of the 12 first-class types only.

---

## 1. Session arc — how we got here

Roundtable 7 picked up from Roundtables 1–6 (`.claude/plans/agency-refactor-plan.md`, `plan-rethink-overview.md`, `round-10-additions.md`, `synthesis-gemini-1-2.md`). Prior locks L1–L11.32′, L11.36, L11.37 in place from earlier rounds.

This round resolved a structural ambiguity left over from R6: the artifact-type ontology had been pinned at 7 base types but **promotion candidates** (role, lock, gherkin, friction-log, hook) were sitting in limbo — sometimes treated as first-class artifacts, sometimes as embedded sections. Gemini's eight-decision table (D1–D8 below) forced the question.

Round closed with:
- A **12-type ontology** (7 base + 5 promoted).
- A **three-mode placement model** (STANDALONE / SUBFILE / SUBDOC).
- A **ULID-prefixed folder convention** (L11.43) with an **archive-first migration policy** — all current artifacts move to a new top-level `archive/` mirror; the live tree starts fresh.

---

## 2. Locks confirmed this round

All locks below are **accepted** by the user. They are not yet codified in ADR form — that's the next step (Q5 in §3).

### L11.32‴ — 12 first-class artifact types

Supersedes L11.32′ (which pinned 7).

**Base (7, unchanged from L11.32′):**
1. `task` — orchestration / coordination unit
2. `prompt` — executable instruction set for an agent
3. `research` — evidence + synthesis workspace
4. `skill` — reusable agent capability
5. `adr` — architecture decision record
6. `spec` — root governance specification
7. `readme` — folder navigation index

**Promoted (5, new this round):**
8. `role` — agent-persona definition (was: embedded in prompts)
9. `lock` — design-decision checkpoint (was: embedded in plan notes)
10. `gherkin` — acceptance-scenario artifact (was: embedded in spec bodies)
11. `friction-log` — FL0–FL3 friction record (was: embedded in PR body / research reflection)
12. `hook` — Claude Code event hook (was: `tools/hooks/<event>.sh` + `.claude/settings.json` only, no graph edge)

**Rationale per promoted type:** each was being authored, referenced, or audited as if first-class, but the graph layer had no edge type for it. Cross-references degraded to body-Markdown links (which the linker ignores). Promotion creates explicit edges.

### L11.36′ — Three placement modes

Every artifact type declares which modes it permits via `templates/<type>/manifest.yml`:

| Mode | Storage | Frontmatter | Example |
|---|---|---|---|
| **STANDALONE** | own folder under `/<type>/<id>/` | top-of-file YAML | `tasks/decouple-architecture-01KRH6J3Y4B2YPD0X276D2GEBY/task.md` |
| **SUBFILE** | own file inside another artifact's folder | top-of-file YAML in the subfile | `tasks/foo-01K.../scenarios/login.gherkin.md` |
| **SUBDOC** | embedded in another artifact's body | Pandoc fenced div with YAML | a `:::{.gherkin id=...}` block inside `task.md` |

Constraint: every type permits at least STANDALONE; SUBFILE / SUBDOC are per-type opt-ins (matrix Q2 in §3).

### L11.37′ — SQLite uniform across modes

Single graph DB at `tools/graph/agency.db`. Schema:

```sql
artifacts(
  id TEXT PRIMARY KEY,           -- <slug>-<ulid> per L11.43 (see below)
  type TEXT NOT NULL,            -- one of the 12
  placement_mode TEXT NOT NULL,  -- 'standalone' | 'subfile' | 'subdoc'
  parent_id TEXT,                -- NULL for standalone; FK for subfile/subdoc
  path TEXT NOT NULL,            -- repo-relative file path
  ulid TEXT NOT NULL,            -- canonical 26-char ULID extracted from id
  slug TEXT NOT NULL,            -- human-readable slug extracted from id
  created_at DATETIME NOT NULL,  -- derived from ULID prefix; kept for query
  updated_at DATETIME NOT NULL
)
edges(
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  PRIMARY KEY (source_id, target_id, edge_type)
)
subdocument_locations(           -- regenerable cache for SUBDOC mode
  artifact_id TEXT PRIMARY KEY,
  parent_path TEXT NOT NULL,
  fenced_div_id TEXT NOT NULL,
  byte_offset_start INTEGER,
  byte_offset_end INTEGER
)
```

Invariant: edges are mode-blind. A `task_uses_prompts` edge from a standalone task to a subdoc prompt works identically to one between two standalone artifacts.

### L11.38′ — Subdoc syntax = Pandoc fenced divs

```markdown
:::{.prompt id=draft-pr-body-01KRH6J3 type=prompt status=draft}
---
slug: draft-pr-body
summary: Prompt for drafting the PR body after a session closes.
created: 2026-05-13
updated: 2026-05-13
---
# Body content here...
:::
```

Subfile syntax = standard top-of-file YAML frontmatter (unchanged from current Agency convention).

### L11.39′ — Mode-aware CLI surface

```
agency new <type> [--mode standalone|subfile|subdoc] [--in <parent-path>] --slug <slug>
agency extract <subdoc-id> --to standalone   # promote SUBDOC → STANDALONE
agency edit <id>                              # frontmatter mutation, mode-aware
agency promote <id> --to <new-mode>           # mode transition with edge rewrite
agency archive <id> [--all]                   # move artifact(s) to archive/ tree
```

`agency promote` rewrites all inbound edges in SQLite + body-Markdown anchor references in real time.

### L11.40′ — Lock placement

Locks are STANDALONE-only artifacts under `decisions/locks/<slug>-<ulid>.md`. Content-addressed via `lock_sha` (SHA-256 of body bytes). No SemVer (per Gemini D3 — locks are checkpoints, not versioned packages; supersession via successor lock that references `lock_supersedes: <previous-id>`).

### L11.41′ — Hook placement

Hooks are STANDALONE-only artifacts under `tools/hooks/<event>/<slug>-<ulid>/`. Each hook folder MUST contain `hook.md` (the artifact) + `<event>.sh` (the executable shim) + `_<event>.py` (the Python module). Registration in `.claude/settings.json` continues to use the `${CLAUDE_PROJECT_DIR}` exec form (D.7 enforcement unchanged from ADR-0011).

### L11.42 — Strict closed schemas

No `notes:`, no `extra:`, no `metadata:` escape hatches in any frontmatter schema (per Gemini D8). Every key declared in the namespace registry. Forward compatibility via schema versioning, not free-form blobs.

### L11.43 — ULID-prefixed folder convention

**Pinned this turn via four-question AskUserQuestion sequence.**

- **Identifier shape:** `<slug>-<ulid>/` for folders, `<slug>-<ulid>.md` for files. ULID is 26-char Crockford base32, full form. Example: `tasks/decouple-architecture-01KRH6J3Y4B2YPD0X276D2GEBY/`.
- **Scope:** all 12 first-class types EXCEPT `adr`. ADRs retain MADR 4.0.0 canonical `<NNNN>-<slug>.md` form. `.claude/plans/*.md` (type=note) and other non-12-type files retain bare-slug convention.
- **Display in prose & CLI:** `<slug>-<first-8-of-ulid>` (e.g. `decouple-architecture-01KRH6J3`). Resolver expands the 8-char ULID prefix to the full 26-char ID. `agency open <slug>-<8-char>` works.
- **Migration policy:** **archive-first big-bang.** Create a new top-level `archive/` folder mirroring current operational paths (`archive/tasks/000-decouple-architecture/`, `archive/prompts/<slug>/`, etc.). Move every current artifact there with `status: archived` set in frontmatter. Live tree (`tasks/`, `prompts/`, `research/`, `skills/`, `roles/`, `tools/hooks/`, `decisions/locks/`) starts fresh; only new artifacts get the ULID convention. Frontmatter audit graph remains queryable across both archive and live trees.
- **SQLite:** `artifacts.id` = `<slug>-<ulid>` (compound primary key). `ulid` and `slug` columns denormalized for cheap lookups. `created_at` denormalized from ULID timestamp prefix for query convenience.

**Why ULID over wall-clock timestamps (the candidate L11.43‴ that was rejected):**
- ULID first 48 bits = ms timestamp → lexical sort still yields creation order (when extracting ULID component).
- 80 bits of randomness → collision-free without coordination, even for same-ms parallel mints.
- Fixed 26-char width → predictable parsing, no collision-suffix policy needed.
- Crockford base32 excludes I/L/O/U to avoid visual ambiguity.
- Slug-first ordering (`<slug>-<ulid>`) means `ls` output sorts by topic; creation order recoverable from ULID prefix in SQLite when needed.

---

## 3. Open questions — pending user decision

These BLOCK ADR drafting. Each has a recommendation but requires user confirmation.

### Q2 — Permissible modes per type (the manifest matrix)

For each of the 12 types, which of STANDALONE / SUBFILE / SUBDOC are permitted? Draft matrix:

| Type | STANDALONE | SUBFILE | SUBDOC | Notes |
|---|---|---|---|---|
| task | required | – | – | Tasks must be standalone (orchestration entry point) |
| prompt | yes | yes | yes | Most flexible — already authored in all three forms in the wild |
| research | required | – | – | Research workspaces are immutable on close; standalone only |
| skill | required | – | – | Skills mirror external corpora; standalone canonical |
| adr | required | – | – | MADR convention |
| spec | required | – | – | Root specs are top-level files |
| readme | required | – | – | One per operational folder |
| role | yes | yes | yes | OPEN — should role allow SUBDOC inside prompt? |
| lock | required | – | – | Per L11.40′ |
| gherkin | yes | yes | yes | OPEN — SUBDOC inside spec (current pattern) vs SUBFILE under `scenarios/` |
| friction-log | yes | yes | – | SUBFILE under `/research/<slug>/reflection/` is current pattern |
| hook | required | – | – | Per L11.41′ |

Recommendation: restrict SUBDOC to four types where it adds value (prompt, role, gherkin, friction-log); ban it elsewhere to keep the graph easy to walk.

### Q3 — `agency promote` edge-rewrite semantics

When SUBDOC promotes to STANDALONE (or vice versa):
- (a) Edges follow automatically — SQLite updates `placement_mode` + `parent_id`, body-Markdown anchors get rewritten in the parent.
- (b) User confirms each rewrite via `AskUserQuestion`.
- (c) Promotion is staged — generates a diff, user reviews, then commits.

Recommendation: **(a)** for non-destructive promotions; **(c)** when promotion would break an inbound edge that crosses a closed-research T4 boundary.

### Q4 — Parallel-edit locking

When two agents simultaneously edit different SUBDOCs inside the same parent file:
- (a) File-level lock via `tools/fm/edit.py` (current behavior; second agent waits).
- (b) Byte-range CRDT — both edits land if non-overlapping.
- (c) Optimistic — both commit, conflict resolved at git layer.

Recommendation: **(a)** — keep `tools/fm/edit.py` invariant; parallel agents on the same parent are rare enough that serializing is fine.

### Q5 — `assumption-entry` as the 13th type?

Currently every operational `readme.md` carries `## Assumptions Log`. Promotion candidate: each assumption becomes a queryable artifact with its own ID + edges (e.g. `assumption_invalidated_by: <task-id>`).

Tradeoff: 13 types is one beyond comfortable "Miller-7±2 doubled" range; assumptions are high-volume (potentially hundreds per repo).

Recommendation: **defer** to a future roundtable. Keep assumptions as Markdown bullets inside readme bodies for now; revisit if the audit graph starts needing assumption-level edges.

### Q6 — Next move

User can choose:
1. **Continue locking** — answer Q2–Q5 in sequence, then close R7.
2. **Consolidate to draft ADR** — write `decisions/00XX-twelve-type-ontology-three-mode-placement.md` now, with Q2–Q5 as "Open Issues" inside.
3. **Cascade into root specs** — update `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `SKILLS.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `AGENTS.md`, `CLAUDE.md` to reflect the 12-type + three-mode + ULID-folder model.
4. **Build the migration tooling first** — write `agency archive`, `agency new`, `agency promote` CLI verbs; build the `archive/` mirror; verify on a sample subset before committing to big-bang.
5. **Close the session** — write FL declaration, index-sync, open PR per CR.1–CR.7; locks survive in this document and operationalize in a follow-up Task.

---

## 4. Cited evidence — Gemini D-table

For the ADR's evidence appendix, the eight Gemini decisions that anchored this round:

- **D1** — Promoting role/lock/gherkin/friction-log/hook to first-class types is correct; the graph layer needs the edges.
- **D2** — Three-mode placement (standalone/subfile/subdoc) is the right factoring; do NOT collapse to standalone-only.
- **D3** — Locks are content-addressed checkpoints, not versioned packages; no SemVer.
- **D4** — Pandoc fenced divs are the right SUBDOC syntax (vs MDX, vs HTML data attributes); plain Markdown with a known AST.
- **D5** — SQLite is sufficient; do not introduce a graph DB (Neo4j, Memgraph) for this scale.
- **D6** — `subdocument_locations` MUST be regenerable from a full repo scan; never the source of truth.
- **D7** — `agency promote` is a first-class CLI verb, not a generic `agency move`.
- **D8** — Closed schemas everywhere; no `notes:` / `metadata:` / `extra:` escape hatches.

---

## 5. Artifacts touched / to-touch in cascade (Q6 option 3 + 4)

If user picks Q6 option 3 (cascade) and/or option 4 (tooling), the following files need edits:

### Tooling (Q6 option 4 — recommended sequencing FIRST)

| File | Change |
|---|---|
| `tools/cli/agency.py` (new) | `agency new`, `extract`, `edit`, `promote`, `archive` verbs |
| `tools/cli/ulid.py` (new) | ULID mint + short-prefix resolver (stdlib only) |
| `tools/graph/migrate-to-ulid.py` (new) | One-shot migration: move artifacts to `archive/`, mint ULIDs for the live tree |
| `tools/fm/validate.py` | add `--check-mode` flag enforcing manifest matrix; recognise `<slug>-<ulid>` id format |
| `tools/check-governance.sh` | add step `[X] tools/fm/validate.py --check-mode` |
| `templates/` | add `role/`, `lock/`, `gherkin/`, `friction-log/`, `hook/` skeleton folders + `manifest.yml` per type |

### Root specs (Q6 option 3)

| File | Change |
|---|---|
| `AGENTS.md` | "Type matrix" section — list all 12 types, document three-mode model, update Skill Index by Category |
| `TASK.md` | §3 frontmatter namespace — add `task_subdoc_locations` array if tasks ever host SUBDOCs |
| `PROMPT.md` | §3 frontmatter namespace — add `prompt_placement_mode`; document fenced-div SUBDOC syntax |
| `RESEARCH.md` | confirm research is STANDALONE-only; document |
| `SKILLS.md` | confirm skill is STANDALONE-only; cross-reference manifest matrix |
| `FOLDERS.md` | §1 operational folders — add `roles/`, `decisions/locks/`, `tools/hooks/<event>/<slug>-<ulid>/` paths; update §4.1 scaffold rules per type; document `archive/` top-level folder |
| `PRE_COMMIT.md` | §7 governance checks — add mode-validation check |
| `CLAUDE.md` | §1 "What this repository is" table — extend from 4 concepts to 12; §12 topology — add `archive/`, `roles/`, `tools/hooks/<event>/` |
| `decisions/00XX-*.md` (new ADR) | consolidates L11.32‴ through L11.43 with evidence appendix |

Estimated scope: one Task per cluster (tooling, specs, ADR); ~10–15 commits total; surfaces in PR for review.

---

## 6. Frustration log (running)

Session FL so far: **FL0** — design conversation proceeding cleanly, one minor friction event noted (initial L11.43‴ timestamp proposal accepted, then revised to ULID one turn later; cost was negligible since the lock had not been promoted to an ADR yet). Will be promoted to a formal `friction-log.md` per CR.1 at session close.

---

*End of plan.*
