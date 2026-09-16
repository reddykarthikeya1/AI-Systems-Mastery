from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class GraphEntity:
    name: str
    entity_type: str
    description: str


@dataclasses.dataclass
class GraphRelationship:
    source: str
    target: str
    description: str


@dataclasses.dataclass
class CommunityReport:
    community_id: int
    title: str
    summary: str
    entities: list[str]


class SimpleGraphRAGEngine:
    """Simulates Microsoft GraphRAG entity graph construction and community summarization."""

    def __init__(self):
        self.entities: dict[str, GraphEntity] = {}
        self.relationships: list[GraphRelationship] = []
        self.communities: dict[int, CommunityReport] = {}

    def add_entity(self, name: str, entity_type: str, description: str) -> None:
        self.entities[name] = GraphEntity(name=name, entity_type=entity_type, description=description)

    def add_relationship(self, source: str, target: str, description: str) -> None:
        self.relationships.append(GraphRelationship(source=source, target=target, description=description))

    def build_communities_and_reports(self) -> list[CommunityReport]:
        """Clusters entities into communities based on connectivity and builds summary reports."""
        # Simple connected component clustering simulation
        visited = set()
        adj: dict[str, set[str]] = {e: set() for e in self.entities}
        for rel in self.relationships:
            if rel.source in adj and rel.target in adj:
                adj[rel.source].add(rel.target)
                adj[rel.target].add(rel.source)

        community_list = []
        c_id = 1

        for ent_name in self.entities:
            if ent_name not in visited:
                # BFS to find component
                cluster = []
                queue = [ent_name]
                visited.add(ent_name)
                while queue:
                    curr = queue.pop(0)
                    cluster.append(curr)
                    for neighbor in adj.get(curr, set()):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                # Generate community summary report
                report = CommunityReport(
                    community_id=c_id,
                    title=f"Cluster {c_id}: {', '.join(cluster[:3])}",
                    summary=f"Community focusing on {len(cluster)} entities including {cluster[0]}.",
                    entities=cluster,
                )
                self.communities[c_id] = report
                community_list.append(report)
                c_id += 1

        return community_list

    def global_search(self, query: str) -> str:
        """Executes a global Map-Reduce search over community reports."""
        if not self.communities:
            return "No communities indexed."

        summaries = [f"- {rep.title}: {rep.summary}" for rep in self.communities.values()]
        return "Global Intelligence Summary:\n" + "\n".join(summaries)
