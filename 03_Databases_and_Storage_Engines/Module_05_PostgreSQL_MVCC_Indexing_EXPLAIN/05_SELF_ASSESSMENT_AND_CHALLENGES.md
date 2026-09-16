# Module 05 PostgreSQL MVCC Indexing EXPLAIN: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **PostgreSQL MVCC, Vacuuming & Execution Plans** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **How does PostgreSQL implement Multi-Version Concurrency Control (MVCC) without in-place updates?** How does PostgreSQL implement Multi-Version Concurrency Control (MVCC) without in-place updates?
2. **What is the purpose of the PostgreSQL Visibility Map?** What is the purpose of the PostgreSQL Visibility Map?
3. **What happens during a standard VACUUM vs VACUUM FULL?** What happens during a standard VACUUM vs VACUUM FULL?
4. **Why does EXPLAIN (ANALYZE, BUFFERS) provide more actionable insight than plain EXPLAIN?** Why does EXPLAIN (ANALYZE, BUFFERS) provide more actionable insight than plain EXPLAIN?
5. **What is the difference between a Sequential Scan, an Index Scan, and a Bitmap Index Scan?** What is the difference between a Sequential Scan, an Index Scan, and a Bitmap Index Scan?
6. **What is Transaction ID (XID) wraparound, and how does PostgreSQL prevent data loss?** What is Transaction ID (XID) wraparound, and how does PostgreSQL prevent data loss?
7. **Why should you always create production indexes using CREATE INDEX CONCURRENTLY?** Why should you always create production indexes using CREATE INDEX CONCURRENTLY?
8. **What is a Partial Index, and when should you use one?** What is a Partial Index, and when should you use one?
9. **How does a B-Tree index handle high-cardinality vs low-cardinality columns?** How does a B-Tree index handle high-cardinality vs low-cardinality columns?
10. **What is HOT (Heap-Only Tuples) optimization in PostgreSQL?** What is HOT (Heap-Only Tuples) optimization in PostgreSQL?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Every UPDATE writes a completely new tuple version to the heap page, populating `xmin` (creation transaction) and `xmax` (deletion transaction).

#### Answer 2:
It tracks which heap pages contain only tuples visible to all current transactions, allowing index-only scans to skip checking heap pages.

#### Answer 3:
Standard VACUUM marks dead tuple space as reusable without shrinking file size; VACUUM FULL rewrites the table into a new file and reclaims disk space under an exclusive lock.

#### Answer 4:
Plain EXPLAIN shows planner estimates; ANALYZE actually executes the query and reports real runtime, while BUFFERS shows exact shared buffer cache hits and disk reads.

#### Answer 5:
Seq Scan reads all heap pages; Index Scan navigates B-Tree to fetch heap tuples individually; Bitmap Index Scan builds an in-memory bitmap of matching pages before reading them sequentially.

#### Answer 6:
PostgreSQL 32-bit transaction counters wrap around after 2 billion transactions. Autovacuum freeze runs freeze older tuples with FrozenXID to prevent them from appearing in the future.

#### Answer 7:
Standard CREATE INDEX locks the table against all writes; CONCURRENTLY runs two scans without blocking concurrent DML.

#### Answer 8:
An index created with a WHERE clause (e.g. `WHERE status = 'PENDING'`), keeping the index compact and fast for specific query filters.

#### Answer 9:
B-Trees excel on high-cardinality keys. On low-cardinality keys (boolean/status), B-Trees provide minimal selectivity unless combined in composite or partial indexes.

#### Answer 10:
When an update does not modify indexed columns and the new tuple fits on the same page, PostgreSQL links them without creating new index entries.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Analyze query plan changes between Index Scan and Bitmap Heap Scan by adjusting random_page_cost.

### 🚀 Challenge 2: Architect Stretch Problem
Simulate high dead tuple bloat using repeated concurrent UPDATEs and observe autovacuum reclamation behavior.

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

### D1. Long-running analytical transaction pinning oldest xmin

```sql
-- Data analyst starts a reporting query and leaves their workstation:
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM huge_sales_log;
-- Transaction remains open for 14 hours...
```

**Observed symptom:** Production OLTP database runs out of disk space; table sizes double; `VACUUM` log reports `0 dead tuples removed; 850,000 dead tuples remain unremovable`.

**(a)** Why does a single open snapshot in REPEATABLE READ prevent VACUUM from purging dead tuples across all other tables?

**(b)** What catalog view exposes the oldest active transaction xmin blocking vacuum?

**(c)** What database setting automatically aborts idle transactions before bloat occurs?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** PostgreSQL `VACUUM` can only purge dead tuples whose `xmax` is older than the oldest active transaction's `xmin` across the entire database cluster. A 14-hour open transaction pins the global `xmin` horizon; millions of deleted/updated tuples cannot be reclaimed.

**Diagnostics:** Query `pg_stat_activity` ordering by `backend_xmin` or `xact_start`.

