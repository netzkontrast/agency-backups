# General Pre-Commit Checklist for Agents

Before committing any code or documentation changes to this repository, the agent MUST perform the following checks. Failure to satisfy these checks means the commit MUST NOT be executed.

## 1. Clean Working Directory
- Verify there are no unintended temporary files, `.py` or `.sh` script scratchpads, or loose log dumps.
- Ensure that you have explicitly deleted any temporary execution scripts used to generate data.
- Use `git status` to ensure only explicitly intended files are staged.
- **Mechanical enforcement (PC.1.1).** [`tools/check-clean-working-directory.py`](./tools/check-clean-working-directory.py) walks the working tree and emits `<relpath>::ERROR:PC.1.1:script-scratchpad` for every `.py`/`.sh`/`.log` file outside the FOLDERS.md §8 exempt set (`/tools/`, `/tests/`, `/skills/`, `/templates/`, `/maintenance/`, `/decisions/`, `/Agency-System/`, `/.githooks/`). `session.log` is always allowed (RESEARCH.md §4.5). Per-repo carve-outs live one-per-line in [`tools/.script-allowlist`](./tools/.script-allowlist). Wired as step `[2c/6]` of [`tools/check-governance.sh`](./tools/check-governance.sh).

## 2. File Integrity & Decentralized Documentation (Batch Update)
- No required documentation file (like `readme.md`, `state.md`, `session.log`) may be left empty (0 bytes).
- **PRE_COMMIT.md §2 — Readme Cadence (canonical, batched-at-pre-commit).** Every operational folder (under `/tasks/`, `/prompts/`, `/research/`, `/skills/`) whose contents change during a session MUST have its `readme.md` updated as part of a single batched audit performed during the pre-commit phase. The agent MUST NOT create a per-file commit whose only purpose is to update an adjacent `readme.md`. The agent MAY iterate the staged readme content during the pre-commit phase before producing the commit, but the readme update MUST land in the same commit as the file changes that triggered it. Per-file readme spam is FL2 bloat per FRUSTRATED.md §FL.Special. *(This paragraph is byte-identical with FRUSTRATED.md §28 modulo the spec-name prefix; canonical source is [`research/pre-commit-readme-update-cadence/output/SPEC.md`](./research/pre-commit-readme-update-cadence/output/SPEC.md) §3. The reciprocal copy lands under [Task 062 B-1](./tasks/062-frustrated-spec-followup-ac1-ac5/task.md).)*
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
# Unified (canonical, Task 054 final cutover):
tools/check-governance.sh                  # fm-validate gates unconditionally

# Targeted invocations:
python3 tools/fm/validate.py               # L1+L2 keys, type/path agreement, required headings
python3 tools/fm/validate.py --check-body  # adds SPEC §12 per-section body-schema checks
python3 tools/fm/validate.py --strict      # promotes WARN-severity diagnostics to non-zero exit
python3 tools/dramatica-nav/validate.py    # narrative-ontology integrity (gated on ontology.json)
python3 tools/dramatica-nav/cleanup.py --check   # dramatica corpus cleanup linter (Task 030 ST-6; gated on ontology.json)

