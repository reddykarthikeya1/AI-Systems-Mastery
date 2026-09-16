"""Diagnostic quiz questions, batch A: Modules 01-06 in Databases course.

Each entry is (title, code, symptom, questions, answer). A diagnostic question
shows real code plus an observed symptom and asks for cause, fix, and which test
would have caught it.
"""

from __future__ import annotations

DIAGNOSTICS: dict[str, list[tuple[str, str, str, list[str], str]]] = {
    "01": [
        (
            "Transitive dependency causing partial update anomaly",
            '''-- Updating user office location in denormalized employee table
UPDATE employees 
SET office_city = 'San Francisco' 
WHERE emp_id = 101;
-- 50 other employees work in the same office building (office_id = 'BLDG-B')''',
            "Queries grouping by office_city report fragmented stats: BLDG-B is split between 'SF' and 'San Francisco'.",
            [
                "Which normal form does this schema violate, and what is the functional dependency chain?",
                "How do you decompose the relation to achieve 3NF?",
                "What database constraint prevents orphaned office records after decomposition?"
            ],
            "**Root cause:** Violates **Third Normal Form (3NF)** due to a transitive dependency: `emp_id -> office_id -> office_city`. Non-key attribute `office_city` depends on non-key attribute `office_id` rather than the primary key `emp_id`.\n\n**Fix:** Decompose into two tables: `employees(emp_id, name, office_id)` with foreign key `office_id REFERENCES offices(office_id)`, and `offices(office_id, office_city)`.\n\n**Constraint:** A `FOREIGN KEY (office_id) REFERENCES offices(office_id) ON UPDATE CASCADE ON DELETE RESTRICT` guarantees referential integrity."
        ),
        (
            "Lost Update under concurrent Read-Modify-Write",
            '''# Thread A and Thread B concurrently executing balance increment:
cur.execute("SELECT balance FROM accounts WHERE id = %s", (acc_id,))
bal = cur.fetchone()[0]
new_bal = bal + deposit_amount
cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_bal, acc_id))''',
            "Two concurrent deposits of $100 both read $500 initial balance; final balance is $600 instead of $700.",
            [
                "Why did Thread B overwrite Thread A's deposit without throwing a concurrency error?",
                "What is the single-statement SQL atomic fix?",
                "If multi-statement logic is required, which locking clause must be appended to the SELECT?"
            ],
            "**Root cause:** Lost Update anomaly under Read Committed isolation. Both transactions read snapshot state $500, calculate $600 locally, and the second `UPDATE` blindsides the first write without conflict detection.\n\n**Fix:** Use atomic in-place mutation: `UPDATE accounts SET balance = balance + %s WHERE id = %s`.\n\n**Locking alternative:** Use pessimistic row-level locking: `SELECT balance FROM accounts WHERE id = %s FOR UPDATE`, forcing Thread B to block until Thread A commits."
        ),
        (
            "Torn Page vulnerability during unbuffered power loss",
            '''# Storage engine writes 8KB database pages using standard OS write()
with open("data.db", "r+b") as f:
    f.seek(page_offset)
    f.write(modified_page_bytes)  # 8192 bytes
    f.flush()  # Power loss happens halfway through disk controller flush!''',
            "On restart, the page contains corrupted header checksums; 4096 bytes are new data and 4096 bytes are old sector data.",
            [
                "Why does `write()` of 8KB fail to guarantee atomicity at the physical drive level?",
                "How does MySQL InnoDB protect against this specific failure using the doublewrite buffer?",
                "How does PostgreSQL protect against torn pages in its WAL stream?"
            ],
            "**Root cause:** Hard drive sector write atomicity is physically limited to 512 bytes or 4KB (Advanced Format). Writing an 8KB or 16KB database page requires multiple hardware sector writes; power loss during intermediate sectors yields a **Torn Page**.\n\n**InnoDB Fix:** InnoDB writes pages first to a contiguous sequential **Doublewrite Buffer** on disk before writing to data files. If a crash occurs during data file write, the page is restored intact from the doublewrite buffer.\n\n**PostgreSQL Fix:** PostgreSQL writes **Full Page Images (FPI)** to WAL on the first modification to a page following a checkpoint (`full_page_writes = on`)."
        ),
        (
            "1NF Violation: Storing comma-separated tags in relational column",
            '''SELECT * FROM products WHERE tags LIKE '%electronics%';''',
            "Query requires a full table scan; indexes on `tags` are bypassed; partial string matches false-positive on 'microelectronics' and 'consumer-electronics-repair'.",
            [
                "What rule of First Normal Form (1NF) is violated by the `tags` column?",
                "What are the severe performance and query limitations of matching CSV strings via LIKE?",
                "What are the two standard relational architectures for resolving this schema defect?"
            ],
            "**Root cause:** Violates 1NF, which dictates that every column must contain **atomic (indivisible) values**. Comma-separated strings encode multi-valued repeating groups.\n\n**Limitations:** Wildcard prefix `%term%` prevents B-Tree index range scans, forcing $O(N)$ table scans, and cannot enforce uniqueness or referential integrity on tag tokens.\n\n**Relational Fixes:** Either (1) create a normalized junction table `product_tags(product_id, tag_id)` with foreign keys and compound primary key, or (2) use native PostgreSQL array types with GIN indexing: `tags text[], WHERE tags @> ARRAY['electronics']`."
        ),
        (
            "Dirty read anomaly under READ UNCOMMITTED isolation",
            '''-- Session 1 (Fraudulent transaction):
BEGIN;
UPDATE accounts SET balance = balance - 10000 WHERE id = 1;
-- Network glitch / validation fails -> ROLLBACK;

-- Session 2 (Concurrent credit check running concurrently before rollback):
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE id = 1; -- Sees balance deducted!''',
            "Session 2 grants a loan based on the uncommitted balance reduction; Session 1 rolls back, leaving invalid loan approvals.",
            [
                "What is a Dirty Read, and why is it permitted in READ UNCOMMITTED?",
                "What is the minimum ANSI SQL transaction isolation level that eliminates Dirty Reads?",
                "How does MVCC in modern PostgreSQL/MySQL prevent dirty reads without locking readers?"
            ],
            "**Root cause:** In READ UNCOMMITTED, readers inspect dirty memory buffers in the buffer pool without checking transaction commit status (`xmax` or commit bits), reading transient uncommitted mutations.\n\n**Fix:** Elevate isolation level to at least **READ COMMITTED**.\n\n**MVCC Mechanics:** In PostgreSQL and InnoDB, readers construct a snapshot based on active transaction IDs (`Snapshot.active_xids`). Any tuple version created by an uncommitted transaction (`xmin` in active list) is invisible to readers, directing them to the previous committed tuple version without taking read locks."
        )
    ],
    "02": [
        (
            "NOT IN with NULL subquery evaluating to empty set",
            '''SELECT customer_id, name 
FROM customers 
WHERE customer_id NOT IN (
    SELECT referrer_id FROM customers
);''',
            "Query returns zero rows even though 90% of customers have never referred anyone.",
            [
                "Why does SQL three-valued logic cause `NOT IN` to evaluate to empty when the subquery contains a single NULL?",
                "What is the exact Boolean expression SQL evaluates when checking `val NOT IN (1, 2, NULL)`?",
                "What is the production-safe rewrite using `NOT EXISTS` or `IS NOT NULL`?"
            ],
            "**Root cause:** In SQL three-valued logic, `x NOT IN (a, b, NULL)` expands to `(x <> a) AND (x <> b) AND (x <> NULL)`. The comparison `x <> NULL` evaluates to `UNKNOWN`. Because `TRUE AND UNKNOWN` yields `UNKNOWN`, the `WHERE` clause filters out every row.\n\n**Fix 1:** Add explicit null check: `SELECT referrer_id FROM customers WHERE referrer_id IS NOT NULL`.\n\n**Fix 2 (Preferred):** Use `NOT EXISTS`: `WHERE NOT EXISTS (SELECT 1 FROM customers r WHERE r.referrer_id = customers.customer_id)`. `NOT EXISTS` uses two-valued logic and is null-safe."
        ),
        (
            "Missing PARTITION BY in Window Function accumulating globally",
            '''SELECT 
    dept_id, 
    emp_name, 
    salary,
    SUM(salary) OVER (ORDER BY salary ROWS UNBOUNDED PRECEDING) AS running_total
FROM employees;''',
            "The running total accumulates across all employees in the entire company instead of resetting per department.",
            [
                "Why did the window function compute an enterprise-wide running total?",
                "What clause must be added to scope window calculations to individual departments?",
                "How does the default frame `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` handle peer duplicate salaries?"
            ],
            "**Root cause:** Missing `PARTITION BY dept_id`. Without a partition clause, the entire result set is treated as a single window partition.\n\n**Fix:** Add partition clause: `SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary ROWS UNBOUNDED PRECEDING)`.\n\n**RANGE vs ROWS:** `RANGE` treats duplicate values of the `ORDER BY` column as peers and aggregates them all together into the running total at once, whereas `ROWS` processes strictly row-by-row."
        ),
        (
            "Correlated Subquery in SELECT clause inducing O(N) execution cliff",
            '''SELECT 
    o.order_id, 
    o.order_date,
    (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) AS item_count
FROM orders o;''',
            "Query on 1,000,000 orders takes 120 seconds to execute, consuming 100% CPU on sequential index lookups.",
            [
                "Why does a correlated scalar subquery in the SELECT list cause severe execution degradation?",
                "Rewrite this query using a `LEFT JOIN` and `GROUP BY`.",
                "Which query plan operator does the optimizer use when converting this into a set-oriented hash join?"
            ],
            "**Root cause:** The scalar subquery executes once for every individual row in the outer `orders` table (an $O(N)$ correlated loop execution).\n\n**Fix:** Rewrite to a set-oriented aggregation:\n```sql\nSELECT o.order_id, o.order_date, COALESCE(COUNT(oi.item_id), 0) AS item_count\nFROM orders o\nLEFT JOIN order_items oi ON o.order_id = oi.order_id\nGROUP BY o.order_id, o.order_date;\n```\n**Optimizer Plan:** The database optimizer can now use a single `Hash Aggregate` over a `Hash Left Join`, completing in $O(N + M)$ time instead of 1,000,000 separate index seeks."
        ),
        (
            "Lexicographical string sorting on numeric VARCHAR column",
            '''SELECT invoice_id, amount_due 
FROM invoices 
ORDER BY invoice_id ASC;''',
            "Invoices sort as: 'INV-1', 'INV-10', 'INV-100', 'INV-2', 'INV-20', 'INV-3'.",
            [
                "Why does 'INV-100' appear before 'INV-2' in standard ascending sort order?",
                "How can you write a deterministic expression in the ORDER BY clause to sort numerically by invoice number?",
                "What is the clean schema migration to prevent this ordering defect permanently?"
            ],
            "**Root cause:** `invoice_id` is stored as `VARCHAR`/`TEXT`. Text strings are compared byte-by-byte lexicographically; character `'1'` has a lower ASCII/Unicode code point than `'2'`, so any string starting with `'1'` precedes `'2'` regardless of length.\n\n**Fix:** Extract and cast the numeric suffix: `ORDER BY CAST(SUBSTRING(invoice_id FROM 5) AS INTEGER) ASC`.\n\n**Schema Fix:** Split into a generated prefix column and an integer sequence: `id INT GENERATED ALWAYS AS IDENTITY`, formatting as `'INV-' || id` only in the presentation layer."
        ),
        (
            "Unbounded Recursive CTE causing infinite loop and stack exhaustion",
            '''WITH RECURSIVE org_chart AS (
    SELECT emp_id, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org_chart o ON e.manager_id = o.emp_id
)
SELECT * FROM org_chart;''',
            "Query hangs indefinitely, exhausting temp memory until terminating with `ERROR: statement timeout` or `recursion limit exceeded`.",
            [
                "What data cycle in the `employees` table causes the recursive member to loop infinitely?",
                "How can you track visited nodes using an array in PostgreSQL to prevent cycles?",
                "What clause in modern PostgreSQL 14+ natively detects recursion cycles?"
            ],
            "**Root cause:** A cycle exists in employee manager hierarchy (e.g. Employee A reports to B, B reports to C, and C mistakenly reports to A). The recursive join continuously re-discovers previously visited nodes.\n\n**Array Tracking Fix:** Track paths: `ARRAY[e.emp_id]` and terminate when `NOT (e.emp_id = ANY(o.path))`.\n\n**PostgreSQL 14+ Native Fix:** Use `CYCLE emp_id SET is_cycle USING path`, which automatically flags and breaks cyclic iterations."
        )
    ],
    "03": [
        (
            "SQLite WAL file growing into gigabytes without truncating",
            '''import sqlite3, time
conn_write = sqlite3.connect("app.db")
conn_write.execute("PRAGMA journal_mode=WAL;")

# Connection 2 starts an unclosed read transaction
conn_read = sqlite3.connect("app.db")
cur = conn_read.cursor()
cur.execute("SELECT * FROM large_table WHERE id = 1")
# Reader never calls commit(), rollback(), or close()!

# Writer continues appending 1,000,000 transactions
for i in range(100_000):
    conn_write.execute("INSERT INTO audit VALUES (?)", (i,))
    conn_write.commit()''',
            "`app.db-wal` grows to 4.2 GB; `PRAGMA wal_checkpoint(TRUNCATE)` returns `(0, 524288, 1)` and fails to shrink the file.",
            [
                "Why does an open reader cursor prevent SQLite from checkpointing and truncating the WAL file?",
                "What does the return tuple `(busy, log_frames, checkpointed_frames)` signify in `wal_checkpoint`?",
                "What defensive architectural pattern guarantees SQLite read cursors do not leak snapshots?"
            ],
            "**Root cause:** SQLite WAL mode operates via lock-free snapshots. When a reader begins a transaction, it records its read mark (the newest WAL frame at that instant). Checkpointing can only copy and truncate frames up to the oldest active read mark. The unclosed reader pins the checkpoint boundary, forcing all subsequent writes to grow the WAL file indefinitely.\n\n**Return tuple:** `(0, 524288, 1)` indicates: `busy=0` (checkpoint completed), `log_frames=524288` total WAL frames exist, but only `checkpointed_frames=1` could be safely flushed past the stalled reader.\n\n**Defensive Fix:** Always wrap read queries in Python context managers (`with sqlite3.connect(...) as conn:` or `try...finally: cur.close()`) to ensure read transactions are released immediately."
        ),
        (
            "Database locked error under concurrent multi-process writes",
            '''# Two worker processes write to the same SQLite database simultaneously
db = sqlite3.connect("tasks.db")
db.execute("INSERT INTO job_queue (task) VALUES ('process_image')")''',
            "Worker 2 crashes with `sqlite3.OperationalError: database is locked` after 0.001 seconds.",
            [
                "What is SQLite's default lock acquisition timeout when encountering write contention?",
                "What PRAGMA command configures SQLite to sleep and retry before returning SQLITE_BUSY?",
                "How does WAL mode improve concurrency for readers while preserving the single-writer invariant?"
            ],
            "**Root cause:** SQLite's default `busy_timeout` is 0 milliseconds. When Worker 2 attempts an exclusive write lock while Worker 1 holds it, SQLite raises `SQLITE_BUSY` (`database is locked`) immediately.\n\n**Fix:** Set busy timeout on connection creation: `PRAGMA busy_timeout = 5000;` or `sqlite3.connect('tasks.db', timeout=5.0)`. SQLite will perform progressive backoff sleeps up to 5 seconds before erroring.\n\n**WAL Concurrency:** In WAL mode, writers append to the `-wal` log without blocking readers reading from the main `.db` file, though writes remain single-threaded."
        ),
        (
            "Foreign Key constraints silently ignored in SQLite",
            '''conn = sqlite3.connect("shop.db")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY);")
conn.execute("CREATE TABLE orders (order_id INT, user_id INT REFERENCES users(id));")
conn.execute("INSERT INTO orders VALUES (101, 99999);") -- User 99999 does not exist!
conn.commit()''',
            "The invalid order is committed successfully without raising an IntegrityError.",
            [
                "Why does SQLite default to ignoring foreign key references?",
                "Which command must be executed on every newly established SQLite database connection?",
                "Which Python sqlite3 connection hook ensures this PRAGMA runs automatically for connection pools?"
            ],
            "**Root cause:** For historical backward compatibility with SQLite 2.x and early 3.x, SQLite has **foreign key enforcement disabled by default**.\n\n**Fix:** Must execute `PRAGMA foreign_keys = ON;` immediately after opening each connection.\n\n**Pool Hook:** In SQLAlchemy or raw connection pools, attach a connect listener: `cursor.execute('PRAGMA foreign_keys=ON')`."
        ),
        (
            "Silent database corruption over Network File System (NFS/SMB)",
            '''# SQLite database placed on AWS EFS or Windows SMB shared network folder
conn = sqlite3.connect(r"\\network_share\storage\prod.db")''',
            "After two weeks of multi-client writes, `PRAGMA integrity_check` reports `*** in database main *** Page 104 is never used, Tree 208 page 208 has bad flags`.",
            [
                "Why do POSIX advisory locks fail to function reliably over network file shares (NFS/SMB)?",
                "What happens to the SQLite Shared Memory file (`-shm`) over network drives in WAL mode?",
                "What is SQLite's official guidance regarding multi-writer setups on network storage?"
            ],
            "**Root cause:** Network File Systems (NFS/SMB) frequently provide buggy, delayed, or broken byte-range file locking implementations. Two clients simultaneously believe they hold exclusive locks, resulting in simultaneous uncoordinated disk writes and catastrophic B-Tree corruption.\n\n**WAL -shm failure:** In WAL mode, SQLite uses mmap on `-shm` to coordinate readers and writers; mmap over network shares is notoriously incoherent across different client kernels.\n\n**Official Guidance:** SQLite is an embedded database designed for local disk storage. For network-attached multi-client storage, use client-server databases like PostgreSQL or MySQL."
        ),
        (
            "Missing commit() call leaving database in active transaction",
            '''def record_audit(event: str):
    conn = sqlite3.connect("audit.db")
    conn.execute("INSERT INTO events (msg) VALUES (?)", (event,))
    conn.close() # Script exits cleanly''',
            "Script finishes with exit code 0, but `SELECT COUNT(*) FROM events` returns 0; no rows were written.",
            [
                "Why does Python's `sqlite3` driver fail to persist rows when `close()` is called without `commit()`?",
                "What is the transaction management behavior difference between Python's default isolation level and `autocommit=True`?",
                "What context manager pattern guarantees atomic commit on success and rollback on exception?"
            ],
            "**Root cause:** Python's `sqlite3` module operates in implicit transaction mode (`isolation_level=''` by default). When a DML statement (`INSERT`) is executed, it opens a transaction, but `close()` rolls back uncommitted transactions by default.\n\n**Fix:** Use connection as a context manager: `with conn: conn.execute(...)`, which issues `conn.commit()` on clean exit and `conn.rollback()` on exception.\n\n**Autocommit:** In Python 3.12+, `sqlite3.connect('audit.db', autocommit=True)` disables implicit transactions, matching standard SQLite CLI behavior."
        )
    ],
    "04": [
        (
            "GIN index bypassed on JSONB due to operator mismatch",
            '''-- Table has GIN index on jsonb column
CREATE INDEX idx_user_meta ON users USING GIN (metadata);

-- Query searching for tier:
EXPLAIN ANALYZE 
SELECT * FROM users 
WHERE metadata->>'tier' = 'premium';''',
            "`Seq Scan on users` is chosen; query latency is 450 ms instead of 0.8 ms on 1,000,000 rows.",
            [
                "Why does standard GIN indexing on `metadata` ignore the `->>` text extraction operator?",
                "What is the containment operator (`@>`) syntax that leverages the default GIN jsonb_ops index?",
                "What alternative index definition optimizes `metadata->>'tier'` specifically?"
            ],
            "**Root cause:** The default GIN index on a JSONB column (`jsonb_ops`) indexes paths and values for the **containment operator (`@>`)**, not the text extraction operator (`->>`).\n\n**Fix 1:** Rewrite query to use containment: `WHERE metadata @> \'{\"tier\": \"premium\"}\'`.\n\n**Fix 2:** Alternatively, build an expression B-Tree index specifically targeting the extracted text: `CREATE INDEX idx_user_tier ON users ((metadata->>'tier'));`."
        ),
        (
            "TOAST pointer decompression latency cliff in Sequential Scans",
            '''-- Table has large JSONB and TEXT columns exceeding 2KB
SELECT user_id, status FROM users WHERE status = 'PENDING';''',
            "Table has 500,000 rows. A simple filter scan takes 12 seconds, reading 8 GB of data from disk.",
            [
                "What is TOAST (The Oversized-Attribute Storage Technique) in PostgreSQL, and when does it trigger?",
                "Why does a `SELECT user_id, status` scan still incur I/O overhead if large columns are not in the SELECT list?",
                "How does creating a covering index eliminate TOAST table lookups completely?"
            ],
            "**Root cause:** When rows exceed `TOAST_TUPLE_THRESHOLD` (approx 2KB), large columns are compressed and stored out-of-line in a auxiliary TOAST table. Even if large columns are not in the `SELECT` list, sequential scan must scan the main heap pages, which are bloated by TOAST pointers.\n\n**Covering Index Fix:** Create an Index-Only Scan index: `CREATE INDEX idx_users_status_inc ON users (status) INCLUDE (user_id);`. The query engine satisfies the query entirely from the B-Tree index without accessing the bloated heap or TOAST tables."
        ),
        (
            "Exclusion constraint failure on overlapping booking ranges",
            '''-- Attempting to prevent overlapping hotel room bookings
CREATE TABLE bookings (
    room_id INT,
    during DATERANGE,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
-- Error: type "daterange" does not have default operator class for access method "gist"''',
            "PostgreSQL rejects table creation with `ERROR: data type integer has no default operator class for access method 'gist'`.",
            [
                "Why does GiST index fail on the `room_id WITH =` column in standard PostgreSQL?",
                "Which standard PostgreSQL extension must be enabled to provide B-Tree operators inside GiST indexes?",
                "What is the exact CREATE EXTENSION command required?"
            ],
            "**Root cause:** GiST natively supports geometric and range operators (`&&`), but does not have built-in operator classes for scalar equality (`=`) on primitive types like `INTEGER`.\n\n**Fix:** Enable the `btree_gist` extension: `CREATE EXTENSION IF NOT EXISTS btree_gist;`.\n\n**Outcome:** `btree_gist` allows standard scalar equality checks inside GiST exclusion constraints, enabling multi-column collision prevention: `EXCLUDE USING gist (room_id WITH =, during WITH &&)`."
        ),
        (
            "Implicit text casting breaking UUID index lookups",
            '''-- users.id is UUID type with B-Tree primary key index
SELECT * FROM users WHERE id = 'e8b2c451-92b1-4f12-98e3-085e3a89326f';
-- External ORM generated parameterized query as TEXT parameter:
SELECT * FROM users WHERE id = $1::text;''',
            "Optimizer falls back to full table `Seq Scan on users`, discarding the primary key index.",
            [
                "Why does casting an indexed column to `text` invalidate a B-Tree index on `uuid`?",
                "What is the correct parameter casting in PostgreSQL SQL statements?",
                "Which test in the test suite verifies that UUID lookups perform index seeks?"
            ],
            "**Root cause:** Wrapping an indexed column in an expression (`id::text` or function call) disables the index because the B-Tree index is organized on the binary `uuid` representation, not its string conversion.\n\n**Fix:** Cast the literal parameter, not the column: `WHERE id = $1::uuid`.\n\n**Test Citation:** `test_jsonb_document_store.py::test_uuid_lookup` verifies direct index scans."
        ),
        (
            "Array subfield updates rewriting entire array attribute",
            '''-- Updating a single element in a 5,000-element array column
UPDATE sensor_readings 
SET telemetry[450] = 99.4 
WHERE sensor_id = 'sensor-alpha';''',
            "High WAL write volume: a 1-byte update generates 40KB of WAL traffic and updates the full row tuple.",
            [
                "Why does PostgreSQL MVCC rewrite the entire array on disk when a single element is modified?",
                "How does this impact Write Amplification and database replication bandwidth?",
                "What schema design should be used when individual array elements undergo frequent independent updates?"
            ],
            "**Root cause:** In PostgreSQL's MVCC append-only storage model, tuples are immutable. Updating a single element in an array does not perform in-place mutation; it copies the entire array into a new heap tuple version.\n\n**Impact:** Causes massive Write Amplification, WAL generation spikes, and heavy table bloat.\n\n**Schema Fix:** Normalize high-cardinality collections into a dedicated child table: `sensor_telemetry(sensor_id, reading_index, value)` with compound PK `(sensor_id, reading_index)`."
        )
    ],
    "05": [
        (
            "Long-running analytical transaction pinning oldest xmin",
            '''-- Data analyst starts a reporting query and leaves their workstation:
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM huge_sales_log;
-- Transaction remains open for 14 hours...''',
            "Production OLTP database runs out of disk space; table sizes double; `VACUUM` log reports `0 dead tuples removed; 850,000 dead tuples remain unremovable`.",
            [
                "Why does a single open snapshot in REPEATABLE READ prevent VACUUM from purging dead tuples across all other tables?",
                "What catalog view exposes the oldest active transaction xmin blocking vacuum?",
                "What database setting automatically aborts idle transactions before bloat occurs?"
            ],
            "**Root cause:** PostgreSQL `VACUUM` can only purge dead tuples whose `xmax` is older than the oldest active transaction's `xmin` across the entire database cluster. A 14-hour open transaction pins the global `xmin` horizon; millions of deleted/updated tuples cannot be reclaimed.\n\n**Diagnostics:** Query `pg_stat_activity` ordering by `backend_xmin` or `xact_start`.\n\n**Prevention Setting:** Configure `idle_in_transaction_session_timeout = '10min'` to forcefully terminate abandoned transactions."
        ),
        (
            "Cost-Based Optimizer choosing Seq Scan over Index Scan due to random_page_cost",
            '''-- Table has 5,000,000 rows stored on fast NVMe SSD storage
-- Query filters for 0.5% of rows:
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'FAILED';''',
            "Optimizer picks `Seq Scan on orders` (cost=125,000) over `Bitmap Index Scan` (cost=180,000); query takes 4.2 seconds instead of 15 ms.",
            [
                "What is PostgreSQL's default `random_page_cost` vs `seq_page_cost`, and what storage era does it assume?",
                "What value should `random_page_cost` be tuned to on modern NVMe / SSD disk infrastructure?",
                "Which command refreshes histogram distribution statistics to ensure accurate selectivity estimates?"
            ],
            "**Root cause:** PostgreSQL defaults to `seq_page_cost = 1.0` and `random_page_cost = 4.0`, modeling spinning magnetic hard drives where random seeks are 4x slower than sequential reads. On NVMe SSDs, random seeks have identical latency to sequential reads.\n\n**Fix:** Set `random_page_cost = 1.1` in `postgresql.conf`.\n\n**Statistics:** Run `ANALYZE orders;` to ensure MCV (Most Common Values) histogram estimates accurate 0.5% selectivity."
        ),
        (
            "Deadlock under concurrent row updates with mismatched acquisition order",
            '''-- Transaction 1:
UPDATE accounts SET balance = balance - 50 WHERE id = 10;
UPDATE accounts SET balance = balance + 50 WHERE id = 20;

-- Concurrent Transaction 2:
UPDATE accounts SET balance = balance - 100 WHERE id = 20;
UPDATE accounts SET balance = balance + 100 WHERE id = 10;''',
            "Transaction 2 crashes with `ERROR: deadlock detected; Detail: Process 4122 waits for ExclusiveLock on tuple (0, 10)...`.",
            [
                "What cycle in the lock dependency graph caused this deadlock?",
                "What programming convention completely prevents deadlocks when updating multiple resources?",
                "How does PostgreSQL detect and break deadlocks?"
            ],
            "**Root cause:** Circular lock dependency. Tx 1 acquired lock on row 10 and requested row 20; Tx 2 acquired lock on row 20 and requested row 10.\n\n**Fix:** Strictly enforce monotonic ordering of resource IDs in application code: always sort row IDs before locking (`sorted([id_a, id_b])`).\n\n**Detection:** PostgreSQL background worker periodically checks lock wait trees (`deadlock_timeout`, default 1s) and kills the transaction with fewer changes."
        ),
        (
            "Serialization failure 40001 under Serializable Snapshot Isolation (SSI)",
            '''-- Under SERIALIZABLE isolation:
-- Tx 1 reads count of doctors on call, sees 2, and takes leave:
UPDATE doctors SET on_call = FALSE WHERE id = 1;

-- Tx 2 concurrently reads count of doctors on call, sees 2, and takes leave:
UPDATE doctors SET on_call = FALSE WHERE id = 2;''',
            "Tx 2 fails with `ERROR: could not serialize access due to read/write dependencies among transactions (SQLSTATE 40001)`.",
            [
                "What business rule anomaly (write skew) did Serializable Snapshot Isolation prevent?",
                "Why is SQLSTATE 40001 an expected transient condition rather than a fatal application bug?",
                "What retry loop pattern must client applications implement when using SERIALIZABLE isolation?"
            ],
            "**Root cause:** Write Skew anomaly. Under Snapshot Isolation, both transactions see 2 doctors and modify disjoint rows, leaving 0 doctors on call. PostgreSQL SSI detects the anti-dependency cycle (SIREAD locks) and aborts Tx 2.\n\n**Application Design:** In SERIALIZABLE isolation, 40001 serialization failures are normal retryable events.\n\n**Fix:** Wrap application transactional calls in an exponential backoff retry loop (retry up to 3–5 times upon catching 40001)."
        ),
        (
            "HOT (Heap-Only Tuples) optimization failure caused by indexed column update",
            '''-- Table has index on (user_id) and index on (last_seen)
UPDATE users SET last_seen = NOW() WHERE user_id = 42;''',
            "Table bloats rapidly; index size grows by 500 MB per day despite constant row count.",
            [
                "What is HOT (Heap-Only Tuples) optimization in PostgreSQL, and why is it beneficial?",
                "Why does updating `last_seen` prevent HOT optimization from occurring?",
                "How can you design caching or index strategies to avoid index bloat on high-frequency timestamp updates?"
            ],
            "**Root cause:** HOT allows tuple updates to link within the same 8KB page without inserting new entries into secondary B-Trees. However, HOT can **only** trigger if *no indexed column is modified*. Since `last_seen` is indexed, every single timestamp update forces a new index entry into all indexes!\n\n**Fix:** Remove `last_seen` from secondary B-Tree indexes, or batch timestamp updates in Redis cache and flush periodically to PostgreSQL."
        )
    ],
    "06": [
        (
            "Secondary index bookmark lookup thrashing on non-covering query",
            '''-- users table: PK is user_id. Secondary index on email.
SELECT user_id, email, phone_number, home_address 
FROM users 
WHERE email = 'alice@example.com';''',
            "Under high concurrency (20,000 req/sec), CPU spikes to 100% and buffer pool read IOPS saturate disk.",
            [
                "Why does querying `phone_number` require a secondary index bookmark lookup in MySQL InnoDB?",
                "How does InnoDB's clustered index architecture differ from heap-table architectures in PostgreSQL?",
                "How does creating a Covering Index with composite columns or USING INDEX eliminate heap seeks?"
            ],
            "**Root cause:** In InnoDB, secondary indexes do not point directly to physical page offsets; they store the Primary Key as a **bookmark**. Querying columns not in the secondary index (`phone_number`, `home_address`) requires an extra clustered index B-Tree lookup for every matched row.\n\n**Covering Index Fix:** Create a composite index containing all queried columns: `CREATE INDEX idx_email_covering ON users (email, phone_number, home_address);`.\n\n**Outcome:** Allows InnoDB to satisfy the query directly from the secondary index leaf page (`Using index` in EXPLAIN) without double-traversal."
        ),
        (
            "Replication lag spike caused by single-threaded replica SQL thread",
            '''-- Master executes bulk migration:
UPDATE orders SET archived = TRUE WHERE created_at < '2025-01-01'; -- 5,000,000 rows
-- Replica Seconds_Behind_Master jumps from 0 to 4,200 seconds!''',
            "Read-replicas serve stale data for over an hour; failover tools declare replicas out of sync.",
            [
                "Why does a single multi-million row UPDATE statement stall MySQL binlog replication?",
                "What is the difference between Statement-Based Replication (SBR) and Row-Based Replication (RBR)?",
                "How does multi-threaded replica configuration (`slave_parallel_workers`) mitigate replication lag?"
            ],
            "**Root cause:** A massive single-transaction UPDATE is serialized into the binary log. Even with multi-threaded replication, a single transaction cannot be split across multiple worker threads and must be executed sequentially by a single replica thread.\n\n**Fix:** Chunk large batch operations into small transactions (e.g. 5,000 rows per commit with sleep intervals):\n```sql\nUPDATE orders SET archived = TRUE WHERE created_at < '2025-01-01' LIMIT 5000;\n```\n**Configuration:** Configure `replica_parallel_type = LOGICAL_CLOCK` and `replica_parallel_workers = 8`."
        ),
        (
            "Deadlock on INSERT ... ON DUPLICATE KEY UPDATE under concurrent workers",
            '''-- Two workers concurrently insert the same user with unique secondary key:
INSERT INTO users (id, email, visits) 
VALUES (1, 'user@test.com', 1) 
ON DUPLICATE KEY UPDATE visits = visits + 1;''',
            "MySQL aborts Worker 2 with `ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction`.",
            [
                "Why does `ON DUPLICATE KEY UPDATE` take gap locks and next-key locks on unique secondary indexes?",
                "What lock mode is acquired on the duplicate index record before the update?",
                "How does replacing this with Redis atomic counter or optimistic application locking prevent deadlocks?"
            ],
            "**Root cause:** When evaluating duplicate keys on secondary unique indexes, InnoDB acquires an **Exclusive Next-Key Lock** covering the gap prior to the record. When two transactions race on the same gap, they obtain shared locks and then mutually wait for exclusive upgrade, deadlocking.\n\n**Fix:** Update counters in high-throughput in-memory stores like Redis (`HINCRBY user:1 visits 1`) and periodically persist aggregate tallies to MySQL."
        ),
        (
            "InnoDB buffer pool thrashing caused by full table scan on reporting query",
            '''-- Midnight analytical query runs on OLTP production master:
SELECT customer_id, SUM(total) 
FROM orders 
GROUP BY customer_id;''',
            "Immediately after the query starts, p99 latency for OLTP transactions jumps from 2 ms to 150 ms across the application.",
            [
                "How did the full table scan evict hot cached OLTP pages from the InnoDB Buffer Pool?",
                "What is the InnoDB midpoint insertion LRU algorithm and the `innodb_old_blocks_time` setting?",
                "What setting prevents transient batch scans from evicting warm operational cache blocks?"
            ],
            "**Root cause:** A massive sequential table scan loads cold disk pages into the InnoDB Buffer Pool, displacing hot working-set pages used by active OLTP transactions.\n\n**Buffer Pool Protection:** InnoDB uses a 3/8 split LRU queue (`innodb_old_blocks_pct = 37`). New pages are inserted at the midpoint. Crucially, `innodb_old_blocks_time` (default 1000ms) dictates that a page must be accessed *longer than 1000 ms after first read* to move to the young sublist.\n\n**Fix:** Ensure `innodb_old_blocks_time = 1000` is active and offload reporting queries to dedicated read replicas."
        ),
        (
            "Auto-increment gap exhaustion under transaction rollbacks",
            '''-- High-volume order ingestion (10,000 rollbacks per minute):
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (101, 50.0);
-- Validation error occurs -> ROLLBACK;''',
            "A table with only 100,000 active records exhausts a standard 32-bit signed `INT` primary key (ID exceeds 2,147,483,647).",
            [
                "Why are auto-increment counter sequences never rolled back when an INSERT transaction aborts?",
                "What catastrophic database error occurs when a primary key auto-increment counter reaches maximum value?",
                "What data type should always be used for primary key identifiers in high-volume production tables?"
            ],
            "**Root cause:** For concurrency performance, the auto-increment mutex generates sequential values immediately. If aborted transactions rolled back the counter, it would cause severe serialization bottlenecks and duplicate key collisions with subsequent transactions.\n\n**Failure Mode:** When signed `INT` hits 2,147,483,647, subsequent `INSERT` operations fail with `ERROR 1062: Duplicate entry '2147483647' for key 'PRIMARY'`, causing a total write outage.\n\n**Fix:** Always define primary keys with `BIGINT UNSIGNED` (up to $1.8 \times 10^{19}$ IDs)."
        )
    ]
}
