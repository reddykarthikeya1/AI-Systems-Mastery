"""Reference Solution — Problem 01: Consistent Hash Ring Vnodes

Topic: 09 Consistent Hashing Distributed Partitioning
"""

from __future__ import annotations


def consistent_hash_ring_vnodes(nodes: list[str], vnodes_per_node: int, key: str) -> str:
    import hashlib
    def h(s: str) -> int:
        return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
    
    ring = []
    for node in sorted(nodes):
        for v in range(vnodes_per_node):
            ring.append((h(f"{node}#v{v}"), node))
    ring.sort()
    
    key_h = h(key)
    for vh, node in ring:
        if vh >= key_h:
            return node
    return ring[0][1]
