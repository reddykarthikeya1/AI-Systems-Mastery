# Module 11 MongoDB Aggregations Replicas Sharding: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **MongoDB Aggregation Pipelines, Replication & Sharding** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the execution model of a MongoDB Aggregation Pipeline?** What is the execution model of a MongoDB Aggregation Pipeline?
2. **How does the $lookup stage perform left outer joins between collections?** How does the $lookup stage perform left outer joins between collections?
3. **What is the difference between a Targeted Query and a Scatter-Gather Query in a sharded cluster?** What is the difference between a Targeted Query and a Scatter-Gather Query in a sharded cluster?
4. **What does the $unwind stage do to an embedded array?** What does the $unwind stage do to an embedded array?
5. **What is the role of the mongos query router in MongoDB sharding?** What is the role of the mongos query router in MongoDB sharding?
6. **How does readPreference secondaryPreferred improve cluster throughput?** How does readPreference secondaryPreferred improve cluster throughput?
7. **What is the 100MB RAM limit on aggregation pipeline stages, and how is it bypassed?** What is the 100MB RAM limit on aggregation pipeline stages, and how is it bypassed?
8. **What is a Change Stream in MongoDB?** What is a Change Stream in MongoDB?
9. **What is Hashed Sharding vs Range-Based Sharding?** What is Hashed Sharding vs Range-Based Sharding?
10. **What is the $facet stage in aggregation pipelines?** What is the $facet stage in aggregation pipelines?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
A multi-stage streaming pipeline where documents pass sequentially through transformation operators ($match, $unwind, $group, $sort).

#### Answer 2:
It matches `localField` in the source collection to `foreignField` in the target collection, outputting matches as an embedded array.

#### Answer 3:
Targeted queries include the Shard Key and route to exactly 1 shard; Scatter-Gather queries lack the shard key and broadcast to every shard in the cluster.

#### Answer 4:
It deconstructs an array field, outputting one document for every element in the array.

#### Answer 5:
It acts as a stateless gateway directing client queries to appropriate shards based on cluster metadata from config servers.

#### Answer 6:
It routes read-heavy analytical queries to secondary replicas, reserving the primary replica for transactional writes.

#### Answer 7:
Stages like $sort and $group cannot exceed 100MB RAM unless `{allowDiskUse: true}` is enabled to spill to temporary files.

#### Answer 8:
A real-time pub/sub API using the replica set oplog to notify applications of document inserts, updates, and deletes.

#### Answer 9:
Hashed sharding hashes shard keys for uniform write distribution; Range sharding groups contiguous keys for efficient range queries.

#### Answer 10:
It executes multiple aggregation pipelines simultaneously within a single stage on the same input document stream.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Build an aggregation pipeline computing customer lifetime value (LTV) across orders and payments.

### 🚀 Challenge 2: Architect Stretch Problem
Simulate a consistent hash shard router evaluating key distribution balance across 5 virtual shards.

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

### D1. Aggregation pipeline exceeding 100MB RAM limit without allowDiskUse

```python
# Aggregation grouping 10,000,000 documents by customer
pipeline = [
    {"$group": {"_id": "$customer_id", "total_spend": {"$sum": "$amount"}}},
    {"$sort": {"total_spend": -1}}
]
db.orders.aggregate(pipeline)
```

**Observed symptom:** Query crashes with `pymongo.errors.OperationFailure: PlanExecutor error during aggregation :: caused by :: Sort exceeded memory limit of 104857600 bytes, but did not allowExternalSort`.

**(a)** What is the default RAM limit for an individual aggregation stage in MongoDB?

**(b)** What flag enables spilling intermediate aggregation groups to disk?

**(c)** How does placing a `$match` filter before `$group` reduce memory footprint?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** MongoDB restricts RAM usage for any single aggregation pipeline stage to **100 MB** to prevent rogue queries from starving cluster memory. Unindexed `$group` and `$sort` stages across millions of documents exceed this limit.

**Fix 1:** Set `allowDiskUse=True`: `db.orders.aggregate(pipeline, allowDiskUse=True)`.

**Fix 2 (Architectural):** Pre-filter data using `$match` at the beginning of the pipeline so only relevant rows reach `$group`, and ensure `$sort` uses an index.

</details>

---

### D2. Monotonically increasing shard key creating single-shard write hotspot

```python
# Cluster sharded using default ObjectId as shard key:
sh.shardCollection("shop.orders", {"_id": 1})
```

