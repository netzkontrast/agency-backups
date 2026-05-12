---
type: adr
status: active
slug: 0010-external-skill-corpora-import
summary: "External skill corpora (SuperClaude, Superpowers) import under vendor-prefixed namespaces with skill_source pin. Closes CLAUDE.md §13 dangling references."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0010
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - skills
  - import-policy
  - frontmatter
  - namespace
  - external-corpora
---

# ADR-0010 — External Skill Corpora Import Policy

## Context and Problem Statement

[`AGENTS.md` Closing Run Procedure](../AGENTS.md#closing-run-procedure) ("Claude Code" implementation note) and [`CLAUDE.md §13`](../CLAUDE.md) cite a set of `/sc:*` slash-commands as canonical Agency primitives — most prominently `/sc:createPR` as the session-closing step 4 of the four-step Closing Run checklist (CR.1–CR.7). The Claude Code implementation note resolves the citation to a remote URL at `https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md`; no `skills/sc-createPR/SKILL.md` exists in this repository. The repository currently ships 22 skills under [`/skills/`](../skills/) (narrative + tooling + meta), none of which are the `/sc:*` set. The references dangle.

Two upstream corpora hold the missing skills under their own conventions:

- **SuperClaude_Framework v4.3.0** — 31 commands, 20 agents, 7 modes, 9 MCP integrations. Distributed via `pipx install superclaude` → `~/.claude/commands/sc/{slug}.md`. Frontmatter: `name`, `description`, `category`, optional `complexity`/`mcp-servers`/`personas`.
- **Superpowers v4.0.3** — 14 skills, 3 commands, 1 code-reviewer agent, SessionStart hook. Distributed via Claude Code's plugin marketplace. Frontmatter: `name`, `description` only.

Both corpora ship `.md` bodies that match Agency's `SKILL.md` shape sufficiently to port — but neither matches Agency's L1 Vault Core ([`SKILLS.md §3.2`](../SKILLS.md)) or L2 `skill_*` namespace ([`SKILLS.md §3.3`](../SKILLS.md)). A port requires policy for namespace, attribution, body adaptation (some upstream skills assume MCP servers Agency does not ship), and sync cadence.

A single umbrella ADR (vs one ADR per imported skill) is the right granularity: the architectural decision being made is *how external corpora land*, not *should this specific skill exist*. Forty separate ADRs would drown the ledger; the policy bound here applies to every future external import without re-litigation.

## Decision Drivers

- **DD.1 Close the dangling-reference gap.** `CLAUDE.md §13` enumerates `sc:implement`, `sc:test`, `sc:createPR`, `sc:improve`, `sc:research` as if they exist; `AGENTS.md` Closing Run Procedure routes step 4 through `/sc:createPR`. Whatever policy lands MUST resolve these references against real local files.
- **DD.2 Provenance preservation.** Imported skill bodies trace to specific upstream releases. Stripping the upstream identity (e.g. flattening to bare slugs) loses the audit trail and risks accidental collision with future Agency-native skills.
- **DD.3 Governance ordering.** Introducing a new top-level pattern (vendor-prefixed folder namespace + new L2 frontmatter key) is a **T3 structural** change per [`MAINTENANCE.md §1`](../MAINTENANCE.md#1-repair-permission-tiers). It MUST land via ADR before any imported file is committed.
- **DD.4 T2 ladder discipline.** [`SKILLS.md §7.3`](../SKILLS.md) caps SKILL.md body at 5 KB (T2). Several upstream bodies exceed this (e.g. `superpowers:writing-skills` at 22.5 KB, `sc:implement` ~9 KB). The policy MUST specify how overflow is handled.
- **DD.5 MCP-free runtime.** Several upstream skills assume MCP servers Agency does not ship (Tavily, Magic, Morphllm, Serena, Chrome DevTools). Verbatim mirroring would create skills that fail silently when invoked. Bodies MUST be adapted for Agency's built-in Claude Code primitives (WebSearch, WebFetch, Read/Write/Edit, Bash).
- **DD.6 Bootstrap contract integrity.** [`AGENTS.md SS.1–SS.3`](../AGENTS.md#session-setup) bind the mandatory session-start sequence. Upstream SessionStart hooks (SuperClaude pm-agent restore, Superpowers `using-superpowers` injection) would conflict; the policy MUST exclude them.
- **DD.7 Sync cadence.** Both upstreams iterate; this port must specify whether re-syncs are automated, scheduled, or operator-triggered. Scope discipline: an automated puller would itself be a substantial Task and is not required for the initial port.

## Considered Options

### Option A — Bare slugs (no vendor prefix)

Land imported skills at `skills/createPR/`, `skills/implement/`, etc. No prefix; no `skill_source` frontmatter.

- **Positives.** Cleanest filesystem layout. Tab-completion friendly.
- **Negatives.** Loses upstream provenance. Risks future collisions when Agency authors a native `skills/research/` that conflicts with the imported one. `CLAUDE.md §13` cites names with the `sc:` prefix; the local skill body would need an `aliases` field to match — adding indirection. Cost: medium ongoing complexity.

### Option B — One ADR per imported skill

Author 40+ ADRs (one per skill in the first batch plus future phases), each ratifying that specific import.

- **Positives.** Maximally explicit; each import is independently auditable.
- **Negatives.** Drowns the ledger (40+ ADRs in a single batch). Re-litigates the same architectural decision per file. The policy *is* the architectural decision; the per-skill imports are mechanical executions of that policy. Cost: high one-time + recurring.

### Option C — Auto-pull on every commit

A pre-commit hook re-fetches upstream `main` and updates `skills/sc-*/` and `skills/superpowers-*/` automatically.

- **Positives.** Imports stay current with zero operator effort.
- **Negatives.** Upstream drift becomes silent; a force-push to upstream `main` would silently rewrite local SKILL.md bodies; the audit trail (which upstream version is in force?) becomes opaque. Conflicts with [`SKILLS.md §7.4`](../SKILLS.md) `SKILLS_SKILL_PIN` discipline. Out of scope for this ADR — properly handled by a future ADR that includes drift detection and operator notification. Cost: high (substantial future Task).

### Option D — Snapshot import with vendor prefix + `skill_source` pin (chosen)

Imported skills land at `skills/<vendor>-<bare-slug>/` where `<vendor>` ∈ `{sc, superpowers}`. Every `SKILL.md` carries a new L2 frontmatter key `skill_source: "<vendor>@v<semver>"`. SHA-pinned citation to the upstream file appears in `## References`. Re-syncs are one-shot Tasks, not automated.

- **Positives.** Provenance preserved (slug + frontmatter both encode it). `/sc:*` user-facing names match what `CLAUDE.md §13` already cites. Future Agency-native skills cannot collide with imports (the bare-slug namespace is reserved for natives). Sync cadence is deliberate — re-syncs require a Task, which forces operator review.
- **Negatives.** Folder names are longer (`skills/sc-implement/` vs `skills/implement/`). One new L2 frontmatter key (`skill_source`) to validate. Tag-only pin carries minor force-push risk on the upstream side; mitigated by upstreams being on PyPI / Claude Code marketplace where releases are immutable. Cost: low.

## Decision Outcome

**Option D (snapshot import with vendor prefix + `skill_source` pin) is chosen, recorded as `adr_status: Proposed`.** The nine normative clauses below bind every external skill import from this point forward.

### Normative clauses (RFC 2119)

- **D.1 Namespace prefixing.** External skill folders MUST live at `skills/<vendor>-<bare-slug>/` where `<vendor>` ∈ `{sc, superpowers}`. Bare slugs (no vendor prefix) MUST be reserved for Agency-native skills.
- **D.2 Source pin.** Every imported `SKILL.md` MUST carry the L2 frontmatter key `skill_source` with value matching `^(superclaude|superpowers)@v\d+\.\d+\.\d+$` (e.g. `superclaude@v4.3.0`). The key MUST NOT appear on Agency-native skills.
- **D.3 Citation.** Every imported `SKILL.md` `## References` section MUST include a SHA-pinned link to the upstream source file in the form `path/to/file.ext:Lstart-Lend@<sha>` per [`AGENTS.md` Citation Reproducibility Protocol](../AGENTS.md).
- **D.4 Agent-as-skill.** Upstream agent files (SuperClaude `src/superclaude/agents/*.md`) MUST be ported as skills — `skill_kind: domain` for single-persona agents, `skill_kind: orchestrator` when the agent coordinates other agents. Agents MUST NOT be stored outside `/skills/`.
- **D.5 Modes as references.** Upstream `MODE_*.md` files MUST be bundled inside the relevant skill's `references/` directory. Modes MUST NOT be ported as standalone skills.
- **D.6 T2 size cap.** Every imported `SKILL.md` body MUST be ≤ 5 KB per [`SKILLS.md §7.3`](../SKILLS.md). Excess prose MUST move to the skill's `references/` directory and MUST be cited from the body's `## References` section.
- **D.7 No SessionStart injection.** Upstream SessionStart hooks (SuperClaude pm-agent restore, Superpowers `using-superpowers` injection) MUST NOT be ported. The Agency bootstrap contract in [`AGENTS.md SS.1–SS.3`](../AGENTS.md#session-setup) remains canonical.
- **D.8 Body adaptation for MCP-free runtimes.** When an upstream body requires an MCP server Agency does not ship (Tavily, Morphllm, Magic, Serena, Chrome DevTools), the SKILL.md body MUST be rewritten so a built-in Claude Code primitive (WebSearch, WebFetch, Read/Write/Edit, Bash) is the primary path. The upstream MCP MUST appear only in `## Compatibility` as OPTIONAL. The verbatim upstream body MUST be archived at `skills/<vendor>-<slug>/references/upstream-<vendor>-<slug>.md`.
- **D.9 Sync cadence.** The first port is a one-shot snapshot. Subsequent re-syncs from upstream MUST file a new Task. Automated upstream-pull is OUT OF SCOPE for this ADR and MUST be addressed by a future ADR if drift evidence accumulates.

### Validator impact (T2 additive)

The `skill_source` key (D.2) requires a small extension to [`tools/fm/validate.py`](../tools/fm/validate.py): two new diagnostic codes (`F.B.7` for `skill_source` on a bare-slug skill, `F.B.8` for a value that does not match the regex). The extension is a **T2 additive** per [`MAINTENANCE.md §1`](../MAINTENANCE.md#1-repair-permission-tiers) — it adds a check; it does not change existing behaviour. Existing skills without `skill_source` continue to validate.

### Skills manifest impact

[`SKILLS.md B.3`](../SKILLS.md) requires `.skills-manifest.json` to list every skill slug and its `skill_kind`. Adding the `skill_source` value to the manifest is RECOMMENDED but not required by this ADR; the manifest schema is not changed.

## Consequences

### Positive

- The five dangling `/sc:*` references in [`CLAUDE.md §13`](../CLAUDE.md) and the [`AGENTS.md` Closing Run Procedure](../AGENTS.md#closing-run-procedure) resolve to real local skill bodies once the follow-up corpus Task executes.
- Provenance is encoded in two complementary places (folder slug + frontmatter key), making the audit trail robust to either one drifting.
- The bare-slug namespace stays reserved for Agency-native skills; future name collisions are impossible by construction.
- The sync-cadence rule (D.9) keeps Agency in control of when upstream churn enters the repo. Operator review is forced on every re-sync.

### Negative

- One new L2 frontmatter key (`skill_source`) to validate, teach readers, and remember by skill authors. Mitigated by extending [`templates/skill.md`](../templates/skill.md) with a commented-example line in a follow-up T2 commit.
- Imported folder names are longer (`skills/sc-implement/` not `skills/implement/`). Mitigated by Claude Code's `Skill` tool surfacing the `/sc:*` user-facing slug regardless of folder layout.
- Tag-only `skill_source` pin carries minor force-push risk on the upstream side. Mitigated by: (a) upstream maintainers do not force-push release tags, (b) PyPI v4.3.0 / Claude Code marketplace v4.0.3 are immutable. If drift is observed, an optional follow-up `tools/check-skill-source-pinning.py` advisory linter can land as a T2 addition.
- `skills/sc-research/SKILL.md` body must diverge from upstream per D.8 (WebSearch/WebFetch primary, not Tavily). Future upstream changes to `sc:research` will not auto-propagate — they require a re-sync Task that re-applies the adaptation. The verbatim upstream body archived at `references/upstream-sc-research.md` keeps the diff auditable.

### Neutral

- [`skills/skills-skill-bootstrap/sync.sh`](../skills/skills-skill-bootstrap/sync.sh) is not modified: it already iterates every `skills/*/` folder and is namespace-agnostic. The new vendor-prefixed folders are picked up automatically.
- [`templates/skill.md`](../templates/skill.md) MAY be extended in a follow-up T2 commit to show a `skill_source` commented-example line; not blocking on the first port.
- This ADR sets precedent for future external corpus imports (e.g. `anthropics/skills` upstream beyond the existing `skill-creator` mirror). The policy is corpus-agnostic; only the `skill_source` regex needs extension if a third vendor lands.

### Falsifier triggers — re-open this ADR when any of the following hold

- **F1.** A third external corpus is proposed for import (e.g. a community plugin). The two-vendor regex in D.2 needs extension; consider whether the policy generalises or whether a successor ADR is warranted.
- **F2.** Drift is observed: an upstream maintainer force-pushes a release tag and the local SKILL.md content silently lags behind the user-facing tag value. The tag-only pin is then insufficient and the policy SHOULD switch to tag + SHA composite pinning.
- **F3.** The bare-slug ↔ vendor-prefix boundary is breached by an Agency-native skill author who unknowingly creates `skills/research/` when `skills/sc-research/` exists. The current policy assumes filename collisions are caught at PR review; if mechanical detection is needed, a `tools/check-skill-namespace.py` linter ratifies it via a successor ADR.

When any falsifier triggers, a successor ADR MUST be authored that re-evaluates Options A–D against the then-current evidence and supersedes this one via `adr_supersedes: [ADR-0010]`.

## Cross-references

- [`AGENTS.md` Closing Run Procedure](../AGENTS.md#closing-run-procedure) — the primary dangling-reference site (CR.7 implementation notes for Claude Code).
- [`CLAUDE.md §13`](../CLAUDE.md) — enumerates the five `/sc:*` skills this policy resolves.
- [`SKILLS.md §3.3`](../SKILLS.md) — the `skill_*` L2 namespace this ADR extends with `skill_source`.
- [`SKILLS.md §7.2`](../SKILLS.md) — trust-boundary invariants B.6–B.9 the imported skills inherit.
- [`SKILLS.md §7.3`](../SKILLS.md) — T1/T2/T3 ladder; D.6 binds T2 ≤ 5 KB.
- [ADR-0003 — Frontmatter Source of Truth](./0003-frontmatter-source-of-truth.md) — `skill_source` is added under that contract.
- [ADR-0006 — Agency-System Prototype Exemption](./0006-agency-system-prototype-exemption.md) — precedent for "imported/external content stays in this repo" pattern.
- [ADR-0007 — `skill_bundles_tools` Frontmatter](./0007-skill-bundles-tools-frontmatter.md) — precedent for adding an L2 additive key via ADR.
- [`tools/fm/validate.py`](../tools/fm/validate.py) — receives the F.B.7 / F.B.8 extension in the follow-up corpus Task.
- [`research/skills-skill-architecture/output/SPEC.md`](../research/skills-skill-architecture/output/SPEC.md) §6 R5 — trust-boundary contract that imported skills inherit unchanged.
- Upstream: [SuperClaude_Framework v4.3.0](https://github.com/netzkontrast/SuperClaude_Framework) (`pyproject.toml` v4.3.0).
- Upstream: [Superpowers v4.0.3](https://github.com/netzkontrast/superpowers) (`.claude-plugin/plugin.json` v4.0.3).

## Acceptance Criteria

```gherkin
Feature: External skill corpora import policy

  # anchor: ADR.10.1
  Scenario: Imported skill carries vendor prefix and source pin
    Given an external SKILL.md is being ported into /skills/
    When the porting agent writes the file
    Then the folder path MUST match skills/(sc|superpowers)-<bare-slug>/
    And the SKILL.md frontmatter MUST contain skill_source matching ^(superclaude|superpowers)@v\d+\.\d+\.\d+$
    And the SKILL.md ## References section MUST include a SHA-pinned upstream citation

  # anchor: ADR.10.2
  Scenario: Validator accepts skill_source on imports, rejects on natives
    Given tools/fm/validate.py runs over /skills/
    When it encounters a SKILL.md with skill_source set
    Then it MUST accept the key if the folder path matches the vendor-prefix rule (D.1)
    And it MUST reject the key with diagnostic F.B.7 if the folder is a bare slug (Agency native)
    And it MUST reject a malformed value with diagnostic F.B.8

  # anchor: ADR.10.3
  Scenario: T2 body cap enforced on every import
    Given any imported SKILL.md whose upstream body exceeds 5 KB
    When tools/fm/validate.py --check-body runs against it
    Then the body MUST be ≤ 5 KB
    And the overflow MUST live under skills/<vendor>-<slug>/references/
    And references/ MUST be cited from the body's ## References section
```
