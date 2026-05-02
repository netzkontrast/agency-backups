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
**Entscheidungsbaum für Expansion-Pattern (ASCII):**

```text
                  [Datei analysieren]
                           |
             +-------------+-------------+
             |                           |
     [type == 'index'?]            [status == 'archived'?]
        /         \                   /          \
     [Ja]        [Nein]             [Ja]        [Nein]
      |            |                 |            |
 [Lese Ordner-]    |             [Ignorieren]     |
 [Inhalt statt]    |                              |
 [Body]            |                              |
                   +------------------------------+
                                 |
                   [Schätze Tokens in 'summary']
                                 |
                        [< Token Budget?]
                         /             \
                      [Ja]            [Nein]
                       |                |
                  [Lese Body]    [Ignoriere Body]
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
# Kickoff-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich glaube mit hoher Confidence, dass es eine inhärente Reibung zwischen den flachen Strukturen gibt, die Obsidian nativ bevorzugt (und unterstützt), und den hierarchischen, relationalen Metadatenstrukturen, die LLM-Agenten für token-effiziente Graphennavigation benötigen.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Ein starkes Gegenbeispiel wäre, wenn sich herausstellt, dass LLMs gar keine stark vorstrukturierten Metadaten brauchen und stattdessen mit reinem rohen Text oder wenigen, sehr flachen Feldern weitaus besser performen, da semantische Retrieval-Engines dies besser handhaben könnten.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich liege am wahrscheinlichsten bei der Annahme falsch, dass eine einheitliche Schema-Spezifikation (eine einzige YAML-Block-Struktur) allen drei Konsumenten optimal gerecht werden kann, ohne dass es zu störendem "Metadaten-Noise" für menschliche Leser führt.

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
N/A - Ich stehe ganz am Anfang der Recherche.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Die höchstwertige nächste Aktion ist die First-Principles-Dekonstruktion (Step 1) der Begriffe "Obsidian Frontmatter", "tokeneffizientes Navigieren", "Expansion Pattern", und "Spec" sowie deren Überprüfung durch initiale Suchen in der Obsidian-Dokumentation und LLM-Context-Management-Literatur.

# Mid-Run-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich glaube mit hoher Confidence, dass das H2-Modell (Layered Schema) durch Namespacing (`prefix_key`) zu einem künstlichen H1-Modell (Flat Schema) kollabiert werden muss, um sowohl die Obsidian-Maximalgrenzen als auch die LLM-Token-Stabilität zu respektieren.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Das stärkste Gegenbeispiel ist das H3-Modell (Sidecar), in dem es dem Agenten vollkommen egal ist, was im Obsidian-YAML steht, weil er ein rohes JSON/YAML in `.meta.yml` liest, das beliebig verschachtelt sein kann.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich unterschätze vermutlich den Overhead, den ein H3-Sidecar-Modell für einen PKM-Nutzer erzeugt (Synchronisationsprobleme, Plugin-Inkompatibilität).

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
Ich würde sofort nach "Obsidian YAML namespace prefixing vs JSON sidecar" suchen, um die Trade-offs direkter zu adressieren.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Die Synthese der H1, H2 und H3 Hypothesen basierend auf dem Wissen über LLM-YAML-Parsing und Obsidian-Limits in `step2.md` abzuschließen und die "surviving architecture" zu identifizieren.

# Post-Query-Expansion-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich bin sehr confident (hoch), dass das Expansion-Pattern nicht primär durch Dateigröße (Token-Limit), sondern durch "Semantic Divergence" getriggert werden muss.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Das stärkste Gegenbeispiel sind Agenten-Frameworks, die starre Chunker verwenden (z.B. "teile nach 500 Wörtern"), weil semantisches Splittern für LLMs fehleranfällig zu programmieren ist.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich könnte falsch liegen in der Annahme, dass eine `README.md` Manifest-Datei im Expansion-Unterordner für Agenten leicht zu finden ist. Wenn sie die Ordner-Struktur nicht kennen, verfehlen sie das Manifest.

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
Ich würde Zettelkasten-Literatur überspringen und direkt auf "File System manifest index parsing für LLM RAG" suchen.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Die Heuristiken in harte Constraints (MUSS/KANN/DARF NICHT) zu gießen, um sie in Schritt 4 in der Spezifikation zu dokumentieren.

# Pre-Synthesis-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich glaube mit hoher Confidence, dass die finalen Spec-Ergebnisse nicht nur für Obsidian, sondern generell für agent-gestütztes PKM richtungsweisend sind, da sie die Trennlinie zwischen Mensch-lesbarem Zustand und Maschinen-Zustand ziehen.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Ein starkes Gegenbeispiel ist die Tatsache, dass sich LLM-Context-Windows auf 1M-2M Token erweitern (z.B. Gemini 1.5 Pro). Wenn Context Windows gigantisch und billig werden, wird tokeneffiziente Metadaten-Navigation möglicherweise obsolet.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich liege am wahrscheinlichsten bei der Definition der "Auslöser-Bedingung" (2000 Tokens) falsch, da dieses Limit durch den schnellen Fortschritt der Modelle bereits veraltet sein könnte.

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
Ich würde den Temporal Scope für Agenten auf 2024-2026 einschränken, da alles vor 2024 in Bezug auf Context-Window-Ökonomie veraltet ist.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Den Pre-Synthesis Integrity Check auszuführen und die gesammelten Artefakte in das endgültige `SPEC.md` Dokument zu gießen.

# Post-Synthesis-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich bin sehr confident (hoch), dass die vorliegende Spezifikation extrem nützlich für die Agenten-Integration ist und alle Vorgaben bezüglich Obsidian-Kompatibilität erfüllt.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Ein Agent, der nicht auf Context-Window-Ökonomie achten muss (weil Token-Kosten gegen Null gehen), würde diese gesamte Spezifikation (insbesondere das `summary` Feld) als überflüssigen Overhead betrachten.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich liege am wahrscheinlichsten bei der strengen Trennung in `index`-Nodes und `note`-Nodes falsch, weil sich eine Datei organisch in der Obsidian-Nutzung ständig dazwischen hin- und herbewegt, was die manuelle Pflege des `type`-Felds anstrengend macht.

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
Ich hätte von vornherein ein Automatisierungs-Script als Constraint eingeführt, um dem Menschen die manuelle Typ-Änderung beim Expansion-Pattern abzunehmen.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Pre-Commit Housekeeping (Löschen von Temp-Scripts, Erstellen der Readmes, Friction-Log) durchführen, um den sauberen State für den Commit vorzubereiten.

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
