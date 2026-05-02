import re
import sys

def test_spec():
    with open('research/obsidian-frontmatter-agentic-spec/output/SPEC.md', 'r') as f:
        content = f.read()

    required_sections = [
        "## Executive Summary",
        "## Hypothesenbaum",
        "## Metadaten-Ebenen-Matrix",
        "### L0 — Obsidian Default",
        "### L1 — Vault Core (Pflicht)",
        "### L2 — Domain Extension Namespacing",
        "### L3 — Agent-Only",
        "## Expansion-Pattern-Spec",
        "## Plugin-Linkliste",
        "## Ontologie-Mapping-Guide",
        "## Synthesis — Spec-Grundlage für Python-Script",
        "## Contradiction Log",
        "## Hypothesis Half-Life Audit",
        "## Query Expansion Log",
        "## Reflection History",
        "## Open Questions / Unresolved",
        "## Sources",
        "## Methodology Note"
    ]

    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    if missing:
        print("Test failed. Missing sections:")
        for m in missing:
            print(m)
        sys.exit(1)

    print("All required sections are present in SPEC.md.")

if __name__ == "__main__":
    test_spec()
