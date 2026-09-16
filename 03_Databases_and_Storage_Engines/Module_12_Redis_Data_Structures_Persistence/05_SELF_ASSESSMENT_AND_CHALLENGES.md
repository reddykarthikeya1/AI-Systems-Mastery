# Module 12 Redis Data Structures Persistence: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Redis Internals: Data Structures, RDB/AOF & Sliding Windows** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Why is Redis single-threaded, and how does it achieve >100,000 operations per second?** Why is Redis single-threaded, and how does it achieve >100,000 operations per second?
2. **What is the difference between Redis RDB snapshots and AOF (Append-Only File) persistence?** What is the difference between Redis RDB snapshots and AOF (Append-Only File) persistence?
3. **How does a Sliding-Window Rate Limiter work using Redis Sorted Sets?** How does a Sliding-Window Rate Limiter work using Redis Sorted Sets?
4. **What is the difference between volatile-lru and allkeys-lru eviction policies?** What is the difference between volatile-lru and allkeys-lru eviction policies?
5. **What is a Redis HyperLogLog, and what is its maximum memory footprint?** What is a Redis HyperLogLog, and what is its maximum memory footprint?
6. **How do Redis Hashes optimize memory for small objects?** How do Redis Hashes optimize memory for small objects?
7. **What does the BGREWRITEAOF command do?** What does the BGREWRITEAOF command do?
8. **What is the Cache-Aside (Lazy Loading) pattern?** What is the Cache-Aside (Lazy Loading) pattern?
9. **How does SET resource_name my_random_token NX EX 30 implement a safe distributed lock?** How does SET resource_name my_random_token NX EX 30 implement a safe distributed lock?
10. **Why must distributed lock releases use a Lua script?** Why must distributed lock releases use a Lua script?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
It operates entirely in RAM and uses non-blocking I/O multiplexing (epoll/kqueue), eliminating thread context switches and lock contention.

#### Answer 2:
RDB creates point-in-time binary disk snapshots; AOF logs every write command sequentially for near-zero RPO.

#### Answer 3:
Keys are timestamps; `ZREMRANGEBYSCORE` removes timestamps older than window; `ZCARD` checks count; `ZADD` appends current timestamp.

#### Answer 4:
volatile-lru evicts least recently used keys among those with an expire TTL; allkeys-lru evicts LRU keys across the entire database.

#### Answer 5:
A probabilistic cardinality estimation structure requiring at most 12KB RAM to count billions of unique elements with ~0.81% error rate.

#### Answer 6:
When small, Redis encodes hashes as compact ziplists/listpacks in contiguous RAM rather than full hash tables.

#### Answer 7:
It builds a new minimal AOF file reflecting current memory state without redundant intermediate command history.

#### Answer 8:
Application checks Redis cache; on miss, reads primary database, populates Redis with a TTL, and returns data.

#### Answer 9:
NX guarantees key is set only if it does not exist; EX sets an automatic expiration TTL preventing deadlocks.

#### Answer 10:
To ensure atomicity: verify the caller's unique random token matches before deleting the key, preventing releasing another worker's lock.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement a production-ready sliding-window rate limiter handling 1,000 requests per minute.

### 🚀 Challenge 2: Architect Stretch Problem
Build an atomic distributed lock in Python with automatic heartbeat extension.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Redis OOM crash due to missing maxmemory-policy configuration

```python
# redis.conf default settings:
# maxmemory 4gb
# maxmemory-policy noeviction

# Ingestion pipeline pushes 10,000,000 cache keys into Redis
```

**Observed symptom:** Application writes fail with `redis.exceptions.ResponseError: OOM command not allowed when used memory > 'maxmemory'`.

**(a)** What does the default `noeviction` policy do when Redis reaches its memory threshold?

**(b)** What is the difference between `allkeys-lru` and `volatile-lru` eviction policies?

**(c)** Why is Redis LRU an approximation rather than an exact linked-list LRU?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Under `noeviction`, Redis refuses all write commands (`SET`, `HSET`, `LPUSH`) with an OOM error once memory hits `maxmemory`.

**Fix:** Configure an active eviction policy in `redis.conf`: `maxmemory-policy allkeys-lru`. When memory is full, Redis evicts the least recently used keys automatically.

**Approximate LRU:** Redis does not maintain an exact doubly-linked list of all keys (which would cost 16 bytes of RAM per key); instead, it samples $N$ random keys (configured by `maxmemory-samples`, default 5) and evicts the best candidate among them.

