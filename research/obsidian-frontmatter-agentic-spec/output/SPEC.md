# Obsidian Frontmatter & Agentic Navigation — Research Synthesis

## Executive Summary
Die Analyse hat ergeben, dass das optimale Schema für ein Obsidian-Vault im Zusammenspiel mit autonomen Agenten ein "Layered Schema mit Namespacing" (H2) ist. Dieses Schema kombiniert die Obsidian-notwendige flache Struktur (Level 0 YAML) mit der semantischen Sicherheit geschichteter Ontologien durch Prefix-Keys (z.B. `research_status`). Die wichtigste unerwartete Erkenntnis war, dass agenten-spezifische Metadaten (L3) wie Embeddings zwingend in eine Sidecar-Datenbank ausgelagert werden müssen, da sie andernfalls die Obsidian Properties-UI sprengen und die Token-Limits beim Parsen überschreiten. Eine Lücke, die keine Quelle direkt abdeckte, war die exakte Token-Auslösegrenze für das Expansion-Pattern, die deshalb aus Retrieval-Augmented Generation (RAG) Best Practices abgeleitet wurde.

## Hypothesenbaum
- **H1 — Flat Schema:** Scheitert an Namenskollisionen bei Skalierung in komplexen Vaults.
- **H3 — Sidecar-Model (Total):** Scheitert, da Obsidian Properties UI komplett ausgehebelt wird und es menschliche Leser benachteiligt.
- **H2 — Layered Schema mit Namespacing (ÜBERLEBEND):** Nutzt Präfixe (`domain_key`), um Ebenen zu simulieren, ohne YAML tiefer als 1 Ebene zu verschachteln. Dies schützt vor LLM-Parsing-Halluzinationen und respektiert Obsidians Limit von 2 Ebenen.
- *Straw-Man-Tests für H1 und H3 wurden durchgeführt und haben die jeweiligen Kernstärken (Einfachheit bei H1, Separation of Concerns bei H3) validiert, bevor sie aufgrund von Konsumenten-Ausschlüssen (Constraint 5) verworfen wurden.*

## Metadaten-Ebenen-Matrix
### L0 — Obsidian Default
| Key | Obsidian-Typ | Verhalten | Reserviert? |
|---|---|---|---|
| tags | list | Nativ für Graphen/Suche genutzt | Ja |
| aliases | list | Erlaubt alternative Wikilinks | Ja |
| cssclasses | list | Modifiziert das UI Rendering | Ja |

### L1 — Vault Core (Pflicht)
| Key | Typ | Obsidian | Mensch | Agent | Quelle/SYNTHESE |
|---|---|---|---|---|---|
| type | string | Ignoriert | Orientierung | Basis für Parsing-Entscheidung | [SYNTHESE] |
| status | string | Ignoriert | Lifecycle | Filtert Rauschen | [SYNTHESE] |
| summary | string | Ignoriert | tl;dr | Ersetzt Body-Reading (Token-Safe) | [SYNTHESE] |
| created | date | Zeigt an | Info | Temporal-Routing | Offiziell |

### L2 — Domain Extension Namespacing
Konvention: `[domain]_[key]`
- **Research Domain:** `research_phase`, `research_sources_count`
- **Novel Domain:** `novel_act`, `novel_pov`
- **Agent Domain:** `agent_token_estimate`, `agent_depends_on`

### L3 — Agent-Only
Felder wie Vektoren, Graph-Scores, Token-Matrizen.
**Entscheidung:** Sidecar. Die Markdown-Datei DARF KEINE L3 Metadaten im YAML Frontmatter enthalten. Diese wandern in `/.agent_cache/[dateiname].meta.json`.

## Expansion-Pattern-Spec
- **MUSS:** Eine Datei wird in einen Ordner gleichen Namens expandiert, wenn "Semantic Divergence" eintritt (mehr als 5 heterogene H2-Blöcke).
- **MUSS:** Die Originaldatei bleibt als `[Name].md` im neuen Ordner als Index-Node erhalten und setzt `type: index` im Frontmatter.
- **DARF NICHT:** Es darf keine `README.md` Manifest-Datei erstellt werden. Der Index-Node fungiert als Manifest.
- **KANN:** Die Datei wird expandiert, wenn sie 2000 Tokens überschreitet.

