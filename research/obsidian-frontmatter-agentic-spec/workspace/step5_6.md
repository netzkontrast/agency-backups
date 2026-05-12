# Step 5 & 6: Plugins und Ontologie-Mapping

## 5. Plugin Linkliste

- **Dataview** (https://github.com/blacksmithgu/obsidian-dataview)
  - Mehrwert: Erlaubt SQL-ähnliche Abfragen über alle Metadaten.
  - Einordnung: Optional (Agenten machen ihre eigenen Suchen, aber für menschliche UI extrem nützlich).
- **Linter** (https://github.com/platers/obsidian-linter)
  - Mehrwert: Automatisiert das Sortieren von YAML-Keys und zwingt Vaults zur Konsistenz.
  - Einordnung: Optional-Advanced (Wichtig für Mensch-Agenten-Zusammenarbeit, damit Agenten ein vorhersehbares Format parsen).
- **Metadata Menu** (https://github.com/mdelobelle/metadatamenu)
  - Mehrwert: Typisierung von Frontmatter-Feldern und Dropdowns für Menschen.
  - Einordnung: Optional (Erzwingt L2-Schemas per UI, was Agenten vor ungültigen Enums schützt).

## 6. Ontologie-Mapping (Dublin Core, Schema.org)

### Mapping Strategien
1. **Direct Mapping:** `dc:title` wird zu `title`.
   - *Vorteil:* Einfach.
   - *Contrast Class:* Verglichen mit Prefix-Mapping unter Obsidian ist Direct Mapping besser für den Menschen, da Obsidian Keys wie `dc:title` aufgrund des Doppelpunkts als Strings wrappen muss, was in der UI seltsam aussieht.
2. **Prefix Mapping (Namespace):** `dc_creator`, `schema_author`.
   - *Vorteil:* Keine Kollisionen, Obsidian Properties UI bleibt intakt.

### [SYNTHESE] Umgang mit nicht-YAML-kompatiblen L3-Metadaten
Agenten-spezifische, komplexe Metadaten (Embedding-Vektoren, Multi-Doc-Relationship-Trees) DARF NICHT ins Obsidian Frontmatter.
**Die Script-Logik:**
Das begleitende Python Script liest `KonzeptA.md`. Wenn es `type: index` erkennt, sucht das Script parallel nach `.agent_cache/KonzeptA.meta.json` im Root des Vaults. L3 Metadaten leben in dieser schattigen Sidecar-Datenbank (einem isolierten Ordner, den Obsidian ignoriert), verknüpft durch den reinen Dateinamen.
