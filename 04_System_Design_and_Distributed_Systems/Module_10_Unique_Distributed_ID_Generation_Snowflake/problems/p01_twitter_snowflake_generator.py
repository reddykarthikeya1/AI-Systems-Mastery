"""Problem 01 — Twitter Snowflake Generator

Topic: 10 Unique Distributed ID Generation Snowflake
Target: Production-grade implementation

Generate 64-bit Snowflake ID with timestamp, machine ID, and sequence counter.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def twitter_snowflake_generator(timestamp_ms: int, machine_id: int, sequence: int, epoch: int = 1700000000000) -> int:
    """Snowflake 64-bit layout:
    - 1 sign bit (0)
    - 41 bits timestamp delta: (timestamp_ms - epoch)
    - 10 bits machine_id (0 <= machine_id < 1024)
    - 12 bits sequence (0 <= sequence < 4096)
    Returns composite 64-bit integer.
    """
    raise NotImplementedError("Implement twitter_snowflake_generator")
