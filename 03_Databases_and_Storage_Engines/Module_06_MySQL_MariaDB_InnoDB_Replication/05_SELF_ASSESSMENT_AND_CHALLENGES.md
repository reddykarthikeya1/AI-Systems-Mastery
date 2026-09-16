# Module 06 MySQL MariaDB InnoDB Replication: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **MySQL & InnoDB Architecture, Buffer Pool & Replication** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **How does InnoDB's Clustered Index architecture differ from secondary indexes?** How does InnoDB's Clustered Index architecture differ from secondary indexes?
2. **What is the purpose of the InnoDB Doublewrite Buffer?** What is the purpose of the InnoDB Doublewrite Buffer?
3. **Explain the difference between Statement-Based Replication (SBR) and Row-Based Replication (RBR).?** Explain the difference between Statement-Based Replication (SBR) and Row-Based Replication (RBR).
4. **What is a Global Transaction Identifier (GTID) in MySQL replication?** What is a Global Transaction Identifier (GTID) in MySQL replication?
5. **How does InnoDB detect and resolve deadlocks?** How does InnoDB detect and resolve deadlocks?
6. **What role does the InnoDB Redo Log (ib_logfile) play during crash recovery?** What role does the InnoDB Redo Log (ib_logfile) play during crash recovery?
7. **How does the InnoDB Buffer Pool LRU list prevent full table scans from evicting cached OLTP pages?** How does the InnoDB Buffer Pool LRU list prevent full table scans from evicting cached OLTP pages?
8. **What is the difference between binlog_format = MIXED and ROW?** What is the difference between binlog_format = MIXED and ROW?
9. **Why does multi-threaded replication (MTR) reduce replication lag on replicas?** Why does multi-threaded replication (MTR) reduce replication lag on replicas?
10. **What is the difference between semi-synchronous replication and asynchronous replication in MySQL?** What is the difference between semi-synchronous replication and asynchronous replication in MySQL?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
The table's primary key forms the clustered index where leaf nodes store the actual row data. Secondary indexes store the primary key value as their pointer.

#### Answer 2:
It writes dirty pages to a contiguous disk buffer before writing to primary data files, preventing page corruption from torn writes during crashes.

#### Answer 3:
SBR transmits SQL statements (prone to non-deterministic divergence, e.g. NOW()); RBR transmits exact before/after row byte changes.

#### Answer 4:
A unique identifier assigned to every committed transaction across a cluster, allowing seamless replica failover without parsing binlog file offsets.

#### Answer 5:
It automatically detects cycles in its wait-for graph and rolls back the transaction with the fewest undo log records (least expensive to undo).

#### Answer 6:
It provides Write-Ahead Logging; upon restart, InnoDB replays committed transactions from the redo log that had not yet reached data pages.

#### Answer 7:
It divides the LRU list into 'young' (5/8) and 'old' (3/8) sublists; pages accessed during scans must remain active for `innodb_old_blocks_time` before entering the young list.

#### Answer 8:
MIXED uses statement-based logging by default, switching to row-based only when non-deterministic functions or triggers are invoked.

#### Answer 9:
It allows the replica applier thread to apply non-conflicting transactions across different databases or transaction dependency sets in parallel.

#### Answer 10:
Async commits on primary without waiting; semi-sync waits for at least one replica to acknowledge receiving the binlog event into its relay log.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Configure a master-replica GTID topology and verify zero-loss failover under simulated primary crash.

### 🚀 Challenge 2: Architect Stretch Problem
Trigger an InnoDB deadlock using two concurrent threads updating rows in inverted order and parse the deadlock graph.

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

### D1. Secondary index bookmark lookup thrashing on non-covering query

```sql
-- users table: PK is user_id. Secondary index on email.
SELECT user_id, email, phone_number, home_address 
FROM users 
WHERE email = 'alice@example.com';
```

**Observed symptom:** Under high concurrency (20,000 req/sec), CPU spikes to 100% and buffer pool read IOPS saturate disk.

**(a)** Why does querying `phone_number` require a secondary index bookmark lookup in MySQL InnoDB?

**(b)** How does InnoDB's clustered index architecture differ from heap-table architectures in PostgreSQL?

**(c)** How does creating a Covering Index with composite columns or USING INDEX eliminate heap seeks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** In InnoDB, secondary indexes do not point directly to physical page offsets; they store the Primary Key as a **bookmark**. Querying columns not in the secondary index (`phone_number`, `home_address`) requires an extra clustered index B-Tree lookup for every matched row.

**Covering Index Fix:** Create a composite index containing all queried columns: `CREATE INDEX idx_email_covering ON users (email, phone_number, home_address);`.

**Outcome:** Allows InnoDB to satisfy the query directly from the secondary index leaf page (`Using index` in EXPLAIN) without double-traversal.

</details>

---

