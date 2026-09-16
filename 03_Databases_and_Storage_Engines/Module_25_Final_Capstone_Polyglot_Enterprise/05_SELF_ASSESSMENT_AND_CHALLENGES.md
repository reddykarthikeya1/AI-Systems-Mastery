# Module 25 Final Capstone Polyglot Enterprise: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Enterprise Polyglot Persistence Platform Capstone** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the Transactional Outbox Pattern, and what distributed data problem does it solve?** What is the Transactional Outbox Pattern, and what distributed data problem does it solve?
2. **How does Change Data Capture (CDC) differ from application-level event publishing?** How does Change Data Capture (CDC) differ from application-level event publishing?
3. **In an enterprise polyglot architecture, what are the distinct roles of PostgreSQL, Redis, Elasticsearch, and ClickHouse?** In an enterprise polyglot architecture, what are the distinct roles of PostgreSQL, Redis, Elasticsearch, and ClickHouse?
4. **What is a Distributed Saga, and how does it handle cross-database transaction failures?** What is a Distributed Saga, and how does it handle cross-database transaction failures?
5. **How does the Cache-Aside pattern prevent stale reads when an update occurs?** How does the Cache-Aside pattern prevent stale reads when an update occurs?
6. **What is the Thundering Herd (Cache Stampede) problem, and how is it mitigated?** What is the Thundering Herd (Cache Stampede) problem, and how is it mitigated?
7. **Why should downstream search engines and caches be treated as derived read models?** Why should downstream search engines and caches be treated as derived read models?
8. **What is Eventual Consistency, and how does an application handle read lag in polyglot stores?** What is Eventual Consistency, and how does an application handle read lag in polyglot stores?
9. **How does an outbox event relay ensure at-least-once delivery?** How does an outbox event relay ensure at-least-once delivery?
10. **What is Idempotency, and why must event consumers enforce it?** What is Idempotency, and why must event consumers enforce it?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
It atomically writes application state and event intentions to the same relational database in one ACID transaction, solving dual-write inconsistency.

#### Answer 2:
CDC reads committed mutations directly from the database transaction log (WAL/binlog), guaranteeing zero event loss even if the app crashes.

#### Answer 3:
PostgreSQL: transactional source of truth; Redis: low-latency caching & leaderboards; Elasticsearch: full-text keyword search; ClickHouse: high-throughput columnar analytics.

#### Answer 4:
A sequence of local transactions across services; if a step fails, the saga orchestrator executes compensating transactions to undo previous steps.

#### Answer 5:
Updates write to the database and invalidate (delete) the cached key; subsequent reads experience a cache miss and fetch fresh data.

#### Answer 6:
Thousands of concurrent clients querying the database on hot key expiration; mitigated with distributed mutex locks or probabilistic early expiration.

#### Answer 7:
Because they can always be rebuilt from scratch by replaying the transactional source of truth event log.

#### Answer 8:
Downstream systems become consistent after a short propagation delay; applications use read-after-write routing to primary for immediate feedback.

#### Answer 9:
By recording published status only after receiving acknowledgment from the downstream message broker/store.

#### Answer 10:
The property where processing an event multiple times produces the same outcome as processing it once, protecting against duplicate message deliveries.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Build an end-to-end polyglot transaction processor coordinating PostgreSQL outbox events to Redis and DuckDB.

### 🚀 Challenge 2: Architect Stretch Problem
Implement an idempotent event consumer that deduplicates incoming CDC events using transaction IDs.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Dual-Write Data Drift Between Postgres and Elasticsearch

```python
# E-Commerce Order Processing Service
@app.post("/orders")
def create_order(order_data: dict):
    # Step 1: Save order to PostgreSQL
    order = db.save_order(order_data)
    
    # Step 2: Push to Elasticsearch for search indexing
    es.index(index="orders", id=order.id, document=order.to_dict())
    
    return {"status": "success", "order_id": order.id}
```

**Observed symptom:** Over 3 months, 2,400 orders exist in PostgreSQL but are completely missing in Elasticsearch. When Elasticsearch experienced a 5-second network timeout, Step 1 committed, Step 2 threw an exception, and state permanently drifted.

**(a)** What is the fundamental flaw of the dual-write anti-pattern across disparate data stores?

**(b)** Why cannot a distributed transaction (2PC) be cleanly executed between Postgres and Elasticsearch?

**(c)** How does the Transactional Outbox Pattern with Change Data Capture (CDC / Debezium) guarantee eventual consistency?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
The **dual-write pattern** lacks atomicity. PostgreSQL and Elasticsearch are separate storage systems without a shared transaction coordinator. If Step 1 succeeds and Step 2 fails (network glitch, ES node restart, or application crash before Step 2), the data exists in the database but never reaches the search index. Conversely, if Step 2 were executed first and Step 1 failed, ghost data would exist in the search engine.

**Diagnostic Commands:**
1. Run reconciliation script comparing record counts and IDs between Postgres and Elasticsearch:
   ```sql
   SELECT count(*) FROM orders;
   ```
   vs `GET /orders/_count`.
