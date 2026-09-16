from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

MODULES_PROJECT_DATA = [
    (
        "Module_02_Modern_SQL_Mastery_Advanced_Queries",
        "Modern SQL Mastery & Advanced Analytics",
        "Hierarchical Organization & Financial Cohort Analysis Engine",
        "window functions, recursive CTEs, and correlated subqueries",
        "Implement basic inner/left joins and simple GROUP BY aggregates.",
        "Build a multi-stage financial analytics query calculating rolling 30-day customer spend, retention cohorts, and recursive managerial hierarchy.",
        "Implement custom temporal gap-and-island detection identifying contiguous subscription streaks using LEAD/LAG."
    ),
    (
        "Module_03_Embedded_Databases_SQLite_WAL",
        "Embedded Databases: SQLite & WAL Architecture",
        "High-Concurrency In-Memory SQLite Telemetry Buffer",
        "WAL journal mode, synchronous pragmas, and custom C/Python UDF extensions",
        "Configure standard SQLite database with table schemas and basic inserts.",
        "Build a thread-safe telemetry ingestion buffer in WAL mode with busy_timeout, custom haversine distance UDF, and zero writer starvation.",
        "Build an automated incremental WAL checkpointing scheduler that dynamically monitors -wal file byte size and executes PASSIVE vs RESTART checkpoints."
    ),
    (
        "Module_04_PostgreSQL_Core_Advanced_Types",
        "PostgreSQL Core Architecture & Advanced Types",
        "Poly-Schema Catalog with JSONB, Arrays & Custom Domains",
        "PostgreSQL native types, GIN indexing, and connection pooling",
        "Create standard relational tables with text, integer, and timestamp fields.",
        "Implement a schema-agnostic product catalog supporting JSONB document containment queries, tag array intersections, and connection pooling via psycopg2 ThreadedConnectionPool.",
        "Construct custom composite types and range types with EXCLUDE USING GIST constraints preventing double-booking anomalies."
    ),
    (
        "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN",
        "PostgreSQL MVCC, Vacuuming & Execution Plans",
        "Index Advisor & MVCC Bloat Diagnosis Engine",
        "Heap pages, visibility maps, vacuuming, and EXPLAIN (ANALYZE, BUFFERS)",
        "Inspect simple index lookups using EXPLAIN.",
        "Build an automated index tuner diagnosing table bloat (xmin/xmax), detecting missing composite indexes, and evaluating Seq Scan vs Index Scan cost shifts.",
        "Design a zero-downtime index migration runner using CREATE INDEX CONCURRENTLY with transaction timeouts and pg_stat_activity deadlock guards."
    ),
    (
        "Module_06_MySQL_MariaDB_InnoDB_Replication",
        "MySQL & InnoDB Architecture, Buffer Pool & Replication",
        "InnoDB Buffer Pool Monitor & Read/Write Split Router",
        "Clustered index (B+ Tree), redo/undo logs, binlog GTID replication, and connection pooling",
        "Execute standard MySQL queries using mysql-connector-python.",
        "Build a dual-pool connection router directing writes to Primary and reads to Read Replicas with replication lag threshold guards.",
        "Implement an automated deadlock forensic collector querying INFORMATION_SCHEMA.INNODB_TRX and parsing LATEST DETECTED DEADLOCK from SHOW ENGINE INNODB STATUS."
    ),
    (
        "Module_07_Oracle_Database_Architecture_SGA_PGA",
        "Oracle Database Architecture: SGA, PGA & Storage",
        "Oracle SGA Library Cache & Buffer Cache Hit Ratio Analyzer",
        "Shared Pool, Database Buffer Cache, Redo Log Buffer, and Extent Allocator",
        "Connect to Oracle Database using python-oracledb and run basic SELECT queries.",
        "Implement an automated SGA diagnostics probe monitoring Shared Pool Library Cache hard vs soft parses and Buffer Cache touch-count hit ratios.",
        "Design a tablespace extent allocation monitor tracking High-Water Mark (HWM) fragmentation and predicting tablespace exhaustion."
    ),
    (
        "Module_08_Oracle_PLSQL_Packages_Triggers",
        "Oracle PL/SQL Packages, Triggers & Autonomous Transactions",
        "Enterprise Core Banking Package with Autonomous Audit Trail",
        "PL/SQL package procedures, compound triggers, FORALL bulk binds, and PRAGMA AUTONOMOUS_TRANSACTION",
        "Deploy basic stored procedures in Oracle and invoke via python-oracledb.",
        "Develop an enterprise banking package enforcing atomic fund transfers, FORALL bulk array processing, and an autonomous audit logger that persists security records across transaction rollbacks.",
        "Build a 4-phase Compound DML Trigger maintaining real-time aggregate materialized caches while preventing mutating table errors (ORA-04091)."
    ),
    (
        "Module_09_Oracle_RAC_DataGuard_GoldenGate",
        "Oracle RAC, Active Data Guard & Real-Time Replication",
        "RAC Cache Fusion & Data Guard Failover Coordinator",
        "Global Cache Service (GCS), interconnect RAM transfer, SCN redo transport, and switchover",
        "Connect to Oracle RAC service names using connection strings.",
        "Build a High Availability coordinator monitoring RAC node interconnect dirty-block transfers and Data Guard transport lag.",
        "Implement an automated Fast Connection Failover (FCF) handler detecting instance crash events and repointing active transaction pools without client data loss."
    ),
    (
        "Module_10_MongoDB_Document_Modeling_BSON",
        "MongoDB Document Modeling & BSON Wire Protocol",
        "E-Commerce Product Catalog with Embedding vs Referencing",
        "BSON serialization, schema validation, TTL indexes, and atomic document updates",
        "Perform basic CRUD operations in MongoDB using pymongo.",
        "Build a high-performance document store optimizing 1:N embedding vs referencing, strict JSON schema validators, and atomic $set/$inc/$push updates.",
        "Implement an automated document migration pipeline restructuring millions of unindexed nested arrays into the Time-Series Bucket Pattern."
    ),
    (
        "Module_11_MongoDB_Aggregations_Replicas_Sharding",
        "MongoDB Aggregation Pipelines, Replication & Sharding",
        "Multi-Stage E-Commerce Sales Pipeline & Shard Router",
        "Aggregation pipeline ($match, $unwind, $group, $facet, $lookup), read preferences, and hash routing",
        "Run simple $match and $group aggregation queries in MongoDB.",
        "Build an analytics aggregation pipeline calculating gross merchandise value, faceted categorization, and cross-collection joins via $lookup.",
        "Simulate a mongos shard router evaluating targeted single-shard queries vs cluster-wide scatter-gather broadcasts across hash-partitioned keys."
    ),
    (
        "Module_12_Redis_Data_Structures_Persistence",
        "Redis Internals: Data Structures, RDB/AOF & Sliding Windows",
        "Sliding-Window Rate Limiter & Token Bucket In-Memory Broker",
        "Strings, Hashes, Sets, Sorted Sets, Bitmaps, HyperLogLog, RDB, and AOF rewrite",
        "Connect to Redis and set/get string keys with TTL.",
        "Build a production-grade sliding-window rate limiter using Redis Sorted Sets (ZADD, ZREMRANGEBYSCORE) and an LRU cache-aside helper.",
        "Implement a Redis-backed Distributed Lock using SET NX EX with Lua script safe-release verification."
    ),
    (
        "Module_13_Redis_Sentinel_Clustering_Lua",
        "Redis High Availability: Sentinel, Clustering & Lua Scripting",
        "Atomic Multi-Resource Reservation Engine with Lua & Sentinel",
        "Redis Sentinel failover, hash slot cluster partitioning (16384 slots), and atomic Lua scripts",
        "Execute simple Lua scripts via EVAL in Redis.",
        "Build an atomic multi-inventory reservation engine executing in Lua, wrapped with Sentinel automatic failover client discovery.",
        "Implement a hash slot cluster router with MOVED/ASK redirection handling and cross-slot multi-key hash tag constraints."
    ),
    (
        "Module_14_Apache_Cassandra_Masterless_Ring",
        "Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column",
        "Distributed IoT Time-Series Store with Tunable Consistency",
        "Consistent hashing token ring, wide-column keyspaces, tunable quorum, and LWT",
        "Create keyspaces and simple tables using CQL and cassandra-driver.",
        "Design a wide-column IoT time-series schema partitioned by (device_id, date_bucket) and ordered by timestamp, executing reads and writes with tunable QUORUM consistency.",
        "Build a chaos testing simulator verifying read-repair reconciliation and tombstone compaction behavior under simulated network partition."
    ),
    (
        "Module_15_LSM_Trees_Compaction_DynamoDB",
        "LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design",
        "Single-Table Enterprise SaaS Core with DynamoDB",
        "LSM-Trees (MemTable, SSTable), Bloom filters, leveled compaction, and DynamoDB single-table design",
        "Perform basic PutItem and GetItem operations using boto3.",
        "Design and implement a DynamoDB Single-Table architecture supporting Users, Organizations, and Invoices using composite PK/SK and GSI inverse lookups.",
        "Build an in-memory LSM storage engine implementing SSTable tiered merge-compaction and Bloom filter membership queries."
    ),
    (
        "Module_16_Neo4j_Graph_Databases_Cypher",
        "Graph Databases: Neo4j & Declarative Cypher",
        "Anti-Money Laundering (AML) Financial Fraud Detection Engine",
        "Property graph model, index-free adjacency, Cypher query optimization, and path algorithms",
        "Create nodes and edges in Neo4j using the official Python driver.",
        "Build a fraud detection pipeline detecting circular payment rings, shell corporation ownership paths, and shortest paths between high-risk entities.",
        "Implement a graph centrality and community detection module calculating PageRank and connected components over transaction subgraphs."
    ),
    (
        "Module_17_Columnar_OLAP_DuckDB_ClickHouse",
        "Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics",
        "High-Throughput Analytics Engine on Parquet & ClickHouse",
        "Columnar storage, vectorized SIMD execution, Parquet pushdown, and ClickHouse MergeTree",
        "Query local CSV and Parquet files using DuckDB SQL.",
        "Build a sub-second analytical reporting engine executing complex group-by aggregations on millions of records using DuckDB and ClickHouse MergeTree engines.",
        "Implement partition-pruning and min/max index skipping benchmarks demonstrating columnar speedups over row-oriented relational storage."
    ),
    (
        "Module_19_Search_Engines_Elasticsearch_Lucene",
        "Search Engines: Elasticsearch, Lucene & Inverted Indexes",
        "Enterprise Knowledge Base Search with BM25 & Fuzzy Matching",
        "Inverted index, postings lists, analyzers, Okapi BM25 ranking, and fuzzy Levenshtein matching",
        "Index and search documents in Elasticsearch using elasticsearch-py.",
        "Build an enterprise search engine with custom tokenizers, BM25 term weighting, compound bool queries, and typo-tolerant fuzzy matching.",
        "Construct a two-phase Query-Then-Fetch distributed search simulation demonstrating score coordination across shards."
    ),
    (
        "Module_20_AI_Vector_Databases_pgvector_Qdrant",
        "AI Vector Databases: pgvector & Qdrant HNSW Similarity",
        "Semantic Document Retrieval Engine with HNSW & Metadata Filtering",
        "Vector embeddings, distance metrics (Cosine, L2, Dot), HNSW graph indexing, and payload filtering",
        "Generate mock vector embeddings and compute cosine similarity.",
        "Build a semantic search service using Qdrant (in-memory / live) and pgvector, supporting HNSW approximate nearest neighbor search with strict metadata payload filters.",
        "Implement an ANN recall benchmark evaluating Top-K retrieval precision against exact brute-force flat search across varying graph ef_search parameters."
    ),
    (
        "Module_21_Storage_Engine_Internals_BPlus_Trees",
        "Storage Engine Internals: Disk Pages & B+ Trees",
        "Disk-Backed B+ Tree Storage Engine with Page Cache",
        "Slotted-page architecture, B+ Tree node splitting/merging, and buffer pool frame management",
        "Implement a binary search over in-memory key-value arrays.",
        "Build a fully functional B+ Tree storage engine storing 4KB disk pages, implementing node splits on overflow, and supporting logarithmic point lookups and range scans.",
        "Implement a concurrent B+ Tree latching protocol using crabbing (coupling) to support simultaneous readers and writers."
    ),
    (
        "Module_22_Query_Optimization_CBO_Index_Tuning",
        "Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning",
        "Relational Query Planner & Cost-Based Optimizer",
        "Relational algebra AST, cost estimation (CPU vs I/O), join ordering (dynamic programming), and index selection",
        "Parse simple SQL SELECT statements into an Abstract Syntax Tree (AST).",
        "Build a cost-based query optimizer that enumerates join permutations (System R dynamic programming), evaluates table statistics (histograms), and selects optimal physical operators (Hash Join vs Nested Loop).",
        "Implement genetic query optimization (GEQO) for large multi-table joins (>10 relations) avoiding exponential search space explosion."
    ),
    (
        "Module_23_Transactions_Isolation_Consensus_Raft",
        "Transactions, Isolation Levels & Distributed Consensus (Raft)",
        "Distributed Transaction Coordinator & Raft Consensus Replicator",
        "ACID isolation levels (Dirty Read, Non-Repeatable Read, Phantom Read), 2-Phase Commit (2PC), and Raft consensus",
        "Simulate two transactions interacting under Read Committed isolation.",
        "Build a Raft consensus cluster implementing Leader Election, Log Replication, and Term progression, coordinating distributed writes across 3 nodes.",
        "Implement a Two-Phase Commit (2PC) coordinator with PREPARE, COMMIT/ABORT phases and crash recovery handling coordinator failure during commit."
    ),
    (
        "Module_24_Production_DBRE_Backups_Migrations_HA",
        "Production DBRE: Backups, Migrations, Monitoring & Runbooks",
        "Production Database Reliability Toolkit & Automated Failover",
        "Physical/logical backups, PITR recovery, zero-downtime schema migrations, connection pooling, and SLO/alerting",
        "Write basic database backup scripts using pg_dump / mysqldump.",
        "Build an automated DBRE reliability suite featuring connection pool health checks, non-blocking online schema migration runners, and point-in-time recovery verification.",
        "Develop an automated failover controller with split-brain prevention (STONITH/fencing) and Prometheus metric exporter for p99 latency and replication lag."
    ),
    (
        "Module_25_Final_Capstone_Polyglot_Enterprise",
        "Enterprise Polyglot Persistence Platform Capstone",
        "Multi-Database Enterprise Polyglot E-Commerce Architecture",
        "Transactional Outbox pattern, CDC event streaming, Redis cache-aside, columnar analytics, and vector/full-text search",
        "Integrate two disparate databases using a single application script.",
        "Build the end-to-end Enterprise Polyglot Platform: PostgreSQL transactional source of truth, Transactional Outbox CDC event relay, Redis cache-aside & spend leaderboard, and DuckDB analytical reporting.",
        "Implement a distributed saga orchestrator managing cross-engine eventual consistency with compensating transactions upon downstream failure."
    ),
]

