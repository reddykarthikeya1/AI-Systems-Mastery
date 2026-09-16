from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

QUIZ_DATA = [
    (
        "Module_02_Modern_SQL_Mastery_Advanced_Queries",
        "Modern SQL Mastery & Advanced Analytics",
        [
            ("What is the formal difference between RANK() and DENSE_RANK() when ties occur in window ordering?",
             "RANK() leaves gaps in the sequence following ties (e.g. 1, 2, 2, 4), while DENSE_RANK() leaves no gaps (e.g. 1, 2, 2, 3)."),
            ("Why does WHERE id NOT IN (SELECT foreign_id FROM t) evaluate to 0 rows if any foreign_id is NULL?",
             "Because in three-valued logic, comparison with NULL yields UNKNOWN. Any condition WHERE UNKNOWN is treated as false."),
            ("How does a Common Table Expression (CTE) differ from a subquery in execution optimization?",
             "In modern query planners, non-recursive CTEs can be inlined or materialized as temp tables, whereas subqueries are typically inlined."),
            ("Explain how RECURSIVE CTE termination works.",
             "The recursive member executes repeatedly, taking the previous iteration's result as input until it returns an empty result set."),
            ("What is an Anti-Join, and how is it implemented using NOT EXISTS?",
             "An anti-join returns rows from table A that have no matching record in table B: WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.id = A.id)."),
            ("What is the default window frame when ORDER BY is specified without a ROWS clause?",
             "RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, which lumps duplicate peer values together."),
            ("How does LEAD(col, 1) OVER (...) differ from LAG(col, 1) OVER (...)?",
             "LEAD accesses the following row value, while LAG accesses the preceding row value."),
            ("Why are correlated subqueries in a SELECT list often an anti-pattern?",
             "They execute once per row in the outer query ($O(N)$ execution), whereas a JOIN or window function executes in set-oriented batches."),
            ("How does COALESCE(val, 'N/A') differ from NULLIF(val1, val2)?",
             "COALESCE returns the first non-null argument. NULLIF returns NULL if both arguments are equal; otherwise returns the first argument."),
            ("What is the difference between UNION and UNION ALL?",
             "UNION deduplicates rows by performing an expensive sort/hash set operation; UNION ALL simply appends streams without deduplication.")
        ],
        ("Implement a query calculating the 7-day moving average of daily sales per region.",
         "Write a recursive CTE that computes transitive closure over an acyclic bill-of-materials graph.")
    ),
    (
        "Module_03_Embedded_Databases_SQLite_WAL",
        "Embedded Databases: SQLite & WAL Architecture",
        [
            ("How does SQLite Write-Ahead Logging (WAL) differ from the default ROLLBACK journal mode?",
             "In WAL mode, changes are appended to a separate -wal file, allowing concurrent readers to read from the main database while a writer appends frames."),
            ("Can readers block writers in SQLite WAL mode?",
             "No. Readers never block writers, and writers never block readers."),
            ("What does PRAGMA synchronous = NORMAL guarantee in WAL mode?",
             "It guarantees durability across application crashes, and calls fsync during checkpoints, providing an optimal balance of safety and speed."),
            ("What causes a -wal file to grow indefinitely?",
             "An active long-running read transaction holds an open read snapshot, preventing the checkpoint from truncating older frames."),
            ("What is a WAL checkpoint?",
             "The process of copying committed frame pages from the -wal file back into the primary .db file and resetting log pointers."),
            ("Why must custom scalar functions in SQLite be registered per database connection?",
             "SQLite stores function pointers in the in-memory connection object (C struct), not on disk in the database file."),
            ("What does PRAGMA busy_timeout = 5000 do?",
             "It instructs SQLite to sleep and retry for up to 5,000 ms before returning SQLITE_BUSY when encountering a locked database."),
            ("How does SQLite enforce single-writer concurrency across multiple operating system processes?",
             "Using operating system file-level byte-range locks on the database and WAL index file (.shm)."),
            ("What is the .shm file accompanying a SQLite WAL database?",
             "A shared-memory index file mapping WAL frame numbers to database page numbers for fast $O(1)$ reader lookups."),
            ("When should you NOT use SQLite in production?",
             "For high-volume multi-node distributed systems, network file systems (NFS), or write workloads exceeding hundreds of concurrent writers.")
        ],
        ("Benchmark single-threaded write throughput across DELETE vs TRUNCATE vs WAL journal modes.",
         "Implement a custom SQLite C/Python aggregate function that computes rolling variance in a single pass.")
    ),
    (
        "Module_04_PostgreSQL_Core_Advanced_Types",
        "PostgreSQL Core Architecture & Advanced Types",
        [
            ("How does PostgreSQL's process-based architecture differ from multi-threaded databases like MySQL?",
             "PostgreSQL forks an independent operating system backend process for each client connection, sharing memory via the Shared Buffer Pool."),
            ("What is the difference between JSON and JSONB in PostgreSQL?",
             "JSON stores exact textual representation (requiring re-parsing on every query), whereas JSONB stores parsed binary format supporting fast indexing."),
            ("Which index type is required to accelerate JSONB containment queries (`@>`)?",
             "A Generalized Inverted Index (GIN) using either jsonb_ops or jsonb_path_ops."),
            ("How do PostgreSQL array operators `&&` and `@>` work?",
             "`&&` tests for array overlap (common elements), while `@>` tests if the left array contains all elements of the right array."),
            ("What is an EXCLUDE USING GIST constraint, and how does it prevent double-booking?",
             "It enforces that no two rows overlap on a range type (e.g. daterange or tsrange) using GiST index bounding-box tests."),
            ("Why should you use BIGINT GENERATED ALWAYS AS IDENTITY instead of standard SERIAL?",
             "SERIAL is a non-standard macro creating an underlying sequence susceptible to manual sequence permission drift; IDENTITY is SQL-standard."),
            ("What role does PgBouncer play in high-throughput PostgreSQL environments?",
             "It pools lightweight client connections and reuses a small set of persistent PostgreSQL backend processes, preventing memory exhaustion."),
            ("What is a PostgreSQL DOMAIN type?",
             "A user-defined data type based on an underlying primitive with built-in CHECK constraints (e.g. valid email format)."),
            ("How does TOAST (The Oversized-Attribute Storage Technique) work in PostgreSQL?",
             "Values exceeding ~2KB are compressed and stored out-of-line in separate TOAST tables, keeping main heap pages compact."),
            ("What is the significance of the `work_mem` configuration parameter?",
             "It defines the amount of RAM allocated per sort or hash join operation before spilling intermediate data to temporary disk files.")
        ],
        ("Design a multi-tenant schema with JSONB document validation and GIN index performance verification.",
         "Implement a conference room reservation system using tsrange and EXCLUDE constraints preventing overlapping slots.")
    ),
    (
        "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN",
        "PostgreSQL MVCC, Vacuuming & Execution Plans",
        [
            ("How does PostgreSQL implement Multi-Version Concurrency Control (MVCC) without in-place updates?",
             "Every UPDATE writes a completely new tuple version to the heap page, populating `xmin` (creation transaction) and `xmax` (deletion transaction)."),
            ("What is the purpose of the PostgreSQL Visibility Map?",
             "It tracks which heap pages contain only tuples visible to all current transactions, allowing index-only scans to skip checking heap pages."),
            ("What happens during a standard VACUUM vs VACUUM FULL?",
             "Standard VACUUM marks dead tuple space as reusable without shrinking file size; VACUUM FULL rewrites the table into a new file and reclaims disk space under an exclusive lock."),
            ("Why does EXPLAIN (ANALYZE, BUFFERS) provide more actionable insight than plain EXPLAIN?",
             "Plain EXPLAIN shows planner estimates; ANALYZE actually executes the query and reports real runtime, while BUFFERS shows exact shared buffer cache hits and disk reads."),
            ("What is the difference between a Sequential Scan, an Index Scan, and a Bitmap Index Scan?",
             "Seq Scan reads all heap pages; Index Scan navigates B-Tree to fetch heap tuples individually; Bitmap Index Scan builds an in-memory bitmap of matching pages before reading them sequentially."),
            ("What is Transaction ID (XID) wraparound, and how does PostgreSQL prevent data loss?",
             "PostgreSQL 32-bit transaction counters wrap around after 2 billion transactions. Autovacuum freeze runs freeze older tuples with FrozenXID to prevent them from appearing in the future."),
            ("Why should you always create production indexes using CREATE INDEX CONCURRENTLY?",
             "Standard CREATE INDEX locks the table against all writes; CONCURRENTLY runs two scans without blocking concurrent DML."),
            ("What is a Partial Index, and when should you use one?",
             "An index created with a WHERE clause (e.g. `WHERE status = 'PENDING'`), keeping the index compact and fast for specific query filters."),
            ("How does a B-Tree index handle high-cardinality vs low-cardinality columns?",
             "B-Trees excel on high-cardinality keys. On low-cardinality keys (boolean/status), B-Trees provide minimal selectivity unless combined in composite or partial indexes."),
            ("What is HOT (Heap-Only Tuples) optimization in PostgreSQL?",
             "When an update does not modify indexed columns and the new tuple fits on the same page, PostgreSQL links them without creating new index entries.")
        ],
        ("Analyze query plan changes between Index Scan and Bitmap Heap Scan by adjusting random_page_cost.",
         "Simulate high dead tuple bloat using repeated concurrent UPDATEs and observe autovacuum reclamation behavior.")
    ),
    (
        "Module_06_MySQL_MariaDB_InnoDB_Replication",
        "MySQL & InnoDB Architecture, Buffer Pool & Replication",
        [
            ("How does InnoDB's Clustered Index architecture differ from secondary indexes?",
             "The table's primary key forms the clustered index where leaf nodes store the actual row data. Secondary indexes store the primary key value as their pointer."),
            ("What is the purpose of the InnoDB Doublewrite Buffer?",
             "It writes dirty pages to a contiguous disk buffer before writing to primary data files, preventing page corruption from torn writes during crashes."),
            ("Explain the difference between Statement-Based Replication (SBR) and Row-Based Replication (RBR).",
             "SBR transmits SQL statements (prone to non-deterministic divergence, e.g. NOW()); RBR transmits exact before/after row byte changes."),
            ("What is a Global Transaction Identifier (GTID) in MySQL replication?",
             "A unique identifier assigned to every committed transaction across a cluster, allowing seamless replica failover without parsing binlog file offsets."),
            ("How does InnoDB detect and resolve deadlocks?",
             "It automatically detects cycles in its wait-for graph and rolls back the transaction with the fewest undo log records (least expensive to undo)."),
            ("What role does the InnoDB Redo Log (ib_logfile) play during crash recovery?",
             "It provides Write-Ahead Logging; upon restart, InnoDB replays committed transactions from the redo log that had not yet reached data pages."),
            ("How does the InnoDB Buffer Pool LRU list prevent full table scans from evicting cached OLTP pages?",
             "It divides the LRU list into 'young' (5/8) and 'old' (3/8) sublists; pages accessed during scans must remain active for `innodb_old_blocks_time` before entering the young list."),
            ("What is the difference between binlog_format = MIXED and ROW?",
             "MIXED uses statement-based logging by default, switching to row-based only when non-deterministic functions or triggers are invoked."),
            ("Why does multi-threaded replication (MTR) reduce replication lag on replicas?",
             "It allows the replica applier thread to apply non-conflicting transactions across different databases or transaction dependency sets in parallel."),
            ("What is the difference between semi-synchronous replication and asynchronous replication in MySQL?",
             "Async commits on primary without waiting; semi-sync waits for at least one replica to acknowledge receiving the binlog event into its relay log.")
        ],
        ("Configure a master-replica GTID topology and verify zero-loss failover under simulated primary crash.",
         "Trigger an InnoDB deadlock using two concurrent threads updating rows in inverted order and parse the deadlock graph.")
    ),
    (
        "Module_07_Oracle_Database_Architecture_SGA_PGA",
        "Oracle Database Architecture: SGA, PGA & Storage",
        [
            ("What is the difference between the System Global Area (SGA) and Program Global Area (PGA) in Oracle?",
             "SGA is shared memory accessible to all Oracle background and server processes; PGA is private non-shared memory allocated per server process for sorting and session state."),
            ("Explain the difference between a Hard Parse and a Soft Parse in Oracle's Library Cache.",
             "A hard parse completely compiles the SQL, analyzes syntax, and computes an execution plan; a soft parse reuses an already compiled plan from the Library Cache using identical SQL text/bind keys."),
            ("How does the Oracle Database Buffer Cache touch-count algorithm work?",
             "It tracks block access frequency using a counter; blocks with high touch counts (>2) are protected from eviction when new blocks are read into the buffer."),
            ("What does the Log Writer (LGWR) process do when a transaction executes COMMIT?",
             "LGWR synchronously writes the transaction's redo vectors from the Redo Log Buffer in SGA to the online redo log files on disk before acknowledging the commit."),
            ("What is the High-Water Mark (HWM) in an Oracle segment?",
             "The boundary up to which blocks have ever been formatted for data. Full table scans read all blocks up to the HWM regardless of whether rows were deleted."),
            ("How does Automatic Memory Management (AMM) differ from Automatic Shared Memory Management (ASMM)?",
             "ASMM tunes SGA pools dynamically (`SGA_TARGET`); AMM manages both SGA and PGA dynamically as a single shared pool (`MEMORY_TARGET`)."),
            ("What is a Tablespace Extent in Oracle storage hierarchy?",
             "A contiguous set of data blocks allocated within a datafile to form segments (tables, indexes)."),
            ("Why is CURSOR_SHARING = FORCE used as an interim performance fix?",
             "It automatically replaces literal values in SQL with system-generated bind variables, converting hard parses into soft parses."),
            ("What is the role of Database Writer (DBWR) processes in Oracle?",
             "DBWR asynchronously writes dirty blocks from the Database Buffer Cache to datafiles on disk during checkpoints or when free buffer space is low."),
            ("How do you calculate the Buffer Cache Hit Ratio from v$sysstat?",
             "Hit Ratio = 1 - (physical reads / (db block gets + consistent gets)).")
        ],
        ("Inspect Shared Pool execution plan reuse using v$sql and calculate soft parse efficiency across 1,000 queries.",
         "Demonstrate HWM impact by comparing full-table scan time on a 100,000-row table before and after DELETE vs TRUNCATE.")
    ),
    (
        "Module_08_Oracle_PLSQL_Packages_Triggers",
        "Oracle PL/SQL Packages, Triggers & Autonomous Transactions",
        [
            ("What is the purpose of PRAGMA AUTONOMOUS_TRANSACTION in PL/SQL?",
             "It executes an independent transaction within a procedure, committing or rolling back its work without affecting the main caller transaction."),
            ("Why does an ORA-04091 'mutating table' error occur, and how do Compound Triggers solve it?",
             "Row triggers cannot query the table being modified. A Compound Trigger provides 4 timing phases, allowing row-level data to be collected and aggregated in the statement phase."),
            ("How does FORALL bulk binding improve DML performance compared to standard FOR loops?",
             "It switches context between the PL/SQL runtime and the SQL execution engine once for the entire array batch rather than once per row."),
            ("What is the difference between a PL/SQL Package Specification and Package Body?",
             "The specification declares public constants, types, and procedure signatures; the body contains the private implementation details and logic."),
            ("What does BULK COLLECT INTO do in PL/SQL?",
             "It retrieves entire query result sets into in-memory collections (nested tables or varrays) in a single context switch."),
            ("How does %ROWTYPE differ from %TYPE in PL/SQL variable declaration?",
             "%TYPE anchors a variable to a single column's data type; %ROWTYPE anchors a record to the entire column structure of a table."),
            ("What is the difference between RAISE_APPLICATION_ERROR and standard RAISE in PL/SQL?",
             "RAISE_APPLICATION_ERROR allows assigning custom error numbers (-20000 to -20999) and human-readable messages returned to client applications."),
            ("What are the four timing points of a Compound DML Trigger?",
             "BEFORE STATEMENT, BEFORE EACH ROW, AFTER EACH ROW, and AFTER STATEMENT."),
            ("Can an autonomous transaction see uncommitted data from its parent transaction?",
             "No. An autonomous transaction is a completely separate session and cannot see the calling transaction's uncommitted writes."),
            ("What is the PL/SQL Result Cache?",
             "A memory structure that caches the return values of deterministic functions in the SGA, eliminating repeated function execution for identical arguments.")
        ],
        ("Build a high-performance bulk billing batch processor using FORALL and SAVE EXCEPTIONS.",
         "Implement an autonomous security auditor logging every transaction attempt regardless of parent transaction outcome.")
    ),
    (
        "Module_09_Oracle_RAC_DataGuard_GoldenGate",
        "Oracle RAC, Active Data Guard & Real-Time Replication",
        [
            ("What is Oracle RAC Cache Fusion?",
             "A technology that transfers data blocks directly between the SGA buffer caches of different cluster instances over high-speed private interconnect RAM, avoiding disk I/O."),
            ("What role does the Global Cache Service (GCS) play in an Oracle RAC cluster?",
             "GCS tracks block ownership, locks, and cache states across all cluster instances to guarantee cluster-wide cache coherency."),
            ("What is the difference between Oracle Active Data Guard and standard physical standby?",
             "Active Data Guard allows the physical standby database to remain open in Read-Only mode for reporting queries while continuously applying redo in real-time."),
            ("Explain the three Data Guard protection modes: Maximum Protection, Maximum Availability, and Maximum Performance.",
             "Max Protection: Zero data loss, synchronous redo commit on standby; primary halts if standby unreachable. Max Availability: Synchronous commit, downgrades to async if standby fails. Max Performance: Asynchronous redo shipping, zero primary impact."),
            ("What is a Fast Connection Failover (FCF) in Oracle RAC?",
             "A mechanism using Oracle Notification Service (ONS) to inform client connection pools immediately when a node crashes, rapidly redirecting sessions without TCP timeouts."),
            ("What is the difference between a Data Guard Switchover and Failover?",
             "Switchover is a planned, zero-data-loss role reversal between primary and standby; Failover is an emergency promotion of standby following unexpected primary catastrophe."),
            ("How does Oracle GoldenGate differ from Data Guard?",
             "Data Guard replicates physical block redo for an entire database; GoldenGate performs logical transactional replication across heterogeneous databases and tables."),
            ("What are RAC Voting Disks used for?",
             "They determine node membership and cluster quorum, evicting unresponsive nodes during split-brain network failures."),
            ("What is an Oracle RAC Service, and why should applications connect to Services rather than SID?",
             "A Service is a logical abstraction representing a workload; it allows load balancing and transparent failover across available cluster instances."),
            ("What metric indicates Cache Fusion interconnect saturation?",
             "`gc cr request` and `gc buffer busy acquire` wait events in AWR reports.")
        ],
        ("Simulate multi-node Cache Fusion block contention and measure cross-instance block transfers.",
         "Implement an automated standby lag monitor evaluating RPO compliance across Active Data Guard.")
    ),
    (
        "Module_10_MongoDB_Document_Modeling_BSON",
        "MongoDB Document Modeling & BSON Wire Protocol",
        [
            ("What is the 16MB document size limit in MongoDB, and what architectural pattern addresses it?",
             "MongoDB caps single BSON documents at 16MB. The Time-Series Bucket Pattern or 1:N referencing solves unbounded array growth."),
            ("Explain the structural components of a 12-byte BSON ObjectId.",
             "4 bytes unix epoch timestamp, 5 bytes random value unique to machine/process, and 3 bytes incrementing counter."),
            ("When should you Embed vs Reference related data in MongoDB?",
             "Embed for 1:1 or bounded 1:N relationships accessed together atomically; Reference for unbounded 1:N or M:N relationships updated independently."),
            ("What is a TTL (Time-To-Live) index in MongoDB?",
             "A single-field index on a date field that automatically deletes documents after a specified number of seconds via a background reaper thread."),
            ("How does schema validation work in MongoDB?",
             "Collections can enforce validation rules using JSON Schema (`$jsonSchema`) with strict or moderate enforcement levels."),
            ("What is the difference between $set, $inc, and $push update operators?",
             "`$set` updates/adds a field; `$inc` atomically increments a numeric field; `$push` appends an item to an array."),
            ("Why is an atomic findAndModify/findOneAndUpdate preferred over find-then-update?",
             "It eliminates race conditions by reading and updating the document in a single atomic database operation."),
            ("What does the stage 'COLLSCAN' indicate in MongoDB query explain output?",
             "A collection scan (every document read into RAM) indicating a missing or unused index."),
            ("How does BSON differ from standard JSON?",
             "BSON is a binary serialization format supporting rich data types (Date, ObjectId, BinData, Int64, Decimal128) and faster field traversal."),
            ("What is the Extended Reference pattern in document modeling?",
             "Embedding only the most frequently read fields of a referenced document (e.g. customer name) while keeping the full entity in a referenced collection.")
        ],
        ("Benchmark single-document read throughput for 1:50 embedded items vs 50 separate referenced queries.",
         "Create a strict JSON Schema validated collection rejecting invalid schema insertions.")
    ),
    (
        "Module_11_MongoDB_Aggregations_Replicas_Sharding",
        "MongoDB Aggregation Pipelines, Replication & Sharding",
        [
            ("What is the execution model of a MongoDB Aggregation Pipeline?",
             "A multi-stage streaming pipeline where documents pass sequentially through transformation operators ($match, $unwind, $group, $sort)."),
            ("How does the $lookup stage perform left outer joins between collections?",
             "It matches `localField` in the source collection to `foreignField` in the target collection, outputting matches as an embedded array."),
            ("What is the difference between a Targeted Query and a Scatter-Gather Query in a sharded cluster?",
             "Targeted queries include the Shard Key and route to exactly 1 shard; Scatter-Gather queries lack the shard key and broadcast to every shard in the cluster."),
            ("What does the $unwind stage do to an embedded array?",
             "It deconstructs an array field, outputting one document for every element in the array."),
            ("What is the role of the mongos query router in MongoDB sharding?",
             "It acts as a stateless gateway directing client queries to appropriate shards based on cluster metadata from config servers."),
            ("How does readPreference secondaryPreferred improve cluster throughput?",
             "It routes read-heavy analytical queries to secondary replicas, reserving the primary replica for transactional writes."),
            ("What is the 100MB RAM limit on aggregation pipeline stages, and how is it bypassed?",
             "Stages like $sort and $group cannot exceed 100MB RAM unless `{allowDiskUse: true}` is enabled to spill to temporary files."),
            ("What is a Change Stream in MongoDB?",
             "A real-time pub/sub API using the replica set oplog to notify applications of document inserts, updates, and deletes."),
            ("What is Hashed Sharding vs Range-Based Sharding?",
             "Hashed sharding hashes shard keys for uniform write distribution; Range sharding groups contiguous keys for efficient range queries."),
            ("What is the $facet stage in aggregation pipelines?",
             "It executes multiple aggregation pipelines simultaneously within a single stage on the same input document stream.")
        ],
        ("Build an aggregation pipeline computing customer lifetime value (LTV) across orders and payments.",
         "Simulate a consistent hash shard router evaluating key distribution balance across 5 virtual shards.")
    ),
    (
        "Module_12_Redis_Data_Structures_Persistence",
        "Redis Internals: Data Structures, RDB/AOF & Sliding Windows",
        [
            ("Why is Redis single-threaded, and how does it achieve >100,000 operations per second?",
             "It operates entirely in RAM and uses non-blocking I/O multiplexing (epoll/kqueue), eliminating thread context switches and lock contention."),
            ("What is the difference between Redis RDB snapshots and AOF (Append-Only File) persistence?",
             "RDB creates point-in-time binary disk snapshots; AOF logs every write command sequentially for near-zero RPO."),
            ("How does a Sliding-Window Rate Limiter work using Redis Sorted Sets?",
             "Keys are timestamps; `ZREMRANGEBYSCORE` removes timestamps older than window; `ZCARD` checks count; `ZADD` appends current timestamp."),
            ("What is the difference between volatile-lru and allkeys-lru eviction policies?",
             "volatile-lru evicts least recently used keys among those with an expire TTL; allkeys-lru evicts LRU keys across the entire database."),
            ("What is a Redis HyperLogLog, and what is its maximum memory footprint?",
             "A probabilistic cardinality estimation structure requiring at most 12KB RAM to count billions of unique elements with ~0.81% error rate."),
            ("How do Redis Hashes optimize memory for small objects?",
             "When small, Redis encodes hashes as compact ziplists/listpacks in contiguous RAM rather than full hash tables."),
            ("What does the BGREWRITEAOF command do?",
             "It builds a new minimal AOF file reflecting current memory state without redundant intermediate command history."),
            ("What is the Cache-Aside (Lazy Loading) pattern?",
             "Application checks Redis cache; on miss, reads primary database, populates Redis with a TTL, and returns data."),
            ("How does SET resource_name my_random_token NX EX 30 implement a safe distributed lock?",
             "NX guarantees key is set only if it does not exist; EX sets an automatic expiration TTL preventing deadlocks."),
            ("Why must distributed lock releases use a Lua script?",
             "To ensure atomicity: verify the caller's unique random token matches before deleting the key, preventing releasing another worker's lock.")
        ],
        ("Implement a production-ready sliding-window rate limiter handling 1,000 requests per minute.",
         "Build an atomic distributed lock in Python with automatic heartbeat extension.")
    ),
    (
        "Module_13_Redis_Sentinel_Clustering_Lua",
        "Redis High Availability: Sentinel, Clustering & Lua Scripting",
        [
            ("How does Redis Sentinel achieve automated master failover?",
             "Sentinels monitor master nodes via heartbeat pings; when a quorum agrees master is down (ODOWN), a sentinel is elected to promote a replica."),
            ("How many Hash Slots exist in a Redis Cluster, and how are keys mapped to them?",
             "16,384 hash slots. Keys are mapped using `CRC16(key) mod 16384`."),
            ("What is a Redis Hash Tag, and why is it essential for multi-key cluster operations?",
             "Wrapping part of a key in braces `{user:101}` forces Redis Cluster to hash only the braced substring, placing related keys in the same slot."),
            ("What happens when a client sends a query for a key to the wrong Redis Cluster node?",
             "The node responds with a `-MOVED <slot> <ip:port>` redirection error instructing the client where to route the request."),
            ("Why are Lua scripts atomic in Redis?",
             "Redis executes the entire Lua script without interleaving any other command in its single-threaded event loop."),
            ("What is the difference between MOVED and ASK redirection in Redis Cluster?",
             "MOVED indicates a slot migration is permanent; ASK indicates a slot is currently in the process of migrating to another node."),
            ("What does SCRIPT LOAD and EVALSHA do?",
             "SCRIPT LOAD pre-compiles a Lua script on the Redis server returning a SHA1 digest; EVALSHA executes it by digest, saving bandwidth."),
            ("How does min-replicas-to-write prevent split-brain data loss in Redis Sentinel?",
             "It halts writes on the master if fewer than the specified number of replicas acknowledge heartbeat within a maximum lag window."),
            ("Can Redis Cluster automatically rebalance hash slots when adding a new node?",
             "Yes, via `redis-cli --cluster reshard` which migrates slot allocations and keys online."),
            ("What is the maximum execution timeout for Lua scripts before Redis allows SCRIPT KILL?",
             "Configured by `lua-time-limit` (default 5,000 ms). After this, Redis accepts `SCRIPT KILL` (read-only) or `SHUTDOWN NOSAVE`.")
        ],
        ("Implement an atomic multi-resource reservation engine in Lua that validates inventory and deducts balances atomically.",
         "Build a Redis Sentinel failover client listener that reconnects transparently during master promotion.")
    ),
    (
        "Module_14_Apache_Cassandra_Masterless_Ring",
        "Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column",
        [
            ("Why is Apache Cassandra described as a masterless, shared-nothing architecture?",
             "Every node in the cluster plays an identical role; any node can coordinate any read or write request without a single point of failure."),
            ("Explain the formula for strong consistency in tunable quorum replication.",
             "$R + W > N$, where $R$ is Read Consistency, $W$ is Write Consistency, and $N$ is Replication Factor."),
            ("What is the difference between a Partition Key and a Clustering Key in CQL?",
             "Partition Key determines which physical node in the token ring stores the row; Clustering Key determines the on-disk sorting order within that partition."),
            ("How does Cassandra resolve write conflicts without locks?",
             "Last-Write-Wins (LWW) based on microsecond client-side timestamps."),
            ("What is a Tombstone in Cassandra storage, and why can excessive tombstones degrade performance?",
             "A deletion marker recorded in SSTables; reading across deleted rows requires scanning all tombstones until compaction purges them."),
            ("What is Read Repair in Apache Cassandra?",
             "When reading with QUORUM, the coordinator compares data hashes; if a replica is stale, it sends the newest data in the background to update it."),
            ("What is a Lightweight Transaction (LWT) in Cassandra?",
             "A linearizable compare-and-set operation (`IF NOT EXISTS` / `IF col = val`) powered by the Paxos consensus protocol."),
            ("How does consistent hashing distribute keys across the Cassandra token ring?",
             "The partition key is hashed to a 64-bit integer (Murmur3Partitioner) and placed on the first node whose assigned token range covers that value."),
            ("Why is SELECT * FROM table WHERE non_partition_key = 'val' prohibited without ALLOW FILTERING?",
             "It forces the cluster to execute a full table scan across all nodes in the cluster, destroying distributed scalability."),
            ("What role does the CommitLog play in Cassandra write durability?",
             "Writes are immediately appended to an on-disk sequential CommitLog before being stored in in-memory MemTables.")
        ],
        ("Design an IoT sensor telemetry schema partitioned by device and day bucket, ordered descending by timestamp.",
         "Simulate a network partition and verify tunable quorum consistency behavior.")
    ),
    (
        "Module_15_LSM_Trees_Compaction_DynamoDB",
        "LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design",
        [
            ("Why do LSM-Trees (Log-Structured Merge-Trees) provide higher write throughput than B+ Trees?",
             "LSM-Trees convert random writes into sequential writes by buffering in memory (MemTable) and writing sequential immutable SSTables to disk."),
            ("What is the role of a Bloom Filter in an SSTable read path?",
             "It probabilistically confirms if a key definitely does NOT exist in an SSTable, skipping expensive disk I/O."),
            ("Explain Leveled Compaction vs Size-Tiered Compaction in LSM storage.",
             "Size-Tiered merges SSTables of similar sizes into larger tables (optimal for writes); Leveled maintains non-overlapping key ranges per level (optimal for reads)."),
            ("How does Amazon DynamoDB Single-Table Design represent 1:N relationships?",
             "Using composite Partition Keys (PK) and Sort Keys (SK) to group related entities (e.g. Customer and Orders) in the same physical partition."),
            ("What is the difference between DynamoDB RCU and WCU billing units?",
             "1 WCU = 1 write up to 1KB/s; 1 RCU = 1 strongly consistent read (or 2 eventually consistent reads) up to 4KB/s."),
            ("What is a Global Secondary Index (GSI) in DynamoDB?",
             "An alternate index with a different PK and SK partitioned and replicated asynchronously across the cluster."),
            ("How do conditional writes prevent concurrent overwrite bugs in DynamoDB?",
             "Using `ConditionExpression = 'attribute_not_exists(PK)'` or checking version numbers before applying mutations."),
            ("What causes hot partition throttling in DynamoDB?",
             "Exceeding 1,000 WCU or 3,000 RCU on a single physical partition due to skewed access patterns."),
            ("What is Write Amplification in storage engines?",
             "The ratio of physical bytes written to storage media relative to logical bytes written by the user application."),
            ("Why are SSTables immutable once written to disk?",
             "Immutability eliminates locking and concurrency hazards during reads and makes background compaction trivial.")
        ],
        ("Implement an in-memory LSM storage engine with MemTable flushing and SSTable binary search.",
         "Design a DynamoDB single-table schema modeling an e-commerce order management system.")
    ),
    (
        "Module_16_Neo4j_Graph_Databases_Cypher",
        "Graph Databases: Neo4j & Declarative Cypher",
        [
            ("What is Index-Free Adjacency in graph databases?",
             "Each node maintains direct memory/disk pointers to its adjacent neighbor relationships, enabling $O(1)$ step traversals independent of total graph size."),
            ("How does Cypher's declarative pattern matching syntax model relationships?",
             "Using ASCII art syntax: `(start:Label)-[:REL_TYPE {prop: val}]->(end:Label)`."),
            ("Why are graph databases significantly faster than relational databases for deep multi-hop queries?",
             "Relational databases must compute expensive join tables on primary/foreign keys ($O(N \\log N)$), while graphs traverse pre-linked pointers ($O(K)$)."),
            ("What does the `shortestPath()` function in Cypher compute?",
             "It uses Breadth-First Search (BFS) to find the minimum-hop relationship path between two nodes."),
            ("How do you detect circular fraud rings in Cypher?",
             "Using variable-length cyclic paths: `MATCH (a:Account)-[:TRANSFERRED*3..6]->(a) RETURN a`."),
            ("What is the difference between Cypher PROFILE and EXPLAIN?",
             "EXPLAIN shows planner operator estimates without running; PROFILE executes the query and reports actual DB hits, rows, and memory."),
            ("What is a 'Supernode' in a property graph, and what operational challenge does it create?",
             "A node with millions of edges; traversing or locking it causes severe latency spikes and memory pressure."),
            ("What is the difference between node labels and relationship types?",
             "Labels group nodes into sets/classes (can have multiple per node); relationship types define the single specific semantic edge connecting two nodes."),
            ("How does PageRank centrality measure node importance in a graph?",
             "It iteratively calculates the probability that a random walk across edges will land on a specific node."),
            ("Can relationships in a property graph have properties?",
             "Yes. In property graphs, edges can store arbitrary key-value properties (e.g. `since`, `weight`, `distance`).")
        ],
        ("Write a Cypher query detecting circular financial laundering rings across bank accounts.",
         "Implement an in-memory graph engine computing BFS shortest paths across 10,000 vertices.")
    ),
    (
        "Module_17_Columnar_OLAP_DuckDB_ClickHouse",
        "Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics",
        [
            ("Why are columnar storage engines 10x-100x faster for analytical aggregations than row stores?",
             "Columnar stores read only the specific columns referenced in queries and use CPU SIMD vectorization to process thousands of values per instruction."),
            ("What is Vectorized Execution in DuckDB?",
             "Processing data in batches of columnar vectors (e.g. 2,048 values in CPU L1/L2 cache) rather than executing an iterator loop one tuple at a time."),
            ("How does the ClickHouse MergeTree storage engine organize data on disk?",
             "It sorts data by primary key, writes immutable sorted column parts, and merges them asynchronously in the background."),
            ("What is Parquet predicate pushdown and projection pushdown?",
             "Projection pushdown reads only requested columns; predicate pushdown uses row-group min/max statistics to skip entire chunks of data without decompression."),
            ("What causes 'Too Many Parts' error in ClickHouse?",
             "Inserting single rows or micro-batches faster than background compaction can merge them."),
            ("What compression algorithms are standard in columnar storage?",
             "Dictionary encoding, Bit-packing, Run-Length Encoding (RLE), Gorilla (floats), and ZSTD / Snappy."),
            ("How does DuckDB query local Parquet files without a dedicated database server?",
             "It embeds directly in the host process (like SQLite) with an in-process vectorized engine executing directly over Parquet byte streams."),
            ("What is a Min/Max Data Skipping index?",
             "Metadata storing minimum and maximum values per column chunk, allowing the query engine to bypass non-matching blocks immediately."),
            ("Why should ClickHouse primary keys NOT be globally unique UUIDs?",
             "ClickHouse primary keys determine physical on-disk sort order; sorting by random UUIDs destroys data locality and compression ratios."),
            ("What is the difference between an OLTP row store and an OLAP columnar store?",
             "OLTP writes and reads entire rows for single transactions; OLAP reads specific columns across millions of rows for analytical aggregates.")
        ],
        ("Benchmark an aggregation query on 5,000,000 rows across DuckDB (columnar) vs SQLite (row store).",
         "Create a ClickHouse MergeTree table with custom partition keys and demonstrate min/max data skipping.")
    ),
    (
        "Module_19_Search_Engines_Elasticsearch_Lucene",
        "Search Engines: Elasticsearch, Lucene & Inverted Indexes",
        [
            ("What is an Inverted Index in information retrieval?",
             "A mapping from unique terms (words) to postings lists containing document IDs and token positions where the terms occur."),
            ("Explain the components of Okapi BM25 ranking function.",
             "Term Frequency (TF) with saturation ($k_1$), Document Frequency (IDF), and Document Length normalization ($b$) relative to average document length."),
            ("What are the stages of an Elasticsearch Text Analyzer?",
             "Character Filters (strip HTML) $\\rightarrow$ Tokenizer (split into terms) $\\rightarrow$ Token Filters (lowercasing, stopwords, stemming)."),
            ("How does a compound Bool Query combine must, should, and filter clauses?",
             "`must`: must match, contributes to score; `should`: optional, boosts score; `filter`: must match, cached, does NOT contribute to score."),
            ("What is Fuzzy Search in Elasticsearch, and how does Levenshtein distance work?",
             "It matches terms within $N$ character edits (insertions, deletions, substitutions) using finite state transducers (FSTs)."),
            ("What is the difference between a `text` field and a `keyword` field in Elasticsearch?",
             "`text` is analyzed and tokenized for full-text search; `keyword` is stored exact and un-tokenized for exact matching, sorting, and aggregations."),
            ("What is the Two-Phase Query-Then-Fetch distributed search execution model?",
             "Phase 1: Coordinator queries all shards for matching document IDs and scores. Phase 2: Coordinator fetches full document sources only for top-K results."),
            ("What is Mapping Explosion, and how is it prevented?",
             "Too many distinct fields in an index exhausting cluster state memory; prevented by setting `\"dynamic\": \"strict\"`."),
            ("How do Term Bucket Aggregations compute top categories?",
             "By building doc-value hash tables counting occurrences of exact keyword values across matching documents."),
            ("Why should deep pagination avoid high `from` offsets in Elasticsearch?",
             "High offsets force all shards to score and return thousands of documents to the coordinator; use `search_after` instead.")
        ],
        ("Build an inverted index with TF-IDF / BM25 scoring in Python matching Lucene formula.",
         "Create an Elasticsearch index with custom stemmer and synonym filters and verify multi-field search.")
    ),
    (
        "Module_20_AI_Vector_Databases_pgvector_Qdrant",
        "AI Vector Databases: pgvector & Qdrant HNSW Similarity",
        [
            ("What is the difference between Cosine Distance, Euclidean ($L_2$) Distance, and Dot Product?",
             "Cosine measures angle regardless of magnitude; Euclidean measures geometric distance; Dot product combines angle and magnitude."),
            ("How does the Hierarchical Navigable Small World (HNSW) graph index work?",
             "It organizes vectors into multi-layer skip-list graphs; upper layers perform long-distance routing; bottom layers perform fine-grained local search."),
            ("What is Approximate Nearest Neighbor (ANN) search vs Flat (Exact) k-NN?",
             "Flat compares query against every vector ($O(N)$); ANN traverses graph or clusters in sub-linear time ($O(\\log N)$) with slight recall trade-off."),
            ("What does the `ef_search` parameter control in HNSW graph traversal?",
             "The size of the dynamic priority queue during search: higher `ef_search` yields higher accuracy (recall) at the cost of latency."),
            ("How does pgvector integrate vector similarity search into PostgreSQL?",
             "As a native C extension providing a `vector` type, operators (`<->` L2, `<=>` Cosine), and IVFFlat / HNSW index access methods."),
            ("What is the difference between Pre-Filtering and Post-Filtering in vector databases?",
             "Pre-filtering filters metadata before vector traversal; post-filtering searches vectors first and then discards non-matching metadata (risking returning fewer than K items)."),
            ("Why must vectors be unit-normalized when using Dot Product for cosine similarity?",
             "For unit vectors, the dot product is mathematically identical to cosine similarity: $\\vec{u} \\cdot \\vec{v} = \\cos(\\theta)$."),
            ("What is the IVFFlat index in vector databases?",
             "Inverted File Flat: vectors are clustered into Voronoi cells around centroids; queries search only the nearest centroids."),
            ("What is Recall@K in vector search benchmarking?",
             "The percentage of true nearest neighbors (from exact brute force) retrieved by an ANN algorithm in its top-K results."),
            ("How does Qdrant achieve sub-millisecond vector search with complex metadata filtering?",
             "It builds combined payload indices and integrates filter evaluation directly into the HNSW graph traversal loop.")
        ],
        ("Benchmark ANN Recall@10 of an HNSW index against exact brute-force search across 10,000 vectors.",
         "Build a hybrid search engine combining vector embeddings with dense scalar filters in Qdrant.")
    ),
    (
        "Module_21_Storage_Engine_Internals_BPlus_Trees",
        "Storage Engine Internals: Disk Pages & B+ Trees",
        [
            ("How does a Slotted-Page architecture organize variable-length records on a 4KB disk page?",
             "Slots grow forward from page header storing (offset, length) pointers; tuple data grows backward from the end of the page."),
            ("Why are B+ Trees preferred over B-Trees for relational database indexing?",
             "B+ Trees store data records exclusively in leaf nodes linked as a doubly-linked list, enabling high fan-out in internal nodes and fast sequential range scans."),
            ("What happens during a B+ Tree node split when maximum capacity is exceeded?",
             "The node divides in half; the median key is promoted to the parent node, creating a new level if root splits."),
            ("What is the fan-out of a B+ Tree node, and how does it determine tree height?",
             "Fan-out is the number of child pointers per node. A fan-out of 100 on a 3-level tree indexes $100^3 = 1,000,000$ pages."),
            ("How does Lock Crabbing (Coupling) enable safe concurrent B+ Tree traversal?",
             "A reader/writer acquires the child lock before releasing the parent lock, ensuring intermediate structural modifications do not corrupt traversal."),
            ("What is the role of the Buffer Pool Manager in a database storage engine?",
             "It maintains an in-memory frame table of disk pages, handling page fetches, pin/unpin reference counting, and dirty-page flushing."),
            ("What is a dirty page in database storage internals?",
             "A page modified in memory whose changes have not yet been flushed to the on-disk datafile."),
            ("Why do B+ Tree leaf nodes maintain sibling pointers?",
             "To execute range scans (`BETWEEN val1 AND val2`) sequentially across leaf pages without returning to the root."),
            ("How does page fragmentation occur, and how do storage engines defragment slotted pages?",
             "Deletions create dead gaps between records; defragmentation compacts active records to the end of the page and updates slot offsets."),
            ("What is the Write-Ahead Logging (WAL) invariant regarding dirty page flushing?",
             "A dirty page cannot be written to disk until the WAL log record describing the modification has been flushed to disk (`page_lsn <= flushed_lsn`).")
        ],
        ("Implement node splitting and root promotion in a disk-page-backed B+ Tree.",
         "Build a Slotted Page manager in Python that packs variable-length records and compacts dead space.")
    ),
    (
        "Module_22_Query_Optimization_CBO_Index_Tuning",
        "Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning",
        [
            ("What is the role of the Cost-Based Optimizer (CBO) in relational engines?",
             "It explores equivalent relational algebra query execution plans and estimates their execution cost (I/O + CPU) to pick the cheapest plan."),
            ("How does System R dynamic programming optimize multi-table join orderings?",
             "It builds optimal join plans bottom-up for sub-relations of size $k$, pruning sub-optimal permutations based on cost and interesting sort orders."),
            ("Explain the differences between Nested Loop Join, Hash Join, and Sort-Merge Join.",
             "Nested Loop: for each outer row, scans inner (fast with inner index); Hash Join: builds hash table on smaller relation, probes with larger; Sort-Merge: sorts both relations, merges linearly."),
            ("What are Column Histograms and Most Common Values (MCV) lists in database statistics?",
             "Statistical summaries in `pg_statistic` estimating value distribution and selectivity for WHERE clause predicates."),
            ("What is an 'Interesting Sort Order' in query planning?",
             "An ordering produced by an index or sort that satisfies subsequent `ORDER BY` or `GROUP BY` clauses, avoiding redundant sort operations."),
            ("Why does wrapping a column in a function (`WHERE UPPER(name) = 'ALICE'`) invalidate an index?",
             "The index stores raw values of `name`, not computed `UPPER(name)`; the planner must fall back to a full table scan."),
            ("What is a Sargable (Search-Argument-Able) query?",
             "A query predicate written such that the engine can utilize an index seek (e.g. `col >= val` instead of `col + 5 >= val`)."),
            ("How does Genetic Query Optimization (GEQO) prevent planning stalls on large queries?",
             "It uses randomized heuristic algorithms rather than exhaustive enumeration when join count exceeds threshold (typically 12 relations)."),
            ("What is Selectivity in query cost estimation?",
             "The estimated fraction of total rows that satisfy a predicate (between 0.0 and 1.0)."),
            ("What does the `random_page_cost` parameter in PostgreSQL represent?",
             "The estimated cost to access a non-sequential disk page relative to `seq_page_cost` (tuned lower for SSDs, e.g. 1.1).")
        ],
        ("Implement dynamic programming join enumeration for a 4-table join and calculate lowest cost plan.",
         "Create extended statistics on correlated columns and verify query plan correction in PostgreSQL.")
    ),
    (
        "Module_23_Transactions_Isolation_Consensus_Raft",
        "Transactions, Isolation Levels & Distributed Consensus (Raft)",
        [
            ("Define the three ANSI SQL read phenomena: Dirty Read, Non-Repeatable Read, and Phantom Read.",
             "Dirty Read: reading uncommitted changes; Non-Repeatable Read: re-reading a row returns modified values; Phantom Read: re-executing range query returns newly inserted rows."),
            ("What is the difference between Two-Phase Locking (2PL) and Strict 2PL (S2PL)?",
             "2PL releases locks during shrinking phase before commit; Strict 2PL holds all exclusive locks until transaction COMMIT or ABORT, preventing cascading rollbacks."),
            ("Explain the two phases of the Two-Phase Commit (2PC) protocol.",
             "Phase 1 (Prepare): Coordinator asks participants if they can commit; participants vote YES and write to WAL. Phase 2 (Commit): If all voted YES, coordinator issues COMMIT; otherwise ABORT."),
            ("Why is 2PC considered a blocking protocol?",
             "If the coordinator crashes after participants enter the PREPARED state, participants must hold locks indefinitely until coordinator recovers."),
            ("How does the Raft consensus algorithm handle Leader Election?",
             "Followers transition to Candidate upon election timer timeout, increment term, vote for self, and request votes; majority votes ($N/2 + 1$) wins election."),
            ("What is a Split-Brain in distributed systems, and how does quorum prevent it?",
             "Two nodes simultaneously believing they are leader; quorum ($N/2 + 1$) guarantees no two disjoint subsets can both achieve majority."),
            ("What is Snapshot Isolation (SI), and what anomaly can occur under it that is prevented by Serializable?",
             "Transactions read from a consistent snapshot taken at start; Write Skew anomaly can occur (prevented only by Serializable)."),
            ("What is Serializable Snapshot Isolation (SSI) in PostgreSQL?",
             "An optimistic implementation of serializable isolation that tracks read-write conflicts (SIREAD locks) and aborts transactions exhibiting dangerous dependency cycles."),
            ("What does the Raft Log Matching Property guarantee?",
             "If two logs contain an entry with the same index and term, they are identical up to that index."),
            ("What is the difference between safety and liveness in distributed consensus?",
             "Safety: nothing bad happens (never two leaders, no split-brain); Liveness: something good eventually happens (cluster makes progress).")
        ],
        ("Build a 3-node Raft consensus cluster in Python implementing leader election and heartbeat replication.",
         "Demonstrate Write Skew under Snapshot Isolation and resolve it using SELECT FOR UPDATE.")
    ),
    (
        "Module_24_Production_DBRE_Backups_Migrations_HA",
        "Production DBRE: Backups, Migrations, Monitoring & Runbooks",
        [
            ("What is the difference between RPO (Recovery Point Objective) and RTO (Recovery Time Objective)?",
             "RPO: maximum acceptable data loss measured in time; RTO: maximum acceptable downtime until service restoration."),
            ("Explain Point-In-Time Recovery (PITR) in relational databases.",
             "Restoring a base physical backup and replaying continuous Write-Ahead Logs (WAL/binlog) up to an exact specific microsecond timestamp."),
            ("What is the Expand/Contract (Parallel Run) pattern in database migrations?",
             "Expand: add new column/table while maintaining old; Contract: migrate application traffic to new structure, then drop old structure online."),
            ("Why should zero-downtime migrations set strict statement_timeout and lock_timeout?",
             "To abort immediately if an exclusive lock cannot be acquired within milliseconds, preventing blocking application traffic queues."),
            ("What is the difference between a Physical Backup (pg_basebackup) and a Logical Backup (pg_dump)?",
             "Physical copies raw page files on disk (fast restore, exact binary); Logical exports SQL DDL/DML statements (portable, slower)."),
            ("What is STONITH ('Shoot The Other Node In The Head') in high availability fencing?",
             "A fencing mechanism that forcefully powers off or isolates a failed primary node to guarantee it cannot write during failover."),
            ("What are the key RED metrics to monitor on database clusters?",
             "Rate (queries/sec), Errors (failed connections/deadlocks), and Duration (p95/p99 query latency)."),
            ("How does connection pool sizing impact database CPU cache efficiency?",
             "Oversized pools cause CPU context switching thrashing; optimal pool size is roughly $(2 \\times \\text{cores}) + \\text{effective spindles}$."),
            ("What is a Split-Brain scenario during failover, and what prevents it?",
             "Both primary and promoted replica accept writes simultaneously; prevented by automated fencing and odd-numbered quorum witnesses."),
            ("Why should disaster recovery runbooks be tested with automated game days?",
             "Untested backups and failovers frequently fail in real emergencies due to configuration drift, permission errors, or capacity shortages.")
        ],
        ("Implement an automated zero-downtime column rename migration runner using views and triggers.",
         "Build a health monitoring daemon that detects replica lag and exports Prometheus metrics.")
    ),
    (
        "Module_25_Final_Capstone_Polyglot_Enterprise",
        "Enterprise Polyglot Persistence Platform Capstone",
        [
            ("What is the Transactional Outbox Pattern, and what distributed data problem does it solve?",
             "It atomically writes application state and event intentions to the same relational database in one ACID transaction, solving dual-write inconsistency."),
            ("How does Change Data Capture (CDC) differ from application-level event publishing?",
             "CDC reads committed mutations directly from the database transaction log (WAL/binlog), guaranteeing zero event loss even if the app crashes."),
            ("In an enterprise polyglot architecture, what are the distinct roles of PostgreSQL, Redis, Elasticsearch, and ClickHouse?",
             "PostgreSQL: transactional source of truth; Redis: low-latency caching & leaderboards; Elasticsearch: full-text keyword search; ClickHouse: high-throughput columnar analytics."),
            ("What is a Distributed Saga, and how does it handle cross-database transaction failures?",
             "A sequence of local transactions across services; if a step fails, the saga orchestrator executes compensating transactions to undo previous steps."),
            ("How does the Cache-Aside pattern prevent stale reads when an update occurs?",
             "Updates write to the database and invalidate (delete) the cached key; subsequent reads experience a cache miss and fetch fresh data."),
            ("What is the Thundering Herd (Cache Stampede) problem, and how is it mitigated?",
             "Thousands of concurrent clients querying the database on hot key expiration; mitigated with distributed mutex locks or probabilistic early expiration."),
            ("Why should downstream search engines and caches be treated as derived read models?",
             "Because they can always be rebuilt from scratch by replaying the transactional source of truth event log."),
            ("What is Eventual Consistency, and how does an application handle read lag in polyglot stores?",
             "Downstream systems become consistent after a short propagation delay; applications use read-after-write routing to primary for immediate feedback."),
            ("How does an outbox event relay ensure at-least-once delivery?",
             "By recording published status only after receiving acknowledgment from the downstream message broker/store."),
            ("What is Idempotency, and why must event consumers enforce it?",
             "The property where processing an event multiple times produces the same outcome as processing it once, protecting against duplicate message deliveries.")
        ],
        ("Build an end-to-end polyglot transaction processor coordinating PostgreSQL outbox events to Redis and DuckDB.",
         "Implement an idempotent event consumer that deduplicates incoming CDC events using transaction IDs.")
    ),
]

for folder, title, questions, (c1, c2) in QUIZ_DATA:
    target_path = root / folder / "SELF_ASSESSMENT_AND_CHALLENGES.md"
    content = f'''# {folder.replace("_", " ")}: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **{title}** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

'''
    for idx, (q, _) in enumerate(questions, 1):
        content += f"{idx}. **{q.split('?')[0]}?** {q}\n"

    content += '''
---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

'''
    for idx, (q, ans) in enumerate(questions, 1):
        content += f"#### Answer {idx}:\n{ans}\n\n"

    content += f'''</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
{c1}

### 🚀 Challenge 2: Architect Stretch Problem
{c2}

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.
'''
    target_path.write_text(content, encoding="utf-8")

print(f"Generated {len(QUIZ_DATA)} SELF_ASSESSMENT_AND_CHALLENGES.md files successfully.")
