# M13 Adversarial Query Expansion - Pass 1

## Seed Query Set
- "Obsidian frontmatter schema layers"
- "YAML metadata namespacing knowledge base"
- "flat frontmatter better than layered Obsidian"
- "YAML sidecar metadata drawbacks Obsidian"
- "AI agent Obsidian navigate metadata"

## Expansion 1 (Adjacent Axis)
**Query:** "PKM metadata taxonomy"
**Novel Finding:** Ja. Taxonomy vs. Schema - In PKM wird oft zwischen taxenomischen Metadaten (Struktur der Kategorien) und prozeduralen Metadaten (Status, Abhängigkeiten) unterschieden.
**Conclusion Modified:** Ja, die Unterscheidung zwischen L1 (Vault Core/Procedural) und L2 (Domain/Taxonomy) wird dadurch gestützt.

## Expansion 2 (Opposing Axis)
**Query:** "YAML frontmatter limitations LLM"
**Novel Finding:** Ja. LLMs halluzinieren stark bei tiefen YAML-Strukturen und haben Probleme, geschachtelte Keys korrekt wieder zusammenzusetzen, besonders wenn Arrays von Objekten genutzt werden.
**Conclusion Modified:** Ja, stützt H1 (Flat Schema) massiv gegenüber tief geschachtelten L2-Ebenen in H2. Die Obsidian-Constraint (max 2 Ebenen) ist für LLMs nicht strikt genug, LLMs bevorzugen 1 Ebene.
## Expansion 3 (Orthogonal Axis)
**Query:** game engine asset metadata taxonomy
**Novel Finding:** Ja. Game Engines lagern Asset-Payload (Textur/Code) fast immer aus und behalten ein .meta Manifest mit GUID und Type. Das Sidecar-Pattern ist Standard für Performance.
**Conclusion Modified:** Ja, festigt die Entscheidung, L3 (Agent-Score/Vector) komplett aus dem Obsidian YAML rauszuhalten.
