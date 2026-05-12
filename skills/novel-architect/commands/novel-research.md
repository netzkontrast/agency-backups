# /novel-research — Phase 4 Trigger

> **Phase:** 4 (World & Research)
> **/sc:-Analog:** `sc:research` (delegiert intern an `research-prompt-optimizer`)

## Zweck

Identifiziert Forschungs-Domänen, erstellt Recherche-Briefs, delegiert an
`research-prompt-optimizer`, integriert Findings in World-Bible + canon-meta.

## Trigger

- „/novel-research"
- „Recherche zu X starten"
- „Welt-Bibel"
- „Forschung integrieren"

## Pre-Conditions

- `intent.yaml` approved (mit philosophy/science_integration_level Hinweisen)
- Optional: `architecture.yaml`, `character-architecture.yaml`

## Workflow

```
Phase 4.1   Identify research domains (auto from intent + askuser)
Phase 4.2   Prioritize domains
            ──── GATE (research scope) ────                     (askuser)
Phase 4.3   Pro Domain: render research brief                   (assets/research-brief-template.md)
Phase 4.4   Hand off to research-prompt-optimizer               (delegates)
Phase 4.5   Ingest findings → world-bible.md                    (manual review)
Phase 4.6   Update NCP signposts wenn relevant                  (delegate ncp-author)
```

## Delegations

- `research-prompt-optimizer` (Deep Research Pipeline)
- `ncp-author` für `signposts[]` content updates

## Output

- `research/briefs/<domain>.md`
- `research/findings/<domain>.md` (kommt von research-prompt-optimizer)
- `world-bible.md` (kuratiert)
- ggf. NCP-Update, canon-meta.md-Update

## Hand-off

→ Phase 5 (`/novel-scenes`) wenn genug Welt-Material vorhanden

## Detail

- `phases/phase4-world-research.md`
- [`novel-architect-world/methods/domain-mapping.md`](../../novel-architect-world/methods/domain-mapping.md)
- [`novel-architect-world/methods/deep-research-briefs.md`](../../novel-architect-world/methods/deep-research-briefs.md)
- `assets/research-brief-template.md`
