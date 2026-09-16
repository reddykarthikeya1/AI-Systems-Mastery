from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

TROUBLESHOOTING_DATA = [
    (
        "Module_02_Modern_SQL_Mastery_Advanced_Queries",
        "Modern SQL Mastery & Advanced Queries",
        [
            ("The NULL Hazard in NOT IN Subqueries",
             "Query with WHERE id NOT IN (SELECT foreign_id FROM ...) returns 0 rows unexpectedly.",
             "In SQL three-valued logic, if the subquery returns even a single row with NULL, `val NOT IN (NULL, 1, 2)` evaluates to UNKNOWN for all rows, which WHERE discards.",
             "Always use `WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...)` or filter out nulls with `WHERE foreign_id IS NOT NULL`."),
            ("Window Function Frame Default Trap (RANGE vs ROWS)",
             "Running sum produces identical duplicate values for rows with the same timestamp or amount.",
             "The SQL standard default frame specification for `ORDER BY` is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which aggregates over peers with identical order values simultaneously.",
             "Explicitly define `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` when you want strict row-by-row running accumulators."),
            ("Cartesian Product in Multi-Join Aggregations",
             "SUM(order_items.amount) returns wildly inflated numbers (e.g. 5x-10x actual values).",
             "Joining a parent table with two independent 1:N child tables simultaneously creates an $N \times M$ Cartesian explosion of duplicate rows.",
             "Aggregate each child table in an independent CTE or subquery before joining to the parent entity.")
        ]
    ),
    (
        "Module_03_Embedded_Databases_SQLite_WAL",
        "Embedded Databases: SQLite & WAL Architecture",
        [
            ("sqlite3.OperationalError: database is locked",
             "Concurrent threads or processes crash with 'database is locked' during write operations.",
             "SQLite allows multiple concurrent readers in WAL mode, but only ONE writer at any instant. If a writer attempts to acquire the exclusive write lock while another transaction holds it and busy_timeout is 0, it fails immediately.",
             "Configure `PRAGMA busy_timeout = 5000;` (wait up to 5 seconds for lock release) and ensure transactions are kept short."),
            ("Runaway -wal File Growth",
             "The database WAL file (`app.db-wal`) grows to tens of gigabytes without shrinking.",
             "A long-running active reader transaction is holding open an old read transaction snapshot, preventing the WAL checkpoint from advancing past that frame.",
             "Terminate idle in-transaction connections and configure automatic periodic checkpointing using `PRAGMA wal_autocheckpoint = 1000;` or invoke `PRAGMA wal_checkpoint(TRUNCATE);` during maintenance windows."),
            ("Silent Corruption via PRAGMA synchronous = OFF",
             "System crashes result in database corruption with `SQLITE_CORRUPT` upon reboot.",
             "With `synchronous = OFF`, SQLite hands data to the OS cache without calling `fsync()`. A sudden power outage results in torn pages or missing header updates on disk.",
             "In production WAL mode, always use `PRAGMA synchronous = NORMAL;`. It provides full ACID durability with minimal performance penalty.")
        ]
    ),
    (
        "Module_04_PostgreSQL_Core_Advanced_Types",
        "PostgreSQL Core Architecture & Advanced Types",
        [
            ("psycopg2.OperationalError: FATAL: remaining connection slots are reserved for non-replication superuser connections",
             "Application starts throwing connection refused errors during traffic spikes.",
             "Direct client connections have exceeded PostgreSQL's `max_connections` setting. Each PostgreSQL backend process consumes ~10MB RAM, causing memory exhaustion.",
             "Deploy PgBouncer or use an in-application connection pool (`ThreadedConnectionPool`) with pool size set to `(core_count * 2) + effective_spindle_count`."),
            ("GIN Index Not Used for JSONB Queries",
             "Query on a JSONB column performs a sequential scan despite a GIN index existing on the column.",
             "The query uses the `->` or `->>` operators instead of JSONB containment operators (`@>`, `?`, `?|`), or the GIN index was created with `jsonb_ops` instead of `jsonb_path_ops`.",
             "Rewrite queries to use containment (`data @> '{\"status\": \"active\"}'`) or create expression indexes on specific extracted fields: `CREATE INDEX idx_status ON tbl ((data->>'status'));`."),
            ("Integer Overflow on Serial Primary Keys",
             "Inserts fail with `ERROR: integer out of range` on high-volume tables.",
             "Standard `SERIAL` uses 32-bit signed integers (maximum 2,147,483,647 rows). When sequence wraps around, all subsequent inserts fail.",
             "Always declare modern tables with `BIGINT GENERATED ALWAYS AS IDENTITY` which supports up to $9 \times 10^{18}$ rows.")
        ]
    ),
    (
        "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN",
        "PostgreSQL MVCC, Vacuuming & Execution Plans",
        [
            ("Table Bloat & Autovacuum Starvation",
             "Table size swells from 500MB to 50GB even though row count remains constant.",
             "High frequency UPDATE/DELETE operations generate dead tuples that cannot be vacuumed because a long-running transaction holds an old transaction snapshot (visible in `pg_stat_activity`).",
             "Kill stale idle-in-transaction sessions using `pg_terminate_backend()`, configure aggressive autovacuum scale factors (`autovacuum_vacuum_scale_factor = 0.05`), and run `VACUUM FULL` or `pg_repack` to reclaim space."),
            ("Misleading EXPLAIN Cost Estimates Due to Stale Statistics",
             "Query planner chooses slow Sequential Scan over an Index Scan, causing 100x latency degradation.",
             "The query planner relies on `pg_statistic` histograms. If massive bulk inserts/deletes occur without triggering ANALYZE, row count estimates are off by orders of magnitude.",
             "Run `ANALYZE table_name;` manually after bulk data loading, or lower `autovacuum_analyze_scale_factor = 0.02`."),
            ("Deadlock on Concurrent Index Creation",
             "Executing `CREATE INDEX` hangs indefinitely and blocks all read/write traffic across the entire table.",
             "`CREATE INDEX` acquires an `ACCESS EXCLUSIVE` lock, preventing all reads and writes until index build completes.",
             "Always use `CREATE INDEX CONCURRENTLY`, which acquires only a weak `SHARE UPDATE EXCLUSIVE` lock allowing concurrent DML to continue.")
        ]
    ),
    (
        "Module_06_MySQL_MariaDB_InnoDB_Replication",
        "MySQL & InnoDB Architecture, Buffer Pool & Replication",
        [
            ("MySQL Error 1213: Deadlock found when trying to get lock; try restarting transaction",
             "High-concurrency e-commerce checkout transactions fail with deadlock errors.",
             "Two concurrent transactions updated multiple rows in reverse order (Transaction A locked Row 1 then tried to lock Row 2; Transaction B locked Row 2 then tried to lock Row 1).",
             "Enforce strict deterministic ordering in application code (e.g. `ORDER BY id ASC` before locking rows) and implement automated transaction retries with exponential backoff."),
            ("Replication Lag & Stale Secondary Reads",
             "Users create a record on the web app, refresh the page, and the record disappears.",
             "The write went to the Primary, but the subsequent read was routed to a Read Replica that is lagging by several seconds due to single-threaded replica SQL applier bottlenecks.",
             "Enable multi-threaded replication (`replica_parallel_workers = 8`) and use read-after-write routing (route reads to Primary for 2 seconds immediately following a user write)."),
            ("InnoDB Buffer Pool Eviction Thrashing",
             "Disk I/O spikes to 100% and query latency degrades from 2ms to 200ms.",
             "A full-table reporting scan swept through the buffer pool, evicting frequently accessed OLTP pages from the LRU cache.",
             "Tune `innodb_old_blocks_time = 1000` (requires pages to stay accessed for 1 second before promotion to the young sublist) preventing single-scan pollution.")
        ]
    ),
    (
        "Module_07_Oracle_Database_Architecture_SGA_PGA",
        "Oracle Database Architecture: SGA, PGA & Storage",
        [
            ("ORA-04031: unable to allocate bytes of shared memory",
             "Queries fail with ORA-04031 during peak hours.",
             "Shared Pool fragmentation caused by thousands of literal SQL statements without bind variables (`SELECT * FROM t WHERE id = 12345` instead of `:id`), exhausting chunk allocations.",
             "Convert application SQL to use bind variables, configure `CURSOR_SHARING = FORCE` as an interim mitigation, and increase Shared Pool sizing."),
            ("Low Buffer Cache Hit Ratio & Free Buffer Waits",
             "Sessions hang waiting on `db file sequential read` and `free buffer waits`.",
             "Database Buffer Cache is undersized relative to active working set, forcing LGWR and DBWR into synchronous checkpoint stalls.",
             "Inspect `v$db_cache_advice` to determine optimal cache sizing, and tune DBWR writer processes (`DB_WRITER_PROCESSES`)."),
            ("High-Water Mark (HWM) Sequential Scan Slowdown",
             "A table with only 10 rows takes 15 seconds to execute `SELECT * FROM t;`.",
             "The table previously contained 100 million rows which were deleted with `DELETE` instead of `TRUNCATE`. The HWM remains at the 100M mark, forcing full table scans to read millions of empty blocks.",
             "Reclaim space and reset HWM using `ALTER TABLE t MOVE;` followed by index rebuilds, or use `TRUNCATE TABLE` when purging data.")
        ]
    ),
    (
        "Module_08_Oracle_PLSQL_Packages_Triggers",
        "Oracle PL/SQL Packages, Triggers & Autonomous Transactions",
        [
            ("ORA-04091: table is mutating, trigger/function may not see it",
             "A row-level trigger fails when attempting to query or aggregate the table being updated.",
             "A row-level trigger cannot query the table it is currently modifying because the table is in a transient, inconsistent state.",
             "Refactor into a **Compound DML Trigger** using the `BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, and `AFTER STATEMENT` lifecycle to collect rows into an in-memory collection and aggregate in the statement phase."),
            ("ORA-06502: PL/SQL: numeric or value error",
             "Stored procedure crashes with buffer overflow during string operations.",
             "A VARCHAR2 variable in PL/SQL was declared without sufficient byte/character length (or byte vs char semantics under UTF-8).",
             "Declare string variables using explicit character semantics: `v_name VARCHAR2(100 CHAR);` or anchor to table column definitions: `v_name customers.name%TYPE;`."),
            ("Autonomous Transaction Deadlock",
             "Procedure using PRAGMA AUTONOMOUS_TRANSACTION hangs permanently.",
             "The parent transaction updated a row and held an exclusive row lock; the autonomous transaction then attempted to update the exact same row.",
             "Never update rows in an autonomous transaction that are locked by the calling parent transaction. Autonomous transactions must operate strictly on independent tables (e.g. audit logs).")
        ]
    ),
    (
        "Module_09_Oracle_RAC_DataGuard_GoldenGate",
        "Oracle RAC, Active Data Guard & Real-Time Replication",
        [
            ("RAC Interconnect Congestion & gc buffer busy acquire",
             "Query latency spikes across all RAC cluster nodes with high `gc cr request` waits.",
             "Cache Fusion pinging: multiple nodes are concurrently writing to the same data blocks, causing the Global Cache Service (GCS) to constantly transfer dirty blocks back and forth over the private interconnect.",
             "Partition workload at the application tier using Oracle Services so specific business domains execute on dedicated instances, avoiding cross-instance block contention."),
            ("Data Guard Transport Lag & Standby Desynchronization",
             "Active Data Guard standby lags behind primary by hours, risking data loss (RPO breach).",
             "Network throughput between primary and standby data centers is saturated or redo transport service is misconfigured.",
             "Tune `redo_transport_user`, configure multiple archiver processes (`LOG_ARCHIVE_MAX_PROCESSES`), and set protection mode to `MAXIMUM AVAILABILITY` with synchronous standby redo logs (SRLs)."),
            ("Split-Brain Scenario During RAC Node Eviction",
             "A node is evicted from the RAC cluster, but continues attempting to write to shared storage.",
             "Network heartbeat was lost over interconnect, but storage fencing (STONITH / CSS voting disks) failed to isolate the node.",
             "Ensure dedicated, redundant physical network switches for RAC private interconnects and verify voting disk quorum configurations.")
        ]
    ),
    (
        "Module_10_MongoDB_Document_Modeling_BSON",
        "MongoDB Document Modeling & BSON Wire Protocol",
        [
            ("Unbounded Array Growth (16MB Document Limit Exceeded)",
             "Inserts crash with `BSONObjectTooLarge: Document size is larger than maximum 16777216`.",
             "An array of orders, comments, or sensor readings was embedded directly inside a parent document without capping, eventually breaching MongoDB's 16MB document size limit.",
             "Refactor to the **Time-Series Bucket Pattern** (e.g., store 500 readings per document bucket) or switch to 1:N referencing with a foreign key in the child documents."),
            ("Accidental Full Collection Scan (COLLSCAN)",
             "CPU usage spikes to 100% on MongoDB servers as traffic grows.",
             "Queries are missing index support or use unindexed sorting fields, forcing MongoDB to load millions of documents into RAM.",
             "Run `explain('executionStats')` on slow queries to verify stage transition from `COLLSCAN` to `IXSCAN` or `FETCH` with `totalDocsExamined` matching `nReturned`."),
            ("Schema Validation Silent Insert Rejections",
             "Application writes fail with `WriteError: Document failed validation`.",
             "A collection with strict `$jsonSchema` validation was updated with mismatched data types (e.g., string instead of int for an age field).",
             "Inspect collection validation rules with `db.getCollectionInfos({name: 'coll'})` and adjust validation action to `warn` in staging before enforcing `strict`.")
        ]
    ),
    (
        "Module_11_MongoDB_Aggregations_Replicas_Sharding",
        "MongoDB Aggregation Pipelines, Replication & Sharding",
        [
            ("Aggregation Pipeline 100MB Memory Limit Exceeded",
             "Complex `$sort` or `$group` aggregation crashes with `Exceeded memory limit for $sort (104857600 bytes)`.",
             "In-memory aggregation stages exceed the 100MB RAM safety cap when sorting large datasets without an index.",
             "Place `$match` and `$limit` as early in the pipeline as possible to minimize working set size, build an index matching the sort key, or enable `{allowDiskUse: true}`."),
            ("Scatter-Gather Sharding Degradation",
             "Queries take seconds to execute across a 10-shard cluster even for single-item lookups.",
             "The query filter does not include the cluster's **Shard Key**, forcing the `mongos` router to broadcast the query to every single shard in the cluster (scatter-gather).",
             "Ensure every targeted operational query includes the shard key (e.g. `tenant_id` or `customer_id`) so mongos routes directly to a single shard."),
            ("Replication Read Concern 'local' Stale Reads",
             "Reading from secondary replicas returns outdated data that does not reflect recent writes.",
             "Default read preference `secondaryPreferred` combined with `readConcern: local` reads uncommitted or lagging oplog frames.",
             "Use `readConcern: majority` and `writeConcern: majority` for strong read-after-write consistency guarantees.")
        ]
    ),
    (
        "Module_12_Redis_Data_Structures_Persistence",
        "Redis Internals: Data Structures, RDB/AOF & Sliding Windows",
        [
            ("OOM Command Not Allowed (MaxMemory Reached)",
             "Redis commands start failing with `OOM command not allowed when used memory > 'maxmemory'`.",
             "Redis memory reached `maxmemory` threshold and the eviction policy was set to `noeviction`.",
             "Configure an appropriate eviction policy such as `volatile-lru` or `allkeys-lru`, ensure all transient keys have explicit TTLs, and monitor memory fragmentation ratio with `INFO memory`."),
            ("RDB Fork Hang & System Memory Exhaustion",
             "Redis latency spikes by hundreds of milliseconds every 15 minutes during background snapshots.",
             "`BGSAVE` calls `fork()`, which duplicates page tables. If the Linux kernel has `vm.overcommit_memory = 0`, the fork fails or triggers massive copy-on-write page swapping.",
             "Set `sysctl vm.overcommit_memory = 1` in `/etc/sysctl.conf` and disable transparent huge pages (`transparent_hugepage = never`)."),
            ("Hot Key CPU Core Saturation",
             "Single Redis CPU core is pinned at 100% while all other cores are idle.",
             "A single hot key (e.g., a massive celebrity follower set or global counter) receives 100,000 requests/sec, bottlenecking the single-threaded Redis event loop.",
             "Implement local in-memory caching (e.g., Python `cachetools`) with 1-second TTL, or shard the hot key across multiple keys (`counter:1`, `counter:2`, etc.).")
        ]
    ),
    (
        "Module_13_Redis_Sentinel_Clustering_Lua",
        "Redis High Availability: Sentinel, Clustering & Lua Scripting",
        [
            ("Lua Script Timeout & Busy Engine Errors",
             "Redis becomes completely unresponsive, throwing `BUSY Redis is busy running a script`.",
             "A custom Lua script contains an infinite loop, expensive table iteration, or slow operations that block the single-threaded Redis event loop.",
             "Keep Lua scripts strictly $O(1)$ or small $O(K)$, use `SCRIPT KILL` for read-only runaway scripts, or `SHUTDOWN NOSAVE` if mutations occurred."),
            ("Redis Cluster CROSSSLOT Keys in Request Don't Hash to the Same Slot",
             "Multi-key operations (MGET, MSET, transactions) fail with `CROSSSLOT Keys in request don't hash to the same slot`.",
             "In Redis Cluster, multi-key operations are only permitted if all keys hash to the exact same hash slot (0-16383).",
             "Use Redis **Hash Tags**: enclose the common partition identifier in curly braces, e.g. `{user:101}:profile` and `{user:101}:orders`."),
            ("Sentinel Split-Brain During Network Partition",
             "Old master continues accepting writes while Sentinel promotes a new master, causing silent data loss upon partition healing.",
             "Network partition separated old master from Sentinel quorum, but clients continued writing to the old master.",
             "Configure `min-replicas-to-write 1` and `min-replicas-max-lag 10` on the master to halt writes if at least one replica is not acknowledging replication.")
        ]
    ),
    (
        "Module_14_Apache_Cassandra_Masterless_Ring",
        "Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column",
        [
            ("Tombstone Overload & Scanned Over 100,000 Tombstones Error",
             "Range queries fail with `ReadFailure: Scanned over 100000 tombstones in table; query aborted`.",
             "Frequent DELETE operations or expiring TTL data create tombstones. When querying, Cassandra scans through all tombstones to find alive rows, degrading memory and CPU.",
             "Avoid using Cassandra as a message queue; optimize partition key filtering to prevent broad range scans; lower `gc_grace_seconds` on dedicated write-heavy keyspaces and tune compaction."),
            ("Hot Partition Due to Low-Cardinality Partition Key",
             "One Cassandra node runs at 95% disk and CPU while other 9 nodes in the cluster sit idle at 5%.",
             "A partition key with low cardinality (e.g. `status` or `country`) caused millions of rows to route to a single token range on a single physical node.",
             "Create a composite partition key combining the category with a time bucket or salt: `PRIMARY KEY ((category, date_bucket), item_id)`."),
            ("WriteTimeoutException with ConsistencyLevel.ALL",
             "Writes fail whenever a single node undergoes maintenance or restarts.",
             "Using `ConsistencyLevel.ALL` requires acknowledgments from every single replica in the replication factor, completely sacrificing High Availability.",
             "Use `ConsistencyLevel.QUORUM` or `LOCAL_QUORUM` to satisfy strict consistency ($R + W > N$) while tolerating node failures.")
        ]
    ),
    (
        "Module_15_LSM_Trees_Compaction_DynamoDB",
        "LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design",
        [
            ("DynamoDB ProvisionedThroughputExceededException (Hot Key Throttle)",
             "API requests fail with 400 ProvisionedThroughputExceededException during flash sales.",
             "Thousands of concurrent writes targeted the exact same partition key (e.g. `PRODUCT#WIDGET`), exceeding the 1,000 WCU / 3,000 RCU per-partition limit.",
             "Implement **Write Sharding** (suffix partition key with random salt `PRODUCT#WIDGET#1` to `PRODUCT#WIDGET#10`) or use DynamoDB Accelerator (DAX) for read caching."),
            ("Write Amplification in Leveled LSM Compaction",
             "Disk I/O latency spikes dramatically on SSDs running heavy write workloads.",
             "As SSTables advance through levels (L0 to L6), compaction repeatedly reads and rewrites data blocks multiple times (write amplification often exceeding 10x-30x).",
             "Tune compaction strategy: switch from Leveled Compaction to Size-Tiered Compaction Strategy (STCS) or Time-Window Compaction Strategy (TWCS) for append-only workloads."),
            ("Silent False Positive Saturation in Bloom Filters",
             "Read operations slow down because every read hits disk SSTables despite Bloom filters being present.",
             "The Bloom filter was initialized with an expected capacity of 10,000 items, but 1,000,000 items were inserted, driving the false-positive rate towards 100%.",
             "Always size Bloom filter bit arrays dynamically based on expected element counts: $m = -\\frac{n \\ln p}{(\\ln 2)^2}$.")
        ]
    ),
    (
        "Module_16_Neo4j_Graph_Databases_Cypher",
        "Graph Databases: Neo4j & Declarative Cypher",
        [
            ("Cypher Cartesian Product & Memory Exhaustion",
             "A MATCH query with multiple unconnected patterns causes OutOfMemoryError and crashes the Neo4j instance.",
             "Writing `MATCH (a:Person), (b:Company)` without an explicit relationship pattern causes Neo4j to evaluate all possible pairs ($N \\times M$ Cartesian product).",
             "Ensure patterns are connected, or use `WITH a MATCH (b) WHERE ...` to sequence intermediate bindings and use `LIMIT`."),
            ("Supernode Graph Traversal Stalls",
             "Traversing relationships from a popular entity (e.g. an account with 5,000,000 followers) takes 30 seconds.",
             "A 'supernode' has millions of relationship pointers. Traversing incoming/outgoing relationships requires scanning all pointers in RAM.",
             "Use direction-specific and typed relationship traversals (`-[:DIRECTED_EDGE]->`), or create intermediate relationship category nodes to shard the fan-out."),
            ("Missing Schema Index Causing Node Scan in Cypher",
             "Cypher execution plan shows `NodeByLabelScan` examining 5,000,000 nodes instead of `NodeIndexSeek`.",
             "No index or unique constraint exists on the lookup property.",
             "Create an index: `CREATE INDEX FOR (p:Person) ON (p.ssn);` and profile queries using `PROFILE MATCH ...`.")
        ]
    ),
    (
        "Module_17_Columnar_OLAP_DuckDB_ClickHouse",
        "Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics",
        [
            ("Too Many Parts Exception in ClickHouse MergeTree",
             "ClickHouse throws `DB::Exception: Too many parts in table. Merges are processing significantly slower than inserts`.",
             "Application executed thousands of small single-row inserts per second instead of batching.",
             "Always batch writes in ClickHouse (insert batches of 10,000 to 100,000 rows at a time) or insert into a `Buffer` engine table."),
            ("DuckDB Out-of-Memory on Enormous Parquet Joins",
             "DuckDB query process is killed by OS OOM killer when aggregating multi-terabyte datasets.",
             "DuckDB attempted to hold massive hash join tables in memory without disk spilling configured.",
             "Configure `PRAGMA max_memory = '16GB';` and specify `PRAGMA temp_directory = '/path/to/fast_disk';` to enable graceful disk-spilling joins."),
            ("Sub-Optimal Parquet Row-Group Sizing",
             "Analytical query execution is 10x slower than expected when reading Parquet files.",
             "Parquet files were saved with tiny row groups (e.g. 500 rows per group), destroying columnar vectorization benefits and increasing metadata parsing overhead.",
             "Size Parquet row groups between 100,000 and 1,000,000 rows (approx 128MB-512MB per row group).")
        ]
    ),
    (
        "Module_19_Search_Engines_Elasticsearch_Lucene",
        "Search Engines: Elasticsearch, Lucene & Inverted Indexes",
        [
            ("Elasticsearch Cluster Red: Unassigned Shards",
             "Elasticsearch cluster status turns RED and queries return 503 Service Unavailable.",
             "Primary shards cannot be allocated due to disk watermarks (`cluster.routing.allocation.disk.watermark.flood_stage` exceeded 95%) or node network partition.",
             "Free disk space on data nodes, clear read-only blocks with `PUT /*/_settings {\"index.blocks.read_only_allow_delete\": null}`, and check shard allocation with `GET _cluster/allocation/explain`."),
            ("Mapping Explosion in Dynamic Indexing",
             "Master node CPU spikes to 100% and cluster state updates take seconds.",
             "Dynamic indexing allowed arbitrary JSON payloads with thousands of unique keys to create separate field mappings, breaching the 1,000 fields limit.",
             "Set `\"dynamic\": \"strict\"` or `\"dynamic\": false` in index mappings and map unpredictable key-value pairs into nested `key`/`value` structures."),
            ("Deep Pagination OOM via from + size",
             "Search query with `from: 50000, size: 50` crashes Elasticsearch data nodes.",
             "Deep pagination requires every shard to sort and return 50,050 documents to the coordinator node, which then merges and discards 50,000 records.",
             "Use the `search_after` API with tie-breaker sorting or Point-In-Time (PIT) searches instead of high `from` offsets.")
        ]
    ),
    (
        "Module_20_AI_Vector_Databases_pgvector_Qdrant",
        "AI Vector Databases: pgvector & Qdrant HNSW Similarity",
        [
            ("Un-Normalized Vectors Breaking Cosine Similarity",
             "Vector search returns nonsensical nearest neighbors with incorrect similarity ranking.",
             "Cosine distance calculations assume vectors are unit normalized or use dot product instead of true cosine distance.",
             "Normalize vector embeddings to unit length ($L_2$ norm = 1.0) before insertion or explicitly configure `Distance.COSINE` in index parameters."),
            ("HNSW Graph Disconnection Causing Catastrophic Recall Drop",
             "Approximate Nearest Neighbor (ANN) search recall drops from 98% to 45%.",
             "The HNSW parameter `ef_construction` or `m` was set too low during bulk insertion, causing disconnected graph clusters.",
             "Set `m = 16` or `32` and `ef_construction = 128` to `200` during index creation, and tune query-time `ef_search` for desired latency vs recall trade-offs."),
            ("pgvector IVFFlat Index Degradation After Data Growth",
             "Query latency on pgvector increases 20x after inserting 500,000 new vectors.",
             "An IVFFlat index partitions vectors into clusters based on centroids calculated *at index creation time*. Adding 10x more vectors invalidates centroid distributions.",
             "Rebuild the IVFFlat index (`REINDEX INDEX`) with `lists = sqrt(total_rows)` or switch to HNSW indexing (`CREATE INDEX USING hnsw`).")
        ]
    ),
    (
        "Module_21_Storage_Engine_Internals_BPlus_Trees",
        "Storage Engine Internals: Disk Pages & B+ Trees",
        [
            ("Off-By-One Key Search in Slotted Pages",
             "Point lookups fail to find newly inserted keys or return adjacent incorrect records.",
             "Binary search on slotted page key offsets failed to account for upper-bound vs lower-bound binary search semantics when keys match.",
             "Implement `bisect_right` or strict equality comparison and verify boundary conditions with property-based testing (Hypothesis)."),
            ("Deadlocks During Concurrent Node Splitting",
             "Multi-threaded B+ Tree threads hang permanently under heavy write load.",
             "Lock crabbing (coupling) acquired child locks without maintaining strict top-down root-to-leaf hierarchy, causing cyclic lock wait states.",
             "Enforce strict lock coupling: acquire child lock before releasing parent lock, and release parent only when child is guaranteed not to split."),
            ("Buffer Pool Dirty Page Eviction Without WAL Flush",
             "Database crashes cause unrecoverable corruption and violates ACID Durability.",
             "The buffer pool evicted a dirty data frame to disk before the corresponding WAL log record was flushed (violating the Write-Ahead Logging invariant).",
             "Strictly enforce WAL rule: `page.page_lsn <= flushed_to_disk_lsn` before allowing buffer pool manager to write any frame to disk.")
        ]
    ),
    (
        "Module_22_Query_Optimization_CBO_Index_Tuning",
        "Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning",
        [
            ("Exponential Join Permutation Explosion",
             "Query compilation takes 45 seconds for an 18-table JOIN query.",
             "Dynamic programming join ordering (System R) explores $O(3^N)$ subproblems, which explodes when joining $>12$ tables.",
             "Implement a threshold switching from exhaustive dynamic programming to Genetic Query Optimization (GEQO) or greedy heuristics for queries with $>10$ joins."),
            ("Missing Correlation Statistics on Interdependent Columns",
             "Query planner estimates 1 row returned, but query actually produces 500,000 rows, selecting a catastrophic Nested Loop join.",
             "The query filtered on `city = 'San Francisco' AND state = 'CA'`. Standard optimizer assumes column independence ($P(A \\cap B) = P(A) \\times P(B)$).",
             "Create extended multi-column statistics: `CREATE STATISTICS s_city_state ON city, state FROM addresses;` followed by `ANALYZE`."),
            ("Index Suppression via Function Wrapping in WHERE Clause",
             "Index on `created_at` is completely ignored, causing a full table scan.",
             "Writing `WHERE DATE(created_at) = '2026-01-01'` prevents the query planner from using the standard B-Tree index on `created_at`.",
             "Write sargable range queries: `WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`, or create an expression index: `CREATE INDEX idx_date ON tbl (DATE(created_at));`.")
        ]
    ),
    (
        "Module_23_Transactions_Isolation_Consensus_Raft",
        "Transactions, Isolation Levels & Distributed Consensus (Raft)",
        [
            ("Phantom Reads Under Repeatable Read in Standard SQL",
             "Transaction re-executes a range query and discovers new rows inserted by another committed transaction.",
             "Repeatable Read prevents non-repeatable reads on existing rows, but in standard locking engines (like MySQL without next-key locks), range locks are not held on phantom gaps.",
             "Elevate transaction isolation to `SERIALIZABLE` or verify your database engine uses Next-Key Locking (InnoDB) or Serializable Snapshot Isolation (PostgreSQL SSI)."),
            ("Split-Brain Leader Election in Raft",
             "Two nodes simultaneously believe they are the legitimate leader, accepting conflicting writes.",
             "A partitioned cluster elected a leader without achieving strict majority quorum ($N/2 + 1$).",
             "Enforce strict quorum vote tallying: a candidate can only step up if it receives affirmative votes from at least $(N/2) + 1$ distinct nodes in the cluster."),
            ("Two-Phase Commit (2PC) Indefinite Blocking on Coordinator Crash",
             "All participant databases in a distributed transaction hang with locked rows indefinitely.",
             "The 2PC coordinator crashed after participants entered the `PREPARED` state, leaving participants unable to decide whether to commit or abort.",
             "Implement automated coordinator recovery using persistent Write-Ahead Logs, or transition distributed transaction protocols to three-phase commit (3PC) or Paxos/Raft-backed transaction engines.")
        ]
    ),
    (
        "Module_24_Production_DBRE_Backups_Migrations_HA",
        "Production DBRE: Backups, Migrations, Monitoring & Runbooks",
        [
            ("Table Rewrite Lock Stalls During ALTER TABLE ADD COLUMN DEFAULT",
             "Executing a schema migration brings down production web services for 40 minutes.",
             "Adding a column with a non-null default value in older database engines rewrites the entire multi-gigabyte table on disk under an exclusive table lock.",
             "In modern PostgreSQL (>= 11) and MySQL (>= 8.0), non-volatile defaults are instant metadata-only operations. In older engines, add column as nullable first, backfill in batches, then set default and NOT NULL constraints."),
            ("Unverified Backups Causing Disaster Recovery Failure",
             "A ransomware event occurs, and engineers discover daily pg_dump backups have been corrupt or empty for 6 months.",
             "Backups were created on schedule but never automatically restored and verified.",
             "Implement automated continuous disaster recovery testing: schedule an automated CI job that restores the latest backup to an isolated staging instance, verifies row counts, and runs smoke tests daily."),
            ("Connection Pool Exhaustion During Upstream Microservice Latency",
             "Database connection pool spikes to 100% and crashes the application gateway.",
             "A slow external payment API caused HTTP worker threads to hold database connections open while waiting for third-party HTTP responses.",
             "Never hold database connections across external network I/O calls. Acquire database connections only for immediate database queries and release immediately.")
        ]
    ),
    (
        "Module_25_Final_Capstone_Polyglot_Enterprise",
        "Enterprise Polyglot Persistence Platform Capstone",
        [
            ("Dual-Write Distributed Inconsistency",
             "Database has customer order recorded, but search catalog and cache have no record of it.",
             "Application executed two independent network writes: `db.save(order)` followed by `redis.set(order)`. The second call failed due to network timeout.",
             "Implement the **Transactional Outbox Pattern**: write the business record AND the event intent to an outbox table in the SAME relational ACID transaction, and relay events downstream asynchronously via CDC."),
            ("Cache Stampede (Thundering Herd) on Hot Key Expiration",
             "Database CPU spikes to 100% and crashes the instant a high-traffic cache key expires.",
             "Thousands of concurrent incoming requests experienced a cache miss simultaneously and all queried the primary database at the exact same millisecond.",
             "Implement **Mutex Locking** (using Redis SET NX) so only 1 worker queries the database while others wait, or use probabilistic early expiration (XFetch algorithm)."),
            ("Stale Event Replay Overwriting Newer Data in Downstream Stores",
             "Customer profile in Elasticsearch shows old address after updating it to a new address.",
             "Out-of-order event delivery: Event 1 (update address to City B) was delayed by network jitter and processed after Event 2 (update address to City C).",
             "Enforce monotonic event versioning or timestamps in CDC payloads: downstream engines only apply mutations if `incoming_version > current_stored_version`.")
        ]
    ),
]

for folder, title, issues in TROUBLESHOOTING_DATA:
    target_path = root / folder / "TROUBLESHOOTING_AND_EDGE_CASES.md"
    content = f'''# {folder.replace("_", " ")}: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **{title}**, complete with root cause analysis and step-by-step resolution runbooks.

---

'''
    for idx, (bug_title, symptom, cause, fix) in enumerate(issues, 1):
        content += f'''## {idx}. {bug_title}

### 🚨 Symptom
> {symptom}

### 🔍 Root Cause Analysis
{cause}

### 🛠️ Production Fix & Mitigation Runbook
{fix}

---

'''

    content += '''## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
'''
    target_path.write_text(content, encoding="utf-8")

print(f"Generated {len(TROUBLESHOOTING_DATA)} TROUBLESHOOTING_AND_EDGE_CASES.md files successfully.")
