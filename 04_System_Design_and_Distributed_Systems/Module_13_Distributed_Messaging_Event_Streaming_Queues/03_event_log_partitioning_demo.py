#!/usr/bin/env python3
"""Module 13 Demo: Partitioned Event Streaming, Consumer Groups & Replay."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from commit_log_stream import ConsumerGroup, Topic


def main() -> None:
    print("=" * 72)
    print("  MODULE 13: PARTITIONED COMMIT-LOG EVENT STREAMING DEMO")
    print("=" * 72)

    # 1. Create a topic with 3 partitions
    topic = Topic(name="financial-transactions", num_partitions=3)
    print(f"\nCreated topic '{topic.name}' with {topic.num_partitions} partitions.")

    # 2. Publish transactions with customer keys
    transactions = [
        ("cust-100", {"amount": 500, "action": "DEPOSIT"}),
        ("cust-200", {"amount": 120, "action": "WITHDRAW"}),
        ("cust-100", {"amount": 250, "action": "TRANSFER"}),
        ("cust-300", {"amount": 90, "action": "PURCHASE"}),
        ("cust-100", {"amount": 1000, "action": "DEPOSIT"}),
    ]

    print("\n--- 1. Publishing Records with Partition Keys ---")
    for key, val in transactions:
        rec = topic.publish(key, val)
        print(f"Key: {key:<9} -> Partition #{rec.partition_id} | Offset: {rec.offset} | Action: {val['action']}")

    print("\nNotice that all 'cust-100' events landed on the EXACT same partition!")
    print("-> Guarantees strict chronological processing order per customer without global locks.")

    # 3. Consumer Group & Rebalance
    print("\n--- 2. Consumer Group Rebalancing & Consumption ---")
    cg = ConsumerGroup(group_id="fraud-detection-service", topic=topic)

    print("Registering worker-A...")
    cg.register_member("worker-A")
    print(f"  Worker-A owns partitions: {cg.assignments['worker-A']}")

    print("Registering worker-B (Triggers Rebalance)...")
    cg.register_member("worker-B")
    print(f"  Worker-A owns partitions: {cg.assignments['worker-A']}")
    print(f"  Worker-B owns partitions: {cg.assignments['worker-B']}")

    # 4. Fetch and Commit
    print("\n--- 3. Fetching and Advancing Offsets ---")
    records_a = cg.fetch("worker-A")
    print(f"Worker-A fetched {len(records_a)} records.")
    for r in records_a:
        print(f"  [Worker-A] Processed Partition {r.partition_id}, Offset {r.offset}: Key={r.key}")
    cg.commit(records_a)

    records_b = cg.fetch("worker-B")
    print(f"\nWorker-B fetched {len(records_b)} records.")
    for r in records_b:
        print(f"  [Worker-B] Processed Partition {r.partition_id}, Offset {r.offset}: Key={r.key}")
    cg.commit(records_b)

    print(f"\nCommitted offsets per partition: {cg.committed_offsets}")

    # 5. Seeking / Log Replay
    print("\n--- 4. Replaying Log from Offset 0 ---")
    target_pid = records_a[0].partition_id if records_a else 0
    print(f"Rewinding Partition #{target_pid} committed offset to 0...")
    cg.seek(partition_id=target_pid, offset=0)
    replayed = cg.fetch("worker-A")
    print(f"Worker-A successfully re-read {len(replayed)} records from offset 0!")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
