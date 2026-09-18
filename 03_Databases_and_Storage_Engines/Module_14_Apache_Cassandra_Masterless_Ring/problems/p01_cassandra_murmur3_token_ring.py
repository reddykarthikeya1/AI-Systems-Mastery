"""Problem 01 — Cassandra Murmur3 Token Ring

Topic: 14 Apache Cassandra Masterless Ring
Target: Production-grade implementation

Find replica node IDs for key using token ring and replication factor RF.

Example:
    >>> ring = [(100, "nodeA"), (200, "nodeB"), (300, "nodeC"), (400, "nodeD")]
    >>> cassandra_murmur3_token_ring(ring, 150, 3)
    ['nodeB', 'nodeC', 'nodeD']

Hints:
    Hint 1: The ring is circular, not linear — after finding the key's home
        position you keep walking clockwise past the highest token straight
        back around to the lowest one, exactly like a clock face.
    Hint 2: First find the "coordinator" position with a forward scan for
        the first token >= key_token (or ring[0] if key_token is past every
        token — that's the wraparound case), then walk forward with modulo
        arithmetic collecting node_ids into a list, skipping ones already
        collected.
    Hint 3: Replication factor counts distinct nodes, not distinct ring
        entries — a real ring often has several tokens (vnodes) per
        physical node, so you must dedupe by node_id while walking and stop
        once you have replication_factor unique nodes (or fewer, if the
        ring has fewer than RF distinct nodes total); an empty ring must
        return [] rather than raising.
"""

from __future__ import annotations


def cassandra_murmur3_token_ring(ring: list[tuple[int, str]], key_token: int, replication_factor: int = 3) -> list[str]:
    """Ring is a list of (token, node_id) sorted by token ascending.
    Find first node whose token >= key_token (wraparound to ring[0] if key_token > all tokens).
    Then select distinct nodes in clockwise order until replication_factor unique nodes are found.
    Returns list of node_ids.
    """
    raise NotImplementedError("Implement cassandra_murmur3_token_ring")
