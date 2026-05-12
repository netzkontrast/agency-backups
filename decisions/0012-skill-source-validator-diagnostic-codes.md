---
type: adr
status: active
slug: 0012-skill-source-validator-diagnostic-codes
summary: "Amendment to ADR-0011 ratifying F.B.8 / F.B.9 (not F.B.7 / F.B.8) as the authoritative diagnostic codes for the skill_source validator extension. Resolves the renumber forced by the pre-existing F.B.7 WARN-tier code in tools/fm/validate.py."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0012
adr_status: Accepted
adr_owner: agency-maintainer
adr_tags:
  - skills
  - validator
  - diagnostic-codes
  - amendment
---

# ADR-0012 — Skill-source validator diagnostic codes (F.B.8 / F.B.9)

## Context and Problem Statement

[ADR-0011](./0011-external-skill-corpora-import.md) §10.2 specified the validator extension that registers the new `skill_source` L2 frontmatter key. Section §10.2 reserved two diagnostic codes:

- **`F.B.7`** — ERROR — `skill_source` present on a bare-slug (Agency-native) skill folder (D.1 violation).
- **`F.B.8`** — ERROR — `skill_source` value does not match `^(superclaude|superpowers)@v\d+\.\d+\.\d+$` (D.2 violation).

The ADR's `## Acceptance Criteria` Gherkin block at anchor `ADR.11.2` cites these codes verbatim:

> ```gherkin
> # anchor: ADR.11.2
> Scenario: Validator accepts skill_source on imports, rejects on natives
>   Given tools/fm/validate.py runs over /skills/
>   When it encounters a SKILL.md with skill_source set
>   Then it MUST accept the key if the folder path matches the vendor-prefix rule (D.1)
>   And it MUST reject the key with diagnostic F.B.7 if the folder is a bare slug (Agency native)
>   And it MUST reject a malformed value with diagnostic F.B.8
> ```

