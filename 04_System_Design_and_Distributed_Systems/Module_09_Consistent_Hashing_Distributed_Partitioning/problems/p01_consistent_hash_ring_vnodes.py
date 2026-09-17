"""Problem 01 — Consistent Hash Ring Vnodes

Topic: 09 Consistent Hashing Distributed Partitioning
Target: Production-grade implementation

Map keys to node IDs using consistent hash ring with virtual nodes.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def consistent_hash_ring_vnodes(nodes: list[str], vnodes_per_node: int, key: str) -> str:
    """Hash virtual node format: f"{node}#v{i}" using hash() or fnv1a.
    Find the first virtual node whose hash >= hash(key) in ring (wraparound to ring[0]).
    Return base node id.
    """
    raise NotImplementedError("Implement consistent_hash_ring_vnodes")
