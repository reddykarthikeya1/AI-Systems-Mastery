# Module 21 Storage Engine Internals BPlus Trees: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Storage Engine Internals: Disk Pages & B+ Trees** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **How does a Slotted-Page architecture organize variable-length records on a 4KB disk page?** How does a Slotted-Page architecture organize variable-length records on a 4KB disk page?
2. **Why are B+ Trees preferred over B-Trees for relational database indexing?** Why are B+ Trees preferred over B-Trees for relational database indexing?
3. **What happens during a B+ Tree node split when maximum capacity is exceeded?** What happens during a B+ Tree node split when maximum capacity is exceeded?
4. **What is the fan-out of a B+ Tree node, and how does it determine tree height?** What is the fan-out of a B+ Tree node, and how does it determine tree height?
5. **How does Lock Crabbing (Coupling) enable safe concurrent B+ Tree traversal?** How does Lock Crabbing (Coupling) enable safe concurrent B+ Tree traversal?
6. **What is the role of the Buffer Pool Manager in a database storage engine?** What is the role of the Buffer Pool Manager in a database storage engine?
7. **What is a dirty page in database storage internals?** What is a dirty page in database storage internals?
8. **Why do B+ Tree leaf nodes maintain sibling pointers?** Why do B+ Tree leaf nodes maintain sibling pointers?
9. **How does page fragmentation occur, and how do storage engines defragment slotted pages?** How does page fragmentation occur, and how do storage engines defragment slotted pages?
10. **What is the Write-Ahead Logging (WAL) invariant regarding dirty page flushing?** What is the Write-Ahead Logging (WAL) invariant regarding dirty page flushing?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Slots grow forward from page header storing (offset, length) pointers; tuple data grows backward from the end of the page.

#### Answer 2:
B+ Trees store data records exclusively in leaf nodes linked as a doubly-linked list, enabling high fan-out in internal nodes and fast sequential range scans.

#### Answer 3:
The node divides in half; the median key is promoted to the parent node, creating a new level if root splits.

#### Answer 4:
Fan-out is the number of child pointers per node. A fan-out of 100 on a 3-level tree indexes $100^3 = 1,000,000$ pages.

#### Answer 5:
A reader/writer acquires the child lock before releasing the parent lock, ensuring intermediate structural modifications do not corrupt traversal.

#### Answer 6:
It maintains an in-memory frame table of disk pages, handling page fetches, pin/unpin reference counting, and dirty-page flushing.

#### Answer 7:
A page modified in memory whose changes have not yet been flushed to the on-disk datafile.

#### Answer 8:
To execute range scans (`BETWEEN val1 AND val2`) sequentially across leaf pages without returning to the root.

#### Answer 9:
Deletions create dead gaps between records; defragmentation compacts active records to the end of the page and updates slot offsets.

#### Answer 10:
A dirty page cannot be written to disk until the WAL log record describing the modification has been flushed to disk (`page_lsn <= flushed_lsn`).

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement node splitting and root promotion in a disk-page-backed B+ Tree.

### 🚀 Challenge 2: Architect Stretch Problem
Build a Slotted Page manager in Python that packs variable-length records and compacts dead space.

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

### D1. Slotted Page Fragmentation and Table Bloat from Variable-Length Updates

```sql
-- PostgreSQL table storing variable-length JSON documents
CREATE TABLE user_sessions (
    session_id uuid PRIMARY KEY,
    user_id bigint,
    metadata text  -- Initially 50 bytes, updated to 800 bytes frequently
);

-- Application performs 500 UPDATEs per second on existing session_ids:
UPDATE user_sessions SET metadata = $new_expanded_json WHERE session_id = $id;
```

**Observed symptom:** Table size grows from 500 MB to 48 GB over 48 hours, even though the total number of active sessions remains fixed at 200,000. Read queries become 15x slower due to excessive page reads.

**(a)** How does a slotted page (page layout with line pointers and tuple data) handle row updates that outgrow available page free space?

**(b)** What is HOT (Heap-Only Tuples) optimization in Postgres, and why did these updates fail to qualify for HOT?

**(c)** How do you diagnose table bloat and tune `fillfactor` and `autovacuum` to prevent page fragmentation?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a slotted page architecture, a page header stores array pointers (line pointers) pointing to row offsets at the end of the 8KB page. When a row is updated in Postgres (MVCC), a new tuple version is created. If the updated row is larger than the remaining contiguous free space in the 8KB slotted page, Postgres cannot keep the new version on the same page. It must insert the new tuple onto a completely different page and update index pointers. Because `fillfactor` was 100% and rows expanded significantly, HOT optimization failed, resulting in massive heap fragmentation and dead tuple bloat.

**Diagnostic Commands:**
1. Check HOT update ratio:
   ```sql
   SELECT relname, n_tup_upd, n_tup_hot_upd,
          round(100.0 * n_tup_hot_upd / nullif(n_tup_upd, 0), 2) AS hot_ratio
   FROM pg_stat_user_tables WHERE relname = 'user_sessions';
   -- hot_ratio near 0% indicates failure to use Heap-Only Tuples.
   ```
