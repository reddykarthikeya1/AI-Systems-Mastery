# High-Level Design for Python & AI Engineers
### Version 3.0: Definitive Learning Edition (`AI-Systems-Mastery`)

An authoritative, mathematically grounded, and code-verified curriculum in modern distributed systems, cloud resilience patterns, and AI infrastructure engineering.

---

## 1. Curriculum Overview

**High-Level Design for Python & AI Engineers** bridges the gap between classic web-scale distributed architectures and modern AI systems infrastructure. Built for senior, staff, and principal engineers, this repository provides:

- **The Master Textbook (195 Pages, Letter Format):** `HLD_Python_Master_Textbook_Final.pdf`, featuring 25 foundational and supplementary chapters, 6 production workshops, 30 publication-grade symmetrical vector SVG blueprints, and the disciplined 9-step FAANG Staff/Principal whiteboard interview framework.
- **The Interactive Python Laboratory (`HLD_Python_Labs`):** A fully tested companion codebase spanning 13 packages and 97 automated unit and integration tests (100% passing) verifying concurrency controls, cache fencing, probabilistic data structures, and virtual memory KV-cache allocation.
- **Authoritative Engineering Audits:** Rigorous technical documentation including `HLD_Technical_Audit_Report.md`, `HLD_PDF_QA_Report.md`, and `HLD_Revision_Changelog.md`.

---

## 2. The 3-Tier Educational Framework

The curriculum is structured around a progressive, three-tier engineering framework:

```
+---------------------------------------------------------------------------------------------------+
| LEVEL 3: MODERN AI INFRASTRUCTURE, HYPERSCALE WORKSHOPS & STAFF WHITEBOARD MASTERY                |
| - Vector DBs & HNSW Graph Complexity Bounds (Empirical O(log N) vs O(N))                         |
| - Google Zanzibar Relationship-Based Access Control (ReBAC) & Fail-Closed Multi-Tenant Gates       |
| - vLLM PagedAttention KV-Cache Management, Copy-on-Write (CoW) Parallel Sampling & Radix Routing  |
| - 6 End-to-End Production Workshops (Flash Sales, 50M Chat, Video, Ride-Hailing, LLM, Agent RAG)  |
| - Disciplined 9-Step FAANG Whiteboard Interview Playbook with 45-Minute Time Allocation Rubrics   |
+---------------------------------------------------------------------------------------------------+
                                                  ^
                                                  |
+---------------------------------------------------------------------------------------------------+
| LEVEL 2: ADVANCED CONCURRENCY, EVENT-DRIVEN PRIMITIVES & RESILIENCE                               |
| - CAP & PACELC Trade-Offs (DynamoDB PA/EL vs MongoDB PC/EC vs Bigtable PC/EC)                    |
| - Consistency Models Spectrum (Linearizability -> Sequential -> Causal -> Eventual)               |
| - Distributed Commit Logs & Kafka Cooperative Sticky Assignor (Eliminating Rebalance STW)         |
| - Transactional Outbox Pattern with Concurrent PostgreSQL `FOR UPDATE SKIP LOCKED` Polling        |
| - Thread-Safe Circuit Breakers with Atomic Single-Probe `HALF_OPEN` Admission Gating              |
| - Orchestrated Sagas with Structured State Logging & Strict Reverse Compensation DAGs            |
| - Multi-Dimensional Token Buckets (RPM + TPM) with Server-Side Time Synchronization               |
+---------------------------------------------------------------------------------------------------+
                                                  ^
                                                  |
+---------------------------------------------------------------------------------------------------+
| LEVEL 1: DISTRIBUTED SYSTEMS CORE FOUNDATIONS                                                     |
| - Scaling Laws: Little's Law (L = λW), Amdahl's Law, and Universal Scalability Law (USL)          |
| - Multi-Tier Ingress Fabric: Layer 4 DSR (Maglev/IPVS) vs Layer 7 Envoy Mesh vs Prefix Routers   |
| - Versioned Cache-Aside Invalidation with Monotonic Watermark Key Preservation                    |
| - Database Sharding Geometry & Scatter-Gather Latency Amplification Bounds                        |
| - Database Replication Topologies, Async Replica Lag, and Monotonic Fencing Token Epochs         |
| - Consistent Hash Rings with Virtual Nodes (Vnodes) & Google Bounded-Load Spillover               |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Curriculum Roadmap & Chapter Index

```
High Level Design/
├── HLD_Python_Master_Textbook_Final.pdf  # The Definitive 195-Page Master Textbook
├── HLD_Technical_Audit_Report.md        # Engineering Audit & Issue 2.1 A–K Findings
├── HLD_PDF_QA_Report.md                 # Publication Quality Assurance & Layout Report
├── HLD_Revision_Changelog.md            # Version 3.0 Milestone Changelog
├── README.md                            # Repository Overview & Quickstart Guide
└── HLD_Python_Labs/                     # Complete Runnable Python Laboratory
    ├── ch01_scalability/                # Little's Law, AIMD & Vegas Adaptive Limiters
    ├── ch03_caching/                    # Versioned Cache-Aside & SingleFlight Stampede Defense
    ├── ch07_consistent_hashing/         # Murmur/SHA-256 Hash Ring & Google Bounded Loads
    ├── ch12_event_driven/               # Transactional Outbox & SKIP LOCKED Poller
    ├── ch15_rate_limiter/               # Dual Token Bucket (RPM + TPM) for LLM Gateways
    ├── ch16_bloom_filter/               # Bloom Filter vs MinHash & LSH Banding
    ├── ch17_circuit_breaker/            # Circuit Breaker with Atomic Single-Probe HALF_OPEN
    ├── ch18_saga_orchestrator/          # Saga Orchestrator with Structured Logging & Async
    ├── ch21_distributed_search/         # Okapi BM25 Lexical + Dense Cosine + RRF
    ├── ch24_zanzibar_rebac/             # Google Zanzibar ReBAC Engine with Cycle Detection
    ├── workshop_ecommerce/              # Flash Sale Redis Inventory & Postgres Reconciliation
    ├── workshop_llm_serving/            # vLLM PagedAttention KV-Cache, CoW & Radix Router
    ├── workshop_rag_agents/             # Enterprise RAG Orchestrator (Zanzibar + Outbox)
    ├── tests/                           # Pytest Test Suite (97 Tests Passing)
    ├── docker-compose.yml               # Local Infrastructure (Redis 7, Postgres 16, Kafka)
    └── requirements.txt                 # Dependencies
