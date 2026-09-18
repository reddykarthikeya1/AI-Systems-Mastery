"""DEBUG LAB: Cartesian Product OutOfMemoryError in Cypher Path Match

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class GraphDB:
    """A toy graph: Person and Company nodes, plus real WORKS_AT relationships."""

    def __init__(self) -> None:
        self.persons: list[dict] = []
        self.companies: list[dict] = []
        self.works_at: set[tuple[int, int]] = set()

    def match_missing_relationship(self) -> list[tuple[int, int]]:
        """MATCH (a:Person), (b:Company) WHERE a.city = b.city -- no edge pattern
        joins the two label scans, so every person is paired with every company."""
        return [
            (p["id"], c["id"])
            for p in self.persons
            for c in self.companies
            if p["city"] == c["city"]
        ]

    def match_with_relationship(self) -> list[tuple[int, int]]:
        """MATCH (a:Person)-[:WORKS_AT]->(b:Company) WHERE a.city = b.city"""
        by_id_p = {p["id"]: p for p in self.persons}
        by_id_c = {c["id"]: c for c in self.companies}
        return [
            (pid, cid)
            for pid, cid in self.works_at
            if by_id_p[pid]["city"] == by_id_c[cid]["city"]
        ]

def reproduce_defect() -> None:
    print("Matching people and companies in the same city, 300 of each...")
    graph = GraphDB()
    for i in range(300):
        graph.persons.append({"id": i, "city": "Metropolis"})
        graph.companies.append({"id": i, "city": "Metropolis"})
    for i in range(50):
        graph.works_at.add((i, i))  # only 50 real employment relationships exist

    cartesian_pairs = graph.match_missing_relationship()
    real_pairs = graph.match_with_relationship()

    print(f"Rows returned without a relationship pattern: {len(cartesian_pairs)}")
    print(f"Rows returned via the real WORKS_AT relationship: {len(real_pairs)}")
    if len(cartesian_pairs) > len(real_pairs) * 100:
        print("[DEFECT OBSERVED] The missing relationship pattern forces a 300x300 "
              "Cartesian product in memory instead of following 50 real edges.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