2. Inspect bloat using `pgstattuple`:
   ```sql
   SELECT * FROM pgstattuple('user_sessions');
   ```

**Production Fix:**
1. **Lower `fillfactor`:** Leave free space on each 8KB page for updates to expand in-place without page jumping:
   ```sql
   ALTER TABLE user_sessions SET (fillfactor = 70);
   VACUUM FULL user_sessions;  -- Reclaim fragmented pages
   ```
2. **Aggressive Autovacuum:** Tune autovacuum to clean dead tuples continuously:
   ```sql
   ALTER TABLE user_sessions SET (
       autovacuum_vacuum_scale_factor = 0.05,
       autovacuum_vacuum_cost_limit = 1000
   );
   ```

</details>

---

### D2. B+ Tree Rightmost Leaf Latch Contention on Auto-Increment Primary Keys

```sql
CREATE TABLE telemetry_events (
    id BIGSERIAL PRIMARY KEY,  -- Monotonically increasing sequence
    device_id INT,
    event_payload JSONB
);

-- 64 concurrent worker threads executing high-frequency concurrent INSERTs:
INSERT INTO telemetry_events (device_id, event_payload) VALUES ($1, $2);
```

**Observed symptom:** Throughput plateaus at 8,000 inserts/sec despite high-end 64-core NVMe server. CPU utilization sits at 25% while threads spend 75% of their time waiting on LWLock (buffer_content / buf_mapping).

**(a)** Why do monotonically increasing sequential keys create a physical concurrency bottleneck in B+ Trees?

**(b)** What is latch contention on the rightmost leaf page of a B+ Tree?

**(c)** What primary key design patterns (such as reverse-key indexes, hash partitioning, or UUIDv7 with salt) relieve latch contention?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a B+ Tree, keys are kept strictly in sorted order. When using an auto-incrementing integer or sequential timestamp as the primary key, every single insert carries a key strictly greater than all existing keys. Consequently, 100% of concurrent insert transactions must acquire an exclusive write latch on the **exact same rightmost leaf page** of the B+ Tree. All 64 threads serialize behind this single 8KB page lock, resulting in massive latch contention and lock wait queues.

**Diagnostic Commands:**
1. Check wait events in `pg_stat_activity`:
   ```sql
   SELECT wait_event_type, wait_event, count(*)
   FROM pg_stat_activity
   WHERE state = 'active'
   GROUP BY wait_event_type, wait_event;
   -- Look for 'BufferContent' or 'BufferMapping' locks.
   ```

**Production Fix:**
1. **Hash Partitioning:** Partition the table across multiple physical B+ Trees using `PARTITION BY HASH (device_id)` with 16 or 32 partitions. Each partition has its own rightmost leaf page, spreading latch acquisition across 32 pages.
2. **Scatter Keys:** Prepend a random shard prefix or tenant ID to the key:
   ```sql
   id = (shard_id << 48) | nextval('telemetry_seq')
   ```
3. **Application-Side Micro-Batching:** Insert multi-row batches (`INSERT INTO ... VALUES (...), (...), (...)`) so a single latch acquisition writes 100 rows rather than acquiring and releasing the latch 100 times.

</details>

---

### D3. Dirty Page Writeback Starvation and Checkpoint Flush Avalanche

```python
# postgresql.conf
shared_buffers = 32GB
max_wal_size = 1GB
checkpoint_timeout = 5min
checkpoint_completion_target = 0.1  # Fast checkpoint flush
```

**Observed symptom:** Every 5 minutes, query throughput plummets to near zero for 20 seconds. Disk write bandwidth spikes to 2.5 GB/s, saturating storage controller and causing client timeouts.

**(a)** What occurs during a database checkpoint, and why did this configuration create a flush avalanche?

**(b)** What role does the background writer (`bgwriter`) play in smoothing out buffer pool writeback?

**(c)** How should `max_wal_size`, `checkpoint_timeout`, and `checkpoint_completion_target` be configured for smooth I/O?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A **checkpoint** flushes all dirty buffer pool pages modified prior to the checkpoint LSN to disk so the WAL can be safely recycled. With `checkpoint_completion_target = 0.1` and `checkpoint_timeout = 5min`, Postgres attempts to flush all gigabytes of accumulated dirty pages within the first 10% of the interval (30 seconds). This floods the storage controller with an enormous burst of I/O writes, starving regular transaction query processing and WAL writes. Furthermore, `max_wal_size = 1GB` is too small for heavy write workloads, triggering checkpoints prematurely.

**Diagnostic Commands:**
1. Inspect checkpoint statistics in `pg_stat_bgwriter`:
   ```sql
   SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time, checkpoint_sync_time, buffers_checkpoint
   FROM pg_stat_bgwriter;
   -- High checkpoints_req indicates max_wal_size is being exceeded before timeout.
   ```

**Production Fix:**
1. **Spread Checkpoint I/O Evenly:** Set `checkpoint_completion_target = 0.9`. This instructs Postgres to spread the dirty page writes smoothly over 90% of the checkpoint interval:
   ```conf
   checkpoint_timeout = 15min
   checkpoint_completion_target = 0.9
   max_wal_size = 16GB
   min_wal_size = 2GB
   ```
