#!/usr/bin/env python3
"""Module 03: collections module & heapq Priority Queues Demonstration.

This script demonstrates deque, Counter, defaultdict, and heapq min-heaps.
"""

from __future__ import annotations

import heapq
from collections import Counter, defaultdict, deque


def demo_deque_ring_buffer() -> None:
    print("=" * 60)
    print("  1. collections.deque (Ring Buffer & Fast FIFO)")
    print("=" * 60)

    # Fixed-size sliding window (maxlen=3)
    recent_logs = deque(maxlen=3)
    recent_logs.append("Log #1: Booting")
    recent_logs.append("Log #2: Initialized Database")
    recent_logs.append("Log #3: Listening on port 8000")
    print(f"Current Window: {list(recent_logs)}")

    # Adding a 4th log automatically drops the oldest log from the left!
    recent_logs.append("Log #4: Incoming GET /api/v1/status")
    print(f"After 4th append: {list(recent_logs)}")


def demo_counter_multiset() -> None:
    print("\n" + "=" * 60)
    print("  2. collections.Counter (Multiset Analysis)")
    print("=" * 60)

    server_errors = [
        "404 Not Found", "500 Internal Error", "404 Not Found",
        "401 Unauthorized", "500 Internal Error", "500 Internal Error",
    ]
    error_counts = Counter(server_errors)
    print(f"Error Frequency Count:\n  {error_counts}")
    print(f"Top 1 Most Frequent Error:\n  {error_counts.most_common(1)}")


def demo_defaultdict_grouping() -> None:
    print("\n" + "=" * 60)
    print("  3. collections.defaultdict (Categorical Grouping)")
    print("=" * 60)

    products = [
        ("Electronics", "Laptop"),
        ("Apparel", "Hoodie"),
        ("Electronics", "Smartphone"),
        ("Books", "Fluent Python"),
        ("Apparel", "Running Shoes"),
    ]

    category_catalog = defaultdict(list)
    for category, item in products:
        category_catalog[category].append(item)

    print("Grouped Category Catalog:")
    for cat, items in category_catalog.items():
        print(f"  [{cat}]: {', '.join(items)}")


def demo_heapq_priority_queue() -> None:
    print("\n" + "=" * 60)
    print("  4. heapq Priority Queue & Top-N Selection")
    print("=" * 60)

    # Numerical scores
    scores = [85, 42, 98, 73, 91, 64, 99, 88]

    # Find Top 3 highest scores in O(N log K) without sorting entire list
    top_3 = heapq.nlargest(3, scores)
    print(f"Top 3 Scores: {top_3}")

    # Min-Heap order simulation
    heap: list[tuple[int, str]] = []
    heapq.heappush(heap, (5, "Low Priority Batch Job"))
    heapq.heappush(heap, (1, "CRITICAL: Database Failover"))
    heapq.heappush(heap, (2, "High: Payment Processing Retry"))

    print("\nExtracting jobs in priority order:")
    while heap:
        priority, job_name = heapq.heappop(heap)
        print(f"  [Priority {priority}] -> {job_name}")


def main() -> None:
    demo_deque_ring_buffer()
    demo_counter_multiset()
    demo_defaultdict_grouping()
    demo_heapq_priority_queue()


if __name__ == "__main__":
    main()
