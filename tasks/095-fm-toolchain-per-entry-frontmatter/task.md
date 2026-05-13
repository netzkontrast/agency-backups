---
type: task
status: active
slug: fm-toolchain-per-entry-frontmatter
summary: "Extend the fm-toolchain (tools/fm/edit.py, tools/fm/validate.py) and/or add a sibling per-entry editor so that files containing multiple inline YAML 'card' blocks (notably skills/novel-architect/references/learnings.md per MIF Level 3 schema) can be mutated and validated entry-by-entry without falling back to manual YAML. Unblocks Task 088 (MIF L3 backport) which discovered tools/fm/edit.py operates on a single file-level frontmatter block only and cannot reach inline per-entry blocks."
created: 2026-05-13
updated: 2026-05-13
task_id: "095"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/fm/edit.py
  - tools/fm/validate.py
  - skills/novel-architect/schemas/mif-level3.yaml
  - skills/novel-architect/references/learnings.md
---

# Task 095 — fm-toolchain: Per-Entry Frontmatter Mutation + MIF L3 Validation

## Goal

The fm-toolchain currently treats every Markdown file as having **at most one** YAML frontmatter block at byte 0 (delimited by `---\n` … `---\n`). The MIF Level 3 schema declared in [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml) (`cognitive_type`, `decay_rate`, `derivation_chain`) requires **per-entry** YAML "card" blocks embedded inside the body Markdown — one card per `### YYYY-MM-DD —` H3 heading in [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md). The existing toolchain (`tools/fm/edit.py`, `tools/fm/validate.py`) cannot address these inline blocks; nor is `mif-level3.yaml` wired into `--check-body` as a body-schema target.

`done` when:

