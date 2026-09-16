"""Beginner playground for Module 16 - News Feed and Recommendation Systems.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------ 1. Push: do the work when the post is written
# The celebrity's 50 million followers are a COUNT, not a list. Materialising
# them would need gigabytes of memory - which is the lesson of this module.
follower_count = {"ana": 2, "celebrity": 50_000_000}
followers = {"ana": ["bo", "cy"], "celebrity": ["fan1", "fan2"]}  # a sample
feeds = {}
writes = {"count": 0}


def post_push(author, message):
    for follower in followers[author]:
        writes["count"] += 1
        feeds.setdefault(follower, []).append((author, message))


writes["count"] = 0
post_push("ana", "hello")
print(f"ana posts -> {writes['count']} feed writes")
print("bo's feed:", feeds["bo"])
assert writes["count"] == 2, "cheap for an ordinary user"
assert feeds["bo"] == [("ana", "hello")]


# -------------------------------------------- 2. And then the celebrity posts
WRITES_PER_SECOND = 100_000
celebrity_writes = follower_count["celebrity"]
seconds = celebrity_writes / WRITES_PER_SECOND

print(f"one celebrity post -> {celebrity_writes:,} feed writes")
print(f"at {WRITES_PER_SECOND:,} writes/second that is {seconds / 60:.1f} minutes")
assert celebrity_writes == 50_000_000
assert seconds > 300, "the last follower waits minutes for a post others saw at once"


# --------------------------------- 3. Pull: do the work when the feed is read
posts = {"celebrity": [("celebrity", "big news")]}
reads = {"count": 0}


def read_pull(user, following):
    merged = []
    for author in following:
        reads["count"] += 1
        merged += posts.get(author, [])
    return merged


reads["count"] = 0
timeline = read_pull("fan1", ["celebrity"])
print("fan1's feed:", timeline, f"({reads['count']} lookups)")
assert timeline == [("celebrity", "big news")]
assert reads["count"] == 1

following_200 = [f"author{i}" for i in range(200)]
reads["count"] = 0
read_pull("heavy_user", following_200)
print(f"a user following 200 accounts: {reads['count']} lookups, every refresh")
assert reads["count"] == 200


# --------------------------- 4. The hybrid, and why it is the standard answer
CELEBRITY_THRESHOLD = 100_000


def post_hybrid(author, message):
    if follower_count[author] > CELEBRITY_THRESHOLD:
        posts.setdefault(author, []).append((author, message))
        return "stored once, pulled at read time"
    for follower in followers[author]:
        writes["count"] += 1
        feeds.setdefault(follower, []).append((author, message))
    return f"pushed to {follower_count[author]} feeds"


writes["count"] = 0
print("ana:      ", post_hybrid("ana", "second post"))
print("celebrity:", post_hybrid("celebrity", "second big news"))
assert writes["count"] == 2, "only the ordinary post fanned out"


def read_hybrid(user, following):
    feed = list(feeds.get(user, []))
    for author in following:
        if follower_count.get(author, 0) > CELEBRITY_THRESHOLD:
            feed += posts.get(author, [])
    return feed


bo_feed = read_hybrid("bo", ["ana", "celebrity"])
print("bo's merged feed has", len(bo_feed), "items")
assert len(bo_feed) == 4, "2 pushed from ana, 2 pulled from the celebrity"


# ---------------------------------- 5. Ranking: two towers, and why it is two
item_vectors = {"post_a": [0.9, 0.1], "post_b": [0.2, 0.8], "post_c": [0.8, 0.2]}
user_vector = [0.85, 0.15]


def score(user, item):
    return sum(u * i for u, i in zip(user, item, strict=True))


ranked = sorted(item_vectors, key=lambda name: score(user_vector, item_vectors[name]),
                reverse=True)
for name in ranked:
    print(f"  {name}: {score(user_vector, item_vectors[name]):.3f}")

assert ranked[0] == "post_a"
assert ranked[-1] == "post_b", "least aligned with this user's interests"
print()
print("Item vectors: precomputed offline. User vector: one computation per request.")


print()
print("All checks passed.")
