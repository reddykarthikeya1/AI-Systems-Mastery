# High-Level Design for Python & AI Engineers
### Version 4.0: Definitive Learning Edition (`AI-Systems-Mastery`)

An authoritative, mathematically grounded, and code-verified curriculum in modern distributed systems, cloud resilience patterns, and AI systems infrastructure engineering.

---

## 1. What This Curriculum Teaches: The Ten Curriculum Pillars

**High-Level Design for Python & AI Engineers** bridges classic web-scale distributed systems with modern AI systems infrastructure. Built for senior, staff, and principal engineers, it establishes rigorous mathematical foundations, verifiable concurrency invariants, and runnable Python implementations across ten foundational pillars:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           TEN CURRICULUM ARCHITECTURAL PILLARS                                    │
├──────────────────────────────────────────────────┬────────────────────────────────────────────────┤
│ Classical Distributed Systems Foundation         │ Modern AI Systems Infrastructure Bridge        │
├──────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ 1. Scalability, Queuing & Little's Law           │ LLM Generation Queuing, TTFT vs TPOT Saturation│
│ 2. Modern Ingress & Intelligent Traffic Routing  │ GPU Cluster Load Balancing & Prefix Affinity   │
│ 3. State Invalidation & SingleFlight Coalescing  │ Radix Tree Prefix Caching & KV-Cache Reuse     │
│ 4. Partitioning, Sharding & Consistent Topologies│ High-Dim Vector Sharding & Tensor Parallelism  │
│ 5. Replication Topologies & Epoch Fencing        │ Distributed Model Checkpointing & Weight Sync  │
│ 6. Consensus Protocols & Replicated State        │ Multi-Agent Swarm Consensus & Orchestration    │
│ 7. Asynchronous Logging & Transactional Outbox   │ Agent Tool Intent Streams & Async Token Bus    │
│ 8. Resilient Fault Isolation & Quota Engineering │ Context Window Token Buckets & GPU Protection  │
│ 9. Probabilistic Structures & Hybrid Search      │ Dense Vector Indices, HNSW Graphs & RRF Ranking│
│ 10. ReBAC Relationship Authorization & Sandboxing│ Enterprise Multi-Tenant RAG & Tool Isolation   │
└──────────────────────────────────────────────────┴────────────────────────────────────────────────┘
```

### Pillar 1: Scalability, Saturation Dynamics & Little's Law
- **Classical Foundation:** Little's Law ($L = \lambda W$), Universal Scalability Law (USL), queue saturation asymptotes, and Vegas adaptive concurrency limiting that senses queue latency inflation before packet drops occur.
- **AI Systems Bridge:** Translating request arrival rates into GPU High Bandwidth Memory (HBM) queue occupancy. Evaluating Time-to-First-Token (TTFT) queue delays versus Time-Per-Output-Token (TPOT) continuous batching saturation.

### Pillar 2: Modern Ingress & Intelligent Traffic Routing
- **Classical Foundation:** Layer 4 Maglev / IPVS Direct Server Return (DSR), Layer 7 Envoy service proxies, Smooth Weighted Round-Robin (Nginx algorithm) load balancing, and active 3-state health monitoring (`HEALTHY`, `SUSPECT`, `EJECTED`) with recovery hysteresis.
- **AI Systems Bridge:** KV-cache prefix-affinity routing in multi-node inference clusters. Dispatching incoming prompt tokens to GPU workers hosting matching cached prefix layers to eliminate redundant prefill computation.

### Pillar 3: State Invalidation, Caching & SingleFlight Coalescing
- **Classical Foundation:** Decoupled cache invalidation with monotonic generation fences and row-version watermarks. Permanent invalidation metadata persistence (`PERSIST`), Redis memory eviction policies (`volatile-lru` immunity vs `allkeys-lru` race recreation), bounded metadata lifecycle options (bounded epoch TTL, tombstone sweepers, dedicated metadata clusters), XFetch probabilistic early expiration, and `SingleFlight` mutex coalescing to annihilate dogpile stampedes.
- **AI Systems Bridge:** Radix tree prefix caching for generative LLMs, prompt KV-cache memory reuse, model weight caching across worker nodes, and thread-safe token streaming.

### Pillar 4: Partitioning, Sharding & Consistent Topologies
- **Classical Foundation:** Consistent hash rings with virtual nodes (vnodes), deterministic salt probing for token collision avoidance, Google Bounded-Load clockwise spillover routing, and 2D hash-range database sharding.
- **AI Systems Bridge:** High-dimensional vector partitioning across ANN graph indices, distributed tensor parallelism (TP) slicing weight matrices across intra-node NVLink, and pipeline parallelism (PP) stage partitioning.

### Pillar 5: Replication Topologies, Epochs & High Availability
- **Classical Foundation:** Semi-synchronous replication, replication lag mitigation, read-after-write consistency, read repair, and split-brain fencing using monotonically incremented epoch fencing tokens.
- **AI Systems Bridge:** Distributed model checkpoint synchronization across GPU clusters, multi-node parameter server architectures, and fault-tolerant weight broadcasting via NCCL ring-allreduce topologies.

### Pillar 6: Consensus Protocols & Replicated State Machines
- **Classical Foundation:** Raft consensus protocol mechanics: leader election, randomized election timeouts ($[T, 2T]$), split-vote resolution, log replication, and committed entry application.
- **AI Systems Bridge:** Multi-agent autonomous decision consensus, distributed coordination of stateful inference engines, and leader election for active-passive vector database ingestion orchestrators.

### Pillar 7: Asynchronous Logging, Event-Driven & Outbox Patterns
- **Classical Foundation:** Partitioned append-only commit logs (Kafka), cooperative sticky rebalancing, Transactional Outbox pattern with CTE `FOR UPDATE SKIP LOCKED` concurrent polling, and idempotent consumer inbox deduplication.
- **AI Systems Bridge:** Event-driven agent tool execution pipelines, asynchronous token delivery buses, persistent agent execution audit traces, and durable checkpoint logs for long-horizon multi-step reasoning.

### Pillar 8: Resilient Fault Isolation & Multi-Tier Quota Engineering
- **Classical Foundation:** Thread-safe circuit breakers with atomic single-probe `HALF_OPEN` gating, non-blocking asynchronous timeout isolation, and thread-safe `HierarchicalRateLimiter` (`threading.RLock`) with atomic multi-tier token enforcement (all-or-nothing check-then-deduct across Global, Tenant, and Client IP tiers).
- **AI Systems Bridge:** Context-window token bucket enforcement (Requests Per Minute + Tokens Per Minute) coupled with physical GPU memory protection via continuous batch preemption and KV-cache paging.

### Pillar 9: Probabilistic Data Structures & High-Dimensional Search
- **Classical Foundation:** Kirsch-Mitzenmacher dual-hashing Bloom filters (zero false negatives), Counting Bloom filter safe removal boundaries, MinHash Jaccard estimation, and deterministic SHA-256 LSH banding.
- **AI Systems Bridge:** Okapi BM25 sparse lexical search fused with dense vector cosine embeddings via Reciprocal Rank Fusion (RRF), and Hierarchical Navigable Small World (HNSW) logarithmic graph proximity search.

### Pillar 10: Relationship-Based Authorization & Sandboxed Execution
- **Classical Foundation:** Google Zanzibar Relationship-Based Access Control (ReBAC): relation tuples, userset rewrites, directed graph BFS traversal with cycle detection, and fail-closed security invariants.
- **AI Systems Bridge:** Multi-tenant RAG security gates preventing cross-tenant document chunk leakage into LLM contexts, sandboxed tool dispatching via Firecracker microVMs, and cryptographically verified agent action boundaries.

---

## 2. Master Textbook PDF

The complete, publication-grade textbook is included directly in the root of this repository:

📄 **[`HLD_Python_Master_Textbook_Final.pdf`](./HLD_Python_Master_Textbook_Final.pdf)**

- **Format:** Publication-grade US Letter format ($8.5 \times 11\text{ inches}$), high-density professional typography
- **Visuals:** 53 publication-grade symmetrical vector SVG architectural blueprints
- **Pedagogical Structure:** 25 deep-dive core chapters + 4 foundational & advanced chapters (Pillars 1, 2, 9, 10), 6 full-system production blueprints (Workshops A–F), and the Staff/Principal Whiteboard Playbook & Practice Bank.
- **Callout Cards:** 4 standardized pedagogical containers (Mental Models, Architectural Clinics, AI Infrastructure Lens, and Production Warnings).

---

## 3. The 17-Part Architectural Structure for All 6 Workshops

Every production workshop in Version 4.0 follows a rigorous, uniform **17-part architectural blueprint** designed to match the depth demanded in Staff and Principal system design evaluations:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       THE 17-PART WORKSHOP ARCHITECTURAL BLUEPRINT                       │
├─────────────────────────────────────────────┬───────────────────────────────────────────┤
│ 1. Executive Summary & Problem Framing      │ 10. Cross-Service Sagas & Distributed Tx  │
│ 2. Scale & Workload Estimation (Math)       │ 11. Security, Tenancy & ReBAC AuthZ       │
│ 3. High-Level Architecture & Topology       │ 12. Observability, Telemetry & SLOs       │
│ 4. Ingress, Routing & Edge Acceleration     │ 13. Failure Modes & Disaster Recovery     │
│ 5. Domain Data Model & Storage Engines      │ 14. Anti-Patterns & Post-Mortem Clinics   │
│ 6. Caching Strategy & Invalidation Dynamics │ 15. AI Infrastructure Lens & GPU Coupling │
│ 7. Concurrency Control & State Machines     │ 16. Pure-Python Lab Verification & Tests  │
│ 8. Partitioning & Consistent Topologies     │ 17. Staff Whiteboard Defense Script       │
│ 9. Asynchronous Pipelines & Outbox Pattern  │                                           │
└─────────────────────────────────────────────┴───────────────────────────────────────────┘
```

