# Module 26: Self-Assessment Quiz & Senior Architecture Mastery Challenges

Test your end-to-end backend architecture mastery before completing the entire curriculum.

---

## Part 1: Comprehensive Architecture Mastery Quiz (10 Questions)

### Questions

1. **Monolith vs Microservices:** What are the key architectural trade-offs between a Modular Monolith and a Distributed Microservice architecture?
2. **API Gateway Role:** What critical responsibilities does an API Gateway fulfill in an enterprise system?
3. **Database Scalability:** What is the difference between Database Vertical Scaling, Read-Replicas, and Horizontal Sharding?
4. **Inter-Service Communication:** When should microservices communicate synchronously over HTTP/gRPC vs asynchronously via Message Brokers?
5. **Distributed Tracing:** How does propagating a `Correlation-ID` through HTTP headers and message envelopes enable distributed root-cause debugging?
6. **Zero-Trust Security:** Why should internal microservices verify JWT scopes and signatures even when behind an API gateway?
7. **Container Orchestration:** How does Kubernetes manage rolling updates, auto-scaling (HPA), and self-healing container restarts?
8. **Cache Invalidation:** Why is "Cache Invalidation" regarded as one of the two hardest problems in computer science?
9. **Zero-Downtime Migrations:** How do expand-and-contract schema migrations prevent downtime when running old and new code simultaneously?
10. **Site Reliability (SRE):** Define **SLA** (Service Level Agreement), **SLO** (Service Level Objective), and **SLI** (Service Level Indicator).

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **Modular Monolith:** Simpler deployments, zero network latency between modules, single database transaction boundary.
- **Microservices:** Independent team deployments, isolated failure domains, technology heterogeneity, but introduces network latency and distributed state complexity.

#### Answer 2:
Centralized SSL termination, authentication/authorization, rate limiting, request routing, telemetry metrics, and CORS policy enforcement.

#### Answer 3:
- **Vertical:** Upgrading CPU/RAM on the single server.
- **Read-Replicas:** Offloading read queries (`SELECT`) to replica nodes while writes (`INSERT`/`UPDATE`) go to the primary node.
- **Sharding:** Partitioning rows across multiple database instances based on a shard key (e.g. `tenant_id` or `user_id`).

#### Answer 4:
- **Sync (HTTP/gRPC):** When the caller immediately requires the return payload to continue (e.g. user authentication).
- **Async (Broker):** When operations are long-running, can be processed out of order, or require high fault tolerance and spike buffering.

#### Answer 5:
It allows centralized logging platforms (Datadog, OpenTelemetry, ELK) to filter all logs, queries, and errors produced across 20 distinct services by a single user request.

#### Answer 6:
Perimeter defense can be breached (insider threats, SSRF attacks). Zero-Trust ensures every component verifies identity and authorization at every boundary.

#### Answer 7:
Kubernetes continuously compares actual state against desired state, spinning up new container replicas when CPU exceeds thresholds, restarting crashed pods, and shifting traffic during zero-downtime rolling deployments.

#### Answer 8:
Because determining exactly when cached data has changed and coordinating immediate invalidation across distributed nodes without causing Cache Avalanches requires careful consistency mechanisms.

#### Answer 9:
1. **Expand:** Add new nullable column to DB.
2. Deploy code that writes to both old and new columns.
3. Backfill historic data.
4. Deploy code reading only new column.
5. **Contract:** Remove old column.

#### Answer 10:
- **SLI:** The exact metric measured (e.g. "99.2% of requests returned in $< 200$ms").
- **SLO:** The internal team target goal (e.g. "99.0% of requests must return in $< 200$ms").
- **SLA:** The contract with customers with financial penalties if breached (e.g. "98.5% uptime guaranteed").

</details>

---

## Part 3: Capstone Platform Extensions

### Challenge 1: Adding a DLQ Metric Counter to the Capstone

**Goal:** Modify the Capstone task broker to expose `dlq_messages_total` in the Prometheus `/metrics` endpoint.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Dual write without an outbox

```python
async def create_order(order: Order) -> None:
    await db.insert_order(order)          # PostgreSQL
    await queue.publish("order.created", order.id)   # Redis
```

**Observed symptom:** Occasionally an order exists in the database with no confirmation email ever sent; occasionally an email is sent for an order that does not exist.

**(a)** Name both failure interleavings.

**(b)** What is the outbox pattern, and why does it work?

**(c)** Why is a distributed transaction not the answer?

<details>
<summary><b>Show the diagnosis</b></summary>

**Both directions fail.** If the process dies after the insert but before the publish, the order exists with no event — no email. If the publish succeeds and the transaction is then rolled back, an event references an order that does not exist.

**Outbox pattern:** write the event into an `outbox` **table in the same database transaction** as the order. Either both commit or neither does — that is ordinary ACID, no coordination needed. A separate poller then reads the outbox and publishes to the queue, marking rows as sent. Publishing may happen more than once, so consumers must be idempotent (Module 18) — but nothing is ever lost.

**Distributed transactions (2PC) are not the answer** because Redis, Mongo and most modern stores do not support them; they require every participant to be available for the whole protocol, they hold locks across a network round trip, and a coordinator crash leaves participants blocked. The outbox achieves the same guarantee using only a local transaction, which is why it is what production systems actually use.

</details>

---

### D2. Cache invalidation race

