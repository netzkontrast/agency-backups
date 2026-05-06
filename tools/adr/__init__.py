"""agency-adr — repo-native ADR governance tooling.

Spec: research/adr-spec-research-synthesis/output/SPEC.md (anchor ADR.A.5.x).
Implementation plan: tasks/028-adr-tooling-impl-plan/implementation-plan.md.

Public sub-commands are exposed via tools/adr/cli.py:

    python3 tools/adr/cli.py validate [PATH ...]
    python3 tools/adr/cli.py synthesize [--token-limit N] [--fidelity-floor F] ...

Submodules:
    schema, body, corpus, graph, ids, extract, compress, fidelity,
    synthesize, runlog, cli.
"""
from __future__ import annotations
