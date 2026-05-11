---
name: novel-architect-world
description: >-
  World & Research Sub-Skill von novel-architect. Unterstützt Phase 4
  (World & Research) bei Domain-Mapping, Welt-Bibel-Erstellung und der
  Delegation an research-prompt-optimizer für Deep-Research-Briefs.
  Trigger: /novel-research, "Welt-Bibel", "Domain-Mapping", "Research Brief",
  "Worldbuilding für Roman". Delegiert Recherche-Ausführung an
  research-prompt-optimizer. NICHT bei generischer Recherche ohne Roman-Scope.
metadata:
  category: creative-writing
  parent: novel-architect
  version: "1.1.0"
  status: active
  date_added: "2026-05-11"
  date_updated: "2026-05-11"
  state_management: "ncp"
  ncp_schema_version: "1.3.0"
  triggers: >-
    novel-architect-world, world bible, welt-bibel, domain mapping,
    research brief, worldbuilding, /novel-research
  delegates_to: >-
    novel-architect (parent orchestrator), research-prompt-optimizer,
    dramatica-theory (optional, für Signpost-Anchoring)
---

# novel-architect-world v1.1.0

Sub-Skill von [`novel-architect`](../novel-architect/). Wird in Phase 4
(World & Research) vom Orchestrator delegiert. Trennt *Methodik der
Recherche* (hier) von *Ausführung der Recherche* (delegiert an
`research-prompt-optimizer`).

## Scope

| Phase | Verantwortung |
|-------|---------------|
| Phase 4 — World & Research | Domain-Inventar; Research-Brief-Generierung; Welt-Bibel-Konsistenz; optional Signpost-Content-Updates |

## Verfügbare Methoden

| File | Methode | Wann verwenden |
|------|---------|----------------|
| [`methods/domain-mapping.md`](./methods/domain-mapping.md) | Systematisches Domain-Inventar | Erste Phase-4-Durchführung; identifiziert recherchierbare Welt-Domänen |
| [`methods/deep-research-briefs.md`](./methods/deep-research-briefs.md) | Brief-Template für research-prompt-optimizer | Pro identifizierter Domain ein Brief; Delegation an externes Research-Tool |

## Delegation Contract

Dieser Sub-Skill schreibt **nur** in:

- Workspace-File `world-bible.md` (Phase 4)
- Workspace-Dir `research/briefs/<domain>.md` (Phase 4, ein Brief pro Domain)
- Optional NCP `signposts[]` content-updates (über `ncp-author`), wenn Forschung Canon ändert

Research-Ausführung selbst (Web-Search, Paper-Extraction, PDF→MD-Pipeline) wird an `research-prompt-optimizer` delegiert. Dieser Sub-Skill **schreibt** den Brief, **liest** die Ergebnisse, integriert sie in die Welt-Bibel.

## Constraints

- **Skill ist projekt-agnostisch:** Genre/Setting kommt aus `intent.yaml`, nicht aus Skill-Defaults.
- **Methoden on demand:** kein eager-load der Recherche-Methoden bei Bootstrap.
- **Research-Auslagerung:** dieser Sub-Skill *spawned* keine Web-Calls — er bereitet sie für `research-prompt-optimizer` vor.
- **Canon-Schutz:** Research-Findings werden NICHT direkt als Canon committed; sie werden im Welt-Bibel-Workflow durch User-Approval gefiltert (analog Phase-2-Gate-Pattern).

## Integration mit novel-architect

| Skill-Call | Aktion |
|---|---|
| `/novel-research` (im Orchestrator) | Orchestrator routet Phase 4 zu diesem Sub-Skill |
| Direct Trigger ("Welt-Bibel für Hard-SF Roman") | Skill-Loader lädt diesen Sub-Skill direkt |

## Closing Note

Dieser Sub-Skill ist die **Recherche-Methodik-Library**, nicht das
Recherche-Tool selbst. Web-Search, Paper-Extraction, PDF-Konvertierung gehören
nach `research-prompt-optimizer`. Hier leben nur die *Templates* + die
*Integration in die Welt-Bibel*.
