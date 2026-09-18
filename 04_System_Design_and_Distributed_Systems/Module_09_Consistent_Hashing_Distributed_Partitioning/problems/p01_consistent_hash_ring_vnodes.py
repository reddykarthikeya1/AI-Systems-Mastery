"""Problem 01 — Consistent Hash Ring Vnodes

Topic: 09 Consistent Hashing Distributed Partitioning
Target: Production-grade implementation

Map keys to node IDs using consistent hash ring with virtual nodes.

Example:
    >>> consistent_hash_ring_vnodes(['server_a', 'server_b', 'server_c'], 5, 'user:12345')
    'server_a'

Hints:
    Hint 1: Each physical node needs several positions on the ring
        (virtual nodes) so load spreads evenly instead of being skewed by
        a single hash point per node.
    Hint 2: Build a sorted list of (hash, node) pairs for every
        `"{node}#v{i}"` virtual-node label, then scan for the first ring
        entry whose hash is >= hash(key).
    Hint 3: If the key's hash is larger than every virtual node's hash,
        you must wrap around to `ring[0]` rather than return nothing; use
        a stable hash (e.g. an int derived from an md5 hex digest, not
        Python's salted `hash()`) so the same key always maps to the same
        node across calls.
"""

from __future__ import annotations


def consistent_hash_ring_vnodes(nodes: list[str], vnodes_per_node: int, key: str) -> str:
    """Hash virtual node format: f"{node}#v{i}" using hash() or fnv1a.
    Find the first virtual node whose hash >= hash(key) in ring (wraparound to ring[0]).
    Return base node id.
    """
    raise NotImplementedError("Implement consistent_hash_ring_vnodes")
