# Module_18_Distributed_Systems_Task_Queues_Streaming: Project Implementation Guide

**Deliverable:** a distributed streaming pipeline using Redis Streams, consumer groups, automatic dead-letter queue (DLQ) transitions, and idempotent processing.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_distributed_pipeline.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — In-Memory & Redis Stream Broker
Implement `DistributedPipelineBroker` abstract base class supporting `publish_event` and `ack_event`.

### Step 2 — Consumer Groups & Claiming
Implement consumer group polling with `XREADGROUP` and handle unacknowledged message claiming with `XAUTOCLAIM`.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_distributed_pipeline.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Dead Letter Queue (DLQ) Routing
Implement retry tracker inspecting message delivery attempts; upon reaching max retries, route to DLQ stream.

### Step 4 — Idempotent Worker Processing
Wrap task handlers with an idempotency store to prevent duplicate execution under message redelivery.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/distributed_pipeline.py`, remove the idempotency deduplication check in the worker task handler.
Run:
```bash
pytest ../project_solution/test_distributed_pipeline.py -k test_idempotent_event_handling -v
```
Watch the test fail when redelivered events double-execute, then restore the deduplication guard.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_distributed_pipeline.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Partitioned Stream Sharding:** Implement consistent hashing to partition events across multiple Redis stream keys.
2. **Backpressure Flow Control:** Dynamically throttle producer publication when consumer lag exceeds threshold.
3. **Poison Pill Isolation:** Quarantine unparseable malformed payloads directly to an error archive stream.
4. **Distributed Lock Heartbeat:** Add lease renewal to task worker locks to survive long-running processing jobs.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_stream_publish_and_consume` | Proves events publish to stream and consume across worker groups |
| `test_dlq_routing_on_max_retries` | Proves failing events transition to Dead Letter Queue |
| `test_idempotent_event_handling` | Proves redelivered tasks are not re-executed |
| `test_consumer_reconnection` | Proves consumers reconnect and resume reading from last acknowledged offset |
| `test_in_memory_broker_fallback` | Proves in-memory broker supports offline testing without live Redis |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain distributed delivery semantics (at-most-once, at-least-once, exactly-once)
- [ ] Use Redis Streams and consumer groups for scalable distributed event processing
- [ ] Implement Dead Letter Queues (DLQ) to isolate failing or poisoned messages
- [ ] Design idempotent task execution handlers using unique message identifiers
- [ ] Handle worker failures and claim abandoned messages using XAUTOCLAIM
- [ ] Test distributed pipelines using mock brokers and live Dockerized Redis
- [ ] Prevent race conditions and double-execution under network partition retries
