# Step 7 & 8: Triangulation & Hypothesis Audit

## 7.1 Mini-Schema: Surviving-Branch Triangulation
- **Claim:** Das "Layered Schema mit Namespacing (H2)" kombiniert mit einer externen L3-Sidecar-Datenbank ist die einzige Architektur, die die Obsidian Properties UI (max 2 Ebenen) respektiert und gleichzeitig LLMs durch flache Keys vor Halluzinationen beim Schema-Parsing schützt.
- **Key Evidence 1:** LLM Parser-Probleme mit nested YAML. [Quelle: M13 Expansion "YAML frontmatter limitations LLM"]
- **Key Evidence 2:** Obsidian Properties Limitationen auf max 2 Ebenen. [Quelle: Offizielle Doku]
- **Key Evidence 3:** Game Engine Asset Management nutzt Sidecars für maschinelle L3 Metadaten. [Quelle: M13 Expansion "game engine asset metadata taxonomy"]
- **Stärkstes Gegenbeispiel:** Vollständige Sidecars (H3) halten die Markdown-Datei völlig sauber für Menschen. [Quelle: Zettelkasten-Puristen-Theorie]
- **Confidence:** HOCH
- **Was-würde-mich-überzeugen-umzustellen:** Wenn Obsidian ein natives JSON-LD Plugin im Core integriert, das unsichtbar für die Properties-UI agiert.

## 8. Hypothesis Half-Life Audit
1. **Foundational Hypothesis:** "Agenten nutzen ausschließlich Context Windows, um Dateien zu lesen."
   - **Decay-Test:** Hypothese decayed, wenn eine Suche nach "agent metadata outside YAML" zeigt, dass Agenten vermehrt RAG und isolierte Vector-DBs nutzen.
   - **Resultat:** Gefeuert. Agenten (wie Claude Code) können Tools nutzen, um Vektordatenbanken abzufragen, weshalb L3 Metadaten (Embeddings) legitim ausgelagert werden können, ohne die Fähigkeiten des Agenten zu beschneiden.