```python
async def update_user(user_id: int, data: dict) -> None:
    await cache.delete(f"user:{user_id}")
    await db.update_user(user_id, data)
```

**Observed symptom:** Occasionally the cache serves the *old* value indefinitely after an update.

**(a)** Describe the interleaving that causes it.

**(b)** What ordering fixes the common case?

**(c)** Why can no ordering fix it completely, and what does?

<details>
<summary><b>Show the diagnosis</b></summary>

**The interleaving:** request A deletes the cache; request B misses, reads the **old** row from the database (A's update has not committed yet), and writes it back; A's update then commits. The cache now holds the stale value with a fresh TTL.

**Better ordering:** update the database **first**, then invalidate the cache. That shrinks the window substantially — but does not close it, because B can still read-then-write across A's invalidate.

**No ordering closes it** because the cache and the database are separate systems without a shared transaction. What actually works: **short TTLs** to bound staleness, **versioned keys** (`user:42:v7`, where the version comes from the row itself, so a stale write lands on a key nobody reads), or **write-through** with a per-key lock. Accepting a bounded staleness window and stating it explicitly is usually the right engineering answer — the mistake is believing you have consistency when you have a race.

</details>

---

### D3. Health check that hides a dependency outage

```
@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
```

**Observed symptom:** The database has been unreachable for ten minutes. Every instance reports healthy, the load balancer keeps routing traffic, and no alert fires.

**(a)** What does this endpoint actually prove?

**(b)** What is the difference between liveness and readiness here?

**(c)** Why can a readiness check that tests the database be dangerous?

<details>
<summary><b>Show the diagnosis</b></summary>

It proves the **process is running and the event loop is responsive** — which the orchestrator already knows from the process being alive. It says nothing about whether this instance can do its job.

**Liveness** = 'restart me' — the process is wedged. It should *not* check external dependencies. **Readiness** = 'send me traffic' — this instance can serve requests, which *does* mean checking the database, cache and queue it needs.

**The danger:** if readiness fails on a database outage, every instance simultaneously reports not-ready, the load balancer removes them all, and a recoverable dependency blip becomes a total outage — with no instances left to serve cached or degraded responses. Worse, if liveness checks the database, every pod restart-loops and you lose warm caches and in-flight work too. Check dependencies in readiness only, with a short timeout, and consider serving degraded responses rather than none.

</details>

---

### D4. Migration that is not safe to run twice

```
-- migration 007
ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';
UPDATE users SET status = 'legacy' WHERE created_at < '2024-01-01';
```

**Observed symptom:** A deployment is retried after a network timeout. The migration fails half-applied, and the release is stuck.

**(a)** Which statement is not idempotent, and why does that matter?

**(b)** How do you make each statement safe to re-run?

**(c)** What is the additional risk of this specific `ALTER TABLE` on a large table?

<details>
<summary><b>Show the diagnosis</b></summary>

The `ALTER TABLE` fails on a second run with *column already exists*, aborting the migration before the `UPDATE`. It matters because deployments **are** retried — by CI, by an operator, by an orchestrator restarting a job. A migration that cannot be re-run is a migration that can leave you half-applied with no way forward.

**Make each safe:** `ADD COLUMN IF NOT EXISTS`, and give the `UPDATE` a guard so re-running is a no-op (`WHERE status = 'active' AND created_at < ...`). Wrap the whole thing in a transaction where the engine supports transactional DDL.

**On a large table:** `ADD COLUMN ... NOT NULL DEFAULT` historically rewrote the entire table under an `ACCESS EXCLUSIVE` lock — minutes of downtime on a big table. PostgreSQL 11+ optimises constant defaults, but the general pattern is **expand/contract**: add the column nullable, backfill in batches, add the constraint, then remove the old path in a later release. Never combine a schema change and a full-table data change in one locking statement.

</details>

---

### D5. One store used for everything

```python
# Everything in PostgreSQL:
#   - transactional orders
#   - session tokens (high write, short TTL)
#   - full-text product search
#   - 50M-row analytics aggregations
#   - vector similarity for recommendations
```

**Observed symptom:** Analytics queries lock tables and slow down checkout. Session writes bloat the WAL. Search is slow and ranking is poor.

**(a)** Which of these workloads is PostgreSQL genuinely the wrong tool for?

**(b)** What would you move, and to what?

**(c)** What is the argument for *not* splitting it up?

<details>
<summary><b>Show the diagnosis</b></summary>

**Genuinely wrong fit:** high-churn session tokens (a durable, WAL-logged, MVCC-versioned store for data that lives 20 minutes is pure overhead, and the dead tuples create vacuum pressure) and large analytical aggregations (row storage scans columns it does not need, and long queries block `VACUUM`).

**Move:** sessions → Redis, with a native TTL. Analytics → a columnar store (DuckDB, ClickHouse) fed from a replica. Search and vectors → PostgreSQL is actually *fine* here: `tsvector` and `pgvector` are good enough for most scales, and a dedicated engine only pays off at volume. Orders stay in PostgreSQL — that is exactly what it is for.

**The argument against splitting:** every store added is another thing to back up, monitor, secure, upgrade, and reason about during an incident — plus the dual-write problem in the first diagnostic above. 'One boring database until it hurts' is a defensible senior position. Move a workload out when you can name the specific metric that forced it, not because the architecture diagram looks better.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