**Observed symptom:** In an 8-shard cluster, 100% of all write traffic lands exclusively on Shard 8; Shards 1 through 7 remain completely idle at 0% CPU.

**(a)** Why does a monotonically increasing shard key (`_id` or `timestamp`) route all writes to a single chunk?

**(b)** What is Hashed Sharding, and how does it distribute sequential writes uniformly across all cluster nodes?

**(c)** What trade-off does Hashed Sharding introduce for range-based queries?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Since `ObjectId` has a leading timestamp, every new document has an `_id` greater than the current max chunk boundary. All inserts land in the topmost chunk on the 'max key' shard (Jailed Chunk Hotspotting).

**Fix:** Use **Hashed Sharding**: `sh.shardCollection('shop.orders', {'_id': 'hashed'})`. Hashes `_id` uniformly with MD5 across all shards.

**Trade-off:** Hashed sharding scatters sequential data; range queries (`_id >= 100 AND _id <= 200`) cannot perform range seeks and must scatter-gather across all shards.

</details>

---

### D3. Scatter-Gather query latency cliff on un-sharded query filters

```python
# Collection sharded on user_id:
# Query searches by email address:
db.users.find({"email": "alice@company.com"})
```

**Observed symptom:** Query p99 latency is 450 ms in a 32-shard cluster, even though email is indexed on every individual shard.

**(a)** Why must `mongos` router broadcast un-sharded queries to every shard in the cluster (Scatter-Gather)?

**(b)** How does the slowest shard in the cluster dictate overall query latency?

**(c)** How does Global Secondary Indexing or Targeted Routing mitigate scatter-gather overhead?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** The `mongos` query router uses the shard key (`user_id`) to route queries directly to the holding shard. Because `email` is not part of the shard key, `mongos` cannot determine where the document lives and must broadcast the query to **all 32 shards**, waiting for all responses (Scatter-Gather).

**Latency Cliff:** Overall latency is bounded by the slowest, highest-load shard in the cluster ($O(\max(	ext{shard latency}))$).

**Fix:** Always include the shard key in query predicates (`{'user_id': 101, 'email': ...}`) to enable **Targeted Routing**.

</details>

---

### D4. Unwind memory explosion on high-cardinality embedded arrays

```python
# Document contains array of 25,000 sub-items:
pipeline = [
    {"$match": {"category": "electronics"}},
    {"$unwind": "$items"},
    {"$group": {"_id": "$items.sku", "count": {"$sum": 1}}}
]
db.catalogs.aggregate(pipeline)
```

**Observed symptom:** Aggregation process consumes 32 GB RAM, triggering Linux OOM killer (`dmesg: Out of memory: Killed process mongod`).

**(a)** How does `$unwind` duplicate document state in memory for every array element?

**(b)** Why should high-cardinality collections avoid large arrays in document modeling?

**(c)** What alternative projection strategy filters array items prior to unwinding?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** `$unwind` physically creates a new document in memory for every single element in the array. Unwinding 1,000 documents with 25,000 items generates 25,000,000 documents in memory simultaneously, overwhelming WiredTiger cache.

**Fix:** Pre-filter array elements using `$filter` in a `$project` stage before unwinding, or remodel the relationship into a separate normalized collection.

</details>

---

### D5. Shard chunk balancing lock contention during peak traffic hours

```python
# Balancer runs continuously across cluster during Black Friday sale:
# Jumbo chunks split and migrate across network links
```

**Observed symptom:** Active checkout transactions experience intermittent lock timeouts and 504 Gateway Errors.

**(a)** How does MongoDB chunk migration acquire collection metadata locks on source and destination shards?

**(b)** What window configuration parameter restricts the chunk balancer to low-traffic off-peak maintenance hours?

**(c)** What is a 'Jumbo Chunk', and why does it fail to split automatically?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Moving chunks between shards requires transferring data over network links and taking brief distributed locks during the critical catch-up phase. Running balancing during peak traffic creates heavy lock contention and saturates internal cluster replication bandwidth.

**Fix:** Define an off-peak balancing window:
```javascript
sh.setBalancerState(true);
sh.updateConfigSetting("balancer.activeWindow", { start: "02:00", stop: "05:00" });
```
**Jumbo Chunks:** Chunks exceeding maximum chunk size (64MB) that cannot be split because all documents share the exact same shard key value.

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
