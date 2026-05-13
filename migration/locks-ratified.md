---
type: note
status: active
slug: locks-ratified
summary: "Canonical text of all 11 user-confirmed locks from Roundtables 7-8 (L11.32triple..L11.44 + Decision 4). Promotes to decisions/locks/ when ADR-0013 ratifies."
created: 2026-05-13
updated: 2026-05-13
---

# Locks ratified — Roundtable 7 + 8

This file is the canonical text of every lock the user has confirmed for the 12-type ontology + three-mode placement + tasks-only ULID + auto-readme-generation refactor. Each lock is **binding** for the design but **not yet operationalised** — see [`handover.md`](./handover.md) §5.

---

## L11.32‴ — Twelve first-class artifact types

Supersedes L11.32′ (which pinned 7) and L11.32″ (which pinned 9).

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

Each promoted type was being authored, referenced, or audited as if first-class but had no graph edge type. Promotion creates explicit edges (e.g. `prompt_uses_role`, `task_references_locks`, `spec_defines_gherkin`).

---

## L11.36′ — Three placement modes

Every artifact type declares which modes it permits via `templates/<type>/manifest.yml`:

| Mode | Storage | Frontmatter | Example |
|---|---|---|---|
| **STANDALONE** | own folder under `/<type>/<id>/` (or own file at `<canonical-path>/<id>.md`) | top-of-file YAML | `tasks/decouple-architecture/task.md` |
| **SUBFILE** | own file inside another artifact's folder | top-of-file YAML in the subfile | `tasks/foo/scenarios/login.gherkin.md` |
| **SUBDOC** | embedded in another artifact's body | Pandoc fenced div with YAML | `:::{.gherkin id=login}` block inside `task.md` |

**Constraint:** every type permits at least STANDALONE — **except for the two types named in R3 below** (`gherkin` and `friction-log`), which are PARENTED-ONLY (SUBFILE / SUBDOC, no STANDALONE). SUBFILE / SUBDOC for the other 10 types are per-type opt-ins; the matrix is **Q1** in [`open-questions.md`](./open-questions.md). The R3 exception is documented in `§Revision history` below and reflected in the Q1 mode-matrix table in `open-questions.md`.

---

## L11.37′ — SQLite uniform across modes

Single graph DB at `tools/graph/agency.db`. Edges are **mode-blind** — a `task_uses_prompts` edge from a standalone task to a subdoc prompt is identical in shape to one between two standalone artifacts.

```sql
artifacts(
  id TEXT PRIMARY KEY,           -- canonical id; format per type (see L11.43 for tasks)
  type TEXT NOT NULL,            -- one of the 12
  placement_mode TEXT NOT NULL,  -- 'standalone' | 'subfile' | 'subdoc'
  parent_id TEXT,                -- NULL for standalone; FK for subfile/subdoc
  path TEXT NOT NULL,            -- repo-relative file path
  slug TEXT NOT NULL,
  ulid TEXT,                     -- canonical ULID where minted (tasks only per L11.43)
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
)

edges(
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  PRIMARY KEY (source_id, target_id, edge_type)
)

subdocument_locations(           -- regenerable cache for SUBDOC mode; never source of truth
  artifact_id TEXT PRIMARY KEY,
  parent_path TEXT NOT NULL,
  fenced_div_id TEXT NOT NULL,
  byte_offset_start INTEGER,
  byte_offset_end INTEGER
)
```

Per Gemini D6, `subdocument_locations` MUST be regenerable from a full repo scan; it is never the source of truth.

---

## L11.38′ — Pandoc fenced divs as SUBDOC syntax

```markdown
:::{.prompt id=draft-pr-body type=prompt status=draft}
---
slug: draft-pr-body
summary: Prompt for drafting the PR body after a session closes.
created: 2026-05-13
updated: 2026-05-13
---
# Body content here...
:::
```

Subfile syntax = standard top-of-file YAML frontmatter (unchanged from current Agency convention). Per Gemini D4, Pandoc fenced divs win over MDX / HTML data attributes because they parse via a known AST and degrade gracefully on Markdown-only renderers.

---

## L11.39′ — Mode-aware `agency` CLI surface

