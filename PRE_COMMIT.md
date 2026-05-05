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