2. Inspect application error logs for unhandled Elasticsearch timeout exceptions.

**Production Fix:**
Implement the **Transactional Outbox Pattern** with **CDC (Debezium)**:
1. When saving the order in PostgreSQL, write an outbox event in the same atomic transaction:
   ```sql
   BEGIN;
   INSERT INTO orders (...) VALUES (...);
   INSERT INTO outbox_events (aggregate_type, aggregate_id, payload) VALUES ('order', order_id, ...);
   COMMIT;
   ```
2. Debezium reads PostgreSQL's write-ahead log (WAL) via logical decoding and publishes events to Apache Kafka.
3. A consumer reads Kafka and indexes documents into Elasticsearch with idempotent upserts (`PUT /orders/_doc/{id}`). This guarantees **at-least-once delivery** with zero data loss.

</details>

---

### D2. Cache Stampede (Thundering Herd) on High-Traffic Key Expiration

```python
def get_homepage_recommendations(category_id: str):
    cache_key = f"recs:{category_id}"
    data = redis_client.get(cache_key)
    
    if data is None:
        # Cache miss: Run complex multi-join SQL query taking 800ms
        data = db.query_heavy_recommendations(category_id)
        redis_client.setex(cache_key, 300, json.dumps(data)) # TTL = 5 mins
        return data
        
    return json.loads(data)
```

**Observed symptom:** Every 5 minutes (exact cache TTL expiration), database CPU shoots to 100% and crashes. 5,000 concurrent requests arrive at the exact instant the cache expires, all executing the 800ms query simultaneously.

**(a)** What is a Cache Stampede (Thundering Herd), and why does simple TTL expiration trigger it?

**(b)** What is Probabilistic Early Expiration (XFetch algorithm)?

**(c)** How can distributed mutex locking (Redis SETNX lock) protect the backing database?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A **cache stampede** occurs when a highly requested cache entry expires. During the 800ms window where the key is absent and being recomputed by the database, all 5,000 incoming requests observe `data is None`. Instead of 1 request updating the cache and 4,999 reading the cached result, all 5,000 requests execute the expensive database query in parallel, overwhelming connection pools and knocking the database offline.

**Diagnostic Commands:**
1. Check Postgres active queries during stampede:
   ```sql
   SELECT count(*), query FROM pg_stat_activity WHERE state = 'active' GROUP BY query;
   -- 500 identical recommendation queries running simultaneously.
   ```

**Production Fix:**
- **Approach 1 (Distributed Locking with Mutex):**
  Only 1 worker computes the value; others wait or return stale data:
  ```python
  if data is None:
      # Acquire lock for 5 seconds
      if redis_client.set(f"lock:{cache_key}", "1", nx=True, ex=5):
          try:
              data = db.query_heavy_recommendations(category_id)
              redis_client.setex(cache_key, 300, json.dumps(data))
          finally:
              redis_client.delete(f"lock:{cache_key}")
      else:
          time.sleep(0.05)
          return get_homepage_recommendations(category_id)
  ```
- **Approach 2 (XFetch Probabilistic Early Expiration):**
  Recompute the cache in the background *before* it expires based on $eta 	imes \delta 	imes \ln(	ext{random}())$.

</details>

---

### D3. Out-of-Order Change Data Capture (CDC) Event Replay Overwrite

```python
# Kafka Consumer updating Read Model in MongoDB from CDC topic
def process_cdc_event(message):
    event = json.loads(message.value)
    order_id = event['order_id']
    new_status = event['status']
    
    # Direct overwrite:
    mongo_db.orders.update_one(
        {"_id": order_id},
        {"$set": {"status": new_status, "updated_at": event['timestamp']}},
        upsert=True
    )
```

**Observed symptom:** An order was CANCELLED by the user. However, the database shows status = 'SHIPPED'. Auditing confirms the user cancelled the order AFTER it was shipped, but MongoDB shows SHIPPED.

**(a)** Why can messages in a distributed streaming platform (Kafka) arrive or be processed out of order?

**(b)** How does Kafka partitioning affect message ordering guarantees?

**(c)** How do version checks / optimistic concurrency control prevent stale events from clobbering newer state?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In distributed systems, network retransmissions, multiple consumer threads, or consumer rebalancing can cause CDC events to arrive out of order. If the events `Status: SHIPPED (seq=1)` and `Status: CANCELLED (seq=2)` are processed concurrently or re-delivered, the consumer may process `seq=2` first and `seq=1` second. Without version checking, the older `SHIPPED` event overwrites the newer `CANCELLED` event, corrupting the read model.

