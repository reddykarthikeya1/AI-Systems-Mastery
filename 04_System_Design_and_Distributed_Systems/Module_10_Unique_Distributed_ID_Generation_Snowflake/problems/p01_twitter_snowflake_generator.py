"""Problem 01 — Twitter Snowflake Generator

Topic: 10 Unique Distributed ID Generation Snowflake
Target: Production-grade implementation

Generate 64-bit Snowflake ID with timestamp, machine ID, and sequence counter.

Example:
    >>> twitter_snowflake_generator(1700000001000, 5, 1)
    4194324481
    >>> twitter_snowflake_generator(1700000001000, 5, 2)
    4194324482

Hints:
    Hint 1: The 64-bit ID is three fields packed side by side by bit
        position, so it only needs to be monotonic within a millisecond
        when sequence increases — nothing fancier.
    Hint 2: Bit-shift and OR the fields together: shift the timestamp
        delta left by 22 (10 + 12 bits), shift `machine_id` left by 12,
        and OR in `sequence`, the same way you'd pack flags into an int.
    Hint 3: Mask each field to its allotted width with a bitwise AND
        before shifting (41 bits for the delta, 10 bits for machine_id,
        12 bits for sequence) so an out-of-range value can't bleed into
        neighboring bits; the delta is `timestamp_ms - epoch`, not the
        raw timestamp.
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
