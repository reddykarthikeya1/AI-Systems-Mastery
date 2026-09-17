"""Unit tests for Partitioned Commit-Log Event Streaming Broker."""

from __future__ import annotations

from commit_log_stream import (
    ConsumerGroup,
    Topic,
)


def test_key_based_partitioning_guarantees_order() -> None:
    topic = Topic("order-events", num_partitions=3)

    # Invariant: All events with the same key MUST map to the same partition!
    r1 = topic.publish(key="order-991", value={"status": "CREATED"})
    r2 = topic.publish(key="order-991", value={"status": "PAID"})
    r3 = topic.publish(key="order-991", value={"status": "SHIPPED"})

    assert r1.partition_id == r2.partition_id == r3.partition_id
    assert r1.offset == 0
    assert r2.offset == 1
    assert r3.offset == 2


def test_consumer_group_partition_assignment_and_rebalance() -> None:
    topic = Topic("clicks", num_partitions=4)
    cg = ConsumerGroup(group_id="analytics-service", topic=topic)

    # 1. Register Consumer 1 -> owns all 4 partitions
    cg.register_member("worker-1")
    assert cg.assignments["worker-1"] == [0, 1, 2, 3]

    # 2. Register Consumer 2 -> rebalance splits partitions evenly (2 each)
    cg.register_member("worker-2")
    assert len(cg.assignments["worker-1"]) == 2
    assert len(cg.assignments["worker-2"]) == 2
    # Combined union covers all 4 partitions
    all_assigned = set(cg.assignments["worker-1"] + cg.assignments["worker-2"])
    assert all_assigned == {0, 1, 2, 3}

    # 3. Consumer 2 leaves -> Consumer 1 reclaims all 4 partitions
    cg.leave_member("worker-2")
    assert cg.assignments["worker-1"] == [0, 1, 2, 3]


def test_consumer_group_fetch_and_offset_commit() -> None:
    topic = Topic("telemetry", num_partitions=2)
    cg = ConsumerGroup(group_id="metrics-writer", topic=topic)
    cg.register_member("c1")

    # Publish 4 messages
    for i in range(4):
        topic.publish(key=f"sensor-{i}", value={"temp": 20 + i})

    # Fetch batch 1
    batch1 = cg.fetch("c1", max_records_per_partition=10)
    assert len(batch1) == 4

    # Before commit, fetching again returns the same records (at-least-once guarantee)
    batch1_repeat = cg.fetch("c1", max_records_per_partition=10)
    assert len(batch1_repeat) == 4

    # Commit the batch
    cg.commit(batch1)

    # Fetching after commit returns 0 new records
    batch2 = cg.fetch("c1", max_records_per_partition=10)
    assert len(batch2) == 0


def test_log_replay_via_seek() -> None:
    topic = Topic("audit-log", num_partitions=1)
    cg = ConsumerGroup(group_id="auditor", topic=topic)
    cg.register_member("auditor-1")

    topic.publish("k1", "Audit Event 1")
    topic.publish("k2", "Audit Event 2")

    records = cg.fetch("auditor-1")
    assert len(records) == 2
    cg.commit(records)
    assert cg.committed_offsets[0] == 2

    # Rewind / Replay from offset 0
    cg.seek(partition_id=0, offset=0)
    replayed = cg.fetch("auditor-1")
    assert len(replayed) == 2
    assert replayed[0].value == "Audit Event 1"
    assert replayed[1].value == "Audit Event 2"
