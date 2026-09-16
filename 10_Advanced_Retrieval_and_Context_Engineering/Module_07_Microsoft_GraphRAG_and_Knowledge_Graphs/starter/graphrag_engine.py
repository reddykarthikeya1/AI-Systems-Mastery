from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class CommunityReport:
    community_id: int
    title: str
    summary: str
    entities: list[str]


class SimpleGraphRAGEngine:
    def __init__(self):
        raise NotImplementedError("Implement SimpleGraphRAGEngine")

    def add_entity(self, name: str, entity_type: str, description: str) -> None:
        raise NotImplementedError("Implement add_entity")

    def add_relationship(self, source: str, target: str, description: str) -> None:
        raise NotImplementedError("Implement add_relationship")

    def build_communities_and_reports(self) -> list[CommunityReport]:
        raise NotImplementedError("Implement build_communities_and_reports")

    def global_search(self, query: str) -> str:
        raise NotImplementedError("Implement global_search")