</details>

---

### D2. SkipList memory bloat compared to compact ziplist/listpack

```python
# Storing 1,000,000 leaderboards with only 5 members each:
for board_id in range(1_000_000):
    r.zadd(f"board:{board_id}", {"player1": 10, "player2": 20})
```

**Observed symptom:** Redis consumes 1.8 GB RAM; memory analysis reveals 70% of memory is pointer overhead.

**(a)** What is the memory structure difference between a SkipList and a Listpack/Ziplist for small sorted sets?

**(b)** Which configuration setting controls the maximum size before a Sorted Set upgrades to a SkipList?

**(c)** What is the memory savings ratio achieved by keeping small sorted sets encoded as listpacks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A full SkipList node allocates multiple forward pointers (`zskiplistLevel`), dict entry structures, and dynamic string buffers. For small sets (2–10 elements), pointer overhead is 10x larger than the actual payload data.

**Fix:** Tune `zset-max-listpack-entries 128` and `zset-max-listpack-value 64`. Redis will store small sorted sets as contiguous flat byte arrays (listpacks), reducing memory footprint by over 70%.

</details>

---

### D3. Large HSET rehashing latency spike blocking event loop single thread

```python
# Storing 5,000,000 fields inside a single Redis Hash key:
for i in range(5_000_000):
    r.hset("global_metrics", f"metric_{i}", i)
```

**Observed symptom:** Every few minutes, Redis experiences a 250 ms latency freeze; sentinel triggers false-positive failover.

**(a)** How does Redis progressive rehashing work, and why does rehashing a 5-million-element hash table cause latency spikes?

**(b)** Why does Redis single-threaded event loop architecture make large operations hazardous?

**(c)** How should massive key spaces be partitioned into smaller independent hashes?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Expanding a hash table dictionary requires doubling the bucket array (e.g. from 4M to 8M slots). Allocating and zeroing an 8-million-pointer array in memory takes hundreds of milliseconds, blocking Redis's single-threaded event loop.

**Fix:** Shard large hashes using bucket hashing: instead of 1 hash with 5,000,000 fields, split into 1,000 hashes with 5,000 fields each: `hset(f'metrics:{hash(key) % 1000}', key, value)`.

</details>

---

### D4. AOF fsync always blocking single-threaded write throughput

```python
# redis.conf configured for maximum durability:
appendonly yes
appendfsync always
```

**Observed symptom:** Redis throughput collapses from 120,000 ops/sec to 1,200 ops/sec; NVMe disk write queues saturate.

**(a)** What does `appendfsync always` force the Redis main thread to do before acknowledging every write command?

**(b)** What is the operational difference between `always`, `everysec`, and `no`?

**(c)** Why is `appendfsync everysec` the industry standard recommended production balance?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Under `appendfsync always`, the main Redis server thread executes a blocking `fsync()` system call to physical disk before acknowledging every single client command. Disk I/O latency (0.5–2 ms) directly throttles the in-memory engine.

**Fix:** Configure `appendfsync everysec`. Fsync is offloaded to a background thread once per second. Redis achieves 100,000+ ops/sec with a maximum theoretical loss window of 1–2 seconds of data during power loss.

</details>

---

### D5. Simple Dynamic String (SDS) buffer memory fragmentation on string append loops

```python
# In-memory buffer construction appending small byte chunks in a loop:
sds = SimpleDynamicString("START")
for i in range(1000):
    sds.append(f"_chunk_{i}")
```

**Observed symptom:** Memory allocated is significantly larger than payload length; inspect shows `alloc` capacity doubled repeatedly.

**(a)** What is the growth buffer pre-allocation algorithm in Redis Simple Dynamic Strings (SDS)?

**(b)** Why does SDS double capacity when length is less than 1MB?

**(c)** What method in `SimpleDynamicString` truncates or compacts unused pre-allocated capacity?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** To prevent $O(N^2)$ memory allocations on frequent string appends, SDS pre-allocates spare capacity: if new length is $< 1	ext{ MB}$, it allocates $2 	imes 	ext{new\_len}$; if $> 1	ext{ MB}$, it allocates $	ext{new\_len} + 1	ext{ MB}$.

**Compaction:** When buffer mutations are complete, call `sds.free_unused()` or `sds.truncate()` to release unutilized allocated memory back to the heap allocator.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.