2. **Tune Background Writer:** Enable `bgwriter` to proactively flush dirty buffers ahead of server demands:
   ```conf
   bgwriter_delay = 20ms
   bgwriter_lru_maxpages = 200
   bgwriter_lru_multiplier = 3.0
   ```

</details>

---

### D4. Double-Write Buffer and WAL Write Amplification in Crash Recovery

```python
# MySQL InnoDB Configuration
innodb_doublewrite = 1
innodb_flush_log_at_trx_commit = 1
sync_binlog = 1

# Workload: 10,000 tiny single-row updates/sec (updating a 4-byte counter)
```

**Observed symptom:** Storage write throughput shows 180 MB/s of physical disk writes, even though user data changes account for only 40 KB/s. SSD wear-out indicators advance rapidly.

**(a)** What is the 'torn page' problem in database storage engines, and why does MySQL use a Doublewrite Buffer?

**(b)** Why does a 4-byte update generate multiple 16KB page writes across WAL, binlog, and doublewrite buffer?

**(c)** How do modern filesystems (ZFS/ext4 with O_DIRECT) or atomic write SSDs allow safely disabling doublewrite buffers?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Operating system and disk sector sizes are typically 512 bytes or 4KB, whereas database pages are 16KB (InnoDB) or 8KB (PostgreSQL). If a crash occurs in the middle of writing a 16KB page to disk, the page is left half-written—a **torn page**—which corrupts the B+ Tree structure beyond recovery by normal WAL replay. To prevent this, InnoDB first writes the complete page to a contiguous **Doublewrite Buffer** on disk before writing it to its physical table location. Thus, a tiny 4-byte update writes: (1) Redo log buffer + fsync, (2) Binary log + fsync, (3) 16KB to Doublewrite buffer, (4) 16KB to table tablespace $pprox$ massive write amplification.

**Diagnostic Commands:**
1. Check InnoDB doublewrite metrics:
   ```sql
   SHOW GLOBAL STATUS LIKE 'Innodb_dblwr%';
   -- Innodb_dblwr_pages_written vs Innodb_pages_written
   ```

**Production Fix:**
1. **Use Atomic Writes (if supported):** Modern NVMe SSDs or enterprise storage controllers (like AWS EBS or ZFS filesystems with copy-on-write semantics) provide atomic 16KB block writes. On these systems, torn pages are physically impossible:
   ```cnf
   innodb_doublewrite = 0
   ```
2. **Batch Updates / Group Commits:** Allow MySQL to flush multiple transactions in a single fsync via group commit, drastically reducing WAL fsync calls.

</details>

---

### D5. Dangling Buffer Pool Row Pointer and Pin Count Race Condition

```cypher
// C / C++ Custom Storage Engine implementation
void* fetch_row(PageId page_id, int slot_id) {
    Page* page = buffer_pool.get_page(page_id); // Acquires latch, increments pin count
    Row* row = page->get_row_ptr(slot_id);
    buffer_pool.unpin(page_id);                  // Pin count decremented to 0
    return row;                                 // Returns raw memory pointer
}

void worker_thread() {
    Row* row = fetch_row(104, 3);
    do_slow_computation();                      // Takes 50ms
    printf("User balance: %d\n", row->balance);  // Read from pointer
}
```

**Observed symptom:** Intermittent segmentation faults or corrupted data printed under high concurrency. balance randomly prints garbage integers or negative values.

**(a)** What is the purpose of 'pinning' a page in a buffer pool manager?

**(b)** What happens when a page's pin count drops to 0 while an application thread still holds a pointer to its memory?

**(c)** How must cursor lifetime, page latching, and page pinning be structured to guarantee memory safety?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a buffer pool manager, **pinning** a page (`pin_count > 0`) informs the buffer eviction algorithm (LRU, CLOCK, or 2Q) that the page is currently being accessed and **must not be evicted or replaced**. The function `fetch_row` unpins the page immediately upon return. During `do_slow_computation()`, another thread requests a new page, and the buffer eviction algorithm selects Page 104 (since `pin_count == 0`), overwriting its memory frame with completely different data from disk. When `worker_thread` subsequently accesses `row->balance`, it reads garbage memory from the new page (use-after-free / eviction race).

**Diagnostic Commands:**
1. Run with AddressSanitizer (ASan) or Valgrind:
   `AddressSanitizer: heap-use-after-free` or invalid memory read.
2. Log buffer eviction events matching `page_id == 104`.

**Production Fix:**
1. **Hold Pin for Lifetime of Access:** The worker thread must hold the pin until it is finished reading the tuple:
   ```cpp
   PageHandle handle = buffer_pool.pin_page(page_id);
   Row* row = handle.get_page()->get_row(slot_id);
   // Read data or copy to local struct
   int balance = row->balance;
   handle.release(); // Unpins page
   ```
2. **Copy on Access:** If computation is long, deserialize or copy the row data into a thread-local object and immediately release the buffer pool page lock and pin.

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
