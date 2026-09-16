# Module 25 Final Capstone Polyglot Enterprise: Project Guide

## 📌 Project Overview: Enterprise Polyglot Persistence Platform

Modern hyper-scale applications cannot survive on a single database engine. An enterprise e-commerce platform processing millions of transactions per day demands:
1. **PostgreSQL** for ACID-compliant, serializable financial transactions and catalog state of record.
2. **Redis** for ultra-low latency (<1 ms) session caching, distributed lock coordination, and live customer spend leaderboards.
3. **MongoDB** for flexible, polymorphic product catalogs, hierarchical variant trees, and user-generated review documents.
4. **Elasticsearch / Qdrant** for sub-millisecond lexical full-text search and high-dimensional semantic vector search over product embeddings.
5. **DuckDB / ClickHouse** for columnar OLAP queries, daily aggregate rollups, and real-time executive dashboarding.

The greatest challenge of polyglot persistence is **not** connecting to multiple databases—it is **guaranteeing cross-engine consistency without introducing distributed deadlocks or catastrophic data divergence**.

This capstone project guides you through architecting, implementing, and battle-testing an enterprise polyglot platform that solves the **Dual-Write Consistency Problem** using the **Transactional Outbox Pattern**, **Change Data Capture (CDC) Event Relaying**, **Idempotent Consumers**, and a **Distributed Saga Orchestrator**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Dual-engine coordinator: Relational OLTP (SQLite/PostgreSQL) coupled with cache-aside read-through logic and cache invalidation. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | The Full 5-Engine Polyglot Platform: ACID Outbox pattern, asynchronous CDC event relay dispatcher, Redis cache & spend leaderboard, BM25 catalog search, and columnar OLAP ingestion. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Enterprise Resiliency Suite: Distributed Saga Orchestrator with compensating transactions, Fenced Redlock distributed locking, Dead Letter Queue (DLQ) for poison messages, and an automated Reconciliation Auditor. |

---

## 1. Architectural Blueprint & Data Flow

```text
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                           Application Gateway                           │
 └──────────────┬──────────────────────────────────────────┬───────────────┘
                │                                          │
                │ 1. Atomic Transaction                    │ Read Cache-Aside
                │ (Order Insert + Outbox Event)            ▼
                ▼                                   ┌──────────────┐
     ┌──────────────────────┐                       │ Redis Cache  │
     │   PostgreSQL / OLTP  │                       │ (Sub-ms reads│
     │                      │                       └──────────────┘
     │  TABLE orders        │                              ▲
     │  TABLE outbox_events │                              │ Cache
     └──────────┬───────────┘                              │ Invalidation
                │                                          │
                │ 2. Change Data Capture (CDC Relay)       │
                ▼                                          │
     ┌─────────────────────────────────────────────────────┴───────┐
     │                     CDC Event Dispatcher                    │
     │          (At-Least-Once Delivery + Deduplication)           │
     └──────┬──────────────────────┬──────────────────────┬────────┘
            │                      │                      │
            ▼                      ▼                      ▼
    ┌───────────────┐     ┌────────────────┐     ┌────────────────┐
    │  Redis ZSET   │     │ Search Catalog │     │ Columnar OLAP  │
    │  Spend        │     │ Inverted /     │     │ DuckDB         │
    │  Leaderboard  │     │ Vector Index   │     │ Warehouse      │
    └───────────────┘     └────────────────┘     └────────────────┘
```

---

## 2. Low-Level Data Contracts & Schemas

### A. Relational OLTP Schema (PostgreSQL / SQLite)
```sql
CREATE TABLE orders (
    order_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    status VARCHAR(32) NOT NULL, -- 'PENDING', 'CONFIRMED', 'CANCELLED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE outbox_events (
    event_id BIGSERIAL PRIMARY KEY,
    aggregate_type VARCHAR(64) NOT NULL, -- 'ORDER'
    aggregate_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,     -- 'ORDER_CREATED', 'ORDER_CANCELLED'
    payload JSONB NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE NULL,
    retry_count INT DEFAULT 0
);
CREATE INDEX idx_outbox_unprocessed ON outbox_events(event_id) WHERE published_at IS NULL;
```