```

### Granular Chapter Index (195 Pages)

- **Part I: Scaling & Ingress (Chapters 1–4)**
  - Ch 01: Scalability, Saturation & Queueing Theory ($L = \lambda W$, Amdahl's Law, USL)
  - Ch 02: Load Balancing & Modern Ingress (Layer 4 Maglev/IPVS DSR vs Layer 7 Envoy)
  - Ch 03: Caching Strategies & Edge Storage (Stale-Fill Invalidation Race, Watermarks, SingleFlight)
  - Ch 04: Content Delivery Networks & Global Edge Routing (Origin Shielding, Anycast POPs)

- **Part II: Distributed Data & Consistency (Chapters 5–10)**
  - Ch 05: Database Sharding & Partitioning (2D Grids, Scatter-Gather Amplification, Keyset Cursors)
  - Ch 06: Database Replication & High Availability (Async Replication Lag, Fencing Tokens)
  - Ch 07: Consistent Hashing (Virtual Nodes, Load Standard Deviation, Google Bounded Loads)
  - Ch 08: CAP Theorem in Practice (Network Partitions, Strict Quorums $R + W > N$)
  - Ch 09: PACELC Theorem (Normal-Mode Latency vs Partition Consistency)
  - Ch 10: Consistency Models (Linearizability, Sequential, Causal, Eventual Consistency)

- **Part III: Asynchronous Systems (Chapters 11–12)**
  - Ch 11: Kafka & Message Queues (Partition Logs, Cooperative Sticky Rebalance)
  - Ch 12: Event-Driven Architecture (Transactional Outbox Pattern, Debezium CDC, Consumer Inbox)

- **Part IV: Service Architecture & Edge (Chapters 13–15)**
  - Ch 13: Microservices Architecture (Fallacies of Distributed Computing, Service Mesh Proxies)
  - Ch 14: API Gateway Architecture (OAuth2 JWT Validation, Interceptor Chains, Guardrail Proxies)
  - Ch 15: Distributed Rate Limiting (Dual Token Bucket RPM/TPM, Redis Lua Server Time)

- **Part V: Resilience & Primitives (Chapters 16–19)**
  - Ch 16: Bloom Filters & Probabilistic Hashing (Kirsch-Mitzenmacher, MinHash Jaccard, LSH Banding)
  - Ch 17: Circuit Breaker Pattern (Atomic Single-Probe `HALF_OPEN`, Exponential Backoff + Jitter)
  - Ch 18: Saga Pattern & Distributed Transactions (Forward Actions vs Reverse Compensations)
  - Ch 19: Blob & Object Storage (Resumable Multipart Uploads, Safetensors, `mmap` vs GPUDirect)

- **Part VI: Quantitative System Design (Chapter 20)**
  - Ch 20: Back-of-the-Envelope Estimation (Binary vs Decimal Units, GPU VRAM & KV-Cache Sizing)

- **Part VII: Modern Distributed Primitives (Chapters 21–25)**
  - Ch 21: Distributed Vector Search (HNSW Proximity Graphs, BM25, Reciprocal Rank Fusion)
  - Ch 22: Consensus Protocols & Raft (Randomized Election Timeouts, Split-Vote Resolution)
  - Ch 23: Stream Processing & Apache Flink (Chandy-Lamport Snapshots, Punctuated Watermarks)
  - Ch 24: Distributed Authorization & Google Zanzibar (Relation Tuples, Userset Rewrites, Zookies)
  - Ch 25: Storage Engines: LSM-Trees vs B+Trees (Write Amplification, Leveled Compaction)

- **Part VIII: End-to-End Production System Design Workshops (Workshops A–F)**
  - Workshop A: Global E-Commerce & Flash Sales (100k RPS, Hash-Tagged Redis Cluster, Aurora DB)
  - Workshop B: Distributed Chat & Presence (50M Concurrent WebSockets, Socket Memory Math)
  - Workshop C: Global Video Streaming Platform (Tus Resumable Ingestion, S3 Lifecycle, CDN Shield)
  - Workshop D: Real-Time Ride-Hailing Service (Uber H3 Hexagonal Indexing, Atomic Match Locks)
  - Workshop E: Distributed LLM Serving Platform (vLLM PagedAttention, Continuous Batching, TP=8)
  - Workshop F: Multi-Tenant RAG & Agent Platform (Fail-Closed Zanzibar ReBAC, Outbox Tooling)

- **Part IX: Staff & Principal Interview Playbook & Appendices**
  - The Repeatable 9-Step HLD Whiteboard Method (45-Minute Pacing & Scored Rubrics)
  - Integrated Practice Bank (12 Staff-Level Real-World System Design Scenarios)
  - Appendix A: Systems & AI Infrastructure Glossary (72 Rigorously Defined Definitions)
  - Appendix B: 30-Day Deliberate Practice Curriculum (Weekly Milestones & Whiteboard Drills)

---

## 4. Laboratory Quickstart & Setup

### Requirements
- Python 3.11+
- Optional: Docker & Docker Compose (for live Redis 7, PostgreSQL 16, Kafka instances)

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone <repo-url>
cd Subject/High\ Level\ Design/HLD_Python_Labs
pip install -r requirements.txt
```

