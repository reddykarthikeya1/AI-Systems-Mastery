# High-Level Design (HLD) Python Laboratory
### Version 4.0: Definitive Learning Edition

A practical, code-verified architecture laboratory and reference pattern codebase for modern distributed systems, cloud resilience patterns, and AI systems infrastructure.

---

## 1. Quickstart (Zero-DevOps Learner Path)

All laboratory exercises and simulations are self-contained and run in memory in pure Python. **No Docker, external database, or message broker is required** for the default learning path.

### Step 1: Environment Setup

```bash
# Navigate to the laboratory folder
cd HLD_Python_Labs

# Create an isolated virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install minimal test dependencies
pip install -r requirements.txt
```

### Step 2: Run All Tests

Verify that all 146 tests pass in memory across all chapters and workshops:

```bash
pytest -q
```

*Expected output:*
```
.................................................................................... [ 56%]
................................................................                     [100%]
146 passed in 2.21s
```

All 146 tests execute in under 3 seconds.

### Step 3: Run Individual Chapter Tests

Run tests for any specific chapter module:

```bash
# Chapter 01: Adaptive Concurrency Limiting (Little's Law & Vegas AIMD)
pytest tests/test_concurrency_limiter.py -q

# Chapter 03: Versioned Cache-Aside with Invalidation Metadata Persistence
pytest tests/test_cache_aside_versioned.py -q

# Chapter 07: Consistent Hash Ring with Virtual Nodes & Bounded Loads
pytest tests/test_hash_ring.py -q

# Chapter 12: Transactional Outbox Pattern & SKIP LOCKED Poller
pytest tests/test_transactional_outbox.py -q

# Chapter 15: Dual Token Bucket Rate Limiter (RPM + TPM)
pytest tests/test_dual_token_bucket.py -q

# Chapter 16: Kirsch-Mitzenmacher Bloom Filter vs MinHash & LSH
pytest tests/test_bloom_and_minhash.py -q

# Chapter 17: Thread-Safe Circuit Breaker with Atomic Single-Probe
pytest tests/test_circuit_breaker.py -q

# Chapter 18: Saga Orchestrator with Structured Logging & Async Compensations
pytest tests/test_saga_orchestrator.py -q

# Chapter 21: Distributed Search (Okapi BM25 + Dense Cosine + RRF)
pytest tests/test_bm25_and_rrf.py -q

# Chapter 24: Google Zanzibar ReBAC Engine with Cycle Detection
pytest tests/test_zanzibar_rebac.py -q

# Workshop A: Flash Sale Inventory Engine & 2-Phase Dual-Write State Machine
pytest tests/test_flash_sale_inventory.py -q

# Workshop E: vLLM PagedAttention KV-Cache Simulator & Radix Router
pytest tests/test_paged_attention_simulator.py -q

# Workshop F: Enterprise Multi-Tenant RAG Engine with Fail-Closed Zanzibar
pytest tests/test_agent_rag_engine.py -q
```

### Step 4: Run Chapter Reference Solutions