### B. Redis In-Memory Structure
- **Order Cache:** Key `order:{order_id}` (JSON payload, TTL 3600s).
- **Customer Spend Leaderboard:** Sorted Set `polyglot:leaderboard:spend` (Score: cumulative total spend, Member: `customer_id`).
- **Distributed Mutex Lock:** Key `lock:order:{order_id}` (Value: unique fencing token, TTL 10s).
- **Idempotency Log:** Key `polyglot:idempotency:{event_id}` (Value: timestamp, TTL 86400s).

### C. Search Catalog Index
- Documents indexed with schema: `{doc_id: str, text: str, vector: list[float], metadata: dict}`.
- Supports both BM25 lexical token matching and Cosine Similarity vector search.
- Term frequencies computed dynamically: $\text{IDF}(q) = \ln\left(1 + \frac{N - n(q) + 0.5}{n(q) + 0.5}\right)$.

### D. Columnar OLAP Star Schema (DuckDB / ClickHouse)
- Table: `sales_fact(order_id VARCHAR, customer_id VARCHAR, amount DOUBLE, sale_date DATE)`.
- Aggregation query: Vectorized windowing and rollups over millions of rows in milliseconds:
```sql
SELECT 
    customer_id, 
    COUNT(*) AS total_orders, 
    SUM(amount) AS total_revenue,
    AVG(amount) AS aov,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS rank
FROM sales_fact
GROUP BY customer_id;
```

---

## 3. The Dual-Write Problem & Failure Modes

When an application attempts to write to two systems directly:
```python
# ANTI-PATTERN: Direct Dual-Write
db.save_order(order)       # Step 1: Succeeds
redis.set(order_id, order) # Step 2: Fails (Network split or timeout)
```
The system enters an inconsistent state. If the order of operations is reversed, the cache might be updated while the database transaction rolls back due to a constraint violation.

### Solution: Transactional Outbox Pattern
1. In the **same database transaction**, the application writes the business entity to `orders` AND appends an event record to `outbox_events`.
2. A decoupled background process (CDC Relay) polls `outbox_events` (or reads Postgres WAL via logical decoding).
3. The relay dispatches events to Redis, Search, and DuckDB with retry backoff.
4. Downstream consumers maintain an `idempotency_log` to safely discard duplicate events.

---

## 4. Step-by-Step Implementation Roadmap

### Phase 1: Core Foundation & Transactional Outbox (Tier 1)
1. Initialize the relational OLTP schema with `orders` and `outbox_events`.
2. Implement `place_order(order_id, customer_id, total, description)` ensuring atomic commit of both tables.
3. Verify that rolling back the transaction leaves neither an order nor an outbox event.
4. Implement Cache-Aside read: check cache first; on miss, query database and populate cache.
5. Provide atomic invalidation to eliminate cache drift.

### Phase 2: CDC Event Relaying & Fan-Out (Tier 2)
1. Build `process_cdc_events(batch_size)` to read unpublished outbox events in strict FIFO order.
2. Invalidate stale cache entries on mutation.
3. Update the Redis sorted set customer spend leaderboard via `ZINCRBY`.
4. Index the order description into the inverted lexical / vector search catalog.
5. Ingest the transaction into the columnar analytical warehouse for immediate OLAP availability.
6. Mark processed outbox events as published in an idempotent manner.
7. Support batch chunking so millions of accumulated events can be processed without memory exhaustion.

### Phase 3: Distributed Resiliency Suite (Tier 3)
1. **Distributed Lock Manager:** Implement `acquire_lock(resource, ttl)` and `release_lock(resource, token)` ensuring only the lock owner holding the correct fencing token can release or mutate.
2. **Dead Letter Queue (DLQ):** Implement poison message handling: if an event fails 3 consecutive delivery attempts, route it to `dlq_events` with error trace, without blocking the pipeline.
3. **Distributed Saga Orchestrator:**
   - Execute forward steps: Reserve Stock -> Authorize Payment -> Confirm Order.
   - If Payment fails, trigger compensating transactions: Release Reserved Stock -> Mark Order Cancelled -> Emit `ORDER_COMPENSATED` event.
