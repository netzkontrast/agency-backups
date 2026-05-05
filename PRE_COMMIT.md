# General Pre-Commit Checklist for Agents

Before committing any code or documentation changes to this repository, the agent MUST perform the following checks. Failure to satisfy these checks means the commit MUST NOT be executed.

## 1. Clean Working Directory
- Verify there are no unintended temporary files, `.py` or `.sh` script scratchpads, or loose log dumps.
- Ensure that you have explicitly deleted any temporary execution scripts used to generate data.
- Use `git status` to ensure only explicitly intended files are staged.

## 2. File Integrity & Decentralized Documentation (Batch Update)
- No required documentation file (like `readme.md`, `state.md`, `session.log`) may be left empty (0 bytes).
- **Global Readme Audit:** EVERY folder that has been touched during this session MUST have its `readme.md` updated *now*, right before the commit.
- **Readme Format:** The `readme.md` MUST explicitly explain the "what" and "why", MUST document any workflow assumptions made by the agent to prevent drift, and MUST use clickable relative Markdown links for every file and subfolder referenced.

## 3. Mandatory Agent Feedback & Frustration Logging
- **Rule:** Regardless of the task type, you MUST create a feedback log entry conforming to [FRUSTRATED.md](./FRUSTRATED.md).
- Even if the task went perfectly (FL0), you must document that status. If you encountered friction (FL1-FL3), you must provide concrete feedback to improve the prompts or architecture.
- For research tasks, this goes in `/reflection/friction-log.md`. For standard tasks, include a `## Frustration Log` section in your final PR description or commit message.

## 4. Testing & Verification
- If modifying code, run all relevant unit tests and ensure they pass.
- If editing UI/frontend elements, generate and verify screenshots/media.

## 5. Formatting & Linting
- All Markdown files must have consistent header formatting, valid relative links, and readable tables.

## 6. Context-Specific Mandates

Pick the matching governance spec — the agent MUST additionally satisfy the `Mandatory Pre-Commit Checks` defined there:

- **Task** (orchestration in `/tasks/<NNN>-<slug>/`): [TASK.md](./TASK.md) §7.
- **Prompt** (instruction set in `/prompts/<slug>/`): [PROMPT.md](./PROMPT.md) §6.
- **Research** (execution workspace in `/research/<slug>/`): [RESEARCH.md](./RESEARCH.md) §5.

## 7. Mechanical Governance Checks

If the change touches any file under `/tasks/`, `/prompts/`, `/research/`, `/skills/`, or `/maintenance/`, the agent MUST run the unified shim below and fix every `ERROR`-level diagnostic before committing.

```bash
# Unified (canonical, Task 017 cutover):
tools/check-governance.sh                  # FM_TOOLCHAIN=1 by default (fm-validate gates)

# Targeted invocations:
python3 tools/fm/validate.py               # L1+L2 keys, type/path agreement, required headings
python3 tools/fm/validate.py --check-body  # adds SPEC §12 per-section body-schema checks
python3 tools/fm/validate.py --strict      # promotes WARN-severity diagnostics to non-zero exit
python3 tools/dramatica-nav/validate.py    # narrative-ontology integrity (gated on ontology.json)

# Legacy escape hatches (one-release deprecation window):
FM_TOOLCHAIN=0 tools/check-governance.sh   # restore the legacy validate-frontmatter gate
python3 tools/legacy/lint-structure.py     # structural rules pending fm- migration
python3 tools/legacy/lint-linkage.py       # cross-ref graph pending fm-query migration
```

### 7.A Toolchain Selection (Legacy → Flexible Transition)

The repository runs **both** the legacy linters and the flexible toolchain in parallel during the Task 016 → Task 019 migration window. Use this matrix to decide which is the source of truth for any given commit:

| Situation | Use | Why |
|---|---|---|
| Default pre-commit hook on a fresh clone | Legacy (`tools/check-governance.sh` without `FM_TOOLCHAIN=1`) | This is the gating set; the hook installed by `tools/install-hooks.sh` runs exactly this. |
| Authoring or modifying root specs (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `MAINTENANCE.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`) | Both — legacy gates the commit; flexible exposes per-section body-schema regressions early | Root specs are read by every downstream agent; running `FM_TOOLCHAIN=1 tools/check-governance.sh` plus `tools/fm/validate.py --check-body` surfaces drift the legacy validator cannot see. |
| Editing a `task.md`, `prompt.md`, or `research/<slug>/output/SPEC.md` body section that the per-type required-headings ontology covers | Flexible (`tools/fm/validate.py --check-body`) before commit; legacy still gates | Body-shape mismatches (missing required headings, wrong ordering) are flexible-only diagnostics today (per [SPEC.md §12](./research/flexible-frontmatter-toolchain/output/SPEC.md)). |
| Investigating a flexible WARN that the legacy validator does not flag | Flexible with `--strict` to reproduce the failure mode | Lets the agent decide whether the WARN is a real defect (file a Task) or a known false positive (document via the waiver protocol below). |
| Expecting the gating semantics post-migration | Flexible only, with `FM_TOOLCHAIN=1` exported in the shell or set in CI | Once Task 019 flips the default, the legacy linters are retired. Practising under `FM_TOOLCHAIN=1` now reduces surprises at flip time. |