# Legacy archive (advisory; no longer wired into the gate):
python3 tools/legacy/lint-structure.py     # used by tools/check-maintenance-bypass.py only
python3 tools/legacy/lint-linkage.py       # used by tools/check-maintenance-bypass.py only
```

### 7.A Toolchain Precedence Matrix (Legacy ↔ Flexible ↔ ADR)

As of Task 054 the **Flexible** toolchain (`tools/fm/`) is the only frontmatter linter wired into [`tools/check-governance.sh`](./tools/check-governance.sh). The **Legacy** scripts (`tools/legacy/{validate-frontmatter,lint-structure,lint-linkage}.py`) survive only because [`tools/check-maintenance-bypass.py`](./tools/check-maintenance-bypass.py) folds their structural and cross-reference output into the bypass index — they no longer run from the gate, and the `FM_TOOLCHAIN` env var has been retired. The **ADR Governance Validator** (`tools/adr/`) runs unconditionally as step `[5/6]` of `tools/check-governance.sh` when `decisions/` is non-empty.

The table below maps every concern the gate covers to the tool that owns it in each toolchain. Use it to decide which command produces the gating diagnostic for any given file path.

| Concern | Legacy | Flexible (canonical) | ADR |
|---|---|---|---|
| Frontmatter L1 + L2 keys | [`tools/legacy/validate-frontmatter.py`](./tools/legacy/validate-frontmatter.py) | [`tools/fm/validate.py`](./tools/fm/validate.py) | — |
| Body section schema (per-type required headings) | — | `tools/fm/validate.py --check-body` | — |
| Cross-reference linkage (`task_uses_prompts` ↔ `prompt_relates_to_task`, etc.) | [`tools/legacy/lint-linkage.py`](./tools/legacy/lint-linkage.py) (shim) | `tools/fm/validate.py --type-check` | — |
| Directory structure (required files per folder) | — | [`tools/lint-structure.py`](./tools/lint-structure.py) | — |
| Run-log records | — | [`tools/lint-runlog.py`](./tools/lint-runlog.py) | — |
| Tasks-index freshness | — | [`tools/fm/index_diff.py`](./tools/fm/index_diff.py) | — |
| Operational `readme.md` L1 frontmatter (FOLDERS.md F.5) | — | [`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py) | — |
| Audit-graph dual-surface drift (FOLDERS.md F.6) | — | [`tools/check-audit-graph-consistency.py`](./tools/check-audit-graph-consistency.py) | — |
| Working-tree script-scratchpad scan (PC.1.1) | — | [`tools/check-clean-working-directory.py`](./tools/check-clean-working-directory.py) | — |
| Workspace-cleanliness (RESEARCH.md R.4.4) | — | [`tools/check-workspace-cleanliness.py`](./tools/check-workspace-cleanliness.py) | — |
| FL declaration (FRUSTRATED.md FR.B.4) | — | [`tools/check-fl-declaration.py`](./tools/check-fl-declaration.py) | — |
| RFC 2119 polarity audit | — | [`tools/check-rfc2119-polarity.py`](./tools/check-rfc2119-polarity.py) | — |
| Trust audit (Spec-J/K/L per-workspace gate) | — | [`tools/check-trust-audit.py`](./tools/check-trust-audit.py) | — |
| Trust audit (closure verification) | — | [`tools/check-trust.py`](./tools/check-trust.py) | — |
| Per-rule waiver loader (§7.B) | (per-file rows in `tools/.frontmatter-waivers`) | [`tools/fm/_core.load_waivers`](./tools/fm/_core.py) (TSV) + [`tools/scripts/migrate-waivers.py`](./tools/scripts/migrate-waivers.py) | (same loader; ADR.A.* codes accepted as rule-ids) |
| Narrative-ontology validate / cleanup (gated on `ontology.json`) | — | [`tools/dramatica-nav/validate.py`](./tools/dramatica-nav/validate.py), [`tools/dramatica-nav/cleanup.py`](./tools/dramatica-nav/cleanup.py) | — |
| ADR governance (MADR fields, supersession DAG, `adr_*` namespace) | — | — | [`tools/adr/cli.py validate`](./tools/adr/cli.py) (step `[5/6]`) |
| ADR synthesis into `AGENTS.md` guarded section | — | — | [`tools/adr/cli.py synthesize`](./tools/adr/cli.py) (author-explicit; not in the gate) |

**Precedence rules.**

1. The Flexible column is the only gating frontmatter linter (Task 054). Legacy scripts live in [`tools/legacy/`](./tools/legacy/) and are invoked only by [`tools/check-maintenance-bypass.py`](./tools/check-maintenance-bypass.py) to round out the bypass index for structural and cross-reference rules `fm-validate` does not yet replace.
2. The ADR column runs unconditionally as step `[5/6]` of [`tools/check-governance.sh`](./tools/check-governance.sh) — see §7.C. When `decisions/` is empty the validator is a graceful no-op (exit 0).
3. ADR diagnostics (codes prefixed `ADR.A.<aspect>.<stmt>`) are gated unconditionally and cannot be silenced via env-var toggles. The only legitimate suppression path is a per-rule waiver entry in [`tools/.frontmatter-waivers`](./tools/.frontmatter-waivers) per §7.B.

### 7.B Frontmatter Waivers — Per-Rule Burn Protocol

