"""Problem 01 — Fanout On Write Feed

Topic: 16 Social Media Newsfeed Recommendation TwoTower
Target: Production-grade implementation

Deliver posts to followers' timelines with celebrity fanout-on-read threshold.

Example:
    >>> fanout_on_write_feed('regular_user', 'post_1', ['f1', 'f2'], 5)
    {'f1': ['post_1'], 'f2': ['post_1']}

Hints:
    Hint 1: This models a cost tradeoff -- pushing a post to every
        follower's inbox is cheap for ordinary users but explodes in cost
        for accounts with huge follower counts, so the strategy must
        branch on follower count.
    Hint 2: A single conditional on `len(followers)` vs
        `celebrity_threshold` decides the path: at or below it, build one
        dict entry per follower; above it, build a single entry keyed by
        `author_id` instead.
    Hint 3: The threshold comparison is inclusive (`<=`), so a follower
        count exactly equal to `celebrity_threshold` still uses
        fan-out-on-write; once in celebrity mode the followers list is
        never touched, and the returned dict has exactly one key, the
        `author_id`.
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