1. `tools/fm/edit.py` (or a sibling tool — implementation choice deferred to the executor) accepts an `--entry <id-or-anchor>` selector that targets a specific inline YAML card block inside a Markdown file's body, and applies `--set` / `--append-list` / `--unset` / `--remove-from-list` semantics identical to the existing file-level mutations. Idempotent + file-locked + body-byte-preserving outside the addressed entry's card region.
2. `tools/fm/validate.py --check-body` recognises `skills/novel-architect/references/learnings.md` as in-scope and validates every entry's inline card block against the schema in [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml). The schema's `entry_schema.required_fields` block becomes a hard gate; the MIF L3 subset (`cognitive_type`, `decay_rate`, `derivation_chain`) declared by Task 088 becomes the per-entry body-schema target.
3. Pytest coverage under `tools/tests/test_fm_edit.py` (or sibling) covers: (a) addressing an entry by `learning_id`, (b) `--set` updating a scalar field inside a card without touching neighbouring entries' bytes, (c) `--append-list` on `derivation_chain` with deduplication, (d) refusal-to-mutate when the addressed entry's body is T4-immutable (`status: archived`), (e) cross-entry body-byte preservation (only the addressed card's bytes change).
4. Task 088 unblocks — after this tool ships, an agent can execute the MIF L3 backport without falling back to manual YAML edits.

## Plan

1. **Design decision** — extend `tools/fm/edit.py` with `--entry <id>` or ship a sibling `tools/fm/entry-edit.py`. Document the choice in this Task's `migration-decision.md` worksheet during the working session. Sibling-tool is the lower-risk path (no regression surface for existing callers).
2. **Card-block parser** — define the canonical inline-card grammar. Two candidates from the schema sample (mif-level3.yaml lines 28–40): (a) blockquote-style (`> - key: value` lines), (b) fenced YAML inside `<!-- card -->` HTML-comment delimiters. Pick one, document the choice. Anchor each card to its preceding H3 heading's `learning_id` (e.g. `L-2026-05-11-003` from `## L-2026-05-11-003: …`).
3. **Mutation API** — implement `--entry <id> --set key=value` / `--append-list` / `--remove-from-list` / `--unset`. Preserve all bytes outside the addressed card region. Reuse `tools/fm/_core.py` parser primitives where possible.
4. **Validation wiring** — extend `tools/fm/validate.py --check-body` to detect files declaring a body-schema target (via a new file-level frontmatter key such as `body_schema: ../schemas/mif-level3.yaml`, or by enumeration in a registry like `tools/fm/_body_schemas.json`). Pick one and document.
5. **T4-immutability gate** — when an entry's card carries `status: archived`, refuse `--set` / `--append-list` / `--unset` on any body-section key; permit only L1 metadata keys (`updated:`, `valid_to:`). Mirror the existing `EXIT_ADR_IMMUTABLE = 5` exit-code pattern.
6. **Pytest** — add `tools/tests/test_fm_entry_edit.py` covering the five cases enumerated in §Goal item 3.
7. **Wire into governance check** — add `tools/fm/validate.py --check-body skills/novel-architect/references/learnings.md` to `tools/check-governance.sh` once the schema is fully wired.
8. **Unblock Task 088** — note in Task 088's `task.md` that this Task lands as its prerequisite; flip Task 088 `task_blocked_by` to include `"095"`.

## Todo

- [ ] 1. Decide extend-vs-sibling-tool. Document.
- [ ] 2. Define inline-card grammar; pick blockquote-style vs HTML-comment-delimited.
- [ ] 3. Implement mutation API (`--entry`, `--set`, `--append-list`, `--unset`, `--remove-from-list`).
- [ ] 4. Implement body-schema wiring in `tools/fm/validate.py --check-body`.
- [ ] 5. Implement T4-immutability gate (exit-code 5 mirror).
- [ ] 6. Author pytest coverage.
- [ ] 7. Wire into `tools/check-governance.sh`.
- [ ] 8. Update Task 088's `task_blocked_by` to include `"095"`; reopen Task 088.

## Acceptance

```gherkin
Feature: fm-toolchain addresses per-entry inline YAML card blocks in files declaring a body-schema target

  # anchor: 095.AC.1
  Scenario: Per-entry mutation preserves neighbouring entries byte-for-byte
    Given skills/novel-architect/references/learnings.md with five entries E1..E5, each carrying an inline YAML card
    When the agent runs `tools/fm/edit.py --entry L-2026-05-11-003 --set cognitive_type=semantic <file>`
    Then only the bytes inside entry E3's card region MUST differ between pre and post
    And the file as a whole MUST still parse under tools/fm/validate.py --check-body

  # anchor: 095.AC.2
  Scenario: Body-schema validation against mif-level3.yaml
    Given skills/novel-architect/references/learnings.md declares body_schema: ../schemas/mif-level3.yaml
    When the agent runs `tools/fm/validate.py --check-body <file>`
    Then every entry's card MUST carry cognitive_type, decay_rate, derivation_chain
    And the exit code MUST be 0 only when every entry validates

  # anchor: 095.AC.3
  Scenario: T4 archived entry refuses body-section mutation
    Given an entry whose card carries status: archived
    When the agent runs `tools/fm/edit.py --entry <id> --set cognitive_type=semantic <file>`
    Then the tool MUST exit non-zero (EXIT_ADR_IMMUTABLE mirror) with a stderr explaining the T4 boundary
    And only L1 metadata keys (updated, valid_to) MAY be mutated on archived entries

  # anchor: 095.AC.4
  Scenario: Task 088 unblocks
    Given Task 095 has task_status: done
    When an agent picks up Task 088
    Then the agent SHALL be able to apply the MIF L3 backport using `tools/fm/edit.py --entry <id> --set` calls only
    And no manual YAML edits SHALL be required
```

## Links

- Blocks: [Task 088 — MIF L3 Backport](../088-novel-architect-mif-l3-backport/task.md)
- Schema: [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml)
- Target file: [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md)
- Tooling: [`tools/fm/edit.py`](../../tools/fm/edit.py), [`tools/fm/validate.py`](../../tools/fm/validate.py), [`tools/fm/_core.py`](../../tools/fm/_core.py)
- Repair tier policy: [`MAINTENANCE.md §1`](../../MAINTENANCE.md#1-repair-permission-tiers), [`MAINTENANCE.md §1.0.1`](../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059)
- Governing specs: [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
