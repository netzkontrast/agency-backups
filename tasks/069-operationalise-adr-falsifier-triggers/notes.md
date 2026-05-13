---
type: note
status: active
slug: 069-operationalise-adr-falsifier-triggers-notes
summary: "Trigger-classification table, audit baseline, and design notes for Task 069. Records the eight ADR-0008/0009 falsifier triggers, their classifier tier, and the first end-to-end audit run against HEAD."
created: 2026-05-13
updated: 2026-05-13
---

# Task 069 — Notes

## 1. Trigger classification table

| Trigger | Predicate | Classifier tier | Audit implementation |
|---|---|---|---|
| ADR-0008 F1 | narrative-skill count > 10 | mechanical | glob `skills/{dramatica-*,ncp-*,novel-architect*,suno-lyric-writer,the-agency-system-architect}` |
| ADR-0008 F2 | bootstrap-bundle > 60 K tokens | mechanical | composes `bundle-size-snapshot.measure_bundle()` |
| ADR-0008 F3 | sustained NO.5-cited FL1+ across 3+ sessions in 14 d | semi-mechanical | walks `tasks/*/friction-log.md` + `research/*/reflection/friction-log.md`; regex on `NO.5` / `narrative-ontology` + `Highest Frustration Level: FL[1-3]`; mtime-windowed |
| ADR-0008 F4 | narrative skill change requires T3 amendment of non-AGENTS/SKILLS root spec | mechanical (candidates) + manual (T3 confirm) | walks `tasks/*/task.md`, extracts `task_affects_paths:` YAML block, flags entries that list a narrative path AND a root spec other than AGENTS.md / SKILLS.md |
| ADR-0008 F5 | third-party adopter blocker | manual | reported as MANUAL; never counts as a fire |
| ADR-0009 F1 | bundle > 100 K tokens | mechanical | composes `bundle-size-snapshot.measure_bundle()` |
| ADR-0009 F2 | either PRE_COMMIT.md or FRUSTRATED.md < 1000 tokens AND < 50 dependents | mechanical | extended `bundle-size-snapshot.count_dependents()` (basename grep over `.md`/`.py`/`.sh`) |
| ADR-0009 F3 | sustained bundle-cited FL1+ across 3+ sessions in 14 d | semi-mechanical | same friction-aggregator as F3, regex on bundle-size / root-spec-count / 11-spec-bundle |

Trigger discovery is hard-coded in `tools/maintenance/adr-trigger-audit.py` (matches the ADR-0008 / ADR-0009 trigger sets directly). The generalisation path — `adr_triggers:` frontmatter on each ADR — is deferred per the Task `Out of scope` clause; the audit's `TRIGGER_ORDER` constant is the single edit point if a future ADR adopts the pattern.

## 2. Audit baseline (2026-05-13)

Command: `python3 tools/maintenance/adr-trigger-audit.py --format text`

```
# adr-trigger-audit (2026-05-13; window=14d)
# bundle: 11 specs / ~77859 tokens

decisions/0008-narrative-skills-status-quo.md::WARN:ADR-0008.F1:[FIRED] narrative-skill count=11 (threshold>10); skills=dramatica-theory,dramatica-vocabulary,ncp-author,novel-architect,novel-architect-character,novel-architect-legacy,novel-architect-scene,novel-architect-structure,novel-architect-world,suno-lyric-writer,the-agency-system-architect
decisions/0008-narrative-skills-status-quo.md::WARN:ADR-0008.F2:[FIRED] bundle-tokens=77859 (threshold>60000)
decisions/0008-narrative-skills-status-quo.md::INFO:ADR-0008.F3:[ok] NO.5-cited FL1+ sessions in last 14d = 2 (threshold>=3); cited=tasks/045-readme-coherence-refresh/friction-log.md,tasks/056-narrative-skills-extraction-adr/friction-log.md
decisions/0008-narrative-skills-status-quo.md::INFO:ADR-0008.F4:[ok] candidates=0 (requires manual T3-vs-T1/T2 review); list=none
decisions/0008-narrative-skills-status-quo.md::INFO:ADR-0008.F5:[MANUAL] third-party-adopter blocker — no in-repo signal; maintainer review required
decisions/0009-root-spec-no-consolidation.md::INFO:ADR-0009.F1:[ok] bundle-tokens=77859 (threshold>=100000)
decisions/0009-root-spec-no-consolidation.md::INFO:ADR-0009.F2:[ok] PRE_COMMIT.md(tokens=5511,deps=200); FRUSTRATED.md(tokens=2164,deps=228) (fire when tokens<1000 AND deps<50)
decisions/0009-root-spec-no-consolidation.md::INFO:ADR-0009.F3:[ok] bundle-cited FL1+ sessions in last 14d = 0 (threshold>=3); cited=none

# summary: any_fired=True; manual triggers are reported but do NOT fire automatically
```