**Diagnostic Commands:**
1. Check Kafka consumer group lag and partition assignments:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group cdc_mongo_consumers
   ```
2. Verify if partition key was set on the message (missing partition key routes messages randomly across partitions).

**Production Fix:**
1. **Ensure Kafka Message Keying:** Always use the primary entity key (e.g. `order_id`) as the Kafka message key so all events for the same order are strictly routed to the **same partition**.
2. **Optimistic Version Filtering in Consumer:** Only update if the incoming event has a greater version/timestamp than what is currently stored:
   ```python
   mongo_db.orders.update_one(
       {
           "_id": order_id,
           "version": {"$lt": event['version']}  # Only overwrite if older
       },
       {
           "$set": {
               "status": new_status,
               "version": event['version'],
               "updated_at": event['timestamp']
           }
       },
       upsert=True
   )
   ```

</details>

---

### D4. Distributed Transaction Failure in Polyglot Workflow Without Saga

```python
# Microservices Architecture: OrderService, InventoryService, PaymentService
def checkout(user_id, cart):
    # Step 1: Deduct inventory in Postgres (InventoryService)
    inv_res = requests.post("http://inventory-service/deduct", json=cart)
    
    # Step 2: Charge credit card via Stripe (PaymentService)
    pay_res = requests.post("http://payment-service/charge", json={"user": user_id, "amount": cart.total})
    
    # Step 3: Insert order into Postgres (OrderService)
    order_res = requests.post("http://order-service/orders", json=cart)
    
    return {"status": "complete"}
```

**Observed symptom:** Step 1 deducted 5 items from inventory. Step 2 charged the customer $500. Step 3 timed out with HTTP 504. The customer was charged, inventory was lost, but no order exists in the system.

**(a)** Why does chaining synchronous HTTP calls across microservices violate transaction atomicity?

**(b)** What is the difference between an Orchestrated Saga and a Choreographed Saga?

**(c)** How do compensating transactions and idempotency keys ensure system consistency?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a polyglot microservice architecture, each service controls its own independent database. Chaining multiple synchronous HTTP requests lacks distributed atomicity. When Step 3 fails or times out, the changes committed in Step 1 (inventory reserved) and Step 2 (credit card charged) remain committed without automatic rollback, leaving the distributed system in an inconsistent, fractured state.

**Diagnostic Commands:**
1. Inspect distributed traces (OpenTelemetry / Jaeger) for trace IDs with failing downstream spans.
2. Check reconciliation logs between Payment transactions and Order database IDs.

**Production Fix:**
Implement the **Saga Pattern** (Orchestrated or Choreographed) with **Compensating Transactions** and **Idempotency Keys**:
1. **Pass Idempotency Keys:** Ensure every call carries a unique `Idempotency-Key: {checkout_id}` so retries do not double-charge.
2. **Compensating Transactions:** If Step 3 fails, the Saga Orchestrator executes compensating actions in reverse order:
   - Call `PaymentService.refund(charge_id)`
   - Call `InventoryService.release(cart_items)`
3. Use workflow orchestrators like **Temporal** or **AWS Step Functions** to persist execution state durable across service crashes.

</details>

---

### D5. Read-Your-Own-Writes Inconsistency on Asynchronous Read Replicas

```python
# Web Application
@app.post("/update_profile")
def update_profile(user_id: int, new_bio: str):
    # Writes go to Primary database
    primary_db.execute("UPDATE users SET bio = %s WHERE id = %s", (new_bio, user_id))
    return redirect("/profile")

@app.get("/profile")
def view_profile(user_id: int):
    # Reads go to Read Replica to offload primary
    user = replica_db.query_one("SELECT * FROM users WHERE id = %s", (user_id,))
    return render_template("profile.html", user=user)
```

**Observed symptom:** User updates their bio and clicks 'Save'. The browser immediately redirects to /profile, displaying their OLD bio. User repeatedly refreshes in confusion; after 3 seconds, the new bio suddenly appears.

**(a)** What causes Read-Your-Own-Writes inconsistency in primary-replica database topologies?

**(b)** What is replication lag, and why is asynchronous replication non-zero latency?

**(c)** What architectural patterns (session-based primary routing, replica lag cookies, or write tracking) solve this?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In asynchronous replication, mutations committed on the Primary database are written to WAL and shipped over the network to the Read Replica. There is an inherent delay—**replication lag** (typically 10ms to 2,000ms)—before the replica receives and applies the WAL. When the web application immediately redirects the user to `/profile` and routes the read to the replica, the replica has not yet processed the update, serving the stale pre-update record.

**Diagnostic Commands:**
1. Measure replication lag on the replica:
   ```sql
   SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;
   ```

**Production Fix:**
1. **Session-Level Sticky Primary Routing:** If a user performs a write, route all subsequent reads from that specific user to the **Primary** database for a window of time (e.g. 5 seconds):
   ```python
   session['last_write_timestamp'] = time.time()
   
   def get_db():
       if time.time() - session.get('last_write_timestamp', 0) < 5:
           return primary_db
       return replica_db
   ```
2. **LSN-Based Routing (Causal Consistency):** Store the commit LSN of the write in a client cookie. When querying the replica, ensure the replica has replayed up to that LSN (`pg_last_wal_replay_lsn() >= cookie_lsn`); if not, route to primary or wait.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.
