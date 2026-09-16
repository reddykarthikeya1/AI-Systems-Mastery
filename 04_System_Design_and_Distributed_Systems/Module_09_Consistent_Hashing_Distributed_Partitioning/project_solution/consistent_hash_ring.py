#!/usr/bin/env python3
"""Module 09: In-Process Architectural Simulation Model: Consistent Hash Ring with Virtual Nodes.

Used by distributed databases (Amazon DynamoDB, Apache Cassandra) and caches
(Memcached, Redis clusters) for horizontal partitioning and replica placement.
"""

from __future__ import annotations

import bisect
import hashlib
import math
from collections import defaultdict
from collections.abc import Iterable


class ConsistentHashRing:
    """Consistent Hash Ring with virtual nodes (vnodes) and replica preference lists."""

    def __init__(self, nodes: Iterable[str] | None = None, vnodes: int = 150) -> None:
        self.vnodes = vnodes
        # Sorted list of 32-bit token hashes representing points on the ring
        self.ring: list[int] = []
        # Mapping from token hash -> physical node id
        self.ring_map: dict[int, str] = {}
        # Set of active physical node ids
        self.physical_nodes: set[str] = set()

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        """Computes a 32-bit integer token using SHA-256."""
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return int(digest[:8], 16)

    def add_node(self, node_id: str) -> None:
        """Adds a physical node and places its virtual nodes across the ring."""
        if node_id in self.physical_nodes:
            return

        self.physical_nodes.add(node_id)
        for i in range(self.vnodes):
            vnode_token = self._hash(f"{node_id}#vnode_{i}")
            # Insert token maintaining sorted order in self.ring
            idx = bisect.bisect_left(self.ring, vnode_token)
            self.ring.insert(idx, vnode_token)
            self.ring_map[vnode_token] = node_id

    def remove_node(self, node_id: str) -> None:
        """Removes a physical node and purges all of its virtual node tokens."""
        if node_id not in self.physical_nodes:
            return

        self.physical_nodes.remove(node_id)
        tokens_to_remove = set()
        for i in range(self.vnodes):
            vnode_token = self._hash(f"{node_id}#vnode_{i}")
            tokens_to_remove.add(vnode_token)

        self.ring = [t for t in self.ring if t not in tokens_to_remove]
        for t in tokens_to_remove:
            self.ring_map.pop(t, None)

    def get_node(self, key: str) -> str | None:
        """Maps a key to its primary coordinator physical node on the ring."""
        if not self.ring:
            return None

        key_token = self._hash(key)
        idx = bisect.bisect_right(self.ring, key_token)

        # Ring wrap-around: if key_token > all tokens on the ring, wrap to index 0
        if idx == len(self.ring):
            idx = 0

        chosen_token = self.ring[idx]
        return self.ring_map[chosen_token]

    def get_preference_list(self, key: str, count: int) -> list[str]:
        """Returns `count` distinct physical nodes (replicas) clockwise from the key.

        Essential for distributed replication (N replicas per key in Dynamo).
        """
        if not self.ring:
            return []

        key_token = self._hash(key)
        start_idx = bisect.bisect_right(self.ring, key_token)

        selected_nodes: list[str] = []
        ring_len = len(self.ring)

        # Traverse ring clockwise until we have `count` distinct physical nodes
        for i in range(ring_len):
            curr_idx = (start_idx + i) % ring_len
            physical_node = self.ring_map[self.ring[curr_idx]]
            if physical_node not in selected_nodes:
                selected_nodes.append(physical_node)
                if len(selected_nodes) == min(count, len(self.physical_nodes)):
                    break

        return selected_nodes

    def get_distribution_stats(self, keys: list[str]) -> dict[str, float]:
        """Calculates key allocation counts and standard deviation across physical nodes."""
        if not self.physical_nodes:
            return {}

        counts: dict[str, int] = defaultdict(int)
        for node in self.physical_nodes:
            counts[node] = 0

        for k in keys:
            node = self.get_node(k)
            if node:
                counts[node] += 1

        total_keys = len(keys)
        expected = total_keys / len(self.physical_nodes)
        variance = sum((c - expected) ** 2 for c in counts.values()) / len(self.physical_nodes)
        std_dev = math.sqrt(variance)

        return {
            "total_keys": total_keys,
            "expected_per_node": expected,
            "std_dev": std_dev,
            "std_dev_ratio": (std_dev / expected) if expected > 0 else 0.0,
            **{f"node_{n}": count for n, count in counts.items()},
        }
