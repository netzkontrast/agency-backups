---
type: note
status: active
slug: triage-note-validator-touchpoints
summary: "ST-2/ST-3 validator-touchpoint cheat sheet: which tools/fm/validate.py diagnostics each port/adapt row will encounter, and the ADR-0012 (when Accepted) renumber implications."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Validator touchpoints for ST-2 / ST-3

When ST-2 and ST-3 port the keep-list, every new `skills/<vendor>-<slug>/SKILL.md` will trigger a fixed set of `tools/fm/validate.py` diagnostics. This note inventories the touchpoints so ST-2/3 authors know exactly which checks gate each port and what an expected-failure-then-fix loop looks like.

## Diagnostics each ported SKILL.md MUST pass

| Diagnostic | Layer | Checks | Failure mode |
|---|---|---|---|
| `F.A.1` | L1 | `type:` ∈ {task, prompt, research, spec, readme, note, index, **skill**} | "type missing" or "type unknown" |
| `F.A.2` | L1 | `slug:` is kebab-case and matches folder name | "slug mismatch with folder" |
| `F.A.5` | L1 | `summary:` present, ≤ 280 chars | "summary missing/long" |
| `F.A.6` | L1 | `created:` + `updated:` are ISO-8601 | "date malformed" |
| `F.B.8` | L2 (skill) | `skill_source:` = `<vendor>@v<semver>` | "skill_source malformed" |
| `F.B.9` | L2 (skill) | vendor ∈ {`superclaude_framework`, `superpowers`} | "vendor prefix unknown" |
| `F.B.10` | body | body ≤ 5 KB (ADR-0011 D.6) | "body cap exceeded" |

> Diagnostic codes `F.B.8` / `F.B.9` were established in Phase 1 ST-1 (Task 091, PR #115). The Phase 1 friction-log noted that the upstream `F.B.7` numbering was renumbered mid-implementation; **ADR-0012** (open per [Task 091 friction-log FL1.1](../../091-port-external-skill-corpora/friction-log.md)) reconciles the renumber. Until ADR-0012 is Accepted, ST-2/3 authors SHOULD pin to the post-renumber codes (`F.B.8` / `F.B.9`) and add a `## Adaptations from upstream` note if the validator surfaces a transitional code.

## Expected failure-then-fix loop per port

1. Author SKILL.md verbatim from snapshot.
2. Run `python3 tools/fm/validate.py skills/<slug>/`.
3. **Likely fail:** missing Agency L1 frontmatter (`type: skill`, etc.) → add per the [pure-ports cluster](./sc-pure-ports-cluster.md) recipe.
4. **Likely fail (adapt rows only):** `F.B.10` body cap → extract overflow to `references/` per the relevant triage note (e.g. [sc-spec-panel](./sc-spec-panel.md), [superpowers-writing-skills](./superpowers-writing-skills.md)).
5. **Likely fail (rows with MCP):** `F.B.8` will not flag MCP refs (it only checks vendor pin) — MCP-strip is a content concern, validated by reviewer not validator. The `## Adaptations from upstream` body section is the audit trail.

## ADR-0012 dependency

Per Task 092 task.md §Context: "This Epic SHOULD wait for ADR-0012 to be Accepted before mass-porting." Until then:

- ST-2 / ST-3 MAY port individual rows but SHOULD NOT batch > 5 rows per PR (to limit churn if ADR-0012 changes diagnostic codes).
- The triage-matrix MUST be re-grepped against ADR-0012's final numbering once Accepted; if codes change, the matrix's "ADR-0011 clauses" column is unaffected but the validator-output examples in each `## Adaptations from upstream` section MAY need a one-shot batch update.

## Governance gate

Every PR closing a port-row MUST cite, in the PR body:

- The matrix row number(s) ported.
- The exact `tools/fm/validate.py` exit code after the port.
- Any `F.B.10` body-cap remediation (and the `references/` files produced).
- The friction-log delta (FL0 if clean; FL1+ if any rework was needed).