### 2. Execute the Test Suite
Run the comprehensive 97-test automated test suite:
```bash
pytest tests -v
```

Output:
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.0.0, pluggy-1.6.0
collected 97 items

tests/test_agent_rag_engine.py .............. [  7%] (7 passed)
tests/test_bloom_and_minhash.py ............. [ 14%] (7 passed)
tests/test_bm25_and_rrf.py .................. [ 20%] (6 passed)
tests/test_cache_aside_versioned.py ......... [ 26%] (6 passed)
tests/test_circuit_breaker.py ............... [ 37%] (10 passed)
tests/test_concurrency_limiter.py ........... [ 41%] (4 passed)
tests/test_dual_token_bucket.py ............. [ 48%] (7 passed)
tests/test_flash_sale_inventory.py .......... [ 60%] (12 passed)
tests/test_hash_ring.py ..................... [ 70%] (9 passed)
tests/test_paged_attention_simulator.py ..... [ 80%] (10 passed)
tests/test_saga_orchestrator.py ............. [ 85%] (5 passed)
tests/test_transactional_outbox.py .......... [ 91%] (6 passed)
tests/test_zanzibar_rebac.py ................ [100%] (8 passed)

============================= 97 passed in 1.47s ==============================
```

All 97 unit tests run in memory without requiring external daemon infrastructure.

### 3. Spin Up Local Infrastructure (Optional)
To test against real database and message broker containers:
```bash
docker-compose up -d
```
Spins up:
- **Redis 7** on port `6379`
- **PostgreSQL 16** on port `5432` (`hld_user` / `hld_password`)
- **Apache Kafka 7.5** on port `9092`

---

## 5. Educational Simulations vs Production Infrastructure

To ensure clear engineering integrity, the laboratory codebase strictly distinguishes between **educational in-memory simulations** and **production cloud infrastructure**:

| Laboratory Module | Educational Simulator Class | Production Contrast / Reference Class | Key Architectural Difference |
|---|---|---|---|
| `ch12_event_driven` | `InMemoryOutboxSimulator` | `PostgresTransactionalOutbox` | Simulator models ACID transactions with mutexes; production class details PostgreSQL MVCC, partial indexing on `WHERE status = 'PENDING'`, and CTE `FOR UPDATE SKIP LOCKED`. |
| `ch24_zanzibar_rebac` | `ZanzibarEngine` | Google Zanzibar Infrastructure | Simulator evaluates tuples via in-memory BFS with cycle detection; production Zanzibar utilizes globally distributed Spanner with TrueTime tokens (Zookies) and an offline Leopard reachability index. |
| `workshop_llm_serving` | `BlockManager` | vLLM C++ Engine & CUDA Kernels | Simulator models virtual memory paging, block mapping, and Copy-on-Write in pure Python; production vLLM executes custom CUDA kernels accessing non-contiguous HBM pages directly via warp lookup tables without CPU GIL delays. |
| `ch15_rate_limiter` | `DualTokenBucketLimiter` | API Gateway Rate Limiting Middleware | In-memory token bucket; production version provides Redis Lua scripts using Redis server-side `TIME` commands. |

---

## 6. Key Code Examples

### 1. Versioned Cache-Aside with Monotonic Watermark Key (`ch03_caching`)
```python
from ch03_caching.cache_aside_versioned import VersionedCacheAside, SimulatedDatabase

