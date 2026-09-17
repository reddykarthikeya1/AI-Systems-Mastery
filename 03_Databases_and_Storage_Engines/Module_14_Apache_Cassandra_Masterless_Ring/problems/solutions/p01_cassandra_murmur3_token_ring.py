"""Reference Solution — Problem 01: Cassandra Murmur3 Token Ring

Topic: 14 Apache Cassandra Masterless Ring
"""

from __future__ import annotations


def cassandra_murmur3_token_ring(ring: list[tuple[int, str]], key_token: int, replication_factor: int = 3) -> list[str]:
    if not ring:
        return []
    n = len(ring)
    idx = 0
    while idx < n and ring[idx][0] < key_token:
        idx += 1
    if idx == n:
        idx = 0
    replicas = []
    curr = idx
    while len(replicas) < min(replication_factor, len(set(x[1] for x in ring))):
        node = ring[curr][1]
        if node not in replicas:
            replicas.append(node)
        curr = (curr + 1) % n
    return replicas
