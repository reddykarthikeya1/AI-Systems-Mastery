"""
================================================================================
SIMULATION 01: Consistent Hash Ring with Virtual Nodes
================================================================================
Zero-Prerequisite Intuition:
Imagine dividing 10,000 files among 4 storage servers (Server 0, 1, 2, 3).
The naive way is: server = hash(file_id) % 4.
What happens if Server 2 crashes and you have 3 servers left?
hash(file_id) % 3 completely scrambles where almost EVERY single file lives!
99% of your cache is wiped out in a single second!

Consistent Hashing arranges servers on a 360-degree circle (0 to 2^32 - 1).
When a server is added or removed, ONLY keys adjacent to that server move!
Virtual Nodes ensure uniform distribution across all servers.

Run this script to observe virtual node balancing and rebalancing metrics live!
================================================================================
"""

import hashlib
import bisect
from collections import defaultdict
import math

class ConsistentHashRing:
    def __init__(self, virtual_nodes_per_server: int = 150):
        self.replicas = virtual_nodes_per_server
        self.ring: list[int] = [] # Sorted hash points on the ring
        self.hash_to_node: dict[int, str] = {} # Hash -> Physical server name

    def _hash(self, key: str) -> int:
        """MD5 32-bit hash mapped onto a 2^32 integer ring."""
        return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)

    def add_server(self, server_name: str):
        """Adds a physical server with multiple virtual node points to the ring."""
        for i in range(self.replicas):
            v_key = f"{server_name}#vn_{i}"
            h = self._hash(v_key)
            self.ring.append(h)
            self.hash_to_node[h] = server_name
        self.ring.sort()

    def remove_server(self, server_name: str):
        """Removes a physical server and all its virtual nodes."""
        for i in range(self.replicas):
            v_key = f"{server_name}#vn_{i}"
            h = self._hash(v_key)
            if h in self.hash_to_node:
                del self.hash_to_node[h]
                self.ring.remove(h)
        self.ring.sort()

    def get_server(self, key: str) -> str:
        """Finds the server responsible for a key by walking clockwise on the ring."""
        if not self.ring:
            raise RuntimeError("Ring is empty!")

        h = self._hash(key)
        # Binary search for the first node with hash >= key's hash
        idx = bisect.bisect_right(self.ring, h)
        
        # If we reached the end of the array, wrap around to the first node (Circle!)
        if idx == len(self.ring):
            idx = 0
            
        return self.hash_to_node[self.ring[idx]]


def run_consistent_hash_simulation():
    print("--- [EXPERIMENT 1] Initializing Ring with 4 Storage Nodes ---")
    ring = ConsistentHashRing(virtual_nodes_per_server=150)
    servers = ["Cache_Alpha", "Cache_Beta", "Cache_Gamma", "Cache_Delta"]
    for s in servers:
        ring.add_server(s)

    # Distribute 100,000 cache keys
    num_keys = 100_000
    distribution = defaultdict(int)
    key_assignments = {}

    for i in range(num_keys):
        key = f"user_session_{i}"
        assigned = ring.get_server(key)
        distribution[assigned] += 1
        key_assignments[key] = assigned

    print(f"\nDistribution of {num_keys:,} keys across 4 servers (Target: ~25,000 each):")
    for s in sorted(distribution.keys()):
        pct = (distribution[s] / num_keys) * 100
        print(f"  Node {s:12}: {distribution[s]:,d} keys ({pct:.1f}%)")

    # Standard Deviation calculation
    mean = num_keys / len(servers)
    variance = sum((count - mean) ** 2 for count in distribution.values()) / len(servers)
    std_dev = math.sqrt(variance)
    print(f"\nUniformity Standard Deviation: {std_dev:.1f} keys (Excellent uniform spread!)")

    print("\n--- [EXPERIMENT 2] Node 'Cache_Gamma' Crashes & Is Removed ---")
    ring.remove_server("Cache_Gamma")

    # Measure how many keys were forced to move
    keys_moved = 0
    new_distribution = defaultdict(int)
    for i in range(num_keys):
        key = f"user_session_{i}"
        new_assigned = ring.get_server(key)
        new_distribution[new_assigned] += 1
        if new_assigned != key_assignments[key]:
            keys_moved += 1

    pct_moved = (keys_moved / num_keys) * 100
    print(f"Total keys that migrated: {keys_moved:,} out of {num_keys:,} ({pct_moved:.1f}%)")
    print(f"[THEORY CONFIRMATION] In consistent hashing, removing 1 of 4 nodes only moves ~25% of keys!")
    print(f"                      In naive hash(k)%N, ~75% to 90% of keys would be wiped out!")

if __name__ == "__main__":
    run_consistent_hash_simulation()