Task 091 ST-1 ([PR #115](https://github.com/netzkontrast/agency/pull/115), commit `680f24b`) implemented the validator extension. Inspection of [`tools/fm/validate.py:143`](../tools/fm/validate.py) revealed that `F.B.7` was **already in use** as a **WARN-tier** code by the existing `_check_body_for_type` function (task_list completion check). Sharing the code across two unrelated check families would:

1. Break `grep`-based diagnostic triage (a single code matches two different message templates).
2. Conflict with the diagnostic-explanations registry at [`maintenance/schemas/diagnostic-explanations.json`](../maintenance/schemas/diagnostic-explanations.json) (the registry maps one code to one entry).
3. Confuse the per-rule waiver mechanism in [`tools/.frontmatter-waivers`](../tools/.frontmatter-waivers) — a `F.B.7` rule-id row would silence two unrelated checks.

Task 091 ST-1 therefore implemented the new codes as **`F.B.8`** and **`F.B.9`** instead of `F.B.7` / `F.B.8`. The friction-log entry [`tasks/091-port-external-skill-corpora/friction-log.md` FL1.1](../tasks/091-port-external-skill-corpora/friction-log.md) records this divergence.

ADR-0011 is `adr_status: Accepted` and is therefore **T4-immutable** per [`MAINTENANCE.md §1`](../MAINTENANCE.md): the F.B.7 / F.B.8 reference inside its Gherkin block cannot be edited in-place even additively. The peer review of Task 091 ST-1 ([`tasks/091-…/review-st1.md`](../tasks/091-port-external-skill-corpora/review-st1.md) Issue 2) explicitly flagged this and required a successor ADR to ratify the as-shipped code pair.

This ADR is that successor. It amends ADR-0011's diagnostic-code references without rewriting ADR-0011's body.

## Decision Drivers

- **DD.1** — `F.B.7` cannot be both an ERROR and a WARN code in the same toolchain (operational requirement: one code = one tier = one message template).
- **DD.2** — ADR-0011 §D.1 / §D.2 normative clauses are unchanged; only the diagnostic-code numbers inside `ADR.11.2`'s Gherkin diverge from implementation.
- **DD.3** — Re-running validators against ADR-0011 produces no F.B.7 ERROR (the actual emit is F.B.8 / F.B.9), so an external test harness reading ADR.11.2 verbatim would silently false-negative.

## Considered Options

### Option A — Edit ADR-0011 in place

Swap `F.B.7` / `F.B.8` → `F.B.8` / `F.B.9` directly inside the `ADR.11.2` Gherkin block of [ADR-0011](./0011-external-skill-corpora-import.md).

- **Positives.** Single-file change. No new ADR clutter in the ledger.
- **Negatives.** Accepted ADRs are **T4-immutable** per [`MAINTENANCE.md §1`](../MAINTENANCE.md). Editing the normative `## Acceptance Criteria` block — even "additively" — is the canonical T4 violation: the ADR's executable test surface is its contract, and rewriting that contract retroactively destroys the audit guarantee that "what was accepted is what's recorded". Cost: governance-rule violation; rejected on principle.

### Option B — Renumber pre-existing F.B.7

Rename the current WARN-tier `F.B.7` (task_list completion check) to `F.B.10`, freeing `F.B.7` for the new ERROR-tier skill_source check.

- **Positives.** Lets the implementation match ADR-0011's verbatim Gherkin without a new ADR.
- **Negatives.** Every existing cite of `F.B.7` (test suite, body-schema tests in [`tools/tests/fm/test_body_schema.py`](../tools/tests/fm/test_body_schema.py), per-rule waivers ledger, any operator documentation) would need synchronised renames. High blast radius for cosmetic gain; risks introducing real regressions. Cost: high; rejected as not worth the breakage.

### Option C — File this amendment ADR (chosen)

Author a new ADR (this one) that ratifies the as-shipped `F.B.8` / `F.B.9` codes as authoritative, citing ADR-0011's substantive D.1–D.9 clauses as unchanged. ADR-0011's `## Acceptance Criteria` Gherkin block survives verbatim in the ledger; this ADR's `## Acceptance Criteria` (ADR.12.1 / ADR.12.2 / ADR.12.3) supersede its specific code-number references via the `adr_relates_to` graph.

- **Positives.** Preserves ADR-0011's T4-immutability. Treats the ADR ledger as append-only (consistent with [ADR-0003](./0003-frontmatter-source-of-truth.md)'s "frontmatter as source of truth" principle). Surface area minimal: a single short amendment ADR. Future readers who reach the inconsistency follow the `adr_relates_to` edge from 0011 to 0012 and find the canonical numbering.
- **Negatives.** Two adjacent ADRs touching the same subsystem. A reader who reads ADR-0011 alone will infer the wrong codes — mitigated by the cross-reference in ADR-0011's `Cross-references` (which is itself **not** edited; the linkage flows only through this ADR's reciprocal cite).

## Decision Outcome

**Chosen: Option C** — file this amendment ADR.

Three normative clauses replace the F.B.7 / F.B.8 references in ADR-0011 §D.2 and §ADR.11.2:

- **D.1 (renumber).** The validator MUST emit diagnostic code **`F.B.8`** (ERROR) when `skill_source` is set on a bare-slug (Agency-native) skill folder. This replaces the `F.B.7` reference in ADR-0011 §10.2 and §ADR.11.2.
- **D.2 (renumber).** The validator MUST emit diagnostic code **`F.B.9`** (ERROR) when `skill_source` does not match the regex `^(superclaude|superpowers)@v\d+\.\d+\.\d+$`. This replaces the `F.B.8` reference in ADR-0011 §10.2 and §ADR.11.2.
- **D.3 (registry).** The diagnostic-explanations registry [`maintenance/schemas/diagnostic-explanations.json`](../maintenance/schemas/diagnostic-explanations.json) SHOULD gain entries for `F.B.8` and `F.B.9` (what / why / fix triplets) so `tools/fm/validate.py --explain` produces useful output. This is a follow-up T2 commit, NOT a blocker on the ADR's `Accepted` flip.

ADR-0011 D.1–D.9 (substantive normative clauses, namespace, source pin, citation, agent-as-skill, modes-as-references, T2 body cap, no SessionStart injection, body adaptation, sync cadence) all remain in force. This amendment narrows only the diagnostic-code numbering inside ADR-0011's executable test surface.

