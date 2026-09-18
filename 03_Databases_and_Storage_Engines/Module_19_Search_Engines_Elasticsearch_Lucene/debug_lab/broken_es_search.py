"""DEBUG LAB: Deep Pagination Offset Crashes Elasticsearch Data Nodes

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class SearchCluster:
    """A toy search cluster. The coordinator merges each shard's page before
    trimming it down to the requested `size`."""

    def __init__(self, num_shards: int) -> None:
        self.num_shards = num_shards

    def deep_page_naive(self, from_: int, size: int) -> int:
        """Every shard must sort and return `from_ + size` docs to the
        coordinator, which then holds num_shards * (from_ + size) in heap."""
        docs_per_shard = from_ + size
        return docs_per_shard * self.num_shards

    def search_after(self, size: int) -> int:
        """A cursor-based scan only ever asks each shard for `size` docs."""
        return size * self.num_shards

def reproduce_defect() -> None:
    print("Fetching page 1,001 (from=50000, size=50) across a 20-shard index...")
    cluster = SearchCluster(num_shards=20)

    naive_heap_docs = cluster.deep_page_naive(from_=50000, size=50)
    cursor_heap_docs = cluster.search_after(size=50)

    print(f"Docs the coordinator must hold with from/size pagination: {naive_heap_docs:,}")
    print(f"Docs the coordinator would hold with a search_after cursor: {cursor_heap_docs:,}")
    if naive_heap_docs > cursor_heap_docs * 100:
        print("[DEFECT OBSERVED] Paginating with a 50,000-row offset forces the "
              "coordinator to sort and hold over a million documents in heap "
              "just to return the final 50.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
