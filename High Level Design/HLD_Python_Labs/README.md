# High-Level Design (HLD) Python Laboratory

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

Verify that all 124 unit tests pass in memory across all chapters and workshops:

```bash
pytest -q
```

*Expected output:*
```
........................................................................ [ 58%]
....................................................                     [100%]
124 passed in 1.45s
```

All 124 unit tests execute in ~1.5 seconds.

### Step 3: Run Individual Chapter Tests

Run tests for any specific chapter module:

```bash
# Chapter 03: Versioned Cache-Aside & SingleFlight
pytest tests/test_cache_aside_versioned.py -q

# Chapter 01: Adaptive Concurrency Limiting (Little's Law)
pytest tests/test_concurrency_limiter.py -q

# Chapter 07: Consistent Hash Ring with Virtual Nodes
pytest tests/test_hash_ring.py -q

# Chapter 12: Transactional Outbox Pattern
pytest tests/test_transactional_outbox.py -q

# Chapter 15: Dual Token Bucket Rate Limiter
pytest tests/test_dual_token_bucket.py -q

# Chapter 17: Thread-Safe Circuit Breaker
pytest tests/test_circuit_breaker.py -q

# Chapter 18: Saga Orchestrator with Compensations
pytest tests/test_saga_orchestrator.py -q

# Chapter 21: Distributed Search (BM25 + Dense RRF)
pytest tests/test_bm25_and_rrf.py -q

# Chapter 24: Google Zanzibar ReBAC Engine
pytest tests/test_zanzibar_rebac.py -q

# Workshop A: Flash Sale Inventory Engine
pytest tests/test_flash_sale_inventory.py -q

# Workshop E: vLLM PagedAttention KV-Cache Simulator
pytest tests/test_paged_attention_simulator.py -q

# Workshop F: Enterprise Multi-Tenant RAG Engine
pytest tests/test_agent_rag_engine.py -q
```

### Step 4: Run Chapter Reference Solutions

Chapters with focused reference architectures (Chapters 02, 04–06, 08–11, 13–14, 19–20, 22–23, 25, and Workshops B–D) live in `chapter_reference_solutions.py`:

```bash
# Run all shared reference solutions
pytest tests/test_chapter_reference_solutions.py -v

# Run an individual test case:
pytest tests/test_chapter_reference_solutions.py::test_round_robin_load_balancing -v
pytest tests/test_chapter_reference_solutions.py::test_vector_clock_causal_order_and_concurrency -v
pytest tests/test_chapter_reference_solutions.py::test_raft_election_requires_majority_and_one_vote_per_term -v
```

---

## 2. Repository Structure

```
HLD_Python_Labs/
├── ch01_scalability/
│   └── concurrency_limiter.py       # Little's Law, AIMD & TCP Vegas Adaptive Limiters
├── ch03_caching/
│   └── cache_aside_versioned.py     # Versioned Cache-Aside, Generation Fence & SingleFlight
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
│   └── flash_sale_inventory.py      # Redis Cluster Flash Sale Inventory Reservation & DB Reconciliation
├── workshop_llm_serving/
│   └── paged_attention_simulator.py # vLLM PagedAttention KV-Cache, Copy-on-Write & Radix Router
├── workshop_rag_agents/
│   └── agent_rag_engine.py          # Enterprise RAG Orchestrator (Zanzibar + Outbox + Hybrid Search)
├── chapter_reference_solutions.py   # Reference models for Chapters 02, 04-06, 08-11, 13-14, 19-20, 22-23, 25 & Workshops B-D
├── tests/                           # Complete Pytest unit test suite (124 tests across 14 modules)
├── docker-compose.yml               # Optional local infrastructure (Redis 7, Postgres 16, Kafka)
├── requirements.txt                 # Dependencies
└── README.md
```

---

## 3. Decoupled Cache Invalidation Architecture (`ch03_caching`)

### The Stale-Fill & Cold-Cache Invalidation Problem

In standard cache-aside:
1. **Reader A** misses in cache, begins querying the database, and fetches row version 1.
2. **Writer B** updates the database to row version 2 and invalidates the cache.
3. If the cache was cold (empty) or if invalidation merely deletes the key or invents versions, **Reader A** (delayed by a network jitter or GC pause) writes stale version 1 into the cache. The cache is now poisoned indefinitely!

### The Two-Tiered Solution: Generation Fence + Row-Version Watermark

To unconditionally eliminate both stale fills and cold-cache invalidation races, the architecture decouples cache metadata into two independent tracking keys:

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

### Python Code Example

