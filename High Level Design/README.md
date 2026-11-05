# High-Level Design for Python & AI Engineers
### Version 3.0: Definitive Learning Edition (`AI-Systems-Mastery`)

An authoritative, mathematically grounded, and code-verified curriculum in modern distributed systems, cloud resilience patterns, and AI systems infrastructure engineering.

---

## 1. What This Curriculum Teaches

**High-Level Design for Python & AI Engineers** bridges classic web-scale distributed systems with state-of-the-art AI systems infrastructure. Built for senior, staff, and principal engineers, it provides first-principles mental models, rigorous mathematics, and runnable Python implementations for:

- **Distributed Systems Foundations:** Little's Law ($L = \lambda W$), queuing saturation, L4/L7 ingress fabric, versioned cache-aside invalidation, database sharding geometry, replication topologies, consistent hash rings with virtual nodes, CAP/PACELC trade-offs, and consistency models (Linearizable to Eventual).
- **Asynchronous & Resilient Primitives:** Partitioned append-only commit logs (Kafka), Transactional Outbox with `FOR UPDATE SKIP LOCKED` poller, Kirsch-Mitzenmacher Bloom filters, MinHash & LSH banding, thread-safe single-probe circuit breakers, and orchestrated Sagas with reverse compensation logs.
- **Modern Distributed Engines:** Okapi BM25 and hybrid Reciprocal Rank Fusion (RRF), Raft consensus leader election, Apache Flink event-time watermarks, Google Zanzibar Relationship-Based Access Control (ReBAC), and LSM-Tree leveled compaction vs B+Trees.
- **AI Systems Infrastructure:** GPU HBM budget calculations ($M_{\text{weights}} + M_{\text{KV}} + M_{\text{activations}}$), vLLM PagedAttention virtual memory block allocation, Copy-on-Write (CoW) parallel sampling, Radix tree prefix caching, and fail-closed multi-tenant RAG agent platforms.
- **Whiteboard Interview Mastery:** The disciplined 9-step FAANG whiteboard interview method with 45-minute clock allocation rubrics, interviewer negotiation scripts, and a 30-day deliberate practice curriculum.

---

## 2. Master Textbook PDF

The complete, publication-grade textbook is included directly in the root of this repository:

📄 **[`HLD_Python_Master_Textbook_Final.pdf`](./HLD_Python_Master_Textbook_Final.pdf)**

- **Format:** 195 Pages, Letter Format, high-density professional typography
- **Visuals:** 31 publication-grade symmetrical vector SVG architectural blueprints
- **Structure:** 25 deep-dive core chapters, 6 full-system production blueprints (Workshops A–F), and the Staff/Principal Whiteboard Playbook & Practice Bank.

---

## 3. Python Laboratory Quickstart (Zero-DevOps Learner Path)

All laboratory exercises and simulations run in memory in pure Python without requiring Docker, external databases, message brokers, or cloud credentials.

### 1. Minimal Setup

```bash
# Navigate to the laboratory
cd HLD_Python_Labs

# Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install minimal dependencies
pip install -r requirements.txt
```

### 2. Run All Tests

Run the full automated test suite (139 tests across all 25 chapters and 6 workshops):

```bash
pytest -q
```

*Expected output:*
```
........................................................................ [ 51%]
...................................................................      [100%]
139 passed in 1.42s
```

All 139 tests execute and pass in under 2 seconds.

### 3. Run an Individual Chapter's Test

You can test any single chapter directly:

```bash
# Test Chapter 03 (Versioned Cache-Aside & SingleFlight)
pytest tests/test_cache_aside_versioned.py -q

# Test Chapter 01 (Vegas Adaptive Concurrency Limiter)
pytest tests/test_concurrency_limiter.py -q

# Test Chapter 24 (Google Zanzibar ReBAC Engine)
pytest tests/test_zanzibar_rebac.py -q

# Test Workshop E (vLLM PagedAttention KV-Cache Simulator)
pytest tests/test_paged_attention_simulator.py -q
```

To run individual reference solution exercises:

```bash
# Run all reference solution exercises
pytest tests/test_chapter_reference_solutions.py -v

# Run only Round-Robin load balancing (Chapter 02)
pytest tests/test_chapter_reference_solutions.py::test_round_robin_load_balancing -v
```

---

## 4. How to Find the Solution for Any Exercise

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

👉 **[TEXTBOOK_EXERCISE_SOLUTIONS.md](./TEXTBOOK_EXERCISE_SOLUTIONS.md)**

---

## 5. Chapter & Workshop Roadmap

```
High Level Design/
├── HLD_Python_Master_Textbook_Final.pdf  # The 195-Page Master Textbook
├── TEXTBOOK_EXERCISE_SOLUTIONS.md        # Granular Chapter-to-Script Index
├── HLD_Technical_Audit_Report.md        # Technical Audit & Systems Verification Report
├── HLD_PDF_QA_Report.md                 # Publication Quality Assurance Report
├── HLD_Revision_Changelog.md            # Version 3.0 Milestone Changelog
├── README.md                            # Repository Overview & Quickstart Guide
└── HLD_Python_Labs/                     # Executable Python Laboratory
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
    ├── chapter_reference_solutions.py   # Reference models for Chapters 02, 04-06, 08-11, 13-14, 19-20, 22-23, 25 & Workshops B-D
    └── tests/                           # Complete Pytest Test Suite (139 Tests Passing)
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

## 6. Educational Simulations vs Production Infrastructure

To ensure engineering integrity, this laboratory codebase explicitly separates **educational architecture simulators** from **production database and cluster engines**:

| Laboratory Module | Educational Simulator Class | Production Contrast / Reference Class | Key Architectural Difference |
|---|---|---|---|
| `ch03_caching` | `SingleFlight`, `VersionedCacheAside` | Distributed Redlock / Redis Cluster / Memcached Leases | Simulator uses process-local locks; production distributed systems require distributed locks, probabilistic early expiration (XFetch), or cluster lease tokens. |
| `ch12_event_driven` | `InMemoryOutboxSimulator` | `PostgresTransactionalOutbox` | Simulator models ACID transactions with mutexes; production class details PostgreSQL MVCC, partial indexing on `WHERE status = 'PENDING'`, and CTE `FOR UPDATE SKIP LOCKED`. |
| `ch17_circuit_breaker` | `CircuitBreaker` | Envoy Proxy / Service Mesh Sidecars | Simulator tracks process-local state; production deployments coordinate circuit breaking at the mesh proxy layer across fleets. |
| `ch18_saga_orchestrator` | `SagaOrchestrator`, `InMemorySagaLog` | Temporal / Cadence / AWS Step Functions | Simulator uses in-memory log; production orchestrators durably append state transitions to an external database or WAL. |
| `ch24_zanzibar_rebac` | `ZanzibarEngine` | Google Zanzibar Infrastructure | Simulator evaluates tuples via in-memory BFS with cycle detection; production Zanzibar utilizes globally distributed Spanner with TrueTime tokens (Zookies) and an offline Leopard reachability index. |
| `workshop_llm_serving` | `BlockManager` | vLLM C++ Engine & CUDA Kernels | Simulator models virtual memory paging, block mapping, and Copy-on-Write in pure Python; production vLLM executes custom CUDA kernels accessing non-contiguous HBM pages directly via warp lookup tables without CPU GIL delays. |
| `ch15_rate_limiter` | `DualTokenBucketLimiter` | API Gateway Rate Limiting Middleware | In-memory token bucket; production version provides Redis Lua scripts using Redis server-side `TIME` commands. |

---

## 7. Optional Infrastructure (Docker Compose)

For advanced learners wishing to verify live network integrations against real database and message broker daemons:

```bash
docker-compose up -d
```

This spins up:
- **Redis 7** on port `6379`
- **PostgreSQL 16** on port `5432` (`hld_user` / `hld_password`)
- **Apache Kafka 7.5** on port `9092`

*(Note: Docker is 100% optional. The core test suite and exercises run completely in memory without containers.)*

---

## 8. License & Attribution

Designed and maintained for advanced distributed systems and AI systems infrastructure engineering education. Developed as an educational architecture simulator and reference pattern.
