---
type: note
status: active
slug: adr-tooling-impl-plan
summary: "Build plan for the agency-adr CLI suite: tooling-primitive audit, module decomposition, acceptance test map, GitHub Actions spec, PRE_COMMIT.md hook spec, open decisions, and complexity estimate. Implementation contracts only — no working code."
created: 2026-05-05
updated: 2026-05-05
---

# `agency-adr` Implementation Plan

This plan executes [Task 028](./task.md) by translating the `[OPEN]` and `[DEFERRED]` boundaries of [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) (the "ADR spec") into a sequenced, unambiguous build order. Every normative ID below cites the SPEC anchor (`ADR.A.<aspect>.<stmt>`).

## §1 Existing-Tooling Audit

### §1.1 Reusable Primitives in `tools/fm/`

| Primitive | File | Public surface | Reuse by `agency-adr`? | Notes |
|---|---|---|---|---|
| Frontmatter parsing (depth-1 enforced) | `tools/fm/_core.py` | `parse_frontmatter(text, strict=True) → dict` | YES — exclusive | Replaces any in-house YAML loader; honours `Diag` exception protocol. |
| `Diagnostic` dataclass | `tools/fm/_core.py` | `Diagnostic(rel, line, severity, code, message)` | YES — exclusive | Every ADR diagnostic MUST be emitted via this shape so `--format=json` composes cleanly with the rest of the toolchain. |
| Heading walker (`# … ##` aware) | `tools/fm/_core.py` | `find_section_body(text, heading, nth=1) → str | None` | YES | Extracts "Decision Outcome" / "Consequences" bodies for synthesis (per ADR.A.3.1). |
| Section shape detector | `tools/fm/_core.py` | `detect_shape(section_body) → str` (`paragraph|ordered_list|...`) | YES — for body-schema checks | Underwrites ADR.A.2.3 / ADR.A.2.4 verification. |
| Required-headings ontology loader | `tools/fm/_core.py` | `load_ontology() → dict` (reads `maintenance/schemas/header-ontology.json`) | YES — exclusive | Drives §7.4 ADR JSON-Schema lookup. |
| File traversal with frontmatter filter | `tools/fm/query.py` | argparse CLI `--scope`, `--type`, `key=value` | YES — invoked as a sub-process or library import | Used for "list every Accepted ADR" without re-walking the tree. |
| Section read | `tools/fm/extract.py` | argparse CLI `--section <name>` | YES — sub-process invocation | Useful for dry-run / audit traces; not on the synthesis hot path. |
| Frontmatter mutation (T1/T2 with file-lock) | `tools/fm/edit.py` | `--set key=value`, `--append-list`, `--unset` | YES — for `adr_status` flip on supersession (ADR.A.4.3) | Preserves body bytes; refuses YAML depth > 1. |
| Diagnostic JSON serialisation | `tools/fm/validate.py` | `--format=json` | YES — copy the convention | `agency-adr --format=json` emits the same structure. |
| Pre-commit shim composition | `tools/check-governance.sh` | numbered-step stdout + per-step exit | YES — append a new `[N/N] ADR governance validator` step | Per ADR.A.5.8. |

### §1.2 Dependency Management

The repo declares its Python dependencies in [`tools/requirements.txt`](../../tools/requirements.txt): `PyYAML>=6.0`, `jsonschema>=4.18`, `pytest>=7.0`. There is no `pyproject.toml` and no installed entry point. The bootstrap script is [`install.sh`](../../install.sh).

Implications for `agency-adr`:

- New runtime deps MUST be added to `tools/requirements.txt`. Anticipated additions: none (the planned modules use only stdlib + `jsonschema` + the in-repo `tools/fm/_core.py`).
- The CLI MUST be invocable as `python3 tools/adr/cli.py [validate|synthesize]` (per ADR.A.5.8). A `setup.py` / `pyproject.toml` entry-point is OUT of scope; consistency with the rest of `tools/` wins.
- A symlink `tools/adr/agency-adr → cli.py` MAY be introduced as an ergonomics affordance once the implementation lands; that decision is deferred to the implementation Task that succeeds Task 028.
- `tools/adr/` MUST follow the same Python style as `tools/fm/`: `from __future__ import annotations`, `pathlib.Path`, hand-rolled argparse, no Click. The fall-back `if __package__ in (None, ""):` import shim is mandatory so the file works as a script and as a module.

