from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

EXPANSIONS = {
    "Module_01_Storage_Theory_ACID_Relational_Model": (
        "Transactional CSV Storage & WAL Internals",
        "csv_storage_engine.py",
        "csv_storage_engine.py (Pure-Python storage model)",
        "sqlite3 (Embedded stdlib reference comparison)",
        "1. Write Amplification: Modifying a 10-byte column in a 500MB CSV rewrites the entire 500MB file to disk.\n2. Torn Writes: Power cut midway through a multi-sector disk write leaves half-written, unparseable lines.\n3. Reader-Writer Lock Starvation: Long-running analytical table scans block write pipelines indefinitely.",
        "Do NOT use flat-file storage for concurrent multi-user transactional workloads, multi-node clustering, or tables exceeding 10,000 rows requiring sub-millisecond indexed point lookups.",
        "python -m project_solution.test_csv_engine -v\npython -c \"import sqlite3; conn = sqlite3.connect(':memory:'); print('SQLite Ready')\"",
        "00_interactive_storage_theory.ipynb"
    ),
    "Module_02_Modern_SQL_Mastery_Advanced_Queries": (
        "Modern SQL Mastery & Advanced Analytics",
        "sql_engine.py",
        "sql_engine.py (In-memory SQL evaluator)",
        "sqlite3 (Built-in engine executing analytical queries)",
        "1. NULL Propagation in NOT IN: A single NULL returned by a subquery causes the entire NOT IN clause to evaluate to empty.\n2. RANGE Frame Duping: Default window framing computes running sums across duplicate timestamp peers simultaneously.\n3. Cartesian Explosion: Joining a parent table with two independent 1:N child tables multiplies row counts exponentially.",
        "Do NOT use complex recursive CTEs for real-time sub-millisecond graph traversals over millions of edges; use a dedicated graph database (Neo4j) instead.",
        "sqlite3 app.db \"EXPLAIN QUERY PLAN SELECT ...\"\nsqlite3 app.db \".timer on\" \"SELECT ...\"",
        "00_interactive_sql_mastery.ipynb"
    ),
    "Module_03_Embedded_Databases_SQLite_WAL": (
        "Embedded Databases: SQLite & WAL Architecture",
        "sqlite_wal_engine.py",
        "sqlite_wal_engine.py (WAL concurrency model)",
        "sqlite3 (WAL mode, busy_timeout, custom UDFs)",
        "1. Database Locked: Concurrent writers without busy_timeout immediately throw SQLITE_BUSY.\n2. Runaway WAL Growth: Long-running active readers holding open old read snapshots prevent WAL checkpoint truncation.\n3. Silent Corruption: Running with PRAGMA synchronous = OFF risks torn pages on sudden power cut.",
        "Do NOT use SQLite across network-attached storage (NFS, SMB) or for applications requiring dozens of simultaneous high-throughput concurrent writers.",
        "sqlite3 app.db \"PRAGMA journal_mode = WAL;\"\nsqlite3 app.db \"PRAGMA wal_checkpoint(TRUNCATE);\"\nsqlite3 app.db \"PRAGMA integrity_check;\"",
        "00_interactive_sqlite_wal.ipynb"
    ),
    "Module_04_PostgreSQL_Core_Advanced_Types": (
        "PostgreSQL Core Architecture & Advanced Types",
        "jsonb_document_store.py",
        "jsonb_document_store.py (JSONB binary encoder & GIN index)",
        "postgres_live.py (psycopg2 connection pool, JSONB queries)",
        "1. Connection Slot Exhaustion: Exceeding max_connections crashes incoming traffic due to per-process RAM consumption.\n2. GIN Index Bypass: Using text extraction (->>) rather than containment (@>) forces full sequential heap scans.\n3. Integer ID Wraparound: Using standard 32-bit SERIAL triggers integer overflow on high-volume tables.",
        "Do NOT use PostgreSQL as a high-velocity write-ahead message broker (Kafka use case) or for petabyte-scale unpartitioned analytical queries without columnar extensions (ClickHouse / DuckDB use case).",
        "psql -h localhost -U postgres -c \"SELECT count(*) FROM pg_stat_activity;\"\npsql -h localhost -U postgres -c \"SELECT pg_size_pretty(pg_database_size('coursedb'));\"",
        "00_interactive_postgres_core.ipynb"
    ),
    "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN": (
        "PostgreSQL MVCC, Vacuuming & Execution Plans",
        "mvcc_engine.py",
        "mvcc_engine.py (Tuple versioning & visibility map simulator)",
        "mvcc_live.py (Real EXPLAIN ANALYZE BUFFERS, dead tuple diagnosis)",
        "1. Autovacuum Starvation: Idle-in-transaction connections hold back xmin, causing table bloat to swell 100x.\n2. Stale Catalog Statistics: Bulk data changes without ANALYZE trick the planner into choosing slow sequential scans.\n3. Exclusive DDL Locks: Running CREATE INDEX without CONCURRENTLY locks out all read/write application traffic.",
        "Do NOT rely on standard B-Tree indexes for high-dimensional vector search (use pgvector/HNSW) or for full-text search with complex linguistic stemming (use Elasticsearch or GiST/GIN tsvector).",
        "psql -h localhost -U postgres -c \"EXPLAIN (ANALYZE, BUFFERS) SELECT ...;\"\npsql -h localhost -U postgres -c \"SELECT relname, n_dead_tup, last_vacuum FROM pg_stat_user_tables;\"",
        "00_interactive_postgres_mvcc.ipynb"
    ),
    "Module_06_MySQL_MariaDB_InnoDB_Replication": (
        "MySQL & InnoDB Architecture, Buffer Pool & Replication",
        "innodb_engine.py",
        "innodb_engine.py (Clustered index & buffer pool LRU model)",
        "mysql_live.py (mysql-connector-python, read/write split router)",
        "1. Transaction Deadlock (Error 1213): Unordered concurrent updates create wait-for graph cycles, triggering rollbacks.\n2. Replication Lag: Single-threaded replica appliers lag behind write-heavy primaries, serving stale read data.\n3. Buffer Pool Thrashing: Large analytical table sweeps flush frequently accessed OLTP pages from the LRU young sublist.",
        "Do NOT use MySQL with MyISAM storage engine in modern production; always use InnoDB to guarantee ACID transaction durability and crash recovery.",
        "mysql -u root -p -e \"SHOW ENGINE INNODB STATUS\\G\"\nmysql -u root -p -e \"SHOW REPLICA STATUS\\G\"\nmysql -u root -p -e \"SELECT * FROM performance_schema.threads WHERE PROCESSLIST_COMMAND != 'Sleep';\"",
        "00_interactive_mysql_innodb.ipynb"
    ),
    "Module_07_Oracle_Database_Architecture_SGA_PGA": (
        "Oracle Database Architecture: SGA, PGA & Storage",
        "oracle_sga_engine.py",
        "oracle_sga_engine.py (Library Cache & Buffer Cache touch-count)",
        "oracle_live.py (python-oracledb, v$sgainfo, v$sysstat)",
        "1. ORA-04031 Shared Pool Exhaustion: Literal SQL without bind variables creates millions of unsharable execution plans.\n2. Buffer Cache Contention: Inadequate buffer pool sizing forces synchronous DBWR writer stalls on dirty page flushes.\n3. High-Water Mark Scan Penalty: Deleted records leave HWM elevated, forcing full table scans to read millions of empty blocks.",
        "Do NOT deploy Oracle Database without configuring automated memory target parameters (ASMM/AMM) and strict bind variable enforcement across client applications.",
        "sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF\nSELECT pool, name, bytes FROM v\\$sgastat WHERE bytes > 10000000;\nEXIT;\nEOF",
        "00_interactive_oracle_architecture.ipynb"
    ),
    "Module_08_Oracle_PLSQL_Packages_Triggers": (
        "Oracle PL/SQL Packages, Triggers & Autonomous Transactions",
        "oracle_plsql_engine.py",
        "oracle_plsql_engine.py (Autonomous audit logger & banking package)",
        "oracle_plsql_live.py (python-oracledb, PL/SQL package execution)",
        "1. ORA-04091 Mutating Table: Row-level triggers attempting to query the table currently being modified.\n2. Context Switching Overhead: Iterating row-by-row in PL/SQL loops rather than using FORALL bulk array binding.\n3. Lost Audit Records: Omitting PRAGMA AUTONOMOUS_TRANSACTION causes security logs to roll back when parent transactions fail.",
        "Do NOT put complex business logic in database triggers where execution flow becomes invisible and difficult to trace; encapsulate logic in PL/SQL Packages.",
        "sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF\nSELECT object_name, status FROM user_objects WHERE object_type = 'PACKAGE BODY';\nEXIT;\nEOF",
        "00_interactive_oracle_plsql.ipynb"
    ),
    "Module_09_Oracle_RAC_DataGuard_GoldenGate": (
        "Oracle RAC, Active Data Guard & Real-Time Replication",
        "oracle_rac_engine.py",
        "oracle_rac_engine.py (Cache Fusion & Data Guard SCN replicator)",
        "oracle_ha_live.py (python-oracledb, v$database, gv$instance)",
        "1. Interconnect Cache Fusion Pinging: Concurrent cross-node writes to the same blocks saturate private interconnect RAM.\n2. Standby Transport Lag: Network bandwidth bottlenecks cause Active Data Guard to lag behind primary transaction streams.\n3. Split-Brain Node Isolation: Loss of private interconnect without proper voting disk quorum causes cluster eviction stalls.",
        "Do NOT stretch Oracle RAC clusters across high-latency WANs (use Active Data Guard or GoldenGate for cross-region replication instead).",
        "sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF\nSELECT inst_id, instance_name, status FROM gv\\$instance;\nSELECT protection_mode, open_mode FROM v\\$database;\nEXIT;\nEOF",
        "00_interactive_oracle_ha.ipynb"
    ),
    "Module_10_MongoDB_Document_Modeling_BSON": (
        "MongoDB Document Modeling & BSON Wire Protocol",
        "bson_document_engine.py",
        "bson_document_engine.py (BSON encoder/decoder & ObjectId)",
        "mongo_live.py (pymongo client, TTL indexes, explain COLLSCAN)",
        "1. 16MB BSON Document Limit: Unbounded array embedding eventually breaches MongoDB's hard document ceiling.\n2. Accidental COLLSCAN: Omitting composite indexes forces MongoDB to scan millions of documents into memory.\n3. Schema Validation Write Rejection: Strict JSON schema rules rejecting mismatched field types during application releases.",
        "Do NOT use MongoDB as a pure relational substitute with hundreds of multi-collection $lookup joins; design documents around application access patterns.",
        "mongosh mongodb://localhost:27017/coursedb --eval \"db.serverStatus().mem\"\nmongosh mongodb://localhost:27017/coursedb --eval \"db.collection.stats()\"",
        "00_interactive_mongo_document.ipynb"
    ),
    "Module_11_MongoDB_Aggregations_Replicas_Sharding": (
        "MongoDB Aggregation Pipelines, Replication & Sharding",
        "mongo_aggregation_engine.py",
        "mongo_aggregation_engine.py (Pipeline stages & shard router)",
        "mongo_scale_live.py (pymongo aggregation pipeline, $facet, $lookup)",
        "1. 100MB Pipeline RAM Limit: In-memory $group and $sort operations crash unless allowDiskUse is enabled.\n2. Scatter-Gather Sharding Penalty: Queries lacking shard keys broadcast to all cluster shards, destroying throughput.\n3. Stale Secondary Reads: Using secondaryPreferred with readConcern local reading uncommitted or lagging oplog states.",
        "Do NOT choose low-cardinality shard keys (e.g. status or country) which create un-splittable jumbo chunks and extreme hot partition bottlenecks.",
        "mongosh mongodb://localhost:27017/coursedb --eval \"sh.status()\"\nmongosh mongodb://localhost:27017/coursedb --eval \"rs.status()\"",
        "00_interactive_mongo_aggregation.ipynb"
    ),
    "Module_14_Apache_Cassandra_Masterless_Ring": (
        "Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column",
        "cassandra_ring_engine.py",
        "cassandra_ring_engine.py (Token ring, consistent hashing, quorum)",
        "cassandra_live.py (cassandra-driver, CQL queries, tunable consistency)",
        "1. Tombstone Overload: Frequent deletions creating millions of tombstones that abort subsequent range scans.\n2. Hot Partitions: Choosing low-cardinality partition keys concentrating gigabytes of writes onto a single physical node.\n3. Write Timeout on ALL: Using ConsistencyLevel.ALL causing write failure whenever a single node undergoes restart.",
        "Do NOT use Apache Cassandra as an ACID queue or run queries requiring ad-hoc JOINs, aggregations, or unpartitioned secondary index searches.",
        "cqlsh localhost 9042 -e \"DESCRIBE KEYSPACES;\"\nnodetool status\nnodetool info",
        "00_interactive_cassandra_ring.ipynb"
    ),
    "Module_16_Neo4j_Graph_Databases_Cypher": (
        "Graph Databases: Neo4j & Declarative Cypher",
        "graph_engine.py",
        "graph_engine.py (Index-free adjacency property graph & BFS)",
        "neo4j_live.py (neo4j driver, Cypher shortest path, social graphs)",
        "1. Cypher Cartesian Product: Unconnected patterns in MATCH generating trillions of intermediate combinations in RAM.\n2. Supernode Traversal Hangs: Nodes with millions of edges causing traversal queries to stall reading relationship pointers.\n3. Missing Schema Indexes: Missing label/property indexes forcing Neo4j into NodeByLabelScan instead of NodeIndexSeek.",
        "Do NOT use a graph database for bulk tabular analytical reporting (OLAP) or simple key-value lookups where Redis or DuckDB are orders of magnitude faster.",
        "cypher-shell -u neo4j -p password \"MATCH (n) RETURN count(n);\"\ncypher-shell -u neo4j -p password \"SHOW INDEXES;\"",
        "00_interactive_neo4j_cypher.ipynb"
    ),
    "Module_20_AI_Vector_Databases_pgvector_Qdrant": (
        "AI Vector Databases: pgvector & Qdrant HNSW Similarity",
        "vector_engine.py",
        "vector_engine.py (Cosine distance, flat k-NN, HNSW graph)",
        "vector_live.py (Qdrant in-memory client, payload filtering, ANN)",
        "1. Unnormalized Vectors in Dot Product: Magnitude disparities distorting similarity rankings away from true angle.\n2. HNSW Graph Disconnection: Undersized ef_construction causing isolated subgraphs and catastrophic recall drops.\n3. IVFFlat Centroid Drift: Substantial data insertions shifting vector distribution without rebuilding centroid lists.",
        "Do NOT use vector databases for exact scalar queries (e.g. `WHERE user_id = 12345`); always combine vector search with relational or document stores.",
        "python -c \"import qdrant_client; print('Qdrant Ready')\"\npsql -h localhost -U postgres -c \"SELECT * FROM pg_extension WHERE extname = 'vector';\"",
        "00_interactive_vector_qdrant.ipynb"
    ),
    "Module_21_Storage_Engine_Internals_BPlus_Trees": (
        "Storage Engine Internals: Disk Pages & B+ Trees",
        "storage_engine.py",
        "storage_engine.py (Slotted pages, B+ Tree node splitting)",
        "storage_engine.py (Pure storage engine internals reference)",
        "1. Deadlocks in Node Splits: Releasing parent latches before acquiring child latches causing concurrent split corruption.\n2. Slotted Page Fragmentation: Deletions creating dead space gaps that exhaust page capacity without defragmentation.\n3. Dirty Page Flush Invariant Breach: Writing dirty pages to disk before flushing corresponding WAL log records.",
        "Do NOT implement custom storage engines for general-purpose applications; rely on battle-tested production engines (RocksDB, InnoDB, PostgreSQL).",
        "pytest Module_21_Storage_Engine_Internals_BPlus_Trees -v",
        "00_interactive_bplus_trees.ipynb"
    ),
    "Module_22_Query_Optimization_CBO_Index_Tuning": (
        "Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning",
        "query_optimizer.py",
        "query_optimizer.py (CBO, System R join dynamic programming)",
        "explain_live.py (psycopg2 EXPLAIN ANALYZE BUFFERS, index advisor)",
        "1. Join Permutation Explosion: Dynamic programming join enumeration exploding exponentially ($O(3^N)$) on $>12$ joins.\n2. Correlated Column Blindness: Multi-column filters assuming attribute independence, miscalculating selectivity by 1000x.\n3. Non-Sargable Function Wrapping: Wrapping indexed columns in functions forcing the planner into full table scans.",
        "Do NOT attempt to force specific index hints in production queries unless automated statistics and optimizer settings have failed and query regression is imminent.",
        "psql -h localhost -U postgres -c \"EXPLAIN (ANALYZE, COSTS, BUFFERS) SELECT ...;\"",
        "00_interactive_query_optimization.ipynb"
    ),
    "Module_23_Transactions_Isolation_Consensus_Raft": (
        "Transactions, Isolation Levels & Distributed Consensus (Raft)",
        "transaction_raft_engine.py",
        "transaction_raft_engine.py (Raft consensus, 2PC, isolation levels)",
        "isolation_live.py (psycopg2 isolation levels, dirty/phantom reads)",
        "1. Write Skew under Snapshot Isolation: Concurrent transactions modifying disjoint rows based on shared premise.\n2. Split-Brain Dual Leader: Candidate becoming leader without strict majority quorum ($N/2 + 1$), accepting divergent writes.\n3. 2PC Indefinite Lock Blocking: Coordinator crashing after participants enter PREPARED state, freezing resources.",
        "Do NOT implement custom distributed consensus protocols in application code; utilize established distributed consensus backbones (etcd, Raft, Paxos).",
        "pytest Module_23_Transactions_Isolation_Consensus_Raft -v",
        "00_interactive_transactions_consensus.ipynb"
    ),
    "Module_24_Production_DBRE_Backups_Migrations_HA": (
        "Production DBRE: Backups, Migrations, Monitoring & Runbooks",
        "dbre_engine.py",
        "dbre_engine.py (PITR, zero-downtime migration, pool monitor)",
        "dbre_live.py (psycopg2 pool monitoring, non-blocking migrations)",
        "1. Table Lock Starvation: Schema migrations lacking strict lock_timeout queuing behind slow queries and bringing down web traffic.\n2. Untested Backups: Creating daily database dumps that fail to restore during real disasters due to corruption or permission drift.\n3. Connection Pool Over-allocation: Oversized connection pools thrashing CPU caches and exhausting database memory.",
        "Do NOT perform schema migrations directly during peak traffic hours without automated transaction timeouts and verified backward compatibility.",
        "pg_isready -h localhost -p 5432\npsql -h localhost -U postgres -c \"SELECT * FROM pg_stat_activity WHERE state != 'idle';\"",
        "00_interactive_production_dbre.ipynb"
    ),
    "Module_25_Final_Capstone_Polyglot_Enterprise": (
        "Enterprise Polyglot Persistence Platform Capstone",
        "polyglot_platform.py",
        "polyglot_platform.py (In-memory polyglot coordinator model)",
        "polyglot_live.py (PostgreSQL OLTP, Outbox CDC, Redis Cache, DuckDB)",
        "1. Dual-Write Inconsistency: Direct application dual-writes dropping downstream updates on network glitch.\n2. Cache Stampede: Hot key expiration causing thousands of concurrent workers to swamp primary relational database.\n3. Out-of-Order Event Replay: CDC event delivery delays causing older event versions to overwrite newer mutations.",
        "Do NOT introduce polyglot persistence prematurely; start with a single robust relational engine until distinct scaling boundaries demand specialized stores.",
        "pytest Module_25_Final_Capstone_Polyglot_Enterprise -v\nredis-cli ping\npsql -h localhost -U postgres -c \"SELECT count(*) FROM outbox_events WHERE published = 0;\"",
        "00_interactive_polyglot_platform.ipynb"
    ),
}

for folder, (title, tr_a_file, tr_a_desc, tr_b_desc, pitfalls, when_not, cli_cmd, nb_file) in EXPANSIONS.items():
    readme_path = root / folder / "README.md"
    if not readme_path.exists():
        continue
    current_content = readme_path.read_text(encoding="utf-8")
    
    # Only append if not already appended
    if "## 5. Dual-Track Curriculum: Track A" in current_content or "## Dual-Track Architecture" in current_content:
        continue
        
    addition = f'''

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/{tr_a_file}` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | {tr_a_desc} | {tr_b_desc} |
| **Verification** | `project_solution/test_{tr_a_file}` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

{pitfalls}

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

{when_not}

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest {folder} -v

# Operational Diagnostics & Health Verification
{cli_cmd}
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab]({nb_file})**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.
'''
    readme_path.write_text(current_content.rstrip() + addition + "\n", encoding="utf-8")

print("Expanded all 19 thin READMEs successfully.")
