#!/usr/bin/env python3
"""Module 09 Demo: Live Consistent Hash Ring Scaling & Rebalancing."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from consistent_hash_ring import ConsistentHashRing


def main() -> None:
    print("=" * 72)
    print("  MODULE 09: CONSISTENT HASHING & DISTRIBUTED REBALANCING")
    print("=" * 72)

    # 1. Initialize Ring with 3 servers
    print("\n--- 1. Initializing Consistent Hash Ring (3 Nodes, 150 vnodes each) ---")
    ring = ConsistentHashRing(nodes=["db-shard-1", "db-shard-2", "db-shard-3"], vnodes=150)
    print(f"Total tokens placed on hash ring: {len(ring.ring)}")

    # 2. Key routing
    sample_keys = [f"user_profile:{i:04d}" for i in range(1000)]
    stats_initial = ring.get_distribution_stats(sample_keys)
    print("\nInitial Key Distribution across 3 Shards (1000 keys):")
    for node in sorted(ring.physical_nodes):
        cnt = stats_initial[f"node_{node}"]
        bar = "#" * int(cnt // 15)
        print(f"  {node:<12}: {cnt:3d} keys | {bar}")
    print(f"Expected per node: {stats_initial['expected_per_node']:.1f}, Std Dev: {stats_initial['std_dev']:.1f}")

    # 3. Dynamic Scaling: Add 4th Node
    print("\n--- 2. Adding 4th Shard ('db-shard-4') to Ring ---")
    before_map = {k: ring.get_node(k) for k in sample_keys}
    ring.add_node("db-shard-4")
    after_map = {k: ring.get_node(k) for k in sample_keys}

    migrated = [k for k in sample_keys if before_map[k] != after_map[k]]
    print(f"Total keys migrated: {len(migrated)} / 1000 ({len(migrated) / 10:.1f}%)")
    print("  -> Under naive modulo hashing (hash % N), ~75% of keys would be invalidated!")
    print(f"  -> Under Consistent Hashing, only ~{100 / 4:.1f}% migrated, matching theoretical optimum!")

    # 4. Replica Preference Lists
    print("\n--- 3. Replica Preference Lists (Replication Factor = 3) ---")
    for key in ["order:9920", "payment:4412"]:
        replicas = ring.get_preference_list(key, count=3)
        print(f"Key '{key}' replicas: Primary={replicas[0]}, Replicas={replicas[1:]}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
