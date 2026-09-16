# Module 15 LSM Trees Compaction DynamoDB: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Why do LSM-Trees (Log-Structured Merge-Trees) provide higher write throughput than B+ Trees?** Why do LSM-Trees (Log-Structured Merge-Trees) provide higher write throughput than B+ Trees?
2. **What is the role of a Bloom Filter in an SSTable read path?** What is the role of a Bloom Filter in an SSTable read path?
3. **Explain Leveled Compaction vs Size-Tiered Compaction in LSM storage.?** Explain Leveled Compaction vs Size-Tiered Compaction in LSM storage.
4. **How does Amazon DynamoDB Single-Table Design represent 1:N relationships?** How does Amazon DynamoDB Single-Table Design represent 1:N relationships?
5. **What is the difference between DynamoDB RCU and WCU billing units?** What is the difference between DynamoDB RCU and WCU billing units?
6. **What is a Global Secondary Index (GSI) in DynamoDB?** What is a Global Secondary Index (GSI) in DynamoDB?
7. **How do conditional writes prevent concurrent overwrite bugs in DynamoDB?** How do conditional writes prevent concurrent overwrite bugs in DynamoDB?
8. **What causes hot partition throttling in DynamoDB?** What causes hot partition throttling in DynamoDB?
9. **What is Write Amplification in storage engines?** What is Write Amplification in storage engines?
10. **Why are SSTables immutable once written to disk?** Why are SSTables immutable once written to disk?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
LSM-Trees convert random writes into sequential writes by buffering in memory (MemTable) and writing sequential immutable SSTables to disk.

#### Answer 2:
It probabilistically confirms if a key definitely does NOT exist in an SSTable, skipping expensive disk I/O.

#### Answer 3:
Size-Tiered merges SSTables of similar sizes into larger tables (optimal for writes); Leveled maintains non-overlapping key ranges per level (optimal for reads).

#### Answer 4:
Using composite Partition Keys (PK) and Sort Keys (SK) to group related entities (e.g. Customer and Orders) in the same physical partition.

#### Answer 5:
1 WCU = 1 write up to 1KB/s; 1 RCU = 1 strongly consistent read (or 2 eventually consistent reads) up to 4KB/s.

#### Answer 6:
An alternate index with a different PK and SK partitioned and replicated asynchronously across the cluster.

#### Answer 7:
Using `ConditionExpression = 'attribute_not_exists(PK)'` or checking version numbers before applying mutations.

#### Answer 8:
Exceeding 1,000 WCU or 3,000 RCU on a single physical partition due to skewed access patterns.

#### Answer 9:
The ratio of physical bytes written to storage media relative to logical bytes written by the user application.

#### Answer 10:
Immutability eliminates locking and concurrency hazards during reads and makes background compaction trivial.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement an in-memory LSM storage engine with MemTable flushing and SSTable binary search.

### 🚀 Challenge 2: Architect Stretch Problem
Design a DynamoDB single-table schema modeling an e-commerce order management system.

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

### D1. LSM Write Stall on Level-0 SSTable Pileup

```python
# RocksDB / LevelDB Storage Engine Configuration
options.write_buffer_size = 64 * 1024 * 1024       # 64MB MemTable
options.level0_file_num_compaction_trigger = 4
options.level0_slowdown_writes_trigger = 8
options.level0_stop_writes_trigger = 12

# Ingestion script writing 50,000 rows/sec using Put()
```

**Observed symptom:** Write ingestion throughput suddenly collapses from 50,000 ops/sec to 0 for 4-8 seconds at a time. Storage logs show: 'Stalling writes because we have 12 L0 files; compaction is lagging behind'.

**(a)** Why does Level 0 in an LSM-tree have key overlaps, and why does a backlog of L0 files force write stalls?

**(b)** What metrics in RocksDB/Cassandra expose pending compaction bytes and write stall durations?

**(c)** How can compaction concurrency and MemTable flushing be tuned to eliminate write stalls?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
When a MemTable fills up, it is flushed to disk as an immutable SSTable in Level 0 (L0). Unlike Levels 1 through N (where keys are non-overlapping and sorted), L0 SSTables have overlapping key ranges because each file represents a snapshot of MemTable keys at a different point in time. Therefore, every point read must check *every* L0 SSTable. To prevent read amplification from spiraling out of control, the engine deliberately stalls or stops incoming writes (`level0_stop_writes_trigger`) when L0 compaction threads cannot keep up with flush speed.

**Diagnostic Commands:**
1. Check RocksDB statistics / LOG:
   ```text
   ** Compaction Stats [default] **
   Level   Files   Size     Score
   L0       12/4   768 MB   3.0   (Compaction pending)
   ```
2. In Cassandra:
   ```bash
   nodetool compactionstats
   ```

