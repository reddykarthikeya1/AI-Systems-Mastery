"""Problem 01 — Back Of Envelope Capacity

Topic: 00 System Design Fundamentals Interview Playbook
Target: Production-grade implementation

Calculate storage and QPS requirements from daily active users and read/write ratios.

Example:
    >>> back_of_envelope_capacity(1_000_000, 20, 0.9, 500)
    {'read_qps': 208.33, 'write_qps': 23.15, 'daily_storage_gb': 0.9313}

Hints:
    Hint 1: Everything here derives from one number: total actions per day
        (dau * read_writes_per_user) -- work that out first.
    Hint 2: Split total actions into a read share and a write share using
        read_ratio, then convert each share to a per-second rate by
        dividing by the number of seconds in a day (86400).
    Hint 3: Storage only accounts for the WRITE share of traffic (reads
        don't consume new storage) multiplied by avg_payload_bytes, and
        the result is in GiB (divide bytes by 1024**3), not GB.
"""

from __future__ import annotations


def back_of_envelope_capacity(dau: int, read_writes_per_user: int, read_ratio: float, avg_payload_bytes: int) -> dict[str, float]:
    """Calculate capacity:
    - total_actions = dau * read_writes_per_user
    - read_qps = (total_actions * read_ratio) / 86400.0
    - write_qps = (total_actions * (1.0 - read_ratio)) / 86400.0
    - daily_storage_gb = (total_actions * (1.0 - read_ratio) * avg_payload_bytes) / (1024.0 ** 3)
    Returns dict with 'read_qps', 'write_qps', and 'daily_storage_gb'.
    """
    raise NotImplementedError("Implement back_of_envelope_capacity")