### Applied Across All 6 Production Workshops:

1. **Workshop A: Global E-Commerce & Flash Sale Inventory**
   - *Scale & Challenge:* 100,000 peak checkout RPS, severe overselling risks, dual-write crash windows.
   - *Core Architecture:* Hash-tagged Redis Cluster Lua reservations, ZSET expiration indexing, PostgreSQL authoritative financial ledger reconciliation, two-phase dual-write state machine (`HELD` $\rightarrow$ `PENDING_CONFIRMATION` $\rightarrow$ `CONFIRMED` / `RELEASED` / `EXPIRED` / `PENDING_RECONCILIATION`), ordinary rollback prohibition while pending reconciliation, and asynchronous background reconciliation workers.
2. **Workshop B: Distributed Real-Time Chat & Presence Fabric**
   - *Scale & Challenge:* 50 Million concurrent WebSockets, socket memory saturation ($1.5\text{ TB}$ kernel RAM), connection churn.
   - *Core Architecture:* Epoll-driven Gateway tier, Redis Pub/Sub distributed message bus, Cassandra wide-column history log, and heartbeat presence tracking with auto-expiring TTLs.
3. **Workshop C: Global Video Streaming & Resumable Ingestion Platform**
   - *Scale & Challenge:* Petabyte-scale uploads, flaky client connections, global CDN egress bandwidth costs.
   - *Core Architecture:* Tus resumable upload protocol, direct S3 chunked uploads with SHA-256 ETags, asynchronous AWS Batch transcoding pipelines, and multi-tier CDN Origin Shielding.
