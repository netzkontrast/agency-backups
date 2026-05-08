---
type: note
status: completed
slug: task-037-pre-commit-spec-integration-friction-log
summary: "Friction log for Task 037 — pre-commit-spec-integration. FL1: research-prompt-optimizer skill not registered as user-invocable in this session forced a workflow detour."
created: 2026-05-07
updated: 2026-05-07
---

Highest Frustration Level: FL1

# Friction Log — Task 037 (PRE_COMMIT.md Spec Integration)

## What landed

- **ST-1.** [`research/pre-commit-readme-update-cadence/`](../../research/pre-commit-readme-update-cadence/) workspace closed (`research_phase: complete`). The optimized research prompt at `research-prompt.md` was produced via the `research-prompt-optimizer` skill (delegated through a `deep-research` Agent) and then executed by `/sc:agent` to overwrite the placeholder SPEC. SPEC.md §3 carries the byte-locked drop-in paragraph for both PRE_COMMIT.md §2 and FRUSTRATED.md §28. Per-workspace `tools/check-trust-audit.py` exits 0 (all three thresholds met).
- **ST-2.** [`tools/check-clean-working-directory.py`](../../tools/check-clean-working-directory.py) (PC.1.1) shipped with [10 unit tests](../../tools/tests/test_clean_working_directory.py) covering: clean tree, scratchpad outside exempt dir (ERROR), scratchpad in `/tools/`, `/tests/`, `/decisions/` (pass — FOLDERS.md §8), allowlist match/non-match, `session.log` always allowed, diagnostic format. Wired as step `[2c/6]` of `tools/check-governance.sh`. Per-repo carve-outs in [`tools/.script-allowlist`](../../tools/.script-allowlist) (`install.sh`, `tasks/041-extract-subtask-prompts/scripts/*.py`).
- **ST-3.** Per-rule TSV waiver mechanism in [`tools/.frontmatter-waivers`](../../tools/.frontmatter-waivers) with loader (`load_waivers` / `apply_waivers`) appended to [`tools/fm/_core.py`](../../tools/fm/_core.py). Applied from both [`tools/fm/validate.py`](../../tools/fm/validate.py) and [`tools/adr/cli.py`](../../tools/adr/cli.py) so `ADR.A.<aspect>.<stmt>` codes are valid rule-ids per §7.C. Migration shim at [`tools/scripts/migrate-waivers.py`](../../tools/scripts/migrate-waivers.py) (legacy single-path → wildcard `*` row + 90-day expiry, idempotent). [18 tests](../../tools/tests/fm/test_per_rule_waivers.py) cover: per-rule match, wildcard, expired/unexpired, no-expiry-dash, malformed column count, malformed expiry, mixed legacy+new rejection, ADR.A.* codes accepted, migration semantics.
- **ST-4.** [`PRE_COMMIT.md`](../../PRE_COMMIT.md) amended:
  - §1 documents the new `[2c/6]` linter and the `tools/.script-allowlist` carve-out file.
  - §2 lifts the byte-locked Readme Cadence paragraph from research SPEC §3 (canonical, batched-at-pre-commit). The reciprocal copy into FRUSTRATED.md §28 lands in [Task 062 B-1](../062-frustrated-spec-followup-ac1-ac5/task.md) per the joint-commit contract.
  - §7.A rewritten as a 3-column **Legacy / Flexible / ADR** tool-mapping matrix covering 16 concerns; §7.C step number corrected from `[5/5]` to `[5/6]` to match the actual `tools/check-governance.sh` numbering.
  - §7.B rewritten as the per-rule burn protocol; ADR.A.* codes explicitly accepted as rule-ids.
  - New §8 carries four Gherkin scenarios anchored `PC.B.1` (§6 hand-off), `PC.B.2` (§7 governance gate), `PC.B.3` (§7.B per-rule waivers incl. ADR.A.3.5 example), `PC.B.4` (§7.C ADR-validator interaction with the synthesis markers).
  - Trust Audit renumbered §8 → §9.

## Friction (FL1)

The single FL1 entry: the `skills/research-prompt-optimizer/` skill exists on disk but is **not registered as a user-invocable Skill** in the current session — only the `sc:*` skill set plus a handful of others are. The `Skill` tool errored with `Unknown skill: research-prompt-optimizer` on first attempt. Resolved by delegating to a `deep-research` Agent that loads `SKILL.md` and follows the 5-phase pipeline, then handing the rendered prompt to `/sc:agent` for execution. Recommendation: a small project README under `skills/` (or a session-start hook entry) documenting which on-disk skills are user-invocable in a default Claude Code session vs. which need Agent-tool delegation would have saved one round-trip.

No FL2 / FL3 entries. The acceptance-coupling note in `task.md` (AC-(a) requires byte-identical wording with FRUSTRATED.md §28, owned by Task 062 B-1) is intentional and tracked: §3 of the readme-cadence SPEC is the canonical source; this commit lands the locked paragraph into PRE_COMMIT.md §2 only, and Task 062 B-1 will copy it byte-for-byte into FRUSTRATED.md §28 in its closing PR.

## Falsification clause

- **ST-1 falsification:** "wrong cut iff any cadence yields >2× token cost vs. status quo" — did not fire. Status quo is Option B (batched-at-pre-commit, 1.0×); Option A is 3.0× (over the 2× threshold for the wrong choice); Option B was selected.
- **ST-2 falsification:** "wrong cut iff legitimate `.py` files (e.g., a one-off migration script kept in a task's notes for audit) trigger ERROR" — did not fire. The two pre-existing legitimate scripts (`install.sh`, `tasks/041-extract-subtask-prompts/scripts/extract.py`) are covered by `tools/.script-allowlist`; the linter's first run on the live repo flagged exactly those two paths and nothing else.
- **ST-3 falsification:** "wrong cut iff the new format breaks parsing of existing per-file waivers" — did not fire. The legacy `tools/.frontmatter-waivers` file did not exist on disk (the per-file mechanism had never been populated), so migration was a no-op; the new TSV file was created clean. Migration semantics still verified against synthetic legacy input in `test_per_rule_waivers.py::MigrateWaiversTests`.
- **ST-4 falsification:** "wrong cut iff the §2 / §28 reconciled wording diverges between the two specs at commit time" — partially deferred. The §2 paragraph here matches research SPEC §3 byte-for-byte; the §28 paragraph is the explicit responsibility of Task 062 B-1 and will be checked by the diff-test contract enumerated there.

## Recommendation

The skill-registration gap noted above is small and self-resolving once a session-start hook lists project-local skills. Otherwise, the four-subtask plan executed cleanly on the first pass after rebasing onto PR #89 (which provided the `[2b/6]` template + slug-rename bedrock). No prompt or process restructure recommended.
