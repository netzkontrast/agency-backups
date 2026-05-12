# Step 3: Die vier Metadaten-Ebenen im Detail

## 3.1 L0: Obsidian Default (Minimal)
Obsidian nativ verarbeitet folgende Keys besonders:
- `tags`: (list of strings) Nativ im Graph und Suche unterstützt.
- `aliases`: (list of strings) Erlaubt alternative Wikilinks.
- `cssclasses`: (list of strings) Beeinflusst UI Rendering.
- `publish`: (boolean) Flag für Obsidian Publish.
Native Datentypen (UI-interpretiert): `Text`, `List`, `Number`, `Checkbox` (bool), `Date`, `Date & time`.
Verschachtelungen über 2 Ebenen brechen das UI und zwingen Obsidian in den Plain-Text-Modus.

## 3.2 L1: Vault Core (Pflichtfelder für Alle)
Synthetisiertes Minimum für Agent+Mensch+UI:
- `type`: [string] (note, index, manifest) - Zeigt dem Agenten das Verhaltensmuster.
- `status`: [string] (draft, active, archived) - Filtert Rauschen für Agenten.
- `summary`: [string] Ein Satz. Erlaubt dem Agenten zu entscheiden, ob er Token für den Body ausgeben soll.
- `created`: [date]
- `modified`: [date]
*Contrast Class:* Ein reines Obsidian Vault braucht keines dieser Felder. Ein Agenten-unterstütztes Vault *muss* `summary` und `type` haben, sonst degeneriert die Suche zu Fulltext-Scans.

## 3.3 L2: Domain Extensions (Namespacing)
Konvention: `[domain]_[key]`
- **Research:** `research_phase`, `research_confidence`
- **Dev:** `dev_module`, `dev_language`
- **Agent:** `agent_token_estimate` (Erlaubt dem Agenten Budget-Planung, bevor er liest).
*Validierung:* Bricht keine Obsidian-Regeln, da Flat YAML.

## 3.4 L3: Agent-Only Metadata
Agenten brauchen intern Zustand (z.B. Vector-Embeddings, Relevanz-Scores).
*Soll das ins Frontmatter?*
NEIN. Embeddings sind Arrays mit 1536 Floats. Das ins YAML zu schreiben zerstört die Datei für den Menschen.
*Abwägung:* L3 MUSS zwingend in eine Sidecar-Datei (`.meta.json` oder eine separate Vektordatenbank). Das Frontmatter (L0-L2) referenziert diese nur indirekt oder gar nicht.
