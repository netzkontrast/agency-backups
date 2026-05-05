---
type: research
status: active
slug: adr-spec-research-synthesis
summary: "Repo-native ADR Governance Specification for netzkontrast/agency. Authoritative §0–§9 contract: storage at /decisions/, adr_* L2 namespace, guarded-section synthesis into AGENTS.md, agency-adr CLI under tools/adr/, supersession DAG with cycle and orphan detection."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: adr-spec-research-synthesis
research_friction_level: FL1
---

# Repo-Native ADR Governance Specification

## §0 Status & Provenance

**Status:** IN-FORCE.
**Target Repository:** [`netzkontrast/agency`](https://github.com/netzkontrast/agency).
**Provenance:** This specification is the synthesised output of [Task 027](../../../tasks/027-adr-spec-research-synthesis/task.md), executed via the [`adr-spec-research-synthesis`](../../../prompts/adr-spec-research-synthesis/prompt.md) prompt. The Gemini draft at [`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`](../../gemini/agency-adr-governance-spec/adr-governance-spec.md) is the theoretical foundation; every §0–§9 block here was re-derived against the actual repo content. The triangulation evidence lives in [`../reflection/M06-source-triangulation.md`](../reflection/M06-source-triangulation.md); the contradictions resolved against Gemini live in [`../reflection/M07-contradictions.md`](../reflection/M07-contradictions.md).

This specification integrates with the existing root files: [`README.md`](../../../README.md), [`AGENTS.md`](../../../AGENTS.md), [`TASK.md`](../../../TASK.md), [`PROMPT.md`](../../../PROMPT.md), [`RESEARCH.md`](../../../RESEARCH.md), [`FOLDERS.md`](../../../FOLDERS.md), [`PRE_COMMIT.md`](../../../PRE_COMMIT.md), [`FRUSTRATED.md`](../../../FRUSTRATED.md), [`MAINTENANCE.md`](../../../MAINTENANCE.md), and [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json).

### World-Change Annotation

The `AGENTS.md` convention is the dominant base-rate for agent-readable repository governance (per [M12] base-rate anchoring in [`../synthesis/methodology.md`](../synthesis/methodology.md)). A parallel emerging standard, `llms.txt`, targets the *web-root level* rather than the repository level; this specification deliberately does not adopt `llms.txt` because the agents this repo orchestrates (Claude Code, Jules, Gemini) read repository files directly. If `llms.txt` becomes a stronger industry default for repo-internal agent guidance, a successor specification will reconsider — that reconsideration MUST go through the supersession DAG defined in §6, not through informal amendment.

The theoretical assumption that infinite-context LLMs make MDL compression obsolete is empirically unsupported as of the 2026-05-05 temporal anchor. Attention recession at high prompt sizes remains observable; this spec retains MDL compression as the synthesis discipline.

---

## §1 Normative Conventions

### §1.1 RFC 2119 / BCP 14 Normative Keywords

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals. This binding is identical to the one declared in [`AGENTS.md`](../../../AGENTS.md) §"RFC 2119 Normative Keywords" and [`maintenance/language-spec.md`](../../../maintenance/language-spec.md); the ADR governance regime inherits it without modification.

### §1.2 Gherkin Syntax Binding

Every acceptance scenario in this document MUST use standard Gherkin syntax (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`). Each `Scenario` MUST carry an `# anchor: <stable-id>` comment on the line immediately above it; the anchor format is `ADR.A.<aspect>.<statement>` (e.g. `ADR.A.4.5`). This anchor convention extends [`AGENTS.md`](../../../AGENTS.md) Gherkin Validity Rules G5.

### §1.3 Style Guide for Normative Statements

- Every normative statement MUST use exactly one BCP-14 keyword per sentence (matches [`AGENTS.md`](../../../AGENTS.md) R1).
- Rationale paragraphs (§X.3) MUST NOT contain RFC 2119 keywords in uppercase (matches R2).
- Every normative statement MUST carry a stable identifier of the form `ADR.A.<aspect>.<statement>` (e.g. `ADR.A.3.4`).
- The aspect numbers are: §3 = Aspect 1 (Explore), §4 = Aspect 2 (Plan), §5 = Aspect 3 (Implement), §6 = Aspect 4 (Review), §7 = Aspect 5 (Validate).

---

## §2 System-Level Conventions

### §2.1 Storage Path

ADR files MUST live under `/decisions/` at the repository root. The path MUST NOT be `docs/decisions/`; the parent `docs/` folder is not authorised by [`FOLDERS.md`](../../../FOLDERS.md) §1 and introducing it would smuggle in a third operational layer for negligible benefit. The path MUST NOT be `research/adr/`; [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1 declares research workspaces immutable post-`complete`, which collides with the ADR `Superseded` lifecycle.

`/decisions/` MUST be added to the [`FOLDERS.md`](../../../FOLDERS.md) §8 "Non-Operational Storage Folders" exemption table as a fifth row. That edit is a T3 change (per [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1) and is sequenced into [Task 028](../../../tasks/028-adr-tooling-impl-plan/task.md).

### §2.2 Frontmatter Composition With L0/L1/L2

Every ADR file MUST carry L0 (optional) + L1 (mandatory) + the new L2 `adr_*` namespace defined in §7. The complete schema is registered in [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) under `types.adr` (Task 028 ships this registration). YAML MUST NOT nest beyond one level (matches [`TASK.md`](../../../TASK.md) §3.4 YAML Depth Rule). Lists MUST contain only scalars.

### §2.3 AGENTS.md Ownership Split (Guarded-Section Synthesis)

The synthesis pipeline MUST write the synthesised normative summary into a *guarded section* of [`AGENTS.md`](../../../AGENTS.md), bounded by exact byte markers:

```text
<!-- BEGIN AGENCY-ADR SYNTHESIS -->
<!-- AGENT-WRITTEN. DO NOT EDIT BY HAND. Edits will be overwritten by tools/adr/cli.py synthesize. -->
... synthesised content derived from Accepted ADRs ...
<!-- END AGENCY-ADR SYNTHESIS -->
```

The pipeline MUST NOT modify any byte outside the markers. The pipeline MUST refuse to write (exit 1, code `ADR.A.3.5`) if either marker is absent. Manual edits inside the markers MUST be overwritten on the next synthesis run. The guarded section MUST end with a footer block citing every contributing ADR by `adr_id` so any synthesised rule is traceable to its source.

The exact insertion point of the markers in the existing [`AGENTS.md`](../../../AGENTS.md) is `[DEFERRED to Task 028]`.

### §2.4 Hook Integration

`agency-adr validate` MUST be invoked as a numbered step inside [`tools/check-governance.sh`](../../../tools/check-governance.sh) (placed after the run-log and narrative-ontology validators, before the trust audit). Direct modification of `.githooks/pre-commit` is prohibited. The validator MUST exit 0 if `/decisions/` is absent or empty.

```text
                       ┌──────────────────────────────┐
git commit  ──────────►│ .githooks/pre-commit (gate)  │
                       └──────────────┬───────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │ tools/check-governance.sh    │
                       └──┬───────┬───────┬───────┬───┘
                          ▼       ▼       ▼       ▼
                    [1] frontmatter     [2] structure
                    [3] linkage         [4] run-log
                    [5] narrative-ontology (gated on ontology.json)
                    [6] ADR governance validator   ◄── Task 028 ships this
                    [7] trust audit (Spec-J/K/L)
```

### §2.5 Branching and Closure

Every ADR-affecting change (creation, status flip, supersession edge) MUST land via the established `claude/<topic>-<date>` branch convention and MUST close with `/sc:createPR` per [`AGENTS.md`](../../../AGENTS.md) §"Closing Run Procedure". The synthesis pipeline MUST be run as part of the same commit that introduces or supersedes an ADR; a commit that mutates `/decisions/` without re-running synthesis MUST be rejected by `agency-adr validate`.

### §2.6 Determinism and Idempotency

A second run of `agency-adr synthesize` against an unchanged ADR corpus MUST produce a byte-identical guarded section. This is verified by an acceptance scenario in §5.2.

---

## §3 Aspect 1 — Explore

This aspect defines how an architecturally significant question is scoped, researched, and verified against prior art before a new ADR is drafted.

### §3.1 Normative Statements

| ID | Keyword | Statement |
|----|---------|-----------|
| ADR.A.1.1 | MUST | The author MUST verify that the proposed change does not duplicate an Accepted ADR currently in `/decisions/`. |
| ADR.A.1.2 | SHOULD | The author SHOULD search Superseded and Deprecated ADRs in `/decisions/` for prior framings of the same topic before drafting. |
| ADR.A.1.3 | MUST | The exploration MUST be limited to architecturally significant requirements that measurably impact repository structure, dependencies, governance, or token-efficiency budgets. |
| ADR.A.1.4 | MUST | The exploration MUST yield a defined problem statement and at least two mutually exclusive technical options. |
| ADR.A.1.5 | MUST | When an autonomous agent triggers an ADR exploration, the agent MUST file a research-proposal Prompt under `/prompts/<slug>/` per [`PROMPT.md`](../../../PROMPT.md) §1.1; the resulting `/research/<slug>/` workspace is the evidence base for the ADR. |
| ADR.A.1.6 | MAY | The exploration MAY consume an existing `/research/<slug>/output/SPEC.md` as evidence rather than spawning a new research run, provided that SPEC's `research_phase` is `complete`. |

### §3.2 Acceptance Criteria

```gherkin
Feature: ADR exploration is bounded and well-scoped

  # anchor: ADR.A.1.1
  Scenario: Duplicate-topic detection halts exploration
    Given /decisions/ contains an Accepted ADR whose adr_tags include "frontmatter-ontology"
    When the author initiates a new exploration with adr_tags including "frontmatter-ontology"
    Then agency-adr validate MUST emit a duplication WARN
    And the WARN MUST cite the existing ADR by adr_id

  # anchor: ADR.A.1.4
  Scenario: Single-option exploration is rejected
    Given an author submits a draft ADR
    And the draft body contains exactly one option block
    When the author commits the draft
    Then agency-adr validate MUST exit 1
    And the diagnostic MUST cite ADR.A.1.4
    And the message MUST state "Exploration requires at least two mutually exclusive options."

  # anchor: ADR.A.1.5
  Scenario: Agent-led exploration leaves an audit trail
    Given an autonomous agent initiates a new ADR exploration
    When the agent finishes evidence-gathering
    Then a research workspace MUST exist at /research/<slug>/
    And /prompts/<slug>/prompt.md MUST exist with prompt_kind: research-proposal
    And the ADR's body MUST link to the research workspace via a relative Markdown link
```

### §3.3 Rationale

the exploration phase is the cheapest place to catch architectural drift, and the only place to enforce "compare at least two options" without burning sprint capacity downstream. duplicate-topic detection prevents the corpus from ballooning with restatements, which would degrade the synthesis pipeline's compression ratio. requiring an audit trail for agent-led explorations preserves the existing repo's task → prompt → research graph (per [`AGENTS.md`](../../../AGENTS.md) §"Task Type Routing"); ADRs do not get a parallel evidence pipeline.

---

## §4 Aspect 2 — Plan

This aspect dictates the structural format, metadata requirements, and drafting protocol for ADR records.

### §4.1 Normative Statements

| ID | Keyword | Statement |
|----|---------|-----------|
| ADR.A.2.1 | MUST | Every ADR file MUST conform to MADR 4.0.0 section structure (`Context and Problem Statement`, `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Consequences`, `Pros and Cons of the Options`). |
| ADR.A.2.2 | MUST | The ADR frontmatter MUST contain valid YAML carrying L1 + the `adr_*` L2 namespace defined in §7. |
| ADR.A.2.3 | MUST | The body MUST include a "Decision Outcome" section that explicitly declares the chosen option in a single sentence. |
| ADR.A.2.4 | MUST | The body MUST include a "Consequences" section enumerating positive, negative, and neutral impacts. |
| ADR.A.2.5 | MUST | Every ADR change MUST land via a `claude/<topic>-<date>` branch and a pull request opened by `/sc:createPR`. |
| ADR.A.2.6 | MAY | The body MAY include a Y-Statement at the top of "Decision Outcome" for token-cheap rationale density. |
| ADR.A.2.7 | MUST | The ADR file MUST be named `decisions/<NNNN>-<slug>.md` where `<NNNN>` is the zero-padded `adr_id` numeric suffix and `<slug>` matches the `slug` L1 field. |

### §4.2 Acceptance Criteria

```gherkin
Feature: ADR records are MADR-compliant and machine-parseable

  # anchor: ADR.A.2.1
  Scenario: Missing required heading rejects the ADR
    Given a draft ADR at decisions/0042-example.md
    And the body is missing the "Decision Outcome" heading
    When agency-adr validate runs in the pre-commit hook
    Then the validator MUST exit 1
    And the diagnostic MUST cite ADR.A.2.1
    And the message MUST name the missing heading

  # anchor: ADR.A.2.2
  Scenario: Frontmatter schema is enforced
    Given a draft ADR with frontmatter missing adr_id
    When agency-adr validate runs
    Then the validator MUST emit ERROR ADR.A.2.2
    And the JSON-Schema violation MUST cite the missing key

  # anchor: ADR.A.2.7
  Scenario: Filename composition mirrors frontmatter
    Given an ADR file at decisions/0042-record-architecture.md
    When agency-adr validate parses the frontmatter
    Then the frontmatter adr_id MUST equal "ADR-0042"
    And the frontmatter slug MUST equal "0042-record-architecture"
    But if either field disagrees with the filename the validator MUST exit 1
```

### §4.3 Rationale

MADR 4.0.0 is the lingua franca of ADR tooling (adr-tools, log4brains, structurizr-adr). adopting it preserves toolchain interoperability if the maintainer ever wants to render the corpus as a static site later. composing `adr_*` additively with the existing L1/L2 ontology is what turns the file from "a markdown file in a folder" into a queryable governance artefact via [`tools/fm/query.py`](../../../tools/fm/query.py). the filename-frontmatter coupling (ADR.A.2.7) catches rename-without-frontmatter-update drift the same way the task folder name and `task_id` are coupled in [`TASK.md`](../../../TASK.md) §2.

---

## §5 Aspect 3 — Implement

This aspect defines the synthesis pipeline that transforms the ADR corpus into the guarded section of `AGENTS.md`.

### §5.1 Normative Statements

| ID | Keyword | Statement |
|----|---------|-----------|
| ADR.A.3.1 | MUST | The synthesis pipeline MUST extract normative content exclusively from the "Decision Outcome" and "Consequences" sections of ADRs whose `adr_status` is `Accepted`. |
| ADR.A.3.2 | MUST | The pipeline MUST compress the extracted content using a Minimum-Description-Length-style discipline (rule deduplication, BCP-14 normalisation, footer-anchor citation). |
| ADR.A.3.3 | MUST | The synthesised guarded section MUST NOT exceed `--token-limit` (default 2000) tokens; on overflow the pipeline MUST exit 1 with code `ADR.A.3.3` and propose a deprecation candidate. |
| ADR.A.3.4 | MUST | The pipeline MUST achieve a fidelity score `≥ --fidelity-floor` (default 0.95) under the algorithm selected by `--fidelity-mode {bcp14-keyword|adr-id-anchor|llm-pass}`; on miss the pipeline MUST exit 1 with code `ADR.A.3.4`. |
| ADR.A.3.5 | MUST | The pipeline MUST write the guarded section in `AGENTS.md` exclusively between the markers defined in §2.3; on missing markers the pipeline MUST exit 1 with code `ADR.A.3.5`. |
| ADR.A.3.6 | MUST | The pipeline MUST be deterministic: the same Accepted-ADR corpus MUST produce a byte-identical guarded section across runs. |
| ADR.A.3.7 | MUST | The pipeline MUST append a record to [`maintenance/run-log.md`](../../../maintenance/run-log.md) per [`MAINTENANCE.md`](../../../MAINTENANCE.md) §2.3 every time it rewrites the guarded section. |

### §5.2 Acceptance Criteria

```gherkin
Feature: Synthesis is bounded, deterministic, and traceable

  # anchor: ADR.A.3.3
  Scenario: Token-limit overflow is rejected
    Given /decisions/ contains 60 Accepted ADRs whose extracted normatives total 3000 tokens
    When agency-adr synthesize --token-limit 2000 runs
    Then the pipeline MUST exit 1
    And the diagnostic MUST cite ADR.A.3.3
    And the message MUST list the lowest-priority ADRs as deprecation candidates

  # anchor: ADR.A.3.5
  Scenario: Missing markers prevent destructive overwrite
    Given AGENTS.md has no <!-- BEGIN AGENCY-ADR SYNTHESIS --> marker
    When agency-adr synthesize runs
    Then the pipeline MUST exit 1
    And the diagnostic MUST cite ADR.A.3.5
    And AGENTS.md MUST be left unmodified byte-for-byte

  # anchor: ADR.A.3.6
  Scenario: Synthesis is idempotent
    Given /decisions/ contains an unchanged Accepted-ADR corpus
    When agency-adr synthesize is invoked twice with identical arguments
    Then the second invocation MUST produce a byte-identical AGENTS.md
    And the run-log MUST record both invocations
    But the diff between the two runs MUST be empty
```

### §5.3 Rationale

the MDL framing forces the pipeline to treat the corpus as a compression problem, separating "learnable structure" (the BCP-14 normative lines) from "unpredictable noise" (the historical narrative). this matters because the guarded section is read on every agent invocation; every redundant token compounds across thousands of sessions. the 2000-token target was inherited from the Gemini draft, but the empirical floor for this repo is `[OPEN]` — at the current `AGENTS.md` size (≈ 4800 tokens by `wc -w` heuristic) and ≈ 40-token average per ADR, ≈ 50 ADRs fit under the limit. the parameterised `--fidelity-mode` admits that the metric algorithm itself is unresolved; defaulting to `bcp14-keyword` means we ship a deterministic, no-LLM v0 immediately and let the assumption audit (Task 029) recommend whether to upgrade.

---

## §6 Aspect 4 — Review

This aspect governs the long-term lifecycle of an ADR: amendment, supersession, deprecation, and conflict resolution.

### §6.1 Normative Statements

| ID | Keyword | Statement |
|----|---------|-----------|
| ADR.A.4.1 | MUST NOT | An Accepted ADR MUST NOT be modified in its frontmatter (other than `adr_status` flips per ADR.A.4.3) or in its "Decision Outcome" body section; it is T4-immutable per [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1. |
| ADR.A.4.2 | MUST | To alter an existing constraint, a new ADR MUST be authored that declares the predecessor's `adr_id` in its `adr_supersedes` list. |
| ADR.A.4.3 | MUST | When a successor ADR is Accepted, `agency-adr` MUST flip every superseded predecessor's `adr_status` from `Accepted` to `Superseded` and set the predecessor's `adr_superseded_by` list reciprocally. |
| ADR.A.4.4 | MUST | The synthesis pipeline MUST resolve conflicting normatives by traversing the supersession DAG, treating any rule whose `adr_status` is `Superseded` or `Deprecated` as not contributing to the synthesised section. |
| ADR.A.4.5 | MUST | `agency-adr validate` MUST run a cycle-detection pass (Kahn's algorithm) over the supersession DAG and MUST exit 1 with code `ADR.A.4.5` on any cycle. |
| ADR.A.4.6 | MUST | Reciprocity between `adr_supersedes` and `adr_superseded_by` MUST be enforced; a missing reciprocal edge MUST exit 1 with code `ADR.A.4.6`. |

### §6.2 Acceptance Criteria

```gherkin
Feature: ADR lifecycle is append-only and DAG-consistent

  # anchor: ADR.A.4.1
  Scenario: Modifying an Accepted ADR's Decision Outcome is rejected
    Given decisions/0007-example.md has adr_status: Accepted
    And a pull request edits the body of its "Decision Outcome" section
    When agency-adr validate runs in the pre-commit hook
    Then the validator MUST exit 1
    And the diagnostic MUST cite ADR.A.4.1
    And the message MUST recommend authoring a superseding ADR

  # anchor: ADR.A.4.5
  Scenario: Cyclic supersession is rejected
    Given ADR-0001 supersedes ADR-0002
    And ADR-0002 supersedes ADR-0003
    When a draft ADR-0003 declares adr_supersedes: [ADR-0001]
    Then agency-adr validate MUST exit 1
    And the diagnostic MUST cite ADR.A.4.5
    And the message MUST list the cycle nodes in topological order

  # anchor: ADR.A.4.6
  Scenario: Reciprocity is enforced both directions
    Given ADR-0042 declares adr_supersedes: [ADR-0017]
    And ADR-0017's adr_superseded_by list is empty
    When agency-adr validate runs
    Then the validator MUST exit 1
    And the diagnostic MUST cite ADR.A.4.6
    And the message MUST identify the missing reciprocal edge
```

### §6.3 Rationale

the append-only ledger is the same pattern the repo already uses for `task_supersedes`/`task_superseded_by` ([`TASK.md`](../../../TASK.md) §4.7) and for completed research workspaces ([`MAINTENANCE.md`](../../../MAINTENANCE.md) §1 T4). reusing it for ADRs minimises the cognitive overhead for contributors who already know the rule. the DAG-traversal model resolves conflict between rules by *recency-on-the-graph*, not recency-by-date — which means a back-port (an ADR that supersedes a younger ADR) is representable as long as it is acyclic. cycle detection is the only correctness invariant the synthesis pipeline genuinely cannot recover from; any cycle would induce infinite recursion in the conflict-resolution traversal.

---

## §7 Aspect 5 — Validate

This aspect defines the strict acceptance criteria for the tooling: schema validation, CLI shape, system idempotency.

### §7.1 Normative Statements

| ID | Keyword | Statement |
|----|---------|-----------|
| ADR.A.5.1 | MUST | The CLI tooling MUST provide an `agency-adr validate` sub-command that checks every ADR file in `/decisions/` against the JSON-Schema in §7.4. |
| ADR.A.5.2 | MUST | The CLI tooling MUST provide an `agency-adr synthesize` sub-command that runs the §5 pipeline and writes the guarded section. |
| ADR.A.5.3 | MUST | `synthesize` MUST accept `--token-limit`, `--fidelity-floor`, and `--fidelity-mode` flags; defaults are `2000`, `0.95`, and `bcp14-keyword` respectively. |
| ADR.A.5.4 | MUST | The ADR YAML frontmatter MUST conform to the JSON-Schema in §7.4 (exit 1 on any violation). |
| ADR.A.5.5 | MUST | The CLI MUST exit `0` on success and `1` on any ERROR diagnostic; `--strict` MUST promote WARN-level diagnostics to non-zero exit. |
| ADR.A.5.6 | MUST | `agency-adr validate` MUST emit ERROR `ADR.A.5.6` on any duplicate `adr_id` across the corpus. |
| ADR.A.5.7 | MUST | `agency-adr validate` MUST emit ERROR `ADR.A.5.7` on any `adr_supersedes` reference whose target file does not exist in `/decisions/`. |
| ADR.A.5.8 | MUST | `agency-adr` MUST be invocable as `python3 tools/adr/cli.py [validate|synthesize]` and MUST be invoked from [`tools/check-governance.sh`](../../../tools/check-governance.sh) per §2.4. |
| ADR.A.5.9 | MUST | `agency-adr` MUST reuse [`tools/fm/_core.py`](../../../tools/fm/_core.py) for frontmatter parsing and diagnostic formatting; reimplementation is prohibited. |

### §7.2 Acceptance Criteria

```gherkin
Feature: agency-adr CLI is correct, composable, and reuses tools/fm/

  # anchor: ADR.A.5.1
  Scenario: Validate exits 0 on a clean corpus
    Given /decisions/ contains 5 ADRs all conforming to §7.4
    When the user runs python3 tools/adr/cli.py validate
    Then the process MUST exit 0
    And the stdout MUST be empty or contain only INFO diagnostics

  # anchor: ADR.A.5.2
  Scenario: Synthesize writes the guarded section
    Given /decisions/ contains 5 Accepted ADRs
    And AGENTS.md contains both BEGIN and END AGENCY-ADR SYNTHESIS markers
    When the user runs python3 tools/adr/cli.py synthesize --token-limit 2000
    Then AGENTS.md MUST be modified only between the markers
    And the process MUST exit 0
    And maintenance/run-log.md MUST gain one new record

  # anchor: ADR.A.5.6
  Scenario: Duplicate adr_id is rejected
    Given /decisions/ contains two files with frontmatter adr_id: ADR-0042
    When the user runs python3 tools/adr/cli.py validate
    Then the process MUST exit 1
    And the diagnostic MUST cite ADR.A.5.6
    And the diagnostic MUST list both file paths

  # anchor: ADR.A.5.8
  Scenario: agency-adr participates in the gate
    Given tools/check-governance.sh runs in pre-commit
    When the script reaches the ADR governance step
    Then python3 tools/adr/cli.py validate MUST be invoked
    And a non-zero exit MUST set the script's overall FAIL state
```

### §7.3 Rationale

reusing [`tools/fm/_core.py`](../../../tools/fm/_core.py) eliminates an entire class of drift: when the L1 ontology evolves (new keys added to `header-ontology.json`), `agency-adr` inherits the change automatically. cycle detection, duplicate-ID detection, and orphan-reference detection are three orthogonal validators; a single CLI invocation runs all three and folds them into one exit code so the pre-commit hook stays simple. the dual-toolchain transition (legacy linters + `FM_TOOLCHAIN=1` flexible) is honoured by composition: when Task 019 flips `FM_TOOLCHAIN=1` to default, `agency-adr` re-registers against the flexible toolchain's diagnostic plumbing without changing its CLI shape.

### §7.4 JSON-Schema for ADR Frontmatter

This schema MUST be merged into [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) under `types.adr` by [Task 028](../../../tasks/028-adr-tooling-impl-plan/task.md). The `additionalProperties: true` value is intentional: future L2 keys (`adr_owner`, `adr_blast_radius`, …) MUST extend the schema additively without breaking existing files.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "ADR L1 + adr_* L2 namespace",
  "properties": {
    "type":     { "const": "adr" },
    "status":   { "type": "string", "enum": ["draft", "active", "archived"] },
    "slug":     { "type": "string", "pattern": "^[0-9]{4}-[a-z0-9-]+$" },
    "summary":  { "type": "string", "maxLength": 240 },
    "created":  { "type": "string", "format": "date" },
    "updated":  { "type": "string", "format": "date" },

    "adr_id":         { "type": "string", "pattern": "^ADR-[0-9]{4}$" },
    "adr_status":     { "type": "string", "enum": ["Proposed", "Accepted", "Superseded", "Deprecated"] },
    "adr_supersedes": {
      "type": "array",
      "items": { "type": "string", "pattern": "^ADR-[0-9]{4}$" }
    },
    "adr_superseded_by": {
      "type": "array",
      "items": { "type": "string", "pattern": "^ADR-[0-9]{4}$" }
    },
    "adr_owner": { "type": "string" }
  },
  "required": ["type", "status", "slug", "summary", "created", "updated", "adr_id", "adr_status"],
  "additionalProperties": true
}
```

L0 Obsidian keys (`tags`, `aliases`, `cssclasses`) remain optional and are NOT duplicated as `adr_*` keys; the existing L0 path is reused.

### §7.5 CLI Shape Reference

```text
agency-adr validate [PATH ...]
                    [--scope=decisions]
                    [--strict]
                    [--format=text|json]

agency-adr synthesize [--token-limit=N]
                      [--fidelity-floor=F]
                      [--fidelity-mode=bcp14-keyword|adr-id-anchor|llm-pass]
                      [--dry-run]
                      [--format=text|json]

Exit:
  0 — no ERROR diagnostics
  1 — at least one ERROR diagnostic (or any WARN under --strict)
```

This shape mirrors [`tools/fm/validate.py`](../../../tools/fm/validate.py)'s argparse signature for consistency.

---

## §8 Known Limitations & Open Questions

Every `[OPEN]` and `[DEFERRED]` item from [`../workspace/brainstorm.md`](../workspace/brainstorm.md) is surfaced here with an explicit owner and unblock condition. Resolving an `[OPEN]` item mutates this specification only via supersession (per §6); patching `output/SPEC.md` in place is prohibited under [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1 T4 immutability of `research_phase: complete` workspaces.

| ID | Item | State | Owner | Unblock condition |
|----|------|-------|-------|-------------------|
| OQ.1 | Migration cardinality: Strategy A (14 ADRs, one per implicit decision) vs Strategy B (≈ 5 ADRs clustered by surface). | `[OPEN]` | Maintainer | Recommendation from [Task 029](../../../tasks/029-adr-assumption-audit/task.md) before the first ADR is authored. |
| OQ.2 | Fidelity-metric algorithm: `bcp14-keyword` (deterministic), `adr-id-anchor` (graph-based), or `llm-pass` (LLM verifier). | `[OPEN]` | Maintainer | Task 029 audit recommendation + Task 028 prototype benchmarks; current default `bcp14-keyword` is provisional. |
| OQ.3 | Token-limit empirical floor: current `AGENTS.md` ≈ 4800 tokens by heuristic; 2000-token guarded section is aspirational. | `[OPEN]` | Maintainer | Once the first synthesis run reports the actual tokeniser count. |
| OQ.4 | Whether `tools/.frontmatter-waivers` covers `/decisions/` files; this spec leans NO (waivers MUST burn down per [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.B). | `[OPEN]` | Maintainer | Decision recorded as either an ADR (if waivers ARE permitted for `/decisions/`) or a Task that hardens `tools/.frontmatter-waivers` to refuse such entries. |
| OQ.5 | Whether `adr_status: Proposed` ADRs participate in synthesis; spec defaults to NO. | `[DEFERRED to Task 028]` | Task 028 | Implementation plan ratifies the default; if changed, a new ADR documents the decision. |
| OQ.6 | Exact insertion location of `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers in `AGENTS.md`. | `[DEFERRED to Task 028]` | Task 028 | Implementation plan finalises the byte range. |
| OQ.7 | Static-site rendering of `/decisions/` (analogous to log4brains). | `[DEFERRED]` | unassigned | Demand-driven; unblock when a maintainer requests the rendering surface. |

Each `[OPEN]` item, when resolved, MUST be encoded either as a new ADR (if it concerns governance) or as a Task closure note (if it concerns implementation only).

---

## §9 Knowledge Base Index

### §9.1 Sources Consumed

| # | Source | Tier | Used For |
|---|--------|------|----------|
| 1 | [`AGENTS.md`](../../../AGENTS.md) | repo-canon | §1 (RFC 2119 + Gherkin), §2 (frontmatter ontology), §2.5 (closing run procedure) |
| 2 | [`TASK.md`](../../../TASK.md) | repo-canon | §2.2 (frontmatter composition), §6 (supersession reciprocity precedent) |
| 3 | [`PROMPT.md`](../../../PROMPT.md) | repo-canon | §3.1 ADR.A.1.5 (research-proposal Prompt), §3.3 rationale |
| 4 | [`RESEARCH.md`](../../../RESEARCH.md) | repo-canon | §3.1 ADR.A.1.5 (research workspace audit trail) |
| 5 | [`FOLDERS.md`](../../../FOLDERS.md) | repo-canon | §2.1 (storage path resolution), §2.4 (operational folder partition) |
| 6 | [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) | repo-canon | §2.4 (hook integration), §7.1 ADR.A.5.8 |
| 7 | [`MAINTENANCE.md`](../../../MAINTENANCE.md) | repo-canon | §6.1 ADR.A.4.1 (T4 immutability paradigm), §5.1 ADR.A.3.7 (run-log) |
| 8 | [`FRUSTRATED.md`](../../../FRUSTRATED.md) | repo-canon | implicit: closure-with-friction-log obligation inherits to ADR PRs |
| 9 | [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) | repo-canon-tooling | §7.4 (composition target) |
| 10 | [`tools/check-governance.sh`](../../../tools/check-governance.sh) + [`tools/fm/`](../../../tools/fm/) | repo-tooling | §7.1 (CLI integration), §7.5 (CLI shape mirror) |
| 11 | [`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`](../../gemini/agency-adr-governance-spec/adr-governance-spec.md) | external-research | §0–§9 structural template (re-derived, not copied) |
| 12 | Nygard (2011) "Documenting Architecture Decisions" | external-canon | implicit: MADR lineage |
| 13 | MADR 4.0.0 specification | external-canon | §4.1 ADR.A.2.1 (template structure) |
| 14 | Pryce, `adr-tools` | external-tooling | §4.1 (sequential numbering) |
| 15 | Thomvaill, `log4brains` | external-tooling | §6.1 (frontmatter-driven supersession) |

### §9.2 Contradictions Resolved

The full table lives in [`../reflection/M07-contradictions.md`](../reflection/M07-contradictions.md). Summary:

| Contradiction | Resolution |
|---|---|
| C1 — `docs/decisions/` vs `decisions/` | `decisions/` (§2.1) |
| C2 — `id/title/status/date` vs L1 + `adr_*` | L1 + `adr_*` (§7.4) |
| C3 — wholesale overwrite vs guarded section | guarded section (§2.3) |
| C4 — standalone CLI vs `tools/`-co-located | `tools/adr/cli.py` (§7.1) |
| C5 — exit codes 0 / >0 vs 0 / 1 + `--strict` | 0 / 1 + `--strict` (§7.1 ADR.A.5.5) |
| C6 — separate "DAG validation phase" vs `check-governance.sh` step | numbered step in `check-governance.sh` (§2.4) |
| C7 — strict 2000-token ceiling vs aspirational floor | guarded-section-only limit, configurable, `[OPEN]` (OQ.3) |
| C8 — fidelity floor 0.95 enforceable vs algorithm undefined | floor declared MUST; algorithm parameterised, `[OPEN]` (OQ.2) |
| C9 — CI-rejection immutability vs T4 immutability | reuse T4 paradigm via `agency-adr validate` (§6.1) |
| C10 — implicit `PRE_COMMIT.md` integration vs explicit `check-governance.sh` step | explicit step (§2.4) |

### §9.3 Query Expansion Log

The full M13 expansion across four axes lives in [`../reflection/M13-query-expansion.md`](../reflection/M13-query-expansion.md).

| Axis | Findings That Modified This Spec |
|------|----------------------------------|
| Adjacent | Added explicit `ADR-NNNN` numbering convention (matches log4brains) — §4.1 ADR.A.2.7. |
| Opposing | Added ADR.A.5.6 (duplicate-id) and ADR.A.5.7 (orphan-reference) — §7.1, prompted by anticipated failure modes. |
| Abstraction | Cited the human-narrative + machine-extractable principle in §2.3 and §5.3 rationale for future challengeability. |
| Orthogonal (MDL) | Documented the 50-ADR practical capacity at the 2000-token limit — §5.3 rationale; surfaced empirical floor as OQ.3. |

### §9.4 Reflection Audit (CB0)

All five mandatory reflection checkpoints (Kickoff, Mid-run, Post-M13, Pre-synthesis, Post-synthesis) were honoured during this run; the entries live in [`../reflection/M13-query-expansion.md`](../reflection/M13-query-expansion.md) §"Reflection Regime".
