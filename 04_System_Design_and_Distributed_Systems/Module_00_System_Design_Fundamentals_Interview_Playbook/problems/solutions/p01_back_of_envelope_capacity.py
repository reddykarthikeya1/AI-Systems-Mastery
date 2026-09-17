"""Reference Solution — Problem 01: Back Of Envelope Capacity

Topic: 00 System Design Fundamentals Interview Playbook
"""

from __future__ import annotations


def back_of_envelope_capacity(dau: int, read_writes_per_user: int, read_ratio: float, avg_payload_bytes: int) -> dict[str, float]:
    total_actions = dau * read_writes_per_user
    read_qps = (total_actions * read_ratio) / 86400.0
    write_qps = (total_actions * (1.0 - read_ratio)) / 86400.0
    daily_storage_gb = (total_actions * (1.0 - read_ratio) * avg_payload_bytes) / (1024.0 ** 3)
    return {
        'read_qps': round(read_qps, 2),
        'write_qps': round(write_qps, 2),
        'daily_storage_gb': round(daily_storage_gb, 4)
    }
