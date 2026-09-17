"""Reference Solution — Problem 01: Fanout On Write Feed

Topic: 16 Social Media Newsfeed Recommendation TwoTower
"""

from __future__ import annotations


def fanout_on_write_feed(author_id: str, post_id: str, followers: list[str], celebrity_threshold: int = 5) -> dict[str, list[str]]:
    res = {}
    if len(followers) <= celebrity_threshold:
        for f in followers:
            res[f] = [post_id]
    else:
        res[author_id] = [post_id]
    return res