4. **Workshop D: Real-Time Geospatial Ride-Hailing Dispatch Engine**
   - *Scale & Challenge:* Millions of moving drivers, continuous GPS pings, high-concurrency dispatch races.
   - *Core Architecture:* Uber H3 hexagonal geospatial indexing (resolution 8 cells), Redis spatial candidate indexing, distributed mutex match locks, and optimistic PostgreSQL driver booking updates.
5. **Workshop E: Distributed LLM Serving Platform (vLLM & PagedAttention)**
   - *Scale & Challenge:* GPU High Bandwidth Memory fragmentation, dynamic batching latency, multi-turn prompt reuse.
   - *Core Architecture:* vLLM PagedAttention virtual memory block manager, dynamic Copy-on-Write (CoW) branching, continuous batching scheduler, and Radix tree prefix router across an 8-GPU tensor-parallel cluster.
6. **Workshop F: Multi-Tenant RAG & Autonomous Agent Platform**
   - *Scale & Challenge:* Cross-tenant data exfiltration, hallucinated tool calls, non-deterministic side effects.
   - *Core Architecture:* Authoritative fail-closed Google Zanzibar ReBAC authorization gate, Okapi BM25 + dense vector cosine hybrid search with Reciprocal Rank Fusion (RRF), 4-stage Transactional Outbox tool execution, and Firecracker microVM sandboxing.

