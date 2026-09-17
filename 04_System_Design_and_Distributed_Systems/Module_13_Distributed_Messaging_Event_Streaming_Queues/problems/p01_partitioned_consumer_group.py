"""Problem 01 — Partitioned Consumer Group

Topic: 13 Distributed Messaging Event Streaming Queues
Target: Production-grade implementation

Assign Kafka-like partitions evenly to active consumer instances.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def partitioned_consumer_group(partitions: list[int], consumers: list[str]) -> dict[str, list[int]]:
    """Distribute partitions evenly across consumers in round-robin fashion.
    Sorted consumers, sorted partitions.
    Returns mapping consumer_id -> list of assigned partition numbers.
    """
    raise NotImplementedError("Implement partitioned_consumer_group")
