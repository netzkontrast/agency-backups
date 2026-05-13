---
type: note
status: active
slug: schemas-delta
summary: "Proposed schema additions implied by ADR-0013: L1 type enum +5, L1 purpose+assumptions, new L2 schemas, body-schema renderer contract for auto-generated readmes."
created: 2026-05-13
updated: 2026-05-13
---

# Schema deltas — proposed but not landed

ADR-0013 ([`adr-draft.md`](./adr-draft.md)) implies a coherent set of changes to `maintenance/schemas/`. **None of these are landed yet.** This file enumerates them so the next session can sequence the schema PR correctly (Path C in [`handover.md`](./handover.md) §4 lands these first).

---

## 1. L1 Vault Core — add 5 types + 2 narrative fields

**File:** `maintenance/schemas/l1-vault-core.schema.json` (regenerated from `header-ontology.json` via `tools/fm/gen_schema_mirror.py`).

**Current type enum:**

```json
"enum": ["task", "prompt", "research", "spec", "readme", "note", "index", "skill", "adr"]
```

**Proposed type enum:**

```json
"enum": [
  "task", "prompt", "research", "spec", "readme", "note", "index", "skill", "adr",
  "role", "lock", "gherkin", "friction-log", "hook"
]
```

**Proposed L1 additions** (carry the prose that used to live in readme bodies, per L11.44 v2):

```json
{
  "purpose": {
    "type": "string",
    "description": "Long-form 'Why this artifact exists' paragraph. Rendered into the auto-generated readme's Why-section. Multi-line permitted; max 2000 chars.",
    "maxLength": 2000
  },
  "assumptions": {
    "type": "array",
    "description": "Structured assumption log. Each entry becomes a row in the auto-generated readme's Assumptions section.",
    "items": {
      "type": "object",
      "properties": {
        "claim": { "type": "string", "minLength": 1 },
        "status": { "type": "string", "enum": ["open", "verified", "invalidated"] },
        "date": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
        "evidence": { "type": "string" }
      },
      "required": ["claim", "status", "date"],
      "additionalProperties": false
    }
  }
}
```

Both fields are **optional** at L1 (not every artifact needs a long-form purpose or assumptions). Auto-generated readmes render `(none)` when absent.

---

## 2. L1 slug pattern — relax for `type: lock`

**Current slug pattern:** `^[a-z0-9][a-z0-9-]*$` (kebab-case lowercase).

**Issue:** Decision 4 ratified that lock filenames preserve `L<round>.<sub>` notation (e.g. `L11.43-twelve-type-ontology.md`). The filename slug `L11.43-twelve-type-ontology` violates the current pattern (contains uppercase `L` and dot `.`).

**Options:**

- **(a) Relax the slug pattern globally** to `^[A-Za-z0-9][A-Za-z0-9.-]*$`. Smallest change; impacts every type.
- **(b) Per-type slug override** — let `l2-lock.schema.json` declare its own slug pattern. Requires schema-mirror generator + validator changes to consult L2 first.
- **(c) Decouple filename from slug for `type: lock` only.** Filename = `L11.43-twelve-type-ontology.md`; frontmatter `slug: l11-43-twelve-type-ontology` (kebab-case L1-conformant). Linter permits the divergence for `type: lock`.

**Recommendation:** **(c)** as the least invasive. The slug remains the canonical L1 identifier; the filename is a human-facing convenience for the lock-numbering scheme.

---

## 3. New L2 schemas — one per promoted type

Add five files under `maintenance/schemas/`:

| File | Namespace | Required keys |
|---|---|---|
| `l2-role.schema.json` | `role_*` | `role_persona`, `role_invocation_pattern`, `role_used_by_prompts` (list) |
| `l2-lock.schema.json` | `lock_*` | `lock_id` (pattern `^L\d+\.\d+[′″‴]?(-[a-z0-9-]+)?$` — accepts prime-mark glyphs `′` `″` `‴` as actually used in `locks-ratified.md` for L11.32‴, L11.36′, etc.; the textual `prime`/`double`/`triple` aliases are NOT accepted to keep one canonical form), `lock_round`, `lock_sub`, `lock_revision_marker` (enum `null|′|″|‴`), `lock_sha`, `lock_supersedes` (optional), `lock_referenced_by_adr` (optional) |
| `l2-gherkin.schema.json` | `gherkin_*` | `gherkin_anchor_id`, `gherkin_feature`, `gherkin_parent_artifact`, `gherkin_scenarios` (list) |
| `l2-friction-log.schema.json` | `friction_log_*` | `friction_log_session_id`, `friction_log_parent_artifact`, `friction_log_max_level` (enum FL0..FL3), `friction_log_entries` (list) |
| `l2-hook.schema.json` | `hook_*` | `hook_event` (enum: 5 D.7-compliant events), `hook_slug`, `hook_script_path`, `hook_python_module_path` |

Each schema follows the same draft-07 shape as the existing `l2-*.schema.json` files (`l2-adr.schema.json`, `l2-task.schema.json`, etc.).

---

## 4. New L2 schema — `l2-readme.schema.json`

**Purpose:** specify the **renderer contract** for auto-generated readmes (L11.44 v2). Any tool that writes `readme.md` must produce output matching this body schema.

