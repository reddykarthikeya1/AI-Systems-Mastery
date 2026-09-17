"""Reference Solution — Problem 01: Twitter Snowflake Generator

Topic: 10 Unique Distributed ID Generation Snowflake
"""

from __future__ import annotations


def twitter_snowflake_generator(timestamp_ms: int, machine_id: int, sequence: int, epoch: int = 1700000000000) -> int:
    delta = (timestamp_ms - epoch) & ((1 << 41) - 1)
    m = machine_id & 0x3FF
    s = sequence & 0xFFF
    return (delta << 22) | (m << 12) | s
