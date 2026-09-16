from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

DEBUG_LABS = [
    (
        "Module_01_Storage_Theory_ACID_Relational_Model",
        "broken_csv_engine.py",
        "Uncommitted Transaction Leaks into Primary Table During Power Failure",
        "The csv engine flushes uncommitted in-memory rows directly to table.csv during insert() rather than deferring until commit(). When a crash occurs before commit(), dirty data is permanently written.",
        "Buffer all rows in self.uncommitted_rows and append to table.csv strictly inside commit() after logging the COMMIT entry to the WAL."
    ),
    (
        "Module_02_Modern_SQL_Mastery_Advanced_Queries",
        "broken_window_query.py",
        "Running Total Generates Identical Duplicate Numbers on Duplicate Dates",
        "Window frame specification uses default RANGE frame instead of ROWS frame, causing rows with identical ORDER BY keys to sum together simultaneously.",
        "Change window frame to: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW."
    ),
    (
        "Module_03_Embedded_Databases_SQLite_WAL",
        "broken_wal_buffer.py",
        "Database is Locked Exception on High Concurrent Ingestion",
        "SQLite connection initialized without setting PRAGMA busy_timeout, causing any writer encountering a momentary lock to crash immediately with SQLITE_BUSY.",
        "Execute cur.execute('PRAGMA busy_timeout = 5000;') upon connection initialization."
    ),
    (
        "Module_04_PostgreSQL_Core_Advanced_Types",
        "broken_jsonb_filter.py",
        "Sequential Scan on 5,000,000 JSONB Document Catalog",
        "Query uses text extraction operator `data->>'status' = 'active'` which bypasses the GIN index created with jsonb_path_ops.",
        "Rewrite query to use JSONB containment: `data @> '{\"status\": \"active\"}'` or create an expression index on `((data->>'status'))`."
    ),
    (
        "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN",
        "broken_mvcc_purger.py",
        "Dead Tuple Bloat Prevents Autovacuum Reclamation",
        "A long-running reporting session opened a transaction with `BEGIN; SELECT ...` and remained idle in transaction for 18 hours, pinning xmin and preventing autovacuum from cleaning dead tuples.",
        "Configure `idle_in_transaction_session_timeout = '60s'` and terminate the lagging backend using `SELECT pg_terminate_backend(pid)`."
    ),
    (
        "Module_06_MySQL_MariaDB_InnoDB_Replication",
        "broken_innodb_order.py",
        "Deadlock 1213 on High Concurrency Multi-Row Updates",
        "Application updates multiple inventory rows in arbitrary order (Thread A updates Item 10 then 20; Thread B updates Item 20 then 10), triggering cyclic lock waits.",
        "Sort item IDs in ascending order in application code prior to issuing UPDATE statements: `for item_id in sorted(item_ids): ...`."
    ),
    (
        "Module_07_Oracle_Database_Architecture_SGA_PGA",
        "broken_sga_cursor.py",
        "ORA-04031 Shared Pool Out of Memory via Literal SQL",
        "Application constructs SQL dynamically using f-strings (`SELECT * FROM emp WHERE id = {emp_id}`), creating 100,000 unique unsharable execution plans in the Library Cache.",
        "Use bind variables: `cur.execute('SELECT * FROM emp WHERE id = :id', {'id': emp_id})`."
    ),
    (
        "Module_08_Oracle_PLSQL_Packages_Triggers",
        "broken_plsql_audit.py",
        "Audit Log Erased When Financial Transaction Fails",
        "The security audit logging procedure was declared without `PRAGMA AUTONOMOUS_TRANSACTION`. When the parent transfer rolls back due to insufficient funds, the audit record is rolled back with it.",
        "Add `PRAGMA AUTONOMOUS_TRANSACTION;` and an explicit `COMMIT;` inside the audit logger procedure body."
    ),
    (
        "Module_09_Oracle_RAC_DataGuard_GoldenGate",
        "broken_rac_router.py",
        "Interconnect Saturation Due to Unpartitioned Workload",
        "Both RAC nodes concurrently write and update the same account block ranges, causing continuous Cache Fusion buffer pinging over private interconnect.",
        "Partition workloads using dedicated Oracle Services (`SRVCTL`) to direct specific account partitions to designated RAC instances."
    ),
    (
        "Module_10_MongoDB_Document_Modeling_BSON",
        "broken_mongo_bucket.py",
        "BSONObjectTooLarge Error on Unbounded Sensor Array",
        "IoT readings appended continuously into a single document array without capping, eventually breaching the 16MB document size limit.",
        "Implement the Time-Series Bucket Pattern: store at most 500 readings per document bucket and insert a new document when bucket reaches capacity."
    ),
    (
        "Module_11_MongoDB_Aggregations_Replicas_Sharding",
        "broken_mongo_router.py",
        "Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB",
        "High-frequency operational user profile queries filter on `email` instead of the collection shard key `tenant_id`, broadcasting every query to all 10 shards.",
        "Include the shard key in the query filter: `db.users.find({'tenant_id': tenant, 'email': email})`."
    ),
    (
        "Module_12_Redis_Data_Structures_Persistence",
        "broken_redis_lock.py",
        "Distributed Lock Race Condition Releases Another Worker's Lock",
        "Worker acquires lock with `SET lock_key 1 EX 10`. Worker takes 12 seconds to finish. Lock expires. Worker 2 acquires lock. Worker 1 then calls `DEL lock_key`, releasing Worker 2's lock prematurely.",
        "Store a unique UUID token as the lock value and release exclusively via an atomic Lua script verifying token ownership before deleting."
    ),
    (
        "Module_13_Redis_Sentinel_Clustering_Lua",
        "broken_redis_cluster.py",
        "CROSSSLOT Keys in Request Don't Hash to the Same Slot",
        "Application attempts multi-key MGET on `user:101:profile` and `user:101:orders` across Redis Cluster, failing with CROSSSLOT error.",
        "Use Redis Hash Tags to force keys to the same slot: `{user:101}:profile` and `{user:101}:orders`."
    ),
    (
        "Module_14_Apache_Cassandra_Masterless_Ring",
        "broken_cassandra_schema.py",
        "ReadFailure Scanned Over 100,000 Tombstones",
        "Application repeatedly deleted expired queue items using CQL DELETE in a high-volume polling loop, generating millions of tombstones that choked subsequent range scans.",
        "Do not use Cassandra as a task queue; model data with TTL expiration on inserts and query using exact partition keys rather than broad range scans."
    ),
    (
        "Module_15_LSM_Trees_Compaction_DynamoDB",
        "broken_dynamo_hotkey.py",
        "ProvisionedThroughputExceededException on Single Partition Key",
        "All telemetry data from 50,000 sensors written to a single static partition key `PK = 'TELEMETRY'`, exceeding DynamoDB's 1,000 WCU per-partition ceiling.",
        "Implement write sharding: salt the partition key with random suffixes `PK = f'TELEMETRY#{random.randint(1, 10)}'`."
    ),
    (
        "Module_16_Neo4j_Graph_Databases_Cypher",
        "broken_cypher_match.py",
        "Cartesian Product OutOfMemoryError in Cypher Path Match",
        "Query written as `MATCH (a:Person), (b:Company) WHERE a.city = b.city` without a relationship pattern, forcing an exhaustive $N \\times M$ Cartesian product in RAM.",
        "Rewrite query to match explicit graph relationships or use an index-supported subquery."
    ),
    (
        "Module_17_Columnar_OLAP_DuckDB_ClickHouse",
        "broken_clickhouse_writer.py",
        "DB::Exception: Too Many Parts in Table in ClickHouse",
        "Microservice sends 5,000 single-row HTTP INSERT requests per second to ClickHouse MergeTree, exhausting background merge worker capacity.",
        "Batch inserts into chunks of at least 10,000 rows before sending to ClickHouse, or insert into a Buffer engine table."
    ),
    (
        "Module_19_Search_Engines_Elasticsearch_Lucene",
        "broken_es_search.py",
        "Deep Pagination Offset Crashes Elasticsearch Data Nodes",
        "Application paginates search results using `from: 50000, size: 50`, exhausting coordinator node heap memory.",
        "Use the `search_after` API with tie-breaker sorting or Point-In-Time (PIT) searches instead of high `from` offsets."
    ),
    (
        "Module_20_AI_Vector_Databases_pgvector_Qdrant",
        "broken_vector_distance.py",
        "Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors",
        "Embeddings inserted with arbitrary magnitudes while index was configured for Dot Product, causing vectors with huge norms to dominate similarity scores regardless of direction.",
        "Normalize all vector embeddings to unit length ($L_2$ norm = 1.0) before insertion: `v = v / np.linalg.norm(v)`."
    ),
    (
        "Module_21_Storage_Engine_Internals_BPlus_Trees",
        "broken_bplus_split.py",
        "Deadlock in Concurrent B+ Tree Node Split",
        "Writer released parent latch before acquiring child latch during downward traversal, allowing a concurrent split to invalidate node pointers.",
        "Enforce strict lock coupling (crabbing): do not release parent lock until child lock is acquired and confirmed safe from splitting."
    ),
    (
        "Module_22_Query_Optimization_CBO_Index_Tuning",
        "broken_query_index.py",
        "Full Table Scan Caused by Function Wrapping on Indexed Timestamp",
        "Query filters on `WHERE DATE(created_at) = '2026-01-01'`, blinding the query optimizer to the B-Tree index on `created_at`.",
        "Rewrite as a sargable range query: `WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`."
    ),
    (
        "Module_23_Transactions_Isolation_Consensus_Raft",
        "broken_raft_vote.py",
        "Split-Brain Dual Leader Election in Raft Cluster",
        "Candidate node transitions to Leader after receiving 2 votes in a 5-node cluster, violating majority quorum ($N/2 + 1 = 3$).",
        "Require strict majority: `if votes_received >= (len(self.nodes) // 2) + 1: self.become_leader()`."
    ),
    (
        "Module_24_Production_DBRE_Backups_Migrations_HA",
        "broken_migration_lock.py",
        "Exclusive Table Lock Starvation During Online Schema Migration",
        "Migration script runs `ALTER TABLE orders ADD COLUMN status_code INT;` without a lock_timeout, blocking behind a slow query and queuing all incoming web requests.",
        "Set strict lock timeout before running DDL: `SET lock_timeout = '2s'; ALTER TABLE ...`."
    ),
    (
        "Module_25_Final_Capstone_Polyglot_Enterprise",
        "broken_polyglot_sync.py",
        "Dual-Write Inconsistency Between Relational DB and Redis Cache",
        "Application updates database and then updates Redis in two uncoordinated calls. Redis network glitch drops cache update, leaving stale data forever.",
        "Implement the Transactional Outbox pattern: write update and outbox event in the same ACID transaction, relaying to Redis via CDC."
    ),
]

