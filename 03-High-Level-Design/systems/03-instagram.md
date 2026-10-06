# HLD Case Study 3: Instagram (Photo Sharing and Feed)

> **Key Focus Areas:** Media upload and processing pipeline, feed generation (fan-out on write vs read), CDN delivery, and storage cost.

---

## 1. Requirements and Scope

**Functional:** upload photos/videos, follow users, home feed of followed users' posts, likes and comments, explore/search.
**Non-functional:** feed loads in under 500 ms p99; uploads never lose data; the feed may be seconds stale (eventual consistency); high availability; global low-latency media.
**Out of scope:** ads, stories expiry mechanics, ML ranking internals.

## 2. Estimates

Assume 1B MAU, 500M DAU, 100M new posts/day (average 2 MB original; derived renditions add about 1.5x), each DAU opens the feed 10 times/day.

```python
dau, posts_per_day, orig_mb = 500e6, 100e6, 2.0
upload_qps = posts_per_day / 86400                  # ~1,157 uploads/s
peak_upload = upload_qps * 3                        # ~3,500/s
feed_reads_qps = dau * 10 / 86400                   # ~57,870 feed loads/s
storage_per_day_tb = posts_per_day * orig_mb * 2.5 / 1e6   # originals + renditions: 500 TB/day
storage_per_year_pb = storage_per_day_tb * 365 / 1000      # ~182 PB/year
egress_gbps = feed_reads_qps * 20 * 0.2 * 8 / 1000  # 20 images/feed, 200 KB each, in Gbps (CDN-served)
print(round(upload_qps), round(feed_reads_qps), storage_per_day_tb, round(storage_per_year_pb), round(egress_gbps))
assert round(upload_qps) == 1157 and storage_per_day_tb == 500.0
```

Takeaways: reads outnumber writes by about 50:1 (cache and CDN everything); media storage is the dominant cost (about 182 PB/year), so use object storage with lifecycle tiering and image compression; egress from feed images alone is about 1.9 Tbps (the code above), and more with video, which only a CDN can serve.

## 3. API Design

* `POST /media/uploads` returns presigned URL(s) (multipart for large files) and `media_id`.
* `POST /posts` `{media_id, caption, idempotency_key}` creates the post after the upload completes.
* `GET /feed?cursor=&limit=20` returns post ids with metadata and signed CDN URLs.
* `POST /posts/{id}/like`, `POST /users/{id}/follow`.

## 4. Data Model

* **posts**: `post_id` (time-sortable id such as Snowflake), `author_id`, `media_keys`, `caption`, `created_at`; sharded by `author_id` or by `post_id` range.
* **follows**: `(follower_id, followee_id)` stored both directions for "who do I follow" and "who follows me" (graph store or sharded relational).
* **feed cache**: `feed:{user_id}` as a Redis sorted set of the latest 500 `post_id`s scored by time.
* **likes**: counters in Redis, periodically flushed; per-user like edge in a KV store.

## 5. Architecture

```mermaid
flowchart TD
    C["Client"] -->|"presigned upload"| S3[("Object Storage")]
    S3 -->|"upload-complete event"| MQ["Kafka"]
    MQ --> Proc["Media Pipeline: virus scan, resize, transcode, blurhash"]
    Proc --> S3
    C --> API["Post / Feed API"]
    API --> Posts[("Post DB (sharded)")]
    Posts --> MQ2["Kafka: post-created"]
    MQ2 --> Fan["Fan-out Service"]
    Fan --> Feed[("Feed Cache (Redis)")]
    API --> Feed
    S3 --> CDN["CDN (signed URLs)"]
    C --> CDN
```

## 6. Deep Dive: Feed Generation

**Fan-out on write (push).** When a user posts, a worker prepends `post_id` to the feed cache of every follower. Reading the feed is a single Redis range read: very fast. Cost: a user with 50M followers causes 50M writes per post.
**Fan-out on read (pull).** At read time, fetch recent posts from each followee and merge. Cheap writes, slow reads for users who follow many accounts.
**Hybrid (what production systems do).** Push for normal users (under about 10K followers); **do not push for celebrities**. At read time, merge the user's precomputed feed with a live pull of recent posts from the celebrities they follow. Then apply ranking (affinity, recency, engagement) on about 500 candidates.

**Media pipeline.** Upload goes straight to object storage via presigned URLs (the API tier never carries bytes). An event triggers asynchronous workers that scan, strip EXIF, generate renditions (for example 150, 320, 640, 1080 px) plus WebP/AVIF, and extract a blur placeholder. The post becomes visible only when processing marks it `READY`.

## 7. Scaling and Bottlenecks

* **Celebrity hot keys:** hybrid fan-out; cache hot posts and counters with request coalescing.
* **Fan-out lag:** use a queue with worker autoscaling; accept seconds of staleness; prioritise active users first.
* **Storage cost:** tier old media to infrequent-access classes, store only needed renditions, deduplicate identical uploads by content hash.
* **Like counters:** write to Redis `INCR`, batch to the database; counts are approximate for display.
* **Cold start feed:** if the cache is empty (new device or evicted), rebuild by pulling and merging, then repopulate.

## 8. Failure Modes and Mitigations

| Failure | Mitigation |
|---|---|
| Upload interrupted | resumable multipart upload; `idempotency_key` on post creation |
| Media worker crash | queue redelivery; processing is idempotent keyed by `media_id` |
| Feed cache loss | rebuild from DB via pull; feeds are derived data |
| CDN regional failure | multi-CDN or origin fallback |
| Poison media (corrupt file) | dead-letter queue, mark post failed, notify user |

## 9. Trade-offs

