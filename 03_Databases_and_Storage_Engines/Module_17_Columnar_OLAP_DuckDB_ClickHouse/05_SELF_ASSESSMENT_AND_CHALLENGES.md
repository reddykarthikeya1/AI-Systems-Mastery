# Module 17 Columnar OLAP DuckDB ClickHouse: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Why are columnar storage engines 10x-100x faster for analytical aggregations than row stores?** Why are columnar storage engines 10x-100x faster for analytical aggregations than row stores?
2. **What is Vectorized Execution in DuckDB?** What is Vectorized Execution in DuckDB?
3. **How does the ClickHouse MergeTree storage engine organize data on disk?** How does the ClickHouse MergeTree storage engine organize data on disk?
4. **What is Parquet predicate pushdown and projection pushdown?** What is Parquet predicate pushdown and projection pushdown?
5. **What causes 'Too Many Parts' error in ClickHouse?** What causes 'Too Many Parts' error in ClickHouse?
6. **What compression algorithms are standard in columnar storage?** What compression algorithms are standard in columnar storage?
7. **How does DuckDB query local Parquet files without a dedicated database server?** How does DuckDB query local Parquet files without a dedicated database server?
8. **What is a Min/Max Data Skipping index?** What is a Min/Max Data Skipping index?
9. **Why should ClickHouse primary keys NOT be globally unique UUIDs?** Why should ClickHouse primary keys NOT be globally unique UUIDs?
10. **What is the difference between an OLTP row store and an OLAP columnar store?** What is the difference between an OLTP row store and an OLAP columnar store?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Columnar stores read only the specific columns referenced in queries and use CPU SIMD vectorization to process thousands of values per instruction.

#### Answer 2:
Processing data in batches of columnar vectors (e.g. 2,048 values in CPU L1/L2 cache) rather than executing an iterator loop one tuple at a time.

#### Answer 3:
It sorts data by primary key, writes immutable sorted column parts, and merges them asynchronously in the background.

#### Answer 4:
Projection pushdown reads only requested columns; predicate pushdown uses row-group min/max statistics to skip entire chunks of data without decompression.

#### Answer 5:
Inserting single rows or micro-batches faster than background compaction can merge them.

#### Answer 6:
Dictionary encoding, Bit-packing, Run-Length Encoding (RLE), Gorilla (floats), and ZSTD / Snappy.

#### Answer 7:
It embeds directly in the host process (like SQLite) with an in-process vectorized engine executing directly over Parquet byte streams.

#### Answer 8:
Metadata storing minimum and maximum values per column chunk, allowing the query engine to bypass non-matching blocks immediately.

#### Answer 9:
ClickHouse primary keys determine physical on-disk sort order; sorting by random UUIDs destroys data locality and compression ratios.

#### Answer 10:
OLTP writes and reads entire rows for single transactions; OLAP reads specific columns across millions of rows for analytical aggregates.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Benchmark an aggregation query on 5,000,000 rows across DuckDB (columnar) vs SQLite (row store).

### 🚀 Challenge 2: Architect Stretch Problem
Create a ClickHouse MergeTree table with custom partition keys and demonstrate min/max data skipping.

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

### D1. ClickHouse 'Too Many Parts in All Data Parts in Table'

```python
# Microservice publishing real-time events to ClickHouse
from clickhouse_driver import Client
client = Client('clickhouse.internal')

def on_user_event(event: dict):
    # Inserts single row immediately upon event receipt (1,000 events/sec)
    client.execute(
        "INSERT INTO user_events (user_id, event_type, created_at) VALUES",
        [(event['user_id'], event['type'], event['time'])]
    )
```

**Observed symptom:** After 15 minutes of operation, ClickHouse rejects all inserts with: DB::Exception: Too many parts in all data parts in table 'user_events' (305 parts, maximum allowed 300). Merges are processing slower than parts are being created.

**(a)** How does ClickHouse's MergeTree engine persist inserted data, and why are single-row inserts fatal?

