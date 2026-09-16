# Module 18: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Distributed Systems, Message Brokers, DLQs, and Idempotency before moving to **Module 17**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Decoupling:** Why should long-running operations (like generating 100-page PDF reports) never run directly inside an HTTP request handler?
2. **Broker Architecture:** What are the distinct responsibilities of a Producer, a Message Broker, and a Worker Consumer?
3. **Poison Pills:** What is a "Poison Pill" message, and what happens to a naive worker pool that does not implement DLQs?
4. **Dead-Letter Queues:** How does a Dead-Letter Queue (DLQ) protect production queues from infinite crash loops?
5. **Thundering Herds:** Why is adding random "Jitter" to exponential backoff retries critical during system recovery?
6. **Idempotency Defined:** What does it mean for a consumer event handler to be "idempotent"?
7. **Delivery Guarantees:** Compare "At-Most-Once", "At-Least-Once", and "Exactly-Once" message delivery semantics.
8. **Queue vs Stream:** What is the architectural difference between a point-to-point Task Queue (Celery/RabbitMQ) and an append-only Event Stream (Kafka)?
9. **Idempotency Keys:** How does a database unique constraint on `idempotency_key` prevent duplicate billing on network timeouts?
10. **Worker Acknowledgements:** What does a consumer `ACK` (Acknowledgement) vs `NACK` (Negative Acknowledgement) tell the broker?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
HTTP requests have strict timeout limits (e.g. 30s) and block client connections. Long tasks must be offloaded to background workers so the API can respond instantly with `202 Accepted` and a job ID.

#### Answer 2:
- **Producer:** Generates job instructions and enqueues them.
- **Broker:** Stores and routes message envelopes safely (Redis, RabbitMQ, Kafka).
- **Consumer:** Long-running background processes pulling jobs and computing results.

#### Answer 3:
A poison pill is a message with corrupt data that crashes the worker. Without DLQs, the broker constantly re-delivers the message, causing an infinite crash loop.

#### Answer 4:
It moves messages that fail $N$ consecutive processing attempts to a quarantined secondary queue for developer inspection without blocking new traffic.

#### Answer 5:
Jitter desynchronizes retry attempts, preventing thousands of failed workers from hammering a recovering database at the exact same millisecond.

#### Answer 6:
It guarantees that processing the exact same event multiple times (due to network retries) produces the identical system state as processing it once.

#### Answer 7:
- **At-Most-Once:** Messages are never duplicated, but may be lost.
- **At-Least-Once:** Messages are never lost, but may be delivered multiple times (requires idempotent consumers).
- **Exactly-Once:** Every message is delivered and processed once (requires complex distributed transactional coordinators).

#### Answer 8:
- **Task Queue:** Messages are deleted upon consumer acknowledgment.
- **Event Stream:** Messages are permanently appended to an immutable ordered log and can be replayed by multiple consumer groups.

#### Answer 9:
Attempting to insert a duplicate `idempotency_key` raises a unique key violation, allowing the handler to return the previous successful result instead of charging again.

#### Answer 10:
- `ACK`: Confirms successful processing; broker deletes/advances message.
- `NACK`: Rejects message; broker re-queues or diverts to DLQ.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Idempotent Event Deduplicator

**Goal:** Implement an `IdempotentProcessor` class that processes event dicts, caching processed event IDs to prevent duplicate execution.

<details>
<summary><b>Solution Code</b></summary>

```python
class IdempotentProcessor:
    def __init__(self) -> None:
        self.processed_ids: set[str] = set()

    def process(self, event_id: str, payload: dict) -> str:
        if event_id in self.processed_ids:
            return f"IGNORED_DUPLICATE: {event_id}"
        self.processed_ids.add(event_id)
        return f"PROCESSED: {event_id}"

# Verification:
proc = IdempotentProcessor()
print(proc.process("EVT-100", {"amount": 25.0}))  # PROCESSED
print(proc.process("EVT-100", {"amount": 25.0}))  # IGNORED_DUPLICATE
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Handler that is not idempotent

```python
def handle_payment(payload: dict) -> None:
    charge_card(payload["card"], payload["amount"])
    mark_order_paid(payload["order_id"])
