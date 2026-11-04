# High-Level Design (HLD) Python Labs

A production-grade reference implementation and interactive laboratory codebase for modern distributed systems, resilient cloud design patterns, and AI systems infrastructure.

---

## Architecture Overview & Modules

This repository covers 13 core chapters and workshops in advanced High-Level Design (HLD):

```
HLD_Python_Labs/
├── ch01_scalability/
│   ├── __init__.py
│   └── concurrency_limiter.py       # Little's Law, AIMD & TCP Vegas Adaptive Limiters
├── ch03_caching/
│   ├── __init__.py
│   └── cache_aside_versioned.py     # Version-Checked Cache-Aside & SingleFlight (Dogpile defense)
├── ch07_consistent_hashing/
│   ├── __init__.py
│   └── hash_ring.py                 # Consistent Hash Ring (vnodes) & Google Bounded Loads
├── ch12_event_driven/
│   ├── __init__.py
│   └── transactional_outbox.py      # Transactional Outbox & SKIP LOCKED Concurrent Poller
├── ch15_rate_limiter/
│   ├── __init__.py
│   └── dual_token_bucket.py         # Dual Token Bucket (RPM + TPM) for LLM Gateways
├── ch16_bloom_filter/
│   ├── __init__.py
│   └── bloom_and_minhash.py         # Bloom Filter (Membership) vs MinHash & LSH (Similarity)
├── ch17_circuit_breaker/
│   ├── __init__.py
│   └── circuit_breaker.py           # Thread-Safe Circuit Breaker with Atomic Single-Probe HALF_OPEN
├── ch18_saga_orchestrator/
│   ├── __init__.py
│   └── saga_orchestrator.py         # Orchestrated Saga Engine with Reverse Compensation Log
├── ch21_distributed_search/
│   ├── __init__.py
│   └── bm25_and_rrf.py              # Okapi BM25 Lexical + Dense Vector Cosine + Reciprocal Rank Fusion
├── ch24_zanzibar_rebac/
│   ├── __init__.py
│   └── zanzibar_rebac.py            # Google Zanzibar ReBAC Graph Engine with Cycle Detection
├── workshop_ecommerce/
│   ├── __init__.py
│   └── flash_sale_inventory.py      # Redis Cluster Flash Sale Inventory Reservation & Reconciliation
├── workshop_llm_serving/
│   ├── __init__.py
│   └── paged_attention_simulator.py # vLLM PagedAttention KV-Cache, Copy-on-Write & Radix Routing
├── workshop_rag_agents/
│   ├── __init__.py
│   └── agent_rag_engine.py          # Enterprise RAG Orchestrator (Hybrid Search + Zanzibar + Outbox)
├── tests/                           # Complete pytest unit test suite (55 tests)
├── docker-compose.yml               # Local infrastructure (Redis, PostgreSQL, Kafka)
├── requirements.txt                 # Dependencies
└── README.md
```

---

## Theoretical & Mathematical Foundations

### 1. Concurrency Limiting & Little's Law (`ch01_scalability`)
- **Little's Law**: $L = \lambda W$
  - $L$: In-flight concurrency (average number of items in system).
  - $\lambda$: Request arrival / throughput rate (requests/sec).
  - $W$: Mean residence time / latency (seconds).
- **TCP Vegas Adaptive Controller**:
  $$\text{queue\_size} = \text{limit} \cdot \left(1 - \frac{\text{min\_rtt}}{\text{smoothed\_rtt}}\right)$$
  - $\text{queue\_size} < \alpha$: Underutilized $\rightarrow \text{limit} \leftarrow \text{limit} + 1$
  - $\text{queue\_size} > \beta$: Congestion $\rightarrow \text{limit} \leftarrow \max(\text{min\_limit}, \text{limit} - 1)$
  - Hard SLO violation: Multiplicative backoff ($\text{limit} \leftarrow \text{limit} \cdot 0.7$).

### 2. Versioned Cache-Aside (`ch03_caching`)
- **Stale-Fill Race Problem**: Reader reads DB at version 1, writer updates DB and cache to version 2, then delayed reader overwrites cache with version 1.
- **Atomic Lua Solution**:
  ```lua
  if (not current_ver) or (ver > tonumber(current_ver)) then
      redis.call('HSET', key, 'data', val, '_version', ver)
      return 1
  else
      return 0 -- Stale fill rejected!
  end
  ```
- **SingleFlight**: Coalesces concurrent cache misses on hot keys into a single in-flight DB query.

### 3. Consistent Hashing with Google Bounded Loads (`ch07_consistent_hashing`)
- **Virtual Nodes**: $V$ tokens per node distributed on $[0, 2^{32}-1]$ via SHA256/MD5.
- **Clockwise Lookup**: $\mathcal{O}(\log(N \cdot V))$ via binary search (`bisect_right`).
- **Bounded-Load Invariant (Mirrokni et al.)**:
  $$\text{max\_load} = \left\lceil c \cdot \frac{\text{total\_load}}{N} \right\rceil \quad (c \ge 1.0)$$
  Prevents cascading server crashes by spilling overflow requests clockwise to non-saturated nodes.

### 4. Transactional Outbox Pattern (`ch12_event_driven`)
- **Dual-Write Defense**: Business state and outbox events are written in the **same ACID transaction**.
- **SKIP LOCKED Concurrency**:
  ```sql
  SELECT * FROM outbox WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED LIMIT batch_size;
  ```
  Allows multiple distributed workers to pull non-overlapping event partitions without table lock contention.

### 5. Dual Token Bucket Rate Limiting (`ch15_rate_limiter`)
- Protects LLM gateways against both connection floods and GPU memory exhaustion:
  - **RPM (Requests Per Minute)**: Throttles API call counts.
  - **TPM (Tokens Per Minute)**: Throttles context prompt + completion token usage.
