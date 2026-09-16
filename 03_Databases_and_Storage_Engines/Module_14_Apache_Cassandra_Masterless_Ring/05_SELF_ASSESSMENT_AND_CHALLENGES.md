# Module 14 Apache Cassandra Masterless Ring: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Why is Apache Cassandra described as a masterless, shared-nothing architecture?** Why is Apache Cassandra described as a masterless, shared-nothing architecture?
2. **Explain the formula for strong consistency in tunable quorum replication.?** Explain the formula for strong consistency in tunable quorum replication.
3. **What is the difference between a Partition Key and a Clustering Key in CQL?** What is the difference between a Partition Key and a Clustering Key in CQL?
4. **How does Cassandra resolve write conflicts without locks?** How does Cassandra resolve write conflicts without locks?
5. **What is a Tombstone in Cassandra storage, and why can excessive tombstones degrade performance?** What is a Tombstone in Cassandra storage, and why can excessive tombstones degrade performance?
6. **What is Read Repair in Apache Cassandra?** What is Read Repair in Apache Cassandra?
7. **What is a Lightweight Transaction (LWT) in Cassandra?** What is a Lightweight Transaction (LWT) in Cassandra?
8. **How does consistent hashing distribute keys across the Cassandra token ring?** How does consistent hashing distribute keys across the Cassandra token ring?
9. **Why is SELECT * FROM table WHERE non_partition_key = 'val' prohibited without ALLOW FILTERING?** Why is SELECT * FROM table WHERE non_partition_key = 'val' prohibited without ALLOW FILTERING?
10. **What role does the CommitLog play in Cassandra write durability?** What role does the CommitLog play in Cassandra write durability?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Every node in the cluster plays an identical role; any node can coordinate any read or write request without a single point of failure.

#### Answer 2:
$R + W > N$, where $R$ is Read Consistency, $W$ is Write Consistency, and $N$ is Replication Factor.

#### Answer 3:
Partition Key determines which physical node in the token ring stores the row; Clustering Key determines the on-disk sorting order within that partition.

#### Answer 4:
Last-Write-Wins (LWW) based on microsecond client-side timestamps.

#### Answer 5:
A deletion marker recorded in SSTables; reading across deleted rows requires scanning all tombstones until compaction purges them.

#### Answer 6:
When reading with QUORUM, the coordinator compares data hashes; if a replica is stale, it sends the newest data in the background to update it.

#### Answer 7:
A linearizable compare-and-set operation (`IF NOT EXISTS` / `IF col = val`) powered by the Paxos consensus protocol.

#### Answer 8:
The partition key is hashed to a 64-bit integer (Murmur3Partitioner) and placed on the first node whose assigned token range covers that value.

#### Answer 9:
It forces the cluster to execute a full table scan across all nodes in the cluster, destroying distributed scalability.

#### Answer 10:
Writes are immediately appended to an on-disk sequential CommitLog before being stored in in-memory MemTables.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Design an IoT sensor telemetry schema partitioned by device and day bucket, ordered descending by timestamp.

### 🚀 Challenge 2: Architect Stretch Problem
Simulate a network partition and verify tunable quorum consistency behavior.

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

### D1. TombstoneOverwhelmingException on Wide-Row Scan

```sql
CREATE TABLE user_notifications (
    user_id uuid,
    notification_id timeuuid,
    is_read boolean,
    payload text,
    PRIMARY KEY (user_id, notification_id)
) WITH CLUSTERING ORDER BY (notification_id DESC);

-- Application cleanup query run every hour:
DELETE FROM user_notifications 
WHERE user_id = ? AND notification_id < ?;

-- Read query executed when user opens inbox:
SELECT * FROM user_notifications 
WHERE user_id = ? AND is_read = false 
LIMIT 20;
```

**Observed symptom:** Read query fails with: org.apache.cassandra.exceptions.ReadFailureException: Server failure during read query at consistency LOCAL_QUORUM (Scanned over 100001 tombstones in user_notifications; query aborted).

**(a)** What is a tombstone in Cassandra, and why did deleting old notifications break subsequent read queries?

**(b)** How can you view tombstone counts per SSTable using `nodetool` and sstable tools?

**(c)** What table design and operational adjustments eliminate tombstone scanning overhead?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In Cassandra (and LSM architectures), `DELETE` does not immediately remove data from disk. Instead, it writes a deletion marker called a **tombstone** with a timestamp. When reading data, Cassandra must scan all clustering rows—including tombstones—to determine whether data was deleted. By default, if a single query scans more than 100,000 tombstones (`tombstone_failure_threshold`), Cassandra aborts the query to prevent JVM heap exhaustion and Garbage Collection pauses.

**Diagnostic Commands:**
1. Check tombstone warnings in `system.log`:
   ```bash
   grep -i "tombstone" /var/log/cassandra/system.log
   ```
2. Inspect SSTable metadata using `sstablemetadata`:
   ```bash
   sstablemetadata /var/lib/cassandra/data/keyspace/user_notifications-*/nb-1-big-Data.db | grep -i "tombstone"
   ```