### §1.3 Existing Files NOT Touched by `agency-adr`

The following files MUST NOT be modified by the `agency-adr` runtime:

| File | Reason |
|---|---|
| `.githooks/pre-commit` | Per ADR.A.5.8 / SPEC §2.4, the only gate edit is via `tools/check-governance.sh`. |
| `tools/validate-frontmatter.py`, `tools/lint-{structure,linkage,runlog}.py` | Legacy linters owned by Task 001 lineage; the ADR validator composes alongside, not on top. |
| Every `research/<slug>/output/SPEC.md` already at `research_phase: complete` | T4-immutable per `MAINTENANCE.md §1`. |

---

## §2 Module Decomposition

### §2.1 Module Inventory

All modules live under `tools/adr/`. Build phases enforce dependency order: a phase-N module MUST NOT import a phase-(N+1) module.

| Phase | Module | Path | Single Responsibility | Public Interface (signatures only) | Internal Deps | External Deps |
|---|---|---|---|---|---|---|
| 1 | `__init__.py` | `tools/adr/__init__.py` | Package marker; re-export public symbols. | `__all__ = ["validate", "synthesize"]` | — | — |
| 1 | `schema.py` | `tools/adr/schema.py` | JSON-Schema validation of ADR YAML frontmatter (ADR.A.2.2, ADR.A.5.4). | `def validate_frontmatter(fm: dict, *, ontology: dict) -> list[Diagnostic]:` | `tools/fm/_core` (Diagnostic, load_ontology) | `jsonschema` |
| 1 | `body.py` | `tools/adr/body.py` | MADR section presence + shape verification (ADR.A.2.1, ADR.A.2.3, ADR.A.2.4, ADR.A.4.1 textual diff). | `def validate_body(text: str, rel: str) -> list[Diagnostic]:` | `tools/fm/_core` (find_section_body, detect_shape, Diagnostic) | — |
| 2 | `corpus.py` | `tools/adr/corpus.py` | Discover and parse every ADR file in `decisions/`; expose typed records. | `def load_corpus(root: Path = Path('decisions')) -> list[AdrRecord]:` and `@dataclass class AdrRecord` | `schema`, `body`, `tools/fm/_core` | — |
| 2 | `graph.py` | `tools/adr/graph.py` | Build the supersession DAG; cycle detection; reciprocity check; orphan-reference detection (ADR.A.4.4 – A.4.6, A.5.7). | `def build_graph(corpus: list[AdrRecord]) -> AdrGraph:` and `def detect_cycles(g: AdrGraph) -> list[list[str]]:` and `def check_reciprocity(g: AdrGraph) -> list[Diagnostic]:` and `def check_orphans(g: AdrGraph) -> list[Diagnostic]:` | `corpus` | — (Kahn's algorithm in stdlib) |
| 2 | `ids.py` | `tools/adr/ids.py` | Duplicate-`adr_id` detection (ADR.A.5.6); filename-frontmatter coupling (ADR.A.2.7). | `def check_unique_ids(corpus: list[AdrRecord]) -> list[Diagnostic]:` and `def check_filename_coupling(corpus: list[AdrRecord]) -> list[Diagnostic]:` | `corpus` | — |
| 3 | `extract.py` | `tools/adr/extract.py` | Pull "Decision Outcome" + "Consequences" from Accepted ADRs (ADR.A.3.1); BCP-14 normalisation. | `def extract_normatives(corpus: list[AdrRecord]) -> list[Normative]:` and `@dataclass class Normative` | `corpus`, `graph` (filter to live nodes), `tools/fm/extract` (section read) | — |
| 3 | `compress.py` | `tools/adr/compress.py` | MDL-style compression: rule deduplication, footer-citation, token counting (ADR.A.3.2, ADR.A.3.3). | `def compress(normatives: list[Normative], *, token_limit: int) -> CompressedSection:` and `def count_tokens(text: str) -> int:` | `extract` | — |
| 3 | `fidelity.py` | `tools/adr/fidelity.py` | Fidelity score under selectable algorithm (ADR.A.3.4). | `def score(corpus: list[AdrRecord], compressed: CompressedSection, *, mode: str) -> float:` (`mode in {"bcp14-keyword", "adr-id-anchor", "llm-pass"}`) | `extract`, `compress` | — (`llm-pass` deferred — see §6 OD.2) |
| 4 | `synthesize.py` | `tools/adr/synthesize.py` | Orchestrator: corpus → graph filter → extract → compress → fidelity gate → guarded-section write. Idempotent (ADR.A.3.5, ADR.A.3.6, ADR.A.3.7). | `def synthesize(*, agents_md: Path, decisions_root: Path, token_limit: int, fidelity_floor: float, fidelity_mode: str, dry_run: bool) -> SynthesizeResult:` and `@dataclass class SynthesizeResult` | `corpus`, `graph`, `extract`, `compress`, `fidelity` | — |
| 4 | `runlog.py` | `tools/adr/runlog.py` | Append a record to `maintenance/run-log.md` per ADR.A.3.7. | `def append_run_record(result: SynthesizeResult) -> None:` | — | — |
| 5 | `cli.py` | `tools/adr/cli.py` | argparse entry (sub-commands `validate` / `synthesize`); composes everything; emits text/JSON; sets exit code (ADR.A.5.1, ADR.A.5.2, ADR.A.5.3, ADR.A.5.5). | `def main(argv: list[str] | None = None) -> int:` | every module above | — |
| 5 | `readme.md` | `tools/adr/readme.md` | Folder index (per `FOLDERS.md §3`). | — | — | — |

### §2.2 Public Interface Excerpts (Type Signatures Only)

```python
# tools/adr/corpus.py
@dataclass(frozen=True)
class AdrRecord:
    path: Path
    frontmatter: dict
    body: str
    adr_id: str          # e.g. "ADR-0042"
    adr_status: str      # one of: Proposed | Accepted | Superseded | Deprecated
    adr_supersedes: tuple[str, ...]
    adr_superseded_by: tuple[str, ...]

# tools/adr/graph.py
@dataclass(frozen=True)
class AdrGraph:
    nodes: dict[str, AdrRecord]
    edges_supersedes: dict[str, tuple[str, ...]]      # adr_id → ids it supersedes
    edges_superseded_by: dict[str, tuple[str, ...]]   # adr_id → ids that supersede it
    live_ids: frozenset[str]                          # Accepted, not yet superseded

# tools/adr/extract.py
@dataclass(frozen=True)
class Normative:
    adr_id: str
    keyword: str         # MUST | MUST NOT | SHOULD | …
    sentence: str
    consequence_kind: str | None  # "positive" | "negative" | "neutral" | None for Decision Outcome
    line: int

# tools/adr/compress.py
@dataclass(frozen=True)
class CompressedSection:
    body: str
    contributing_adr_ids: tuple[str, ...]
    token_count: int

# tools/adr/synthesize.py
@dataclass(frozen=True)
class SynthesizeResult:
    section: CompressedSection
    fidelity: float
    written: bool        # False on dry_run
    diagnostics: tuple[Diagnostic, ...]
    exit_code: int       # 0 | 1
```

### §2.3 CLI Entry Shape (Mirrors SPEC §7.5)

```text
agency-adr validate [PATH ...] [--scope=decisions] [--strict] [--format=text|json]
agency-adr synthesize [--token-limit=N] [--fidelity-floor=F]
                      [--fidelity-mode=bcp14-keyword|adr-id-anchor|llm-pass]
                      [--dry-run] [--format=text|json]
```

Exit-code contract (per ADR.A.5.5):
- `0` — no ERROR diagnostics; on `synthesize`, the guarded section was written (or the dry-run report was emitted).
- `1` — at least one ERROR diagnostic; `--strict` promotes WARN to ERROR for purposes of the exit code.
- `2` — usage error (argparse default; mirrors `tools/fm/extract.py`).

---

## §3 Acceptance Test Map

Every Gherkin scenario in the SPEC carries a `# anchor: ADR.A.<aspect>.<stmt>` comment. Each anchor maps to exactly one parametrised pytest function. Tests live under `tests/adr/`.

### §3.1 Test File Inventory

| Phase | Test file | Anchors covered | Fixtures required | Build-phase dependency |
|---|---|---|---|---|
| 1 | `tests/adr/conftest.py` | — | `tmp_decisions_root`, `make_adr(adr_id, status, supersedes=[], body=…)`, `mini_ontology` | — |
| 1 | `tests/adr/test_schema.py` | ADR.A.2.2, ADR.A.5.4 | `make_adr` with malformed frontmatter samples | phase-1 modules |
| 1 | `tests/adr/test_body.py` | ADR.A.2.1, ADR.A.2.3, ADR.A.2.4 | `make_adr` with missing-heading variants | phase-1 |
| 2 | `tests/adr/test_filename_coupling.py` | ADR.A.2.7 | `make_adr` writing files whose name disagrees with frontmatter | phase-2 |
| 2 | `tests/adr/test_ids.py` | ADR.A.5.6 | two `make_adr` calls with the same `adr_id` | phase-2 |
| 2 | `tests/adr/test_graph.py` | ADR.A.4.2, ADR.A.4.3, ADR.A.4.4, ADR.A.4.5, ADR.A.4.6, ADR.A.5.7 | three-node cycle fixture; broken-reciprocity fixture; orphan-reference fixture | phase-2 |
| 3 | `tests/adr/test_extract.py` | ADR.A.3.1 | corpus mixing Accepted + Superseded + Proposed | phase-3 |
| 3 | `tests/adr/test_compress.py` | ADR.A.3.2, ADR.A.3.3 | corpus exceeding `--token-limit=2000` | phase-3 |
| 3 | `tests/adr/test_fidelity.py` | ADR.A.3.4 | corpus with a controlled BCP-14 keyword distribution | phase-3 |
| 4 | `tests/adr/test_synthesize.py` | ADR.A.3.5, ADR.A.3.6, ADR.A.3.7 | `tmp_path / "AGENTS.md"` with and without markers; idempotency double-call | phase-4 |
| 4 | `tests/adr/test_runlog.py` | (supports ADR.A.3.7) | spy on `maintenance/run-log.md` writes | phase-4 |
| 5 | `tests/adr/test_cli.py` | ADR.A.1.1, ADR.A.1.4, ADR.A.5.1, ADR.A.5.2, ADR.A.5.3, ADR.A.5.5, ADR.A.5.8 | `subprocess.run` against `python3 tools/adr/cli.py` | phase-5 |
| 5 | `tests/adr/test_explore.py` | ADR.A.1.5 | corpus with an agent-led exploration trace (linked research workspace stub) | phase-5 |

### §3.2 Test Function Naming Convention

`test_<anchor_with_underscores>(<fixtures>)` — e.g. `test_adr_a_4_5_cycle_detection(tmp_decisions_root, make_adr)`. One function per Scenario; parametrise only when the same `Given/When/Then` shape repeats across multiple anchors.

### §3.3 Minimum Passing Suite Per Build Phase

A build phase is "complete" when its test file row above passes plus every preceding phase still passes. The phase ordering is the same as §2.1 (1 → 5).

---

## §4 GitHub Actions Workflow Specification

Path: `.github/workflows/adr-validate.yml` (the `.github/` folder does not yet exist; the implementation Task creates it).

### §4.1 Trigger

- `on.push.branches: ["main", "claude/**"]` — fire on the canonical branch and on every `claude/<topic>-<date>` working branch.
- `on.push.paths`: `["decisions/**", "AGENTS.md", "tools/adr/**", "tests/adr/**", ".github/workflows/adr-validate.yml"]`.
- `on.pull_request.paths`: same as `on.push.paths`.

### §4.2 Job Steps (Ordered)

1. **Checkout.** `actions/checkout@v4` with `fetch-depth: 0` so the immutability check (ADR.A.4.1) can diff against `HEAD~1`.
2. **Setup Python.** `actions/setup-python@v5` pinned to the same minor version as `install.sh` resolves (currently CPython 3.11 per the install.sh output captured in the Task 027 session log).
3. **Install dependencies.** `./install.sh` — never `pip install -r tools/requirements.txt` directly; the bootstrap script is the source of truth.
4. **Run governance gate.** `tools/check-governance.sh` — this MUST exit 0 on the unmodified working tree of the PR. Failure here is the same gate as the local pre-commit hook.
5. **Run ADR test suite.** `python -m pytest tests/adr/ -q` — only relevant in the implementation Task that succeeds Task 028; before then this step is OPTIONAL.
6. **Run `agency-adr synthesize --dry-run`.** Exits 0 if the synthesis would succeed without modifying `AGENTS.md`. The dry-run output (the proposed guarded-section bytes) is captured to a job artefact.
7. **Diff gate.** Compare the dry-run output against the actual `<!-- BEGIN…END -->` slice of the committed `AGENTS.md`:
   - **Pass condition** — slices are byte-equal. The author re-ran synthesis as part of the commit; nothing else to enforce.
   - **Fail condition** — slices differ. The author committed an ADR change without re-running synthesis; the workflow exits 1 with a comment explaining the remedy ("`python3 tools/adr/cli.py synthesize` and re-commit").
   - **Edge: no markers in `AGENTS.md` yet.** The diff gate is skipped; the implementation Task lands the markers as part of the same PR that introduces this workflow.

### §4.3 Failure Handling

- Any non-zero exit from steps 4–7 fails the workflow.
- The job MUST emit a clear annotation citing the SPEC anchor (`[ADR.A.3.5]`, `[ADR.A.4.5]`, …) so the PR reviewer can locate the rule.
- Step 6 + 7 artefacts (the dry-run output and the diff) MUST be retained for ≥ 7 days for forensic review.

### §4.4 Out of Scope (Future Workflows)

- Static-site rendering of `decisions/` (`log4brains`-style) — `[DEFERRED]` per SPEC OQ.7.
- Auto-comment with the synthesised guarded section as a PR preview — nice-to-have; not on the critical path.

---

## §5 PRE_COMMIT.md Hook Specification

Per SPEC §2.4 / ADR.A.5.8, the only mechanical gate edit is via [`tools/check-governance.sh`](../../tools/check-governance.sh); direct `.githooks/pre-commit` modification is prohibited. The user-facing documentation lives in [`PRE_COMMIT.md`](../../PRE_COMMIT.md).

### §5.1 New Section to Add to `PRE_COMMIT.md`

The implementation Task MUST insert the following section between the existing `## 7. Mechanical Governance Checks` and `## 8. Trust Audit (Spec-J/K/L)`:

> **§ 7.C ADR Governance Validator (Task 028 lineage)**
>
> Composed inside `tools/check-governance.sh` as step `[6/7]` (renumbering the trust audit to `[7/7]`). The validator:
>
> - Triggers when the commit modifies `decisions/**`, `AGENTS.md`, or `tools/adr/**`.
> - Exits 0 if `decisions/` is absent or empty (graceful no-op).
> - Exits 1 on any ERROR diagnostic with the message format `[ADR.A.<aspect>.<stmt>] <relpath>:<line>: <message>`.
>
> Diagnostic codes and their meanings:
>
> | Code | Cause | Author remedy |
> |---|---|---|
> | `ADR.A.2.1` | Required MADR heading missing in body. | Add the heading. |
> | `ADR.A.2.2` | Frontmatter fails JSON-Schema. | Fix the listed key/value. |
> | `ADR.A.2.7` | Filename and frontmatter `adr_id`/`slug` disagree. | Rename file or amend frontmatter. |
> | `ADR.A.3.3` | Synthesis would exceed `--token-limit`. | Deprecate older ADRs or raise limit (justify in PR). |
> | `ADR.A.3.4` | Fidelity score below floor. | Investigate; usually a paraphrasing error in a recent ADR. |
> | `ADR.A.3.5` | `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers missing. | Restore markers in `AGENTS.md`. |
> | `ADR.A.4.1` | Accepted ADR's "Decision Outcome" body modified. | Author a superseding ADR instead. |
> | `ADR.A.4.5` | Cyclic supersession edge. | Break the cycle; the diagnostic lists the cycle nodes. |
> | `ADR.A.4.6` | Missing reciprocal `adr_supersedes` / `adr_superseded_by`. | Add the reciprocal entry. |
> | `ADR.A.5.6` | Duplicate `adr_id`. | Renumber the later-created ADR. |
> | `ADR.A.5.7` | `adr_supersedes` references a missing ADR. | Restore the file or fix the reference. |

### §5.2 `tools/check-governance.sh` Edit

A new numbered step is inserted between the run-log validator and the trust audit. Pseudo-shell:

```bash
echo ""
echo "--- [N/M] ADR governance validator ---"
if ! "$PYTHON" tools/adr/cli.py validate; then
  FAIL=1
fi
```

The implementation Task renumbers downstream steps and adjusts the summary banner.

### §5.3 Hook Granularity

- The hook does NOT run `agency-adr synthesize` automatically; that mutates `AGENTS.md` and would surprise the author. Synthesis is the author's explicit step before commit (and is gated by the GitHub Actions diff in §4.2 step 7).
- The hook DOES run `agency-adr validate`, which is read-only.

---

## §6 Open Decisions

Items inherited from SPEC §8 plus those surfaced during this plan. Each row identifies the blocked module(s) so the implementation Task can sequence around them.

| ID | Decision | Options | Blocks | Recommended owner |
|---|---|---|---|---|
| OD.1 | Migration cardinality (SPEC OQ.1) — Strategy A (14 ADRs) vs Strategy B (≈ 5 ADRs). | A (granular) / B (clustered) / hybrid | None of the modules above are blocked; the *first ADR PR* is blocked until this is decided. | Maintainer, after Task 029 audit. |
| OD.2 | Fidelity-metric algorithm (SPEC OQ.2). | `bcp14-keyword` / `adr-id-anchor` / `llm-pass` | `tools/adr/fidelity.py`. v0 ships `bcp14-keyword` (deterministic, no LLM dep). `llm-pass` requires Anthropic SDK + cost/latency analysis — defer. | Task 029 audit + Task 028 prototype. |
| OD.3 | Token-limit empirical floor (SPEC OQ.3). | Keep 2000 / raise to 3000 / parameterise per-repo | `tools/adr/compress.py` default; `agency-adr synthesize --token-limit` accepts override regardless. | Maintainer, after first synthesis run reports actual count. |
| OD.4 | Waiver scope for `decisions/` (SPEC OQ.4). | Allow waivers / forbid waivers | `tools/adr/cli.py validate` waiver-loading code path. Spec leans NO. | Maintainer. |
| OD.5 | `adr_status: Proposed` in synthesis (SPEC OQ.5). | Include / exclude | `tools/adr/extract.py`. Default exclude. | Implementation Task; revisit if first authors push back. |
| OD.6 | Marker placement in `AGENTS.md` (SPEC OQ.6). | Between Frontmatter Ontology and Narrative Ontology / between Closing Run Procedure and Spec Language Reference / new "## Synthesised ADR Constraints" section | The implementation Task itself (PR that introduces markers). | Implementation Task; reviewed by maintainer. |
| OD.7 | Tokeniser choice (new — surfaced by §3.1 / §6.OD.3). | `len(text.split())` heuristic / `tiktoken` (OpenAI) / Anthropic `cl100k`-equivalent | `tools/adr/compress.py count_tokens`. Initial heuristic is fine for v0; precision matters only at the hard limit. | Implementation Task. |
| OD.8 | Symlink `tools/adr/agency-adr → cli.py` for ergonomics (new). | Yes / no | Cosmetic; not on the critical path. | Implementation Task; default no. |
| OD.9 | `--strict` semantics for warn-only diagnostics (new). | Match `tools/fm/validate.py --strict` exactly / introduce ADR-only WARN class | `tools/adr/cli.py`. Recommendation: match `tools/fm/validate.py`. | Implementation Task. |
| OD.10 | First-batch ADR authoring agent (new). | Maintainer-authored / agent-authored under prompt / hybrid (agent drafts, maintainer reviews) | The corpus seed; not a code dependency. | Maintainer. |

OD.1, OD.2, OD.4, and OD.10 are routed to [Task 029](../029-adr-assumption-audit/task.md) where the multi-subagent assumption audit is the natural place to surface the recommendation.

---

## §7 Complexity Estimate

Scale: **S** = under 1 day, **M** = 1–3 days, **L** > 3 days. Estimates assume the implementing agent has full context of this plan and the ADR spec.

### §7.1 Module Estimates

| Module | Estimate | Notes |
|---|---|---|
| `__init__.py` | S | Trivial. |
| `schema.py` | S | `jsonschema` is a thin wrapper over the schema in SPEC §7.4. |
| `body.py` | S | Reuses `find_section_body` and `detect_shape`. |
| `corpus.py` | M | Discovery + parse + typed records; the lifting-grade parsing already lives in `tools/fm/_core.py`. |
| `graph.py` | M | Kahn's algorithm + reciprocity + orphan checks; ≤ 200 lines. |
| `ids.py` | S | Two list-comprehension checks. |
| `extract.py` | M | BCP-14 sentence extraction is regex-tight; "Decision Outcome" body shape varies between authors. |
| `compress.py` | M | Deduplication strategy + footer-citation generator; the *correctness* is testable by determinism. |
| `fidelity.py` | M | `bcp14-keyword` mode is small; `adr-id-anchor` adds graph traversal; `llm-pass` is deferred (OD.2). |
| `synthesize.py` | M | Orchestrator with the no-marker safety check + idempotency contract. |
| `runlog.py` | S | Append a structured record; reuse the format from `maintenance/run-log.md`. |
| `cli.py` | M | argparse, sub-commands, `--format=json`, exit-code wiring. |
| `readme.md` | S | Folder index. |

### §7.2 Test File Estimates

| Test file | Estimate | Notes |
|---|---|---|
| `tests/adr/conftest.py` | S | Fixtures only. |
| `tests/adr/test_schema.py` | S | Table-driven against malformed-frontmatter samples. |
| `tests/adr/test_body.py` | S | Heading-presence assertions. |
| `tests/adr/test_filename_coupling.py` | S | One scenario, parametrised. |
| `tests/adr/test_ids.py` | S | One scenario, parametrised. |
| `tests/adr/test_graph.py` | M | Cycle + reciprocity + orphan; deterministic graph fixtures. |
| `tests/adr/test_extract.py` | M | Multiple status-mix corpora. |
| `tests/adr/test_compress.py` | M | Exceeds-limit + happy-path + idempotency. |
| `tests/adr/test_fidelity.py` | M | Per-mode parametrisation. |
| `tests/adr/test_synthesize.py` | M | Marker handling + idempotency double-call. |
| `tests/adr/test_runlog.py` | S | Spy on append. |
| `tests/adr/test_cli.py` | M | Sub-process invocation; exit-code matrix. |
| `tests/adr/test_explore.py` | S | Audit-trail presence. |

### §7.3 Glue and CI Estimates

| Item | Estimate | Notes |
|---|---|---|
| `header-ontology.json` registration of `types.adr` | S | Add the §7.4 schema body. |
| `tools/check-governance.sh` insertion + step renumbering | S | One block; downstream renumber. |
| `PRE_COMMIT.md §7.C` documentation block | S | The exact text in §5.1 above. |
| `.github/workflows/adr-validate.yml` | M | First workflow in this repo; setup boilerplate dominates. |
| First-batch ADR authoring (one demo ADR-0001 to seed the corpus) | M | Decoupled from the implementation; recommended in the same PR for end-to-end smoke-test. |
| Maintenance docs touch (`MAINTENANCE.md` mentioning the new validator) | S | One-paragraph addition to §1. |

### §7.4 Aggregate

S items: 16 (≈ 8 days at one-per-half-day). M items: 14 (≈ 28 days at two-per-day average). L items: 0.

**Headline estimate:** ≈ **3–5 working weeks** for a focused implementing agent, including tests and CI but excluding the first-batch ADR authoring decision (OD.10). The critical path is `corpus → graph → extract → compress → synthesize → cli`, with `fidelity.py` and `tests/adr/test_*.py` parallelisable from phase 3 onward.

### §7.5 Suggested Sequencing

1. **Week 1.** Phase 1+2 modules (`schema`, `body`, `corpus`, `ids`, `graph`) and their tests. Land a PR that ships `agency-adr validate` end-to-end against an empty `decisions/` corpus.
2. **Week 2.** Phase 3 modules (`extract`, `compress`, `fidelity`) and their tests. `bcp14-keyword` fidelity mode only.
3. **Week 3.** Phase 4 modules (`synthesize`, `runlog`) and tests. Land the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers in `AGENTS.md` (OD.6 decision applied) and the first synthesised guarded section.
4. **Week 4.** Phase 5 (`cli`); register in `tools/check-governance.sh`; add `PRE_COMMIT.md §7.C`; ship `.github/workflows/adr-validate.yml`. Author ADR-0001 (per OD.10) as the smoke-test record.
5. **Week 5.** Buffer for OD-resolution feedback (Task 029 recommendations on OD.1, OD.2, OD.4) and any spec-clarifying follow-up ADRs.

---

## §A Cross-References

- ADR governance spec: [`../../research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md).
- Predecessor task: [`../027-adr-spec-research-synthesis/task.md`](../027-adr-spec-research-synthesis/task.md) (`task_status: done`).
- Sibling task: [`../029-adr-assumption-audit/task.md`](../029-adr-assumption-audit/task.md) (`task_status: done`; produced [`../../research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md)).
- Reusable tooling: [`../../tools/fm/_core.py`](../../tools/fm/_core.py), [`../../tools/check-governance.sh`](../../tools/check-governance.sh).

## §B Task 029 Audit Cross-Reference (PD ↔ OD)

Added 2026-05-05 by Task 029 closure (per its prompt Step 7.3). This appendix is read-only metadata: it neither modifies any §1–§7 row nor changes the build sequencing. It cross-links the PDs from [`../../research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) §3 to the ODs in §6 above.

| PD (REPORT §3) | Maps to OD (§6) | Audit recommendation | Effect on build |
|---|---|---|---|
| PD-001 — storage path | implicit (resolved at SPEC drafting) | `decisions/` (Option A) confirmed | none — already in plan §1 |
| PD-002 — fidelity algorithm | OD.2 | Ship A+B together as v0; defer C (`llm-pass`) | upgrades plan §2.1 `tools/adr/fidelity.py` from "ships A only" to "ships A+B"; +1 day on §7.1 estimate |
| PD-003 — AGENTS.md ownership | OD.6 (placement) | Option B (guarded section) confirmed; placement still deferred | none on contract; sub-mitigations from REPORT.md §4 Action 3 extend OD.6 |
| PD-004 — DAG storage | OD-implicit (plan §2.1 resolved) | Option A (frontmatter source-of-truth) confirmed | none — already in plan §2.1 |
| PD-005 — bootstrap cardinality | OD.1 | **Hybrid Option C** — 5 P1 individual + 1–2 P2 clusters + P3 deferred | unblocks Task 030 candidate (first-batch ADR authoring); does NOT block any §2.1 module |
| PD-006 — ADR review loop (NOVEL) | none — extends PRE_COMMIT.md §7.D | Append 5-item review checklist | extends plan §5.1 with a §7.D sub-section; +S effort |
| PD-007 — stale-Proposed lifecycle (NOVEL) | none — defer to Task 031 | Defer; default forever-open | post-v0; not on critical path |

REPORT.md §4 enumerates 5 Recommended Actions tied to the table above. The implementing-agent Task that succeeds Task 028 SHOULD treat REPORT.md §4 as a binding refinement of plan §6.