**Prevention Setting:** Configure `idle_in_transaction_session_timeout = '10min'` to forcefully terminate abandoned transactions.

</details>

---

### D2. Cost-Based Optimizer choosing Seq Scan over Index Scan due to random_page_cost

```sql
-- Table has 5,000,000 rows stored on fast NVMe SSD storage
-- Query filters for 0.5% of rows:
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'FAILED';
```

**Observed symptom:** Optimizer picks `Seq Scan on orders` (cost=125,000) over `Bitmap Index Scan` (cost=180,000); query takes 4.2 seconds instead of 15 ms.

**(a)** What is PostgreSQL's default `random_page_cost` vs `seq_page_cost`, and what storage era does it assume?

**(b)** What value should `random_page_cost` be tuned to on modern NVMe / SSD disk infrastructure?

**(c)** Which command refreshes histogram distribution statistics to ensure accurate selectivity estimates?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** PostgreSQL defaults to `seq_page_cost = 1.0` and `random_page_cost = 4.0`, modeling spinning magnetic hard drives where random seeks are 4x slower than sequential reads. On NVMe SSDs, random seeks have identical latency to sequential reads.

**Fix:** Set `random_page_cost = 1.1` in `postgresql.conf`.

**Statistics:** Run `ANALYZE orders;` to ensure MCV (Most Common Values) histogram estimates accurate 0.5% selectivity.

</details>

---

### D3. Deadlock under concurrent row updates with mismatched acquisition order

```sql
-- Transaction 1:
UPDATE accounts SET balance = balance - 50 WHERE id = 10;
UPDATE accounts SET balance = balance + 50 WHERE id = 20;

-- Concurrent Transaction 2:
UPDATE accounts SET balance = balance - 100 WHERE id = 20;
UPDATE accounts SET balance = balance + 100 WHERE id = 10;
```

**Observed symptom:** Transaction 2 crashes with `ERROR: deadlock detected; Detail: Process 4122 waits for ExclusiveLock on tuple (0, 10)...`.

**(a)** What cycle in the lock dependency graph caused this deadlock?

**(b)** What programming convention completely prevents deadlocks when updating multiple resources?

**(c)** How does PostgreSQL detect and break deadlocks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Circular lock dependency. Tx 1 acquired lock on row 10 and requested row 20; Tx 2 acquired lock on row 20 and requested row 10.

**Fix:** Strictly enforce monotonic ordering of resource IDs in application code: always sort row IDs before locking (`sorted([id_a, id_b])`).

**Detection:** PostgreSQL background worker periodically checks lock wait trees (`deadlock_timeout`, default 1s) and kills the transaction with fewer changes.

</details>

---

### D4. Serialization failure 40001 under Serializable Snapshot Isolation (SSI)

```sql
-- Under SERIALIZABLE isolation:
-- Tx 1 reads count of doctors on call, sees 2, and takes leave:
UPDATE doctors SET on_call = FALSE WHERE id = 1;

-- Tx 2 concurrently reads count of doctors on call, sees 2, and takes leave:
UPDATE doctors SET on_call = FALSE WHERE id = 2;
```

**Observed symptom:** Tx 2 fails with `ERROR: could not serialize access due to read/write dependencies among transactions (SQLSTATE 40001)`.

**(a)** What business rule anomaly (write skew) did Serializable Snapshot Isolation prevent?

**(b)** Why is SQLSTATE 40001 an expected transient condition rather than a fatal application bug?

**(c)** What retry loop pattern must client applications implement when using SERIALIZABLE isolation?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Write Skew anomaly. Under Snapshot Isolation, both transactions see 2 doctors and modify disjoint rows, leaving 0 doctors on call. PostgreSQL SSI detects the anti-dependency cycle (SIREAD locks) and aborts Tx 2.

**Application Design:** In SERIALIZABLE isolation, 40001 serialization failures are normal retryable events.

**Fix:** Wrap application transactional calls in an exponential backoff retry loop (retry up to 3–5 times upon catching 40001).

</details>

---

### D5. HOT (Heap-Only Tuples) optimization failure caused by indexed column update

```sql
-- Table has index on (user_id) and index on (last_seen)
UPDATE users SET last_seen = NOW() WHERE user_id = 42;
```

**Observed symptom:** Table bloats rapidly; index size grows by 500 MB per day despite constant row count.

**(a)** What is HOT (Heap-Only Tuples) optimization in PostgreSQL, and why is it beneficial?

**(b)** Why does updating `last_seen` prevent HOT optimization from occurring?

**(c)** How can you design caching or index strategies to avoid index bloat on high-frequency timestamp updates?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** HOT allows tuple updates to link within the same 8KB page without inserting new entries into secondary B-Trees. However, HOT can **only** trigger if *no indexed column is modified*. Since `last_seen` is indexed, every single timestamp update forces a new index entry into all indexes!

**Fix:** Remove `last_seen` from secondary B-Tree indexes, or batch timestamp updates in Redis cache and flush periodically to PostgreSQL.

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