3. Check table statistics:
   ```bash
   nodetool tablestats keyspace.user_notifications
   ```

**Production Fix:**
1. **TTL Instead of DELETE:** Use native column/row TTL (`INSERT ... USING TTL 2592000`) and Time-Window Compaction Strategy (TWCS), which drops entire expired SSTables without generating tombstones.
2. **Bucket the Partition:** Partition by user and month/week (`PRIMARY KEY ((user_id, year_month), notification_id)`). To clear old data, drop old partition buckets rather than issuing cell-level `DELETE`.
3. **Tune GC Grace Seconds:** For tables where deleted data does not need resurrection protection for 10 days, lower `gc_grace_seconds` from 864,000 (10 days) to e.g. 86,400 (1 day) if repairs run frequently.

</details>

---

### D2. Last-Write-Wins (LWW) Silent Data Loss via Clock Skew

```python
# Microservice A on Host 1 (Clock skewed: 2026-09-08 10:05:00 UTC)
session.execute(
    "UPDATE accounts SET status = 'ACTIVE' WHERE account_id = %s",
    (acc_id,)
)

# Microservice B on Host 2 (Accurate NTP: 2026-09-08 10:00:00 UTC)
# Executed 2 minutes LATER in real time:
session.execute(
    "UPDATE accounts SET status = 'SUSPENDED' WHERE account_id = %s",
    (acc_id,)
)
```

**Observed symptom:** Even though Microservice B executed the SUSPENDED update 2 minutes after Microservice A, querying the database returns status = 'ACTIVE'. The later update was discarded.

**(a)** How does Cassandra's Last-Write-Wins (LWW) conflict resolution mechanism determine the winning mutation?

**(b)** How can you inspect the internal timestamp of a column cell in CQL?

**(c)** How do you guarantee monotonic write ordering or prevent clock skew anomalies in distributed systems?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Cassandra resolves concurrent writes to the same cell using **Last-Write-Wins (LWW)** based on microsecond-level timestamps generated either by the client driver or the coordinator node. Because Host 1's system clock was drifting 5 minutes into the future (+300s), its write carried timestamp $T + 300s$. When Host 2 issued its write at real time $T + 120s$, Cassandra compared timestamps: $(T + 300s) > (T + 120s)$, and silently ignored Host 2's mutation as an older update.

**Diagnostic Commands:**
1. Query the writetime of the cell in CQL:
   ```sql
   SELECT status, WRITETIME(status) FROM accounts WHERE account_id = 12345;
   ```
2. Verify clock synchronization across cluster and application servers:
   ```bash
   chronyc tracking   # or ntpstat / timedatectl
   ```

**Production Fix:**
1. **NTP Monitoring:** Maintain sub-millisecond clock synchronization across all Cassandra nodes and client application hosts using `chrony` with strict alerting on clock jitter > 5ms.
2. **Lightweight Transactions (LWT / Paxos):** When deterministic linearizable ordering is required, use Paxos conditional updates (`IF status = '...'`) which use ballot numbers rather than wall clocks:
   ```sql
   UPDATE accounts SET status = 'SUSPENDED' WHERE account_id = ? IF status = 'ACTIVE';
   ```

</details>

---

### D3. Wide-Row Latency Spike and Read Repair Storm

```sql
CREATE TABLE device_telemetry (
    device_type text,         -- e.g. "temperature_sensor"
    recorded_at timestamp,
    device_id text,
    reading double,
    PRIMARY KEY (device_type, recorded_at, device_id)
);

-- Inserted 500,000,000 records under device_type = 'temperature_sensor'
-- Query:
SELECT * FROM device_telemetry 
WHERE device_type = 'temperature_sensor' 
ORDER BY recorded_at DESC LIMIT 50;
```

**Observed symptom:** p99 read latency spikes to 8,000ms. Node JVM experiences consecutive 15-second Stop-The-World GC pauses. nodetool tpstats shows high ReadRepairStage and MutationStage backpressure.

**(a)** Why is partitioning by `device_type` a catastrophic anti-pattern in Cassandra?

**(b)** What is the recommended maximum partition size in Cassandra, and how do you inspect partition sizes with `nodetool`?

**(c)** How should the primary key be re-modeled to distribute telemetry evenly across the token ring?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Cassandra stores each partition as a contiguous structure on disk and in memory. The entire partition for `device_type = 'temperature_sensor'` hashes to a single token in the ring, concentrating hundreds of gigabytes onto a single primary node and its replicas. When querying this partition, Cassandra must load large index offsets into JVM heap, triggering violent Stop-The-World garbage collection pauses and read timeouts.

**Diagnostic Commands:**
1. Find large partitions:
   ```bash
   nodetool tablestats keyspace.device_telemetry | grep -i "compacted partition minimum bytes\|maximum bytes"
   ```
2. Check GC pauses:
   ```bash
   nodetool gcstats
   ```
3. Check thread pool drops:
   ```bash
   nodetool tpstats | grep ReadStage
   ```

