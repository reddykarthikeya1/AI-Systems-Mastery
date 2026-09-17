"""Problem 01 — Back Of Envelope Capacity

Topic: 00 System Design Fundamentals Interview Playbook
Target: Production-grade implementation

Calculate storage and QPS requirements from daily active users and read/write ratios.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
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
