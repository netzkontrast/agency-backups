---
type: index
status: active
slug: tools-adr
summary: "agency-adr — repo-native Architectural Decision Record governance CLI: validates the /decisions/ corpus and synthesises Accepted ADRs into the guarded section of AGENTS.md."
created: 2026-05-06
updated: 2026-05-06
---

# `agency-adr`

**What is this folder?** The CLI tooling that enforces the repo-native ADR governance specification at [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md). It owns two responsibilities:

1. **Validate** — walk `/decisions/`, parse every ADR's frontmatter and body, and emit diagnostics for schema, MADR-shape, supersession-DAG, duplicate-id, and orphan-reference violations.
2. **Synthesize** — extract normatives from every Accepted ADR, MDL-compress them under a token budget, score fidelity, and rewrite the guarded section of [`../../AGENTS.md`](../../AGENTS.md) atomically.

**Why is it here?** ADRs only retain governance value if every commit that touches `/decisions/` is mechanically checked, and if the synthesised summary in `AGENTS.md` is provably traceable to its source. This package satisfies anchors `ADR.A.5.1`–`ADR.A.5.9` of the spec.

## Usage

```bash
# Read-only check — runs in pre-commit via tools/check-governance.sh.
python3 tools/adr/cli.py validate [--strict] [--format=text|json]

# Rewrite AGENTS.md guarded section. Requires the BEGIN/END markers.
python3 tools/adr/cli.py synthesize \
    [--token-limit=2000] [--fidelity-floor=0.95] \
    [--fidelity-mode=bcp14-keyword|adr-id-anchor|llm-pass] \
    [--dry-run] [--format=text|json]
```

Exit codes mirror [`../fm/validate.py`](../fm/validate.py): `0` clean, `1` on any ERROR diagnostic (or any WARN under `--strict`), `2` on argparse usage error.

## Module Map

| Module | Responsibility | Spec anchors |
|---|---|---|
| [`schema.py`](./schema.py) | JSON-Schema validation of ADR frontmatter. | ADR.A.2.2, ADR.A.5.4 |
| [`body.py`](./body.py) | MADR section presence + non-empty Decision Outcome / Consequences. | ADR.A.2.1, ADR.A.2.3, ADR.A.2.4 |
| [`corpus.py`](./corpus.py) | Walk `/decisions/`; produce typed `AdrRecord` objects. | ADR.A.5.9 |
| [`graph.py`](./graph.py) | Supersession DAG + Kahn cycle detection + reciprocity + orphan checks. | ADR.A.4.4–4.6, ADR.A.5.7 |
| [`ids.py`](./ids.py) | Duplicate `adr_id` detection; filename↔frontmatter coupling. | ADR.A.5.6, ADR.A.2.7 |
| [`extract.py`](./extract.py) | Pull BCP-14-bearing sentences from Accepted ADRs. | ADR.A.3.1 |
| [`compress.py`](./compress.py) | MDL compression: dedupe, group by keyword, footer cite. | ADR.A.3.2, ADR.A.3.3 |
| [`fidelity.py`](./fidelity.py) | Score modes: `bcp14-keyword`, `adr-id-anchor`; `llm-pass` deferred. | ADR.A.3.4 |
| [`synthesize.py`](./synthesize.py) | Orchestrator: corpus → graph → extract → compress → fidelity → write. | ADR.A.3.5–3.7 |
| [`runlog.py`](./runlog.py) | Append a record to `maintenance/run-log.md` per run. | ADR.A.3.7 |
| [`cli.py`](./cli.py) | argparse entry point; sub-commands `validate` / `synthesize`. | ADR.A.5.1–5.5, 5.8 |

## Reuse from `tools/fm/`

Per anchor ADR.A.5.9 the package uses [`../fm/_core.py`](../fm/_core.py) for frontmatter parsing, heading walking, section-shape detection, file locking, ontology loading, and the `Diagnostic` shape. No YAML loader is reimplemented inside `tools/adr/`.

## Tests

[`../../tests/adr/`](../../tests/adr/) carries one pytest module per build phase, each scenario carrying a `# anchor: ADR.A.<aspect>.<stmt>` comment that matches the Gherkin scenario in the spec.