**(b)** Which system table allows inspecting part counts and active background merges in ClickHouse?

**(c)** What architectural patterns (buffer tables, application batching, or Kafka engine) solve this problem?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Every `INSERT` into a ClickHouse `MergeTree` table creates a new immutable on-disk **part** containing columnar compressed files for each column. ClickHouse runs background merge threads to asynchronously combine small parts into larger parts. ClickHouse is designed for inserts of $10,000$ to $100,000$ rows per batch. Inserting 1 row at a time 1,000 times per second creates 1,000 parts per second. The background merge process is quickly overwhelmed, and ClickHouse enforces the `parts_to_throw_insert` safety limit (default 300) to protect the filesystem.

**Diagnostic Commands:**
1. Inspect part count in `system.parts`:
   ```sql
   SELECT table, count() as total_parts, sum(rows) as total_rows
   FROM system.parts
   WHERE active = 1 AND table = 'user_events'
   GROUP BY table;
   ```
2. Check background merge activity:
   ```sql
   SELECT * FROM system.merges;
   ```

**Production Fix:**
1. **Application-Level Micro-Batching:** Accumulate records in memory (e.g. using `queue.Queue` or vector buffers) and flush in batches of at least 5,000 rows or every 2 seconds.
2. **ClickHouse Buffer Table:** Insert into an in-memory `Buffer` table engine that flushes to `MergeTree` in batches:
   ```sql
   CREATE TABLE user_events_buffer AS user_events ENGINE = Buffer(
       currentDatabase(), user_events, 16, 5, 10, 10000, 100000, 10000000, 100000000
   );
   ```
3. **Kafka Table Engine:** Ingest from Kafka topics using ClickHouse's native `ENGINE = Kafka` which batches messages automatically.

</details>

---

### D2. Run-Length Encoding (RLE) Negative Compression on High-Cardinality Column

```sql
-- Parquet / ClickHouse Columnar Table definition
CREATE TABLE sensor_readings (
    metric_id UUID,                -- High cardinality: 10,000,000 distinct UUIDs
    device_status LowCardinality(String),
    reading Float64,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (timestamp, metric_id);

-- Code uses RLE / Dictionary compression on metric_id
```

**Observed symptom:** Parquet / ClickHouse table storage size for metric_id is 30% LARGER than raw uncompressed binary data. Column scans over metric_id are 4x slower than scanning uncompressed data.

**(a)** How does Run-Length Encoding (RLE) and Dictionary encoding work, and why does it fail on high-cardinality sorted data?

**(b)** How can you inspect column compression ratios and physical sizes in ClickHouse or Parquet files?

**(c)** What encoding algorithm is optimal for UUIDs, timestamps, and high-cardinality float measurements?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Run-Length Encoding (RLE) compresses contiguous repeating values by storing `(value, count)` pairs. Dictionary encoding replaces values with integer pointers into a symbol dictionary. For high-cardinality columns (like unique UUIDs or random measurements) where values never repeat consecutively, RLE replaces a 16-byte UUID with a `(16-byte UUID, count=1)` pair (e.g. 20 bytes), resulting in negative compression. Dictionary encoding builds a dictionary that contains every single key, adding massive index overhead.

**Diagnostic Commands:**
1. Check column compression in ClickHouse:
   ```sql
   SELECT column, type, data_compressed_bytes, data_uncompressed_bytes,
          round(data_uncompressed_bytes / data_compressed_bytes, 2) AS ratio,
          compression_codec
   FROM system.columns
   WHERE table = 'sensor_readings';
   ```
2. Inspect Parquet metadata with `parquet-tools meta file.parquet`.

**Production Fix:**
1. Do not use `LowCardinality` or dictionary encoding on UUIDs or high-cardinality identifiers.
2. Configure specialized codecs based on data type:
   - **UUID / Hashes:** Generic LZ4 or ZSTD: `CODEC(ZSTD(3))`
   - **Timestamps / Incremental IDs:** DoubleDelta with ZSTD: `CODEC(DoubleDelta, ZSTD)`
   - **Floating Point Readings:** Gorilla or FPC (Floating Point Compression): `CODEC(Gorilla, ZSTD)`
   - **Low-cardinality strings (<10,000 distinct):** `LowCardinality(String)` (uses dictionary + RLE)