---

## 4. Python Laboratory Quickstart (Zero-DevOps Learner Path)

The laboratory codebase is engineered for **immediate execution without infrastructure friction**:

> [!NOTE]
> **The Zero-DevOps Principle:** All 170 laboratory tests and architectural models run in memory in pure Python 3.11+. No Docker containers, PostgreSQL servers, Redis instances, Kafka clusters, or cloud service credentials are required. Simulated backends provide high-fidelity modeling of thread contention, atomic CAS gates, Lua scripting semantics, network timeouts, and disk compactions.

### 1. Minimal Setup

```bash
# Navigate to the laboratory directory
cd HLD_Python_Labs

# Create and activate an isolated virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install minimal test dependencies
pip install -r requirements.txt
```

### 2. Run All Tests

Run the complete automated verification test suite (170 tests across 14 modules, 25 chapters, and 6 workshops):

```bash
pytest -q
```

*Expected output:*
```
170 passed in 2.97s
```

All 170 tests execute deterministically and pass in under 3 seconds.

### 3. Run Specific Component Tests

Test newly integrated and advanced architectural components directly:

```bash
# Run Load Balancers, Health Monitors & Hierarchical Rate Limiters (Chapter 02, 14, 15)
pytest tests/test_chapter_reference_solutions.py -v

# Run Smooth Weighted Round-Robin distribution test
pytest tests/test_chapter_reference_solutions.py::test_weighted_round_robin_distribution -v

# Run 3-State Backend Health Monitor transition test (HEALTHY -> SUSPECT -> EJECTED)
pytest tests/test_chapter_reference_solutions.py::test_backend_health_state_transitions -v

# Run Little's Law exact concurrency derivation test
pytest tests/test_chapter_reference_solutions.py::test_littles_law_concurrency_calculation -v

# Run Hierarchical Multi-Tier Rate Limiter test (IP -> Tenant -> Global)
pytest tests/test_chapter_reference_solutions.py::test_hierarchical_rate_limiter_multilevel_enforcement -v

# Run Versioned Cache-Aside with Invalidation Metadata Persistence (Chapter 03)
pytest tests/test_cache_aside_versioned.py -v

# Run Flash Sale Inventory with 2-Phase Dual-Write State Machine (Workshop A)
pytest tests/test_flash_sale_inventory.py -v

# Run vLLM PagedAttention KV-Cache Simulator (Workshop E)
pytest tests/test_paged_attention_simulator.py -v

# Run Enterprise Multi-Tenant RAG Engine with Fail-Closed Zanzibar (Workshop F)
pytest tests/test_agent_rag_engine.py -v
```

---

