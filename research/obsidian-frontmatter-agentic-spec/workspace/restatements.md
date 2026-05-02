# Restatement Checkpoint vor Step 1

## Role
Ich agiere als PKM-Architekt und LLM-Systems-Ingenieur mit tiefgreifender Expertise in Obsidian-Vault-Design (YAML-Frontmatter, Properties API, Plugins), Knowledge-Graph-Modellierung, token-ökonomischem Design für LLM-Context-Windows, Agent-Tool-Design und Zettelkasten-Methodik. Mein Ziel ist es, eine Obsidian-Vault-Metadaten-Spezifikation für einen Software-Architekten zu erforschen, die für ein Python-Script zur tokeneffizienten Metadatenauslese als Grundlage dient, als Agent-Skill nutzbar ist, von Claude Code, Google Jules konsumiert werden kann und zu 100% Obsidian-kompatibel bleibt.

## Active Constraint Blocks
- **CONSTRAINT BLOCK 0 — Reflection Baseline:** Ich muss vor/während spezifischer Checkpoints schriftliche Reflektionen in `M00` Dateien (Q1-Q5 Format) generieren und aufschreiben. Diese Reflektionen dürfen nicht ausgelassen werden.
- **CONSTRAINT BLOCK 1 — Source Priority Rules:** Primärquellen (Offizielle Docs, Github, etc) > Aggregatoren (Reddit, etc) > Praktiker-Vaults. Bei Konflikten kommt das Contradiction Log zum Einsatz. Synthetisches Wissen muss explizit mit `[SYNTHESE]` markiert werden.
- **CONSTRAINT BLOCK 2 — Temporal Scope:** Research muss Quellen von 2020-2026 für PKM abdecken. Agentic/LLM spezifische Quellen gelten von 2022-2026.
- **CONSTRAINT BLOCK 3 — Output Exclusions:** Ausschluss von Plugin-Implementierungsdetails (Code zum Schreiben eines Plugins), generischer PKM-Philosophie ohne Frontmatter-Bezug, Obsidian-Vergleichen mit anderen Tools ohne Bezug auf Metadaten-Design, und Marketing-Inhalten.
- **CONSTRAINT BLOCK 4 — Obsidian-Kompatibilitätspflicht:** Nur YAML-Frontmatter (kein JSON/TOML), max. 2 Ebenen der Verschachtelung, nur Obsidian-native Typen, Respektierung von reservierten Keys, Beachtung von Performance-Limits (Graph degradiert ab ~500 Dateien ohne Struktur).
- **CONSTRAINT BLOCK 5 — Agentic-Konsumenten-Dualität:** Metadaten müssen für UI, Mensch und Agent gleichzeitig funktionieren. Ein Agent darf nicht gezwungen sein, eine Datei komplett lesen zu müssen, um deren Relevanz zu verstehen. Die Metadaten allein müssen zur Navigation reichen.

## Active Critical-Thinking Methods
1. **Falsification (Popper):** Aktiv nach Evidenz suchen, die eine Hypothese widerlegt.
2. **First-Principles Decomposition:** Begriffe in ihre basalsten Komponenten aufbrechen und hinterfragen.
3. **Steelmanning:** Die stärkste Version eines Arguments aufbauen, bevor es verworfen wird.
4. **Contrast Classes:** Explizite Kontraste (verglichen womit? unter welcher Bedingung?) für evaluative Aussagen.
5. **Adversarial Query Expansion:** Suchbegriffe bei Checkpoints in vier Achsen (Adjacent, Opposing, Abstraction, Orthogonal) erweitern, um Local-Minimum-Lock-In zu vermeiden.