**Production Fix:**
1. Increase compaction thread concurrency:
   ```python
   options.max_background_jobs = 8        # Allow parallel flushes and compactions
   options.max_subcompactions = 4          # Parallelize single large SSTable compactions
   ```
2. Increase write buffer and trigger thresholds:
   ```python
   options.level0_file_num_compaction_trigger = 8
   options.level0_slowdown_writes_trigger = 20
   options.level0_stop_writes_trigger = 36
   options.write_buffer_size = 128 * 1024 * 1024
   ```
3. Use dedicated fast NVMe SSD storage with high random I/O write capability.

</details>

---

### D2. Bloom Filter False Positive Rate Causing Excessive Disk Seeks

```python
# LSM-tree custom implementation / configuration
# Bloom filter initialized with 3 bits per key
bloom_bits_per_key = 3   # Yields ~30% false positive probability

def get(key: bytes):
    if key in memtable:
        return memtable[key]
    for sstable in sstables:
        if sstable.bloom_filter.contains(key):
            # Disk seek and block read
            val = sstable.read_block(key)
            if val is not None:
                return val
    return None
```

**Observed symptom:** When looking up non-existent keys (cache-miss pattern), disk read IOPS spikes to 25,000 IOPS and p99 query latency jumps from 0.4ms to 35ms, even though 99% of queried keys do not exist in the database.

**(a)** How does a Bloom filter accelerate point lookups in LSM SSTables, and how does `bits_per_key` impact false positive rate?

**(b)** What mathematical formula relates bits per key $m/n$ to false positive probability $p$?

**(c)** What is the industry standard bits-per-key allocation for LSM engines, and how much RAM is required?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A Bloom filter is a space-efficient probabilistic data structure that answers whether an element is *definitely not* in the set or *might be* in the set. If the filter returns false, the SSTable can be completely skipped without touching disk. With only 3 bits per key, the false positive probability is approximately $30\%$. This means for every query of a non-existent key across 10 SSTables, the engine performs on average 3 unnecessary disk I/O seeks and block decodes.

**Mathematical Proof:**
The optimal false positive rate is:
$$p pprox \left(rac{1}{2}ight)^{\ln(2) \cdot rac{m}{n}} pprox 0.6185^{m/n}$$
- At $m/n = 3$: $p pprox 23.7\%$
- At $m/n = 10$: $p pprox 0.8\%$ to $1\%$
- At $m/n = 14$: $p pprox 0.1\%$

**Production Fix:**
Allocate **10 bits per key** (approx. 1.25 bytes per entry in RAM):
```python
# In RocksDB:
options.table_factory = rocksdb.BlockBasedTableFactory(
    filter_policy=rocksdb.NewBloomFilterPolicy(bits_per_key=10)
)
```
For 100 million keys, 10 bits/key requires only $pprox 120	ext{ MB}$ of RAM and reduces disk reads for missing keys by 99%.

</details>

---

### D3. DynamoDB Hot Partition Throttling via Hash Skew

```python
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FlashSaleOrders')

# Partition Key: status (String: 'PENDING', 'PROCESSED', 'SHIPPED')
# Sort Key: order_id (String)

def record_order(order_id: str, payload: dict):
    table.put_item(
        Item={
            'status': 'PENDING',  # 99.8% of all incoming writes use 'PENDING'
            'order_id': order_id,
            **payload
        }
    )
```

**Observed symptom:** Client receives botocore.exceptions.ClientError: An error occurred (ProvisionedThroughputExceededException) when calling the PutItem operation. CloudWatch shows the table has 5,000 WCU provisioned, but total consumption is only 1,050 WCU.

**(a)** Why is the table throttled even though total consumed capacity is well below the provisioned 5,000 WCU?

**(b)** What is the maximum throughput limit per individual physical partition in DynamoDB?

**(c)** How do you redesign the partition key with synthetic sharding / salt to distribute writes?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
DynamoDB distributes tables across multiple internal storage partitions based on the MD5 hash of the **Partition Key**. An individual physical partition has a hard limit of **1,000 WCU** and **3,000 RCU**. When 5,000 WCU is provisioned, DynamoDB spreads that across at least 5 physical partitions. Because 99.8% of writes use `status = 'PENDING'`, all writes are routed to the single physical partition responsible for that key hash, capping write throughput at 1,000 WCU.

**Diagnostic Commands:**
1. Check CloudWatch metrics for `ProvisionedThroughputExceededEvents` vs `ConsumedWriteCapacityUnits`.
2. Inspect CloudWatch Contributor Insights for DynamoDB to identify the exact hot partition keys.

