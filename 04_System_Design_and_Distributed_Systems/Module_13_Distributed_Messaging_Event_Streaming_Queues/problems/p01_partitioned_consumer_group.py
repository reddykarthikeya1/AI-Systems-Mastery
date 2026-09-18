"""Problem 01 — Partitioned Consumer Group

Topic: 13 Distributed Messaging Event Streaming Queues
Target: Production-grade implementation

Assign Kafka-like partitions evenly to active consumer instances.

Example:
    >>> partitioned_consumer_group([0, 1, 2, 3, 4], ['c1', 'c2'])
    {'c1': [0, 2, 4], 'c2': [1, 3]}

Hints:
    Hint 1: This is round-robin dealing, like dealing cards -- partitions
        go to consumers in turn, cycling back to the first consumer once
        you run out of consumers.
    Hint 2: Sort both partitions and consumers for a deterministic order,
        then assign `sorted_partitions[i]` to
        `sorted_consumers[i % len(sorted_consumers)]`.
    Hint 3: An empty consumer list must return `{}` immediately instead of
        raising a `ZeroDivisionError` on the modulo; sorting the consumer
        list (not just the partitions) is what makes the assignment
        reproducible and testable.
"""

from __future__ import annotations


def partitioned_consumer_group(partitions: list[int], consumers: list[str]) -> dict[str, list[int]]:
    """Distribute partitions evenly across consumers in round-robin fashion.
    Sorted consumers, sorted partitions.
    Returns mapping consumer_id -> list of assigned partition numbers.
    """
    raise NotImplementedError("Implement partitioned_consumer_group")