Runlog projection (appendable to `maintenance/run-log.md`):

```
2026-05-13 | adr-trigger-audit | 8 triggers / window=14d / bundle~77859 tokens | FIRED:ADR-0008.F1,ADR-0008.F2 | manual=ADR-0008.F5
```

## 3. Baseline findings — divergence from the task brief

The task brief asserted "assert no trigger currently fires; ADR-0009 F1 should be ~70,676 tokens / 11 specs per the existing snapshot." The audit ran honestly and surfaced two genuine fires plus one drift:

- **ADR-0008 F1 fired (11 narrative skills).** ADR-0008's prose lists 6 narrative skills ("today: 6"); since the ADR was authored, the `novel-architect` corpus has split into 5 sub-skills (`-character`, `-legacy`, `-scene`, `-structure`, `-world`) plus the original. The audit counts 11 directories matching the narrative glob (`dramatica-*`, `ncp-*`, `novel-architect*`, `suno-lyric-writer`, `the-agency-system-architect`). This is a *genuine* fire that the maintainer needs to know about — the audit's job was to surface it, not to suppress it. A successor ADR is the correct response per the ADR-0008 protocol.
- **ADR-0008 F2 fired (~77,859 tokens > 60 K).** The ADR-0008 baseline of "~50 K tokens" predates the README, MAINTENANCE.md, and ADR ratifications that landed during Tasks 056/057/060. The threshold was crossed at some point between then and now. Again, surfacing this is the *correct* outcome — the audit reveals that a baseline written 2 days ago is already stale relative to its own threshold.
- **ADR-0009 F1 still under (~77,859 < 100 K).** The brief's stated 70,676 was the 2026-05-11 measurement; today's 77,859 reflects the run-log appending, this Task's MAINTENANCE.md and ADR amendments. No fire.
- **ADR-0009 F2 not fired.** PRE_COMMIT.md (5,511 tokens, 200 deps) and FRUSTRATED.md (2,164 tokens, 228 deps) both pass the threshold.

The maintainer SHOULD review ADR-0008 F1 / F2 fires and either (a) file a successor ADR per the protocol, or (b) update the ADR-0008 thresholds if the original numbers were undercounted (a T3 amendment requiring a Task). The audit script's job ends here.

## 4. Design notes

- **Composition, not duplication.** `adr-trigger-audit.py` imports `bundle-size-snapshot.py` via `importlib.util.spec_from_file_location` (the dashed filename forbids a `from … import …` form). The loader prefers the script colocated with this audit file (canonical install) and falls back to `<repo_root>/tools/maintenance/`, so tests can spawn the audit against a synthetic `tmp_path` repo without copying the bundle script in.
- **`bundle-size-snapshot.py` extension.** Added `count_dependents(repo_root, spec_rel)` and an `--include-dependents` CLI flag. Dependents are counted by basename match over `.md` / `.py` / `.sh` files, skipping `.git`, `.agent_cache`, `node_modules`, `Agency-System`. The default measure-bundle path is unchanged (no dependents in the record) so ADR-0009 F1 stays cheap.
- **Manual triggers.** ADR-0008 F5 is reported as `MANUAL` with `level: INFO` and `fired: False`. The audit's `any_fired` aggregation deliberately excludes manual triggers — a third-party-adopter signal can only come from a maintainer.
- **Friction-window correctness.** Window is `mtime`-based, not parsed from frontmatter, so the audit measures "files touched in the last 14 days" regardless of whether the friction log's body claims a different date. This matches the ADR-0008 F3 / ADR-0009 F3 intent ("sessions in a 14-day window").
- **F4 heuristic precision.** The heuristic scans only the `task_affects_paths:` YAML block (not the whole task body), which eliminates the false positive observed in a first-pass implementation where prose mentions of MAINTENANCE.md / PRE_COMMIT.md triggered F4. The remaining residual risk: a Task's `task_affects_paths` may list a root spec for a T1 / T2 metadata bump (not a T3 amendment); the audit flags it as a *candidate* and the maintainer confirms tier.