**Production Fix:**
1. **Cassandra Partition Rule of Thumb:** Partition size must stay under **100MB** and fewer than 100,000 clustering cells.
2. **Compound Partition Key:** Partition by `(device_id, date)` so data is evenly dispersed across the token ring and bounded per day:
   ```sql
   CREATE TABLE device_telemetry (
       device_id text,
       day date,
       recorded_at timestamp,
       reading double,
       PRIMARY KEY ((device_id, day), recorded_at)
   ) WITH CLUSTERING ORDER BY (recorded_at DESC);
   ```

</details>

---

### D4. Secondary Index Scatter-Gather Timeout with ALLOW FILTERING

```sql
CREATE TABLE user_profiles (
    user_id uuid PRIMARY KEY,
    country_code text,
    email text,
    signup_date date
);

CREATE INDEX idx_users_country ON user_profiles(country_code);

-- Query executed by analytics dashboard:
SELECT * FROM user_profiles 
WHERE country_code = 'US' AND signup_date >= '2026-01-01' 
ALLOW FILTERING;
```

**Observed symptom:** Analytics query times out with NoHostAvailableException after 12 seconds. Cassandra nodes CPU spikes to 100% across all 12 nodes in the cluster simultaneously.

**(a)** How do 2i (secondary indexes) execute in Cassandra, and why is `ALLOW FILTERING` dangerous on large clusters?

**(b)** What tool or tracing command reveals the scatter-gather coordinator execution plan?

**(c)** What query-driven data modeling pattern replaces secondary indexes for high-throughput filtering?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Cassandra secondary indexes are **local indexes**, not global. Every node indexes only the partitions stored locally on that specific node. When querying by `country_code`, the coordinator node has no idea which node holds matching data, so it must issue a **scatter-gather broadcast** to every single node in the cluster. Adding `ALLOW FILTERING` forces every node to sequentially read and discard non-matching rows in memory across millions of partitions, causing cluster-wide CPU starvation.

**Diagnostic Commands:**
1. Run tracing in cqlsh:
   ```sql
   TRACING ON;
   SELECT * FROM user_profiles WHERE country_code = 'US' AND signup_date >= '2026-01-01' ALLOW FILTERING;
   ```
   Examine the trace: you will see `Executing single-partition query` executed thousands of times on all nodes.

**Production Fix:**
1. **Materialized Table / Query-First Modeling:** Create a query-specific table keyed by the search criteria:
   ```sql
   CREATE TABLE users_by_country_date (
       country_code text,
       signup_date date,
       user_id uuid,
       email text,
       PRIMARY KEY ((country_code, signup_date), user_id)
   );
   ```
2. Or use SASI (SSTable-Attached Secondary Indexes) for prefix search, or replicate data to Elasticsearch/OpenSearch for ad-hoc analytical queries.

</details>

---

### D5. Gossip Lag and WriteTimeoutException on Hint Hand-off Saturation

```python
# 3-Node Cassandra Cluster (Node 1, Node 2, Node 3)
# Replication factor: 3. Consistency Level: LOCAL_QUORUM (needs 2 acks)

# Node 2 undergoes a 4-hour hardware maintenance outage.
# Node 1 and Node 3 handle all writes and buffer mutations into Hints.
# Node 2 boots back up.
```

**Observed symptom:** As soon as Node 2 boots up, writes across the cluster begin failing with WriteTimeoutException: Operation timed out - received only 1 responses. Node 1 and 3 disk I/O climbs to 100% utilization.

**(a)** What are Hints in Cassandra, and why did Node 2's recovery overwhelm the remaining nodes?

**(b)** How do you monitor hinted handoff delivery and throttle hint dispatching?

**(c)** What is `max_hint_window_in_ms`, and what should be done if a node is offline longer than the window?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
When a replica is unreachable, coordinators store write mutations locally as **hints** for up to `max_hint_window_in_ms` (default 3 hours). If Node 2 was down for 4 hours, hints stopped accumulating after hour 3. When Node 2 came back, Node 1 and 3 immediately began streaming gigabytes of stored hints while simultaneously handling ongoing user writes and read repairs. The unthrottled hint replay saturated network and disk I/O, causing coordinators to drop client write acknowledgments within the 2,000ms write timeout.

**Diagnostic Commands:**
1. Check pending hints:
   ```bash
   nodetool getendpoints keyspace table key
   nodetool tpstats | grep -i hint
   ```
2. Check gossip status:
   ```bash
   nodetool gossipinfo
   nodetool status
   ```

**Production Fix:**
1. **Throttle Hint Delivery:** In `cassandra.yaml`:
   ```yaml
   hinted_handoff_throttle_in_kb: 10240   # Throttle hint replay to 10MB/s
   max_hints_delivery_threads: 2
   ```
2. **If node is down longer than 3 hours:** Do not rely on hints. Node 2 has missed mutations that were dropped after the 3-hour window. Immediately run a full repair on Node 2 upon recovery:
   ```bash
   nodetool repair -pr keyspace  # Partition-range repair
   ```

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
