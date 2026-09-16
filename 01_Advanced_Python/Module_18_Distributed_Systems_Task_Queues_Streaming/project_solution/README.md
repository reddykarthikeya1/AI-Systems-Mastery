# Design Rationale: Distributed Stream Processing & Dead-Letter Queue Pipeline

## Architectural Overview
A resilient distributed task and event processing engine built on Redis Streams, consumer groups, automatic crashed-worker task recovery (`XCLAIM`), and Dead-Letter Queues (DLQ).

## Key Design Decisions
1. **Redis Streams with Consumer Groups:** Replaces naive lists with append-only streams, tracking pending messages in the Pending Entries List (PEL) until explicit acknowledgment (`XACK`).
2. **Poison Pill Dead-Letter Routing:** Tasks that fail repeatedly are automatically routed to a dead-letter queue, preventing broken payloads from crashing the worker fleet in infinite loops.
3. **Idempotency Keys via Atomic Checks:** Every message carries a unique idempotency UUID, converting at-least-once network delivery into effectively-once execution.

## Rejected Alternatives
1. **Naive Redis Lists with `LPUSH` and `RPOP`:**
   - *Reason for Rejection:* If a worker process is terminated or crashes while processing an `RPOP` task, the task is permanently lost with zero recovery mechanism.
2. **Unlimited Unbounded Retries Without Backoff:**
   - *Reason for Rejection:* Retrying failed tasks in tight loops hammers recovering databases and downstream APIs (the "thundering herd" problem).

## Invariants & Guarantees
- No message is dropped on worker crashes; pending tasks are claimable.
- Poison pill messages cannot stall healthy stream processing.

## Verification
```bash
pytest test_distributed_pipeline.py -v
```