for folder, code_file, bug_title, cause, fix in DEBUG_LABS:
    lab_dir = root / folder / "debug_lab"
    lab_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. broken code
    broken_code = f'''"""DEBUG LAB: {bug_title}

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: {bug_title}")
    # Root Cause: {cause}
    raise RuntimeError("Defect triggered: {bug_title}")

if __name__ == "__main__":
    reproduce_defect()
'''
    (lab_dir / code_file).write_text(broken_code, encoding="utf-8")
    
    # 2. SYMPTOMS.md
    symptoms_md = f'''# Debug Lab: Incident Report & Symptoms

## Incident: {bug_title}
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** {folder.replace("_", " ")}

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd {folder}/debug_lab
   ```
2. Run the repro script:
   ```bash
   python {code_file}
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `{code_file}` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
'''
    (lab_dir / "SYMPTOMS.md").write_text(symptoms_md, encoding="utf-8")
    
    # 3. ANSWERS.md
    answers_md = f'''# Debug Lab: Forensic Analysis & Solution

## Incident: {bug_title}

### 🔍 Root Cause Analysis
{cause}

### 🛠️ The Fix
{fix}

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
'''
    (lab_dir / "ANSWERS.md").write_text(answers_md, encoding="utf-8")

print(f"Generated {len(DEBUG_LABS)} debug_lab directories successfully.")
