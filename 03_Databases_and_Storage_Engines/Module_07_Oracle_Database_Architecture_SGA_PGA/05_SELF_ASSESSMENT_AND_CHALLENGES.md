# Module 07 Oracle Database Architecture SGA PGA: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Oracle Database Architecture: SGA, PGA & Storage** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the difference between the System Global Area (SGA) and Program Global Area (PGA) in Oracle?** What is the difference between the System Global Area (SGA) and Program Global Area (PGA) in Oracle?
2. **Explain the difference between a Hard Parse and a Soft Parse in Oracle's Library Cache.?** Explain the difference between a Hard Parse and a Soft Parse in Oracle's Library Cache.
3. **How does the Oracle Database Buffer Cache touch-count algorithm work?** How does the Oracle Database Buffer Cache touch-count algorithm work?
4. **What does the Log Writer (LGWR) process do when a transaction executes COMMIT?** What does the Log Writer (LGWR) process do when a transaction executes COMMIT?
5. **What is the High-Water Mark (HWM) in an Oracle segment?** What is the High-Water Mark (HWM) in an Oracle segment?
6. **How does Automatic Memory Management (AMM) differ from Automatic Shared Memory Management (ASMM)?** How does Automatic Memory Management (AMM) differ from Automatic Shared Memory Management (ASMM)?
7. **What is a Tablespace Extent in Oracle storage hierarchy?** What is a Tablespace Extent in Oracle storage hierarchy?
8. **Why is CURSOR_SHARING = FORCE used as an interim performance fix?** Why is CURSOR_SHARING = FORCE used as an interim performance fix?
9. **What is the role of Database Writer (DBWR) processes in Oracle?** What is the role of Database Writer (DBWR) processes in Oracle?
10. **How do you calculate the Buffer Cache Hit Ratio from v$sysstat?** How do you calculate the Buffer Cache Hit Ratio from v$sysstat?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
SGA is shared memory accessible to all Oracle background and server processes; PGA is private non-shared memory allocated per server process for sorting and session state.

#### Answer 2:
A hard parse completely compiles the SQL, analyzes syntax, and computes an execution plan; a soft parse reuses an already compiled plan from the Library Cache using identical SQL text/bind keys.

#### Answer 3:
It tracks block access frequency using a counter; blocks with high touch counts (>2) are protected from eviction when new blocks are read into the buffer.

#### Answer 4:
LGWR synchronously writes the transaction's redo vectors from the Redo Log Buffer in SGA to the online redo log files on disk before acknowledging the commit.

#### Answer 5:
The boundary up to which blocks have ever been formatted for data. Full table scans read all blocks up to the HWM regardless of whether rows were deleted.

#### Answer 6:
ASMM tunes SGA pools dynamically (`SGA_TARGET`); AMM manages both SGA and PGA dynamically as a single shared pool (`MEMORY_TARGET`).

#### Answer 7:
A contiguous set of data blocks allocated within a datafile to form segments (tables, indexes).

#### Answer 8:
It automatically replaces literal values in SQL with system-generated bind variables, converting hard parses into soft parses.

#### Answer 9:
DBWR asynchronously writes dirty blocks from the Database Buffer Cache to datafiles on disk during checkpoints or when free buffer space is low.

#### Answer 10:
Hit Ratio = 1 - (physical reads / (db block gets + consistent gets)).

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Inspect Shared Pool execution plan reuse using v$sql and calculate soft parse efficiency across 1,000 queries.

### 🚀 Challenge 2: Architect Stretch Problem
Demonstrate HWM impact by comparing full-table scan time on a 100,000-row table before and after DELETE vs TRUNCATE.

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

### D1. ORA-04031 Shared Pool exhaustion from unshared literal SQL cursors

```python
# Application constructs raw literal SQL strings in Python loop:
for user_id in user_id_list:
    cursor.execute(f"SELECT * FROM accounts WHERE id = {user_id}")
```

**Observed symptom:** Database crashes with `ORA-04031: unable to allocate 4120 bytes of shared memory ('shared pool','unknown object','sga heap','kglsim heap')`.

**(a)** Why does concatenating literal values into SQL strings exhaust the Oracle SGA Shared Pool?

**(b)** How does the Library Cache use SQL text hashing to detect reusable execution plans?

**(c)** What is the fix using bind variables, and what cursor sharing setting provides server-side relief?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Every query with distinct literal text produces a unique SHA-1 hash in the Oracle Library Cache. The database performs an expensive **Hard Parse** for every single execution, generating thousands of unique cursor heaps that fragment and exhaust the SGA Shared Pool.

**Fix:** Use bind variables: `cursor.execute('SELECT * FROM accounts WHERE id = :id', {'id': user_id})`. Identical SQL text is hashed to the same Library Cache parent cursor, achieving **Soft Parses**.

