"""Diagnostic quiz questions, batch B: Modules 07-12 in Databases course.

Each entry is (title, code, symptom, questions, answer). A diagnostic question
shows real code plus an observed symptom and asks for cause, fix, and which test
would have caught it.
"""

from __future__ import annotations

DIAGNOSTICS: dict[str, list[tuple[str, str, str, list[str], str]]] = {
    "07": [
        (
            "ORA-04031 Shared Pool exhaustion from unshared literal SQL cursors",
            '''# Application constructs raw literal SQL strings in Python loop:
for user_id in user_id_list:
    cursor.execute(f"SELECT * FROM accounts WHERE id = {user_id}")''',
            "Database crashes with `ORA-04031: unable to allocate 4120 bytes of shared memory ('shared pool','unknown object','sga heap','kglsim heap')`.",
            [
                "Why does concatenating literal values into SQL strings exhaust the Oracle SGA Shared Pool?",
                "How does the Library Cache use SQL text hashing to detect reusable execution plans?",
                "What is the fix using bind variables, and what cursor sharing setting provides server-side relief?"
            ],
            "**Root cause:** Every query with distinct literal text produces a unique SHA-1 hash in the Oracle Library Cache. The database performs an expensive **Hard Parse** for every single execution, generating thousands of unique cursor heaps that fragment and exhaust the SGA Shared Pool.\n\n**Fix:** Use bind variables: `cursor.execute('SELECT * FROM accounts WHERE id = :id', {'id': user_id})`. Identical SQL text is hashed to the same Library Cache parent cursor, achieving **Soft Parses**.\n\n**Server Setting:** As a temporary emergency mitigation, set `CURSOR_SHARING = FORCE` in Oracle init parameters."
        ),
        (
            "Buffer busy waits on hot index leaf block",
            '''-- 1,000 concurrent threads inserting into table with monotonic sequence PK:
CREATE TABLE sensor_logs (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reading_val NUMBER
);''',
            "AWR report shows Top 5 Timed Events dominated by `buffer busy waits` (75% of total wait time).",
            [
                "Why does a monotonically ascending sequence create severe buffer contention on the rightmost leaf block of a B-Tree index?",
                "What is a Reverse Key Index, and how does it disperse concurrent inserts across the index tree?",
                "What range-scan limitation is introduced when an index is converted to a Reverse Key Index?"
            ],
            "**Root cause:** Monotonically increasing numbers always target the rightmost leaf block of the B-Tree index. 1,000 concurrent threads contend for exclusive buffer cache pin latches on the exact same physical disk block in the SGA Database Buffer Cache.\n\n**Reverse Key Index Fix:** `CREATE INDEX idx_sensor_rev ON sensor_logs (id) REVERSE;`. Reversing the binary bytes of sequential keys (e.g. 1001, 1002, 1003 -> 1001, 2001, 3001) hashes inserts across different leaf blocks throughout the entire index.\n\n**Trade-off:** Reverse Key Indexes cannot perform index range scans (`WHERE id BETWEEN 10 AND 50` must fall back to full table scan)."
        ),
        (
            "PGA memory exhaustion causing disk temp tablespace spill",
            '''-- Complex analytics query running on limited PGA:
SELECT customer_id, AVG(order_total) 
FROM orders 
GROUP BY customer_id 
ORDER BY AVG(order_total) DESC;''',
            "Query execution time degrades from 0.4s to 85s; Enterprise Manager reports massive `direct path read temp` and `direct path write temp` I/O.",
            [
                "What is the architectural distinction between Oracle SGA (Shared) and PGA (Program Global Area)?",
                "Why did the hash aggregation and sort operation spill from PGA Workareas into TEMP disk storage?",
                "What parameter governs maximum private workarea size per session?"
            ],
            "**Root cause:** Unlike the shared SGA, the PGA is private memory dedicated to an individual server process. When in-memory hash aggregation and sorting exceeds the session's allocated workarea (`PGA_AGGREGATE_TARGET` / `pga_aggregate_limit`), Oracle performs a multi-pass spill to the temporary tablespace on disk.\n\n**Fix:** Increase `PGA_AGGREGATE_TARGET` or tune the session: `ALTER SESSION SET WORKAREA_SIZE_POLICY = MANUAL; ALTER SESSION SET SORT_AREA_SIZE = 104857600;`."
        ),
        (
            "Redo log switch checkpoint incomplete hang",
            '''-- Heavy batch ETL loading 50,000,000 rows:
INSERT INTO warehouse_staging SELECT * FROM raw_external_stream;''',
            "Entire Oracle instance freezes completely; alert.log reports `Thread 1 cannot allocate new log, sequence 485; Checkpoint not complete`.",
            [
                "What does 'Checkpoint not complete' signify in the Oracle Redo Log Buffer architecture?",
                "Why does the Log Writer (LGWR) refuse to overwrite the next online redo log group?",
                "What two database configuration changes resolve this architectural bottleneck?"
            ],
            "**Root cause:** Oracle online redo logs are written circularly. Before LGWR can overwrite a redo log group, DBWn (Database Writer) must have flushed all dirty buffer cache blocks protected by that redo group to disk. If disk I/O cannot keep up with batch generation, LGWR stalls all instance writes.\n\n**Fix 1:** Add more online redo log groups and increase log file sizes (e.g. from 100MB to 4GB each).\n\n**Fix 2:** Increase checkpoint frequency or enable multiple database writer processes (`DB_WRITER_PROCESSES = 4`)."
        ),
        (
            "Library Cache latch contention on high-frequency hard parses",
            '''-- Web microservice with 200 connection pool workers executing dynamic SQL:
cursor.execute(f"SELECT * FROM products WHERE sku = '{sku_code}'")''',
            "CPU utilization reaches 100% with low TPS; `v$active_session_history` shows sessions waiting on `latch: library cache`.",
            [
                "What is a latch in Oracle database internal architecture, and how does it differ from a transaction lock?",
                "Why does parsing dynamic SQL require acquiring exclusive library cache latches?",
                "What is the architectural fix to reduce latch acquisition frequency?"
            ],
            "**Root cause:** A latch is a low-level, short-duration mutual exclusion primitive (spinlock) protecting shared SGA memory structures from concurrent modification. Parsing dynamic SQL requires acquiring the `library cache` latch to insert new syntax trees into the hash table.\n\n**Fix:** Rewrite queries with bind variables (`:sku_code`). Reusing execution plans bypasses exclusive library cache latch acquisition, allowing concurrent shared reads."
        )
    ],
    "08": [
        (
            "ORA-04091 Mutating Table error in row-level trigger",
            '''CREATE OR REPLACE TRIGGER trg_check_salary
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
DECLARE
    v_max_sal NUMBER;
BEGIN
    -- Querying the very table that is currently being modified!
    SELECT MAX(salary) INTO v_max_sal FROM employees WHERE dept_id = :NEW.dept_id;
    IF :NEW.salary > v_max_sal * 1.5 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Salary exceeds departmental ceiling');
    END IF;
END;''',
            "Updating employee salary fails with `ORA-04091: table HR.EMPLOYEES is mutating, trigger/function may not see it`.",
            [
                "What is a 'mutating table' in Oracle PL/SQL, and why does Oracle restrict row-level triggers from reading it?",
                "Why does a Compound Trigger eliminate the mutating table restriction?",
                "Which timing points (phases) are supported in an Oracle Compound Trigger?"
            ],
            "**Root cause:** A table is 'mutating' when it is in the middle of a DML statement. If a row-level trigger (`FOR EACH ROW`) reads the table, it would see an inconsistent, partially updated state, violating transaction consistency rules.\n\n**Fix:** Use a **Compound Trigger**. In the `BEFORE STATEMENT` phase, initialize state; in `AFTER EACH ROW`, record affected IDs into a package collection; in `AFTER STATEMENT`, query the table and perform bulk validation after the table has stabilized.\n\n**Compound Trigger Phases:** `BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, `AFTER STATEMENT`."
        ),
        (
            "Autonomous Transaction deadlock on uncommitted parent row lock",
            '''PROCEDURE transfer(p_from INT, p_to INT, p_amt NUMBER) IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    -- Parent transaction has ALREADY updated account p_from!
    UPDATE accounts SET balance = balance - p_amt WHERE id = p_from;
    COMMIT;
END;''',
            "Application freezes indefinitely; after 60 seconds, Oracle terminates the session with a deadlock error.",
            [
                "Why is an autonomous transaction considered a completely independent database session?",
                "What happens when an autonomous transaction attempts to modify a row locked by its parent transaction?",
                "What is the valid architectural use case for `PRAGMA AUTONOMOUS_TRANSACTION`?"
            ],
            "**Root cause:** `PRAGMA AUTONOMOUS_TRANSACTION` creates a separate child transaction boundary. It cannot see uncommitted changes made by the parent transaction and cannot acquire exclusive locks held by the parent. Attempting to update `p_from` causes the child to wait on the parent, while the parent waits for the procedure to return — an immediate deadlock!\n\n**Valid Use Case:** Autonomous transactions should **only** be used for independent audit logging or error logging that must commit even if the parent transaction rolls back: `INSERT INTO audit_log VALUES (...) COMMIT;`."
        ),
        (
            "Bulk FORALL processing losing error indexes without SAVE EXCEPTIONS",
            '''BEGIN
    FORALL i IN 1..order_ids.COUNT
        UPDATE orders SET status = 'PROCESSED' WHERE id = order_ids(i);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Batch failed: ' || SQLERRM);
END;''',
            "Row 42 has an invalid constraint; the entire batch of 10,000 updates aborts, and the exception handler cannot determine which specific row failed.",
            [
                "Why does standard FORALL abort execution on the very first encountered exception?",
                "What clause allows FORALL to process all valid rows and defer exception collection?",
                "How do you inspect individual error indices and error codes using `SQL%BULK_EXCEPTIONS`?"
            ],
            "**Root cause:** Without `SAVE EXCEPTIONS`, the first DML error immediately terminates the `FORALL` statement and rolls back uncommitted rows.\n\n**Fix:** Add `SAVE EXCEPTIONS`:\n```plsql\nFORALL i IN 1..order_ids.COUNT SAVE EXCEPTIONS\n    UPDATE orders SET status = 'PROCESSED' WHERE id = order_ids(i);\n```\nIn the exception block, catch `ORA-24381` and iterate through `SQL%BULK_EXCEPTIONS` to log `SQL%BULK_EXCEPTIONS(i).ERROR_INDEX` and `SQL%BULK_EXCEPTIONS(i).ERROR_CODE`."
        ),
        (
            "Package state invalidation ORA-04068 under concurrent sessions",
            '''-- Session A is actively running a banking package with package package variables
-- DBA recompiles the package in Session B:
ALTER PACKAGE banking_pkg COMPILE BODY;''',
            "Session A's next call crashes with `ORA-04068: existing state of packages has been discarded; ORA-04061: existing state of package body has been invalidated`.",
            [
                "What is package state in Oracle PL/SQL, and where is it stored?",
                "Why does compiling a package body invalidate the session memory (UGA/PGA) of all active sessions?",
                "How does `PRAGMA SERIALLY_REUSABLE` eliminate package state invalidation for stateless utility packages?"
            ],
            "**Root cause:** When a package declares global package variables (variables outside procedures), Oracle allocates state memory in each user's UGA. Recompiling the package invalidates this memory structure across all connected sessions.\n\n**Fix:** Add `PRAGMA SERIALLY_REUSABLE;` to the package specification. This frees package state at the end of each database call, preventing cross-call state persistence and eliminating ORA-04068 errors during zero-downtime hot code deployments."
        ),
        (
            "PL/SQL context switching penalty in row-by-row cursor loops",
            '''FOR r IN (SELECT id, salary FROM employees) LOOP
    UPDATE employees SET bonus = r.salary * 0.1 WHERE id = r.id;
END LOOP;''',
            "Processing 200,000 employees takes 45 seconds due to millions of internal context switches.",
            [
                "What is a context switch between the PL/SQL runtime engine and the SQL query engine?",
                "How does `BULK COLLECT INTO ... LIMIT` with `FORALL` eliminate context switching overhead?",
                "What is the single-statement SQL replacement that eliminates PL/SQL altogether?"
            ],
            "**Root cause:** A row-by-row cursor loop alternates execution between the PL/SQL procedural engine and the SQL execution engine on every single iteration (200,000 context switches).\n\n**Fix 1 (Single SQL):** `UPDATE employees SET bonus = salary * 0.1;` (0 context switches, executed entirely inside the SQL engine in 0.2 seconds).\n\n**Fix 2 (Batching):** Use `FETCH c BULK COLLECT INTO l_data LIMIT 1000;` followed by `FORALL i IN 1..l_data.COUNT`."
        )
    ],
    "09": [
        (
            "Cache Fusion block ping thrashing across RAC interconnect",
            '''-- Instance 1 and Instance 2 concurrently inserting high-volume orders
-- Primary key generated via standard cached sequence:
CREATE SEQUENCE order_seq INCREMENT BY 1 CACHE 20;''',
            "Interconnect network saturates; Top Wait Event is `gc current block busy` and `gc buffer busy acquire`; transaction throughput drops by 80%.",
            [
                "What is Oracle RAC Cache Fusion, and how does it transfer dirty data blocks between instance buffer caches?",
                "Why does a low sequence cache size cause Global Cache Service (GCS) block ping thrashing?",
                "How does increasing sequence cache to `CACHE 5000 NOORDER` eliminate interconnect contention?"
            ],
            "**Root cause:** Small sequence cache (`CACHE 20`) causes Instance 1 and Instance 2 to constantly fight for exclusive ownership of the sequence data block and index leaf blocks. Cache Fusion must ping the block across the private interconnect on every 20 inserts.\n\n**Fix:** `ALTER SEQUENCE order_seq CACHE 10000 NOORDER;`. Each RAC instance preallocates a large contiguous chunk of numbers locally, completely eliminating cross-instance Cache Fusion block transfers."
        ),
        (
            "Primary database freeze under Data Guard MAXIMUM PROTECTION",
            '''-- Oracle Data Guard configured with MAXIMUM PROTECTION:
ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PROTECTION;
# Network maintenance switch reboot causes a 10-second blip on standby link!''',
            "The production primary database immediately panics and terminates with `ORA-03113: end-of-file on communication channel`; the entire business platform goes offline.",
            [
                "What is the mathematical durability contract of Data Guard MAXIMUM PROTECTION mode?",
                "Why is the primary database designed to intentionally crash if the standby cannot acknowledge redo?",
                "Which protection mode should be used to guarantee Zero Data Loss (RPO=0) without taking down the primary upon link failure?"
            ],
            "**Root cause:** `MAXIMUM PROTECTION` strictly enforces Zero Data Loss ($RPO=0$) under all circumstances. If LGWR cannot synchronously confirm redo receipt on at least one standby database, the primary instance **intentionally terminates** to prevent un-replicated data from ever being committed.\n\n**Fix:** Use `MAXIMUM AVAILABILITY`. In this mode, transactions commit synchronously ($RPO=0$), but if the standby becomes unreachable, the primary automatically downgrades to asynchronous mode to preserve cluster uptime, resynchronizing upon reconnection."
        ),
        (
            "Private interconnect split-brain node eviction",
            '''# Switch configuration error on private RAC cluster heartbeat interface:
# Heartbeat packets delayed by 32 seconds (exceeding misscount threshold)''',
            "Node 2 abruptly reboots; alert.log reports `CRS-1607: Node 2 was evicted by CSS daemon; voting disk lease expired`.",
            [
                "What role do Voting Disks and the Cluster Synchronization Service (CSS) play in Oracle RAC split-brain prevention?",
                "Why must a partitioned node commit 'fencing' (reboot) when it loses quorum?",
                "How do redundant dedicated NICs and LACP network bonding prevent spurious evictions?"
            ],
            "**Root cause:** If heartbeat communication is interrupted between nodes, each partition could attempt to access shared SAN/NAS disks independently, causing catastrophic filesystem and database corruption. The CSS daemon uses Voting Disks to determine majority quorum; the minority partition is forcefully evicted (fenced) via reboot.\n\n**Hardware Fix:** Configure redundant dedicated private network interfaces with LACP bonding on independent physical switches, ensuring no single network cable or switch failure drops the cluster interconnect."
        ),
        (
            "Active Data Guard read-only standby ORA-01555 Snapshot Too Old",
            '''-- Analytical query running on Active Data Guard read-only replica:
SELECT * FROM financial_ledger WHERE fiscal_year = 2025; -- Takes 45 minutes
-- Primary database commits millions of small updates and purges undo''',
            "Standby reporting query crashes after 30 minutes with `ORA-01555: snapshot too old: rollback segment number 12 with name '_SYSSMU12$' too small`.",
            [
                "Why does a query on a read-only standby database require undo segments generated on the primary?",
                "What happens when the primary database overwrites old undo blocks before the standby query finishes?",
                "What setting on the primary database (`UNDO_RETENTION`) prevents premature undo overwrite?"
            ],
            "**Root cause:** Under MVCC, long-running queries must reconstruct past image blocks using undo data. On Active Data Guard, queries use the standby's replicated undo stream. If high transaction volume on the primary causes undo blocks to be overwritten before the standby query completes, reconstruction fails with `ORA-01555`.\n\n**Fix:** Increase `UNDO_RETENTION` on both primary and standby (e.g. `UNDO_RETENTION = 14400` for 4 hours) and enable `RETENTION GUARANTEE` on the undo tablespace."
        ),
        (
            "GoldenGate bidirectional replication ping-pong infinite loop",
            '''-- User updates row on Node A:
UPDATE users SET status = 'ACTIVE' WHERE user_id = 10;
-- GoldenGate captures mutation on A, replicates to B.
-- GoldenGate on B captures mutation on B, replicates back to A!''',
            "A single UPDATE triggers millions of circular replication events, consuming 100% CPU and network bandwidth.",
            [
                "What causes replication ping-pong loops in bidirectional active-active replication?",
                "How does GoldenGate's `SUPPRESSTRIGGERS` and `GETREPLICATES / IGNOREREPLICATES` parameter prevent loopback?",
                "What is Conflict Detection and Resolution (CDR) based on monotonic timestamps?"
            ],
            "**Root cause:** The Extract process on Node B captures changes applied by the Replicat process on Node B and forwards them back to Node A, causing an infinite replication feedback loop.\n\n**Fix:** Configure the Extract process to ignore transactions generated by the Replicat process using `TRANLOGOPTIONS EXCLUDEUSER ggs_admin` or `IGNOREREPLICATES`.\n\n**Conflict Resolution:** Implement timestamp-based CDR: only apply updates if incoming timestamp is strictly greater than local row timestamp."
        )
    ],
    "10": [
        (
            "Document exceeding MongoDB 16MB BSON size limit",
            '''# IoT sensor schema storing unbounded array of readings inside device doc:
db.sensors.update_one(
    {"_id": "sensor_99"},
    {"$push": {"readings": {"timestamp": datetime.now(), "temp": 24.5}}}
)''',
            "After 6 months of operation, application crashes with `pymongo.errors.WriteError: BSONObj size: 16793610 (0x100400A) is invalid. Size must be between 0 and 16793600(16MB)`.",
            [
                "What is MongoDB's hard maximum BSON document size limit, and why was it chosen?",
                "What schema design anti-pattern causes unbounded array growth in document databases?",
                "How does the Time-Series Bucketing Pattern (e.g. one document per sensor per hour) resolve this limit?"
            ],
            "**Root cause:** MongoDB enforces a hard **16 MB BSON document size limit** to prevent memory bloat in the WiredTiger cache and avoid network socket saturation. Storing unbounded arrays inside a single document guarantees eventual failure.\n\n**Fix:** Use the **Bucketing Pattern**: create one document per hour/day with a fixed pre-allocated array of up to 60 readings (e.g., `_id: \"sensor_99:2026-03-08:14\"`), or store each reading as an individual document in a dedicated time-series collection."
        ),
        (
            "ObjectId generation timestamp drift under unsynchronized clocks",
            '''# Server A clock is running 15 minutes ahead due to NTP failure
doc_id_a = ObjectId() # Generated on Server A
doc_id_b = ObjectId() # Generated on Server B (accurate clock)
# Sorting documents by _id:
docs = list(db.orders.find().sort("_id", 1))''',
            "Orders created on Server A appear in the future; real-time order processing queues process orders completely out of chronological sequence.",
            [
                "What are the four components encoded within a standard 12-byte MongoDB `ObjectId`?",
                "Why does ObjectId timestamp generation depend on local server operating system clocks?",
                "What separate monotonically increasing sequence or distributed timestamp authority should be used when strict global ordering is required?"
            ],
            "**Root cause:** The first 4 bytes of a 12-byte `ObjectId` represent a Unix epoch timestamp (in seconds) read from the local machine clock. If machine clocks drift, ObjectIds generated on different servers lose monotonic global ordering.\n\n**ObjectId Structure:** 4-byte timestamp + 5-byte random value (machine/process identifier) + 3-byte incrementing counter.\n\n**Fix:** Ensure NTP/Chrony synchronizes all app servers to within milliseconds. For strict business sequencing, generate cluster-wide monotonic IDs using a counter collection or Snowflake ID generator."
        ),
        (
            "BSON integer type coercion causing silent numeric precision loss",
            '''# Python driver writing integer into MongoDB:
large_balance = 5_000_000_000 # 5 Billion (requires 64-bit int)
db.accounts.insert_one({"user": "corp", "balance": large_balance})

# Downstream Node.js / Python service reads balance with 32-bit driver:
doc = db.accounts.find_one({"user": "corp"})''',
            "Balance is read as `705032704` (overflow wrapped) or throws `BSONTypeError: value out of bounds`.",
            [
                "What is the difference between BSON type `` (double), `` (int32), and `` (int64)?",
                "How does Python's dynamic arbitrary-precision integer model interact with strict BSON wire types?",
                "What BSON type must be used when storing monetary values requiring exact decimal precision?"
            ],
            "**Root cause:** BSON distinguishes between 32-bit signed integers (`int32`, max 2.14B) and 64-bit signed integers (`int64`, max 9.22E18). If an integer exceeds $2^{31}-1$, it must be explicitly encoded as `int64`. In languages without native 64-bit integers (e.g. JavaScript Number), precision is lost.\n\n**Monetary Precision:** Always use **BSON Decimal128** (`NumberDecimal` / `bson.decimal128.Decimal128`) for financial balances to prevent floating-point and integer truncation errors."
        ),
        (
            "Compound index prefix mismatch causing COLLSCAN",
            '''-- Collection has compound index on (status, created_at, customer_id)
db.orders.create_index([("status", 1), ("created_at", -1), ("customer_id", 1)])

-- Query issued by user dashboard:
db.orders.find({"customer_id": "cust_42", "created_at": {"$gte": start_date}}).explain("executionStats")''',
            "`executionStages.stage` reports `COLLSCAN`; query examines 2,000,000 documents instead of using the index.",
            [
                "What is the Golden Rule of compound index prefixing in B-Tree / MongoDB indexes?",
                "Why does omitting `status` prevent the query planner from using the index?",
                "What index definition satisfies the Equality, Sort, Range (ESR) rule for this query?"
            ],
            "**Root cause:** B-Tree compound indexes can only be utilized if query filters include the **index prefix**. Since the query omits the leading column `status`, the database cannot traverse the compound B-Tree and falls back to a full collection scan (`COLLSCAN`).\n\n**ESR Rule Fix:** Create an index matching Equality, Sort, Range: `db.orders.create_index([('customer_id', 1), ('created_at', -1)])`."
        ),
        (
            "Unindexed array field search causing multi-key explosion",
            '''# Query filtering on embedded array tags without multikey index:
db.articles.find({"tags": "distributed-systems"})''',
            "Under 5,000 concurrent queries, WiredTiger cache fills with un-indexed document scans; memory usage hits 95%.",
            [
                "What is a Multikey Index in MongoDB, and how does it index array fields?",
                "What restriction prevents creating compound multikey indexes where two fields are both arrays?",
                "Which test in the test suite verifies BSON serialization and collection indexing?"
            ],
            "**Root cause:** Querying an array element without an index forces a full collection scan where every document's array is unpacked and scanned in memory.\n\n**Fix:** Create a multikey index: `db.articles.create_index({'tags': 1})`. MongoDB automatically creates an index entry for every individual element in the array.\n\n**Multikey Restriction:** A compound multikey index cannot have more than one field that is an array (to prevent exponential Cartesian product entry explosion in index B-Trees)."
        )
    ],
    "11": [
        (
            "Aggregation pipeline exceeding 100MB RAM limit without allowDiskUse",
            '''# Aggregation grouping 10,000,000 documents by customer
pipeline = [
    {"$group": {"_id": "$customer_id", "total_spend": {"$sum": "$amount"}}},
    {"$sort": {"total_spend": -1}}
]
db.orders.aggregate(pipeline)''',
            "Query crashes with `pymongo.errors.OperationFailure: PlanExecutor error during aggregation :: caused by :: Sort exceeded memory limit of 104857600 bytes, but did not allowExternalSort`.",
            [
                "What is the default RAM limit for an individual aggregation stage in MongoDB?",
                "What flag enables spilling intermediate aggregation groups to disk?",
                "How does placing a `$match` filter before `$group` reduce memory footprint?"
            ],
            "**Root cause:** MongoDB restricts RAM usage for any single aggregation pipeline stage to **100 MB** to prevent rogue queries from starving cluster memory. Unindexed `$group` and `$sort` stages across millions of documents exceed this limit.\n\n**Fix 1:** Set `allowDiskUse=True`: `db.orders.aggregate(pipeline, allowDiskUse=True)`.\n\n**Fix 2 (Architectural):** Pre-filter data using `$match` at the beginning of the pipeline so only relevant rows reach `$group`, and ensure `$sort` uses an index."
        ),
        (
            "Monotonically increasing shard key creating single-shard write hotspot",
            '''# Cluster sharded using default ObjectId as shard key:
sh.shardCollection("shop.orders", {"_id": 1})''',
            "In an 8-shard cluster, 100% of all write traffic lands exclusively on Shard 8; Shards 1 through 7 remain completely idle at 0% CPU.",
            [
                "Why does a monotonically increasing shard key (`_id` or `timestamp`) route all writes to a single chunk?",
                "What is Hashed Sharding, and how does it distribute sequential writes uniformly across all cluster nodes?",
                "What trade-off does Hashed Sharding introduce for range-based queries?"
            ],
            "**Root cause:** Since `ObjectId` has a leading timestamp, every new document has an `_id` greater than the current max chunk boundary. All inserts land in the topmost chunk on the 'max key' shard (Jailed Chunk Hotspotting).\n\n**Fix:** Use **Hashed Sharding**: `sh.shardCollection('shop.orders', {'_id': 'hashed'})`. Hashes `_id` uniformly with MD5 across all shards.\n\n**Trade-off:** Hashed sharding scatters sequential data; range queries (`_id >= 100 AND _id <= 200`) cannot perform range seeks and must scatter-gather across all shards."
        ),
        (
            "Scatter-Gather query latency cliff on un-sharded query filters",
            '''# Collection sharded on user_id:
# Query searches by email address:
db.users.find({"email": "alice@company.com"})''',
            "Query p99 latency is 450 ms in a 32-shard cluster, even though email is indexed on every individual shard.",
            [
                "Why must `mongos` router broadcast un-sharded queries to every shard in the cluster (Scatter-Gather)?",
                "How does the slowest shard in the cluster dictate overall query latency?",
                "How does Global Secondary Indexing or Targeted Routing mitigate scatter-gather overhead?"
            ],
            "**Root cause:** The `mongos` query router uses the shard key (`user_id`) to route queries directly to the holding shard. Because `email` is not part of the shard key, `mongos` cannot determine where the document lives and must broadcast the query to **all 32 shards**, waiting for all responses (Scatter-Gather).\n\n**Latency Cliff:** Overall latency is bounded by the slowest, highest-load shard in the cluster ($O(\max(\text{shard latency}))$).\n\n**Fix:** Always include the shard key in query predicates (`{'user_id': 101, 'email': ...}`) to enable **Targeted Routing**."
        ),
        (
            "Unwind memory explosion on high-cardinality embedded arrays",
            '''# Document contains array of 25,000 sub-items:
pipeline = [
    {"$match": {"category": "electronics"}},
    {"$unwind": "$items"},
    {"$group": {"_id": "$items.sku", "count": {"$sum": 1}}}
]
db.catalogs.aggregate(pipeline)''',
            "Aggregation process consumes 32 GB RAM, triggering Linux OOM killer (`dmesg: Out of memory: Killed process mongod`).",
            [
                "How does `$unwind` duplicate document state in memory for every array element?",
                "Why should high-cardinality collections avoid large arrays in document modeling?",
                "What alternative projection strategy filters array items prior to unwinding?"
            ],
            "**Root cause:** `$unwind` physically creates a new document in memory for every single element in the array. Unwinding 1,000 documents with 25,000 items generates 25,000,000 documents in memory simultaneously, overwhelming WiredTiger cache.\n\n**Fix:** Pre-filter array elements using `$filter` in a `$project` stage before unwinding, or remodel the relationship into a separate normalized collection."
        ),
        (
            "Shard chunk balancing lock contention during peak traffic hours",
            '''# Balancer runs continuously across cluster during Black Friday sale:
# Jumbo chunks split and migrate across network links''',
            "Active checkout transactions experience intermittent lock timeouts and 504 Gateway Errors.",
            [
                "How does MongoDB chunk migration acquire collection metadata locks on source and destination shards?",
                "What window configuration parameter restricts the chunk balancer to low-traffic off-peak maintenance hours?",
                "What is a 'Jumbo Chunk', and why does it fail to split automatically?"
            ],
            "**Root cause:** Moving chunks between shards requires transferring data over network links and taking brief distributed locks during the critical catch-up phase. Running balancing during peak traffic creates heavy lock contention and saturates internal cluster replication bandwidth.\n\n**Fix:** Define an off-peak balancing window:\n```javascript\nsh.setBalancerState(true);\nsh.updateConfigSetting(\"balancer.activeWindow\", { start: \"02:00\", stop: \"05:00\" });\n```\n**Jumbo Chunks:** Chunks exceeding maximum chunk size (64MB) that cannot be split because all documents share the exact same shard key value."
        )
    ],
    "12": [
        (
            "Redis OOM crash due to missing maxmemory-policy configuration",
            '''# redis.conf default settings:
# maxmemory 4gb
# maxmemory-policy noeviction

# Ingestion pipeline pushes 10,000,000 cache keys into Redis''',
            "Application writes fail with `redis.exceptions.ResponseError: OOM command not allowed when used memory > 'maxmemory'`.",
            [
                "What does the default `noeviction` policy do when Redis reaches its memory threshold?",
                "What is the difference between `allkeys-lru` and `volatile-lru` eviction policies?",
                "Why is Redis LRU an approximation rather than an exact linked-list LRU?"
            ],
            "**Root cause:** Under `noeviction`, Redis refuses all write commands (`SET`, `HSET`, `LPUSH`) with an OOM error once memory hits `maxmemory`.\n\n**Fix:** Configure an active eviction policy in `redis.conf`: `maxmemory-policy allkeys-lru`. When memory is full, Redis evicts the least recently used keys automatically.\n\n**Approximate LRU:** Redis does not maintain an exact doubly-linked list of all keys (which would cost 16 bytes of RAM per key); instead, it samples $N$ random keys (configured by `maxmemory-samples`, default 5) and evicts the best candidate among them."
        ),
        (
            "SkipList memory bloat compared to compact ziplist/listpack",
            '''# Storing 1,000,000 leaderboards with only 5 members each:
for board_id in range(1_000_000):
    r.zadd(f"board:{board_id}", {"player1": 10, "player2": 20})''',
            "Redis consumes 1.8 GB RAM; memory analysis reveals 70% of memory is pointer overhead.",
            [
                "What is the memory structure difference between a SkipList and a Listpack/Ziplist for small sorted sets?",
                "Which configuration setting controls the maximum size before a Sorted Set upgrades to a SkipList?",
                "What is the memory savings ratio achieved by keeping small sorted sets encoded as listpacks?"
            ],
            "**Root cause:** A full SkipList node allocates multiple forward pointers (`zskiplistLevel`), dict entry structures, and dynamic string buffers. For small sets (2–10 elements), pointer overhead is 10x larger than the actual payload data.\n\n**Fix:** Tune `zset-max-listpack-entries 128` and `zset-max-listpack-value 64`. Redis will store small sorted sets as contiguous flat byte arrays (listpacks), reducing memory footprint by over 70%."
        ),
        (
            "Large HSET rehashing latency spike blocking event loop single thread",
            '''# Storing 5,000,000 fields inside a single Redis Hash key:
for i in range(5_000_000):
    r.hset("global_metrics", f"metric_{i}", i)''',
            "Every few minutes, Redis experiences a 250 ms latency freeze; sentinel triggers false-positive failover.",
            [
                "How does Redis progressive rehashing work, and why does rehashing a 5-million-element hash table cause latency spikes?",
                "Why does Redis single-threaded event loop architecture make large operations hazardous?",
                "How should massive key spaces be partitioned into smaller independent hashes?"
            ],
            "**Root cause:** Expanding a hash table dictionary requires doubling the bucket array (e.g. from 4M to 8M slots). Allocating and zeroing an 8-million-pointer array in memory takes hundreds of milliseconds, blocking Redis's single-threaded event loop.\n\n**Fix:** Shard large hashes using bucket hashing: instead of 1 hash with 5,000,000 fields, split into 1,000 hashes with 5,000 fields each: `hset(f'metrics:{hash(key) % 1000}', key, value)`."
        ),
        (
            "AOF fsync always blocking single-threaded write throughput",
            '''# redis.conf configured for maximum durability:
appendonly yes
appendfsync always''',
            "Redis throughput collapses from 120,000 ops/sec to 1,200 ops/sec; NVMe disk write queues saturate.",
            [
                "What does `appendfsync always` force the Redis main thread to do before acknowledging every write command?",
                "What is the operational difference between `always`, `everysec`, and `no`?",
                "Why is `appendfsync everysec` the industry standard recommended production balance?"
            ],
            "**Root cause:** Under `appendfsync always`, the main Redis server thread executes a blocking `fsync()` system call to physical disk before acknowledging every single client command. Disk I/O latency (0.5–2 ms) directly throttles the in-memory engine.\n\n**Fix:** Configure `appendfsync everysec`. Fsync is offloaded to a background thread once per second. Redis achieves 100,000+ ops/sec with a maximum theoretical loss window of 1–2 seconds of data during power loss."
        ),
        (
            "Simple Dynamic String (SDS) buffer memory fragmentation on string append loops",
            '''# In-memory buffer construction appending small byte chunks in a loop:
sds = SimpleDynamicString("START")
for i in range(1000):
    sds.append(f"_chunk_{i}")''',
            "Memory allocated is significantly larger than payload length; inspect shows `alloc` capacity doubled repeatedly.",
            [
                "What is the growth buffer pre-allocation algorithm in Redis Simple Dynamic Strings (SDS)?",
                "Why does SDS double capacity when length is less than 1MB?",
                "What method in `SimpleDynamicString` truncates or compacts unused pre-allocated capacity?"
            ],
            "**Root cause:** To prevent $O(N^2)$ memory allocations on frequent string appends, SDS pre-allocates spare capacity: if new length is $< 1\text{ MB}$, it allocates $2 \times \text{new\_len}$; if $> 1\text{ MB}$, it allocates $\text{new\_len} + 1\text{ MB}$.\n\n**Compaction:** When buffer mutations are complete, call `sds.free_unused()` or `sds.truncate()` to release unutilized allocated memory back to the heap allocator."
        )
    ]
}