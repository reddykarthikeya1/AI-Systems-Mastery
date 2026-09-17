"""Reference Solution — Problem 01: Heartbeat Presence Tracker

Topic: 15 RealTime Chat Presence System Discord
"""

from __future__ import annotations


def heartbeat_presence_tracker(heartbeats: dict[str, int], current_time: int, ttl_seconds: int = 30) -> tuple[set[str], set[str]]:
    online = set()
    expired = set()
    for u, ts in heartbeats.items():
        if current_time - ts <= ttl_seconds:
            online.add(u)
        else:
            expired.add(u)
    return (online, expired)
