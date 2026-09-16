"""Module 13: Redis Sentinel, Clustering, Lua & Streams Demo.

Demonstrates:
1. Redis Cluster 16,384 Hash Slot mapping and Hash Tag extraction.
2. Redis Sentinel leader election and highest-offset replica promotion.
3. Redis Stream consumer group message distribution and PEL acknowledgment.
"""

from __future__ import annotations

import binascii
import time


def compute_redis_crc16(key: str) -> int:
    """Compute Redis Cluster hash slot (0 - 16383) using CRC16 and Hash Tags."""
    # Check for Hash Tag: {tag}
    start = key.find("{")
    if start != -1:
        end = key.find("}", start + 1)
        if end != -1 and end > start + 1:
            key = key[start + 1 : end]

    # Redis uses CRC16-CCITT (polynomial 0x1021)
    crc = binascii.crc_hqx(key.encode("utf-8"), 0)
    return crc % 16384


def demo_cluster_hash_slots() -> None:
    print("=" * 75)
    print("    1. REDIS CLUSTER: 16,384 HASH SLOTS & HASH TAGS")
    print("=" * 75)

    keys = [
        "user:100:profile",
        "user:100:orders",
        "{user:100}:profile",
        "{user:100}:orders",
        "orders:2026:jan",
    ]

    for k in keys:
        slot = compute_redis_crc16(k)
        print(f"Key: {k:<25} -> Hash Slot: {slot:>5} / 16383")

    slot_profile = compute_redis_crc16("{user:100}:profile")
    _ = compute_redis_crc16("{user:100}:orders")
    print("\nResult Analysis:")
    print("  -> Plain keys hashed to different slots (cannot do multi-key transaction).")
    print(f"  -> Hash-tagged keys '{'{user:100}'}:profile' and '{'{user:100}'}:orders' hash to slot {slot_profile}!")
    print("  -> Both keys are guaranteed to reside on the same cluster shard!")


def demo_sentinel_failover() -> None:
    print("\n" + "=" * 75)
    print("    2. REDIS SENTINEL: ODOWN CONSENSUS & REPLICA PROMOTION")
    print("=" * 75)

    # Master node dies
    print("Master Node (10.0.0.1:6379) [DOWN] (No PONG to PING)")
    print("Sentinel-1 detects SDOWN (Subjective Down)")
    print("Sentinel-2 detects SDOWN")
    print("Sentinel-3 detects SDOWN")
    print("  -> Quorum 3/3 reached => Escalated to ODOWN (Objective Down)!")

    # Candidate replicas
    replicas = [
        {"id": "replica-1", "ip": "10.0.0.2:6379", "priority": 100, "repl_offset": 8450200},
        {"id": "replica-2", "ip": "10.0.0.3:6379", "priority": 100, "repl_offset": 8450950},  # Highest offset!
        {"id": "replica-3", "ip": "10.0.0.4:6379", "priority": 0,   "repl_offset": 8450950},  # Priority 0: never promote
    ]

    print("\nCandidate Replicas Evaluation:")
    for r in replicas:
        print(f"  [{r['id']}] IP: {r['ip']}, Priority: {r['priority']}, Offset: {r['repl_offset']:,} bytes")

    # Promotion decision
    eligible = [r for r in replicas if r["priority"] > 0]
    promoted = max(eligible, key=lambda r: (r["repl_offset"], -r["priority"]))

    print("\nFailover Result:")
    print(f"  -> Promoted Master: {promoted['id']} ({promoted['ip']}) with highest offset {promoted['repl_offset']:,}!")
    print(f"  -> Replicas reconfigured to replicate from {promoted['ip']}.")


def demo_streams_and_pel() -> None:
    print("\n" + "=" * 75)
    print("    3. REDIS STREAMS: CONSUMER GROUPS & PENDING ENTRIES LIST (PEL)")
    print("=" * 75)

    # Simulated Stream Entries
    now = int(time.time() * 1000)
    stream = [
        {"id": f"{now}-0", "data": {"order_id": "ord_101", "amount": 250}},
        {"id": f"{now}-1", "data": {"order_id": "ord_102", "amount": 890}},
    ]
    print(f"Stream 'orders_stream' has {len(stream)} events.")

    # Worker-1 reads message 0
    pel = {
        stream[0]["id"]: {"consumer": "worker-1", "delivered_at": now - 30000, "data": stream[0]["data"]}
    }
    print(f"Worker-1 consumed '{stream[0]['id']}' -> Entry added to PEL (Pending Entries List).")
    print("Worker-1 crashed before sending XACK!")

    # Worker-2 inspects PEL after 30s idle time
    idle_ms = 30000
    print(f"\nWorker-2 discovers dead message in PEL (idle for {idle_ms} ms):")
    for msg_id, meta in pel.items():
        print(f"  -> XCLAIM: Worker-2 reclaims '{msg_id}' from crashed {meta['consumer']}")
        meta["consumer"] = "worker-2"

    print("Worker-2 successfully processes order and sends XACK.")
    del pel[stream[0]["id"]]
    print(f"PEL Size after XACK: {len(pel)} (Message safely retired with zero data loss).")


def main() -> None:
    demo_cluster_hash_slots()
    demo_sentinel_failover()
    demo_streams_and_pel()


if __name__ == "__main__":
    main()