</details>

---

### D3. DuckDB Out-Of-Memory Crash on Large Hash Join

```python
import duckdb

con = duckdb.connect()
# Memory limit set for container
con.execute("SET max_memory = '4GB'")
# Temp directory set to disabled / read-only path

# Query joining two 20GB Parquet datasets
con.execute("""
    SELECT a.customer_id, count(b.transaction_id), sum(b.amount)
    FROM 'customers_large.parquet' a
    JOIN 'transactions_large.parquet' b ON a.customer_id = b.customer_id
    GROUP BY a.customer_id
""").fetchall()
```

**Observed symptom:** Query terminates with duckdb.duckdb.OutOfMemoryException: Out of Memory Error: could not allocate block of size 268435456 bytes (4GB max_memory reached). Process crashes without finishing aggregation.

**(a)** Why does a hash join require significant memory, and how does DuckDB manage out-of-core (disk spilling) execution?

**(b)** What configuration setting in DuckDB enables external spilling to disk for memory-constrained queries?

**(c)** How can the query be optimized using Parquet projection pushdown and partition pruning?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a standard hash join, DuckDB builds an in-memory hash table of the build-side relation (e.g. `customers_large`). When both relations exceed available RAM (`max_memory = '4GB'`), DuckDB requires an active temporary directory to spill intermediate hash partitions and sort buffers to disk (external / out-of-core processing). If temp disk spilling is not configured or disk permissions fail, DuckDB throws `OutOfMemoryException` once memory allocation reaches `max_memory`.

**Diagnostic Commands:**
1. Check memory and temp settings in DuckDB:
   ```sql
   SELECT * FROM duckdb_settings() WHERE name IN ('max_memory', 'temp_directory', 'preserve_insertion_order');
   ```
2. Enable profiling to check memory allocation:
   ```sql
   PRAGMA enable_profiling;
   PRAGMA profiling_output = 'profile.json';
   ```

**Production Fix:**
1. **Enable Disk Spilling:** Specify a writable directory for temporary data spilling:
   ```python
   con.execute("PRAGMA temp_directory = '/tmp/duckdb_temp'")
   ```
2. **Disable Insertion Order Preservation:** Setting `preserve_insertion_order = false` significantly reduces memory overhead during large aggregations.
3. **Projection Pushdown:** Select only the columns required for the join and aggregation, rather than scanning full schemas:
   ```sql
   SELECT a.customer_id, count(b.transaction_id), sum(b.amount)
   FROM (SELECT customer_id FROM 'customers_large.parquet') a
   JOIN (SELECT customer_id, transaction_id, amount FROM 'transactions_large.parquet') b
     ON a.customer_id = b.customer_id
   GROUP BY a.customer_id;
   ```

</details>

---

### D4. ClickHouse ReplacingMergeTree Unmerged Duplicate Rows

```sql
CREATE TABLE user_subscriptions (
    user_id UInt64,
    plan_name String,
    status String,
    updated_at DateTime
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (user_id);

-- User upgrades from 'FREE' to 'PRO':
INSERT INTO user_subscriptions VALUES (101, 'FREE', 'ACTIVE', '2026-01-01 10:00:00');
INSERT INTO user_subscriptions VALUES (101, 'PRO', 'ACTIVE', '2026-02-01 10:00:00');

-- User views current plan:
SELECT * FROM user_subscriptions WHERE user_id = 101;
```

**Observed symptom:** Query returns 2 rows instead of 1: user 101 shows both FREE and PRO plans simultaneously.

**(a)** When does `ReplacingMergeTree` actually deduplicate rows, and why did a direct `SELECT` return duplicates?

**(b)** What are the performance implications of adding `FINAL` to queries on large tables?