for folder, title, proj_title, tech_stack, t1, t2, t3 in MODULES_PROJECT_DATA:
    target_path = root / folder / "PROJECT_GUIDE.md"
    content = f'''# {folder.replace("_", " ")}: Project Guide

## 📌 Project Overview: {proj_title}

This comprehensive guide walks you step-by-step through building the project for **{title}**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **{tech_stack}**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | {t1} |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | {t2} |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | {t3} |

---

## 1. Architectural Blueprint & Data Flow

```text
       ┌────────────────────────────────────────────────────────┐
       │                   Application Layer                    │
       └───────────────────────────┬────────────────────────────┘
                                   │
              ┌────────────────────┴───────────────────┐
              │                                        │
     ┌────────▼──────────┐                   ┌─────────▼─────────┐
     │  Track A (Model)  │                   │  Track B (Live)   │
     │ Pure-Python Engine│                   │ Real Driver / DB  │
     │ Internal Mechanics│                   │ Production Engine │
     └────────┬──────────┘                   └─────────┬─────────┘
              │                                        │
              └────────────────────┬───────────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │   Reconciliation Test     │
                     │  Validates Shared Semantics│
                     └───────────────────────────┘
```

---

## 2. Directory Structure & Key Files

```text
{folder}/
├── README.md                                 # Core theory, diagrams, and operational syllabus
├── PROJECT_GUIDE.md                          # This 3-tier guided project specification
├── TROUBLESHOOTING_AND_EDGE_CASES.md         # Production error signatures and debugging runbooks
├── SELF_ASSESSMENT_AND_CHALLENGES.md         # 10 diagnostic questions + coding challenges
├── starter/                                  # Skeleton code with exercises and hints
└── project_solution/                         # Reference implementations & full test suites
    ├── conftest.py                           # Pytest fixtures and isolated configuration
    ├── *_engine.py                           # Track A: In-memory reference engine
    ├── test_*_engine.py                      # Track A verification tests
    ├── *_live.py                             # Track B: Real driver & client operations
    └── test_*_live.py                        # Track B integration & reconciliation tests
```

---

## 3. Step-by-Step Implementation Roadmap

### Phase 1: Environment & Setup
1. Verify required Python packages are installed: `pip install -e .`
2. If working with live database engines, ensure local services are running via Docker:
   ```bash
   docker compose up -d
   ```
3. Run existing baseline tests to verify environment health:
   ```bash
   pytest {folder} -v
   ```

### Phase 2: Building Core Capabilities (Tier 1 & 2)
1. Complete the starter exercises in `starter/`.
2. Ensure all unit tests pass with zero assertion failures.
3. Validate operational behaviors against Track B live implementations.

### Phase 3: Architect Stretch (Tier 3)
1. Implement the advanced stretch challenge specified in Tier 3.
2. Add dedicated test cases verifying boundary conditions, concurrency limits, and failure recovery.
3. Profile execution performance and record latency/throughput improvements.

---

## 4. Verification & Self-Check Checklist

- [ ] All Track A unit tests pass: `pytest {folder}/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest {folder}/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.
'''
    target_path.write_text(content, encoding="utf-8")

print(f"Generated {len(MODULES_PROJECT_DATA)} PROJECT_GUIDE.md files successfully.")