The flexible toolchain MUST NOT be used to bypass a legacy `ERROR`. If `tools/check-governance.sh` (default mode) fails, the commit MUST be blocked, regardless of what `FM_TOOLCHAIN=1` says.

### 7.B Frontmatter Waivers — Burn Protocol

`tools/.frontmatter-waivers` is the legacy validator's escape hatch for files that pre-date a tightened rule. Because waivers silently turn a real defect into "we promised to fix this later", they accumulate technical debt every time the validator gains a stricter check. The protocol below keeps the waiver list shrinking, never growing.

**Rules.**

1. **No new research files.** `tools/.frontmatter-waivers` MUST NOT gain a new entry pointing under `/research/`. Research outputs are immutable after `research_phase: complete`; if a completed research workspace fails the validator, the correct response is to file a Task that updates the validator (or re-runs the research with a corrected schema), not to waive the file.
2. **Burn-down, not stand-still.** Every coherence-check run (per `MAINTENANCE.md §2`) SHOULD attempt to remove at least one waiver. The agent MUST verify the file now passes the validator before deleting the waiver line; if it does not, the agent MUST file a T3 Task to repair the underlying defect.
3. **Rationale is mandatory.** Every line in `tools/.frontmatter-waivers` MUST be preceded by a `# <YYYY-MM-DD> <reason> (Task <NNN> tracks repair)` comment. Waivers without a tracking Task are an immediate cleanup target for the next maintenance run.
4. **Scope is per-file, not per-rule.** A waiver disables the entire validator for the listed file. The agent MUST NOT use waivers to silence a single rule across the repo; that is a validator change (T3 Task on `tools/validate-frontmatter.py`).
5. **Re-expression at toolchain flip.** When Task 019 flips `FM_TOOLCHAIN=1` to the default, every surviving waiver MUST be re-expressed against `tools/fm/validate.py`'s waiver mechanism (or burned). A blind copy is not acceptable; each carry-over waiver MUST be re-justified in its rationale comment with the new validator's diagnostic code.

This protocol resolves the Task 001 friction-log finding (FL1) where a research workspace was added to the waiver list to unblock a commit and was never removed.

The narrative-ontology validator runs automatically inside `check-governance.sh` when `maintenance/schemas/narrative-ontology/ontology.json` exists. It enforces five hard cross-entry invariants (errors → exit 1):

| Check | What it catches |
|---|---|
| schema | Per-entry violations of `ontology.schema.json` (Draft 2020-12) |
| reciprocity | Asymmetric `dynamic_pair_id` cross-references |
| pair_member | `kind: dynamic-pair` entries pointing at non-existent members |
| alias-uniqueness | Same alias string in two entries' `aliases_<locale>` lists |
| ncp-enum | `ncp_appreciation` values not in any NCP enum surface |

Three coverage warnings (do NOT fail CI; documented v0.1 limitations): `quad-membership` (fractal-distortion in quad members), `term_file-anchor` (hand-authored anchors that don't resolve), `unmapped-heading` (`##` headings without a backing ontology entry). Run with `--strict` to promote warnings to errors.

The pre-commit hook under `.githooks/pre-commit` runs all three automatically. Install once per clone with **either** of the equivalent commands below:

```bash
# Recommended: idempotent installer with sanity checks
tools/install-hooks.sh

# Or directly:
git config core.hooksPath .githooks
```

Diagnostics at `ERROR` level MUST be addressed by fixing the file (preferred) or by documenting a waiver in `tools/.frontmatter-waivers` with a rationale comment. `WARN`-level diagnostics are advisory only.

## 8. Trust Audit (Spec-J/K/L)

Before closing a Task (`task_status: done`), the agent MUST run the trust audit:

```bash
python3 tools/check-trust.py
```

This script verifies that every `done` Task has a `friction-log.md` and that the friction log's FL declaration is traceable (Spec-L.3.1 / Spec-L.7.1).

Only when all applicable boxes above are conceptually "checked" may the agent invoke the `submit` or `git commit` commands.
