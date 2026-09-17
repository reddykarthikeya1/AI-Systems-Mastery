"""Reference Solution — Problem 01: Shard Key Range Router

Topic: 11 MongoDB Aggregations Replicas Sharding
"""

from __future__ import annotations


def shard_key_range_router(chunks: list[dict], query_key_val: int) -> str:
    for c in chunks:
        if c['min'] <= query_key_val < c['max']:
            return c['shard_id']
    return 'UNROUTED'
