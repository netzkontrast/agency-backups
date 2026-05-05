"""Load + index ontology.json. Provides 7 lookup methods.

Indexes are built once at construction time. Subsequent queries are O(1)
(dict lookup) or O(N) where N is the small per-key bucket size.

Lookup methods (all returning typed records or None):
    by_id(id)                    → entry or raises LookupNotFoundError
    by_alias(alias, locale="en") → entry or raises LookupNotFoundError
    by_scenario(sid, kind=None)  → list[entry] (possibly empty)
    by_quad(quad_id)             → list[entry] (the quad's members)
    by_ktad(position)            → list[entry] (all entries at this KTAD position)
    by_ncp(appreciation)         → list[entry] (entries mapping to this NCP enum)
    by_pair(member_id)           → list[entry] (the dp.* entries containing member)
    pair_partner(member_id)      → entry or None (the partner via dynamic_pair_id)
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional

from . import LookupNotFoundError, OntologyError


class OntologyIndex:
    """In-memory ontology with prebuilt lookup indexes."""

    def __init__(self, ontology_path: Path):
        self.path = ontology_path
        try:
            data = json.loads(ontology_path.read_text())
        except FileNotFoundError as e:
            raise OntologyError(f"ontology.json not found at {ontology_path}") from e
        except json.JSONDecodeError as e:
            raise OntologyError(f"ontology.json malformed: {e}") from e

        self.schema_version = data.get("schema_version", "unknown")
        self.ontology_version = data.get("ontology_version", "unknown")
        self.entries: list[dict] = data.get("entries", [])

        self._build_indexes()

    def _build_indexes(self) -> None:
        self._by_id: dict[str, dict] = {}
        self._by_alias: dict[str, dict[str, dict]] = defaultdict(dict)
        self._by_scenario: dict[str, list[dict]] = defaultdict(list)
        self._by_quad: dict[str, list[dict]] = defaultdict(list)
        self._by_ktad: dict[str, list[dict]] = defaultdict(list)
        self._by_ncp: dict[str, list[dict]] = defaultdict(list)
        self._by_pair_member: dict[str, list[dict]] = defaultdict(list)

        for e in self.entries:
            if "id" not in e:
                continue
            self._by_id[e["id"]] = e

            for k, v in e.items():
                if k.startswith("aliases_") and isinstance(v, list):
                    locale = k[len("aliases_"):]
                    for alias in v:
                        self._by_alias[locale][alias.lower()] = e
                elif k.startswith("deprecated_aliases_") and isinstance(v, list):
                    locale = k[len("deprecated_aliases_"):]
                    for alias in v:
                        self._by_alias[locale][alias.lower()] = e

            # canonical_label is also a queryable alias in every locale
            label = e.get("canonical_label")
            if label:
                # Make canonical findable in every known locale even if not listed
                self._by_alias["en"].setdefault(label.lower(), e)

            for s in e.get("scenarios", []) or []:
                self._by_scenario[s].append(e)

            qid = e.get("quad_id")
            if qid:
                self._by_quad[qid].append(e)

            ktad = e.get("ktad_position")
            if ktad:
                self._by_ktad[ktad].append(e)

            ncp = e.get("ncp_appreciation")
            if ncp:
                self._by_ncp[ncp].append(e)

            if e.get("kind") == "dynamic-pair":
                a = e.get("pair_member_a")
                b = e.get("pair_member_b")
                if a:
                    self._by_pair_member[a].append(e)
                if b:
                    self._by_pair_member[b].append(e)

    # ---- public lookup methods ----

    def by_id(self, entry_id: str) -> dict:
        try:
            return self._by_id[entry_id]
        except KeyError as e:
            raise LookupNotFoundError(f"no ontology entry with id={entry_id!r}") from e

    def by_alias(self, alias: str, locale: str = "en") -> dict:
        bucket = self._by_alias.get(locale, {})
        hit = bucket.get(alias.lower())
        if hit is None:
            raise LookupNotFoundError(
                f"no ontology entry with alias={alias!r} in locale={locale!r}"
            )
        return hit

    def by_scenario(self, scenario_id: str, kind: Optional[str] = None) -> list[dict]:
        results = list(self._by_scenario.get(scenario_id, []))
        if kind is not None:
            results = [e for e in results if e.get("kind") == kind]
        return results

    def by_quad(self, quad_id: str) -> list[dict]:
        return list(self._by_quad.get(quad_id, []))

    def by_ktad(self, position: str) -> list[dict]:
        return list(self._by_ktad.get(position.upper(), []))

    def by_ncp(self, appreciation: str) -> list[dict]:
        return list(self._by_ncp.get(appreciation, []))

    def by_pair(self, member_id: str) -> list[dict]:
        """Return dp.* entries that contain member_id as pair_member_a or _b."""
        return list(self._by_pair_member.get(member_id, []))

    def pair_partner(self, member_id: str) -> Optional[dict]:
        """Return the partner entry via the member's dynamic_pair_id field, if any."""
        member = self._by_id.get(member_id)
        if member is None:
            return None
        partner_id = member.get("dynamic_pair_id")
        return self._by_id.get(partner_id) if partner_id else None

    # ---- enumeration helpers ----

    def all_ids(self) -> set[str]:
        return set(self._by_id.keys())

    def by_kind(self, kind: str) -> list[dict]:
        return [e for e in self.entries if e.get("kind") == kind]

    def all_scenarios(self) -> Iterable[str]:
        return self._by_scenario.keys()


# Convenience factory
def load(ontology_path: Optional[Path] = None) -> OntologyIndex:
    if ontology_path is None:
        # default: relative to this file
        here = Path(__file__).resolve()
        # tools/dramatica-nav/lib/ontology.py → repo root → maintenance/...
        repo_root = here.parents[3]
        ontology_path = repo_root / "maintenance" / "schemas" / "narrative-ontology" / "ontology.json"
    return OntologyIndex(ontology_path)
