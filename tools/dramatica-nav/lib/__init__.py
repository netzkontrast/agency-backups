"""Shared library for the dramatica-nav navigator suite.

Three modules:
- frontmatter: extract embedded YAML blocks from per-term markdown
- ontology:    load + index ontology.json (7 lookup methods)
- ncp_bridge:  load NCP enum closure set from pinned upstream schema

Library functions raise typed exceptions; CLI scripts catch them and
emit structured stderr + non-zero exit. stdout is reserved for data.
"""


class OntologyError(Exception):
    """Base error for all dramatica-nav library failures."""


class LookupNotFoundError(OntologyError):
    """Raised when a query resolves to no matching ontology entry."""


class ValidationError(OntologyError):
    """Raised when a structural invariant is violated."""