## Consequences

### Positive

- ADR-0011's Acceptance Criteria are now executable: an external test harness reading both ADRs (0011 first, 0012 second) sees a consistent F.B.8 / F.B.9 expectation.
- The amendment ADR pattern is established for future "spec-implementation reconciliation" cases.
- `F.B.7` remains exclusively a WARN-tier code for the task_list completion check; no semantic overload.

### Negative

- ADR readers MUST follow the `adr_relates_to` graph (this ADR cites ADR-0011) to discover the renumber. A reader who reads ADR-0011 alone will infer the wrong codes.
- The ADR ledger now carries two adjacent ADRs touching the same subsystem (ADR-0011 + ADR-0012). This is the cost of preserving T4-immutability.

### Neutral

- `tools/fm/validate.py` requires no code change — it already emits F.B.8 / F.B.9 as of commit `680f24b`. The 6 tests in `tools/tests/fm/test_validate_skill_source.py` already assert F.B.8 / F.B.9.
- No tooling-config change required. No waiver entries change.

## Cross-references

- **Amended ADR:** [`0011-external-skill-corpora-import.md`](./0011-external-skill-corpora-import.md) (`adr_status: Accepted`). Normative clauses D.1–D.9 survive verbatim; this ADR overrides only the diagnostic-code references inside §10.2 and §ADR.11.2.
- **Friction-log entry:** [`tasks/091-port-external-skill-corpora/friction-log.md` FL1.1](../tasks/091-port-external-skill-corpora/friction-log.md) — original record of the renumber.
- **Peer-review issue:** [`tasks/091-port-external-skill-corpora/review-st1.md` Issue 2](../tasks/091-port-external-skill-corpora/review-st1.md) — the reviewer who flagged that FL1.1's original T2-edit recommendation was T4-prohibited and required this amendment-ADR path instead.
- **Implementation:** [`tools/fm/validate.py:_check_skill_source`](../tools/fm/validate.py) (commit `680f24b`, PR #115). 6 tests at [`tools/tests/fm/test_validate_skill_source.py`](../tools/tests/fm/test_validate_skill_source.py), all green.
- **Governing root specs:** [`MAINTENANCE.md §1`](../MAINTENANCE.md) (T4-immutability rule), [`PRE_COMMIT.md §7.A`](../PRE_COMMIT.md) (Flexible toolchain diagnostic mapping).
- **Sibling ADRs cited:** [`0003-frontmatter-source-of-truth.md`](./0003-frontmatter-source-of-truth.md) (ledger append-only principle), [`0007-skill-bundles-tools-frontmatter.md`](./0007-skill-bundles-tools-frontmatter.md) (precedent for skill-validator L2 amendments).

## Acceptance Criteria

```gherkin
Feature: ADR-0012 ratifies F.B.8 / F.B.9 as the authoritative skill_source codes

  # anchor: ADR.12.1
  Scenario: F.B.8 fires on bare-slug skill_source violation
    Given tools/fm/validate.py runs over a skills/<bare-slug>/SKILL.md
    When the file's frontmatter contains skill_source: "superclaude@v4.3.0"
    Then the validator MUST emit diagnostic code F.B.8
    And the emit MUST NOT be diagnostic code F.B.7

  # anchor: ADR.12.2
  Scenario: F.B.9 fires on malformed skill_source value
    Given tools/fm/validate.py runs over a skills/sc-<slug>/SKILL.md
    When the file's frontmatter contains skill_source: "superclaude@latest"
    Then the validator MUST emit diagnostic code F.B.9
    And the emit MUST NOT be diagnostic code F.B.8

  # anchor: ADR.12.3
  Scenario: F.B.7 retains its WARN-tier task_list semantics
    Given tools/fm/validate.py --check-body runs over a task.md whose Todo section is all-checked
        but whose task_status frontmatter is not 'done'
    When the body-schema check evaluates the task_list completion rule
    Then the validator MUST emit diagnostic code F.B.7 at WARN severity
    And the emit MUST NOT collide with the ERROR-tier skill_source checks (F.B.8 / F.B.9)
```
