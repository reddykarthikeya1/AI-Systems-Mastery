"""Problem 01 — Heartbeat Presence Tracker

Topic: 15 RealTime Chat Presence System Discord
Target: Production-grade implementation

Track active user sessions and expire missed heartbeat deadlines.

Example:
    >>> active, expired = heartbeat_presence_tracker(
    ...     {'u1': 100, 'u2': 80, 'u3': 60}, 110, 30)
    >>> sorted(active), sorted(expired)
    (['u1', 'u2'], ['u3'])

Hints:
    Hint 1: This is a single-pass classification problem -- every user is
        independently either still online or timed out, based purely on
        how long it has been since their last heartbeat.
    Hint 2: Iterate `heartbeats.items()` once, compute
        `current_time - last_seen` for each user, and bucket the user_id
        into one of two sets based on that elapsed time.
    Hint 3: The boundary is inclusive on the online side -- a user exactly
        at the ttl (elapsed == ttl_seconds) still counts as online, so the
        expired branch needs a strict `>` comparison against
        `ttl_seconds`, not `>=`.
"""

from __future__ import annotations


def heartbeat_presence_tracker(heartbeats: dict[str, int], current_time: int, ttl_seconds: int = 30) -> tuple[set[str], set[str]]:
    """heartbeats: user_id -> last_seen_timestamp.
    Returns (online_users, expired_users) where expired if current_time - last_seen > ttl_seconds.
    """
    raise NotImplementedError("Implement heartbeat_presence_tracker")
