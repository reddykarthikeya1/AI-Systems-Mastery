"""Unit tests for Hybrid Newsfeed & Two-Tower AI Recommendation Engine."""

from __future__ import annotations

from newsfeed_recommendation_engine import (
    HybridNewsfeedEngine,
    Post,
    UserProfile,
)


def test_standard_user_fanout_on_write() -> None:
    engine = HybridNewsfeedEngine(celebrity_threshold_followers=100)

    alice = UserProfile("alice")
    bob = UserProfile("bob")
    engine.register_user(alice)
    engine.register_user(bob)

    # Bob follows Alice
    engine.follow("bob", "alice")

    post = Post(
        post_id="post-1",
        author_id="alice",
        content="Deploying microservices!",
        category="TECH",
        embedding=(1.0, 0.0, 0.0, 0.0),
    )
    engine.publish_post(post)

    # Post must be pushed directly into Bob's timeline cache
    assert len(engine.timeline_cache["bob"]) == 1
    assert engine.timeline_cache["bob"][0].post_id == "post-1"


def test_celebrity_fanout_on_read_merging() -> None:
    # Set threshold low for test (3 followers makes an account a celebrity)
    engine = HybridNewsfeedEngine(celebrity_threshold_followers=3)

    elon = UserProfile("elon")
    engine.register_user(elon)

    # 3 users follow Elon -> triggers celebrity status
    for i in range(1, 4):
        u = UserProfile(f"follower-{i}")
        engine.register_user(u)
        engine.follow(f"follower-{i}", "elon")

    assert engine.users["elon"].is_celebrity is True

    celeb_post = Post(
        post_id="tweet-mars",
        author_id="elon",
        content="Starship orbital test tomorrow!",
        category="SPACE",
        embedding=(0.0, 1.0, 0.0, 0.0),
    )
    engine.publish_post(celeb_post)

    # Invariant: Celebrity post must NOT be duplicated across all followers' timeline caches!
    assert len(engine.timeline_cache["follower-1"]) == 0
    assert len(engine.celebrity_posts["elon"]) == 1

    # When follower reads feed, celebrity post is dynamically merged!
    feed = engine.get_chronological_feed("follower-1")
    assert len(feed) == 1
    assert feed[0].post_id == "tweet-mars"


def test_two_tower_candidate_retrieval_and_ranking() -> None:
    engine = HybridNewsfeedEngine()

    # User with strong interest in TECH: (1.0, 0.0, 0.0, 0.0)
    tech_user = UserProfile("techie", interest_vector=(1.0, 0.0, 0.0, 0.0))
    engine.register_user(tech_user)

    # Post A: Tech related (vector match = 1.0)
    post_a = Post(
        post_id="p-tech",
        author_id="author-1",
        content="Kubernetes vs Nomad",
        category="TECH",
        embedding=(1.0, 0.0, 0.0, 0.0),
        likes=50,
    )
    # Post B: Cooking related (orthogonal vector match = 0.0)
    post_b = Post(
        post_id="p-cooking",
        author_id="author-2",
        content="Best Pasta Carbonara Recipe",
        category="FOOD",
        embedding=(0.0, 1.0, 0.0, 0.0),
        likes=200,
    )
    engine.publish_post(post_a)
    engine.publish_post(post_b)

    # AI Personalized feed must rank the relevant Tech post first despite Cooking having more likes
    ai_feed = engine.get_personalized_ai_feed("techie", limit=5)
    assert len(ai_feed) == 2
    assert ai_feed[0].post_id == "p-tech"
    assert ai_feed[1].post_id == "p-cooking"