```
agency new <type> [--mode standalone|subfile|subdoc] [--in <parent-path>] --slug <slug>
agency extract <subdoc-id> --to standalone   # promote SUBDOC → STANDALONE
agency edit <id>                              # frontmatter mutation, mode-aware
agency promote <id> --to <new-mode>           # mode transition with edge rewrite
agency archive <id> [--all]                   # move artifact(s) to archive/ tree
agency readme <id> [--all] [--check]          # render readme.md from frontmatter (L11.44)
```

`agency promote` rewrites all inbound edges in SQLite + body-Markdown anchor references. Semantics still under **Q2** in [`open-questions.md`](./open-questions.md).

---

## L11.40′ — Lock placement

Locks are STANDALONE-only artifacts under `decisions/locks/<lock-id>-<slug>.md`. Content-addressed via `lock_sha` (SHA-256 of body bytes below the frontmatter). No SemVer — per Gemini D3, locks are checkpoints, not versioned packages. Supersession via successor lock that references `lock_supersedes: <previous-lock-id>`.

Per **Decision 4**, the `<lock-id>` portion preserves the user-facing `L<round>.<sub>` notation (e.g. `L11.43`). The slug remains kebab-case for L1 conformance — filename and slug differ where the lock notation introduces a dot or uppercase letter.

---

## L11.41′ — Hook placement

Hooks are STANDALONE-only artifacts under `tools/hooks/<event>/<slug>/`. Each hook folder MUST contain `hook.md` (the artifact) + `<event>.sh` (the executable shim) + `_<event>.py` (the Python module). Registration in `.claude/settings.json` continues to use the `${CLAUDE_PROJECT_DIR}` exec form (D.7 enforcement unchanged from ADR-0011).

The detailed natural-fit (multi-hook-per-event vs one-hook-per-event-file) is **Q6** in [`open-questions.md`](./open-questions.md).

---

## L11.42 — Closed schemas everywhere

No `notes:`, no `extra:`, no `metadata:` escape hatches in any frontmatter schema. Every key declared in the namespace registry. Forward compatibility via schema versioning (new keys land via ADR), not free-form blobs. Per Gemini D8.

---

## L11.43 (revised) — Tasks-only ULID convention

**Revision history:** the original L11.43 (Roundtable 7) applied ULIDs to all 12 types except ADR with `<slug>-<ulid>/` folder shape. Revised in Roundtable 8 to narrow scope and move the ULID into frontmatter.

- **Scope:** **tasks only**, permanently. Other types keep their current schemes — `prompts/<slug>/`, `research/<slug>/`, `roles/<slug>/`, `decisions/<NNNN>-<slug>.md`, `decisions/locks/<L-id>-<slug>.md`, `tools/hooks/<event>/<slug>/`, etc.
- **Folder shape:** `tasks/<slug>/` — bare slug. No numeric prefix, no ULID in the path.
- **Identity:** `id: 01KRH6J3Y4B2YPD0X276D2GEBY` in `task.md` frontmatter. Canonical for graph queries + SQLite primary key.
- **Slug uniqueness:** enforced at `agency new` time. Two tasks cannot share a slug in the live tree. Collisions force the user to pick a more specific slug.
- **Prose references:** slug alone (`decouple-architecture`) is the canonical form. Short-prefix ULID (`decouple-architecture-01KRH6J3`) is auto-appended **only** when disambiguation is required (e.g. a slug appears in both live and archived trees, or two simultaneous renames collide).
- **Migration:** archive-first. All current `tasks/<NNN>-<slug>/` move to `archive/tasks/<NNN>-<slug>/` **preserving the original NNN-slug name** (matches git history; no rename diff; existing PR / external references still resolve). Live `tasks/` starts empty. New tasks created post-migration use the new convention.
- **No retroactive ULID minting** for archived tasks. They retain `<NNN>-<slug>` paths and pre-migration frontmatter. Audit graph queries cross both trees transparently.

**Why ULID over wall-clock timestamps** (the rejected candidate L11.43‴):

- ULID first 48 bits = ms timestamp → lexical sort still yields creation order (when extracting the ULID component).
- 80 bits of randomness → collision-free without coordination, even for same-ms parallel mints.
- Fixed 26-char width → predictable parsing.
- Crockford base32 excludes I/L/O/U to avoid visual ambiguity.

