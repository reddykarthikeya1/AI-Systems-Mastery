"""DEBUG LAB: Sequential Scan on 5,000,000 JSONB Document Catalog

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class DocumentStore:
    """A toy catalog with a GIN-style containment index alongside the rows."""

    def __init__(self) -> None:
        self.docs: list[tuple[int, dict]] = []
        self.gin_index: dict[tuple[str, str], set[int]] = {}

    def insert(self, doc_id: int, data: dict) -> None:
        self.docs.append((doc_id, data))
        for key, value in data.items():
            self.gin_index.setdefault((key, value), set()).add(doc_id)

    def query_text_extract_eq(self, key: str, value: str) -> tuple[list[int], int]:
        """Simulates `data->>'key' = 'value'`, which the GIN index cannot serve."""
        matches, scanned = [], 0
        for doc_id, data in self.docs:
            scanned += 1
            if str(data.get(key)) == value:
                matches.append(doc_id)
        return matches, scanned

    def query_containment(self, key: str, value: str) -> tuple[list[int], int]:
        """Simulates `data @> '{"key": "value"}'::jsonb`, served by gin_index."""
        ids = self.gin_index.get((key, value), set())
        return sorted(ids), len(ids)

def reproduce_defect() -> None:
    print("Filtering a 5,000-document catalog for status = 'active'...")
    store = DocumentStore()
    for doc_id in range(5000):
        status = "active" if doc_id % 1250 == 0 else "inactive"
        store.insert(doc_id, {"status": status})

    _, scanned_via_operator = store.query_text_extract_eq("status", "active")
    matches_via_index, scanned_via_index = store.query_containment("status", "active")

    print(f"Rows scanned via data->>'status' = 'active': {scanned_via_operator}")
    print(f"Rows scanned via GIN containment index:      {scanned_via_index} "
          f"(matches: {len(matches_via_index)})")
    if scanned_via_operator > scanned_via_index * 10:
        print("[DEFECT OBSERVED] The query touched every row in the catalog instead "
              "of the handful the GIN index could have returned directly.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