**(c)** How can deduplication be achieved efficiently without the performance penalty of `FINAL`?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
`ReplacingMergeTree` does **not** deduplicate data on insert. Deduplication occurs solely in the background during asynchronous part merges at indeterminate times. A standard `SELECT` reads all active parts as-is, which will contain duplicates until background merges happen to coincide. Relying on `ReplacingMergeTree` for real-time unique lookups without explicit deduplication logic is an architectural flaw.

**Diagnostic Commands:**
1. Force an on-demand merge to verify behavior:
   ```sql
   OPTIMIZE TABLE user_subscriptions FINAL;
   SELECT * FROM user_subscriptions WHERE user_id = 101; -- Now returns 1 row
   ```
   *(Note: OPTIMIZE TABLE FINAL is an expensive administrative command and should never run in application request paths).*

**Production Fix:**
1. **Use `FINAL` for low-volume reads:**
   ```sql
   SELECT * FROM user_subscriptions FINAL WHERE user_id = 101;
   ```
   *Caution:* In older ClickHouse versions, `FINAL` forces single-threaded merge processing across all parts.
2. **Use `argMax()` Aggregation (Optimal OLAP pattern):**
   ```sql
   SELECT user_id, argMax(plan_name, updated_at) AS plan_name,
          argMax(status, updated_at) AS status, max(updated_at) AS updated_at
   FROM user_subscriptions
   WHERE user_id = 101
   GROUP BY user_id;
   ```
   This is parallel, highly vectorized, and guarantees accurate state without full-table `FINAL` locks.

</details>

---

### D5. Vectorized Execution De-Optimization via Python UDF Row Fallback

```python
import duckdb

con = duckdb.connect()

# Custom row-by-row Python function
def clean_phone(val: str) -> str:
    if val is None:
        return ""
    import re
    return re.sub(r'\D', '', val)

con.create_function("clean_phone", clean_phone, ["VARCHAR"], "VARCHAR")

# Run on 50,000,000 customer records
con.execute("""
    SELECT clean_phone(phone_number) FROM 'customers.parquet'
""").fetchall()
```

**Observed symptom:** Query latency jumps from 0.3 seconds to 118 seconds. CPU profiler shows 95% of execution time spent in Python C-API PyObject_Call and garbage collector overhead rather than columnar SIMD processing.

**(a)** What is vectorized execution, and why does invoking a standard scalar Python function break vectorized pipelining?

**(b)** What is the per-row overhead of converting Arrow/columnar chunk buffers into individual Python objects?

**(c)** How can vector-native Arrow/PyArrow expressions or built-in DuckDB regex functions replace Python UDFs?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
DuckDB is a vectorized OLAP database that processes data in columnar vectors of 2,048 values using CPU cache-friendly loops and SIMD vectorization instructions. When a scalar Python UDF is called row-by-row, the execution engine must break the vectorized vector, box each value into an individual `PyObject`, invoke the Python interpreter (acquiring the GIL), execute interpreted bytecode, unbox the return value, and repack it into an Arrow vector. Repeating this 50,000,000 times introduces massive context switching and memory allocation overhead.

**Diagnostic Commands:**
1. Profile execution plan:
   ```sql
   EXPLAIN ANALYZE SELECT clean_phone(phone_number) FROM 'customers.parquet';
   ```
2. Look for `EXPRESSION` node with excessive execution time and scalar UDF barriers.

**Production Fix:**
1. **Use DuckDB Built-in SQL Functions:** DuckDB has native C++ SIMD-optimized regular expressions:
   ```sql
   SELECT regexp_replace(phone_number, '[^0-9]', '', 'g') FROM 'customers.parquet';
   ```
   This executes in < 0.5 seconds for 50 million records.
2. **Use Vectorized PyArrow UDFs:** If a custom Python function is mandatory, define it as a vectorized Arrow compute function using `type='arrow'` so DuckDB passes PyArrow chunk arrays (thousands of rows at once) directly without row-by-row unboxing.

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