---

## L11.44 (v2) — `agency readme` CLI auto-generates every operational readme

**Revision history:** the original L11.44 (Roundtable 8) proposed a hand-written body + auto-managed nav block inside marker comments. Revised same-session: **every readme.md is fully auto-generated**, end-to-end. No hand-written body content. Frontmatter is the **sole** source of truth.

- **Scope:** all operational folders — `tasks/<slug>/`, `prompts/<slug>/`, `research/<slug>/`, `roles/<slug>/`, `decisions/locks/`, `tools/hooks/<event>/<slug>/`, every other operational tree.
- **Trigger:** pre-commit auto-regenerates when any touched file's frontmatter changes. The block is always current at commit time.
- **Edge direction:** bidirectional. Each readme shows both outgoing edges (what this artifact declares it depends on) and incoming edges (what other artifacts point back at this one).
- **Empty handling:** every readme has the same shape; rows for zero-edge relations render `(none)` in the artifact cell. Predictable structure.
- **Source of truth:** frontmatter. Per the v2 revision, every piece of information that used to live in a hand-written readme body (the "What and Why" prose, the assumption log, the link inventory) **must** be representable in frontmatter. Schemas expand to carry it — see [`schemas-delta.md`](./schemas-delta.md) for the proposed L1 additions (`purpose`, `assumptions`).
- **Renderer output:** entire `readme.md` is machine-written. Top-of-file marker indicates auto-generation: `<!-- AUTOGENERATED by agency readme; edit frontmatter to change. -->`. The CLI's `--check` mode regenerates in-memory and exits non-zero if the on-disk file diverges from the rendered output.
- **Non-readme files unaffected.** `task.md`, `prompt.md`, `research.md`, `role.md`, etc. — the *primary* artifact files — remain hand-written. Only the sibling `readme.md` is auto-generated.

---

## Decision 4 — Per-type natural-fit ID convention for the 5 promoted types

Closes the question "what identifies role / lock / gherkin / friction-log / hook now that L11.43 is tasks-only?". Master rule: **each promoted type keeps the convention it already de-facto uses; no migration cost for naming.**

| Type | Convention | Folder shape | Status |
|---|---|---|---|
| `role` | slug, unique within type | `roles/<slug>/role.md` — **new top-level operational folder** | ratified |
| `lock` | preserve user's `L<round>.<sub>` notation | `decisions/locks/L<round>.<sub>-<slug>.md` | ratified |
| `gherkin` | existing `# anchor: <id>` scheme; SUBDOC or SUBFILE | `<parent>/scenarios/<scenario-slug>.gherkin.md` (SUBFILE) or `:::{.gherkin id=<id>}` (SUBDOC) | deferred (Q6 detail) |
| `friction-log` | parent + session-date | `<parent>/reflection/friction-log.md` (current pattern) | deferred (Q6 detail) |
| `hook` | event-name as primary key | `tools/hooks/<event>/<slug>/hook.md` per L11.41′ | deferred (Q6 detail) |

**Implication for `role`:** new top-level `roles/` operational folder. Affects `FOLDERS.md §1` and the `tools/lint-structure.py` registry of operational folders.

**Implication for `lock`:** filename `L11.43-twelve-type-ontology.md` retains user-facing notation; the L1 `slug` field uses kebab-case `l11-43-twelve-type-ontology` for schema conformance. Pre-commit must permit filename-↔-slug divergence for `type: lock` only — see [`schemas-delta.md`](./schemas-delta.md).

---

## Cross-references

- ADR draft: [`adr-draft.md`](./adr-draft.md) (ADR-0013, `Proposed`)
- Open questions: [`open-questions.md`](./open-questions.md)
- Schema deltas implied: [`schemas-delta.md`](./schemas-delta.md)
- Evidence appendix: [`gemini-evidence.md`](./gemini-evidence.md)
- Session arc: [`session-log.md`](./session-log.md)

## Revision history — answers given mid-session after waiver request

During the session that produced this folder, after the [`waiver.md`](./waiver.md) request was made, three more answers came in via `AskUserQuestion`. They are recorded here as **provisional** — the user interrupted the question round before confirming the full design implications. The next session should confirm or revise.

### R1 — Decision 4 reversed: all 5 promoted types adopt ULID

