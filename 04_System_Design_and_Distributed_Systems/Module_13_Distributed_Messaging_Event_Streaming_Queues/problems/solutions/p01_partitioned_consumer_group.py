"""Reference Solution — Problem 01: Partitioned Consumer Group

Topic: 13 Distributed Messaging Event Streaming Queues
"""

from __future__ import annotations


def partitioned_consumer_group(partitions: list[int], consumers: list[str]) -> dict[str, list[int]]:
    s_cons = sorted(consumers)
    s_parts = sorted(partitions)
    if not s_cons:
        return {}
    res = {c: [] for c in s_cons}
    for i, p in enumerate(s_parts):
        c = s_cons[i % len(s_cons)]
        res[c].append(p)
    return res
