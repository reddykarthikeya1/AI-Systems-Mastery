"""Problem 01 — Cassandra Murmur3 Token Ring

Topic: 14 Apache Cassandra Masterless Ring
Target: Production-grade implementation

Find replica node IDs for key using token ring and replication factor RF.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def cassandra_murmur3_token_ring(ring: list[tuple[int, str]], key_token: int, replication_factor: int = 3) -> list[str]:
    """Ring is a list of (token, node_id) sorted by token ascending.
    Find first node whose token >= key_token (wraparound to ring[0] if key_token > all tokens).
    Then select distinct nodes in clockwise order until replication_factor unique nodes are found.
    Returns list of node_ids.
    """
    raise NotImplementedError("Implement cassandra_murmur3_token_ring")
