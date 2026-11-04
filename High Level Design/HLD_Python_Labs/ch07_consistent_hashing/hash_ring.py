"""Consistent Hashing with Virtual Nodes and Google Bounded Loads Algorithm.

Key Architectural Concepts:
---------------------------
1. Virtual Nodes (vnodes):
   Distributes multiple hash tokens per physical server (e.g. 150 vnodes)
   around the integer ring [0, 2^128 - 1] to minimize variance and achieve
   uniform statistical key distribution.

2. Deterministic & Collision-Free Hashing:
   Uses cryptographic digests (SHA-256 or MD5) generating 128-bit integer tokens.
   Never relies on Python's built-in `hash()` which has randomized per-process seeds
   (PYTHONHASHSEED). In the extraordinarily rare event of a 128-bit token collision,
   tokens are deterministically re-hashed using incremental salting.

3. Clockwise Lookup via Binary Search:
   Given key hash `h`, finds the smallest token >= `h` using bisect_right.
   If `h` exceeds all tokens, wraps around clockwise to token 0.

4. Preference List (Replica Placement):
   Retrieves the top N distinct physical nodes encountering tokens clockwise.
   Guarantees all returned nodes represent separate physical fault domains.

5. Google Bounded Load Algorithm (Mirrokni, Thorup, Zadimoghaddam - SODA 2018):
   Standard consistent hashing can suffer from severe hot-spotting when a popular
   key or shard attracts massive traffic, cascading overload upon node failure.
   Bounded load enforces:
       max_node_load = ceil(c * (total_load / N))   where c >= 1.0 (typically 1.25 - 1.30)
   If the preferred primary node is at capacity, the algorithm walks clockwise to the next
   available distinct physical node on the ring.
   
   Production Implementation vs. Academic Paper:
   - Paper formalization: In an online stream of M requests over N nodes with capacity
     parameter c = 1 + epsilon, the algorithm guarantees maximum load on any bin is at most
     ceil(c * M / N) while maintaining minimal key migration under node joins/leaves.
   - Production systems (e.g. Google Cloud CDN, Vimeo cache proxies): Total load M is dynamically
     tracked via active concurrent connections or rolling-window request rate counters.
     When a node reaches its dynamic capacity threshold max(1, ceil(c * avg_load)), requests
     spill over clockwise to the next node on the ring.
"""

from __future__ import annotations
import bisect
import hashlib
import math
from typing import Callable, Dict, List, Optional, Set, Tuple


def _sha256_hasher(key: str) -> int:
    """Deterministic 128-bit integer hash from SHA-256."""
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:32], 16)


def _md5_hasher(key: str) -> int:
    """Deterministic 128-bit integer hash from MD5."""
    return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:32], 16)


class ConsistentHashRing:
    """Consistent Hash Ring with configurable vnodes and deterministic hashing."""

    def __init__(
        self,
        nodes: Optional[List[str]] = None,
        vnodes: int = 150,
        hash_algo: str = "sha256",
    ) -> None:
        if vnodes <= 0:
            raise ValueError("vnodes must be greater than 0")

        self.vnodes = vnodes
        self._hasher: Callable[[str], int] = (
            _md5_hasher if hash_algo.lower() == "md5" else _sha256_hasher
        )
        self.ring_tokens: List[int] = []
        self.token_to_node: Dict[int, str] = {}
        self.physical_nodes: Set[str] = set()

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, val: str) -> int:
        return self._hasher(val)

    def add_node(self, node: str) -> None:
        """Add a physical node and its virtual tokens to the ring idempotently.

        Collisions are detected and resolved via deterministic salt probing.
        """
        if node in self.physical_nodes:
            # Idempotent: already present
            return

        self.physical_nodes.add(node)
        for v in range(self.vnodes):
            salt = 0
            while True:
                suffix = f"#vn_{v}" if salt == 0 else f"#vn_{v}#salt_{salt}"
                token = self._hash(f"{node}{suffix}")
                if token not in self.token_to_node:
                    break
                salt += 1

            self.ring_tokens.append(token)
            self.token_to_node[token] = node

        self.ring_tokens.sort()

    def remove_node(self, node: str) -> None:
        """Remove a physical node and all associated virtual tokens idempotently."""
        if node not in self.physical_nodes:
            return

        self.physical_nodes.remove(node)
        tokens_to_remove = [t for t, n in self.token_to_node.items() if n == node]
        for t in tokens_to_remove:
            self.token_to_node.pop(t, None)

        tokens_to_remove_set = set(tokens_to_remove)
        self.ring_tokens = [t for t in self.ring_tokens if t not in tokens_to_remove_set]

    def get_node(self, key: str) -> Optional[str]:
        """Lookup the physical node responsible for a given key."""
        if not self.ring_tokens:
            return None
        key_hash = self._hash(key)
        idx = bisect.bisect_right(self.ring_tokens, key_hash)
        if idx == len(self.ring_tokens):
            idx = 0
        token = self.ring_tokens[idx]
        return self.token_to_node[token]

    def get_preference_list(self, key: str, n: int) -> List[str]:
        """Return the top N distinct physical nodes clockwise on the ring (for replication).

        Guarantees that all returned nodes are distinct physical nodes.
        If n > total physical nodes, returns all available distinct nodes.
        """
        if not self.ring_tokens or n <= 0 or not self.physical_nodes:
            return []

        key_hash = self._hash(key)
        start_idx = bisect.bisect_right(self.ring_tokens, key_hash)
        total_tokens = len(self.ring_tokens)
        preference: List[str] = []
        visited_nodes: Set[str] = set()

        for step in range(total_tokens):
            idx = (start_idx + step) % total_tokens
            node = self.token_to_node[self.ring_tokens[idx]]
            if node not in visited_nodes:
                visited_nodes.add(node)
                preference.append(node)
                if len(preference) == n or len(visited_nodes) == len(self.physical_nodes):
                    break

        return preference

    def analyze_redistribution(
        self, test_keys: List[str], new_node: str
    ) -> Dict[str, float]:
        """Calculates fraction of keys migrated when a new node joins."""
        if not self.physical_nodes:
            return {"migrated_fraction": 0.0, "total_keys": float(len(test_keys))}

        initial_mapping = {k: self.get_node(k) for k in test_keys}
        self.add_node(new_node)
        new_mapping = {k: self.get_node(k) for k in test_keys}

        migrated = sum(1 for k in test_keys if initial_mapping[k] != new_mapping[k])
        fraction = migrated / len(test_keys) if test_keys else 0.0

        # Roll back node addition to maintain pure analysis state
        self.remove_node(new_node)

        return {
            "migrated_keys": float(migrated),
            "total_keys": float(len(test_keys)),
            "migrated_fraction": fraction,
            "theoretical_ideal": 1.0 / (len(self.physical_nodes) + 1),
        }


