"""Reference Solution — Problem 01: Rdb Snapshot Ziplist

Topic: 12 Redis Data Structures Persistence
"""

from __future__ import annotations


def rdb_snapshot_ziplist(items: list[str | int]) -> bytes:
    body = bytearray()
    for it in items:
        raw = str(it).encode('utf-8')
        body.append(len(raw))
        body.extend(raw)
    total_len = 6 + len(body)
    header = bytearray()
    header.extend(total_len.to_bytes(4, 'big'))
    header.extend(len(items).to_bytes(2, 'big'))
    return bytes(header + body)