4. **Reconciliation Auditor:** Run a background verification check asserting that:
   $$\text{Sum of Postgres Orders} \equiv \text{Sum of DuckDB Sales} \equiv \text{Sum of Redis Leaderboard Scores}$$
5. **Cache Stampede Guard:** Implement single-flight mutex locking to prevent thundering herds on hot-key cache expiration.

---

## 5. Failure Scenarios & Self-Healing Runbook

| Failure Mode | Impact | Self-Healing Architecture Mechanism |
| :--- | :--- | :--- |
| **Worker Crash Mid-CDC** | Event processed in Redis but crashed before updating DuckDB | Consumer idempotency deduplicates Redis increment on replay; DuckDB completes successfully. |
| **Poison Pill Payload** | Malformed JSON in outbox event crashes worker | Quarantine event to Dead Letter Queue (DLQ) after 3 retries; pipeline continues uninterrupted. |
| **Network Split to Cache** | Redis becomes unreachable | Platform gracefully degrades to relational direct read; circuit breaker prevents socket starvation. |
| **Stale Cache Read** | Outdated item returned to user | CDC relay performs explicit key deletion (`DEL`) upon mutation; TTL guarantees bounded staleness. |
| **Saga Payment Failure** | Inventory reserved but funds cannot be captured | Saga Orchestrator dispatches reverse compensating action, restoring inventory balance within 50 ms. |
| **Split-Brain Concurrent Writes**| Two workers mutate customer balance simultaneously | Fenced Redlock token monotonicity rejects outdated mutation attempts. |

---

## 6. Production Deployment & Monitoring Metrics

When deploying polyglot architecture to production Kubernetes or cloud clusters:
- **Outbox Lag Metric:** Track `SELECT COUNT(*) FROM outbox_events WHERE published_at IS NULL`. Alert if lag exceeds 500 records or latency > 2.0s.
- **Cache Hit Ratio:** Target > 92% in Redis:
  $$\text{Hit Ratio} = \frac{\text{keyspace\_hits}}{\text{keyspace\_hits} + \text{keyspace\_misses}}$$
- **CDC Replay Idempotency Violations:** Count of duplicate events suppressed. Spike indicates network jitter or worker timeout thrashing.
- **DLQ Alarm:** Any non-zero count in `dlq_events` must trigger a PagerDuty alert for schema divergence or malformed event payloads.

---

## 7. Verification & Acceptance Rubric

Your implementation must satisfy all the following automated test assertions:

1. **Atomicity:** Rolling back an OLTP transaction produces 0 orphaned outbox rows.
2. **At-Least-Once Delivery:** Network interruptions trigger retries without dropping events.
3. **Idempotency:** Replaying the same CDC batch 5 times produces identical final balances and zero duplicate leaderboard increments.
4. **Ordering:** Outbox events are processed strictly in monotonic sequence.
5. **Isolation:** Concurrent orders on the same customer correctly serialize through the distributed lock.
6. **Poison Pill Quarantine:** Malformed event payloads are safely moved to the Dead Letter Queue without halting relay execution.
7. **Saga Compensation:** Mid-flight failures successfully invoke reverse compensating steps and leave all engines in a consistent state.
8. **Reconciliation:** The auditor detects zero discrepancies between primary OLTP and replica stores.
9. **Single-Flight Guard:** Simultaneous cache misses on an expired hot key trigger only 1 database query.
10. **Vector Semantic Search:** Query vectors retrieve relevant catalog products ranked by cosine similarity score.

Run the full verification suite:
```bash
pytest Module_25_Final_Capstone_Polyglot_Enterprise -v
```

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Choose the right engine for each part of a polyglot system, with reasons
- [ ] Explain the dual-write problem and implement the outbox pattern
- [ ] Say why distributed transactions across engines are usually the wrong answer
- [ ] Design a saga with compensating actions for a multi-store operation
- [ ] Explain how you keep a cache and a system of record consistent
- [ ] Diagnose which store is responsible for an observed inconsistency
- [ ] Defend a decision to use *one* database instead of five

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