- **Atomic Check**: Both buckets must have sufficient capacity; otherwise, **zero tokens** are deducted (all-or-nothing rollback).

### 6. Bloom Filter vs. MinHash & LSH (`ch16_bloom_filter`)
- **Bloom Filter (Membership Testing)**:
  - Optimal bit size: $m = -\frac{n \ln p}{(\ln 2)^2}$
  - Optimal hash functions: $k = \frac{m}{n} \ln 2$
  - Zero false negatives; bounded false positive probability $p$.
- **MinHash (Similarity Estimation)**:
  $$P(\text{min\_hash}(A) == \text{min\_hash}(B)) = J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
- **LSH Banding (Candidate Pair Retrieval)**:
  $$P(\text{candidate collision}) = 1 - (1 - s^r)^b \quad (k = b \cdot r)$$

### 7. Circuit Breaker with Single-Probe HALF_OPEN (`ch17_circuit_breaker`)
- **Half-Open Race Fix**: When OPEN cooldown expires, only **one single probe** is admitted using atomic mutex / CAS. Concurrent requests arriving while the probe is in flight are immediately rejected with `CircuitBreakerProbeInFlightException`, preventing downstream services from being overwhelmed.

### 8. Saga Orchestration (`ch18_saga_orchestrator`)
- Orchestrates multi-step distributed workflows.
- On step $k$ failure, executes compensations $C_{k-1}, C_{k-2}, \dots, C_1$ in **strict reverse order**.
- Forward and compensating actions are idempotent.

### 9. Okapi BM25 & Reciprocal Rank Fusion (`ch21_distributed_search`)
- **BM25 Lexical Ranking**:
  $$\text{BM25}(D, Q) = \sum_{q_i \in Q} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
- **Reciprocal Rank Fusion (RRF)**:
  $$\text{RRF}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)} \quad (k=60)$$

### 10. Google Zanzibar ReBAC Engine (`ch24_zanzibar_rebac`)
- Relation Tuples: `object_namespace:object_id#relation@user_or_subject_set`
- Directed Graph BFS traversal with cycle detection.
- Relation rewrites: `owner` $\rightarrow$ `editor` $\rightarrow$ `viewer`.

### 11. Flash Sale Inventory System (`workshop_ecommerce`)
- **Redis Cluster Hash Tags**: `{item:<id>}:stock`, `{item:<id>}:reserves`, `{item:<id>}:idempotency` guarantee multi-key transactions hash to the same cluster slot (avoids `CROSSSLOT` error).
- **Two-Phase Hold Lifecycle**: `HELD` $\rightarrow$ `CONFIRMED` / `RELEASED` / `EXPIRED`.
- Background reconciliation worker restores stock from expired holds.

### 12. PagedAttention KV-Cache Simulator (`workshop_llm_serving`)
- Virtual memory paging for transformer KV cache (avoids 60-80% memory fragmentation).
- Copy-on-Write (CoW) for parallel sampling branches ($n > 1$).
- Radix tree prefix router for directing prompts sharing prefixes to the same worker node.

### 13. Enterprise RAG & Agentic Engine (`workshop_rag_agents`)
- Integrates Hybrid Search (BM25 + Dense Vector + RRF).
- Enforces **authoritative Zanzibar ReBAC**: candidate chunks are authorized before entering LLM context.
- Agent tool side effects are committed atomically to a Transactional Outbox.

---

## Quickstart & Setup

### Requirements
- Python 3.10+
- Optional: Docker & Docker Compose (for local Redis, Postgres, Kafka)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Local Infrastructure (Optional)
```bash
docker-compose up -d
```
Spins up:
- Redis 7 on `localhost:6379`
- PostgreSQL 16 on `localhost:5432` (`hld_user` / `hld_password`)
- Kafka 7.5 on `localhost:9092`

### 3. Run the Unit Test Suite
```bash
pytest tests -v
```
All **55 unit tests** run and pass in ~1.0 second without requiring external daemon services.

---

## Code Examples

### 1. Adaptive Concurrency Limiter
```python
from ch01_scalability.concurrency_limiter import VegasAdaptiveLimiter

limiter = VegasAdaptiveLimiter(initial_limit=10.0, slo_latency_ms=200.0)

try:
    with limiter.acquire():
        # Execute latency-sensitive RPC call
        response = call_service()
except ConcurrencyLimitExceeded:
    # Shed load gracefully
    return HTTPStatus.SERVICE_UNAVAILABLE
```

### 2. Dual Token Bucket for LLM Serving
```python
from ch15_rate_limiter.dual_token_bucket import DualTokenBucketLimiter

limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=10_000.0)

# Request 1 query with estimated 1,500 tokens
result = limiter.acquire(client_id="team_analytics", tokens_requested=1500)
if not result.allowed:
    print(f"Rate limited: {result.reason}. Retry after {result.retry_after_seconds:.2f}s")
```

### 3. Google Zanzibar Authorization Check
```python
from ch24_zanzibar_rebac.zanzibar_rebac import ZanzibarEngine, RelationTuple

engine = ZanzibarEngine()
# doc:design#viewer -> group:engineering#member
engine.write_tuple(RelationTuple("doc", "design", "viewer", "group:engineering#member"))
# group:engineering#member -> user:bob
engine.write_tuple(RelationTuple("group", "engineering", "member", "user:bob"))

# Query authorization
can_view = engine.check("user:bob", "viewer", "doc:design")
print(f"Can Bob view design doc? {can_view}") # True
```

---

## License & Attribution
Designed for the High-Level Design (HLD) curriculum. Developed for production-grade educational use.