## 5. How to Find the Solution for Any Exercise

Each chapter in the textbook presents architectural challenges, concurrency hazards, and design exercises. Follow this simple 4-step workflow:

```
[1. Read Chapter in PDF] ──> [2. Attempt Exercise] ──> [3. Open Solution in HLD_Python_Labs] ──> [4. Run pytest & Inspect]
```

1. **Read the chapter** in [`HLD_Python_Master_Textbook_Final.pdf`](./HLD_Python_Master_Textbook_Final.pdf).
2. **Attempt the exercise** at the end of the chapter on paper or in code.
3. **Open the referenced solution** script inside `HLD_Python_Labs/` indicated on the chapter's Revision Summary sheet.
4. **Run the companion pytest test** to verify invariants, explore edge cases, and inspect assertions.

### Direct Exercise-to-Solution Map

For the complete, granular index mapping every single chapter and workshop to its runnable solution script and test command, consult:

👉 **[`TEXTBOOK_EXERCISE_SOLUTIONS.md`](./TEXTBOOK_EXERCISE_SOLUTIONS.md)**

---

## 6. Chapter & Workshop Roadmap

```
High Level Design/
├── HLD_Python_Master_Textbook_Final.pdf  # The 237-Page Master Textbook (10.57 MB / 11,082,406 bytes)
├── TEXTBOOK_EXERCISE_SOLUTIONS.md        # Granular Chapter-to-Script Index & Solutions
├── HLD_Technical_Audit_Report.md        # Version 4.0 Technical Audit & Systems Verification Report
├── HLD_PDF_QA_Report.md                 # Publication Quality Assurance & Layout Report
├── HLD_Revision_Changelog.md            # Version 4.0.0 Milestone Changelog
├── README.md                            # Repository Overview & Quickstart Guide
└── HLD_Python_Labs/                     # Executable Python Laboratory
    ├── ch01_scalability/                # Little's Law, AIMD & Vegas Adaptive Limiters
    ├── ch03_caching/                    # Versioned Cache-Aside, Invalidation Metadata Persistence & SingleFlight
    ├── ch07_consistent_hashing/         # Murmur/SHA-256 Hash Ring & Google Bounded Loads
    ├── ch12_event_driven/               # Transactional Outbox & SKIP LOCKED Poller
    ├── ch15_rate_limiter/               # Dual Token Bucket (RPM + TPM) for LLM Gateways
    ├── ch16_bloom_filter/               # Bloom Filter vs MinHash & LSH Banding
    ├── ch17_circuit_breaker/            # Circuit Breaker with Atomic Single-Probe HALF_OPEN
    ├── ch18_saga_orchestrator/          # Saga Orchestrator with Structured Logging & Async
    ├── ch21_distributed_search/         # Okapi BM25 Lexical + Dense Cosine + RRF
    ├── ch24_zanzibar_rebac/             # Google Zanzibar ReBAC Engine with Cycle Detection
    ├── workshop_ecommerce/              # Flash Sale Redis Inventory, 2-Phase Dual-Write & Postgres
    ├── workshop_llm_serving/            # vLLM PagedAttention KV-Cache, CoW & Radix Router
    ├── workshop_rag_agents/             # Enterprise RAG Orchestrator (Zanzibar + Outbox)
    ├── chapter_reference_solutions.py   # Reference models (Weighted RR, Health Monitor, Hierarchical Limiter, etc.)
    └── tests/                           # Complete Pytest Test Suite (170 Tests Passing)
```

### Granular Chapter Index (237 Pages)

- **Part I: Scaling & Ingress (Chapters 1–4)**
  - Ch 01: Scalability, Saturation & Queueing Theory ($L = \lambda W$, Amdahl's Law, USL, Little's Law exact derivation)
  - Ch 02: Load Balancing & Modern Ingress (Layer 4 Maglev/IPVS DSR vs Layer 7 Envoy, Smooth Weighted Round-Robin, 3-State Health Monitor)
  - Ch 03: Caching Strategies & Edge Storage (Stale-Fill Invalidation Race, Persistent Metadata Fences, Watermarks, SingleFlight)
  - Ch 04: Content Delivery Networks & Global Edge Routing (Origin Shielding, Anycast POPs)

