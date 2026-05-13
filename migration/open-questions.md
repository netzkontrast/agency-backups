---
type: note
status: active
slug: open-questions
summary: "Q1-Q7 open questions blocking ADR-0013 acceptance. Each requires user decision before promotion from /migration/ to decisions/."
created: 2026-05-13
updated: 2026-05-13
---

# Open questions — block ADR-0013 acceptance

Each question below has a recommendation and a tradeoff. Resolving all 7 unblocks promotion of [`adr-draft.md`](./adr-draft.md) to `decisions/0013-twelve-type-ontology.md`.

---

## Q1 — Mode matrix per type

For each of the 12 first-class types, which of STANDALONE / SUBFILE / SUBDOC are permitted? Draft matrix:

| Type | STANDALONE | SUBFILE | SUBDOC | Notes |
|---|---|---|---|---|
| `task` | required | – | – | Orchestration entry point — always standalone |
| `prompt` | yes | yes | yes | Most flexible; already authored all three ways in the wild |
| `research` | required | – | – | Immutable on close; standalone only |
| `skill` | required | – | – | Mirrors external corpora; standalone canonical |
| `adr` | required | – | – | MADR 4.0.0 — single file in `decisions/` |
| `spec` | required | – | – | Root-level governance specs |
| `readme` | required | – | – | One per operational folder; **auto-generated per L11.44** |
| `role` | yes | yes | yes | **OPEN — should role allow SUBDOC inside prompt?** |
| `lock` | required | – | – | Per L11.40′ |
| `gherkin` | yes | yes | yes | **OPEN — SUBDOC inside spec (current pattern) vs SUBFILE under `scenarios/`** |
| `friction-log` | yes | yes | – | SUBFILE under `<parent>/reflection/` is current pattern |
| `hook` | required | – | – | Per L11.41′ |

**Recommendation:** restrict SUBDOC to four types where it adds value (`prompt`, `role`, `gherkin`, `friction-log`); ban it elsewhere to keep the graph easy to walk.

**Tradeoff:** permissive SUBDOC simplifies in-the-wild authoring but introduces more edge cases for the linter and the `agency extract` command.

---

## Q2 — `agency promote` edge-rewrite semantics

When a SUBDOC promotes to STANDALONE (or vice versa):

- **(a) Auto** — Edges follow automatically. SQLite updates `placement_mode` + `parent_id`; body-Markdown anchors get rewritten in the parent.
- **(b) Confirm per edge** — User confirms each rewrite via `AskUserQuestion`.
- **(c) Staged** — Promotion generates a reviewable diff; user accepts or rejects before commit.

**Recommendation:** **(a) auto** for non-destructive promotions (no inbound edges crossing a closed-research T4 boundary); **(c) staged** when promotion would break an inbound edge crossing a T4 boundary.

**Tradeoff:** auto-mode is faster but invisibly mutates parent files; staged mode is slower but auditable.

---

## Q3 — Parallel-edit locking

When two agents simultaneously edit different SUBDOCs inside the same parent file:

- **(a) File-level lock** via `tools/fm/edit.py` (current behavior; second agent waits).
- **(b) Byte-range CRDT** — both edits land if non-overlapping.
- **(c) Optimistic** — both commit, conflict resolved at git layer.

**Recommendation:** **(a) file-level**. Keep `tools/fm/edit.py` invariant; parallel agents on the same parent are rare enough that serialising is fine.

**Tradeoff:** file-level lock is simple but blocks legitimate parallel work; CRDT is the right long-term answer if multi-agent parallel editing becomes common.

---

## Q4 — Slug-collision disambiguation tooling

L11.43 specifies that prose references auto-append the short ULID when two slugs collide. Which tool detects the collision and renders the suffix?

- **(a) `agency new` at mint time** — errors if the slug exists in `tasks/`. User must pick a more specific slug or pass `--allow-collision` to mint anyway with the suffix.
- **(b) Pre-commit linter** — scans the live tree; emits WARN on collisions; suggests rewrites.
- **(c) Lazy at reference resolution** — `agency open <slug>` returns the disambiguation prompt only when ambiguous.

**Recommendation:** **(a)** as the primary defense, with **(b)** as a backstop for collisions introduced by branch merges. **(c)** falls out for free.

**Tradeoff:** (a) is restrictive (forces the user to pick a unique slug upfront); (b) is permissive (allows transient duplicates).

---

## Q5 — `assumption-entry` as the 13th type?

L11.44 v2 moves the assumption log into frontmatter as `assumptions: list[Assumption]`. Should each entry **also** become a queryable first-class artifact (`assumption-entry`) with its own ID + edges (e.g. `assumption_invalidated_by: <task-id>`)?

**Recommendation:** **defer**. Keep assumptions as structured frontmatter list entries for now. Promote to a 13th type only if the audit graph starts needing assumption-level edges (e.g. "find all tasks invalidated by assumption A.42"). 13 types crosses Miller-7±2-doubled comfort.

**Tradeoff:** defer is reversible (assumption entries can be lifted into their own type later); promote-now is forward-compatible but adds schema surface immediately.

---

## Q6 — Detailed natural-fit for `gherkin` / `friction-log` / `hook`

Decision 4 ratified the "natural fit" principle but deferred specifics for these three types. Each needs:

**`gherkin`:**
- Always parented (SUBFILE / SUBDOC inside a spec or task) — never STANDALONE?
- Or STANDALONE under `scenarios/<scenario-slug>/scenario.gherkin.md` permitted?
- Identifier: existing `# anchor: <stable-id>` anchor convention, or new slug?

**`friction-log`:**
- Always parented to a session (research or task or PR) — never STANDALONE?
- Filename: `friction-log.md` (singular per parent) or `<session-date>-friction-log.md` (multiple per parent over time)?
- Identifier: parent + date, or its own slug + frontmatter linkage?

**`hook`:**
- One hook per event (current pattern: `tools/hooks/<event>.sh`) or multiple hooks per event (`tools/hooks/<event>/<slug>/`)?
- Identifier: event-name alone (when one-hook-per-event) or event + slug (when multi)?

**Recommendation for each:** start parented-only (gherkin always-parented; friction-log always-parented + singular per parent; hook = one-per-event + add slug for future multi-hook expansion). Revisit only on concrete pressure.

---

## Q7 — Sequencing — what gets done in what order?

Three paths surfaced in [`handover.md`](./handover.md) §4:

- **Path A** — Close Q1–Q6 → ratify ADR-0013 → cascade root specs → build migration tooling.
- **Path B** — Build thin `agency readme` prototype → revise ADR with implementation evidence → cascade.
- **Path C** — Land schema deltas first → ADR references already-landed schemas.

**Recommendation:** **Path A**. Schema deltas (Path C) ahead of ADR acceptance invert the governance contract; Path B's prototype is valuable but premature when Q1–Q6 are open.

**Tradeoff:** Path A is linear and slow (multiple sessions). Path B / C front-load implementation risk but compress the timeline.

---

## Cross-references

- Canonical lock text: [`locks-ratified.md`](./locks-ratified.md)
- ADR draft (the synthesis these Qs gate): [`adr-draft.md`](./adr-draft.md)
- Schema deltas implied: [`schemas-delta.md`](./schemas-delta.md)
- Next-session entry point: [`handover.md`](./handover.md)

## Assumptions Log

(none)