* Push gives O(1) reads but write amplification; pull gives O(1) writes but expensive reads; hybrid bounds both.
* Strong consistency for follows/posts is unnecessary; eventual consistency keeps latency low.
* Precompute renditions (storage cost) vs on-the-fly resizing at the edge (CPU cost and latency).
* Chronological vs ranked feed: ranking raises engagement but needs features, models and explainability.

## 10. Interview Timeline and Follow-ups

Lead with the read:write ratio, then the fan-out decision, then the celebrity edge case. **Follow-ups:** How do you delete a post everywhere? (tombstone, async removal from caches and CDN purge). How do you implement "Explore"? (offline candidate generation plus an ANN index, course 10). How do you shard posts? (by `author_id` keeps profile pages local; by `post_id` spreads writes evenly). How would you support stories that expire in 24 h? (TTL in storage and cache, lifecycle policy).


---

## 5. Runnable Model: Fan-out on Write, Fan-out on Read, and the Hybrid

The feed design stands or falls on one trade-off, and a small simulation shows why celebrities force a hybrid.

```python
import heapq

class Feed:
    def __init__(self, celebrity_threshold=1000):
        self.followers = {}                       # author -> list of followers
        self.following = {}                       # user -> list of authors
        self.posts = {}                           # author -> list of (timestamp, post_id), newest last
        self.inbox = {}                           # user -> list of (timestamp, post_id) pushed at write time
        self.threshold = celebrity_threshold
        self.writes = 0                           # counts push operations, the cost of fan-out on write

    def follow(self, user, author):
        self.followers.setdefault(author, []).append(user)
        self.following.setdefault(user, []).append(author)

    def post(self, author, ts, post_id, mode):
        self.posts.setdefault(author, []).append((ts, post_id))
        followers = self.followers.get(author, [])
        push = mode == "push" or (mode == "hybrid" and len(followers) < self.threshold)
        if push:
            for f in followers:
                self.inbox.setdefault(f, []).append((ts, post_id))
                self.writes += 1

    def read(self, user, mode, k=5):
        items = list(self.inbox.get(user, []))
        for author in self.following.get(user, []):
            pull = mode == "pull" or (mode == "hybrid" and len(self.followers.get(author, [])) >= self.threshold)
            if pull:
                items.extend(self.posts.get(author, [])[-k:])
        return [p for _, p in heapq.nlargest(k, items)]

def build(mode):
    f = Feed(celebrity_threshold=1000)
    for i in range(5000):
        f.follow(f"u{i}", "star")                 # a celebrity with 5,000 followers
    for i in range(5):
        f.follow("reader", f"friend{i}")          # an ordinary user following five friends
    f.follow("reader", "star")
    ts = 0
    for i in range(5):
        ts += 1; f.post(f"friend{i}", ts, f"friend-post-{i}", mode)
    ts += 1; f.post("star", ts, "star-post", mode)
    return f

push, hybrid, pull = build("push"), build("hybrid"), build("pull")
assert push.writes == 5001 + 5 and hybrid.writes == 5 and pull.writes == 0    # the star has 5,001 followers (5,000 plus the reader)
feed_push, feed_hybrid, feed_pull = push.read("reader", "push"), hybrid.read("reader", "hybrid"), pull.read("reader", "pull")
assert feed_push == feed_hybrid == feed_pull       # all three modes produce the same feed
assert feed_hybrid[0] == "star-post"               # newest first
```

The three modes return the same feed but cost differently: **push** makes reads trivial and a celebrity post costs thousands of writes; **pull** makes writes free and every read merges many authors; **hybrid** pushes for ordinary users and pulls celebrity posts at read time, which bounds both costs. This is the design in the architecture section above, shown as numbers.

---

## 6. Failure Modes and Mitigations

| Failure | Effect | Mitigation |
| :--- | :--- | :--- |
| Fan-out queue backlog | New posts appear late in followers' feeds | Prioritise active followers first, scale workers, degrade to pull for lagging users |
| Media upload succeeds, metadata write fails | Orphan blob | Write metadata after upload and garbage-collect unreferenced blobs, or use a pending state |
| Cache loss for a popular feed | Thundering herd on the database | Request coalescing, replicas, staggered TTLs |
| CDN origin overload from a viral post | Slow images | Tiered CDN, origin shield, pre-warm for known big accounts |
| Unfollow or delete after fan-out | Stale items in inboxes | Filter at read time against current follow and deletion state |

## 7. Trade-offs and Alternatives

- **Ranked versus chronological feed:** chronological is cheap and predictable; ranking needs candidate generation, features and a model, and moves cost to read time.
- **Inbox size:** cap each precomputed inbox (for example the newest 1,000 items) so storage per user is bounded and old content is fetched by pull.
- **Counts (likes, followers):** exact counters are expensive at scale; approximate or sharded counters with periodic aggregation are normal.
- **Storing media:** originals in an object store, several resized variants generated asynchronously, everything behind a CDN.

## 8. Interview Timeline (45 minutes) and Follow-ups

| Minutes | Do |
| :--- | :--- |
| 0 to 5 | Scope: feed, upload, follow, likes; scale; ranked or chronological |
| 5 to 10 | Estimates: uploads per day, feed reads per second, storage and egress |
| 10 to 20 | APIs, data model, upload and media pipeline |
| 20 to 35 | **Feed generation**: push, pull, hybrid and the celebrity problem |
| 35 to 42 | Caching, CDN, counters, sharding |
| 42 to 45 | Failure modes and what you would improve next |

**Follow-ups to prepare:** What is the cost of one celebrity post under push? How do you pick the celebrity threshold? How do you add ranking without making reads slow? How do you handle deletes and privacy changes already fanned out?
