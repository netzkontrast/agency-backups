# Scripts

Utility-Skripte für Workspace-Setup und Skill-Packaging.

| File | Funktion |
|------|----------|
| `bootstrap_project.sh` | Erstellt Projekt-Workspace unter `/home/claude/novel-projects/<slug>/`. Bei `kohaerenz-protokoll`: migriert vom Legacy-Skill |
| `package_skill.sh` | Wrapper für `skill-creator/scripts/package_skill.py` — packt diesen Skill in `.skill`-Datei |
| `convert_pdfplumber.py` | PDF→Markdown Fallback (übernommen aus Legacy) für Research-Pipeline wenn `pymupdf4llm` nicht installierbar |

## Usage

```bash
# Neues Projekt anlegen:
bash scripts/bootstrap_project.sh my-sf-novel

# Kohärenz-Protokoll migrieren:
bash scripts/bootstrap_project.sh kohaerenz-protokoll

# Skill packen (Checkpoint):
bash scripts/package_skill.sh
```

## Permissions

`bootstrap_project.sh` und `package_skill.sh` müssen ausführbar sein:

```bash
chmod +x scripts/bootstrap_project.sh scripts/package_skill.sh
```