db = SimulatedDatabase()
db.write("item:100", {"price": 50})

cache = VersionedCacheAside(db)

# Cache miss fills cache with version 1
val = cache.get("item:100")

# Invalidation advances watermark key to v2 and deletes data key
cache.invalidate("item:100", watermark=2)

# A delayed reader attempting to write stale v1 is rejected!
rejected = cache.put_cache("item:100", {"price": 50}, version=1)
assert rejected is False
```

### 2. Thread-Safe Single-Probe Circuit Breaker (`ch17_circuit_breaker`)
```python
from ch17_circuit_breaker.circuit_breaker import CircuitBreaker, CircuitBreakerProbeInFlightException

cb = CircuitBreaker(failure_threshold=5, base_cooldown_seconds=10.0)

@cb
def call_external_payment_gateway():
    # Downstream network call
    return execute_remote_rpc()
```

### 3. Fail-Closed Google Zanzibar ReBAC Authorization (`ch24_zanzibar_rebac`)
```python
from ch24_zanzibar_rebac.zanzibar_rebac import ZanzibarEngine, RelationTuple

engine = ZanzibarEngine()
# doc:annual_report#viewer -> group:finance#member
engine.write_tuple(RelationTuple("doc", "annual_report", "viewer", "group:finance#member"))
# group:finance#member -> user:alice
engine.write_tuple(RelationTuple("group", "finance", "member", "user:alice"))

# Evaluates transitive group expansion:
assert engine.check(user="user:alice", relation="viewer", object_str="doc:annual_report") is True
assert engine.check(user="user:mallory", relation="viewer", object_str="doc:annual_report") is False
```

---

## 7. Audit & Verification Documents

For deep-dive technical evaluations, inspect the companion verification artifacts:

- **[HLD_Technical_Audit_Report.md](file:///C:/Users/Karthikeya%20Reddy/OneDrive%20-%20RITE/Desktop/Office%20Work/Subject/High%20Level%20Design/HLD_Technical_Audit_Report.md):** Comprehensive SRE engineering audit report detailing the resolution of issues 2.1 A through K with honest verification categories.
- **[HLD_PDF_QA_Report.md](file:///C:/Users/Karthikeya%20Reddy/OneDrive%20-%20RITE/Desktop/Office%20Work/Subject/High%20Level%20Design/HLD_PDF_QA_Report.md):** Publication QA report documenting 195 verified pages, typography hierarchies, and SVG blueprint clarity.
- **[HLD_Revision_Changelog.md](file:///C:/Users/Karthikeya%20Reddy/OneDrive%20-%20RITE/Desktop/Office%20Work/Subject/High%20Level%20Design/HLD_Revision_Changelog.md):** Granular changelog tracking the architectural evolution across all editions.

---

## 8. License & Attribution

Designed and maintained for advanced distributed systems and AI systems infrastructure engineering education. Developed for production-grade educational use.
