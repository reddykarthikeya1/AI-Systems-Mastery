#!/usr/bin/env python3
"""Module 16 Demo: Hybrid Fanout & Two-Tower AI Recommendation Pipeline."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from newsfeed_recommendation_engine import (
    HybridNewsfeedEngine,
    Post,
    UserProfile,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 16: SOCIAL MEDIA NEWSFEED & TWO-TOWER AI RECOMMENDATION")
    print("=" * 72)

    engine = HybridNewsfeedEngine(celebrity_threshold_followers=5)

    # 1. Register users: Alice (Normal), Cristiano (Celebrity)
    alice = UserProfile("alice", is_celebrity=False)
    cristiano = UserProfile("cristiano", is_celebrity=True)
    bob = UserProfile("bob", interest_vector=(0.8, 0.2, 0.0, 0.0))  # interested in Sports/Tech

    engine.register_user(alice)
    engine.register_user(cristiano)
    engine.register_user(bob)

    engine.follow("bob", "alice")
    engine.follow("bob", "cristiano")

    print("\n--- 1. Hybrid Fanout: Push vs. Pull Mechanics ---")
    post_alice = Post(
        post_id="p-alice-1",
        author_id="alice",
        content="Working on a distributed cache tutorial!",
        category="TECH",
        embedding=(0.9, 0.1, 0.0, 0.0),
        likes=12,
    )
    post_celeb = Post(
        post_id="p-cristiano-1",
        author_id="cristiano",
        content="Victory in Champions League! Great team effort.",
        category="SPORTS",
        embedding=(0.1, 0.9, 0.0, 0.0),
        likes=5_000_000,
    )

    print("Publishing Alice's post (Normal User)...")
    engine.publish_post(post_alice)
    print(f"  Pushed to Bob's Timeline Cache: {len(engine.timeline_cache['bob'])} post(s)")

    print("\nPublishing Cristiano's post (Celebrity with Millions of Followers)...")
    engine.publish_post(post_celeb)
    print(f"  NOT pushed to Bob's cache! (Celebrity store count: {len(engine.celebrity_posts['cristiano'])})")

    print("\nBob requests his Chronological Feed (Merged dynamically):")
    chrono_feed = engine.get_chronological_feed("bob")
    for p in chrono_feed:
        print(f"  [{p.author_id}] {p.content} (Likes: {p.likes:,})")

    # 2. Modern AI Two-Tower Recommendation
    print("\n--- 2. Modern Two-Tower AI Recommendation Pipeline (TikTok/X 'For You') ---")
    # Add multiple items across categories
    more_posts = [
        Post("p-fin-1", "fin_guru", "Federal Reserve interest rate update", "FINANCE", (0.0, 0.0, 1.0, 0.0), 350),
        Post("p-tech-2", "cloud_arch", "Raft vs Paxos consensus simplified", "TECH", (0.85, 0.15, 0.0, 0.0), 890),
        Post("p-sport-2", "fifa_news", "World cup qualifiers kickoff", "SPORTS", (0.05, 0.95, 0.0, 0.0), 4500),
    ]
    for p in more_posts:
        engine.publish_post(p)

    print("Running Two-Tower Embedding Retrieval + Heavy Ranking for Bob:")
    ai_feed = engine.get_personalized_ai_feed("bob", limit=3)
    for rank, post in enumerate(ai_feed, 1):
        print(f"  Rank #{rank}: [{post.category:<7}] {post.content} | Author: {post.author_id}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