**Answer:** "All ULID-prefixed like tasks (extend L11.43)" — replaces the earlier "per-type natural fit" answer.

**Implication:** role, lock, gherkin, friction-log, hook each get a ULID in frontmatter. L11.43's "tasks only, permanently" scope was wrong; the correct scope is **task + 5 promoted = 6 types** carry ULID. Other 6 types (prompt, research, skill, adr, spec, readme) keep their current schemes.

**Cascade to L11.43:**

- **L11.43 (revised v2)** — ULID convention scope = **6 types**: `task`, `role`, `lock`, `gherkin`, `friction-log`, `hook`. Bare-slug folders (where the type uses a folder; lock and gherkin and friction-log are file-only). ULID lives in frontmatter `id:` field. Slug uniqueness enforced at `agency new` time per type. Prose references use slug alone with auto-disambiguation only on collision.
- **For lock specifically:** filename `L<round>.<sub>-<slug>.md` retains user-facing notation; the ULID lives **in addition** in frontmatter as the canonical graph identity. Both coexist — humans read `L11.43`, the linker reads the ULID.

**Status:** ratified by click; **not yet confirmed** by user after the implication "L11.43 v2 changes scope from tasks-only to 6 types" was surfaced.

### R2 — Lock round counter tracks design-conversation rounds

**Answer:** "Round = design-conversation round (Recommended)" — keeps the existing notation.

**Implication:** when Roundtable 7 closes and Roundtable 8 begins, lock numbering continues from `L11.x` to `L12.x` (assuming we treat each Roundtable as one round in the L11.x sense; or whatever increment user picks). The current locks are all in the L11.x family; the next round opens L12.x.

**Note:** the locks in [`locks-ratified.md`](./locks-ratified.md) above carry `L11.32‴`, `L11.36′`, …, `L11.44`. These are sub-counter `.32` through `.44` of round 11. The next conversation round (whatever the user opens) increments the round counter.

**Status:** ratified by click; consistent with current usage.

### R3 — Gherkin and friction-log are always parented

**Answer:** "Both always parented (Recommended)" — confirms the Q6 deferred-detail recommendation in [`open-questions.md`](./open-questions.md).

**Implication:** gherkin and friction-log artifacts MUST exist as SUBFILE or SUBDOC inside a parent (task / spec / research / prompt). STANDALONE is **not** permitted for these two types. Q6 partially closes.

**Cascade to the Q1 mode matrix in [`open-questions.md`](./open-questions.md):**

| Type | STANDALONE | SUBFILE | SUBDOC |
|---|---|---|---|
| `gherkin` | – (banned) | yes | yes |
| `friction-log` | – (banned) | yes | – (banned per R3 implicit; confirm next session) |

**Status:** ratified by click. Q6 closes for these two types; `hook` natural-fit detail still pending.

---

## Open issue introduced by R1

If L11.43's scope extends to 6 types (task + 5 promoted), the "tasks-only ULID" framing in [`adr-draft.md`](./adr-draft.md) is wrong. The ADR draft needs revision. This was **not** done before the session's commit-and-handover pivot — flagging here so the next session catches it during ADR-promotion review.

---

## Assumptions Log

- **Assumption B1.** The `lock_sha` content-addressing scheme uses SHA-256 over body bytes *below* the frontmatter `---` close. Frontmatter is excluded so the hash stabilises when only metadata (e.g. `updated:`) changes. *Status: proposed; not user-confirmed.*
- **Assumption B2.** `agency readme`'s auto-disambiguation logic appends the first 8 chars of the ULID only when a slug collision is detected, never speculatively. *Status: proposed; aligns with L11.43 prose-rules but not separately ratified.*
- **Assumption B3.** Existing `tasks/<NNN>-<slug>/` folders moved to `archive/tasks/<NNN>-<slug>/` retain their **existing** frontmatter unchanged (no retroactive `id:` ULID minting, no schema migration). The audit graph treats archived tasks via their pre-migration identity. *Status: implied by L11.43 revised; not explicit.*
- **Assumption B4.** Revisions R1 / R2 / R3 above are binding once next-session confirms them, but currently carry "provisional" status because the user interrupted the question round to request the waiver. *Status: explicit; pending next-session confirmation.*
