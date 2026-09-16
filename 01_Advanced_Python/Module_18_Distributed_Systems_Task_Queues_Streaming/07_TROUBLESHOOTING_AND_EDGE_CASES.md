# Module 18: Troubleshooting, Distributed Traps & Retry Storms

This reference guide details common distributed systems failures, poison pills, and idempotency hazards.

---

## 1. The Poison Pill Queue Blocker

### The Bug
A malformed message (corrupted JSON or missing field) crashes worker process. The broker re-enqueues the message at the head of the queue, crashing the next worker indefinitely!

### The Fix
Implement an explicit **Retry Threshold with Dead-Letter Queue (DLQ)**. After $N$ failures, divert the poisoned message into a dead-letter queue and acknowledge it from the main stream.

---

## 2. Retry Avalanches & Jitter

### The Problem
When a database goes down for 5 seconds, 10,000 workers fail simultaneously and all retry at the exact same moment ($t + 1s$), creating a massive thundering herd that keeps the database crashed forever.

### The Fix
Always use **Exponential Backoff with Random Jitter**:
$$\text{delay} = 2^{\text{attempt}} + \text{random.uniform}(0, 1)$$