Core reference implementations (Smooth Weighted Round-Robin, 3-State Health Monitor, Hierarchical Rate Limiter, Little's Law, Chapters 02, 04–06, 08–11, 13–14, 19–20, 22–23, 25, and Workshops B–D) live in `chapter_reference_solutions.py`:

```bash
# Run all shared reference solutions (27 tests)
pytest tests/test_chapter_reference_solutions.py -v

# Run Smooth Weighted Round-Robin load balancer
pytest tests/test_chapter_reference_solutions.py::test_weighted_round_robin_distribution -v

# Run 3-State Backend Health Monitor (HEALTHY -> SUSPECT -> EJECTED)
pytest tests/test_chapter_reference_solutions.py::test_backend_health_state_transitions -v

# Run Little's Law exact concurrency calculation
pytest tests/test_chapter_reference_solutions.py::test_littles_law_concurrency_calculation -v

# Run Hierarchical Multi-Tier Rate Limiter (IP -> Tenant -> Global)
pytest tests/test_chapter_reference_solutions.py::test_hierarchical_rate_limiter_multilevel_enforcement -v

# Run Raft leader election quorum and majority test
pytest tests/test_chapter_reference_solutions.py::test_raft_election_requires_majority_and_one_vote_per_term -v

# Run Vector clock causal ordering and concurrency detection
pytest tests/test_chapter_reference_solutions.py::test_vector_clock_causal_order_and_concurrency -v
```

---

## 2. Repository Structure

```
HLD_Python_Labs/
├── ch01_scalability/
│   └── concurrency_limiter.py       # Little's Law, AIMD & TCP Vegas Adaptive Limiters
├── ch03_caching/
│   └── cache_aside_versioned.py     # Versioned Cache-Aside, Invalidation Metadata Persistence (PERSIST) & SingleFlight
├── ch07_consistent_hashing/
│   └── hash_ring.py                 # Consistent Hash Ring (vnodes) & Google Bounded Loads
├── ch12_event_driven/
│   └── transactional_outbox.py      # Transactional Outbox & SKIP LOCKED Concurrent Poller
├── ch15_rate_limiter/
│   └── dual_token_bucket.py         # Dual Token Bucket (RPM + TPM) for LLM Gateways
├── ch16_bloom_filter/
│   └── bloom_and_minhash.py         # Bloom Filter vs MinHash & LSH Deterministic Banding
├── ch17_circuit_breaker/
│   └── circuit_breaker.py           # Thread-Safe Circuit Breaker with Atomic Single-Probe HALF_OPEN
├── ch18_saga_orchestrator/
│   └── saga_orchestrator.py         # Orchestrated Saga Engine with Reverse Compensation Log
├── ch21_distributed_search/
│   └── bm25_and_rrf.py              # Okapi BM25 Lexical + Dense Cosine + Reciprocal Rank Fusion
├── ch24_zanzibar_rebac/
│   └── zanzibar_rebac.py            # Google Zanzibar ReBAC Graph Engine with Cycle Detection
├── workshop_ecommerce/
│   └── flash_sale_inventory.py      # Flash Sale Inventory: 2-Phase Dual-Write State Machine & PG Protection
├── workshop_llm_serving/
│   └── paged_attention_simulator.py # vLLM PagedAttention KV-Cache, Copy-on-Write & Radix Router
├── workshop_rag_agents/
│   └── agent_rag_engine.py          # Enterprise RAG Orchestrator (Zanzibar + Outbox + Hybrid Search)
├── chapter_reference_solutions.py   # Reference models (Weighted RR, Health Monitor, Hierarchical Limiter, Little's Law, etc.)
├── tests/                           # Complete Pytest test suite (146 tests across 14 modules, 100% passing)
├── docker-compose.yml               # Optional local infrastructure (Redis 7, Postgres 16, Kafka 7.5)
├── requirements.txt                 # Dependencies (pytest, cryptography, redis, psycopg2-binary)
└── README.md
```

### Complete Test Suite Inventory (146 Tests)

| Test Module | Chapter / Area | Test Count | Key Invariants Verified |
|---|---|---|---|
| `test_agent_rag_engine.py` | Workshop F | 7 | Fail-closed Zanzibar ReBAC, outbox intent before tool dispatch, cross-tenant isolation |
| `test_bloom_and_minhash.py` | Chapter 16 | 9 | Zero false negatives, Counting Bloom removal bounds, deterministic SHA-256 LSH banding |
| `test_bm25_and_rrf.py` | Chapter 21 | 6 | BM25 document re-indexing posting cleanup, `avgdl` consistency, dense cosine, RRF ranking |
| `test_cache_aside_versioned.py` | Chapter 03 | 9 | Generation fence, monotonic watermark, persistent metadata (`PERSIST`), SingleFlight stampede defense |
| `test_chapter_reference_solutions.py` | Ch 02, 04-06, 08-11, etc. | 27 | Smooth Weighted RR, 3-state health monitor, Little's Law concurrency, Hierarchical Limiter, Raft, LSM |
| `test_circuit_breaker.py` | Chapter 17 | 11 | Atomic single-probe CAS gate, 4xx exclusion, `asyncio.CancelledError` bypass, thread-isolated timeouts |
| `test_concurrency_limiter.py` | Chapter 01 | 4 | Little's Law queue delay inflation, AIMD backoff, Vegas gradient adjustment, SLO load shedding |
| `test_dual_token_bucket.py` | Chapter 15 | 7 | RPM + TPM dual quota, atomic rollback on partial rejection, Redis server-side `TIME` skew protection |
| `test_flash_sale_inventory.py` | Workshop A | 25 | 2-phase state machine, `PENDING_RECONCILIATION`, PostgreSQL rollback protection, ZSET expiry |
| `test_hash_ring.py` | Chapter 07 | 9 | Virtual node balance, deterministic salt probing on collision, Google Bounded-Load clockwise spillover |
| `test_paged_attention_simulator.py` | Workshop E | 12 | Virtual block tables, dynamic CoW parallel sampling, double-free validation, Radix prefix router |
| `test_saga_orchestrator.py` | Chapter 18 | 6 | Forward DAG execution, strict reverse compensation ($C_{k-1} \dots C_1$), async non-blocking execution |
| `test_transactional_outbox.py` | Chapter 12 | 6 | Dual-write elimination, CTE `FOR UPDATE SKIP LOCKED` concurrent polling, idempotent consumer inbox |
| `test_zanzibar_rebac.py` | Chapter 24 | 8 | Direct relation tuples, userset rewrite inheritance, BFS graph traversal with cycle detection |
| **Total** | | **146** | **100% Passing in ~2.21 Seconds** |

---

## 3. Decoupled Cache Invalidation & Metadata Persistence (`ch03_caching`)

### The Stale-Fill & Cold-Cache Invalidation Problem

In standard cache-aside:
1. **Reader A** misses in cache, begins querying the database, and fetches row version 1.
2. **Writer B** updates the database to row version 2 and invalidates the cache.
3. If the cache was cold (empty) or if invalidation merely deletes the key or invents versions, **Reader A** (delayed by a network jitter or GC pause) writes stale version 1 into the cache. The cache is now poisoned indefinitely!

### Finding 4.0-A: Metadata Persistence (`PERSIST` vs `EXPIRE`)

Prior heuristic approaches set an expiration on metadata keys (e.g. `EXPIRE watermark_key, ttl * 2`). Under production memory pressure or after extended data expiration:
- If `{entity}:v_watermark` and `{entity}:gen` expire, an arbitrarily delayed reader thread querying a slow database replica can awake and repopulate the cache with obsolete data.
- **The Version 4.0 Architectural Fix:** Invalidation metadata keys MUST be made permanently persistent using `PERSIST`. The volatile data key (`{entity}:data`) retains its TTL, while metadata keys (`{entity}:v_watermark` and `{entity}:gen`) are explicitly persisted via `PERSIST`. This guarantees that version fences survive data eviction and prevent stale-fill races forever.

### The Two-Tiered Solution: Generation Fence + Row-Version Watermark

1. **Monotonic Invalidation-Generation Fence (`{entity}:gen`)**:
   - Advanced on **every invalidation** (`INCR {entity}:gen`).
   - Invalidation removes `{entity}:data` and increments `{entity}:gen`.
   - **Crucially: Invalidation does NOT invent database row versions!**
2. **Monotonic Database Row Watermark (`{entity}:v_watermark`)**:
   - Strictly reflects observed database row versions.
3. **Reader Two-Tiered Validation**:
   - Reader samples the current generation fence **before** querying the DB: `captured_gen = cache.get_generation(key)`.
   - When attempting to write to cache (`put_cache`):
     - **Check 1 (Generation):** `captured_gen == current_gen` (verifies zero invalidations occurred while reading DB).
     - **Check 2 (Watermark):** `incoming_version >= current_watermark` (verifies version is not older than observed DB state).
   - If either check fails, the write is atomically **rejected** as stale.

### Production Redis Lua Scripts

#### Atomic Versioned Cache Fill with Metadata Persistence (`LUA_VERSIONED_SET`)

```lua
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- KEYS[3]: Generation key (e.g. record:{id}:gen)
-- ARGV[1]: Serialized value, ARGV[2]: Incoming Version, ARGV[3]: Captured Generation, ARGV[4]: TTL

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local gen_key = KEYS[3]
local val = ARGV[1]
local incoming_ver = tonumber(ARGV[2])
local captured_gen = tonumber(ARGV[3])
local ttl = tonumber(ARGV[4])

-- 1. Invalidation Generation Fence Check
local current_gen = tonumber(redis.call('GET', gen_key) or '0')
if captured_gen ~= current_gen then
    return 0 -- Rejected: Invalidation occurred while reader queried DB
end

-- 2. Monotonic Row-Version Watermark Check
local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
if incoming_ver >= current_watermark then
    redis.call('SET', data_key, val)
    if incoming_ver > current_watermark then
        redis.call('SET', watermark_key, incoming_ver)
    end
    if ttl and ttl > 0 then
        redis.call('EXPIRE', data_key, ttl)
    end
    -- Invalidation metadata MUST remain persistent to eliminate stale-fill windows across data-key expiration
    redis.call('PERSIST', watermark_key)
    redis.call('PERSIST', gen_key)
    return 1 -- Accepted
else
    return 0 -- Rejected: Stale row version
end
```

#### Atomic Safe Invalidation (`LUA_INVALIDATE`)

```lua
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- KEYS[3]: Generation key (e.g. record:{id}:gen)
-- ARGV[1]: New watermark version (optional, 0 to leave unchanged)

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local gen_key = KEYS[3]
local new_ver = tonumber(ARGV[1] or '0')

redis.call('DEL', data_key)
redis.call('INCR', gen_key) -- Advances generation fence atomically!
redis.call('PERSIST', gen_key)

if new_ver and new_ver > 0 then
    local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
    if new_ver > current_watermark then
        redis.call('SET', watermark_key, new_ver)
    end
    redis.call('PERSIST', watermark_key)
end
return 1
```

---

## 4. Key Laboratory Implementations

### 1. Modern Ingress & Load Balancing (`chapter_reference_solutions.py`)

#### Smooth Weighted Round-Robin (`WeightedRoundRobinBalancer`)
Implements the smooth weighted round-robin distribution algorithm (as popularized by Nginx). For backends with weights $W = \{\text{srv-a}: 4, \text{srv-b}: 2, \text{srv-c}: 1\}$, standard weighted round-robin clusters 4 consecutive requests to `srv-a`, inducing latency spikes. Smooth Weighted Round-Robin interleaves requests evenly ($a, b, a, c, a, b, a$) by tracking effective dynamic weights:

```python
from chapter_reference_solutions import WeightedRoundRobinBalancer

balancer = WeightedRoundRobinBalancer({"srv-a": 4, "srv-b": 2, "srv-c": 1})
selection = [balancer.choose() for _ in range(7)]
# Evenly dispersed distribution: ['srv-a', 'srv-b', 'srv-a', 'srv-c', 'srv-a', 'srv-b', 'srv-a']
```

#### 3-State Backend Health Monitor (`BackendHealthMonitor`)
Tracks backend health transitions through an explicit three-state finite state machine with recovery hysteresis:
- `HEALTHY`: Backend operational, receives normal routed traffic.
- `SUSPECT`: Backend encountered consecutive failures exceeding `suspect_threshold`. Still routable for soft fallback, but flagged for active synthetic probing.
- `EJECTED`: Failures exceeded `eject_threshold`. Stripped from `routable_backends()` completely.
- **Recovery Hysteresis:** Requires `recovery_threshold` consecutive successful probes to transition from `EJECTED` $\rightarrow$ `SUSPECT`, and further successes to transition `SUSPECT` $\rightarrow$ `HEALTHY`, eliminating route flapping under borderline network jitter.

```python
from chapter_reference_solutions import BackendHealthMonitor, BackendHealthState

monitor = BackendHealthMonitor(["srv-1", "srv-2"], suspect_threshold=2, eject_threshold=3, recovery_threshold=2)
monitor.record_failure("srv-1")
monitor.record_failure("srv-1") # State transitions to SUSPECT
assert monitor.state_of("srv-1") == BackendHealthState.SUSPECT

monitor.record_failure("srv-1") # State transitions to EJECTED
assert "srv-1" not in monitor.routable_backends()
```

### 2. Multi-Tier Hierarchical Rate Limiter (`chapter_reference_solutions.py`)

Enforces defense-in-depth quota management across three hierarchical tiers:
1. **IP Tier:** Prevents aggressive denial-of-service from individual IP addresses.
2. **Tenant Tier:** Restricts total API consumption per enterprise account.
3. **Global Tier:** Protects cluster-wide backend infrastructure and database thread pools.

**Atomic Rollback on Partial Rejection:** If a request satisfies IP and Tenant limits but breaches the Global capacity limit, consumed tokens are atomically rolled back at the lower tiers, preserving token consistency.

```python
from chapter_reference_solutions import HierarchicalRateLimiter

limiter = HierarchicalRateLimiter(
    global_capacity=100.0, global_refill_rate=10.0,
    tenant_capacity=20.0, tenant_refill_rate=2.0,
    ip_capacity=5.0, ip_refill_rate=1.0,
)

allowed, reason = limiter.acquire(tenant_id="tenant_acme", ip="192.168.1.1", tokens=1)
assert allowed is True
assert reason == "ALLOWED"
```

### 3. Concurrency Limiter & Little's Law (`ch01_scalability` & `chapter_reference_solutions.py`)

#### Exact Little's Law Concurrency Calculation
```python
from chapter_reference_solutions import littles_law_concurrency

# 2,000 RPS with 350ms mean latency -> exactly 700 concurrent in-flight requests
concurrency = littles_law_concurrency(arrival_rate_rps=2000.0, mean_latency_seconds=0.350)
assert concurrency == 700.0
```

#### Adaptive TCP Vegas Concurrency Limiter
Dynamically adjusts in-flight concurrency permits based on queue delay and smoothed round-trip time:
```python
from ch01_scalability.concurrency_limiter import VegasAdaptiveLimiter, ConcurrencyLimitExceeded

limiter = VegasAdaptiveLimiter(initial_limit=10.0, slo_latency_ms=200.0)
try:
    with limiter.acquire():
        response = call_downstream_service()
except ConcurrencyLimitExceeded:
    return "Service Saturated - Shedding Load (HTTP 429/503)"
```

### 4. Flash Sale 2-Phase Dual-Write State Machine (`workshop_ecommerce`)

Solves the dual-write consistency gap between high-throughput Redis reservations and authoritative PostgreSQL financial ledgers:
- **State Machine:** `HELD` $\rightarrow$ `CONFIRMED` / `RELEASED` / `EXPIRED` / `PENDING_RECONCILIATION`.
- **Finding 4.0-B (Ambiguous Database Timeout & Rollback Protection):**
  - If PostgreSQL reconciliation encounters an ambiguous network timeout during commit, the reservation transitions to `PENDING_RECONCILIATION` instead of rolling back.
  - Ordinary rollback is strictly forbidden while in `PENDING_RECONCILIATION`, preventing stock restoration while a committed order might exist in PostgreSQL.
  - A background reconciliation daemon queries PostgreSQL: if an order exists, the reservation is confirmed; if the transaction definitively aborted, stock is safely restored.

```python
from workshop_ecommerce.flash_sale_inventory import FlashSaleInventory, ReservationState

svc = FlashSaleInventory()
svc.initialize_stock("item_100", 10)
res = svc.reserve("item_100", "user_1", quantity=2, idempotency_key="order_tx_1")
assert res.success is True
```

### 5. Google Zanzibar ReBAC Engine (`ch24_zanzibar_rebac`)

Graph-based relationship authorization with cycle detection and fail-closed security:
```python
from ch24_zanzibar_rebac.zanzibar_rebac import ZanzibarEngine, RelationTuple

engine = ZanzibarEngine()
engine.write_tuple(RelationTuple("doc", "design_spec", "viewer", "group:engineers#member"))
engine.write_tuple(RelationTuple("group", "engineers", "member", "user:karthik"))

assert engine.check(user="user:karthik", relation="viewer", object_str="doc:design_spec") is True
assert engine.check(user="user:eve", relation="viewer", object_str="doc:design_spec") is False
```

### 6. vLLM PagedAttention & Radix Router (`workshop_llm_serving`)

Models virtual memory block allocation, dynamic Copy-on-Write branching, and Radix tree prefix routing:
```python
from workshop_llm_serving.paged_attention_simulator import BlockManager, RadixRouter

block_mgr = BlockManager(num_blocks=1024, block_size=16)
router = RadixRouter()

router.register_worker("worker_gpu_0", load=0.2)
router.insert_prefix([101, 2054, 2003], "worker_gpu_0")

best_worker = router.match_prefix([101, 2054, 2003, 1037])
assert best_worker == "worker_gpu_0"
```

---

## 5. Educational Simulators vs Production Infrastructure

| Laboratory Module | Educational Simulator Class | Production Reference Architecture | Key Architectural Differences |
|---|---|---|---|
| `ch02_load_balancing` | `WeightedRoundRobinBalancer`, `BackendHealthMonitor` | Envoy Proxy / Nginx / Maglev | In-process round-robin loops; production proxies utilize kernel eBPF / DPDK packet steering and multi-threaded health checking. |
| `ch03_caching` | `SingleFlight`, `VersionedCacheAside` | Redis Cluster / Memcached Leases / Envoy | Simulator uses process-local threading locks; distributed clusters require Redlock, probabilistic early expiration (XFetch), or cluster lease tokens. |
| `ch12_event_driven` | `InMemoryOutboxSimulator` | PostgreSQL + Debezium CDC + Kafka | Simulator models ACID boundaries with in-memory dicts; production uses PostgreSQL MVCC, partial indexes (`WHERE status = 'PENDING'`), CTE `FOR UPDATE SKIP LOCKED`, or Debezium WAL tailing. |
| `ch15_rate_limiter` | `HierarchicalRateLimiter`, `DualTokenBucketLimiter` | API Gateway Rate Limiting Middleware / Redis Lua | In-memory token bucket; production version provides Redis Lua scripts using Redis server-side `TIME` commands across multi-tiered keys. |
| `ch17_circuit_breaker` | `CircuitBreaker` | Envoy Proxy / Istio Service Mesh | Simulator manages process-local failure counters; production microservices delegate circuit breaking to sidecar proxies coordinating across thousands of instances. |
| `ch18_saga_orchestrator` | `SagaOrchestrator`, `InMemorySagaLog` | Temporal / Cadence / AWS Step Functions | Simulator stores logs in Python memory; production distributed orchestrators durably append state transitions to an external WAL/RDBMS before dispatching RPCs. |
| `ch24_zanzibar_rebac` | `ZanzibarEngine` | Google Zanzibar Infrastructure | Simulator evaluates tuples via in-memory BFS; production Zanzibar runs across globally distributed Spanner with TrueTime tokens (Zookies) and an offline Leopard reachability index. |
| `workshop_ecommerce` | `FlashSaleInventory` | Redis Cluster + Aurora PostgreSQL 2PC | Simulator implements two-phase state machine with `PENDING_RECONCILIATION`; production employs distributed cross-datacenter reconciliation workers. |
| `workshop_llm_serving` | `BlockManager` | vLLM Engine (C++ & CUDA Kernels) | Simulator models block allocation and CoW in pure Python; production vLLM executes custom C++/CUDA kernels reading non-contiguous GPU HBM pages directly inside warp lookup tables without GIL delays. |

---

## 6. Optional Infrastructure (Docker Compose)

For testing against real database and message broker containers:

```bash
docker-compose up -d
```

Spins up:
- **Redis 7** on `localhost:6379`
- **PostgreSQL 16** on `localhost:5432` (`hld_user` / `hld_password`)
- **Apache Kafka 7.5** on `localhost:9092`

---

## 7. Exercise & Solution Map

To map any textbook chapter or workshop to its corresponding laboratory script and test command, consult:

👉 **[`../TEXTBOOK_EXERCISE_SOLUTIONS.md`](../TEXTBOOK_EXERCISE_SOLUTIONS.md)**
