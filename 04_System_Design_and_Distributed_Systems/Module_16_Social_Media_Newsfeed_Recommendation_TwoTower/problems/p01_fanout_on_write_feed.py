"""Problem 01 — Fanout On Write Feed

Topic: 16 Social Media Newsfeed Recommendation TwoTower
Target: Production-grade implementation

Deliver posts to followers' timelines with celebrity fanout-on-read threshold.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def fanout_on_write_feed(author_id: str, post_id: str, followers: list[str], celebrity_threshold: int = 5) -> dict[str, list[str]]:
    """If len(followers) <= celebrity_threshold:
        fanout-on-write: append post_id to each follower's inbox in returned dict.
    Else:
        celebrity: do not push to follower inboxes; store post under author's outbox only (dict key author_id).
    Returns dict mapping id -> list of post_ids.
    """
    raise NotImplementedError("Implement fanout_on_write_feed")
