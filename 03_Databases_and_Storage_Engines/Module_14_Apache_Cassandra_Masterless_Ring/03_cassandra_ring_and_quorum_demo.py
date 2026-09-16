"""Module 14: Apache Cassandra Masterless Ring & Tunable Quorum Demo.

Demonstrates:
1. Consistent Hashing Token Ring with 64-bit integer space.
2. Natural replica placement for Replication Factor N=3.
3. Strict Quorum math (R + W > N) preventing stale reads vs Eventual Consistency.
"""

from __future__ import annotations

import hashlib
import struct


def murmur3_64bit_hash(key: str) -> int:
    """Simulate Murmur3 64-bit signed integer token generation (-2^63 to 2^63 - 1)."""
    digest = hashlib.md5(key.encode("utf-8")).digest()
    # Unpack 8 bytes as signed 64-bit integer
    (val,) = struct.unpack(">q", digest[:8])
    return val


def demo_token_ring() -> None:
    print("=" * 75)
    print("    1. CASSANDRA CONSISTENT HASHING: 64-BIT TOKEN RING")
    print("=" * 75)

    # 4 Simulated Physical Nodes
    nodes = {
        "node_1": -4_611_686_018_427_387_904,
        "node_2": 0,
        "node_3": 4_611_686_018_427_387_903,
        "node_4": 9_223_372_036_854_775_807,
    }

    sorted_ring = sorted(nodes.items(), key=lambda x: x[1])
    print("Cluster Ring Topology (Token Range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807):")
    for name, token in sorted_ring:
        print(f"  [{name:<8}] -> Token: {token:>22,}")

    sample_keys = [
        "users:user_1001",
        "orders:order_8829",
        "telemetry:device_alpha",
        "logs:system_kernel",
    ]

    print("\nMapping Partition Keys to Responsible Primary Nodes:")
    for k in sample_keys:
        token = murmur3_64bit_hash(k)
        # Walk ring clockwise to find first node with token >= key_token
        target_node = sorted_ring[0][0]
        for name, n_token in sorted_ring:
            if n_token >= token:
                target_node = name
                break
        print(f"  Key: {k:<25} -> Token: {token:>22,} -> Primary Node: {target_node}")


def demo_quorum_math() -> None:
    print("\n" + "=" * 75)
    print("    2. TUNABLE CONSISTENCY MATH: R + W > N (STRONG vs STALE)")
    print("=" * 75)

    rf = 3
    print(f"Replication Factor (N) : {rf}")
    print(f"Required QUORUM count  : {rf // 2 + 1} replicas")

    # Scenario A: W=QUORUM (2), R=QUORUM (2)
    w_a, r_a = 2, 2
    sum_a = w_a + r_a
    is_strong_a = sum_a > rf
    print(f"\nScenario A: Write=QUORUM ({w_a}), Read=QUORUM ({r_a})")
    print(f"  -> R + W = {sum_a} > N({rf}) ? {is_strong_a}")
    print("  -> GUARANTEE: Strong Consistency (Pigeonhole principle guarantees at least 1 replica overlap!)")

    # Scenario B: W=ONE (1), R=ONE (1)
    w_b, r_b = 1, 1
    sum_b = w_b + r_b
    is_strong_b = sum_b > rf
    print(f"\nScenario B: Write=ONE ({w_b}), Read=ONE ({r_b})")
    print(f"  -> R + W = {sum_b} > N({rf}) ? {is_strong_b}")
    print("  -> GUARANTEE: Eventual Consistency (High risk of reading stale data if written replica is not queried!)")


def main() -> None:
    demo_token_ring()
    demo_quorum_math()


if __name__ == "__main__":
    main()