[`tools/.frontmatter-waivers`](./tools/.frontmatter-waivers) is the **per-rule** escape hatch for files that pre-date a tightened diagnostic. Because waivers silently turn a real defect into "we promised to fix this later", they accumulate technical debt every time a validator gains a stricter check. The protocol below keeps the waiver list shrinking, never growing.

**Format.** TSV with four tab-separated columns:

```
<path-glob>\t<rule-id>\t<rationale>\t<expires>
```

- `path-glob`: fnmatch glob, repo-relative.
- `rule-id`: an exact diagnostic code (e.g. `F.4.2`, `R.4.4`, `ADR.A.3.5`) emitted by [`tools/fm/validate.py`](./tools/fm/validate.py) or [`tools/adr/cli.py validate`](./tools/adr/cli.py). The literal `*` is permitted as a wildcard (silences every rule for the matching paths — same coarse semantics as the legacy per-file row); wildcards SHOULD be tightened to a specific code as part of the burn-down.
- `rationale`: short justification including the tracking Task slug (e.g. `Task 030 tracks repair`).
- `expires`: ISO-8601 calendar date `YYYY-MM-DD`, or `-` for no expiry. After the expiry date the waiver no longer suppresses diagnostics; the burn-down protocol expects the underlying defect to be fixed before then.

**Rules.**

1. **No new research-output files.** `tools/.frontmatter-waivers` MUST NOT gain a new entry pointing under `/research/<slug>/output/`. Research outputs are immutable after `research_phase: complete`; if a completed research workspace fails the validator, the correct response is to file a Task that updates the validator (or re-runs the research with a corrected schema), not to waive the file.
2. **Burn-down, not stand-still.** Every coherence-check run (per `MAINTENANCE.md §2`) SHOULD attempt to remove at least one waiver. The agent MUST verify the file now passes the validator before deleting the waiver line; if it does not, the agent MUST file a T3 Task to repair the underlying defect.
3. **Rationale + tracking Task are mandatory.** Every row MUST be preceded (or accompanied) by a `# <YYYY-MM-DD> <reason> (Task <NNN> tracks repair)` comment line, and the `rationale` column MUST cite the same Task slug. Waivers without a tracking Task are an immediate cleanup target for the next maintenance run.
4. **Per-rule scope is the default.** A waiver row silences exactly one diagnostic code on the matching paths. The wildcard rule-id `*` is permitted only when migrating legacy per-file rows or when an entire validator is provisionally unfit for the file (rare); the agent MUST NOT use `*` to silence unrelated rules in bulk.
5. **`ADR.A.<aspect>.<stmt>` codes are valid rule-ids.** Per §7.C, ADR diagnostics are gated unconditionally; the only legitimate suppression path is a per-rule waiver row whose `rule-id` is the exact ADR code (e.g. `ADR.A.3.5`). Wildcards (`*`) on ADR paths are explicitly DISCOURAGED.
6. **Re-expression at toolchain flip.** When the Legacy toolchain is retired, surviving rows whose path-globs target legacy-only diagnostics MUST be burned or re-expressed against the Flexible validator's diagnostic codes. A blind copy is not acceptable; each carry-over row MUST be re-justified in its rationale with the new diagnostic code.

**Migration shim.** [`tools/scripts/migrate-waivers.py`](./tools/scripts/migrate-waivers.py) translates legacy single-path-per-line rows to per-rule TSV rows with `rule-id = *` and a 90-day expiry. The migration is idempotent and semantics-preserving; the agent SHOULD then walk the migrated rows and tighten each one to a specific rule-id per Rule 4 above.

This protocol resolves the Task 001 friction-log finding (FL1) where a research workspace was added to the waiver list to unblock a commit and was never removed; per-rule scope plus mandatory expiry close the underlying mechanism gap.

The narrative-ontology validator runs automatically inside `check-governance.sh` when `maintenance/schemas/narrative-ontology/ontology.json` exists. It enforces five hard cross-entry invariants (errors → exit 1):