class BoundedLoadHashRing(ConsistentHashRing):
    """Google Bounded-Load Consistent Hashing (Mirrokni et al., SODA 2018).

    Guarantees no physical node serves more than:
        max_load = max(1, ceil(c * (total_load / N)))
    where c is the load factor (e.g. 1.25), preventing cascading hot-spot failures.

    Comparison to Google Production Paper:
    --------------------------------------
    In Mirrokni et al., each item x is allocated dynamically to the first node clockwise
    along the ring whose current load does not exceed ceil(c * average_load).
    In this implementation:
    - Active load is tracked dynamically per physical node.
    - When `assign_key` is called, the primary hash token's node is inspected.
    - If that node has reached `get_max_allowed_load()`, we advance clockwise across distinct
      physical nodes until an available node is found.
    - If all nodes are saturated, we assign to the node with the minimum current load as fallback.
    - `release_load` decrements the load counter upon request completion.
    """

    def __init__(
        self,
        nodes: Optional[List[str]] = None,
        vnodes: int = 150,
        load_factor: float = 1.25,
        hash_algo: str = "sha256",
    ) -> None:
        if load_factor < 1.0:
            raise ValueError("load_factor c must be >= 1.0")
        self.load_factor = load_factor
        self.node_loads: Dict[str, int] = {}
        super().__init__(nodes=nodes, vnodes=vnodes, hash_algo=hash_algo)

    def add_node(self, node: str) -> None:
        super().add_node(node)
        if node not in self.node_loads:
            self.node_loads[node] = 0

    def remove_node(self, node: str) -> None:
        super().remove_node(node)
        self.node_loads.pop(node, None)

    @property
    def total_load(self) -> int:
        return sum(self.node_loads.values())

    def get_max_allowed_load(self) -> int:
        n = len(self.physical_nodes)
        if n == 0:
            return 0
        avg_load = self.total_load / n
        return max(1, math.ceil(self.load_factor * avg_load))

    def assign_key(self, key: str) -> Optional[str]:
        """Assign key to the clockwise node that has not reached capacity."""
        if not self.ring_tokens:
            return None

        key_hash = self._hash(key)
        start_idx = bisect.bisect_right(self.ring_tokens, key_hash)
        total_tokens = len(self.ring_tokens)
        max_allowed = self.get_max_allowed_load()

        seen_nodes: Set[str] = set()
        chosen_node: Optional[str] = None

        for step in range(total_tokens):
            idx = (start_idx + step) % total_tokens
            candidate = self.token_to_node[self.ring_tokens[idx]]
            if candidate in seen_nodes:
                continue
            seen_nodes.add(candidate)

            if self.node_loads[candidate] < max_allowed:
                chosen_node = candidate
                break

        # Fallback if all nodes are strictly saturated
        if chosen_node is None:
            chosen_node = min(self.node_loads.keys(), key=lambda n: self.node_loads[n])

        self.node_loads[chosen_node] += 1
        return chosen_node

    def release_load(self, node: str, amount: int = 1) -> None:
        """Release load from a node when request finishes or key is deleted."""
        if node in self.node_loads:
            self.node_loads[node] = max(0, self.node_loads[node] - amount)