**Server Setting:** As a temporary emergency mitigation, set `CURSOR_SHARING = FORCE` in Oracle init parameters.

</details>

---

### D2. Buffer busy waits on hot index leaf block

```sql
-- 1,000 concurrent threads inserting into table with monotonic sequence PK:
CREATE TABLE sensor_logs (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reading_val NUMBER
);
```

**Observed symptom:** AWR report shows Top 5 Timed Events dominated by `buffer busy waits` (75% of total wait time).

**(a)** Why does a monotonically ascending sequence create severe buffer contention on the rightmost leaf block of a B-Tree index?

**(b)** What is a Reverse Key Index, and how does it disperse concurrent inserts across the index tree?

**(c)** What range-scan limitation is introduced when an index is converted to a Reverse Key Index?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Monotonically increasing numbers always target the rightmost leaf block of the B-Tree index. 1,000 concurrent threads contend for exclusive buffer cache pin latches on the exact same physical disk block in the SGA Database Buffer Cache.

**Reverse Key Index Fix:** `CREATE INDEX idx_sensor_rev ON sensor_logs (id) REVERSE;`. Reversing the binary bytes of sequential keys (e.g. 1001, 1002, 1003 -> 1001, 2001, 3001) hashes inserts across different leaf blocks throughout the entire index.

**Trade-off:** Reverse Key Indexes cannot perform index range scans (`WHERE id BETWEEN 10 AND 50` must fall back to full table scan).

</details>

---

### D3. PGA memory exhaustion causing disk temp tablespace spill

```sql
-- Complex analytics query running on limited PGA:
SELECT customer_id, AVG(order_total) 
FROM orders 
GROUP BY customer_id 
ORDER BY AVG(order_total) DESC;
```

**Observed symptom:** Query execution time degrades from 0.4s to 85s; Enterprise Manager reports massive `direct path read temp` and `direct path write temp` I/O.

**(a)** What is the architectural distinction between Oracle SGA (Shared) and PGA (Program Global Area)?

**(b)** Why did the hash aggregation and sort operation spill from PGA Workareas into TEMP disk storage?

**(c)** What parameter governs maximum private workarea size per session?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Unlike the shared SGA, the PGA is private memory dedicated to an individual server process. When in-memory hash aggregation and sorting exceeds the session's allocated workarea (`PGA_AGGREGATE_TARGET` / `pga_aggregate_limit`), Oracle performs a multi-pass spill to the temporary tablespace on disk.

**Fix:** Increase `PGA_AGGREGATE_TARGET` or tune the session: `ALTER SESSION SET WORKAREA_SIZE_POLICY = MANUAL; ALTER SESSION SET SORT_AREA_SIZE = 104857600;`.

</details>

---

### D4. Redo log switch checkpoint incomplete hang

```sql
-- Heavy batch ETL loading 50,000,000 rows:
INSERT INTO warehouse_staging SELECT * FROM raw_external_stream;
```

**Observed symptom:** Entire Oracle instance freezes completely; alert.log reports `Thread 1 cannot allocate new log, sequence 485; Checkpoint not complete`.

**(a)** What does 'Checkpoint not complete' signify in the Oracle Redo Log Buffer architecture?

**(b)** Why does the Log Writer (LGWR) refuse to overwrite the next online redo log group?

**(c)** What two database configuration changes resolve this architectural bottleneck?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Oracle online redo logs are written circularly. Before LGWR can overwrite a redo log group, DBWn (Database Writer) must have flushed all dirty buffer cache blocks protected by that redo group to disk. If disk I/O cannot keep up with batch generation, LGWR stalls all instance writes.

**Fix 1:** Add more online redo log groups and increase log file sizes (e.g. from 100MB to 4GB each).

**Fix 2:** Increase checkpoint frequency or enable multiple database writer processes (`DB_WRITER_PROCESSES = 4`).

</details>

---

### D5. Library Cache latch contention on high-frequency hard parses

```sql
-- Web microservice with 200 connection pool workers executing dynamic SQL:
cursor.execute(f"SELECT * FROM products WHERE sku = '{sku_code}'")
```

**Observed symptom:** CPU utilization reaches 100% with low TPS; `v$active_session_history` shows sessions waiting on `latch: library cache`.

**(a)** What is a latch in Oracle database internal architecture, and how does it differ from a transaction lock?

**(b)** Why does parsing dynamic SQL require acquiring exclusive library cache latches?

**(c)** What is the architectural fix to reduce latch acquisition frequency?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A latch is a low-level, short-duration mutual exclusion primitive (spinlock) protecting shared SGA memory structures from concurrent modification. Parsing dynamic SQL requires acquiring the `library cache` latch to insert new syntax trees into the hash table.

**Fix:** Rewrite queries with bind variables (`:sku_code`). Reusing execution plans bypasses exclusive library cache latch acquisition, allowing concurrent shared reads.

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
