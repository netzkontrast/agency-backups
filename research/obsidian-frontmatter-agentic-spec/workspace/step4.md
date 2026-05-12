# Step 4: Das Expansion Pattern

**[SYNTHESE] Heuristiken für Dateigrößen-Entscheidungen**

## Auslöser-Bedingungen (Wann wird expandiert?)
Ein Datei MUSS in einen Index-Node umgewandelt und in einen Ordner expandiert werden, wenn:
1. **Token-Schwellwert:** Die Datei überschreitet 2000 Tokens (ca. 1500 Wörter). Bei dieser Größe beginnt der Rauschen-zu-Signal-Wert für RAG drastisch zu fallen.
2. **Referenz-Dichte-Schwellwert:** Es gibt mehr als 5 H2-Überschriften, die intern stark verschiedene Sub-Konzepte behandeln (Semantic Divergence).

## Das Index-Node-Pattern
Wenn `KonzeptA.md` expandiert wird:
1. Erstelle Ordner `/KonzeptA/`.
2. Verschiebe Originaldatei `KonzeptA.md` nach `/KonzeptA/KonzeptA.md` (Obsidian updated Backlinks automatisch).
3. **MUSS:** Die Datei behält ihre Existenz.
4. **MUSS:** Im Frontmatter wird `type: index` gesetzt.
5. **KANN:** Ein neues Feld `expanded_to: ./` kann eingefügt werden.
6. Der Inhalt wird in kleinere Notes (z.B. `/KonzeptA/Subkonzept1.md`) umgewandelt.

## Die Manifest-Datei
**DARF NICHT:** Das Index-Node-Pattern verlangt keine dedizierte `README.md` *zusätzlich* zur `KonzeptA.md` als Index. Das wäre eine Verdopplung. Die ursprüngliche `KonzeptA.md` WIRD zum Manifest für den Ordner `/KonzeptA/`.
- **MUSS:** Das Manifest enthält Dataview-Queries oder Wikilinks zu allen Unterdateien.

## Agent-lesbare Entscheidungsregeln
Damit ein Agent **nie** eine Datei öffnen muss, um Relevanz zu beurteilen, müssen diese 4 Felder im L1-Core existieren:
1. `type` (Weiß der Agent, ob es ein Index ist oder roher Text?)
2. `status` (Ist es relevant/aktuell?)
3. `summary` (Reicht die kurze Essenz aus?)
4. `tags` (In welchem Kontext steht es?)