### D2. Replication lag spike caused by single-threaded replica SQL thread

```sql
-- Master executes bulk migration:
UPDATE orders SET archived = TRUE WHERE created_at < '2025-01-01'; -- 5,000,000 rows
-- Replica Seconds_Behind_Master jumps from 0 to 4,200 seconds!
```

**Observed symptom:** Read-replicas serve stale data for over an hour; failover tools declare replicas out of sync.

**(a)** Why does a single multi-million row UPDATE statement stall MySQL binlog replication?

**(b)** What is the difference between Statement-Based Replication (SBR) and Row-Based Replication (RBR)?

**(c)** How does multi-threaded replica configuration (`slave_parallel_workers`) mitigate replication lag?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A massive single-transaction UPDATE is serialized into the binary log. Even with multi-threaded replication, a single transaction cannot be split across multiple worker threads and must be executed sequentially by a single replica thread.

**Fix:** Chunk large batch operations into small transactions (e.g. 5,000 rows per commit with sleep intervals):
```sql
UPDATE orders SET archived = TRUE WHERE created_at < '2025-01-01' LIMIT 5000;
```
**Configuration:** Configure `replica_parallel_type = LOGICAL_CLOCK` and `replica_parallel_workers = 8`.

</details>

---

### D3. Deadlock on INSERT ... ON DUPLICATE KEY UPDATE under concurrent workers

```sql
-- Two workers concurrently insert the same user with unique secondary key:
INSERT INTO users (id, email, visits) 
VALUES (1, 'user@test.com', 1) 
ON DUPLICATE KEY UPDATE visits = visits + 1;
```

**Observed symptom:** MySQL aborts Worker 2 with `ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction`.

**(a)** Why does `ON DUPLICATE KEY UPDATE` take gap locks and next-key locks on unique secondary indexes?

**(b)** What lock mode is acquired on the duplicate index record before the update?

**(c)** How does replacing this with Redis atomic counter or optimistic application locking prevent deadlocks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** When evaluating duplicate keys on secondary unique indexes, InnoDB acquires an **Exclusive Next-Key Lock** covering the gap prior to the record. When two transactions race on the same gap, they obtain shared locks and then mutually wait for exclusive upgrade, deadlocking.

**Fix:** Update counters in high-throughput in-memory stores like Redis (`HINCRBY user:1 visits 1`) and periodically persist aggregate tallies to MySQL.

</details>

---

### D4. InnoDB buffer pool thrashing caused by full table scan on reporting query

```sql
-- Midnight analytical query runs on OLTP production master:
SELECT customer_id, SUM(total) 
FROM orders 
GROUP BY customer_id;
```

**Observed symptom:** Immediately after the query starts, p99 latency for OLTP transactions jumps from 2 ms to 150 ms across the application.

**(a)** How did the full table scan evict hot cached OLTP pages from the InnoDB Buffer Pool?

**(b)** What is the InnoDB midpoint insertion LRU algorithm and the `innodb_old_blocks_time` setting?

**(c)** What setting prevents transient batch scans from evicting warm operational cache blocks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A massive sequential table scan loads cold disk pages into the InnoDB Buffer Pool, displacing hot working-set pages used by active OLTP transactions.

**Buffer Pool Protection:** InnoDB uses a 3/8 split LRU queue (`innodb_old_blocks_pct = 37`). New pages are inserted at the midpoint. Crucially, `innodb_old_blocks_time` (default 1000ms) dictates that a page must be accessed *longer than 1000 ms after first read* to move to the young sublist.

**Fix:** Ensure `innodb_old_blocks_time = 1000` is active and offload reporting queries to dedicated read replicas.

</details>

---

### D5. Auto-increment gap exhaustion under transaction rollbacks

```sql
-- High-volume order ingestion (10,000 rollbacks per minute):
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (101, 50.0);
-- Validation error occurs -> ROLLBACK;
```

**Observed symptom:** A table with only 100,000 active records exhausts a standard 32-bit signed `INT` primary key (ID exceeds 2,147,483,647).

**(a)** Why are auto-increment counter sequences never rolled back when an INSERT transaction aborts?

**(b)** What catastrophic database error occurs when a primary key auto-increment counter reaches maximum value?

**(c)** What data type should always be used for primary key identifiers in high-volume production tables?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** For concurrency performance, the auto-increment mutex generates sequential values immediately. If aborted transactions rolled back the counter, it would cause severe serialization bottlenecks and duplicate key collisions with subsequent transactions.

**Failure Mode:** When signed `INT` hits 2,147,483,647, subsequent `INSERT` operations fail with `ERROR 1062: Duplicate entry '2147483647' for key 'PRIMARY'`, causing a total write outage.

**Fix:** Always define primary keys with `BIGINT UNSIGNED` (up to $1.8 	imes 10^{19}$ IDs).

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