| Check | What it catches |
|---|---|
| schema | Per-entry violations of `ontology.schema.json` (Draft 2020-12) |
| reciprocity | Asymmetric `dynamic_pair_id` cross-references |
| pair_member | `kind: dynamic-pair` entries pointing at non-existent members |
| alias-uniqueness | Same alias string in two entries' `aliases_<locale>` lists |
| ncp-enum | `ncp_appreciation` values not in any NCP enum surface |
| dramatica-cleanup (Task 030 ST-6) | Four locked corruption classes — `DR-CLEAN-001` Screenplay Systems copyright footer, `DR-CLEAN-002` orphan page-number-only line, `DR-CLEAN-003` `''` double-apostrophe escape, `DR-CLEAN-004` `## ` heading whose body is `See <Other>` with ≤2 lines (NON-AUTO-FIX). Run via `python3 tools/dramatica-nav/cleanup.py --check` (gated on `ontology.json`, like `validate.py`). The catalogue is locked at four rules; growing it requires an `agency-adr` ADR. |

Three coverage warnings (do NOT fail CI; documented v0.1 limitations): `quad-membership` (fractal-distortion in quad members), `term_file-anchor` (hand-authored anchors that don't resolve), `unmapped-heading` (`##` headings without a backing ontology entry). Run with `--strict` to promote warnings to errors.

The pre-commit hook under `.githooks/pre-commit` runs all three automatically. Install once per clone with **either** of the equivalent commands below:

```bash
# Recommended: idempotent installer with sanity checks
tools/install-hooks.sh

# Or directly:
git config core.hooksPath .githooks
```

Diagnostics at `ERROR` level MUST be addressed by fixing the file (preferred) or by documenting a waiver in `tools/.frontmatter-waivers` with a rationale comment. `WARN`-level diagnostics are advisory only.

### 7.C ADR Governance Validator (Task 028)

Composed inside [`tools/check-governance.sh`](./tools/check-governance.sh) as step `[5/6]`. The validator [`tools/adr/cli.py validate`](./tools/adr/cli.py) is read-only and:

- triggers when the commit modifies `decisions/**`, `AGENTS.md`, or `tools/adr/**`;
- exits 0 if `decisions/` is absent or empty (graceful no-op);
- exits 1 on any ERROR diagnostic; the message format is `<relpath>::ERROR:<code>:<message>` where `<code>` is the `ADR.A.<aspect>.<stmt>` anchor from [`research/adr-spec-research-synthesis/output/SPEC.md`](./research/adr-spec-research-synthesis/output/SPEC.md).

Diagnostic codes the validator can emit and their author remedies:

| Code | Cause | Author remedy |
|---|---|---|
| `ADR.A.2.1` | Required MADR heading missing in body. | Add the heading. |
| `ADR.A.2.2` | Frontmatter fails JSON-Schema. | Fix the listed key/value. |
| `ADR.A.2.3` | "Decision Outcome" body is empty. | Declare the chosen option in one sentence. |
| `ADR.A.2.4` | "Consequences" body is empty. | Enumerate positive / negative / neutral impacts. |
| `ADR.A.2.7` | Filename and frontmatter `adr_id`/`slug` disagree. | Rename file or amend frontmatter. |
| `ADR.A.3.3` | Synthesis would exceed `--token-limit`. | Deprecate older ADRs or raise the limit (justify in PR). |
| `ADR.A.3.4` | Fidelity score below floor. | Investigate; usually a paraphrasing error in a recent ADR. |
| `ADR.A.3.5` | `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers missing in `AGENTS.md`. | Restore the markers. |
| `ADR.A.4.5` | Cyclic supersession edge. | Break the cycle; the diagnostic lists the cycle nodes. |
| `ADR.A.4.6` | Missing reciprocal `adr_supersedes` / `adr_superseded_by`. | Add the reciprocal entry. |
| `ADR.A.5.4` | Required ADR frontmatter key missing. | Add the missing key. |
| `ADR.A.5.6` | Duplicate `adr_id`. | Renumber the later-created ADR. |
| `ADR.A.5.7` | `adr_supersedes` references an absent ADR. | Restore the file or fix the reference. |

Hook granularity:

- The hook runs `agency-adr validate` (read-only). It does NOT auto-run `agency-adr synthesize`, since synthesis mutates `AGENTS.md` and surprising the author with a cross-file diff in the middle of a commit is unsafe. Synthesis is the author's explicit step before commit; the [`adr-validate`](./.github/workflows/adr-validate.yml) GitHub Actions workflow then verifies that the committed guarded-section bytes match what `synthesize --dry-run` would emit.

## 8. Acceptance Scenarios (Gherkin)

The following Gherkin scenarios are the executable acceptance contract for §6 (context-specific delegation), §7 (governance gate), §7.B (per-rule waivers), and §7.C (ADR validator). Each scenario is anchored with a stable identifier (`PC.B.<n>`); downstream tooling (e.g., a Gherkin-aware test harness) MAY mechanically execute the scenarios against the working tree.

```gherkin
# anchor: PC.B.1 — §6 context-specific delegation
Feature: Pick the matching layer-spec for the touched files
Scenario Outline: §6 hand-off routing by touched directory
  Given a commit that modifies a file under <root>
  When the agent reaches the §6 "Context-Specific Mandates" step
  Then the agent MUST additionally satisfy the layer-spec's
        "Mandatory Pre-Commit Checks" listed at <spec-section>
  And the agent MUST NOT proceed to `git commit` until those checks pass

  Examples:
    | root          | spec-section            |
    | tasks/        | TASK.md §7              |
    | prompts/      | PROMPT.md §6            |
    | research/     | RESEARCH.md §5          |
```

```gherkin
# anchor: PC.B.2 — §7 governance gate
Feature: tools/check-governance.sh exit-0 contract
Scenario: Default invocation gates the commit on any ERROR
  Given a commit that modifies a file under `/tasks/`, `/prompts/`,
        `/research/`, `/skills/`, or `/maintenance/`
  And the working tree carries no per-rule waiver matching the would-be
        diagnostic
  When `tools/check-governance.sh` runs at pre-commit
  Then every step `[1/6]` through `[6/6]` MUST run to completion
  And step `[5/6]` MUST invoke `tools/adr/cli.py validate` (per §7.C)
  And the script MUST exit 0 only when no step emits an ERROR
        (or every emitted ERROR is suppressed by an unexpired per-rule
         waiver per §7.B)
  And the commit MUST be blocked when the script exits non-zero
```

```gherkin
# anchor: PC.B.3 — §7.B per-rule waiver scope (incl. ADR.A.* codes)
Feature: Per-rule waivers silence exactly one diagnostic code per row
Scenario: ADR.A.3.5 waiver suppresses only the named diagnostic
  Given a commit that triggers the ADR validator (modifies `decisions/**`,
        `AGENTS.md`, or `tools/adr/**`)
  And `tools/.frontmatter-waivers` carries the row
        `decisions/0042-*.md\tADR.A.3.5\tTask 099 tracks repair\t2026-12-31`
  And today's date is 2026-05-07 (waiver unexpired)
  When `tools/adr/cli.py validate` runs as step `[5/6]`
        of `tools/check-governance.sh`
  Then any `ADR.A.3.5` diagnostic on a path matching `decisions/0042-*.md`
        MUST be suppressed
  And any other diagnostic on the same path (e.g. `ADR.A.4.5`) MUST
        still emit and gate the commit
  And `tools/check-governance.sh` MUST exit 0 if and only if no
        non-suppressed ERROR survives
```

```gherkin
# anchor: PC.B.4 — §7.C ADR validator interaction
Feature: Edit to AGENTS.md guarded section triggers the ADR validator
Scenario: Synthesis-marker break blocks the commit until restored
  Given a commit that modifies `AGENTS.md` between the markers
        `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` and
        `<!-- END AGENCY-ADR SYNTHESIS -->`
  And the markers are absent from the staged file
  When `tools/check-governance.sh` runs step `[5/6]`
  Then `tools/adr/cli.py validate` MUST exit 1 with diagnostic code
        `ADR.A.3.5`
  And `tools/check-governance.sh` MUST exit non-zero
  And the commit MUST be blocked until the markers are restored
        OR the edit is moved outside the guarded section
        OR the maintainer re-runs `tools/adr/cli.py synthesize` to
            refresh the section
```

## 9. Trust Audit (Spec-J/K/L)

Before closing a Task (`task_status: done`), the agent MUST run the trust audit:

```bash
python3 tools/check-trust.py
```

This script verifies that every `done` Task has a `friction-log.md` and that the friction log's FL declaration is traceable (Spec-L.3.1 / Spec-L.7.1).

Only when all applicable boxes above are conceptually "checked" may the agent invoke the `submit` or `git commit` commands.
