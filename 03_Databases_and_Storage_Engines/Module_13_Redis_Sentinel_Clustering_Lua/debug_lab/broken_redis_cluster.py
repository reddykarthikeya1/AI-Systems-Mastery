"""DEBUG LAB: CROSSSLOT Keys in Request Don't Hash to the Same Slot

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

import zlib

NUM_SLOTS = 16384

class RedisCluster:
    """A toy Redis Cluster: each key hashes to a slot, each slot lives on a node."""

    def __init__(self, num_nodes: int) -> None:
        self.num_nodes = num_nodes
        self.nodes: list[dict[str, str]] = [dict() for _ in range(num_nodes)]

    def slot(self, key: str) -> int:
        return zlib.crc32(key.encode()) % NUM_SLOTS

    def node_for(self, key: str) -> int:
        return self.slot(key) % self.num_nodes

    def set(self, key: str, value: str) -> None:
        self.nodes[self.node_for(key)][key] = value

    def mget_naive(self, keys: list[str]) -> list[str | None]:
        """Routes the whole multi-key request to the node owning the FIRST
        key only, the way a single-hop client behaves if it never validates
        that every key maps to the same hash slot."""
        target_node = self.node_for(keys[0])
        return [self.nodes[target_node].get(k) for k in keys]

def reproduce_defect() -> None:
    print("Fetching a user's profile and cart with one multi-key GET...")
    cluster = RedisCluster(num_nodes=3)
    cluster.set("user:101:profile", "profile-data")
    cluster.set("user:101:cart", "cart-data")

    result = cluster.mget_naive(["user:101:profile", "user:101:cart"])
    expected = ["profile-data", "cart-data"]

    print(f"mget_naive result: {result}")
    print(f"Expected result:   {expected}")
    if result != expected:
        print("[DEFECT OBSERVED] 'user:101:profile' and 'user:101:cart' hash to "
              "different slots on different nodes, so the second key silently "
              "returns None instead of raising CROSSSLOT or being fetched.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