```python
from ch03_caching.cache_aside_versioned import VersionedCacheAside, SimulatedDatabase

db = SimulatedDatabase()
db.write("item:100", {"price": 50, "stock": 10}) # Creates row version 1

cache = VersionedCacheAside(db)

# 1. Normal read populates cache at version 1, generation 0
val = cache.get("item:100")
assert val == {"price": 50, "stock": 10}

# 2. Delayed Reader begins read and captures generation 0
captured_gen = cache.get_generation("item:100") # captured_gen = 0
db_row, db_ver = db.read("item:100")            # reads version 1

# 3. Concurrent Writer updates DB to version 2 and invalidates cache
db.write("item:100", {"price": 45, "stock": 9})  # DB now at version 2
cache.invalidate("item:100")                     # Deletes data, advances gen to 1!

# 4. Delayed Reader attempts to write stale version 1 using captured generation 0:
# REJECTED! Generation fence mismatch (captured_gen 0 != current_gen 1)
accepted = cache.put_cache("item:100", db_row, version=db_ver, captured_gen=captured_gen)
assert accepted is False
assert cache.stale_fill_rejections == 1
```

### Production Redis Lua Scripts

#### Atomic Versioned Cache Fill (`LUA_VERSIONED_SET`)

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
        redis.call('EXPIRE', watermark_key, ttl * 2)
        redis.call('EXPIRE', gen_key, ttl * 2)
    end
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

if new_ver and new_ver > 0 then
    local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
    if new_ver > current_watermark then
        redis.call('SET', watermark_key, new_ver)
    end
end
return 1
```

---

## 4. Key Laboratory Implementations

### 1. Concurrency Limiter & Little's Law (`ch01_scalability`)
Adaptive TCP Vegas-style concurrency limiter that dynamically adjusts max in-flight permits based on queue delay and smoothed RTT:
```python
from ch01_scalability.concurrency_limiter import VegasAdaptiveLimiter, ConcurrencyLimitExceeded

limiter = VegasAdaptiveLimiter(initial_limit=10.0, slo_latency_ms=200.0)
try:
    with limiter.acquire():
        # Execute latency-critical RPC
        response = call_downstream_service()
except ConcurrencyLimitExceeded:
    # Shed load with HTTP 429 / 503
    return "Service Saturated - Shedding Load"
```

### 2. Dual Token Bucket Rate Limiter (`ch15_rate_limiter`)
Simultaneously enforces request limits (RPM) and token volume (TPM) for LLM gateways with all-or-nothing rollback:
```python
from ch15_rate_limiter.dual_token_bucket import DualTokenBucketLimiter

limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=10_000.0)
result = limiter.acquire(client_id="agent_pool_1", tokens_requested=1200)
if not result.allowed:
    print(f"Rate limited: {result.reason}. Retry after {result.retry_after_seconds:.2f}s")
```

### 3. Google Zanzibar ReBAC Engine (`ch24_zanzibar_rebac`)
Graph-based relationship authorization with cycle detection and fail-closed security:
```python
from ch24_zanzibar_rebac.zanzibar_rebac import ZanzibarEngine, RelationTuple

engine = ZanzibarEngine()
engine.write_tuple(RelationTuple("doc", "design_spec", "viewer", "group:engineers#member"))
engine.write_tuple(RelationTuple("group", "engineers", "member", "user:karthik"))

assert engine.check(user="user:karthik", relation="viewer", object_str="doc:design_spec") is True
assert engine.check(user="user:eve", relation="viewer", object_str="doc:design_spec") is False
```

### 4. vLLM PagedAttention & Radix Router (`workshop_llm_serving`)
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

## 5. Educational Simulators vs. Production Infrastructure

| Laboratory Module | Educational Simulator Class | Production Reference Architecture | Key Architectural Differences |
|---|---|---|---|
| `ch03_caching` | `SingleFlight`, `VersionedCacheAside` | Redis Cluster / Memcached Leases / Envoy | Simulator uses process-local threading locks; distributed clusters require Redlock, probabilistic early expiration (XFetch), or cluster lease tokens. |
| `ch12_event_driven` | `InMemoryOutboxSimulator` | PostgreSQL + Debezium CDC + Kafka | Simulator models ACID boundaries with in-memory dicts; production uses PostgreSQL MVCC, partial indexes (`WHERE status = 'PENDING'`), CTE `FOR UPDATE SKIP LOCKED`, or Debezium WAL tailing. |
| `ch17_circuit_breaker` | `CircuitBreaker` | Envoy Proxy / Istio Service Mesh | Simulator manages process-local failure counters; production microservices delegate circuit breaking to sidecar proxies coordinating across thousands of instances. |
| `ch18_saga_orchestrator` | `SagaOrchestrator`, `InMemorySagaLog` | Temporal / Cadence / AWS Step Functions | Simulator stores logs in Python memory; production distributed orchestrators durably append state transitions to an external WAL/RDBMS before dispatching RPCs. |
| `ch24_zanzibar_rebac` | `ZanzibarEngine` | Google Zanzibar Infrastructure | Simulator evaluates tuples via in-memory BFS; production Zanzibar runs across globally distributed Spanner with TrueTime tokens (Zookies) and an offline Leopard reachability index. |
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