## Plugin-Linkliste
- **Dataview** | https://github.com/blacksmithgu/obsidian-dataview | SQL-Metadaten Abfragen | Optional
- **Linter** | https://github.com/platers/obsidian-linter | Zwingt YAML-Konsistenz | Optional-Advanced
- **Metadata Menu** | https://github.com/mdelobelle/metadatamenu | Typisierung in der UI | Optional

## Ontologie-Mapping-Guide
- **Direct Mapping:** (`dc:title` -> `title`) Besser für Obsidian UI, da Doppelpunkte in Obsidian Keys unschön als String gewrappt werden.
- **Prefix Mapping:** (`dc_creator` -> `schema_author`) Besser für Agenten, da Namespaces Kollisionen verhindern.
- **Metadaten die nicht in Obsidian passen:** Multi-Doc-Trees und Embeddings wandern in die externe L3-Sidecar JSON.

## Synthesis — Spec-Grundlage für Python-Script
```yaml
# L0+L1 Minimal-Pflicht (YAML)
---
tags: [research, agentic]
aliases: []
type: "note" # Oder index, manifest
status: "active" # Oder draft, archived
summary: "Kurze Zusammenfassung für den Agenten, um Token-Laden zu vermeiden."
---
```
**Pseudocode für Script-Logik:**
```python
def process_file(filepath):
    frontmatter = extract_yaml(filepath)
    if frontmatter['type'] == 'index':
        children = get_folder_contents(filepath.parent)
        return {"action": "scan_children", "targets": children}
    if frontmatter['status'] == 'archived':
        return {"action": "ignore"}
    if estimate_tokens(frontmatter['summary']) < budget:
        return {"action": "read_body"}
```

## Contradiction Log
- **Widerspruch:** "Flat vs Layered Schema".
- **Auflösung:** Resolved durch "Layered Schema mit Namespacing" (Simulierte Schichten in flacher Struktur).

## Hypothesis Half-Life Audit
- **Hypothese:** Agenten lesen alles im Context Window.
- **Decay:** Gefeuert. Agenten nutzen heute isolierte Vector-DBs (RAG) als Tools, weshalb L3 in Sidecars ausgelagert werden kann.

## Query Expansion Log
1. **Adjacent:** "PKM metadata taxonomy" -> Novel: Trennung von Taxonomic vs Procedural. Modified H2.
2. **Opposing:** "YAML frontmatter limitations LLM" -> Novel: LLMs halluzinieren bei tiefen YAMLs. Modified H2.
3. **Orthogonal:** "game engine asset metadata taxonomy" -> Novel: Asset-Sidecars sind Industrie-Standard für Metadaten. Modified L3 Handling.

## Reflection History
[M00-Kickoff] Fokus auf Reibung zwischen Obsidian (flach) und Agent (Hierarchie). Nächster Schritt: First-Principles.
[M00-Midrun] Confidence in Namespacing. Sidecar (H3) als stärkstes Gegenbeispiel.
[M00-Post-Query] Expansion-Pattern wird durch Semantik, nicht nur Tokens getriggert.
[M00-Pre-Synthesis] Agenten-Technologie (Context Windows) entwickelt sich schnell, Auslöser-Grenzen könnten veralten.

## Open Questions / Unresolved
Wie geht die Obsidian Graph View nativ mit dem L2-Namespacing um, ohne dass externe Plugins die Verbindungen visualisieren müssen?

## Sources
- Offizielle Obsidian Properties-Doku [Primärquelle]
- Obsidian GitHub Issues (YAML Nesting Limits) [Primärquelle]
- Community Foren (Zettelkasten-Implementierungen) [Sekundärquelle]

## Methodology Note
Methoden angewandt: M01 (Falsifikation bei H-Baum), M06 (First Principles bei Begriffen), M07 (Contradiction Log bei Flat vs Layered), M13 (Adversarial Query Expansion).
Erkenntnis L1-Pflichtfelder generiert durch `[SYNTHESE]`.
Erkenntnis Expansion-Auslöser generiert durch `[SYNTHESE]`.