- **Part II: Distributed Data & Consistency (Chapters 5–10)**
  - Ch 05: Database Sharding & Partitioning (2D Grids, Scatter-Gather Amplification, Keyset Cursors)
  - Ch 06: Database Replication & High Availability (Async Replication Lag, Read Repair, Fencing Tokens)
  - Ch 07: Consistent Hashing (Virtual Nodes, Load Standard Deviation, Google Bounded Loads)
  - Ch 08: CAP Theorem in Practice (Network Partitions, Strict Quorums $R + W > N$)
  - Ch 09: PACELC Theorem (Normal-Mode Latency vs Partition Consistency)
  - Ch 10: Consistency Models (Linearizability, Sequential, Causal, Eventual Consistency, Vector Clocks)

- **Part III: Asynchronous Systems (Chapters 11–12)**
  - Ch 11: Kafka & Message Queues (Partition Logs, Cooperative Sticky Rebalance)
  - Ch 12: Event-Driven Architecture (Transactional Outbox Pattern, Debezium CDC, Consumer Inbox Deduplication)

- **Part IV: Service Architecture & Edge (Chapters 13–15)**
  - Ch 13: Microservices Architecture (Fallacies of Distributed Computing, Service Mesh Proxies)
  - Ch 14: API Gateway Architecture (OAuth2 JWT Validation, Interceptor Chains, Guardrail Proxies)
  - Ch 15: Distributed Rate Limiting (Hierarchical Multi-Tier Limiting, Dual Token Bucket RPM/TPM, Redis Lua Server Time)

- **Part V: Resilience & Primitives (Chapters 16–19)**
  - Ch 16: Bloom Filters & Probabilistic Hashing (Kirsch-Mitzenmacher, Counting Bloom Safety, MinHash Jaccard, LSH Banding)
  - Ch 17: Circuit Breaker Pattern (Atomic Single-Probe `HALF_OPEN`, Exponential Backoff + Jitter, Async Cancellation Safety)
  - Ch 18: Saga Pattern & Distributed Transactions (Forward Actions vs Reverse Compensations, Structured Audit Logging)
  - Ch 19: Blob & Object Storage (Resumable Multipart Uploads, Safetensors, `mmap` vs GPUDirect)

- **Part VI: Quantitative System Design (Chapter 20)**
  - Ch 20: Back-of-the-Envelope Estimation (Binary vs Decimal Units, GPU VRAM & KV-Cache Sizing)

- **Part VII: Modern Distributed Primitives (Chapters 21–25)**
  - Ch 21: Distributed Vector Search (HNSW Proximity Graphs, Okapi BM25, Reciprocal Rank Fusion)
  - Ch 22: Consensus Protocols & Raft (Randomized Election Timeouts, Split-Vote Resolution, Heartbeats)
  - Ch 23: Stream Processing & Apache Flink (Chandy-Lamport Snapshots, Punctuated Watermarks)
  - Ch 24: Distributed Authorization & Google Zanzibar (Relation Tuples, Userset Rewrites, Zookies, Cycle Detection)
  - Ch 25: Storage Engines: LSM-Trees vs B+Trees (Write Amplification, Leveled Compaction, MemTable Flushing)

- **Part VIII: End-to-End Production System Design Workshops (Workshops A–F)**
  - Workshop A: Global E-Commerce & Flash Sales (100k RPS, Hash-Tagged Redis Cluster, 2-Phase State Machine, Aurora DB)
  - Workshop B: Distributed Chat & Presence (50M Concurrent WebSockets, Socket Memory Math, Redis Pub/Sub)
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

## 7. Educational Simulations vs Production Infrastructure