Required body sections (rendered in this order):

1. `# <Slug humanized>` — title.
2. `## Purpose` — `purpose` field, or `(none)` if absent.
3. `## Navigation` — bidirectional edge table (outgoing + incoming).
4. `## Assumptions` — `assumptions` list, one row per entry, or `(none)`.

Top-of-file marker:

```html
<!-- AUTOGENERATED by agency readme; edit the parent artifact's frontmatter to change. -->
```

**Pre-commit check:** `agency readme --check` regenerates in-memory and diffs against on-disk. Non-zero exit = stale readme.

---

## 5. `header-ontology.json` — declare new edge keys

Edges that must exist for the audit graph to traverse the 5 promoted types correctly:

| Edge key | From → To | Cardinality |
|---|---|---|
| `prompt_uses_role` | `prompt` → `role` | many |
| `role_used_by_prompts` | `role` → `prompt` | many (reverse) |
| `task_references_locks` | `task` → `lock` | many |
| `lock_referenced_by` | `lock` → `task` \| `adr` | many (reverse) |
| `spec_defines_gherkin` | `spec` → `gherkin` | many |
| `task_satisfies_gherkin` | `task` → `gherkin` | many |
| `gherkin_defined_in` | `gherkin` → `spec` \| `task` | one |
| `task_produced_friction_log` | `task` → `friction-log` | one |
| `research_produced_friction_log` | `research` → `friction-log` | one |
| `friction_log_produced_by` | `friction-log` → `task` \| `research` | one (reverse) |
| `hook_invokes_skill` | `hook` → `skill` | many |
| `skill_invoked_by_hook` | `skill` → `hook` | many (reverse) |
| `adr_supersedes_lock` | `adr` → `lock` | many (when an ADR is the formal home of a lock) |

Forward + reverse pairs are populated by `agency readme` from the **forward** declaration only; reverse edges are computed by scan.

---

## 6. `tools/fm/validate.py` — recognize new types and placement modes

Three discrete changes:

- **(a) Permit `type` values for the 5 promoted types.** Currently any unknown type errors out.
- **(b) `--check-mode` flag** that enforces the per-type manifest matrix (Q1). Validation: artifact's `placement_mode` ∈ `manifest.modes`.
- **(c) `--check-readme` flag** that wraps `agency readme --check` so `tools/check-governance.sh` can invoke a single linter.

---

## 7. `tools/lint-structure.py` — register new operational folders

Add to the registry:

- `roles/` — new top-level for `role` artifacts.
- `decisions/locks/` — new sub-folder for `lock` artifacts.
- `tools/hooks/<event>/<slug>/` — new shape for `hook` artifacts.
- `archive/` — new top-level for archived pre-migration artifacts. Sub-tree mirrors operational paths (`archive/tasks/<NNN>-<slug>/`, etc.).

For each, declare the required files (`<type>.md` + `readme.md`).

---

## 8. `tools/check-governance.sh` — new gate steps

Add steps:

- `[X] python3 tools/fm/validate.py --check-mode` — enforce mode matrix.
- `[Y] python3 -m agency.cli readme --check` — verify auto-readmes are current.

Renumber existing steps as needed.

---

## 9. Body-schema contract per type

ADR-0013 ratifies frontmatter as the source of truth, but the **primary artifact files** (`task.md`, `prompt.md`, `research.md`, `role.md`, `lock.md`-equivalent, `gherkin`-equivalent, etc.) still have body content. The body-schema for each type needs updating:

- **`task.md`** — gains `<!-- assumption log moved to frontmatter; do not author here -->` marker; nav block moves to sibling `readme.md`.
- **`prompt.md`** — same treatment.
- **`research.md`** — same treatment.
- **`role.md`** — new body schema; sections TBD per Q6 detail.
- **`lock.md`-equivalent** (i.e. `L11.43-twelve-type-ontology.md`) — body holds the lock text + supersession chain + assumption log moved to frontmatter.

---

## Sequencing for landing these deltas

Recommended order (Path C in [`handover.md`](./handover.md)):

1. Add the 5 types to L1 enum + regenerate.
2. Add `purpose` + `assumptions` to L1 + regenerate.
3. Add the 5 new L2 schemas.
4. Add the `l2-readme.schema.json`.
5. Update `header-ontology.json` edges.
6. Wire `tools/fm/validate.py` flags.
7. Wire `tools/lint-structure.py` paths.
8. Wire `tools/check-governance.sh` gates.

Each step is independently testable. After step 3, lock files can validate; after step 4, the `agency readme` CLI has a contract to target; after step 8, the whole gate is enforced.

## Assumptions Log

- **Assumption D1.** Regenerating L1 mirrors via `tools/fm/gen_schema_mirror.py` does not require human edits to `l1-vault-core.schema.json`; the source of truth is `header-ontology.json`. *Status: implied by the existing comment in `l1-vault-core.schema.json`; not verified by reading the generator.*
- **Assumption D2.** The `friction_log_max_level` enum FL0..FL3 matches the existing FRUSTRATED.md scale. *Status: declared in FRUSTRATED.md; not re-verified here.*
