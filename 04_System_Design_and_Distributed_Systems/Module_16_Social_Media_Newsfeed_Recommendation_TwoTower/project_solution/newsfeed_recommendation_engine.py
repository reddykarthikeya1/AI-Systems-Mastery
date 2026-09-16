#!/usr/bin/env python3
"""Module 16: Hybrid Fan-out & Modern Two-Tower AI Recommendation Newsfeed Engine.

Implements:
1. Hybrid Fan-out: Push for normal users, Pull-on-demand for celebrities.
2. Two-Tower Neural Candidate Generation (User Vector dot Item Vector).
3. Real-Time Feature Store hydration.
4. Heavy Ranking Model with Engagement Velocity and Recency Decay.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import math
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Post:
    post_id: str
    author_id: str
    content: str
    category: str
    embedding: tuple[float, ...]  # Dense vector representation
    created_at: float = field(default_factory=time.time)
    likes: int = 0
    shares: int = 0


@dataclass
class UserProfile:
    user_id: str
    is_celebrity: bool = False
    preferred_category: str = "TECH"
    interest_vector: tuple[float, ...] = (0.0, 0.0, 0.0, 0.0)


def dot_product(v1: tuple[float, ...], v2: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(v1, v2, strict=False))


def vector_norm(v: tuple[float, ...]) -> float:
    return math.sqrt(sum(x * x for x in v)) or 1.0


def cosine_similarity(v1: tuple[float, ...], v2: tuple[float, ...]) -> float:
    return dot_product(v1, v2) / (vector_norm(v1) * vector_norm(v2))


class TwoTowerCandidateRetriever:
    """Simulates a Two-Tower deep learning retrieval model (e.g. YouTube / Pinterest).

    User Tower produces user interest embedding.
    Item Tower produces post candidate embedding.
    Retrieval evaluates cosine/inner product to retrieve top-K candidates from millions.
    """

    def __init__(self) -> None:
        self._item_corpus: dict[str, Post] = {}
        self._lock = threading.Lock()

    def index_post(self, post: Post) -> None:
        with self._lock:
            self._item_corpus[post.post_id] = post

    def retrieve_candidates(self, user: UserProfile, top_k: int = 20) -> list[Post]:
        with self._lock:
            scored = [
                (cosine_similarity(user.interest_vector, post.embedding), post)
                for post in self._item_corpus.values()
            ]
        # Sort descending by vector similarity
        scored.sort(key=lambda x: x[0], reverse=True)
        return [post for _, post in scored[:top_k]]


class RealTimeFeatureStore:
    """In-memory low-latency feature store providing user and context features."""

    def __init__(self) -> None:
        self.user_features: dict[str, dict[str, float]] = {}

    def get_features(self, user_id: str) -> dict[str, float]:
        return self.user_features.get(user_id, {"engagement_rate": 0.5, "activity_level": 1.0})

    def update_user_feature(self, user_id: str, key: str, value: float) -> None:
        if user_id not in self.user_features:
            self.user_features[user_id] = {}
        self.user_features[user_id][key] = value


class HeavyRankingModel:
    """Multi-task scoring model: combines semantic match, engagement velocity, and recency."""

    @staticmethod
    def score(user: UserProfile, post: Post, user_features: dict[str, float]) -> float:
        # 1. Semantic relevance (acts as gating factor; floor at 0.05 for serendipity)
        sim = cosine_similarity(user.interest_vector, post.embedding)
        relevance = max(0.05, sim)

        # 2. Normalized engagement velocity (log1p scaled to ~ [0, 1])
        engagement = math.log1p(post.likes + post.shares * 2.0) / 10.0

        # 3. Recency decay (half-life of 3600 seconds / 1 hour)
        age_seconds = max(0.0, time.time() - post.created_at)
        recency = math.exp(-age_seconds / 3600.0)

        # 4. User engagement multiplier from feature store
        user_multiplier = user_features.get("engagement_rate", 1.0)

        # Multiplicative gating: semantic relevance modulates engagement
        return relevance * (1.0 + engagement + 0.5 * recency) * user_multiplier


class HybridNewsfeedEngine:
    """Enterprise Hybrid Newsfeed Engine with Follower Fan-out & AI Recommendation."""

    def __init__(self, celebrity_threshold_followers: int = 10_000) -> None:
        self.celebrity_threshold = celebrity_threshold_followers
        self.users: dict[str, UserProfile] = {}
        # Social Graph: follower_id -> set of followed author_ids
        self.following: dict[str, set[str]] = defaultdict(set)
        # Social Graph: author_id -> set of followers
        self.followers: dict[str, set[str]] = defaultdict(set)
        # Timeline Cache (Redis-style): user_id -> list of post_ids (Fanout on Write)
        self.timeline_cache: dict[str, list[Post]] = defaultdict(list)
        # Celebrity Posts: author_id -> list of posts (Fanout on Read)
        self.celebrity_posts: dict[str, list[Post]] = defaultdict(list)

        # AI Recommendation Components
        self.retriever = TwoTowerCandidateRetriever()
        self.feature_store = RealTimeFeatureStore()
        self.ranker = HeavyRankingModel()
        self._lock = threading.RLock()

    def register_user(self, user: UserProfile) -> None:
        with self._lock:
            self.users[user.user_id] = user

    def follow(self, follower_id: str, followee_id: str) -> None:
        with self._lock:
            self.following[follower_id].add(followee_id)
            self.followers[followee_id].add(follower_id)
            # Crossing the threshold flips this account to celebrity fan-out,
            # which is what stops a 50M-follower write from fanning out eagerly.
            if (
                len(self.followers[followee_id]) >= self.celebrity_threshold
                and followee_id in self.users
            ):
                self.users[followee_id].is_celebrity = True

    def publish_post(self, post: Post) -> None:
        """Publishes post: fanout-on-write for normal users, or store in celebrity bucket."""
        with self._lock:
            author = self.users.get(post.author_id)
            is_celeb = author.is_celebrity if author else False

            # Always index into AI candidate retriever
            self.retriever.index_post(post)

            if is_celeb:
                # Celebrity: Do NOT write to 10M followers! Store in celebrity bucket (Pull on read)
                self.celebrity_posts[post.author_id].append(post)
            else:
                # Normal User: Fanout-on-write to all direct followers' timeline caches
                for follower in self.followers[post.author_id]:
                    self.timeline_cache[follower].insert(0, post)

    def get_chronological_feed(self, user_id: str, limit: int = 10) -> list[Post]:
        """Hybrid fanout feed: merges follower timeline cache + followed celebrities."""
        with self._lock:
            # 1. Direct follower posts from cache (Fanout on Write)
            timeline = list(self.timeline_cache.get(user_id, []))

            # 2. Merge posts from any followed celebrities (Fanout on Read)
            followed_authors = self.following.get(user_id, set())
            for author_id in followed_authors:
                if author_id in self.celebrity_posts:
                    timeline.extend(self.celebrity_posts[author_id])

            # Sort combined timeline by timestamp descending
            timeline.sort(key=lambda p: p.created_at, reverse=True)
            return timeline[:limit]

    def get_personalized_ai_feed(self, user_id: str, limit: int = 10) -> list[Post]:
        """AI Recommendation Feed (TikTok / Twitter 'For You' style).

        1. Two-Tower Candidate Generation (Retrieves top 50 relevant items)
        2. Real-Time Feature Store Hydration
        3. Heavy Scoring & Ranking
        4. Return top-K recommendations
        """
        with self._lock:
            user = self.users.get(user_id)
            if not user:
                raise KeyError(f"User {user_id} not found")

            # Step 1: Candidate Generation
            candidates = self.retriever.retrieve_candidates(user, top_k=50)

            # Step 2: Feature Store Hydration
            features = self.feature_store.get_features(user_id)

            # Step 3: Heavy Ranking
            ranked = [
                (self.ranker.score(user, post, features), post)
                for post in candidates
            ]
            ranked.sort(key=lambda x: x[0], reverse=True)

            return [post for _, post in ranked[:limit]]