To ensure engineering integrity, this laboratory codebase explicitly separates **educational architecture simulators** from **production database and cluster engines**:

| Laboratory Module | Educational Simulator Class | Production Contrast / Reference Class | Key Architectural Difference |
|---|---|---|---|
| `ch02_load_balancing` | `WeightedRoundRobinBalancer`, `BackendHealthMonitor` | Envoy Proxy / Nginx / Maglev | Simulator runs in-process round-robin loops; production proxies utilize kernel eBPF / DPDK packet steering and multi-threaded health checking. |
| `ch03_caching` | `SingleFlight`, `VersionedCacheAside` | Distributed Redlock / Redis Cluster / Memcached Leases | Simulator uses process-local locks and Lua scripts; production clusters require persistent metadata (`PERSIST`) under `volatile-lru` eviction (to prevent `allkeys-lru` metadata eviction race recreation) with bounded epoch TTLs, distributed locks, or cluster lease tokens. |
| `ch12_event_driven` | `InMemoryOutboxSimulator` | `PostgresTransactionalOutbox` | Simulator models ACID transactions with mutexes; production class details PostgreSQL MVCC, partial indexing on `WHERE status = 'PENDING'`, and CTE `FOR UPDATE SKIP LOCKED`. |
| `ch15_rate_limiter` | `HierarchicalRateLimiter`, `DualTokenBucketLimiter` | API Gateway Rate Limiting Middleware / Redis Lua | Thread-safe in-memory token bucket with internal `threading.RLock()` and atomic multi-tier token enforcement; production version provides Redis Lua scripts using Redis server-side `TIME` commands across multi-tiered keys. |
| `ch17_circuit_breaker` | `CircuitBreaker` | Envoy Proxy / Service Mesh Sidecars | Simulator tracks process-local state with atomic CAS gates; production deployments coordinate circuit breaking at the mesh proxy layer across fleets. |
| `ch18_saga_orchestrator` | `SagaOrchestrator`, `InMemorySagaLog` | Temporal / Cadence / AWS Step Functions | Simulator uses in-memory log; production orchestrators durably append state transitions to an external database or WAL. |
| `ch24_zanzibar_rebac` | `ZanzibarEngine` | Google Zanzibar Infrastructure | Simulator evaluates tuples via in-memory BFS with cycle detection; production Zanzibar utilizes globally distributed Spanner with TrueTime tokens (Zookies) and an offline Leopard reachability index. |
| `workshop_ecommerce` | `FlashSaleInventory` | Redis Cluster + Aurora PostgreSQL 2PC | Simulator implements two-phase state machine (`HELD` $\rightarrow$ `PENDING_CONFIRMATION` $\rightarrow$ `CONFIRMED` / `RELEASED` / `EXPIRED` / `PENDING_RECONCILIATION`) with ordinary rollback strictly prohibited while in `PENDING_RECONCILIATION`; production employs distributed cross-datacenter reconciliation workers. |
| `workshop_llm_serving` | `BlockManager` | vLLM C++ Engine & CUDA Kernels | Simulator models virtual memory paging, block mapping, and Copy-on-Write in pure Python; production vLLM executes custom CUDA kernels accessing non-contiguous HBM pages directly via warp lookup tables without CPU GIL delays. |

---

## 8. Optional Infrastructure (Docker Compose)

For advanced learners wishing to verify live network integrations against real database and message broker daemons:

```bash
docker-compose up -d
```

This spins up:
- **Redis 7** on port `6379`
- **PostgreSQL 16** on port `5432` (`hld_user` / `hld_password`)
- **Apache Kafka 7.5** on port `9092`

*(Note: Docker is 100% optional. The core test suite of 170 tests and all exercises run completely in memory without containers.)*

---

## 9. License & Attribution

Designed and maintained for advanced distributed systems and AI systems infrastructure engineering education. Developed as an educational architecture simulator and reference pattern.
