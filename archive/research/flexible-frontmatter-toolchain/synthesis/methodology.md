# Methodology

Methods applied (per the executing prompt's S—Steps and the language-spec):

- **M01 Falsification** — every proposed primitive was attacked by asking "what input causes this to fail open?". Primitives that survived: required-keys-only validation, required-headings-only validation, stateless filesystem scan, set-difference diagnostic shape.
- **M06 First Principles** — the two non-negotiables (1) "extras pass / missing required fails" and (2) "no stored index" were derived from token-economy first principles, not from any source's recommendation.
- **M07 Contradiction Log** — three contradictions were logged in `../reflection/M07-contradiction-log.md`. The most consequential is store-an-index (task 010) vs. stateless (this prompt). Resolution: keep the *query CLI surface* from task 010, drop the persisted JSON.
- **M13 Adversarial Query Expansion** — generated 8 "trick" queries (e.g., "how does the toolchain handle a SKILL.md with a bilingual title and 14 ## headings?") to stress-test the spec; each yielded an acceptance-criterion in §6 of the SPEC.

## Source Takeaways (one bullet per source)

1. `MAINTENANCE.md` — Tier ladder (T1/T2/T3/T4) is the right gate for repair authority; the spec keeps it intact.
2. `PRE_COMMIT.md` — eight checklist items; only items 5/7 (formatting + mechanical governance) need the new toolchain — others are unchanged.
3. `RESEARCH.md` — research-folder structure is unchanged; the new spec is a *peer* to RESEARCH.md, not a replacement.
4. `TASK.md` (frontmatter ontology summary) — flat YAML, prefix-namespacing, max-1 nesting — all preserved.
5. `maintenance/language-spec.md` — RFC-2119 + Gherkin + L0/L1/L2/L3 ontology — the new SPEC inherits all three.
6. `research/obsidian-frontmatter-agentic-spec/output/SPEC.md` — Layered Schema with Namespacing — the new SPEC's required-keys table is keyed by `type:` exactly per L1+L2.
7. `research/repo-maintenance-protocol-spec/output/SPEC.md` — Run-Log + Coherence-Check protocol — preserved.
8. `research/skills-skill-architecture/output/SPEC.md` — three-tier disclosure — informs `fm-extract`'s default-section policy.
9. `research/skills-skill-container-capabilities/output/SPEC.md` — no git, REST API only — the toolchain is pure-Python stdlib, no git dependency.
10. `research/skills-namespace-ontology/output/SPEC.md` — closed `skill_kind` vocabulary; reciprocity error vs. warning rule — adopted verbatim.
11. `research/skills-navigation-bootstrap/output/SPEC.md` — manifest-driven nav — the new SPEC supersedes manifest emission with stateless `fm-query`.
12. `research/token-efficiency-tool-suite/output/SPEC.md` — four-stage pipeline (Estimator/Pruner/Enforcer/Validator) — `fm-extract` is the Pruner; `fm-validate` is the Validator; the other two stages remain out of scope.
13. `tools/dramatica-nav/{extract.py,validate.py,nav.py}` — direct prior art; the new tools are the generalisation.
14. `skills/skill-creator/SKILL.md` — validate→package→improve loop maps onto lint→repair→re-lint with `friction-log.md` as the feedback channel.
15. `skills/skill-creator/scripts/quick_validate.py` — short, schema-driven, one-diagnostic-per-problem — adopted as the diagnostic shape for `fm-validate`.