**Production Fix:**
Use **Synthetic Partition Key Sharding (Write Salting)**:
```python
import random

NUM_SHARDS = 10  # Distribute across 10 partitions -> up to 10,000 WCU

def record_order(order_id: str, payload: dict):
    shard_id = random.randint(0, NUM_SHARDS - 1)
    table.put_item(
        Item={
            'partition_key': f"PENDING#{shard_id}",
            'order_id': order_id,
            **payload
        }
    )
```
Workers reading pending orders can query each shard in parallel (`PENDING#0` through `PENDING#9`).

</details>

---

### D4. Size-Tiered Compaction Strategy (STCS) Disk Headroom Exhaustion

```sql
-- Table configuration using Size-Tiered Compaction Strategy (STCS)
CREATE TABLE user_activity_log (
    user_id uuid,
    activity_time timestamp,
    action text,
    PRIMARY KEY (user_id, activity_time)
) WITH compaction = {'class': 'SizeTieredCompactionStrategy'};

-- Disk size: 1.0 TB total. Current data volume: 680 GB (68% disk used).
```

**Observed symptom:** Compaction begins merging 4 large SSTables (160GB each). 2 hours into compaction, the node crashes with java.io.IOException: No space left on device. The node enters a crash loop and cannot boot.

**(a)** Why does Size-Tiered Compaction require up to 50% free disk space headroom?

**(b)** How does Leveled Compaction Strategy (LCS) differ in terms of disk headroom requirements?

**(c)** How can an administrator recover a node with a full disk without corrupting SSTables?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In Size-Tiered Compaction (STCS), Cassandra merges 4 SSTables of similar size into 1 new, larger SSTable. During the compaction process, the original 4 SSTables must remain on disk to answer read queries until the new SSTable is fully written and fsynced. Therefore, merging four 160GB SSTables ($4 	imes 160	ext{ GB} = 640	ext{ GB}$) requires an additional 640GB of free space simultaneously. Since the node only had 320GB available, disk filled up completely.

**Diagnostic Commands:**
1. Check disk utilization:
   ```bash
   df -h /var/lib/cassandra/data
   ```
2. Check ongoing compactions:
   ```bash
   nodetool compactionstats
   ```

**Production Fix:**
1. **Disk Headroom Rule for STCS:** Never allow disk utilization to exceed **50%** when using STCS.
2. **Switch to Leveled Compaction Strategy (LCS):** LCS breaks data into small, fixed-size SSTables (typically 160MB). Compaction merges small files, requiring only **10%** disk headroom:
   ```sql
   ALTER TABLE user_activity_log WITH compaction = {'class': 'LeveledCompactionStrategy'};
   ```
3. **Emergency Recovery:**
   - Temporarily mount an external disk and move older SSTable files.
   - Run `nodetool stop COMPACTION` on boot if possible.
   - Or run `sstable-scrub` after freeing space.

</details>

---

### D5. DynamoDB Global Secondary Index (GSI) Write Throttling Backpressure

```python
# Main Table: 'Orders' (Provisioned: 4000 WCU, 4000 RCU)
# Global Secondary Index: 'CustomerEmailIndex' (Provisioned: 200 WCU, 200 RCU)

import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

# Application inserting into main table
table.put_item(
    Item={
        'order_id': 'ord_987123',
        'customer_email': 'shopper@example.com',
        'total': 120.50
    }
)
```

**Observed symptom:** PutItem writes to the main 'Orders' table fail with ProvisionedThroughputExceededException, even though main table write consumption is only 300 WCU against its 4,000 WCU limit.

**(a)** Why does an undersized Global Secondary Index (GSI) cause write failures on the main table?

**(b)** What CloudWatch metric confirms GSI-induced backpressure?

**(c)** How should GSIs be provisioned, and when should DynamoDB on-demand capacity or sparse GSIs be used?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
When an item is inserted or updated in a DynamoDB table, any Global Secondary Index that indexes an attribute present in the item must be updated asynchronously by DynamoDB's internal replication engine. If the GSI does not have enough Write Capacity Units (WCUs) to keep up with the write rate of the main table, DynamoDB throttles writes to the **main table** to prevent the GSI from falling indefinitely behind.

**Diagnostic Commands:**
1. Check CloudWatch metric:
   `OnlineIndexPercentageProgress` and `IndexThrottleEvents` on `CustomerEmailIndex`.
2. Compare `ConsumedWriteCapacityUnits` between base table and index.

**Production Fix:**
1. **Match Provisioning:** Ensure GSI WCU is provisioned to equal or exceed the base table's WCU (or enable Auto Scaling on both base table and GSIs).
2. **Switch to On-Demand Billing:** If traffic is spiky, use `PAY_PER_REQUEST` billing so both the table and its GSIs scale automatically without provisioned limits.
3. **Sparse Indexing:** Only include `customer_email` on items that actually need GSI indexing. If an item does not contain the GSI partition key, it will not be written to the GSI, saving GSI WCU.

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
