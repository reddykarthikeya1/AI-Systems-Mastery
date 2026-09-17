"""Problem 01 — Skip List Probabilistic Index

Topic: 21 Vector Database HNSW Index Milvus
Target: Production-grade implementation

Probabilistic layered skip list search returning target value node.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def skip_list_probabilistic_index(layers: list[dict[int, int]], target: int) -> int | None:
    """layers: list of dicts mapping key -> next_key in that layer, from top layer to bottom layer 0.
    Start at top layer, walk forward while next_key <= target. Drop to next layer when blocked.
    Returns target if found at bottom layer, else None.
    """
    raise NotImplementedError("Implement skip_list_probabilistic_index")
