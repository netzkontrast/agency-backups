---
type: note
status: active
slug: triage-note-superpowers-discipline-cluster
summary: "Combined triage note for the Superpowers 'discipline gates' cluster: systematic-debugging, test-driven-development, verification-before-completion, receiving-code-review. All port but require references/ extraction (D.6) and Agency-native tool re-binding."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Superpowers "discipline gates" cluster

Four Superpowers skills enforce **engineering discipline gates** that prevent shortcut-taking under cognitive pressure. None binds to MCP, but three exceed the D.6 5 KB body cap and require structured `references/` extraction.

## Files

| Snapshot path | KB | Landing slug | Phase split |
|---|---|---|---|
| `superpowers/skills/systematic-debugging/SKILL.md` | 9.9 | `superpowers-systematic-debugging` | 4 phases (gather / hypothesise / test / fix) → `references/phase-{1..4}.md`. |
| `superpowers/skills/test-driven-development/SKILL.md` | 9.9 | `superpowers-tdd` | RED + GREEN + REFACTOR → `references/{red,green,refactor}.md`. |
| `superpowers/skills/verification-before-completion/SKILL.md` | 3.9 | `superpowers-verification-before-completion` | Fits ≤ 5 KB; no references/. |
| `superpowers/skills/receiving-code-review/SKILL.md` | 6.3 | `superpowers-receiving-code-review` | Heuristics + worked-examples → `references/heuristics.md`. |

## Adaptation plan (ST-3)

1. **Body extraction.** Each SKILL.md keeps the methodology overview + invocation triggers; phase / phase / heuristic content moves to `references/`. Target body ≤ 4 KB per skill.
2. **Tool re-binding.** Upstream cites generic Claude tools (Read, Bash, Edit) — already Agency-native, no rewrite needed.
3. **Cross-reference Agency's `sc-test` + `sc-troubleshoot`.** The Superpowers TDD skill and Agency's `sc-test` skill complement each other (TDD discipline vs. test execution); document the relationship in each SKILL.md.
4. **`skill_source: "superpowers@v4.0.3"`** in every ported SKILL.md frontmatter (per Phase 1 ST-1 convention; F.B.8 / F.B.9 validator).

## Audit-graph linkage

- All four skills carry `skill_source: "superpowers@v4.0.3"`.
- `skill_references_skills` cross-edges:
  - `superpowers-tdd` → `[sc-test]`
  - `superpowers-systematic-debugging` → `[sc-troubleshoot, sc-root-cause-analyst]`
  - `superpowers-verification-before-completion` → `[sc-self-review, sc-test]`
  - `superpowers-receiving-code-review` → `[superpowers-requesting-code-review]`

## Tier assignment

- L1: `superpowers-verification-before-completion`, `superpowers-receiving-code-review`.
- L2: `superpowers-tdd`, `superpowers-systematic-debugging` (depend on Agency's test + debug substrate).