```

**Observed symptom:** A worker crashes between the charge and the mark. After reclaim, the customer is charged twice.

**(a)** Why does at-least-once delivery make this a certainty rather than a risk?

**(b)** What makes a handler idempotent?

**(c)** Why is exactly-once delivery not the answer?

<details>
<summary><b>Show the diagnosis</b></summary>

Redis Streams (and SQS, and Kafka) guarantee **at-least-once** delivery: an unacknowledged message is redelivered. A crash between two side effects means the first one is replayed. Given enough messages this is not a risk, it is a scheduled event.

**Idempotent means** the second execution has no additional effect. Here: pass an **idempotency key** to the payment provider (every real one supports this), and make `mark_order_paid` a conditional update (`WHERE status != 'paid'`). Module 18's `Worker._process` also keeps a consumer-side `_processed_keys` set.

**Exactly-once does not exist** across a network with independent failure domains — you cannot atomically both acknowledge a message and commit a side effect in another system. What you can have is at-least-once delivery plus idempotent handlers, which produces the same *observable result*. That combination is the real answer, and it is why idempotency is a requirement rather than a nicety.

</details>

---

### D2. Visibility timeout below processing time

```python
broker.reclaim_stalled(consumer="worker-a", min_idle_ms=5_000)
# ... while the actual handler routinely takes 30 seconds
```

**Observed symptom:** Long jobs run two, three, four times concurrently. Output is duplicated and the database deadlocks.

**(a)** What does `min_idle_ms` actually mean?

**(b)** What is the correct way to size it?

**(c)** What if the processing time is unpredictable?

<details>
<summary><b>Show the diagnosis</b></summary>

`min_idle_ms` is how long a message may sit **unacknowledged** before another consumer may claim it. Set to 5 s while jobs take 30 s, every job is stolen roughly six times over — each thief also failing to finish in 5 s.

**Size it** above your p99 processing time with headroom: if p99 is 30 s, use 90–120 s. The trade-off is recovery latency — a genuinely crashed worker's message waits that long before being retried.

**Unpredictable durations:** extend the claim while working (a heartbeat that re-claims or touches the message periodically), which is what SQS's `ChangeMessageVisibility` and Celery's late-ack do. Alternatively split the job into bounded steps. Never solve it by making the timeout enormous — that destroys crash recovery.

</details>

---

### D3. Dead-lettered message left pending

```python
def dead_letter(self, job, error: str) -> None:
    self._client.xadd(self.dlq_stream, {"error": error, **job.to_wire()})
    # no XACK
```

**Observed symptom:** The poison message is copied to the DLQ, then reclaimed and dead-lettered again, forever. The DLQ grows without bound.

**(a)** What is missing, and why does the loop continue?

**(b)** Why must the ack come after the DLQ write, not before?

**(c)** What monitoring would have caught this in minutes?

<details>
<summary><b>Show the diagnosis</b></summary>

There is no `XACK`, so the message remains in the pending-entries list. It is reclaimed after the visibility timeout, fails again, and is appended to the DLQ again.

**Order matters:** write to the DLQ **first**, then ack. Acking first risks a crash in between, which loses the message entirely — and losing a poison message means losing the evidence of a bug. Duplicate DLQ entries are recoverable; a silently dropped payload is not.

**Monitoring:** alert on **DLQ depth rate of change**, not just depth. A DLQ that grows steadily with no new input is this bug exactly. Also alert on pending-entry age (`XPENDING`) — a message older than a few visibility timeouts is stuck, not slow.

</details>

---

### D4. Idempotency key from an unsorted dict

```python
def derive_key(task_type: str, payload: dict) -> str:
    return hashlib.sha256(f"{task_type}:{payload}".encode()).hexdigest()
```

**Observed symptom:** The same logical job is occasionally enqueued twice, and it correlates with which web server handled the request.

**(a)** Why do two identical payloads produce different keys?

**(b)** What is the fix?

**(c)** Why does the bug appear intermittent?

<details>
<summary><b>Show the diagnosis</b></summary>

`f"{payload}"` uses `dict.__repr__`, which reflects **insertion order**. `{'a':1,'b':2}` and `{'b':2,'a':1}` are equal dicts with different reprs, hence different hashes.

**Fix:** canonical serialisation —

```python
canonical = json.dumps({'t': task_type, 'p': payload}, sort_keys=True, separators=(',', ':'))
```

`sort_keys=True` makes the representation independent of construction order; the explicit `separators` removes whitespace variation.

**Intermittent because** insertion order depends on the code path that built the payload — a JSON body parsed by one framework, a form parsed by another, a retry constructing the dict in a different order. Same logical job, different key, no deduplication. Module 18's `derive_idempotency_key` and its test `test_idempotency_key_ignores_dict_ordering` pin this.

</details>

---

### D5. Retry without backoff or jitter

```python
for attempt in range(10):
    try:
        return call_upstream()
    except ConnectionError:
        continue        # immediate retry
```

**Observed symptom:** When the upstream service recovers from an outage, it immediately falls over again.

**(a)** Name the two distinct problems with this retry loop.

**(b)** What does jitter add beyond exponential backoff?

**(c)** What should you *not* retry?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two problems.** (1) No delay — ten retries complete in milliseconds, hammering a struggling service and turning a blip into an outage. (2) No jitter — every client retries on the same schedule.

**Jitter** breaks synchronisation. With pure exponential backoff, a thousand clients that failed at the same instant retry together at t=1s, t=2s, t=4s — a **thundering herd** that re-breaks the service the moment it recovers. Randomising each delay (`delay * random.uniform(0.5, 1.5)`, or full jitter) spreads the load smoothly.

**Do not retry:** anything non-idempotent without an idempotency key, and any **4xx** client error — a 400 or 403 will fail identically forever, so retrying wastes capacity and delays the real error reaching the caller. Retry timeouts, connection failures, 429s (respecting `Retry-After`) and 5xx.

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
