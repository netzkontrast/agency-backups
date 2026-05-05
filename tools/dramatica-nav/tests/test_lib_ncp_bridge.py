"""Unit tests for lib/ncp_bridge."""
from __future__ import annotations

from lib import ncp_bridge


def test_load_returns_union_of_all_enums(repo_root):
    """Per kickoff SPEC §2.5, ncp_appreciation references three enum surfaces:
    canonical_appreciation (463) + canonical_narrative_function (144) + throughline (4).
    Total ≥ 611 (potentially less due to deduplication where Approach appears in both
    canonical_narrative_function AND in the dynamic kind enum)."""
    enums = ncp_bridge.load_ncp_appreciations(repo_root)
    # Expect ≥ 600 (allowing for some deduplication overlap)
    assert len(enums) >= 600
    # Spot-check throughline values are present (the inline-buried enum)
    for tl in ("Main Character", "Influence Character", "Objective Story", "Relationship Story"):
        assert tl in enums, f"throughline enum value {tl!r} missing from union"


def test_is_valid_appreciation_smoke(repo_root):
    """Spot-check a known-valid + a known-invalid appreciation."""
    enums = ncp_bridge.load_ncp_appreciations(repo_root)
    assert ncp_bridge.is_valid_appreciation("Relationship Story", enums)
    assert not ncp_bridge.is_valid_appreciation("ZzzClearlyBogusValue", enums)
