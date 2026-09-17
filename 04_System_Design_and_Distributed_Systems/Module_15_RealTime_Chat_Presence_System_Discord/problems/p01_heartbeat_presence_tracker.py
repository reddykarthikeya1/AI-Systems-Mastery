"""Problem 01 — Heartbeat Presence Tracker

Topic: 15 RealTime Chat Presence System Discord
Target: Production-grade implementation

Track active user sessions and expire missed heartbeat deadlines.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def heartbeat_presence_tracker(heartbeats: dict[str, int], current_time: int, ttl_seconds: int = 30) -> tuple[set[str], set[str]]:
    """heartbeats: user_id -> last_seen_timestamp.
    Returns (online_users, expired_users) where expired if current_time - last_seen > ttl_seconds.
    """
    raise NotImplementedError("Implement heartbeat_presence_tracker")
