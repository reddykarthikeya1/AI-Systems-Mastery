#!/usr/bin/env python3
"""Generates all_175_modules_data.json with high-precision queries and top-tier channels."""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# Custom curation mapping per course and module
# Each course has tailored queries targeting world-class creators
CURATION_MAP = {
    # COURSE 01
    "01_Advanced_Python": {
        "title": "Course 01: Advanced Python & Systems Mastery",
        "subtitle": "Language Internals, Concurrency, CPython Bytecode & High-Performance Microservices",
        "defaults": ["ArjanCodes", "mCoding", "Corey Schafer", "freeCodeCamp", "Amigoscode"],
        "modules": {
            "Module_00_Environment_Tooling_Workflow": {
                "name": "Module 00: Environment, uv, ruff & Modern Tooling",
                "query": "Astral uv python package manager tutorial",
                "authors": ["ArjanCodes", "mCoding", "Christopher Trudeau"],
                "focus": "Modern high-speed Rust-based Python packaging, lockfiles, and dependency resolution with uv."
            },
            "Module_01_Python_Fundamentals": {
                "name": "Module 01: Python Fundamentals, Types & Control Flow",
                "query": "Corey Schafer Python Tutorial Integers and Floats Working with Numeric Data",
                "authors": ["Corey Schafer", "freeCodeCamp"],
                "focus": "Primitive types, arbitrary precision integers, memory allocation, and numeric semantics."
            },
            "Module_02_Functions_Scopes_Closures": {
                "name": "Module 02: Functions, Scopes, Closures & LEGB Rule",
                "query": "Corey Schafer Python Tutorial Variable Scope LEGB rule",
                "authors": ["Corey Schafer", "ArjanCodes", "mCoding"],
                "focus": "Local, Enclosing, Global, and Built-in scope hierarchies, closure cells, and nonlocal bindings."
            },
            "Module_03_Data_Structures_Collections": {
                "name": "Module 03: Data Structures, Collections & Hash Table Internals",
                "query": "mCoding How dictionaries work in Python",
                "authors": ["mCoding", "James Murphy", "ArjanCodes"],
                "focus": "Compact dict layout, hash table open addressing, probing algorithms, and collision handling."
            },
            "Module_04_Deep_OOP": {
                "name": "Module 04: Deep OOP, Inheritance, MRO & Dunder Protocols",
                "query": "Corey Schafer Python OOP Tutorial 6 Property Decorators",
                "authors": ["Corey Schafer", "ArjanCodes"],
                "focus": "C3 Linearization, Method Resolution Order (MRO), properties, and special dunder methods."
            },
            "Module_05_Decorators_Generators_Context_Managers": {
                "name": "Module 05: Decorators, Generators & Context Managers",
                "query": "Corey Schafer Python Tutorial Decorators Dynamically Alter",
                "authors": ["Corey Schafer", "ArjanCodes", "mCoding"],
                "focus": "First-class functions, parameter wrapping, generator lazy evaluation, and the with protocol."
            },
            "Module_06_Error_Handling_Logging": {
                "name": "Module 06: Enterprise Error Handling & Resilient Logging",
                "query": "Corey Schafer Python Logging Basics Advanced",
                "authors": ["Corey Schafer", "ArjanCodes"],
                "focus": "Structured exception hierarchies, tracebacks, logging handlers, formatters, and rotation."
            },
            "Module_07_Files_Data_Formats_Serialization": {
                "name": "Module 07: Modern File I/O, Data Formats & Serialization",
                "query": "Corey Schafer Python Tutorial Working with JSON Data",
                "authors": ["Corey Schafer", "ArjanCodes"],
                "focus": "File descriptors, atomic write operations, JSON parsing, and binary protocol buffers."
            },
            "Module_08_Testing_Quality_Assurance": {
                "name": "Module 08: Modern Testing & QA (Pytest & Hypothesis)",
                "query": "ArjanCodes How to test your code with pytest",
                "authors": ["ArjanCodes", "mCoding", "freeCodeCamp"],
                "focus": "Pytest fixtures, parametrized test cases, monkeypatching, and property-based verification."
            },
            "Module_09_Concurrency_Threading_Multiprocessing": {
                "name": "Module 09: Concurrency (Threading, Multiprocessing & GIL)",
                "query": "Corey Schafer Python Multiprocessing Tutorial",
                "authors": ["Corey Schafer", "ArjanCodes", "mCoding"],
                "focus": "Overcoming the Global Interpreter Lock (GIL), process IPC, queues, and pool executors."
            },
            "Module_10_Concurrency_Asyncio": {
                "name": "Module 10: Concurrency (Modern Asyncio & TaskGroups)",
                "query": "ArjanCodes Next Level Asyncio in Python",
                "authors": ["ArjanCodes", "mCoding"],
                "focus": "Event loop reactor pattern, non-blocking coroutines, TaskGroups, and structured concurrency."
            },
            "Module_11_Networking_Sockets_HTTP": {
                "name": "Module 11: Networking, Raw Sockets & HTTP Protocols",
                "query": "Corey Schafer Python Socket Programming Tutorial",
                "authors": ["Corey Schafer", "Tech With Tim"],
                "focus": "TCP stream sockets, packet buffering, framing, and low-level protocol parsing."
            },
            "Module_12_Python_Internals_Bytecode_Memory": {
                "name": "Module 12: CPython Bytecode, AST & Memory Architecture",
                "query": "mCoding What is Python bytecode",
                "authors": ["mCoding", "James Murphy", "Anthony Shaw"],
                "focus": "Disassembling code with dis, opcode stack evaluation, and the CPython interpreter loop."
            },
            "Module_13_FastAPI_ASGI_Architecture": {
                "name": "Module 13: High-Performance Backend with FastAPI & ASGI",
                "query": "ArjanCodes FastAPI tutorial modern python",
                "authors": ["ArjanCodes", "freeCodeCamp", "Amigoscode"],
                "focus": "Asynchronous Server Gateway Interface (ASGI), Starlette concurrency, and Uvicorn workers."
            },
            "Module_14_Pydantic_V2_Validation_Routing": {
                "name": "Module 14: Robust Data Modeling with Pydantic V2",
                "query": "ArjanCodes Pydantic V2 Python tutorial",
                "authors": ["ArjanCodes", "mCoding"],
                "focus": "Rust-powered pydantic-core validation, field validators, serialization, and type safety."
            },
            "Module_15_SQLAlchemy_Alembic_Database": {
                "name": "Module 15: Database Architecture with SQLAlchemy 2.0 & Alembic",
                "query": "Amigoscode SQLAlchemy 2.0 tutorial python",
                "authors": ["Amigoscode", "freeCodeCamp", "ArjanCodes"],
                "focus": "Declarative mapping, async sessions, relationship eager-loading, and schema migration chains."
            },
            "Module_16_Authentication_Authorization_Security": {
                "name": "Module 16: Enterprise API Security (JWT & RBAC)",
                "query": "ArjanCodes Python API security JWT authentication",
                "authors": ["ArjanCodes", "Amigoscode", "freeCodeCamp"],
                "focus": "Asymmetric RSA/HMAC tokens, OAuth2 password flows, bcrypt hashing, and scopes."
            },
            "Module_17_Advanced_FastAPI_WebSockets_DI": {
                "name": "Module 17: Advanced FastAPI (WebSockets & Dependency Injection)",
                "query": "FastAPI WebSockets tutorial python",
                "authors": ["ArjanCodes", "Tech With Tim", "freeCodeCamp"],
                "focus": "Bidirectional persistent streaming, custom ASGI middlewares, and hierarchical dependency trees."
            },
            "Module_18_Distributed_Systems_Task_Queues_Streaming": {
                "name": "Module 18: Task Queues & Streaming with Celery and Redis",
                "query": "ArjanCodes Celery Redis task queue python",
                "authors": ["ArjanCodes", "freeCodeCamp"],
                "focus": "Asynchronous job queues, worker prefork pools, dead-letter exchanges, and consumer groups."
            },
            "Module_19_Containerization_CICD_Deployment": {
                "name": "Module 19: Containerization, Docker & Production CI/CD",
                "query": "Docker Python tutorial deployment freeCodeCamp",
                "authors": ["freeCodeCamp", "TechWorld with Nana", "ArjanCodes"],
                "focus": "Multi-stage Docker builds, non-root user security, health checks, and GitHub Actions."
            },
            "Module_20_Performance_Optimization_Profiling_Caching": {
                "name": "Module 20: Performance Engineering & Redis Multi-Tier Caching",
                "query": "mCoding Python profiling speed optimization",
                "authors": ["mCoding", "ArjanCodes"],
                "focus": "Deterministic cProfile analysis, flame graphs, and cache-aside patterns with Redis."
            },
            "Module_21_Metaprogramming_Descriptors_Memory": {
                "name": "Module 21: Descriptors, Metaclasses & Zero-Copy Memory",
                "query": "mCoding Python descriptors explained",
                "authors": ["mCoding", "James Murphy", "ArjanCodes"],
                "focus": "__get__ and __set__ descriptor protocols, metaclass class factory creation, and memoryview."
            },
            "Module_22_CPython_Internals_Rust_PyO3_Extensions": {
                "name": "Module 22: CPython Internals & Native Rust Extensions (PyO3)",
                "query": "Rust PyO3 Python native extensions tutorial",
                "authors": ["mCoding", "No Boilerplate", "ArjanCodes"],
                "focus": "Calling high-speed compiled Rust from Python, PyO3 bindings, and GIL release."
            },
            "Module_23_Strict_Typing_Packaging_Publishing": {
                "name": "Module 23: Strict Typing, Mypy & Modern Packaging",
                "query": "ArjanCodes Python type hints mypy typing",
                "authors": ["ArjanCodes", "mCoding"],
                "focus": "Generics, TypeVars, Protocol duck-typing, ParamSpec, and pyproject.toml distribution."
            },
            "Module_24_Data_Engineering_Polars_Playwright": {
                "name": "Module 24: High-Performance Data Engineering (Polars & DuckDB)",
                "query": "Polars Python tutorial high performance dataframe",
                "authors": ["ArjanCodes", "freeCodeCamp", "Luke Barousse"],
                "focus": "Columnar Arrow memory model, streaming execution engines, and headless automation."
            },
            "Module_25_AI_Engineering_LLM_Integration": {
                "name": "Module 25: AI Engineering (Vector Embeddings & Tool Calling)",
                "query": "Building LLM applications Python LangChain OpenAI",
                "authors": ["freeCodeCamp", "Prompt Engineering", "ArjanCodes"],
                "focus": "Tokenization, cosine similarity vector search, structured JSON outputs, and function calling."
            },
            "Module_26_Final_Capstone_Project": {
                "name": "Module 26: Enterprise Capstone (Distributed Platform)",
                "query": "Full stack Python microservices architecture enterprise",
                "authors": ["ArjanCodes", "freeCodeCamp", "ByteByteGo"],
                "focus": "End-to-end event-driven architecture, CQRS, resiliency patterns, and production deployment."
            }
        }
    },

    # COURSE 02
    "02_Data_Structures_and_Algorithms": {
        "title": "Course 02: Data Structures & Algorithms Mastery",
        "subtitle": "Memory Hierarchies, Asymptotic Bounds, Graph Theory & Dynamic Programming",
        "defaults": ["NeetCode", "Abdul Bari", "William Fiset", "freeCodeCamp"],
        "modules": {
            "Module_01_Complexity_Analysis_and_Memory_Layout": {
                "name": "Module 01: Complexity Analysis & Memory Layout",
                "query": "Abdul Bari Big O notation time complexity",
                "authors": ["Abdul Bari", "NeetCode", "freeCodeCamp"],
                "focus": "Big-O, Omega, Theta asymptotic notation, cache lines, and spatial/temporal locality."
            },
            "Module_02_Arrays_Dynamic_Arrays_and_Strings": {
                "name": "Module 02: Arrays, Dynamic Arrays & Two-Pointer Patterns",
                "query": "NeetCode Dynamic Array design leetcode",
                "authors": ["NeetCode", "Abdul Bari"],
                "focus": "Amortized resizing complexity, sliding windows, and in-place string manipulation."
            },
            "Module_03_Linked_Lists_and_Pointer_Manipulation": {
                "name": "Module 03: Linked Lists & Pointer Manipulation",
                "query": "Abdul Bari Linked List data structure tutorial",
                "authors": ["Abdul Bari", "NeetCode", "freeCodeCamp"],
                "focus": "Singly/doubly linked chains, cycle detection (Floyd's algorithm), and pointer reversal."
            },
            "Module_04_Stacks_Queues_and_Monotonic_Structures": {
                "name": "Module 04: Stacks, Queues & Monotonic Structures",
                "query": "NeetCode Monotonic Stack Next Greater Element",
                "authors": ["NeetCode", "Abdul Bari", "William Fiset"],
                "focus": "LIFO/FIFO guarantees, circular ring buffers, and O(N) monotonic stack invariants."
            },
            "Module_05_Hash_Tables_and_Collision_Resolution": {
                "name": "Module 05: Hash Tables & Collision Resolution",
                "query": "Abdul Bari Hashing technique collision resolution",
                "authors": ["Abdul Bari", "William Fiset", "NeetCode"],
                "focus": "MurmurHash, SipHash, open addressing, linear probing, and Robin Hood hashing."
            },
            "Module_06_Trees_Binary_Search_Trees_and_Self_Balancing": {
                "name": "Module 06: Trees, BSTs & Self-Balancing AVL/Red-Black",
                "query": "Abdul Bari AVL Tree insertion rotation",
                "authors": ["Abdul Bari", "William Fiset", "NeetCode"],
                "focus": "Tree traversals (in/pre/post/level), BST search invariants, and AVL rotations."
            },
            "Module_07_Heaps_Priority_Queues_and_TopK_Patterns": {
                "name": "Module 07: Heaps, Priority Queues & Top-K Patterns",
                "query": "Abdul Bari Heap Sort insertion deletion",
                "authors": ["Abdul Bari", "NeetCode", "William Fiset"],
                "focus": "Complete binary trees in contiguous memory, heapify sift-up/down, and median finding."
            },
            "Module_08_Graph_Algorithms_Traversals_and_DAGs": {
                "name": "Module 08: Graph Traversals, BFS/DFS & Topological Sort",
                "query": "Abdul Bari Graph traversal BFS DFS",
                "authors": ["Abdul Bari", "William Fiset", "NeetCode"],
                "focus": "Adjacency lists/matrices, Kahn's topological sort, and cycle detection in DAGs."
            },
            "Module_09_Graph_Algorithms_Shortest_Paths_and_MST": {
                "name": "Module 09: Shortest Paths (Dijkstra, Bellman-Ford) & MST",
                "query": "Abdul Bari Dijkstra algorithm shortest path",
                "authors": ["Abdul Bari", "William Fiset", "NeetCode"],
                "focus": "Greedy relaxation, Prim's and Kruskal's Minimum Spanning Tree algorithms."
            },
            "Module_10_Dynamic_Programming_1D_and_Sequence_Patterns": {
                "name": "Module 10: 1D Dynamic Programming & Sequence Patterns",
                "query": "NeetCode Dynamic Programming 1D pattern",
                "authors": ["NeetCode", "Abdul Bari", "freeCodeCamp"],
                "focus": "Optimal substructure, overlapping subproblems, memoization vs tabulation."
            },
            "Module_11_Dynamic_Programming_2D_Knapsack_and_Grids": {
                "name": "Module 11: 2D Dynamic Programming (Knapsack & Grid Paths)",
                "query": "Abdul Bari 0/1 Knapsack Problem Dynamic Programming",
                "authors": ["Abdul Bari", "NeetCode", "freeCodeCamp"],
                "focus": "Bounded/unbounded knapsack, state-space compression, and longest common subsequence."
            },
            "Module_12_Greedy_Algorithms_and_Interval_Scheduling": {
                "name": "Module 12: Greedy Algorithms & Interval Scheduling",
                "query": "Abdul Bari Greedy Method Knapsack Job Sequencing",
                "authors": ["Abdul Bari", "NeetCode", "William Fiset"],
                "focus": "Matroid theory, greedy choice property, activity selection, and Huffman encoding."
            },
            "Module_13_Backtracking_and_Constraint_Satisfaction": {
                "name": "Module 13: Backtracking & Constraint Satisfaction",
                "query": "Abdul Bari N Queen Problem Backtracking",
                "authors": ["Abdul Bari", "NeetCode", "William Fiset"],
                "focus": "State-space tree exploration, pruning branches, Sudoku solver, and N-Queens."
            },
            "Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree": {
                "name": "Module 14: Advanced Structures: Trie, Union-Find & Segment Tree",
                "query": "NeetCode Trie data structure design add search",
                "authors": ["NeetCode", "Abdul Bari", "William Fiset"],
                "focus": "Prefix retrieval, Disjoint Set Union (DSU) with path compression, and range queries."
            },
            "Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU": {
                "name": "Module 15: Systems-Level Structures: SkipLists, Bloom Filters & LRU",
                "query": "ByteByteGo Bloom Filter system design",
                "authors": ["ByteByteGo", "Hussein Nasser", "NeetCode"],
                "focus": "Probabilistic membership tests, false positive bounds, and O(1) LRU eviction caches."
            },
            "Module_16_String_Algorithms_and_Pattern_Matching": {
                "name": "Module 16: String Algorithms & Substring Pattern Matching",
                "query": "Abdul Bari KMP algorithm substring pattern matching",
                "authors": ["Abdul Bari", "NeetCode", "William Fiset"],
                "focus": "Knuth-Morris-Pratt (KMP) failure functions, Rabin-Karp rolling hashes, and Z-algorithm."
            },
            "Module_17_Network_Flow_and_Matching": {
                "name": "Module 17: Network Flow & Bipartite Matching",
                "query": "William Fiset Ford Fulkerson max flow network flow",
                "authors": ["William Fiset", "Abdul Bari", "Michael Sambol"],
                "focus": "Residual capacity graphs, Ford-Fulkerson, Edmonds-Karp, and max-flow min-cut theorem."
            }
        }
    },

    # COURSE 03
    "03_Databases_and_Storage_Engines": {
        "title": "Course 03: Databases & Storage Engine Architecture",
        "subtitle": "Relational Internals, Columnar OLAP, Distributed Consensus & LSM Engines",
        "defaults": ["Hussein Nasser", "ByteByteGo", "CMU Database Group", "IBM Technology"],
        "modules": {
            "Module_01_Storage_Theory_ACID_Relational_Model": {
                "name": "Module 01: Storage Theory, ACID & Relational Foundation",
                "query": "Hussein Nasser Database ACID properties isolation levels",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Atomicity, Consistency, Isolation anomalies (dirty reads, phantom reads), and Durability."
            },
            "Module_02_Modern_SQL_Mastery_Advanced_Queries": {
                "name": "Module 02: Advanced SQL: Window Functions, CTEs & Joins",
                "query": "Hussein Nasser Advanced SQL window functions CTEs",
                "authors": ["Hussein Nasser", "freeCodeCamp"],
                "focus": "Recursive Common Table Expressions, PARTITION BY, sliding windows, and join algorithms."
            },
            "Module_03_Embedded_Databases_SQLite_WAL": {
                "name": "Module 03: Embedded Databases: SQLite Architecture & WAL",
                "query": "Hussein Nasser SQLite architecture Write Ahead Log WAL",
                "authors": ["Hussein Nasser", "CMU Database Group"],
                "focus": "B-Tree paging, rollbacks, and concurrent readers via Write-Ahead Logging."
            },
            "Module_04_PostgreSQL_Core_Advanced_Types": {
                "name": "Module 04: PostgreSQL Core Architecture & Advanced Types",
                "query": "Hussein Nasser PostgreSQL Architecture processes memory",
                "authors": ["Hussein Nasser", "freeCodeCamp"],
                "focus": "Postmaster process hierarchy, shared buffers, work_mem, JSONB, and TOAST storage."
            },
            "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN": {
                "name": "Module 05: PostgreSQL MVCC, Indexing & EXPLAIN ANALYZE",
                "query": "Hussein Nasser Postgres MVCC EXPLAIN ANALYZE index",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Multi-Version Concurrency Control (xmin/xmax), B-Tree vs GiST vs GIN, and vacuuming."
            },
            "Module_06_MySQL_MariaDB_InnoDB_Replication": {
                "name": "Module 06: MySQL & MariaDB Architecture: InnoDB & Replication",
                "query": "Hussein Nasser MySQL InnoDB engine architecture replication",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Clustered indexes, redo logs, binlogs, undo logs, and semi-sync replication topologies."
            },
            "Module_07_Oracle_Database_Architecture_SGA_PGA": {
                "name": "Module 07: Oracle Architecture: SGA, PGA & Storage Subsystems",
                "query": "Oracle Database architecture SGA PGA memory background processes",
                "authors": ["Oracle Learning", "Hussein Nasser", "Knowledge Powerhouse"],
                "focus": "System Global Area (Buffer Cache, Shared Pool), Program Global Area, and DBWR/LGWR."
            },
            "Module_08_Oracle_PLSQL_Packages_Triggers": {
                "name": "Module 08: Oracle PL/SQL, Packages, Triggers & Cursors",
                "query": "Oracle PL SQL tutorial packages stored procedures triggers",
                "authors": ["Oracle Learning", "freeCodeCamp"],
                "focus": "Compiled server-side logic, autonomous transactions, packages, and compound triggers."
            },
            "Module_09_Oracle_RAC_DataGuard_GoldenGate": {
                "name": "Module 09: Oracle High Availability: RAC, Data Guard & GoldenGate",
                "query": "Oracle Data Guard RAC GoldenGate high availability architecture",
                "authors": ["Oracle Learning", "Hussein Nasser"],
                "focus": "Real Application Clusters cache fusion, physical standby recovery, and change data capture."
            },
            "Module_10_MongoDB_Document_Modeling_BSON": {
                "name": "Module 10: MongoDB Document Modeling & BSON Internals",
                "query": "Hussein Nasser MongoDB document modeling BSON schema",
                "authors": ["Hussein Nasser", "MongoDB"],
                "focus": "Embedded vs referenced relationships, WiredTiger engine, and BSON byte layout."
            },
            "Module_11_MongoDB_Aggregations_Replicas_Sharding": {
                "name": "Module 11: MongoDB Aggregation Pipeline, Replication & Sharding",
                "query": "Hussein Nasser MongoDB replication sharding architecture",
                "authors": ["Hussein Nasser", "ByteByteGo", "MongoDB"],
                "focus": "Oplog replication, Raft-like elections, mongos routing, and chunk rebalancing."
            },
            "Module_12_Redis_Data_Structures_Persistence": {
                "name": "Module 12: Redis In-Memory Architecture & Persistence",
                "query": "Hussein Nasser Redis architecture data structures persistence RDB AOF",
                "authors": ["Hussein Nasser", "ByteByteGo", "Fireship"],
                "focus": "Single-threaded event loop, string/hash/zset memory encoding, and RDB/AOF durability."
            },
            "Module_13_Redis_Sentinel_Clustering_Lua": {
                "name": "Module 13: Redis Sentinel, Clustering & Lua Scripting",
                "query": "Hussein Nasser Redis Cluster Sentinel replication",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Automated failover with Sentinel, 16384 hash slots in Redis Cluster, and atomic Lua execution."
            },
            "Module_14_Apache_Cassandra_Masterless_Ring": {
                "name": "Module 14: Cassandra & ScyllaDB: Masterless Ring & Murmur3",
                "query": "Hussein Nasser Apache Cassandra architecture masterless ring consistent hashing",
                "authors": ["Hussein Nasser", "ByteByteGo", "DataStax"],
                "focus": "Dynamo-style peer-to-peer ring, token ranges, gossip protocol, and tunable consistency (QUORUM)."
            },
            "Module_15_LSM_Trees_Compaction_DynamoDB": {
                "name": "Module 15: LSM-Trees, SSTables, Compaction & DynamoDB",
                "query": "Hussein Nasser LSM Tree vs B-Tree database storage engine",
                "authors": ["Hussein Nasser", "ByteByteGo", "CMU Database Group"],
                "focus": "Append-only commit logs, in-memory MemTables, immutable SSTables, and Leveled Compaction."
            },
            "Module_16_Neo4j_Graph_Databases_Cypher": {
                "name": "Module 16: Neo4j & Graph Databases: Index-Free Adjacency",
                "query": "Neo4j graph database architecture Cypher tutorial",
                "authors": ["Neo4j", "freeCodeCamp", "Fireship"],
                "focus": "Direct double-linked pointer traversal, property graph modeling, and Cypher pattern matching."
            },
            "Module_17_Columnar_OLAP_DuckDB_ClickHouse": {
                "name": "Module 17: Columnar OLAP: DuckDB, ClickHouse & Parquet",
                "query": "Hussein Nasser Columnar databases OLAP ClickHouse DuckDB",
                "authors": ["Hussein Nasser", "ByteByteGo", "ClickHouse"],
                "focus": "Row vs columnar storage, SIMD vectorized execution, dictionary encoding, and run-length compression."
            },
            "Module_18_Analytics_Engineering_Dimensional_Modeling_Pipelines": {
                "name": "Module 18: Analytics Engineering: Star Schemas & dbt Pipelines",
                "query": "Dimensional Modeling data warehouse star schema Kimbal",
                "authors": ["Seattle Data Guy", "freeCodeCamp"],
                "focus": "Kimball fact and dimension tables, slowly changing dimensions (SCD), and ELT transformations."
            },
            "Module_19_Search_Engines_Elasticsearch_Lucene": {
                "name": "Module 19: Search Engines: Apache Lucene & BM25 Relevance",
                "query": "Hussein Nasser Elasticsearch Apache Lucene inverted index BM25",
                "authors": ["Hussein Nasser", "ByteByteGo", "freeCodeCamp"],
                "focus": "Inverted index posting lists, term frequencies, inverse document frequency, and BM25 scoring."
            },
            "Module_20_AI_Vector_Databases_pgvector_Qdrant": {
                "name": "Module 20: AI Vector Databases: pgvector, Qdrant & HNSW",
                "query": "Hussein Nasser Vector databases pgvector embeddings HNSW",
                "authors": ["Hussein Nasser", "ByteByteGo", "IBM Technology"],
                "focus": "High-dimensional embedding representations, Cosine/Dot product similarity, and HNSW graph traversal."
            },
            "Module_21_Storage_Engine_Internals_BPlus_Trees": {
                "name": "Module 21: Storage Engine Internals: Buffer Pools & B+ Trees",
                "query": "Hussein Nasser B-tree vs B+ tree in Database Systems",
                "authors": ["Hussein Nasser", "CMU Database Group", "ByteByteGo"],
                "focus": "Slotted page layout, disk block management, buffer pool replacement (LRU-K), and node splitting."
            },
            "Module_22_Query_Optimization_CBO_Index_Tuning": {
                "name": "Module 22: Query Optimization, Cost Models & Physical Joins",
                "query": "Andy Pavlo Query Optimization CMU Database",
                "authors": ["CMU Database Group", "Hussein Nasser", "ByteByteGo"],
                "focus": "Relational algebra transformations, cardinality estimation, Hash Join vs Nested Loop vs Merge Join."
            },
            "Module_23_Transactions_Isolation_Consensus_Raft": {
                "name": "Module 23: Transactions, Two-Phase Commit & Distributed Consensus",
                "query": "Hussein Nasser Two Phase Commit 2PC distributed transactions",
                "authors": ["Hussein Nasser", "ByteByteGo", "Martin Kleppmann"],
                "focus": "Serializability, Snapshot Isolation anomalies, 2PC blocking limitations, and Raft consensus logs."
            },
            "Module_24_Production_DBRE_Backups_Migrations_HA": {
                "name": "Module 24: Database Reliability Engineering (DBRE) & Migrations",
                "query": "Hussein Nasser Zero Downtime Database Migrations",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Point-in-time recovery (PITR), logical vs physical backups, and expand/contract schema patterns."
            },
            "Module_25_Final_Capstone_Polyglot_Enterprise": {
                "name": "Module 25: Capstone: Polyglot Persistence Architecture",
                "query": "ByteByteGo Polyglot Persistence microservices database design",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Combining Relational, In-Memory, Search, and Vector engines with Change Data Capture (Debezium)."
            }
        }
    },

    # COURSE 04
    "04_System_Design_and_Distributed_Systems": {
        "title": "Course 04: System Design & Distributed Systems Mastery",
        "subtitle": "High-Throughput Scalability, Event-Driven Architectures & Production Case Studies",
        "defaults": ["ByteByteGo", "Hussein Nasser", "Gaurav Sen", "IBM Technology"],
        "modules": {
            "Module_00_System_Design_Fundamentals_Interview_Playbook": {
                "name": "Module 00: System Design Fundamentals & Interview Playbook",
                "query": "ByteByteGo System Design interview framework",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "4-step interview framework, functional vs non-functional requirements, and back-of-the-envelope estimation."
            },
            "Module_01_Physics_of_Scalability_Capacity_Math": {
                "name": "Module 01: Physics of Scalability & Latency Hierarchy",
                "query": "ByteByteGo Latency numbers every programmer should know",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "L1/L2/RAM/SSD/Network latency numbers, throughput calculations, and bandwidth ceilings."
            },
            "Module_02_Network_Protocols_Transport_API_Paradigms": {
                "name": "Module 02: Network Protocols: HTTP/2, gRPC & WebSockets",
                "query": "Hussein Nasser REST vs gRPC vs GraphQL vs WebSockets",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "Multiplexing, TCP head-of-line blocking, Protobuf binary encoding, and full-duplex communication."
            },
            "Module_03_Edge_Infrastructure_Reverse_Proxies": {
                "name": "Module 03: Edge Infrastructure, CDNs & API Gateways",
                "query": "Hussein Nasser Reverse Proxy vs Forward Proxy API Gateway",
                "authors": ["Hussein Nasser", "ByteByteGo"],
                "focus": "SSL termination, Edge caching (Cloudflare/Fastly), rate limiting, and request routing."
            },
            "Module_04_Load_Balancing_Algorithms_Health_Probes": {
                "name": "Module 04: Load Balancing Algorithms & Health Probes",
                "query": "ByteByteGo Load Balancers system design",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "L4 vs L7 balancing, Round Robin, Weighted Least Connections, IP hash, and passive/active probes."
            },
            "Module_05_SOLID_Principles_Clean_Architecture": {
                "name": "Module 05: SOLID Principles & Clean Architecture",
                "query": "ArjanCodes SOLID principles in Python software architecture",
                "authors": ["ArjanCodes", "freeCodeCamp"],
                "focus": "Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion."
            },
            "Module_06_GoF_Design_Patterns_Scalable_Systems": {
                "name": "Module 06: GoF Design Patterns in Scalable Backends",
                "query": "ArjanCodes Design patterns in Python Gang of Four",
                "authors": ["ArjanCodes", "freeCodeCamp", "Fireship"],
                "focus": "Factory, Singleton, Adapter, Strategy, Observer, and Decorator implementations."
            },
            "Module_07_LLD_State_Machines_Scheduling_Elevator_Parking": {
                "name": "Module 07: Low-Level Design: Elevator LOOK Scheduling",
                "query": "Gaurav Sen Elevator System Design low level design",
                "authors": ["Gaurav Sen", "Concept Coding"],
                "focus": "State machine transitions, SCAN/LOOK disk-scheduling algorithms applied to multi-car systems."
            },
            "Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting": {
                "name": "Module 08: Low-Level Design: Rate Limiting & Debt Simplification",
                "query": "Gaurav Sen Rate Limiter system design Leaky Token Bucket",
                "authors": ["Gaurav Sen", "ByteByteGo", "Hussein Nasser"],
                "focus": "Token Bucket, Leaky Bucket, Sliding Window Log, and graph debt simplification algorithms."
            },
            "Module_09_Consistent_Hashing_Distributed_Partitioning": {
                "name": "Module 09: Consistent Hashing & Distributed Partitioning",
                "query": "ByteByteGo Consistent Hashing system design",
                "authors": ["ByteByteGo", "Hussein Nasser", "Gaurav Sen"],
                "focus": "Hash rings, virtual nodes, load skew reduction, and minimal remapping during node failures."
            },
            "Module_10_Unique_Distributed_ID_Generation_Snowflake": {
                "name": "Module 10: Unique Distributed ID Generation (Twitter Snowflake)",
                "query": "ByteByteGo Distributed ID generator Twitter Snowflake",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "64-bit integer packing: epoch timestamp, datacenter ID, machine ID, and sequence counter."
            },
            "Module_11_Distributed_Caching_Stampede_Prevention": {
                "name": "Module 11: Distributed Caching & Cache Stampede Prevention",
                "query": "ByteByteGo Caching strategies cache stampede cache penetration",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Write-through, write-back, probabilistic early expiration (XFetch), and mutex locking."
            },
            "Module_12_Probabilistic_Data_Structures": {
                "name": "Module 12: Probabilistic Data Structures in Large-Scale Systems",
                "query": "ByteByteGo Bloom filter HyperLogLog Count Min Sketch",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Counting unique elements via HyperLogLog, frequency estimation with Count-Min Sketch."
            },
            "Module_13_Distributed_Messaging_Event_Streaming_Queues": {
                "name": "Module 13: Distributed Messaging & Commit Logs (Kafka vs RabbitMQ)",
                "query": "ByteByteGo Kafka vs RabbitMQ message queue commit log",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Partition offsets, log compaction, consumer groups, and backpressure handling."
            },
            "Module_14_Distributed_URL_Shortener_TinyURL": {
                "name": "Module 14: System Design Case Study: Distributed URL Shortener (TinyURL)",
                "query": "ByteByteGo Design TinyURL URL shortener system design",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "Base62 encoding, pre-generated key generation service (KGS), and high read/write ratio caching."
            },
            "Module_15_RealTime_Chat_Presence_System_Discord": {
                "name": "Module 15: System Design Case Study: Real-Time Chat & Presence (Discord)",
                "query": "ByteByteGo Design Discord chat app system design",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "WebSocket session routing, distributed presence heartbeats, and Cassandra message storage."
            },
            "Module_16_Social_Media_Newsfeed_Recommendation_TwoTower": {
                "name": "Module 16: System Design Case Study: Newsfeed & Recommendation (Twitter)",
                "query": "ByteByteGo Design Twitter News Feed system design",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "Fanout-on-write vs fanout-on-read, celebrity problem, and two-tower ranking models."
            },
            "Module_17_Geospatial_Ride_Sharing_Dispatch_Uber": {
                "name": "Module 17: System Design Case Study: Geospatial Ride-Sharing (Uber/Lyft)",
                "query": "ByteByteGo Design Uber ride sharing geospatial H3 QuadTree",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "Geohashing, Uber H3 hexagonal spatial indexing, and driver matching optimization."
            },
            "Module_18_Video_Ingestion_Streaming_YouTube_Netflix": {
                "name": "Module 18: System Design Case Study: Video Streaming (YouTube/Netflix)",
                "query": "ByteByteGo Design YouTube or Netflix video streaming CDN",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Chunking, adaptive bitrate streaming (HLS/DASH), DAG transcoding pipelines, and edge CDNs."
            },
            "Module_19_Distributed_Web_Crawler_Deduplication_Google": {
                "name": "Module 19: System Design Case Study: Distributed Web Crawler (Google)",
                "query": "ByteByteGo Design Web Crawler system design",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "Frontier queue management, politeness delays, DNS caching, and SimHash fingerprint deduplication."
            },
            "Module_20_Flash_Sale_Inventory_Reservation_Amazon": {
                "name": "Module 20: System Design Case Study: Flash Sale & Inventory Reservation",
                "query": "ByteByteGo Flash Sale system design concurrency inventory",
                "authors": ["ByteByteGo", "Concept Coding"],
                "focus": "High concurrency oversell prevention, Redis Lua atomic decrement, and asynchronous checkout queues."
            },
            "Module_21_Vector_Database_HNSW_Index_Milvus": {
                "name": "Module 21: Vector Databases & HNSW Indexing (Milvus/Pinecone)",
                "query": "ByteByteGo Vector Search HNSW system design",
                "authors": ["ByteByteGo", "IBM Technology"],
                "focus": "Hierarchical graph navigation, skip-list intuition in high dimensions, and search Recall@K."
            },
            "Module_22_Distributed_LLM_Serving_PagedAttention_vLLM": {
                "name": "Module 22: Distributed LLM Serving & PagedAttention (vLLM)",
                "query": "vLLM PagedAttention LLM serving architecture",
                "authors": ["Tales Of Tensors", "Umar Jamil", "ByteByteGo"],
                "focus": "Virtual memory paging for GPU KV-caches, continuous batching, and eliminating memory fragmentation."
            },
            "Module_23_Distributed_Transactions_Sagas_Outbox": {
                "name": "Module 23: Distributed Transactions: Sagas & Transactional Outbox",
                "query": "ByteByteGo Saga pattern transactional outbox distributed transactions",
                "authors": ["ByteByteGo", "Hussein Nasser"],
                "focus": "Compensating transactions, choreography vs orchestration, and reliable outbox event publishing."
            },
            "Module_24_Distributed_Consensus_Raft_Vector_Clocks": {
                "name": "Module 24: Distributed Consensus: Raft Protocol & Vector Clocks",
                "query": "Raft consensus algorithm visual explanation",
                "authors": ["ByteByteGo", "Heidi Howard", "Martin Kleppmann"],
                "focus": "Leader election, log replication safety, split-brain mitigation, and Lamport logical clocks."
            },
            "Module_25_Observability_Distributed_Tracing_SRE": {
                "name": "Module 25: Observability, Distributed Tracing & SRE Resilience",
                "query": "ByteByteGo Distributed Tracing OpenTelemetry metrics logs traces",
                "authors": ["ByteByteGo", "IBM Technology"],
                "focus": "W3C trace contexts, span propagation, Prometheus metric scraping, and circuit breakers."
            },
            "Module_26_Capstone_Payment_Gateway_AI_Fraud": {
                "name": "Module 26: Capstone: Enterprise Payment Gateway & AI Fraud Detection",
                "query": "ByteByteGo Design Payment System idempotency Stripe",
                "authors": ["ByteByteGo", "Gaurav Sen"],
                "focus": "Idempotency keys, distributed locks, double-entry ledger bookkeeping, and ML fraud scoring."
            }
        }
    },

    # COURSE 05
    "05_Mathematics_for_ML_and_AI": {
        "title": "Course 05: Mathematics for Machine Learning & Deep Learning",
        "subtitle": "Linear Algebra, Spectral Theory, Multivariable Calculus & Probability",
        "defaults": ["3Blue1Brown", "StatQuest with Josh Starmer", "Steve Brunton", "Khan Academy"],
        "modules": {
            "Module_01_Set_Language_for_Machine_Learning": {
                "name": "Module 01: Set Language & Probability Sample Spaces",
                "query": "3Blue1Brown probability set theory intuition",
                "authors": ["3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Unions, intersections, subsets, sample spaces, and probabilistic events."
            },
            "Module_02_Logic_for_Precise_Reasoning": {
                "name": "Module 02: Mathematical Logic for Precise Reasoning",
                "query": "Propositional logic predicate logic computer science Stanford",
                "authors": ["MIT OpenCourseWare", "CrashCourse"],
                "focus": "Truth tables, implications, quantifiers, contrapositives, and inductive proofs."
            },
            "Module_03_Linear_Systems_and_Geometric_Maps": {
                "name": "Module 03: Linear Systems & Matrix Transformations",
                "query": "3Blue1Brown Linear transformations and matrices Chapter 3",
                "authors": ["3Blue1Brown"],
                "focus": "Geometric interpretation of matrix-vector multiplication as space transformation."
            },
            "Module_04_Vector_Spaces_Bases_and_Rank": {
                "name": "Module 04: Vector Spaces, Span, Bases & Rank",
                "query": "3Blue1Brown Span and basis vectors Essence of linear algebra Chapter 2",
                "authors": ["3Blue1Brown"],
                "focus": "Linear combinations, span, linear independence, dimension, and rank-nullity."
            },
            "Module_05_Spectral_Thinking_and_Diagonalization": {
                "name": "Module 05: Eigenvectors, Eigenvalues & Diagonalization",
                "query": "3Blue1Brown Eigenvectors and eigenvalues Chapter 14",
                "authors": ["3Blue1Brown", "Steve Brunton"],
                "focus": "Characteristic polynomials, eigenbasis, scaling factors, and matrix powers."
            },
            "Module_06_Orthogonality_and_Projections": {
                "name": "Module 06: Orthogonality, Projections & Gram-Schmidt",
                "query": "Gilbert Strang Orthogonal Vectors and Subspaces MIT 18.06",
                "authors": ["MIT OpenCourseWare", "3Blue1Brown", "Steve Brunton"],
                "focus": "Inner products, orthogonal subspaces, projection matrices, and least squares."
            },
            "Module_07_LowRank_Structure_and_Quadratic_Forms": {
                "name": "Module 07: Singular Value Decomposition (SVD) & Quadratic Forms",
                "query": "Steve Brunton Singular Value Decomposition SVD",
                "authors": ["Steve Brunton", "3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Left/right singular vectors, singular values, Eckart-Young low-rank approximation."
            },
            "Module_08_Linear_Algebra_in_Models": {
                "name": "Module 08: Linear Algebra in ML Models & PCA",
                "query": "StatQuest Principal Component Analysis PCA step by step",
                "authors": ["StatQuest with Josh Starmer", "3Blue1Brown"],
                "focus": "Dimensionality reduction, covariance matrix diagonalization, and variance maximization."
            },
            "Module_09_Multivariable_Calculus_for_Learning": {
                "name": "Module 09: Multivariable Calculus & Gradient Descent",
                "query": "3Blue1Brown Gradient descent how neural networks learn Chapter 2",
                "authors": ["3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Partial derivatives, gradient vectors, Jacobian, Hessian matrices, and optimization."
            },
            "Module_10_Reasoning_Under_Uncertainty": {
                "name": "Module 10: Bayes Theorem & Probabilistic Reasoning",
                "query": "3Blue1Brown Bayes theorem visual guide",
                "authors": ["3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Prior, likelihood, marginal, and posterior probability updates."
            },
            "Module_11_Joint_Distributions_and_Covariance": {
                "name": "Module 11: Joint Distributions, Covariance & Independence",
                "query": "StatQuest Covariance and Correlation clearly explained",
                "authors": ["StatQuest with Josh Starmer", "3Blue1Brown"],
                "focus": "Joint probability mass functions, marginal distributions, correlation, and independence."
            },
            "Module_12_Statistical_Estimation_from_Samples": {
                "name": "Module 12: Statistical Estimation & Maximum Likelihood (MLE)",
                "query": "StatQuest Maximum Likelihood clearly explained",
                "authors": ["StatQuest with Josh Starmer", "3Blue1Brown"],
                "focus": "Likelihood functions, log-likelihood, parameter optimization, and bias-variance trade-off."
            }
        }
    },

    # COURSE 06
    "06_Deep_Learning_and_AI_Foundations": {
        "title": "Course 06: Deep Learning & AI Foundations",
        "subtitle": "Neural Networks, Transformers, Fine-Tuning & LLMs From Scratch",
        "defaults": ["Andrej Karpathy", "3Blue1Brown", "StatQuest with Josh Starmer", "Umar Jamil"],
        "modules": {
            "Module_01_Math_Fundamentals": {
                "name": "Module 01: Backpropagation Calculus & Neural Intuitions",
                "query": "3Blue1Brown Neural networks calculus backpropagation Chapter 3",
                "authors": ["3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Chain rule across computational graphs and loss gradient propagation."
            },
            "Module_02_Core_AI_Intuitions": {
                "name": "Module 02: Core AI Intuitions & LLM High-Level Architecture",
                "query": "Andrej Karpathy What is a neural network Intro to Large Language Models",
                "authors": ["Andrej Karpathy", "3Blue1Brown"],
                "focus": "Next-token prediction, pretraining vs fine-tuning, and inference dynamics."
            },
            "Module_03_PyTorch_Fundamentals": {
                "name": "Module 03: PyTorch Bootcamp: Tensors, Autograd & Modules",
                "query": "freeCodeCamp PyTorch for Deep Learning Bootcamp full course Daniel Bourke",
                "authors": ["freeCodeCamp", "Aladdin Persson"],
                "focus": "Tensor operations, autograd backward pass, nn.Module, and optimizer loops."
            },
            "Module_04_TensorFlow_Fundamentals": {
                "name": "Module 04: TensorFlow & Keras Foundations",
                "query": "freeCodeCamp TensorFlow 2.0 Complete Course Python",
                "authors": ["freeCodeCamp", "Daniel Bourke"],
                "focus": "Eager execution, tf.data pipelines, Functional API, and SavedModel deployment."
            },
            "Module_05_Neural_Network_from_Scratch": {
                "name": "Module 05: Building Neural Networks from Scratch (Micrograd)",
                "query": "Andrej Karpathy Building micrograd neural network from scratch",
                "authors": ["Andrej Karpathy"],
                "focus": "Writing an autograd engine with topological sort and backprop from bare Python."
            },
            "Module_06_Transformers": {
                "name": "Module 06: Transformers & Self-Attention Explained",
                "query": "3Blue1Brown Attention in transformers step by step Chapter 6",
                "authors": ["3Blue1Brown", "StatQuest with Josh Starmer"],
                "focus": "Queries, Keys, Values, Softmax scaling, and multi-head attention visual mechanics."
            },
            "Module_07_Reinforcement_Learning": {
                "name": "Module 07: Reinforcement Learning & Policy Gradients",
                "query": "Andrej Karpathy Deep Reinforcement Learning Pong from Pixels",
                "authors": ["Andrej Karpathy", "DeepMind"],
                "focus": "Markov Decision Processes, rewards, discounted returns, and REINFORCE policy gradients."
            },
            "Module_08_LLM_From_Scratch": {
                "name": "Module 08: Building GPT from Scratch (Karpathy Masterclass)",
                "query": "Andrej Karpathy Let's build GPT from scratch spelled out",
                "authors": ["Andrej Karpathy"],
                "focus": "Character-level and BPE tokenization, transformer decoder blocks, and autoregressive generation."
            },
            "Module_09_Write_Research_Paper": {
                "name": "Module 09: Reading & Writing Frontier AI Research Papers",
                "query": "Andrew Ng How to read and write research papers AI machine learning",
                "authors": ["Andrew Ng", "Yannic Kilcher"],
                "focus": "Navigating arXiv, literature synthesis, experimental ablation methodology, and academic writing."
            },
            "Module_10_How_to_FineTune_Models": {
                "name": "Module 10: Parameter-Efficient Fine-Tuning (PEFT & LoRA)",
                "query": "Umar Jamil LoRA Low Rank Adaptation of Large Language Models",
                "authors": ["Umar Jamil", "Weights & Biases", "Yannic Kilcher"],
                "focus": "Freezing base weights, low-rank matrix decomposition (A and B), and adapter merging."
            },
            "Module_11_Machine_Learning_Operations_MLOps": {
                "name": "Module 11: Machine Learning Operations (MLOps) in Production",
                "query": "freeCodeCamp MLOps Course Machine Learning Operations",
                "authors": ["freeCodeCamp", "Weights & Biases"],
                "focus": "Model registry, experiment tracking, data drift monitoring, and CI/CD for models."
            },
            "Module_12_Bonus_Lessons": {
                "name": "Module 12: Frontier LLM Trends & State of the Art",
                "query": "Andrej Karpathy State of GPT Microsoft Build",
                "authors": ["Andrej Karpathy", "Yannic Kilcher"],
                "focus": "RLHF, DPO, instruction fine-tuning, reasoning models, and the road to AGI."
            }
        }
    },

    # COURSE 07
    "07_GPU_Programming_and_AI_Kernels": {
        "title": "Course 07: GPU Programming & AI Kernel Optimization",
        "subtitle": "CUDA C++, OpenAI Triton, FlashAttention & Hopper/Blackwell Architecture",
        "defaults": ["GPU MODE", "CoffeeBeforeArch", "NVIDIA Developer", "Umar Jamil"],
        "modules": {
            "Module_01_GPU_Microarchitecture_and_Execution_Model": {
                "name": "Module 01: GPU Microarchitecture & Execution Model",
                "query": "Stanford CS149 GPU architecture SIMD warps Kayvon Fatahalian",
                "authors": ["Stanford Online", "CoffeeBeforeArch", "GPU MODE"],
                "focus": "Streaming Multiprocessors (SMs), warps, thread blocks, and hardware scheduling."
            },
            "Module_02_CUDA_Cpp_Programming_Fundamentals": {
                "name": "Module 02: CUDA C++ Programming Fundamentals",
                "query": "CUDA Crash Course GPU programming CoffeeBeforeArch",
                "authors": ["CoffeeBeforeArch", "NVIDIA Developer"],
                "focus": "Host vs device memory, kernel launch configurations (<<<grid, block>>>), and error checking."
            },
            "Module_03_CUDA_Memory_Hierarchy_and_Coalescing": {
                "name": "Module 03: CUDA Memory Hierarchy & Coalescing",
                "query": "CUDA Memory hierarchy shared memory coalescing CoffeeBeforeArch",
                "authors": ["CoffeeBeforeArch", "GPU MODE"],
                "focus": "Global memory transactions, 32-byte coalescing, shared memory bank conflicts, and registers."
            },
            "Module_04_Parallel_Reduction_and_Prefix_Sum": {
                "name": "Module 04: Parallel Reduction & Warp Primitives",
                "query": "Mark Harris Optimizing Parallel Reduction in CUDA NVIDIA",
                "authors": ["NVIDIA Developer", "CoffeeBeforeArch", "GPU MODE"],
                "focus": "Tree reduction, warp shuffle (__shfl_down_sync), eliminating branch divergence."
            },
            "Module_05_Tiled_Matrix_Multiplication_GEMM": {
                "name": "Module 05: Tiled Matrix Multiplication (GEMM)",
                "query": "CUDA Tiled Matrix Multiplication shared memory CoffeeBeforeArch",
                "authors": ["CoffeeBeforeArch", "GPU MODE"],
                "focus": "2D shared memory cache tiling, outer product formulation, and achieving roofline compute peak."
            },
            "Module_06_OpenAI_Triton_Programming_Fundamentals": {
                "name": "Module 06: OpenAI Triton Programming Fundamentals",
                "query": "OpenAI Triton GPU programming tutorial GPU MODE",
                "authors": ["GPU MODE", "Umar Jamil"],
                "focus": "Block-level programming, automatic memory coalescing, and writing Pythonic GPU kernels."
            },
            "Module_07_Fused_Activations_and_Normalization": {
                "name": "Module 07: Fused Activations & Normalization Kernels",
                "query": "GPU MODE LayerNorm Softmax Triton kernel optimization",
                "authors": ["GPU MODE", "CoffeeBeforeArch"],
                "focus": "Eliminating HBM memory roundtrips by fusing Softmax, LayerNorm, and GELU into SRAM."
            },
            "Module_08_FlashAttention_1_and_2_Internals": {
                "name": "Module 08: FlashAttention-1 & 2 Internals",
                "query": "Umar Jamil FlashAttention explained step by step",
                "authors": ["Umar Jamil", "GPU MODE", "Yannic Kilcher"],
                "focus": "Online softmax, block-tiling Q/K/V in SRAM, and cutting attention IO from O(N^2) to O(N)."
            },
            "Module_09_FlashAttention_3_and_Hopper_Blackwell_Features": {
                "name": "Module 09: FlashAttention-3 & Hopper/Blackwell Innovations",
                "query": "Tri Dao FlashAttention 3 Hopper TMA Tensor Cores",
                "authors": ["GPU MODE", "Stanford Online", "Weights & Biases"],
                "focus": "Tensor Memory Accelerator (TMA), Warp Specialized pipelines, and FP8 GEMM precision."
            },
            "Module_10_Quantization_Kernels_in_Triton": {
                "name": "Module 10: Quantization Kernels in Triton (FP8 & INT4)",
                "query": "Tim Dettmers Quantization FP8 INT4 LLM GPU",
                "authors": ["GPU MODE", "Weights & Biases", "Umar Jamil"],
                "focus": "Scale and zero-point packing, AWQ dequantization in registers, and low-bit GEMM."
            },
            "Module_11_Profiling_with_Nsight_Compute_and_Systems": {
                "name": "Module 11: Profiling & Tuning with Nsight (NCU & NSYS)",
                "query": "NVIDIA Nsight Compute tutorial kernel profiling",
                "authors": ["NVIDIA Developer", "GPU MODE"],
                "focus": "Roofline model analysis, memory throughput bottlenecks, warp stall reasons, and timeline traces."
            }
        }
    },

    # COURSE 08
    "08_Distributed_Training_and_GPU_Infrastructure": {
        "title": "Course 08: Distributed Training & GPU Infrastructure",
        "subtitle": "Cluster Networking, NCCL, 3D Parallelism (Megatron/DeepSpeed) & FSDP",
        "defaults": ["ByteByteGo", "Umar Jamil", "Weights & Biases", "Stanford Online"],
        "modules": {
            "Module_01_GPU_Cluster_Hardware_and_Interconnects": {
                "name": "Module 01: GPU Cluster Hardware & Interconnects",
                "query": "NVIDIA InfiniBand NVLink GPU cluster architecture explained",
                "authors": ["ByteByteGo", "NVIDIA Developer"],
                "focus": "NVLink crossbars, NVSwitch topology, InfiniBand HDR/NDR, and RoCE v2 networking."
            },
            "Module_02_NCCL_Collective_Communication_Primitives": {
                "name": "Module 02: NCCL Collective Communication Primitives",
                "query": "Ring AllReduce NCCL collective communication distributed deep learning",
                "authors": ["ByteByteGo", "GPU MODE"],
                "focus": "Ring-AllReduce, Tree-AllReduce, Broadcast, AllGather, and ReduceScatter bandwidth formulas."
            },
            "Module_03_Distributed_Data_Parallel_DDP": {
                "name": "Module 03: PyTorch Distributed Data Parallel (DDP)",
                "query": "PyTorch Distributed Data Parallel DDP tutorial explained",
                "authors": ["PyTorch", "Weights & Biases", "Umar Jamil"],
                "focus": "Gradient bucketing, overlapping computation with communication, and multi-process architecture."
            },
            "Module_04_DeepSpeed_ZeRO_and_PyTorch_FSDP": {
                "name": "Module 04: DeepSpeed ZeRO & PyTorch FSDP",
                "query": "DeepSpeed ZeRO explained memory optimization distributed training",
                "authors": ["Umar Jamil", "Weights & Biases"],
                "focus": "ZeRO-1 (Optimizer States), ZeRO-2 (Gradients), ZeRO-3 (Parameters), and FSDP sharding."
            },
            "Module_05_Tensor_Parallelism_Megatron_LM": {
                "name": "Module 05: Tensor Parallelism (Megatron-LM)",
                "query": "Tensor Parallelism Megatron LM Shoeybi explained",
                "authors": ["Umar Jamil", "Stanford Online"],
                "focus": "Column-parallel Linear and Row-parallel Linear splits in Multi-Head Attention and MLP."
            },
            "Module_06_Pipeline_Parallelism_and_Schedules": {
                "name": "Module 06: Pipeline Parallelism (1F1B Schedules)",
                "query": "Pipeline Parallelism 1F1B schedule GPipe Megatron",
                "authors": ["Stanford Online", "Umar Jamil"],
                "focus": "Micro-batching, pipeline bubble reduction, 1F1B steady-state, and activation checkpointing."
            },
            "Module_07_Sequence_and_Context_Parallelism_Ring_Attention": {
                "name": "Module 07: Sequence Parallelism & Ring Attention",
                "query": "Ring Attention long context distributed training explained",
                "authors": ["Yannic Kilcher", "Umar Jamil"],
                "focus": "Splitting sequence length across GPUs, circular ring KV communication, and scaling to 1M tokens."
            },
            "Module_08_3D_Parallelism_Integration_and_Orchestration": {
                "name": "Module 08: 3D Parallelism Integration & Orchestration",
                "query": "3D Parallelism DP TP PP Megatron DeepSpeed",
                "authors": ["Weights & Biases", "Stanford Online"],
                "focus": "Combining DP x TP x PP across GPU racks to train multi-hundred-billion parameter models."
            },
            "Module_09_Distributed_Checkpointing_DCP_and_Failure_Recovery": {
                "name": "Module 09: Distributed Checkpointing & Fault Tolerance",
                "query": "PyTorch Distributed Checkpoint DCP fault tolerance",
                "authors": ["PyTorch", "Weights & Biases"],
                "focus": "Asynchronous non-blocking checkpoint saves, elastic cluster rescheduling, and fast state recovery."
            },
            "Module_10_Scaling_Laws_Profiling_and_FinOps": {
                "name": "Module 10: Scaling Laws, Cluster Profiling & FinOps",
                "query": "Chinchilla scaling laws Kaplan OpenAI deep learning",
                "authors": ["Yannic Kilcher", "Weights & Biases", "Andrej Karpathy"],
                "focus": "Model compute efficiency (MFU), compute-optimal training tokens, and GPU cluster cost budgeting."
            }
        }
    },

    # COURSE 09
    "09_Inference_Systems_and_Serving_Engines": {
        "title": "Course 09: LLM Inference Systems & Serving Engines",
        "subtitle": "PagedAttention, Continuous Batching, Speculative Decoding & TensorRT-LLM",
        "defaults": ["ByteByteGo", "Tales Of Tensors", "Umar Jamil", "Weights & Biases"],
        "modules": {
            "Module_01_Inference_Latency_Throughput_Tradeoffs": {
                "name": "Module 01: Inference Latency, TTFT & TPOT Trade-offs",
                "query": "LLM inference latency vs throughput TTFT TPOT explained",
                "authors": ["ByteByteGo", "Weights & Biases"],
                "focus": "Time To First Token (TTFT), Time Per Output Token (TPOT), and memory bandwidth ceilings."
            },
            "Module_02_KV_Cache_Memory_Management": {
                "name": "Module 02: KV-Cache Memory Hierarchy & Growth",
                "query": "KV Cache LLM inference memory explained",
                "authors": ["ByteByteGo", "Umar Jamil"],
                "focus": "Autoregressive cache mechanics, memory footprints per token, and multi-query/grouped-query attention."
            },
            "Module_03_PagedAttention_Architecture_vLLM": {
                "name": "Module 03: PagedAttention Architecture (vLLM)",
                "query": "PagedAttention vLLM architecture paper explained",
                "authors": ["Tales Of Tensors", "Umar Jamil", "ByteByteGo"],
                "focus": "Translating virtual memory paging into GPU KV-cache blocks, eliminating internal fragmentation."
            },
            "Module_04_RadixAttention_and_Prefix_Caching": {
                "name": "Module 04: RadixAttention & Prefix Caching (SGLang)",
                "query": "SGLang RadixAttention prefix caching LLM serving",
                "authors": ["LMSYS", "Stanford Online"],
                "focus": "Radix tree prefix reuse across multi-turn chats, few-shot prompts, and shared system messages."
            },
            "Module_05_Continuous_and_Dynamic_Batching": {
                "name": "Module 05: Continuous & Dynamic Iteration-Level Batching",
                "query": "Continuous batching cellular batching LLM serving TGI vLLM",
                "authors": ["ByteByteGo", "Hugging Face"],
                "focus": "Iteration-level scheduling, inserting incoming prompts without waiting for completed sequences."
            },
            "Module_06_Chunked_Prefill_and_PD_Disaggregation": {
                "name": "Module 06: Chunked Prefill & Prefill-Decode (PD) Disaggregation",
                "query": "Chunked prefill disaggregated prefill decode LLM serving",
                "authors": ["Weights & Biases", "vLLM"],
                "focus": "Separating compute-bound prefill nodes from memory-bound decode nodes to eliminate inter-token jitter."
            },
            "Module_07_Speculative_Decoding_Architectures": {
                "name": "Module 07: Speculative Decoding & Medusa Multi-Head Verification",
                "query": "Speculative decoding for faster LLM inference explained",
                "authors": ["Yannic Kilcher", "Umar Jamil"],
                "focus": "Draft model speculation, parallel verification by the target model, and acceptance rates."
            },
            "Module_08_Quantization_for_Serving": {
                "name": "Module 08: Model Quantization for Serving (FP8, AWQ, Marlin)",
                "query": "AWQ Activation aware Weight Quantization for LLM serving",
                "authors": ["Umar Jamil", "Yannic Kilcher"],
                "focus": "Weight-only vs weight-activation quantization, outlier protection, and Marlin high-speed kernels."
            },
            "Module_09_Production_Benchmarking_and_Autoscaling": {
                "name": "Module 09: Production Benchmarking, SLAs & Autoscaling",
                "query": "Benchmarking and autoscaling LLM inference in production",
                "authors": ["Weights & Biases", "ByteByteGo"],
                "focus": "Load testing with synthetic concurrency, TTFT p99 latency SLAs, and GPU pod autoscaling."
            }
        }
    },

    # COURSE 10
    "10_Advanced_Retrieval_and_Context_Engineering": {
        "title": "Course 10: Advanced Retrieval & Context Engineering",
        "subtitle": "Hierarchical Chunking, Hybrid Search, ColBERT Late Interaction & GraphRAG",
        "defaults": ["Prompt Engineering", "ByteByteGo", "IBM Technology", "Pinecone"],
        "modules": {
            "Module_01_Parsing_and_Hierarchical_Chunking": {
                "name": "Module 01: Parsing & Hierarchical Semantic Chunking",
                "query": "Advanced chunking strategies RAG document parsing LangChain",
                "authors": ["LangChain", "Prompt Engineering"],
                "focus": "Document structure preservation, semantic splitters, parent-child chunk hierarchies."
            },
            "Module_02_Contextual_Retrieval_Architecture": {
                "name": "Module 02: Anthropic Contextual Retrieval Architecture",
                "query": "Anthropic Contextual Retrieval RAG architecture explained",
                "authors": ["Prompt Engineering", "AI Jason"],
                "focus": "Pre-pending chunk-specific context descriptions before vector embedding to prevent ambiguity."
            },
            "Module_03_Vector_Database_Internals": {
                "name": "Module 03: Vector Database Internals (HNSW & Product Quantization)",
                "query": "HNSW Vector search index hierarchical navigable small world explained",
                "authors": ["Pinecone", "ByteByteGo", "IBM Technology"],
                "focus": "Multi-layer skip-graph connectivity, vector quantization, and trade-offs between memory and recall."
            },
            "Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion": {
                "name": "Module 04: Hybrid Search & Reciprocal Rank Fusion (RRF)",
                "query": "Hybrid search dense sparse reciprocal rank fusion RRF",
                "authors": ["Pinecone", "Prompt Engineering", "Cohere"],
                "focus": "Combining BM25 keyword matching with dense embeddings using parameter-free RRF scoring."
            },
            "Module_05_Multi_Stage_Retrieval_and_Reranking": {
                "name": "Module 05: Multi-Stage Retrieval & Cross-Encoder Reranking",
                "query": "Cross Encoder reranking RAG multi stage retrieval",
                "authors": ["Cohere", "Prompt Engineering", "AI Jason"],
                "focus": "Bi-encoder fast candidate retrieval followed by heavy cross-encoder attention scoring."
            },
            "Module_06_ColBERTv2_and_Late_Interaction": {
                "name": "Module 06: ColBERTv2 & Token-Level Late Interaction",
                "query": "ColBERT late interaction multi vector retrieval explained",
                "authors": ["Stanford Online", "Prompt Engineering"],
                "focus": "MaxSim operator, retaining per-token contextual vectors, and sub-millisecond retrieval."
            },
            "Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs": {
                "name": "Module 07: Microsoft GraphRAG & Community Summarization",
                "query": "Microsoft GraphRAG knowledge graph RAG explained",
                "authors": ["Prompt Engineering", "AI Jason"],
                "focus": "Entity-relation extraction, graph clustering (Leiden algorithm), and hierarchical global summaries."
            },
            "Module_08_Query_Transformation_and_Agentic_RAG": {
                "name": "Module 08: Query Transformation & Agentic Multi-Hop RAG",
                "query": "Query rewriting expansion Hyde Agentic RAG LangChain",
                "authors": ["LangChain", "Prompt Engineering"],
                "focus": "Hypothetical Document Embeddings (HyDE), step-back prompting, and routing agent decisions."
            },
            "Module_09_Context_Optimization_and_NIAH_Testing": {
                "name": "Module 09: Context Optimization & Needle-in-a-Haystack (NIAH)",
                "query": "Needle In A Haystack test LLM long context evaluation Greg Kamradt",
                "authors": ["Greg Kamradt", "Prompt Engineering"],
                "focus": "Testing context retrieval recall across document depth, prompt compression, and lost-in-the-middle."
            }
        }
    },

    # COURSE 11
    "11_Autonomous_Agents_and_Cognitive_Architectures": {
        "title": "Course 11: Autonomous Agents & Cognitive Architectures",
        "subtitle": "ReAct Loops, LangGraph State Machines, Multi-Agent Swarms & Secure Sandboxing",
        "defaults": ["LangChain", "DeepLearning.AI", "Prompt Engineering", "AI Jason"],
        "modules": {
            "Module_01_Agent_Cognitive_Architectures_and_Loops": {
                "name": "Module 01: Agent Cognitive Loops & ReAct Architecture",
                "query": "ReAct Reason and Act LLM agents explained",
                "authors": ["DeepLearning.AI", "LangChain", "Prompt Engineering"],
                "focus": "Thought-Action-Observation cognitive loop, reflection mechanisms, and trajectory planning."
            },
            "Module_02_State_Machine_Graphs_LangGraph_Internals": {
                "name": "Module 02: LangGraph Internals: Stateful Graphs & Cyclic Loops",
                "query": "Harrison Chase LangGraph tutorial stateful multi agent",
                "authors": ["LangChain", "freeCodeCamp", "Prompt Engineering"],
                "focus": "State channels, conditional edges, reducer functions, and managing stateful agent transitions."
            },
            "Module_03_Tool_Execution_and_Constrained_Generation": {
                "name": "Module 03: Function Calling & Structured Tool Execution",
                "query": "OpenAI Function Calling Tool Use tutorial python",
                "authors": ["freeCodeCamp", "Prompt Engineering", "LangChain"],
                "focus": "JSON schema tool definitions, parser validation, exception recovery, and strict mode."
            },
            "Module_04_Agent_Memory_Systems": {
                "name": "Module 04: Agent Memory: Short-Term, Episodic & Semantic",
                "query": "LLM Agent Memory short term long term episodic semantic memory",
                "authors": ["LangChain", "Prompt Engineering", "AI Jason"],
                "focus": "Buffer memories, vector-backed episodic recall, and user profile semantic extraction."
            },
            "Module_05_Multi_Agent_Collaboration_Topologies": {
                "name": "Module 05: Multi-Agent Collaboration Topologies & Swarms",
                "query": "Multi-agent collaboration LangGraph CrewAI AutoGen",
                "authors": ["DeepLearning.AI", "LangChain", "freeCodeCamp"],
                "focus": "Supervisor orchestrators, hierarchical delegators, and peer-to-peer consensus debates."
            },
            "Module_06_Sandboxed_Code_Execution_and_Security": {
                "name": "Module 06: Sandboxed Code Execution & Security Isolation",
                "query": "Securing LLM code execution sandboxing Docker E2B",
                "authors": ["Weights & Biases", "Prompt Engineering"],
                "focus": "Isolating untrusted AI-generated code via microVMs, Docker containers, and capability restrictions."
            },
            "Module_07_Human_in_the_Loop_and_Time_Travel": {
                "name": "Module 07: Human-in-the-Loop & Time Travel State Rewinding",
                "query": "LangGraph Human in the loop breakpoints time travel",
                "authors": ["LangChain", "Prompt Engineering"],
                "focus": "Approval breakpoints, editing state mid-flight, and branching alternative trajectory paths."
            },
            "Module_08_Production_Agent_Evaluation": {
                "name": "Module 08: Production Agent Evaluation & Benchmarks",
                "query": "Evaluating LLM agents in production benchmarks DeepLearningAI",
                "authors": ["DeepLearning.AI", "LangChain", "Weights & Biases"],
                "focus": "Task completion metrics, trajectory efficiency, LLM-as-a-judge scorers, and GAIA benchmarks."
            }
        }
    },

    # COURSE 12
    "12_LLM_Evaluation_Science_and_Guardrails": {
        "title": "Course 12: LLM Evaluation Science & Production Guardrails",
        "subtitle": "Evaluation Harnesses, LLM-as-a-Judge, NeMo Guardrails & Adversarial Red Teaming",
        "defaults": ["DeepLearning.AI", "Weights & Biases", "IBM Technology", "NVIDIA Developer"],
        "modules": {
            "Module_01_LLM_Evaluation_Science_and_Metrics": {
                "name": "Module 01: LLM Evaluation Science: Ground Truth & RAGAS",
                "query": "LLM evaluation metrics RAGAS BLEU ROUGE DeepLearningAI",
                "authors": ["DeepLearning.AI", "Weights & Biases"],
                "focus": "Faithfulness, Answer Relevance, Context Precision, and semantic similarity bounds."
            },
            "Module_02_LLM_as_a_Judge_Calibration_and_Bias": {
                "name": "Module 02: LLM-as-a-Judge Calibration & Bias Mitigation",
                "query": "LLM as a judge evaluation calibration position bias",
                "authors": ["Weights & Biases", "LMSYS", "Stanford Online"],
                "focus": "Position bias, verbosity bias, self-enhancement bias, and pairwise swap calibration."
            },
            "Module_03_Standardized_Benchmark_Harnesses": {
                "name": "Module 03: Benchmark Harnesses (MMLU, GSM8K, HumanEval)",
                "query": "MMLU GSM8K HumanEval LLM benchmark harnesses evaluation",
                "authors": ["Yannic Kilcher", "Weights & Biases"],
                "focus": "Few-shot evaluation, chain-of-thought prompting impact, and contamination detection."
            },
            "Module_04_Production_Guardrails_Architecture": {
                "name": "Module 04: Production Guardrails Architecture & Policy Filters",
                "query": "Guardrails AI production validation LLM security",
                "authors": ["DeepLearning.AI", "Prompt Engineering", "IBM Technology"],
                "focus": "Input/output validation layers, PII anonymization, hallucination detectors, and schema enforcement."
            },
            "Module_05_NeMo_Guardrails_and_Llama_Guard": {
                "name": "Module 05: NVIDIA NeMo Guardrails & Meta Llama Guard",
                "query": "NVIDIA NeMo Guardrails Llama Guard tutorial",
                "authors": ["NVIDIA Developer", "DeepLearning.AI"],
                "focus": "Colang conversational flows, topical steering, and safety classifier models."
            },
            "Module_06_Adversarial_AI_Security_OWASP_Top_10": {
                "name": "Module 06: Adversarial AI Security & OWASP Top 10 for LLMs",
                "query": "OWASP Top 10 for LLMs prompt injection jailbreaking",
                "authors": ["IBM Technology", "freeCodeCamp"],
                "focus": "Direct and indirect prompt injection, data exfiltration, system prompt leakage, and jailbreak vectors."
            },
            "Module_07_Automated_Red_Teaming": {
                "name": "Module 07: Automated Red Teaming & Jailbreak Testing (PyRIT)",
                "query": "Red teaming LLMs automated prompt security PyRIT Microsoft",
                "authors": ["Microsoft Developer", "DeepLearning.AI"],
                "focus": "Adversarial prompt generation, multi-turn jailbreaking, and vulnerability discovery automation."
            },
            "Module_08_Production_AI_Observability_and_Tracing": {
                "name": "Module 08: Production AI Observability & OpenTelemetry Tracing",
                "query": "OpenInference Arize Phoenix OpenTelemetry LLM observability tracing",
                "authors": ["DeepLearning.AI", "Arize AI", "Weights & Biases"],
                "focus": "Tracing token usage, latency heatmaps, user feedback loops, and live production alerting."
            }
        }
    }
}

def generate_dataset():
    meta = json.loads((ROOT_DIR / "scripts" / "modules_meta.json").read_text(encoding="utf-8"))
    out_courses = []

    total_modules = 0

    for folder, mods in meta.items():
        if folder not in CURATION_MAP:
            print(f"[!] Warning: missing curation for course: {folder}")
            continue

        c_info = CURATION_MAP[folder]
        c_title = c_info["title"]
        c_subtitle = c_info["subtitle"]
        defaults = c_info["defaults"]
        course_mods_def = c_info["modules"]

        module_list = []
        for m in mods:
            m_dir = m["dir"]
            m_clean_title = m["title"]
            if m_dir in course_mods_def:
                m_def = course_mods_def[m_dir]
                module_list.append({
                    "dir": m_dir,
                    "name": m_def["name"],
                    "query": m_def["query"],
                    "authors": m_def["authors"],
                    "focus": m_def["focus"]
                })
            else:
                # Fallback clean query
                clean_name = m_dir.replace("Module_", "Module ").replace("_", " ")
                query = f"{clean_name} {defaults[0]} tutorial"
                module_list.append({
                    "dir": m_dir,
                    "name": clean_name,
                    "query": query,
                    "authors": defaults,
                    "focus": f"Architectural breakdown and implementation for {clean_name}."
                })

        total_modules += len(module_list)
        out_courses.append({
            "folder": folder,
            "title": c_title,
            "subtitle": c_subtitle,
            "modules": module_list
        })

    out_file = ROOT_DIR / "scripts" / "all_175_modules_data.json"
    out_file.write_text(json.dumps(out_courses, indent=2), encoding="utf-8")
    print(f"[✓] Generated all_175_modules_data.json with {len(out_courses)} courses and {total_modules} modules total.")

if __name__ == "__main__":
    generate_dataset()
