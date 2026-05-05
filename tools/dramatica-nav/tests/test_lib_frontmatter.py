"""Unit tests for lib/frontmatter.py."""
from __future__ import annotations

from lib import frontmatter


def test_extract_blocks_valid():
    text = """## Trust

<!-- nav-ontology (auto-managed; see maintenance/schemas/narrative-ontology/) -->
```yaml
id: el.trust
kind: element
canonical_label: Trust
provenance: source-original
```

Some prose follows.
"""
    blocks = frontmatter.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0]["id"] == "el.trust"
    assert blocks[0]["kind"] == "element"


def test_extract_blocks_empty_when_no_marker():
    text = "## Trust\n\nJust prose, no nav-ontology block here.\n"
    assert frontmatter.extract_blocks(text) == []


def test_walk_vocab_blocks_count(repo_root):
    """Confirm 187 per-term blocks land — matches Step 5 commit."""
    blocks = list(frontmatter.walk_vocab_blocks(repo_root))
    assert len(blocks) == 187, f"expected 187 blocks per Step 5; found {len(blocks)}"


def test_slugify_variants():
    # paren-stripping form
    assert frontmatter.slugify("Direction (Overall Story Throughline)") == "direction"
    assert frontmatter.slugify("Trust") == "trust"
    assert frontmatter.slugify("Self-Interest") == "self-interest"
    # paren-keeping form (GitHub anchor algorithm)
    assert (
        frontmatter.slugify_keep_parens("Direction (Overall Story Throughline)")
        == "direction-overall-story-throughline"
    )
    assert frontmatter.slugify_keep_parens("Trust") == "trust"
